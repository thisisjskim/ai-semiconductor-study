# 학습 기록: 메모리 계층 구조와 데이터 재사용 (Memory Hierarchy and Data Reuse)

## Metadata
- Date: 2026-08-09
- Topic: Memory Hierarchy and Data Reuse
- Status: working
- Source: conversation
- Last updated: 2026-08-09

## 1. 오늘 공부한 목적
AI 연산이 hardware에서 어떻게 수행되는지 현재 이해 수준을 진단하고, NPU architecture를 이해하기 위한 기초인 MAC, memory bandwidth bottleneck, Memory Hierarchy, Data Movement, Data Reuse를 학습한다.

## 2. 오늘 이해한 내용
딥러닝에서는 많은 matrix/vector operation이 발생하며 weight와 activation은 memory에 저장된다. Compute unit은 필요한 데이터를 가져와 연산한다.

MAC(Multiply-Accumulate)을 많이 배치하면 병렬 연산 능력은 증가하지만 memory가 충분한 속도로 데이터를 공급하지 못하면 MAC이 데이터를 기다린다. 따라서 MAC 수만 늘린다고 성능이 같은 비율로 증가하지 않으며 Memory Bandwidth Bottleneck이 생길 수 있다.

동일한 데이터를 여러 연산에서 사용한다면 DRAM에서 매번 읽는 대신 한 번 가져온 데이터를 compute 가까이에 저장해 여러 번 사용하는 Data Reuse가 효율적이다.

현재는 Memory Hierarchy를 다음과 같이 단순화해 이해했다.

`Off-chip DRAM/HBM → On-chip SRAM → Register → MAC`

큰 데이터를 DRAM/HBM에 저장하고 현재 연산에 필요한 데이터를 SRAM과 Register처럼 compute에 가까운 저장 공간으로 가져와 재사용하면 반복적인 off-chip Data Movement를 줄일 수 있다.

## 3. 핵심 개념
- **MAC (Multiply-Accumulate)**: 곱셈 결과를 기존 값에 누적하는 연산.
- **PE (Processing Element)**: MAC 등의 연산을 수행하는 작은 processing unit.
- **Latency (지연시간)**: 데이터를 요청한 시점부터 사용할 수 있을 때까지 걸리는 시간.
- **Bandwidth (대역폭)**: 단위 시간 동안 전송할 수 있는 데이터의 양.
- **Memory Bandwidth Bottleneck**: compute가 요구하는 만큼 memory가 데이터를 공급하지 못해 연산기가 기다리는 상황.
- **Data Movement**: memory와 compute 또는 memory level 사이에서 데이터가 이동하는 것.
- **Data Reuse**: 한 번 가져온 데이터를 여러 연산에서 다시 사용하는 것.
- **Memory Hierarchy**: 서로 다른 속도, 용량, 면적 및 접근 비용을 가진 memory를 계층적으로 사용하는 구조.
- **On-chip / Off-chip**: 연산 chip 내부 / 외부.
- **Register**: compute가 당장 사용할 값이나 partial sum 등을 가까이 보관하는 작은 저장 공간.
- **On-chip SRAM**: compute 가까이에서 필요한 데이터를 보관하고 재사용하는 데 활용할 수 있는 memory.

## 4. 내가 처음 이해한 방식
처음에는 input `x`와 weight matrix `W`가 memory에 저장되어 있고 CPU/GPU가 memory 또는 HBM에서 필요한 값을 가져와 연산한 뒤 결과를 다시 memory에 저장하는 큰 흐름으로 이해했다.

MAC을 많이 배치해도 memory가 그만큼 데이터를 가져오지 못하면 연산 속도를 따라갈 수 없고 bandwidth bottleneck이 생길 것이라고 추론했다.

Memory Hierarchy를 배우기 전에도 Register/SRAM은 빠르지만 작고 area 부담이 크며 DRAM은 큰 용량을 제공한다는 직관은 있었지만, 여러 memory를 왜 계층적으로 사용하고 Data Reuse와 어떻게 연결되는지는 명확하지 않았다.

## 5. 오해 또는 불확실한 부분
- Bandwidth를 처음에는 “한 번 전송할 때 얼마나 많이 보내는가”로 이해했다. 핵심은 **단위 시간당 전송 가능한 데이터 양**이다.
- Latency를 “명령에 반응하는 속도”로 표현했지만, 더 정확히는 **memory access request 이후 데이터를 사용할 수 있을 때까지의 시간**이다.
- DRAM은 SRAM/Register보다 항상 bandwidth가 낮다고 일반화했다. Bandwidth는 memory 종류만으로 고정되지 않으며 구조와 interface에 따라 달라진다. HBM처럼 높은 bandwidth를 목표로 한 DRAM 계열 memory도 있다.
- SRAM/Register와 MAC의 역할을 일부 혼동했다. Register와 SRAM은 저장 공간이고 MAC은 연산 회로이다.
- SRAM access를 “가격이 덜 든다”고 표현했지만 현재 중요한 것은 금전적 가격이 아니라 **data access/movement의 energy cost**이다.
- AI 연산을 “행렬곱으로 weight를 갱신한다”고 표현했는데 이는 training에 더 가깝다. Inference에서는 일반적으로 학습된 weight를 사용해 계산한다.

## 6. 수정된 이해
AI 연산에서는 많은 matrix/vector operation이 발생한다. 모든 데이터를 작은 빠른 memory에 저장할 수 없기 때문에 큰 데이터를 DRAM/HBM에 두고 필요한 데이터를 on-chip SRAM과 Register 등 compute 가까이로 가져와 사용한다.

Latency와 Bandwidth는 서로 다른 성능 지표이다. Latency는 개별 access에서 기다리는 시간이고 Bandwidth는 단위 시간당 전송 가능한 데이터 양이다.

동일한 데이터를 여러 번 사용한다면 DRAM에서 반복적으로 가져오기보다 on-chip memory로 한 번 가져와 재사용하여 off-chip Data Movement를 줄이는 것이 성능과 energy efficiency 측면에서 중요하다.

## 7. 질문

### 해결되지 않은 질문
- Register는 실제로 어떤 회로로 구성되고 SRAM과 무엇이 다른가?
- SRAM과 DRAM은 구조와 동작 방식에서 어떻게 다른가?
- NPU에서는 SRAM, Register, PE/MAC array를 실제로 어떻게 연결하는가?
- Weight, activation, partial sum의 배치에 따라 Dataflow가 어떻게 달라지는가?

### 해결된 질문
- **Access Latency란?** 데이터를 요청한 시점부터 사용할 수 있을 때까지 걸리는 시간.
- **Latency와 Bandwidth의 차이는?** Latency는 기다리는 시간, Bandwidth는 단위 시간당 전송량.
- **MAC을 많이 추가하면 무조건 같은 비율로 빨라지는가?** 아니다. Memory Bandwidth Bottleneck으로 MAC이 기다릴 수 있다.
- **왜 DRAM에서 같은 데이터를 계속 가져오지 않는가?** 반복적인 off-chip Data Movement를 줄이고 가까운 memory에서 재사용하는 것이 유리하기 때문이다.
- **Memory Hierarchy가 왜 필요한가?** 서로 다른 memory의 속도, 용량, area, 접근 비용 trade-off를 함께 활용하기 위해서다.

## 8. AI 반도체 및 SSL 목표와의 연결
이번 학습은 AI Computation에서 Computer Architecture와 Memory Architecture로 넘어가는 기초 단계이다.

NPU의 성능은 MAC 개수만으로 결정되지 않는다. PE/MAC array에 데이터를 어떻게 공급하고, partial sum을 어디에 유지하며, on-chip memory를 이용해 데이터를 얼마나 재사용하는지가 중요하다.

따라서 Memory Hierarchy와 Data Reuse는 이후 NPU Dataflow, SRAM/DRAM, tiling, PIM/CIM을 이해하는 기반이 된다.

## 9. 다음 행동
1. Register의 역할을 학습하고 SRAM과의 차이를 이해한다.
2. 이해 확인 후 SRAM의 기본 구조와 특성을 학습한다.
3. DRAM과 SRAM을 비교하며 Memory Hierarchy를 구체화한다.
4. PE/MAC array로 돌아와 weight, activation, partial sum의 이동과 Dataflow를 학습한다.
5. 새 개념마다 사용자가 자기 언어로 다시 설명하여 이해를 확인한다.

## 10. 자기 설명 점검
- [x] 용어의 정의를 설명할 수 있다.
- [x] 구조 또는 동작 과정을 설명할 수 있다.
- [ ] 관련 개념과 비교할 수 있다.
- [x] AI 반도체에서 왜 중요한지 설명할 수 있다.

## 사용자 원문

<details>
<summary>대화에서 제공한 원문 보기</summary>

> 일단 x는 input이고, W는 가중치 matrix잖아. 이 값들은 memory에 저장되어있고 연산이 필요할 때, GPU나 CPU에서 연결된 memory(or HBM)에서 필요한 값들을 불러와서 연산을 하고 그 연산을 한 값을 다시 메모리에 저장하는 방식으로 데이터가 흘러갈 것 같아.

> 메모리에서 그 만큼의 많은 양의 데이터를 가져올 수 없어. MAC이 많다고 해도, 그 많은 MAC에 메모리를 제공해줘야 하는데, MAC의 연산 속도에 걸맞는 메모리 이동 속도에서 한계를 맞이하게 될 것 같아. bandwidth bottleneck? 이 발생할 것 같다는 말이야.

> 먼저, Memory Hierarchy가 무엇인지 잘 몰라. 그 이후, 답변을 할게. 모든 weight와 activation을 MAC의 register에 저장할 수 없는 이유는, 메모리 용량이 너무 작아서 그런 것 같아. SRAM, Register은 빠르게 메모리를 교환할 수 있다는 장점이 있지만 비용(Cost)가 높고, 면적(Area)(Transistor)을 많이 차지해서 한계가 있으며, 많은 transistor를 사용하는 것 대비 Capacity가 낮기 때문이라고 생각해.

> latency가 낮다는 말은, CPU, GPU가 memory에 명령을 내렸을 때, 이 명령에 대한 응답을 빨리 한다는 말이야.

> latency는 명령에 반응하는 속도라면, bandwidth는 한 번 메모리 전송을 할 때 얼마나 많이 보낼 수 있는가를 말함

> 데이터를 요청했을 때 늦게 데이터를 보내지만, 단위 시간동안 보낼 수 있는 메모리 용량이 많다라는 의미야.

> A는 DRAM과 Chip사이 100번의 Data movement가 있다면 B는 DRAM과 SRAM 사이의 1번의 Data movement가 발생하고 SRAM에서 저장된 x1이라는 데이터를 MAC에 주는거야. SRAM에서 MAC에 주는게 DRAM에 비해 더 빠르고 가격도 덜 들기 때문에 성능이나 에너지 측면에서 더 이득이야

> AI 연산을 단순하게 말하면 수많은 행렬곱을 통해 가중치를 갱신하는거지. 그래서 우리는 이 수많은 행렬곱을 반도체가 어떻게 효율적으로 빠르게 시행하는지 관심이 있는거야. 여기서 메모리는 DRAM -> on chip SRAM -> Register 순으로 Memory hierarchy로 되어있고, 상위로 갈 수록 빠르게 data를 주고받을 수 있는 대신 용량이 작고  차지하는 면적이 넓어서 비효율적이야. 그래서 특정 하나의 memory만 사용할 수 없어. 알다싶이 AI 연산은 하나의 데이터를 여러번 사용하는 Data Reuse가 발생해. 그래서 우리는 DRAM에서 필요한 데이터를 계속 가져오는 것이 아닌, 한 번 가져와서 SRAM에 옮겨서 그 데이터를 SRAM에서 Regigster(MAC)에 여러번 전송해주는 것이 더 효율적이야. 왜냐하면 DRAM은 off chip memory이기 때문에 메모리를 이동할 때 필요한 에너지와 시간이 오래걸리기 때문이지.

</details>
