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

사용자가 `PB로 남겨줘`, `Prerequisite Bridge에 기록해줘`, `선수지식으로 저장하자`처럼 자연어로 명시적으로 선택했거나 GPT의 PB 제안에 동의한 개념만 기록한다. 질문·설명·오해 수정이 있었다는 사실만으로 자동 추가하지 않는다. 선택된 개념을 별도 Learning Log로 만들지 않기로 했다면 이 section에 기록한다.

- 개념이 등장한 논문 위치를 기록한다.
- 이 논문에서 왜 필요한지를 기록한다.
- `실제 정의`에는 사용자의 이해와 분리된 개념 자체의 뜻을, 나중에 이 항목만 읽어도 확인할 수 있도록 간결하게 기록한다. 논문이 직접 정의한 범위와 이해를 위한 보충 정의를 혼동하지 않는다.
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

### Paper-source section의 evidence boundary

`Problem`, `Key Idea`, `Architecture`, `Method`, `Experiments`, `Results`, `Trade-offs`, `Paper-Reported Limitations`와 Final Summary의 paper claim은 PDF Source Gate를 통과한 첨부 PDF에서 직접 확인한 내용만 기록한다. GPT는 일반 지식, 다른 논문, 구조적 개연성 또는 자신의 reasoning으로 빈칸을 채우지 않는다. 논문이 원인, 연결 관계, operation, benefit, limitation이나 저자의 의도를 직접 설명하지 않았다면 그럴듯하게 보이더라도 paper fact로 작성하지 않는다. 합리적으로 추론할 수 있어도 paper fact로 작성하지 않는다.

아직 해당 범위를 확인하지 않았다면 `아직 분석하지 않음`, 필요한 범위를 확인했지만 특정 field에 해당하는 내용이 없거나 근거가 부족하면 정확히 `논문에서 언급되지 않음`으로 구분한다. `논문에서 언급되지 않음`을 보충하기 위해 외부 reference나 GPT 추론을 source-grounded field에 넣지 않는다. GPT 또는 사용자의 해석은 `User-Identified Limitations`, `Questions`, `Connection to My Research Interest`, `사용자 분석 근거`처럼 해석을 허용한 영역에만 paper claim과 구분해 기록한다.

## 8. Full-paper source synthesis와 User-Identified Limitations

`## 5. Architecture`, `## 6. Method`, `## 9. Trade-offs`와 `Paper-Reported Limitations`는 사용자의 읽기 진도에서 수집한 이해 evidence를 기다려 채우는 section이 아니다. 현재 conversation의 첨부 PDF가 `system/PAPER_READING_TUTOR_POLICY.md`의 PDF Source Gate를 통과하면, ChatGPT는 논문 전체에서 관련 section, figure, subfigure, caption, table, equation과 연결된 본문을 확인하고 네 영역의 초안을 바로 작성한다. 이 예외는 source-grounded 초안 작성에만 적용하며, 사용자의 실제 읽기 범위나 이해 evidence로 승격하지 않는다. 파일 저장과 기존 Paper Note update는 여전히 사용자 승인을 받아야 한다.

### Architecture

먼저 논문의 전체 architecture와 end-to-end operation을 요약한다. 그다음 논문이 제안하거나 새롭게 사용하는 architecture, circuit, cell 또는 structure를 다음 원칙으로 분리한다.

- 단일 제안 논문은 system level 또는 architecture family 아래에 구성 요소를 나눈다.
- Overview/review paper는 DRAM-CIM, NVM-CIM 또는 논문이 사용하는 architecture family처럼 비교 축을 먼저 세운다.
- 서로 다른 구성, 동작 또는 trade-off를 갖는 figure·subfigure는 각각 별도 항목으로 작성한다.
- Figure가 없어도 이름이 붙은 새로운 circuit 또는 structure는 별도 항목으로 작성한다.
- 같은 구조를 여러 figure가 반복 설명하면 중복 항목을 만들지 않고 근거 위치를 함께 기록한다.
- Result plot, dataset 예시와 배경 설명용 figure는 architecture를 설명하지 않으면 포함하지 않는다.

각 항목에는 최소한 `근거 위치`, `논문 내 역할`, `Main Structure (Components)`, `Operation Overview`, `Data / Signal Flow`, `Benefits`, `Challenges / Trade-offs`, `논문이 제공하지 않은 세부사항`을 사용한다. Figure caption만 보고 동작을 완성하지 않으며 연결된 본문을 함께 확인한다. 논문에 없는 연결 관계, 회로 동작, 저자의 의도 또는 장단점은 추측하지 않는다. 적용되지 않거나 근거가 부족한 field는 정확히 `논문에서 언급되지 않음`으로 표시한다.

### Method

Method는 Architecture의 architecture family와 structure heading, 이름과 순서를 그대로 사용한다. Architecture의 `Operation Overview`를 반복해서 늘리지 않고, 같은 structure가 수행하는 operation의 원리와 절차를 논문이 설명한 범위 안에서 상세화한다. Operation은 MAC으로 한정하지 않으며 arithmetic, logic, memory, data movement, sensing, conversion, control 또는 algorithmic procedure를 포함할 수 있다.

각 structure에는 `Architecture reference`, `Method purpose`, `Input / Initial state`, `Core operation`, `Operation mechanism`, `Output / State change`, `Required conditions or assumptions`, `Benefits`, `Limitations / Trade-offs`, `근거 위치`를 사용한다. 논문에 실제로 존재하는 단계만 설명하고, 일반적인 pipeline을 완성하기 위해 precharge, encoding, accumulation, sensing, conversion 또는 post-processing 단계를 임의로 추가하지 않는다. 특정 field가 논문에 없거나 근거가 부족하면 정확히 `논문에서 언급되지 않음`으로 표시한다.

### Trade-offs

Trade-off는 논문이 동일한 structure 또는 approach의 `Benefit (Gain)`과 `Trade-off / Cost`를 모두 설명하고 둘의 관계를 직접 연결한 경우에만 선정한다. PDF 근거 위치가 있어야 하며, GPT가 서로 떨어진 장점과 단점을 하나의 교환 관계로 조합하지 않는다. Cost만 있고 대응하는 gain이 없으면 Trade-off가 아니다. 그 cost가 capability 또는 applicability를 직접 제한한다고 논문이 설명한 경우에만 Paper-Reported Limitation 후보로 검토한다.

Gain–Cost 관계 전체는 Trade-offs에만 기록하고 Limitations에 반복하지 않는다. 논문이 Trade-off와 별개인 residual hard boundary를 직접 명시한 경우에만 그 경계를 Limitation으로 별도 기록한다. 조건을 만족하는 항목이 없으면 빈 table row를 만들지 않고 `논문에서 언급되지 않음`으로 표시한다.

### Paper-Reported Limitations

Paper-Reported Limitation은 논문이 limitation, constraint 또는 지원 범위의 경계를 직접 설명하고, 영향을 받는 structure, method, system 또는 paper claim을 특정할 수 있으며, 지원 operation, workload, precision, accuracy, scalability, reliability, operating condition, hardware feasibility 또는 claim의 유효 범위를 실제로 제한하는 경우에만 선정한다. 단순한 Gain–Cost 관계이거나 Trade-offs에 같은 내용이 있으면 제외하며 PDF 근거 위치가 반드시 있어야 한다.

논문이 `challenge`라고 표현했더라도 제한되는 capability 또는 applicability를 설명하지 않았다면 Limitation으로 승격하지 않는다. 모든 structure에 limitation을 의무적으로 만들지 않고 해당되는 항목만 `Structure-specific Capability / Applicability Limits`에 기록한다. 여러 structure를 임의로 묶지 않으며, 전체 system 또는 paper claim의 경계라고 논문이 직접 설명한 항목만 `System- or Paper-level Capability / Applicability Limits`에 기록한다. 조건을 만족하는 항목이 하나도 없으면 subsection 전체에 `논문에서 언급되지 않음`으로 표시한다.

### User-Identified Limitations

이 subsection만 사용자의 학습과 대화를 따라 업데이트한다. 논문을 처음 받았을 때 자동 생성하지 않는다. 사용자가 limitation을 직접 제기한 경우에만 후보로 수집하며, 단순한 질문이나 GPT의 correction은 limitation으로 확정하지 않고 `Questions` 또는 적절한 evidence 영역에 둔다. GPT는 사용자의 발언을 확대하거나 새로운 limitation을 만들지 않고 가능한 한 사용자의 표현을 보존한다.

학습 세션을 마무리할 때 마지막 checkpoint 이후 대화에서 확인된 후보를 모아 `사용자가 지적한 limitation`, `Related Architecture / Method`, `사용자가 근거로 사용한 paper content`, `Paper에서 직접 확인된 내용`, `추가 확인이 필요한 부분`으로 정리한다. Paper claim과 user observation을 혼동하지 않으며, Paper Note update와 저장은 기존 승인 절차를 따른다.

## 9. 사용자 선택 PB Inventory와 Bridge Audit

Paper Note 저장안을 작성하기 전에 마지막으로 저장된 checkpoint 이후 현재 conversation에서 사용자가 명시적으로 선택한 개념만 `PB Inventory`로 모은다. 다음 두 경우만 포함한다.

- 사용자가 `PB`, `Prerequisite Bridge`, `선수지식` 등으로 남겨 달라고 자연어로 직접 요청한 개념
- GPT가 PB 기록을 제안한 뒤 사용자가 명시적으로 동의한 개념

GPT는 다음 세션 복구에 가치가 큰 개념을 PB로 남길지 제안할 수 있다. 그러나 제안만으로 선택된 것이 아니며, 사용자가 동의하기 전에는 PB Inventory나 저장안에 넣지 않는다. 사용자가 단어의 뜻이나 작동 원리를 질문한 것, GPT가 개념을 설명한 것, 중요한 오해를 correction한 것과 reference deep-dive 후보가 생긴 것만으로는 PB 선택으로 간주하지 않는다.

일반적인 `Paper Note를 저장해줘` 또는 checkpoint 저장 승인은 지정되지 않은 PB 항목의 추가 승인으로 확대 해석하지 않는다. 사용자가 PB 기록은 요청했지만 별도 Learning Log 학습은 선택하지 않았다면 `논문 안에서 해결한 선수지식`으로 분류한다. 별도 학습을 명시적으로 선택한 경우에만 `별도로 이어가는 선수지식`으로 분류한다.

선택되지 않은 설명·correction은 필요에 따라 Architecture, Method, Questions, 사용자 분석 근거 등 적절한 section에 기록할 수 있지만 PB에는 추가하지 않는다. Reference deep-dive candidate도 사용자가 PB로 선택하지 않았다면 기존 `Questions` 또는 관련 분석 section에만 자연어로 보존한다.

PB Inventory를 기존·제안 Prerequisite Bridge와 대조해 신규 추가, 기존 항목 업데이트, 변경 없음 또는 사용자가 철회한 항목으로 구분한다. 이 audit은 저장 전 검토용 절차이며 Paper Note에 새로운 고정 section이나 evidence status field를 추가하지 않는다. 승인 전에는 최소한 다음을 보여 준다.

```text
Prerequisite Bridge audit
- 사용자가 직접 선택한 PB:
- GPT 제안 후 승인된 PB:
- Bridge 신규 추가:
- 기존 Bridge 업데이트:
- 변경 없음 또는 철회:
```

## 10. 저장 전 점검

- 전체 canonical Paper Note를 보냈는가?
- Metadata의 제목·저자·논문 식별 정보가 첨부 PDF와 일치하는가?
- 임시 attachment 경로나 과거 conversation URL을 영구 source로 기록하지 않았는가?
- 이번 paper-specific 평가가 PDF Source Gate를 통과한 상태에서 이루어졌는가?
- Architecture가 첨부 PDF 전체의 architecture 관련 본문과 figure를 근거로 작성되었는가?
- Method가 Architecture와 같은 family·structure heading, 이름과 순서를 따르는가?
- Trade-off마다 논문이 직접 연결한 Gain과 Cost가 모두 있고 PDF 근거가 있는가?
- Gain과 Cost를 GPT가 임의로 조합하거나 같은 관계를 Limitation에 반복하지 않았는가?
- Paper-Reported Limitation마다 제한되는 capability 또는 applicability와 영향 대상이 논문에 직접 명시되어 있는가?
- 단순한 challenge나 Trade-off를 Limitation으로 자동 승격하지 않았는가?
- User-Identified Limitations에는 사용자가 직접 제기한 항목만 있으며 학습 종료 시점에 업데이트했는가?
- 사용자의 단순한 질문이나 GPT의 correction을 User-Identified Limitation으로 만들지 않았는가?
- Architecture와 Method의 모든 사실이 첨부 PDF에서 직접 확인되었는가?
- 논문에 없거나 근거가 부족한 field를 `논문에서 언급되지 않음`으로 표시했는가?
- 일반 지식, 다른 논문, GPT의 추론 또는 구조적 개연성으로 source-grounded field를 채우지 않았는가?
- 새로운 architecture·circuit·structure를 figure·subfigure 또는 이름이 붙은 구조별로 분리했는가?
- Architecture, Method, Trade-offs와 Paper-Reported Limitations의 source synthesis를 사용자의 읽기 범위나 이해 evidence로 기록하지 않았는가?
- Resume Point가 비어 있지 않은가?
- 이번 변경이 실제 Paper Reading Checkpoint인가?
- `studying`이 두 개 이상이지 않은가?
- `studying`인 개념마다 실제 저장된 Learning Log가 하나 이상 연결됐는가?
- Bridge Status가 허용값인가?
- 연결한 Learning Log가 실제 저장됐는가?
- 사용자의 자기 설명과 AI 설명을 구분했는가?
- 논문 안에서 해결한 각 선수지식에 등장 위치, 필요한 이유, 실제 정의와 사용자의 이해가 모두 기록됐는가?
- 마지막 checkpoint 이후 사용자가 명시적으로 선택한 개념만 PB Inventory에 넣었는가?
- GPT가 제안만 했거나 설명·correction만 한 개념을 승인 없이 PB에 추가하지 않았는가?
- 일반적인 Paper Note 저장 승인을 지정되지 않은 PB 추가 승인으로 확대하지 않았는가?
- 선택된 PB를 기존·제안 Bridge와 대조했는가?
- Reading Session History가 과거 기록을 보존하는가?
