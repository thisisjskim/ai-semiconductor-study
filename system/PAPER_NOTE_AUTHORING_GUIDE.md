# Paper Note Authoring Guide

이 문서는 하나의 living Paper Note를 여러 읽기 세션에 걸쳐 안전하게 갱신하는 기준이다. Paper Note는 논문의 내용을 대신하는 요약문이 아니라 사용자가 실제로 읽고 설명하고 질문한 분석 evidence와 다음 복귀 위치를 보존한다.

`templates/paper-note.md`는 저장 결과의 heading, field와 반복 가능한 record shape만 정의하는 간결한 output schema다. Lifecycle, 선정 gate, no-inference, 중복 방지, evidence 판정과 완독 조건은 이 Authoring Guide와 `system/PAPER_READING_TUTOR_POLICY.md`에서만 설명하며 생성된 Paper Note에 정책 문단을 복사하지 않는다. Template의 placeholder는 실제 항목으로 교체하고, 동적 record가 없을 때는 각 section 규칙이 지정한 `논문에서 언급되지 않음`, `선정된 질문 없음`, `확인된 연구 연결 없음`, `아직 분석하지 않음` 등의 상태만 남긴다.

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

아직 해당 범위를 확인하지 않았다면 `아직 분석하지 않음`, 필요한 범위를 확인했지만 특정 field에 해당하는 내용이 없거나 근거가 부족하면 정확히 `논문에서 언급되지 않음`으로 구분한다. `논문에서 언급되지 않음`을 보충하기 위해 외부 reference나 GPT 추론을 source-grounded field에 넣지 않는다. GPT 또는 사용자의 해석은 `User-Identified Limitations`, `Questions`, `Connection to My Research Direction`, `사용자 분석 근거`처럼 해석을 허용한 영역에만 paper claim과 구분해 기록한다.

## 8. Full-paper source synthesis와 conversation-following sections

### Section lifecycle boundary

Paper Note section은 작성 source와 update trigger에 따라 다음 세 lifecycle로 구분한다.

- **Paper-source immediate sections:** `Problem`, `Key Idea`, `Architecture`, `Method`, `Experiments`, `Results`, `Trade-offs`, `Paper-Reported Limitations`. PDF Source Gate를 통과하면 사용자와의 학습 대화를 기다리지 않고 첨부 PDF 전체의 직접 근거만으로 바로 초안을 작성한다.
- **Conversation-derived sections:** `User-Identified Limitations`, `Questions`, `Connection to My Research Direction`. 실제 사용자–ChatGPT 학습 대화에서 발생하고 확인된 내용만 후보로 삼아 학습 세션을 마무리할 때 업데이트한다. 첨부 PDF만 읽어서 자동 생성하거나 갱신하지 않는다.
- **Reading-completion synthesis:** `Final Summary`. 사용자가 논문 본문을 끝까지 읽었다고 명시하고 checkpoint evidence가 마지막 본문 section까지의 읽기 완료를 뒷받침할 때만 마지막 정리로 작성한다. GPT가 PDF 전체를 분석했다는 사실만으로 작성하지 않는다.

세 lifecycle을 서로 대신하지 않는다. 대화가 있었다는 이유로 PDF 근거 없이 Paper-source immediate section을 채우지 않으며, PDF 전체를 분석했다는 이유로 사용자가 제기하지 않은 User-Identified Limitation, Question 또는 Research Connection을 만들지 않는다.

`## 3. Problem`, `## 4. Key Idea`, `## 5. Architecture`, `## 6. Method`, `## 7. Experiments`, `## 8. Results`, `## 9. Trade-offs`와 `Paper-Reported Limitations`는 사용자의 읽기 진도에서 수집한 이해 evidence를 기다려 채우는 section이 아니다. 현재 conversation의 첨부 PDF가 `system/PAPER_READING_TUTOR_POLICY.md`의 PDF Source Gate를 통과하면, ChatGPT는 논문 전체에서 관련 section, figure, subfigure, caption, table, equation과 연결된 본문을 확인하고 여덟 영역의 초안을 바로 작성한다. 이 예외는 source-grounded 초안 작성에만 적용하며, 사용자의 실제 읽기 범위나 이해 evidence로 승격하지 않는다. 파일 저장과 기존 Paper Note update는 여전히 사용자 승인을 받아야 한다.

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

이 subsection은 사용자의 학습과 대화를 따라 업데이트한다. 논문을 처음 받았을 때 자동 생성하지 않는다. 사용자가 limitation을 직접 제기한 경우에만 후보로 수집하며, 단순한 질문이나 GPT의 correction은 limitation으로 확정하지 않고 `Questions` 또는 적절한 evidence 영역에 둔다. GPT는 사용자의 발언을 확대하거나 새로운 limitation을 만들지 않고 가능한 한 사용자의 표현을 보존한다.

학습 세션을 마무리할 때 마지막 checkpoint 이후 대화에서 확인된 후보를 모아 `사용자가 지적한 limitation`, `Related Architecture / Method`, `사용자가 근거로 사용한 paper content`, `Paper에서 직접 확인된 내용`, `추가 확인이 필요한 부분`으로 정리한다. Paper claim과 user observation을 혼동하지 않으며, Paper Note update와 저장은 기존 승인 절차를 따른다.

### Questions

Questions는 full-paper source synthesis 영역이 아니라 실제 사용자–ChatGPT 학습 대화를 source로 삼는 지연 업데이트 영역이다. 질문의 답을 확인할 때 Paper 근거를 사용할 수 있지만, 질문 후보 자체는 대화에서 발생해야 한다. 논문을 처음 받았거나 PDF를 전부 분석했다는 사실만으로 작성하지 않으며, 학습 세션을 마무리할 때 마지막 checkpoint 이후 대화의 Question Inventory를 만든 뒤 다음 gate를 순서대로 적용한다.

1. **Origin Gate:** 사용자가 실제로 질문했거나, GPT가 제안한 질문을 사용자가 명시적으로 채택해 실제로 탐구했다.
2. **Paper Grounding Gate:** Problem, Key Idea, Architecture, Method, Experiments, Results, Trade-offs, Limitations, 특정 figure·table·equation·claim 또는 논문 이해에 필요한 핵심 prerequisite 중 하나와 직접 연결된다.
3. **Learning Value Gate:** 핵심 이해의 막힘 해소, 의미 있는 오해 수정, 논문 내 개념·section 연결, claim·evidence·assumption·comparison 평가, 가치 있는 미해결 next action 또는 구체적인 후속 연구 발전 중 하나 이상에 실제 영향을 준다.
4. **Persistence Gate:** 답, 해결 과정 또는 남은 불확실성을 다음 세션에서 복구할 가치가 있다.
5. **Deduplication Gate:** 기존 질문과 중복되지 않는다. 질문이 재표현되거나 발전한 경우 별도 항목을 만들지 않고 기존 기록에 통합한다.

단순 용어 뜻을 즉시 확인해 이후 이해에 영향이 없었던 질문, 기술 의미를 바꾸지 않는 번역·문법 질문, 학습 절차·기록 방식에 관한 meta 질문, 학습 영향이 없는 단순 정보 조회는 제외한다. GPT가 사용자가 하지 않은 질문을 만들어 기록하지 않는다. GPT가 제안만 한 질문도 제외하며, 사용자가 명시적으로 받아들여 실제로 탐구한 경우에만 Origin Gate를 통과한다. §12의 tutoring verification 질문도 사용자가 자신의 질문으로 받아들여 탐구하지 않았다면 Paper Note Questions가 아니다.

통과한 질문은 목적에 따라 `이해를 위한 질문`, `비판적 질문`, `후속 연구 질문` 중 하나에 배치한다. 이해를 위한 질문은 핵심 mechanism, prerequisite, 개념 간 연결 또는 이후 해석을 막는 오해에 관한 것이어야 한다. 비판적 질문은 claim, evidence, assumption, comparison, 적용 범위 또는 평가 타당성에 영향을 주어야 한다. 후속 연구 질문은 논문에서 확인된 한계, 열린 문제 또는 비교 필요성을 구체적인 검증 대상이나 다음 research action으로 발전시켜야 한다.

각 기록에는 `사용자의 질문`, `질문이 발생한 위치 또는 맥락`, `선정 이유`, `해결 과정`, `해결하며 알게 된 내용`, `해결 상태`, `해결하지 못한 부분`, `해결에 사용한 근거`를 남긴다. 해결 상태는 다음 의미로만 사용한다.

- `resolved`: 질문의 핵심 답이 Paper 또는 대화에서 확인되었고, 남은 핵심 불확실성이 없다.
- `partially-resolved`: 핵심의 일부는 확인했지만 중요한 조건, 근거 또는 적용 범위가 남아 있다.
- `unresolved`: Paper와 현재 대화에서 핵심 답을 확인하지 못했다.

Paper direct evidence, GPT supplementary explanation, User interpretation / hypothesis를 분리한다. GPT 설명만으로 사용자의 이해가 확인되었다고 기록하지 않는다. Paper에 직접 답이 없으면 `논문에서 언급되지 않음`으로 표시하고 GPT 추론으로 해결 상태를 높이지 않는다. 대화에서 해결 과정이나 사용자 해석을 확인할 수 없는 field는 추정하지 않고 `대화에서 확인되지 않음`으로 표시한다. 해결된 질문의 `해결하지 못한 부분`은 `해당 없음`으로 쓰고, 부분 해결 또는 미해결 질문은 무엇이 부족하며 다음에 무엇을 확인해야 하는지 구체적으로 기록한다. 해당 category에 통과한 질문이 없으면 placeholder record를 만들지 않고 `선정된 질문 없음`으로 표시한다. 기존 질문의 후속 대화가 생기면 원래 질문과 이전 해결 이력을 보존하면서 해결 과정, 알게 된 내용과 상태를 갱신한다.

### Connection to My Research Direction

이 section은 사용자가 대화에서 표현하거나 명시적으로 받아들인 research interest·goal·problem awareness와 논문의 구체적인 element 사이의 확인된 관계만 기록한다. Paper를 처음 받았을 때 자동으로 작성하지 않으며, PDF 전체 분석은 connection 후보를 생성하는 근거가 아니다. GPT는 연결 후보를 제안할 수 있지만 사용자가 받아들여 실제로 탐구하기 전에는 기록하지 않는다.

학습 세션을 마무리할 때 마지막 checkpoint 이후 대화에서 Research Connection Inventory를 만들고 다음 gate를 모두 적용한다.

1. **User-Origin Gate:** 사용자가 research interest·goal·problem awareness를 직접 표현했거나 GPT 제안을 명시적으로 채택해 탐구했다.
2. **Paper-Anchor Gate:** 연결되는 claim, architecture, method, result, trade-off, limitation 또는 question과 PDF 근거 위치를 특정할 수 있다.
3. **Mechanism Gate:** keyword가 비슷하다는 이유가 아니라 사용자 관심과 Paper element가 연결되는 기술적 이유를 설명할 수 있다.
4. **Directional-Value Gate:** research framing, paper comparison, anchor-paper 선정, portfolio evidence 또는 후속 연구 방향 중 하나에 실제 영향을 준다.
5. **Non-Duplication Gate:** Questions, Limitations, Final Summary를 반복하지 않고 이 논문이 사용자 연구 방향에서 수행하는 역할을 설명한다.

Questions는 알아내야 할 epistemic gap과 그 해결 상태를 기록한다. Research Connection은 그 질문이나 Paper element가 사용자의 연구 방향에서 왜 중요한지와 어떤 역할을 하는지를 기록한다. 같은 질문이나 limitation 본문을 복사하지 않고 `기존 Questions / Limitations와의 관계`에서 참조한다. 단순한 흥미 표현, 사용자가 받아들이지 않은 GPT 연결 제안, 구체적인 Paper anchor가 없는 일반적 진로 문장과 다른 section의 재요약은 제외한다.

통과한 각 connection은 `사용자가 표현한 research interest 또는 goal`, `연결되는 Paper element`, `연결 근거 위치`, `연결 방식`, `이 논문이 내 연구 방향에서 수행하는 역할`, `기존 Questions / Limitations와의 관계`, `연결의 경계 또는 아직 확인되지 않은 부분`, `향후 활용`으로 정리한다. Paper fact와 user observation을 분리하며 사용자의 관심 범위를 확대하지 않는다. Paper 근거가 없으면 `논문에서 언급되지 않음`, 대화 근거가 없으면 `대화에서 확인되지 않음`으로 표시하고 임의로 연결하지 않는다.

새 Paper Note에서 통과한 connection이 없으면 `확인된 연구 연결 없음`으로 표시한다. 기존 Paper Note에서 이번 세션에 새로운 connection이 없으면 기존 기록을 그대로 보존하고 section을 변경하지 않는다. 새 connection, 기존 connection 갱신, 제외 후보와 제외 이유를 저장안에 보여 준 뒤 사용자 승인 후에만 Paper Note를 수정한다.

### Final Summary

Final Summary는 full-paper source synthesis로 미리 채우는 section도, 각 학습 세션에서 부분적으로 누적하는 section도 아니다. 다음 조건을 모두 만족할 때 한 번의 reading-completion synthesis로 작성한다.

1. 사용자가 현재 논문 본문을 끝까지 읽었다고 명시했다.
2. Reading Checkpoint, Resume Point와 Reading Session History가 conclusion 또는 사용자가 정한 마지막 본문 범위까지 도달했음을 뒷받침한다.
3. Final Summary에 포함할 Paper claim을 현재 conversation의 첨부 PDF에서 직접 확인할 수 있다.

완독 전에는 확인된 field만 부분적으로 채우지 않고 Final Summary 전체를 `아직 분석하지 않음`으로 둔다. GPT가 Problem, Key Idea, Architecture, Method, Experiments, Results, Trade-offs와 Paper-Reported Limitations를 full-paper source synthesis로 작성했더라도 Final Summary 작성 조건을 충족한 것이 아니다. 사용자가 중간 요약을 요청하면 대화에서 답할 수 있지만 이를 canonical Final Summary에 저장하지 않는다.

완독 후 `Problem`, `Key Idea`, `Architecture`, `Main Claim / Result and Supporting Evidence`, `Main Trade-off`, `Limitation`, `내가 기억할 한 문장` 구조를 사용한다. Paper claim은 PDF 직접 근거로만 작성하고, 사용자의 해석과 기억 문장은 실제 대화 evidence를 보존한다. `내가 기억할 한 문장`이 사용자 대화에서 확인되지 않았다면 GPT가 대신 만들지 않고 `대화에서 확인되지 않음`으로 표시한다. 완독은 reading coverage evidence일 뿐 모든 mechanism의 이해, 질문 해결 또는 mastery evidence가 아니다.

`Main Claim / Result and Supporting Evidence`에는 논문의 primary claim 또는 result 하나만 선정한다. 이를 가장 직접적으로 지지하는 대표 evidence 또는 synthesis basis를 1~3개 고르고, claim을 해석하는 데 필요한 baseline, workload, dataset, precision, array size, technology, measured/simulated 여부 또는 논문 유형에 맞는 scope를 보존한다. Claim의 범위를 evidence보다 넓히거나, 서로 다른 결과를 합쳐 논문이 하지 않은 종합 주장을 만들지 않는다.

Experimental paper는 measured/simulated result와 비교 조건을, architecture·circuit·method paper는 제안 contribution과 이를 검증한 evaluation을, analytical paper는 model·equation·proof 또는 analysis를 기록할 수 있다. Overview/review paper는 신규 실험 결과를 만들어 넣지 않고 taxonomy, surveyed literature, representative architecture, table 또는 comparison처럼 논문이 실제로 제시한 synthesis basis를 기록한다.

Detailed Results는 주요 figure, table, metric과 조건을 보존하는 전체 evidence inventory다. Final Summary는 이를 복사하지 않고 primary claim 하나와 가장 대표적인 support만 압축한다. Evidence가 claim을 직접 지지하는지 확인할 수 없으면 관계를 추론하지 않으며, 근거나 조건이 논문에 없으면 해당 field를 `논문에서 언급되지 않음`으로 표시한다.

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
- Questions를 논문을 처음 받았을 때 자동으로 작성하지 않고 학습 종료 시 Question Inventory에 gate를 적용했는가?
- 사용자가 실제로 질문했거나 GPT 제안을 명시적으로 채택해 탐구한 질문만 포함했는가?
- 각 질문이 구체적인 paper element와 연결되고 학습 가치 및 다음 세션 복구 가치를 갖는가?
- 단순 용어 확인, 의미 변화 없는 번역·문법, meta 질문과 학습 영향 없는 조회를 제외했는가?
- 중복되거나 발전한 질문을 새 항목으로 늘리지 않고 기존 기록에 통합했는가?
- 각 질문에 해결 과정, 알게 된 내용, 해결 상태, 미해결 부분과 구분된 근거가 있는가?
- GPT의 설명만으로 사용자의 이해가 확인되었다고 기록하거나 Paper에 없는 답을 추론하지 않았는가?
- Connection to My Research Direction을 Paper 전체 분석만으로 자동 작성하지 않고 대화 기반 Research Connection Inventory에서 만들었는가?
- 사용자가 직접 표현하거나 명시적으로 채택한 research interest·goal·problem awareness만 사용했는가?
- 각 connection에 구체적인 Paper anchor와 기술적인 연결 방식이 있는가?
- 각 connection이 사용자 연구 방향에서 수행하는 역할과 실제 directional value가 있는가?
- Questions, Limitations와 Final Summary를 반복하지 않고 필요한 경우 참조만 했는가?
- 단순한 흥미 표현, 승인되지 않은 GPT 제안과 generic career statement를 제외했는가?
- 연결이 없을 때 억지로 만들지 않고, 기존 기록은 새로운 후보가 없다는 이유로 덮어쓰지 않았는가?
- Final Summary를 사용자의 명시적 완독과 마지막 본문 section까지의 checkpoint evidence가 모두 확인된 뒤 작성했는가?
- 완독 전에 Final Summary 일부 field를 채우거나 full-paper source synthesis 결과만으로 미리 작성하지 않았는가?
- Final Summary의 Paper claim은 첨부 PDF의 직접 근거만 사용했는가?
- Main Claim / Result를 하나로 제한하고 이를 직접 지지하는 evidence 또는 synthesis basis만 1~3개 선별했는가?
- Evidence의 baseline, workload, precision, evaluation method와 scope 중 claim 해석에 필요한 조건을 보존했는가?
- Overview/review paper에 존재하지 않는 신규 실험 결과를 만들지 않고 실제 synthesis basis를 기록했는가?
- Detailed Results를 복사하거나 evidence보다 넓은 claim을 만들지 않았는가?
- `내가 기억할 한 문장`을 사용자 대화에서 확인하지 않고 GPT가 대신 만들지 않았는가?
- 완독 사실을 사용자의 전체 이해나 mastery evidence로 확대하지 않았는가?
- Architecture와 Method의 모든 사실이 첨부 PDF에서 직접 확인되었는가?
- 논문에 없거나 근거가 부족한 field를 `논문에서 언급되지 않음`으로 표시했는가?
- 일반 지식, 다른 논문, GPT의 추론 또는 구조적 개연성으로 source-grounded field를 채우지 않았는가?
- 새로운 architecture·circuit·structure를 figure·subfigure 또는 이름이 붙은 구조별로 분리했는가?
- Problem, Key Idea, Architecture, Method, Experiments, Results, Trade-offs와 Paper-Reported Limitations의 source synthesis를 사용자의 읽기 범위나 이해 evidence로 기록하지 않았는가?
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
