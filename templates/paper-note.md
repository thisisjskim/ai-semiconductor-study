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

이 subsection만 사용자의 학습과 대화를 따라간다. 논문을 처음 받았을 때 자동으로 만들지 않는다. 사용자가 limitation을 직접 제기한 경우에만 후보로 수집하고, 단순한 질문은 limitation으로 확정하지 않고 `## 11. Questions`에 유지한다. GPT가 사용자의 발언을 확대하거나 새로운 limitation을 만들어서는 안 된다. 사용자의 표현을 가능한 한 보존하고, 학습 세션을 마무리할 때 이번 대화에서 확인된 후보만 Paper Note update안에 반영한다.

#### {User Observation}

- 사용자가 지적한 limitation:
- Related Architecture / Method:
- 사용자가 근거로 사용한 paper content:
- Paper에서 직접 확인된 내용:
- 추가 확인이 필요한 부분:

## 11. Questions

### 이해를 위한 질문

-

### 비판적 질문

-

### 후속 연구 질문

-

## 12. Connection to My Research Interest

이 논문이 NPU architecture, memory architecture, PIM/CIM 및 KAIST SSL Lab 개별연구 목표와 어떻게 연결되는가?

- 흥미로운 점:
- 더 탐구하고 싶은 부분:
- 다른 논문과의 연결:
- 가능한 research direction:

## 13. Final Summary

부분 분석 중이면 확인된 항목만 작성하고 나머지는 `아직 분석하지 않음`으로 둔다.

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
- 새롭게 발생한 질문:
- Bridge 변화:
- 종료 당시 Resume Point:

## 사용자 분석 근거

대화에서 사용자가 직접 설명하거나 비교하거나 질문한 내용을 가능한 한 원문 그대로 보존한다. 사용자의 설명이 아직 없으면 `아직 기록되지 않음`으로 표시한다.
