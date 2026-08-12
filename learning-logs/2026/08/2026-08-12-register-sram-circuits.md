# 학습 기록: Register와 SRAM 회로 기초 (Register and SRAM Circuit Foundations)

## Metadata

- Date: 2026-08-12
- Topic: Register와 SRAM 회로 기초
- Document type: learning-log
- Domain: sram
- Roadmap stage: Stage 3 — Memory
- Status: working
- Source: conversation
- Evidence: self-explanation, misconception-correction, comparison
- Related notes: learning-logs/2026/08/2026-08-09-memory-hierarchy-data-reuse.md
- Last updated: 2026-08-12

## 1. 오늘 공부한 목적

- Memory Hierarchy에서 Register가 SRAM보다 compute 가까이에 배치되는 이유를 circuit/architecture 관점에서 연결한다.
- Cross-coupled inverter, latch, D flip-flop, multi-bit register의 관계를 이해한다.
- Transistor와 inverter/logic gate/register의 추상화 계층을 구분한다.
- 6T SRAM의 기본 구성인 4T storage core와 2T access transistor의 역할을 이해한다.
- 6T SRAM 학습에 필요한 NMOS/PMOS와 Pull-up/Pull-down 개념을 복습한다.

## 2. 오늘 이해한 내용

### Register의 역할과 Memory Hierarchy

처음에는 Register가 SRAM보다 latency가 짧기 때문에 reuse되는 데이터를 Register에 저장해 MAC에 빠르게 제공한다고 설명했다. 이 방향은 맞았고, 이후 Register의 역할을 다음처럼 구체화했다.

- Register는 compute 가까이에 작은 working set을 유지한다.
- 자주 재사용되는 operand나 partial sum을 Register에 두면 반복적인 SRAM access와 data movement를 줄일 수 있다.
- Register를 무작정 크게 만들면 제한된 on-chip area에서 SRAM, PE/MAC array, interconnect 등 다른 hardware가 사용할 면적이 줄어든다.
- 따라서 Register는 빠른 접근과 높은 data reuse가 중요한 작은 데이터에 사용하고, 더 큰 on-chip storage는 SRAM이 담당하는 계층 구조가 합리적이다.

### Cross-coupled inverter와 state storage

두 inverter를 서로 feedback으로 연결하면 두 개의 stable state를 만들 수 있다는 점을 이해했다.

- Q=1, Q̅=0
- Q=0, Q̅=1

두 inverter의 feedback이 node voltage state를 유지하며 1 bit를 표현한다. 다만 전원이 제거되면 이 상태를 계속 유지할 수 없으므로 Register와 SRAM은 volatile memory이다.

### Latch와 Flip-Flop

단순한 feedback storage에는 새로운 값을 받아들이는 경로와 기존 값을 유지하는 경로를 제어하는 장치가 필요하다.

D-latch는 특정 clock level 동안 transparent할 수 있으므로 level-sensitive하다. 반면 edge-triggered flip-flop은 특정 clock edge에서 D를 capture하고 다음 유효 edge까지 Q를 유지한다.

대표적인 master-slave 구조에서는 서로 반대 clock phase에서 동작하는 두 latch를 직렬로 연결하여 전체 D→Q 경로가 동시에 transparent해지는 것을 막고 edge-triggered 동작을 구현할 수 있다.

### Multi-bit Register

사용자의 자기 설명:

> "32bit register는 1-bit D Flip-Flop이 32개 병렬연결되어 있는 구조라고 생각해. 그래서 총 32개의 bit를 저장할 수 있는 구조인거야."

32-bit Register는 개념적으로 1-bit D flip-flop 32개가 각 bit를 저장하고 common clock에 맞춰 동시에 capture하는 구조로 이해했다. Rising edge 순간의 D[31:0]을 capture하고, 이후 D가 변해도 다음 유효 edge까지 Q[31:0]을 유지한다.

### Transistor, Logic Gate, Flip-Flop, Register의 관계

Transistor 자체가 inverter나 AND 같은 logic operator와 같은 것은 아니다. CMOS digital circuit에서 MOSFET transistor는 가장 아래의 switching device이고, 여러 transistor를 조합하여 logic gate와 storage circuit을 구성한다.

- CMOS inverter: 대표적으로 1 PMOS + 1 NMOS = 2T
- Cross-coupled inverter 2개: 4T storage core
- 6T SRAM cell: 4T storage core + 2T access transistor
- Flip-flop 기반 Register bit: topology에 따라 transistor 수가 달라지며, 일반적으로 SRAM 6T cell보다 더 큰 circuit/area cost를 가질 수 있다.

따라서 "Register 1 bit = 정확히 N transistor"라는 고정된 숫자를 암기하기보다 구현 topology에 따라 달라진다는 점과, SRAM cell보다 storage density 측면에서 불리하다는 architecture-level 의미를 이해하는 것이 중요하다.

### 6T SRAM의 기본 구조

사용자의 자기 설명:

> "transistor 2개를 더 붙이는 이유는, cross-coupled inverter로는 0이나 1이라는 특정 state를 안정적으로 유지시켜주는 데에 있어서 좋지만, 새로운 값을 저장하거나 값을 읽고, 바꿀 수(read/write)없어. 따라서 read/write를 해주기 위해서, 두 개의 access transistor를 더 붙이는 것 같아"

이 설명을 바탕으로 6T SRAM을 다음처럼 정리했다.

- 4T: 두 개의 cross-coupled CMOS inverter가 1 bit의 state를 유지한다.
- 2T: access transistor가 storage node Q/Q̅와 BL/BL̅ 사이를 선택적으로 연결한다.
- WL(Word Line): access transistor의 ON/OFF를 제어하여 cell을 bit line에 연결하거나 격리한다.
- BL/BL̅(Bit Line): read/write 시 cell과 데이터를 주고받는 경로이다.

현재는 6T SRAM의 세부 Hold/Write/Read 동작으로 들어가기 전에 MOSFET과 CMOS inverter 기초를 다시 확인하는 단계이다.

### NMOS/PMOS와 Pull-up/Pull-down

CMOS inverter를 이해하기 위해 NMOS와 PMOS의 동작을 복습했다.

- NMOS는 VGS가 threshold 조건을 만족할 때 channel이 형성된다.
- NMOS는 output을 GND 쪽으로 pull-down하여 strong 0을 만드는 데 적합하다.
- PMOS는 output을 VDD 쪽으로 pull-up하여 strong 1을 만드는 데 적합하다.
- Pull-Up Network(PUN)는 output node를 VDD 방향으로 끌어올리는 network이다.
- Pull-Down Network(PDN)는 output node를 GND 방향으로 끌어내리는 network이다.

사용자는 NMOS로 HIGH를 전달할 때의 문제를 다음과 같이 자기 언어로 설명했다.

> "NMOS로 1을 전달하려고 하면 (pull-up), 처음에는 Vgs가 Vth보다 높은 상태라고 NMOS가 활성화된 상태로 유지하게 되어, NMOS 채널이 열려서 처음에는 잘 전달하게 됨. 그런데 이제 채널이 열리게 되면 V_DD가 전달되게 되며 source쪽의 전압이 상승하게 됨. 그로 인하여 Vgs의 크기가 점점 줄어들게 됨. 그러다가 Vgs의 크기가 Vth와 가까워지거나, 같아지거나, 그 아래가 되어버리면 NMOS의 채널이 형성되지 않게 되며 동작이 되지 않음. 따라서 NMOS로는 전압을 올리는 pull-up이 좋지 않음."

이를 통해 `Vout 상승 → source potential 상승 → VGS 감소 → VGS≈VTN에서 channel 약화`라는 인과관계를 확인했다.

### MOSFET을 switch와 amplifier로 보는 관점

MOSFET의 β를 BJT의 current gain β와 혼동하지 않도록 구분했다. MOSFET에서는 gate voltage가 channel conductivity와 drain current를 제어한다.

Digital circuit에서 MOSFET이 ON된다는 것은 Drain과 Source를 완벽한 이상적 wire로 합친다는 의미라기보다 conducting channel을 형성한다는 의미이다. Channel을 통해 흐르는 current가 circuit node의 capacitance를 charge/discharge하고, 그 결과 node voltage가 변한다.

따라서 CMOS/SRAM을 이해할 때는 다음 흐름이 중요하다.

Gate voltage → channel 형성/차단 → current flow → node capacitance charge/discharge → node voltage 변화

Analog circuit에서는 VGS 변화에 따른 ID 변화를 이용해 amplification을 구현할 수 있고, digital circuit에서는 같은 MOSFET을 주로 switch 관점에서 사용한다.

## 3. 핵심 개념

- Register는 작은 working set을 compute 가까이에 두어 latency와 data movement를 줄인다.
- Register의 높은 bit당 circuit/area cost 때문에 대용량 storage에는 SRAM이 더 적합하다.
- Cross-coupled inverter는 feedback을 통해 두 stable voltage states를 유지한다.
- Latch는 level-sensitive하고, edge-triggered flip-flop은 특정 clock edge의 input을 capture한다.
- Multi-bit Register는 여러 1-bit storage element가 common clock에 맞춰 병렬로 동작하는 구조로 볼 수 있다.
- Transistor는 logic gate 자체가 아니라 logic gate와 storage circuit을 구성하는 physical switching device이다.
- CMOS inverter 하나는 대표적으로 PMOS 1개와 NMOS 1개로 구성된다.
- 6T SRAM은 4T cross-coupled inverter storage core와 2T access transistor로 구성된다.
- NMOS는 strong 0/pull-down, PMOS는 strong 1/pull-up에 적합하다.
- MOSFET ON 시 형성된 channel을 통한 current가 node capacitance를 charge/discharge하면서 digital node voltage를 변화시킨다.

## 4. 내가 처음 이해한 방식

- Register가 SRAM보다 latency가 짧으므로 reuse되는 데이터를 Register에 저장해 MAC에 빠르게 제공한다고 이해했다.
- Register가 빠른 대신 "capacitance가 낮다"고 표현했다.
- 두 inverter의 feedback 사이에 0/1이 저장되고, 전원이 꺼져도 그 값이 유지된다고 생각했다.
- Flip-flop에 추가 transistor가 필요한 이유를 cross-coupled inverter 자체가 불안정하기 때문일 수 있다고 추측했다.
- MOSFET은 gate 전압으로 Source와 Drain을 연결하면서 BJT의 β와 유사하게 전류를 증폭하는 장치라고 일부 혼합하여 기억하고 있었다.
- MOSFET이 ON되면 Drain과 Source가 등전위가 되는 것인지, current 관점과 voltage 관점을 어떻게 함께 이해해야 하는지 불확실했다.

## 5. 오해 또는 불확실한 부분

- Register의 architecture-level 단점을 capacitance와 capacity 중 어떤 용어로 표현해야 하는가?
- Cross-coupled inverter는 전원이 꺼져도 state를 유지하는가?
- 실제 Register bit에서 cross-coupled inverter 외에 추가 circuitry가 필요한 근본 이유는 무엇인가?
- Register 1 bit의 transistor 수를 SRAM의 6T, DRAM의 1T1C처럼 하나의 고정 숫자로 볼 수 있는가?
- NMOS를 VDD 쪽, PMOS를 GND 쪽에 배치해도 같은 방식으로 동작할 수 있는가?
- MOSFET의 β와 BJT의 current gain β는 같은 의미인가?
- MOSFET ON을 "D-S가 등전위가 된다"고 이해해도 되는가?
- Pull-up/Pull-down을 transistor switching뿐 아니라 current와 charge 관점에서 어떻게 해석해야 하는가?

## 6. 수정된 이해

- Register의 중요한 trade-off는 낮은 capacitance가 아니라 작은 **capacity**, 높은 bit당 area/circuit cost이다.
- Register와 SRAM은 전원이 제거되면 state를 유지할 수 없는 volatile storage이다.
- Cross-coupled inverter 자체는 stable state를 만드는 핵심이다. 추가 circuitry는 불안정성을 보완하기 위한 것이 아니라 write/hold/clocked capture와 같은 제어 기능을 구현하기 위해 필요하다.
- Register bit의 transistor 수는 flip-flop topology와 reset/enable/scan 등의 기능에 따라 달라지므로 하나의 고정 숫자로 정의할 수 없다.
- NMOS는 VGS/VTN 관계 때문에 strong 0을 전달하고 pull-down하는 데 유리하며, PMOS는 strong 1을 전달하고 pull-up하는 데 유리하다.
- MOSFET 식에서 사용하는 β parameter는 BJT의 current gain β와 같은 개념이 아니다.
- MOSFET ON은 D-S를 이상적인 0 Ω wire로 만드는 것이 아니라 conducting channel을 형성한다. 이 channel을 통한 current가 node capacitance를 charge/discharge하여 node voltage를 변화시킨다.

## 7. 질문

### 해결되지 않은 질문

- CMOS inverter에서 input이 0→1 또는 1→0으로 변할 때 output node의 charge가 실제로 어떤 경로로 이동하며 charge/discharge되는가?
- Pull-up/Pull-down network를 current, charge, node capacitance 관점에서 어떻게 완전히 연결해 설명할 수 있는가?
- 6T SRAM에서 Hold, Write, Read가 WL, BL/BL̅, Q/Q̅와 각 transistor의 동작으로 구체적으로 어떻게 구현되는가?
- 6T SRAM Read 과정에서 cell stability와 read disturb는 왜 발생하는가?

### 해결된 질문

- Register를 왜 SRAM 대신 무한히 늘리지 않는가?
- 두 D-latch를 반대 clock phase로 연결하면 왜 edge-triggered flip-flop 동작을 만들 수 있는가?
- 32-bit Register와 1-bit D flip-flop의 관계는 무엇인가?
- Transistor와 inverter/logic gate는 같은 개념인가?
- 6T SRAM에서 추가 access transistor 2개가 왜 필요한가?
- NMOS가 pull-down, PMOS가 pull-up에 적합한 device-level 이유는 무엇인가?
- NMOS로 HIGH를 전달할 때 왜 VDD까지 강하게 전달하기 어려운가?

## 8. AI 반도체 및 SSL 목표와의 연결

현재 내용은 Roadmap Stage 3 — Memory의 Register와 SRAM 기초에 해당한다. NPU에서 Register와 SRAM은 모두 on-chip data movement와 data reuse를 결정하는 핵심 storage hierarchy이다.

Register의 높은 speed와 낮은 density, SRAM의 상대적으로 높은 density와 on-chip access 특성을 circuit 수준에서 이해하면 이후 NPU architecture에서 PE local register, register file, on-chip SRAM buffer의 역할과 dataflow trade-off를 더 구체적으로 분석할 수 있다.

또한 6T SRAM의 read/write 및 cell stability를 이해하는 것은 이후 SRAM-CIM을 학습할 때 기존 SRAM cell과 peripheral circuit을 어떻게 computation에 활용하거나 수정하는지 분석하기 위한 기초가 된다. 다만 현재 단계에서는 PIM/CIM으로 성급하게 확장하지 않고 6T SRAM의 기본 동작을 먼저 확실히 이해한다.

## 9. 다음 행동

현재 학습 중인 6T SRAM 블로그의 흐름을 주교재로 삼고, 다음 순서로 이어간다.

1. MOSFET switch 관점 복습을 마무리한다.
2. CMOS inverter에서 PMOS/NMOS에 의한 output node charge/discharge 과정을 current/charge 관점에서 설명한다.
3. Pull-Up Network와 Pull-Down Network를 CMOS inverter 회로에서 확실히 구분한다.
4. Cross-coupled inverter가 1 bit state를 유지하는 과정을 다시 연결한다.
5. 6T SRAM의 Hold → Write → Read 동작을 WL, BL/BL̅, Q/Q̅ 기준으로 분석한다.
6. 이후 필요하면 read disturb, cell stability 및 SRAM array/peripheral circuit으로 확장한다.

## 10. 자기 설명 점검

- [x] Register가 SRAM보다 작은 capacity를 가지면서도 MAC 가까이에 사용되는 이유를 설명할 수 있다.
- [x] Cross-coupled inverter가 두 stable state를 만드는 feedback 구조를 설명할 수 있다.
- [x] Latch와 edge-triggered flip-flop의 동작 차이를 설명할 수 있다.
- [x] Transistor와 inverter/logic gate/register의 추상화 계층을 구분할 수 있다.
- [x] 6T SRAM의 4T storage + 2T access 구성을 설명할 수 있다.
- [x] NMOS가 strong 0/pull-down에 적합한 이유를 VGS와 VTN을 이용해 설명할 수 있다.
- [ ] CMOS inverter의 switching을 current, charge, node capacitance 관점에서 완전히 설명할 수 있다.
- [ ] 6T SRAM의 Hold/Write/Read 동작을 transistor-level에서 설명할 수 있다.
- [ ] SRAM의 read disturb와 cell stability를 설명할 수 있다.

## 사용자 원문

<details>
<summary>대화에서 제공한 원문 보기</summary>

> "register가 SRAM보다 더 빠른 latency를 가졌기 때문에, reuse 되는 data를 register에 저장해서 MAC에 빠르게 제공하기 위해서 MAC 옆에 register를 두는거야. register가 이렇게 빠르긴 하지만, capacitance가 낮다는 단점이 존재해"

> "register 용량을 크게 만들고 싶어도, 용량의 한계가 있기 때문이지. ... 그래서 data reuse가 많이 되는 것들만 register에 저장해서 빠르게 MAC에 보내주는 것이 효율적이야."

> "32bit register는 1-bit D Flip-Flop이 32개 병렬연결되어 있는 구조라고 생각해. 그래서 총 32개의 bit를 저장할 수 있는 구조인거야."

> "transistor 2개를 더 붙이는 이유는, cross-coupled inverter로는 0이나 1이라는 특정 state를 안정적으로 유지시켜주는 데에 있어서 좋지만, 새로운 값을 저장하거나 값을 읽고, 바꿀 수(read/write)없어. 따라서 read/write를 해주기 위해서, 두 개의 access transistor를 더 붙이는 것 같아"

> "NMOS로 1을 전달하려고 하면 (pull-up), 처음에는 Vgs가 Vth보다 높은 상태라고 NMOS가 활성화된 상태로 유지하게 되어, NMOS 채널이 열려서 처음에는 잘 전달하게 됨. 그런데 이제 채널이 열리게 되면 V_DD가 전달되게 되며 source쪽의 전압이 상승하게 됨. 그로 인하여 Vgs의 크기가 점점 줄어들게 됨. 그러다가 Vgs의 크기가 Vth와 가까워지거나, 같아지거나, 그 아래가 되어버리면 NMOS의 채널이 형성되지 않게 되며 동작이 되지 않음. 따라서 NMOS로는 전압을 올리는 pull-up이 좋지 않음."

> "MOSFET은 gate 전압을 줌으로써(NMOS기준) source와 drain을 연결해줌과 동시에 전류를 증폭시켜주는(beta비율만큼) 역할을 한다고 알고 있는데, 전류의 관점에서 보지 않고 전압을 연결시켜주어 등전위로 만드는 데에도 쓰이는지 궁금해. mosfet이 활성화 되면 drain와 source사이의 전류가 흐름과 동시에 전압차도 줄어들고, 등전위가 되는걸까?"

</details>
