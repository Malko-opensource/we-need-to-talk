# 면담: {{topic}}

현재 상태와 재개 경로를 짧게 유지한다. 답변 본문·도구 출력은 복사하지 않고 원본 테마로 연결한다.

- 세션 ID: {{topic-slug}}-{{YYYY-MM-DD}}
- 날짜 / 시간대: {{date}} / {{timezone}}
- 상태: in-progress
- 모드: {{gauntlet-or-vc-or-partner-or-security}}
- 현재 관문: {{vc-or-partner-or-security}}
- 강도: {{spiciness}}
- 설명 청중: {{audience-or-adaptive}}
- 역할별 문서: {{all-or-none}}
- contract_bundle_status: {{not-requested-or-pending-or-partial-or-current-or-stale}}
- 목표: {{outcome}}
- 프로젝트: {{absolute-project-path-or-none}}
- 출력 경로: {{absolute-session-path}}
- 마지막 저장 회차: 없음
- 최종 명세: 아직 생성하지 않음
- 사용자 명세 검토: 아직 요청하거나 받지 않음

## 관문 진행 상태

선택한 관문의 상태와 근거를 기록한다. 단일 모드에서 검토하지 않은 관문은 not-reviewed로 남긴다.
관문 상태: pending / active / complete / deferred / needs-review / not-reviewed.

| 관문 | 상태 | 완료 또는 보류 근거·관련 ID | 재검토 이유 |
| --- | --- | --- | --- |
| vc | {{vc-status}} | {{vc-evidence}} | {{vc-recheck-or-none}} |
| partner | {{partner-status}} | {{partner-evidence}} | {{partner-recheck-or-none}} |
| security | {{security-status}} | {{security-evidence}} | {{security-recheck-or-none}} |

## 사전 확인

관찰한 근거만 기록한다. 기존 자료가 없으면 그 사실을 적는다.

| 근거 ID | 유형 | 확인한 내용 | 출처 | 확인 범위·한계 |
| --- | --- | --- | --- | --- |

## 테마와 유효한 결정

테마 파일이 생길 때 상대 링크와 결정 ID를 추가한다.

| 테마 파일 | 유효한 결정 ID | 요약 |
| --- | --- | --- |

## 열린 쟁점

종류는 누락·모순·보류, 영향은 차단·비차단으로 구분한다. 해결된 항목은 아래 이력으로 옮긴다.

| ID | 종류 | 쟁점과 근거 | 영향받는 범위 | 차단 여부 | 상세 기록 |
| --- | --- | --- | --- | --- | --- |

## 해결·변경 이력

회차·대체 결정 ID와 원본 링크만 간단히 남긴다. 상세 경위는 테마 파일 한 곳에서 보존한다.

| 회차 | 쟁점 또는 이전 결정 | 해결 내용 / 대체 결정 | 근거 |
| --- | --- | --- | --- |

## 재개 지점

- 답변을 기다리는 질문: {{pending-question-or-none}}
- 다음 확인 사항: {{next-topic}}
- 답변을 기다리는 이해 확인: {{decision-id-and-round-or-none}}
- 저장 실패 또는 불일치: 없음

## 역할별 문서

요청한 파일이 실제 생성된 경우에만 링크한다. 원본이 바뀌면 이전 문서는 stale로 표시한다.

| 문서 | source_revision | spec_status | 마지막 생성 회차 |
| --- | --- | --- | --- |
