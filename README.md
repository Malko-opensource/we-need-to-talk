# We Need To Talk 🌶️

**Your spec said “it should just work.” We have follow-up questions.**

[English](README.md) · [한국어](README.ko.md)

![A nervous potato builder says “It should just work.” A potato interviewer replies “Define 'work'.”](docs/assets/we-need-to-talk.png)

[![Validate](https://github.com/Malko-opensource/we-need-to-talk/actions/workflows/validate.yml/badge.svg)](https://github.com/Malko-opensource/we-need-to-talk/actions/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**We Need To Talk** is an interview skill for **Codex and Claude Code**. Three interview perspectives challenge your scope, your architecture, and your failure handling. Decisions are written down after every answer, and important trade-offs get a quick understanding check when expectations are unclear. The result is a specification you can hand to an implementation agent.

Inspired by the Korean phrase **“오빠 나랑 이야기 좀 해”** — the ominous “we need to talk” — but aimed at the holes in your spec. Your dignity survives. “Make it scalable” might not.

## A small taste

> **You:** “Don't store drafts anywhere. Also restore them after a crash.”
>
> **Skill:** “Those requirements conflict. Where would the restored draft come from?”
>
> **You:** “Okay, save them locally. No server sync.”
>
> **Skill:** *Records the decision.* “How much typing can be lost if the process dies before the next save?”

This is an illustrative conversation. The skill uses your actual files and answers as evidence.

## What you get

- **Questions with receipts.** Relevant code, docs, and earlier decisions ground the interview. No repository? It says so.
- **A record after every answer.** Decisions, assumptions, open issues, and sources stay in Markdown files.
- **Trade-offs with actual costs.** Options explain what you gain and give up, without invented estimates.
- **Changeable decisions.** Changed requirements supersede old decisions; history stays readable.
- **An honest handoff.** Unresolved blockers produce an `incomplete` spec, not a pretend agreement.
- **Pause and resume.** Continue from the saved files instead of relying on a long chat history.
- **“Did that actually make sense?”** Check an important consequence before treating a vague “just do it” as a settled decision.

No bundled server, API key, or additional service is required. You still need a working Codex or Claude Code setup with file access.

## Choose your interviewer

**The Tri-Grill Protocol** defaults to `--mode gauntlet`: **VC → Partner → Security**. One agent changes perspective while keeping the same decision record.

| Mode | The question behind the questions | What it settles |
| --- | --- | --- |
| `vc` · Scope Guillotine | “Does all of this need to ship now?” | User value, minimum scope, exclusions, success criteria |
| `partner` · Consistency Grill | “That isn't what your existing code says.” | Interfaces, state ownership, contracts, contradictions |
| `security` · Catastrophe Drill | “What happens when the process dies?” | Failure behavior, trust boundaries, recovery responsibility |
| `gauntlet` · All three | “First trim it. Then align it. Then break the assumptions.” | All three perspectives, in order |

Each stage can take several exchanges. Existing evidence can settle a stage without redundant questions. If a later decision changes an earlier assumption, only the affected stages reopen. A single mode records what it covered and what it left unreviewed.

`security` is a design interview about failures and trust boundaries. It does not perform a security audit or penetration test. `vc` applies to hobby projects and internal tools too; it does not require a business model.

```text
$we-need-to-talk My writing app --mode gauntlet --spiciness spicy
$we-need-to-talk Trim this MVP --mode vc
$we-need-to-talk Check the existing state-management design --mode partner
$we-need-to-talk Review retry and crash behavior --mode security --spiciness hell
```

## Pick your heat

| Mode | Interview style | Typical exploration budget |
| --- | --- | --- |
| 🌱 `mild` | A calm senior asking about the biggest gaps | ~3–4 rounds |
| 🌶️ `spicy` | A lead who wants concrete costs and failure behavior | ~5–7 rounds |
| 🔥 `hell` | Every assumption meets a counterexample | ~8–12 rounds |

`spicy` is the default. These budgets cover the **whole interview**, including all three gauntlet stages. They are guidelines, not quotas. Every mode asks only **1–2 questions at a time**. You can change your mind, defer a decision, lower the heat, or stop.

## “Wait. Did you understand what I just said?”

Saying “go with your recommendation” can mean informed delegation—or a trade-off that never quite landed. **Readback Check** looks at the actual decision and earlier answers before deciding whether to ask.

> **Skill:** “Keeping drafts only in memory is simpler, but a restart loses them.”
>
> **You:** “Sure, just do it.”
>
> **Skill:** “One quick check: if the app closes before you save, what happens to the draft?”
>
> **You:** “It disappears. That's okay for v1.”
>
> **Skill:** *Records the accepted consequence and moves on.*

The playful Korean version is **“오빠, 내가 한 말 이해한 거 맞아?”** The useful part is the concrete scenario that follows it. If the answer is “but it still comes back, right?”, the misunderstanding becomes an open issue instead of a false agreement.

The check is for consequential, unclear choices. It skips small implementation details and trade-offs you've already acknowledged. You can ask for an explanation, delegate the decision, or decline the check. It does not grade your knowledge or require repeated approval.

## Install

### Codex — standalone skill

With Git and Python 3.10 or later:

```sh
git clone https://github.com/Malko-opensource/we-need-to-talk.git
cd we-need-to-talk
python3 scripts/install.py codex
```

The installer copies the skill to `${CODEX_HOME:-~/.codex}/skills/we-need-to-talk` and refuses to overwrite a different installation. Start a new chat and invoke:

```text
$we-need-to-talk A notes app that restores drafts after a restart --spiciness spicy
```

If your Codex setup uses `~/.agents/skills`, choose that directory explicitly:

```sh
python3 scripts/install.py codex --skills-dir "$HOME/.agents/skills"
```

Use one installation location. [OpenAI's skill documentation](https://learn.chatgpt.com/docs/build-skills) describes current discovery paths; older/local builds can differ.

### Claude Code — plugin

In Claude Code, add the marketplace and install:

```text
/plugin marketplace add Malko-opensource/we-need-to-talk
/plugin install we-need-to-talk@we-need-to-talk
```

Then invoke:

```text
/we-need-to-talk:we-need-to-talk A notes app that restores drafts --spiciness spicy
```

For a local checkout, you can load the plugin directly:

```sh
claude --plugin-dir ./plugins/we-need-to-talk
```

Or install it as a standalone Claude skill with `python3 scripts/install.py claude` and invoke `/we-need-to-talk`. Choose either the plugin or the standalone skill to avoid duplicates.

### Codex — plugin alternative

The repository includes a Codex marketplace too:

```sh
codex plugin marketplace add Malko-opensource/we-need-to-talk
```

Install **We Need To Talk** from that marketplace in the app. See [OpenAI's plugin guide](https://developers.openai.com/plugins/build/plugins) for the installation flow supported by your version.

## Use it

### 1. Bring a topic

```text
$we-need-to-talk A local-first writing app. Challenge the requirements before we code.
```

The skill inspects the relevant project context, creates a session index, and asks about the most consequential missing decision. It follows your language; ask in Korean for a Korean interview and documents.

### 2. Make the trade-offs

```text
Keep drafts on this device. No accounts or cloud sync for v1.
```

The answer is saved before the next question. Ask for a recommendation when you need one. “You decide” is recorded as delegation, not misquoted as your direct choice.

### 3. Choose a folder or turn up the heat

```text
$we-need-to-talk Cancellation and timeout behavior --mode security --spiciness hell --output ./docs/specs/cancellation
```

| Input | Meaning |
| --- | --- |
| Topic | What to interview you about; existing conversation context can supply it |
| `--mode gauntlet\|vc\|partner\|security` | Interview perspective; defaults to `gauntlet` for new sessions |
| `--spiciness mild\|spicy\|hell` | Interview intensity; defaults to `spicy` |
| `--output <path>` | A new session directory |
| `--resume <path>` | Continue with the saved mode, stage, and intensity unless overridden |

These are arguments interpreted by the skill inside your coding agent, not a separate terminal command.

### 4. Pause, resume, or finish

```text
Pause here. We'll decide the sync policy later.
```

```text
$we-need-to-talk --resume ./docs/specs/cancellation
```

```text
Write the final specification now and keep the unresolved items visible.
```

The output status tells you whether the spec is ready for implementation. A request for an interview does not itself authorize implementation or deployment.

Switch perspective mid-session with “let's only review failure handling now” or `--mode security`. Resuming a pre-0.2 session without mode metadata preserves its previous flow as `partner`; it does not silently restart the three-stage gauntlet.

## What lands on disk

```text
docs/specs/notes-app-2026-10-27/
├── _session-index.md       # Mode, stage progress, evidence, open issues, resume point
├── draft-storage.md        # Decisions, readback evidence, interview history
├── recovery-policy.md
├── _final-contract.md      # Consolidated implementation specification
└── _deferred-risks.md       # Created only when something is deferred
```

Without `--output`, sessions go under the project's `docs/specs/`, or `~/Documents/interviews/` when there is no project. Files appear as they become useful.

| ID / state | Meaning |
| --- | --- |
| `D-*` / `A-*` / `Q-*` | Decision / assumption / open issue |
| `E-*` / `R-*` | Evidence / interview round |
| `superseded` | A decision was replaced; its history remains |
| `ready` | The specification has the required decisions and acceptance criteria |
| `incomplete` | An implementation-blocking decision is still missing |
| `paused` | The user stopped the interview for now |
| `stale` | An existing final specification needs updating after a change |

Stage progress is tracked separately: `pending`, `active`, `complete`, `deferred`, `needs-review`, or `not-reviewed`. Completing the VC stage does not make the entire implementation specification ready.

`ready` describes the specification, not implemented or tested software. The skill gives the agent a workflow; it is not a separate engine that enforces every file write.

## Under the hood

```mermaid
flowchart LR
    A["Pre-audit<br/>Read the evidence"] --> V["VC<br/>Trim the scope"]
    V --> P["Partner<br/>Resolve contradictions"]
    P --> S["Security<br/>Define failure behavior"]
    S --> F["Final specification<br/>Ready or incomplete"]
    S -. Changed earlier assumptions .-> V
```

Inside each stage: **AUDIT → CONFRONT → LOCK → DRILL**. Readback Check fits into that loop when a consequential choice is unclear; it is not a fourth mandatory stage.

The portable skill lives in [`plugins/we-need-to-talk/skills/we-need-to-talk`](plugins/we-need-to-talk/skills/we-need-to-talk). Both plugin manifests point to the same instructions and templates.

## Update, uninstall, and troubleshoot

- **Updating:** pull this repository and rerun the installer. An identical installation is left alone; a different one requires `--backup-existing`. Backups go under `.we-need-to-talk-backups/` beside the skill.
- **Not in the selector:** open a new chat, check the skill directory your agent scans, and avoid installing the same skill through multiple routes.
- **File writes unavailable:** the agent should report that and provide an unsaved draft, rather than claim persistence.
- **Uninstalling a standalone skill:** remove only its `we-need-to-talk` directory from the location printed by the installer. Your interview output stays in its own directory.

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for local checks, packaging, and useful behavior reports. Translation improvements and realistic interview examples are welcome.

Format validation, packaging checks, and local skill discovery have been checked. Broad multi-round behavior across models remains an area for testing.

## Credits and license

Created by [Malko](https://github.com/Malko-opensource). The incremental interview idea was inspired by [`deep-interview`](https://github.com/aviz85/claude-skills-library/tree/90bbc16773886226be46375bec52a910dbfcf711/plugins/deep-interview). See [SOURCES.md](SOURCES.md) for attribution.

[MIT](LICENSE). The README illustration was generated with OpenAI's built-in image-generation tool; its prompt is in [docs/assets/PROVENANCE.md](docs/assets/PROVENANCE.md).
