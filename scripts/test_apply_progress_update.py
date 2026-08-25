#!/usr/bin/env python3
"""Contract tests for apply_progress_update.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import apply_progress_update as progress
import build_learning_context as learning_context
from test_build_learning_context import note, setup_root, write_fixture


PROGRESS = """# AI Semiconductor Research Progress

## 3. Current Focus

- Execution Phase: Phase 1 — Memory Bridge and Paper Scouting
- Active Track: Track A — Essential Foundations
- Current Stage: Stage 3 — Memory
- Current Topic: 6T SRAM
- Current Deliverable: explain SRAM
- Current Bottleneck: read disturb
- Next Milestone: NPU buffer
- Phase Deadline: 2026-08-23
- Last Updated: 2026-08-13

## 4. Progress Dashboard

| Stage | Status | 현재 목표 | Evidence / Notes |
| --- | --- | --- | --- |
| NPU Architecture | Not Started | PE array와 buffer | Phase 2 |
| PIM / CIM | Not Started | data movement | Phase 3 |

## 5. Application Deliverables
"""


def make_root(temp: str) -> Path:
    root = Path(temp)
    target = root / progress.TARGET_PATH
    target.parent.mkdir(parents=True)
    target.write_text(PROGRESS, encoding="utf-8")
    evidence = root / "learning-logs/2026/08/2026-08-13-npu-buffer.md"
    evidence.parent.mkdir(parents=True)
    evidence.write_text("# evidence\n", encoding="utf-8")
    return root


def proposal(changes: list[dict], evidence_paths: list[str] | None = None) -> dict:
    return {
        "evidence_paths": evidence_paths
        or ["learning-logs/2026/08/2026-08-13-npu-buffer.md"],
        "changes": changes,
    }


def payload(
    root: Path, changes: list[dict], evidence_paths: list[str] | None = None
) -> dict:
    sha = progress.git_blob_sha((root / progress.TARGET_PATH).read_bytes())
    body = (
        "<!-- research-os-progress-update:v1\n"
        "target_path: roadmap/PROGRESS.md\n"
        f"expected_sha: {sha}\n"
        "-->\n"
        + json.dumps(proposal(changes, evidence_paths), ensure_ascii=False)
    )
    return {
        "title": "[progress-update] 2026-08-14",
        "author": "thisisjskim",
        "repository_owner": "thisisjskim",
        "body": body,
    }


def rejected(action, code: str | None = None) -> progress.ProgressUpdateError:
    try:
        action()
    except progress.ProgressUpdateError as error:
        if code:
            assert error.code == code, (error.code, str(error))
        return error
    raise AssertionError("요청이 거부되지 않았습니다.")


def focus(field: str, old: str, new: str) -> dict:
    return {"type": "current_focus", "field": field, "from": old, "to": new}


def dashboard(stage: str, old: str = "Not Started", new: str = "Learning") -> dict:
    return {"type": "dashboard_status", "stage": stage, "from": old, "to": new}


def main() -> int:
    with tempfile.TemporaryDirectory() as temp:
        root = make_root(temp)
        request = payload(
            root,
            [
                focus("Current Stage", "Stage 3 — Memory", "Stage 4 — NPU Architecture"),
                focus("Current Topic", "6T SRAM", "NPU PE와 Buffer"),
                dashboard("NPU Architecture"),
                focus("Last Updated", "2026-08-13", "2026-08-14"),
            ],
        )
        path, count = progress.apply_update(request, root)
        assert path == progress.TARGET_PATH and count == 4
        updated = (root / path).read_text(encoding="utf-8")
        assert "- Current Stage: Stage 4 — NPU Architecture" in updated
        assert "- Current Topic: NPU PE와 Buffer" in updated
        assert "| NPU Architecture | Learning |" in updated
        assert "- Execution Phase: Phase 1 — Memory Bridge and Paper Scouting" in updated

    # End-to-end regression: an approved Progress update produces a context whose
    # provenance SHA matches the updated Progress and whose reconciliation is aligned.
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        setup_root(root)
        write_fixture(
            root,
            "roadmap/PROGRESS.md",
            "# Progress\n\n"
            "## 3. Current Focus\n\n"
            "- Current Stage: Not Started\n"
            "- Current Topic: SRAM\n\n"
            "## 4. Progress Dashboard\n\n"
            "| Stage | Status | 현재 목표 | Evidence / Notes |\n"
            "| --- | --- | --- | --- |\n"
            "| SRAM / DRAM / eDRAM | Not Started | SRAM | evidence |\n\n"
            "## 5. Application Deliverables\n",
        )
        evidence_path = "learning-logs/2026/08/2026-08-14-sram.md"
        write_fixture(
            root,
            evidence_path,
            note(
                date="2026-08-14",
                understanding="Read Disturb를 설명했다.",
                questions=(),
            ),
        )
        request = payload(
            root,
            [
                focus("Current Stage", "Not Started", "Stage 3 — Memory"),
                dashboard("SRAM / DRAM / eDRAM"),
            ],
            [evidence_path],
        )
        progress.apply_update(request, root)
        snapshot = learning_context.build_context(root)
        updated_sha = learning_context.git_blob_sha(root / progress.TARGET_PATH)
        assert f"Progress source SHA: `{updated_sha}`" in snapshot
        assert "Roadmap reconciliation" not in snapshot

    forbidden_fields = [
        "Primary Goal",
        "Target Contact Window",
        "Execution Phase",
        "Active Track",
        "Current Deliverable",
        "Current Bottleneck",
        "Next Milestone",
        "Phase Deadline",
    ]
    for field in forbidden_fields:
        with tempfile.TemporaryDirectory() as temp:
            root = make_root(temp)
            rejected(lambda: progress.apply_update(payload(root, [focus(field, "a", "b")]), root), "forbidden-field")

    with tempfile.TemporaryDirectory() as temp:
        root = make_root(temp)
        for old, new in (("Learning", "Review"), ("Learning", "Completed"), ("Not Started", "Completed")):
            rejected(lambda o=old, n=new: progress.apply_update(payload(root, [dashboard("NPU Architecture", o, n)]), root), "forbidden-transition")

    with tempfile.TemporaryDirectory() as temp:
        root = make_root(temp)
        request = payload(root, [dashboard("NPU Architecture")])
        request["body"] = request["body"].replace("expected_sha: ", "expected_sha: " + "0" * 40 + "\nignored: ", 1)
        rejected(lambda: progress.apply_update(request, root))

    with tempfile.TemporaryDirectory() as temp:
        root = make_root(temp)
        request = payload(root, [dashboard("NPU Architecture")])
        request["body"] = request["body"].replace(
            progress.git_blob_sha((root / progress.TARGET_PATH).read_bytes()), "0" * 40
        )
        rejected(lambda: progress.apply_update(request, root), "stale-sha")

    with tempfile.TemporaryDirectory() as temp:
        root = make_root(temp)
        request = payload(root, [dashboard("NPU Architecture")])
        request["body"] = request["body"].replace("2026-08-13-npu-buffer.md", "2026-08-13-missing.md")
        rejected(lambda: progress.apply_update(request, root))

    with tempfile.TemporaryDirectory() as temp:
        root = make_root(temp)
        request = payload(root, [dashboard("NPU Architecture")])
        request["author"] = "attacker"
        rejected(lambda: progress.apply_update(request, root), "unauthorized")

    with tempfile.TemporaryDirectory() as temp:
        root = make_root(temp)
        rejected(
            lambda: progress.apply_update(payload(root, [focus("Last Updated", "2026-08-13", "2026-08-13")]), root)
        )

    with tempfile.TemporaryDirectory() as temp:
        root = make_root(temp)
        payload_path = root / "payload.json"
        report_path = root / "report.md"
        output_path = root / "github-output.txt"
        payload_path.write_text(
            json.dumps(payload(root, [dashboard("NPU Architecture")]), ensure_ascii=False),
            encoding="utf-8",
        )
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(Path(__file__).with_name("apply_progress_update.py")),
                "--payload",
                str(payload_path),
                "--root",
                str(root),
                "--report",
                str(report_path),
                "--github-output",
                str(output_path),
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert completed.returncode == 0, completed.stderr
        assert "✅ Progress Update 처리 완료" in report_path.read_text(encoding="utf-8")
        assert "target_path=roadmap/PROGRESS.md" in output_path.read_text(encoding="utf-8")

    with tempfile.TemporaryDirectory() as temp:
        root = make_root(temp)
        payload_path = root / "payload.json"
        report_path = root / "report.md"
        payload_path.write_text(
            json.dumps(payload(root, [dashboard("NPU Architecture", "Learning", "Completed")]), ensure_ascii=False),
            encoding="utf-8",
        )
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(Path(__file__).with_name("apply_progress_update.py")),
                "--payload",
                str(payload_path),
                "--root",
                str(root),
                "--report",
                str(report_path),
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert completed.returncode == 1
        report = report_path.read_text(encoding="utf-8")
        assert "❌ Progress Update 처리 실패" in report
        assert "Error code: `forbidden-transition`" in report
        assert (root / progress.TARGET_PATH).read_text(encoding="utf-8") == PROGRESS

    workflow = (Path(__file__).resolve().parents[1] / ".github/workflows/progress-update.yml").read_text(encoding="utf-8")
    for phrase in (
        "startsWith(github.event.issue.title, '[progress-update]')",
        "python -B scripts/test_apply_progress_update.py",
        "python scripts/apply_progress_update.py",
        '[[ "${changed_paths[0]}" != "roadmap/PROGRESS.md" ]]',
        "✅ Progress Update 처리 완료",
        "Progress source SHA",
        "Learning Context Refresh가 자동 실행됩니다",
        "❌ Progress Update 처리 실패",
    ):
        assert phrase in workflow, phrase

    learning_workflow = (Path(__file__).resolve().parents[1] / ".github/workflows/learning-log-ingest.yml").read_text(encoding="utf-8")
    assert "startsWith(github.event.issue.title, '[learning-log]')" in learning_workflow

    root = Path(__file__).resolve().parents[1]
    entrypoint = (root / "system/CHATGPT_ENTRYPOINT.md").read_text(encoding="utf-8")
    research_os = (root / "system/RESEARCH_OS.md").read_text(encoding="utf-8")
    assert "## Learning Log 이후 Progress 반영" in entrypoint
    assert "PROGRESS.md에도 반영할까요?" in entrypoint
    assert "Learning Log 저장 승인을 Progress 변경 승인으로 재사용하지 않는다" in entrypoint
    assert "research-os-progress-update:v1" in research_os
    assert "Review" in research_os and "Completed" in research_os
    assert "자동 반영 금지" in research_os
    print("All progress update tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
