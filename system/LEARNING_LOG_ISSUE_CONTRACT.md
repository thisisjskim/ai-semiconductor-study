# Learning Log Issue Contract

이 문서는 일반 ChatGPT와 GitHub plugin이 Learning Log 저장 직전에 확인하는 tool-independent gate다. 계약의 역할별 canonical source는 다음과 같다.

- Human-readable Issue wire contract: 이 문서
- Markdown structure: `templates/learning-log.md`
- Executable validation: `scripts/ingest_learning_log.py`
- Metadata enum: `system/LEARNING_LOG_METADATA_SCHEMA.json`
- Approval and verification policy: `system/RESEARCH_OS.md`
- Evidence-based authoring: `system/LEARNING_LOG_AUTHORING_GUIDE.md`
- Custom GPT Action interface only: `system/ACTION_SCHEMA.yaml`

위 파일의 내용을 다른 안내 문서에 임의로 변형해 복사하지 않는다. 이 문서와 canonical source의 drift는 `scripts/test_ingest_learning_log.py`가 검사한다.

## 저장 전 필수 순서

1. 이 문서의 wire contract와 성공 판정 기준을 확인한다.
2. `templates/learning-log.md`, `system/LEARNING_LOG_AUTHORING_GUIDE.md`, `system/LEARNING_LOG_METADATA_SCHEMA.json`을 다시 읽고 Domain은 schema의 허용값 중 하나만 선택한다.
3. 현재 conversation만으로 evidence inventory를 만들고, 과거 로그의 문장이나 서사를 복제하지 않는다.
4. 같은 날짜·slug의 실제 target path가 존재하는지 조회한다.
5. 없으면 `create`와 `expected_sha: new`, 있으면 `update`와 방금 읽은 40자리 SHA를 선택한다.
6. 전체 Markdown이 canonical heading, metadata enum과 evidence 품질 기준을 충족하는지 확인한다.
7. 사용자에게 target path, create/update, 핵심 evidence를 보여 주고 승인을 받는다.
8. 정확한 title과 envelope로 Issue를 만들고 필요한 chunk를 모두 추가한 뒤 닫는다.
9. 결과 comment에서 성공 marker, path, commit을 확인한다.
10. 결과 commit ref에서 target file을 다시 읽고 실제 존재와 내용 반영을 확인한다.

`Recorded at`은 사용자가 입력하는 wire field가 아니다. GitHub Actions가 Issue의 변경되지 않는 `created_at`을 읽어 Learning Log Metadata에 UTC `YYYY-MM-DDTHH:MM:SSZ` 형식으로 자동 기록한다. 같은 `Date`의 Learning Log가 여러 개이면 context builder는 이 값을 실제 저장 요청 순서로 사용한다. 파일명과 target path 형식은 바뀌지 않는다.

Update에서는 기존 파일의 `Recorded at`을 그대로 보존하며 Issue 본문에 적힌 값은 사용하지 않는다. 기존 파일에 이 값이 없으면 임의 시각으로 채우지 않고 검증된 과거 Issue 시각을 별도 보완할 때까지 update를 거부한다.

일반 GitHub plugin에서는 현재 환경이 제공하는 Issue create, comment append, Issue close, Issue/comment read, repository file-read 기능을 사용한다. tool 이름은 plugin마다 다를 수 있으므로 capability를 기준으로 대응시킨다. `system/ACTION_SCHEMA.yaml`은 Custom GPT Action을 직접 설정할 때만 필요하며 일반 plugin 저장의 선행 읽기 파일이 아니다.

## 정확한 wire contract

Title:

```text
[learning-log] YYYY-MM-DD topic-slug
```

Create body의 첫 부분:

```text
<!-- research-os-ingest:v1
operation: create
target_path: learning-logs/YYYY/MM/YYYY-MM-DD-topic-slug.md
expected_sha: new
-->
```

Update는 `operation: update`와 방금 읽은 target file의 40자리 blob SHA를 사용한다. Envelope에는 `operation`, `target_path`, `expected_sha`만 허용된다. `mode` 같은 alias는 허용하지 않는다. Title의 날짜·slug는 target path와 같아야 한다.

## Evidence 품질 gate

- AI가 설명한 내용을 요약하는 대신 사용자의 설명, 추론, 질문, 비교와 수정 evidence를 중심에 둔다.
- `처음 이해 → 문제 또는 불확실성 → 수정된 이해`를 서로 다른 section에 보존한다.
- 중요한 실제 표현은 `## 사용자 원문`에 의미를 바꾸지 않고 남긴다.
- 해결된 질문과 미해결 질문을 구분한다.
- 자기 설명 checkbox는 대화에서 확인된 항목만 보수적으로 체크한다.
- 관련성이 있는 경우에만 AI semiconductor 또는 SSL 목표와 연결한다.
- 정보가 없으면 꾸며내지 않고 `아직 기록되지 않음` 또는 `없음`으로 둔다.
- 과거의 좋은 Issue는 품질 기준을 발견하는 evidence일 뿐 작성 template이 아니다. 과거 문장·서사·checkbox를 복제하지 않는다.

## 성공 판정

Issue 생성과 close는 enqueue다. 다음 세 조건이 모두 충족되어야 저장 완료다.

1. `✅ Learning Log 처리 완료` comment가 있다.
2. comment에 실제 path와 commit이 있다.
3. 해당 commit ref에서 target file을 읽을 수 있고 승인한 내용이 반영되어 있다.

결과가 아직 없으면 `접수 완료, 처리 확인 대기`, failure marker가 있으면 `저장 실패`라고 말한다.
