# AI Semiconductor Research Progress

이 문서는 2026년 9월 말~10월 초 KAIST SSL Lab 교수 연락과 2027년 겨울학기 개별연구 지원을 준비하기 위한 현재 계기판이다. 장기 방향과 완료 기준은 `roadmap/ROADMAP.md`, 실제 학습 근거는 `learning-logs/**`와 관련 정제 문서에 있다.

## 1. Target Snapshot

- Primary Goal: KAIST SSL Lab 개별연구 참여와 AI 반도체 대학원 진학을 위한 연구 포트폴리오 구축
- Application Target: 2027년 겨울학기 KAIST SSL Lab 개별연구
- Target Contact Window: 2026-09-28 ~ 2026-10-04
- Weekly Study Capacity: 주 10시간 이상, 약 90분 단위 세션
- Must-have Deliverables: 중심 Paper Note 1개, 관련 논문 1~2편 비교 자료, 핵심 기초 evidence, 연구 관심 정리, CV와 교수 연락 이메일 초안
- Stretch Deliverable: 논문과 연결된 작은 Python simulation 또는 분석 프로젝트

## 2. Status Definition

- **Not Started**: 현재 목표 기준의 의미 있는 evidence가 없음
- **Learning**: 설명, 질문, 분석 등 진행 중인 evidence가 있음
- **Review**: 핵심 범위의 1차 학습을 마치고 자기 설명·비교·비판을 점검 중
- **Completed**: 현재 목표의 exit gate를 충족해 다음 단계에서 사용할 수 있음

> Completed는 영구 숙련을 뜻하지 않는다. 논문에서 새로운 prerequisite gap이 발견되면 Learning 또는 Review로 돌아갈 수 있다.

## 3. Current Focus

- Execution Phase: Phase 2 — NPU and Dataflow Foundation
- Active Track: Track A — Essential Foundations → Foundational Paper transition
- Current Stage: Stage 5 — PIM / CIM foundations completed; paper-analysis transition
- Current Topic: 중심 Foundational PIM/CIM Paper의 claim map과 architecture walkthrough
- Current Deliverable: 중심 논문 1편의 `problem → bottleneck → proposed architecture → data path → claimed benefit` claim map
- Current Bottleneck: 기초 개념 자체보다 실제 논문 figure와 measured result에서 system-level bottleneck을 찾아내는 분석 경험 부족
- Next Milestone: 중심 Foundational Paper 선정 후 abstract와 주요 architecture figure를 자기 말로 설명하고 claim map 작성
- Phase Deadline: 2026-09-06
- Last Updated: 2026-08-24

## 4. Progress Dashboard

| Stage | Status | 현재 목표 | Evidence / Notes |
| --- | --- | --- | --- |
| 전자공학 기초 (Electronics Fundamentals) | Learning | 논문 이해에 필요한 MOSFET/CMOS/circuit prerequisite를 필요 시 spiral review | 기존 SRAM/circuit Learning Log |
| AI Computation | Learning | MAC, weight, activation, partial sum과 data reuse를 accelerator 관점에서 설명 | NPU/PIM 학습에서 반복 적용 |
| Computer Architecture | Learning | latency, throughput, utilization, locality, bottleneck을 accelerator에 적용 | NPU/CIM bottleneck reasoning evidence 확보 |
| Memory Architecture | Review | hierarchy, data movement, reuse와 bandwidth의 관계를 architecture에 적용 | SRAM/DRAM/NPU/PIM Learning Logs |
| SRAM / DRAM / eDRAM | Review | 구조·동작 차이를 NPU buffer 및 PIM/CIM compute location과 연결 | 기존 SRAM/DRAM 학습 기록 |
| NPU Architecture | Review | PE array, tiling, dataflow, memory-bound reasoning을 논문 분석에 적용 | `learning-logs/2026/08/2026-08-22-npu-pe-array-systolic-tiling.md` |
| PIM / CIM | Completed | NPU와 PIM/CIM의 data movement 차이, CIM tiling, ADC/activation bottleneck, analog/digital trade-off 설명 | `learning-logs/2026/08/2026-08-23-memory-wall-analog-cim-fundamentals.md`, `learning-logs/2026/08/2026-08-24-pim-cim-tiling-roofline-foundations.md` |
| Foundational Papers | Learning | 중심 논문의 claim과 architecture 분석 훈련 | 다음 활성 학습 단위 |
| KAIST SSL Lab Papers | Not Started | SSL Lab 중심 논문 1편과 관련 논문 1~2편 분석 | Foundational Paper 분석 후 연결 |
| Research Questions / Portfolio | Not Started | Paper Note, 비교표, 연구 관심과 지원 자료 연결 | 중심 논문 분석 결과부터 축적 |

## 5. Application Deliverables

| Deliverable | Status | Target | Evidence / Next Action |
| --- | --- | --- | --- |
| 핵심 기초 Learning Log | Review | 2026-09-20까지 지원에 필요한 핵심 evidence 선별 | NPU/PIM-CIM foundations까지 evidence 확보; 논문 prerequisite gap만 spiral 보충 |
| 중심 논문 선정 | Learning | 즉시 | PIM/CIM Foundational Paper 후보를 확인하고 1편을 anchor로 선택 |
| 중심 Paper Note | Not Started | 2026-09-20 초안, 2026-09-27 검토 | claim map과 architecture walkthrough 후 `templates/paper-note.md` 사용 |
| 관련 논문 비교 자료 | Not Started | 2026-09-27 | 중심 논문과 1~2편을 problem, architecture, result, limitation으로 비교 |
| 연구 관심 정리 | Learning | 2026-09-27 | Memory Wall, data movement, PIM/CIM bottleneck에 대한 현재 관심을 논문 질문으로 구체화 |
| GitHub 포트폴리오 안내 | Not Started | 2026-09-30 | 교수에게 보여줄 핵심 문서와 읽는 순서를 안내 |
| CV 초안 | Not Started | 2026-09-27 | 학업 배경, 관심 분야, 분석 결과와 프로젝트 후보 연결 |
| 교수 연락 이메일 | Not Started | 2026-09-30 | 관심 이유, 준비 evidence, 문의 목적을 간결하게 작성 |
| Python simulation / 분석 프로젝트 | Not Started | 지원 전에는 선택 사항 | 중심 논문 분석 후 작고 설명 가능한 후보를 결정 |

## 6. Phase Checkpoints

| Phase | Date | Status | Exit Gate |
| --- | --- | --- | --- |
| Phase 1 — Memory Bridge and Paper Scouting | 2026-08-13 ~ 2026-08-23 | Review | Memory/NPU/PIM bridge evidence는 확보; paper scouting 결과를 다음 단계에서 확정 |
| Phase 2 — NPU and Dataflow Foundation | 2026-08-24 ~ 2026-09-06 | Learning | NPU data path 설명, dataflow 비교, 중심 논문 claim map |
| Phase 3 — PIM/CIM and Anchor Paper Analysis | 2026-09-07 ~ 2026-09-20 | Not Started | 중심 논문의 key idea, architecture, result와 limitation 초안 |
| Phase 4 — Comparison and Application Package | 2026-09-21 ~ 2026-10-04 | Not Started | 최소 지원 패키지 검토와 교수 연락 준비 |
| Phase 5 — Post-contact Growth | 2026-10 이후 | Not Started | 피드백 기반 학습, 프로젝트와 research question 발전 |

## 7. Current Evidence-based Understanding

현재 자기 설명과 문제 적용으로 확인된 내용:

- NPU에서 tiling과 data reuse가 제한된 on-chip SRAM과 PE resource를 효율적으로 사용하고 DRAM traffic을 줄이는 이유를 설명할 수 있다.
- K-tiling은 reduction dimension을 나누므로 각 tile이 partial sum을 만들고 마지막 accumulation이 필요함을 설명할 수 있다.
- CIM에서도 weight matrix가 array capacity보다 크면 tiling과 inter-array accumulation이 필요하며, array를 크게 하는 것에는 area뿐 아니라 WL/BL parasitic과 sensing trade-off가 있음을 설명할 수 있다.
- Analog CIM의 current/charge summation 장점과 noise, variation, precision, ADC burden을 Digital CIM의 digital logic/accumulation cost와 비교할 수 있다.
- ADC sharing은 area와 일부 energy overhead를 줄이는 대신 conversion serialization으로 throughput bottleneck을 만들 수 있음을 설명할 수 있다.
- CIM array의 MAC peak를 높여도 ADC throughput이나 activation bandwidth가 따라가지 못하면 system throughput과 utilization이 개선되지 않을 수 있음을 설명할 수 있다.
- SRAM-CIM과 DRAM-PIM을 capacity와 data movement 관점에서 비교하고, weight movement를 줄인 뒤 activation movement가 새로운 bottleneck이 될 수 있음을 설명할 수 있다.
- Weight-stationary의 이점은 weight size 자체뿐 아니라 reuse frequency와 movement cost에 달려 있음을 설명할 수 있다.
- Arithmetic Intensity를 `Operations / Bytes moved`로 해석하고, data reuse와 DRAM traffic 감소가 AI를 높이는 이유를 계산 예제에 적용할 수 있다.
- `BW × AI`는 memory가 연산한다는 뜻이 아니라 memory system이 해당 workload의 compute를 지속시킬 수 있는 rate의 상한임을 설명할 수 있다.
- Roofline 직관에서 actual performance upper bound를 `min(Peak Compute, BW × AI)`로 판단하고 memory-bound와 compute-bound를 구분할 수 있다.
- Bottleneck은 제거되기보다 memory → ADC → activation/interconnect → compute 등 다른 subsystem으로 이동할 수 있다는 system-level 관점을 형성했다.

최근 수정된 오해/어려움:

- TOPS, GB/s, GOP, GB, OP/Byte의 단위 관계에서 혼란이 있었으나 dimensional analysis로 구분했다.
- Peak compute와 actual performance를 동일하게 보는 오류를 수정했다.
- 특정 traffic이 4배 줄었다고 전체 AI가 반드시 4배 증가하는 것은 아니며 다른 traffic이 남는다는 점을 수정했다.
- Digital CIM이 반드시 순차 accumulation을 해야 하거나 ADC를 더 필요로 한다는 초기 이해를 수정했다.
- BL capacitance 증가 시 latency 방향을 반대로 표현한 부분을 수정했으며, capacitance 증가와 ADC throughput 사이를 직접적인 단일 인과로 두지 않도록 정리했다.

Source:

- `learning-logs/2026/08/2026-08-22-npu-pe-array-systolic-tiling.md`
- `learning-logs/2026/08/2026-08-23-memory-wall-analog-cim-fundamentals.md`
- `learning-logs/2026/08/2026-08-24-pim-cim-tiling-roofline-foundations.md`

## 8. Immediate Next Actions

가장 중요한 행동 세 개만 활성화한다.

1. 중심 Foundational PIM/CIM 논문 한 편을 선정하고 abstract와 주요 architecture figure에서 `problem → prior bottleneck → proposed compute location → data path → claimed benefit` claim map을 만든다.
2. Figure에서 weight, activation, partial sum, ADC/digital accumulation의 위치와 이동 경로를 직접 추적하고, 어느 subsystem이 system throughput을 제한할 가능성이 있는지 설명한다.
3. 논문의 성능/에너지 결과를 array peak와 system-level result로 구분하고 ADC/peripheral overhead, precision, utilization, data movement를 비판적으로 읽는다.

필요할 때만 돌아갈 spiral review:

- ADC/DAC circuit 세부
- device nonlinearity/variation
- Digital CIM logic topology
- DRAM-PIM bank-level scheduling
- 실제 Roofline/operational-intensity 정량 분석

## 9. Weekly Review

주간 검토에서는 다음만 확인한다.

- 이번 주에 자신의 말로 설명한 핵심 개념 또는 논문 주장이 있는가?
- 실제 Learning Log, Paper Note 또는 결과물 진전이 있는가?
- 막힌 이유가 영어, 수식, circuit, architecture, paper-reading 중 무엇인지 분류했는가?
- prerequisite 보충 후 논문으로 돌아갈 날짜가 정해져 있는가?
- 현재 활동이 2026년 10월 지원 패키지에 어떻게 기여하는가?
- 다음 주 최우선 행동이 1~3개로 제한되어 있는가?

## 10. Decision Log

- 2026-08-13: 기초를 모두 마친 뒤 논문으로 이동하는 방식 대신, 필수 기초와 논문 분석을 병행하기로 결정함.
- 2026-08-13: 지원 전 필수 결과물을 중심 Paper Note 1개, 관련 논문 비교, 핵심 기초 evidence, 연구 관심 정리, CV와 이메일 초안으로 정함.
- 2026-08-13: Python simulation은 지원 전 필수가 아닌 stretch goal로 둠.
- 2026-08-13: 진행 상태는 Not Started, Learning, Review, Completed 네 단계로 유지함.
- 2026-08-24: PIM/CIM foundations의 exit criteria를 충족한 것으로 판단하고, optional deep-dive를 기본 경로에서 제외해 Foundational Paper claim map과 architecture walkthrough로 advance하기로 함.
- 2026-08-24: 이후 prerequisite gap은 논문 분석 중 필요할 때 spiral learning으로 보충하기로 함.
