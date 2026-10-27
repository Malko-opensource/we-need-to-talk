# Contributing · 기여 안내

English and Korean contributions are welcome. 한국어로 이슈와 PR을 작성해도 좋습니다.

## Local checks

Python 3.10+ is required. Installation and packaging use only the standard library; the metadata checker also uses PyYAML.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/check.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/run-evals.py
.venv/bin/python scripts/package.py
```

On Windows, use `.venv\Scripts\python.exe` instead. Generated archives and checksums appear in `dist/`.

With Claude Code installed, validate the plugin and marketplace with the native parser:

```sh
claude plugin validate ./plugins/we-need-to-talk
claude plugin validate .
```

## Editing the skill

- Keep one canonical skill under `plugins/we-need-to-talk/skills/we-need-to-talk`.
- Keep `README.md` and `README.ko.md` aligned when options or behavior change.
- Keep the two plugin versions and metadata aligned.
- Preserve the core behavior: read relevant evidence, ask 1–2 questions, save each answer, expose unresolved decisions.
- Intensity changes the depth of scrutiny. It must not remove the user's ability to revise, defer, or stop.
- Templates are starting structures. Session language should follow the user while IDs, filenames, and state tokens remain stable.
- Keep interview mode (`gauntlet`, `vc`, `partner`, `security`) independent from intensity. Track stage coverage separately from specification readiness.
- Readback checks concern the consequence of a decision. Preserve informed delegation, avoid repeated checks, and never turn them into knowledge scores or extra permission gates.
- Feynman probes clarify unspecified flows. Analogies must map back to the system and preserve constraints; teach when asked instead of forcing repeated quizzes.
- Audience views must retain the canonical revision, state, decision IDs and material blockers. Never invent dates, schemas or approved UI copy to fill a template.

## Useful behavior reports

Format and package checks cannot prove interview quality. For an interview report, include the agent/model version, the language and intensity, the smallest reproducible prompt, and the observed file changes. Remove private data and credentials before sharing.

Useful scenarios include a project with no existing code, a decision reversal, an unresolved contradiction, a deferred blocker, a write failure, resuming after an interrupted write, and an English-language session using the Korean templates.

For Tri-Grill, also try switching between single and gauntlet modes, resuming a pre-0.2 session, and a Security decision that invalidates earlier scope. For Readback Check, compare a first vague acceptance of a major trade-off, an already acknowledged consequence, a misunderstanding, and a user who declines the check and delegates instead.

Separate observations from expectations: “the index was not updated after R-003” is more useful than “persistence is broken.” Do not claim a simulation is a real model run.

See the [evaluation guide](evals/README.md) ([한국어](evals/README.ko.md)) for cases, offline checks and explicitly opted-in live comparisons. Preserve transcripts and audit judge quotations. Unit tests use synthetic results and do not establish a skill-quality benchmark.

## 한국어 요약

설치기는 표준 라이브러리만 사용하며, 검사용으로 PyYAML을 설치합니다. 위 명령으로 포맷·링크·설치·패키징을 검사할 수 있습니다.

옵션이나 동작이 바뀌면 두 언어 README와 플러그인 메타데이터도 함께 수정해주세요. 면담 문제를 제보할 때는 에이전트·모델 버전, 강도, 재현 입력, 실제로 저장된 내용을 적어주세요. 개인 정보와 비밀키는 제거하고, 기대한 동작과 관찰한 결과를 구별해주세요.
