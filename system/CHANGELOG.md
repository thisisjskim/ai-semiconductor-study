# Changelog

AI Semiconductor Research OS의 주요 기능 변경 사항을 기록한다.

## v0.2.0 — Current

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
