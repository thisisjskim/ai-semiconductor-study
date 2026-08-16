# Current Learning Context

> 이 문서는 `learning-logs/**`와 roadmap에서 자동 생성한 derived/generated snapshot이다. Source of truth가 아니며 원본 기록을 다시 확인할 수 있다.

- Last generated date: 2026-08-15
- Roadmap reconciliation: **aligned**

## 현재 상태

- 최신 의미 있는 학습 기록: `learning-logs/2026/08/2026-08-15-sram-cell-ratio-snm.md`
- Current Topic: SRAM Cell Ratio와 SNM
- Domain: sram
- Roadmap stage: Stage 3 — Memory

### 같은 날짜의 의미 있는 학습 단위

- `learning-logs/2026/08/2026-08-15-sram-cell-ratio-snm.md` — SRAM Cell Ratio와 SNM

## 현재 확인된 핵심 개념

- 6T SRAM Read Disturb
- Cell Ratio
- Pull-down NMOS와 Access NMOS의 strength 경쟁
- Pull-up PMOS와 Access NMOS의 Write 경쟁
- 대표적인 transistor sizing 방향
- MOSFET threshold voltage (Vth)
- CMOS inverter switching threshold (VM)
- Cross-coupled inverter positive feedback

## 아직 해결되지 않은 질문

- Sense Amplifier는 BL과 BL̅ 사이의 작은 differential voltage를 어떻게 증폭하는가?
- Differential sensing은 single-ended sensing에 비해 왜 유리한가?
- Read Margin과 SNM은 실제 회로 시뮬레이션과 측정에서 어떻게 구분되고 연결되는가?
- Process Variation과 Monte Carlo 분석은 SNM 분포를 어떻게 변화시키는가?

## 미완료 자기 설명 점검

- 없음

## 바로 다음 행동

- Sense Amplifier가 precharged BL/BL̅의 작은 differential voltage를 증폭하는 원리를 학습한다.
- Differential sensing과 precharge가 Read latency와 noise immunity에 주는 이점을 설명한다.
- 이후 Read Margin과 SNM을 연결하고 Process Variation에 따른 SNM 분포로 확장한다.

## Roadmap reconciliation

- 최신 Learning Log와 dashboard의 현재 stage/topic에 명백한 충돌이 없음
- `roadmap/PROGRESS.md`는 자동 수정하지 않음

## 제외한 기록과 이유

- `learning-logs/2026/08/2026-08-09-memory-hierarchy-data-reuse.md` — 필수 Metadata 누락: Document type, Domain, Roadmap stage

## 참고한 source paths

- `roadmap/ROADMAP.md`
- `roadmap/PROGRESS.md`
- `learning-logs/2026/08/2026-08-15-sram-cell-ratio-snm.md`
