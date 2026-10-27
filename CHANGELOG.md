# Changelog

## 0.2.0 — 2026-10-27

- Add `--mode gauntlet|vc|partner|security`. New sessions default to the Tri-Grill sequence: VC → Partner → Security.
- Track stage progress, mode switching, and targeted re-review when earlier decisions change.
- Add Readback Check for consequential choices whose practical effects remain unclear, while preserving informed delegation and the ability to decline a check.
- Record stage coverage and readback evidence in session, topic, and final-specification templates.
- Update the English and Korean guides. Pre-0.2 sessions without mode metadata resume as `partner`.

한국어: 세 모드와 연속 관문, 선택 결과의 이해 확인, 관문 재검토·재개 기록을 추가했습니다. 새 세션은 gauntlet로 시작하며 이전 세션의 기존 흐름은 유지합니다.

## 0.1.0 — 2026-10-27

- Initial skill, Codex and Claude Code packaging, bilingual READMEs, and installation/package checks.
