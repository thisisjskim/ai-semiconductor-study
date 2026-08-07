# Changelog

AI Semiconductor Research OS의 주요 기능 변경 사항을 기록한다.

## v0.1.2 — Current

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
- GitHub를 장기 학습 기록의 Source of Truth로 사용하는 원칙 설정

## 현재 상태

- Version: v0.1.2
- Repository Role: AI Semiconductor Research OS
- Primary Goal: KAIST SSL Lab 개별연구 준비
- Current Focus: v0.1.2 Learning Protocol 구축 완료, 실제 학습 시작 준비 완료
