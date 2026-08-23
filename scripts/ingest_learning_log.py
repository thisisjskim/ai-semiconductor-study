#!/usr/bin/env python3
"""Convert one approved GitHub Issue into one Learning Log Markdown file."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

from learning_log_metadata import load_domain_policy


TARGET_RE = re.compile(
    r"^learning-logs/(?P<year>\d{4})/(?P<month>\d{2})/"
    r"(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)\.md$"
)
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
TITLE_RE = re.compile(
    r"^\[learning-log\] (?P<date>\d{4}-\d{2}-\d{2}) "
    r"(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)$"
)
ENVELOPE_RE = re.compile(
    r"\A<!--\s*research-os-ingest:v1\s*\n(?P<meta>.*?)\n-->\s*\n?",
    re.DOTALL,
)
RESULT_MARKER = "<!-- research-os-result -->"
COMMANDS = {"/기록", "/retry", "/ingest"}
REQUIRED_HEADINGS = (
    "## Metadata",
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
HEADING_ALIASES = {
    "## 1. 오늘 공부한 목표": "## 1. 오늘 공부한 목적",
}
FENCE_RE = re.compile(r"^ {0,3}(?P<fence>`{3,}|~{3,})")
MAX_ERROR_MESSAGE_LENGTH = 300
ENVELOPE_KEYS = {"operation", "target_path", "expected_sha"}
METADATA_RE = re.compile(r"^- (?P<key>[^:]+):\s*(?P<value>.*)$")
RECORDED_AT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class IngestError(RuntimeError):
    def __init__(self, message: str, code: str = "ingest-validation-error") -> None:
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
        raise IngestError("Issue 본문 첫 부분에 research-os-ingest:v1 메타데이터가 없습니다.")

    metadata: dict[str, str] = {}
    for raw_line in match.group("meta").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            raise IngestError("잘못된 메타데이터 행이 있습니다.", "invalid-metadata")
        key, value = line.split(":", 1)
        key = key.strip()
        if key in metadata:
            raise IngestError(f"중복 메타데이터 필드: {key}", "invalid-metadata")
        metadata[key] = value.strip()

    missing = sorted(ENVELOPE_KEYS - metadata.keys())
    if missing:
        raise IngestError("필수 메타데이터 누락: " + ", ".join(missing))
    unknown = sorted(metadata.keys() - ENVELOPE_KEYS)
    if unknown:
        raise IngestError(
            "허용되지 않은 메타데이터 필드: " + ", ".join(unknown),
            "invalid-metadata",
        )

    markdown = assembled[match.end() :].strip() + "\n"
    return metadata, markdown


def markdown_heading_lines(markdown: str) -> list[str]:
    """Return independent Markdown heading lines outside fenced code blocks."""
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
            headings.append(line)

    return headings


def markdown_metadata(markdown: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    in_metadata = False
    for line in markdown.splitlines():
        if line == "## Metadata":
            in_metadata = True
            continue
        if in_metadata and line.startswith("## "):
            break
        if not in_metadata:
            continue
        match = METADATA_RE.fullmatch(line.strip())
        if match:
            key = match.group("key").strip()
            if key in metadata:
                raise IngestError(
                    f"Learning Log Metadata에 중복 필드가 있습니다: {key}",
                    "invalid-document-metadata",
                )
            metadata[key] = match.group("value").strip()
    return metadata


def normalize_recorded_at(value: object) -> str:
    raw = str(value or "").strip()
    if not RECORDED_AT_RE.fullmatch(raw):
        raise IngestError(
            "Issue created_at은 YYYY-MM-DDTHH:MM:SSZ 형식이어야 합니다.",
            "invalid-recorded-at",
        )
    try:
        parsed = dt.datetime.fromisoformat(raw.removesuffix("Z") + "+00:00")
    except ValueError as error:
        raise IngestError(
            "Issue created_at에 유효하지 않은 시각이 있습니다.",
            "invalid-recorded-at",
        ) from error
    return parsed.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def set_recorded_at(markdown: str, recorded_at: str) -> str:
    """Insert the workflow-owned timestamp directly after Date metadata."""
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
    recorded_lines = []
    date_index = None
    for index in range(metadata_start + 1, metadata_end):
        match = METADATA_RE.fullmatch(lines[index].strip())
        if not match:
            continue
        key = match.group("key").strip()
        if key == "Recorded at":
            recorded_lines.append(index)
        elif key == "Date":
            date_index = index

    for index in reversed(recorded_lines):
        del lines[index]
        metadata_end -= 1
        if date_index is not None and index < date_index:
            date_index -= 1
    insert_at = (date_index + 1) if date_index is not None else metadata_start + 1
    lines.insert(insert_at, f"- Recorded at: {recorded_at}")
    return "\n".join(lines).rstrip() + "\n"


def normalize_headings(markdown: str) -> str:
    """Normalize only explicitly allowed independent heading aliases."""
    headings = markdown_heading_lines(markdown)
    for alias, canonical in HEADING_ALIASES.items():
        if alias in headings and canonical in headings:
            raise IngestError(
                f"canonical section과 alias가 동시에 있습니다: `{canonical}`",
                "duplicate-required-heading",
            )

    lines = markdown.splitlines(keepends=True)
    fence_char = ""
    fence_length = 0
    normalized: list[str] = []
    for line in lines:
        content = line.rstrip("\r\n")
        ending = line[len(content) :]
        fence_match = FENCE_RE.match(content)
        if fence_match:
            fence = fence_match.group("fence")
            if not fence_char:
                fence_char = fence[0]
                fence_length = len(fence)
            elif fence[0] == fence_char and len(fence) >= fence_length:
                fence_char = ""
                fence_length = 0
            normalized.append(line)
            continue
        if not fence_char and content in HEADING_ALIASES:
            content = HEADING_ALIASES[content]
        normalized.append(content + ending)

    return "".join(normalized)


def validate_target(target_path: str) -> re.Match[str]:
    match = TARGET_RE.fullmatch(target_path)
    if not match:
        raise IngestError(
            "target_path는 learning-logs/YYYY/MM/YYYY-MM-DD-topic-slug.md 형식이어야 합니다."
        )
    if match.group("date")[:4] != match.group("year"):
        raise IngestError("파일 날짜의 연도와 상위 directory 연도가 다릅니다.")
    if match.group("date")[5:7] != match.group("month"):
        raise IngestError("파일 날짜의 월과 상위 directory 월이 다릅니다.")
    try:
        dt.date.fromisoformat(match.group("date"))
    except ValueError as error:
        raise IngestError("target_path에 유효하지 않은 날짜가 있습니다.") from error
    return match


def validate_markdown(markdown: str, root: Path) -> None:
    if len(markdown) < 300:
        raise IngestError("학습 기록이 지나치게 짧습니다. 전체 Learning Log를 보내야 합니다.")
    if not markdown.startswith("# 학습 기록:"):
        raise IngestError("문서는 '# 학습 기록:' 제목으로 시작해야 합니다.")
    headings = markdown_heading_lines(markdown)
    missing = [heading for heading in REQUIRED_HEADINGS if heading not in headings]
    if missing:
        raise IngestError(
            "필수 section이 없습니다: " + ", ".join(f"`{item}`" for item in missing),
            "missing-required-heading",
        )
    metadata = markdown_metadata(markdown)
    recorded_at = metadata.get("Recorded at", "")
    if not recorded_at or normalize_recorded_at(recorded_at) != recorded_at:
        raise IngestError(
            "Learning Log Metadata에 workflow가 생성한 유효한 Recorded at이 필요합니다.",
            "invalid-recorded-at",
        )
    domain = metadata.get("Domain", "")
    if not domain:
        raise IngestError(
            "Learning Log Metadata에 Domain이 필요합니다.",
            "invalid-domain",
        )
    try:
        domain_policy = load_domain_policy(root)
    except ValueError as error:
        raise IngestError(str(error), "invalid-metadata-schema") from error
    if domain not in domain_policy.allowed_domains:
        allowed = ", ".join(sorted(domain_policy.allowed_domains))
        raise IngestError(
            f"지원되지 않는 Domain metadata입니다: {domain}. 허용값: {allowed}",
            "invalid-domain",
        )


def validate_payload(payload: dict, root: Path) -> tuple[str, str, str]:
    """Validate an Issue payload without writing the Learning Log."""
    title = str(payload.get("title") or "")
    issue_author = str(payload.get("author") or "")
    repo_owner = str(payload.get("repository_owner") or "")
    title_match = TITLE_RE.fullmatch(title)
    if not title_match:
        raise IngestError(
            "Issue 제목은 '[learning-log] YYYY-MM-DD topic-slug' 형식이어야 합니다."
        )
    if not issue_author or issue_author.casefold() != repo_owner.casefold():
        raise IngestError("Repository owner가 만든 Issue만 처리할 수 있습니다.")
    issue_created_at = normalize_recorded_at(payload.get("issue_created_at"))

    metadata, markdown = parse_envelope(assemble(payload))
    markdown = normalize_headings(markdown)
    operation = metadata["operation"]
    target_path = metadata["target_path"]
    expected_sha = metadata["expected_sha"].lower()
    target_match = validate_target(target_path)
    if title_match.group("date") != target_match.group("date"):
        raise IngestError("Issue 제목과 target_path의 날짜가 다릅니다.")
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

    recorded_at = issue_created_at
    if operation == "update":
        existing_metadata = markdown_metadata(target.read_text(encoding="utf-8"))
        recorded_at = existing_metadata.get("Recorded at", "")
        if not recorded_at:
            raise IngestError(
                "기존 Learning Log에 Recorded at이 없습니다. 검증된 과거 시각을 먼저 보완해야 합니다.",
                "missing-recorded-at",
            )
        recorded_at = normalize_recorded_at(recorded_at)
    markdown = set_recorded_at(markdown, recorded_at)
    validate_markdown(markdown, root)

    return target_path, operation, markdown


def ingest(payload: dict, root: Path) -> tuple[str, str]:
    target_path, operation, markdown = validate_payload(payload, root)

    target = root / target_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(markdown, encoding="utf-8")
    return target_path, operation


def sanitize_error_message(message: str) -> str:
    """Limit untrusted error text before it is exposed in an Issue comment."""
    cleaned = " ".join(
        re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", message).splitlines()
    ).strip()
    if len(cleaned) > MAX_ERROR_MESSAGE_LENGTH:
        return cleaned[: MAX_ERROR_MESSAGE_LENGTH - 1] + "…"
    return cleaned or "알 수 없는 오류가 발생했습니다."


def failure_report(code: str, message: str) -> str:
    return (
        f"{RESULT_MARKER}\n"
        "❌ Learning Log 처리 실패\n\n"
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
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="계약을 검증하되 파일은 쓰지 않습니다.",
    )
    args = parser.parse_args()

    try:
        payload = json.loads(Path(args.payload).read_text(encoding="utf-8"))
        if args.validate_only:
            target_path, operation, _ = validate_payload(payload, Path(args.root))
            action = "검증 완료"
        else:
            target_path, operation = ingest(payload, Path(args.root))
            action = "처리 완료"
        report = (
            f"{RESULT_MARKER}\n"
            f"✅ Learning Log {action}\n\n"
            f"- Operation: `{operation}`\n"
            f"- Path: `{target_path}`\n"
        )
        write_report(args.report, report)
        if args.github_output:
            with open(args.github_output, "a", encoding="utf-8") as output:
                output.write(f"target_path={target_path}\n")
                output.write(f"operation={operation}\n")
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
            print(f"Learning Log 실패 report 작성 실패: {report_error}", file=sys.stderr)
        print(f"Learning Log ingest 실패: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
