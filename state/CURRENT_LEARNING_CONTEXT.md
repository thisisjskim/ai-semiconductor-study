# Current Learning Context

> 이 문서는 `learning-logs/**`와 roadmap에서 자동 생성한 derived/generated snapshot이다. Source of truth가 아니며 원본 기록을 다시 확인할 수 있다.

- Last generated date: 2026-08-22
- Roadmap reconciliation: **aligned**

## Roadmap Position

- 최신 의미 있는 학습 기록: `learning-logs/2026/08/2026-08-22-sram-dram-sense-amplifier.md`
- Current Stage: Stage 3 — Memory
- Current Topic: Register와 SRAM 회로 기초
- Domain: memory-architecture
- Depth Boundary: `sram-foundations`

### 같은 날짜의 의미 있는 학습 단위

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
- [ ] Register와 DRAM 사이에서 SRAM이 맡는 memory 역할을 설명한다.

## Evidence of Completion

- 6T SRAM과 cross-coupled inverter의 저장 구조를 설명한다.
- WL, BL/BL̅, Q/Q̅를 사용해 Hold, Write, Read의 기본 동작을 설명한다.
- Read Disturb와 Cell Ratio가 read stability에 미치는 관계를 설명한다.
- 위 표시는 관련 Learning Log의 자기 설명·수정 이해에서 최소 evidence keyword가 모두 확인된 경우만 생성함

## Blocking Gaps

- Register와 DRAM 사이에서 SRAM이 맡는 memory 역할을 설명한다.

## Optional Open Questions

- Sense Amplifier는 BL과 BL̅ 사이의 작은 differential voltage를 어떻게 증폭하는가?
- Differential sensing은 single-ended sensing에 비해 왜 유리한가?
- Read Margin과 SNM은 실제 회로 시뮬레이션과 측정에서 어떻게 구분되고 연결되는가?
- Process Variation과 Monte Carlo 분석은 SNM 분포를 어떻게 변화시키는가?
- SRAM Write Path에서 실제 state flip은 어떤 node의 pull-down을 기점으로 시작되는가?
- Write Margin은 어떤 방식으로 정의하고 측정하는가?
- 명시적 deep-dive 요청 때 선택 가능한 범위: 상세 SNM extraction; advanced Sense Amplifier circuit; SRAM assist technique; process variation과 Monte Carlo 분석

## Recommended Next Move

- Decision: **review_then_advance**
- 이유: blocking gap 하나만 짧게 확인한 뒤 다음 Roadmap topic으로 이동한다.
- 우선 학습: Register와 DRAM 사이에서 SRAM이 맡는 memory 역할을 설명한다.

## Required Source Before First Learning Unit

- `learning-logs/2026/08/2026-08-12-register-sram-circuits.md`
- 이유: 첫 Blocking Gap과 가장 가까운 저장 evidence를 확인해 사용자의 실제 설명 수준에 맞춘다.
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

- 현재 stage/topic과 dashboard가 Roadmap boundary 및 Learning Log evidence와 일치함; 학습 이동 판단은 review_then_advance이며 공식 topic 변경은 아직 필요하지 않음
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
