#!/usr/bin/env python3
"""Contract tests for build_learning_context.py."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import build_learning_context as context
from learning_log_metadata import load_domain_policy


def note(
    topic: str = "SRAM",
    domain: str = "sram",
    date: str = "2026-08-12",
    recorded_at: str | None = None,
    stage: str = "Stage 3 — Memory",
    concepts: int = 10,
    understanding: str = "기본 이해",
    questions: tuple[str, ...] = ("unresolved one", "unresolved two"),
) -> str:
    concept_lines = "\n".join(f"- concept {index}" for index in range(concepts))
    action_lines = "\n".join(f"{index}. action {index}" for index in range(1, 9))
    question_lines = "\n".join(f"- {item}" for item in questions)
    recorded_at_line = f"- Recorded at: {recorded_at}\n" if recorded_at else ""
    return f"""# 학습 기록: {topic}

## Metadata
- Date: {date}
{recorded_at_line}- Topic: {topic}
- Document type: learning-log
- Domain: {domain}
- Roadmap stage: {stage}

## 1. 오늘 공부한 목적
목적

## 2. 오늘 이해한 내용
{understanding}

## 3. 핵심 개념
{concept_lines}

## 4. 내가 처음 이해한 방식
초기 이해

## 5. 오해 또는 불확실한 부분
없음

## 6. 수정된 이해
수정

## 7. 질문
### 해결되지 않은 질문
{question_lines}
### 해결된 질문
- resolved must not appear

## 8. AI 반도체 및 SSL 목표와의 연결
연결

## 9. 다음 행동
{action_lines}

## 10. 자기 설명 점검
- [x] completed must not appear
- [ ] weak one
- [ ] weak two

## 사용자 원문
원문
"""


def paper_note(
    title: str,
    checkpoint_recorded_at: str,
    resume_point: str = "Section 3.2 / PDF p.6 / Figure 4부터 재개",
    bridge_statuses: tuple[str, ...] = (),
    paper_type: str = "foundational",
) -> str:
    bridge_lines = "\n".join(
        f"#### Bridge {index}\n\n- Status: {status}"
        for index, status in enumerate(bridge_statuses, start=1)
    ) or "- 없음"
    return f"""# Paper Note: {title}

## Metadata
- Title: {title}
- Document type: paper-note
- Paper type: {paper_type}
- Checkpoint recorded at: {checkpoint_recorded_at}

## 2. Reading Checkpoint
- Resume Point: {resume_point}

## 3. Prerequisite Bridge
### 논문 안에서 해결한 선수지식
- 없음
### 별도로 이어가는 선수지식
{bridge_lines}
"""


def write_fixture(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def setup_root(root: Path) -> None:
    repository_root = Path(__file__).resolve().parents[1]
    schema = (
        repository_root / "system/LEARNING_LOG_METADATA_SCHEMA.json"
    ).read_text(encoding="utf-8")
    write_fixture(root, "system/LEARNING_LOG_METADATA_SCHEMA.json", schema)
    write_fixture(root, "roadmap/ROADMAP.md", "# Roadmap\n")
    boundary = {
        "version": 1,
        "policy": "progression-over-exhaustiveness",
        "boundaries": [
            {
                "id": "sram-foundations",
                "current_topic": "SRAM",
                "progress_topics": ["SRAM"],
                "domains": ["sram"],
                "roadmap_stage": "Stage 3 — Memory",
                "topic_goal": "SRAM 기본 동작을 설명한다.",
                "minimum_required_understanding": ["Read Disturb", "Cell Ratio"],
                "exit_criteria": [
                    {
                        "text": "Read Disturb를 설명한다.",
                        "evidence_groups": [["Read Disturb"]],
                    },
                    {
                        "text": "Cell Ratio와 read stability 관계를 설명한다.",
                        "evidence_groups": [["Cell Ratio"], ["read stability"]],
                    },
                ],
                "blocking_question_keywords": ["Read Disturb", "Cell Ratio"],
                "optional_question_keywords": ["Sense Amplifier topology"],
                "optional_deep_dive": ["advanced Sense Amplifier topology"],
                "next_roadmap_topic": "SRAM/DRAM 비교",
            }
        ],
    }
    write_fixture(
        root,
        "roadmap/LEARNING_BOUNDARIES.json",
        json.dumps(boundary, ensure_ascii=False),
    )
    write_fixture(
        root,
        "roadmap/PROGRESS.md",
        "# Progress\n\n"
        "## 3. Current Focus\n\n"
        "- Current Boundary: sram-foundations\n",
    )


def assert_workflow_contract(repository_root: Path) -> None:
    workflow = (
        repository_root / ".github/workflows/learning-context-refresh.yml"
    ).read_text(encoding="utf-8")
    assert "learning-logs/**" in workflow
    assert "paper-notes/**" in workflow
    push_paths = workflow.split("paths:", 1)[1].split("workflow_run:", 1)[0]
    assert "state/CURRENT_LEARNING_CONTEXT.md" not in push_paths
    assert (
        'workflows: ["Learning Log Ingest", "Paper Note Ingest", "Progress Update"]'
        in workflow
    )
    assert "github.event.workflow_run.conclusion == 'success'" in workflow
    assert "github.event_name != 'workflow_run'" in workflow
    assert "group: research-os-main" in workflow
    assert '- "roadmap/PROGRESS.md"' in workflow
    assert '- "roadmap/ROADMAP.md"' in workflow
    assert '- "roadmap/LEARNING_BOUNDARIES.json"' in workflow
    assert '- "system/LEARNING_LOG_METADATA_SCHEMA.json"' in workflow
    assert '- "scripts/build_learning_context.py"' in workflow
    assert '- "scripts/learning_boundaries.py"' in workflow
    assert '- "scripts/test_build_learning_context.py"' in workflow
    assert '- ".github/workflows/learning-context-refresh.yml"' in workflow
    assert "python -B scripts/test_build_learning_context.py" in workflow
    assert "python -B scripts/build_learning_context.py" in workflow
    assert 'git add -- state/CURRENT_LEARNING_CONTEXT.md' in workflow
    assert "git add -A" not in workflow
    assert '[[ "${changed_paths[0]}" != "state/CURRENT_LEARNING_CONTEXT.md" ]]' in workflow
    for removed_path in (
        ".github/workflows/progress-reconciliation.yml",
        "scripts/build_progress_reconciliation.py",
        "scripts/progress_policy.py",
        "scripts/test_build_progress_reconciliation.py",
        "state/PROGRESS_RECONCILIATION.md",
    ):
        assert not (repository_root / removed_path).exists()


def main() -> int:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        lf = root / "lf.md"
        crlf = root / "crlf.md"
        lf.write_bytes(b"line\n")
        crlf.write_bytes(b"line\r\n")
        assert context.git_blob_sha(lf) == context.git_blob_sha(crlf)

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        write_fixture(root, "learning-logs/2026/08/older.md", note(topic="Older", date="2026-08-11"))
        write_fixture(
            root,
            "learning-logs/2026/08/z-latest.md",
            note(topic="Latest Z", recorded_at="2026-08-12T09:00:00Z"),
        )
        write_fixture(
            root,
            "learning-logs/2026/08/a-latest.md",
            note(topic="Latest A", recorded_at="2026-08-12T15:00:00Z"),
        )
        write_fixture(root, "learning-logs/2026/08/research-os.md", note(topic="System", domain="research-os"))
        write_fixture(
            root,
            "learning-logs/2026/08/ingest-smoke-test.md",
            note(topic="Ingest smoke test", domain="research-os"),
        )
        write_fixture(
            root,
            "learning-logs/2026/08/system-development.md",
            note(topic="System Stage", stage="system-development"),
        )
        write_fixture(root, "learning-logs/2026/08/invalid.md", note().replace("- Domain: sram\n", ""))
        write_fixture(
            root,
            "learning-logs/2026/08/invalid-date.md",
            note(topic="Invalid Date", date="2026-8-12"),
        )
        write_fixture(
            root,
            "learning-logs/2026/08/invalid-recorded-at.md",
            note(topic="Invalid Recorded At", recorded_at="2026-08-12 15:00"),
        )
        write_fixture(
            root,
            "learning-logs/2026/08/invalid-structure.md",
            note(topic="Invalid Structure").replace("# 학습 기록:", "# 메모:", 1),
        )
        write_fixture(
            root,
            "learning-logs/2026/08/invalid-domain.md",
            note(topic="Invalid Domain", domain="memory"),
        )

        included, excluded = context.discover_logs(root)
        assert [item.topic for item in included] == ["Older", "Latest Z", "Latest A"]
        assert any(path.endswith("research-os.md") and "research-os" in reason for path, reason in excluded)
        assert any(
            path.endswith("ingest-smoke-test.md") and "research-os" in reason
            for path, reason in excluded
        )
        assert any(
            path.endswith("system-development.md") and "system-development" in reason
            for path, reason in excluded
        )
        assert any(path.endswith("invalid.md") and "Metadata" in reason for path, reason in excluded)
        assert any(
            path.endswith("invalid-date.md") and "YYYY-MM-DD" in reason
            for path, reason in excluded
        )
        assert any(
            path.endswith("invalid-recorded-at.md") and "Recorded at" in reason
            for path, reason in excluded
        )
        assert any(
            path.endswith("invalid-structure.md") and "canonical" in reason
            for path, reason in excluded
        )
        assert any(
            path.endswith("invalid-domain.md")
            and "지원되지 않는 Domain metadata" in reason
            for path, reason in excluded
        )

        first = context.build_context(root)
        second = context.build_context(root)
        assert first == second
        progress_sha = context.git_blob_sha(root / "roadmap/PROGRESS.md")
        assert f"Progress source SHA: `{progress_sha}`" in first
        assert "최신 의미 있는 학습 기록: `learning-logs/2026/08/a-latest.md`" in first
        assert "Current Boundary: `sram-foundations`" in first
        assert "Current Stage: Stage 3 — Memory" in first
        assert "Current Topic: SRAM" in first
        assert "unresolved one" in first and "unresolved two" in first
        assert "resolved must not appear" not in first
        assert "weak one" in first and "weak two" in first
        assert "completed must not appear" not in first
        assert "action 1" in first and "action 6" in first
        assert "action 7" not in first
        assert "concept 0" in first and "concept 7" in first
        assert "concept 8" not in first
        assert first.count("같은 날짜의 의미 있는 학습 단위") == 1
        same_date = first.split("### 같은 날짜의 의미 있는 학습 단위", 1)[1].split(
            "## 현재 확인된 핵심 개념", 1
        )[0]
        assert same_date.index("z-latest.md") < same_date.index("a-latest.md")
        assert "## Roadmap Position" in first
        assert "## Topic Goal" in first
        assert "## Exit Criteria" in first
        assert "## Blocking Gaps" in first
        assert "## Optional Open Questions" in first
        assert "## Recommended Next Move" in first
        assert "## Required Source Before First Learning Unit" in first
        assert "## Next Roadmap Topic" in first
        assert "Decision: **continue**" in first
        required_source = first.split(
            "## Required Source Before First Learning Unit", 1
        )[1].split("## Next Roadmap Topic", 1)[0]
        assert "a-latest.md" in required_source
        assert "z-latest.md" in required_source
        assert "최신 의미 있는 Learning Log를 최대 2개" in required_source
        assert "Roadmap reconciliation" not in first

        original_glob = Path.glob
        try:
            Path.glob = lambda self, pattern: iter(reversed(list(original_glob(self, pattern))))
            reordered = context.build_context(root)
        finally:
            Path.glob = original_glob
        assert reordered == first

    # Regression: three logs on one date follow Issue time, not filename order.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        write_fixture(
            root,
            "learning-logs/2026/08/2026-08-22-sram-dram-sense-amplifier.md",
            note(date="2026-08-22", recorded_at="2026-08-22T05:09:33Z"),
        )
        write_fixture(
            root,
            "learning-logs/2026/08/2026-08-22-npu-sram-data-reuse-dataflow.md",
            note(date="2026-08-22", recorded_at="2026-08-22T09:54:52Z"),
        )
        write_fixture(
            root,
            "learning-logs/2026/08/2026-08-22-npu-pe-array-systolic-tiling.md",
            note(date="2026-08-22", recorded_at="2026-08-22T14:58:51Z"),
        )
        same_day = context.build_context(root)
        assert (
            "최신 의미 있는 학습 기록: "
            "`learning-logs/2026/08/2026-08-22-npu-pe-array-systolic-tiling.md`"
            in same_day
        )
        same_day_required = same_day.split(
            "## Required Source Before First Learning Unit", 1
        )[1].split("## Next Roadmap Topic", 1)[0]
        assert "2026-08-22-npu-sram-data-reuse-dataflow.md" in same_day_required
        assert "2026-08-22-npu-pe-array-systolic-tiling.md" in same_day_required
        assert "2026-08-22-sram-dram-sense-amplifier.md" not in same_day_required

    # Scenario A: a roadmap-required Cell Ratio gap remains.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        write_fixture(
            root,
            "learning-logs/2026/08/a.md",
            note(
                understanding="Read Disturb를 설명했다.",
                questions=("Cell Ratio는 read stability와 어떤 관계인가?",),
            ),
        )
        plan = context.build_context(root)
        assert "- [x] Read Disturb를 설명한다." in plan
        assert "- [ ] Cell Ratio와 read stability 관계를 설명한다." in plan
        assert "우선 학습: Cell Ratio와 read stability 관계를 설명한다." in plan

    # Scenario B/C: optional depth does not block advancement after all exit criteria.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        write_fixture(
            root,
            "learning-logs/2026/08/a.md",
            note(
                understanding="Read Disturb와 Cell Ratio가 read stability를 좌우한다.",
                questions=("advanced Sense Amplifier topology는 무엇인가?",),
            ),
        )
        plan = context.build_context(root)
        assert "Decision: **advance**" in plan
        assert "advanced Sense Amplifier topology는 무엇인가?" in plan
        assert "우선 학습: SRAM/DRAM 비교" in plan
        assert "`roadmap/LEARNING_BOUNDARIES.json`" in plan.split(
            "## Required Source Before First Learning Unit", 1
        )[1].split("## Next Roadmap Topic", 1)[0]
        assert "`learning-logs/2026/08/a.md`" in plan.split(
            "## Required Source Before First Learning Unit", 1
        )[1].split("## Next Roadmap Topic", 1)[0]

    # Scenario D: one remaining criterion produces a brief review then advance.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        write_fixture(
            root,
            "learning-logs/2026/08/a.md",
            note(understanding="Read Disturb를 설명했다.", questions=()),
        )
        plan = context.build_context(root)
        assert "Decision: **review_then_advance**" in plan
        assert "`learning-logs/2026/08/a.md`" in plan.split(
            "## Required Source Before First Learning Unit", 1
        )[1].split("## Next Roadmap Topic", 1)[0]

    # A fully aligned review does not rename the official boundary after the latest log.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        write_fixture(
            root,
            "learning-logs/2026/08/narrow.md",
            note(topic="SRAM Read Path Fundamentals", understanding="Read Disturb를 설명했다.", questions=()),
        )
        aligned_review = context.build_context(root)
        assert "Decision: **review_then_advance**" in aligned_review
        assert "Current Topic: SRAM" in aligned_review
        aligned_sha = context.git_blob_sha(root / "roadmap/PROGRESS.md")
        assert f"Progress source SHA: `{aligned_sha}`" in aligned_review

    # A Paper Reading Checkpoint, not a Learning Log or filename, selects Current Paper.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        write_fixture(
            root,
            "learning-logs/2026/08/2026-08-29-edram.md",
            note(
                topic="eDRAM",
                domain="memory-architecture",
                date="2026-08-29",
                recorded_at="2026-08-29T12:00:00Z",
            ),
        )
        write_fixture(
            root,
            "paper-notes/foundational/2026-08-27-z-old-paper.md",
            paper_note("Old Paper", "2026-08-27T12:00:00Z"),
        )
        write_fixture(
            root,
            "paper-notes/foundational/2026-08-26-a-current-paper.md",
            paper_note("Current Paper", "2026-08-28T12:00:00Z"),
        )
        selected = context.build_context(root)
        assert "## Current Paper" in selected
        assert (
            "Current Paper Note: "
            "`paper-notes/foundational/2026-08-26-a-current-paper.md`"
            in selected
        )
        assert "Last generated date: 2026-08-29" in selected

        invalid = paper_note(
            "Invalid Newest",
            "2026-08-30T12:00:00Z",
            bridge_statuses=("studying", "studying"),
        )
        write_fixture(
            root,
            "paper-notes/foundational/2026-08-30-invalid-newest.md",
            invalid,
        )
        still_selected = context.build_context(root)
        assert "2026-08-26-a-current-paper.md" in still_selected
        assert "2026-08-30-invalid-newest.md" not in still_selected

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        no_paper = context.build_context(root)
        assert "## Current Paper" in no_paper
        assert "Current Paper Note: 없음" in no_paper

    # Current Paper is still recoverable before the first Learning Log exists.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        write_fixture(
            root,
            "paper-notes/related/2026-08-27-paper-only.md",
            paper_note("Paper Only", "2026-08-27T03:04:05Z").replace(
                "- Paper type: foundational", "- Paper type: related", 1
            ),
        )
        paper_only = context.build_context(root)
        assert "최신 의미 있는 학습 기록: 없음" in paper_only
        assert (
            "Current Paper Note: `paper-notes/related/2026-08-27-paper-only.md`"
            in paper_only
        )
        assert "Last generated date: 2026-08-27" in paper_only

    # Scenario E is a session policy: deep dive is selectable only on explicit request.
    repository_root = Path(__file__).resolve().parents[1]
    domain_policy = load_domain_policy(repository_root)
    boundaries = context.load_boundaries(repository_root)
    boundary_domains = {
        domain for boundary in boundaries for domain in boundary.domains
    }
    assert domain_policy.learning_domains == boundary_domains
    progress_topics = {
        topic for boundary in boundaries for topic in boundary.progress_topics
    }
    for boundary in boundaries:
        assert boundary.current_topic in boundary.progress_topics
    for boundary in boundaries[:-1]:
        assert boundary.next_roadmap_topic in progress_topics
    sram_boundary = next(item for item in boundaries if item.id == "sram-foundations")
    assert "memory-architecture" in sram_boundary.evidence_domains
    entrypoint = (repository_root / "system/CHATGPT_ENTRYPOINT.md").read_text(encoding="utf-8")
    assert "optional_deep_dive" in entrypoint
    assert "명시적으로" in entrypoint
    assert "Required Source Before First Learning Unit" in entrypoint
    assert "모델의 일반 지식만으로 첫 질문을 만들지 않는다" in entrypoint
    assert "짧은 연결 설명과 쉬운 예시를 먼저 제공한 뒤" in entrypoint
    assert "Checkpoint 발생은 Learning Log 저장 제안을 의미하지 않는다" in entrypoint
    assert "단일 질문과 답변" in entrypoint
    assert "prerequisite가 저장 evidence 또는 현재 conversation에서 확인되었는지" in entrypoint
    assert "추론 질문은 최소한 하나의 관련 seed fact" in entrypoint
    assert "현재 세션의 Tutor 운영 제약" in entrypoint
    assert "`Current Paper Note`가 `없음`이 아니면 해당 Paper Note 전체를 읽는다" in entrypoint
    assert "Resume Point와 Bridge 상태는 Context 문구나 대화 기억으로 추측하지 않는다" in entrypoint
    assert "Current Paper가 있으면 해당 Paper Note 전체를 읽고" in entrypoint
    assert "`system/PAPER_READING_TUTOR_POLICY.md`를 전체 읽는다" in entrypoint

    actual = context.build_context(repository_root)
    actual_progress = (repository_root / "roadmap/PROGRESS.md").read_text(
        encoding="utf-8"
    )
    actual_focus = actual_progress.split("## 3. Current Focus", 1)[1].split(
        "\n## ", 1
    )[0]
    assert sum(
        line.startswith("- Current ") for line in actual_focus.splitlines()
    ) == 1
    assert "Current Stage" not in actual_progress
    assert "Current Topic" not in actual_progress
    assert "## 4. Progress Dashboard" in actual_progress
    assert "Last Updated" not in actual_progress
    expected_boundary_id = context.progress_value(actual_progress, "Current Boundary")
    expected_progress_sha = context.git_blob_sha(
        repository_root / "roadmap/PROGRESS.md"
    )
    expected_boundary = next(
        boundary for boundary in boundaries if expected_boundary_id == boundary.id
    )
    expected_stage = expected_boundary.roadmap_stage
    expected_topic = expected_boundary.current_topic
    actual_required_source = actual.split(
        "## Required Source Before First Learning Unit", 1
    )[1].split("## Next Roadmap Topic", 1)[0]
    assert f"- Current Boundary: `{expected_boundary_id}`" in actual
    assert f"- Current Stage: {expected_stage}" in actual
    assert f"- Current Topic: {expected_topic}" in actual
    assert f"- Depth Boundary: `{expected_boundary.id}`" in actual
    assert f"- Progress source SHA: `{expected_progress_sha}`" in actual
    assert "Roadmap reconciliation" not in actual
    assert actual_required_source.strip()
    actual_logs, _ = context.discover_logs(repository_root)
    if not any(
        log.domain in expected_boundary.evidence_domains for log in actual_logs
    ):
        assert "`roadmap/LEARNING_BOUNDARIES.json`" in actual_required_source
    for criterion in expected_boundary.exit_criteria:
        assert criterion.text in actual

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        write_fixture(root, "learning-logs/2026/08/system.md", note(domain="research-os"))
        empty = context.build_context(root)
        assert "최신 의미 있는 학습 기록: 없음" in empty
        assert "Roadmap reconciliation" not in empty
        assert "research-os" in empty

    assert_workflow_contract(repository_root)
    print("All learning context tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
