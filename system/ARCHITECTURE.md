# Research OS Architecture

## 목적과 책임

| 구성 요소 | 책임 |
| --- | --- |
| GitHub Repository | 장기 기록의 Source of Truth. 정책, 상태 근거, 코드와 변경 이력을 보존한다. |
| 일반 ChatGPT | 학습 대화, 설명, 자기 설명 점검을 담당하는 Tutor Interface다. `system/CHATGPT_ENTRYPOINT.md`에서 시작한다. |
| Codex | 코드, 지침, 테스트, workflow를 branch에서 개발하는 Developer Interface다. |
| GitHub Issue | 승인된 Learning Log 또는 Progress Update 요청과 versioned envelope를 전달하는 queue다. Issue 생성·닫기는 처리 완료가 아니다. |
| GitHub Actions | Issue와 comments를 payload로 만들고 검증·저장·결과 회신을 연결하는 orchestration layer다. |
| `scripts/ingest_learning_log.py` | Learning Log 저장의 canonical validation 및 Markdown 변환 구현이다. 작성자, 제목, envelope, 경로, 문서 형식, create/update와 SHA를 검사한다. |
| `system/LEARNING_LOG_METADATA_SCHEMA.json` | Learning Log Domain의 단일 canonical enum이다. 작성 지침, 저장 validator와 context builder가 같은 값을 사용한다. |
| `scripts/apply_progress_update.py` | 승인된 Progress 제안의 SHA, evidence, 허용 필드, 현재 값과 상태 전이를 검증하고 `roadmap/PROGRESS.md`만 수정한다. |
| `scripts/progress_policy.py` | Current Learning Context와 Progress Reconciliation이 공유하는 stage/topic/dashboard 판정 규칙이다. Learning Log 제목은 evidence로만 취급하고 공식 topic 이동은 boundary 계약으로 결정한다. |
| `learning-logs/**` | 사용자의 자기 설명, 오해 수정, 질문과 다음 행동을 보존하는 학습 evidence다. |
| `roadmap/**` | 장기 학습 방향과 명시적으로 관리되는 진행 상태다. |
| `roadmap/LEARNING_BOUNDARIES.json` | Roadmap topic별 목표, 최소 이해, exit criteria, optional depth와 다음 topic을 기계적으로 읽을 수 있게 연결하는 운영 계약이다. |
| `state/**` | 빠른 context 복구와 진행표 검토를 위해 source를 압축한 generated/derived state다. current context와 progress reconciliation proposal을 포함한다. |
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

일반 ChatGPT는 entrypoint와 snapshot을 먼저 읽고 필요할 때만 관련 Learning Log와 roadmap을 확인한다. Learning Unit checkpoint에서 저장 승인을 받으면 `system/LEARNING_LOG_ISSUE_CONTRACT.md`의 tool-independent 계약으로 Issue를 enqueue한다. `system/ACTION_SCHEMA.yaml`은 별도로 구성한 Custom GPT Action interface에만 사용한다. `.github/workflows/learning-log-ingest.yml`은 Issue와 comments를 모아 `scripts/ingest_learning_log.py`에 전달한다. Python 검증을 통과한 한 개의 `learning-logs/**` 파일만 commit하며, 결과 comment의 path와 commit 및 실제 파일까지 확인해야 저장이 끝난다.

Learning Log 저장이 확인된 뒤 ChatGPT는 실제 evidence와 최신 `roadmap/PROGRESS.md`를 비교한다. 허용된 변경이 있을 때만 별도로 제안하고 두 번째 사용자 승인을 받는다. `[progress-update]` Issue를 닫으면 `.github/workflows/progress-update.yml`이 `scripts/apply_progress_update.py`로 요청을 검증하고 `roadmap/PROGRESS.md` 한 파일만 commit한다. ChatGPT는 성공 comment의 commit을 읽어 제안한 값이 실제 반영됐는지 확인한 뒤, 후속 context refresh까지 검증한다.

Learning Log 또는 Progress Update commit 이후 `.github/workflows/learning-context-refresh.yml`이 별도로 실행되어 `state/CURRENT_LEARNING_CONTEXT.md`만 다시 생성하고 별도 commit한다. Roadmap, learning boundary, context builder 또는 공유 progress policy가 변경되어도 같은 refresh를 실행한다. builder는 사용한 `roadmap/PROGRESS.md`의 Git blob SHA를 snapshot 상단의 `Progress source SHA`로 기록한다. 따라서 ChatGPT는 최신 Progress의 blob SHA와 이 값을 비교해 후속 refresh가 정확히 어느 Progress를 반영했는지 확인할 수 있다. builder는 Progress에서 현재 위치를 정하고, boundary의 exit criteria를 관련 Learning Log evidence와 비교한 뒤 Blocking Gap과 Optional Open Question을 분리한다. 첫 Blocking Gap과 keyword overlap이 가장 큰 Learning Log 한 개도 `Required Source Before First Learning Unit`으로 지정한다. 일반 ChatGPT는 두 SHA가 일치하는 최신 snapshot으로 방향을 정한 뒤 이 source를 읽어야 첫 설명이나 질문을 만들 수 있다. 세 main writer workflow는 쓰기를 직렬화하지만 실패 경계는 분리된다. Context refresh 실패는 이미 성공한 Learning Log 저장이나 Progress 변경을 되돌리지 않으며 `roadmap/PROGRESS.md`도 수정하지 않는다. 이 경우 ChatGPT는 Progress 변경 성공과 context 갱신 실패·대기를 분리해 알리고 stale snapshot으로 수업을 진행하지 않는다.

Context refresh가 성공하면 `.github/workflows/progress-reconciliation.yml`이 `scripts/build_progress_reconciliation.py`를 실행해 `state/PROGRESS_RECONCILIATION.md`만 갱신한다. 두 state builder는 `scripts/progress_policy.py`의 동일한 판정을 사용하므로 같은 evidence에 서로 다른 정합성 상태를 표시하지 않는다. 이 파일은 dashboard 변경 후보와 근거를 보여주는 제안서이며 canonical progress가 아니다. 자동화는 `roadmap/PROGRESS.md`를 stage하거나 commit하지 않는다. 사용자가 제안을 승인한 경우에만 승인된 범위를 `[progress-update]` Issue와 검증 workflow로 반영한다.

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
- 일반 ChatGPT 저장 계약: `system/LEARNING_LOG_ISSUE_CONTRACT.md`
- Custom GPT Action API schema: `system/ACTION_SCHEMA.yaml`
- 저장 검증 구현: `scripts/ingest_learning_log.py`, `scripts/apply_progress_update.py`
- Learning Log metadata enum: `system/LEARNING_LOG_METADATA_SCHEMA.json`
- 장기 방향, topic depth boundary와 명시적 진행표: `roadmap/ROADMAP.md`, `roadmap/LEARNING_BOUNDARIES.json`, `roadmap/PROGRESS.md`
- 학습 evidence: `learning-logs/**`
- 기록 형식: `templates/**`

`state/CURRENT_LEARNING_CONTEXT.md`와 `state/PROGRESS_RECONCILIATION.md`는 source of truth가 아니다. 각각 현재 학습 snapshot과 progress 변경 제안이며, Learning Log와 roadmap에서 다시 만들 수 있다. derived state와 source가 다르면 source를 확인하고 충돌을 드러내며, `roadmap/PROGRESS.md`를 자동으로 고치지 않는다.

최상위 `AGENTS.md`와 `system/CHATGPT_ENTRYPOINT.md`는 정책 복사본이 아니라 canonical source로 안내하는 router와 bootstrap이다.
