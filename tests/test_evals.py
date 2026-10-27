"""Offline evaluator checks. Synthetic results do not measure skill quality."""
from contextlib import redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import eval_runner as ev


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.cases = ev.load_cases(ev.ROOT / "evals/evals.json")

    def test_default_plan_does_not_invoke_any_process(self):
        with patch.object(ev.subprocess, "run", side_effect=AssertionError("No process allowed")):
            with redirect_stdout(io.StringIO()) as output:
                self.assertEqual(ev.main([]), 0)
        plan = json.loads(output.getvalue())
        self.assertEqual(plan["mode"], "offline-plan")
        self.assertEqual(len(plan["plan"]), len(self.cases) * 2)
        self.assertTrue(all({r["arm"] for r in plan["plan"] if r["case"] == c["id"]}
                            == set(ev.ARMS) for c in self.cases))

    def test_duplicate_cases_and_unsafe_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "cases.json"
            for cases in ([self.cases[0], self.cases[0]],
                          [{"id": "unsafe", "turns": ["x"], "assertions": [
                              {"id": "escape", "kind": "file_exists", "path": "output/../../secret"}]}]):
                ev.dump(path, {"schema_version": 1, "method": "scripted-turn-replay", "cases": cases})
                with self.assertRaises(ValueError):
                    ev.load_cases(path)

    def test_stream_rejects_errors_missing_results_and_unknown_cost(self):
        success = {"type": "result", "subtype": "success", "is_error": False,
                   "result": "answer", "total_cost_usd": 0.05}
        self.assertEqual(ev.parse_stream(json.dumps(success))[1]["result"], "answer")
        for data in ("not-json", "[]", "", json.dumps(success) + "\n" + json.dumps(success),
                     json.dumps({**success, "is_error": True}),
                     json.dumps({**success, "total_cost_usd": None}),
                     json.dumps({**success, "total_cost_usd": float("nan")})):
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    ev.parse_stream(data)

    def test_judge_cannot_omit_duplicate_invent_ids_or_evidence(self):
        row = {"id": "a", "verdict": "pass", "evidence_ref": "T1.response",
               "quote": "observed", "reason": "Recorded evidence"}
        evidence = {"T1.response": "actually observed text"}
        self.assertIn("a", ev.validate_grades({"grades": [row]}, {"a"}, evidence))
        for rows in ([], [row, row], [{**row, "id": "invented"}],
                     [{**row, "quote": "not in evidence"}],
                     [{**row, "evidence_ref": "missing"}],
                     [{**row, "verdict": "maybe"}]):
            with self.subTest(rows=rows):
                with self.assertRaises(ValueError):
                    ev.validate_grades({"grades": rows}, {"a"}, evidence)

    def test_snapshot_checks_real_changes_and_rejects_links(self):
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder)
            (work / "output").mkdir()
            path = work / "output/index.md"
            path.write_text("first")
            first = {"artifacts": ev.snapshot(work)}
            item = {"id": "save", "kind": "updates_after_reply"}
            self.assertEqual(ev.deterministic(item, [first, first])["verdict"], "fail")
            path.write_text("first\nnew answer")
            second = {"artifacts": ev.snapshot(work)}
            self.assertEqual(ev.deterministic(item, [first, second])["verdict"], "pass")
            (work / "output/link").symlink_to(work / "output/index.md")
            with self.assertRaises(ValueError):
                ev.snapshot(work)

    def test_contracts_require_matching_revision_and_state(self):
        text = '---\nsource_revision: "1"\nspec_status: incomplete\n---\nD-001'
        files = {p: {"text": text} for p in ev.CONTRACTS}
        item = {"id": "bundle", "kind": "contract_consistency"}
        self.assertEqual(ev.deterministic(item, [{"artifacts": files}])["verdict"], "pass")
        files[ev.CONTRACTS[1]] = {"text": text.replace("incomplete", "ready")}
        self.assertEqual(ev.deterministic(item, [{"artifacts": files}])["verdict"], "fail")
        files[ev.CONTRACTS[1]] = {"text": text.replace('"1"', '"2"')}
        self.assertEqual(ev.deterministic(item, [{"artifacts": files}])["verdict"], "fail")

    def test_missing_unknown_and_duplicate_results_suppress_delta(self):
        cases = [{"id": "toy", "assertions": [{"id": "a"}, {"id": "b"}]}]
        results = [{"case": "toy", "repeat": 1, "arm": arm, "status": "complete",
                    "grades": {"a": {"verdict": "pass"}, "b": {"verdict": verdict}}}
                   for arm, verdict in (("baseline", "fail"), ("with_skill", "pass"))]
        summary = ev.summarize(cases, 1, results)
        self.assertEqual(summary["delta_percentage_points"], 50.0)
        incomplete = deepcopy(results)
        incomplete[1]["grades"]["b"]["verdict"] = "unknown"
        for items in (results[:1], incomplete, results + results[:1]):
            with self.subTest(items=items):
                score = ev.summarize(cases, 1, items)
                self.assertEqual(score["status"], "incomplete")
                self.assertIsNone(score["delta_percentage_points"])
                self.assertIsNone(score["arms"]["baseline"]["pass_rate"])

    def test_live_requires_explicit_model_and_budget_before_adapter(self):
        with patch.object(ev, "ClaudeAdapter", side_effect=AssertionError("Not authorized")):
            with self.assertRaises(SystemExit):
                ev.main(["--live"])

    def test_scripted_pair_preserves_evidence_and_isolates_skill(self):
        calls = []

        class FakeAdapter:
            version = "synthetic-cli"
            spent = 0.0

            def __init__(self, *args):
                pass

            def call(self, prompt, workspace, log_path, judge=False):
                calls.append((workspace, judge, (workspace / ".skill").exists()))
                log_path.write_text('{"fixture": true}\n')
                self.spent += 0.01
                if judge:
                    request = json.loads(prompt)
                    ref = "T1.response"
                    return [], {"result": "", "structured_output": {"grades": [
                        {"id": a["id"], "verdict": "pass", "evidence_ref": ref,
                         "quote": request["evidence"][ref], "reason": "Synthetic test grade"}
                        for a in request["assertions"]]}}
                out = workspace / "output"
                out.mkdir(exist_ok=True)
                index = out / "_session-index.md"
                index.write_text((index.read_text() if index.exists() else "") + "record\n")
                for file in ev.CONTRACTS:
                    target = workspace / file
                    target.parent.mkdir(exist_ok=True)
                    target.write_text('---\nsource_revision: "1"\nspec_status: incomplete\n---\nD-001')
                return [], {"result": "synthetic response"}

        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "run"
            with patch.object(ev, "ClaudeAdapter", FakeAdapter), redirect_stdout(io.StringIO()):
                status = ev.main(["--live", "--model", "fixture-model", "--budget-usd", "1",
                                  "--case", "vague-agent-spec", "--output", str(output)])
            self.assertEqual(status, 0)
            summary = json.loads((output / "summary.json").read_text())
            self.assertEqual(summary["delta_percentage_points"], 0.0)
            self.assertTrue((output / "skill-source/SKILL.md").exists())
            self.assertEqual(len(list(output.glob("*/turn-*.json"))), 4)
            interviews = [x for x in calls if not x[1]]
            self.assertEqual(sum(x[2] for x in interviews), 2)
            self.assertEqual(len({x[0] for x in interviews}), 2)
            self.assertTrue(all(not x[2] for x in calls if x[1]))

    def test_cli_adapter_limits_tools_and_carries_remaining_budget(self):
        import subprocess
        result = {"type": "result", "subtype": "success", "is_error": False,
                  "total_cost_usd": 0.04, "result": "response"}
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            (base / "config").mkdir()
            with patch.object(ev.subprocess, "run", side_effect=[
                subprocess.CompletedProcess([], 0, "test-version", ""),
                subprocess.CompletedProcess([], 0, json.dumps(result), ""),
                subprocess.CompletedProcess([], 0, json.dumps(result), ""),
            ]) as run:
                adapter = ev.ClaudeAdapter("claude", "model", "judge-model", 0.09, 30, base / "config")
                adapter.call("interview", base, base / "one.jsonl")
                adapter.call("judge", base, base / "two.jsonl", judge=True)
                cmd = run.call_args_list[1].args[0]
                judge = run.call_args_list[2].args[0]
                self.assertIn("--bare", cmd)
                self.assertIn("--disable-slash-commands", cmd)
                self.assertEqual(cmd[cmd.index("--tools") + 1], "Read,Write,Edit,Glob,Grep")
                self.assertEqual(judge[judge.index("--tools") + 1], "")
                self.assertEqual(judge[judge.index("--model") + 1], "judge-model")
                self.assertAlmostEqual(float(judge[judge.index("--max-budget-usd") + 1]), 0.05)
                self.assertEqual(run.call_args_list[1].kwargs["timeout"], 30)
                self.assertNotEqual(run.call_args_list[1].kwargs["env"]["CLAUDE_CONFIG_DIR"],
                                    run.call_args_list[2].kwargs["env"]["CLAUDE_CONFIG_DIR"])

    def test_execution_error_stops_run_and_preserves_incomplete_summary(self):
        calls = []

        class BrokenAdapter:
            version = "synthetic-cli"
            spent = 0.0

            def __init__(self, *args):
                pass

            def call(self, *args, **kwargs):
                calls.append(args)
                raise ValueError("synthetic failure")

        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "run"
            with patch.object(ev, "ClaudeAdapter", BrokenAdapter), redirect_stdout(io.StringIO()):
                code = ev.main(["--live", "--model", "fixture", "--budget-usd", "1",
                                "--output", str(output)])
            self.assertEqual(code, 1)
            self.assertEqual(len(calls), 1)
            score = json.loads((output / "summary.json").read_text())
            self.assertEqual(score["status"], "incomplete")
            self.assertIsNone(score["delta_percentage_points"])


if __name__ == "__main__":
    unittest.main()
