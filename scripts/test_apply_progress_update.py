#!/usr/bin/env python3
"""Contract tests for apply_progress_update.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import apply_progress_update as progress


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


def proposal(changes: list[dict]) -> dict:
    return {
        "evidence_paths": ["learning-logs/2026/08/2026-08-13-npu-buffer.md"],
        "changes": changes,
    }


def payload(root: Path, changes: list[dict]) -> dict:
    sha = progress.git_blob_sha((root / progress.TARGET_PATH).read_bytes())
    body = (
        "<!-- research-os-progress-update:v1\n"
        "target_path: roadmap/PROGRESS.md\n"
        f"expected_sha: {sha}\n"
        "-->\n"
        + json.dumps(proposal(changes), ensure_ascii=False)
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
        "❌ Progress Update 처리 실패",
    ):
        assert phrase in workflow, phrase

    learning_workflow = (Path(__file__).resolve().parents[1] / ".github/workflows/learning-log-ingest.yml").read_text(encoding="utf-8")
    assert "startsWith(github.event.issue.title, '[learning-log]')" in learning_workflow

    schema = (Path(__file__).resolve().parents[1] / "system/ACTION_SCHEMA.yaml").read_text(encoding="utf-8")
    assert "operationId: createLearningLogIssue" in schema
    assert "ProgressUpdateIssueRequest:" in schema
    assert "research-os-progress-update:v1" in schema

    instructions = (Path(__file__).resolve().parents[1] / "system/CUSTOM_GPT_INSTRUCTIONS.md").read_text(encoding="utf-8")
    assert "## 6. Learning Log 이후 Progress 반영" in instructions
    assert "PROGRESS.md에도 반영할까요?" in instructions
    assert "Review와 Completed를 자동 판정하지 않는다" in instructions
    print("All progress update tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
