#!/usr/bin/env python3
"""Build the derived current learning context from repository-native sources."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable

from learning_log_metadata import DomainPolicy, load_domain_policy
from progress_policy import ProgressDecision, decide_progress


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
DASHBOARD_LABELS = {
    "ai-computation": ("AI Computation",),
    "computer-architecture": ("Computer Architecture",),
    "memory-architecture": ("Memory Architecture",),
    "sram": ("SRAM / DRAM / eDRAM",),
    "dram": ("SRAM / DRAM / eDRAM",),
    "npu": ("NPU Architecture",),
    "pim-cim": ("PIM / CIM",),
    "paper": ("Foundational Papers", "KAIST SSL Lab Papers"),
}


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
class ExitCriterion:
    text: str
    evidence_groups: tuple[tuple[str, ...], ...]


@dataclass(frozen=True)
class LearningBoundary:
    id: str
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


def load_boundaries(root: Path) -> list[LearningBoundary]:
    path = root / "roadmap/LEARNING_BOUNDARIES.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("version") != 1 or payload.get("policy") != "progression-over-exhaustiveness":
        raise ValueError("Unsupported learning boundary contract")
    boundaries: list[LearningBoundary] = []
    for raw in payload.get("boundaries", []):
        criteria = tuple(
            ExitCriterion(
                text=item["text"],
                evidence_groups=tuple(tuple(group) for group in item["evidence_groups"]),
            )
            for item in raw["exit_criteria"]
        )
        boundaries.append(
            LearningBoundary(
                id=raw["id"],
                progress_topics=tuple(raw["progress_topics"]),
                domains=tuple(raw["domains"]),
                evidence_domains=tuple(raw.get("evidence_domains", raw["domains"])),
                roadmap_stage=raw["roadmap_stage"],
                topic_goal=raw["topic_goal"],
                minimum_required_understanding=tuple(raw["minimum_required_understanding"]),
                exit_criteria=criteria,
                blocking_question_keywords=tuple(raw["blocking_question_keywords"]),
                optional_question_keywords=tuple(raw["optional_question_keywords"]),
                optional_deep_dive=tuple(raw["optional_deep_dive"]),
                next_roadmap_topic=raw["next_roadmap_topic"],
            )
        )
    if not boundaries:
        raise ValueError("No learning boundaries configured")
    return boundaries


def progress_value(progress: str, label: str) -> str:
    match = re.search(rf"^- {re.escape(label)}:\s*(.+)$", progress, re.MULTILINE)
    return match.group(1).strip() if match else ""


def select_boundary(
    boundaries: Iterable[LearningBoundary], progress: str, primary: LearningLog
) -> LearningBoundary:
    available = list(boundaries)
    current_topic = progress_value(progress, "Current Topic").casefold()
    for boundary in available:
        if any(alias.casefold() == current_topic for alias in boundary.progress_topics):
            return boundary
    for boundary in available:
        if primary.domain in boundary.domains:
            return boundary
    raise ValueError(
        f"No learning boundary for Current Topic={current_topic or '없음'} / domain={primary.domain}"
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
    relevant: list[LearningLog], remaining: tuple[ExitCriterion, ...]
) -> tuple[str, ...]:
    if not remaining:
        return ("roadmap/LEARNING_BOUNDARIES.json",)

    criterion = remaining[0]
    ranked = sorted(
        relevant,
        key=lambda log: (
            criterion_match_count(criterion, evidence_corpus([log])),
            learning_log_order(log),
        ),
        reverse=True,
    )
    return (ranked[0].path,) if ranked else ()


def contains_keyword(text: str, keywords: Iterable[str]) -> bool:
    folded = text.casefold()
    return any(keyword.casefold() in folded for keyword in keywords)


def build_learning_plan(
    boundaries: Iterable[LearningBoundary],
    progress: str,
    included: Iterable[LearningLog],
    primary: LearningLog,
) -> LearningPlan:
    boundary = select_boundary(boundaries, progress, primary)
    relevant = [log for log in included if log.domain in boundary.evidence_domains]
    corpus = evidence_corpus(relevant)
    completed = tuple(item for item in boundary.exit_criteria if criterion_is_met(item, corpus))
    remaining = tuple(item for item in boundary.exit_criteria if item not in completed)

    latest_date = max(log.date for log in relevant)
    latest_relevant = [log for log in relevant if log.date == latest_date]
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
        grounding_paths=select_grounding_paths(relevant, remaining),
        evidence_paths=tuple(log.path for log in relevant),
    )


def dashboard_labels_for_log(log: LearningLog) -> tuple[str, ...]:
    if log.domain != "paper":
        return DASHBOARD_LABELS.get(log.domain, ())
    stage = log.roadmap_stage.casefold()
    if "stage 6" in stage or "foundational" in stage:
        return ("Foundational Papers",)
    if "stage 7" in stage or "ssl" in stage:
        return ("KAIST SSL Lab Papers",)
    return ()


def progress_decision(
    progress: str, included: Iterable[LearningLog], plan: LearningPlan | None
) -> ProgressDecision:
    logs = list(included)
    if not logs or plan is None:
        return decide_progress(
            progress,
            has_evidence=False,
            canonical_stage="",
            canonical_topic="",
            next_roadmap_topic="",
            recommended_move="continue",
            evidence_dashboard_labels=(),
        )
    labels = [label for log in logs for label in dashboard_labels_for_log(log)]
    return decide_progress(
        progress,
        has_evidence=True,
        canonical_stage=plan.boundary.roadmap_stage,
        canonical_topic=plan.boundary.progress_topics[0],
        next_roadmap_topic=plan.boundary.next_roadmap_topic,
        recommended_move=plan.recommended_move,
        evidence_dashboard_labels=labels,
    )


def bullet_lines(items: list[str], empty: str = "없음") -> list[str]:
    return [f"- {item}" for item in items] if items else [f"- {empty}"]


def build_context(root: Path) -> str:
    included, excluded = discover_logs(root)
    progress_path = root / "roadmap/PROGRESS.md"
    progress = progress_path.read_text(encoding="utf-8")
    roadmap_path = root / "roadmap/ROADMAP.md"
    roadmap_path.read_text(encoding="utf-8")  # Required source; validates readability.
    boundaries = load_boundaries(root)

    if not included:
        decision = progress_decision(progress, [], None)
        lines = [
            "# Current Learning Context",
            "",
            "> 이 문서는 `learning-logs/**`와 roadmap에서 자동 생성한 derived/generated snapshot이다. Source of truth가 아니며 원본 기록을 다시 확인할 수 있다.",
            "",
            "- Last generated date: 없음",
            f"- Roadmap reconciliation: **{decision.status}**",
            "",
            "## 현재 상태",
            "",
            "- 최신 의미 있는 학습 기록: 없음",
            "- Current Topic: 없음",
            "- Domain: 없음",
            "- Roadmap stage: 없음",
            "",
            "## Roadmap reconciliation",
            "",
            f"- {decision.reason}",
            "- `roadmap/PROGRESS.md`는 자동 수정하지 않음",
            "",
            "## 제외한 기록과 이유",
            "",
        ]
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
    latest_logs = [item for item in included if item.date == latest_date]
    primary = latest_logs[-1]
    concepts = extract_items(primary.sections["## 3. 핵심 개념"], LIMITS["concepts"])
    weaknesses = extract_unfinished(
        primary.sections["## 10. 자기 설명 점검"], LIMITS["weaknesses"]
    )
    actions = extract_items(primary.sections["## 9. 다음 행동"], LIMITS["actions"])
    plan = build_learning_plan(boundaries, progress, included, primary)
    decision = progress_decision(progress, included, plan)
    current_stage = progress_value(progress, "Current Stage") or primary.roadmap_stage
    current_topic = progress_value(progress, "Current Topic") or primary.topic

    move_explanations = {
        "continue": "현재 topic의 blocking gap이 둘 이상이므로 필요한 최소 범위만 계속 학습한다.",
        "review_then_advance": "blocking gap 하나만 짧게 확인한 뒤 다음 Roadmap topic으로 이동한다.",
        "advance": "현재 exit criteria를 충족했으므로 optional question을 기본 경로에 넣지 않고 다음 Roadmap topic으로 이동한다.",
    }

    lines = [
        "# Current Learning Context",
        "",
        "> 이 문서는 `learning-logs/**`와 roadmap에서 자동 생성한 derived/generated snapshot이다. Source of truth가 아니며 원본 기록을 다시 확인할 수 있다.",
        "",
        f"- Last generated date: {latest_date.isoformat()}",
        f"- Roadmap reconciliation: **{decision.status}**",
        "",
        "## Roadmap Position",
        "",
        f"- 최신 의미 있는 학습 기록: `{primary.path}`",
        f"- Current Stage: {current_stage}",
        f"- Current Topic: {current_topic}",
        f"- Domain: {primary.domain}",
        f"- Depth Boundary: `{plan.boundary.id}`",
        "",
        "### 같은 날짜의 의미 있는 학습 단위",
        "",
    ]
    lines.extend(bullet_lines([f"`{item.path}` — {item.topic}" for item in latest_logs]))
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
    lines.append("- 이 source를 읽기 전에는 일반 지식만으로 첫 설명이나 진단 질문을 만들지 않는다.")
    lines.extend(["", "## Next Roadmap Topic", "", f"- {plan.boundary.next_roadmap_topic}"])
    lines.extend(["", "## 현재 확인된 핵심 개념", ""])
    lines.extend(bullet_lines(concepts))
    lines.extend(["", "## 미완료 자기 설명 점검", ""])
    lines.extend(bullet_lines(weaknesses))
    lines.extend(["", "## 최근 Learning Log의 다음 행동 (참고용)", ""])
    lines.extend(bullet_lines(actions))
    lines.append("- 위 항목은 source evidence이며 Roadmap-aware 추천보다 우선하지 않음")
    lines.extend(["", "## Roadmap reconciliation", "", f"- {decision.reason}", "- `roadmap/PROGRESS.md`는 자동 수정하지 않음", "", "## 제외한 기록과 이유", ""])
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
