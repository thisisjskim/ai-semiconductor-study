# Current Learning Context

> 이 문서는 `learning-logs/**`와 roadmap에서 자동 생성한 derived/generated snapshot이다. Source of truth가 아니며 원본 기록을 다시 확인할 수 있다.

- Last generated date: 2026-08-24
- Progress source SHA: `40fb5174cae68a5a1674410e483354292d6c5afa`
- Roadmap reconciliation: **pending-approval**

## Roadmap Position

- 최신 의미 있는 학습 기록: `learning-logs/2026/08/2026-08-24-pim-cim-tiling-roofline-foundations.md`
- Current Stage: Stage 4 — NPU Architecture
- Current Topic: Memory Wall과 PIM/CIM의 compute 위치 변화
- Domain: pim-cim
- Depth Boundary: `pim-cim-foundations`

### 같은 날짜의 의미 있는 학습 단위

- `learning-logs/2026/08/2026-08-24-pim-cim-tiling-roofline-foundations.md` — PIM/CIM Tiling, Bottleneck과 Roofline 기초

## Topic Goal

- 기존 NPU와 PIM/CIM의 data movement 차이와 핵심 trade-off를 설명한다.

## Minimum Required Understanding

- Memory Wall
- SRAM-CIM과 DRAM-PIM
- Digital CIM과 Analog CIM
- precision, energy, area trade-off

## Exit Criteria

- [x] 기존 NPU와 PIM/CIM의 compute 위치와 data movement 차이를 설명한다.
- [x] SRAM-CIM 또는 DRAM-PIM의 이점과 비용을 하나 이상 비교한다.

## Evidence of Completion

- 기존 NPU와 PIM/CIM의 compute 위치와 data movement 차이를 설명한다.
- SRAM-CIM 또는 DRAM-PIM의 이점과 비용을 하나 이상 비교한다.
- 위 표시는 관련 Learning Log의 자기 설명·수정 이해에서 최소 evidence keyword가 모두 확인된 경우만 생성함

## Blocking Gaps

- 없음

## Optional Open Questions

- 실제 Foundational PIM/CIM 논문에서 architecture block diagram을 볼 때 어떤 subsystem이 measured bottleneck인지 어떻게 찾아낼 것인가?
- 실제 논문의 compute efficiency, energy efficiency, ADC overhead, data reuse를 Roofline 또는 유사한 quantitative framework로 어떻게 해석할 것인가?
- Digital CIM과 Analog CIM을 실제 silicon result로 비교할 때 precision, area, TOPS/W, TOPS/mm²를 어떤 기준으로 공정하게 비교해야 하는가?
- 명시적 deep-dive 요청 때 선택 가능한 범위: ADC/DAC transistor-level circuit; device nonlinearity model; 고급 mapping algorithm

## Recommended Next Move

- Decision: **advance**
- 이유: 현재 exit criteria를 충족했으므로 optional question을 기본 경로에 넣지 않고 다음 Roadmap topic으로 이동한다.
- 우선 학습: 중심 Foundational Paper의 claim map과 architecture walkthrough

## Required Source Before First Learning Unit

- `roadmap/LEARNING_BOUNDARIES.json`
- `learning-logs/2026/08/2026-08-23-memory-wall-analog-cim-fundamentals.md`
- `learning-logs/2026/08/2026-08-24-pim-cim-tiling-roofline-foundations.md`
- 이유: 다음 topic의 depth boundary를 확인한 뒤 새 학습을 시작한다.
- 이유: 최신 의미 있는 Learning Log를 최대 2개 읽어 최근 이해·오해 수정·다음 행동을 실제 evidence로 확인한다.
- 이 source를 읽기 전에는 일반 지식만으로 첫 설명이나 진단 질문을 만들지 않는다.

## Next Roadmap Topic

- 중심 Foundational Paper의 claim map과 architecture walkthrough

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

## Roadmap reconciliation

- Current Stage가 현재 depth boundary의 공식 stage와 일치하지 않음; 모든 exit criterion을 충족해 Roadmap에 정의된 다음 topic을 제안함
- `roadmap/PROGRESS.md`는 자동 수정하지 않음

## 제외한 기록과 이유

- `learning-logs/2026/08/2026-08-09-memory-hierarchy-data-reuse.md` — 필수 Metadata 누락: Document type, Domain, Roadmap stage

## 참고한 source paths

- `roadmap/ROADMAP.md`
- `roadmap/LEARNING_BOUNDARIES.json`
- `roadmap/PROGRESS.md`
- `learning-logs/2026/08/2026-08-23-memory-wall-analog-cim-fundamentals.md`
- `learning-logs/2026/08/2026-08-24-pim-cim-tiling-roofline-foundations.md`
