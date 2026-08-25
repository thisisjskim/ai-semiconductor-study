# Current Learning Context

> 이 문서는 `learning-logs/**`와 roadmap에서 자동 생성한 derived/generated snapshot이다. Source of truth가 아니며 원본 기록을 다시 확인할 수 있다.

- Last generated date: 2026-08-24
- Progress source SHA: `d843c4f8a0d43bab3106144b486e14a5da56df34`

## Roadmap Position

- 최신 의미 있는 학습 기록: `learning-logs/2026/08/2026-08-24-pim-cim-tiling-roofline-foundations.md`
- Current Stage: Stage 5 — PIM / CIM
- Current Topic: 중심 Foundational Paper의 claim map과 architecture walkthrough
- Domain: pim-cim
- Depth Boundary: `paper-analysis-foundations`

### 같은 날짜의 의미 있는 학습 단위

- `learning-logs/2026/08/2026-08-24-pim-cim-tiling-roofline-foundations.md` — PIM/CIM Tiling, Bottleneck과 Roofline 기초

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
- `learning-logs/2026/08/2026-08-23-memory-wall-analog-cim-fundamentals.md`
- `learning-logs/2026/08/2026-08-24-pim-cim-tiling-roofline-foundations.md`
- 이유: 첫 Blocking Gap과 가장 가까운 저장 evidence를 확인해 사용자의 실제 설명 수준에 맞춘다.
- 이유: 최신 의미 있는 Learning Log를 최대 2개 읽어 최근 이해·오해 수정·다음 행동을 실제 evidence로 확인한다.
- 이 source를 읽기 전에는 일반 지식만으로 첫 설명이나 진단 질문을 만들지 않는다.

## Next Roadmap Topic

- 관련 논문 비교와 Research Portfolio

## 현재 확인된 핵심 개념

- CIM K-tiling과 reduction dimension
- Partial sum과 inter-array accumulation
- M/N tiling과 K-tiling의 차이
- CIM array size와 mapping capacity
- Bitline/wordline parasitic resistance와 capacitance
- I=C·dV/dt와 sensing latency 직관
- Analog CIM과 Digital CIM
- Multi-bit representation, bit-serial, bit-slicing, shift-and-add

## 미완료 자기 설명 점검

- 없음

## 최근 Learning Log의 다음 행동 (참고용)

- 중심 Foundational PIM/CIM 논문 한 편을 선정하고 abstract와 주요 architecture figure를 읽으면서 `problem → prior bottleneck → proposed compute location → data path → claimed benefit`의 claim map을 만든다.
- 논문의 주요 figure에서 weight, activation, partial sum, ADC/digital accumulation이 각각 어디에 위치하고 어떻게 이동하는지 직접 표시한다.
- 논문의 성능/에너지 결과를 읽을 때 array peak만 보지 않고 ADC/peripheral overhead, data movement, precision, utilization을 함께 확인하고, 가능하면 Arithmetic Intensity 또는 Roofline 관점으로 memory-bound/compute-bound 가능성을 추론한다.
- 위 항목은 source evidence이며 Roadmap-aware 추천보다 우선하지 않음

## 제외한 기록과 이유

- `learning-logs/2026/08/2026-08-09-memory-hierarchy-data-reuse.md` — 필수 Metadata 누락: Document type, Domain, Roadmap stage

## 참고한 source paths

- `roadmap/ROADMAP.md`
- `roadmap/LEARNING_BOUNDARIES.json`
- `roadmap/PROGRESS.md`
