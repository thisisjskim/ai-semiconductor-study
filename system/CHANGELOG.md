# Changelog

AI Semiconductor Research OS의 주요 기능 변경 사항을 기록한다.

## v0.3.0 — Current

### Added
- 첫 Learning Unit 전에 boundary 또는 gap source와 함께 최신 의미 있는 Learning Log 최대 2개를 읽는 Required Source 정책
- Progress Update 뒤 생성된 context가 최신 `PROGRESS.md`를 사용했는지 검증하는 `Progress source SHA` provenance
- 질문 전 prerequisite readiness와 새 topic Explain-first gate, Learning Unit 완료와 log-worthy 저장 판정의 분리 규칙
- Learning Log 작성기, 저장 validator와 context builder가 함께 읽는 canonical Domain metadata schema
- Roadmap topic별 Learning Objective, Minimum Required Understanding, Exit Criteria, Optional Deep Dive와 Next Topic을 정의하는 boundary 계약
- Progress와 Learning Log evidence를 함께 비교해 `continue`, `review_then_advance`, `advance`를 만드는 Roadmap-aware planner
- Blocking Gap과 Optional Open Question 분리 및 progression-over-exhaustiveness / spiral learning 세션 규칙
- Learning Log 저장 확인 뒤 별도 사용자 승인으로 실행하는 `[progress-update]` Issue 계약
- `roadmap/PROGRESS.md`의 최신 blob SHA와 Learning Log evidence 경로를 확인하는 Progress 전용 Python 검증기
- `Current Stage`, `Current Topic`, Dashboard `Not Started → Learning`, 필요한 `Last Updated`만 반영하는 GitHub Actions
- 성공·실패 Issue comment와 ChatGPT의 최종 commit 내용 재확인 절차
- Learning Log 저장 직전 gate, session-evidence 기반 authoring guide, 새 세션 end-to-end 검증 시나리오
- 파일을 쓰지 않고 title, envelope, target, Markdown을 검사하는 Learning Log preflight mode
- 일반 ChatGPT의 GitHub plugin tool 이름에 의존하지 않는 capability-based entrypoint
- 일반 ChatGPT용 Tutor Loop, 작은 Learning Unit 완료 기준, checkpoint와 저장 보류 protocol

### Fixed
- 현재 boundary에 해당하는 Learning Log가 아직 없을 때 Current Learning Context 생성이 실패하던 빈 evidence 처리
- 실제 학습 진도가 다음 boundary로 이동해도 과거 SRAM 문구를 고정 검사해 Context Refresh가 실패하던 저장소 상태 테스트
- Progress 반영 성공과 후속 `CURRENT_LEARNING_CONTEXT.md` 갱신 완료를 구분하지 않아 stale snapshot으로 다음 학습을 제안할 수 있던 실행 경로
- 단일 질문·답변 또는 Exit Criterion 하나의 충족 직후 Learning Log 저장을 너무 일찍 제안할 수 있던 Checkpoint 모호성
- `memory-architecture`로 분류된 8월 22일 SRAM/DRAM 학습 evidence가 현재 SRAM boundary의 마지막 criterion에 반영되지 않던 cross-domain evidence 누락
- `next_roadmap_topic` 설명문을 다음 boundary의 공식 topic으로 다시 인식하지 못할 수 있던 transition alias 누락
- 허용 목록에 없는 Domain이 저장된 뒤에야 context evidence에서 제외되던 검증 공백
- 미지원 Domain을 학습 내용의 무효로 표현하던 context 제외 사유를 metadata 오류로 명확화
- 최신 Learning Log의 세부 Topic 제목을 공식 Current Topic으로 자동 승격하던 오류; 공식 변경은 boundary의 exit criteria와 `next_roadmap_topic`만 사용
- 새 학습 세션이 snapshot 두 파일만 읽고 사용자의 실제 Learning Log evidence를 확인하지 않은 채 첫 진단 질문을 만들 수 있던 grounding 공백
- 첫 Blocking Gap과 가장 가까운 Learning Log를 필수 source로 지정하고, 설명·예시 없이 cold quiz부터 시작하지 않도록 session protocol 강화
- `mode: create`처럼 계약에 없는 envelope 필드와 `expected_sha` 누락을 명시적으로 거부
- Learning Log title의 전체 pattern과 target path의 날짜·slug 일치를 실행 코드에서 검증
- 성공 comment뿐 아니라 결과 commit의 실제 target file까지 확인해야 저장 완료로 판정

### Safety
- 지원 날짜, 실행 계획 필드, milestone, deadline, Roadmap 구조는 자동 변경하지 않음
- Dashboard의 `Review`와 `Completed`는 자동 판정하지 않음
- 모든 main 쓰기 workflow를 하나의 concurrency group으로 직렬화하고 각 Issue 유형을 제목으로 분리함

### Removed
- 자동 Progress Reconciliation state, builder, shared policy와 후속 GitHub Actions workflow

## v0.2.3

### Fixed
- 학습 세션 bootstrap을 세 파일의 필수 연속 조회에서 `state/CURRENT_LEARNING_CONTEXT.md` 한 번의 조회로 단순화
- 후속 Learning Log·Progress·Roadmap 조회를 학습 시작의 전제조건이 아닌 필요 시 근거 확인 단계로 변경
- 연속 Action 호출 불가를 이유로 학습을 거부하거나 사용자에게 파일별 호출을 요구하는 응답을 금지

## v0.2.2

### Fixed
- `이전 공부를 이어나가자` 같은 자연어 요청에서 GPT가 GitHub Action을 호출하지 않고 저장소 접근 불가를 추측하던 routing 문제 수정
- Action의 relevance description에 학습 재개·현재 상태·논문 재개 trigger와 필수 bootstrap 경로를 명시
- 실제 Action 오류 없이 파일 붙여넣기를 요청하거나 접근 불가를 선언하지 않도록 Custom GPT 실행 계약 추가
- Custom GPT의 300자 제한을 넘지 않도록 모든 Action description·summary 길이 회귀 검사 추가

## v0.2.1

### Fixed
- ChatGPT Actions가 component `$ref`로 선언된 `issue_number` path parameter를 읽지 못해 Issue 관련 operation을 건너뛰던 schema 호환성 문제 수정
- Issue 조회·댓글·종료 operation의 `issue_number`를 inline parameter로 선언하고 회귀 test 추가

## v0.2.0

### Added
- Custom GPT의 파일 직접 PUT을 제거하고 `Issue → GitHub Actions → learning-logs/**` 저장 경로 도입
- `createLearningLogIssue`, `appendLearningLogChunk`, `closeLearningLogIssue`, 처리 결과 조회 Action 추가
- 평문 chunk 저장과 Issue 종료 후 비동기 결과 검증 절차 추가
- `operation`, `target_path`, `expected_sha`를 사용하는 안전한 create/update 계약 추가
- Repository owner 검증, 경로 allowlist, 기존 파일 SHA 검증 추가
- Learning Log Metadata에 Document type, Domain, Roadmap stage, Evidence, Related notes 추가
- Issue ingest 변환기와 contract test 추가

### Changed
- Learning Log는 Meaningful Learning Unit 종료를 감지한 GPT가 제안하고 사용자 승인 후 저장
- 한 Issue는 한 파일만 처리하며 긴 기록은 section 경계에서 30,000자 미만 chunk로 분할
- 저장 성공은 GitHub Actions 결과 댓글의 path와 commit 확인 후에만 선언
- Custom GPT PAT 권한을 Contents read-only, Issues read/write로 축소

### Principle
- GPT는 학습 내용을 판단하고 평문을 전달하며, deterministic CI가 파일 경로 검증과 commit을 담당한다.
- Base64 생성과 큰 파일 쓰기를 모델에게 맡기지 않는다.
- 자동화의 목적은 파일 수 증가가 아니라 학습 evidence의 안정적 보존이다.

## v0.1.3

### Added
- Meaningful Learning Unit 기준 추가
- 의미 있는 학습 단위 종료 시 GPT가 Learning Log 저장을 먼저 제안하는 정책 추가
- 사용자 승인 후 GitHub에 반영하는 저장 절차 추가
- Learning Log의 문서 유형, Domain, Roadmap Stage, Evidence, Related Notes 분류 기준 추가
- 긴 학습 세션을 개념별 Learning Log로 나누는 정책 추가
- 한 번의 Action에서 하나의 파일만 처리하고 저장 후 검증하는 정책 추가
- Learning Log, Foundation Note, Paper Note, Final Note의 역할과 경로 구분 추가

### Principle
- 전체 대화가 아니라 학습 Evidence와 이해 변화를 기록한다.
- Learning Log 생성은 학습 완료나 Foundation 승격을 의미하지 않는다.
- 분류와 연결은 일관되게 수행하지만 자동 Promotion은 하지 않는다.
- 기능 확장보다 저장 안정성과 사용자의 학습 효과를 우선한다.

## v0.1.2

### Added
- Custom GPT의 역할을 AI Semiconductor Tutor, Research Mentor, Research OS Manager로 확장
- Learning Protocol 도입: Big Picture → Why → What → How → Example → AI Semiconductor Connection → Self Explanation → Misconception Check
- 중요한 개념에서 사용자의 자기 설명(Self Explanation)을 유도하는 Active Learning 원칙 추가
- 사용자 설명에 대해 정확한 부분 / 불완전한 부분 / 잘못된 부분을 구분해 피드백하는 원칙 추가
- Depth Control 도입: Intuition → System → Architecture → Circuit → Device / Physics
- 새 채팅에서 roadmap/PROGRESS.md, 최근 learning-logs, 관련 foundation notes를 이용해 학습 위치를 복구하는 Session Recovery 원칙 추가
- Roadmap을 강제 syllabus가 아닌 navigation map으로 사용하는 원칙 추가
- 기초 학습과 논문 읽기를 왕복하는 Paper Bridge Protocol 추가
- Bottom-up + Top-down learning 병행 원칙 추가
- learning-log → foundation → final-note를 파일 이동이 아닌 새로운 문서 생성으로 다루는 Knowledge Promotion 원칙 추가

### Principle
- v0.1.2에서는 Knowledge Promotion을 자동 수행하지 않는다.
- 기능을 미리 과도하게 추가하지 않고 실제 학습 과정에서 발견되는 문제를 기반으로 Progress Tracking, 분류, 자동화, 요약, Foundation/Final Note 승격 등을 후속 버전에서 개선한다.

## v0.1.1

### Added
- File Discovery 기능 추가
- 기존 Markdown 파일을 수정하기 전에 실제 경로를 탐색하고 확인하는 절차 추가
- 기존 파일의 최신 내용과 SHA를 확인한 뒤 변경점을 비교하는 안전 업데이트 workflow 추가
- 기존 파일 수정 전 사용자 승인 절차 추가

### Principle
- Never guess when you can verify.
- 기존 파일을 중복 생성하거나 확인 없이 덮어쓰지 않는다.

## v0.1

### Added
- Custom GPT와 GitHub repository 연결
- AI semiconductor 학습 내용을 Markdown 기반으로 장기 기록하는 기본 구조 도입
- Daily Learning Log를 통한 학습 과정 기록 시작
- GitHub를 장기 학습 기록의 Source of Truth로 사용하는 원칙 도입

## 현재 상태

- Version: v0.2.0
- Repository Role: AI Semiconductor Research OS
- Primary Goal: KAIST SSL Lab 개별연구 준비
- Current Focus: Stable Issue-based Learning Capture
