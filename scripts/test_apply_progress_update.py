#!/usr/bin/env python3
"""Contract and end-to-end tests for approved Current Boundary updates."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import apply_progress_update as progress
import build_learning_context as learning_context
from test_build_learning_context import note, setup_root, write_fixture


PIM_FOCUS = """# Progress

공식 학습 위치만 관리한다.

## 3. Current Focus

- Current Boundary: pim-cim-foundations
"""
EVIDENCE_PATH = "learning-logs/2026/08/2026-08-24-pim.md"


def make_root(temp: str) -> Path:
    root = Path(temp)
    setup_root(root)
    repository_root = Path(__file__).resolve().parents[1]
    write_fixture(
        root,
        "roadmap/LEARNING_BOUNDARIES.json",
        (repository_root / "roadmap/LEARNING_BOUNDARIES.json").read_text(
            encoding="utf-8"
        ),
    )
    write_fixture(root, progress.TARGET_PATH, PIM_FOCUS)
    write_fixture(
        root,
        EVIDENCE_PATH,
        note(
            topic="PIM foundations",
            domain="pim-cim",
            date="2026-08-24",
            stage="Stage 5 — PIM / CIM",
            understanding="PIM과 data movement를 설명했다.",
            questions=(),
        ),
    )
    return root


def proposal(old: str = "pim-cim-foundations", new: str = "paper-analysis-foundations") -> dict:
    return {
        "evidence_paths": [EVIDENCE_PATH],
        "changes": [{"type": "current_boundary", "from": old, "to": new}],
    }


def payload(root: Path, body: dict | None = None) -> dict:
    sha = progress.git_blob_sha((root / progress.TARGET_PATH).read_bytes())
    issue_body = (
        "<!-- research-os-progress-update:v2\n"
        "target_path: roadmap/PROGRESS.md\n"
        f"expected_sha: {sha}\n"
        "-->\n"
        + json.dumps(body or proposal(), ensure_ascii=False)
    )
    return {
        "title": "[progress-update] 2026-08-25",
        "author": "thisisjskim",
        "repository_owner": "thisisjskim",
        "body": issue_body,
    }


def rejected(action, code: str | None = None) -> progress.ProgressUpdateError:
    try:
        action()
    except progress.ProgressUpdateError as error:
        if code:
            assert error.code == code, (error.code, str(error))
        return error
    raise AssertionError("요청이 거부되지 않았습니다.")


def main() -> int:
    assert progress.git_blob_sha(b"line\r\n") == progress.git_blob_sha(b"line\n")

    # One approved boundary change edits only the official pointer.
    with tempfile.TemporaryDirectory() as temp:
        root = make_root(temp)
        path, count = progress.apply_update(payload(root), root)
        assert path == progress.TARGET_PATH and count == 1
        updated = (root / path).read_text(encoding="utf-8")
        assert "- Current Boundary: paper-analysis-foundations" in updated
        focus = updated.split("## 3. Current Focus", 1)[1]
        assert sum(line.startswith("- Current ") for line in focus.splitlines()) == 1
        assert "Current Stage" not in updated and "Current Topic" not in updated
        assert "Progress Dashboard" not in updated and "Last Updated" not in updated

        snapshot = learning_context.build_context(root)
        updated_sha = learning_context.git_blob_sha(root / progress.TARGET_PATH)
        assert f"Progress source SHA: `{updated_sha}`" in snapshot
        assert "Current Boundary: `paper-analysis-foundations`" in snapshot
        assert "Current Stage: Stage 6 — Foundational Papers" in snapshot
        assert (
            "Current Topic: 중심 Foundational Paper의 claim map과 architecture walkthrough"
            in snapshot
        )
        assert "Depth Boundary: `paper-analysis-foundations`" in snapshot

    # Unknown boundaries and stale/malformed requests are rejected before writes.
    with tempfile.TemporaryDirectory() as temp:
        root = make_root(temp)
        original = (root / progress.TARGET_PATH).read_text(encoding="utf-8")
        rejected(
            lambda: progress.apply_update(
                payload(root, proposal(new="not-a-boundary")), root
            ),
            "invalid-boundary",
        )
        assert (root / progress.TARGET_PATH).read_text(encoding="utf-8") == original

    with tempfile.TemporaryDirectory() as temp:
        root = make_root(temp)
        malformed = proposal()
        malformed["changes"].append(
            {
                "type": "current_boundary",
                "from": "paper-analysis-foundations",
                "to": "pim-cim-foundations",
            }
        )
        rejected(lambda: progress.apply_update(payload(root, malformed), root))

    with tempfile.TemporaryDirectory() as temp:
        root = make_root(temp)
        request = payload(root)
        request["body"] = request["body"].replace(
            progress.git_blob_sha((root / progress.TARGET_PATH).read_bytes()),
            "0" * 40,
        )
        rejected(lambda: progress.apply_update(request, root), "stale-sha")

    with tempfile.TemporaryDirectory() as temp:
        root = make_root(temp)
        request = payload(root)
        request["body"] = request["body"].replace(EVIDENCE_PATH, "learning-logs/2026/08/2026-08-24-missing.md")
        rejected(lambda: progress.apply_update(request, root))

    with tempfile.TemporaryDirectory() as temp:
        root = make_root(temp)
        request = payload(root)
        request["author"] = "attacker"
        rejected(lambda: progress.apply_update(request, root), "unauthorized")

    with tempfile.TemporaryDirectory() as temp:
        root = make_root(temp)
        stale = (root / progress.TARGET_PATH).read_text(encoding="utf-8").replace(
            "pim-cim-foundations", "npu-architecture-foundations"
        )
        write_fixture(root, progress.TARGET_PATH, stale)
        rejected(lambda: progress.apply_update(payload(root), root), "stale-value")

    # CLI writes success/failure reports used by the workflow comment step.
    with tempfile.TemporaryDirectory() as temp:
        root = make_root(temp)
        payload_path = root / "payload.json"
        report_path = root / "report.md"
        output_path = root / "github-output.txt"
        payload_path.write_text(
            json.dumps(payload(root), ensure_ascii=False), encoding="utf-8"
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

    workflow = (
        Path(__file__).resolve().parents[1] / ".github/workflows/progress-update.yml"
    ).read_text(encoding="utf-8")
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

    root = Path(__file__).resolve().parents[1]
    entrypoint = (root / "system/CHATGPT_ENTRYPOINT.md").read_text(encoding="utf-8")
    research_os = (root / "system/RESEARCH_OS.md").read_text(encoding="utf-8")
    assert "## Learning Log 이후 Current Boundary 검토" in entrypoint
    assert "Current Boundary도 변경할까요?" in entrypoint
    assert "Learning Log 저장 승인을 Current Boundary 변경 승인으로 재사용하지 않는다" in entrypoint
    assert "research-os-progress-update:v2" in research_os
    assert "Current Boundary" in research_os
    assert "최신 Learning Log만으로" in research_os
    print("All progress update tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
