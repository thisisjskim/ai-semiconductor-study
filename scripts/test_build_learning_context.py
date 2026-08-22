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
    stage: str = "Stage 3 — Memory",
    concepts: int = 10,
    understanding: str = "기본 이해",
    questions: tuple[str, ...] = ("unresolved one", "unresolved two"),
) -> str:
    concept_lines = "\n".join(f"- concept {index}" for index in range(concepts))
    action_lines = "\n".join(f"{index}. action {index}" for index in range(1, 9))
    question_lines = "\n".join(f"- {item}" for item in questions)
    return f"""# 학습 기록: {topic}

## Metadata
- Date: {date}
- Topic: {topic}
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
        "| Stage | Status |\n"
        "|---|---|\n"
        "| SRAM / DRAM / eDRAM | Not Started |\n"
        "- Current Stage: Not Started\n"
        "- Current Topic: SRAM\n",
    )


def assert_workflow_contract(repository_root: Path) -> None:
    workflow = (
        repository_root / ".github/workflows/learning-context-refresh.yml"
    ).read_text(encoding="utf-8")
    assert "learning-logs/**" in workflow
    push_paths = workflow.split("paths:", 1)[1].split("workflow_run:", 1)[0]
    assert "state/CURRENT_LEARNING_CONTEXT.md" not in push_paths
    assert 'workflows: ["Learning Log Ingest", "Progress Update"]' in workflow
    assert "github.event.workflow_run.conclusion == 'success'" in workflow
    assert "group: research-os-main" in workflow
    assert '- "roadmap/PROGRESS.md"' in workflow
    assert '- "roadmap/ROADMAP.md"' in workflow
    assert '- "roadmap/LEARNING_BOUNDARIES.json"' in workflow
    assert '- "system/LEARNING_LOG_METADATA_SCHEMA.json"' in workflow
    assert "python -B scripts/test_build_learning_context.py" in workflow
    assert "python -B scripts/build_learning_context.py" in workflow
    assert 'git add -- state/CURRENT_LEARNING_CONTEXT.md' in workflow
    assert "git add -A" not in workflow
    assert '[[ "${changed_paths[0]}" != "state/CURRENT_LEARNING_CONTEXT.md" ]]' in workflow


def main() -> int:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        write_fixture(root, "learning-logs/2026/08/older.md", note(topic="Older", date="2026-08-11"))
        write_fixture(root, "learning-logs/2026/08/z-latest.md", note(topic="Latest Z"))
        write_fixture(root, "learning-logs/2026/08/a-latest.md", note(topic="Latest A"))
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
            "learning-logs/2026/08/invalid-structure.md",
            note(topic="Invalid Structure").replace("# 학습 기록:", "# 메모:", 1),
        )
        write_fixture(
            root,
            "learning-logs/2026/08/invalid-domain.md",
            note(topic="Invalid Domain", domain="memory"),
        )

        included, excluded = context.discover_logs(root)
        assert [item.topic for item in included] == ["Older", "Latest A", "Latest Z"]
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
        assert "`learning-logs/2026/08/z-latest.md`" in first
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
        assert same_date.index("a-latest.md") < same_date.index("z-latest.md")
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
        assert "z-latest.md" in required_source
        assert "Roadmap reconciliation: **pending-approval**" in first
        assert "dashboard 상태가 Not Started" in first

        original_glob = Path.glob
        try:
            Path.glob = lambda self, pattern: iter(reversed(list(original_glob(self, pattern))))
            reordered = context.build_context(root)
        finally:
            Path.glob = original_glob
        assert reordered == first

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
        assert "Roadmap reconciliation: **pending-approval**" in plan
        assert "`learning-logs/2026/08/a.md`" in plan.split(
            "## Required Source Before First Learning Unit", 1
        )[1].split("## Next Roadmap Topic", 1)[0]

    # A fully aligned review does not rename the roadmap topic after the latest log.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        write_fixture(
            root,
            "roadmap/PROGRESS.md",
            (root / "roadmap/PROGRESS.md").read_text(encoding="utf-8")
            .replace("- Current Stage: Not Started", "- Current Stage: Stage 3 — Memory")
            .replace("| SRAM / DRAM / eDRAM | Not Started |", "| SRAM / DRAM / eDRAM | Learning |"),
        )
        write_fixture(
            root,
            "learning-logs/2026/08/narrow.md",
            note(topic="SRAM Read Path Fundamentals", understanding="Read Disturb를 설명했다.", questions=()),
        )
        aligned_review = context.build_context(root)
        assert "Decision: **review_then_advance**" in aligned_review
        assert "Roadmap reconciliation: **aligned**" in aligned_review
        assert "Current Topic: SRAM" in aligned_review

    # Scenario E is a session policy: deep dive is selectable only on explicit request.
    repository_root = Path(__file__).resolve().parents[1]
    domain_policy = load_domain_policy(repository_root)
    boundaries = context.load_boundaries(repository_root)
    boundary_domains = {
        domain for boundary in boundaries for domain in boundary.domains
    }
    assert domain_policy.learning_domains == boundary_domains
    assert domain_policy.learning_domains == frozenset(context.DASHBOARD_LABELS)
    entrypoint = (repository_root / "system/CHATGPT_ENTRYPOINT.md").read_text(encoding="utf-8")
    assert "optional_deep_dive" in entrypoint
    assert "명시적으로" in entrypoint
    assert "Required Source Before First Learning Unit" in entrypoint
    assert "모델의 일반 지식만으로 첫 질문을 만들지 않는다" in entrypoint
    assert "짧은 연결 설명과 쉬운 예시를 먼저 제공한 뒤" in entrypoint

    actual = context.build_context(repository_root)
    actual_required_source = actual.split(
        "## Required Source Before First Learning Unit", 1
    )[1].split("## Next Roadmap Topic", 1)[0]
    assert "2026-08-12-register-sram-circuits.md" in actual_required_source

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        write_fixture(root, "learning-logs/2026/08/system.md", note(domain="research-os"))
        empty = context.build_context(root)
        assert "최신 의미 있는 학습 기록: 없음" in empty
        assert "Roadmap reconciliation: **not-needed**" in empty
        assert "research-os" in empty

    assert_workflow_contract(repository_root)
    print("All learning context tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
