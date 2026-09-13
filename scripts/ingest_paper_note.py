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
    r"\A<!--\s*research-os-paper-note:(?P<version>v1|v2)\s*\n(?P<meta>.*?)\n-->\s*\n?",
    re.DOTALL,
)
RESULT_MARKER = "<!-- research-os-result -->"
COMMANDS = {"/기록", "/retry", "/ingest"}
PAPER_TYPES = {"foundational", "ssl-lab", "related"}
BRIDGE_STATUSES = {"studying", "paused", "sufficient-for-paper"}
ENVELOPE_FIELDS = {"operation", "intent", "target_path", "expected_sha"}
REQUIRED_METADATA = (
    "Title",
    "Document type",
    "Paper type",
    "Venue / Year",
    "Authors",
    "Paper link",
    "Started",
    "Checkpoint recorded at",
    "Related notes",
)
REQUIRED_HEADINGS = (
    "## Metadata",
    "## 1. Reading Checkpoint",
    "## 2. Prerequisite Bridge",
    "## 3. Problem",
    "## 4. Key Idea",
    "## 5. Architecture",
    "## 6. Method",
    "## 7. Experiments",
    "## 8. Results",
    "## 9. Trade-offs",
    "## 10. Limitations",
    "## 11. Questions",
    "## 12. Connection to My Research Direction",
    "## 13. Final Summary",
    "## 14. Reading Session History",
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


def parse_envelope(assembled: str) -> tuple[str, dict[str, str], str]:
    match = ENVELOPE_RE.match(assembled)
    if not match:
        raise IngestError(
            "Issue 본문 첫 부분에 research-os-paper-note:v1 또는 v2 메타데이터가 없습니다."
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
    return match.group("version"), metadata, markdown


def section_bounds(markdown: str, heading: str) -> tuple[int, int]:
    """Return the byte offsets for one exact level-two section body."""
    heading_match = re.search(rf"(?m)^{re.escape(heading)}\s*$", markdown)
    if not heading_match:
        raise IngestError(f"필수 section이 없습니다: `{heading}`")
    body_start = heading_match.end()
    next_heading = re.search(r"(?m)^##\s+", markdown[body_start:])
    body_end = body_start + next_heading.start() if next_heading else len(markdown)
    return body_start, body_end


def replace_resume_point(markdown: str, resume_point: str) -> str:
    start, end = section_bounds(markdown, "## 1. Reading Checkpoint")
    body = markdown[start:end]
    replacement = f"- Resume Point: {resume_point}"
    updated, count = re.subn(
        r"(?m)^- Resume Point:.*$", lambda _: replacement, body, count=1
    )
    if count != 1:
        raise IngestError(
            "Reading Checkpoint에는 정확히 하나의 Resume Point가 필요합니다.",
            "invalid-resume-point-structure",
        )
    return markdown[:start] + updated + markdown[end:]


def append_to_section(markdown: str, heading: str, addition: str) -> str:
    start, end = section_bounds(markdown, heading)
    body = markdown[start:end].rstrip()
    separator = "\n\n" if body.strip() else "\n"
    updated = body + separator + addition.strip() + "\n\n"
    return markdown[:start] + updated + markdown[end:].lstrip("\n")


def validate_delta_text(value: object, label: str, *, max_length: int = 4000) -> str:
    text = str(value or "").strip()
    if not text:
        raise IngestError(f"v2 delta의 {label} 값이 비어 있습니다.", "invalid-delta")
    if len(text) > max_length:
        raise IngestError(f"v2 delta의 {label} 값이 지나치게 깁니다.", "invalid-delta")
    if "\n## " in f"\n{text}" or "\r" in text:
        raise IngestError(
            f"v2 delta의 {label}에는 level-two heading 또는 CR 문자를 넣을 수 없습니다.",
            "invalid-delta",
        )
    return text


def parse_checkpoint_delta(raw: str) -> dict:
    try:
        delta = json.loads(raw)
    except json.JSONDecodeError as error:
        raise IngestError(
            "v2 본문은 유효한 JSON object여야 합니다.", "invalid-delta-json"
        ) from error
    if not isinstance(delta, dict):
        raise IngestError("v2 본문은 JSON object여야 합니다.", "invalid-delta")
    allowed = {
        "resume_point",
        "reading_session_history",
        "user_analysis_evidence",
        "prerequisite_bridge",
        "user_identified_limitations_upsert",
        "questions_upsert",
        "research_connections_upsert",
    }
    extra = sorted(set(delta) - allowed)
    if extra:
        raise IngestError(
            "v2 delta에 허용되지 않는 필드: " + ", ".join(extra), "invalid-delta"
        )
    if "resume_point" not in delta or "reading_session_history" not in delta:
        raise IngestError(
            "v2 delta에는 resume_point와 reading_session_history가 필요합니다.",
            "invalid-delta",
        )
    return delta


def validate_concept_name(value: object) -> str:
    concept = validate_delta_text(value, "concept", max_length=120)
    if "\n" in concept or concept.startswith("#"):
        raise IngestError("PB concept는 단일 행의 일반 텍스트여야 합니다.", "invalid-delta")
    return concept


def validate_record_title(value: object, label: str = "title") -> str:
    title = validate_delta_text(value, label, max_length=160)
    if "\n" in title or title.startswith("#"):
        raise IngestError(f"{label}은 단일 행의 일반 텍스트여야 합니다.", "invalid-delta")
    return title


def one_line(value: object, label: str, *, max_length: int = 4000) -> str:
    text = validate_delta_text(value, label, max_length=max_length)
    if "\n" in text:
        raise IngestError(f"{label}은 단일 행이어야 합니다.", "invalid-delta")
    return text


def upsert_subsection_record(
    markdown: str,
    parent_heading: str,
    subsection_heading: str,
    record_title: str,
    block: str,
) -> str:
    parent_start, parent_end = section_bounds(markdown, parent_heading)
    parent = markdown[parent_start:parent_end]
    subsection_match = re.search(
        rf"(?m)^{re.escape(subsection_heading)}\s*$", parent
    )
    if not subsection_match:
        raise IngestError(f"필수 subsection이 없습니다: `{subsection_heading}`")
    body_start = subsection_match.end()
    next_subsection = re.search(r"(?m)^###\s+", parent[body_start:])
    body_end = body_start + next_subsection.start() if next_subsection else len(parent)
    body = parent[body_start:body_end]
    record_matches = list(re.finditer(r"(?m)^####\s+(.+?)\s*$", body))
    target_index = next(
        (
            index
            for index, match in enumerate(record_matches)
            if match.group(1).strip() == record_title
        ),
        None,
    )
    rendered = f"#### {record_title}\n\n{block.strip()}"
    if target_index is None:
        cleaned = re.sub(
            r"(?m)^\s*(?:- 없음|선정된 질문 없음)\s*$", "", body
        ).strip()
        updated_body = (cleaned + "\n\n" if cleaned else "\n") + rendered + "\n\n"
    else:
        item_start = record_matches[target_index].start()
        item_end = (
            record_matches[target_index + 1].start()
            if target_index + 1 < len(record_matches)
            else len(body)
        )
        updated_body = body[:item_start] + rendered + "\n\n" + body[item_end:].lstrip("\n")
    updated_parent = parent[:body_start] + updated_body + parent[body_end:]
    return markdown[:parent_start] + updated_parent + markdown[parent_end:]


def upsert_section_record(
    markdown: str, parent_heading: str, record_title: str, block: str
) -> str:
    parent_start, parent_end = section_bounds(markdown, parent_heading)
    body = markdown[parent_start:parent_end]
    record_matches = list(re.finditer(r"(?m)^###\s+(.+?)\s*$", body))
    target_index = next(
        (
            index
            for index, match in enumerate(record_matches)
            if match.group(1).strip() == record_title
        ),
        None,
    )
    rendered = f"### {record_title}\n\n{block.strip()}"
    if target_index is None:
        cleaned = re.sub(
            r"(?m)^\s*(?:- 없음|확인된 연구 연결 없음)\s*$", "", body
        ).strip()
        updated = (cleaned + "\n\n" if cleaned else "\n") + rendered + "\n\n"
    else:
        item_start = record_matches[target_index].start()
        item_end = (
            record_matches[target_index + 1].start()
            if target_index + 1 < len(record_matches)
            else len(body)
        )
        updated = body[:item_start] + rendered + "\n\n" + body[item_end:].lstrip("\n")
    return markdown[:parent_start] + updated + markdown[parent_end:]


def upsert_bridge_concept(
    markdown: str, subsection_heading: str, concept: str, block: str
) -> str:
    section_start, section_end = section_bounds(markdown, "## 2. Prerequisite Bridge")
    section = markdown[section_start:section_end]
    subsection_match = re.search(
        rf"(?m)^{re.escape(subsection_heading)}\s*$", section
    )
    if not subsection_match:
        raise IngestError(f"Prerequisite Bridge subsection 누락: {subsection_heading}")
    body_start = subsection_match.end()
    next_subsection = re.search(r"(?m)^###\s+", section[body_start:])
    body_end = body_start + next_subsection.start() if next_subsection else len(section)
    body = section[body_start:body_end]
    concept_matches = list(re.finditer(r"(?m)^####\s+(.+?)\s*$", body))
    target_index = next(
        (
            index
            for index, match in enumerate(concept_matches)
            if match.group(1).strip() == concept
        ),
        None,
    )
    rendered = f"#### {concept}\n\n{block.strip()}"
    if target_index is None:
        cleaned = re.sub(r"(?m)^\s*- 없음\s*$", "", body).strip()
        updated_body = (cleaned + "\n\n" if cleaned else "\n") + rendered + "\n\n"
    else:
        item_start = concept_matches[target_index].start()
        item_end = (
            concept_matches[target_index + 1].start()
            if target_index + 1 < len(concept_matches)
            else len(body)
        )
        updated_body = body[:item_start] + rendered + "\n\n" + body[item_end:].lstrip("\n")
    updated_section = section[:body_start] + updated_body + section[body_end:]
    return markdown[:section_start] + updated_section + markdown[section_end:]


def apply_bridge_delta(markdown: str, value: object) -> str:
    if not isinstance(value, dict):
        raise IngestError("prerequisite_bridge는 JSON object여야 합니다.", "invalid-delta")
    allowed = {"resolved_upsert", "tracked_upsert"}
    extra = sorted(set(value) - allowed)
    if extra:
        raise IngestError("prerequisite_bridge에 허용되지 않는 필드: " + ", ".join(extra), "invalid-delta")
    for key in allowed:
        records = value.get(key, [])
        if not isinstance(records, list):
            raise IngestError(f"prerequisite_bridge.{key}는 JSON array여야 합니다.", "invalid-delta")
        if len(records) > 20:
            raise IngestError(f"prerequisite_bridge.{key}는 20개를 넘을 수 없습니다.", "invalid-delta")
    for record in value.get("resolved_upsert", []):
        if not isinstance(record, dict):
            raise IngestError("resolved_upsert 항목은 JSON object여야 합니다.", "invalid-delta")
        required = {"concept", "location", "reason", "definition", "user_understanding"}
        if set(record) != required:
            raise IngestError("resolved_upsert 필드를 확인하세요.", "invalid-delta")
        concept = validate_concept_name(record["concept"])
        fields = (
            ("등장 위치", "location"),
            ("논문에서 필요한 이유", "reason"),
            ("실제 정의", "definition"),
            ("사용자의 이해", "user_understanding"),
        )
        lines = []
        for label, key in fields:
            text = validate_delta_text(record[key], key)
            if "\n" in text:
                raise IngestError(f"{key}는 단일 행이어야 합니다.", "invalid-delta")
            lines.append(f"- {label}: {text}")
        markdown = upsert_bridge_concept(
            markdown, "### 논문 안에서 해결한 선수지식", concept, "\n".join(lines)
        )
    for record in value.get("tracked_upsert", []):
        if not isinstance(record, dict):
            raise IngestError("tracked_upsert 항목은 JSON object여야 합니다.", "invalid-delta")
        required = {"concept", "status", "reason", "sufficient_criterion", "learning_logs"}
        if set(record) != required:
            raise IngestError("tracked_upsert 필드를 확인하세요.", "invalid-delta")
        concept = validate_concept_name(record["concept"])
        status = validate_delta_text(record["status"], "status", max_length=30)
        reason = validate_delta_text(record["reason"], "reason")
        criterion = validate_delta_text(record["sufficient_criterion"], "sufficient_criterion")
        logs = record["learning_logs"]
        if status not in BRIDGE_STATUSES or not isinstance(logs, list):
            raise IngestError("tracked_upsert의 status 또는 learning_logs를 확인하세요.", "invalid-delta")
        if any("\n" in item for item in (reason, criterion)):
            raise IngestError("tracked_upsert 설명은 단일 행이어야 합니다.", "invalid-delta")
        log_lines = []
        for log in logs:
            path = validate_delta_text(log, "learning_log", max_length=200)
            if not LEARNING_LOG_PATH_RE.fullmatch(path):
                raise IngestError(f"잘못된 Learning Log 경로: {path}", "invalid-delta")
            log_lines.append(f"  - `{path}`")
        if not log_lines:
            log_lines.append("  - 없음")
        block = "\n".join(
            [
                f"- Status: {status}",
                f"- 논문에서 필요한 이유: {reason}",
                f"- 이 논문에 충분한 기준: {criterion}",
                "- Learning Logs:",
                *log_lines,
            ]
        )
        markdown = upsert_bridge_concept(
            markdown, "### 별도로 이어가는 선수지식", concept, block
        )
    return markdown


def require_record(record: object, required: set[str], label: str) -> dict:
    if not isinstance(record, dict) or set(record) != required:
        raise IngestError(f"{label} 필드를 확인하세요.", "invalid-delta")
    return record


def apply_user_limitations(markdown: str, records: object) -> str:
    if not isinstance(records, list) or len(records) > 20:
        raise IngestError("user_identified_limitations_upsert는 최대 20개의 JSON array여야 합니다.", "invalid-delta")
    required = {
        "title",
        "limitation",
        "related_architecture_method",
        "user_basis",
        "paper_direct",
        "needs_confirmation",
    }
    fields = (
        ("사용자가 지적한 limitation", "limitation"),
        ("Related Architecture / Method", "related_architecture_method"),
        ("사용자가 근거로 사용한 paper content", "user_basis"),
        ("Paper에서 직접 확인된 내용", "paper_direct"),
        ("추가 확인이 필요한 부분", "needs_confirmation"),
    )
    for item in records:
        record = require_record(item, required, "user limitation")
        title = validate_record_title(record["title"])
        block = "\n".join(
            f"- {label}: {one_line(record[key], key)}" for label, key in fields
        )
        markdown = upsert_subsection_record(
            markdown,
            "## 10. Limitations",
            "### User-Identified Limitations",
            title,
            block,
        )
    return markdown


QUESTION_CATEGORIES = {
    "understanding": "### 이해를 위한 질문",
    "critical": "### 비판적 질문",
    "follow-up-research": "### 후속 연구 질문",
}


def apply_questions(markdown: str, records: object) -> str:
    if not isinstance(records, list) or len(records) > 30:
        raise IngestError("questions_upsert는 최대 30개의 JSON array여야 합니다.", "invalid-delta")
    required = {
        "category",
        "title",
        "user_question",
        "context",
        "selection_reason",
        "resolution_process",
        "learned",
        "resolution_status",
        "unresolved",
        "evidence",
    }
    evidence_required = {"paper_direct", "gpt_supplementary", "user_interpretation"}
    for item in records:
        record = require_record(item, required, "question")
        category = one_line(record["category"], "category", max_length=30)
        if category not in QUESTION_CATEGORIES:
            raise IngestError("question category를 확인하세요.", "invalid-delta")
        status = one_line(record["resolution_status"], "resolution_status", max_length=30)
        if status not in {"resolved", "partially-resolved", "unresolved"}:
            raise IngestError("question resolution_status를 확인하세요.", "invalid-delta")
        evidence = require_record(record["evidence"], evidence_required, "question evidence")
        block = "\n".join(
            [
                f"- 사용자의 질문: {one_line(record['user_question'], 'user_question')}",
                f"- 질문이 발생한 위치 또는 맥락: {one_line(record['context'], 'context')}",
                f"- 선정 이유: {one_line(record['selection_reason'], 'selection_reason')}",
                f"- 해결 과정: {one_line(record['resolution_process'], 'resolution_process')}",
                f"- 해결하며 알게 된 내용: {one_line(record['learned'], 'learned')}",
                f"- 해결 상태: {status}",
                f"- 해결하지 못한 부분: {one_line(record['unresolved'], 'unresolved')}",
                "- 해결에 사용한 근거:",
                f"  - Paper direct evidence: {one_line(evidence['paper_direct'], 'paper_direct')}",
                f"  - GPT supplementary explanation: {one_line(evidence['gpt_supplementary'], 'gpt_supplementary')}",
                f"  - User interpretation / hypothesis: {one_line(evidence['user_interpretation'], 'user_interpretation')}",
            ]
        )
        markdown = upsert_subsection_record(
            markdown,
            "## 11. Questions",
            QUESTION_CATEGORIES[category],
            validate_record_title(record["title"]),
            block,
        )
    return markdown


def apply_research_connections(markdown: str, records: object) -> str:
    if not isinstance(records, list) or len(records) > 20:
        raise IngestError("research_connections_upsert는 최대 20개의 JSON array여야 합니다.", "invalid-delta")
    required = {
        "title",
        "user_interest",
        "paper_element",
        "evidence_location",
        "connection",
        "role",
        "questions_limitations_relation",
        "boundary",
        "future_use",
    }
    fields = (
        ("사용자가 표현한 research interest 또는 goal", "user_interest"),
        ("연결되는 Paper element", "paper_element"),
        ("연결 근거 위치", "evidence_location"),
        ("연결 방식", "connection"),
        ("이 논문이 내 연구 방향에서 수행하는 역할", "role"),
        ("기존 Questions / Limitations와의 관계", "questions_limitations_relation"),
        ("연결의 경계 또는 아직 확인되지 않은 부분", "boundary"),
        ("향후 활용", "future_use"),
    )
    for item in records:
        record = require_record(item, required, "research connection")
        block = "\n".join(
            f"- {label}: {one_line(record[key], key)}" for label, key in fields
        )
        markdown = upsert_section_record(
            markdown,
            "## 12. Connection to My Research Direction",
            validate_record_title(record["title"]),
            block,
        )
    return markdown


def render_session_history(value: object) -> str:
    if not isinstance(value, dict):
        raise IngestError(
            "reading_session_history는 JSON object여야 합니다.", "invalid-delta"
        )
    required = {
        "date",
        "read_range",
        "understood",
        "questions",
        "bridge_changes",
        "ending_resume_point",
    }
    missing = sorted(required - set(value))
    extra = sorted(set(value) - required)
    if missing or extra:
        details = []
        if missing:
            details.append("누락: " + ", ".join(missing))
        if extra:
            details.append("허용되지 않음: " + ", ".join(extra))
        raise IngestError(
            "reading_session_history 필드를 확인하세요 ("
            + "; ".join(details)
            + ").",
            "invalid-delta",
        )
    date = validate_delta_text(value["date"], "date", max_length=10)
    try:
        dt.date.fromisoformat(date)
    except ValueError as error:
        raise IngestError(
            "reading_session_history.date는 YYYY-MM-DD여야 합니다.", "invalid-delta"
        ) from error
    fields = (
        ("읽은 범위", "read_range"),
        ("이해한 내용", "understood"),
        ("Question Selection Gate를 통과한 질문과 해결 상태", "questions"),
        ("Bridge 변화", "bridge_changes"),
        ("종료 당시 Resume Point", "ending_resume_point"),
    )
    lines = [f"### {date}", ""]
    for label, key in fields:
        text = validate_delta_text(value[key], key)
        if "\n" in text:
            raise IngestError(f"{key}는 한 문단의 단일 행이어야 합니다.", "invalid-delta")
        lines.append(f"- {label}: {text}")
    return "\n".join(lines)


def apply_checkpoint_delta(markdown: str, raw_delta: str, recorded_at: str) -> str:
    delta = parse_checkpoint_delta(raw_delta)
    resume_point = validate_delta_text(delta["resume_point"], "resume_point")
    if "\n" in resume_point:
        raise IngestError("resume_point는 단일 행이어야 합니다.", "invalid-delta")
    markdown = replace_resume_point(markdown, resume_point)
    markdown = append_to_section(
        markdown,
        "## 14. Reading Session History",
        render_session_history(delta["reading_session_history"]),
    )
    if "prerequisite_bridge" in delta:
        markdown = apply_bridge_delta(markdown, delta["prerequisite_bridge"])
    if "user_identified_limitations_upsert" in delta:
        markdown = apply_user_limitations(
            markdown, delta["user_identified_limitations_upsert"]
        )
    if "questions_upsert" in delta:
        markdown = apply_questions(markdown, delta["questions_upsert"])
    if "research_connections_upsert" in delta:
        markdown = apply_research_connections(
            markdown, delta["research_connections_upsert"]
        )
    evidence = delta.get("user_analysis_evidence", [])
    if not isinstance(evidence, list):
        raise IngestError(
            "user_analysis_evidence는 JSON array여야 합니다.", "invalid-delta"
        )
    if len(evidence) > 20:
        raise IngestError("한 checkpoint의 사용자 분석 근거는 20개를 넘을 수 없습니다.", "invalid-delta")
    for item in evidence:
        text = validate_delta_text(item, "user_analysis_evidence", max_length=2000)
        if "\n" in text:
            raise IngestError("사용자 분석 근거 한 항목은 단일 행이어야 합니다.", "invalid-delta")
        markdown = append_to_section(markdown, "## 사용자 분석 근거", f"> {text}")
    return set_checkpoint_recorded_at(markdown, recorded_at)


def markdown_heading_lines(markdown: str) -> list[str]:
    return [
        line.strip()
        for line in markdown_lines_outside_fences(markdown)
        if line.startswith("## ")
    ]


def markdown_lines_outside_fences(markdown: str) -> list[str]:
    """Return Markdown lines that are structural, excluding fenced code content."""
    visible: list[str] = []
    fence_char = ""
    fence_length = 0
    for line in markdown.splitlines():
        if fence_char:
            candidate = line.lstrip(" ")
            indentation = len(line) - len(candidate)
            if indentation <= 3 and re.fullmatch(
                rf"{re.escape(fence_char)}{{{fence_length},}}[ \t]*", candidate
            ):
                fence_char = ""
                fence_length = 0
            continue

        fence_match = FENCE_RE.match(line)
        if fence_match:
            fence = fence_match.group("fence")
            suffix = line[fence_match.end() :]
            if fence[0] != "`" or "`" not in suffix:
                fence_char = fence[0]
                fence_length = len(fence)
                continue

        visible.append(line)
    return visible


def parse_sections(markdown: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = ""
    for line in markdown_lines_outside_fences(markdown):
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
    resolved_heading = "### 논문 안에서 해결한 선수지식"
    tracked_heading = "### 별도로 이어가는 선수지식"
    resolved_start = bridge_text.find(resolved_heading)
    tracked_start = bridge_text.find(tracked_heading)
    if resolved_start < 0:
        raise IngestError(
            "Prerequisite Bridge에 '논문 안에서 해결한 선수지식' section이 없습니다.",
            "missing-resolved-bridge-section",
        )
    if tracked_start < 0:
        raise IngestError(
            "Prerequisite Bridge에 '별도로 이어가는 선수지식' section이 없습니다.",
            "missing-tracked-bridge-section",
        )
    if resolved_start > tracked_start:
        raise IngestError(
            "Prerequisite Bridge section 순서를 확인하세요.",
            "invalid-bridge-section-order",
        )
    resolved_text = bridge_text[
        resolved_start + len(resolved_heading) : tracked_start
    ]
    resolved_concepts = list(
        re.finditer(r"(?m)^####\s+(?P<concept>.+?)\s*$", resolved_text)
    )
    required_resolved_fields = (
        "등장 위치",
        "논문에서 필요한 이유",
        "실제 정의",
        "사용자의 이해",
    )
    for index, concept_match in enumerate(resolved_concepts):
        block_end = (
            resolved_concepts[index + 1].start()
            if index + 1 < len(resolved_concepts)
            else len(resolved_text)
        )
        concept = concept_match.group("concept").strip()
        block = resolved_text[concept_match.end() : block_end]
        fields = parse_fields(block, f"논문 안에서 해결한 선수지식 '{concept}'")
        missing_fields = [
            field for field in required_resolved_fields if not fields.get(field)
        ]
        if missing_fields:
            raise IngestError(
                f"논문 안에서 해결한 선수지식 '{concept}'의 필수 필드 누락: "
                + ", ".join(missing_fields),
                "missing-resolved-bridge-field",
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
        sections["## 1. Reading Checkpoint"], "Reading Checkpoint"
    )
    resume_point = checkpoint_fields.get("Resume Point", "").strip()
    if not resume_point or resume_point in {"없음", "아직 기록되지 않음"}:
        raise IngestError("Reading Checkpoint의 Resume Point가 필요합니다.")
    validate_bridges(sections["## 2. Prerequisite Bridge"], root)


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
    version, metadata, content = parse_envelope(assemble(payload))
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
    if version == "v2" and operation != "checkpoint-update":
        raise IngestError("v2는 operation: checkpoint-update만 허용합니다.", "invalid-operation")
    if version == "v1" and operation == "checkpoint-update":
        raise IngestError("checkpoint-update는 v2 envelope를 사용해야 합니다.", "invalid-operation")
    if operation == "create":
        if expected_sha != "new":
            raise IngestError("새 파일은 expected_sha: new를 사용해야 합니다.")
        if target.exists():
            raise IngestError("같은 경로의 파일이 이미 있습니다. update 절차를 사용하세요.")
    elif operation in {"update", "checkpoint-update"}:
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
        raise IngestError("operation은 create, update 또는 checkpoint-update만 허용합니다.")
    if version == "v2":
        markdown = apply_checkpoint_delta(
            target.read_text(encoding="utf-8"), content, checkpoint_recorded_at
        )
    else:
        markdown = set_checkpoint_recorded_at(content, checkpoint_recorded_at)
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
