# Research OS Architecture

## 목적과 책임

| 구성 요소 | 책임 |
| --- | --- |
| GitHub Repository | 장기 기록의 Source of Truth. 정책, 상태 근거, 코드와 변경 이력을 보존한다. |
| 일반 ChatGPT | 학습 대화, 설명, 자기 설명 점검을 담당하는 Tutor Interface다. `system/CHATGPT_ENTRYPOINT.md`에서 시작한다. |
| Codex | 코드, 지침, 테스트, workflow를 branch에서 개발하는 Developer Interface다. |
| GitHub Issue | 승인된 Learning Log 저장 요청과 versioned envelope를 전달하는 queue다. Issue 생성·닫기는 저장 완료가 아니다. |
| GitHub Actions | Issue와 comments를 payload로 만들고 검증·저장·결과 회신을 연결하는 orchestration layer다. |
| `scripts/ingest_learning_log.py` | Learning Log 저장의 canonical validation 및 Markdown 변환 구현이다. 작성자, 제목, envelope, 경로, 문서 형식, create/update와 SHA를 검사한다. |
| `learning-logs/**` | 사용자의 자기 설명, 오해 수정, 질문과 다음 행동을 보존하는 학습 evidence다. |
| `roadmap/**` | 장기 학습 방향과 명시적으로 관리되는 진행 상태다. |
| `state/**` | 빠른 context 복구를 위해 source를 압축한 generated/derived state다. `scripts/build_learning_context.py`가 생성한다. |
| `system/**` | Research OS의 정책, 진입점, 구조와 저장 계약이다. |
| `templates/**` | Learning Log 등 기록의 형식을 정의한다. |
| Custom GPT | 당분간 유지되는 legacy/fallback interface다. 정책의 유일한 보관 장소로 사용하지 않는다. |

## A. 학습 흐름

```text
GitHub context load
→ ChatGPT 학습 대화
→ 저장 시점 감지
→ 사용자 승인
→ Issue 생성
→ GitHub Actions 실행
→ Python 검증
→ Learning Log commit
→ Actions 성공과 결과 comment 확인
```

ChatGPT는 snapshot을 먼저 읽되 관련 Learning Log와 roadmap을 확인한다. 저장 승인을 받으면 `system/ACTION_SCHEMA.yaml`의 계약으로 Issue를 enqueue한다. `.github/workflows/learning-log-ingest.yml`은 Issue와 comments를 모아 `scripts/ingest_learning_log.py`에 전달한다. Python 검증을 통과한 한 개의 `learning-logs/**` 파일만 commit하며, 결과 comment의 path와 commit까지 확인해야 저장이 끝난다.

Learning Log 저장 commit 이후 `.github/workflows/learning-context-refresh.yml`이 별도로 실행되어 `state/CURRENT_LEARNING_CONTEXT.md`만 다시 생성하고 별도 commit한다. 두 workflow는 main 쓰기를 직렬화하지만 실패 경계는 분리된다. Context refresh 실패는 이미 성공한 Learning Log 저장을 되돌리지 않으며 `roadmap/PROGRESS.md`도 수정하지 않는다.

## B. Research OS 개발 흐름

```text
요구사항 확인
→ Codex 진단
→ branch에서 구현
→ 테스트
→ 사용자 검토
→ Pull Request
→ main merge
```

OS 정책·문서·코드·workflow 변경은 Learning Log Issue 경로와 분리한다. Codex는 실제 파일과 현재 `main`을 확인하고, 관련 테스트를 실행하며, 사용자 검토 전 임의로 `main`에 직접 개발 변경을 넣지 않는다.

## Canonical source와 derived state

Canonical source는 판단을 다시 만들 수 있는 원본이다.

- 운영·학습 정책: `system/RESEARCH_OS.md`
- 저장 API 계약: `system/ACTION_SCHEMA.yaml`
- 저장 검증 구현: `scripts/ingest_learning_log.py`
- 장기 방향과 명시적 진행표: `roadmap/ROADMAP.md`, `roadmap/PROGRESS.md`
- 학습 evidence: `learning-logs/**`
- 기록 형식: `templates/**`

`state/CURRENT_LEARNING_CONTEXT.md`는 source of truth가 아니다. `scripts/build_learning_context.py`가 Learning Log와 roadmap을 읽어 만든 generated/derived snapshot이며, 빠른 시작을 돕는다. snapshot과 source가 다르면 source를 확인하고 충돌을 드러내며, `roadmap/PROGRESS.md`를 자동으로 고치지 않는다.

최상위 `AGENTS.md`와 `system/CHATGPT_ENTRYPOINT.md`는 정책 복사본이 아니라 canonical source로 안내하는 router와 bootstrap이다.
