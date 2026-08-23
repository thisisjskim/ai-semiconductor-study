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

- Execution Phase: Phase 1 — Memory Bridge and Paper Scouting
- Active Track: Track A — Essential Foundations
- Current Stage: Stage 3 — Memory
- Current Topic: SRAM과 DRAM의 구조·역할 비교 및 NPU on-chip buffer 연결
- Current Deliverable: 6T SRAM Hold/Write/Read 자기 설명이 포함된 후속 Learning Log
- Current Bottleneck: CMOS inverter의 charge/discharge와 6T SRAM 동작을 current, charge, node capacitance 관점으로 연결하기
- Next Milestone: SRAM 회로 핵심을 마치고 SRAM/DRAM 비교와 NPU on-chip buffer로 연결하기
- Phase Deadline: 2026-08-23
- Last Updated: 2026-08-13

## 4. Progress Dashboard

| Stage | Status | 현재 목표 | Evidence / Notes |
| --- | --- | --- | --- |
| 전자공학 기초 (Electronics Fundamentals) | Learning | MOSFET switch, CMOS inverter와 storage circuit 복습 | `learning-logs/2026/08/2026-08-12-register-sram-circuits.md` |
| AI Computation | Not Started | MAC, weight, activation, partial sum의 hardware 흐름 이해 | Phase 2에서 NPU와 함께 시작 |
| Computer Architecture | Not Started | latency, throughput, parallelism, locality의 핵심 이해 | Phase 2에서 필요한 범위 우선 학습 |
| Memory Architecture | Learning | hierarchy, data movement와 Register/SRAM/DRAM 연결 | `learning-logs/2026/08/2026-08-12-register-sram-circuits.md` |
| SRAM / DRAM / eDRAM | Learning | 6T SRAM 동작을 설명하고 SRAM과 DRAM 비교 | `learning-logs/2026/08/2026-08-12-register-sram-circuits.md` |
| NPU Architecture | Learning | PE array, buffer hierarchy와 dataflow 설명 | `learning-logs/2026/08/2026-08-22-npu-pe-array-systolic-tiling.md` |
| PIM / CIM | Not Started | 기존 NPU와 PIM/CIM의 data movement 차이 분석 | Phase 3 핵심 목표; 관심 동기는 확인됐지만 repository 학습 evidence는 아직 없음 |
| Foundational Papers | Not Started | 중심 논문의 claim과 architecture 분석 훈련 | 중심 논문 선정 후 시작 |
| KAIST SSL Lab Papers | Not Started | SSL Lab 중심 논문 1편과 관련 논문 1~2편 분석 | Phase 1에서 후보 조사, Phase 2~4에서 분석 |
| Research Questions / Portfolio | Not Started | Paper Note, 비교표, 연구 관심과 지원 자료 연결 | 결과물 구조만 확정; 실제 연구 결과물 evidence는 아직 없음 |

## 5. Application Deliverables

| Deliverable | Status | Target | Evidence / Next Action |
| --- | --- | --- | --- |
| 핵심 기초 Learning Log | Learning | 2026-09-20까지 지원에 필요한 핵심 evidence 선별 | 현재 SRAM 기록에서 시작해 NPU/PIM으로 확장 |
| 중심 논문 선정 | Not Started | 2026-08-23 | SSL Lab 연구 주제와 논문 후보를 실제 source로 확인 |
| 중심 Paper Note | Not Started | 2026-09-20 초안, 2026-09-27 검토 | `templates/paper-note.md` 사용 |
| 관련 논문 비교 자료 | Not Started | 2026-09-27 | 중심 논문과 1~2편을 problem, architecture, result, limitation으로 비교 |
| 연구 관심 정리 | Not Started | 2026-09-27 | PIM 관심 계기와 학습을 통해 구체화된 질문을 약 1페이지로 정리 |
| GitHub 포트폴리오 안내 | Not Started | 2026-09-30 | 교수에게 보여줄 핵심 문서와 읽는 순서를 안내 |
| CV 초안 | Not Started | 2026-09-27 | 학업 배경, 관심 분야, 분석 결과와 프로젝트 후보 연결 |
| 교수 연락 이메일 | Not Started | 2026-09-30 | 관심 이유, 준비 evidence, 문의 목적을 간결하게 작성 |
| Python simulation / 분석 프로젝트 | Not Started | 지원 전에는 선택 사항 | 중심 논문 분석 후 작고 설명 가능한 후보를 결정 |

## 6. Phase Checkpoints

| Phase | Date | Status | Exit Gate |
| --- | --- | --- | --- |
| Phase 1 — Memory Bridge and Paper Scouting | 2026-08-13 ~ 2026-08-23 | Learning | SRAM 핵심 설명, SRAM/DRAM 연결, 중심 논문 후보 확인 |
| Phase 2 — NPU and Dataflow Foundation | 2026-08-24 ~ 2026-09-06 | Not Started | NPU data path 설명, dataflow 1개 비교, 중심 논문 claim map |
| Phase 3 — PIM/CIM and Anchor Paper Analysis | 2026-09-07 ~ 2026-09-20 | Not Started | 중심 논문의 key idea, architecture, result와 limitation 초안 |
| Phase 4 — Comparison and Application Package | 2026-09-21 ~ 2026-10-04 | Not Started | 최소 지원 패키지 검토와 교수 연락 준비 |
| Phase 5 — Post-contact Growth | 2026-10 이후 | Not Started | 피드백 기반 학습, 프로젝트와 research question 발전 |

## 7. Current Evidence-based Understanding

현재 확인된 내용:

- Register는 작은 working set을 compute 가까이에 두어 latency와 data movement를 줄인다.
- Register의 높은 bit당 circuit/area cost 때문에 더 큰 on-chip storage에는 SRAM이 적합하다.
- Cross-coupled inverter, latch, flip-flop과 multi-bit Register의 관계를 기본 수준에서 설명할 수 있다.
- 6T SRAM이 4T storage core와 2T access transistor로 구성됨을 설명할 수 있다.
- MOSFET channel의 current가 node capacitance를 charge/discharge해 voltage를 바꾼다는 관점을 학습 중이다.

아직 통과하지 못한 점검:

- CMOS inverter의 switching을 current, charge, node capacitance 관점에서 완전히 설명하기
- 6T SRAM의 Hold/Write/Read를 transistor-level에서 설명하기
- SRAM read disturb와 cell stability 설명하기
- SRAM과 DRAM을 구조, 동작, density, latency와 NPU 역할로 비교하기
- NPU의 Register/SRAM/PE array 연결과 dataflow로 확장하기

Source:

- `learning-logs/2026/08/2026-08-12-register-sram-circuits.md`
- `state/CURRENT_LEARNING_CONTEXT.md`는 위 source에서 만든 derived snapshot이므로 근거 자체로 사용하지 않음

## 8. Immediate Next Actions

가장 중요한 행동 세 개만 활성화한다.

1. CMOS inverter의 output node charge/discharge를 PMOS/NMOS, current와 capacitance로 자기 설명한다.
2. 6T SRAM의 Hold → Write → Read를 WL, BL/BL̅, Q/Q̅ 기준으로 설명하고 Learning Log evidence로 남긴다.
3. 2026-08-23까지 SSL Lab 중심 논문 후보를 조사하고 abstract와 주요 figure를 미리 본다.

그다음 행동:

- SRAM과 DRAM 비교
- NPU의 PE, Register, on-chip buffer 전체 그림
- 중심 논문 선정과 claim map 시작

## 9. Weekly Review

주간 검토에서는 다음만 확인한다.

- 이번 주에 자신의 말로 설명한 핵심 개념 또는 논문 주장이 있는가?
- 실제 Learning Log, Paper Note 또는 결과물 진전이 있는가?
- 막힌 이유가 영어, 수식, circuit, architecture 중 무엇인지 분류했는가?
- prerequisite 보충 후 논문으로 돌아갈 날짜가 정해져 있는가?
- 현재 활동이 2026년 10월 지원 패키지에 어떻게 기여하는가?
- 다음 주 최우선 행동이 1~3개로 제한되어 있는가?

## 10. Decision Log

- 2026-08-13: 기초를 모두 마친 뒤 논문으로 이동하는 방식 대신, 필수 기초와 논문 분석을 병행하기로 결정함.
- 2026-08-13: 지원 전 필수 결과물을 중심 Paper Note 1개, 관련 논문 비교, 핵심 기초 evidence, 연구 관심 정리, CV와 이메일 초안으로 정함.
- 2026-08-13: Python simulation은 지원 전 필수가 아닌 stretch goal로 둠.
- 2026-08-13: 진행 상태는 Not Started, Learning, Review, Completed 네 단계로 유지함.
