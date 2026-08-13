#!/usr/bin/env python3
"""Build the derived current learning context from repository-native sources."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


AI_LEARNING_DOMAINS = {
    "ai-computation",
    "computer-architecture",
    "memory-architecture",
    "sram",
    "dram",
    "npu",
    "pim-cim",
    "paper",
}
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
    topic: str
    domain: str
    roadmap_stage: str
    sections: dict[str, str]


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


def classify_log(path: Path, root: Path) -> tuple[LearningLog | None, str | None]:
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
    domain = metadata["Domain"]
    if domain == "research-os":
        return None, "Domain이 research-os인 시스템 개발·운영 기록"
    if domain not in AI_LEARNING_DOMAINS:
        return None, f"AI semiconductor 학습 domain이 아님: {domain}"
    if metadata["Roadmap stage"].casefold() == "system-development":
        return None, "Roadmap stage가 system-development인 시스템 개발 기록"
    missing_sections = [heading for heading in REQUIRED_SECTIONS if heading not in sections]
    if missing_sections:
        return None, "필수 Learning Log section 누락: " + ", ".join(missing_sections)

    return (
        LearningLog(
            path=relative,
            date=parsed_date,
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
    paths = sorted(
        (root / "learning-logs").glob("**/*.md"), key=lambda item: item.as_posix()
    )
    for path in paths:
        log, reason = classify_log(path, root)
        if log:
            included.append(log)
        else:
            excluded.append((repository_path(path, root), reason or "분류할 수 없음"))
    included.sort(key=lambda item: (item.date, item.path))
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


def progress_reconciliation(progress: str, latest: Iterable[LearningLog]) -> tuple[str, str]:
    latest_logs = list(latest)
    if not latest_logs:
        return "not-needed", "의미 있는 Learning Log가 없어 dashboard와 비교할 학습 evidence가 없음"

    current_stage = re.search(r"^- Current Stage:\s*(.+)$", progress, re.MULTILINE)
    current_topic = re.search(r"^- Current Topic:\s*(.+)$", progress, re.MULTILINE)
    stage_value = current_stage.group(1).strip() if current_stage else ""
    topic_value = current_topic.group(1).strip() if current_topic else ""
    pending_reasons: list[str] = []
    if not stage_value or stage_value.casefold() == "not started":
        pending_reasons.append("의미 있는 Learning Log가 있지만 Current Stage가 Not Started")
    if not topic_value or topic_value in {"아직 지정되지 않음", "없음", "Not Started"}:
        pending_reasons.append("의미 있는 Learning Log가 있지만 Current Topic이 지정되지 않음")
    latest_stages = {item.roadmap_stage for item in latest_logs}
    if stage_value and stage_value.casefold() != "not started" and stage_value not in latest_stages:
        pending_reasons.append("최신 Learning Log stage와 dashboard Current Stage가 일치하지 않음")
    dashboard_rows: dict[str, str] = {}
    for line in progress.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) >= 2:
            dashboard_rows[cells[0]] = cells[1]
    for item in latest_logs:
        for label in DASHBOARD_LABELS.get(item.domain, ()):
            if dashboard_rows.get(label) == "Not Started":
                pending_reasons.append(
                    f"최신 Learning Log domain({item.domain})의 dashboard 상태가 Not Started"
                )
                break
    pending_reasons = list(dict.fromkeys(pending_reasons))
    if pending_reasons:
        return "pending", "; ".join(pending_reasons)
    return "aligned", "최신 Learning Log와 dashboard의 현재 stage/topic에 명백한 충돌이 없음"


def bullet_lines(items: list[str], empty: str = "없음") -> list[str]:
    return [f"- {item}" for item in items] if items else [f"- {empty}"]


def build_context(root: Path) -> str:
    included, excluded = discover_logs(root)
    progress_path = root / "roadmap/PROGRESS.md"
    progress = progress_path.read_text(encoding="utf-8")
    roadmap_path = root / "roadmap/ROADMAP.md"
    roadmap_path.read_text(encoding="utf-8")  # Required source; validates readability.

    if not included:
        status, reason = progress_reconciliation(progress, [])
        lines = [
            "# Current Learning Context",
            "",
            "> 이 문서는 `learning-logs/**`와 roadmap에서 자동 생성한 derived/generated snapshot이다. Source of truth가 아니며 원본 기록을 다시 확인할 수 있다.",
            "",
            "- Last generated date: 없음",
            f"- Roadmap reconciliation: **{status}**",
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
            f"- {reason}",
            "- `roadmap/PROGRESS.md`는 자동 수정하지 않음",
            "",
            "## 제외한 기록과 이유",
            "",
        ]
        lines.extend(bullet_lines([f"`{path}` — {why}" for path, why in excluded]))
        lines.extend(["", "## 참고한 source paths", "", "- `roadmap/ROADMAP.md`", "- `roadmap/PROGRESS.md`", ""])
        return "\n".join(lines)

    latest_date = included[-1].date
    latest_logs = [item for item in included if item.date == latest_date]
    primary = latest_logs[-1]
    concepts = extract_items(primary.sections["## 3. 핵심 개념"], LIMITS["concepts"])
    unresolved = extract_items(
        extract_subsection(primary.sections["## 7. 질문"], "### 해결되지 않은 질문"),
        LIMITS["questions"],
    )
    weaknesses = extract_unfinished(
        primary.sections["## 10. 자기 설명 점검"], LIMITS["weaknesses"]
    )
    actions = extract_items(primary.sections["## 9. 다음 행동"], LIMITS["actions"])
    status, reason = progress_reconciliation(progress, latest_logs)

    lines = [
        "# Current Learning Context",
        "",
        "> 이 문서는 `learning-logs/**`와 roadmap에서 자동 생성한 derived/generated snapshot이다. Source of truth가 아니며 원본 기록을 다시 확인할 수 있다.",
        "",
        f"- Last generated date: {latest_date.isoformat()}",
        f"- Roadmap reconciliation: **{status}**",
        "",
        "## 현재 상태",
        "",
        f"- 최신 의미 있는 학습 기록: `{primary.path}`",
        f"- Current Topic: {primary.topic}",
        f"- Domain: {primary.domain}",
        f"- Roadmap stage: {primary.roadmap_stage}",
        "",
        "### 같은 날짜의 의미 있는 학습 단위",
        "",
    ]
    lines.extend(bullet_lines([f"`{item.path}` — {item.topic}" for item in latest_logs]))
    lines.extend(["", "## 현재 확인된 핵심 개념", ""])
    lines.extend(bullet_lines(concepts))
    lines.extend(["", "## 아직 해결되지 않은 질문", ""])
    lines.extend(bullet_lines(unresolved))
    lines.extend(["", "## 미완료 자기 설명 점검", ""])
    lines.extend(bullet_lines(weaknesses))
    lines.extend(["", "## 바로 다음 행동", ""])
    lines.extend(bullet_lines(actions))
    lines.extend(["", "## Roadmap reconciliation", "", f"- {reason}", "- `roadmap/PROGRESS.md`는 자동 수정하지 않음", "", "## 제외한 기록과 이유", ""])
    lines.extend(bullet_lines([f"`{path}` — {why}" for path, why in excluded]))
    lines.extend(["", "## 참고한 source paths", "", "- `roadmap/ROADMAP.md`", "- `roadmap/PROGRESS.md`"])
    lines.extend(f"- `{item.path}`" for item in latest_logs)
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
