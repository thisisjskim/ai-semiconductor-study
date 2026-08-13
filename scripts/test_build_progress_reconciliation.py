#!/usr/bin/env python3
"""Contract tests for build_progress_reconciliation.py."""

from __future__ import annotations

import tempfile
from pathlib import Path

import build_progress_reconciliation as reconciliation
from test_build_learning_context import note, write_fixture


PROGRESS = """# Progress

| Stage | Status | 핵심 목표 | Evidence / Notes |
|---|---|---|---|
| Memory Architecture | Not Started | goal | - |
| SRAM / DRAM / eDRAM | Not Started | goal | - |
| Foundational Papers | Review | goal | existing |

- Current Stage: Not Started
- Current Topic: 아직 지정되지 않음
- Next Milestone: 첫 주제
- Last Updated: 2026-08-01
"""


def setup_root(root: Path) -> None:
    write_fixture(root, "roadmap/ROADMAP.md", "# Roadmap\n")
    write_fixture(root, "roadmap/PROGRESS.md", PROGRESS)


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
        assert "| Current Topic | 아직 지정되지 않음 | 6T SRAM |" in first
        assert "| Next Milestone | 첫 주제 | action 1 |" in first
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
        empty = reconciliation.build_reconciliation(root)
        assert "Proposal status: **no-evidence**" in empty
        assert "진행 상태 변경을 제안하지 않음" in empty

    repository_root = Path(__file__).resolve().parents[1]
    assert_workflow_contract(repository_root)
    print("All progress reconciliation tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
