#!/usr/bin/env python3
"""Verify that only accepted writer jobs enter the shared FIFO queue."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = {
    ".github/workflows/learning-log-ingest.yml": ("ingest", "[learning-log]"),
    ".github/workflows/paper-note-ingest.yml": ("ingest", "[paper-note]"),
    ".github/workflows/progress-update.yml": ("update", "[progress-update]"),
    ".github/workflows/learning-context-refresh.yml": ("refresh", None),
}


def job_block(workflow: str, job_id: str) -> str:
    jobs_marker = "\njobs:\n"
    if jobs_marker not in workflow:
        raise AssertionError("Workflow에 jobs section이 없습니다.")
    prefix, jobs = workflow.split(jobs_marker, 1)
    if re.search(r"(?m)^concurrency:\s*$", prefix):
        raise AssertionError("concurrency는 workflow 수준이 아니라 writer job 안에 있어야 합니다.")

    start_match = re.search(rf"(?m)^  {re.escape(job_id)}:\s*$", jobs)
    if not start_match:
        raise AssertionError(f"writer job을 찾을 수 없습니다: {job_id}")
    following = jobs[start_match.end() :]
    next_job = re.search(r"(?m)^  [A-Za-z0-9_-]+:\s*$", following)
    return following[: next_job.start()] if next_job else following


def assert_writer_queue(path: str, job_id: str, issue_prefix: str | None) -> None:
    workflow = (ROOT / path).read_text(encoding="utf-8")
    block = job_block(workflow, job_id)
    assert "python -B scripts/test_workflow_concurrency.py" in block, (
        f"{path}: writer queue 계약 테스트 실행 단계가 없습니다."
    )
    expected = (
        "    concurrency:\n"
        "      group: research-os-main\n"
        "      cancel-in-progress: false\n"
        "      queue: max\n"
    )
    assert expected in block, f"{path}: job-level writer queue 계약이 다릅니다."
    assert block.count("group: research-os-main") == 1
    assert block.count("cancel-in-progress: false") == 1
    assert block.count("queue: max") == 1
    assert "    if:" in block, f"{path}: writer job의 accept 조건이 없습니다."
    assert block.index("    if:") < block.index("    concurrency:")

    if issue_prefix is not None:
        assert "github.event_name == 'workflow_dispatch'" in block
        assert f"startsWith(github.event.issue.title, '{issue_prefix}')" in block
        other_prefixes = {"[learning-log]", "[paper-note]", "[progress-update]"} - {
            issue_prefix
        }
        for other_prefix in other_prefixes:
            assert other_prefix not in block, (
                f"{path}: 다른 Issue 유형 {other_prefix}까지 accept하고 있습니다."
            )


def main() -> int:
    for path, (job_id, issue_prefix) in WORKFLOWS.items():
        assert_writer_queue(path, job_id, issue_prefix)

    refresh = (
        ROOT / ".github/workflows/learning-context-refresh.yml"
    ).read_text(encoding="utf-8")
    assert 'workflows: ["Learning Log Ingest", "Paper Note Ingest", "Progress Update"]' in refresh
    assert "github.event.workflow_run.conclusion == 'success'" in refresh
    assert '- "scripts/test_workflow_concurrency.py"' in refresh

    # The shared queue is intentionally restricted to the four jobs that can
    # write generated state or user-approved records to main.
    all_workflows = list((ROOT / ".github/workflows").glob("*.yml"))
    queue_users = []
    for workflow_path in all_workflows:
        workflow = workflow_path.read_text(encoding="utf-8")
        if "group: research-os-main" in workflow:
            queue_users.append(workflow_path.relative_to(ROOT).as_posix())
    assert sorted(queue_users) == sorted(WORKFLOWS), (
        "공용 writer queue의 사용 Workflow 집합이 예상과 다릅니다: "
        f"{queue_users}"
    )

    print("All writer concurrency contract tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
