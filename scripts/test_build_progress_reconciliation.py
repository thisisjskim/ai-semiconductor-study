#!/usr/bin/env python3
"""Contract tests for build_progress_reconciliation.py."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import build_learning_context as context
import build_progress_reconciliation as reconciliation
from test_build_learning_context import note, write_fixture


PROGRESS = """# Progress

## 3. Current Focus

- Execution Phase: Phase 1 — Test
- Active Track: Track A — Test
- Current Deliverable: phase deliverable
- Current Bottleneck: phase bottleneck
- Next Milestone: phase milestone
- Phase Deadline: 2026-08-23
- Current Stage: Not Started
- Current Topic: 아직 지정되지 않음
- Last Updated: 2026-08-01

## 4. Progress Dashboard

| Stage | Status | 핵심 목표 | Evidence / Notes |
|---|---|---|---|
| Memory Architecture | Not Started | goal | - |
| SRAM / DRAM / eDRAM | Not Started | goal | - |
| Foundational Papers | Review | goal | existing |
"""


def setup_root(root: Path) -> None:
    write_fixture(root, "roadmap/ROADMAP.md", "# Roadmap\n")
    write_fixture(root, "roadmap/PROGRESS.md", PROGRESS)
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
            },
            {
                "id": "memory-architecture-foundations",
                "progress_topics": ["Memory Architecture"],
                "domains": ["memory-architecture"],
                "roadmap_stage": "Stage 3 — Memory",
                "topic_goal": "Memory hierarchy를 설명한다.",
                "minimum_required_understanding": ["Memory hierarchy"],
                "exit_criteria": [
                    {
                        "text": "Memory hierarchy를 설명한다.",
                        "evidence_groups": [["Memory Hierarchy"]],
                    }
                ],
                "blocking_question_keywords": ["Memory"],
                "optional_question_keywords": [],
                "optional_deep_dive": [],
                "next_roadmap_topic": "SRAM",
            },
        ],
    }
    write_fixture(
        root,
        "roadmap/LEARNING_BOUNDARIES.json",
        json.dumps(boundary, ensure_ascii=False),
    )


def assert_workflow_contract(repository_root: Path) -> None:
    workflow = (
        repository_root / ".github/workflows/progress-reconciliation.yml"
    ).read_text(encoding="utf-8")
    assert 'workflows: ["Learning Context Refresh"]' in workflow
    assert "github.event.workflow_run.conclusion == 'success'" in workflow
    assert "python -B scripts/test_build_progress_reconciliation.py" in workflow
    assert "python -B scripts/build_progress_reconciliation.py" in workflow
    assert 'git add -- state/PROGRESS_RECONCILIATION.md' in workflow
    assert "roadmap/PROGRESS.md" not in workflow.split("git add --", 1)[1]
    assert "git add -A" not in workflow
    assert '[[ "${changed_paths[0]}" != "state/PROGRESS_RECONCILIATION.md" ]]' in workflow


def main() -> int:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        write_fixture(
            root,
            "learning-logs/2026/08/memory.md",
            note(topic="Memory Hierarchy", domain="memory-architecture", date="2026-08-11"),
        )
        write_fixture(
            root,
            "learning-logs/2026/08/sram.md",
            note(topic="6T SRAM", domain="sram", date="2026-08-12"),
        )
        write_fixture(
            root,
            "learning-logs/2026/08/system.md",
            note(topic="System", domain="research-os", date="2026-08-13"),
        )
        write_fixture(
            root,
            "learning-logs/2026/08/paper.md",
            note(
                topic="Foundational Paper",
                domain="paper",
                date="2026-08-10",
                stage="Stage 6 — Foundational Papers",
            ),
        )

        progress_before = (root / "roadmap/PROGRESS.md").read_text(encoding="utf-8")
        first = reconciliation.build_reconciliation(root)
        second = reconciliation.build_reconciliation(root)
        assert (root / "roadmap/PROGRESS.md").read_text(encoding="utf-8") == progress_before
        assert first == second
        assert "Proposal status: **pending-approval**" in first
        assert "Latest evidence date: 2026-08-12" in first
        assert "| Current Stage | Not Started | Stage 3 — Memory |" in first
        assert "| Current Topic | 아직 지정되지 않음 | SRAM |" in first
        assert "| Current Topic | 아직 지정되지 않음 | 6T SRAM |" not in first
        assert "Next Milestone |" not in first
        assert "phase-level 계획이므로 자동 제안하지 않음" in first
        assert "| Memory Architecture | `Not Started` → `Learning`" in first
        assert "| SRAM / DRAM / eDRAM | `Not Started` → `Learning`" in first
        assert "| Foundational Papers | `Review` 유지" in first
        assert "Review` →" not in first
        assert "Maximum automatic status proposal: **Learning**" in first
        assert "Domain이 research-os" in first
        assert "별도 branch와 Pull Request" in first
        assert reconciliation.markdown_cell("a|b\nc") == "a\\|b c"

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        write_fixture(
            root,
            "roadmap/PROGRESS.md",
            PROGRESS.replace("- Current Stage: Not Started", "- Current Stage: Stage 3 — Memory")
            .replace("- Current Topic: 아직 지정되지 않음", "- Current Topic: 6T SRAM")
            .replace("- Last Updated: 2026-08-01", "- Last Updated: 2026-08-13")
            .replace("| SRAM / DRAM / eDRAM | Not Started |", "| SRAM / DRAM / eDRAM | Learning |"),
        )
        write_fixture(
            root,
            "learning-logs/2026/08/sram.md",
            note(topic="6T SRAM", domain="sram", date="2026-08-12"),
        )
        aligned = reconciliation.build_reconciliation(root)
        assert "Proposal status: **aligned**" in aligned
        assert "현재 학습 이동 판단상 공식 stage/topic 변경이 필요하지 않음" in aligned
        assert "`Learning` 유지" in aligned
        assert "phase milestone" not in aligned

    # A narrow Learning Log title is evidence, not the canonical Current Topic.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        write_fixture(
            root,
            "roadmap/PROGRESS.md",
            PROGRESS.replace("- Current Stage: Not Started", "- Current Stage: Stage 3 — Memory")
            .replace("- Current Topic: 아직 지정되지 않음", "- Current Topic: SRAM")
            .replace("| SRAM / DRAM / eDRAM | Not Started |", "| SRAM / DRAM / eDRAM | Learning |"),
        )
        write_fixture(
            root,
            "learning-logs/2026/08/sram.md",
            note(topic="SRAM Read Path Fundamentals", domain="sram", date="2026-08-12"),
        )
        narrow_topic = reconciliation.build_reconciliation(root)
        narrow_context = context.build_context(root)
        assert "Proposal status: **aligned**" in narrow_topic
        assert "Roadmap reconciliation: **aligned**" in narrow_context
        assert "SRAM Read Path Fundamentals |" not in narrow_topic
        assert "세부 Topic 제목을 공식 Current Topic으로 자동 승격하지 않음" in narrow_topic

    # Advancement proposes the configured next roadmap topic in both generated views.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        write_fixture(
            root,
            "roadmap/PROGRESS.md",
            PROGRESS.replace("- Current Stage: Not Started", "- Current Stage: Stage 3 — Memory")
            .replace("- Current Topic: 아직 지정되지 않음", "- Current Topic: SRAM")
            .replace("| SRAM / DRAM / eDRAM | Not Started |", "| SRAM / DRAM / eDRAM | Learning |"),
        )
        write_fixture(
            root,
            "learning-logs/2026/08/sram.md",
            note(
                topic="SRAM Read Path Fundamentals",
                domain="sram",
                date="2026-08-12",
                understanding="Read Disturb와 Cell Ratio가 read stability를 좌우한다.",
                questions=(),
            ),
        )
        advanced_proposal = reconciliation.build_reconciliation(root)
        advanced_context = context.build_context(root)
        assert "Proposal status: **pending-approval**" in advanced_proposal
        assert "Roadmap reconciliation: **pending-approval**" in advanced_context
        assert "Decision: **advance**" in advanced_context
        assert "| Current Topic | SRAM | SRAM/DRAM 비교 |" in advanced_proposal
        assert "| Current Topic | SRAM | SRAM Read Path Fundamentals |" not in advanced_proposal

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        empty = reconciliation.build_reconciliation(root)
        assert "Proposal status: **no-evidence**" in empty
        assert "진행 상태 변경을 제안하지 않음" in empty

    repository_root = Path(__file__).resolve().parents[1]
    assert_workflow_contract(repository_root)
    print("All progress reconciliation tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
