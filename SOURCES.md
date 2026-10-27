# Sources and acknowledgments · 출처

## Inspiration

The idea of writing interview answers incrementally was inspired by [deep-interview in aviz85/claude-skills-library](https://github.com/aviz85/claude-skills-library/blob/90bbc16773886226be46375bec52a910dbfcf711/plugins/deep-interview/skills/deep-interview/SKILL.md).

- Reference revision: `90bbc16773886226be46375bec52a910dbfcf711`.
- Consulted file: `plugins/deep-interview/skills/deep-interview/SKILL.md`.
- Consulted on: 2026-10-27.
- Upstream README labels the project MIT; a standalone LICENSE file was not present in the inspected tree and GitHub's license metadata was null.
- No upstream source files are bundled. This project's instructions and templates were written for the We Need To Talk interview protocol.

The protocol adds evidence-based challenges, explicit decision/assumption/issue records, decision replacement history, resumable sessions, and an implementation specification with a truthful readiness state.

## Audience framing and evaluations

[DreambigOu/ELI5](https://github.com/DreambigOu/ELI5/tree/a766623b062331fdde53467001379b4ddf3acc2f)
inspired audience-adaptive vocabulary/analogies/framing and assertion-based baseline-versus-skill evaluation.

- Reference revision: `a766623b062331fdde53467001379b4ddf3acc2f`.
- Consulted on: 2026-10-27; `skills/eli5/SKILL.md`, `eli5-workspace/evals.json`, `eli5-workspace/run-evals.py` and `LICENSE` inspected.
- Upstream license: [MIT](https://github.com/DreambigOu/ELI5/blob/a766623b062331fdde53467001379b4ddf3acc2f/LICENSE), copyright (c) 2026 as written upstream.
- No upstream source or artwork is bundled. Instructions, templates, cases and evaluator implementation were written independently here.
- This adaptation adds a reverse explanation probe, explicit analogy limits, three views of one canonical specification, and scripted multi-turn file evidence.
- The evaluator requires complete assertion IDs and real evidence quotations, preserves missing/unknown results, and reports percentage-point deltas only for complete pairs. It does not inherit or claim upstream performance results.

The Tri-Grill roles and playful “we need to talk” framing came from the project brief. They do not assert traits about a gender or require a romantic roleplay. No specific `grill-me` source was imported or bundled.

## Platform references

- [OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills): skill discovery and supported locations.
- [OpenAI — Package your plugin](https://developers.openai.com/plugins/build/plugins): Codex compatibility manifests and marketplace layout.
- [Claude Code — Plugin manifest reference](https://code.claude.com/docs/en/plugins-reference): plugin metadata and native validation.
- [Claude Code — Programmatic usage](https://code.claude.com/docs/en/headless) and [CLI reference](https://code.claude.com/docs/en/cli-reference): live evaluator flags, streaming output, structured judging and bare-mode authentication. Local CLI help checked on 2.1.118; no paid live evaluation performed.

## 한국어

답변을 받을 때마다 파일에 남기는 면담 아이디어는 위 `deep-interview`를 참고했습니다. 원본 소스 파일은 배포하지 않으며, 이 프로젝트의 지침과 템플릿은 별도로 작성했습니다.

We Need To Talk는 근거에 따른 질문, 결정·가정·쟁점의 구분, 결정 변경 이력, 세션 재개, 준비 상태를 명시하는 실행 명세를 더합니다. 원본 저장소의 라이선스 표기와 조회한 커밋은 위에 기록했습니다.

ELI5에서는 청중에 따라 설명을 조절하는 방식과 Assertion 기반 A/B 평가 아이디어를 참고했습니다.
원본 코드를 복사하지 않고 면담용 질문·문서 템플릿·다회차 평가기를 별도로 작성했습니다.
비유의 조건과 한계, 독자별 문서의 원본 일치, 채점 누락 시 비교 보류를 추가했으며 실측하지 않은 개선 수치를 주장하지 않습니다.
