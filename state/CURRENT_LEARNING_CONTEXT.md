# Current Learning Context

> 이 문서는 `learning-logs/**`와 roadmap에서 자동 생성한 derived/generated snapshot이다. Source of truth가 아니며 원본 기록을 다시 확인할 수 있다.

- Last generated date: 2026-08-15
- Roadmap reconciliation: **aligned**

## Roadmap Position

- 최신 의미 있는 학습 기록: `learning-logs/2026/08/2026-08-15-sram-read-path-fundamentals.md`
- Current Stage: Stage 3 — Memory
- Current Topic: Register와 SRAM 회로 기초
- Domain: sram
- Depth Boundary: `sram-foundations`

### 같은 날짜의 의미 있는 학습 단위

- `learning-logs/2026/08/2026-08-15-sram-cell-ratio-snm.md` — SRAM Cell Ratio와 SNM
- `learning-logs/2026/08/2026-08-15-sram-read-path-fundamentals.md` — SRAM Read Path Fundamentals

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

- 6T SRAM Read Disturb
- Cell Ratio와 transistor sizing
- Pull-down NMOS vs Access NMOS
- Access NMOS vs Pull-up PMOS
- MOSFET threshold voltage (Vth)
- CMOS inverter switching threshold (VM)
- Static Noise Margin (SNM)
- Hold SNM vs Read SNM

## 미완료 자기 설명 점검

- AI 반도체에서 왜 중요한지 설명할 수 있다.

## 최근 Learning Log의 다음 행동 (참고용)

- SRAM Write Path를 학습하고 1→0 pull-down과 positive feedback에 의한 state flip 과정을 설명한다.
- Write Margin과 Write Failure를 transistor strength 관점에서 이해한다.
- 이후 Process Variation, Monte Carlo, SNM/Offset distribution과 SRAM yield로 확장한다.
- 위 항목은 source evidence이며 Roadmap-aware 추천보다 우선하지 않음

## Roadmap reconciliation

- 현재 stage/topic과 dashboard가 Roadmap boundary 및 Learning Log evidence와 일치함; 학습 이동 판단은 review_then_advance이며 공식 topic 변경은 아직 필요하지 않음
- `roadmap/PROGRESS.md`는 자동 수정하지 않음

## 제외한 기록과 이유

- `learning-logs/2026/08/2026-08-09-memory-hierarchy-data-reuse.md` — 필수 Metadata 누락: Document type, Domain, Roadmap stage
- `learning-logs/2026/08/2026-08-22-sram-dram-sense-amplifier.md` — AI semiconductor 학습 domain이 아님: memory

## 참고한 source paths

- `roadmap/ROADMAP.md`
- `roadmap/LEARNING_BOUNDARIES.json`
- `roadmap/PROGRESS.md`
- `learning-logs/2026/08/2026-08-12-register-sram-circuits.md`
- `learning-logs/2026/08/2026-08-14-sram-read-disturb-cell-stability.md`
- `learning-logs/2026/08/2026-08-15-sram-cell-ratio-snm.md`
- `learning-logs/2026/08/2026-08-15-sram-read-path-fundamentals.md`
