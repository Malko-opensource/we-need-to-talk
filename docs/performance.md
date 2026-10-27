# Memory growth investigation · 메모리 증가 조사

## Status · 현재 상태

A user report relayed on 2026-10-27 says memory increased substantially while using the skill in “Claude.”
The exact product (Code, desktop or web), version, process, memory metric, starting/peak values,
session length and reproduction steps are unknown. **The reported RAM increase has not been reproduced.
Its cause and whether 0.3.1 improves it remain unverified.**

2026-10-27에 “Claude에서 스킬 사용 중 메모리가 크게 늘었다”는 간접 제보를 받았습니다.
정확한 제품·버전·프로세스·측정값·발생 회차는 아직 없습니다.
**RAM 증가를 재현하지 않았으며 원인과 0.3.1의 개선 여부도 미확인입니다.**

## Source findings · 소스에서 확인한 것

At revision [841af74](https://github.com/Malko-opensource/we-need-to-talk/commit/841af7440ab06d6c9dbb55e24bebf4f10dde2a86), version 0.3.0:

| Observation / 관찰 | Boundary / 해석 범위 |
| --- | --- |
| LOCK asked the agent to reread related files after every answer. / 답변마다 관련 파일 재읽기 | Could be interpreted as rereading growing files in full. No affected-session trace confirms this happened. / 누적 파일 전체 읽기로 해석될 수 있으나 실제 실행 기록은 없음 |
| Resume asked for the index, linked themes and final spec. / 재개 시 인덱스·연결 테마·최종 명세 읽기 | No explicit limit to relevant sections. / 필요한 구역으로 제한하는 규칙이 없었음 |
| SKILL.md: 20,165 UTF-8 bytes. Plugin ZIP: 31,540 bytes; 59,627 uncompressed bytes, 18 files. / 스킬·패키지 크기 | Source/archive sizes, **not process RAM**. / 이 수치가 실행 메모리 사용량을 뜻하지 않음 |
| No images in the plugin ZIP; README PNGs total 25,110,957 bytes in the repository. / 패키지에 이미지 없음 | README loading is a separate concern. A host may still read repository files if instructed to. / README 로딩과 별개이며 에이전트가 저장소 그림을 따로 열 가능성까지 배제하지 않음 |
| The distributed skill contains instructions/templates, not a background service. / 상주 서비스 없음 | A text workflow can still induce costly host/tool behavior. / 지침에 따른 도구 사용이 무거워질 가능성은 있음 |

Claude Code's documentation explains that the conversation, tool results and file contents consume
context. That supports investigating repeated reads; it does **not** establish a relationship
between token counts and this user's OS memory measurements.
See [how Claude Code works](https://code.claude.com/docs/en/how-claude-code-works)
and [context/cost management](https://code.claude.com/docs/en/costs).

공식 문서는 대화·도구 결과·파일 내용이 컨텍스트를 차지한다고 설명합니다.
반복 읽기를 조사할 근거는 되지만, 토큰 증가를 이 제보의 OS 메모리 증가 원인으로 확정할 근거는 아닙니다.

## Mitigation in 0.3.1 · 완화 조치

- Reuse unchanged instructions already in the conversation. / 이미 읽은 변경 없는 지침 재사용.
- Read changed sections and relevant index fields to verify writes. / 저장 확인은 변경 구역·관련 인덱스 항목으로 제한.
- Resume from current state, then retrieve needed D/Q/R-ID sections. / 현재 상태부터 복원하고 필요한 ID 구역만 추가 조회.
- Keep history in its source theme rather than duplicating it in the index. / 상세 이력을 인덱스에 중복 복사하지 않음.
- Generate audience handoffs at finalization or an explicit update, not after every answer. / 독자별 문서는 인계·갱신 시 생성.
- Retain file-write verification, decisions, blockers and history. / 저장 검증·결정·차단 쟁점·이력은 보존.

These are agent instructions, not an enforced memory cap or a change to the Claude runtime.
No measured RAM reduction is claimed. Packaging and unit-test success do not establish that this
workflow is followed in a real session.

에이전트 지침을 수정한 것이며 Claude 런타임이나 강제 메모리 상한을 바꾼 것은 아닙니다.
실측 RAM 절감률을 주장하지 않습니다. 패키징·단위 테스트 통과로 실제 세션의 지침 준수까지 입증하지 않습니다.

## Reproduction evidence · 재현에 필요한 근거

First identify the application and affected process; “Claude memory” might mean process RAM,
context-window usage, token totals, or storage on disk. Do not combine them into one metric.

먼저 정확한 앱과 프로세스를 확인합니다. 프로세스 RAM, 컨텍스트 사용량, 누적 토큰, 디스크 사용량은 별도 지표입니다.

| Field / 항목 | Useful report / 필요한 내용 |
| --- | --- |
| Environment / 환경 | Claude product, version, OS, model, skill version and install method |
| Memory / 메모리 | Named process/PID, measurement tool and metric, baseline/peak/idle values with units and timestamps |
| Session / 세션 | Invocation, number of exchanges, whether it was a fresh session or resume |
| File operations / 파일 동작 | Paths and byte sizes of repeatedly read or rewritten files; relevant redacted tool events |
| Isolation / 비교 | Same project, model, prompts and replies in separate fresh sessions, with and without the skill; optionally compare 0.3.0 with 0.3.1 |
| Persistence / 지속 여부 | Whether memory settles after activity stops or after closing that session |

Prepare three copies of a nonsensitive project if comparing baseline, 0.3.0 and 0.3.1.
Record the same fixed user replies, the memory metric at the same points, and the actual file/tool activity.
Use fresh sessions and keep other plugins/configuration consistent. Do not add extra model calls
merely to collect a report without the operator's agreement.
A remaining difference is a reproduction lead, not proof of a leak or its owner.

민감한 정보 없는 동일 프로젝트 사본으로 조건을 맞추고, 같은 회차에서 같은 지표를 기록합니다.
프로세스 메모리와 도구 출력량을 함께 봐야 반복 읽기와의 관련성을 검토할 수 있습니다.
차이가 나더라도 누수나 원인 주체가 곧바로 확정되는 것은 아닙니다.

The existing [A/B harness](../evals/README.md) evaluates behavior assertions. It does **not**
sample Claude process RAM. Its pass-rate delta cannot validate a memory fix.

기존 [A/B 평가기](../evals/README.ko.md)는 행동 판정용이며 Claude 프로세스 RAM을 측정하지 않습니다.
통과율 차이로 메모리 문제 해결을 입증할 수 없습니다.

## While investigating · 조사 중 사용

If only the canonical spec is needed, use `--contracts none` to omit the three audience documents.
For a long conversation, save the current answer and resume the saved session from a new chat.
Do not delete interview records to reduce context. Neither step is a guaranteed RAM fix.

원본 명세만 필요하면 `--contracts none`으로 문서 생성을 줄일 수 있습니다.
긴 대화는 현재 답변을 저장한 뒤 새 채팅에서 저장 경로로 재개할 수 있습니다.
기록을 지우지 마세요. 이 방법들도 RAM 문제 해결을 보장하지는 않습니다.
