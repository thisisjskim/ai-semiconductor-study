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
- Current Stage: Stage 5 — PIM / CIM
- Current Topic: 중심 Foundational Paper의 claim map과 architecture walkthrough
- Current Deliverable: 6T SRAM Hold/Write/Read 자기 설명이 포함된 후속 Learning Log
- Current Bottleneck: CMOS inverter의 charge/discharge와 6T SRAM 동작을 current, charge, node capacitance 관점으로 연결하기
- Next Milestone: SRAM 회로 핵심을 마치고 SRAM/DRAM 비교와 NPU on-chip buffer로 연결하기
- Phase Deadline: 2026-08-23
- Last Updated: 2026-08-24

## 4. Progress Dashboard

| Stage | Status | 현재 목표 | Evidence / Notes |
| --- | --- | --- | --- |
| 전자공학 기초 (Electronics Fundamentals) | Learning | MOSFET switch, CMOS inverter와 storage circuit 복습 | `learning-logs/2026/08/2026-08-12-register-sram-circuits.md` |
| AI Computation | Not Started | MAC, weight, activation, partial sum의 hardware 흐름 이해 | Phase 2에서 NPU와 함께 시작 |
| Computer Architecture | Not Started | latency, throughput, parallelism, locality의 핵심 이해 | Phase 2에서 필요한 범위 우선 학습 |
| Memory Architecture | Learning | hierarchy, data movement와 Register/SRAM/DRAM 연결 | `learning-logs/2026/08/2026-08-22-sram-dram-sense-amplifier.md`, `learning-logs/2026/08/2026-08-22-npu-sram-data-reuse-dataflow.md` |
| SRAM / DRAM / eDRAM | Learning | 6T SRAM 동작을 설명하고 SRAM과 DRAM 비교 | `learning-logs/2026/08/2026-08-14-sram-read-disturb-cell-stability.md`, `learning-logs/2026/08/2026-08-15-sram-cell-ratio-snm.md`, `learning-logs/2026/08/2026-08-15-sram-read-path-fundamentals.md` |
| NPU Architecture | Learning | PE array, buffer hierarchy와 dataflow 설명 | `learning-logs/2026/08/2026-08-22-npu-pe-array-systolic-tiling.md` |
| PIM / CIM | Learning | 기존 NPU와 PIM/CIM의 data movement 차이 분석 | `learning-logs/2026/08/2026-08-23-memory-wall-analog-cim-fundamentals.md`, `learning-logs/2026/08/2026-08-24-pim-cim-tiling-roofline-foundations.md` |
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

