#!/usr/bin/env python3
"""Apply one approved Current Boundary transition to Progress."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

from learning_boundaries import (
    LearningBoundary,
    boundary_by_id,
    load_boundaries,
)


TARGET_PATH = "roadmap/PROGRESS.md"
TITLE_RE = re.compile(r"^\[progress-update\] (?P<date>\d{4}-\d{2}-\d{2})$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
EVIDENCE_RE = re.compile(
    r"^learning-logs/\d{4}/\d{2}/\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"
)
ENVELOPE_RE = re.compile(
    r"\A<!--\s*research-os-progress-update:v2\s*\n(?P<meta>.*?)\n-->\s*\n?",
    re.DOTALL,
)
FOCUS_HEADING = "## 3. Current Focus"
RESULT_MARKER = "<!-- research-os-result -->"
MAX_ERROR_MESSAGE_LENGTH = 300


class ProgressUpdateError(RuntimeError):
    def __init__(self, message: str, code: str = "progress-validation-error") -> None:
        super().__init__(message)
        self.code = code


def git_blob_sha(content: bytes) -> str:
    content = content.replace(b"\r\n", b"\n")
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def parse_envelope(body: str) -> tuple[dict[str, str], dict]:
    match = ENVELOPE_RE.match(body.strip())
    if not match:
        raise ProgressUpdateError(
            "Issue 본문 첫 부분에 research-os-progress-update:v2 메타데이터가 없습니다.",
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
                raise ProgressUpdateError(
                    f"JSON key가 중복되었습니다: {key}", "invalid-proposal"
                )
            result[key] = value
        return result

    try:
        proposal = json.loads(
            body.strip()[match.end() :].strip(), object_pairs_hook=reject_duplicate_keys
        )
    except json.JSONDecodeError as error:
        raise ProgressUpdateError(
            "제안서가 유효한 JSON이 아닙니다.", "invalid-proposal"
        ) from error
    if not isinstance(proposal, dict):
        raise ProgressUpdateError("제안서는 JSON object여야 합니다.", "invalid-proposal")
    return metadata, proposal


def validate_scalar(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
        raise ProgressUpdateError(f"{name}은 비어 있지 않은 한 줄 문자열이어야 합니다.")
    if len(value) > 300:
        raise ProgressUpdateError(f"{name}이 너무 깁니다.")
    return value


def validate_proposal(
    proposal: dict, root: Path, boundaries: list[LearningBoundary]
) -> dict[str, str]:
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
    if not isinstance(changes, list) or len(changes) != 1:
        raise ProgressUpdateError("changes는 Current Boundary 변경 한 개만 허용합니다.")
    change = changes[0]
    if not isinstance(change, dict) or set(change) != {"type", "from", "to"}:
        raise ProgressUpdateError(
            "Current Boundary change 필드가 계약과 다릅니다.", "invalid-proposal"
        )
    if change.get("type") != "current_boundary":
        raise ProgressUpdateError(
            "current_boundary change만 허용합니다.", "invalid-change-type"
        )

    old = validate_scalar(change["from"], "from")
    new = validate_scalar(change["to"], "to")
    if old == new:
        raise ProgressUpdateError("from과 to가 같은 변경은 허용하지 않습니다.")
    try:
        boundary_by_id(boundaries, old)
        boundary_by_id(boundaries, new)
    except ValueError as error:
        raise ProgressUpdateError(str(error), "invalid-boundary") from error
    return {"type": "current_boundary", "from": old, "to": new}


def focus_section(content: str) -> tuple[int, int, str]:
    start = content.find(FOCUS_HEADING)
    if start < 0:
        raise ProgressUpdateError("Current Focus section을 찾을 수 없습니다.")
    end = content.find("\n## ", start + len(FOCUS_HEADING))
    if end < 0:
        end = len(content)
    return start, end, content[start:end].rstrip()


def replace_current_boundary(content: str, old: str, new: str) -> str:
    start, end, section = focus_section(content)
    pattern = re.compile(
        rf"^- Current Boundary: {re.escape(old)}$", re.MULTILINE
    )
    if len(pattern.findall(section)) != 1:
        raise ProgressUpdateError(
            "Current Boundary가 제안서의 from과 다릅니다.", "stale-value"
        )
    updated_section = pattern.sub(
        lambda _: f"- Current Boundary: {new}", section, count=1
    )
    suffix = content[end:]
    if not suffix:
        updated_section += "\n"
    return content[:start] + updated_section + suffix


def apply_update(payload: dict, root: Path) -> tuple[str, int]:
    title = str(payload.get("title") or "")
    title_match = TITLE_RE.fullmatch(title)
    if not title_match:
        raise ProgressUpdateError(
            "Issue 제목은 [progress-update] YYYY-MM-DD 형식이어야 합니다.",
            "invalid-title",
        )
    try:
        date.fromisoformat(title_match.group("date"))
    except ValueError as error:
        raise ProgressUpdateError(
            "Issue 제목의 날짜가 유효하지 않습니다.", "invalid-title"
        ) from error

    author = str(payload.get("author") or "")
    owner = str(payload.get("repository_owner") or "")
    if not author or author.casefold() != owner.casefold():
        raise ProgressUpdateError(
            "Repository owner가 만든 Issue만 처리할 수 있습니다.", "unauthorized"
        )

    metadata, proposal = parse_envelope(str(payload.get("body") or ""))
    if metadata["target_path"] != TARGET_PATH:
        raise ProgressUpdateError(
            "target_path는 roadmap/PROGRESS.md만 허용합니다.", "invalid-target"
        )
    expected_sha = metadata["expected_sha"].lower()
    if not SHA_RE.fullmatch(expected_sha):
        raise ProgressUpdateError(
            "읽어서 확인한 40자리 expected_sha가 필요합니다.", "invalid-sha"
        )

    target = root / TARGET_PATH
    if not target.is_file():
        raise ProgressUpdateError("roadmap/PROGRESS.md가 없습니다.", "missing-target")
    actual_sha = git_blob_sha(target.read_bytes())
    if actual_sha != expected_sha:
        raise ProgressUpdateError(
            f"PROGRESS.md가 제안 후 변경되었습니다. expected {expected_sha}, actual {actual_sha}",
            "stale-sha",
        )

    try:
        boundaries = load_boundaries(root)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise ProgressUpdateError(
            f"Learning Boundary 계약을 읽을 수 없습니다: {error}",
            "invalid-boundary-contract",
        ) from error
    change = validate_proposal(proposal, root, boundaries)
    original = target.read_text(encoding="utf-8")
    updated = replace_current_boundary(original, change["from"], change["to"])
    if updated == original:
        raise ProgressUpdateError("제안서가 실제 변경을 만들지 않았습니다.")
    target.write_text(updated, encoding="utf-8")
    return TARGET_PATH, 1


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
                output.write(
                    f"target_path={target_path}\nchange_count={change_count}\n"
                )
        return 0
    except (ProgressUpdateError, json.JSONDecodeError, OSError) as error:
        code = getattr(error, "code", "progress-processing-error")
        write_report(args.report, failure_report(code, str(error)))
        print(
            f"Progress Update 실패 [{code}]: {sanitize_error_message(str(error))}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
