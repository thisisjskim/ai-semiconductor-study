# Current Learning Context

> 이 문서는 빠른 context 복구를 위한 derived snapshot이다. Source of truth는 아래에 명시한 Learning Log와 roadmap이며, 차이가 있으면 source를 다시 확인한다.

- Last updated: 2026-08-12
- Roadmap reconciliation: **pending**

## 현재 상태

- **활성 학습 영역 — 추론:** Computer Architecture에서 Memory Architecture로 넘어가는 구간(Stage 2 → Stage 3).
- **현재 학습 주제 — 사실:** Memory Hierarchy와 Data Reuse.
- **마지막 의미 있는 학습 기록 — 사실:** `learning-logs/2026/08/2026-08-09-memory-hierarchy-data-reuse.md`.

## 확인된 이해

다음은 위 Learning Log에 자기 설명과 오해 수정으로 기록된 사실이다.

- MAC을 늘려도 memory가 데이터를 충분히 공급하지 못하면 bandwidth bottleneck으로 연산기가 기다릴 수 있다.
- Latency는 한 access의 대기 시간이고, Bandwidth는 단위 시간당 전송량이다.
- `Off-chip DRAM/HBM → On-chip SRAM → Register → MAC`의 단순화된 hierarchy와, 가까운 memory에서의 Data Reuse가 off-chip data movement를 줄인다는 목적을 설명했다.
- Register와 SRAM은 저장 공간이고 MAC은 연산 회로라는 역할 구분, inference와 training의 차이에 관한 초기 혼동을 수정했다.

## 아직 약한 부분과 미해결 질문

- **비교 능력 — 사실:** 자기 설명 점검에서 관련 개념 비교가 아직 완료되지 않았다.
- Register가 실제로 어떤 회로로 구성되며 SRAM과 어떻게 다른가?
- SRAM과 DRAM은 구조와 동작 방식에서 어떻게 다른가?
- NPU에서 Register, SRAM, PE/MAC array는 실제로 어떻게 연결되는가?
- Weight, activation, partial sum의 배치에 따라 NPU Dataflow가 어떻게 달라지는가?

## 바로 다음 학습

**추천: Register와 SRAM의 역할 차이.** 이는 마지막 의미 있는 Learning Log의 첫 번째 다음 행동이며, 그 뒤의 `SRAM과 DRAM 비교 → NPU에서 Register/SRAM/PE 연결 → NPU Dataflow`를 이해하기 위한 가장 가까운 선수 주제다.

## 참고한 source paths

- `roadmap/ROADMAP.md`
- `roadmap/PROGRESS.md`
- `learning-logs/2026/08/2026-08-09-memory-hierarchy-data-reuse.md`

## 검토했지만 학습 근거에서 제외한 기록

- `learning-logs/2026/08/2026-08-07-custom-gpt-github-integration.md`: GitHub 연동과 Research OS 저장 방식에 관한 시스템 개발 기록으로, AI semiconductor 개념 학습 성취의 근거가 아니다.
- `learning-logs/2026/08/2026-08-12-ingest-contract-smoke-test.md`: create/update pipeline을 확인한 운영 smoke test로, 학습 성취의 근거가 아니다.

## Roadmap reconciliation

`roadmap/PROGRESS.md`는 2026-08-07 기준으로 모든 Stage를 `Not Started`, 현재 주제를 미지정으로 표시한다. 그러나 2026-08-09 Learning Log에는 Memory Hierarchy, Data Reuse, latency/bandwidth와 NPU 연결에 대한 실제 학습 evidence가 있다. 두 source가 충돌하므로 이 snapshot에서는 상태를 임의로 확정하거나 `PROGRESS.md`를 수정하지 않고 **reconciliation pending**으로 둔다.
