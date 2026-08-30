# Current Learning Context

> 이 문서는 `learning-logs/**`, `paper-notes/**`와 roadmap에서 자동 생성한 derived/generated snapshot이다. Source of truth가 아니며 원본 기록을 다시 확인할 수 있다.

- Last generated date: 2026-08-30
- Progress source SHA: `e210eecd0f2e04363d42703a38a0dd1c4a921958`

## Roadmap Position

- 최신 의미 있는 학습 기록: `learning-logs/2026/08/2026-08-30-nvm-fundamentals.md`
- Current Boundary: `paper-analysis-foundations`
- Current Stage: Stage 6 — Foundational Papers
- Current Topic: 중심 Foundational Paper의 claim map과 architecture walkthrough
- Domain: pim-cim
- Depth Boundary: `paper-analysis-foundations`

### 같은 날짜의 의미 있는 학습 단위

- `learning-logs/2026/08/2026-08-30-nvm-fundamentals.md` — NVM Fundamentals — ReRAM, MRAM, PCM과 NVM-CIM

## Current Paper

- Current Paper Note: `paper-notes/foundational/2026-08-28-overview-of-cim-circuits-with-dram-and-nvm.md`

## Topic Goal

- 중심 논문의 problem, claim, architecture, evidence와 limitation을 연결해 설명한다.

## Minimum Required Understanding

- problem과 prior-work gap
- key claim
- architecture와 data path
- baseline, result, limitation

## Exit Criteria

- [ ] 논문의 problem, prior-work gap과 key claim을 자기 언어로 설명한다.
- [ ] 핵심 architecture와 result를 연결하고 limitation을 하나 이상 제시한다.

## Evidence of Completion

- Learning Log에서 자동 확인된 exit criterion이 없음
- 위 표시는 관련 Learning Log의 자기 설명·수정 이해에서 최소 evidence keyword가 모두 확인된 경우만 생성함

## Blocking Gaps

- 논문의 problem, prior-work gap과 key claim을 자기 언어로 설명한다.
- 핵심 architecture와 result를 연결하고 limitation을 하나 이상 제시한다.

## Optional Open Questions

- 없음
- 명시적 deep-dive 요청 때 선택 가능한 범위: 논문 전체 재현; 모든 수식 유도; 전문 전체 번역

## Recommended Next Move

- Decision: **continue**
- 이유: 현재 topic의 blocking gap이 둘 이상이므로 필요한 최소 범위만 계속 학습한다.
- 우선 학습: 논문의 problem, prior-work gap과 key claim을 자기 언어로 설명한다.

## Required Source Before First Learning Unit

- `roadmap/LEARNING_BOUNDARIES.json`
- `learning-logs/2026/08/2026-08-24-pim-cim-tiling-roofline-foundations.md`
- `learning-logs/2026/08/2026-08-30-nvm-fundamentals.md`
- 이유: 첫 Blocking Gap과 가장 가까운 저장 evidence를 확인해 사용자의 실제 설명 수준에 맞춘다.
- 이유: 최신 의미 있는 Learning Log를 최대 2개 읽어 최근 이해·오해 수정·다음 행동을 실제 evidence로 확인한다.
- 이 source를 읽기 전에는 일반 지식만으로 첫 설명이나 진단 질문을 만들지 않는다.

## Next Roadmap Topic

- 관련 논문 비교와 Research Portfolio

## 현재 확인된 핵심 개념

- NVM 공통 구조: physical state → resistance state → read current
- LRS / HRS와 Ohm's law 기반 current sensing
- ReRAM: MIM, metal oxide, conductive filament, SET/RESET
- MRAM: MTJ, fixed/free layer, parallel/antiparallel, spin-dependent tunneling, TMR 직관
- PCM: chalcogenide, crystalline/amorphous, Joule heating, crystallization, melting, quenching
- Conductance: G=1/R
- NVM-CIM multiplication: I=VG
- Column current summation과 MAC

## 미완료 자기 설명 점검

- 없음

## 최근 Learning Log의 다음 행동 (참고용)

- 현재 읽고 있는 overview 논문의 Section III NVM-CIM으로 복귀해 NVM의 non-volatility, density, current-based computing advantage와 각 기술의 circuit-level trade-off를 user-first 방식으로 읽는다.
- 논문에서 low signal margin, nonlinearity, variation이 실제 architecture에서 어떻게 나타나고 어떤 circuit technique으로 완화되는지 연결한다.
- 이 Learning Log가 저장된 뒤 현재 Paper Note의 prerequisite bridge에 연결할지 별도 checkpoint로 결정한다.
- 위 항목은 source evidence이며 Roadmap-aware 추천보다 우선하지 않음

## 제외한 기록과 이유

- `learning-logs/2026/08/2026-08-09-memory-hierarchy-data-reuse.md` — 필수 Metadata 누락: Document type, Domain, Roadmap stage
- `learning-logs/2026/08/2026-08-25-learning-log-pipeline-e2e.md` — Domain이 research-os인 시스템 개발·운영 기록

## 참고한 source paths

- `roadmap/ROADMAP.md`
- `roadmap/LEARNING_BOUNDARIES.json`
- `roadmap/PROGRESS.md`
