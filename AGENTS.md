# Repository Agent Router

이 저장소는 AI semiconductor, memory architecture, NPU, PIM/CIM과 관련 논문을 장기적으로 학습하고 연구 질문으로 발전시키는 Repository-native Research OS다.

## 시작할 때 읽을 문서

- 일반 ChatGPT 학습 시작점: `system/CHATGPT_ENTRYPOINT.md`
- 정책의 canonical source: `system/RESEARCH_OS.md`
- 현재 학습 상태: `state/CURRENT_LEARNING_CONTEXT.md`
- 장기 방향, topic depth boundary와 진행표: `roadmap/ROADMAP.md`, `roadmap/LEARNING_BOUNDARIES.json`, `roadmap/PROGRESS.md`
- Learning Log 형식: `templates/learning-log.md`
- Learning Log 저장 계약: `system/LEARNING_LOG_ISSUE_CONTRACT.md`
- Paper Note 형식과 작성 기준: `templates/paper-note.md`, `system/PAPER_NOTE_AUTHORING_GUIDE.md`
- Paper Reading Checkpoint 저장 계약: `system/PAPER_NOTE_ISSUE_CONTRACT.md`

## 작업 라우팅

- **일반 학습**: 현재 context와 관련 Learning Log를 확인하고 Tutor 흐름을 따른다. Current Paper가 있으면 해당 Paper Note를 읽어 Resume Point와 Prerequisite Bridge를 먼저 복구한다.
- **상태 진단**: `state/CURRENT_LEARNING_CONTEXT.md`, `roadmap/PROGRESS.md`, 실제 Learning Log를 비교한다. 사실과 추론, 충돌을 구분하고 승인 없이 상태표를 수정하지 않는다.
- **Research OS 개발**: 정책, 계약, workflow, script와 테스트를 실제로 읽고 별도 branch에서 변경한다.

Pull Request의 제목, 본문과 사용자에게 제공하는 변경 설명은 사용자가 달리 요청하지 않는 한 한국어로 작성한다.

Learning Log와 Paper Reading Checkpoint 저장은 사용자 승인 후 각각의 Issue → Actions → `learning-logs/**` 또는 `paper-notes/**` 경로를 사용한다. OS 코드·지침·상태 문서의 개발 변경은 branch → 테스트 → 검토 → PR → `main` merge 경로를 사용하며 `main`에 직접 넣지 않는다.

기존 기록이나 상태를 근거 없이 수정하지 말고, 경로와 파일 존재 여부를 확인한다. 이 파일에는 정책을 길게 복사하지 않는다. 세부 규칙은 위 canonical 문서를 참조한다.
