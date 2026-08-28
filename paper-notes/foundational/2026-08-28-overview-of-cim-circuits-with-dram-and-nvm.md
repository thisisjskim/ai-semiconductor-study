# Paper Note: An Overview of Computing-in-Memory Circuits With DRAM and NVM

## Metadata

- Title: An Overview of Computing-in-Memory Circuits With DRAM and NVM
- Document type: paper-note
- Paper type: foundational
- Venue / Year: IEEE Transactions on Circuits and Systems II: Express Briefs / 2024
- Authors: Sangjin Kim, Hoi-Jun Yoo
- Paper link: https://doi.org/10.1109/TCSII.2023.3333851
- Started: 2026-08-28
- Checkpoint recorded at: 2026-08-28T13:48:33Z
- Related notes: learning-logs/2026/08/2026-08-23-memory-wall-analog-cim-fundamentals.md; learning-logs/2026/08/2026-08-24-pim-cim-tiling-roofline-foundations.md

## 1. Citation

S. Kim and H.-J. Yoo, “An Overview of Computing-in-Memory Circuits With DRAM and NVM,” IEEE Transactions on Circuits and Systems II: Express Briefs, vol. 71, no. 3, pp. 1626–1631, Mar. 2024. doi: 10.1109/TCSII.2023.3333851.

## 2. Reading Checkpoint

- Resume Point: Section II. DRAM-CIM, A. 1T-1C DRAM — multiple-row activation을 이용한 bitwise Boolean operation과 cell-array internal bandwidth/data-movement 이점을 읽고 이해한 직후. 이어지는 1T-1C DRAM-CIM circuit technique 설명의 다음 문장부터 재개하며, 아직 읽지 않은 뒤 회로 세부는 미리 가정하지 않는다.

## 3. Prerequisite Bridge

### 논문 안에서 해결한 선수지식

#### DRAM leakage / refresh
- 등장 위치: Abstract, Introduction
- 논문에서 필요한 이유: DRAM-CIM의 효율과 정확도에 영향을 주는 대표 challenge를 이해하기 위해 필요하다.
- 사용자의 이해: DRAM cell은 capacitor charge로 data를 저장하며 leakage/noise로 charge가 손상될 수 있음을 이해했다. 일반 DRAM에서는 SA가 cell 신호를 binary 0/1로 sensing하지만, DRAM-CIM에서는 cell data가 computation에 직접 관여하므로 leakage/noise가 계산 결과에 영향을 줄 수 있다는 점까지 문답으로 수정·확인했다. DRAM-CIM이 반드시 SA를 사용하지 않는다는 뜻은 아님을 확인했다.

#### NVM non-linearity / low signal margin
- 등장 위치: Abstract, Introduction
- 논문에서 필요한 이유: NVM-CIM의 circuit-level challenge를 이해하기 위해 필요하다.
- 사용자의 이해: NVM의 resistance-related 저장/연산 특성과 circuit non-ideality가 non-linearity 및 low signal margin 문제로 연결될 수 있다는 수준까지 이해했다. 구체적인 발생 mechanism은 NVM-CIM section에서 확인하기로 했다.

#### SRAM pushed-rule / bitcell density
- 등장 위치: Introduction, PDF page 1
- 논문에서 필요한 이유: SRAM의 compact cell density 장점을 이해하기 위해 필요하다.
- 사용자의 이해: SRAM bitcell의 규칙적이고 반복적인 구조가 tight한 pushed-rule layout에 유리하고, 그 결과 단위 면적당 더 많은 SRAM bitcell을 배치할 수 있다고 자기 설명으로 확인했다.

#### SRAM-CIM area overhead
- 등장 위치: Introduction, PDF page 1
- 논문에서 필요한 이유: SRAM 자체의 compact bitcell과 SRAM-CIM의 compute-logic area overhead가 동시에 성립하는 이유를 이해하기 위해 필요하다.
- 사용자의 이해: 기본 SRAM cell에 compute logic이 추가되면서 unit MAC의 transistor/area overhead가 증가하며, pushed-rule에 의한 bitcell density와 비교 수준이 다르므로 모순이 아니라고 이해했다.

#### SRAM weight density / cross-coupled storage node
- 등장 위치: Introduction, PDF page 1
- 논문에서 필요한 이유: 1 bit/cell이 multi-bit weight storage density를 제한하는 이유를 이해하기 위해 필요하다.
- 사용자의 이해: AI가 설명함. 사용자 자기 설명: 아직 확인하지 않음.

#### Event-driven application
- 등장 위치: Introduction, PDF page 1
- 논문에서 필요한 이유: volatility가 power-off를 활용하는 application에서 왜 불리한지 이해하기 위해 필요하다.
- 사용자의 이해: NVM의 non-volatility와 power-off NN system을 학습하는 과정에서 event 발생 시 power-on하여 inference하고 다시 power-off하는 흐름과 연결해 설명을 들음. 사용자 자기 설명: 아직 확인하지 않음.

#### DRAM-dedicated process / eDRAM
- 등장 위치: Introduction, PDF page 1
- 논문에서 필요한 이유: DRAM이 high density와 logic-process integration이라는 서로 다른 구현 장점을 가질 수 있다는 문장을 이해하기 위해 필요하다.
- 사용자의 이해: DRAM-dedicated process는 pushed-rule과 동일한 개념이 아니라 fabrication process 자체를 DRAM에 최적화한 것이며 high density에 유리하다는 점을 문답으로 수정했다. eDRAM은 logic이 있는 die/process에 DRAM을 함께 집적하는 형태이며, logic compatibility는 logic을 더 빠르고 정확하게 계산한다는 뜻이 아니라 logic 공정/회로와 함께 집적하기에 호환된다는 뜻임을 확인했다. eDRAM은 on-chip capacity를 늘려 off-chip access를 줄일 가능성이 있지만 die-area/process/refresh trade-off가 있어 모든 DRAM을 eDRAM으로 대체할 수 있는 것은 아님을 이해했다.

#### NVM multi-level cell / initial data writing
- 등장 위치: Introduction, PDF page 1
- 논문에서 필요한 이유: NVM의 high density, low standby/system power 장점을 이해하기 위해 필요하다.
- 사용자의 이해: NVM은 여러 distinguishable storage level을 이용해 하나의 cell에 여러 bit를 표현할 수 있으며, 단순 high/low 두 상태만이면 1 bit라는 점까지 수정·확인했다. 또한 non-volatility로 power-off 후에도 weight가 유지되어 재기동 시 initial data writing을 줄이거나 제거할 수 있고, 이에 따른 data movement/write energy를 줄일 수 있다고 자기 설명했다.

#### NN inference와 NVM non-volatility
- 등장 위치: Introduction, NVM의 power-off state 관련 문장
- 논문에서 필요한 이유: power-off를 활용하는 NN system에서 NVM의 energy-efficiency 장점을 이해하기 위해 필요하다.
- 사용자의 이해: AI가 weight/activation, training/inference와 학습 완료 weight의 반복 사용을 최소 선수지식으로 설명함. 사용자 자기 설명: 아직 확인하지 않음.

#### DIMM / PNM buffer device
- 등장 위치: Section II-A 1T-1C DRAM
- 논문에서 필요한 이유: cell array를 직접 수정하지 않는 DRAM-side processing 접근인 PNM을 이해하기 위해 필요하다.
- 사용자의 이해: DIMM을 여러 DRAM chip과 관련 회로가 실장된 memory module로 이해했고, PNM은 DRAM cell array 자체보다 DIMM의 buffer device 같은 memory-near 영역에 computing logic을 배치하는 접근이라는 점을 질문을 통해 확인했다.

#### Bitwise operation
- 등장 위치: Section II-A 1T-1C DRAM
- 논문에서 필요한 이유: multiple-row activation으로 여러 BL에서 수행되는 Boolean computation을 이해하기 위해 필요하다.
- 사용자의 이해: bitwise operation은 여러 bit로 이루어진 데이터의 동일 위치 bit마다 AND/OR 등의 Boolean operation을 독립적으로 적용하는 것이라는 설명을 들은 뒤, 여러 BL을 통한 bitwise operation이 더 복잡한 Boolean operation을 도울 수 있다고 자기 설명했다.

#### DRAM internal bandwidth
- 등장 위치: Section II-A 1T-1C DRAM
- 논문에서 필요한 이유: cell-array-level CIM이 conventional read path보다 data movement를 더 줄일 수 있는 이유를 이해하기 위해 필요하다.
- 사용자의 이해: DRAM array 내부의 많은 cell/BL에 병렬 접근할 수 있는 능력을 internal bandwidth로 이해했고, cell array에서 일부 연산을 수행하면 많은 데이터를 외부 SRAM/register/MAC 쪽으로 이동시키는 양을 줄일 수 있다고 자기 설명했다. internal bandwidth가 단순히 DRAM 내부의 memory 이동 자체만을 뜻하지 않으며, external interface bandwidth 자체가 자동으로 증가한다는 의미도 아님을 확인했다.

### 별도로 이어가는 선수지식

없음.

## 4. Problem

부분 분석 중.

현재까지 읽은 범위에서, SRAM-CIM은 안정적 storage와 compact bitcell의 장점이 있지만 compute logic 추가에 따른 area overhead, 1 bit/cell weight density 제약, volatility가 있다. 이를 보완할 DRAM/NVM-CIM은 각각 높은 density 및 non-volatility 등의 장점이 있지만 DRAM의 leakage/noise와 NVM의 non-linearity/low signal margin이라는 새로운 circuit challenge를 갖는다. 특히 conventional 1T1C DRAM array를 직접 수정하는 비용이 크고, digital-PIM/PNM은 conventional sensing/read/data-transfer path가 남아 있어 cell-array-level CIM보다 data movement reduction에 한계가 있다.

## 5. Motivation and Prior-Work Gap

부분 분석 중.

SRAM-CIM의 한계 때문에 DRAM/NVM이 재검토된다. DRAM은 1T1C와 DRAM-dedicated process를 통한 high density, logic process에서 eDRAM 구현 가능성이라는 장점이 있고, NVM은 low standby power, multi-level cell, non-volatility로 인한 initial data writing 제거 가능성이 있다. 그러나 이러한 memory를 CIM에 사용할 때 DRAM leakage/noise와 NVM non-linearity/low signal margin이라는 fresh challenges가 생겨 새로운 circuits/datapaths가 필요하다.

1T1C DRAM에서는 기존 array를 크게 바꾸지 않는 digital-PIM/PNM도 연구됐지만, computation이 cell array에서 직접 이루어지지 않고 conventional sensing/read가 필요해 energy/latency improvement가 제한될 수 있다. 따라서 cell/BL의 내부 병렬성을 computation에 직접 활용하는 DRAM-CIM 접근을 살펴볼 동기가 생긴다.

## 6. Prerequisites

| Prerequisite | 현재 상태 | 필요한 보충 |
| --- | --- | --- |
| DRAM leakage / refresh / SA read | 논문 읽기에 충분 | Section II에서 실제 circuit과 연결 |
| NVM resistance / non-linearity / low signal margin | 논문 읽기에 충분한 기초 | Section III에서 실제 circuit example과 연결 |
| SRAM pushed-rule / area overhead | 사용자 이해 확인됨 | 추가 보충 없음 |
| SRAM weight density | AI 설명, 자기 설명 미확인 | 필요 시 짧게 확인 |
| Event-driven application | AI 설명, 자기 설명 미확인 | 필요 시 짧게 확인 |
| DRAM-dedicated process / eDRAM | 문답으로 이해 확인 | 이후 architecture 비교 시 재사용 |
| NVM MLC / non-volatility / initial writing | 사용자 자기 설명 확인됨 | Section III에서 구체적 device/circuit과 연결 |
| NN inference 기초 | AI 설명, 자기 설명 미확인 | 논문 진행에 필요한 경우만 보충 |
| DIMM / PNM | 문답으로 이해 확인 | 추가 보충 없음 |
| Bitwise operation | 사용자 설명으로 확인됨 | 구체 Boolean circuit은 다음 읽기 범위에서 확인 |
| DRAM internal bandwidth | 사용자 설명으로 확인됨 | 정량 비교는 논문 근거가 나올 때만 확장 |

## 7. Key Idea

부분 분석 중.

> 한 문장 요약: DRAM/NVM은 SRAM-CIM의 일부 한계를 보완할 수 있지만 각 memory의 비이상성이 새로운 CIM challenge를 만들며, 1T1C DRAM-CIM에서는 cell/BL의 내부 병렬성과 저장 data를 computation에 직접 활용해 conventional read/data movement overhead를 더 줄이는 접근이 가능하다.

## 8. Architecture

부분 분석 중 — Section II-A에서 확인한 범위만 기록한다.

- 주요 component: 1T1C DRAM cell array, WL, BL, SA, digital-PIM compute logic, PNM의 memory-near buffer/compute 영역
- Data path: conventional/digital-PIM은 cell → BL/SA sensing → digital data → compute 경로를 유지한다. cell-array-level DRAM-CIM은 multiple rows를 동시에 activate해 여러 cell의 저장 상태가 공통 BL에 함께 영향을 주도록 하고 이를 computation에 활용한다.
- Control: multiple-row activation이 Boolean computation의 핵심 control idea로 소개됨. 구체 control circuit은 아직 분석하지 않음.
- Memory organization: 1T1C DRAM array의 여러 rows가 BL을 공유하는 구조를 활용한다.
- Parallelism: 여러 BL에서 bitwise operation을 병렬적으로 수행할 수 있다는 점까지 이해함.
- Dataflow: cell array 내부에서 일부 computation을 수행해 array 밖으로 이동해야 하는 data를 줄이고 internal bandwidth를 활용한다.

### Architecture Walkthrough

현재까지 이해한 흐름: conventional DRAM은 선택된 row의 cell signal을 BL/SA로 sensing해 digital data로 읽는다. Digital-PIM은 이 read 이후 computing logic을 수행하고, PNM은 DIMM buffer device와 같은 memory-near 위치에 compute를 둔다. 반면 소개된 cell-array-level DRAM-CIM 접근은 read 시 여러 WL을 동시에 activate하여 여러 cell의 저장 상태가 공통 BL에 함께 영향을 주도록 하고, 여러 BL에서 이 collective electrical effect를 bitwise Boolean computation에 활용한다. 구체적인 Boolean function과 sensing circuit은 아직 다음 읽기 범위에서 확인해야 한다.

## 9. Method

부분 분석 중.

- 1T1C DRAM에서 multiple rows를 동시에 activate하여 여러 cell의 상태를 shared BL에 반영한다.
- 여러 BL을 통해 bitwise operation을 병렬적으로 수행하고 이를 더 복잡한 Boolean operation에 활용하는 접근까지 확인했다.
- 정확한 Boolean function 구현, voltage/sensing mechanism 및 이후 제안 회로는 아직 분석하지 않음.

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
| SRAM의 stable static storage와 compact bitcell layout | SRAM-CIM compute logic 추가로 transistor/area overhead 증가 | Introduction |
| SRAM의 reliable 1-bit storage | 1 bit/cell 구조로 multi-bit weight density 제약 | Introduction |
| SRAM의 fast/low-power read-write | volatility로 power-off data 유지 불가 | Introduction |
| DRAM-dedicated process의 high density | logic integration과는 별도 구현 선택지 | Introduction |
| eDRAM을 통한 logic-process integration 및 on-chip capacity 가능성 | die area/process/refresh trade-off가 존재할 수 있음; 구체 정량 비교는 이 문단에서 제시되지 않음 | Introduction + prerequisite discussion |
| NVM의 MLC/non-volatility | NVM-CIM에서는 non-linearity/low signal margin challenge | Introduction |
| Digital-PIM/PNM보다 cell array에 가까운 computation으로 data movement 감소 가능 | DRAM cell leakage/noise가 computation에 직접 영향을 줄 수 있음 | Introduction, Section II-A |
| 여러 BL의 internal parallelism/bandwidth 활용 | 구체 circuit/sensing robustness는 아직 분석하지 않음 | Section II-A |

## 13. Limitations

### Authors' Limitations

현재까지 확인된 limitation:
- SRAM-CIM: transistor/area overhead, 1 bit/cell weight density 제약, volatility
- DRAM-CIM: capacitor charge leakage/noise가 computation에 영향을 줄 수 있음
- NVM-CIM: non-linearity, low signal margin
- Digital-PIM/PNM: cell array에서 직접 computation하지 않고 conventional sensing/read path가 남아 있어 energy/latency improvement가 제한될 수 있음

### My Observations

- SRAM pushed-rule high density와 SRAM-CIM area overhead는 비교 수준이 달라 모순이 아니다.
- eDRAM의 logic compatibility는 logic 연산 자체를 더 빠르고 정확하게 만든다는 의미가 아니라 logic 공정/회로와 함께 집적할 수 있다는 의미다.
- cell-array-level DRAM-CIM의 이점은 external bandwidth를 단순히 높이는 것보다, memory array 내부의 병렬성을 computation에 활용해 외부 data movement 요구량을 줄이는 관점으로 이해하는 것이 적절하다.
- 사용자는 memory-bound NPU에서 MAC utilization이 낮다면 일부 compute area를 on-chip memory capacity에 재배분해 off-chip access를 줄이는 것이 전체 inference throughput을 높일 수도 있다고 architecture-level로 연결했다. 이는 논문의 직접 주장이라기보다 기존 학습과 연결한 사용자 관찰이다.

## 14. Questions

### 이해를 위한 질문

- DRAM-dedicated process와 SRAM pushed-rule은 둘 다 density에 유리할 수 있지만 각각 fabrication-process 최적화와 layout/design-rule 최적화로 수준이 다르다.
- eDRAM의 logic compatibility/high availability가 정확히 어떤 구현상의 의미인지 확인했고, 연산 정확도/속도 자체를 뜻하지 않음을 수정했다.
- NVM multi-level cell은 여러 distinguishable level로 cell당 여러 bit를 표현할 수 있다는 뜻이다.
- initial data writing 제거는 non-volatility로 power cycle 후 weight를 다시 써넣는 작업을 줄일 수 있다는 의미다.
- 일반 DRAM의 SA sensing과 DRAM-CIM의 cell-data-direct computation 차이를 확인했다.
- DIMM buffer device와 PNM의 위치 관계를 확인했다.
- multiple-row activation은 여러 WL을 동시에 켜 여러 cell이 shared BL에 함께 영향을 주게 하는 접근이다.
- bitwise operation과 DRAM internal bandwidth의 의미를 확인했다.

### 비판적 질문

- cell-array-level DRAM-CIM이 data movement를 줄이는 대신 leakage/noise에 더 직접 노출될 때 실제 robustness/accuracy를 어떻게 확보하는가? 이후 회로 설명에서 확인한다.

### 후속 연구 질문

- memory-bound AI accelerator에서 compute area와 on-chip memory area를 어떻게 배분해야 utilization/throughput/energy가 최적화되는가? 논문의 직접 범위를 넘어선 사용자 연결 질문으로 보존한다.

## 15. Connection to My Research Interest

부분 분석 중.

- 흥미로운 점: memory hierarchy에서 단순히 external bandwidth를 높이는 것뿐 아니라 cell-array internal parallelism을 computation에 활용해 data movement 자체를 줄일 수 있다는 점
- 더 탐구하고 싶은 부분: multiple-row activation이 실제 Boolean operation으로 변환되는 sensing/circuit mechanism과 leakage/noise robustness
- 다른 논문과의 연결: 기존 memory-wall, analog/digital CIM, tiling/Roofline 학습에서 다룬 data movement와 memory-bound/utilization 개념과 연결됨
- 가능한 research direction: compute-resource와 on-chip memory capacity/bandwidth의 area allocation trade-off, DRAM-CIM의 robustness-aware circuit/architecture 설계

## 16. Final Summary

부분 분석 중이며 확인된 항목만 기록한다.

### Problem

SRAM-CIM의 area/weight-density/volatility 한계로 DRAM/NVM-CIM이 재검토되지만, DRAM leakage/noise와 NVM non-linearity/low signal margin이라는 새로운 challenge가 있다. 1T1C DRAM에서는 conventional read path를 유지하는 digital-PIM/PNM의 data movement/latency 개선에도 한계가 있다.

### Key Idea

DRAM/NVM의 memory 특성을 CIM에 활용하되 각 technology의 circuit challenge를 해결해야 한다. 1T1C DRAM-CIM에서는 multiple-row activation과 BL-level parallelism을 이용해 cell data를 computation에 더 직접 활용할 수 있다.

### Architecture

현재까지는 1T1C DRAM array의 shared BL, WL multiple activation, SA/conventional read path, digital-PIM/PNM과 cell-array-level CIM의 위치 차이까지 분석했다.

### Main Result

아직 분석하지 않음.

### Main Trade-off

cell array에 computation을 더 가까이 가져갈수록 conventional data movement를 줄이고 internal parallelism을 활용할 가능성이 커지지만, DRAM cell의 leakage/noise 같은 비이상성이 computation에 직접 영향을 줄 수 있다.

### Limitation

현재까지 DRAM leakage/noise, NVM non-linearity/low signal margin, SRAM-CIM area/weight-density/volatility, digital-PIM/PNM의 conventional read-path overhead를 확인했다.

### 내가 기억할 한 문장

DRAM-CIM은 DRAM array가 가진 높은 density와 내부 BL 병렬성을 computation에 직접 활용해 data movement를 줄이려 하지만, 그만큼 cell leakage/noise를 계산 정확도 문제로 직접 다뤄야 한다.

## 17. Reading Session History

### 2026-08-28

- 읽은 범위: Abstract 및 Introduction 일부 — SRAM-CIM의 장점과 세 가지 limitation까지
- 이해한 내용: CIM의 energy-efficiency motivation, SRAM-CIM이 prevalent한 가운데 DRAM/NVM-CIM이 다시 주목받는 연구 흐름, DRAM-CIM의 leakage/refresh challenge, NVM-CIM의 non-linearity/low signal margin challenge, SRAM의 cross-coupled static storage와 pushed-rule 기반 compact bitcell, SRAM-CIM의 transistor/area overhead와 1 bit/cell/volatility 한계
- 새롭게 발생한 질문: pushed-rule의 의미, bitcell과 bitline의 차이, SRAM 자체의 high density와 SRAM-CIM area overhead가 왜 모순이 아닌지, cross-coupled storage node가 weight density를 어떻게 제한하는지, event-driven application이 무엇인지
- Bridge 변화: pushed-rule/bitcell density와 SRAM-CIM area overhead는 사용자 설명으로 이해 확인. weight density와 event-driven application은 AI 설명까지 진행했으나 사용자 자기 설명은 아직 확인되지 않음.
- 종료 당시 Resume Point: Introduction, PDF page 1 — “As the field of CIM progresses, these limitations underscore…” 문장부터 재개

## 사용자 분석 근거

> “DRAM을 쓰면 공정에서 최적화가 잘 되어있고 ... 더 높은 메모리 집적도 및 수율을 보인다고 이해하면 될까?” — high density 방향은 유지하고, ‘최적화가 쉽다/다른 memory보다 높은 수율’은 논문 근거가 없어 수정함.

> “기존 DRAM은 off-chip memory로 생각하고 있었는데, eDRAM은 logic이 있는 die 내부에 DRAM을 함께 탑재하여 MAC과 같은 연산기들과 가깝게 위치하고, 이를 통해 더 빠르고, 에너지도 덜 드는 연산을 할 수 있다는 뜻인가?”

> “MAC의 utilization이 낮고 그 이유가 memory bandwidth의 한계로 인한 memory bound라면 MAC의 일부를 줄이고 eDRAM의 memory를 탑재하여 ... 전체 AI inference 성능이 올라갈 수도 있을 것이라고 생각해.”

> “multi-level cell을 NVM은 구현할 수 있다 ... NVM은 non-volatile이기 때문에, 전원을 off해도 data가 사라지지 않는다 ... initial data writing이 제거 되었기 때문에, 외부와의 data movement를 줄여서 에너지 효율을 더 높일 수 있다.”

> “DRAM, NVM이 앞서 설명한 장점이 있다고 했지만, 이 둘의 단점도 존재한다 ... DRAM의 leakage, noise라는 단점과 non-linearity, low signal margin이라는 NVM의 단점을 cover할 수 있는 연구가 필요하다.”

> “DRAM cell은 1개의 capacitance를 통해 데이터를 저장한다 ... capacitance에 저장된 charge가 leakage나 noise를 통해 손상을 입을 수 있다 ... DRAM-CIM에서 고려해야할 문제점들을 서술한 문단이라고 판단했음.”

> “즉 일반 DRAM에서는 SA가 capacitance에 저장된 값을 0/1로 감지하여 logic에 전달하는 구조이지만, DRAM-CIM은 SA 없이 ...?” — ‘DRAM-CIM=SA 없음’은 일반화할 수 없다고 수정·확인함.

> “1T-1C DRAM은 가장 많이 범용적으로 사용된다. 높은 메모리 집적도를 보이기 때문이다 ... digital-PIM은 SA 작동 이후 computing logic을 실시하는 것이고 ... PNM ... buffer device of DIMM이 무엇인지 이해가 안됨.”

> “DIMM 이란 그러면 DRAM을 놓는 기판이라고 생각하면 될까? ... 그 device에 연산장치를 추가하는 것이 PNM의 기본 원리라는 것인가?”

> “PNM, digital-PIM에서 에너지의 효율성 및 반응속도의 상승은 어느정도 제한되어있다. 그 이유는 computing logic이 실제 cell array 내부에 있지 않고, SA가 모든 데이터를 읽는데 사용되어지기 때문이다.”

> “즉 여러 WL을 동시에 켜서 여러개의 cell이 하나로 연결된 BL에 영향을 주게 하여, 그 영향을 통해 boolean operation을 할 수 있다는 접근까지만 이해하면 되는걸까”

> “그러한 접근은 DRAM의 여러 BL을 통한 bitwise operation을 할 수 있고, 이 bitwise operation은 더 복잡한 boolean operations을 도와줄 수 있다. 게다가, bandwidth가 최적화 되는데, 그 이유는 연산이 cell array 내부에서 이루어 지기 때문이다 ... 수많은 memory의 이동을 조금 줄일 수 있기 때문에 bandwidth가 더 최적화 된다고 이해했다.”

> “internal bandwidth라는게 DRAM 내부에서의 memory 이동을 의미하는것인가? 그렇다면 그 internal bandwidth는 DRAM -> SRAM으로 memory를 보낼 때의 bandwidth보다 확실히 더 큰 것인가?”
