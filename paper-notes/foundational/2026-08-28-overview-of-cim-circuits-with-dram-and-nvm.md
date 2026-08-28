# Paper Note: An Overview of Computing-in-Memory Circuits With DRAM and NVM

## Metadata

- Title: An Overview of Computing-in-Memory Circuits With DRAM and NVM
- Document type: paper-note
- Paper type: foundational
- Venue / Year: IEEE Transactions on Circuits and Systems II: Express Briefs / 2024
- Authors: Sangjin Kim, Hoi-Jun Yoo
- Paper link: https://doi.org/10.1109/TCSII.2023.3333851
- Started: 2026-08-28
- Checkpoint recorded at: 2026-08-28T04:59:38Z
- Related notes: learning-logs/2026/08/2026-08-23-memory-wall-analog-cim-fundamentals.md; learning-logs/2026/08/2026-08-24-pim-cim-tiling-roofline-foundations.md

## 1. Citation

S. Kim and H.-J. Yoo, “An Overview of Computing-in-Memory Circuits With DRAM and NVM,” IEEE Transactions on Circuits and Systems II: Express Briefs, vol. 71, no. 3, pp. 1626–1631, Mar. 2024. doi: 10.1109/TCSII.2023.3333851.

## 2. Reading Checkpoint

- Resume Point: Introduction, PDF page 1 — Introduction을 읽기 직전. 다음에는 Introduction 첫 문단부터 읽고, 사용자가 읽은 범위까지만 이해를 점검한다.

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

### 별도로 이어가는 선수지식

없음.

## 4. Problem

아직 분석하지 않음.

## 5. Motivation and Prior-Work Gap

아직 분석하지 않음.

## 6. Prerequisites

| Prerequisite | 현재 상태 | 필요한 보충 |
| --- | --- | --- |
| DRAM leakage / refresh | 논문 읽기에 충분 | 이후 DRAM-CIM section에서 필요한 범위만 확장 |
| NVM resistance-based computation | 논문 읽기에 충분한 기초 | 이후 NVM-CIM section에서 실제 circuit example과 함께 확장 |
| NVM non-linearity / low signal margin | 논문 읽기에 충분한 기초 | later section에서 실제 signal path와 연결 |

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

아직 분석하지 않음.

| Gain | Cost / Trade-off | Evidence |
| --- | --- | --- |
| 아직 분석하지 않음 | 아직 분석하지 않음 | 아직 분석하지 않음 |

## 13. Limitations

### Authors' Limitations

아직 분석하지 않음.

### My Observations

아직 분석하지 않음.

## 14. Questions

### 이해를 위한 질문

- Abstract의 “impacting efficiency”는 DRAM leakage/refresh가 energy와 throughput overhead를 만든다는 의미로 이해했다.
- NVM의 low signal margin과 non-linearity는 이후 NVM-CIM section에서 실제 circuit example과 연결해 확인할 필요가 있다.

### 비판적 질문

아직 분석하지 않음.

### 후속 연구 질문

아직 분석하지 않음.

## 15. Connection to My Research Interest

현재는 Abstract까지 읽은 상태라 아직 분석하지 않음.

- 흥미로운 점: DRAM-CIM과 NVM-CIM이 각각 memory technology의 장점과 고유한 computation challenge를 동시에 가진다는 점
- 더 탐구하고 싶은 부분: 실제 circuit/datapath가 leakage, non-linearity, low signal margin을 어떻게 다루는지
- 다른 논문과의 연결: 아직 분석하지 않음
- 가능한 research direction: 아직 분석하지 않음

## 16. Final Summary

부분 분석 중이며 확인된 항목만 기록한다.

### Problem

아직 분석하지 않음.

### Key Idea

아직 분석하지 않음.

### Architecture

아직 분석하지 않음.

### Main Result

아직 분석하지 않음.

### Main Trade-off

아직 분석하지 않음.

### Limitation

아직 분석하지 않음.

### 내가 기억할 한 문장

아직 분석하지 않음.

## 17. Reading Session History

### 2026-08-28

- 읽은 범위: Abstract
- 이해한 내용: CIM의 energy-efficiency motivation, SRAM-CIM이 prevalent한 가운데 DRAM/NVM-CIM이 다시 주목받는 연구 흐름, DRAM-CIM의 leakage/refresh challenge, NVM-CIM의 non-linearity/low signal margin challenge
- 새롭게 발생한 질문: DRAM refresh가 efficiency에 주는 구체적 영향, NVM의 resistance-based computation에서 non-linearity와 low signal margin이 발생하는 구체적 mechanism
- Bridge 변화: DRAM leakage/refresh와 NVM non-linearity/low signal margin을 논문 안에서 해결한 선수지식으로 기록. 별도 Learning Log로 승격하지 않음.
- 종료 당시 Resume Point: Introduction, PDF page 1 — Introduction을 읽기 직전

## 사용자 분석 근거

> "CIM 은 ML, AI 를 학습하는데 있어서 energy를 효율적으로 사용할 수 있는 해법으로 제시되었다."

> "DRAM은 current leakage, refresh issue 등이 많이 발생함"

> "NVM은 low signal margins, non-linear characteristics 라는 단점이 많이 발생한다."

> "DRAM-CIM은 current leakage, refresh issue 등의 문제이고, NVM-CIM은 resistance를 통해 값을 저장하기 때문에, resistance 회로가 linear 하지 않아서 발생하는 문제 그리고 low signal margin 즉, 두 신호를 구분하는데에 어려움이 있기 때문임."

사용자와의 문답을 통해 연구 흐름은 “과거 DRAM/NVM-CIM에서 최근 SRAM-CIM으로 이동”이라기보다 “SRAM-CIM이 널리 연구되는 가운데 DRAM/NVM-CIM의 장점 때문에 다시 관심이 증가”하는 방향으로 수정되었다. NVM non-linearity는 “resistance 자체가 원래 non-linear”라는 일반화가 아니라 resistance-based computation과 주변 circuit의 non-ideal transfer 특성에서 나타날 수 있는 문제로 수정해 이해했다.
