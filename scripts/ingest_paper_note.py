#!/usr/bin/env python3
"""Convert one approved Paper Note Issue into one canonical checkpoint file."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path


TARGET_RE = re.compile(
    r"^paper-notes/(?P<paper_type>foundational|ssl-lab|related)/"
    r"(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)\.md$"
)
TITLE_RE = re.compile(r"^\[paper-note\] (?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
ENVELOPE_RE = re.compile(
    r"\A<!--\s*research-os-paper-note:v1\s*\n(?P<meta>.*?)\n-->\s*\n?",
    re.DOTALL,
)
RESULT_MARKER = "<!-- research-os-result -->"
COMMANDS = {"/기록", "/retry", "/ingest"}
PAPER_TYPES = {"foundational", "ssl-lab", "related"}
BRIDGE_STATUSES = {"studying", "paused", "sufficient-for-paper"}
PDF_ACCESS = "session-attachment (새 채팅마다 재첨부 필요)"
ENVELOPE_FIELDS = {"operation", "intent", "target_path", "expected_sha"}
REQUIRED_METADATA = (
    "Title",
    "Document type",
    "Paper type",
    "Venue / Year",
    "Authors",
    "Paper link",
    "PDF access",
    "Started",
    "Checkpoint recorded at",
    "Related notes",
)
REQUIRED_HEADINGS = (
    "## Metadata",
    "## 1. Citation",
    "## 2. Reading Checkpoint",
    "## 3. Prerequisite Bridge",
    "## 4. Problem",
    "## 5. Motivation and Prior-Work Gap",
    "## 6. Prerequisites",
    "## 7. Key Idea",
    "## 8. Architecture",
    "## 9. Method",
    "## 10. Experiments",
    "## 11. Results",
    "## 12. Trade-offs",
    "## 13. Limitations",
    "## 14. Questions",
    "## 15. Connection to My Research Interest",
    "## 16. Final Summary",
    "## 17. Reading Session History",
    "## 사용자 분석 근거",
)
FENCE_RE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})")
FIELD_RE = re.compile(r"^- (?P<key>[^:]+):\s*(?P<value>.*)$")
LEARNING_LOG_PATH_RE = re.compile(
    r"learning-logs/\d{4}/\d{2}/\d{4}-\d{2}-\d{2}-"
    r"[a-z0-9]+(?:-[a-z0-9]+)*\.md"
)
MAX_ERROR_MESSAGE_LENGTH = 300


class IngestError(RuntimeError):
    def __init__(self, message: str, code: str = "paper-note-validation-error") -> None:
        super().__init__(message)
        self.code = code


def git_blob_sha(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content).hexdigest()


def assemble(payload: dict) -> str:
    issue_author = str(payload.get("author") or "")
    repo_owner = str(payload.get("repository_owner") or "")
    allowed = {issue_author.casefold(), repo_owner.casefold()}
    chunks = [str(payload.get("body") or "").strip()]
    for comment in payload.get("comments") or []:
        author = str(comment.get("author") or "").casefold()
        body = str(comment.get("body") or "").strip()
        if author not in allowed or author.endswith("[bot]"):
            continue
        if not body or body in COMMANDS or body.startswith(RESULT_MARKER):
            continue
        chunks.append(body)
    return "\n\n".join(chunk for chunk in chunks if chunk).strip() + "\n"


def parse_envelope(assembled: str) -> tuple[dict[str, str], str]:
    match = ENVELOPE_RE.match(assembled)
    if not match:
        raise IngestError(
            "Issue 본문 첫 부분에 research-os-paper-note:v1 메타데이터가 없습니다."
        )
    metadata: dict[str, str] = {}
    for raw_line in match.group("meta").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            raise IngestError("잘못된 envelope 행이 있습니다.", "invalid-envelope")
        key, value = line.split(":", 1)
        key = key.strip()
        if key in metadata:
            raise IngestError(f"중복 envelope 필드: {key}", "invalid-envelope")
        metadata[key] = value.strip()
    missing = sorted(ENVELOPE_FIELDS - metadata.keys())
    extra = sorted(metadata.keys() - ENVELOPE_FIELDS)
    if missing:
        raise IngestError(
            "필수 envelope 필드 누락: " + ", ".join(missing),
            "invalid-envelope",
        )
    if extra:
        raise IngestError(
            "허용되지 않는 envelope 필드: " + ", ".join(extra),
            "invalid-envelope",
        )
    markdown = assembled[match.end() :].strip() + "\n"
    return metadata, markdown


def markdown_heading_lines(markdown: str) -> list[str]:
    headings: list[str] = []
    fence_char = ""
    fence_length = 0
    for line in markdown.splitlines():
        fence_match = FENCE_RE.match(line)
        if fence_match:
            fence = fence_match.group("fence")
            if not fence_char:
                fence_char = fence[0]
                fence_length = len(fence)
                continue
            if fence[0] == fence_char and len(fence) >= fence_length:
                fence_char = ""
                fence_length = 0
                continue
        if not fence_char and line.startswith("## "):
            headings.append(line.strip())
    return headings


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


def parse_fields(text: str, label: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        match = FIELD_RE.fullmatch(line.strip())
        if not match:
            continue
        key = match.group("key").strip()
        if key in fields:
            raise IngestError(f"{label}에 중복 필드가 있습니다: {key}")
        fields[key] = match.group("value").strip()
    return fields


def normalize_timestamp(value: object) -> str:
    raw = str(value or "").strip()
    if not TIMESTAMP_RE.fullmatch(raw):
        raise IngestError(
            "Issue created_at은 YYYY-MM-DDTHH:MM:SSZ 형식이어야 합니다.",
            "invalid-checkpoint-recorded-at",
        )
    try:
        parsed = dt.datetime.fromisoformat(raw.removesuffix("Z") + "+00:00")
    except ValueError as error:
        raise IngestError(
            "Issue created_at에 유효하지 않은 시각이 있습니다.",
            "invalid-checkpoint-recorded-at",
        ) from error
    return parsed.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def set_checkpoint_recorded_at(markdown: str, recorded_at: str) -> str:
    lines = markdown.splitlines()
    metadata_start = next(
        (index for index, line in enumerate(lines) if line == "## Metadata"), None
    )
    if metadata_start is None:
        return markdown
    metadata_end = next(
        (
            index
            for index in range(metadata_start + 1, len(lines))
            if lines[index].startswith("## ")
        ),
        len(lines),
    )
    checkpoint_lines: list[int] = []
    started_index = None
    for index in range(metadata_start + 1, metadata_end):
        match = FIELD_RE.fullmatch(lines[index].strip())
        if not match:
            continue
        key = match.group("key").strip()
        if key == "Checkpoint recorded at":
            checkpoint_lines.append(index)
        elif key == "Started":
            started_index = index
    for index in reversed(checkpoint_lines):
        del lines[index]
        if started_index is not None and index < started_index:
            started_index -= 1
    insert_at = (started_index + 1) if started_index is not None else metadata_start + 1
    lines.insert(insert_at, f"- Checkpoint recorded at: {recorded_at}")
    return "\n".join(lines).rstrip() + "\n"


def validate_target(target_path: str) -> re.Match[str]:
    match = TARGET_RE.fullmatch(target_path)
    if not match:
        raise IngestError(
            "target_path는 paper-notes/{foundational|ssl-lab|related}/"
            "YYYY-MM-DD-paper-slug.md 형식이어야 합니다."
        )
    try:
        dt.date.fromisoformat(match.group("date"))
    except ValueError as error:
        raise IngestError("target_path의 날짜가 유효하지 않습니다.") from error
    return match


def validate_bridges(bridge_text: str, root: Path) -> None:
    statuses = [
        match.group("value").strip()
        for line in bridge_text.splitlines()
        if (match := FIELD_RE.fullmatch(line.strip()))
        and match.group("key").strip() == "Status"
    ]
    invalid = sorted({status for status in statuses if status not in BRIDGE_STATUSES})
    if invalid:
        raise IngestError(
            "허용되지 않는 Bridge Status: " + ", ".join(invalid),
            "invalid-bridge-status",
        )
    if statuses.count("studying") > 1:
        raise IngestError(
            "한 Paper Note에서 studying인 선수지식은 최대 하나만 허용합니다.",
            "multiple-studying-bridges",
        )
    tracked_heading = "### 별도로 이어가는 선수지식"
    tracked_start = bridge_text.find(tracked_heading)
    if tracked_start < 0:
        raise IngestError(
            "Prerequisite Bridge에 '별도로 이어가는 선수지식' section이 없습니다.",
            "missing-tracked-bridge-section",
        )
    tracked_text = bridge_text[tracked_start + len(tracked_heading) :]
    next_section = re.search(r"(?m)^###\s+", tracked_text)
    if next_section:
        tracked_text = tracked_text[: next_section.start()]
    tracked_statuses = [
        match.group("value").strip()
        for line in tracked_text.splitlines()
        if (match := FIELD_RE.fullmatch(line.strip()))
        and match.group("key").strip() == "Status"
    ]
    concept_matches = list(re.finditer(r"(?m)^####\s+(?P<concept>.+?)\s*$", tracked_text))
    concept_statuses: list[str] = []
    for index, concept_match in enumerate(concept_matches):
        block_end = (
            concept_matches[index + 1].start()
            if index + 1 < len(concept_matches)
            else len(tracked_text)
        )
        concept = concept_match.group("concept").strip()
        block = tracked_text[concept_match.end() : block_end]
        fields = parse_fields(block, f"별도 선수지식 '{concept}'")
        status = fields.get("Status", "")
        if not status:
            raise IngestError(
                f"별도 선수지식에 Status가 필요합니다: {concept}",
                "missing-bridge-status",
            )
        concept_statuses.append(status)
        if status == "studying" and not LEARNING_LOG_PATH_RE.search(block):
            raise IngestError(
                f"studying 상태인 별도 선수지식에는 Learning Log가 필요합니다: {concept}",
                "studying-bridge-without-learning-log",
            )
    if len(tracked_statuses) != len(concept_statuses):
        raise IngestError(
            "별도 선수지식의 Status는 '#### Concept' 항목 안에 기록해야 합니다.",
            "invalid-tracked-bridge-structure",
        )
    referenced_paths = LEARNING_LOG_PATH_RE.findall(bridge_text)
    if len(referenced_paths) != len(set(referenced_paths)):
        raise IngestError(
            "Prerequisite Bridge에 중복 Learning Log 경로가 있습니다.",
            "duplicate-learning-log-path",
        )
    for relative_path in referenced_paths:
        if not (root / relative_path).is_file():
            raise IngestError(
                f"연결한 Learning Log가 존재하지 않습니다: {relative_path}",
                "missing-related-learning-log",
            )


def validate_markdown(markdown: str, target_match: re.Match[str], root: Path) -> None:
    if len(markdown) < 700:
        raise IngestError("Paper Note가 지나치게 짧습니다. canonical 전체 문서를 보내야 합니다.")
    if not markdown.startswith("# Paper Note:"):
        raise IngestError("문서는 '# Paper Note:' 제목으로 시작해야 합니다.")
    headings = markdown_heading_lines(markdown)
    duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
    if duplicates:
        raise IngestError(
            "중복 section이 있습니다: " + ", ".join(f"`{item}`" for item in duplicates),
            "duplicate-required-heading",
        )
    missing = [heading for heading in REQUIRED_HEADINGS if heading not in headings]
    if missing:
        raise IngestError(
            "필수 section이 없습니다: " + ", ".join(f"`{item}`" for item in missing),
            "missing-required-heading",
        )
    sections = parse_sections(markdown)
    metadata = parse_fields(sections["## Metadata"], "Paper Note Metadata")
    missing_metadata = [key for key in REQUIRED_METADATA if not metadata.get(key)]
    if missing_metadata:
        raise IngestError("필수 Paper Note Metadata 누락: " + ", ".join(missing_metadata))
    if metadata["Document type"] != "paper-note":
        raise IngestError("Document type은 paper-note여야 합니다.")
    if metadata["PDF access"] != PDF_ACCESS:
        raise IngestError(
            "PDF access는 session-attachment (새 채팅마다 재첨부 필요)여야 합니다."
        )
    if metadata["Paper type"] not in PAPER_TYPES:
        raise IngestError("Paper type은 foundational, ssl-lab, related 중 하나여야 합니다.")
    if metadata["Paper type"] != target_match.group("paper_type"):
        raise IngestError("Metadata의 Paper type과 target_path directory가 다릅니다.")
    try:
        started = dt.date.fromisoformat(metadata["Started"])
    except ValueError as error:
        raise IngestError("Started는 유효한 YYYY-MM-DD 형식이어야 합니다.") from error
    if started.isoformat() != target_match.group("date"):
        raise IngestError("Started와 target_path의 최초 생성 날짜가 다릅니다.")
    checkpoint = metadata["Checkpoint recorded at"]
    if normalize_timestamp(checkpoint) != checkpoint:
        raise IngestError("Checkpoint recorded at이 정규화된 UTC 형식이 아닙니다.")
    checkpoint_fields = parse_fields(
        sections["## 2. Reading Checkpoint"], "Reading Checkpoint"
    )
    resume_point = checkpoint_fields.get("Resume Point", "").strip()
    if not resume_point or resume_point in {"없음", "아직 기록되지 않음"}:
        raise IngestError("Reading Checkpoint의 Resume Point가 필요합니다.")
    validate_bridges(sections["## 3. Prerequisite Bridge"], root)


def validate_payload(payload: dict, root: Path) -> tuple[str, str, str, str]:
    title = str(payload.get("title") or "")
    title_match = TITLE_RE.fullmatch(title)
    if not title_match:
        raise IngestError("Issue 제목은 '[paper-note] paper-slug' 형식이어야 합니다.")
    issue_author = str(payload.get("author") or "")
    repo_owner = str(payload.get("repository_owner") or "")
    if not issue_author or issue_author.casefold() != repo_owner.casefold():
        raise IngestError("Repository owner가 만든 Issue만 처리할 수 있습니다.")
    checkpoint_recorded_at = normalize_timestamp(payload.get("issue_created_at"))
    metadata, markdown = parse_envelope(assemble(payload))
    operation = metadata["operation"]
    intent = metadata["intent"]
    target_path = metadata["target_path"]
    expected_sha = metadata["expected_sha"].lower()
    if intent != "paper-reading-checkpoint":
        raise IngestError(
            "intent는 paper-reading-checkpoint여야 합니다.", "invalid-intent"
        )
    target_match = validate_target(target_path)
    if title_match.group("slug") != target_match.group("slug"):
        raise IngestError("Issue 제목과 target_path의 slug가 다릅니다.")
    target = root / target_path
    if operation == "create":
        if expected_sha != "new":
            raise IngestError("새 파일은 expected_sha: new를 사용해야 합니다.")
        if target.exists():
            raise IngestError("같은 경로의 파일이 이미 있습니다. update 절차를 사용하세요.")
    elif operation == "update":
        if not SHA_RE.fullmatch(expected_sha):
            raise IngestError("기존 파일 수정에는 읽어서 확인한 40자리 expected_sha가 필요합니다.")
        if not target.exists():
            raise IngestError("수정 대상 파일이 없습니다. 경로를 다시 확인하세요.")
        actual_sha = git_blob_sha(target.read_bytes())
        if actual_sha != expected_sha:
            raise IngestError(
                f"파일이 읽은 뒤 변경되었습니다. expected {expected_sha}, actual {actual_sha}"
            )
    else:
        raise IngestError("operation은 create 또는 update만 허용합니다.")
    markdown = set_checkpoint_recorded_at(markdown, checkpoint_recorded_at)
    validate_markdown(markdown, target_match, root)
    return target_path, operation, checkpoint_recorded_at, markdown


def ingest(payload: dict, root: Path) -> tuple[str, str, str]:
    target_path, operation, checkpoint_recorded_at, markdown = validate_payload(
        payload, root
    )
    target = root / target_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(markdown, encoding="utf-8")
    return target_path, operation, checkpoint_recorded_at


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
        "❌ Paper Note 처리 실패\n\n"
        f"- Error code: `{code}`\n"
        f"- 원인: {sanitize_error_message(message)}\n"
        "- 파일 저장: 수행되지 않음\n"
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
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()
    try:
        payload = json.loads(Path(args.payload).read_text(encoding="utf-8"))
        root = Path(args.root)
        if args.validate_only:
            target_path, operation, checkpoint_recorded_at, _ = validate_payload(
                payload, root
            )
            print(
                "Paper Note preflight 완료: "
                f"{operation} {target_path} at {checkpoint_recorded_at}"
            )
            return 0
        target_path, operation, checkpoint_recorded_at = ingest(payload, root)
        report = (
            f"{RESULT_MARKER}\n"
            "✅ Paper Note 처리 완료\n\n"
            f"- Operation: `{operation}`\n"
            "- Intent: `paper-reading-checkpoint`\n"
            f"- Path: `{target_path}`\n"
            f"- Checkpoint recorded at: `{checkpoint_recorded_at}`\n"
        )
        write_report(args.report, report)
        if args.github_output:
            with open(args.github_output, "a", encoding="utf-8") as output:
                output.write(f"target_path={target_path}\n")
                output.write(f"operation={operation}\n")
                output.write(f"checkpoint_recorded_at={checkpoint_recorded_at}\n")
        print(report)
        return 0
    except (OSError, json.JSONDecodeError, IngestError) as exc:
        if isinstance(exc, IngestError):
            error_code = exc.code
        elif isinstance(exc, json.JSONDecodeError):
            error_code = "invalid-json"
        else:
            error_code = "io-error"
        try:
            write_report(args.report, failure_report(error_code, str(exc)))
        except OSError as report_error:
            print(f"Paper Note 실패 report 작성 실패: {report_error}", file=sys.stderr)
        print(f"Paper Note ingest 실패: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
