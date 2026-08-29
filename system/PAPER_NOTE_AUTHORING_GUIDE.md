# Paper Note Authoring Guide

이 문서는 하나의 living Paper Note를 여러 읽기 세션에 걸쳐 안전하게 갱신하는 기준이다. Paper Note는 논문의 내용을 대신하는 요약문이 아니라 사용자가 실제로 읽고 설명하고 질문한 분석 evidence와 다음 복귀 위치를 보존한다.

## 1. 기존 파일을 먼저 읽는다

Update 전에 `main`의 기존 Paper Note 전체와 최신 blob SHA를 읽는다. 기존 분석, 질문, Bridge와 Reading Session History를 삭제하거나 과거 내용을 새 세션의 evidence처럼 바꾸지 않는다.

## 2. Resume Point를 정확히 쓴다

`Resume Point`에는 다음 세션에서 바로 찾을 수 있도록 가능한 범위에서 다음 정보를 기록한다.

- section 또는 subsection
- PDF page
- figure, table 또는 equation
- 문장 시작 부분
- 아직 확인하지 못한 내용 또는 재개할 행동

단순히 `Section 3`처럼 넓게 적지 않는다. Paper를 읽지 않고 Bridge를 학습하는 동안에는 기존 Resume Point를 이동하지 않는다.

## 3. Prerequisite Bridge를 두 방식으로 구분한다

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

## 4. Learning Log 연결

Learning Log가 실제 commit에 저장된 것을 확인한 뒤에만 Paper Note에 경로를 추가한다. 같은 개념의 Log가 여러 개면 생성 순서대로 나열하고, 각 Learning Log의 `Related notes`에도 Paper Note와 필요한 이전 Log를 연결한다.

동일한 학습 묶음을 이어가면 기존 Log update 후보로 처리하고, 날짜·하위 주제·의미 있는 학습 묶음이 달라지면 새 Log를 만든다. 기존 Learning Log의 문장과 checkbox를 새 evidence로 복제하지 않는다.

## 5. Reading Session History

사용자가 `오늘은 여기까지`처럼 세션 종료를 명시하면 그날 읽은 범위, 확인된 이해, 새 질문, Bridge 변화와 종료 당시 Resume Point를 날짜별로 추가한다. 과거 세션 기록을 덮어쓰지 않는다.

## 6. 사용자 evidence

Paper Note의 분석 내용과 Bridge 이해는 다음을 구분한다.

- 사용자가 직접 설명하거나 비교함
- 사용자와의 문답으로 수정·확인됨
- AI가 설명했지만 사용자 확인은 아직 없음
- 아직 읽거나 검증하지 않음

사용자가 읽지 않은 논문 부분을 일반 지식으로 추측해 채우지 않는다. 아직 확인하지 않은 canonical section은 `아직 분석하지 않음`으로 둔다.

## 7. 저장 전 점검

- 전체 canonical Paper Note를 보냈는가?
- Resume Point가 비어 있지 않은가?
- 이번 변경이 실제 Paper Reading Checkpoint인가?
- `studying`이 두 개 이상이지 않은가?
- `studying`인 개념마다 실제 저장된 Learning Log가 하나 이상 연결됐는가?
- Bridge Status가 허용값인가?
- 연결한 Learning Log가 실제 저장됐는가?
- 사용자의 자기 설명과 AI 설명을 구분했는가?
- Reading Session History가 과거 기록을 보존하는가?
