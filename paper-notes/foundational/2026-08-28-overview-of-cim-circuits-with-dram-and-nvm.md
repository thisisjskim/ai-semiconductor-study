# Paper Note: An Overview of Computing-in-Memory Circuits With DRAM and NVM

## Metadata

- Title: An Overview of Computing-in-Memory Circuits With DRAM and NVM
- Document type: paper-note
- Paper type: foundational
- Venue / Year: IEEE Transactions on Circuits and Systems II: Express Briefs / 2024
- Authors: Sangjin Kim, Hoi-Jun Yoo
- Paper link: https://doi.org/10.1109/TCSII.2023.3333851
- Started: 2026-08-28
- Checkpoint recorded at: 2026-09-01T13:03:01Z
- Related notes: learning-logs/2026/08/2026-08-23-memory-wall-analog-cim-fundamentals.md; learning-logs/2026/08/2026-08-24-pim-cim-tiling-roofline-foundations.md; learning-logs/2026/08/2026-08-30-nvm-fundamentals.md

## 1. Citation

S. Kim and H.-J. Yoo, “An Overview of Computing-in-Memory Circuits With DRAM and NVM,” IEEE Transactions on Circuits and Systems II: Express Briefs, vol. 71, no. 3, pp. 1626–1631, Mar. 2024. doi: 10.1109/TCSII.2023.3333851.

## 2. Reading Checkpoint

- Resume Point: Section V. Conclusion, PDF page 5까지 전체 reading 완료. 이 overview paper의 본문 분석은 종료했다. 다음 선택적 deep dive는 [21] DynaPlasia 원 논문을 확보해 Fig. 2(e) 3T-2C의 transistor/capacitor 역할, IA/W truth table, switching sequence와 coupling capacitor의 ΔV/ΔQ 전달을 transistor-level로 확인하거나, roadmap의 후속 paper comparison으로 진행한다.

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


#### 4T-2C Gain-Cell / signed ternary multiplication
- 등장 위치: Section II-B Gain-Cell DRAM, Fig. 2(a)
- 논문에서 필요한 이유: complementary 2T-1C pair가 signed weight와 1-b IA multiplication을 어떻게 표현하는지 이해하기 위해 필요하다.
- 사용자의 이해: 4T-2C가 두 개의 2T-1C gain-cell pair로 구성되고 complementary storage를 이용해 signed representation을 지원한다는 점을 확인했다. 1-b IA는 1-bit input activation, ternary W는 {-1, 0, +1}의 세 weight state라는 점을 문답으로 수정·확인했다. signed representation을 일반 binary sign-bit와 동일시하지 않도록 구분했다.

#### Current-based row-parallel accumulation / process variation
- 등장 위치: Section II-B, Fig. 2(a)
- 논문에서 필요한 이유: 64-row parallel multiplication의 accumulation 방식과 variation-induced current mismatch를 이해하기 위해 필요하다.
- 사용자의 이해: 각 row의 multiplication 결과가 current contribution으로 나타나 shared RBL에서 합산되어 accumulation을 형성하며, cell-to-cell current mismatch가 그대로 합산 오차로 들어갈 수 있다고 자기 언어로 설명했다. Fig. 2(a)의 driving transistor가 Q1이며 storage node 상태에 따라 RBL current path를 구동하는 역할이라는 점도 확인했다.

#### Voltage clipping / column-only accumulation
- 등장 위치: Section II-B, Fig. 2(b), reference [17]
- 논문에서 필요한 이유: row parallelism을 제거하고 variation/leakage robustness를 얻는 구조를 이해하기 위해 필요하다.
- 사용자의 이해: self-detect voltage clipper는 모든 전압을 임의의 값으로 변환하는 회로가 아니라 RBL voltage를 predefined reference level에 제한해 cell variation/leakage가 accumulation에 직접 전달되는 영향을 줄이는 회로라는 점을 문답으로 이해했다. Fig. 2(b)는 individual multiplication result를 clipping한 뒤 column 방향 charge-sharing accumulation을 사용하며, clipper 자체가 일반적으로 row parallelism을 불가능하게 만드는 것은 아니라는 점을 구분했다.

#### Segmented RBL / row-segment parallelism
- 등장 위치: Section II-B, Fig. 2(c), reference [19]
- 논문에서 필요한 이유: variation/leakage를 줄이면서 row parallelism을 다시 확보하는 방법을 이해하기 위해 필요하다.
- 사용자의 이해: 하나의 긴 RBL을 transmission gate로 여러 segment로 나누고, 각 segment에서 한 row가 1-b multiplication을 동시에 수행한 뒤 segment RBL voltages를 charge sharing으로 accumulate한다는 구조로 이해했다. “두 segment”가 아니라 multiple row segments라는 점을 수정했다.

#### Common-mode error / reference cell array
- 등장 위치: Section II-B, Fig. 2(c), reference [19]
- 논문에서 필요한 이유: leakage-induced error와 coupling noise를 reference array로 줄이는 원리를 이해하기 위해 필요하다.
- 사용자의 이해: common-mode error는 signal과 reference에 비슷한 방향과 크기로 공통으로 들어가는 error이며, reference cell array가 ADC 자체가 아니라 ADC의 reference voltage를 제공하는 기준점이라는 점을 수정·확인했다. 사용자는 Vsignal과 Vref에 같은 error가 들어오면 비교 과정에서 공통 error가 상쇄되어 ADC 결과에 미치는 영향이 줄어든다고 자기 언어로 설명했다.

#### 3T-1C 4b weight / pulse-width IA multiplication
- 등장 위치: Section II-B, Fig. 2(d), reference [18]
- 논문에서 필요한 이유: 3T gain-cell이 4b weight와 4b IA의 analog multiplication을 구현하는 방식을 이해하기 위해 필요하다.
- 사용자의 이해: 4-bit는 4 level이 아니라 16개의 distinguishable value를 의미하며, storage capacitor의 4b analog weight가 Q1 current magnitude를 조절하고 4b IA가 Q2의 pulse width/turn-on time을 조절한다고 이해했다. Q1-Q2 serial path를 통해 전달되는 charge가 직관적으로 I(W)×T(IA)에 비례해 multiplication을 표현한다는 설명을 듣고, IA가 커지면 Q2 ON time이 길어져 RBL에 전달되는 total charge가 증가한다고 자기 설명했다.

#### 3T-1C analog storage trade-off
- 등장 위치: Section II-B, Fig. 2(d)
- 논문에서 필요한 이유: multi-level analog storage와 cell density/accuracy trade-off를 이해하기 위해 필요하다.
- 사용자의 이해: 4b analog weight는 16개 voltage state를 구분해야 하므로 leakage/noise에 의한 state overlap을 줄이기 위해 큰 capacitor가 필요하고, 이 때문에 cell density가 낮아질 수 있다고 자기 설명했다. current-based operation은 transistor non-linearity와 process variation 때문에 multiplication accuracy가 제한될 수 있다는 점도 확인했다.

#### 3T-2C capacitive coupling / leakage-tolerant computing
- 등장 위치: Section II-B, Fig. 2(e), references [21], [22]
- 논문에서 필요한 이유: storage-node leakage가 multiplication result에 직접 영향을 주지 않도록 voltage domain을 분리하는 구조를 이해하기 위해 필요하다.
- 사용자의 이해: Fig. 2(e)는 storage node와 multiplication logic의 voltage domain을 분리하고, cell 내부 transistor logic에서 1-b multiplication을 digital domain에서 수행한 뒤 coupling capacitor를 통해 결과를 RBL accumulation에 전달한다는 overview-level 흐름을 이해했다. leakage robustness의 핵심은 “capacitor를 사용했다”는 사실 자체가 아니라 storage voltage가 analog current magnitude에 직접 연결되지 않도록 storage domain과 compute domain을 분리한 것이라고 자기 설명으로 수정·확인했다. exact transistor truth table, switching sequence, IA/W mapping과 coupling mechanism은 overview에 충분히 제시되지 않아 reference [21] DynaPlasia 원 논문을 확보한 뒤 transistor-level deep dive하기로 했다.

### 별도로 이어가는 선수지식

#### NVM Fundamentals — ReRAM, MRAM, PCM과 NVM-CIM

- Status: sufficient-for-paper
- 논문에서 필요한 이유: Section III의 ReRAM/MRAM/PCM resistance-state storage, LRS/HRS, conductance-based multiplication, NVM-CIM의 low signal margin과 nonlinearity를 이해하기 위해 필요했다.
- 이 논문에 충분한 기준: ReRAM/MRAM/PCM의 물리적 저장 mechanism 차이와 공통적인 resistance-state sensing을 설명하고, G=1/R 및 I=VG에서 activation을 voltage, weight를 conductance에 대응시켜 NVM-CIM multiplication/MAC과 연결할 수 있다.
- Learning Logs:
  - learning-logs/2026/08/2026-08-30-nvm-fundamentals.md

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
| 4T-2C signed/ternary multiplication | 문답으로 수정·확인 | exact encoding은 reference [20] 필요 시 확인 |
| Current accumulation / variation | 사용자 자기 설명 확인 | reference [20] 정량 회로는 필요 시 확인 |
| Voltage clipper / Fig. 2(b) | 문답으로 이해 확인 | transistor-level clipper는 reference [17] 필요 |
| Segmented RBL / Fig. 2(c) | 구조적 이해 확인 | [19]의 세부 timing/charge path는 원 논문 필요 |
| Common-mode / reference cell array | 사용자 자기 설명 확인 | ADC 세부 구조는 overview 범위 밖 |
| 3T-1C 4b-4b multiplication | 사용자 자기 설명 확인 | [18]의 transistor equation/timing은 원 논문 필요 |
| 3T-2C capacitive coupling | overview-level 이해 확인 | [21]/[22] 원 논문으로 truth table·switching deep dive 예정 |
| NVM device fundamentals | 별도 Learning Log 학습 완료, 논문 읽기에 충분 | learning-logs/2026/08/2026-08-30-nvm-fundamentals.md와 Section III circuit examples 연결 완료 |

## 7. Key Idea

> 한 문장 요약: SRAM-CIM의 area/weight-density/volatility 한계를 보완하기 위해 DRAM과 NVM을 CIM에 활용하되, DRAM의 leakage/refresh와 NVM의 nonlinearity/low signal margin/write overhead를 회로·데이터패스·hybrid architecture로 완화하면서 accuracy, density, throughput과 energy efficiency 사이를 설계하는 것이 이 overview의 핵심이다.

## 8. Architecture

전체 overview reading 완료. Section II DRAM-CIM과 Section III NVM-CIM의 대표 circuit/data-path design space를 함께 기록한다.

- 주요 component: 1T1C DRAM cell array, WL, BL/RBL/WBL, SA, digital-PIM/PNM compute logic, 2T-1C/4T-2C Gain-Cell, voltage clipper, segmented RBL/transmission gate, reference cell array/ADC reference path, 3T-1C current-based cell, 3T-2C capacitive-coupling cell, ReRAM/MRAM/PCM resistance cells, complementary NVM cell, Flash/SAR ADC, VTC/TDC, SLC/MLC hybrid array와 NMC compute unit
- Data path: conventional/digital-PIM은 cell → BL/SA sensing → digital compute 경로를 유지한다. cell-array-level DRAM-CIM은 shared BL current, charge sharing 또는 segmented BL을 computation/accumulation에 활용한다. 3T-2C는 storage node와 compute voltage domain을 분리하고 cell 내부 1-b multiplication result를 coupling capacitor를 통해 RBL accumulation으로 전달한다.
- Control: Fig. 2(a)는 64-row parallel current accumulation, Fig. 2(b)는 row parallelism을 제거하고 clipping 후 column charge sharing, Fig. 2(c)는 segmented RBL에서 segment당 한 row를 병렬 activation한 뒤 segment voltages를 charge sharing, Fig. 2(d)는 Q1 current amplitude와 Q2 pulse width를 이용한 4b-4b multiplication, Fig. 2(e)는 digital-domain 1-b multiplication과 capacitive coupling을 사용한다.
- Memory organization: 1T1C는 shared BL 구조, Gain-Cell은 RBL/WBL 분리, [19]는 RBL segmentation과 reference cell array를 사용한다.
- Parallelism: multiple-row current accumulation, column charge sharing, segment-level row parallelism이 서로 다른 robustness/parallelism trade-off를 형성한다.
- Dataflow: DRAM-CIM은 각 cell/row의 multiplication contribution을 BL/RBL current 또는 charge-domain에서 accumulate한다. NVM-CIM은 cell conductance G와 input voltage V에 의해 생성된 current contribution을 column에서 합산해 MVM/MAC을 구성하고, architecture에 따라 BL voltage sensing, differential sensing, discharge-time sensing 또는 NMC peripheral compute로 결과를 읽는다.

### Architecture Walkthrough

현재까지의 DRAM-CIM 흐름은 1T1C의 높은 density와 cell-array parallelism을 활용하는 대신 destructive read, leakage/noise, SA overhead와 analog variation이 문제로 등장하고, Gain-Cell 계열이 read/write path 분리와 새로운 computation datapath로 이를 완화하는 방향이다. Fig. 2(a)는 complementary 4T-2C pair가 1-b IA × ternary W를 수행하고 64 rows의 current를 RBL에서 accumulate하지만 process variation에 민감하다. Fig. 2(b)는 self-detect voltage clipping으로 row parallelism을 희생하고 robustness를 높인다. Fig. 2(c)는 RBL segmentation으로 segment마다 한 row를 동시에 계산하고 이후 charge sharing으로 accumulate하여 row parallelism을 일부 회복하며, reference cell array를 ADC reference로 사용해 common-mode leakage/coupling error를 줄인다. Fig. 2(d)는 4b analog weight가 Q1 current magnitude를, 4b IA가 Q2 pulse width를 제어하는 current-time multiplication을 사용하지만 large capacitor, non-linearity와 variation trade-off가 있다. Fig. 2(e)는 capacitive-coupling과 voltage-domain separation을 사용해 storage leakage가 1-b multiplication/accumulation에 직접 영향을 주는 것을 줄이고 큰 storage capacitor 요구를 완화한다. Section III에서는 NVM resistance/conductance를 computation primitive로 사용하는 구조를 분석했다. XNOR-RRAM/MRAM은 complementary cell과 current/voltage sensing을 사용하며, nonlinear BL transfer에는 [26]의 nonlinear-reference Flash ADC가 사용된다. [29]의 4T-4R dual complementary coding은 BL/BLB differential output을 이용해 voltage transfer의 linearity를 높여 SAR ADC sensing을 가능하게 하고, 4T-4R과 two 2T-2R mode를 accuracy/efficiency 요구에 따라 reconfigure한다. [23]은 BL parasitic capacitor를 precharge한 뒤 computation current에 따른 discharge latency를 sensing하는 time-space readout으로 DC-current-free operation을 구현한다. [24]/[25]는 SLC/MLC hybrid로 signal margin과 density/efficiency를 절충하고, [25]는 CIM과 NMC를 한 macro에서 선택해 accuracy와 throughput/efficiency를 trade-off한다.

## 9. Method

부분 분석 중.

- 1T1C DRAM에서 multiple rows를 동시에 activate하여 여러 cell의 상태를 shared BL에 반영하고 bitwise Boolean operation을 수행한다.
- [15]는 cell capacitors의 charge sharing으로 IA에 대응하는 analog voltage를 만들고, weight value에 따라 cells 사이의 charge sharing을 수행해 multi-bit IA와 W의 MAC을 구현한다. 구체 circuit은 overview에 충분히 제시되지 않음.
- [16]은 SNN을 채택하여 scalar IA 대신 spike를 사용하고, cell-column charge sharing으로 integration을, SA operation으로 firing을 구현한다. 구체 threshold circuit은 overview에 충분히 제시되지 않음.
- 1T-1C read/computation의 destructive read와 frequent SA recovery overhead를 줄이기 위해 Gain-Cell은 RBL과 WBL을 분리하여 non-destructive read path를 computing datapath로 사용한다.
- Fig. 2(a)의 4T-2C complementary pair는 1-b IA와 ternary W multiplication을 수행하고, 64 rows의 current contributions를 병렬 accumulate한다. process variation에 따른 cell current mismatch가 accuracy 문제로 이어질 수 있다.
- Fig. 2(b)는 row parallelism을 제거하고 각 1-b multiplication 뒤 RBL voltage를 predefined reference voltage로 clipping한 후 column charge sharing으로 accumulation해 leakage/variation 영향을 줄인다.
- Fig. 2(c)는 RBL을 transmission gate로 여러 row segments로 나누고 segment당 한 row를 동시에 계산한 뒤 segment RBL voltages를 charge sharing한다. [19]는 reference cell array를 ADC reference로 사용해 common-mode leakage/coupling error를 완화한다.
- Fig. 2(d)는 storage capacitor의 4b analog W가 Q1 current amount를, pulse-width encoded 4b IA가 Q2 turn-on time을 결정하는 current-time multiplication으로 4b-4b operation을 구현한다.
- Fig. 2(e)는 storage node와 multiplication voltage domain을 분리하고 digital-domain 1-b multiplication result를 capacitive coupling으로 RBL에 전달해 leakage-tolerant computation을 구현한다. exact truth table/switching은 overview 범위 밖이며 [21]/[22] deep dive가 필요하다.
- ReRAM, MRAM, PCM은 물리 mechanism은 다르지만 resistance/conductance state로 data를 표현하며, NVM-CIM에서는 G=1/R와 I=VG를 이용해 activation voltage와 stored conductance의 곱을 current contribution으로 만든다.
- [26]의 XNOR-RRAM은 PU transistor와 cell resistance의 voltage division으로 BL voltage를 만들지만 non-ideal resistance로 nonlinear transfer가 생겨 nonlinear reference를 쓰는 Flash ADC로 linear quantization한다.
- [27]은 1-b input vector와 4-b matrix의 MRAM-CIM에서 4-column current output을 current combiner로 한 ADC에 공급하며, [28]은 refined bit-cell로 XNOR readout margin을 높인다. exact multi-bit weighting/current-combining circuit은 overview만으로 확정하지 않는다.
- [29]의 4T-4R dual complementary coding은 complementary WL/BL을 이용해 BL/BLB의 differential voltage를 더 선형적으로 만들고 SAR ADC sensing을 가능하게 한다. 4T-4R은 higher-accuracy mode, two 2T-2R은 higher-efficiency/lower-accuracy mode로 reconfigure할 수 있다.
- [23]의 time-space readout은 BL parasitic capacitor를 precharge하고 computation current로 discharge한 latency를 VTC/TDC 계열에서 sensing해 DC-current-free operation과 higher efficiency를 얻는다.
- [24]는 8-bit weight의 upper 2-bit를 SLC에 저장해 signal margin을 확보하고 lower 6-bit를 MLC에 저장해 efficiency를 높인다. [25]는 MLC에 저장하는 bit 수를 0/2/4/6/8 bit로 reconfigure하고 CIM/NMC mode를 accuracy requirement에 따라 선택한다.
- NVM-NMC는 multiple-row activation을 제거하고 cell array 주변/아래의 computing unit에서 연산해 computation accuracy를 높이는 대신 throughput과 efficiency를 희생한다.

## 10. Experiments

이 논문은 새로운 단일 hardware implementation의 실험 결과를 제시하는 논문이 아니라 기존 DRAM/NVM-CIM 연구를 정리한 tutorial/overview이므로 통합된 baseline, workload, dataset, hardware configuration 또는 measurement methodology가 없다. 각 cited work의 정량 결과는 Table I/II와 references에 분산되어 있으며 이번 reading에서는 개별 수치를 재검증하지 않았다.

- Baseline: 통합 baseline 없음
- Workloads / Models: cited works별로 다름; overview 수준에서 NN inference를 중심으로 비교
- Dataset: 통합 dataset 없음
- Hardware configuration: cited works별 DRAM/NVM-CIM macro
- Metrics: density, energy/efficiency, throughput, accuracy/signal margin 등 design trade-off 중심
- Simulation / Measurement methodology: cited original works를 따라야 하며 overview 자체의 신규 measurement는 없음

## 11. Results

이 overview의 main result는 하나의 새로운 정량 성능 수치가 아니라 DRAM/NVM-CIM의 circuit design space와 challenge/solution map을 정리한 것이다.

- Performance: 높은 cell/row/column parallelism을 활용하는 CIM과 accuracy를 우선하는 NMC/reconfigured mode 사이의 trade-off를 정리한다.
- Energy / Efficiency: DRAM cell-array computation, NVM time-space readout, MLC hybrid와 CIM mode가 data movement/DC current/peripheral overhead를 줄이는 방향을 보여 준다.
- Area / Cost: standard/high-density memory cell을 유지하는 것과 custom CIM cell/peripheral compute 기능 사이의 density·area trade-off가 핵심이다.
- Accuracy: clipping, reference array, complementary coding, differential sensing, SLC/MLC hybrid와 NMC mode가 leakage/variation/nonlinearity/low signal margin을 완화한다.
- Other: process compatibility, DRAM refresh control, NVM write/programming overhead가 scale-up의 주요 future challenge로 남는다.

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
| Fig. 2(a) 64-row current accumulation의 높은 row parallelism | cell-to-cell current mismatch와 process variation이 accumulation error로 직접 반영될 수 있음 | Section II-B, Fig. 2(a) |
| Fig. 2(b) clipping으로 leakage/variation robustness 향상 | row parallelism을 제거하고 column parallelism만 사용 | Section II-B, Fig. 2(b) |
| Fig. 2(c) segmented RBL로 row parallelism 일부 회복 | segmented BL, transmission gate, reference array 등 추가 회로/조직 복잡도 | Section II-B, Fig. 2(c) |
| 3T-1C single-cell 4b W와 4b IA analog multiplication | large storage capacitor로 density 감소, transistor non-linearity/variation으로 accuracy 제한 | Section II-B, Fig. 2(d) |
| 3T-2C leakage-tolerant capacitive-coupling operation으로 smaller storage capacitor와 higher density 가능 | exact circuit mechanism은 overview에 충분히 설명되지 않아 [21]/[22] reference 확인 필요 | Section II-B, Fig. 2(e) |
| Nonlinear-reference Flash ADC로 nonlinear BL transfer를 linear quantization code에 mapping | reference threshold generation과 ADC peripheral cost가 필요 | Section III-A, [26] |
| 4T-4R dual complementary coding으로 differential output linearity와 readout margin 개선 | 4T-4R mode는 cell/resource cost가 증가하며 2T-2R mode 대비 efficiency를 희생 | Section III-A, [29] |
| Time-space readout으로 DC-current-free operation과 higher efficiency | BL discharge latency/VTC/TDC 기반 sensing path가 필요 | Section III-B, [23] |
| SLC/MLC hybrid로 signal margin과 weight density/efficiency를 절충 | MLC bit 비중이 커질수록 signal margin/accuracy 부담 증가 | Section III-C, [24], [25] |
| NMC mode로 multiple-row analog accumulation을 피하고 accurate computation | throughput과 efficiency 희생 | Section III-C, [25] |

## 13. Limitations

### Authors' Limitations

현재까지 확인된 limitation:
- SRAM-CIM: transistor/area overhead, 1 bit/cell weight density 제약, volatility
- DRAM-CIM: capacitor charge leakage/noise가 computation에 영향을 줄 수 있음
- NVM-CIM: non-linearity, low signal margin
- Digital-PIM/PNM: cell array에서 직접 computation하지 않고 conventional sensing/read path가 남아 있어 energy/latency improvement가 제한될 수 있음
- 1T-1C DRAM-CIM: destructive read 때문에 frequent SA recovery가 필요해 considerable power를 소비할 수 있음
- Gain-Cell: additional transistor와 separated read/write path로 1T-1C보다 density가 낮음
- 4T-2C current-based row-parallel accumulation: process variation으로 cell current mismatch가 생길 수 있음
- 3T-1C analog 4b weight storage: large capacitor 요구로 cell density 제한, transistor non-linearity/variation으로 accuracy 제한
- NVM-CIM: static current, nonlinear voltage characteristics와 limited sensing margin
- NVM process limitation: ReRAM/MRAM/PCM 등 memory type에 따라 가능한 fabrication process가 제한되고 eDRAM/DRAM-CIM circuit이 서로 다른 process에 그대로 이식되기 어려울 수 있음
- Custom CIM cell: in-fab standard cell array보다 density가 낮아질 수 있음
- DRAM refresh: energy와 throughput overhead, large-scale에서 computation/memory access와 refresh scheduling/control 복잡도
- NVM write: high voltage/high latency, 경우에 따라 iterative write-read-verify와 multiple voltage sources 또는 pulse-width modulation 필요

### My Observations

- SRAM pushed-rule high density와 SRAM-CIM area overhead는 비교 수준이 달라 모순이 아니다.
- eDRAM의 logic compatibility는 logic 연산 자체를 더 빠르고 정확하게 만든다는 의미가 아니라 logic 공정/회로와 함께 집적할 수 있다는 의미다.
- cell-array-level DRAM-CIM의 이점은 external bandwidth를 단순히 높이는 것보다, memory array 내부의 병렬성을 computation에 활용해 외부 data movement 요구량을 줄이는 관점으로 이해하는 것이 적절하다.
- 사용자는 memory-bound NPU에서 MAC utilization이 낮다면 일부 compute area를 on-chip memory capacity에 재배분해 off-chip access를 줄이는 것이 전체 inference throughput을 높일 수도 있다고 architecture-level로 연결했다. 이는 논문의 직접 주장이라기보다 기존 학습과 연결한 사용자 관찰이다.
- [15], [16]의 overview 문장은 핵심 computation mapping은 보여 주지만 exact capacitor connection, weight-dependent charge-sharing path, SNN firing threshold circuit까지는 충분히 설명하지 않는다. 현재 단계에서는 reference를 모두 따라가지 않고 overview의 design-space map을 먼저 완성하기로 했다.
- Fig. 2(a)→(b)→(c)는 row parallelism과 analog robustness 사이의 trade-off를 보여 준다: direct current accumulation은 높은 parallelism을 주지만 variation에 민감하고, clipping은 robustness를 높이는 대신 row parallelism을 희생하며, segmented RBL은 segment-level parallelism을 다시 확보한다.
- Fig. 2(e)의 leakage robustness는 단순히 capacitor를 사용했기 때문이 아니라 storage-node analog voltage가 multiplication magnitude에 직접 연결되지 않도록 storage domain과 compute domain을 분리한 데 핵심이 있다.
- Fig. 2(e)의 exact transistor truth table, IA/W switching sequence와 coupling mechanism은 overview로 확정할 수 없어 [21] DynaPlasia 원 논문을 확보한 뒤 별도 deep dive하기로 했다.
- NVM-CIM에서는 같은 G-based multiplication이라도 voltage-domain sensing, current/differential sensing, time-domain sensing, SLC/MLC hybrid와 NMC mode로 accuracy/efficiency trade-off를 서로 다르게 설계할 수 있음을 확인했다.
- Section IV의 “process limitation”은 computation process가 아니라 semiconductor fabrication/manufacturing process limitation임을 수정·확인했다.
- Future direction은 custom CIM cell만 확장하기보다 standard high-density bit-cell을 유지하고 peripheral 또는 cell+peripheral compute를 결합하거나, SRAM/digital architecture와 hybrid화하고 algorithm/compiler와 hardware를 co-design하는 방향까지 포함한다.

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
- 4T-2C의 signed representation은 일반 binary sign-bit가 아니라 complementary gain-cell pair를 이용한 signed weight 표현임을 확인했다.
- 1-b IA와 ternary W, 4-bit=16 levels의 의미를 수정·확인했다.
- Fig. 2(a) current accumulation과 process variation mismatch, Fig. 2(b) voltage clipping, Fig. 2(c) segmented RBL 및 common-mode/reference array의 역할을 확인했다.
- Fig. 2(d)의 Q1 current amplitude × Q2 pulse duration으로 4b-4b multiplication이 표현되는 직관을 확인했다.
- Fig. 2(e)의 capacitive coupling, storage/compute voltage-domain separation과 leakage-tolerant computing의 overview-level 의미를 확인했다.
- MVM은 matrix의 각 dot product를 병렬로 수행하는 연산이며, NVM-CIM에서 G를 weight, V를 IA로 대응시키고 column current summation으로 MAC/MVM을 구현하는 연결을 확인했다.
- PU transistor와 cell resistance의 voltage division, nonlinear BL transfer function과 nonlinear-reference Flash ADC의 역할을 확인했다.
- 4T-4R dual complementary coding의 BL/BLB differential sensing과 SAR ADC 사용 가능성, 4T-4R↔2T-2R reconfiguration의 accuracy-efficiency trade-off를 확인했다.
- Time-space readout에서 BL parasitic capacitance precharge, computation current에 따른 discharge time과 TDC sensing을 확인했다.
- SLC/MLC hybrid에서 [24]의 upper 2-bit SLC + lower 6-bit MLC와 [25]의 0/2/4/6/8-bit MLC reconfiguration을 확인했다.
- NMC의 multiple-row activation 제거와 peripheral computing unit 배치, accuracy 대 throughput/efficiency trade-off를 확인했다.
- Section IV의 fabrication process limitation, DRAM refresh overhead/control, NVM write programming overhead와 세 가지 future research direction을 확인했다.

### 비판적 질문

- cell-array-level DRAM-CIM이 data movement를 줄이는 대신 leakage/noise에 더 직접 노출될 때 실제 robustness/accuracy를 어떻게 확보하는가? 이후 회로 설명에서 확인한다.
- Gain-Cell이 non-destructive read로 SA overhead를 줄이는 대신 density를 희생할 때, 실제 efficiency/density optimum은 어떤 workload와 circuit configuration에서 결정되는가?

### 후속 연구 질문

- memory-bound AI accelerator에서 compute area와 on-chip memory area를 어떻게 배분해야 utilization/throughput/energy가 최적화되는가? 논문의 직접 범위를 넘어선 사용자 연결 질문으로 보존한다.
- [15]/[16] 같은 analog/SNN DRAM-CIM에서 charge sharing의 정확도와 leakage/noise robustness가 실제 multi-bit computation에 어떤 제약을 주는지 원 논문 deep-dive 후보로 보존한다.
- [21] DynaPlasia 원 논문을 확보한 뒤 Fig. 2(e) 3T-2C cell의 transistor/capacitor 역할, IA/W 입력 위치, truth table, switching sequence, storage/compute-domain separation, coupling capacitor의 ΔV/ΔQ 전달과 leakage-tolerant mechanism을 transistor-level로 분석한다.

## 15. Connection to My Research Interest

- 흥미로운 점: memory hierarchy에서 단순히 external bandwidth를 높이는 것뿐 아니라 cell-array internal parallelism과 charge sharing을 computation에 활용해 data movement 자체를 줄일 수 있다는 점
- 더 탐구하고 싶은 부분: multiple-row activation의 Boolean sensing mechanism, analog charge-sharing MAC/SNN integration, Gain-Cell의 non-destructive computing datapath와 leakage/noise robustness, [21] DynaPlasia 3T-2C의 transistor-level capacitive-coupling truth table, NVM complementary/time-domain/hybrid sensing의 회로-level accuracy–efficiency trade-off
- 다른 논문과의 연결: 기존 memory-wall, analog/digital CIM, tiling/Roofline 학습에서 다룬 data movement와 memory-bound/utilization 개념과 연결됨
- 가능한 research direction: compute-resource와 on-chip memory capacity/bandwidth의 area allocation trade-off, DRAM-CIM의 robustness-aware circuit/architecture 설계, destructive-read/SA-overhead와 density의 trade-off

## 16. Final Summary

### Problem

SRAM-CIM의 area/weight-density/volatility 한계로 DRAM/NVM-CIM이 재검토되지만, DRAM leakage/noise와 NVM non-linearity/low signal margin이라는 새로운 challenge가 있다. 1T1C DRAM에서는 conventional read path를 유지하는 digital-PIM/PNM의 data movement/latency 개선에도 한계가 있고, cell-array computation은 destructive read와 frequent SA recovery power overhead를 동반할 수 있다.

### Key Idea

DRAM/NVM의 memory 특성을 CIM에 활용하되 각 technology의 circuit challenge를 해결해야 한다. 1T1C DRAM-CIM에서는 multiple-row activation, BL-level parallelism, capacitor charge sharing을 이용해 cell data를 computation에 직접 활용할 수 있고, Gain-Cell은 read/write path를 분리해 non-destructive computing datapath를 제공한다.

### Architecture

1T1C DRAM array의 shared BL, WL multiple activation, SA/conventional read path, digital-PIM/PNM과 cell-array-level CIM의 위치 차이를 분석했다. [15]의 charge-sharing multi-bit MAC, [16]의 SNN integration/firing mapping, Gain-Cell의 RBL/WBL separation과 non-destructive read path, Fig. 2(a)~(e)의 current/charge/capacitive-coupling datapath를 overview-level로 분석했다. NVM-CIM에서는 complementary XNOR cell, nonlinear-reference Flash ADC, 4T-4R dual complementary differential sensing/SAR ADC, time-space readout의 BL discharge latency, SLC/MLC hybrid와 CIM/NMC reconfiguration까지 전체 design space를 읽었다.

### Main Result

이 tutorial/overview의 main result는 단일 신규 chip 수치가 아니라 DRAM/NVM-CIM이 SRAM-CIM의 한계를 보완하는 동시에 각 memory technology 고유의 leakage, refresh, nonlinearity, signal margin, process와 write overhead를 만든다는 design-space map과, 이를 완화하기 위한 representative circuit/datapath techniques를 체계적으로 정리한 것이다.

### Main Trade-off

cell array에 computation을 더 가까이 가져갈수록 conventional data movement와 SA overhead를 줄이고 internal parallelism을 활용할 수 있지만, analog current/charge-domain computation에서는 variation, leakage, non-linearity와 density trade-off가 생긴다. Fig. 2(a)는 높은 row parallelism 대신 current mismatch에 민감하고, Fig. 2(b)는 clipping robustness 대신 row parallelism을 희생하며, Fig. 2(c)는 segmented BL로 이를 절충한다. Fig. 2(d)는 4b-4b functionality 대신 large capacitor와 analog accuracy cost가 있고, Fig. 2(e)는 voltage-domain separation/capacitive coupling으로 leakage tolerance와 density를 개선한다.

### Limitation

SRAM-CIM의 transistor/area overhead, 1 bit/cell weight density와 volatility에 더해, DRAM-CIM은 leakage/noise, destructive read/refresh overhead와 process/density 제약을 갖고 NVM-CIM은 static current, nonlinearity, low signal margin, process 제한과 high-voltage/high-latency write/programming overhead를 갖는다.

### 내가 기억할 한 문장

DRAM/NVM-CIM은 SRAM-CIM의 density·non-volatility 한계를 보완하면서 memory device 자체를 computation에 활용하지만, leakage/refresh/nonlinearity/signal-margin/write/process 문제를 회로·sensing·hybrid architecture와 algorithm/compiler co-design으로 해결하며 accuracy·density·throughput·energy 사이의 trade-off를 설계해야 한다.

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


### 2026-08-30

- 읽은 범위: Section II-B Gain-Cell DRAM의 Fig. 2(a)~(e) 전체와 Section III NVM-CIM 도입부의 ReRAM/MRAM/PCM resistance-storage mechanism 소개 문장까지.
- 이해한 내용: 4T-2C complementary pair의 1-b IA × ternary W, Q1 driving transistor와 64-row current accumulation, process-variation current mismatch, Fig. 2(b) voltage clipping과 column-only charge sharing, Fig. 2(c) segmented RBL/segment-level row parallelism 및 reference cell array의 common-mode error cancellation, Fig. 2(d) 4b analog W × 4b pulse-width IA의 current-time multiplication과 capacitor-size/non-linearity trade-off, Fig. 2(e) storage/compute voltage-domain separation과 capacitive-coupling 기반 leakage-tolerant operation을 문답과 자기 설명으로 확인했다.
- 새롭게 발생한 질문: Fig. 2(e)의 exact 3T-2C transistor truth table, IA/W 입력과 switching sequence, coupling capacitor의 실제 ΔV/ΔQ 전달 방식과 leakage-tolerant mechanism을 [21] DynaPlasia 원 논문에서 transistor-level로 확인하고 싶다. Section III를 읽기 위해 ReRAM/MRAM/PCM의 MIM/MTJ/phase-change 구조, LRS/HRS와 sensing에 대한 NVM fundamentals 학습이 필요하다고 판단했다.
- Bridge 변화: Fig. 2(a)~(e) 관련 개념은 논문 안에서 overview-level prerequisite로 해결·확인했다. NVM fundamentals는 별도 Learning Log로 학습하기로 사용자와 결정했으나 아직 실제 Learning Log가 생성되지 않았으므로 이번 checkpoint에는 studying Bridge로 연결하지 않는다.
- 종료 당시 Resume Point: Section III. NVM-CIM, PDF page 3 — ReRAM/MRAM/PCM이 resistance state를 이용한다는 도입 문장까지 읽음. 다음 논문 문장은 “NVM brings unique advantages to CIM, non-volatility...”이며, 그 전에 별도 NVM fundamentals 학습을 진행한다.

### 2026-09-01

- 읽은 범위: Section III NVM-CIM의 “NVM brings unique advantages to CIM...”부터 Section III-A Current-Based Operation With Complementary Cell, III-B Time-Based Operation, III-C Hybrid Method, Section IV Challenges and Future Research Directions, Section V Conclusion까지 완료.
- 이해한 내용: NVM-CIM에서 G=1/R와 I=VG를 activation/weight multiplication 및 MVM으로 연결했다. [26]의 nonlinear BL voltage transfer와 nonlinear-reference Flash ADC, [27]/[28] MRAM XNOR/multi-bit current combining/readout margin, [29]의 4T-4R dual complementary differential sensing과 SAR ADC 및 2T-2R reconfiguration, [23]의 BL parasitic-capacitance discharge-time readout, [24]/[25]의 SLC-MLC hybrid와 CIM/NMC mode를 문답으로 이해했다. Section IV에서는 process limitation을 fabrication process limitation으로 수정·확인하고, DRAM refresh의 energy/throughput/scheduling overhead와 NVM write의 high voltage/high latency/write-read-verify/programming control을 이해했다. Future direction은 standard high-density bit-cell 유지, peripheral/cell-peripheral compute, SRAM/digital hybrid, algorithm/compiler-hardware co-design으로 정리했다. Conclusion에서는 DRAM/NVM-CIM이 고유 challenge를 갖지만 향후 energy-efficient AI/ML CIM hardware에서 중요한 역할을 할 것이라는 저자의 관점을 사용자 언어로 설명했다.
- 새롭게 발생한 질문: [21] DynaPlasia Fig. 2(e)의 exact transistor-level truth table/switching/capacitive-coupling mechanism은 overview 범위 밖 질문으로 계속 보존한다. [27]/[29]의 exact multi-bit current weighting과 differential cancellation circuit도 원 논문 확인 없이는 확정하지 않는다.
- Bridge 변화: 2026-08-30에 저장된 NVM Fundamentals Learning Log를 성공 comment/commit과 실제 파일로 확인했으며, 현재 paper reading에 충분하므로 sufficient-for-paper로 연결한다.
- 종료 당시 Resume Point: Section V Conclusion까지 전체 overview reading 완료. 다음은 [21] DynaPlasia deep dive 또는 후속 paper comparison 중 선택한다.

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

> “64개의 cell에서 병렬로 IA, W의 곱 연산을 해서 BL에서 accumulate 하는 과정에서, 각각의 cell에서 나오는 current의 양이 일정하지 않기에 ... BL에서 다 더해버리면 분명 오류가 발생할 것” — Fig. 2(a) current mismatch의 accumulation error를 자기 언어로 설명함.

> “reference cell array가 있다면 Vsignal과 Vref를 비교하여 ADC를 적용하기 때문에 오류의 영향이 줄어듬 ... Vsignal, Vreference 모두 같은 error가 발생하였고, 이 값을 서로 비교하면 ... error를 소거할 수 있기 때문에” — common-mode error와 reference voltage의 역할을 자기 설명으로 확인함.

> “IA를 더 큰 값으로 바꾸면 IA의 pulse가 더 길어진다 ... Q2가 active되는 시간이 늘어난다 ... BL에 더 많은 charge가 흐르게 된다. 따라서 BL은 multiplication 결과를 더 크게 인식한다.” — Fig. 2(d)의 pulse-width IA와 current-time multiplication을 자기 설명함.

> “1개의 bit는 0/1로 구분되니깐 2bit weight는 4개의 서로 다른 값, 4bit weight는 16개의 서로 다른 값을 표현할 수 있고, Q1이 4bit weight를 구분하려면 총 16개의 전류 ... 를 구분할 수 있어야 한다” — 4-bit와 16 distinguishable levels의 관계를 수정 후 자기 설명함.

> “하나의 capacitor에 많은 bit를 저장해야 하기 때문에, 4bit라면 16개의 상태를 capacitor에서 구분할 수 있어야 함 ... capacitor size를 키워서 이러한 오류를 줄여야함.” — 4b analog storage와 capacitor-size/density trade-off를 자기 설명함.

> “multiplication은 weight가 저장되어 있는 capacitor 오른쪽에 있는 CMOS에서 발생함 ... 이 값이 capacitor를 통해 RBL에 전달됨 ... RBL에서는 여러 다른 cell에서의 결과를 accumulation함.” — Fig. 2(e)의 in-cell multiplication과 RBL accumulation을 구분했으며, 이후 leakage robustness의 원인을 voltage-domain separation으로 수정함.

> “기존에는 storage voltage를 통해 발생된 current를 직접적으로 연산에 사용하여 storage voltage에서 leakage가 발생하면 ... 연산값에 오류를 일으켰다. 그러나 figure2(e)에서는 storage domain과 compute domain을 분리했다.” — leakage-tolerant computing의 핵심을 storage/compute-domain separation으로 자기 설명함.

> “fig2(e)의 회로적 특징도 궁금함. truth table이 어떤식으로 작용되는지, 회로적으로 어떻게 구현되는지 궁금해 reference에 적힌 논문을 읽고 ... 설명해줄 수 있니?” — [21] DynaPlasia 원 논문 확보 후 transistor-level deep dive 후보로 보존함.

> “NVM에 대한 기본적인 학습이 필요하다고 생각하니? 그러면 새로운 학습 세션을 통해 NVM의 동작원리나 기본적인 특징등을 학습하는 것을 도와줘” — Section III 진행 전 ReRAM/MRAM/PCM fundamentals를 별도 Learning Log로 학습하기로 결정함.

> “MVM multiple dot products; cell VG with V as IA and conductance as weight maps to MVM.” — NVM-CIM의 conductance-based MVM 연결을 자기 설명으로 확인함.

> “8bit weight가 있으면 2bit 이상 정도는 SLC에 저장하고, 6bit 이하 정도는 MLC에 저장한다” — 논문 [24]의 정확한 표현은 upper 2-bit를 SLC, remaining lower 6-bit를 MLC에 저장하는 것으로 다시 확인함.

> “process limitation 안에서 다루는 내용이 NVM의 type에 따른 공정 문제, DRAM-CIM, eDRAM은 서로 각각 다른 공정 과정을 거쳐야 한다는 점...” — process를 computation process가 아니라 fabrication/manufacturing process로 수정 후 자기 설명함.

> “refresh 상태이면 access를 못하기 때문에?” — DRAM 전체가 항상 완전히 멈춘다고 일반화하지 않고, refresh가 memory resource를 점유해 memory access/CIM computation scheduling과 throughput에 overhead를 준다는 방향으로 확인함.

> “NVM의 write operation은 high voltage와 high latency를 요구한다...” — 원하는 conductance state programming과 이후 I=VG read/computation을 구분하고, write-read-verify·multiple voltage/pulse control이 write overhead와 연결됨을 확인함.

> “chip에서만 해결하는 것이 아니라 알고리즘 영역에서 latency와 energy를 적게 쓰려는 방법을 찾는 것 같음” — lightweight algorithm/compiler와 hardware co-design이라는 future direction으로 확인함.

> “SRAM-CIM의 한계를 극복하기 위해 DRAM, NVM-CIM에 대해 연구했고...” — 알고리즘 자체보다 energy-efficient AI/ML CIM hardware 구현에 DRAM/NVM-CIM이 중요한 역할을 할 것이라는 conclusion으로 표현을 수정·확인함.
