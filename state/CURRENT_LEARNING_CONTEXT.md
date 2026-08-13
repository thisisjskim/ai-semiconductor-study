# Current Learning Context

> 이 문서는 `learning-logs/**`와 roadmap에서 자동 생성한 derived/generated snapshot이다. Source of truth가 아니며 원본 기록을 다시 확인할 수 있다.

- Last generated date: 2026-08-12
- Roadmap reconciliation: **aligned**

## 현재 상태

- 최신 의미 있는 학습 기록: `learning-logs/2026/08/2026-08-12-register-sram-circuits.md`
- Current Topic: Register와 SRAM 회로 기초
- Domain: sram
- Roadmap stage: Stage 3 — Memory

### 같은 날짜의 의미 있는 학습 단위

- `learning-logs/2026/08/2026-08-12-register-sram-circuits.md` — Register와 SRAM 회로 기초

## 현재 확인된 핵심 개념

- Register는 작은 working set을 compute 가까이에 두어 latency와 data movement를 줄인다.
- Register의 높은 bit당 circuit/area cost 때문에 대용량 storage에는 SRAM이 더 적합하다.
- Cross-coupled inverter는 feedback을 통해 두 stable voltage states를 유지한다.
- Latch는 level-sensitive하고, edge-triggered flip-flop은 특정 clock edge의 input을 capture한다.
- Multi-bit Register는 여러 1-bit storage element가 common clock에 맞춰 병렬로 동작하는 구조로 볼 수 있다.
- Transistor는 logic gate 자체가 아니라 logic gate와 storage circuit을 구성하는 physical switching device이다.
- CMOS inverter 하나는 대표적으로 PMOS 1개와 NMOS 1개로 구성된다.
- 6T SRAM은 4T cross-coupled inverter storage core와 2T access transistor로 구성된다.

## 아직 해결되지 않은 질문

- CMOS inverter에서 input이 0→1 또는 1→0으로 변할 때 output node의 charge가 실제로 어떤 경로로 이동하며 charge/discharge되는가?
- Pull-up/Pull-down network를 current, charge, node capacitance 관점에서 어떻게 완전히 연결해 설명할 수 있는가?
- 6T SRAM에서 Hold, Write, Read가 WL, BL/BL̅, Q/Q̅와 각 transistor의 동작으로 구체적으로 어떻게 구현되는가?
- 6T SRAM Read 과정에서 cell stability와 read disturb는 왜 발생하는가?

## 미완료 자기 설명 점검

- CMOS inverter의 switching을 current, charge, node capacitance 관점에서 완전히 설명할 수 있다.
- 6T SRAM의 Hold/Write/Read 동작을 transistor-level에서 설명할 수 있다.
- SRAM의 read disturb와 cell stability를 설명할 수 있다.

## 바로 다음 행동

- 현재 학습 중인 6T SRAM 블로그의 흐름을 주교재로 삼고, 다음 순서로 이어간다.
- MOSFET switch 관점 복습을 마무리한다.
- CMOS inverter에서 PMOS/NMOS에 의한 output node charge/discharge 과정을 current/charge 관점에서 설명한다.
- Pull-Up Network와 Pull-Down Network를 CMOS inverter 회로에서 확실히 구분한다.
- Cross-coupled inverter가 1 bit state를 유지하는 과정을 다시 연결한다.
- 6T SRAM의 Hold → Write → Read 동작을 WL, BL/BL̅, Q/Q̅ 기준으로 분석한다.

## Roadmap reconciliation

- 최신 Learning Log와 dashboard의 현재 stage/topic에 명백한 충돌이 없음
- `roadmap/PROGRESS.md`는 자동 수정하지 않음

## 제외한 기록과 이유

- `learning-logs/2026/08/2026-08-09-memory-hierarchy-data-reuse.md` — 필수 Metadata 누락: Document type, Domain, Roadmap stage

## 참고한 source paths

- `roadmap/ROADMAP.md`
- `roadmap/PROGRESS.md`
- `learning-logs/2026/08/2026-08-12-register-sram-circuits.md`
