# Paper Note: An Overview of Computing-in-Memory Circuits With DRAM and NVM

## Metadata

- Title: An Overview of Computing-in-Memory Circuits With DRAM and NVM
- Document type: paper-note
- Paper type: foundational
- Venue / Year: IEEE Transactions on Circuits and Systems II: Express Briefs / 2024
- Authors: Sangjin Kim, Hoi-Jun Yoo
- Paper link: https://doi.org/10.1109/TCSII.2023.3333851
- Started: 2026-08-28
- Checkpoint recorded at: 2026-08-28T06:51:52Z
- Related notes: learning-logs/2026/08/2026-08-23-memory-wall-analog-cim-fundamentals.md; learning-logs/2026/08/2026-08-24-pim-cim-tiling-roofline-foundations.md

## 1. Citation

S. Kim and H.-J. Yoo, “An Overview of Computing-in-Memory Circuits With DRAM and NVM,” IEEE Transactions on Circuits and Systems II: Express Briefs, vol. 71, no. 3, pp. 1626–1631, Mar. 2024. doi: 10.1109/TCSII.2023.3333851.

## 2. Reading Checkpoint

- Resume Point: Introduction, PDF page 1 — SRAM-CIM의 장점과 세 가지 한계(transistor/area overhead, 1-bit weight density, volatility)를 읽은 뒤, “As the field of CIM progresses, these limitations underscore…” 문장부터 재개한다. 사용자가 읽은 범위까지만 이해를 점검한다.

## 3. Prerequisite Bridge

### 논문 안에서 해결한 선수지식

#### DRAM leakage / refresh

- 등장 위치: Abstract
- 논문에서 필요한 이유: DRAM-CIM의 효율과 정확도에 영향을 주는 대표 challenge를 이해하기 위해 필요하다.
- 사용자의 이해: DRAM-CIM은 current leakage와 refresh issue가 발생하며, leakage로 저장 charge가 줄어 refresh가 필요하고 이것이 efficiency/throughput overhead로 이어질 수 있다는 방향을 이해했다.

#### NVM non-linearity / low signal margin

- 등장 위치: Abstract
- 논문에서 필요한 이유: NVM-CIM의 resistance-based computation에서 정확도 challenge가 왜 생기는지 이해하기 위해 필요하다.
- 사용자의 이해: NVM은 resistance를 통해 값을 저장하고 이를 computation에 이용하며, 실제 회로의 non-ideal 특성 때문에 출력 signal이 ideal하게 linear하지 않을 수 있고 low signal margin 때문에 서로 다른 신호를 구분하기 어려울 수 있다는 수준까지 확인했다.

#### SRAM pushed-rule / bitcell density

- 등장 위치: Introduction, PDF page 1
- 논문에서 필요한 이유: SRAM이 cross-coupled static storage의 안정성뿐 아니라 compact cell density 측면에서도 장점을 갖는다는 문장을 이해하기 위해 필요하다.
- 사용자의 이해: SRAM bitcell은 규칙적이고 반복적인 구조이므로 pushed-rule 기반의 더 tight한 layout 최적화가 가능하고, 그 결과 단위 면적당 더 많은 SRAM cell을 배치해 memory density를 높일 수 있다고 설명했다. bitcell과 bitline은 서로 다른 개념이며, 여기서 density는 bitcell density를 뜻한다는 점을 확인했다.

#### SRAM-CIM area overhead

- 등장 위치: Introduction, PDF page 1
- 논문에서 필요한 이유: SRAM 자체의 compact bitcell 장점과 SRAM-CIM에서의 transistor/area overhead가 왜 동시에 성립하는지 구분하기 위해 필요하다.
- 사용자의 이해: SRAM 자체는 pushed-rule로 compact할 수 있지만, SRAM-CIM에서는 기본 6T cell에 compute logic이 추가되어 unit MAC 기준 transistor 수와 area overhead가 증가할 수 있다고 이해했다. 두 진술은 비교 대상이 다르므로 모순이 아니라고 정리했다.

#### SRAM weight density / cross-coupled storage node

- 등장 위치: Introduction, PDF page 1
- 논문에서 필요한 이유: SRAM-CIM이 1 bit/cell 구조 때문에 multi-bit weight storage density에 제약을 받는 이유를 이해하기 위해 필요하다.
- 사용자의 이해: AI가 설명함. 사용자 자기 설명: 아직 확인하지 않음.

#### Event-driven application

- 등장 위치: Introduction, PDF page 1
- 논문에서 필요한 이유: SRAM의 volatility가 어떤 application context에서 불리한지 이해하기 위해 필요하다.
- 사용자의 이해: AI가 설명함. 사용자 자기 설명: 아직 확인하지 않음.

### 별도로 이어가는 선수지식

없음.

## 4. Problem

부분 분석 중.

현재까지 읽은 범위에서, SRAM-CIM은 안정적인 static storage와 효율적인 read/write, compact cell layout의 장점이 있지만 CIM 구현 시 추가 compute logic으로 transistor/area overhead가 커지고, 1 bit/cell 구조로 weight density가 제한되며, volatility 때문에 power-off 상태에서 data를 유지할 수 없다는 한계가 있다.

## 5. Motivation and Prior-Work Gap

부분 분석 중.

현재까지 읽은 범위에서, SRAM-CIM은 널리 연구되어 왔지만 transistor/area overhead, 1-bit weight storage density, volatility라는 한계가 있어 DRAM-CIM과 NVM-CIM 같은 대안 memory technology를 다시 검토할 동기가 형성된다.

## 6. Prerequisites

| Prerequisite | 현재 상태 | 필요한 보충 |
| --- | --- | --- |
| DRAM leakage / refresh | 논문 읽기에 충분 | 이후 DRAM-CIM section에서 필요한 범위만 확장 |
| NVM resistance-based computation | 논문 읽기에 충분한 기초 | 이후 NVM-CIM section에서 실제 circuit example과 함께 확장 |
| NVM non-linearity / low signal margin | 논문 읽기에 충분한 기초 | later section에서 실제 signal path와 연결 |
| SRAM pushed-rule / bitcell density | 사용자 자기 설명 확인됨 | 추가 보충 없음 |
| SRAM-CIM area overhead | 사용자 이해 확인됨 | 이후 DRAM/NVM-CIM과 비교 시 재사용 |
| SRAM weight density | 설명은 들었으나 자기 설명 미확인 | 필요하면 다음 reading turn에서 짧게 확인 |
| Event-driven application | 설명은 들었으나 자기 설명 미확인 | 필요하면 다음 reading turn에서 짧게 확인 |

## 7. Key Idea

아직 분석하지 않음.

> 한 문장 요약: 아직 분석하지 않음.

## 8. Architecture

아직 분석하지 않음.

- 주요 component: 아직 분석하지 않음
- Data path: 아직 분석하지 않음
- Control: 아직 분석하지 않음
- Memory organization: 아직 분석하지 않음
- Parallelism: 아직 분석하지 않음
- Dataflow: 아직 분석하지 않음

### Architecture Walkthrough

아직 분석하지 않음.

## 9. Method

아직 분석하지 않음.

## 10. Experiments

아직 분석하지 않음.

- Baseline: 아직 분석하지 않음
- Workloads / Models: 아직 분석하지 않음
- Dataset: 아직 분석하지 않음
- Hardware configuration: 아직 분석하지 않음
- Metrics: 아직 분석하지 않음
- Simulation / Measurement methodology: 아직 분석하지 않음

## 11. Results

아직 분석하지 않음.

- Performance: 아직 분석하지 않음
- Energy / Efficiency: 아직 분석하지 않음
- Area / Cost: 아직 분석하지 않음
- Accuracy: 아직 분석하지 않음
- Other: 아직 분석하지 않음

## 12. Trade-offs

부분 분석 중.

| Gain | Cost / Trade-off | Evidence |
| --- | --- | --- |
| SRAM의 stable static storage와 compact bitcell layout | SRAM-CIM에서는 compute logic 추가로 transistor/area overhead 증가 | Introduction, PDF page 1 |
| SRAM의 reliable 1-bit storage | 1 bit/cell 구조로 multi-bit weight density 제약 | Introduction, PDF page 1 |
| SRAM의 fast/low-power read-write 특성 | volatility로 power-off 상태에서 data 유지 불가 | Introduction, PDF page 1 |

## 13. Limitations

### Authors' Limitations

현재까지 읽은 범위에서 확인된 SRAM-CIM의 limitation:
- 추가 compute logic으로 인한 transistor count 및 area overhead
- 1 bit/cell 구조로 인한 weight density 제약
- volatility로 인한 long-term storage 및 event-driven application 제약

### My Observations

- SRAM 자체의 pushed-rule 기반 high cell density와 SRAM-CIM의 area overhead는 서로 모순이 아니라, bitcell 자체와 CIM 기능이 포함된 unit MAC의 비교 기준이 다르다는 점을 확인했다.

## 14. Questions

### 이해를 위한 질문

- Abstract의 “impacting efficiency”는 DRAM leakage/refresh가 energy와 throughput overhead를 만든다는 의미로 이해했다.
- NVM의 low signal margin과 non-linearity는 이후 NVM-CIM section에서 실제 circuit example과 연결해 확인할 필요가 있다.
- “high-density cells with pushed-rule”은 SRAM bitcell의 규칙적 layout을 더 tight하게 최적화해 단위 면적당 더 많은 cell을 배치한다는 의미로 이해했다.
- “limits the weight density because of cross-coupled storage node”는 1 bit/cell binary storage 구조가 multi-bit weight storage density를 제한한다는 의미로 설명을 들었으나, 사용자 자기 설명은 아직 확인하지 않았다.
- event-driven application은 필요할 때만 깨어나 동작하는 application context로 설명을 들었으나, 사용자 자기 설명은 아직 확인하지 않았다.

### 비판적 질문

아직 분석하지 않음.

### 후속 연구 질문

아직 분석하지 않음.

## 15. Connection to My Research Interest

현재는 Abstract와 Introduction 일부까지만 읽은 상태라 부분 분석 중.

- 흥미로운 점: SRAM-CIM은 안정성과 compact bitcell이라는 장점이 있지만, 실제 CIM 구현에서는 transistor/area overhead, weight density, volatility라는 별도의 trade-off가 생긴다는 점
- 더 탐구하고 싶은 부분: DRAM-CIM과 NVM-CIM이 SRAM-CIM의 어떤 한계를 보완하고 대신 어떤 새로운 circuit challenge를 만드는지
- 다른 논문과의 연결: 아직 분석하지 않음
- 가능한 research direction: 아직 분석하지 않음

## 16. Final Summary

부분 분석 중이며 확인된 항목만 기록한다.

### Problem

SRAM-CIM은 안정적인 storage와 compact cell의 장점이 있지만 CIM 구현 시 transistor/area overhead, 1 bit/cell weight density 제약, volatility라는 한계가 있다.

### Key Idea

아직 분석하지 않음.

### Architecture

아직 분석하지 않음.

### Main Result

아직 분석하지 않음.

### Main Trade-off

SRAM의 stable/compact storage 장점과 CIM 구현 시 area, weight density, volatility 비용이 공존한다.

### Limitation

현재까지는 SRAM-CIM의 transistor/area overhead, 1 bit/cell weight density, volatility를 확인했다.

### 내가 기억할 한 문장

현재까지: SRAM-CIM은 안정적이고 compact한 memory cell을 기반으로 하지만, CIM 기능을 넣으면 area와 weight density, volatility 측면에서 trade-off가 생긴다.

## 17. Reading Session History

### 2026-08-28

- 읽은 범위: Abstract 및 Introduction 일부 — SRAM-CIM의 장점과 세 가지 limitation까지
- 이해한 내용: CIM의 energy-efficiency motivation, SRAM-CIM이 prevalent한 가운데 DRAM/NVM-CIM이 다시 주목받는 연구 흐름, DRAM-CIM의 leakage/refresh challenge, NVM-CIM의 non-linearity/low signal margin challenge, SRAM의 cross-coupled static storage와 pushed-rule 기반 compact bitcell, SRAM-CIM의 transistor/area overhead와 1 bit/cell/volatility 한계
- 새롭게 발생한 질문: pushed-rule의 의미, bitcell과 bitline의 차이, SRAM 자체의 high density와 SRAM-CIM area overhead가 왜 모순이 아닌지, cross-coupled storage node가 weight density를 어떻게 제한하는지, event-driven application이 무엇인지
- Bridge 변화: pushed-rule/bitcell density와 SRAM-CIM area overhead는 사용자 설명으로 이해 확인. weight density와 event-driven application은 AI 설명까지 진행했으나 사용자 자기 설명은 아직 확인되지 않음.
- 종료 당시 Resume Point: Introduction, PDF page 1 — “As the field of CIM progresses, these limitations underscore…” 문장부터 재개

## 사용자 분석 근거

> "CIM 은 ML, AI 를 학습하는데 있어서 energy를 효율적으로 사용할 수 있는 해법으로 제시되었다."

> "DRAM은 current leakage, refresh issue 등이 많이 발생함"

> "NVM은 low signal margins, non-linear characteristics 라는 단점이 많이 발생한다."

> "DRAM-CIM은 current leakage, refresh issue 등의 문제이고, NVM-CIM은 resistance를 통해 값을 저장하기 때문에, resistance 회로가 linear 하지 않아서 발생하는 문제 그리고 low signal margin 즉, 두 신호를 구분하는데에 어려움이 있기 때문임."

> "pushed-rule layout 덕분에, 6T로 transistor 수가 많더라도, 일반 공정에 비해 더 tight하게 구조를 형성할 수 있음. SRAM은 정형화된 chip이기 때문에 transistor 사이의 거리를 더 좁히는 등의 공정 기법을 이용하여 같은 면적에 더 많은 transistor(SRAM)을 추가할 수 있기 때문임"

> "OK 이해했음 결국 SRAM의 정형화된 패턴 덕분에 pushed-rule 이라는 설계를 할 수 있고, 이 설계 덕분에 단위 면적당 더 많은 SRAM을 넣을 수 있어서 memory density가 증가한다고 이해하면 되는걸까"

> "이러한 장점이 있음에도, SRAM-CIM은 DRAM,NVM-CIM에 비해 약점이 존재한다. 먼저 SRAM은 6T로 구성된다. SRAM-CIM은 computing logic을 요구하는데 더 많은 transistor를 요구한다. 따라서 상대적으로 더 많은 transistor를 unit MAC이 고려해야한다. 추가로 1.4~2 배 정도 더 많은 영역이 요구된다."

사용자와의 문답을 통해 연구 흐름은 “과거 DRAM/NVM-CIM에서 최근 SRAM-CIM으로 이동”이라기보다 “SRAM-CIM이 널리 연구되는 가운데 DRAM/NVM-CIM의 장점 때문에 다시 관심이 증가”하는 방향으로 수정되었다. NVM non-linearity는 “resistance 자체가 원래 non-linear”라는 일반화가 아니라 resistance-based computation과 주변 circuit의 non-ideal transfer 특성에서 나타날 수 있는 문제로 수정해 이해했다. 또한 pushed-rule은 bitline이 아니라 bitcell density와 관련되며, SRAM 자체의 compactness와 SRAM-CIM의 compute area overhead는 비교 대상이 달라 동시에 성립할 수 있음을 확인했다.
