#!/usr/bin/env python3
"""Convert one approved GitHub Issue into one Learning Log Markdown file."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


TARGET_RE = re.compile(
    r"^learning-logs/(?P<year>\d{4})/(?P<month>\d{2})/"
    r"(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>[a-z0-9]+(?:-[a-z0-9]+)*)\.md$"
)
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
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


class IngestError(RuntimeError):
    pass


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
            raise IngestError(f"잘못된 메타데이터 행: {line}")
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()

    required = {"operation", "target_path", "expected_sha"}
    missing = sorted(required - metadata.keys())
    if missing:
        raise IngestError("필수 메타데이터 누락: " + ", ".join(missing))

    markdown = assembled[match.end() :].strip() + "\n"
    return metadata, markdown


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
    return match


def validate_markdown(markdown: str) -> None:
    if len(markdown) < 300:
        raise IngestError("학습 기록이 지나치게 짧습니다. 전체 Learning Log를 보내야 합니다.")
    if not markdown.startswith("# 학습 기록:"):
        raise IngestError("문서는 '# 학습 기록:' 제목으로 시작해야 합니다.")
    missing = [heading for heading in REQUIRED_HEADINGS if heading not in markdown]
    if missing:
        raise IngestError("Learning Log 필수 section 누락: " + ", ".join(missing))


def ingest(payload: dict, root: Path) -> tuple[str, str]:
    title = str(payload.get("title") or "")
    issue_author = str(payload.get("author") or "")
    repo_owner = str(payload.get("repository_owner") or "")
    if not title.casefold().startswith("[learning-log]"):
        raise IngestError("Issue 제목이 [learning-log]로 시작하지 않습니다.")
    if not issue_author or issue_author.casefold() != repo_owner.casefold():
        raise IngestError("Repository owner가 만든 Issue만 처리할 수 있습니다.")

    metadata, markdown = parse_envelope(assemble(payload))
    operation = metadata["operation"]
    target_path = metadata["target_path"]
    expected_sha = metadata["expected_sha"].lower()
    validate_target(target_path)
    validate_markdown(markdown)

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

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(markdown, encoding="utf-8")
    return target_path, operation


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload", required=True)
    parser.add_argument("--root", default=".")
    parser.add_argument("--report")
    parser.add_argument("--github-output")
    args = parser.parse_args()

    try:
        payload = json.loads(Path(args.payload).read_text(encoding="utf-8"))
        target_path, operation = ingest(payload, Path(args.root))
        report = (
            f"{RESULT_MARKER}\n"
            f"✅ Learning Log 처리 완료\n\n"
            f"- Operation: `{operation}`\n"
            f"- Path: `{target_path}`\n"
        )
        if args.report:
            Path(args.report).write_text(report, encoding="utf-8")
        if args.github_output:
            with open(args.github_output, "a", encoding="utf-8") as output:
                output.write(f"target_path={target_path}\n")
                output.write(f"operation={operation}\n")
        print(report)
        return 0
    except (OSError, json.JSONDecodeError, IngestError) as exc:
        print(f"Learning Log ingest 실패: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
