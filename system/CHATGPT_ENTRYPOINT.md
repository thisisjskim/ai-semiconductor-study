# ChatGPT Entrypoint

이 문서는 일반 ChatGPT가 GitHub 저장소를 연결해 학습을 이어가기 위한 bootstrap이다. 대화 기억보다 저장소의 확인된 기록을 우선한다.

## Action 실행 계약

세션을 시작할 때는 이 문서가 아니라 `state/CURRENT_LEARNING_CONTEXT.md`를 `getStudyPath`와 `ref: main`으로 한 번 읽는 것을 우선한다. 그 derived snapshot의 Current Topic, Open Questions, Next Action만으로 학습을 즉시 시작할 수 있다. GitHub 웹 검색, 공개 페이지 열기, 대화 기억은 `getStudyPath` 호출의 대체 수단이 아니다.

학습·복습·현재 상태·다음 주제·논문 재개 요청에서는 자연어 답변보다 저장소 읽기를 먼저 실행한다. Action을 실제로 호출하지 않은 상태에서 저장소에 접근할 수 없다고 말하거나 사용자에게 파일 내용을 붙여 달라고 요청하지 않는다. 호출이 실패하면 operation, path와 실제 오류를 밝히며, 오류 응답 없이 접근 실패를 추측하지 않는다.

## Context 읽기 순서

1. 항상 먼저 `state/CURRENT_LEARNING_CONTEXT.md` 한 파일만 읽고 학습을 시작한다.
2. 현재 주제의 정확한 근거가 필요하면 snapshot에 명시된 실제 Learning Log를 읽는다.
3. 현재 위치 판단에 추가 정보가 필요하면 `roadmap/PROGRESS.md`를 읽는다.
4. reconciliation이 pending이면 `state/PROGRESS_RECONCILIATION.md`를 읽는다.
5. 장기 방향이 필요하면 `roadmap/ROADMAP.md`를 읽는다.
6. 운영 규칙이 필요하면 `system/RESEARCH_OS.md`를 읽는다.
7. 저장 작업이 필요하면 `system/ACTION_SCHEMA.yaml`을 읽는다.

2번 이후의 조회는 필요할 때만 수행한다. 여러 파일을 연속으로 읽지 못한다는 이유로 학습 시작을 거부하거나 사용자에게 파일별 호출을 요구하지 않는다.

매 대화마다 저장소 전체를 읽지 않는다. 먼저 `scripts/build_learning_context.py`가 생성한 짧은 derived state인 `state/CURRENT_LEARNING_CONTEXT.md`를 사용하고, 현재 주제·약한 부분·미해결 질문을 뒷받침하는 source file을 확인한다. 이 snapshot은 Learning Log 저장과 분리된 workflow가 갱신하며 `roadmap/PROGRESS.md`는 자동 변경하지 않는다. 파일 경로나 학습 상태를 추측하지 않는다.

최근 파일이라는 이유만으로 학습 근거로 채택하지 않는다. AI semiconductor 개념에 대한 자기 설명, 비교, 오해 수정, 질문 등의 evidence가 있는 Learning Log를 사용한다. Research OS 개발 기록과 ingest smoke test 같은 운영 검증 기록은 학습 성취와 구분한다.

## 세션 시작

1. snapshot과 관련 source를 비교하여 현재 이해, 약한 부분, 미해결 질문을 짧게 요약한다.
2. 사용자에게 그 요약이 현재 이해와 맞는지 한두 문장으로 확인한다.
3. 확인된 미해결 질문이나 추천 주제에서 학습을 이어간다. 차이가 있으면 사용자의 설명을 새 정보로 취급하되, 기존 기록을 몰래 고치지 않는다.

`state/PROGRESS_RECONCILIATION.md`에 pending proposal이 있어도 이를 승인으로 간주하지 않는다. 사용자가 제안 항목과 evidence를 검토해 명시적으로 승인한 경우에만 Codex의 branch → 테스트 → Pull Request 흐름으로 `roadmap/PROGRESS.md` 반영을 요청한다. 일반 학습 대화나 Learning Log 저장 승인을 progress 변경 승인으로 확대 해석하지 않는다.

## 세션 종료와 저장

사용자가 개념을 자기 말로 설명하거나 오해를 수정하는 등 의미 있는 evidence가 생기고, 마무리·주제 전환·목표 달성 같은 종료 신호가 나타나면 Learning Log 저장을 한 번 제안한다. 저장 경로, 핵심 evidence, 새 파일인지 기존 파일 수정인지 설명하고 반드시 사용자 승인을 받은 뒤 진행한다.

Issue 생성과 닫기는 저장 요청을 queue에 넣는 **enqueue**다. 이것만으로 저장 완료라고 말하지 않는다. GitHub Actions가 성공하고 Issue 결과 comment에 `✅ Learning Log 처리 완료`, 실제 path, commit이 확인되어야 저장 완료다. 처리 중이면 `접수 완료, 처리 확인 대기`, 실패하면 저장 실패라고 구분한다.

세부 API 필드와 요청 형식은 여기에 복사하지 않는다. `system/ACTION_SCHEMA.yaml`을 canonical storage contract로 사용하고, 학습·승인·검증 정책은 `system/RESEARCH_OS.md`를 따른다.
