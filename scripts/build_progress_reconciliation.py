#!/usr/bin/env python3
"""Build a review-only proposal for reconciling PROGRESS.md with learning evidence."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

import build_learning_context as context


OUTPUT_PATH = "state/PROGRESS_RECONCILIATION.md"
STATUS_ORDER = {"Not Started": 0, "Learning": 1, "Review": 2, "Completed": 3}
DOMAIN_ROWS = {
    "ai-computation": "AI Computation",
    "computer-architecture": "Computer Architecture",
    "memory-architecture": "Memory Architecture",
    "sram": "SRAM / DRAM / eDRAM",
    "dram": "SRAM / DRAM / eDRAM",
    "npu": "NPU Architecture",
    "pim-cim": "PIM / CIM",
}


@dataclass(frozen=True)
class DashboardRow:
    label: str
    status: str
    goal: str
    evidence: str


def parse_dashboard(progress: str) -> list[DashboardRow]:
    rows: list[DashboardRow] = []
    for line in progress.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 4 or cells[0] in {"Stage", "---"}:
            continue
        if cells[1] not in STATUS_ORDER:
            continue
        rows.append(DashboardRow(*cells))
    return rows


def current_field(progress: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}:\s*(.+)$", progress, re.MULTILINE)
    return match.group(1).strip() if match else "없음"


def dashboard_label(log: context.LearningLog) -> str | None:
    direct = DOMAIN_ROWS.get(log.domain)
    if direct:
        return direct
    if log.domain != "paper":
        return None
    stage = log.roadmap_stage.casefold()
    if "stage 6" in stage or "foundational" in stage:
        return "Foundational Papers"
    if "stage 7" in stage or "ssl" in stage:
        return "KAIST SSL Lab Papers"
    return None


def evidence_by_row(
    logs: list[context.LearningLog],
) -> dict[str, list[context.LearningLog]]:
    grouped: dict[str, list[context.LearningLog]] = {}
    for log in logs:
        label = dashboard_label(log)
        if label:
            grouped.setdefault(label, []).append(log)
    return grouped


def first_next_action(log: context.LearningLog) -> str:
    section = log.sections["## 9. 다음 행동"]
    listed = [
        match.group("text").strip()
        for line in section.splitlines()
        if (match := context.LIST_RE.match(line.strip()))
    ]
    actions = listed[:1] or context.extract_items(section, 1)
    return actions[0] if actions else "다음 학습 행동을 사용자와 확인"


def markdown_cell(value: str, limit: int = 240) -> str:
    cleaned = " ".join(value.replace("|", "\\|").split())
    return cleaned if len(cleaned) <= limit else cleaned[: limit - 1].rstrip() + "…"


def proposal_rows(
    dashboard: list[DashboardRow], grouped: dict[str, list[context.LearningLog]]
) -> list[str]:
    rows: list[str] = []
    by_label = {row.label: row for row in dashboard}
    for label in [row.label for row in dashboard]:
        logs = grouped.get(label, [])
        if not logs:
            continue
        row = by_label[label]
        proposed_status = "Learning" if row.status == "Not Started" else row.status
        paths = ", ".join(f"`{item.path}`" for item in logs[-3:])
        status_change = (
            f"`{row.status}` → `{proposed_status}`"
            if row.status != proposed_status
            else f"`{row.status}` 유지"
        )
        rows.append(f"| {markdown_cell(label)} | {status_change} | {paths} |")
    return rows


def build_reconciliation(root: Path) -> str:
    progress_path = root / "roadmap/PROGRESS.md"
    roadmap_path = root / "roadmap/ROADMAP.md"
    progress = progress_path.read_text(encoding="utf-8")
    roadmap_path.read_text(encoding="utf-8")
    logs, excluded = context.discover_logs(root)
    dashboard = parse_dashboard(progress)

    lines = [
        "# Progress Reconciliation Proposal",
        "",
        "> 이 문서는 Learning Log evidence와 `roadmap/PROGRESS.md`를 비교해 자동 생성한 검토용 제안서다. `roadmap/PROGRESS.md`를 수정하지 않으며, 아래 변경은 사용자 승인 후 별도 branch와 Pull Request에서만 적용한다.",
        "",
    ]

    if not logs:
        lines.extend(
            [
                "- Proposal status: **no-evidence**",
                "- Latest evidence date: 없음",
                "",
                "## 제안",
                "",
                "- 유효한 학습 evidence가 없어 진행 상태 변경을 제안하지 않음",
            ]
        )
    else:
        latest_date = logs[-1].date
        latest = [item for item in logs if item.date == latest_date]
        primary = latest[-1]
        grouped = evidence_by_row(logs)
        rows = proposal_rows(dashboard, grouped)
        proposed_fields = {
            "Current Stage": primary.roadmap_stage,
            "Current Topic": primary.topic,
            "Next Milestone": first_next_action(primary),
            "Last Updated": primary.date.isoformat(),
        }
        changes_needed = any(
            current_field(progress, label) != value
            for label, value in proposed_fields.items()
        ) or any("→" in row for row in rows)
        lines.extend(
            [
                f"- Proposal status: **{'pending-approval' if changes_needed else 'aligned'}**",
                f"- Latest evidence date: {latest_date.isoformat()}",
                "- Maximum automatic status proposal: **Learning**",
                "",
                "## 현재 포커스 변경 제안",
                "",
                "| Field | 현재 값 | 제안 값 |",
                "| --- | --- | --- |",
            ]
        )
        for label, value in proposed_fields.items():
            lines.append(
                f"| {label} | {markdown_cell(current_field(progress, label))} | "
                f"{markdown_cell(value)} |"
            )
        lines.extend(
            [
                "",
                "## Dashboard 변경 제안",
                "",
                "| Stage | 상태 제안 | 근거 Learning Log |",
                "| --- | --- | --- |",
            ]
        )
        lines.extend(rows or ["| 없음 | 변경 없음 | 유효한 매핑 evidence 없음 |"])
        lines.extend(
            [
                "",
                "## 판단 제한",
                "",
                "- Learning Log가 존재한다는 사실만으로 `Review` 또는 `Completed`를 제안하지 않음",
                "- 기존 `Review` 또는 `Completed` 상태를 자동으로 낮추지 않음",
                "- Metadata로 dashboard row를 안전하게 특정할 수 없는 기록은 상태 변경 근거로 사용하지 않음",
                "- 실제 반영 전 사용자가 stage, topic, milestone과 evidence를 검토해야 함",
            ]
        )

    lines.extend(
        [
            "",
            "## 사용한 source paths",
            "",
            "- `roadmap/ROADMAP.md`",
            "- `roadmap/PROGRESS.md`",
        ]
    )
    lines.extend(f"- `{item.path}`" for item in logs)
    lines.extend(["", "## 제외한 기록과 이유", ""])
    lines.extend(
        context.bullet_lines([f"`{path}` — {reason}" for path, reason in excluded])
    )
    lines.extend(
        [
            "",
            "## 승인 후 적용 절차",
            "",
            "1. 사용자가 이 제안의 적용 범위를 명시적으로 승인한다.",
            "2. Codex가 최신 `main`에서 별도 branch를 만든다.",
            "3. 승인된 항목만 `roadmap/PROGRESS.md`에 반영한다.",
            "4. 검증 후 Pull Request를 만들고 사용자가 검토·merge한다.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", default=OUTPUT_PATH)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_reconciliation(root), encoding="utf-8")
    print(f"Refreshed {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
