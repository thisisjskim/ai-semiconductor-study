# 학습 기록: Memory Wall과 Analog CIM 기초 (Memory Wall and Analog CIM Fundamentals)

## Metadata

- Date: 2026-08-23
- Recorded at: 2026-08-23T14:53:43Z
- Topic: Memory Wall과 Analog CIM 기초
- Document type: learning-log
- Domain: pim-cim
- Roadmap stage: PIM/CIM fundamentals
- Status: working
- Source: conversation
- Evidence: 사용자의 자기 설명, analog MAC 계산 문제, NPU-CIM 비교 검증, ADC/activation bandwidth/bitline scaling trade-off 검증
- Related notes: 없음
- Last updated: 2026-08-23

## 1. 오늘 공부한 목적

기존 NPU에서 data reuse와 tiling을 사용해도 남는 data movement 문제를 출발점으로, CIM이 compute 위치를 어떻게 바꾸는지 이해한다. 이어서 analog CIM에서 weight와 activation의 곱 및 accumulation이 memory array의 물리적 신호와 어떻게 대응되는지, 그리고 실제 accelerator에서 peripheral과 bandwidth가 어떤 새로운 병목을 만드는지 설명할 수 있는 수준까지 확인한다.

## 2. 오늘 이해한 내용

사용자는 먼저 NPU에서 SRAM buffer의 제한 때문에 큰 데이터가 tiling되어야 하고, 이에 따라 DRAM과의 data movement가 계속 발생할 수 있다는 점을 설명했다. 이후 CIM에서는 weight를 compute-capable memory에 비교적 고정하여 weight movement를 줄일 수 있다는 방향으로 이해를 확장했다.

Binary analog CIM 예제에서는 저장된 weight bit와 activation bit가 모두 1일 때만 current contribution이 발생하는 단순화된 모델을 사용했다. 사용자는 w=[1,1,0], x=[1,0,1]에서 각 곱이 [1,0,0]이고, 1×1당 5 µA라면 bitline 합이 5 µA임을 계산했다. 3×3 matrix-vector 예제에서도 output [1,1,2]와 대응하는 bitline current [5,5,10] µA를 정확히 계산했다.

Multi-bit 값에서는 각 bit가 서로 다른 2^n 자리값을 갖기 때문에 단순히 bit contribution을 같은 가중치로 더하면 안 된다는 점을 설명했다. 사용자는 bit별 결과를 분리한 뒤 digital domain에서 shift를 통해 자리값을 반영하는 방식을 제시했고, analog multi-level input보다 bit-serial input이 더 많은 cycle을 요구하지만 noise에 대한 구분 여유를 확보하기 쉽다는 trade-off를 설명했다.

Layer 간 dataflow에서는 이전 layer의 output이 다음 layer의 input activation이 되며, weight는 inference 동안 상대적으로 고정되지만 activation은 input에 따라 계속 바뀐다고 설명했다. 또한 activation buffer의 a1을 W2가 저장된 CIM array에 공급하여 a2를 만들고, 이를 다시 activation buffer에 저장한 뒤 다음 CIM array에 공급하는 흐름을 자기 언어로 설명했다.

System-level trade-off에서는 ADC 수를 줄여 공유하면 area와 ADC energy를 줄일 가능성이 있지만 conversion serialization으로 시간이 늘어날 수 있고, column별 ADC를 많이 배치하면 throughput은 높일 수 있지만 area와 energy overhead가 커진다고 설명했다. Activation buffer bandwidth가 부족하면 CIM array 일부가 놀게 되어 PE utilization 문제와 유사한 utilization bottleneck이 발생한다고 연결했다.

마지막으로 큰 CIM array에서는 긴 bitline과 더 많은 연결 소자 때문에 parasitic capacitance가 증가할 수 있고, sensing 속도와 signal margin이 불리해질 수 있다는 방향을 추론했다. 다만 capacitance 증가가 cell current 자체를 반드시 감소시키는 것은 아니며, I=C·dV/dt 관계에서 같은 current라면 voltage response가 느려지거나 같은 시간 동안의 voltage swing이 작아진다는 점으로 수정했다.

## 3. 핵심 개념

- Memory Wall: compute 성능만 높여도 memory hierarchy를 통한 data movement가 latency/energy 병목으로 남을 수 있다.
- Weight-stationary CIM: weight를 memory array에 두고 activation을 공급하여 weight movement를 줄이는 방향이다.
- Analog CIM MAC: cell의 w×x에 해당하는 physical contribution을 current/charge/voltage 등의 analog quantity로 표현하고 bitline에서 accumulation할 수 있다.
- Multi-bit handling: positional weight 때문에 bit slicing/bit-serial 및 digital shift-and-add 등의 재구성이 필요할 수 있다.
- Activation buffer: 특별한 memory technology의 이름이라기보다 activation을 임시 저장하는 역할이며, accelerator에서는 SRAM으로 구현될 수 있다.
- Peripheral bottleneck: ADC, input driver/DAC, activation SRAM, interconnect, digital accumulation 등이 array 밖의 area/energy/throughput을 제한할 수 있다.
- Array scaling: 큰 WL/BL은 parasitic resistance/capacitance와 sensing/precision 문제를 키울 수 있어 array size를 무조건 확대할 수 없다.

## 4. 내가 처음 이해한 방식

사용자는 처음에 NPU가 연산할 때마다 DRAM에서 MAC까지 데이터를 다시 가져오는 것으로 강하게 단순화했고, CIM에서는 DRAM 내부에서 어느 정도 계산된 결과를 MAC으로 한 번 보내는 구조처럼 이해했다.

Analog CIM에서는 multi-bit 값을 하나의 analog level로 정밀하게 표현하면 level 간격이 좁아져 noise와 offset에 취약해질 것이라고 추론했고, 이를 피하기 위해 bit별로 나누어 여러 cycle에 계산한 뒤 자리값을 반영하는 방식이 더 직관적이라고 생각했다.

또한 bitline capacitance가 커지면 CIM cell이 만들어내는 current 자체가 작아질 수 있다고 추론했다.

## 5. 오해 또는 불확실한 부분

- NPU가 매 MAC마다 DRAM에서 weight를 다시 가져오는 것은 아니다. SRAM, register, tiling, dataflow를 통해 한번 가져온 데이터를 적극적으로 reuse한다.
- CIM은 반드시 DRAM 기반이 아니며, SRAM-CIM 등 다양한 구현이 있다.
- CIM 결과를 반드시 기존 PE의 MAC으로 다시 보내 동일한 MAC을 수행하는 것이 핵심은 아니다. Array/bitline에서 이미 dot-product의 일부 또는 상당 부분을 계산할 수 있다.
- CIM이 weight movement를 줄인다고 해서 off-chip traffic 전체가 항상 비약적으로 줄어드는 것은 아니다. Activation/output movement와 capacity에 따른 weight loading/remapping이 남을 수 있다.
- Bitline capacitance 증가가 cell current 자체를 일반적으로 감소시킨다고 볼 수 없다. 같은 current에서는 voltage response의 속도와 swing 관점으로 해석해야 한다.

## 6. 수정된 이해

기존 NPU는 data reuse와 tiling을 통해 data movement를 최소화하지만 memory와 compute가 분리된 구조에서 weight와 activation을 compute 쪽으로 전달해야 한다. CIM은 weight가 저장된 memory array 내부 또는 가까운 위치에서 연산함으로써 특히 weight movement를 줄이는 방향이며, activation과 output movement는 여전히 남는다.

Analog CIM에서는 binary weight와 activation의 조합이 conduction/no-conduction 또는 이에 준하는 physical contribution으로 mapping될 수 있고, 여러 cell의 contribution을 bitline에서 합쳐 dot product를 형성할 수 있다. Multi-bit에서는 각 bit의 positional weight를 별도로 반영해야 하므로 bit-serial 계산과 digital shift-and-add 같은 방법이 자연스럽게 연결된다.

CIM accelerator 전체의 효율은 array MAC만으로 결정되지 않는다. ADC 수와 공유 방식, activation buffer bandwidth, interconnect, digital accumulation, WL/BL parasitic 등이 전체 throughput과 energy를 제한할 수 있다. 특히 큰 bitline capacitance에서는 동일한 current에 대해 dV/dt가 감소하고 일정 sensing 시간에서 voltage swing이 작아질 수 있어 latency와 sensing margin 문제가 커질 수 있다.

## 7. 질문

### 해결되지 않은 질문

- 큰 neural-network weight matrix를 제한된 크기의 여러 CIM array에 어떻게 tiling/mapping하고, 각 array에서 생성된 partial sum을 어떻게 결합하는가?
- PIM/CIM의 구현 범위와 analog/digital CIM의 세부 경계는 이후 architecture 학습에서 추가 정리할 수 있다.

### 해결된 질문

- Activation은 무엇인가? → 현재 layer의 weight와 곱해지는 input이며, 중간 layer에서는 주로 이전 layer의 output activation이다.
- Activation은 어디에 저장되는가? → architecture에 따라 on-chip SRAM activation buffer 또는 필요 시 DRAM/HBM 등에 저장될 수 있다.
- Activation buffer는 register보다 빠른 특수 memory인가? → 보통 특정 technology 이름이 아니라 역할이며 SRAM으로 구현되는 경우가 많다.
- 여러 binary cell의 결과가 어떻게 MAC과 대응되는가? → cell contribution이 bitline에서 합산되어 dot-product accumulation과 대응될 수 있다.
- ADC를 많이 붙이면 항상 좋은가? → throughput에는 유리할 수 있으나 area/energy overhead가 커지는 trade-off가 있다.

## 8. AI 반도체 및 SSL 목표와의 연결

이번 학습은 NPU의 dataflow와 memory hierarchy에서 출발해 PIM/CIM이 왜 연구되는지를 architecture와 circuit 관점으로 연결했다. 단순히 MAC throughput만 비교하지 않고 weight/activation movement, peripheral energy, array utilization, analog sensing constraint를 함께 보는 관점은 향후 CIM accelerator 및 관련 논문의 architecture claim을 비판적으로 읽는 기반이 된다.

## 9. 다음 행동

1. CIM tiling과 mapping을 학습한다.
2. 큰 matrix를 여러 CIM array로 분할했을 때 발생하는 partial sum과 inter-array accumulation을 직접 계산한다.
3. NPU tiling과 CIM tiling의 공통점과 차이를 capacity, data movement, circuit constraint 관점에서 비교한다.

## 10. 자기 설명 점검

- [x] 용어의 정의를 설명할 수 있다.
- [x] 구조 또는 동작 과정을 설명할 수 있다.
- [x] 관련 개념과 비교할 수 있다.
- [x] AI 반도체에서 왜 중요한지 설명할 수 있다.

## 사용자 원문

<details>
<summary>대화에서 제공한 원문 보기</summary>

> "CIM은 weight가 memory안에 들어가있다."

> "layer2에 들어갈 activation은 layer 1에서 계산이 끝난 각각의 값들이지. layer2에서 weight는 비교적 고정되어있지만 activation은 input에 따라 계속 변화함. 그래서 weight는 memory cell에 비교적 지정하여 저장할 수 있는 것이고, activation은 계속해서 array 형식으로 받아와야함."

> "a1을 만들었고 그 a1이 activation buffer에 존재한다면, layer2의 연산을 위해서 activation buffer에 저장된 a1을 W2가 저장되어 있는 CIM array로 접근시켜서 memory 내부에서 행렬연산을 시킨다. 그렇게 연산되어 a2가 만들어지면 그 a2도 activation buffer에 저장시키고, 그 다음 layer3의 weight가 저장되어 있는 CIM으로 접근시켜 a3를 연산시킨다."

> "B의 설계가 ADC를 적게 이용하기 때문에 ADC가 차지하는 면적도 줄어들고, ADC로 인해 발생하는 에너지의 양도 줄일 수 있을 것이다. 그러나 하나의 ADC가 여러개의 column의 analog값을 digital로 변경해주어야하기 때문에 시간이 더 소모될 수 있다."

> "activation buffer의 bandwidth가 작아서 activation을 한 번에 제공하지 못한다면, CIM에서 연산할 수 있는 memory 일부가 쉬게 되기 때문에 성능이 크게 향상되지 못한다. 마치 PE utilization 때와 유사하다."

> "기존 NPU에서는 weight와 activation을 최대한 PE 근처에 위치하게 하여 data reuse를 효율적으로 하여 DRAM과의 data movement를 최소화했다. ... 그러나 CIM에서도 activation의 data는 움직여야 하고, 이 data가 움직이면서 발생하는 bottleneck도 분명히 존재함."

</details>
