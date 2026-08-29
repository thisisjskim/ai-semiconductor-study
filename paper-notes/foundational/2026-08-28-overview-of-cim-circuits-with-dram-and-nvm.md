# Paper Note: An Overview of Computing-in-Memory Circuits With DRAM and NVM

## Metadata

- Title: An Overview of Computing-in-Memory Circuits With DRAM and NVM
- Document type: paper-note
- Paper type: foundational
- Venue / Year: IEEE Transactions on Circuits and Systems II: Express Briefs / 2024
- Authors: Sangjin Kim, Hoi-Jun Yoo
- Paper link: https://doi.org/10.1109/TCSII.2023.3333851
- Started: 2026-08-28
- Checkpoint recorded at: 2026-08-28T15:37:05Z
- Related notes: learning-logs/2026/08/2026-08-23-memory-wall-analog-cim-fundamentals.md; learning-logs/2026/08/2026-08-24-pim-cim-tiling-roofline-foundations.md

## 1. Citation

S. Kim and H.-J. Yoo, “An Overview of Computing-in-Memory Circuits With DRAM and NVM,” IEEE Transactions on Circuits and Systems II: Express Briefs, vol. 71, no. 3, pp. 1626–1631, Mar. 2024. doi: 10.1109/TCSII.2023.3333851.

## 2. Reading Checkpoint

- Resume Point: Section II. DRAM-CIM, B. Gain-Cell DRAM, PDF page 2 — 1T-1C의 destructive read, frequent SA recovery power overhead, Gain-Cell의 RBL/WBL 분리와 non-destructive read path의 장단점을 읽고 이해한 직후. 다음 세션에서는 “The 4T-2C cell proposed in [20] is a pair of 2T-1C gain-cells…” 문장부터 Fig. 2(a)의 4T-2C structure와 1-b IA / ternary W multiplication을 읽는다. 아직 읽지 않은 4T-2C 회로 세부는 미리 가정하지 않는다.

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
- 사용자의 이해: 사용자는 cell array 내부 computation이 외부 SRAM/register/MAC으로 이동하는 data를 줄일 수 있다고 자기 설명했다. 이어 internal bandwidth가 무엇인지 질문했고, AI 설명을 통해 array 내부의 많은 cell/BL을 병렬적으로 access/processing할 수 있는 능력이며 external interface bandwidth 자체가 자동으로 증가한다는 의미는 아님을 확인했다. 정확한 정의는 사용자 자기 설명보다는 문답으로 수정·확인된 상태다.

#### 1T-1C analog DRAM-CIM / charge sharing
- 등장 위치: Section II-A 1T-1C DRAM, PDF page 2, references [15], [16]
- 논문에서 필요한 이유: 최근 DRAM-CIM이 Boolean operation뿐 아니라 analog operation을 이용해 higher efficiency와 parallelism을 얻는 방식을 이해하기 위해 필요하다.
- 사용자의 이해: [15]에서 IA 값에 대응하는 analog voltage가 cell capacitors 사이의 charge sharing으로 생성되어 cell에 write된다는 점을 문답으로 확인했다. Weight 자체를 동일한 방식의 analog voltage로 저장한다고 단정하지 않고, 논문 문장 수준에서는 weight 값에 따라 cells 사이의 charge sharing을 수행해 multi-bit IA와 W의 MAC을 수행한다고 이해했다. 구체적인 weight-dependent charge-sharing circuit은 overview에 충분히 설명되지 않아 필요하면 reference [15]에서 확인하기로 했다.

#### SNN / spike / integrate-and-firing
- 등장 위치: Section II-A 1T-1C DRAM, PDF page 2, reference [16]
- 논문에서 필요한 이유: [16]이 scalar IA와 MAC 대신 spike IA와 integrate-and-firing operation을 사용하는 이유를 이해하기 위해 필요하다.
- 사용자의 이해: SNN에서는 IA를 scalar 대신 spike 형태로 표현하고, spike의 영향을 누적하는 integrate operation과 조건을 만족할 때 firing하는 operation을 사용한다는 최소 개념을 이해했다. 사용자는 [16]에서 integration을 cell column의 charge sharing으로, firing을 SA operation으로 구현한다고 자기 설명했다. 구체적인 threshold/firing circuit은 overview가 직접 설명하지 않으므로 확정하지 않았다.

#### Cell column
- 등장 위치: Section II-A 1T-1C DRAM, reference [16]
- 논문에서 필요한 이유: “charge sharing of cell columns”가 SNN integration에 어떻게 연결되는지 이해하기 위해 필요하다.
- 사용자의 이해: 하나의 BL을 공유하는 여러 DRAM cells의 column 단위에서 charge sharing을 이용해 spike 영향의 integration을 구현한다고 이해했다. 특정 spike가 어느 capacitor에 얼마의 charge를 전달하는지는 overview만으로 확정하지 않았다.

#### Destructive read / SA recovery / Gain-Cell
- 등장 위치: Section II-B Gain-Cell DRAM, PDF page 2
- 논문에서 필요한 이유: 1T-1C DRAM-CIM의 frequent SA power overhead와 Gain-Cell 구조가 등장하는 이유를 이해하기 위해 필요하다.
- 사용자의 이해: 1T-1C는 read와 write에 single bit line을 사용하고 read/computation 중 charge sharing으로 cell data가 훼손되는 destructive read가 발생하며, 이후 SA operation으로 값을 recover해야 한다고 문답으로 수정·확인했다. Gain-Cell은 additional transistor로 RBL과 WBL을 분리하여 non-destructive read path를 computing datapath로 사용할 수 있고 SA operation 빈도를 줄일 수 있지만, 1T-1C보다 density가 낮아지는 trade-off가 있다고 자기 설명했다. Gain-Cell DRAM-CIM의 2–4 transistor/cell이 SRAM-CIM의 6–18 transistor보다 적다는 비교도 확인했다.

#### DRAM-CIM의 computation operation
- 등장 위치: Section II-B Gain-Cell DRAM, PDF page 2
- 논문에서 필요한 이유: “during every read or computation”에서 computation이 일반 DRAM의 read/write 외 별도 memory primitive인지 구분하기 위해 필요하다.
- 사용자의 이해: 여기서 computation은 일반 DRAM의 기본 read/write operation에 추가된 독립 memory primitive가 아니라, DRAM-CIM에서 cell data/charge를 이용해 Boolean operation, analog MAC, SNN integration 등을 수행하는 CIM computation을 가리킨다는 설명을 듣고 이해를 확인했다. 사용자 자기 설명: 아직 확인하지 않음.

### 별도로 이어가는 선수지식

없음.

## 4. Problem

부분 분석 중.

현재까지 읽은 범위에서, SRAM-CIM은 안정적 storage와 compact bitcell의 장점이 있지만 compute logic 추가에 따른 area overhead, 1 bit/cell weight density 제약, volatility가 있다. 이를 보완할 DRAM/NVM-CIM은 각각 높은 density 및 non-volatility 등의 장점이 있지만 DRAM의 leakage/noise와 NVM의 non-linearity/low signal margin이라는 새로운 circuit challenge를 갖는다. 특히 conventional 1T1C DRAM array를 직접 수정하는 비용이 크고, digital-PIM/PNM은 conventional sensing/read/data-transfer path가 남아 있어 cell-array-level CIM보다 data movement reduction에 한계가 있다. 1T-1C DRAM-CIM은 cell charge를 computation에 직접 활용할 수 있지만 destructive read와 frequent SA recovery로 power overhead가 커질 수 있어 Gain-Cell 같은 대안 구조가 등장한다.

## 5. Motivation and Prior-Work Gap

부분 분석 중.

SRAM-CIM의 한계 때문에 DRAM/NVM이 재검토된다. DRAM은 1T1C와 DRAM-dedicated process를 통한 high density, logic process에서 eDRAM 구현 가능성이라는 장점이 있고, NVM은 low standby power, multi-level cell, non-volatility로 인한 initial data writing 제거 가능성이 있다. 그러나 이러한 memory를 CIM에 사용할 때 DRAM leakage/noise와 NVM non-linearity/low signal margin이라는 fresh challenges가 생겨 새로운 circuits/datapaths가 필요하다.

1T1C DRAM에서는 기존 array를 크게 바꾸지 않는 digital-PIM/PNM도 연구됐지만, computation이 cell array에서 직접 이루어지지 않고 conventional sensing/read가 필요해 energy/latency improvement가 제한될 수 있다. 따라서 cell/BL의 내부 병렬성을 computation에 직접 활용하는 DRAM-CIM 접근을 살펴볼 동기가 생긴다. 또한 최근 [15], [16]은 analog operation을 이용해 higher efficiency와 parallelism을 추구하며, [15]는 charge sharing으로 multi-bit IA/W MAC을, [16]은 SNN의 integrate-and-firing을 DRAM operation에 mapping한다. 반면 1T-1C의 destructive read는 frequent SA recovery와 power overhead를 만들기 때문에 Section II-B에서는 read/write path를 분리한 Gain-Cell을 검토한다.

## 6. Prerequisites

| Prerequisite | 현재 상태 | 필요한 보충 |
| --- | --- | --- |
| DRAM leakage / refresh / SA read | 논문 읽기에 충분 | 이후 circuit과 연결 |
| NVM resistance / non-linearity / low signal margin | 논문 읽기에 충분한 기초 | Section III에서 실제 circuit example과 연결 |
| SRAM pushed-rule / area overhead | 사용자 이해 확인됨 | 추가 보충 없음 |
| SRAM weight density | AI 설명, 자기 설명 미확인 | 필요 시 짧게 확인 |
| Event-driven application | AI 설명, 자기 설명 미확인 | 필요 시 짧게 확인 |
| DRAM-dedicated process / eDRAM | 문답으로 이해 확인 | 이후 architecture 비교 시 재사용 |
| NVM MLC / non-volatility / initial writing | 사용자 자기 설명 확인됨 | Section III에서 구체적 device/circuit과 연결 |
| NN inference 기초 | AI 설명, 자기 설명 미확인 | 논문 진행에 필요한 경우만 보충 |
| DIMM / PNM | 문답으로 이해 확인 | 추가 보충 없음 |
| Bitwise operation | 사용자 설명으로 확인됨 | 구체 Boolean circuit은 reference 필요 시 확인 |
| DRAM internal bandwidth | 문답으로 수정·확인 | 정량 비교는 논문 근거가 나올 때만 확장 |
| Analog DRAM-CIM / charge sharing | 문답으로 수정·확인 | [15] 세부 circuit은 필요 시 원 논문에서 확인 |
| SNN / integrate-and-firing | 사용자 설명으로 확인됨 | [16] threshold/firing circuit은 필요 시 원 논문에서 확인 |
| Cell column | 문답으로 이해 확인 | 구체 charge path는 overview 범위 밖 |
| Destructive read / Gain-Cell | 사용자 설명 + 문답 수정으로 확인 | 다음 4T-2C gain-cell circuit과 연결 |
| DRAM-CIM computation | AI 설명 후 사용자 이해 확인 | 필요 시 실제 circuit example과 연결 |

## 7. Key Idea

부분 분석 중.

> 한 문장 요약: DRAM/NVM은 SRAM-CIM의 일부 한계를 보완할 수 있지만 각 memory의 비이상성이 새로운 CIM challenge를 만들며, DRAM-CIM은 1T-1C의 cell/BL 병렬성·charge sharing을 computation에 직접 활용하거나 Gain-Cell의 분리된 read path를 이용해 data movement와 SA overhead를 줄이는 방향으로 발전한다.

## 8. Architecture

부분 분석 중 — Section II-B Gain-Cell 첫 문단까지 확인한 범위만 기록한다.

- 주요 component: 1T1C DRAM cell array, WL, BL, SA, digital-PIM compute logic, PNM의 memory-near buffer/compute 영역, Gain-Cell의 RBL/WBL
- Data path: conventional/digital-PIM은 cell → BL/SA sensing → digital data → compute 경로를 유지한다. cell-array-level 1T-1C DRAM-CIM은 multiple rows와 shared BL 또는 capacitor charge sharing을 computation에 활용한다. Gain-Cell은 read path와 write path를 분리해 non-destructive read path를 computing datapath로 사용할 수 있다.
- Control: multiple-row activation이 Boolean computation에 사용된다. [15]는 weight value에 따른 charge sharing, [16]은 SNN spike 처리에서 integration/firing mapping을 사용한다. Gain-Cell의 세부 4T-2C control은 아직 분석하지 않음.
- Memory organization: 1T1C DRAM array는 여러 rows가 BL을 공유한다. Gain-Cell은 additional transistor를 사용해 RBL과 WBL을 분리한다.
- Parallelism: 여러 BL의 bitwise operation, analog charge-sharing operation, SNN cell-column integration이 소개됨.
- Dataflow: cell array 내부에서 computation을 수행해 외부 이동 data를 줄이며, Gain-Cell은 non-destructive read path를 이용해 frequent SA recovery를 줄이는 방향을 취한다.

### Architecture Walkthrough

현재까지 이해한 흐름: conventional DRAM은 선택된 row의 cell signal을 BL/SA로 sensing해 digital data로 읽는다. Digital-PIM은 이 read 이후 computing logic을 수행하고, PNM은 DIMM buffer device와 같은 memory-near 위치에 compute를 둔다. cell-array-level 1T-1C DRAM-CIM은 multiple-row activation을 이용한 bitwise Boolean computation을 수행할 수 있고, 최근 analog approaches에서는 capacitor charge sharing을 이용해 [15]의 multi-bit IA/W MAC 또는 [16]의 SNN integration을 구현한다. [16]의 firing은 SA operation으로 mapping된다. 그러나 1T-1C는 read/computation 시 charge sharing 때문에 destructive read가 발생해 SA recovery가 자주 필요하고 power를 소비한다. Gain-Cell은 RBL과 WBL을 분리하여 non-destructive read path를 computing datapath로 사용하고 SA operation 빈도를 낮추는 대신 1T-1C보다 cell density가 낮아진다. 다음 세션에서 4T-2C Gain-Cell의 구체적인 multiplication/accumulation 구조를 분석한다.

## 9. Method

부분 분석 중.

- 1T1C DRAM에서 multiple rows를 동시에 activate하여 여러 cell의 상태를 shared BL에 반영하고 bitwise Boolean operation을 수행한다.
- [15]는 cell capacitors의 charge sharing으로 IA에 대응하는 analog voltage를 만들고, weight value에 따라 cells 사이의 charge sharing을 수행해 multi-bit IA와 W의 MAC을 구현한다. 구체 circuit은 overview에 충분히 제시되지 않음.
- [16]은 SNN을 채택하여 scalar IA 대신 spike를 사용하고, cell-column charge sharing으로 integration을, SA operation으로 firing을 구현한다. 구체 threshold circuit은 overview에 충분히 제시되지 않음.
- 1T-1C read/computation의 destructive read와 frequent SA recovery overhead를 줄이기 위해 Gain-Cell은 RBL과 WBL을 분리하여 non-destructive read path를 computing datapath로 사용한다.
- 4T-2C Gain-Cell 이후의 구체 multiplication, row/column parallelism, variation mitigation은 아직 분석하지 않음.

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
| 여러 BL의 internal parallelism/bandwidth 활용 | exact internal-bandwidth definition/quantification은 architecture-dependent | Section II-A + prerequisite discussion |
| 1T-1C analog charge sharing으로 multi-bit MAC/SNN operation 지원 | overview만으로 [15]/[16]의 구체 circuit mechanism은 완전히 확인할 수 없음 | Section II-A |
| Gain-Cell의 non-destructive read path로 SA operation 빈도와 power overhead 감소 가능 | 1T-1C보다 낮은 memory density | Section II-B |
| Gain-Cell DRAM-CIM의 2–4 transistor/cell | 1T-1C의 minimal cell보다 transistor 수 증가 | Section II-B |

## 13. Limitations

### Authors' Limitations

현재까지 확인된 limitation:
- SRAM-CIM: transistor/area overhead, 1 bit/cell weight density 제약, volatility
- DRAM-CIM: capacitor charge leakage/noise가 computation에 영향을 줄 수 있음
- NVM-CIM: non-linearity, low signal margin
- Digital-PIM/PNM: cell array에서 직접 computation하지 않고 conventional sensing/read path가 남아 있어 energy/latency improvement가 제한될 수 있음
- 1T-1C DRAM-CIM: destructive read 때문에 frequent SA recovery가 필요해 considerable power를 소비할 수 있음
- Gain-Cell: additional transistor와 separated read/write path로 1T-1C보다 density가 낮음

### My Observations

- SRAM pushed-rule high density와 SRAM-CIM area overhead는 비교 수준이 달라 모순이 아니다.
- eDRAM의 logic compatibility는 logic 연산 자체를 더 빠르고 정확하게 만든다는 의미가 아니라 logic 공정/회로와 함께 집적할 수 있다는 의미다.
- cell-array-level DRAM-CIM의 이점은 external bandwidth를 단순히 높이는 것보다, memory array 내부의 병렬성을 computation에 활용해 외부 data movement 요구량을 줄이는 관점으로 이해하는 것이 적절하다.
- 사용자는 memory-bound NPU에서 MAC utilization이 낮다면 일부 compute area를 on-chip memory capacity에 재배분해 off-chip access를 줄이는 것이 전체 inference throughput을 높일 수도 있다고 architecture-level로 연결했다. 이는 논문의 직접 주장이라기보다 기존 학습과 연결한 사용자 관찰이다.
- [15], [16]의 overview 문장은 핵심 computation mapping은 보여 주지만 exact capacitor connection, weight-dependent charge-sharing path, SNN firing threshold circuit까지는 충분히 설명하지 않는다. 현재 단계에서는 reference를 모두 따라가지 않고 overview의 design-space map을 먼저 완성하기로 했다.

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
- [15]에서 IA는 analog voltage로 cell에 write되고, W는 논문 문장 수준에서는 charge-sharing behavior를 결정하는 값으로 이해하며, 정확한 circuit은 reference가 필요함을 확인했다.
- SNN의 spike, integrate-and-firing과 [16]의 cell-column charge sharing / SA mapping을 확인했다.
- 1T-1C destructive read와 Gain-Cell의 RBL/WBL separation, SA recovery overhead 관계를 확인했다.
- Section II-B의 “computation”은 일반 DRAM의 새로운 memory primitive가 아니라 DRAM-CIM computation을 뜻함을 확인했다.

### 비판적 질문

- cell-array-level DRAM-CIM이 data movement를 줄이는 대신 leakage/noise에 더 직접 노출될 때 실제 robustness/accuracy를 어떻게 확보하는가? 이후 회로 설명에서 확인한다.
- Gain-Cell이 non-destructive read로 SA overhead를 줄이는 대신 density를 희생할 때, 실제 efficiency/density optimum은 어떤 workload와 circuit configuration에서 결정되는가?

### 후속 연구 질문

- memory-bound AI accelerator에서 compute area와 on-chip memory area를 어떻게 배분해야 utilization/throughput/energy가 최적화되는가? 논문의 직접 범위를 넘어선 사용자 연결 질문으로 보존한다.
- [15]/[16] 같은 analog/SNN DRAM-CIM에서 charge sharing의 정확도와 leakage/noise robustness가 실제 multi-bit computation에 어떤 제약을 주는지 원 논문 deep-dive 후보로 보존한다.

## 15. Connection to My Research Interest

부분 분석 중.

- 흥미로운 점: memory hierarchy에서 단순히 external bandwidth를 높이는 것뿐 아니라 cell-array internal parallelism과 charge sharing을 computation에 활용해 data movement 자체를 줄일 수 있다는 점
- 더 탐구하고 싶은 부분: multiple-row activation의 Boolean sensing mechanism, analog charge-sharing MAC/SNN integration, Gain-Cell의 non-destructive computing datapath와 leakage/noise robustness
- 다른 논문과의 연결: 기존 memory-wall, analog/digital CIM, tiling/Roofline 학습에서 다룬 data movement와 memory-bound/utilization 개념과 연결됨
- 가능한 research direction: compute-resource와 on-chip memory capacity/bandwidth의 area allocation trade-off, DRAM-CIM의 robustness-aware circuit/architecture 설계, destructive-read/SA-overhead와 density의 trade-off

## 16. Final Summary

부분 분석 중이며 확인된 항목만 기록한다.

### Problem

SRAM-CIM의 area/weight-density/volatility 한계로 DRAM/NVM-CIM이 재검토되지만, DRAM leakage/noise와 NVM non-linearity/low signal margin이라는 새로운 challenge가 있다. 1T1C DRAM에서는 conventional read path를 유지하는 digital-PIM/PNM의 data movement/latency 개선에도 한계가 있고, cell-array computation은 destructive read와 frequent SA recovery power overhead를 동반할 수 있다.

### Key Idea

DRAM/NVM의 memory 특성을 CIM에 활용하되 각 technology의 circuit challenge를 해결해야 한다. 1T1C DRAM-CIM에서는 multiple-row activation, BL-level parallelism, capacitor charge sharing을 이용해 cell data를 computation에 직접 활용할 수 있고, Gain-Cell은 read/write path를 분리해 non-destructive computing datapath를 제공한다.

### Architecture

현재까지 1T1C DRAM array의 shared BL, WL multiple activation, SA/conventional read path, digital-PIM/PNM과 cell-array-level CIM의 위치 차이를 분석했다. 또한 [15]의 charge-sharing multi-bit MAC, [16]의 SNN integration/firing mapping, Gain-Cell의 RBL/WBL separation과 non-destructive read path까지 확인했다. 4T-2C Gain-Cell의 구체 회로는 아직 분석하지 않음.

### Main Result

아직 분석하지 않음.

### Main Trade-off

cell array에 computation을 더 가까이 가져갈수록 conventional data movement를 줄이고 internal parallelism을 활용할 가능성이 커지지만, 1T-1C에서는 leakage/noise와 destructive read/frequent SA recovery가 문제가 될 수 있다. Gain-Cell은 SA overhead를 줄이는 대신 1T-1C보다 density를 희생한다.

### Limitation

현재까지 DRAM leakage/noise, NVM non-linearity/low signal margin, SRAM-CIM area/weight-density/volatility, digital-PIM/PNM의 conventional read-path overhead, 1T-1C destructive read/SA power overhead와 Gain-Cell density trade-off를 확인했다.

### 내가 기억할 한 문장

DRAM-CIM은 1T-1C의 높은 density와 charge/BL 병렬성을 직접 계산에 활용할 수 있지만 destructive read와 SA overhead가 생기며, Gain-Cell은 read/write path를 분리해 이 문제를 줄이는 대신 density를 희생한다.

## 17. Reading Session History

### 2026-08-28

- 읽은 범위: Abstract 및 Introduction 일부 — SRAM-CIM의 장점과 세 가지 limitation까지
- 이해한 내용: CIM의 energy-efficiency motivation, SRAM-CIM이 prevalent한 가운데 DRAM/NVM-CIM이 다시 주목받는 연구 흐름, DRAM-CIM의 leakage/refresh challenge, NVM-CIM의 non-linearity/low signal margin challenge, SRAM의 cross-coupled static storage와 pushed-rule 기반 compact bitcell, SRAM-CIM의 transistor/area overhead와 1 bit/cell/volatility 한계
- 새롭게 발생한 질문: pushed-rule의 의미, bitcell과 bitline의 차이, SRAM 자체의 high density와 SRAM-CIM area overhead가 왜 모순이 아닌지, cross-coupled storage node가 weight density를 어떻게 제한하는지, event-driven application이 무엇인지
- Bridge 변화: pushed-rule/bitcell density와 SRAM-CIM area overhead는 사용자 설명으로 이해 확인. weight density와 event-driven application은 AI 설명까지 진행했으나 사용자 자기 설명은 아직 확인되지 않음.
- 종료 당시 Resume Point: Introduction, PDF page 1 — “As the field of CIM progresses, these limitations underscore…” 문장부터 재개

### 2026-08-28 (추가 세션)

- 읽은 범위: Section II-A 1T-1C DRAM의 multiple-row activation/bitwise operation 이후부터 analog DRAM-CIM [15], SNN DRAM-CIM [16]까지 완료하고, Section II-B Gain-Cell DRAM의 첫 문단까지 읽음.
- 이해한 내용: [15]에서 IA를 charge sharing으로 analog voltage로 만들고 cell에 write한 뒤 weight 값에 따라 cell 간 charge sharing을 수행해 multi-bit MAC을 구현한다는 overview-level 흐름, [16]에서 scalar IA 대신 spike를 사용하고 cell-column charge sharing으로 integration, SA operation으로 firing을 구현한다는 SNN mapping, 1T-1C의 destructive read와 SA recovery power overhead, Gain-Cell의 RBL/WBL separation과 non-destructive read path 및 density trade-off.
- 새롭게 발생한 질문: [15]에서 exact weight-dependent charge-sharing circuit이 어떻게 구현되는지, SNN의 integrate-and-firing이 무엇인지, cell column이 무엇인지, [16]의 exact firing threshold circuit이 어떻게 구현되는지, DRAM-CIM 문맥의 computation이 무엇을 뜻하는지.
- Bridge 변화: analog DRAM-CIM/charge sharing은 문답으로 수정·확인, SNN integrate-and-firing은 사용자 자기 설명으로 확인, cell column과 destructive read/Gain-Cell은 문답 및 사용자 설명으로 확인. exact [15]/[16] circuit은 overview 범위 밖으로 남기고 별도 Learning Log로 승격하지 않음. DRAM internal bandwidth의 evidence 상태를 “사용자 설명으로 확인”에서 “문답으로 수정·확인”으로 엄밀하게 수정.
- 종료 당시 Resume Point: Section II-B Gain-Cell DRAM, PDF page 2 — “The 4T-2C cell proposed in [20] is a pair of 2T-1C gain-cells…” 문장부터 Fig. 2(a)와 함께 재개.

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

> “최근 연구에서 더 높은 성능과 병렬 연산을 위해서 analog 동작을 DRAM-CIM에 도입하였다. 1T1C cell의 capacitor 가 NN model에서 activation 과 weight를 MAC 연산을 생성하는 역할을 한다는 것을 확인했다.” — capacitor가 activation/weight를 ‘생성’하는 것이 아니라 IA/W의 MAC logic에 활용된다는 방향으로 수정함.

> “또한 같은 논리로, weight의 값도 cell들의 charge sharing을 통해 표현되어 진다. 그리고 이 weight의 값과 IA가 multi bit 연산을 MAC을 통해 실시한다.” — weight를 IA와 동일한 analog voltage로 저장한다고 단정하지 않고, weight 값에 따라 charge sharing이 수행된다고 수정함.

> “맞아 이걸 이해하려면 reference [15]에 해당하는 논문을 읽고 거기 나와있는 회로를 확인해야 할 것 같음 ..”

> “[16]은 SNN일때를 채택하여 보았다. IA를 크기로 보기 보다는 spike의 형태로 인식을 한다 ... integration operation을 cell column에서의 charge sharing으로, 그리고 firing operation을 SA operation으로 구현한다.”

> “DRAM-CIM을 통해 SNN에서 MAC operation 대신 integrate-and-firing operation을 구현하는데 쓰였다 ... integrate operation을 cell column에서의 charge sharing으로 구현하였고, firing을 ... SA operation ... 을 이용하여 구현하였다.” — exact threshold circuit은 overview가 명시하지 않아 일반 SNN/SA intuition과 논문 직접 근거를 구분함.

> “1T-1C cell은 오직 single-bit line로 read,write operation을 구현한다 ... read, computing 할 때 cell에 저장된 charge가 destroyed ... SA operation을 통해 다시 DRAM cell에 값을 recover ... gain-cell structure는 RBL과 WBL을 추가의 transistor를 사용하여 분리 ... non-destructive read path ... SA operation의 빈도를 낮춤 ... 1T-1C cell 보다는 memory density가 낮다.”

> “그 전에, DRAM에서 computation 과정이 의미하는게 무엇이야? ... DRAM-CIM에서의 특성을 말하고 있는 것인가?”
