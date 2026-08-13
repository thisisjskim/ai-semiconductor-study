# Progress Reconciliation Proposal

> 이 문서는 Learning Log evidence와 `roadmap/PROGRESS.md`를 비교해 자동 생성한 검토용 제안서다. `roadmap/PROGRESS.md`를 수정하지 않으며, 아래 변경은 사용자 승인 후 별도 branch와 Pull Request에서만 적용한다.

- Proposal status: **aligned**
- Latest evidence date: 2026-08-12
- Maximum automatic status proposal: **Learning**

## 현재 포커스 변경 제안

| Field | 현재 값 | 제안 값 |
| --- | --- | --- |
| 없음 | 변경 제안 없음 | Progress의 Last Updated가 최신 Learning Log evidence보다 새로움 |

## Dashboard 변경 제안

| Stage | 상태 제안 | 근거 Learning Log |
| --- | --- | --- |
| SRAM / DRAM / eDRAM | `Learning` 유지 | `learning-logs/2026/08/2026-08-12-register-sram-circuits.md` |

## 판단 제한

- Learning Log가 존재한다는 사실만으로 `Review` 또는 `Completed`를 제안하지 않음
- 기존 `Review` 또는 `Completed` 상태를 자동으로 낮추지 않음
- `Execution Phase`, `Active Track`, `Current Deliverable`, `Current Bottleneck`, `Next Milestone`, `Phase Deadline`은 phase-level 계획이므로 자동 제안하지 않음
- Progress가 최신 Learning Log보다 새로우면 과거 evidence로 현재 focus를 되돌리지 않음
- Metadata로 dashboard row를 안전하게 특정할 수 없는 기록은 상태 변경 근거로 사용하지 않음
- 실제 반영 전 사용자가 stage, topic, status와 evidence를 검토해야 함

## 사용한 source paths

- `roadmap/ROADMAP.md`
- `roadmap/PROGRESS.md`
- `learning-logs/2026/08/2026-08-12-register-sram-circuits.md`

## 제외한 기록과 이유

- `learning-logs/2026/08/2026-08-09-memory-hierarchy-data-reuse.md` — 필수 Metadata 누락: Document type, Domain, Roadmap stage

## 승인 후 적용 절차

1. 사용자가 이 제안의 적용 범위를 명시적으로 승인한다.
2. Codex가 최신 `main`에서 별도 branch를 만든다.
3. 승인된 항목만 `roadmap/PROGRESS.md`에 반영한다.
4. 검증 후 Pull Request를 만들고 사용자가 검토·merge한다.
