# Changelog

## 0.3.1 — 2026-10-27

- Limit write verification to changed sections and associated index fields; reuse unchanged instructions already in context.
- Resume from current state and relevant decision IDs before retrieving historical detail, and avoid scanning unrelated generated output.
- Keep the session index concise; clarify that audience documents are generated at handoff, not on every answer.
- Document the unconfirmed Claude memory-growth report and the evidence needed to distinguish process RAM from context growth. This is a context-amplification mitigation, not a verified memory-leak fix.

한국어: 누적 기록의 반복 읽기를 줄이는 완화 조치를 추가했습니다. Claude 메모리 증가 제보의 원인·해결 여부는 아직 미확인입니다.

## 0.3.0 — 2026-10-27

- Add Feynman Probe and audience-adaptive framing without turning jargon or delegation into a knowledge test.
- Add `--audience` and `--contracts all|none`; new sessions default to three audience handoffs, while older sessions keep their existing output scope.
- Keep engineer, manager and designer documents aligned with the canonical revision, decision IDs, unresolved issues and readiness state.
- Add six scripted A/B cases, an opt-in Claude evaluator, file evidence, strict assertion grading and offline tests. No live performance improvement is claimed.
- Add eight original potato feature illustrations and matching Korean/English guides.

한국어: 쉬운 말로 흐름 확인, 청중 맞춤 비유, 독자별 명세 3종, 근거를 보존하는 A/B 평가 도구와 기능별 감자 이미지 8종을 추가했습니다.

## 0.2.0 — 2026-10-27

- Add `--mode gauntlet|vc|partner|security`. New sessions default to the Tri-Grill sequence: VC → Partner → Security.
- Track stage progress, mode switching, and targeted re-review when earlier decisions change.
- Add Readback Check for consequential choices whose practical effects remain unclear, while preserving informed delegation and the ability to decline a check.
- Record stage coverage and readback evidence in session, topic, and final-specification templates.
- Update the English and Korean guides. Pre-0.2 sessions without mode metadata resume as `partner`.

한국어: 세 모드와 연속 관문, 선택 결과의 이해 확인, 관문 재검토·재개 기록을 추가했습니다. 새 세션은 gauntlet로 시작하며 이전 세션의 기존 흐름은 유지합니다.

## 0.1.0 — 2026-10-27

- Initial skill, Codex and Claude Code packaging, bilingual READMEs, and installation/package checks.
