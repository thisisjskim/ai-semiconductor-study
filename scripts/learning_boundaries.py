#!/usr/bin/env python3
"""Load the canonical learning-boundary contract shared by Progress and Context."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class ExitCriterion:
    text: str
    evidence_groups: tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class LearningBoundary:
    id: str
    current_topic: str
    progress_topics: tuple[str, ...]
    domains: tuple[str, ...]
    evidence_domains: tuple[str, ...]
    roadmap_stage: str
    topic_goal: str
    minimum_required_understanding: tuple[str, ...]
    exit_criteria: tuple[ExitCriterion, ...]
    blocking_question_keywords: tuple[str, ...]
    optional_question_keywords: tuple[str, ...]
    optional_deep_dive: tuple[str, ...]
    next_roadmap_topic: str


def load_boundaries(root: Path) -> list[LearningBoundary]:
    path = root / "roadmap/LEARNING_BOUNDARIES.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if (
        payload.get("version") != 1
        or payload.get("policy") != "progression-over-exhaustiveness"
    ):
        raise ValueError("Unsupported learning boundary contract")

    boundaries: list[LearningBoundary] = []
    for raw in payload.get("boundaries", []):
        criteria = tuple(
            ExitCriterion(
                text=item["text"],
                evidence_groups=tuple(
                    tuple(group) for group in item["evidence_groups"]
                ),
            )
            for item in raw["exit_criteria"]
        )
        boundaries.append(
            LearningBoundary(
                id=raw["id"],
                current_topic=raw["current_topic"],
                progress_topics=tuple(raw["progress_topics"]),
                domains=tuple(raw["domains"]),
                evidence_domains=tuple(
                    raw.get("evidence_domains", raw["domains"])
                ),
                roadmap_stage=raw["roadmap_stage"],
                topic_goal=raw["topic_goal"],
                minimum_required_understanding=tuple(
                    raw["minimum_required_understanding"]
                ),
                exit_criteria=criteria,
                blocking_question_keywords=tuple(
                    raw["blocking_question_keywords"]
                ),
                optional_question_keywords=tuple(
                    raw["optional_question_keywords"]
                ),
                optional_deep_dive=tuple(raw["optional_deep_dive"]),
                next_roadmap_topic=raw["next_roadmap_topic"],
            )
        )

    if not boundaries:
        raise ValueError("No learning boundaries configured")
    ids = [boundary.id for boundary in boundaries]
    if len(ids) != len(set(ids)):
        raise ValueError("Learning boundary id must be unique")
    for boundary in boundaries:
        if boundary.current_topic not in boundary.progress_topics:
            raise ValueError(
                f"current_topic must be a progress_topics alias: {boundary.id}"
            )
    return boundaries


def boundary_by_id(
    boundaries: Iterable[LearningBoundary], boundary_id: str
) -> LearningBoundary:
    matches = [boundary for boundary in boundaries if boundary.id == boundary_id]
    if len(matches) != 1:
        raise ValueError(f"Unknown Current Boundary: {boundary_id or '없음'}")
    return matches[0]
