# Current Learning Context

> 이 문서는 `learning-logs/**`와 roadmap에서 자동 생성한 derived/generated snapshot이다. Source of truth가 아니며 원본 기록을 다시 확인할 수 있다.

- Last generated date: 2026-08-16
- Roadmap reconciliation: **aligned**

## 현재 상태

- 최신 의미 있는 학습 기록: `learning-logs/2026/08/2026-08-16-sram-read-path-fundamentals.md`
- Current Topic: SRAM Read Path Fundamentals
- Domain: sram
- Roadmap stage: Stage 3 — Memory

### 같은 날짜의 의미 있는 학습 단위

- `learning-logs/2026/08/2026-08-16-sram-read-path-fundamentals.md` — SRAM Read Path Fundamentals

## 현재 확인된 핵심 개념

- 6T SRAM Read Disturb
- Cell Ratio와 transistor sizing
- Pull-down NMOS vs Access NMOS
- Access NMOS vs Pull-up PMOS
- MOSFET threshold voltage (Vth)
- CMOS inverter switching threshold (VM)
- Static Noise Margin (SNM)
- Hold SNM vs Read SNM

## 아직 해결되지 않은 질문

- SRAM Write Path에서 실제 state flip은 어떤 node의 pull-down을 기점으로 시작되는가?
- Write Margin은 어떤 방식으로 정의하고 측정하는가?
- Write Failure와 Write Assist 기법은 Cell Ratio 및 Pull-up Ratio와 어떻게 연결되는가?
- Process Variation과 Monte Carlo 분석에서 SNM 및 Sense Amp Offset 분포를 어떻게 해석하는가?

## 미완료 자기 설명 점검

- AI 반도체에서 왜 중요한지 설명할 수 있다.

## 바로 다음 행동

- SRAM Write Path를 학습하고 1→0 pull-down과 positive feedback에 의한 state flip 과정을 설명한다.
- Write Margin과 Write Failure를 transistor strength 관점에서 이해한다.
- 이후 Process Variation, Monte Carlo, SNM/Offset distribution과 SRAM yield로 확장한다.

## Roadmap reconciliation

- 최신 Learning Log와 dashboard의 현재 stage/topic에 명백한 충돌이 없음
- `roadmap/PROGRESS.md`는 자동 수정하지 않음

## 제외한 기록과 이유

- `learning-logs/2026/08/2026-08-09-memory-hierarchy-data-reuse.md` — 필수 Metadata 누락: Document type, Domain, Roadmap stage

## 참고한 source paths

- `roadmap/ROADMAP.md`
- `roadmap/PROGRESS.md`
- `learning-logs/2026/08/2026-08-16-sram-read-path-fundamentals.md`
