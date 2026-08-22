# 학습 기록: NPU SRAM Data Reuse와 Dataflow (NPU SRAM Data Reuse and Dataflow)

## Metadata

- Date: 2026-08-22
- Topic: NPU SRAM Data Reuse와 Dataflow
- Document type: learning-log
- Domain: memory-architecture
- Roadmap stage: Stage 3 — Memory
- Status: working
- Source: conversation
- Evidence: self-explanation, inference, comparison, misconception-correction
- Related notes: learning-logs/2026/08/2026-08-22-sram-dram-sense-amplifier.md
- Last updated: 2026-08-22

## 1. 오늘 공부한 목적

- SRAM/DRAM의 구조·역할 차이를 NPU on-chip buffer의 data reuse, bandwidth, energy와 연결한다.
- SRAM capacity 제한에서 tiling이 필요한 이유를 이해한다.
- weight, activation, partial sum의 reuse와 dataflow가 data movement를 줄이는 방식을 설명한다.
- memory bandwidth와 PE utilization, memory-bound 성능의 관계를 설명한다.

## 2. 오늘 이해한 내용

### SRAM buffer와 DRAM traffic

사용자는 하나의 weight가 100번 사용될 때 SRAM이 없다면 DRAM에서 같은 데이터를 반복해서 가져와야 하며, off-chip DRAM access로 시간과 전력 비용이 커진다고 설명했다. 반대로 reuse가 높은 데이터를 on-chip SRAM에 저장하면 반복적인 DRAM access가 감소하고, 정해진 DRAM bandwidth에서 다른 필요한 데이터를 전달할 여유가 생긴다고 설명했다.

### Tiling과 partial sum 유지

SRAM capacity가 전체 working set보다 작으면 SRAM 용량 이하의 tile로 연산을 나누어야 한다고 추론했다. 처음에는 각 tile의 계산 결과를 DRAM에 다시 저장하고 나중에 불러와 합치는 흐름을 생각했지만, 이후 partial sum을 매번 DRAM/SRAM으로 왕복시키는 것 자체가 추가 data movement를 만든다는 점을 확인했다. 가능한 경우 partial sum을 PE 내부 register나 가까운 on-chip storage에 유지하면서 누적하고 최종 결과를 완성한 뒤 상위 memory로 보내는 것이 효율적이다.

### Bandwidth와 PE utilization

사용자는 partial sum을 DRAM으로 반복적으로 주고받으면 energy가 증가하고 DRAM bandwidth를 차지하여 다른 데이터 이동을 방해할 수 있다고 설명했다. 또한 memory bandwidth 부족으로 PE가 쉬고 있는 memory-bound 상황에서는 PE 수를 늘려 peak compute를 높여도 더 많은 PE가 idle 상태가 되므로 실제 성능이 크게 증가하지 않는다고 설명했다.

### Weight, activation, partial sum reuse와 dataflow

사용자는 Weight Stationary에서 reuse가 높은 weight를 PE 근처에 오래 유지하면 반복적으로 weight를 불러오는 data movement를 줄일 수 있다고 설명했다. Output Stationary에서는 누적되는 partial sum을 PE 내부에 유지함으로써 매 MAC마다 SRAM에 쓰고 다시 읽는 시간과 energy를 줄일 수 있다고 설명했다. Activation reuse에서는 동일 activation을 반복적으로 SRAM에서 읽는 대신 PE array에서 재사용하면 SRAM traffic과 energy를 줄이고 제한된 bandwidth를 다른 데이터 전달에 사용할 수 있다고 설명했다.

### PE-to-PE communication과 locality

사용자는 하나의 activation을 여러 PE가 필요로 할 때 각 PE가 SRAM에서 독립적으로 읽는 대신 PE-to-PE communication을 통해 전달하면 SRAM에서 한 번만 읽어도 되어 data movement의 시간과 energy를 줄일 수 있다고 설명했다. 이를 통해 reuse가 높은 데이터는 DRAM에서 PE까지 가져온 뒤 PE 근처 register나 local storage에서 반복적으로 사용하는 것이 효율적이라고 연결했다.

### Memory hierarchy trade-off

사용자는 DRAM만 사용하면 데이터 공급 latency와 off-chip movement 때문에 연산 속도가 제한되고, 반대로 Register/SRAM만 사용하면 bit당 큰 area 때문에 충분한 memory capacity를 확보하기 어렵다고 설명했다. 따라서 많은 데이터는 off-chip DRAM, 자주 쓰이는 데이터는 SRAM, reuse가 높은 현재 작업 데이터는 PE 근처 register에 배치하는 hierarchy가 storage와 movement 비용을 균형 있게 만든다고 설명했다.

## 3. 핵심 개념

- NPU on-chip SRAM buffer와 data reuse
- DRAM traffic, bandwidth pressure, data movement energy
- SRAM capacity와 tiling
- Partial sum accumulation과 local storage
- Weight Stationary와 weight reuse
- Output Stationary와 partial-sum reuse
- Activation reuse와 PE-to-PE communication
- Memory-bound와 PE utilization
- Register → SRAM → DRAM memory hierarchy
- capacity, latency, area, energy trade-off
- data locality

## 4. 내가 처음 이해한 방식

- SRAM이 존재하면 reuse가 많은 데이터를 on-chip에 저장하여 DRAM에서 같은 값을 반복적으로 가져오지 않을 수 있고, 그만큼 DRAM bandwidth에 여유가 생긴다고 이해했다.
- SRAM capacity보다 전체 weight가 크면 작은 tile로 나누어 계산해야 한다고 추론했다.
- 처음에는 각 tile의 계산 결과를 DRAM으로 다시 전달하고 이후 다시 불러와 모든 tile의 연산값을 합치는 흐름을 생각했다.
- Weight Stationary는 자주 사용하는 weight를 PE 가까이에 유지하여 빠르고 적은 energy로 재사용하기 위한 것이라고 이해했다.
- Output Stationary는 계속 누적되는 P를 PE 안에 유지하여 SRAM 왕복을 줄이는 방식이라고 이해했다.

## 5. 오해 또는 불확실한 부분

- Tiling을 처음 설명할 때 각 tile의 중간 결과를 반드시 DRAM에 저장했다가 다시 읽어 합쳐야 하는 것으로 생각했다. 실제로는 dataflow와 storage capacity가 허용한다면 partial sum을 on-chip에 유지하여 중간 결과의 반복적인 off-chip/on-chip 이동을 피하는 것이 중요하다.
- SRAM을 사용하면 DRAM의 물리적 peak bandwidth 자체가 증가하는 것은 아니다. 동일 데이터의 반복 traffic을 줄여 필요한 DRAM bandwidth와 bandwidth pressure를 낮추는 것이다.
- SRAM/PE communication과 PE-to-PE communication도 비용이 없지는 않으며, 전체 dataflow는 각 데이터의 reuse, movement cost, storage capacity를 함께 고려해야 한다.

## 6. 수정된 이해

- Tiling은 단순히 데이터를 SRAM 크기에 맞게 자르는 것뿐 아니라, tile 안에서 weight, activation, partial sum을 최대한 reuse하여 상위 memory traffic을 줄이는 방향으로 구성해야 한다.
- Partial sum은 가능한 경우 PE register 또는 가까운 on-chip storage에 유지하고 연산이 끝날 때까지 누적함으로써 반복적인 SRAM/DRAM read-write를 줄인다.
- Reuse가 좋아지면 DRAM의 최대 bandwidth가 커지는 것이 아니라 같은 bandwidth에서 중복 traffic이 줄어 새로운 필요한 데이터를 더 원활하게 공급할 수 있다.
- Memory-bound 상황에서는 compute unit을 추가하는 것보다 data supply bottleneck을 완화해야 PE utilization과 실제 throughput이 개선된다.
- Dataflow는 weight, activation, partial sum 중 하나를 무조건 선택하는 문제가 아니라 reuse 정도, 이동 비용과 시간, 필요한 저장 용량을 함께 고려해 전체 data movement를 줄이는 문제이다.

## 7. 질문

### 해결되지 않은 질문

- Stage 4에서 실제 NPU PE array와 buffer hierarchy를 통해 Weight/Output/Activation reuse가 어떻게 mapping되는가?
- 대표 dataflow가 실제 tensor/matrix tile을 PE array에 어떻게 배치하는가?

### 해결된 질문

- SRAM buffer가 weight reuse를 통해 DRAM traffic과 bandwidth pressure를 어떻게 줄이는가?
- SRAM capacity가 제한될 때 왜 tiling이 필요한가?
- Partial sum을 on-chip에 유지하면 왜 data movement가 줄어드는가?
- Memory bandwidth가 부족하면 왜 PE를 추가해도 실제 성능이 크게 증가하지 않을 수 있는가?
- Weight Stationary와 Output Stationary는 각각 어떤 data movement를 줄이는가?
- Activation reuse와 PE-to-PE communication은 SRAM access를 어떻게 줄이는가?
- 왜 Register, SRAM, DRAM을 하나의 memory hierarchy로 사용하는가?

## 8. AI 반도체 및 SSL 목표와의 연결

이번 학습은 memory circuit에서 배운 SRAM/DRAM의 특성을 NPU architecture의 data movement 문제로 연결했다. SRAM의 낮은 density를 감수하고 on-chip buffer로 사용하는 이유를 data reuse, DRAM bandwidth, energy와 PE utilization 관점에서 설명할 수 있게 되었다. 또한 dataflow가 연산 순서만의 문제가 아니라 memory hierarchy에서 reuse를 어디에서 잡을지 결정하는 architecture 문제라는 기반을 형성했다.

## 9. 다음 행동

1. Stage 4 NPU Architecture에서 PE와 PE array의 기본 data path를 학습한다.
2. NPU buffer hierarchy와 PE local storage 사이의 데이터 이동을 구체적으로 추적한다.
3. 대표 dataflow를 하나 선택해 어떤 weight/activation/partial-sum movement를 줄이는지 분석한다.

## 10. 자기 설명 점검

- [x] 용어의 정의를 설명할 수 있다.
- [x] 구조 또는 동작 과정을 설명할 수 있다.
- [x] 관련 개념과 비교할 수 있다.
- [x] AI 반도체에서 왜 중요한지 설명할 수 있다.

## 사용자 원문

<details>
<summary>대화에서 제공한 원문 보기</summary>

> "SRAM이 존재하면 reuse를 많이 하는 data를 on-chip인 SRAM에 저장하여 빠르게 data를 사용할 수 있다. 그리고 이렇게 SRAM을 사용하게 되면 DRAM에서 다른 data를 더 많이 가져올 수 있게 되고, 이는 DRAM의 bandwidth가 상대적으로 여유로워질 것이다."

> "그러면 DRAM에서 데이터를 주고 받아야 하기 때문에, 거기서 발생하는 에너지 소모가 있을 것이고, DRAM에게 데이터 이동을 요구하기 때문에 bandwidth를 차지하게 되어 다른 data들이 이동할 수 없어질 수도 있을 것이다"

> "성능 올라가지 않을 것. 왜냐하면 현재 memory를 충분히 공급하지 못해 PE가 쉬고 있는 상황에서 굳이 PE를 더 추가한다고 해서 의미가 없음. 더 많은 PE가 쉴 것이다. memory-bound라 memory bandwidth가 현재 병목임"

> "output P에 계속해서 값들을 더해가는 구조이기 때문에, P를 PE안에 계속 유지한다면 새로 계산된 값 (새로 누적될 값)들만 불러와서 P에 더해주는 것이 효율적일 것이다."

> "각 데이터의 reuse 정도를 고려해야할 것 같아. 계산 마다, 많이 사용되는 값이 다를 수 있기 때문이지."

> "이렇게 하나의 A가 PE1 ~ PE4로 전달된다면, 각각의 PE가 SRAM에서 A를 독립적으로 읽는 것보다 유리할 것이다."

> "우리는 data reuse를 많이 하는 data는 DRAM에서 부터 PE까지 끌고 온 이후, PE 근처 register나 PE 내부의 저장소에 저장시켜서 필요할 때 마다 MAC에 데이터를 주는 것이 더 효율적이기 때문이다."

> "memory hierarchy를 사용하여, 많은 데이터는 off chip DRAM에 보관하고, 자주 쓰이는 data를 한 층 올려 SRAM에 그리고 data reuse가 많이 발생하는 data는 PE 근처 register 등에 배치하는 것이 데이터를 움직이고 저장하는데에 효율적이다."

</details>
