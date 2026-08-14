#!/usr/bin/env python3
"""Apply one approved, evidence-backed Progress update Issue."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path


TARGET_PATH = "roadmap/PROGRESS.md"
TITLE_RE = re.compile(r"^\[progress-update\] (?P<date>\d{4}-\d{2}-\d{2})$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
EVIDENCE_RE = re.compile(
    r"^learning-logs/\d{4}/\d{2}/\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"
)
ENVELOPE_RE = re.compile(
    r"\A<!--\s*research-os-progress-update:v1\s*\n(?P<meta>.*?)\n-->\s*\n?",
    re.DOTALL,
)
CURRENT_FOCUS_FIELDS = {"Current Stage", "Current Topic", "Last Updated"}
CANONICAL_STAGES = {
    "Stage 0 — Big Picture",
    "Stage 1 — AI Computation",
    "Stage 2 — Computer Architecture",
    "Stage 3 — Memory",
    "Stage 4 — NPU Architecture",
    "Stage 5 — PIM / CIM",
    "Stage 6 — Foundational Papers",
    "Stage 7 — SSL Lab Papers",
    "Stage 8 — Research Portfolio",
}
FORBIDDEN_CURRENT_FOCUS_FIELDS = {
    "Execution Phase",
    "Active Track",
    "Current Deliverable",
    "Current Bottleneck",
    "Next Milestone",
    "Phase Deadline",
}
RESULT_MARKER = "<!-- research-os-result -->"
MAX_ERROR_MESSAGE_LENGTH = 300


class ProgressUpdateError(RuntimeError):
    def __init__(self, message: str, code: str = "progress-validation-error") -> None:
        super().__init__(message)
        self.code = code


def git_blob_sha(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def parse_envelope(body: str) -> tuple[dict[str, str], dict]:
    match = ENVELOPE_RE.match(body.strip())
    if not match:
        raise ProgressUpdateError(
            "Issue 본문 첫 부분에 research-os-progress-update:v1 메타데이터가 없습니다.",
            "invalid-envelope",
        )

    metadata: dict[str, str] = {}
    for raw_line in match.group("meta").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            raise ProgressUpdateError("잘못된 메타데이터 행이 있습니다.", "invalid-metadata")
        key, value = line.split(":", 1)
        key = key.strip()
        if key in metadata:
            raise ProgressUpdateError(f"중복 메타데이터입니다: {key}", "invalid-metadata")
        metadata[key] = value.strip()

    if set(metadata) != {"target_path", "expected_sha"}:
        raise ProgressUpdateError(
            "메타데이터는 target_path와 expected_sha만 포함해야 합니다.",
            "invalid-metadata",
        )

    def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict:
        result: dict = {}
        for key, value in pairs:
            if key in result:
                raise ProgressUpdateError(f"JSON key가 중복되었습니다: {key}", "invalid-proposal")
            result[key] = value
        return result

    try:
        proposal = json.loads(
            body.strip()[match.end() :].strip(), object_pairs_hook=reject_duplicate_keys
        )
    except json.JSONDecodeError as error:
        raise ProgressUpdateError("제안서가 유효한 JSON이 아닙니다.", "invalid-proposal") from error
    if not isinstance(proposal, dict):
        raise ProgressUpdateError("제안서는 JSON object여야 합니다.", "invalid-proposal")
    return metadata, proposal


def validate_scalar(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
        raise ProgressUpdateError(f"{name}은 비어 있지 않은 한 줄 문자열이어야 합니다.")
    if len(value) > 300:
        raise ProgressUpdateError(f"{name}이 너무 깁니다.")
    return value


def validate_proposal(proposal: dict, root: Path, issue_date: str) -> list[dict[str, str]]:
    if set(proposal) != {"evidence_paths", "changes"}:
        raise ProgressUpdateError(
            "제안서는 evidence_paths와 changes만 포함해야 합니다.", "invalid-proposal"
        )

    evidence_paths = proposal["evidence_paths"]
    if not isinstance(evidence_paths, list) or not evidence_paths:
        raise ProgressUpdateError("최소 한 개의 Learning Log evidence_path가 필요합니다.")
    if len(evidence_paths) != len(set(map(str, evidence_paths))):
        raise ProgressUpdateError("evidence_path가 중복되었습니다.")
    for raw_path in evidence_paths:
        path = validate_scalar(raw_path, "evidence_path")
        if not EVIDENCE_RE.fullmatch(path):
            raise ProgressUpdateError(
                "evidence_path는 실제 learning-logs/YYYY/MM/*.md 경로여야 합니다."
            )
        if not (root / path).is_file():
            raise ProgressUpdateError(f"학습 evidence 파일이 없습니다: {path}")

    changes = proposal["changes"]
    if not isinstance(changes, list) or not 1 <= len(changes) <= 4:
        raise ProgressUpdateError("changes는 1개 이상 4개 이하이어야 합니다.")

    validated: list[dict[str, str]] = []
    targets: set[tuple[str, str]] = set()
    substantive_changes = 0
    for raw_change in changes:
        if not isinstance(raw_change, dict):
            raise ProgressUpdateError("각 change는 JSON object여야 합니다.")
        change_type = raw_change.get("type")
        if change_type == "current_focus":
            if set(raw_change) != {"type", "field", "from", "to"}:
                raise ProgressUpdateError("current_focus change 필드가 계약과 다릅니다.")
            field = validate_scalar(raw_change["field"], "field")
            if field in FORBIDDEN_CURRENT_FOCUS_FIELDS or field not in CURRENT_FOCUS_FIELDS:
                raise ProgressUpdateError(
                    f"자동 변경이 금지된 Current Focus 필드입니다: {field}",
                    "forbidden-field",
                )
            old = validate_scalar(raw_change["from"], "from")
            new = validate_scalar(raw_change["to"], "to")
            if old == new:
                raise ProgressUpdateError("from과 to가 같은 변경은 허용하지 않습니다.")
            if field == "Current Stage":
                if new not in CANONICAL_STAGES:
                    raise ProgressUpdateError("Current Stage의 canonical 형식이 아닙니다.")
            elif field == "Last Updated":
                try:
                    date.fromisoformat(new)
                except ValueError as error:
                    raise ProgressUpdateError("Last Updated는 YYYY-MM-DD 형식이어야 합니다.") from error
                if new != issue_date:
                    raise ProgressUpdateError("Last Updated는 Issue 제목의 날짜와 같아야 합니다.")
            if field != "Last Updated":
                substantive_changes += 1
            target = (change_type, field)
        elif change_type == "dashboard_status":
            if set(raw_change) != {"type", "stage", "from", "to"}:
                raise ProgressUpdateError("dashboard_status change 필드가 계약과 다릅니다.")
            stage = validate_scalar(raw_change["stage"], "stage")
            old = validate_scalar(raw_change["from"], "from")
            new = validate_scalar(raw_change["to"], "to")
            if (old, new) != ("Not Started", "Learning"):
                raise ProgressUpdateError(
                    "Dashboard 자동 변경은 Not Started → Learning만 허용합니다.",
                    "forbidden-transition",
                )
            substantive_changes += 1
            target = (change_type, stage)
        else:
            raise ProgressUpdateError("지원하지 않는 change type입니다.", "invalid-change-type")

        if target in targets:
            raise ProgressUpdateError("같은 대상을 두 번 변경할 수 없습니다.")
        targets.add(target)
        validated.append({key: str(value) for key, value in raw_change.items()})

    if substantive_changes == 0:
        raise ProgressUpdateError("Last Updated만 단독으로 변경할 수 없습니다.")
    return validated


def replace_current_focus(content: str, field: str, old: str, new: str) -> str:
    section_start = content.find("## 3. Current Focus")
    section_end = content.find("\n## ", section_start + 1)
    if section_start < 0 or section_end < 0:
        raise ProgressUpdateError("Current Focus section을 찾을 수 없습니다.")
    section = content[section_start:section_end]
    pattern = re.compile(rf"^- {re.escape(field)}: {re.escape(old)}$", re.MULTILINE)
    if len(pattern.findall(section)) != 1:
        raise ProgressUpdateError(f"현재 값이 제안서의 from과 다릅니다: {field}", "stale-value")
    updated = pattern.sub(lambda _: f"- {field}: {new}", section, count=1)
    return content[:section_start] + updated + content[section_end:]


def replace_dashboard_status(content: str, stage: str, old: str, new: str) -> str:
    section_start = content.find("## 4. Progress Dashboard")
    section_end = content.find("\n## ", section_start + 1)
    if section_start < 0 or section_end < 0:
        raise ProgressUpdateError("Progress Dashboard section을 찾을 수 없습니다.")
    section = content[section_start:section_end]
    lines = section.splitlines(keepends=True)
    matches = []
    for index, line in enumerate(lines):
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0] == stage:
            matches.append((index, cells, "\r\n" if line.endswith("\r\n") else "\n"))
    if len(matches) != 1:
        raise ProgressUpdateError(f"Dashboard stage를 정확히 하나 찾을 수 없습니다: {stage}")
    index, cells, ending = matches[0]
    if cells[1] != old:
        raise ProgressUpdateError(f"Dashboard 현재 값이 제안서의 from과 다릅니다: {stage}", "stale-value")
    cells[1] = new
    lines[index] = "| " + " | ".join(cells) + " |" + ending
    updated = "".join(lines)
    return content[:section_start] + updated + content[section_end:]


def apply_update(payload: dict, root: Path) -> tuple[str, int]:
    title = str(payload.get("title") or "")
    title_match = TITLE_RE.fullmatch(title)
    if not title_match:
        raise ProgressUpdateError(
            "Issue 제목은 [progress-update] YYYY-MM-DD 형식이어야 합니다.", "invalid-title"
        )
    try:
        date.fromisoformat(title_match.group("date"))
    except ValueError as error:
        raise ProgressUpdateError("Issue 제목의 날짜가 유효하지 않습니다.", "invalid-title") from error
    author = str(payload.get("author") or "")
    owner = str(payload.get("repository_owner") or "")
    if not author or author.casefold() != owner.casefold():
        raise ProgressUpdateError("Repository owner가 만든 Issue만 처리할 수 있습니다.", "unauthorized")

    metadata, proposal = parse_envelope(str(payload.get("body") or ""))
    if metadata["target_path"] != TARGET_PATH:
        raise ProgressUpdateError("target_path는 roadmap/PROGRESS.md만 허용합니다.", "invalid-target")
    expected_sha = metadata["expected_sha"].lower()
    if not SHA_RE.fullmatch(expected_sha):
        raise ProgressUpdateError("읽어서 확인한 40자리 expected_sha가 필요합니다.", "invalid-sha")

    target = root / TARGET_PATH
    if not target.is_file():
        raise ProgressUpdateError("roadmap/PROGRESS.md가 없습니다.", "missing-target")
    actual_sha = git_blob_sha(target.read_bytes())
    if actual_sha != expected_sha:
        raise ProgressUpdateError(
            f"PROGRESS.md가 제안 후 변경되었습니다. expected {expected_sha}, actual {actual_sha}",
            "stale-sha",
        )

    changes = validate_proposal(proposal, root, title_match.group("date"))
    original = target.read_text(encoding="utf-8")
    updated = original
    for change in changes:
        if change["type"] == "current_focus":
            updated = replace_current_focus(
                updated, change["field"], change["from"], change["to"]
            )
        else:
            updated = replace_dashboard_status(
                updated, change["stage"], change["from"], change["to"]
            )
    if updated == original:
        raise ProgressUpdateError("제안서가 실제 변경을 만들지 않았습니다.")
    target.write_text(updated, encoding="utf-8")
    return TARGET_PATH, len(changes)


def sanitize_error_message(message: str) -> str:
    cleaned = " ".join(
        re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", message).splitlines()
    ).strip()
    if len(cleaned) > MAX_ERROR_MESSAGE_LENGTH:
        return cleaned[: MAX_ERROR_MESSAGE_LENGTH - 1] + "…"
    return cleaned or "알 수 없는 오류가 발생했습니다."


def failure_report(code: str, message: str) -> str:
    return (
        f"{RESULT_MARKER}\n"
        "❌ Progress Update 처리 실패\n\n"
        f"- Error code: `{code}`\n"
        f"- 원인: {sanitize_error_message(message)}\n"
        "- 파일 변경: 수행되지 않음\n"
    )


def write_report(path: str | None, report: str) -> None:
    if path:
        Path(path).write_text(report, encoding="utf-8")


def configure_stdio() -> None:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def main() -> int:
    configure_stdio()
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload", required=True)
    parser.add_argument("--root", default=".")
    parser.add_argument("--report")
    parser.add_argument("--github-output")
    args = parser.parse_args()
    try:
        payload = json.loads(Path(args.payload).read_text(encoding="utf-8"))
        target_path, change_count = apply_update(payload, Path(args.root))
        write_report(
            args.report,
            f"{RESULT_MARKER}\n✅ Progress Update 처리 완료\n\n"
            f"- Path: `{target_path}`\n- Applied changes: {change_count}\n",
        )
        if args.github_output:
            with open(args.github_output, "a", encoding="utf-8") as output:
                output.write(f"target_path={target_path}\nchange_count={change_count}\n")
        return 0
    except (ProgressUpdateError, json.JSONDecodeError, OSError) as error:
        code = getattr(error, "code", "progress-processing-error")
        write_report(args.report, failure_report(code, str(error)))
        print(f"Progress Update 실패 [{code}]: {sanitize_error_message(str(error))}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
