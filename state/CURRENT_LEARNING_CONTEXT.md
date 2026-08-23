# Current Learning Context

> 이 문서는 `learning-logs/**`와 roadmap에서 자동 생성한 derived/generated snapshot이다. Source of truth가 아니며 원본 기록을 다시 확인할 수 있다.

- Last generated date: 2026-08-23
- Progress source SHA: `3df019f079517bfd210035c89773c01339a6daad`
- Roadmap reconciliation: **pending-approval**

## Roadmap Position

- 최신 의미 있는 학습 기록: `learning-logs/2026/08/2026-08-23-memory-wall-analog-cim-fundamentals.md`
- Current Stage: Stage 3 — Memory
- Current Topic: NPU PE array, buffer hierarchy와 dataflow
- Domain: pim-cim
- Depth Boundary: `npu-architecture-foundations`

### 같은 날짜의 의미 있는 학습 단위

- `learning-logs/2026/08/2026-08-23-memory-wall-analog-cim-fundamentals.md` — Memory Wall과 Analog CIM 기초

## Topic Goal

- NPU data path와 dataflow가 data movement와 utilization을 바꾸는 방식을 설명한다.

## Minimum Required Understanding

- PE와 PE array
- buffer hierarchy
- 대표 dataflow 한 가지
- data reuse와 utilization

## Exit Criteria

- [x] 입력부터 출력까지 PE array와 buffer를 지나는 data path를 설명한다.
- [x] 대표 dataflow가 어떤 data movement를 줄이는지 설명한다.

## Evidence of Completion

- 입력부터 출력까지 PE array와 buffer를 지나는 data path를 설명한다.
- 대표 dataflow가 어떤 data movement를 줄이는지 설명한다.
- 위 표시는 관련 Learning Log의 자기 설명·수정 이해에서 최소 evidence keyword가 모두 확인된 경우만 생성함

## Blocking Gaps

- 없음

## Optional Open Questions

- Stage 5의 memory wall은 지금까지 배운 NPU tiling/dataflow 최적화로도 왜 완전히 해결되지 않는가?
- PIM/CIM은 compute 위치를 memory 쪽으로 옮겨 data movement를 어떻게 바꾸는가?
- 명시적 deep-dive 요청 때 선택 가능한 범위: NoC routing; compiler scheduling; RTL 또는 cycle-accurate 구현

## Recommended Next Move

- Decision: **advance**
- 이유: 현재 exit criteria를 충족했으므로 optional question을 기본 경로에 넣지 않고 다음 Roadmap topic으로 이동한다.
- 우선 학습: Memory Wall과 PIM/CIM의 compute 위치 변화

## Required Source Before First Learning Unit

- `roadmap/LEARNING_BOUNDARIES.json`
- `learning-logs/2026/08/2026-08-22-npu-pe-array-systolic-tiling.md`
- `learning-logs/2026/08/2026-08-23-memory-wall-analog-cim-fundamentals.md`
- 이유: 다음 topic의 depth boundary를 확인한 뒤 새 학습을 시작한다.
- 이유: 최신 의미 있는 Learning Log를 최대 2개 읽어 최근 이해·오해 수정·다음 행동을 실제 evidence로 확인한다.
- 이 source를 읽기 전에는 일반 지식만으로 첫 설명이나 진단 질문을 만들지 않는다.

## Next Roadmap Topic

- Memory Wall과 PIM/CIM의 compute 위치 변화

## 현재 확인된 핵심 개념

- Memory Wall: compute 성능만 높여도 memory hierarchy를 통한 data movement가 latency/energy 병목으로 남을 수 있다.
- Weight-stationary CIM: weight를 memory array에 두고 activation을 공급하여 weight movement를 줄이는 방향이다.
- Analog CIM MAC: cell의 w×x에 해당하는 physical contribution을 current/charge/voltage 등의 analog quantity로 표현하고 bitline에서 accumulation할 수 있다.
- Multi-bit handling: positional weight 때문에 bit slicing/bit-serial 및 digital shift-and-add 등의 재구성이 필요할 수 있다.
- Activation buffer: 특별한 memory technology의 이름이라기보다 activation을 임시 저장하는 역할이며, accelerator에서는 SRAM으로 구현될 수 있다.
- Peripheral bottleneck: ADC, input driver/DAC, activation SRAM, interconnect, digital accumulation 등이 array 밖의 area/energy/throughput을 제한할 수 있다.
- Array scaling: 큰 WL/BL은 parasitic resistance/capacitance와 sensing/precision 문제를 키울 수 있어 array size를 무조건 확대할 수 없다.

## 미완료 자기 설명 점검

- 없음

## 최근 Learning Log의 다음 행동 (참고용)

- CIM tiling과 mapping을 학습한다.
- 큰 matrix를 여러 CIM array로 분할했을 때 발생하는 partial sum과 inter-array accumulation을 직접 계산한다.
- NPU tiling과 CIM tiling의 공통점과 차이를 capacity, data movement, circuit constraint 관점에서 비교한다.
- 위 항목은 source evidence이며 Roadmap-aware 추천보다 우선하지 않음

## Roadmap reconciliation

- Current Stage가 현재 depth boundary의 공식 stage와 일치하지 않음; 모든 exit criterion을 충족해 Roadmap에 정의된 다음 topic을 제안함; PIM / CIM에 학습 evidence가 있지만 dashboard 상태가 Not Started임
- `roadmap/PROGRESS.md`는 자동 수정하지 않음

## 제외한 기록과 이유

- `learning-logs/2026/08/2026-08-09-memory-hierarchy-data-reuse.md` — 필수 Metadata 누락: Document type, Domain, Roadmap stage

## 참고한 source paths

- `roadmap/ROADMAP.md`
- `roadmap/LEARNING_BOUNDARIES.json`
- `roadmap/PROGRESS.md`
- `learning-logs/2026/08/2026-08-22-npu-pe-array-systolic-tiling.md`
