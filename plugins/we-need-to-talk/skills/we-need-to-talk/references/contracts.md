# Multi-Audience Contracts

원본은 세션 루트의 `_final-contract.md`다. 역할별 문서는 그 명세의 관점을 바꾼 파생 문서다.
`--contracts all`이면 다음 템플릿을 복사하고 사용자의 언어로 채운다.

| 템플릿 | 출력 경로 | 목적 |
| --- | --- | --- |
| [coding-agent](../assets/contracts/coding-agent.md) | contracts/1-for-coding-agent.md | 동작·계약·실패 처리·수용 기준 |
| [manager-exec](../assets/contracts/manager-exec.md) | contracts/2-for-manager-exec.md | 가치·범위·포기한 것·일정과 위험의 원인 |
| [designer-pm](../assets/contracts/designer-pm.md) | contracts/3-for-designer-pm.md | 사용자 흐름·화면 상태·오류와 복구 |

## 생성 순서

1. 원본 명세를 저장하고 다시 읽어 현재 유효한 결정, Q-ID, 수용 기준과 준비 상태를 확정한다.
2. 각 파생 문서의 YAML `source_revision`과 `spec_status`를 원본 값과 정확히 맞춘다.
   키와 상태 토큰은 언어에 따라 번역하지 않는다. 값에 특수문자가 있으면 YAML에서 인용한다.
3. 각 문서의 결정·제약·위험에 원본 D-ID 또는 Q-ID를 붙인다. 새 결정을 발명하지 않는다.
   독자별로 선택한 핵심 내용을 본문에 써서 링크만 있는 문서를 만들지 않는다.
4. 해당 독자의 작업에 영향을 주는 차단 쟁점·제외 범위·데이터 손실·권한 제약은 반드시 전달한다.
   관련 없는 세부는 링크로 줄일 수 있지만 `incomplete`를 `ready`로 바꾸지 않는다.
5. 세 문서를 다시 읽어 원본과 비교하고 인덱스에 링크와 버전을 기록한다.

타입·API·시간·예산·ROI·정확한 UI 문구가 합의되지 않았으면 미정이라고 적는다.
제안을 넣을 때는 **제안, 미확정**으로 표시한다. 경영진용 문서를 위해 납기를 지어내지 않는다.
문서 3종 생성은 검토·공유·배포·보안 인증의 완료를 뜻하지 않는다.

## 갱신과 중단

원본이 바뀌면 기존 파생 문서의 `spec_status`를 `stale`로 표시하고
인덱스의 `contract_bundle_status`도 `stale`로 바꾼다. 이전 source_revision은 갱신할 때까지 유지한다.
다시 생성할 때 새 원본의 상태와 개정으로 교체한다.

파일 하나라도 저장되지 않았으면 `partial`로 표시하고 성공한 경로·실패한 경로를 구분한다.
요청한 세 문서가 실제로 저장되고 일치할 때만 `current`다.
`current`는 문서 동기화 상태다. 원본이 `incomplete`인 묶음도 `current`일 수 있다.
생성 전에는 `pending`, `--contracts none`이면 `not-requested`다.
none으로 바꿔도 기존 파일을 지우거나 오래된 파일을 최신으로 표시하지 않는다.
