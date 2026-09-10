# Paper Note: An Overview of Processing-in-Memory Circuits for Artificial Intelligence and Machine Learning

## Metadata

- Title: An Overview of Processing-in-Memory Circuits for Artificial Intelligence and Machine Learning
- Document type: paper-note
- Paper type: foundational
- Venue / Year: IEEE Journal on Emerging and Selected Topics in Circuits and Systems / 2022
- Authors: Donghyuk Kim; Chengshuo Yu; Shanshan Xie; Yuzong Chen; Joo-Young Kim; Bongjin Kim; Jaydeep P. Kulkarni; Tony Tae-Hyoung Kim
- Paper link: https://doi.org/10.1109/JETCAS.2022.3160455
- Started: 2026-09-10
- Checkpoint recorded at: 2026-09-10T14:04:11Z
- Related notes: 없음

## 1. Reading Checkpoint

- Resume Point: 사용자 reading은 아직 시작되지 않음. Abstract, PDF p.1 (journal p.338)의 첫 문장부터 시작한다.

## 2. Prerequisite Bridge

### 논문 안에서 해결한 선수지식

- 없음

### 별도로 이어가는 선수지식

- 없음

## 3. Problem

**Problem being addressed:** AI/ML의 MAC 중심 workload에서 processor와 memory 사이의 빈번한 데이터 전송이 system bottleneck과 높은 전력 소비를 만든다. 이 논문은 데이터 이동을 줄이는 PIM을 SRAM, DRAM, ReRAM의 memory type별 circuit, macro, architecture 관점에서 조사하고, 실제 도입에 필요한 software stack과 연구 과제를 함께 정리한다.

**Limitations of existing approaches:** 전통적인 von-Neumann 구조는 processing element와 memory가 분리되어 대량의 데이터를 interconnect로 이동해야 한다. 기존 PIM 연구도 SRAM의 낮은 density, DRAM의 좁은 cell pitch와 logic integration 제약, ReRAM의 device variation과 sensing·converter 문제를 갖고 있으며, PIM을 host system에 통합하기 위한 offloading, mapping, scheduling, cache coherence 문제도 남아 있다.

**Why this problem matters:** AI/ML의 data-intensive workload에서는 power-hungry data movement를 최소화하는 것이 energy-efficient computing, 특히 edge computing과 large-model acceleration에 중요하다. 저자들은 PIM의 장점은 널리 받아들여졌지만 limitation과 challenge에 대한 종합 조사가 충분하지 않았다고 설명한다.

## 4. Key Idea

**Proposed approach:** SRAM-, DRAM-, ReRAM-based PIM을 memory type과 logic-integration level별로 분류하고 representative bitcell·macro·architecture의 동작과 trade-off를 비교한다. 이어 PIM framework, library, runtime, device driver로 구성된 software stack과 offloading, mapping, scheduling, coherence를 정리하고 data converter, test accuracy, intra-memory data movement를 미래 연구 축으로 제시한다.

**Key mechanism:** 공통 원리는 memory 내부 또는 가까운 위치에서 computation을 수행해 off-chip data movement를 줄이는 것이다. 구현은 SRAM bitline accumulation과 digital MAC, DRAM의 cell/bank/3-D integration, ReRAM conductance 기반 current/voltage sensing처럼 memory device와 integration level에 따라 달라진다.

**What is novel or different:** 단일 PIM circuit을 제안하는 대신 SRAM·DRAM·ReRAM을 bitcell에서 system architecture까지 같은 overview 안에서 다루고, hardware taxonomy를 software-stack adoption challenge와 data-conversion·accuracy·intra-memory-movement research direction까지 연결한다.

## 5. Architecture

### Overall Architecture

- 목적과 system context: AI/ML workload의 processor-memory data movement를 줄이기 위해 computation을 memory cell, bank 또는 stacked-memory logic 가까이에 배치한다.
- 전체 구성과 hierarchy: memory-device별 SRAM PIM, DRAM PIM, ReRAM PIM과 이들을 application에 노출하는 framework-library-runtime-driver software stack으로 구성된다.
- End-to-end operation / dataflow: application operation을 PIM-friendly kernel로 식별하고 memory와 가까운 compute structure로 offload한 뒤, memory 내부 데이터에 대해 logic 또는 MAC을 수행하고 필요한 결과를 sensing·conversion하여 host와 공유한다. 실제 path는 architecture family별로 다르다.

### SRAM PIM

#### Fig. 2(a)-(d) — Analog SRAM PIM Cell Variants

- 근거 위치: Section II-B, PDF pp.2-3, Fig. 2
- 논문 내 역할: standard 6T와 modified 8T/MOMCAP cell이 analog MAC에서 read disturbance, operation diversity, dynamic range와 non-ideality를 어떻게 다루는지 비교한다.
- Main Structure (Components): standard 6T; independent RBL path를 추가한 foundry 8T; differential/custom 8T; 6T 위에 two inverters와 XNOR를 둔 voltage-mode cell; 8T와 MOM capacitor를 결합한 cell.
- Operation Overview: binary input을 WL/RWL에, weight를 SRAM node에 두고 bitline의 current 또는 voltage 변화로 multiplication을 표현하며 column에서 accumulation한다.
- Data / Signal Flow: input WL/RWL → SRAM storage state와 read/discharge path → BL/RBL 변화 → column accumulation 및 sensing.
- Benefits: independent read path는 read disturbance를 줄이고, custom/differential 구조는 지원 MAC 또는 dynamic range를 확장하며, passive capacitor는 residual analog non-ideality를 줄인다.
- Challenges / Trade-offs: foundry 8T는 single-ended read와 큰 bitcell area, custom/current mode는 limited dynamic range와 non-ideality, differential/MOMCAP 구조는 증가한 cell size 또는 transistor/capacitor area overhead를 갖는다.
- 논문이 제공하지 않은 세부사항: 각 cited macro의 전체 timing sequence와 transistor sizing은 이 overview에 제시되지 않는다.

#### Fig. 3(a)-(d) — Analog SRAM Accumulation Modes

- 근거 위치: Section II-B, PDF p.3, Fig. 3
- 논문 내 역할: current-mode, voltage-mode, charge-sharing, capacitive-coupling이라는 analog accumulation design space를 제시한다.
- Main Structure (Components): column-shared BL/RBL, discharge 또는 pull-up/pull-down paths, charge-sharing switch/capacitors 또는 coupling capacitors.
- Operation Overview: cell별 binary multiplication 결과를 discharge current, shared-node voltage, capacitor charge sharing 또는 capacitive coupling으로 column에 누적한다.
- Data / Signal Flow: cell multiplication result → shared bitline/capacitor network → aggregated analog current/voltage → readout.
- Benefits: voltage mode는 rail-to-rail dynamic range를 높이고, charge-domain 방식은 analog non-linearity와 variation을 줄이며 높은 energy efficiency와 throughput을 제공한다.
- Challenges / Trade-offs: current mode는 linearity를 위해 dynamic range 제한이 필요하고 voltage mode에도 residual non-linearity와 variation이 남는다. Charge-sharing은 coupling 방식보다 cell당 switch 하나와 accumulation cycle 하나가 더 필요하며 capacitor area와 charge injection도 문제다.
- 논문이 제공하지 않은 세부사항: 공통 baseline에서 네 방식의 정량 비교는 제공되지 않는다.

#### Fig. 4 — Digital SRAM PIM Macro

- 근거 위치: Section II-C, PDF pp.3-4, Fig. 4
- 논문 내 역할: analog conversion과 PVT-induced non-linearity를 피하는 fully digital PIM 대안을 보여 준다.
- Main Structure (Components): 6T SRAM, XNOR, 1-bit full adder로 된 PIM cell과 stacked unit-column MAC; 후속 예에서는 fused 6T SRAM/NOR cell과 dedicated adder tree.
- Operation Overview: binary multiplication과 accumulation을 digital logic으로 처리하고 필요한 precision에 따라 cell 또는 macro를 조합한다.
- Data / Signal Flow: reconfigurable input/weight → SRAM+logic cell의 binary multiplication → unit-column 또는 adder-tree accumulation → multi-bit MAC output.
- Benefits: physical variation의 영향을 피하고 ADC/DAC data conversion을 제거하며 input, weight, output precision을 재구성할 수 있다.
- Challenges / Trade-offs: memory와 computation block의 hardware redundancy로 unit cell이 커지고 memory density가 낮아지며 precision 확장은 추가 macro와 area를 요구한다.
- 논문이 제공하지 않은 세부사항: Fig. 4 design의 전체 physical implementation과 measured operating condition은 overview 본문에 제시되지 않는다.

### DRAM PIM

#### Fig. 6 — Cell-Level AMBIT and DRISA

- 근거 위치: Section III-B, PDF pp.4-5, Fig. 6
- 논문 내 역할: 좁은 DRAM cell pitch에서 cell/SA-level bulk bitwise computation을 구현하는 대표 구조를 비교한다.
- Main Structure (Components): AMBIT triple-row activation과 dual-contact cell; DRISA 3T1C-NOR, 1T1C-NOR/MIX, 1T1C-ADDER 및 SA 아래 latch, shifter, logic.
- Operation Overview: AMBIT는 세 row의 charge sharing majority와 preset row를 이용해 AND/OR를 만들고 DCC로 NOT을 수행한다. DRISA는 modified/early DRAM cell과 SA 주변 logic으로 NOR, selection, multiplication, addition을 수행한다.
- Data / Signal Flow: multiple WL activation → shared BL charge/sense-amplifier state → Boolean result 또는 SA 아래 latch/logic → adjacent BL/data movement.
- Benefits: cell-level 접근은 bank의 전체 internal bandwidth를 활용하고 bulk bitwise operation을 수행한다.
- Challenges / Trade-offs: DCC 또는 extra logic을 shrinking cell pitch에 넣기 어렵고 DRISA의 modified cell/SA logic도 physical integration 제약을 받는다.
- 논문이 제공하지 않은 세부사항: 비교 구조들의 동일 공정·동일 workload 정량 평가는 제공되지 않는다.

#### Fig. 7 — Bank-Level Newton and HBM-PIM

- 근거 위치: Section III-C, PDF pp.5-6, Fig. 7
- 논문 내 역할: column decoder 뒤의 더 넓은 logic area를 사용해 feasible DRAM PIM을 구현하는 두 사례를 보여 준다.
- Main Structure (Components): Newton의 bank당 16 multipliers, 16-adder reduction tree, 16-bit accumulator와 global buffer; HBM-PIM의 two-bank-shared PCU, interface/execution/register groups, FP16 SIMD units와 PIM controller.
- Operation Overview: Newton은 fixed dataflow와 GWRITE/G_ACT/COMP/READRES command로 bank-parallel MVM을 수행한다. HBM-PIM은 row-address activation으로 PIM mode를 선택하고 CRF에 저장된 programmable instruction을 PCU가 실행한다.
- Data / Signal Flow: memory array/column selector → global buffer 또는 IO SA → bank-side multiplier/adder or PCU → accumulator/register → result readout.
- Benefits: cell pitch에 logic을 넣지 않고 bank parallelism을 활용하며 Newton은 memory-bound model에 fixed MVM을, HBM-PIM은 FP16 programmable computation을 제공한다.
- Challenges / Trade-offs: cell-level PIM처럼 전체 row internal bandwidth를 사용하지 못하며 Newton의 specialization과 HBM-PIM의 programmability는 서로 다른 적용 범위를 갖는다.
- 논문이 제공하지 않은 세부사항: 두 구조를 같은 조건에서 직접 비교한 측정 결과는 제공되지 않는다.

#### Fig. 8 — 3-D PIM: Neurocube, Tetris, iPIM

- 근거 위치: Section III-D, PDF p.6, Fig. 8
- 논문 내 역할: HMC vault와 logic die/memory die를 결합한 3-D PIM의 구조 변형을 보여 준다.
- Main Structure (Components): HMC의 16 vault; Neurocube의 vault별 PNG/PE와 2-D mesh; Tetris의 vault별 PE array/global buffer; iPIM의 logic-die control core와 memory-die process group.
- Operation Overview: vault-local compute와 inter-vault communication으로 DNN을 실행하며 Tetris는 data reuse를 높이고 iPIM은 control과 execution을 서로 다른 die에 분리해 bank-level bandwidth를 활용한다.
- Data / Signal Flow: stacked-memory vault data → vault-local PE/PG → local/global buffer 또는 mesh/TSV communication → result.
- Benefits: logic-memory die 사이의 high-bandwidth, energy-efficient communication과 vault/bank parallel execution을 제공한다.
- Challenges / Trade-offs: 3-D stacked die의 엄격한 physical/timing constraint 때문에 구현이 어렵고 조사된 Neurocube/Tetris/iPIM은 모두 simulation으로 평가됐다.
- 논문이 제공하지 않은 세부사항: 이 overview에 silicon measurement는 제시되지 않는다.

### ReRAM PIM

#### Fig. 9 — Current-Mode and Voltage-Mode ReRAM MAC

- 근거 위치: Section IV-B, PDF p.7, Fig. 9
- 논문 내 역할: ReRAM conductance를 weight로 사용하는 column dot-product의 두 sensing mode를 설명한다.
- Main Structure (Components): ReRAM crossbar, WL input, SL driver/ground, clamped or precharged BL, current ADC 또는 voltage ADC.
- Operation Overview: binary input을 WL에 적용하고 conductance weight와의 multiplication을 cell current로 표현해 column에서 합산한다. Current mode는 BL clamp/current readout을, voltage mode는 floating BL capacitance discharge를 사용한다.
- Data / Signal Flow: WL input + ReRAM conductance → cell current → column current sum 또는 BL discharge voltage → ADC → digital dot-product.
- Benefits: current mode는 큰 sensing margin과 빠른 sensing을, voltage mode는 static current 없이 dynamic power operation을 제공한다.
- Challenges / Trade-offs: current mode는 sensing 동안 static current가 필요해 energy efficiency가 낮고 voltage mode는 sensing margin이 작다. Device non-ideality 때문에 accuracy 관점에서는 sensing margin이 중요하다.
- 논문이 제공하지 않은 세부사항: 모든 cited prototype에 공통인 array bias와 timing은 제공되지 않는다.

#### Fig. 10 and Table III — Multi-Bit Digital ReRAM MAC

- 근거 위치: Section IV-C, PDF pp.7-8, Fig. 10, Table III
- 논문 내 역할: binary-state ReRAM으로 multi-bit input/weight와 signed ternary multiplication을 구성하는 방법을 보여 준다.
- Main Structure (Components): PIPW의 multiple macros와 weighted ReRAM devices; SIPW의 single macro와 multi-cycle input, binary-weighted capacitors; positive/negative ternary arrays.
- Operation Overview: PIPW는 input bit를 parallel macro에 분배해 weighted BL current를 합치고 SIPW는 input bit를 cycle별로 적용해 이전 current를 capacitor에 저장·병합한다. Ternary weight는 positive/negative arrays의 current 차로 얻는다.
- Data / Signal Flow: multi-bit input/weight mapping → macro/column별 BL current → spatial 또는 temporal current merge → multiplication result.
- Benefits: binary-state ReRAM을 유지하면서 multi-bit input/weight와 signed ternary operation을 지원한다.
- Challenges / Trade-offs: PIPW는 multiple macros/columns, SIPW는 multiple cycles/capacitors가 필요하며 둘 다 large BL-current distribution과 device variation 때문에 accuracy 개선용 merge circuit이 요구된다.
- 논문이 제공하지 않은 세부사항: PIPW와 SIPW의 동일 조건 정량 비교는 제공되지 않는다.

#### Figs. 11-12 — ReRAM Coprocessor and Versatile 2T2R Macro

- 근거 위치: Sections IV-F.1 and IV-F.3, PDF pp.8-9, Figs. 11-12
- 논문 내 역할: ReRAM PIM을 full computing system에 통합하고 MAC 외 search/Boolean operation까지 확장하는 연구 방향을 보여 준다.
- Main Structure (Components): RISC processor, SRAMs, controller, mixed-signal ReRAM macro and shared bus; 또는 2T2R array, decoders, drivers, reconfigurable SAs, PIM logic.
- Operation Overview: coprocessor는 pulse-modulated row input과 column current로 VMM을 수행하고 mixed-signal interface로 제어한다. 2T2R macro는 SA/CIM logic 재구성으로 search, Boolean logic, dot product를 수행한다.
- Data / Signal Flow: host/control → input buffer/DAC or row driver → ReRAM array/crossbar → ADC/SA and PIM logic → output buffer/shared bus.
- Benefits: 단일 macro를 넘어 programmable system integration 또는 versatile PIM functions를 지원한다.
- Challenges / Trade-offs: 2T2R PIM operation의 pseudo-write effect를 줄이기 위한 stress-voltage mitigation이 필요하다.
- 논문이 제공하지 않은 세부사항: 두 figure는 서로 다른 cited works이며 직접 비교 대상으로 제시되지 않는다.

### PIM Software Stack

#### Fig. 13 — Framework, Library, Runtime, Device Driver

- 근거 위치: Section V-A, PDF p.9, Fig. 13
- 논문 내 역할: passive memory와 달리 operation을 수행하는 PIM을 application에서 사용할 수 있도록 software stack 수정 지점을 제시한다.
- Main Structure (Components): PIM framework custom operations, PIM-optimized BLAS/library, runtime, device driver.
- Operation Overview: framework operation을 low-level library routine으로 내리고 runtime이 offload와 instruction/memory/kernel configuration을 관리하며 driver가 PIM memory space를 할당한다.
- Data / Signal Flow: application/framework operation → PIM library → runtime-generated instruction and mapping → device driver → PIM hardware.
- Benefits: PIM hardware를 application에서 사용하고 workload와 hardware에 맞게 최적화할 수 있다.
- Challenges / Trade-offs: offloading selection, data mapping, execution scheduling과 host-PIM cache coherence를 함께 해결해야 한다.
- 논문이 제공하지 않은 세부사항: 여러 PIM hardware를 포괄하는 하나의 표준 API specification은 제시되지 않는다.

## 6. Method

### SRAM PIM

#### Fig. 2(a)-(d) — Analog SRAM PIM Cell Variants

- Architecture reference: `## 5. Architecture`의 동일 항목
- Method purpose: SRAM cell에서 binary multiplication을 수행하면서 standard 6T의 read disturbance와 analog non-ideality를 완화한다.
- Input / Initial state: SRAM internal node에 binary weight가 저장되고 WL/RWL에 binary input level 또는 pulse가 적용된다.
- Core operation: storage state와 read path가 BL/RBL의 discharge 또는 voltage response를 결정한다.
- Operation mechanism: foundry 8T는 independent RBL discharge path를 추가하고 custom/differential cells는 지원 weight/input encoding 또는 voltage range를 확장하며 MOMCAP는 passive capacitor contribution으로 non-ideality를 줄인다.
- Output / State change: cell multiplication result가 bitline response로 나타나 column accumulation에 기여한다.
- Required conditions or assumptions: architecture별 input/weight encoding과 read path가 필요하다.
- Benefits: read disturbance 완화, operation diversity 또는 dynamic-range/variation 개선.
- Limitations / Trade-offs: single-ended read, larger cell, residual non-ideality 또는 transistor/capacitor area overhead.
- 근거 위치: Section II-B, PDF pp.2-3, Fig. 2

#### Fig. 3(a)-(d) — Analog SRAM Accumulation Modes

- Architecture reference: `## 5. Architecture`의 동일 항목
- Method purpose: 여러 cell의 multiplication result를 column-level analog MAC으로 누적한다.
- Input / Initial state: 동일 column의 cell별 binary multiplication result와 preconditioned shared BL/capacitor network.
- Core operation: current summation, pull-up/pull-down voltage drive, charge sharing 또는 capacitive coupling.
- Operation mechanism: current mode는 discharge contribution을 합치고 voltage mode는 parallel path로 shared RBL을 rail 방향으로 구동하며 charge-domain 방식은 capacitor network에서 charge를 결합한다.
- Output / State change: accumulated bitline current/voltage 또는 capacitor voltage.
- Required conditions or assumptions: current mode는 linear accumulation을 위한 limited dynamic range가 필요하다.
- Benefits: voltage-mode dynamic range 개선; charge-domain non-linearity/variation 완화와 높은 efficiency/throughput.
- Limitations / Trade-offs: residual non-linearity, extra switch/cycle, capacitor area 및 charge injection.
- 근거 위치: Section II-B, PDF p.3, Fig. 3

#### Fig. 4 — Digital SRAM PIM Macro

- Architecture reference: `## 5. Architecture`의 동일 항목
- Method purpose: analog conversion과 physical-variation-induced computation error 없이 reconfigurable multi-bit MAC을 수행한다.
- Input / Initial state: SRAM에 저장된 weight와 digital input/output precision 설정.
- Core operation: XNOR/NOR 기반 binary multiplication과 full-adder 또는 adder-tree accumulation.
- Operation mechanism: PIM cells를 precision에 따라 unit column 또는 multiple macro로 조합한다.
- Output / State change: 1-16-bit 또는 cited design의 12-bit MAC output.
- Required conditions or assumptions: precision 확장 시 multiple cells/macros가 필요하다.
- Benefits: digital robustness와 reconfigurability, ADC/DAC 제거.
- Limitations / Trade-offs: hardware redundancy, large unit cell, lower memory density, precision 확장 area.
- 근거 위치: Section II-C, PDF pp.3-4, Fig. 4

### DRAM PIM

#### Fig. 6 — Cell-Level AMBIT and DRISA

- Architecture reference: `## 5. Architecture`의 동일 항목
- Method purpose: DRAM row와 sense-amplifier path를 이용해 bulk Boolean operation과 data movement를 수행한다.
- Input / Initial state: AMBIT의 A/B rows와 preset C row, 또는 DRISA의 operand rows와 modified cell/SA logic.
- Core operation: triple-row charge-sharing majority, inverted SA writeback, NOR/mix/adder operation.
- Operation mechanism: AMBIT TRA는 세 cell의 majority를 SA로 판정하고 C=1/0으로 OR/AND를 선택한다. DCC는 inverted SA value를 cell로 이동한다. DRISA는 3T1C transistor path 또는 SA 아래 latch/logic을 사용한다.
- Output / State change: Boolean result row 또는 SA/latch/adjacent-BL result.
- Required conditions or assumptions: modified row control, multi-row activation, preset/control rows; DCC/DRISA variant에는 추가 cell 또는 peripheral structure.
- Benefits: whole-row parallelism과 internal bandwidth 활용.
- Limitations / Trade-offs: cell pitch 안의 extra transistor/wordline/logic integration feasibility.
- 근거 위치: Section III-B, PDF p.5, Fig. 6

#### Fig. 7 — Bank-Level Newton and HBM-PIM

- Architecture reference: `## 5. Architecture`의 동일 항목
- Method purpose: bank-side logic area와 bank parallelism으로 MVM 또는 programmable FP16 computation을 수행한다.
- Input / Initial state: memory-bank operands, Newton global-buffer input vector 또는 HBM-PIM CRF instruction과 selected row activation.
- Core operation: bank별 multiplier/reduction/accumulation 또는 PCU SIMD multiply/add.
- Operation mechanism: Newton의 GWRITE-G_ACT-COMP-READRES command sequence; HBM-PIM의 PIM-mode detection과 CRF program-counter progression.
- Output / State change: bank accumulator/result 또는 PCU register result.
- Required conditions or assumptions: customized PIM commands/controller와 bank-side compute logic.
- Benefits: cell-pitch 제약을 피하면서 bank parallelism과 programmable/fixed compute를 제공한다.
- Limitations / Trade-offs: whole-row internal bandwidth를 사용하지 못하고 architecture별 specialization 범위가 다르다.
- 근거 위치: Section III-C, PDF pp.5-6, Fig. 7

#### Fig. 8 — 3-D PIM: Neurocube, Tetris, iPIM

- Architecture reference: `## 5. Architecture`의 동일 항목
- Method purpose: stacked-memory vault 근처에서 DNN computation과 data reuse/communication을 수행한다.
- Input / Initial state: HMC vault에 배치된 data와 logic-die 또는 memory-die compute/control.
- Core operation: vault-local PE execution, mesh/TSV communication, buffer reuse 또는 bank-near process-group execution.
- Operation mechanism: Neurocube는 vault별 PNG/PE를, Tetris는 PE array/global buffer를, iPIM은 separated control core/PG와 SIMB ISA를 사용한다.
- Output / State change: vault-local 또는 inter-vault DNN computation result.
- Required conditions or assumptions: 3-D stacked memory, TSV, vault partition 및 architecture별 mapping/control.
- Benefits: high-bandwidth, energy-efficient die communication과 parallel execution/data reuse.
- Limitations / Trade-offs: physical/timing integration challenge; paper가 조사한 세 구조는 simulation-only evaluation.
- 근거 위치: Section III-D, PDF p.6, Fig. 8

### ReRAM PIM

#### Fig. 9 — Current-Mode and Voltage-Mode ReRAM MAC

- Architecture reference: `## 5. Architecture`의 동일 항목
- Method purpose: ReRAM conductance에 저장한 weight로 vector-matrix dot product를 수행한다.
- Input / Initial state: conductance Gij, binary WL input, current mode의 Vread/Vref 또는 voltage mode의 precharged floating BL.
- Core operation: cell current multiplication과 column accumulation.
- Operation mechanism: current mode는 SL을 Vread로 drive하고 BL을 Vref로 clamp한다. Voltage mode는 SL을 ground하고 BL capacitance discharge rate에 dot product를 반영한다.
- Output / State change: current ADC 또는 voltage ADC가 digitize한 column dot-product.
- Required conditions or assumptions: sensing mode별 bias와 ADC가 필요하다.
- Benefits: current mode의 large margin/fast sensing 또는 voltage mode의 dynamic-only power.
- Limitations / Trade-offs: current-mode static current energy 또는 voltage-mode smaller sensing margin.
- 근거 위치: Section IV-B, PDF p.7, Fig. 9

#### Fig. 10 and Table III — Multi-Bit Digital ReRAM MAC

- Architecture reference: `## 5. Architecture`의 동일 항목
- Method purpose: binary HRS/LRS devices로 multi-bit input/weight와 signed ternary multiplication을 구성한다.
- Input / Initial state: bit-sliced input, weighted ReRAM devices 또는 positive/negative weight arrays.
- Core operation: PIPW spatial merge, SIPW temporal merge 또는 differential positive/negative current merge.
- Operation mechanism: input MSB/LSB를 macro 또는 cycle에 배치하고 2x weighted current와 binary-weighted capacitor를 이용해 partial result를 합친다.
- Output / State change: multi-bit 또는 ternary multiplication current/result.
- Required conditions or assumptions: multiple macro/column/cycle 및 merge circuit; signed ternary에는 two arrays.
- Benefits: binary-device robustness를 유지하며 multi-bit/signed operation을 지원한다.
- Limitations / Trade-offs: resource/cycle overhead, broad BL-current distribution과 variation-sensitive accuracy.
- 근거 위치: Section IV-C, PDF pp.7-8, Fig. 10, Table III

#### Figs. 11-12 — ReRAM Coprocessor and Versatile 2T2R Macro

- Architecture reference: `## 5. Architecture`의 동일 항목
- Method purpose: ReRAM VMM을 programmable system에 통합하거나 한 array에서 search/Boolean/dot-product를 선택한다.
- Input / Initial state: coprocessor instruction/data와 pulse-modulated row input, 또는 2T2R macro의 opcode/address/data.
- Core operation: crossbar analog VMM 및 mixed-signal conversion, 또는 reconfigurable SA/CIM logic operation.
- Operation mechanism: RISC가 shared bus로 macro를 제어하고 2T2R peripheral이 requested PIM function에 맞게 sensing/logic path를 구성한다.
- Output / State change: digitized VMM output 또는 search/Boolean/dot-product result.
- Required conditions or assumptions: mixed-signal interface 또는 reconfigurable SA/CIM logic.
- Benefits: full-system programmability 또는 versatile PIM functions.
- Limitations / Trade-offs: PIM operation 중 ReRAM pseudo-write stress를 줄이는 기법이 필요하다.
- 근거 위치: Sections IV-F.1 and IV-F.3, PDF pp.8-9, Figs. 11-12

### PIM Software Stack

#### Fig. 13 — Framework, Library, Runtime, Device Driver

- Architecture reference: `## 5. Architecture`의 동일 항목
- Method purpose: application operation을 PIM hardware에 offload하고 memory/instruction/kernel을 관리한다.
- Input / Initial state: application/framework operation과 target PIM hardware.
- Core operation: PIM-friendly operation identification, low-level routine mapping, instruction generation, memory allocation과 kernel configuration.
- Operation mechanism: framework custom op가 PIM BLAS/library를 호출하고 runtime이 offload와 resource를 결정한 뒤 driver가 addressable PIM memory space를 제공한다.
- Output / State change: PIM hardware에서 실행 가능한 instruction/kernel과 memory placement.
- Required conditions or assumptions: hardware capability에 맞는 operations, runtime/compiler support와 host integration.
- Benefits: end-user application에서 PIM을 활용하고 hardware execution units를 최적화한다.
- Limitations / Trade-offs: specialized logic는 suitable operation 식별이 쉽지만 범위가 좁고 general-purpose PIM은 operation selection이 어렵다. Mapping, dynamic scheduling, coherence overhead도 남는다.
- 근거 위치: Sections V-A-V-E, PDF pp.9-11, Fig. 13

## 7. Experiments

- Baseline: 이 논문 자체의 통합 experimental baseline은 없다. Table I, II, IV, V, VI가 서로 다른 cited SRAM/DRAM/ReRAM PIM 연구와 converter/accuracy 결과를 요약한다.
- Workloads / Models: cited work별 CNN, FCN, RNN, RBM, SNN, DLRM, BERT 등으로 다르며 software-stack 예시는 Chrome, TensorFlow Mobile, video playback/capture를 포함한다.
- Dataset: cited accuracy comparison은 MNIST, CIFAR-10, CIFAR-100, ImageNet 등을 포함한다.
- Hardware configuration: cited SRAM/DRAM/ReRAM macro와 cell-, bank-, 3-D-level architecture로 서로 다르다. 논문 자체가 제작한 공통 hardware configuration은 없다.
- Metrics: TOPS/W, capacity, precision, test/software accuracy, accuracy difference, converter power/area share, data movement와 throughput/latency 관련 결과.
- Simulation / Measurement methodology: overview가 cited works의 reported silicon 또는 simulation 결과를 종합한다. Neurocube, Tetris, iPIM은 본문에서 simulation-only라고 명시한다. 논문 자체의 신규 measurement는 없다.

## 8. Results

- Performance: Table IV는 recent ReRAM PIM에서 더 복잡한 ML algorithm/dataset을 위한 MAC precision 증가 추세를 정리한다. Data-mapping 사례 [52]에서는 분석한 offloaded code block의 85%가 access address 사이 fixed offset을 보여 consecutive-address mapping으로 internal movement를 줄일 수 있었다. 이 값들은 cited works의 결과다.
- Energy / Efficiency: cited ReRAM macro [34]의 1152x128 array, 2-bit DAC, 8-bit ADC breakdown에서 DAC와 ADC는 각각 total power의 24%와 61%를 소비한다. 논문은 converter overhead가 array 자체보다 지배적일 수 있음을 보여 준다.
- Area / Cost: 같은 cited breakdown에서 8-bit output precision의 ADC가 total area의 91%를 차지한다. ADC 수를 줄이면 area/energy는 감소하지만 동일 MAC result 처리 cycle이 늘어난다.
- Accuracy: Table VI에서 MNIST test accuracy는 design/algorithm에 따라 97%-99.63%, CIFAR-10은 약 80.1%-92.52%, reported software-accuracy 대비 drop은 0.55%-1.39%다. 별도 cited retraining 사례 [65]는 CIFAR-10에서 calibrated multiplicative DAC의 90.3%를 3 epochs 후 91.6%로 회복하며 91.9% software accuracy보다 0.3% 낮다고 보고한다.
- Other: survey synthesis는 SRAM/DRAM/ReRAM 각각의 circuit-to-system design space와 PIM adoption을 위한 software-stack 문제를 함께 제시하고 data converter overhead, ML test accuracy, intra-memory data movement를 future research priorities로 정리한다.

## 9. Trade-offs

| Structure / Approach | Benefit (Gain) | Trade-off / Cost | Evidence |
| --- | --- | --- | --- |
| Analog vs. digital SRAM PIM | Analog macro는 높은 energy/area efficiency를 제공한다. | Flexibility와 classification accuracy가 제한된다. Digital macro는 physical variation을 피하지만 efficiency와 throughput이 낮다. | Section II, PDF p.2 |
| Foundry 8T SRAM cell, Fig. 2(b) | Independent RBL path로 standard 6T의 read disturbance를 해결한다. | Single-ended read만 지원하며 bitcell area가 커진다. | Section II-B, PDF p.3, Fig. 2(b) |
| Charge-sharing vs. capacitive-coupling SRAM accumulation, Fig. 3(c)-(d) | Charge-domain approach는 analog non-linearity와 variation을 줄인다. | Charge-sharing은 coupling보다 cell당 switch 하나와 accumulation cycle 하나가 더 필요하고 capacitor area와 charge injection 부담이 있다. | Section II-B, PDF p.3, Fig. 3(c)-(d) |
| Digital SRAM PIM, Fig. 4 | Physical variation과 ADC/DAC conversion을 피하고 precision을 재구성한다. | Memory/compute redundancy로 cell이 커지고 density가 낮으며 precision 확장에 multiple macro area가 든다. | Section II-C, PDF pp.3-4, Fig. 4 |
| DRAM cell-level vs. bank-level PIM, Fig. 5 | Cell level은 whole-row internal bandwidth를 최대한 활용한다. Bank level은 column decoder 뒤 넓은 logic area를 사용해 구현 가능성을 높인다. | Cell level은 shrinking cell pitch의 severe area constraint를 받고 bank level은 cell level만큼 maximum internal bandwidth를 쓰지 못한다. | Section III introduction and III-C, PDF pp.4-5, Fig. 5 |
| 3-D PIM, Fig. 8 | TSV-connected logic/memory dies로 high-bandwidth, energy-efficient communication을 제공한다. | Stacked dies의 strict physical and timing constraints로 realization이 어렵다. | Section III-D, PDF p.6, Fig. 8 |
| Current-mode vs. voltage-mode ReRAM MAC, Fig. 9 | Current mode는 larger sensing margin과 faster sensing을 제공한다. Voltage mode는 dynamic power만 사용한다. | Current mode는 sensing 기간 static current 때문에 energy efficiency가 낮고 voltage mode는 sensing margin이 작다. | Section IV-B, PDF p.7, Fig. 9 |
| Analog multi-state vs. digital HRS/LRS ReRAM weight | Analog state는 cell당 multi-bit weight로 capacity를 높인다. | Device variation으로 MAC accuracy가 낮고 multi-state control에 complex write-verification overhead가 필요해 대부분의 surveyed work는 digital ReRAM을 선호한다. | Section IV-C and IV-E, PDF pp.7-8 |
| PIPW vs. SIPW multi-bit ReRAM, Fig. 10 | PIPW는 input bits를 parallel 처리하고 SIPW는 하나의 macro를 여러 cycle에 재사용한다. | PIPW는 multiple macros가, SIPW는 multiple cycles와 binary-weighted capacitors가 필요하며 둘 다 large BL-current distribution 문제를 갖는다. | Section IV-C, PDF p.7, Fig. 10 |
| ReRAM ADC count reduction | ADC 수를 줄이면 converter energy/area overhead를 낮출 수 있다. | 동시에 생성하는 MAC result 수가 줄어 동일 workload 처리 cycle이 늘고 performance가 저하된다. | Section IV-D.1, PDF p.8 |
| DAC/ADC precision reduction | Converter area와 power를 줄일 수 있다. | Lower precision은 ML accuracy loss를 유발할 수 있다. | Section VI-A-VI-B, PDF pp.11-12, Tables V-VI |
| Conventional CIM data placement | Off-chip data movement와 energy를 줄이고 높은 throughput을 얻는다. | im2col duplication과 extra intra-memory movement가 cache/memory bandwidth와 peripheral energy를 지배할 수 있다. | Section VI-C, PDF pp.12-13 |

## 10. Limitations

### Paper-Reported Limitations

#### Structure-specific Capability / Applicability Limits

##### 3-D DRAM PIM — Neurocube, Tetris, iPIM

- Related Architecture / Method: Fig. 8의 HMC-based 3-D PIM
- Limitation: 논문이 조사한 세 architecture는 simulation으로만 평가됐다.
- Limited capability or applicability: fabricated 3-D PIM silicon evidence를 이 overview의 해당 사례에서 확인할 수 없다.
- Applicable condition: Neurocube, Tetris, iPIM의 reported evaluation.
- Consequence: 실제 stacked-die physical/timing constraint 아래 실현 가능성과 measured behavior는 이 사례들로 입증되지 않는다.
- 근거 위치: Section III-D, PDF p.6, Fig. 8

##### ReRAM Multi-Bit MAC — BL Sensing

- Related Architecture / Method: Fig. 10과 Table III의 multi-bit/ternary ReRAM MAC
- Limitation: device variation과 HRS offset current가 같은 MAC value에서도 넓고 겹치는 BL-current distribution을 만든다.
- Limited capability or applicability: distinguishable sensing margin과 MAC accuracy가 제한된다.
- Applicable condition: multiple WL/current contribution을 합치는 ReRAM PIM read path.
- Consequence: accuracy 개선을 위해 split-current merge와 sensing 회로가 추가로 필요하다.
- 근거 위치: Sections IV-C and IV-D.2, PDF pp.7-8, Table III

#### System- or Paper-level Capability / Applicability Limits

##### PIM-Friendly Operation Scope

- Affected scope: PIM offloading과 host-PIM execution
- Limitation: 모든 operation이 PIM의 이점을 얻는 것은 아니며 PIM-friendly operation을 다른 operation과 구분해야 한다.
- Limited capability or applicability: specialized PIM은 특정 operation만 실행하고 general-purpose PIM은 suitable memory-intensive operation 식별이 더 어렵다.
- Applicable condition: application kernel을 PIM hardware로 offload할 때.
- Consequence: analytical/runtime criteria와 workload-aware selection이 없으면 PIM 자원을 효과적으로 사용할 수 없다.
- 근거 위치: Section V-B, PDF pp.9-10

##### Conventional Host-PIM Cache Coherence

- Affected scope: host processor와 PIM이 shared data를 사용하는 system
- Limitation: conventional bypass/write-through/message-passing/write-back 방식은 shared data가 증가할 때 narrow off-chip bandwidth를 통과해야 하므로 scale하지 않는다.
- Limited capability or applicability: 많은 shared data가 있는 host-PIM coherence.
- Applicable condition: PIM과 host 사이의 coherence traffic이 증가하는 경우.
- Consequence: PIM의 benefit이 저하된다.
- 근거 위치: Section V-E, PDF p.11

### User-Identified Limitations

사용자가 지적한 limitation 없음

## 11. Questions

### 이해를 위한 질문

선정된 질문 없음

### 비판적 질문

선정된 질문 없음

### 후속 연구 질문

선정된 질문 없음

## 12. Connection to My Research Direction

확인된 연구 연결 없음

## 13. Final Summary

아직 분석하지 않음

## 14. Reading Session History

아직 기록되지 않음

## 사용자 분석 근거

아직 기록되지 않음
