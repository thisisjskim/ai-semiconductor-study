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
3. 새 Paper Note 또는 paper-source 분석 section을 바꾸는 일반 update이면 `templates/paper-note.md`와 `system/PAPER_NOTE_AUTHORING_GUIDE.md`를 읽고 전체 canonical Markdown을 작성한다. 사용자와의 학습으로 Resume Point, Reading Session History, 사용자 분석 근거와 Prerequisite Bridge를 바꾸는 checkpoint이면 아래 v2 delta를 작성하고 기존 전체 문서를 재전송하지 않는다. Metadata의 제목·저자·Paper link는 이번 채팅에서 PDF Source Gate를 통과한 첨부 PDF의 identity와 일치해야 하며 임시 attachment 경로나 과거 conversation URL은 저장하지 않는다.
4. `studying` Bridge를 저장하거나 다른 Learning Log를 연결하면 해당 Log의 성공 comment, commit과 실제 파일을 먼저 확인한다. 저장된 `studying`에는 실제 Learning Log 경로가 하나 이상 필요하다.
5. 사용자에게 create/update, target path, Resume Point, Bridge 변화와 변경 전·후 상태창을 보여 주고 승인을 받는다.
6. 정확한 title과 envelope로 Issue를 만들고 필요한 chunk를 모두 추가한 뒤 닫는다.
7. 결과 comment에서 성공 marker, path, commit과 Checkpoint recorded at을 확인한다.
8. 결과 commit ref에서 Paper Note를 다시 읽어 승인 내용이 반영됐는지 확인한다.
9. 이어지는 Learning Context Refresh에서 Current Paper가 해당 경로로 갱신됐는지 확인한다.

Bridge 변화에는 사용자가 직접 PB 기록을 요청했거나 GPT의 제안에 명시적으로 동의한 개념만 포함한다. Paper Note 또는 checkpoint 전체의 저장 승인을 지정되지 않은 PB 항목 추가 승인으로 사용하지 않는다.

## Checkpoint 시간

`Checkpoint recorded at`은 사용자가 입력하는 wire field가 아니다. GitHub Actions가 Issue의 변경되지 않는 `created_at`을 UTC `YYYY-MM-DDTHH:MM:SSZ`로 자동 기록한다. Update 때도 이번 Paper Reading Checkpoint의 Issue 시각으로 갱신한다.

Context 생성기는 파일명, Git 수정 시각이나 최신 Learning Log가 아니라 유효한 Paper Note의 `Checkpoint recorded at`을 비교해 Current Paper를 결정한다.

## 정확한 wire contract

### v1: create와 전체 문서 update

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

### v2: 작은 reading checkpoint delta

기존 paper-source 분석 section을 바꾸지 않고 두 번째 cycle의 Resume Point, Reading Session History, 사용자 분석 근거, Prerequisite Bridge, User-Identified Limitations, Questions와 Research Connection을 갱신할 때는 전체 Paper Note 대신 다음 JSON delta를 보낸다.

```text
<!-- research-os-paper-note:v2
operation: checkpoint-update
intent: paper-reading-checkpoint
target_path: paper-notes/foundational/YYYY-MM-DD-paper-slug.md
expected_sha: <방금 읽은 target file의 40자리 blob SHA>
-->
{
  "resume_point": "다음 세션에서 재개할 정확한 위치",
  "reading_session_history": {
    "date": "YYYY-MM-DD",
    "read_range": "이번 세션에서 읽은 범위",
    "understood": "확인된 이해",
    "questions": "Question Selection Gate를 통과한 질문과 해결 상태 또는 선정된 질문 없음",
    "bridge_changes": "변경 내용 또는 변경 없음",
    "ending_resume_point": "종료 당시 Resume Point"
  },
  "user_analysis_evidence": ["사용자의 실제 표현"],
  "prerequisite_bridge": {
    "resolved_upsert": [{
      "concept": "논문 안에서 해결한 개념",
      "location": "논문 위치",
      "reason": "논문에서 필요한 이유",
      "definition": "사용자 이해와 분리된 실제 정의",
      "user_understanding": "자연어 understanding evidence"
    }],
    "tracked_upsert": [{
      "concept": "별도로 이어가는 개념",
      "status": "studying | paused | sufficient-for-paper",
      "reason": "논문에서 필요한 이유",
      "sufficient_criterion": "이 논문에 충분한 기준",
      "learning_logs": ["learning-logs/YYYY/MM/YYYY-MM-DD-topic.md"]
    }]
  },
  "user_identified_limitations_upsert": [{
    "title": "사용자 limitation 제목",
    "limitation": "사용자가 지적한 limitation",
    "related_architecture_method": "관련 Architecture / Method",
    "user_basis": "사용자가 근거로 사용한 paper content",
    "paper_direct": "Paper에서 직접 확인된 내용",
    "needs_confirmation": "추가 확인이 필요한 부분"
  }],
  "questions_upsert": [{
    "category": "understanding | critical | follow-up-research",
    "title": "질문 제목",
    "user_question": "사용자의 질문",
    "context": "발생 위치 또는 맥락",
    "selection_reason": "선정 이유",
    "resolution_process": "해결 과정",
    "learned": "해결하며 알게 된 내용",
    "resolution_status": "resolved | partially-resolved | unresolved",
    "unresolved": "해결하지 못한 부분 또는 해당 없음",
    "evidence": {
      "paper_direct": "Paper direct evidence",
      "gpt_supplementary": "GPT supplementary explanation",
      "user_interpretation": "User interpretation / hypothesis"
    }
  }],
  "research_connections_upsert": [{
    "title": "연결 제목",
    "user_interest": "사용자가 표현한 research interest 또는 goal",
    "paper_element": "연결되는 Paper element",
    "evidence_location": "연결 근거 위치",
    "connection": "연결 방식",
    "role": "이 논문이 내 연구 방향에서 수행하는 역할",
    "questions_limitations_relation": "기존 Questions / Limitations와의 관계",
    "boundary": "연결의 경계 또는 아직 확인되지 않은 부분",
    "future_use": "향후 활용"
  }]
}
```

`resume_point`와 `reading_session_history`는 필수이고 나머지 delta field는 변화가 없으면 생략할 수 있다. PB는 concept 이름, 나머지 conversation-derived record는 category와 title을 기준으로 새 항목을 추가하거나 기존 항목만 교체한다. 기존 Bridge 검증과 전체 canonical Markdown 검증은 병합 결과에 다시 적용한다. 첫 번째 cycle의 paper-source section과 세 번째 cycle의 Final Summary를 바꿀 때만 v1 전체 update를 사용한다.

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
