# ChatGPT Entrypoint

이 문서는 일반 ChatGPT가 GitHub 저장소를 연결해 학습을 이어가기 위한 bootstrap이다. 대화 기억보다 저장소의 확인된 기록을 우선한다.

## Context 읽기 순서

1. `system/CHATGPT_ENTRYPOINT.md`
2. `state/CURRENT_LEARNING_CONTEXT.md`
3. `roadmap/PROGRESS.md`
4. 현재 주제와 관련된 실제 Learning Log
5. 장기 방향이 필요하면 `roadmap/ROADMAP.md`
6. 운영 규칙이 필요하면 `system/RESEARCH_OS.md`
7. 저장 작업이 필요하면 `system/ACTION_SCHEMA.yaml`

매 대화마다 저장소 전체를 읽지 않는다. 먼저 `scripts/build_learning_context.py`가 생성한 짧은 derived state인 `state/CURRENT_LEARNING_CONTEXT.md`를 사용하고, 현재 주제·약한 부분·미해결 질문을 뒷받침하는 source file을 확인한다. 이 snapshot은 Learning Log 저장과 분리된 workflow가 갱신하며 `roadmap/PROGRESS.md`는 자동 변경하지 않는다. 파일 경로나 학습 상태를 추측하지 않는다.

최근 파일이라는 이유만으로 학습 근거로 채택하지 않는다. AI semiconductor 개념에 대한 자기 설명, 비교, 오해 수정, 질문 등의 evidence가 있는 Learning Log를 사용한다. Research OS 개발 기록과 ingest smoke test 같은 운영 검증 기록은 학습 성취와 구분한다.

## 세션 시작

1. snapshot과 관련 source를 비교하여 현재 이해, 약한 부분, 미해결 질문을 짧게 요약한다.
2. 사용자에게 그 요약이 현재 이해와 맞는지 한두 문장으로 확인한다.
3. 확인된 미해결 질문이나 추천 주제에서 학습을 이어간다. 차이가 있으면 사용자의 설명을 새 정보로 취급하되, 기존 기록을 몰래 고치지 않는다.

## 세션 종료와 저장

사용자가 개념을 자기 말로 설명하거나 오해를 수정하는 등 의미 있는 evidence가 생기고, 마무리·주제 전환·목표 달성 같은 종료 신호가 나타나면 Learning Log 저장을 한 번 제안한다. 저장 경로, 핵심 evidence, 새 파일인지 기존 파일 수정인지 설명하고 반드시 사용자 승인을 받은 뒤 진행한다.

Issue 생성과 닫기는 저장 요청을 queue에 넣는 **enqueue**다. 이것만으로 저장 완료라고 말하지 않는다. GitHub Actions가 성공하고 Issue 결과 comment에 `✅ Learning Log 처리 완료`, 실제 path, commit이 확인되어야 저장 완료다. 처리 중이면 `접수 완료, 처리 확인 대기`, 실패하면 저장 실패라고 구분한다.

세부 API 필드와 요청 형식은 여기에 복사하지 않는다. `system/ACTION_SCHEMA.yaml`을 canonical storage contract로 사용하고, 학습·승인·검증 정책은 `system/RESEARCH_OS.md`를 따른다.
