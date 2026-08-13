# AI Semiconductor Research Roadmap

## 1. Mission

이 Roadmap의 1차 목적은 2026년 9월 말~10월 초까지 KAIST SSL Lab 교수에게 개별연구 참여 의사와 준비 과정을 설득력 있게 보여줄 수 있는 지원 기반을 만드는 것이다. 2027년 겨울학기 개별연구 참여와 이후 AI 반도체 분야 대학원 진학을 목표로 한다.

장기적으로는 NPU architecture, memory architecture, PIM/CIM 논문을 독립적으로 읽고 다음을 수행할 수 있어야 한다.

- 논문이 해결하려는 문제와 기존 접근의 한계를 설명한다.
- 핵심 architecture와 data movement를 자신의 언어와 그림으로 설명한다.
- 성능, 에너지, 면적, 정확도와 유연성의 trade-off를 비교한다.
- 논문의 주장과 실험 evidence를 구분하고 limitation을 찾는다.
- 학습과 분석을 research question, 실습 프로젝트와 연구 포트폴리오로 발전시킨다.

성공 기준은 모든 기초 과목을 완주하는 것이 아니다. 지원 시점에 **학습 능력, 실제 논문 분석 경험, 연구 관심의 구체성, 계속 성장할 수 있는 evidence**를 보여주는 것이 우선이다.

## 2. Starting Point and Constraints

### 학업 배경

- 주전공: 전기및전자공학부
- 부전공: 신소재공학부
- 수강 경험: 미적분학, 선형대수학, 응용미분방정식, 전자회로, 디지털 논리회로, 반도체 소자
- 보충 필요: Computer Architecture, 체계적인 Deep Learning, 영어 논문 독해
- 프로그래밍: C와 Python 기초

### 강점과 위험 요소

- 반도체 소자와 기본 회로는 복습을 통해 다시 연결할 수 있다.
- PIM에서 시작한 관심 동기와 AI 연산 효율에 대한 문제의식이 분명하다.
- 현재 약점은 transistor 회로, 영어 논문, 수식, architecture diagram 해석이다.
- 가장 큰 운영 위험은 기초를 완벽하게 끝내려다 논문 분석과 결과물 제작을 늦추는 것이다.

### 시간 조건

- 주당 목표 학습 시간: 10시간 이상
- 권장 세션 길이: 약 90분
- 교대근무를 고려해 고정 요일보다 주간 목표량과 결과물로 관리한다.

## 3. Operating Principles

### 두 경로를 동시에 사용한다

```text
필수 기초 학습 ─────────┐
                      ├→ 논문 이해 → 부족한 선수지식 발견 → 필요한 만큼 보충
논문 미리보기·분석 ─────┘
```

- 2026년 8월 안에 논문 읽기를 시작한다. 모든 기초가 끝날 때까지 기다리지 않는다.
- 회로와 수식은 현재 논문과 architecture를 이해하는 데 필요한 깊이까지 학습한다.
- 논문에서 막힌 개념은 prerequisite gap으로 기록하고 해당 부분만 보충한 뒤 논문으로 돌아온다.
- ChatGPT는 다음 주제를 추천하지만 최종 선택은 사용자가 한다.
- 목표에서 멀어진 학습, 근거 없는 진도 상승, 지나친 기초 매몰이 감지되면 ChatGPT가 알린다.

### 학습 방법

기본 흐름은 다음을 사용하되 필요한 단계만 적용한다.

```text
Big Picture → Why → What → How → Example
→ AI Semiconductor Connection → Self Explanation → Misconception Check
```

- 전문용어는 피하지 않되 처음 등장하면 쉬운 설명과 기술적 정의를 함께 제공한다.
- 수식은 의미와 변수를 먼저 설명한 뒤 사용한다.
- 중요한 전환점에서 자기 설명과 짧은 퀴즈로 확인하며 퀴즈를 남발하지 않는다.
- 영어 논문은 문장 번역보다 claim, figure, architecture, evidence의 구조를 먼저 찾는다.

### Canonical Stage Mapping

Learning Log의 `Roadmap stage` Metadata와 자동화는 다음 Stage 이름을 사용한다. Track은 병행 작업을 구분하고, Stage는 학습 내용의 위치를 나타낸다.

| Stage | Scope |
| --- | --- |
| Stage 0 — Big Picture | AI workload에서 NPU와 PIM/CIM까지의 전체 연결 |
| Stage 1 — AI Computation | MAC, tensor, weight, activation, precision |
| Stage 2 — Computer Architecture | parallelism, latency, bandwidth, locality, hierarchy |
| Stage 3 — Memory | Register, SRAM, DRAM/HBM, data movement |
| Stage 4 — NPU Architecture | PE array, buffer, dataflow, mapping |
| Stage 5 — PIM / CIM | SRAM-CIM, DRAM-PIM과 architecture trade-off |
| Stage 6 — Foundational Papers | 핵심 AI accelerator 논문 분석 |
| Stage 7 — SSL Lab Papers | KAIST SSL Lab 논문 분석과 비교 |
| Stage 8 — Research Portfolio | research question, 프로젝트와 지원 결과물 |

## 4. Knowledge and Research Tracks

Track은 순서대로 모두 끝내는 과목 목록이 아니다. 현재 논문과 결과물에 필요한 항목을 병행한다.

### Track A — Essential Foundations

#### A1. AI Computation

핵심 범위:

- Matrix multiplication, convolution, tensor의 hardware 관점
- MAC, weight, activation, partial sum
- Inference와 training의 차이
- Precision과 quantization의 역할

현재 목표의 완료 기준:

- 대표적인 AI workload가 많은 MAC과 data movement를 만드는 이유를 설명한다.
- weight, activation, partial sum이 어디에 저장되고 이동하는지 추적한다.
- NPU 또는 PIM/CIM 논문에서 workload와 precision 관련 표현을 알아본다.

#### A2. Computer and Memory Architecture

핵심 범위:

- Latency, throughput, bandwidth, parallelism
- Locality, memory hierarchy, cache의 역할
- Register, on-chip SRAM, DRAM/HBM
- Data movement, data reuse, memory bandwidth bottleneck

현재 목표의 완료 기준:

- latency와 bandwidth를 비교하고 memory hierarchy가 필요한 이유를 설명한다.
- Register, SRAM, DRAM/HBM의 capacity, speed, area, energy trade-off를 비교한다.
- architecture diagram에서 compute, on-chip buffer와 off-chip memory를 구분한다.

#### A3. Circuit and Device Bridge

논문 이해에 필요한 범위만 선택적으로 복습한다.

- MOSFET switch, CMOS inverter, pull-up/pull-down
- Latch, flip-flop, register
- 6T SRAM Hold, Write, Read
- Read disturb, cell stability의 기본 직관
- 필요할 때 SRAM array와 peripheral circuit

현재 목표의 완료 기준:

- CMOS inverter의 charge/discharge를 current와 node capacitance 관점에서 설명한다.
- 6T SRAM의 Hold, Write, Read를 WL, BL/BL̅, Q/Q̅로 설명한다.
- circuit 특성이 SRAM architecture와 SRAM-CIM의 제약으로 이어지는 지점을 알아본다.

> 깊은 공정 이론, 모든 analog circuit, 복잡한 transistor 식 유도는 논문이 요구하지 않는 한 1차 지원 준비의 필수 범위가 아니다.

#### A4. NPU Architecture and Dataflow

핵심 범위:

- PE, MAC unit, PE array, systolic array
- Register file, local buffer, global buffer, DRAM interface
- Weight, activation, partial sum의 이동
- Weight-stationary, output-stationary, row-stationary의 기본 비교
- Tiling, mapping, utilization, data reuse

현재 목표의 완료 기준:

- 입력부터 출력까지 NPU의 data path를 그려 설명한다.
- dataflow가 어떤 데이터를 어디에 유지하고 어떤 이동을 줄이는지 비교한다.
- PE 수만 늘릴 때 성능이 선형으로 증가하지 않는 이유를 설명한다.
- 논문의 accelerator block diagram과 memory organization을 따라간다.

#### A5. PIM / CIM

핵심 범위:

- Memory Wall과 von Neumann bottleneck
- Near-memory processing, DRAM-PIM, SRAM-CIM
- Digital CIM과 Analog CIM
- Compute primitive, ADC/DAC와 peripheral overhead
- Precision, accuracy, energy, area, programmability trade-off

현재 목표의 완료 기준:

- 기존 NPU와 PIM/CIM의 compute 위치와 data movement 차이를 설명한다.
- SRAM-CIM과 DRAM-PIM의 장점과 제약을 비교한다.
- 논문이 주장하는 efficiency gain의 비용과 baseline을 질문할 수 있다.

### Track B — Paper Analysis

#### B1. Paper Reading Skill

논문은 다음 세 번의 pass로 읽는다.

1. **Claim map**: Problem, Motivation, Prior-work gap, Key claim을 찾는다.
2. **Architecture walkthrough**: figure를 따라 component, data path, memory와 computation을 설명한다.
3. **Evidence and critique**: baseline, metric, result, trade-off, limitation을 확인한다.

영어 문장을 처음부터 전부 번역하지 않는다. 핵심 claim과 figure를 먼저 잡고 필요한 문장과 수식을 깊게 읽는다.

#### B2. Anchor Paper

지원 전 중심 논문 한 편을 선정해 `templates/paper-note.md`의 구조로 분석한다.

완료 기준:

- Problem, prior-work gap과 key idea를 자신의 언어로 설명한다.
- 핵심 architecture figure를 보며 data movement와 computation을 설명한다.
- 주요 실험 결과가 어떤 주장을 뒷받침하는지 연결한다.
- 적어도 하나의 trade-off, limitation 또는 비판적 질문을 제시한다.

#### B3. Related Paper Comparison

중심 논문과 관련 논문 1~2편을 비교한다.

- 해결하려는 문제
- compute와 memory organization
- 핵심 mechanism
- baseline과 평가 지표
- 얻는 이득과 치르는 비용
- 적용 범위와 limitation

지원 전에는 많은 논문을 얕게 읽기보다 중심 논문 한 편을 깊게 설명하는 것을 우선한다.

### Track C — Portfolio Deliverables

#### C1. Evidence Records

- Learning Log: 자기 설명, 오해 수정, 질문과 다음 행동
- Concept/Foundation Note: 여러 기록에서 안정된 개념의 정제본
- Paper Note: 논문의 주장, architecture, evidence와 limitation

#### C2. Application Portfolio

지원 전 최소 결과물:

- 깊게 분석한 중심 Paper Note 1개
- 관련 논문 1~2편 비교 자료 1개
- 기초 학습 evidence와 핵심 Concept Note
- 연구 관심과 SSL Lab 연결을 정리한 약 1페이지 문서
- 선별된 GitHub 결과물을 소개하는 짧은 포트폴리오 안내

#### C3. Practical Project

Python simulation 또는 작은 분석 프로젝트는 시간이 허락하면 수행하는 stretch goal이다. 논문과 연결되지 않는 큰 프로젝트를 억지로 시작하지 않는다.

좋은 후보의 조건:

- data movement, dataflow, memory hierarchy 또는 PIM/CIM trade-off를 보여준다.
- 입력, 가정, metric과 결과를 설명할 수 있다.
- 작은 범위라도 질문과 결론이 분명하다.
- CV에서 자신의 역할과 배운 점을 한두 문장으로 소개할 수 있다.

### Track D — Application Readiness

- SSL Lab의 연구 주제와 최근 논문 흐름 조사
- 자신의 관심 동기와 준비 과정을 연구실 주제에 연결
- CV에서 보여줄 repository evidence와 결과물 선별
- 교수 연락 이메일 초안 작성과 검토
- 중심 논문과 관심 연구에 관한 예상 질문 준비
- 연락 후에도 학습과 결과물 개선 지속

## 5. Time-boxed Execution Plan

날짜는 교대근무 상황에 따라 며칠 조정할 수 있지만, 논문 진입과 지원 결과물 마감은 계속 뒤로 미루지 않는다.

### Phase 1 — Memory Bridge and Paper Scouting

**기간:** 2026-08-13 ~ 2026-08-23

핵심 학습:

- CMOS inverter와 6T SRAM의 핵심 동작 마무리
- SRAM과 DRAM의 구조·역할 비교
- Memory hierarchy에서 NPU on-chip buffer로 연결

동시 결과물:

- 현재 SRAM Learning Log 보강 또는 후속 기록
- 중심 논문 후보와 선정 기준 정리
- 늦어도 이 Phase 안에 후보 논문의 abstract와 주요 figure 미리보기

Exit gate:

- Register/SRAM/DRAM의 역할 차이를 설명한다.
- 6T SRAM 기본 동작을 설명하고 남은 circuit gap을 구분한다.
- 분석할 중심 논문 후보를 실제 경로 또는 링크로 확인한다.

### Phase 2 — NPU and Dataflow Foundation

**기간:** 2026-08-24 ~ 2026-09-06

핵심 학습:

- AI workload와 MAC data path
- PE array, buffer hierarchy, data reuse
- 대표 dataflow와 memory bottleneck

동시 결과물:

- NPU architecture Concept Note 후보
- 중심 논문 1차 claim map
- 논문에서 발견한 prerequisite gap 목록

Exit gate:

- NPU의 compute와 memory 구조를 큰 그림으로 설명한다.
- 한 가지 dataflow가 data movement를 줄이는 방식을 설명한다.
- 중심 논문의 problem, motivation과 핵심 figure를 찾는다.

### Phase 3 — PIM/CIM and Anchor Paper Analysis

**기간:** 2026-09-07 ~ 2026-09-20

핵심 학습:

- Memory Wall, SRAM-CIM, DRAM-PIM
- Digital/Analog CIM과 주요 trade-off
- 중심 논문에 필요한 circuit/architecture 보충

동시 결과물:

- 중심 Paper Note 초안
- architecture walkthrough
- 주요 실험과 baseline 정리
- 관련 논문 1~2편 선정

Exit gate:

- 중심 논문의 key idea와 architecture를 자기 언어로 설명한다.
- 주요 결과가 뒷받침하는 claim을 연결한다.
- 최소 하나의 trade-off 또는 limitation을 제시한다.

### Phase 4 — Comparison and Application Package

**기간:** 2026-09-21 ~ 2026-10-04

핵심 작업:

- 중심 Paper Note 완성도 검토
- 관련 논문 비교표 작성
- 약 1페이지 연구 관심 정리
- GitHub 결과물 선별과 안내 정리
- CV와 교수 연락 이메일 초안 작성·검토

최소 지원 패키지:

1. 중심 Paper Note 1개
2. 관련 논문 1~2편 비교 자료
3. 핵심 기초 학습 evidence
4. 연구 관심 정리 약 1페이지
5. CV와 교수 연락 이메일 초안

Exit gate:

- 결과물마다 자신의 설명과 실제 source가 연결되어 있다.
- 이메일에서 관심 계기, 준비 내용, 논문을 통해 생긴 질문을 간결하게 설명한다.
- GitHub 링크를 받는 사람이 무엇을 먼저 봐야 하는지 알 수 있다.

### Phase 5 — Post-contact Growth

**기간:** 2026-10 이후 ~ 2027년 겨울학기 개별연구

- 교수 연락 결과와 피드백에 따라 학습 우선순위를 조정한다.
- Paper Note와 논문 비교를 계속 확장한다.
- 적합한 Python simulation 또는 작은 연구 프로젝트를 수행한다.
- Research Question을 근거, 가설, 필요한 실험과 함께 발전시킨다.
- 개별연구 참여에 필요한 도구와 구현 역량을 보충한다.

## 6. Weekly Operating Rhythm

교대근무 때문에 요일별 고정 계획 대신 주간 단위로 운영한다.

권장 배분:

- 약 60%: 필수 개념 학습과 논문 읽기
- 약 25%: Paper Note, 비교표, Concept Note 등 결과물 작성
- 약 15%: 자기 설명 점검, 복습, 다음 주 계획

한 주의 최소 evidence:

- 의미 있는 Learning Log 또는 Paper Note 진전 1개 이상
- 자신의 말로 설명한 핵심 개념이나 논문 주장 1개 이상
- 해결하거나 명확히 분류한 prerequisite gap 1개 이상
- 다음 주에 수행할 가장 중요한 행동 1~3개

## 7. Status and Evidence Rules

진행 상태는 `roadmap/PROGRESS.md`에서 다음 네 단계로 관리한다.

- **Not Started**: 현재 목표 기준의 의미 있는 evidence가 없음
- **Learning**: 설명, 질문, 분석 등 진행 중인 evidence가 있음
- **Review**: 핵심 범위의 1차 학습을 마치고 자기 설명·비교·비판을 검증 중
- **Completed**: 현재 목표의 exit gate를 충족했으며 다음 단계에서 사용할 수 있음

`Completed`는 영구 숙련을 의미하지 않는다. 논문에서 새로운 prerequisite gap이 발견되면 다시 `Learning` 또는 `Review`로 돌아갈 수 있다.

상태 변경의 근거는 실제 repository path로 연결한다.

- 기초 학습: `learning-logs/**`, Concept/Foundation Note
- 논문 분석: Paper Note와 논문 비교 자료
- 프로젝트: 코드, 실험 설명, 결과와 limitation
- 지원 준비: 연구 관심 정리, CV와 이메일 검토본

## 8. Scope Guardrails

다음은 1차 지원 준비의 필수 조건이 아니다.

- 모든 전자회로와 반도체 공정의 완전한 복습
- 복잡한 transistor 식의 전 과정 유도
- 본격적인 RTL/Verilog 프로젝트
- 대규모 논문 재현
- 많은 논문을 얕게 요약하는 작업
- 관심 연구와 연결되지 않은 대형 simulation

다음 신호가 보이면 학습 방향을 다시 점검한다.

- 기초 학습 때문에 중심 논문 시작일이 계속 미뤄진다.
- 번역과 요약은 늘지만 자신의 설명, 비교와 질문이 없다.
- 파일 수는 늘지만 교수에게 보여줄 결과물이 선명하지 않다.
- 현재 활동이 2026년 10월 지원 패키지에 어떻게 기여하는지 설명하기 어렵다.

현재 위치, 이번 주 행동과 실제 evidence는 `roadmap/PROGRESS.md`에서 관리한다.
