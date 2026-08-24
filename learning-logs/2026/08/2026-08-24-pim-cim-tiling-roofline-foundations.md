# 학습 기록: PIM/CIM Tiling, Bottleneck과 Roofline 기초 (PIM/CIM Tiling, Bottlenecks, and Roofline Foundations)

## Metadata

- Date: 2026-08-24
- Recorded at: 2026-08-24T13:18:08Z
- Topic: PIM/CIM Tiling, Bottleneck과 Roofline 기초
- Document type: learning-log
- Domain: pim-cim
- Roadmap stage: Stage 5 — PIM / CIM
- Status: working
- Source: conversation
- Evidence: self-explanation, numerical reasoning, architecture comparison, misconception-correction, bottleneck diagnosis, unit analysis
- Related notes: learning-logs/2026/08/2026-08-23-memory-wall-analog-cim-fundamentals.md; learning-logs/2026/08/2026-08-22-npu-pe-array-systolic-tiling.md
- Last updated: 2026-08-24

## 1. 오늘 공부한 목적

이번 학습의 목적은 이전에 익힌 Memory Wall과 Analog CIM 기초를 더 구체적인 accelerator architecture reasoning으로 확장하는 것이었다. 특히 단순히 “CIM은 memory에서 연산하므로 data movement가 줄어든다”는 수준에서 멈추지 않고, 실제 큰 neural-network matrix를 제한된 CIM array에 mapping할 때 왜 tiling과 partial sum이 다시 등장하는지, 그리고 array 내부 MAC 성능을 높여도 ADC, activation bandwidth, interconnect, array parasitic 등의 주변 요소가 전체 성능을 제한할 수 있는 이유를 설명하는 것을 목표로 했다.

또한 NPU에서 배웠던 K-tiling, data reuse, memory-bound 개념을 CIM에 연결하고, Digital CIM과 Analog CIM의 차이, SRAM-CIM과 DRAM-PIM의 차이, 그리고 Arithmetic Intensity와 Roofline Model의 기본 직관까지 확장했다. 최종적으로는 component 하나의 peak 성능보다 전체 data path의 balance가 중요하다는 관점을 자기 언어로 설명하는 것을 목표로 했다.

## 2. 오늘 이해한 내용

### CIM K-tiling과 partial sum

사용자는 하나의 CIM array가 K=4까지만 처리할 수 있고 전체 dot product가 K=16이라면 4개의 K-tile이 필요하다고 계산했다. 각 CIM array가 만드는 결과는 최종 output이 아니라 같은 output을 구성하는 partial sum이며, 마지막에 이 partial sum들을 모두 더해야 한다고 설명했다.

이 과정에서 NPU의 M/N tiling과 K-tiling의 차이와 CIM tiling이 연결되었다. M/N 방향 tiling은 서로 다른 output 위치를 분할하므로 결과를 각 위치에 배치하지만, K 방향 tiling은 하나의 dot product의 reduction dimension을 분할하기 때문에 각 tile 결과를 누적해야 한다. 사용자는 이후 CIM에서도 큰 weight matrix가 하나의 array에 들어가지 않을 때 같은 이유로 K-tiling과 inter-array accumulation이 필요함을 설명했다.

### Array size 증가의 이점과 제약

K=4에서 K=8까지 처리할 수 있는 더 큰 CIM array를 가정했을 때, 사용자는 K-tile 수가 4개에서 2개로 줄어들고 partial sum 수, partial sum movement, digital accumulation workload도 감소한다고 추론했다. ADC conversion workload 역시 설계에 따라 줄어들 수 있다는 방향으로 이해했다.

반면 array를 무조건 크게 만들 수 없는 이유로 area와 transistor resource뿐 아니라 bitline capacitance 증가를 제시했다. 특히 더 긴 BL에 더 많은 cell이 연결되면 parasitic capacitance가 증가하고 sensing response가 느려질 수 있다는 점을 설명했다. 이후 I=C·dV/dt 관계를 통해 capacitance 증가가 cell current 자체를 반드시 줄인다는 뜻이 아니라, 같은 current에서 voltage 변화 속도를 늦출 수 있다는 쪽으로 정리했다.

### NPU tiling과 CIM tiling 비교

사용자는 NPU에서 큰 workload를 제한된 SRAM buffer와 compute resource에 맞추기 위해 tiling이 필요하고, CIM에서는 거대한 weight matrix를 제한된 CIM array에 모두 저장할 수 없을 때 tiling이 필요하다고 비교했다.

NPU에서는 주요 제약이 SRAM capacity, PE array 크기, local storage, bandwidth, reuse 등 architecture resource 중심이라면, CIM에서는 여기에 WL/BL parasitic resistance/capacitance, sensing margin, precision 등의 circuit-level 제약이 강하게 추가된다고 이해했다. 따라서 CIM에서도 array를 크게 하면 tiling overhead는 줄일 수 있지만 physical array scaling cost가 증가하는 trade-off가 존재한다고 정리했다.

### Analog CIM precision과 multi-bit 표현

사용자는 높은 precision을 하나의 analog voltage/current level로 직접 표현하려 하면 0~1 등의 제한된 signal range를 더 많은 level로 나누어야 하므로 각 level 간 간격이 좁아지고 noise에 민감해질 수 있다고 설명했다. ADC 역시 작은 analog 차이를 더 정밀하게 구분해야 하기 때문에 부담이 커질 수 있다고 이해했다.

처음에는 8-bit 연산이면 하나의 analog range를 반드시 256개 level로 직접 나누는 식으로 일반화하는 경향이 있었으나, bit-serial 또는 bit-slicing 방식으로 여러 cycle에 나누어 계산하고 digital shift-and-add로 positional weight를 복원할 수 있다는 점을 다시 확인했다. 따라서 높은 precision이 곧 하나의 analog signal에서 2^N level을 직접 구분해야 한다는 뜻은 아니며, analog precision 부담과 cycle/digital reconstruction 비용 사이의 trade-off가 존재한다고 수정했다.

### Analog CIM과 Digital CIM 비교

사용자는 Analog CIM에서는 current가 전달되고 sensing되는 과정에서 noise, variation, leakage, parasitic 등의 영향으로 값이 변할 수 있어 precision 문제가 생길 수 있다고 보았다. Digital CIM은 logic 0/1을 threshold와 noise margin으로 구분하므로 상대적으로 noise에 robust할 수 있다고 설명했다.

초기에는 Digital CIM이 모든 신호를 digital로 변환하기 위한 별도의 conversion hardware를 많이 필요로 하고, analog처럼 병렬 accumulation을 할 수 없어 순차적으로 합산해야 한다고 생각했다. 이후 이 부분이 수정되었다. Digital CIM의 핵심 cost는 ADC가 아니라 AND/XNOR, adder, popcount, accumulator 등의 digital logic, area, wiring, energy overhead에 있으며, adder tree 등을 사용하면 digital accumulation도 충분히 병렬적으로 수행할 수 있다. Analog CIM은 bitline의 물리적 current/charge summation으로 accumulation을 자연스럽게 얻을 수 있다는 점에서 높은 compute density 잠재력이 있지만, ADC, sensing, variation, precision 문제를 부담한다는 차이를 이해했다.

### ADC sharing과 system bottleneck

사용자는 ADC 수를 줄여 여러 column이 공유하도록 하면 ADC가 차지하는 area와 관련 energy overhead를 줄일 수 있지만, 여러 column 결과를 시간적으로 나누어 conversion해야 하므로 throughput이 감소할 수 있다고 설명했다.

또한 ADC가 한 column 결과를 처리하는 동안 다른 column이 기다릴 수 있어 system-level utilization이 떨어질 수 있다고 추론했다. 이후 “column이 반드시 연산하지 못한다”라고 단정하기보다는 architecture에 따라 result holding이나 pipelining이 가능하고, 정확한 의미는 ADC conversion bandwidth가 array result generation rate를 따라가지 못할 때 array/system이 기다리면서 effective utilization이 감소한다는 것으로 정리했다.

수치 예제에서 CIM array가 cycle당 64개 column 결과를 만들지만 ADC subsystem이 16개만 변환할 수 있다면 ADC가 bottleneck이며 array의 잠재 result generation capability 대비 25%만 소화할 수 있다고 계산했다. CIM array compute를 128 results/cycle로 두 배 높여도 ADC가 16 results/cycle로 고정되어 있으면 system throughput은 거의 증가하지 않고 상대 utilization은 12.5% 수준으로 더 낮아질 수 있다고 설명했다.

### SRAM-CIM과 DRAM-PIM

사용자는 아주 큰 neural-network weight가 on-chip SRAM에 모두 들어가지 않는 상황에서는 DRAM-PIM이 weight movement를 더 크게 줄일 가능성이 있다고 추론했다. SRAM-CIM에서는 capacity가 부족해 weight를 DRAM에서 반복적으로 가져와야 할 수 있지만, DRAM-PIM에서는 큰 DRAM capacity 내부 또는 가까운 위치에 weight를 두고 activation을 공급하여 외부 weight movement를 줄일 수 있기 때문이다.

초기에는 DRAM에 연산자를 추가하면 memory cell 자체에 transistor가 늘어 density가 낮아질 것이라고 주로 생각했다. 이후 PIM이 반드시 cell마다 compute transistor를 추가하는 구조는 아니며 bank peripheral이나 memory-near logic을 활용할 수도 있다는 점을 확인했다. 따라서 DRAM-PIM의 trade-off를 density 하나로만 보지 않고 area, power, thermal, bandwidth interference, programmability, integration overhead 등 broader system cost로 보는 관점으로 확장했다.

### Weight movement를 줄여도 남는 activation bottleneck

사용자는 DRAM-PIM에서 weight movement를 거의 0으로 줄이더라도 activation과 intermediate result가 NPU와 DRAM-PIM 사이를 계속 이동해야 하고, 이 traffic이 PIM compute rate보다 느리면 다시 bandwidth bottleneck이 생긴다고 설명했다.

즉 PIM/CIM은 Memory Wall을 완전히 제거한다기보다 특정 data movement, 특히 weight movement를 크게 줄이는 방향이며, 병목이 activation movement, ADC, interconnect, accumulation 등 다른 위치로 이동할 수 있다고 이해했다.

### Workload 특성과 stationary strategy

두 workload 비교에서 사용자는 같은 1 GB weight를 높은 reuse로 반복 사용하는 workload A가 weight-stationary PIM/CIM의 이점을 더 크게 얻을 것이라고 판단했다. Activation traffic도 작다면 PIM/CIM compute에 필요한 data supply가 비교적 쉬워 bottleneck이 적을 수 있다고 설명했다.

반면 weight reuse가 낮고 큰 activation/intermediate tensor가 계속 생성되는 workload B에서는 weight-stationary 최적화의 상대적 가치가 낮고, activation locality와 tiling/dataflow optimization이 더 중요할 수 있다고 추론했다. 처음에는 B에서 NPU가 더 유리할 수 있다고 바로 결론내렸지만, 이후 architecture 이름 자체보다 data size × movement frequency × movement cost 관점으로 판단해야 한다는 방향으로 정리했다.

### Arithmetic Intensity의 의미

사용자는 Arithmetic Intensity가 단순히 Byte와 OP를 같게 보는 개념이 아니라, workload가 수행한 총 operation 수를 DRAM과 이동한 총 Byte 수로 나눈 비율임을 학습했다.

예를 들어 100 OP을 수행하면서 20 Byte를 이동하면 AI는 5 OP/Byte이다. 이는 “1 Byte와 5 OP가 같은 단위”라는 뜻이 아니라, 해당 workload에서 DRAM traffic 1 Byte당 평균 5번의 useful operation을 수행했다는 의미이다.

64 GOP workload가 8 GB의 DRAM traffic을 발생시키면 AI=8 OP/Byte이며, traffic을 2 GB로 줄이면 AI=32 OP/Byte로 4배 증가한다고 계산했다. 또한 같은 총 operation에서 DRAM traffic을 줄이는 data reuse가 AI를 높인다는 점을 이해했다.

Weight-stationary 예제에서는 A 설계가 activation마다 1 GB weight를 다시 DRAM에서 읽고, B 설계가 weight를 한 번 SRAM에 올린 뒤 4개의 activation에 재사용하는 상황을 비교했다. A의 총 traffic은 4.4 GB, B는 1.4 GB로 계산했고, 동일한 800 GOP workload에서 각각 약 181.8 OP/Byte와 571.4 OP/Byte의 AI를 구했다. 마지막 배율을 처음에는 대략 4배라고 답했지만 실제로는 약 3.14배이며, activation 0.4 GB traffic이 그대로 남기 때문에 weight traffic의 4배 감소가 전체 traffic 4배 감소로 그대로 이어지지 않는다는 점을 수정했다.

### Roofline Model의 직관

사용자는 memory bandwidth의 단위가 GB/s이고 peak compute의 단위가 TOPS라는 점을 구분했다. BW×AI를 계산하면 Byte/s × OP/Byte = OP/s가 되어, memory가 직접 연산한다는 뜻이 아니라 현재 workload의 data reuse를 고려했을 때 memory system이 PE의 연산을 최대 몇 OP/s까지 지속적으로 뒷받침할 수 있는지를 의미한다고 이해했다.

Peak compute가 10 TOPS인데 BW×AI가 3 TOPS라면 actual performance upper bound는 min(10,3)=3 TOPS이고 memory-bound이다. 반대로 BW×AI가 20 TOPS라도 compute peak가 10 TOPS라면 실제 성능은 10 TOPS이며 compute-bound이다.

Peak compute 12 TOPS, BW×AI 8 TOPS 예제에서는 actual performance를 8 TOPS, memory-bound로 올바르게 판단했다. 이후 peak compute를 24 TOPS로 높였을 때 처음에는 12 TOPS라고 답했지만, memory-side limit가 여전히 8 TOPS이므로 actual performance는 8 TOPS 그대로라는 점을 수정했다.

Dataflow 개선으로 AI가 2배 증가하여 BW×AI가 8→16 TOPS가 되면 peak compute 12 TOPS가 새로운 bottleneck이 되어 actual performance 12 TOPS, compute-bound가 된다고 정확히 설명했다.

Ridge point 계산에서는 peak compute 20 TOPS와 bandwidth 500 GB/s에서 AI=40 OP/Byte가 경계임을 확인했고, 8 TOPS와 200 GB/s에서도 같은 40 OP/Byte를 계산했다. 사용자는 단위가 헷갈린다고 명시적으로 질문했고, TOPS=OP/s, GB/s=Byte/s로 풀어 쓴 뒤 나누면 OP/Byte가 된다는 방식으로 단위를 정리했다.

64 GOP workload, 8 GB traffic, 16 TOPS peak, 400 GB/s bandwidth 문제에서는 AI=8 OP/Byte, memory-supported rate=3.2 TOPS, memory-bound임을 계산했다. 처음에는 actual performance를 peak compute인 16 TOPS로 답했으나 실제 상한은 min(16,3.2)=3.2 TOPS임을 수정했다. Traffic을 2 GB로 줄이면 AI=32 OP/Byte, memory-supported rate=12.8 TOPS, actual performance 12.8 TOPS로 증가하며 성능 향상 배율이 4배임을 확인했다.

Traffic을 1 GB로 줄인 경우 AI=64 OP/Byte, BW×AI=25.6 TOPS, actual performance 16 TOPS, compute-bound로 판단했다. 실행 시간 계산에서 처음에는 64 GB / 16 TOPS라고 적었지만 workload 양은 64 GOP이므로 64 GOP / 16 TOPS = 4 ms가 맞다는 점을 수정했다.

### 종합 bottleneck reasoning

최종 종합 문제에서 사용자는 CIM array의 MAC 성능을 높여도 activation bandwidth가 compute rate를 따라가지 못하면 MAC에 필요한 data가 충분히 공급되지 않고, ADC throughput이 낮으면 analog output conversion이 지연되어 effective utilization이 낮아진다고 설명했다. 이 상태에서 MAC peak만 높이는 것은 전체 성능 향상 효과가 작다고 판단했다.

또한 array를 크게 만들수록 BL capacitance가 증가해 sensing latency 문제가 커질 수 있다고 연결했고, Arithmetic Intensity를 높여 이동한 data를 더 많이 reuse하면 bandwidth pressure를 완화할 수 있다고 제안했다. 여기서 “BL capacitance 증가로 latency가 줄어든다”라고 표현한 부분은 반대로 latency가 증가할 가능성이 크다는 것으로 교정했고, BL capacitance 증가가 곧 ADC throughput 감소를 직접 보장하는 것은 아니라 sensing margin, parasitic, ADC architecture를 함께 봐야 한다는 점도 정리했다.

## 3. 핵심 개념

- CIM K-tiling과 reduction dimension
- Partial sum과 inter-array accumulation
- M/N tiling과 K-tiling의 차이
- CIM array size와 mapping capacity
- Bitline/wordline parasitic resistance와 capacitance
- I=C·dV/dt와 sensing latency 직관
- Analog CIM과 Digital CIM
- Multi-bit representation, bit-serial, bit-slicing, shift-and-add
- ADC resolution, ADC sharing, conversion serialization
- System-level utilization과 ADC-bound 상태
- SRAM-CIM과 DRAM-PIM
- PIM과 CIM의 compute location 차이
- Weight movement, activation movement, intermediate movement
- Weight-stationary dataflow
- Data reuse와 locality
- Arithmetic Intensity (OP/Byte)
- Peak compute (TOPS)
- Memory bandwidth (GB/s)
- Memory-supported compute rate = BW × AI
- Roofline upper bound = min(Peak Compute, BW × AI)
- Memory-bound / Compute-bound
- Ridge point
- Traffic reduction과 AI 증가
- Component peak 성능과 end-to-end system balance

## 4. 내가 처음 이해한 방식

- CIM K dimension을 크게 할수록 tile 수와 partial sum이 줄어드니 가능한 크게 만드는 것이 유리하다고 보았고, 주요 제약을 area와 transistor 수로 먼저 생각했다.
- 큰 CIM array에서 BL capacitance가 증가하면 cell current 자체가 줄어드는 방향으로 생각했던 이전 직관이 남아 있었고, 이후 같은 current에서 voltage response가 느려진다는 관점으로 수정했다.
- 높은 bit precision에서는 0~1 사이 analog voltage range를 2^N개의 촘촘한 영역으로 직접 나누어 digital 값을 배정해야 한다고 일반화했다.
- Digital CIM은 모든 signal을 digital로 바꾸기 위한 conversion hardware가 많이 필요하고, analog처럼 current summation을 사용할 수 없으므로 순차적으로 모두 더해야 한다고 생각했다.
- ADC sharing 시 다른 column은 연산 자체를 못 하므로 utilization이 감소한다고 단순화했다.
- DRAM-PIM은 DRAM cell에 compute transistor를 추가하는 구조로 생각하여 memory density 감소를 주요 trade-off로 예상했다.
- Weight reuse가 낮고 activation traffic이 큰 workload에서는 곧바로 NPU가 더 유리할 수 있다고 판단했다.
- TOPS와 GB/s가 서로 다른 종류의 단위라는 점에서 혼란을 느꼈고, “1 Byte = 1 OP인가?”라는 질문을 했다.
- Peak compute가 높으면 actual performance도 그 값에 가까울 것이라고 생각해 memory-bound 예제에서 16 TOPS를 실제 성능으로 답하거나, compute peak를 높였을 때 memory limit가 그대로인데도 성능이 증가한다고 답한 적이 있었다.
- 동일 workload에서 weight traffic이 4배 줄었으므로 AI 향상도 약 4배일 것이라고 추정했으나 activation traffic이 남아 있어 전체 AI 향상은 약 3.14배였다.

## 5. 오해 또는 불확실한 부분

### 수정된 오해

- K를 더 크게 처리하는 CIM array가 무조건 좋은 것은 아니다. Tile/partial-sum overhead를 줄이는 대신 WL/BL parasitic, sensing, precision, area 문제가 커질 수 있다.
- BL capacitance가 증가한다고 해서 cell current 자체가 반드시 감소하는 것은 아니다. 같은 current라면 dV/dt가 작아져 voltage response가 느려질 수 있다.
- 8-bit 연산이 반드시 하나의 analog signal에서 256개 level을 직접 구분한다는 뜻은 아니다. Bit-serial/bit-slicing으로 precision 부담을 시간과 digital reconstruction cost로 바꿀 수 있다.
- Digital CIM이 ADC를 더 많이 필요로 하는 것은 아니다. 오히려 high-resolution ADC burden을 피할 수 있고, 대신 digital adder/popcount/accumulator logic과 area/energy cost가 증가할 수 있다.
- Digital CIM은 반드시 순차적으로 accumulation하는 것이 아니다. Adder tree 등으로 병렬 reduction이 가능하다.
- ADC sharing은 “공유되지 않는 column이 반드시 연산하지 못한다”로 단정할 수 없다. 정확한 system bottleneck은 conversion bandwidth가 result generation rate보다 낮아 pipeline/system이 기다리는가에 달려 있다.
- DRAM-PIM은 반드시 DRAM cell마다 compute transistor를 추가하는 구조가 아니다. Bank peripheral 또는 memory-near logic을 활용하는 구현도 가능하다.
- Weight movement 감소만으로 Memory Wall이 완전히 해결되는 것은 아니다. Activation/output/intermediate movement가 새로운 bandwidth bottleneck이 될 수 있다.
- Arithmetic Intensity의 OP와 Byte는 같은 단위가 아니다. AI는 두 양의 ratio이다.
- Peak compute는 actual performance와 동일하지 않다. Actual upper bound는 memory-supported rate와 peak compute 중 작은 값이다.
- Data traffic을 특정 component에서 4배 줄였다고 전체 AI가 항상 4배 증가하는 것은 아니다. 다른 traffic이 남아 있으면 전체 ratio 개선 폭은 작아질 수 있다.
- 실행 시간 계산에서 workload 양은 GOP이고 data traffic은 GB이다. Compute time에 GB를 넣으면 단위가 맞지 않는다.

### 아직 깊게 검증하지 않은 부분

- 실제 Digital CIM macro에서 사용하는 구체적인 logic topology와 popcount/adder placement
- 실제 DRAM-PIM 제품/논문에서 bank-level compute와 memory scheduling이 어떻게 공존하는지
- Analog CIM에서 ADC architecture별 resolution/energy/throughput scaling의 정량적 차이
- 실제 논문의 measured Roofline 또는 operational intensity analysis

위 항목은 현재 PIM/CIM foundation의 blocking gap은 아니며, 이후 논문 분석에서 필요할 때 spiral learning으로 돌아갈 수 있다.

## 6. 수정된 이해

- CIM tiling은 NPU tiling과 마찬가지로 hardware가 전체 problem dimension을 한 번에 수용하지 못할 때 필요하며, K 방향 분할은 같은 output의 reduction을 나누므로 partial sum accumulation이 필요하다.
- CIM array를 크게 하면 tile 수와 inter-array accumulation overhead를 줄일 수 있지만, physical array가 커지면서 WL/BL parasitic과 sensing/precision 문제가 증가할 수 있으므로 optimal array size는 architecture와 circuit constraint의 trade-off로 결정된다.
- Analog CIM은 physical current/charge/voltage summation을 활용해 높은 병렬성과 compute density를 얻을 잠재력이 있지만 noise, variation, parasitic, ADC/sensing precision 부담이 있다.
- Digital CIM은 logic threshold와 noise margin 덕분에 analog precision 문제에서 상대적으로 robust할 수 있고 high-resolution ADC burden을 피할 수 있으나, digital compute/accumulation logic의 area와 energy cost가 있다. Digital accumulation도 병렬화할 수 있다.
- ADC sharing은 area/일부 energy overhead를 줄일 수 있지만 conversion serialization으로 throughput bottleneck을 만들 수 있다. Array result rate보다 ADC conversion rate가 낮으면 system이 ADC-bound가 될 수 있다.
- DRAM-PIM은 큰 capacity와 internal bandwidth를 활용해 특히 weight movement를 줄일 수 있지만 activation/output movement, integration cost, power/thermal, bandwidth interference 등의 trade-off가 남는다.
- PIM/CIM은 Memory Wall을 완전히 제거하는 기술이라기보다 compute 위치를 memory 쪽으로 이동해 특정 movement를 줄이는 전략이며, bottleneck이 다른 subsystem으로 이동할 수 있다.
- 어떤 stationary strategy가 좋은지는 data size 자체보다 reuse frequency와 movement cost를 함께 봐야 한다.
- Arithmetic Intensity는 이동한 Byte당 수행한 useful operation의 양이며, data reuse가 증가해 DRAM traffic이 줄면 같은 workload에서 AI가 증가한다.
- Roofline 관점에서는 actual performance upper bound가 `min(Peak Compute, BW × AI)`로 제한된다. 따라서 memory-bound 상태에서는 compute peak를 높이는 것보다 bandwidth 또는 AI 개선이 먼저 효과를 낼 수 있다.
- 반대로 AI가 충분히 높아져 BW×AI가 peak compute를 넘으면 bottleneck은 compute로 이동하며, 이후 memory traffic을 더 줄여도 성능이 같은 비율로 증가하지 않는다.
- 전체 accelerator 성능은 array MAC peak 하나보다 activation supply, ADC throughput, interconnect, accumulation, memory traffic, parasitic 등 end-to-end data path balance로 판단해야 한다.

## 7. 질문

### 해결되지 않은 질문

- 실제 Foundational PIM/CIM 논문에서 architecture block diagram을 볼 때 어떤 subsystem이 measured bottleneck인지 어떻게 찾아낼 것인가?
- 실제 논문의 compute efficiency, energy efficiency, ADC overhead, data reuse를 Roofline 또는 유사한 quantitative framework로 어떻게 해석할 것인가?
- Digital CIM과 Analog CIM을 실제 silicon result로 비교할 때 precision, area, TOPS/W, TOPS/mm²를 어떤 기준으로 공정하게 비교해야 하는가?

### 해결된 질문

- CIM에서 K-tiling이 발생하면 왜 각 array 결과를 partial sum으로 더해야 하는가?
- K capacity를 키우면 tile 수, ADC workload, partial-sum movement, digital accumulation에 어떤 이점이 생기는가?
- CIM array를 무조건 크게 만들 수 없는 이유는 무엇인가?
- NPU K-tiling과 CIM K-tiling의 공통점과 차이는 무엇인가?
- 높은 analog precision이 noise와 ADC에 왜 부담을 주는가?
- Digital CIM은 왜 analog precision 문제에 상대적으로 robust할 수 있으며 어떤 hardware cost를 지불하는가?
- Digital CIM은 반드시 순차적으로 accumulation해야 하는가?
- ADC sharing은 area, energy, throughput, utilization에 어떤 trade-off를 만드는가?
- CIM array compute를 높여도 ADC throughput이 낮으면 왜 system throughput이 증가하지 않는가?
- SRAM-CIM보다 DRAM-PIM이 큰 weight movement를 더 줄일 수 있는 상황은 언제인가?
- DRAM-PIM에서 weight movement가 사라져도 왜 activation bandwidth가 새로운 bottleneck이 될 수 있는가?
- Weight-stationary PIM/CIM이 특히 유리한 workload는 어떤 특성을 가지는가?
- Arithmetic Intensity는 무엇이며 Byte와 OP는 어떤 관계인가?
- Data reuse와 DRAM traffic 감소가 AI를 어떻게 변화시키는가?
- BW×AI의 TOPS 값은 memory가 연산한다는 뜻인가?
- Roofline에서 memory-bound와 compute-bound를 어떻게 판단하는가?
- Peak compute를 올려도 memory-bound 성능이 그대로일 수 있는 이유는 무엇인가?
- Ridge point는 어떤 의미인가?
- Workload operation 수, DRAM traffic, peak compute, bandwidth로 actual upper bound와 실행 시간을 어떻게 계산하는가?

## 8. AI 반도체 및 SSL 목표와의 연결

이번 학습은 NPU architecture와 memory hierarchy에서 배운 data movement 관점을 PIM/CIM까지 확장했다. 특히 단순한 “CIM은 memory에서 계산해서 빠르다”는 설명에서 벗어나, 실제 accelerator의 성능은 array compute, ADC, activation buffer, interconnect, partial-sum accumulation, physical array scaling이 함께 결정한다는 architecture-level 관점을 형성했다.

이는 PIM/CIM 논문의 핵심 claim을 비판적으로 읽는 데 직접적인 기반이 된다. 향후 논문에서 “X TOPS/W”, “높은 array utilization”, “ADC overhead 감소”, “in-memory MAC” 같은 claim을 볼 때, 해당 수치가 array-local peak인지 system-level end-to-end result인지, 어떤 data movement가 포함되거나 제외되었는지, workload의 Arithmetic Intensity와 reuse가 어떤지 질문할 수 있게 되었다.

또한 NPU의 memory-bound 문제와 CIM의 ADC/activation-bound 문제를 동일한 bottleneck 이동 관점으로 연결했고, Roofline의 `min(Peak Compute, BW × AI)` 직관을 통해 component peak와 actual throughput을 구분할 수 있게 되었다. 이는 이후 Foundational Paper의 architecture walkthrough와 claim map을 만들 때 problem → bottleneck → architectural intervention → new bottleneck → measured evidence를 연결하는 핵심 prerequisite가 된다.

## 9. 다음 행동

1. 중심 Foundational PIM/CIM 논문 한 편을 선정하고 abstract와 주요 architecture figure를 읽으면서 `problem → prior bottleneck → proposed compute location → data path → claimed benefit`의 claim map을 만든다.
2. 논문의 주요 figure에서 weight, activation, partial sum, ADC/digital accumulation이 각각 어디에 위치하고 어떻게 이동하는지 직접 표시한다.
3. 논문의 성능/에너지 결과를 읽을 때 array peak만 보지 않고 ADC/peripheral overhead, data movement, precision, utilization을 함께 확인하고, 가능하면 Arithmetic Intensity 또는 Roofline 관점으로 memory-bound/compute-bound 가능성을 추론한다.

## 10. 자기 설명 점검

- [x] 용어의 정의를 설명할 수 있다.
- [x] 구조 또는 동작 과정을 설명할 수 있다.
- [x] 관련 개념과 비교할 수 있다.
- [x] AI 반도체에서 왜 중요한지 설명할 수 있다.

## 사용자 원문

<details>
<summary>대화에서 제공한 원문 보기</summary>

> "4개의 K-tile이 필요하다. 각 CIM array가 만드는 결과는 partial sum이고 마지막으로 이 partial sum들을 다 더해주는 과정이 필요함"

> "먼저 2번의 cycle로 연산이 끝남. 그리고 이 뜻은 ADC 를 사용하는 횟수도 2번으로 줄어들고, partial sum도 2개만 만들어서 합치면 되기 때문에 partial sum의 이동도 줄어들게 됨. 당연하게도 digital accumulation도 줄어들게 됨."

> "그러나 array를 무조건 크게 만들 수 없는 이유는 아무래도 제한된 area, transistor일 것임. 혹은 array를 크게 만들게 되면 한 번의 연산을 통해 부담해야하는 memory cell이 증가하여 BL에 부담을 줄 수도 있고, BL자체가 증가하여 BL capacitance 증가로 인한 문제도 발생할 수도 있을 것임"

> "NPU에서 K-tiling을 해야하는 이유는 NPU의 SRAM buffer의 memory 용량이 충분하지 않기 때문에 DRAM에서 한 번에 모든 data를 이동할 수 없음. 그래서 큰 data를 여러개로 쪼개는 tiling 과정이 필요하게 됨."

> "CIM 에서 K-tiling이 발생할 경우 추가적으로 고려해야하는 제약은, K를 무작정 늘린다고 해서 좋아지는 것이 아니라는 사실임."

> "precision 요구가 높아지게 되고 bit수가 증가하게 되면, 0~1사이의 voltage 영역을 많이 쪼개서 각 영역에 digital 값을 배정해야 한다. bit가 증가하게 되면 그 영역이 많이 발생하고 촘촘하게 발생되어, 약간의 noise에도 값이 변화할 수 있는 위험이 발생한다."

> "analog CIM은 이렇게 정보(current)가 전달되는 과정에서 noise가 발생되어 그 값이 변할 수 있다는 위험이 존재한다. ... 그러나 digital CIM은 값을 0,1로 획일화 하여 연산하기 때문에 noise에 비교적 안전하다."

> "ADC가 차지하는 area를 줄일 수 있고, ADC가 사용하는 energy 역시 줄일 수 있다. 그러나 여러 column이 ADC를 공유하기 때문에 당연하게도 한 번에 처리할 수 있는 데이터의 양은 줄어들게 된다. throughput이 줄어든다는 의미이다."

> "CIM은 column에 결과를 빠르게 만들어내지만 ADC가 한 cycle에 16개의 결과만 변환할 수 있다면, ADC에서 bottleneck이 발생하여 CIM의 연산속도를 온전히 감당할 수 없다."

> "DRAM-PIM이 weight movement를 더 크게 줄일 것 같음. 그 이유는 SRAM에 weight를 다 넣을 수 없어서 DRAM과의 data movement를 많이 해야하는 상황이라면, DRAM 내부에 연산자를 탑재하여 DRAM 내부에 방대한 양의 weight를 지정해두고, activation을 불러와서 DRAM 내부에서 연산을 하는 것이 weight movement를 더 크게 줄일 것 같음."

> "이 시스템에서 새로운 bottleneck은 activation의 움직임이다. weight movement 는 0이라고, activation이 PIM-DRAM에서의 연산 속도보다 느리게 전달 된다면, bottleneck이 형성된다."

> "A가 장점을 더 크게 얻을 것임. 그 이유는 weight의 reuse가 많기 때문에, weight의 data movement가 적은 PIM/CIM이 유리할 것."

> "AI는 증가할 것이다. 왜냐하면 동일한 데이터를 더 많이 reuse했기 때문에 하나의 데이터를 여러번 연산해서 AI가 증가할 것."

> "근데 이 TOPS라는게 결국 초당 얼마나 많은 연산을 하는지를 나타내는 것인데, 이것은 PE의 성능이고 너가 지금까지 memory bandwidth가 좋아져서 최대 3TOPS 라고 하는 의미는, memory에서 PE가 최대 3TOPS의 연산을 할 수 있게끔 data를 준다는 의미지? memory가 3TOPS의 연산을 한다는 말이 아니지?"

> "단위가 헷갈림 ㅠㅠ 20TOPS / 500GB/s 일 것 같음. 둘을 나누면 됨"

> "1byte = 1OP야??"

> "5OP/byte 이게 AI아님?"

> "A : 4.4GB의 data flow가 발생할 것. AI = 800GOP / 4.4GB = 181.8 OP/byte\nB : 1.4GB의 data flow가 발생할 것. AI = 800GOP / 1.4GB = 571.4 OP/byte"

> "CIM array의 MAC 성능을 높인다고 해도 MAC에 가져다줄 data가 MAC의 연산속도를 따라갈 수가 없음. activation bandwidth가 부족하기 때문임. 또한 ADC throughput도 낮기 때문에, MAC에서 연산이 끝난 analog output을 digital 값으로 변환시켜주는 시간도 오래걸림. 따라서 MAC utilization이 낮은 상태임."

> "Arithmetic intensity를 높이는 것이 더 좋아보임. memory의 이동량의 한계가 있다면 AI를 높여서 data reuse를 높인 다음, 하나의 memory를 더 많이 연산시키는 것이 현재 CIM을 더욱 가속할 수 있을 것임"

</details>
