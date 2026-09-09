# Paper Note: {Paper Title}

## Metadata

- Title:
- Document type: paper-note
- Paper type: foundational | ssl-lab | related
- Venue / Year:
- Authors:
- Paper link:
- Started: YYYY-MM-DD
- Checkpoint recorded at: {GitHub Actions가 Issue created_at으로 자동 설정}
- Related notes: 없음

## 1. Reading Checkpoint

- Resume Point:

`Resume Point`는 다음 세션에서 재개할 section, PDF page, figure·table·equation 또는 문장 시작 부분과 아직 확인해야 할 내용을 함께 기록한다.

## 2. Prerequisite Bridge

### 논문 안에서 해결한 선수지식

사용자가 PB 또는 Prerequisite Bridge에 남기도록 명시적으로 요청했거나 GPT의 제안에 동의한 개념만 기록한다. 질문·설명·오해 수정이 있었다는 이유만으로 자동 추가하지 않는다. Learning Log를 별도로 만들지 않고 현재 논문 안에서 해결한 개념을 기록하며, 사용자의 자기 설명이 확인되지 않았다면 AI의 설명을 사용자의 이해로 바꾸지 말고 `사용자 자기 설명: 아직 확인하지 않음`으로 표시한다.

#### {Concept}

- 등장 위치:
- 논문에서 필요한 이유:
- 실제 정의:
- 사용자의 이해:

### 별도로 이어가는 선수지식

별도 Learning Log로 학습하는 개념을 기록한다. `studying`은 Paper Note 전체에서 최대 하나만 허용하며, 저장 시 실제로 존재하는 Learning Log 경로가 하나 이상 필요하다.

#### {Concept}

- Status: studying | paused | sufficient-for-paper
- 논문에서 필요한 이유:
- 이 논문에 충분한 기준:
- Learning Logs:
  - 없음

## 3. Problem

Problem부터 Results, Trade-offs와 Paper-Reported Limitations까지 논문의 내용을 기록하는 field는 현재 conversation에 첨부되어 PDF Source Gate를 통과한 원문에서 직접 확인한 내용만 작성한다. 문맥상 그럴듯하거나 일반 지식으로 예상할 수 있어도 GPT가 원인, 동작, 장점, 한계 또는 저자의 의도를 추론해 채우지 않는다. 특정 field의 내용을 논문에서 찾을 수 없으면 추측하거나 빈칸으로 두지 말고 정확히 `논문에서 언급되지 않음`으로 표시한다. GPT 또는 사용자의 해석은 허용된 observation, question, research-interest와 사용자 분석 근거 영역에만 출처를 구분해 기록한다.

**Problem being addressed:**

**Limitations of existing approaches:**

**Why this problem matters:**

## 4. Key Idea

**Proposed approach:**

**Key mechanism:**

**What is novel or different:**

## 5. Architecture

이 section은 PDF Source Gate를 통과한 뒤 ChatGPT가 논문 전체의 architecture 설명, figure, caption과 본문 참조를 확인해 바로 작성하는 paper-source synthesis다. 사용자가 해당 범위를 읽을 때까지 기다리지 않으며, 이 내용을 사용자의 이해 evidence로 기록하지 않는다. 각 field는 논문이 직접 제공한 내용만 기록하고, 근거가 없거나 부족하면 `논문에서 언급되지 않음`으로 표시한다.

### Overall Architecture

- 목적과 system context:
- 전체 구성과 hierarchy:
- End-to-end operation / dataflow:

### {Architecture Family 또는 System Level}

논문이 제안하거나 새롭게 사용하는 architecture, circuit, cell 또는 structure를 figure·subfigure 또는 이름이 붙은 구조별로 나눈다. Overview/review paper는 먼저 architecture family로 묶는다. 서로 다른 구성이나 동작을 보이는 subfigure는 각각 분리하고, 같은 구조를 반복 설명하는 figure는 한 항목에 근거 위치를 함께 적는다. Result plot, dataset 예시와 배경 설명용 figure는 architecture를 설명하는 경우가 아니면 포함하지 않는다.

#### {Figure N(a) 또는 Structure Name}

- 근거 위치: Section / PDF p. / Figure
- 논문 내 역할:
- Main Structure (Components):
- Operation Overview:
- Data / Signal Flow:
- Benefits:
- Challenges / Trade-offs:
- 논문이 제공하지 않은 세부사항:

각 항목은 figure caption만이 아니라 연결된 본문 설명까지 확인해 작성한다. 논문에 직접 명시되지 않은 연결 관계, 회로 동작, 장점, 한계 또는 저자의 의도를 GPT가 추론해 채우지 않는다. 합리적으로 추론할 수 있는 내용도 이 section에는 넣지 않으며, 해당 field에는 `논문에서 언급되지 않음`을 기록한다.

## 6. Method

이 section은 `## 5. Architecture`에서 나눈 architecture family와 structure의 heading, 이름과 순서를 그대로 따른다. Architecture에서는 structure의 구성과 operation overview를 설명하고, 여기서는 해당 structure가 수행하는 operation의 원리와 절차를 논문이 설명한 범위 안에서 자세히 기록한다.

Operation은 MAC에 한정하지 않는다. 논문에 따라 arithmetic operation, logic operation, memory operation, data movement, sensing, conversion, control 또는 algorithmic procedure를 다룰 수 있다. 논문에 존재하지 않는 method나 단계를 GPT가 만들어 내지 않는다.

### {Architecture Family 또는 System Level}

#### {Figure N(a) 또는 Structure Name}

- Architecture reference:
- Method purpose:
- Input / Initial state:
- Core operation:
- Operation mechanism:
- Output / State change:
- Required conditions or assumptions:
- Benefits:
- Limitations / Trade-offs:
- 근거 위치: Section / PDF p. / Figure / Equation

각 field는 첨부 PDF의 본문, figure, caption, table 또는 equation에서 직접 확인한 내용만 작성한다. 논문이 특정 field를 설명하지 않거나 근거가 충분하지 않으면 빈칸을 임의로 보완하지 말고 정확히 `논문에서 언급되지 않음`으로 표시한다. 일반 지식, 다른 논문, GPT의 추론 또는 구조에서 유추한 인과관계를 Method의 사실처럼 기록하지 않는다.

## 7. Experiments

실험 환경과 평가 방법을 정리한다.

- Baseline:
- Workloads / Models:
- Dataset:
- Hardware configuration:
- Metrics:
- Simulation / Measurement methodology:

## 8. Results

주요 결과를 정리한다.

- Performance:
- Energy / Efficiency:
- Area / Cost:
- Accuracy:
- Other:

논문의 주장과 실제 result가 어떻게 연결되는지 확인한다.

## 9. Trade-offs

이 section은 PDF Source Gate를 통과한 뒤 ChatGPT가 첨부 PDF 전체를 확인해 바로 작성하는 paper-source synthesis다. 사용자의 학습 진도를 기다리지 않는다.

논문의 구체적인 structure 또는 approach별로 얻는 이점과 그에 따라 발생하는 cost를 직접 연결한다. Trade-off row는 논문이 동일한 설계 선택에 대한 `Benefit (Gain)`과 `Trade-off / Cost`를 모두 설명하고 둘의 관계를 직접 연결하며 PDF 근거 위치를 제시할 수 있을 때만 만든다. GPT가 서로 떨어진 장점과 단점을 임의로 조합하지 않는다. Cost만 제시되고 대응하는 gain이 없으면 Trade-off로 선정하지 않고, capability 또는 applicability의 직접적인 경계라면 `## 10. Limitations`의 후보로 검토한다.

한 행에는 하나의 structure 또는 approach만 기록한다. Gain–Cost 관계 전체는 Trade-offs에만 기록하고 Limitations에 반복하지 않는다. Trade-off와 별개인 residual hard boundary를 논문이 직접 명시한 경우에만 그 별도 경계를 Limitations에 기록한다. 조건을 만족하는 trade-off가 논문 전체에 없으면 표를 억지로 채우지 말고 `논문에서 언급되지 않음`으로 표시한다.

| Structure / Approach | Benefit (Gain) | Trade-off / Cost | Evidence |
| --- | --- | --- | --- |
|  |  |  |  |

## 10. Limitations

`Paper-Reported Limitations`는 PDF Source Gate를 통과한 뒤 ChatGPT가 첨부 PDF 전체를 확인해 바로 작성한다. 사용자의 학습 진도를 기다리지 않는다. Architecture와 Method의 모든 challenge나 Trade-off를 반복하지 않고, 논문이 capability, applicability 또는 claim의 경계로 직접 제시한 내용만 선정한다.

### Paper-Reported Limitations

다음 조건을 모두 만족하는 항목만 기록한다.

1. 논문이 limitation, constraint 또는 지원 범위의 경계를 직접 설명한다.
2. 영향을 받는 structure, method, system 또는 paper claim을 특정할 수 있다.
3. 지원 operation, workload, precision, accuracy, scalability, reliability, operating condition, hardware feasibility 또는 claim의 유효 범위를 실제로 제한한다.
4. 단순한 Gain–Cost 관계가 아니며 Trade-offs에 같은 내용이 없다.
5. PDF 근거 위치를 제시할 수 있다.

논문이 단순히 `challenge`라고 표현했지만 제한되는 capability나 applicability를 설명하지 않았다면 Limitation으로 승격하지 않는다. 모든 structure에 limitation을 의무적으로 만들지 않으며, 해당되는 항목만 생성한다. 특정 field의 내용이 없거나 근거가 부족하면 `논문에서 언급되지 않음`으로 표시한다. 조건을 만족하는 Paper-Reported Limitation이 하나도 없으면 이 subsection 전체에 `논문에서 언급되지 않음`으로 기록한다.

#### Structure-specific Capability / Applicability Limits

##### {Architecture Family — Figure N(a) 또는 Structure Name}

- Related Architecture / Method:
- Limitation:
- Limited capability or applicability:
- Applicable condition:
- Consequence:
- 근거 위치: Section / PDF p. / Figure / Table

#### System- or Paper-level Capability / Applicability Limits

##### {Limitation Name}

- Affected scope:
- Limitation:
- Limited capability or applicability:
- Applicable condition:
- Consequence:
- 근거 위치: Section / PDF p. / Figure / Table

### User-Identified Limitations

이 subsection은 사용자의 학습과 대화를 따라간다. 논문을 처음 받았을 때 자동으로 만들지 않는다. 사용자가 limitation을 직접 제기한 경우에만 후보로 수집하고, 단순한 질문은 limitation으로 확정하지 않고 `## 11. Questions`에 유지한다. GPT가 사용자의 발언을 확대하거나 새로운 limitation을 만들어서는 안 된다. 사용자의 표현을 가능한 한 보존하고, 학습 세션을 마무리할 때 이번 대화에서 확인된 후보만 Paper Note update안에 반영한다.

#### {User Observation}

- 사용자가 지적한 limitation:
- Related Architecture / Method:
- 사용자가 근거로 사용한 paper content:
- Paper에서 직접 확인된 내용:
- 추가 확인이 필요한 부분:

## 11. Questions

이 section은 **Conversation-derived section**이다. 첨부 PDF만을 읽어 바로 작성하는 **Paper-source immediate sections**인 Architecture, Method, Trade-offs, Paper-Reported Limitations와 명확히 구분한다. Questions의 질문 후보와 업데이트 근거는 실제 사용자–ChatGPT 학습 대화에서만 발생하며, 논문을 처음 받았다는 이유나 PDF 전체를 분석했다는 이유만으로 작성하거나 업데이트하지 않는다. 학습 세션을 마무리할 때 대화를 검토하고, 모든 질문이 아니라 아래 Question Selection Gate를 모두 통과한 질문만 반영한다. GPT가 사용자가 하지 않은 질문을 만들지 않는다. GPT가 제안한 질문은 사용자가 명시적으로 받아들여 실제로 탐구한 경우에만 후보가 된다.

### Question Selection Gate

1. **Origin Gate:** 사용자가 실제로 질문했거나, GPT가 제안한 질문을 사용자가 명시적으로 채택해 탐구했는가?
2. **Paper Grounding Gate:** 질문이 Problem, Key Idea, Architecture, Method, Experiments, Results, Trade-offs, Limitations, 특정 figure·table·equation·claim 또는 논문 이해에 필요한 핵심 prerequisite와 직접 연결되는가?
3. **Learning Value Gate:** 질문이 핵심 이해의 막힘을 해소하거나, 의미 있는 오해를 수정하거나, 논문 내 개념·section을 연결하거나, claim·evidence·assumption·comparison을 평가하거나, 구체적인 후속 연구 방향을 만드는가?
4. **Persistence Gate:** 답, 해결 과정 또는 남은 불확실성을 다음 세션에서 복구할 가치가 있는가?
5. **Deduplication Gate:** 기존 질문의 단순 반복이나 표현 변경이 아닌가? 같은 질문이 발전한 경우 새 항목을 만들지 않고 기존 기록에 통합한다.

단순 용어 뜻을 즉시 확인하고 이후 이해에 영향이 없었던 질문, 기술 의미를 바꾸지 않는 번역·문법 질문, 학습 절차나 기록 방식에 관한 meta 질문, 학습 영향이 없는 단순 정보 조회는 기록하지 않는다.

각 질문은 사용자의 표현을 가능한 한 보존한다. Paper의 직접 답, GPT의 보충 설명, 사용자의 해석이나 hypothesis를 서로 구분하며, GPT가 설명했다는 사실만으로 사용자가 이해한 것으로 기록하지 않는다. Paper에서 답을 찾을 수 없으면 추론으로 채우지 않고 `논문에서 언급되지 않음`이라고 표시한다. 대화에서 해결 과정이나 사용자 해석이 확인되지 않은 field는 추정하지 않고 `대화에서 확인되지 않음`으로 표시한다. 해당 category에 gate를 통과한 질문이 없으면 질문 항목을 만들지 않고 `선정된 질문 없음`으로 표시한다.

### 이해를 위한 질문

핵심 mechanism, prerequisite, 개념 간 연결 또는 이후 해석을 막는 오해를 해결한 질문만 기록한다.

#### {Question Title}

- 사용자의 질문:
- 질문이 발생한 위치 또는 맥락:
- 선정 이유:
- 해결 과정:
- 해결하며 알게 된 내용:
- 해결 상태: resolved | partially-resolved | unresolved
- 해결하지 못한 부분: 해결된 경우 `해당 없음`; Paper에 답이 없으면 `논문에서 언급되지 않음`과 남은 확인 사항을 함께 기록
- 해결에 사용한 근거:
  - Paper direct evidence:
  - GPT supplementary explanation:
  - User interpretation / hypothesis:

### 비판적 질문

논문의 claim, evidence, assumption, comparison, 적용 범위 또는 평가 타당성을 검토하는 데 실제 영향을 준 질문만 기록한다.

#### {Question Title}

- 사용자의 질문:
- 질문이 발생한 위치 또는 맥락:
- 선정 이유:
- 해결 과정:
- 해결하며 알게 된 내용:
- 해결 상태: resolved | partially-resolved | unresolved
- 해결하지 못한 부분: 해결된 경우 `해당 없음`; Paper에 답이 없으면 `논문에서 언급되지 않음`과 남은 확인 사항을 함께 기록
- 해결에 사용한 근거:
  - Paper direct evidence:
  - GPT supplementary explanation:
  - User interpretation / hypothesis:

### 후속 연구 질문

논문에서 확인된 한계, 열린 문제 또는 비교 필요성을 구체적인 검증 대상이나 다음 research action으로 발전시킨 질문만 기록한다.

#### {Question Title}

- 사용자의 질문:
- 질문이 발생한 위치 또는 맥락:
- 선정 이유:
- 해결 과정:
- 해결하며 알게 된 내용:
- 해결 상태: resolved | partially-resolved | unresolved
- 해결하지 못한 부분: 해결된 경우 `해당 없음`; Paper에 답이 없으면 `논문에서 언급되지 않음`과 남은 확인 사항을 함께 기록
- 해결에 사용한 근거:
  - Paper direct evidence:
  - GPT supplementary explanation:
  - User interpretation / hypothesis:

## 12. Connection to My Research Direction

이 section은 **Conversation-derived section**이다. 사용자가 실제 학습 대화에서 표현한 research interest·goal·problem awareness와 논문의 구체적인 element 사이에서 확인된 연결만 학습 세션을 마무리할 때 기록한다. 논문을 받거나 PDF 전체를 분석했다는 이유만으로 작성하지 않는다. GPT가 연결 후보를 제안할 수는 있지만, 사용자가 명시적으로 받아들여 실제로 탐구하기 전에는 기록하지 않는다.

### Research Connection Gate

다음 조건을 모두 만족하는 connection만 기록한다.

1. **User-Origin Gate:** 사용자가 research interest·goal·problem awareness를 직접 표현했거나, GPT가 제안한 연결을 명시적으로 받아들여 실제로 탐구했는가?
2. **Paper-Anchor Gate:** 연결되는 claim, architecture, method, result, trade-off, limitation 또는 question과 그 Paper 근거 위치를 특정할 수 있는가?
3. **Mechanism Gate:** 단순한 keyword 유사성이 아니라 사용자 관심과 Paper element가 왜 연결되는지 기술적으로 설명할 수 있는가?
4. **Directional-Value Gate:** 이 연결이 research framing, paper comparison, anchor-paper 선정, portfolio evidence 또는 후속 연구 방향 중 하나에 실제 영향을 주는가?
5. **Non-Duplication Gate:** Questions, Limitations, Final Summary의 내용을 반복하지 않고, 이 논문이 사용자 연구 방향에서 수행하는 역할을 설명하는가?

통과한 connection이 없으면 새 Paper Note에는 connection placeholder를 만들지 않고 `확인된 연구 연결 없음`으로 표시한다. 기존 Paper Note에서 이번 세션에 새로운 connection이 없으면 기존 기록을 보존하고 이 section을 변경하지 않는다. Paper 근거가 없으면 `논문에서 언급되지 않음`, 사용자 대화 근거가 없으면 `대화에서 확인되지 않음`으로 표시하며 연결을 추론해 채우지 않는다.

### {Connection Title}

- 사용자가 표현한 research interest 또는 goal:
- 연결되는 Paper element:
- 연결 근거 위치: Section / PDF p. / Figure / Table / Equation
- 연결 방식:
- 이 논문이 내 연구 방향에서 수행하는 역할:
- 기존 Questions / Limitations와의 관계:
- 연결의 경계 또는 아직 확인되지 않은 부분:
- 향후 활용: comparison paper | anchor paper | portfolio evidence | research framing | 기타 사용자 확인 내용

## 13. Final Summary

이 section은 **Reading-completion synthesis**다. 사용자가 논문 본문을 끝까지 읽었다고 명시하고 Reading Checkpoint와 Reading Session History에서 마지막 본문 section까지의 읽기 완료가 확인된 경우에만 마지막 정리로 작성한다. 논문을 받았거나 GPT가 PDF 전체를 분석했다는 이유만으로 미리 작성하지 않는다. 완독 전에는 일부 field를 먼저 채우지 않고 Final Summary 전체를 `아직 분석하지 않음`으로 둔다.

완독 후에도 Paper claim은 PDF Source Gate를 통과한 논문의 직접 근거만 사용한다. 사용자의 해석이나 기억할 한 문장은 실제 대화에서 확인된 내용과 구분해 기록하며 GPT가 임의로 사용자의 이해나 결론을 만들어서는 안 된다. Final Summary 작성은 사용자가 논문을 끝까지 읽었다는 사실만 나타내며, 모든 내용을 완전히 이해하거나 검증했다는 evidence로 사용하지 않는다.

### Problem

-

### Key Idea

-

### Architecture

-

### Main Result

-

### Main Trade-off

-

### Limitation

-

### 내가 기억할 한 문장

-

## 14. Reading Session History

### YYYY-MM-DD

- 읽은 범위:
- 이해한 내용:
- Question Selection Gate를 통과한 질문과 해결 상태:
- Bridge 변화:
- 종료 당시 Resume Point:

## 사용자 분석 근거

대화에서 사용자가 직접 설명하거나 비교하거나 질문한 내용을 가능한 한 원문 그대로 보존한다. 사용자의 설명이 아직 없으면 `아직 기록되지 않음`으로 표시한다.
