# Paper Note Issue Contract

이 문서는 일반 ChatGPT와 GitHub plugin이 하나의 Paper Reading Checkpoint를 Paper Note에 저장하기 직전에 확인하는 계약이다.

- Human-readable Issue wire contract: 이 문서
- Markdown structure: `templates/paper-note.md`
- Executable validation: `scripts/ingest_paper_note.py`
- Evidence-based authoring: `system/PAPER_NOTE_AUTHORING_GUIDE.md`
- Approval and verification policy: `system/RESEARCH_OS.md`

## 저장 전 필수 순서

1. 현재 `state/CURRENT_LEARNING_CONTEXT.md`가 가리키는 Paper Note 또는 새로 만들 대상 경로를 확인한다.
2. Update이면 `main`의 기존 Paper Note 전체와 40자리 blob SHA를 읽는다.
3. `templates/paper-note.md`와 `system/PAPER_NOTE_AUTHORING_GUIDE.md`를 읽고 전체 canonical Markdown을 작성한다. Metadata의 제목·저자·Paper link가 이번 채팅에서 PDF Source Gate를 통과한 첨부 PDF의 identity와 일치하는지 확인한다. 임시 attachment 경로나 과거 conversation URL은 저장하지 않는다.
4. `studying` Bridge를 저장하거나 다른 Learning Log를 연결하면 해당 Log의 성공 comment, commit과 실제 파일을 먼저 확인한다. 저장된 `studying`에는 실제 Learning Log 경로가 하나 이상 필요하다.
5. 사용자에게 create/update, target path, Resume Point, Bridge 변화와 변경 전·후 상태창을 보여 주고 승인을 받는다.
6. 정확한 title과 envelope로 Issue를 만들고 필요한 chunk를 모두 추가한 뒤 닫는다.
7. 결과 comment에서 성공 marker, path, commit과 Checkpoint recorded at을 확인한다.
8. 결과 commit ref에서 Paper Note를 다시 읽어 승인 내용이 반영됐는지 확인한다.
9. 이어지는 Learning Context Refresh에서 Current Paper가 해당 경로로 갱신됐는지 확인한다.

## Checkpoint 시간

`Checkpoint recorded at`은 사용자가 입력하는 wire field가 아니다. GitHub Actions가 Issue의 변경되지 않는 `created_at`을 UTC `YYYY-MM-DDTHH:MM:SSZ`로 자동 기록한다. Update 때도 이번 Paper Reading Checkpoint의 Issue 시각으로 갱신한다.

Context 생성기는 파일명, Git 수정 시각이나 최신 Learning Log가 아니라 유효한 Paper Note의 `Checkpoint recorded at`을 비교해 Current Paper를 결정한다.

## 정확한 wire contract

Title:

```text
[paper-note] paper-slug
```

Body의 첫 부분:

```text
<!-- research-os-paper-note:v1
operation: create
intent: paper-reading-checkpoint
target_path: paper-notes/foundational/YYYY-MM-DD-paper-slug.md
expected_sha: new
-->
```

Update는 `operation: update`와 방금 읽은 target file의 40자리 blob SHA를 사용한다. Envelope에는 `operation`, `intent`, `target_path`, `expected_sha`만 허용한다. `intent`는 `paper-reading-checkpoint`만 허용한다.

Issue 제목의 slug는 target path의 날짜 뒤 slug와 같아야 한다. Paper Note 파일명 날짜는 최초 생성일이며 Update Issue 날짜와 맞출 필요가 없다.

## 사용자 승인과 두 기록 연결

별도 선수지식 Learning Log와 Paper Note를 함께 갱신할 때 변경 예정 파일과 내용을 한꺼번에 보여 주고 한 번 승인받을 수 있다. 승인 뒤에는 다음 두 요청을 순서대로 처리한다.

1. Learning Log Issue를 처리하고 실제 저장을 검증한다.
2. 검증된 Learning Log 경로를 포함한 Paper Note Issue를 처리한다.

Learning Log 저장이 실패하면 Paper Note에 존재하지 않는 경로를 추가하지 않는다. 한 단계만 성공하면 부분 성공으로 보고하고 전체 완료라고 말하지 않는다.

## 성공 판정

Issue 생성과 close는 enqueue다. 다음 조건이 모두 충족되어야 Paper Note 저장 완료다.

1. `✅ Paper Note 처리 완료` comment가 있다.
2. comment에 operation, path, commit과 Checkpoint recorded at이 있다.
3. 해당 commit ref에서 target Paper Note를 읽을 수 있고 승인한 내용이 반영되어 있다.
4. 후속 Context가 같은 Paper Note를 Current Paper로 표시한다.

Context 갱신 전에는 `Paper Note 저장 성공, 상태 갱신 확인 대기`로 구분한다.
