# Paper Note Authoring Guide

이 문서는 하나의 living Paper Note를 여러 읽기 세션에 걸쳐 안전하게 갱신하는 기준이다. Paper Note는 논문의 내용을 대신하는 요약문이 아니라 사용자가 실제로 읽고 설명하고 질문한 분석 evidence와 다음 복귀 위치를 보존한다.

## 1. 기존 파일을 먼저 읽는다

Update 전에 `main`의 기존 Paper Note 전체와 최신 blob SHA를 읽는다. 기존 분석, 질문, Bridge와 Reading Session History를 삭제하거나 과거 내용을 새 세션의 evidence처럼 바꾸지 않는다.

## 2. 첨부 PDF에서 논문 identity를 확인한다

Paper Note의 Metadata에는 PDF를 대신하지 않는 논문 identity만 기록한다. PDF 첨부 여부와 접근 가능성은 영구 상태가 아니라 매 채팅에서 다시 확인하는 session-level gate다.

- `Title`, `Authors`, `Paper link`에는 첨부 PDF 첫 페이지와 문서 안에서 직접 확인한 제목, 저자와 DOI·arXiv ID 등 식별 정보를 기록한다.
- 대화 첨부파일의 임시 경로나 과거 conversation의 attachment URL을 영구 경로처럼 기록하지 않는다.

Paper Note의 identity가 있다는 사실 자체는 원문 접근 evidence가 아니다. 매 새 채팅에서 `system/PAPER_READING_TUTOR_POLICY.md`의 PDF Source Gate를 다시 통과해야 하며, Paper Note에 고정된 접근 방식이나 이번 채팅의 PDF 확인 결과를 기록하지 않는다.

## 3. Resume Point를 정확히 쓴다

`Resume Point`에는 다음 세션에서 바로 찾을 수 있도록 가능한 범위에서 다음 정보를 기록한다.

- section 또는 subsection
- PDF page
- figure, table 또는 equation
- 문장 시작 부분
- 아직 확인하지 못한 내용 또는 재개할 행동

단순히 `Section 3`처럼 넓게 적지 않는다. Paper를 읽지 않고 Bridge를 학습하는 동안에는 기존 Resume Point를 이동하지 않는다.

## 4. Prerequisite Bridge를 두 방식으로 구분한다

### 논문 안에서 해결한 선수지식

대화 길이가 아니라 저장 목적을 기준으로 분류한다. 별도 Learning Log를 만들지 않기로 한 개념은 설명이 길더라도 이 section에 기록할 수 있다.

- 개념이 등장한 논문 위치를 기록한다.
- 이 논문에서 왜 필요한지를 기록한다.
- 중요한 개념의 이해 확인은 `system/PAPER_READING_TUTOR_POLICY.md`에 따라 짧은 자기 설명으로 수행한다.
- 별도 evidence status 필드를 추가하지 않고 사용자가 직접 설명했는지, AI 설명만 들은 상태인지 자연어로 구분한다.
- AI가 설명했지만 사용자의 자기 설명이 확인되지 않았다면 사용자의 이해로 기록하지 않는다.

### 별도로 이어가는 선수지식

사용자가 명시적으로 별도 학습을 선택한 경우에만 Learning Log를 생성·수정하고 경로를 연결한다. ChatGPT가 필요성을 제안할 수는 있지만 사용자 선택 없이 승격하지 않는다.

- `studying`: 현재 이어가야 하는 학습. Paper Note 저장 시 실제 Learning Log 경로가 하나 이상 있어야 한다.
- `paused`: 아직 충분하지 않지만 사용자가 논문으로 돌아감
- `sufficient-for-paper`: 일반적인 완전 숙련이 아니라 현재 논문을 읽기에 충분함

한 Paper Note에서 `studying`은 최대 하나만 허용한다. `이 논문에 충분한 기준`을 구체적으로 적고 현재 논문에 필요하지 않은 깊이로 확장하지 않는다.

## 5. Learning Log 연결

Learning Log가 실제 commit에 저장된 것을 확인한 뒤에만 Paper Note에 경로를 추가한다. 같은 개념의 Log가 여러 개면 생성 순서대로 나열하고, 각 Learning Log의 `Related notes`에도 Paper Note와 필요한 이전 Log를 연결한다.

동일한 학습 묶음을 이어가면 기존 Log update 후보로 처리하고, 날짜·하위 주제·의미 있는 학습 묶음이 달라지면 새 Log를 만든다. 기존 Learning Log의 문장과 checkbox를 새 evidence로 복제하지 않는다.

## 6. Reading Session History

사용자가 `오늘은 여기까지`처럼 세션 종료를 명시하면 그날 읽은 범위, 확인된 이해, 새 질문, Bridge 변화와 종료 당시 Resume Point를 날짜별로 추가한다. 과거 세션 기록을 덮어쓰지 않는다.

## 7. 사용자 evidence

Paper Note의 분석 내용과 Bridge 이해는 다음을 구분한다.

- 사용자가 직접 설명하거나 비교함
- 사용자와의 문답으로 수정·확인됨
- AI가 설명했지만 사용자 확인은 아직 없음
- 아직 읽거나 검증하지 않음

사용자가 읽지 않은 논문 부분을 일반 지식으로 추측해 채우지 않는다. 아직 확인하지 않은 canonical section은 `아직 분석하지 않음`으로 둔다.

사용자의 해석을 correction하거나 exact number 또는 architecture mechanism을 Paper Note에 반영할 때는 확인한 PDF page 또는 section을 함께 기록한다. Paper Note, DOI·웹페이지·abstract, 사용자가 붙여 넣은 문장이나 모델 기억만으로 paper-direct fact를 만들지 않는다.

## 8. Prerequisite Inventory와 Bridge Audit

Paper Note 저장안을 작성하기 전에 마지막으로 저장된 checkpoint 이후 현재 conversation을 다시 훑어 임시 `Prerequisite Inventory`를 만든다. 다음은 inventory 후보다.

- 사용자가 논문 이해를 위해 뜻이나 작동 원리를 질문했고 GPT가 별도로 설명한 개념
- 사용자의 중요한 개념적 오해를 correction한 내용
- 현재 overview만으로 exact mechanism을 확인할 수 없어 원 논문이나 reference 확인 대상으로 남긴 내용

단순 영어 문법·번역, 기술 개념을 추가하지 않은 문장 재표현과 논문 문장을 그대로 요약한 내용은 Bridge 후보에서 제외한다.

각 후보를 다음 중 하나로 분류하고 기존·제안 Prerequisite Bridge와 대조한다.

- `논문 안에서 해결한 선수지식`
- `별도로 이어가는 선수지식`
- `Reference deep-dive candidate`
- `Bridge 대상 아님`과 제외 이유

Inventory의 각 후보가 Bridge 신규 추가, 기존 Bridge 업데이트, reference 후보 또는 제외 사유 중 하나로 설명되는지 확인한다. Architecture, Method, Questions에 내용이 있다는 이유로 Bridge 반영을 생략하지 않는다. 누락을 보완한 뒤에만 사용자에게 Paper Note 변경안을 제시한다.

`Reference deep-dive candidate`는 새 고정 section을 만들지 않고 기존 `Questions` 또는 관련 분석 section에 자연어로 보존한다. 이는 현재 paper를 이해하기 위해 이미 설명한 prerequisite를 Bridge에 기록하는 의무를 대신하지 않는다.

이 audit은 저장 전 검토용 절차이며 Paper Note에 새로운 고정 section이나 evidence status field를 추가하지 않는다. 승인 전에는 최소한 다음을 보여 준다.

```text
Prerequisite Bridge audit
- 이번 세션 후보:
- Bridge 신규 추가:
- 기존 Bridge 업데이트:
- Reference 후보:
- 제외한 항목과 이유:
```

## 9. 저장 전 점검

- 전체 canonical Paper Note를 보냈는가?
- Metadata의 제목·저자·논문 식별 정보가 첨부 PDF와 일치하는가?
- 임시 attachment 경로나 과거 conversation URL을 영구 source로 기록하지 않았는가?
- 이번 paper-specific 평가가 PDF Source Gate를 통과한 상태에서 이루어졌는가?
- Resume Point가 비어 있지 않은가?
- 이번 변경이 실제 Paper Reading Checkpoint인가?
- `studying`이 두 개 이상이지 않은가?
- `studying`인 개념마다 실제 저장된 Learning Log가 하나 이상 연결됐는가?
- Bridge Status가 허용값인가?
- 연결한 Learning Log가 실제 저장됐는가?
- 사용자의 자기 설명과 AI 설명을 구분했는가?
- 마지막 checkpoint 이후 Prerequisite Inventory를 만들었는가?
- Inventory의 모든 후보를 기존·제안 Bridge와 대조하고 누락을 보완했는가?
- 단순 문법·번역·문장 재표현을 Bridge로 과잉 기록하지 않았는가?
- Reading Session History가 과거 기록을 보존하는가?
