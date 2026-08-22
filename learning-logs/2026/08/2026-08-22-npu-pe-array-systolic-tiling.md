# 학습 기록: NPU PE Array, Systolic Array와 Matrix Tiling (NPU PE Array, Systolic Array and Matrix Tiling)

## Metadata

- Date: 2026-08-22
- Topic: NPU PE Array, Systolic Array와 Matrix Tiling
- Document type: learning-log
- Domain: npu
- Roadmap stage: Stage 4 — NPU Architecture
- Status: working
- Source: conversation
- Evidence: self-explanation, inference, comparison, misconception-correction, application
- Related notes: learning-logs/2026/08/2026-08-22-npu-sram-data-reuse-dataflow.md
- Last updated: 2026-08-22

## 1. 오늘 공부한 목적

- PE/PE array와 buffer hierarchy의 관계를 이해한다.
- pipeline, parallelism, PE utilization을 구분하고 systolic array에 연결한다.
- CPU/GPU/NPU의 specialization 차이를 NPU architecture 관점에서 이해한다.
- matrix multiplication의 M/N/K tiling과 partial sum을 구분한다.
- DRAM → SRAM → PE array → local storage/MAC → SRAM → DRAM의 전체 data path를 설명한다.

## 2. 오늘 이해한 내용

### PE array와 memory supply

사용자는 PE의 처리량과 memory가 PE에 공급할 수 있는 데이터 양을 비교해야 하며, memory-bound 상태에서는 PE를 크게 늘려도 실제 성능이 비례해 증가하지 않는다고 설명했다. PE 수가 증가하면 peak compute는 커질 수 있지만 memory bandwidth와 data reuse가 이를 뒷받침하지 못하면 PE가 데이터를 기다리게 된다.

### SRAM과 PE local storage

사용자는 같은 weight를 SRAM에서 매번 읽는 것보다 PE 내부/local register에 저장해 반복 사용하는 것이 더 빠르고, SRAM bandwidth와 SRAM access energy를 줄일 수 있다고 설명했다. 이를 통해 남은 SRAM bandwidth를 다른 필요한 데이터 전달에 사용할 수 있다고 연결했다.

### PE-to-PE communication의 이점과 새로운 병목

동일 activation을 여러 PE가 사용할 때 SRAM에서 각 PE로 반복 공급하는 대신 PE array 내부에서 공유하면 SRAM access와 bandwidth pressure를 줄일 수 있다고 설명했다. 이후 검증 과정에서 PE 내부 interconnect도 bandwidth, latency, communication energy를 가지며, SRAM 병목이 interconnect 병목으로 이동할 수 있음을 설명했다. SRAM access 감소가 곧 전체 성능 향상을 보장하지 않는다는 점도 확인했다.

### Pipeline, parallelism, PE utilization

사용자는 하나의 MAC resource를 동시에 두 데이터가 사용할 수 없는 이유를 hardware resource 수로 설명했다. Pipeline은 제한된 서로 다른 stage를 겹쳐 처리하는 방식이고, parallelism은 여러 MAC resource가 서로 다른 연산을 동시에 수행하는 방식이라고 구분했다. 또한 4개 PE 중 2개만 연산 중이면 utilization이 50%이며, data supply 부족 또는 pipeline 문제 등으로 PE가 idle할 수 있다고 설명했다. Memory-bound 상태에서는 PE 수만 늘려도 utilization 문제가 해결되지 않는다고 적용했다.

### Latency와 throughput

사용자는 pipeline이 채워진다고 해서 A1 하나가 더 빨리 이동하는 것은 아니며, 대신 더 많은 데이터를 동시에 처리할 수 있어 throughput이 증가한다고 설명했다. 하나의 작업 완료 시간인 latency는 같은 pipeline 조건에서 그대로일 수 있음을 구분했다.

### Systolic array

사용자는 matrix multiplication에서 각 원소가 반복적으로 사용되므로 data reuse가 발생하며, systolic array에서 데이터가 PE 사이를 규칙적으로 이동하면서 재사용되는 것이 효율적이라고 설명했다. PE-to-PE communication으로 SRAM 반복 traffic을 줄이고, pipeline이 채워지면 많은 PE를 동시에 활용하여 utilization과 throughput을 높일 수 있다고 설명했다. 또한 branch-heavy workload는 다음 연산과 data movement가 불규칙하여 systolic PE array를 규칙적으로 채우기 어렵다고 추론했다.

### CPU/GPU/NPU specialization

사용자는 큰 matrix multiplication 중심 workload에서는 범용 control에 transistor를 사용하는 것보다 MAC PE array와 SRAM buffer에 area를 투자한 AI-specialized chip이 유리하다고 설명했다. 같은 area budget에서 범용 기능을 위한 transistor를 줄이고 matrix/tensor compute와 on-chip storage에 투자하면 더 많은 병렬 MAC과 data reuse 기회를 얻을 수 있음을 이해했다. 다만 NPU가 복잡한 branch를 절대 수행할 수 없는 것이 아니라 CPU만큼 범용적이고 불규칙한 control flow에 최적화되지 않았다는 점으로 수정했다.

### Matrix tiling: M/N과 K의 차이

처음에는 A와 B를 어떻게 tile해야 하는지 불확실했고 C의 여러 tile을 어떻게 합쳐야 하는지 감이 없다고 명시했다. 이후 K 방향 tiling은 하나의 dot product를 SRAM capacity에 맞게 여러 조각으로 나누는 것이므로 각 조각의 partial sum을 더해야 한다고 설명했다. 예를 들어 8개의 곱을 한 tile에 4쌍씩 처리하면 K tile은 2개이며 두 tile의 결과를 더해 하나의 output을 완성한다고 설명했다.

반면 M/N 방향 tiling은 C의 서로 다른 output 영역을 나누는 것이므로 tile끼리 더하지 않고 각 위치에 배치한다고 설명했다. 하나의 C tile 계산에서는 A tile의 열 차원과 B tile의 행 차원이 같은 K tile dimension을 가져야 한다고 설명했다.

### Stage 4 종합 적용

PE 수를 2배로 늘렸지만 DRAM bandwidth가 포화되고 SRAM이 작아 tile을 자주 교체하며 PE가 idle한 상황에서, 사용자는 이를 memory-bound 상태로 진단했다. 작은 SRAM은 tile 교체와 DRAM↔SRAM movement를 증가시키고 on-chip reuse 기회를 제한하며, 결국 PE utilization을 낮춘다고 연결했다. 따라서 PE 추가보다 memory bandwidth, SRAM capacity, memory hierarchy, data reuse/dataflow를 함께 개선해야 한다고 제안했다.

## 3. 핵심 개념

- PE와 PE array
- Global SRAM buffer와 PE local register
- SRAM bandwidth와 PE-to-PE interconnect
- Pipeline과 parallelism
- Latency와 throughput
- PE utilization과 memory-bound
- Systolic array와 local data reuse
- CPU/GPU/NPU specialization
- Area budget과 compute-memory balance
- Matrix multiplication M/N/K dimensions
- M/N tiling과 output placement
- K tiling과 partial-sum accumulation
- NPU end-to-end data path

## 4. 내가 처음 이해한 방식

- PE 내부에서 데이터를 순차적으로 전달하면 SRAM에서 각 PE가 데이터를 읽는 것보다 내부 작업이므로 무리가 덜할 것으로 예상했다.
- Pipeline 예제에서 여러 데이터를 같은 cycle에 모두 fetch할 수 없는 이유가 한 번에 하나만 가져올 수 있기 때문인지 질문했다.
- Systolic array가 NPU에만 유리한 것인지, CPU/GPU에도 유용하지 않은지 의문을 제기했다.
- Matrix tiling에서 A의 윗부분과 B의 오른쪽 부분을 가져오는 식으로 생각했으나, C를 4등분했을 때 결과를 어떻게 합쳐야 하는지는 감이 없었다.
- 처음 K-tiling 문제에서는 6개의 곱 항에 대해 6개의 tile이 필요하다고 답했다.

## 5. 오해 또는 불확실한 부분

- PE-to-PE communication은 SRAM traffic을 줄일 수 있지만 내부 communication이 항상 가볍거나 빠른 것은 아니다. Interconnect bandwidth, hop latency, fan-out 및 communication energy가 새로운 병목이 될 수 있다.
- SRAM bandwidth를 줄이면 전체 NPU 성능이 자동으로 좋아지는 것은 아니다. 병목이 PE interconnect 또는 다른 memory level로 이동할 수 있다.
- Pipeline과 parallelism은 같은 개념이 아니다. MAC resource 수 증가가 직접적으로 의미하는 것은 spatial parallelism 증가이며, pipeline은 서로 다른 stage의 작업을 시간적으로 겹치는 것이다.
- NPU가 branch-heavy workload를 절대 수행할 수 없는 것은 아니다. 범용 CPU만큼 불규칙한 control flow에 최적화되지 않았다고 보는 것이 정확하다.
- Tile의 개수는 element 수와 같지 않다. Tile은 hardware가 한 번에 처리할 수 있는 데이터/연산 묶음이다.
- C의 모든 tile 결과를 마지막에 더하는 것은 아니다. M/N 방향의 서로 다른 output tile은 배치하고, K 방향으로 분할한 동일 output의 partial sum만 누적한다.

## 6. 수정된 이해

- SRAM에서 동일 데이터를 반복 공급하는 대신 PE array 내부 reuse를 활용하면 SRAM traffic을 줄일 수 있지만, 그 비용은 interconnect로 이동하므로 전체 bottleneck을 함께 분석해야 한다.
- Pipeline은 한 데이터의 latency를 반드시 줄이는 기술이 아니라 서로 다른 작업을 여러 stage에서 겹쳐 전체 throughput을 높이는 방식이다.
- Systolic array는 NPU 전용 개념이 아니라, 규칙적인 대규모 MAC과 data reuse가 많은 AI workload에 특히 잘 맞기 때문에 NPU/AI accelerator에서 유리하다.
- 같은 area budget에서 NPU는 범용 control 일부를 줄이고 MAC PE array, SRAM buffer, dataflow/interconnect에 더 많은 transistor를 배치할 수 있지만 compute와 memory의 균형이 필요하다.
- Matrix multiplication에서 M/N tiling은 output 공간을 나누고, K tiling은 같은 output의 dot-product reduction을 나눈다. 따라서 M/N tile은 위치에 배치하고 K tile 결과는 partial sum으로 누적한다.
- SRAM capacity가 커지는 것만으로 reuse가 자동 증가하는 것은 아니며, 더 큰 working set을 on-chip에 유지할 기회를 dataflow와 tiling이 실제 reuse로 활용해야 한다.

## 7. 질문

### 해결되지 않은 질문

- Stage 5의 memory wall은 지금까지 배운 NPU tiling/dataflow 최적화로도 왜 완전히 해결되지 않는가?
- PIM/CIM은 compute 위치를 memory 쪽으로 옮겨 data movement를 어떻게 바꾸는가?

### 해결된 질문

- PE 수를 늘려도 memory bandwidth가 부족하면 왜 실제 성능이 비례해 증가하지 않는가?
- SRAM과 PE local register 사이에서 locality를 높이면 어떤 이점이 있는가?
- PE-to-PE communication은 SRAM traffic을 줄이는 대신 어떤 interconnect 비용을 만드는가?
- Pipeline, parallelism, PE utilization은 어떻게 다른가?
- Pipeline이 latency와 throughput에 각각 어떤 영향을 주는가?
- Systolic array가 규칙적인 matrix multiplication에 왜 적합한가?
- CPU/GPU/NPU의 specialization은 area budget과 어떤 관계가 있는가?
- M/N tiling과 K tiling은 결과를 합치는 방식이 왜 다른가?
- Memory-bound NPU에서 PE 추가보다 memory/dataflow 개선이 필요한 이유는 무엇인가?

## 8. AI 반도체 및 SSL 목표와의 연결

이번 학습에서는 SRAM/DRAM 수준에서 배운 memory hierarchy를 실제 NPU PE array, systolic dataflow, matrix tiling과 연결했다. 특히 NPU 성능을 MAC 개수만으로 판단하지 않고 data movement, on-chip reuse, interconnect, utilization과 compute-memory balance를 함께 보는 architecture 관점을 형성했다. 이는 다음 단계에서 memory wall과 PIM/CIM을 이해하기 위한 직접적인 prerequisite가 된다.

## 9. 다음 행동

1. Stage 5에서 memory wall을 NPU의 off-chip data movement와 연결해 학습한다.
2. 기존 NPU의 compute-centric data movement와 PIM/CIM의 compute-location 변화를 비교한다.
3. PIM/CIM이 줄이는 movement와 새로 만드는 circuit/architecture trade-off를 자기 설명으로 검증한다.

## 10. 자기 설명 점검

- [x] 용어의 정의를 설명할 수 있다.
- [x] 구조 또는 동작 과정을 설명할 수 있다.
- [x] 관련 개념과 비교할 수 있다.
- [x] AI 반도체에서 왜 중요한지 설명할 수 있다.

## 사용자 원문

<details>
<summary>대화에서 제공한 원문 보기</summary>

> "memory bound 상태라면 1000개 넣었다고 해서 연산 성능이 더 좋아지지는 않을 것. compute bound에서는 PE가 추가되면 연산 성능이 더 좋아질 것."

> "SRAM에서 PE로 매번 읽는 것 보다는, PE 내부에 저장해서 읽는 것이 더 빠르기 때문. 그리고 그렇게 되면 SRAM bandwidth에도 부담을 덜 주기 때문에, 더 의미있는 data들이 SRAM을 통해 이동하게 되어 data 속도가 빨라질 것."

> "SRAM access를 줄인다고 해도, data가 PE 내부에서 잘 이동하지 못하는 상황, PE interconnect가 data를 잘 전달하지 못한다면 전체 성능이 좋아진다고 말하기 어렵다."

> "pipeline이 채워진다고 해서, A1이 더 빨리 이동하는 것이 아님. 더 많은 데이터를 처리할 수 있는 것이고, throughput이 증가하기는 할 것임. 근데 data를 처리하는 속도인 latency 는 변화 없음"

> "효율적인 이유는, 행렬곱을 할 때 특정 값이 계속해서 필요하다. 이는 data reuse가 각 원소별로 발생한다는 뜻이고 systolic array는 data들이 왼쪽->오른쪽, 위->아래로 이동하며 재사용되기 때문에 data reuse의 관점에서 보았을 때 효율적이다."

> "+한가지 궁금한점, 이게 NPU랑 무슨상관? CPU, GPU와 같은 곳에도 유용하지 않나?"

> "A는 범용적인 일을 처리하는데 transistor를 많이 소비했다면, B는 단순 행렬 연산을 빠르게 하는데에 transistor를 사용했기 때문이야. MAC이 더 많을 수록, 더 많은 양의 데이터를 병렬 연산...할 수 있잖아"

> "행렬을 어떻게 tile 해야하는지 모르겠음. A x B이면 내 생각에는 A의 윗부분과 B의 오른쪽 부분을 tiling 해서 적절하게 배치하는 것이 좋아보이는데, 저렇게 4등분하면 어떻게 합쳐야하는지 감이 안옴"

> "K 방향으로 나눈 tile들은 각 구역에 특정 위치에 존재하는 값을 계산하는데, 이 값을 계산하는 것 또한 SRAM 의 용량으로 인하여 한 번에 하지 못해서 dot곱들의 합을 쪼개는 행위임. 그래서 dot곱의 합을 또 다시 쪼갰기 때문에, 나중에 합칠 때 다 더해주어야함."

> "DRAM의 bandwidth가 100% 사용중인 상태에서 PE를 늘렸는데 속도가 빨라지지 않았다는 것은 memory boundary 상태임을 알 수 있다... PE를 추가하는 것 보다 memory의 용량을 늘리는 방향으로 가야한다. memory bandwidth를 증가시키고, DRAM,SRAM,register 간의 memory hierarchy를 잘 활용하여 SRAM에서의 data reuse를 더 효율적으로 할 수 있게끔 메모리 차원에서의 architecture 개선이 필요하다고 생각한다"

</details>
