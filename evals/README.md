# Interview evaluations

[English](README.md) · [한국어](README.ko.md)

Compare **baseline** and **with_skill** using the same scripted user turns, model,
tools, and assertions. This is an independently written harness inspired by
[DreambigOu/ELI5](https://github.com/DreambigOu/ELI5); see [source notes](../SOURCES.md).

**No benchmark result is claimed yet.** Offline tests validate orchestration, parsing,
file evidence and scoring. The live Claude adapter has not been exercised against a paid model.

## Start without calling a model

Requires Python 3.10+. The evaluator itself uses only the standard library.

```sh
python3 scripts/run-evals.py
python3 scripts/run-evals.py --case jargon-probe --repeats 3 --seed 42
python3 -m unittest discover -s tests -v
```

Without `--live`, the command only validates cases and prints the experiment plan.
It does not launch Claude, contact a provider, or write run artifacts.

## Run an actual comparison

Requires Claude Code with the flags used by the adapter (local help checked on 2.1.118)
and API/provider credentials in the environment. `--bare` does not use your subscription
OAuth login or keychain; see the official
[programmatic usage guide](https://code.claude.com/docs/en/headless).
Use a pinned model ID supported by your provider, not a moving alias.

```sh
python3 scripts/run-evals.py --live \
  --model YOUR_PINNED_MODEL_ID \
  --case jargon-probe --repeats 3 --seed 42 \
  --budget-usd 5 --timeout 180
```

This makes billable model calls, including judging. `--judge-model` optionally pins a
different judge; otherwise the same model is used. The budget is shared across calls
using reported costs and the CLI's per-call budget option. It is **not** a provider
spending limit: a timed-out or failed call may incur unreported charges. The harness stops
after the first execution/grading error or exhausted budget. Partial runs produce no delta.
There is no automatic retry or resume that could silently spend more.

Use disposable environments and nonsensitive cases. Temporary working directories and
restricted tools reduce accidental interference but are **not an OS sandbox**.
The adapter allows only Read, Write, Edit, Glob and Grep during interviews, and no tools
during judging. It disables native skills, slash commands, discovered settings and MCP servers.
Each call gets a fresh configuration directory; environment provider configuration and
organization policy can still affect behavior. Nothing in the harness logs your environment.

## What is compared

[`evals.json`](evals.json) contains six cases:

| Case | What it checks |
| --- | --- |
| vague-agent-spec | Clarification, question budget, recording, no false readiness |
| jargon-probe | Plain-language flow, helpful teaching, accurate analogy |
| memory-tradeoff | Audience framing and a consequential misunderstanding |
| informed-delegation | No repeated quiz after informed delegation and a stop request |
| multi-audience | Canonical spec plus three consistent, truthful views |
| deferred-blocker | Visible blockers, incomplete status and a respectful stop |

The generic assistant system prompt and user turns are identical between arms.
Only the treatment receives a copy of the skill and an instruction to read it.
Each case, repeat and arm gets a fresh directory outside the repository.
The baseline cannot discover this repository's installed skill through the current directory.
Order is randomized with a recorded seed. Models are configured identically across arms;
provider nondeterminism is not eliminated.

This is **scripted-turn replay**, not a simulated human or native resumed chat.
Every invocation receives the previous user/assistant text; workspace files persist.
Fixed follow-up answers can fit one response better than another. Inspect transcripts and
use real interviews before generalizing. Codex behavior is not evaluated by this Claude adapter.

## Assertions and evidence

- `file_exists`: a nonempty artifact actually exists at the expected path.
- `updates_after_reply`: at least one Markdown artifact changes by the end of each follow-up turn.
  This alone does **not** prove that writing preceded the next question.
- `contract_consistency`: all four documents share explicit `source_revision` and `spec_status`
  frontmatter. Allowed canonical states are ready, incomplete and paused. This is a metadata check;
  semantic consistency is separately judged.
- `judge`: a model grades the assertion as pass, fail or unknown and quotes real response,
  tool-event or artifact evidence. Missing, duplicate or unknown IDs, invented quotes,
  malformed responses and execution errors invalidate the comparison.

The judge gets assertions, user turns and evidence without arm labels. Interview wording
may reveal the treatment, so this is not a fully blinded evaluation. Evidence references
validate that a quote exists, not that the judge's reasoning is correct. Audit the grades.

No metric silently drops missing assertions. Both pass rates and the delta stay null unless
every expected result has a pass/fail grade. Coverage remains available for debugging.
A delta is **percentage points of these assertion pass rates**, not a percentage of hidden
requirements discovered, time saved, or a general improvement claim. Repeated trials are not
statistical confidence intervals.

## Output

Runs default to ignored `evals/runs/<UTC timestamp>/`; `--output` selects a new directory.
Existing output directories are refused.

```text
run.json                 # Seed, order, requested models, CLI version, hashes, timestamps
cases.json               # Exact selected cases
skill-source/            # Frozen treatment source
001-.../turn-1.jsonl      # Raw CLI events; resolved model information when supplied by CLI
001-.../turn-1.json       # Response and file contents/hashes at end of turn
001-.../judge.jsonl       # Judge evidence
results.json             # Per-assertion verdicts and cited evidence
summary.json             # Coverage, pass rates/delta or incomplete, reported cost
```

Raw stderr is retained beside each invocation. Workspaces are removed after collection.
Snapshots reject symlinks, non-UTF-8 and oversized output rather than silently dropping evidence.
Keep local logs private until reviewed; prompts and generated files may contain sensitive context.

## Add a case

Add fixed `turns` and uniquely identified `assertions` to `evals.json`.
Keep each assertion observable and decision-relevant. Include both desirable behavior and
counterexamples such as informed delegation, refusal to explain, or unresolved blockers.
Do not add a “must be spicy” assertion that rewards insults or verbosity.
CI only runs the offline plan and unit tests; it never performs a live evaluation.
