# Current Learning Context

> 이 문서는 `learning-logs/**`와 roadmap에서 자동 생성한 derived/generated snapshot이다. Source of truth가 아니며 원본 기록을 다시 확인할 수 있다.

- Last generated date: 2026-08-22
- Progress source SHA: `3df019f079517bfd210035c89773c01339a6daad`
- Roadmap reconciliation: **pending-approval**

## Roadmap Position

- 최신 의미 있는 학습 기록: `learning-logs/2026/08/2026-08-22-npu-pe-array-systolic-tiling.md`
- Current Stage: Stage 3 — Memory
- Current Topic: NPU PE array, buffer hierarchy와 dataflow
- Domain: npu
- Depth Boundary: `npu-architecture-foundations`

### 같은 날짜의 의미 있는 학습 단위

- `learning-logs/2026/08/2026-08-22-sram-dram-sense-amplifier.md` — SRAM-DRAM 구조 비교와 DRAM Sense Amplifier
- `learning-logs/2026/08/2026-08-22-npu-sram-data-reuse-dataflow.md` — NPU SRAM Data Reuse와 Dataflow
- `learning-logs/2026/08/2026-08-22-npu-pe-array-systolic-tiling.md` — NPU PE Array, Systolic Array와 Matrix Tiling

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
- `learning-logs/2026/08/2026-08-22-npu-sram-data-reuse-dataflow.md`
- `learning-logs/2026/08/2026-08-22-npu-pe-array-systolic-tiling.md`
- 이유: 다음 topic의 depth boundary를 확인한 뒤 새 학습을 시작한다.
- 이유: 최신 의미 있는 Learning Log를 최대 2개 읽어 최근 이해·오해 수정·다음 행동을 실제 evidence로 확인한다.
- 이 source를 읽기 전에는 일반 지식만으로 첫 설명이나 진단 질문을 만들지 않는다.

## Next Roadmap Topic

- Memory Wall과 PIM/CIM의 compute 위치 변화

## 현재 확인된 핵심 개념

- PE와 PE array
- Global SRAM buffer와 PE local register
- SRAM bandwidth와 PE-to-PE interconnect
- Pipeline과 parallelism
- Latency와 throughput
- PE utilization과 memory-bound
- Systolic array와 local data reuse
- CPU/GPU/NPU specialization

## 미완료 자기 설명 점검

- 없음

## 최근 Learning Log의 다음 행동 (참고용)

- Stage 5에서 memory wall을 NPU의 off-chip data movement와 연결해 학습한다.
- 기존 NPU의 compute-centric data movement와 PIM/CIM의 compute-location 변화를 비교한다.
- PIM/CIM이 줄이는 movement와 새로 만드는 circuit/architecture trade-off를 자기 설명으로 검증한다.
- 위 항목은 source evidence이며 Roadmap-aware 추천보다 우선하지 않음

## Roadmap reconciliation

- Current Stage가 현재 depth boundary의 공식 stage와 일치하지 않음; 모든 exit criterion을 충족해 Roadmap에 정의된 다음 topic을 제안함
- `roadmap/PROGRESS.md`는 자동 수정하지 않음

## 제외한 기록과 이유

- `learning-logs/2026/08/2026-08-09-memory-hierarchy-data-reuse.md` — 필수 Metadata 누락: Document type, Domain, Roadmap stage

## 참고한 source paths

- `roadmap/ROADMAP.md`
- `roadmap/LEARNING_BOUNDARIES.json`
- `roadmap/PROGRESS.md`
- `learning-logs/2026/08/2026-08-22-npu-pe-array-systolic-tiling.md`
