#!/usr/bin/env python3
"""Canonical decision policy shared by generated progress views."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable


UNSET_VALUES = {"", "아직 지정되지 않음", "없음", "not started"}


@dataclass(frozen=True)
class DashboardChange:
    label: str
    current: str
    proposed: str


@dataclass(frozen=True)
class ProgressDecision:
    status: str
    reason: str
    proposed_fields: tuple[tuple[str, str], ...]
    dashboard_changes: tuple[DashboardChange, ...]


def progress_value(progress: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}:\s*(.+)$", progress, re.MULTILINE)
    return match.group(1).strip() if match else ""


def dashboard_statuses(progress: str) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in progress.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 2:
            rows[cells[0]] = cells[1]
    return rows


def decide_progress(
    progress: str,
    *,
    has_evidence: bool,
    canonical_stage: str,
    canonical_topic: str,
    next_roadmap_topic: str,
    recommended_move: str,
    evidence_dashboard_labels: Iterable[str],
) -> ProgressDecision:
    """Return one decision for both context and reconciliation documents.

    A Learning Log topic is deliberately not accepted as an input. A log title is
    evidence for work performed, not the canonical roadmap position.
    """
    if not has_evidence:
        return ProgressDecision(
            status="not-needed",
            reason="의미 있는 Learning Log가 없어 진행 상태를 비교할 evidence가 없음",
            proposed_fields=(),
            dashboard_changes=(),
        )

    current_stage = progress_value(progress, "Current Stage")
    current_topic = progress_value(progress, "Current Topic")
    proposed_fields: list[tuple[str, str]] = []
    reasons: list[str] = []

    if current_stage.casefold() in UNSET_VALUES:
        proposed_fields.append(("Current Stage", canonical_stage))
        reasons.append("Current Stage가 지정되지 않아 현재 depth boundary의 공식 stage를 제안함")
    elif current_stage != canonical_stage:
        proposed_fields.append(("Current Stage", canonical_stage))
        reasons.append("Current Stage가 현재 depth boundary의 공식 stage와 일치하지 않음")

    if current_topic.casefold() in UNSET_VALUES:
        proposed_fields.append(("Current Topic", canonical_topic))
        reasons.append("Current Topic이 지정되지 않아 현재 depth boundary의 공식 topic을 제안함")
    elif recommended_move == "advance" and current_topic != next_roadmap_topic:
        proposed_fields.append(("Current Topic", next_roadmap_topic))
        reasons.append("모든 exit criterion을 충족해 Roadmap에 정의된 다음 topic을 제안함")

    statuses = dashboard_statuses(progress)
    dashboard_changes: list[DashboardChange] = []
    for label in dict.fromkeys(evidence_dashboard_labels):
        current = statuses.get(label, "")
        if current == "Not Started":
            dashboard_changes.append(DashboardChange(label, current, "Learning"))
            reasons.append(f"{label}에 학습 evidence가 있지만 dashboard 상태가 Not Started임")

    if proposed_fields or dashboard_changes:
        return ProgressDecision(
            status="pending-approval",
            reason="; ".join(dict.fromkeys(reasons)),
            proposed_fields=tuple(proposed_fields),
            dashboard_changes=tuple(dashboard_changes),
        )
    return ProgressDecision(
        status="aligned",
        reason=(
            "현재 stage/topic과 dashboard가 Roadmap boundary 및 Learning Log evidence와 일치함; "
            f"학습 이동 판단은 {recommended_move}이며 공식 topic 변경은 아직 필요하지 않음"
        ),
        proposed_fields=(),
        dashboard_changes=(),
    )
