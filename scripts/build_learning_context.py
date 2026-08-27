#!/usr/bin/env python3
"""Build the derived current learning context from repository-native sources."""

from __future__ import annotations

import argparse
import hashlib
import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable

from learning_boundaries import (
    ExitCriterion,
    LearningBoundary,
    boundary_by_id,
    load_boundaries,
)
from learning_log_metadata import DomainPolicy, load_domain_policy


REQUIRED_SECTIONS = (
    "## 1. 오늘 공부한 목적",
    "## 2. 오늘 이해한 내용",
    "## 3. 핵심 개념",
    "## 4. 내가 처음 이해한 방식",
    "## 5. 오해 또는 불확실한 부분",
    "## 6. 수정된 이해",
    "## 7. 질문",
    "## 8. AI 반도체 및 SSL 목표와의 연결",
    "## 9. 다음 행동",
    "## 10. 자기 설명 점검",
    "## 사용자 원문",
)
LIMITS = {
    "concepts": 8,
    "questions": 6,
    "weaknesses": 6,
    "actions": 6,
}
METADATA_RE = re.compile(r"^- (?P<key>[^:]+):\s*(?P<value>.*)$")
HEADING_RE = re.compile(r"^(?P<level>#{2,3})\s+.+$")
CHECKBOX_RE = re.compile(r"^- \[(?P<state>[ xX])\]\s*(?P<text>.+)$")
LIST_RE = re.compile(r"^(?:[-*+] |\d+[.)]\s+)(?P<text>.+)$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RECORDED_AT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
PAPER_NOTE_PATH_RE = re.compile(
    r"^paper-notes/(?P<paper_type>foundational|ssl-lab|related)/"
    r"\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"
)
BRIDGE_STATUSES = {"studying", "paused", "sufficient-for-paper"}


def git_blob_sha(path: Path) -> str:
    """Return the Git blob SHA used by GitHub's repository contents API."""
    data = path.read_bytes().replace(b"\r\n", b"\n")
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


@dataclass(frozen=True)
class LearningLog:
    path: str
    date: date
    recorded_at: datetime | None
    topic: str
    domain: str
    roadmap_stage: str
    sections: dict[str, str]


@dataclass(frozen=True)
class PaperNote:
    path: str
    checkpoint_recorded_at: datetime


@dataclass(frozen=True)
class LearningPlan:
    boundary: LearningBoundary
    completed: tuple[ExitCriterion, ...]
    remaining: tuple[ExitCriterion, ...]
    blocking_questions: tuple[str, ...]
    optional_questions: tuple[str, ...]
    recommended_move: str
    grounding_paths: tuple[str, ...]
    evidence_paths: tuple[str, ...]


def learning_log_order(log: LearningLog) -> tuple[date, datetime, str]:
    return (
        log.date,
        log.recorded_at or datetime.min.replace(tzinfo=timezone.utc),
        log.path,
    )


def repository_path(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def parse_sections(markdown: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = ""
    for line in markdown.splitlines():
        if line.startswith("## "):
            current = line.strip()
            sections.setdefault(current, [])
        elif current:
            sections[current].append(line)
    return {heading: "\n".join(lines).strip() for heading, lines in sections.items()}


def parse_metadata(sections: dict[str, str]) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in sections.get("## Metadata", "").splitlines():
        match = METADATA_RE.fullmatch(line.strip())
        if match:
            metadata[match.group("key").strip()] = match.group("value").strip()
    return metadata


def classify_log(
    path: Path, root: Path, domain_policy: DomainPolicy
) -> tuple[LearningLog | None, str | None]:
    relative = repository_path(path, root)
    try:
        markdown = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None, "파일을 UTF-8로 읽을 수 없음"
    if not markdown.startswith("# 학습 기록:"):
        return None, "문서가 canonical Learning Log 제목으로 시작하지 않음"

    sections = parse_sections(markdown)
    metadata = parse_metadata(sections)
    required_metadata = ("Date", "Topic", "Document type", "Domain", "Roadmap stage")
    missing_metadata = [key for key in required_metadata if not metadata.get(key)]
    if missing_metadata:
        return None, "필수 Metadata 누락: " + ", ".join(missing_metadata)
    if metadata["Document type"] != "learning-log":
        return None, "Document type이 learning-log가 아님"
    if not DATE_RE.fullmatch(metadata["Date"]):
        return None, "Date가 유효한 YYYY-MM-DD 형식이 아님"
    try:
        parsed_date = date.fromisoformat(metadata["Date"])
    except ValueError:
        return None, "Date가 유효한 YYYY-MM-DD 형식이 아님"
    recorded_at = None
    if metadata.get("Recorded at"):
        if not RECORDED_AT_RE.fullmatch(metadata["Recorded at"]):
            return None, "Recorded at이 유효한 YYYY-MM-DDTHH:MM:SSZ 형식이 아님"
        try:
            recorded_at = datetime.fromisoformat(
                metadata["Recorded at"].removesuffix("Z") + "+00:00"
            )
        except ValueError:
            return None, "Recorded at이 유효한 YYYY-MM-DDTHH:MM:SSZ 형식이 아님"
    domain = metadata["Domain"]
    if domain in domain_policy.non_learning_domains:
        return None, f"Domain이 {domain}인 시스템 개발·운영 기록"
    if domain not in domain_policy.learning_domains:
        allowed = ", ".join(sorted(domain_policy.allowed_domains))
        return None, f"지원되지 않는 Domain metadata: {domain} (허용값: {allowed})"
    if metadata["Roadmap stage"].casefold() == "system-development":
        return None, "Roadmap stage가 system-development인 시스템 개발 기록"
    missing_sections = [heading for heading in REQUIRED_SECTIONS if heading not in sections]
    if missing_sections:
        return None, "필수 Learning Log section 누락: " + ", ".join(missing_sections)

    return (
        LearningLog(
            path=relative,
            date=parsed_date,
            recorded_at=recorded_at,
            topic=metadata["Topic"],
            domain=domain,
            roadmap_stage=metadata["Roadmap stage"],
            sections=sections,
        ),
        None,
    )


def discover_logs(root: Path) -> tuple[list[LearningLog], list[tuple[str, str]]]:
    included: list[LearningLog] = []
    excluded: list[tuple[str, str]] = []
    domain_policy = load_domain_policy(root)
    paths = sorted(
        (root / "learning-logs").glob("**/*.md"), key=lambda item: item.as_posix()
    )
    for path in paths:
        log, reason = classify_log(path, root, domain_policy)
        if log:
            included.append(log)
        else:
            excluded.append((repository_path(path, root), reason or "분류할 수 없음"))
    included.sort(key=learning_log_order)
    excluded.sort()
    return included, excluded


def classify_paper_note(path: Path, root: Path) -> PaperNote | None:
    relative = repository_path(path, root)
    path_match = PAPER_NOTE_PATH_RE.fullmatch(relative)
    if not path_match:
        return None
    try:
        markdown = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None
    if not markdown.startswith("# Paper Note:"):
        return None
    sections = parse_sections(markdown)
    if not {
        "## Metadata",
        "## 2. Reading Checkpoint",
        "## 3. Prerequisite Bridge",
    }.issubset(sections):
        return None
    metadata = parse_metadata(sections)
    if metadata.get("Document type") != "paper-note":
        return None
    if metadata.get("Paper type") != path_match.group("paper_type"):
        return None
    checkpoint = metadata.get("Checkpoint recorded at", "")
    if not RECORDED_AT_RE.fullmatch(checkpoint):
        return None
    try:
        checkpoint_recorded_at = datetime.fromisoformat(
            checkpoint.removesuffix("Z") + "+00:00"
        )
    except ValueError:
        return None

    checkpoint_fields = parse_metadata(
        {"## Metadata": sections["## 2. Reading Checkpoint"]}
    )
    if not checkpoint_fields.get("Resume Point"):
        return None
    statuses = [
        match.group("value").strip()
        for line in sections["## 3. Prerequisite Bridge"].splitlines()
        if (match := METADATA_RE.fullmatch(line.strip()))
        and match.group("key").strip() == "Status"
    ]
    if any(status not in BRIDGE_STATUSES for status in statuses):
        return None
    if statuses.count("studying") > 1:
        return None
    return PaperNote(relative, checkpoint_recorded_at)


def discover_current_paper(root: Path) -> PaperNote | None:
    paper_root = root / "paper-notes"
    if not paper_root.exists():
        return None
    notes = [
        note
        for path in sorted(paper_root.glob("**/*.md"), key=lambda item: item.as_posix())
        if (note := classify_paper_note(path, root)) is not None
    ]
    if not notes:
        return None
    return max(notes, key=lambda note: (note.checkpoint_recorded_at, note.path))


def append_current_paper(lines: list[str], current_paper: PaperNote | None) -> None:
    lines.extend(["", "## Current Paper", ""])
    if current_paper:
        lines.append(f"- Current Paper Note: `{current_paper.path}`")
    else:
        lines.append("- Current Paper Note: 없음")


def extract_items(text: str, limit: int) -> list[str]:
    items: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or HEADING_RE.match(line):
            continue
        match = LIST_RE.match(line)
        value = match.group("text").strip() if match else line
        if value and value not in items:
            items.append(value)
        if len(items) == limit:
            break
    return items


def extract_subsection(text: str, heading: str) -> str:
    lines = text.splitlines()
    collecting = False
    selected: list[str] = []
    for line in lines:
        if line.strip() == heading:
            collecting = True
            continue
        if collecting and line.startswith("### "):
            break
        if collecting:
            selected.append(line)
    return "\n".join(selected).strip()


def extract_unfinished(text: str, limit: int) -> list[str]:
    items: list[str] = []
    for line in text.splitlines():
        match = CHECKBOX_RE.fullmatch(line.strip())
        if match and match.group("state") == " ":
            items.append(match.group("text").strip())
        if len(items) == limit:
            break
    return items


def progress_value(progress: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}:\s*(.+)$", progress, re.MULTILINE)
    return match.group(1).strip() if match else ""


def select_boundary(
    boundaries: Iterable[LearningBoundary], progress: str
) -> LearningBoundary:
    return boundary_by_id(
        boundaries, progress_value(progress, "Current Boundary")
    )


def checked_self_explanations(text: str) -> list[str]:
    values: list[str] = []
    for line in text.splitlines():
        match = CHECKBOX_RE.fullmatch(line.strip())
        if match and match.group("state").casefold() == "x":
            values.append(match.group("text").strip())
    return values


def evidence_corpus(logs: Iterable[LearningLog]) -> str:
    evidence_sections = (
        "## 2. 오늘 이해한 내용",
        "## 3. 핵심 개념",
        "## 4. 내가 처음 이해한 방식",
        "## 5. 오해 또는 불확실한 부분",
        "## 6. 수정된 이해",
        "## 8. AI 반도체 및 SSL 목표와의 연결",
    )
    chunks: list[str] = []
    for log in logs:
        chunks.extend(log.sections.get(section, "") for section in evidence_sections)
        chunks.extend(checked_self_explanations(log.sections.get("## 10. 자기 설명 점검", "")))
    return "\n".join(chunks).casefold()


def criterion_is_met(criterion: ExitCriterion, corpus: str) -> bool:
    return all(any(term.casefold() in corpus for term in group) for group in criterion.evidence_groups)


def criterion_match_count(criterion: ExitCriterion, corpus: str) -> int:
    return sum(
        1
        for group in criterion.evidence_groups
        if any(term.casefold() in corpus for term in group)
    )


def select_grounding_paths(
    relevant: list[LearningLog],
    all_logs: Iterable[LearningLog],
    remaining: tuple[ExitCriterion, ...],
) -> tuple[str, ...]:
    logs = list(all_logs)
    latest_paths = [log.path for log in logs[-2:]]
    paths: list[str] = []

    if not remaining:
        paths.append("roadmap/LEARNING_BOUNDARIES.json")
    else:
        criterion = remaining[0]
        ranked = sorted(
            relevant,
            key=lambda log: (
                criterion_match_count(criterion, evidence_corpus([log])),
                learning_log_order(log),
            ),
            reverse=True,
        )
        if ranked:
            paths.append(ranked[0].path)
        else:
            paths.append("roadmap/LEARNING_BOUNDARIES.json")

    paths.extend(latest_paths)
    return tuple(dict.fromkeys(paths))


def contains_keyword(text: str, keywords: Iterable[str]) -> bool:
    folded = text.casefold()
    return any(keyword.casefold() in folded for keyword in keywords)


def build_learning_plan(
    boundaries: Iterable[LearningBoundary],
    progress: str,
    included: Iterable[LearningLog],
    primary: LearningLog,
) -> LearningPlan:
    boundary = select_boundary(boundaries, progress)
    logs = list(included)
    relevant = [log for log in logs if log.domain in boundary.evidence_domains]
    corpus = evidence_corpus(relevant)
    completed = tuple(item for item in boundary.exit_criteria if criterion_is_met(item, corpus))
    remaining = tuple(item for item in boundary.exit_criteria if item not in completed)

    latest_date = max((log.date for log in relevant), default=None)
    latest_relevant = (
        [log for log in relevant if log.date == latest_date]
        if latest_date is not None
        else []
    )
    questions: list[str] = []
    for log in latest_relevant:
        questions.extend(
            extract_items(
                extract_subsection(log.sections["## 7. 질문"], "### 해결되지 않은 질문"),
                LIMITS["questions"],
            )
        )
    questions = list(dict.fromkeys(questions))[: LIMITS["questions"]]
    blocking_questions: list[str] = []
    optional_questions: list[str] = []
    for question in questions:
        if contains_keyword(question, boundary.optional_question_keywords):
            optional_questions.append(question)
        elif remaining and contains_keyword(question, boundary.blocking_question_keywords):
            blocking_questions.append(question)
        else:
            optional_questions.append(question)

    blocking_count = len(remaining) + len(blocking_questions)
    if blocking_count == 0:
        recommended_move = "advance"
    elif blocking_count == 1:
        recommended_move = "review_then_advance"
    else:
        recommended_move = "continue"
    return LearningPlan(
        boundary=boundary,
        completed=completed,
        remaining=remaining,
        blocking_questions=tuple(blocking_questions),
        optional_questions=tuple(optional_questions),
        recommended_move=recommended_move,
        grounding_paths=select_grounding_paths(relevant, logs, remaining),
        evidence_paths=tuple(log.path for log in relevant),
    )


def bullet_lines(items: list[str], empty: str = "없음") -> list[str]:
    return [f"- {item}" for item in items] if items else [f"- {empty}"]


def build_context(root: Path) -> str:
    included, excluded = discover_logs(root)
    current_paper = discover_current_paper(root)
    progress_path = root / "roadmap/PROGRESS.md"
    progress = progress_path.read_text(encoding="utf-8")
    progress_sha = git_blob_sha(progress_path)
    roadmap_path = root / "roadmap/ROADMAP.md"
    roadmap_path.read_text(encoding="utf-8")  # Required source; validates readability.
    boundaries = load_boundaries(root)
    official_boundary = select_boundary(boundaries, progress)

    if not included:
        latest_snapshot_date = (
            current_paper.checkpoint_recorded_at.date().isoformat()
            if current_paper
            else "없음"
        )
        lines = [
            "# Current Learning Context",
            "",
            "> 이 문서는 `learning-logs/**`, `paper-notes/**`와 roadmap에서 자동 생성한 derived/generated snapshot이다. Source of truth가 아니며 원본 기록을 다시 확인할 수 있다.",
            "",
            f"- Last generated date: {latest_snapshot_date}",
            f"- Progress source SHA: `{progress_sha}`",
            "",
            "## 현재 상태",
            "",
            "- 최신 의미 있는 학습 기록: 없음",
            f"- Current Boundary: `{official_boundary.id}`",
            f"- Current Stage: {official_boundary.roadmap_stage}",
            f"- Current Topic: {official_boundary.current_topic}",
            "- Domain: 없음",
            f"- Depth Boundary: `{official_boundary.id}`",
        ]
        append_current_paper(lines, current_paper)
        lines.extend(["", "## 제외한 기록과 이유", ""])
        lines.extend(bullet_lines([f"`{path}` — {why}" for path, why in excluded]))
        lines.extend(
            [
                "",
                "## 참고한 source paths",
                "",
                "- `roadmap/ROADMAP.md`",
                "- `roadmap/LEARNING_BOUNDARIES.json`",
                "- `roadmap/PROGRESS.md`",
                "",
            ]
        )
        return "\n".join(lines)

    latest_date = included[-1].date
    latest_snapshot_date = latest_date
    if current_paper:
        latest_snapshot_date = max(
            latest_snapshot_date, current_paper.checkpoint_recorded_at.date()
        )
    latest_logs = [item for item in included if item.date == latest_date]
    primary = latest_logs[-1]
    concepts = extract_items(primary.sections["## 3. 핵심 개념"], LIMITS["concepts"])
    weaknesses = extract_unfinished(
        primary.sections["## 10. 자기 설명 점검"], LIMITS["weaknesses"]
    )
    actions = extract_items(primary.sections["## 9. 다음 행동"], LIMITS["actions"])
    plan = build_learning_plan(boundaries, progress, included, primary)
    current_stage = plan.boundary.roadmap_stage
    current_topic = plan.boundary.current_topic

    move_explanations = {
        "continue": "현재 topic의 blocking gap이 둘 이상이므로 필요한 최소 범위만 계속 학습한다.",
        "review_then_advance": "blocking gap 하나만 짧게 확인한 뒤 다음 Roadmap topic으로 이동한다.",
        "advance": "현재 exit criteria를 충족했으므로 optional question을 기본 경로에 넣지 않고 다음 Roadmap topic으로 이동한다.",
    }

    lines = [
        "# Current Learning Context",
        "",
        "> 이 문서는 `learning-logs/**`, `paper-notes/**`와 roadmap에서 자동 생성한 derived/generated snapshot이다. Source of truth가 아니며 원본 기록을 다시 확인할 수 있다.",
        "",
        f"- Last generated date: {latest_snapshot_date.isoformat()}",
        f"- Progress source SHA: `{progress_sha}`",
        "",
        "## Roadmap Position",
        "",
        f"- 최신 의미 있는 학습 기록: `{primary.path}`",
        f"- Current Boundary: `{plan.boundary.id}`",
        f"- Current Stage: {current_stage}",
        f"- Current Topic: {current_topic}",
        f"- Domain: {primary.domain}",
        f"- Depth Boundary: `{plan.boundary.id}`",
        "",
        "### 같은 날짜의 의미 있는 학습 단위",
        "",
    ]
    lines.extend(bullet_lines([f"`{item.path}` — {item.topic}" for item in latest_logs]))
    append_current_paper(lines, current_paper)
    lines.extend(["", "## Topic Goal", "", f"- {plan.boundary.topic_goal}"])
    lines.extend(["", "## Minimum Required Understanding", ""])
    lines.extend(bullet_lines(list(plan.boundary.minimum_required_understanding)))
    lines.extend(["", "## Exit Criteria", ""])
    for criterion in plan.boundary.exit_criteria:
        marker = "x" if criterion in plan.completed else " "
        lines.append(f"- [{marker}] {criterion.text}")
    lines.extend(["", "## Evidence of Completion", ""])
    lines.extend(
        bullet_lines(
            [criterion.text for criterion in plan.completed],
            "Learning Log에서 자동 확인된 exit criterion이 없음",
        )
    )
    lines.append("- 위 표시는 관련 Learning Log의 자기 설명·수정 이해에서 최소 evidence keyword가 모두 확인된 경우만 생성함")
    lines.extend(["", "## Blocking Gaps", ""])
    blocking_gaps = [criterion.text for criterion in plan.remaining]
    blocking_gaps.extend(plan.blocking_questions)
    lines.extend(bullet_lines(blocking_gaps))
    lines.extend(["", "## Optional Open Questions", ""])
    lines.extend(bullet_lines(list(plan.optional_questions)))
    if plan.boundary.optional_deep_dive:
        lines.append("- 명시적 deep-dive 요청 때 선택 가능한 범위: " + "; ".join(plan.boundary.optional_deep_dive))
    lines.extend(["", "## Recommended Next Move", ""])
    lines.append(f"- Decision: **{plan.recommended_move}**")
    lines.append(f"- 이유: {move_explanations[plan.recommended_move]}")
    if blocking_gaps:
        lines.append(f"- 우선 학습: {blocking_gaps[0]}")
    else:
        lines.append(f"- 우선 학습: {plan.boundary.next_roadmap_topic}")
    lines.extend(["", "## Required Source Before First Learning Unit", ""])
    lines.extend(f"- `{path}`" for path in plan.grounding_paths)
    if plan.remaining:
        lines.append("- 이유: 첫 Blocking Gap과 가장 가까운 저장 evidence를 확인해 사용자의 실제 설명 수준에 맞춘다.")
    else:
        lines.append("- 이유: 다음 topic의 depth boundary를 확인한 뒤 새 학습을 시작한다.")
    lines.append("- 이유: 최신 의미 있는 Learning Log를 최대 2개 읽어 최근 이해·오해 수정·다음 행동을 실제 evidence로 확인한다.")
    lines.append("- 이 source를 읽기 전에는 일반 지식만으로 첫 설명이나 진단 질문을 만들지 않는다.")
    lines.extend(["", "## Next Roadmap Topic", "", f"- {plan.boundary.next_roadmap_topic}"])
    lines.extend(["", "## 현재 확인된 핵심 개념", ""])
    lines.extend(bullet_lines(concepts))
    lines.extend(["", "## 미완료 자기 설명 점검", ""])
    lines.extend(bullet_lines(weaknesses))
    lines.extend(["", "## 최근 Learning Log의 다음 행동 (참고용)", ""])
    lines.extend(bullet_lines(actions))
    lines.append("- 위 항목은 source evidence이며 Roadmap-aware 추천보다 우선하지 않음")
    lines.extend(["", "## 제외한 기록과 이유", ""])
    lines.extend(bullet_lines([f"`{path}` — {why}" for path, why in excluded]))
    lines.extend(["", "## 참고한 source paths", "", "- `roadmap/ROADMAP.md`", "- `roadmap/LEARNING_BOUNDARIES.json`", "- `roadmap/PROGRESS.md`"])
    lines.extend(f"- `{path}`" for path in plan.evidence_paths)
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", default="state/CURRENT_LEARNING_CONTEXT.md")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_context(root), encoding="utf-8")
    print(f"Refreshed {output.relative_to(root).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
