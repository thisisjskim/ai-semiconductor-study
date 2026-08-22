# Current Learning Context

> 이 문서는 `learning-logs/**`와 roadmap에서 자동 생성한 derived/generated snapshot이다. Source of truth가 아니며 원본 기록을 다시 확인할 수 있다.

- Last generated date: 2026-08-22
- Roadmap reconciliation: **pending-approval**

## Roadmap Position

- 최신 의미 있는 학습 기록: `learning-logs/2026/08/2026-08-22-sram-dram-sense-amplifier.md`
- Current Stage: Stage 3 — Memory
- Current Topic: Register와 SRAM 회로 기초
- Domain: memory-architecture
- Depth Boundary: `sram-foundations`

### 같은 날짜의 의미 있는 학습 단위

- `learning-logs/2026/08/2026-08-22-npu-pe-array-systolic-tiling.md` — NPU PE Array, Systolic Array와 Matrix Tiling
- `learning-logs/2026/08/2026-08-22-npu-sram-data-reuse-dataflow.md` — NPU SRAM Data Reuse와 Dataflow
- `learning-logs/2026/08/2026-08-22-sram-dram-sense-amplifier.md` — SRAM-DRAM 구조 비교와 DRAM Sense Amplifier

## Topic Goal

- 6T SRAM의 기본 read/write 동작과 안정성을 이해하고 memory architecture에서 SRAM의 역할을 설명한다.

## Minimum Required Understanding

- 6T SRAM과 cross-coupled inverter 구조
- WL, BL/BL̅, Q/Q̅ 기준의 Hold, Write, Read
- Read Disturb와 Cell Ratio의 관계
- Register와 DRAM 사이에서 SRAM이 맡는 역할

## Exit Criteria

- [x] 6T SRAM과 cross-coupled inverter의 저장 구조를 설명한다.
- [x] WL, BL/BL̅, Q/Q̅를 사용해 Hold, Write, Read의 기본 동작을 설명한다.
- [x] Read Disturb와 Cell Ratio가 read stability에 미치는 관계를 설명한다.
- [x] Register와 DRAM 사이에서 SRAM이 맡는 memory 역할을 설명한다.

## Evidence of Completion

- 6T SRAM과 cross-coupled inverter의 저장 구조를 설명한다.
- WL, BL/BL̅, Q/Q̅를 사용해 Hold, Write, Read의 기본 동작을 설명한다.
- Read Disturb와 Cell Ratio가 read stability에 미치는 관계를 설명한다.
- Register와 DRAM 사이에서 SRAM이 맡는 memory 역할을 설명한다.
- 위 표시는 관련 Learning Log의 자기 설명·수정 이해에서 최소 evidence keyword가 모두 확인된 경우만 생성함

## Blocking Gaps

- 없음

## Optional Open Questions

- Stage 4에서 실제 NPU PE array와 buffer hierarchy를 통해 Weight/Output/Activation reuse가 어떻게 mapping되는가?
- 대표 dataflow가 실제 tensor/matrix tile을 PE array에 어떻게 배치하는가?
- 지금까지의 SRAM/DRAM circuit-level 차이가 NPU on-chip SRAM buffer의 data reuse, memory bandwidth, energy와 구체적으로 어떻게 연결되는가?
- NPU의 실제 SRAM buffer hierarchy와 tiling/dataflow는 DRAM traffic을 어떻게 줄이는가?
- 명시적 deep-dive 요청 때 선택 가능한 범위: 상세 SNM extraction; advanced Sense Amplifier circuit; SRAM assist technique; process variation과 Monte Carlo 분석

## Recommended Next Move

- Decision: **advance**
- 이유: 현재 exit criteria를 충족했으므로 optional question을 기본 경로에 넣지 않고 다음 Roadmap topic으로 이동한다.
- 우선 학습: SRAM과 DRAM의 구조·역할 비교 및 NPU on-chip buffer 연결

## Required Source Before First Learning Unit

- `roadmap/LEARNING_BOUNDARIES.json`
- 이유: 다음 topic의 depth boundary를 확인한 뒤 새 학습을 시작한다.
- 이 source를 읽기 전에는 일반 지식만으로 첫 설명이나 진단 질문을 만들지 않는다.

## Next Roadmap Topic

- SRAM과 DRAM의 구조·역할 비교 및 NPU on-chip buffer 연결

## 현재 확인된 핵심 개념

- Register → SRAM → DRAM memory hierarchy와 capacity/latency/area trade-off
- SRAM 6T와 DRAM 1T1C
- DRAM charge leakage, retention, refresh
- Charge sharing과 destructive read
- VDD/2 precharge와 differential sensing
- Cross-coupled regenerative sense amplifier
- Sense → Amplify → Restore
- Sense amplifier mismatch/offset과 sensing margin

## 미완료 자기 설명 점검

- 없음

## 최근 Learning Log의 다음 행동 (참고용)

- NPU on-chip SRAM buffer가 activation, weight, partial sum의 data reuse를 어떻게 지원하는지 학습한다.
- SRAM capacity와 tiling이 DRAM traffic 및 memory bandwidth 요구량에 미치는 영향을 연결한다.
- 이후 data movement energy와 compute utilization 관점에서 memory hierarchy를 분석한다.
- 위 항목은 source evidence이며 Roadmap-aware 추천보다 우선하지 않음

## Roadmap reconciliation

- 모든 exit criterion을 충족해 Roadmap에 정의된 다음 topic을 제안함; NPU Architecture에 학습 evidence가 있지만 dashboard 상태가 Not Started임
- `roadmap/PROGRESS.md`는 자동 수정하지 않음

## 제외한 기록과 이유

- `learning-logs/2026/08/2026-08-09-memory-hierarchy-data-reuse.md` — 필수 Metadata 누락: Document type, Domain, Roadmap stage

## 참고한 source paths

- `roadmap/ROADMAP.md`
- `roadmap/LEARNING_BOUNDARIES.json`
- `roadmap/PROGRESS.md`
- `learning-logs/2026/08/2026-08-12-register-sram-circuits.md`
- `learning-logs/2026/08/2026-08-14-sram-read-disturb-cell-stability.md`
- `learning-logs/2026/08/2026-08-15-sram-cell-ratio-snm.md`
- `learning-logs/2026/08/2026-08-15-sram-read-path-fundamentals.md`
- `learning-logs/2026/08/2026-08-22-npu-sram-data-reuse-dataflow.md`
- `learning-logs/2026/08/2026-08-22-sram-dram-sense-amplifier.md`
