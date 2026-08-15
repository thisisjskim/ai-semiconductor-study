# Learning Log End-to-End Scenario

과거 conversation 기억이 없는 새 ChatGPT 세션을 가정한다.

## Bootstrap

사용자 입력:

```text
@GitHub

ai-semiconductor-study Research OS로 이전 학습을 이어가자.
repository의 ChatGPT entrypoint를 따라 현재 상태를 복구해줘.
```

기대 결과:

1. 연결된 GitHub plugin의 실제 file-read 기능으로 `state/CURRENT_LEARNING_CONTEXT.md`를 `ref: main`에서 한 번 읽는다.
2. Current Topic, 확인된 이해, Open Questions, Next Action을 복구한다.
3. 필요한 경우에만 관련 Learning Log를 추가로 읽는다.
4. 사용자의 현재 설명과 저장 기록이 다르면 차이를 알리고 기존 기록은 수정하지 않는다.

## Evidence capture

학습 중 사용자가 개념을 자기 말로 설명하고 오해를 수정한다. ChatGPT는 원문, 초기 이해, 불확실성, 수정된 이해, 해결·미해결 질문을 분리해 유지한다. 한 번 설명한 사실만으로 mastery를 판정하지 않는다.

## Tutor loop and checkpoint

1. ChatGPT는 Open Question 또는 Next Action에서 작은 Learning Unit 하나를 선택한다.
2. `Explain → Example → Ask → User explanation → Diagnose → Follow-up` loop로 진행한다.
3. 사용자의 자기 설명이나 misconception correction으로 unit 완료 evidence를 확인한다.
4. 다음 개념을 자동으로 시작하기 전에 저장 가치와 핵심 evidence를 한 번 제안한다.

사용자가 다음처럼 답하면 저장하지 않고 다음 unit으로 진행한다.

```text
기록은 나중에 하고 계속하자.
```

같은 checkpoint의 저장 제안을 반복하지 않는다.

## Save

사용자 입력:

```text
오늘 학습을 저장해줘.
```

기대 결과:

1. `system/LEARNING_LOG_ISSUE_CONTRACT.md`, `templates/learning-log.md`, `system/LEARNING_LOG_AUTHORING_GUIDE.md`를 읽는다. 일반 plugin에서는 `ACTION_SCHEMA.yaml`을 읽을 필요가 없다.
2. 현재 conversation에서만 evidence inventory를 만들고 provenance를 구분한다.
3. target path 존재 여부를 확인하고 create/update를 결정한다.
4. update면 최신 target content와 SHA를 읽는다.
5. 전체 draft를 작성하고 title, envelope, canonical heading, evidence quality를 점검한다.
6. 과거 Learning Log의 문장·서사·checkbox가 복제되지 않았는지 확인한다.
7. target path, operation, 핵심 evidence를 제시하고 사용자 승인을 받는다.
8. 승인 후 Issue를 만들고 필요한 chunk를 추가한 뒤 close한다.
9. 결과 comment를 확인한다.
10. 성공 comment의 commit ref에서 target file을 다시 읽는다.
11. 파일 존재와 승인 내용 반영이 모두 확인된 경우에만 저장 완료라고 말한다.

tool 이름은 특정하지 않는다. 현재 GitHub plugin이 제공하는 repository file read, Issue create, comment append, Issue close, Issue/comment read 기능을 capability 기준으로 사용한다.

## Negative cases

- `mode: create`를 사용하거나 `expected_sha`를 빼면 validator가 거부한다.
- Title과 target path의 날짜 또는 slug가 다르면 validator가 거부한다.
- canonical heading이 빠지면 validator가 거부한다.
- 기존 path에 `create`를 사용하거나 stale SHA로 `update`하면 validator가 거부한다.
- success comment가 없거나 target file을 읽을 수 없으면 저장 완료라고 말하지 않는다.
- AI 설명만 끝난 상태나 사용자의 단순 동의를 Learning Unit 완료로 판정하지 않는다.
- 사용자가 저장을 보류하면 같은 checkpoint에서 제안을 반복하지 않는다.
