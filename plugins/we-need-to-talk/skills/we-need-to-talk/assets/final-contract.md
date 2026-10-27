---
source_revision: "{{revision}}"
spec_status: "{{ready-or-incomplete-or-paused}}"
---

# 실행 명세: {{topic}}

- 개정: {{revision}}
- 명세 상태: {{ready-or-incomplete-or-paused}}
- 기준 회차 / 날짜: {{last-round}} / {{date}}
- 면담 모드 / 강도: {{mode}} / {{spiciness}}
- 사용자 명세 검토: {{not-reviewed-or-user-statement-with-round}}
- 실제 구현·검증 결과: 이 면담에서는 검증하지 않음
- 원본 기록: [_session-index.md](_session-index.md)

## 검토 범위

| 관문 | 상태 | 확인한 내용·근거 | 검토하지 않았거나 다시 확인할 내용 |
| --- | --- | --- | --- |
| vc | {{vc-status}} | {{vc-summary}} | {{vc-open-or-none}} |
| partner | {{partner-status}} | {{partner-summary}} | {{partner-open-or-none}} |
| security | {{security-status}} | {{security-summary}} | {{security-open-or-none}} |

단일 모드의 관문 완료를 전체 명세의 준비 완료로 바꾸지 않는다. Security 면담은 보안 테스트 결과가 아니다.

## 목표와 범위

- 사용자와 해결할 문제: {{user-and-problem}}
- 이번 범위: {{in-scope}}
- 제외 범위: {{out-of-scope}}

## 유효한 결정

현재 구현해야 할 동작을 이 문서만 읽어도 알 수 있게 요약한다.
각 결정에 ID와 상대 경로의 상세 기록 링크를 붙인다. 폐기된 결정은 여기 포함하지 않는다.

{{current-decisions-with-constraints-and-rationale}}

## 핵심 흐름과 실패 처리

{{main-flow-and-agreed-failure-behaviors}}

## 수용 기준

| ID | 조건 / 행동 | 기대 결과 | 확인 방법 | 관련 결정 |
| --- | --- | --- | --- | --- |

## 남은 쟁점과 준비 상태의 근거

- 차단 쟁점: {{blocking-items-or-none}}
- 보류 항목과 적용할 기본값: {{deferred-items-or-none}}
- 이해가 엇갈린 결정 또는 위임된 판단: {{relevant-decision-and-round-ids-or-none}}
- 상태 판정 근거: {{why-ready-or-why-incomplete}}

보류 파일이 실제로 있을 때만 링크한다. 미결 항목이 허용하는 작업 범위도 적는다.

## 인계 조건

- 요청받은 다음 작업: {{authorized-next-work-or-spec-only}}
- 구현자가 다시 확인할 외부 사실: {{facts-that-may-change-or-none}}
- 결정 변경 시: 원본 기록에 새 결정과 대체 관계를 남기고 이 명세의 개정을 갱신한다.

## 역할별 문서

{{links-to-generated-contracts-or-not-requested}}

역할별 문서는 이 명세에서 파생한다. 같은 source_revision과 spec_status인지 확인한다.
