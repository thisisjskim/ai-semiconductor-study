#!/usr/bin/env python3
"""Contract tests for ingest_learning_log.py."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import ingest_learning_log as ingest


def assert_rejected(action, message: str) -> ingest.IngestError:
    try:
        action()
    except ingest.IngestError as error:
        return error
    raise AssertionError(message)


def assert_workflow_contract() -> None:
    workflow_path = (
        Path(__file__).resolve().parents[1]
        / ".github/workflows/learning-log-ingest.yml"
    )
    workflow = workflow_path.read_text(encoding="utf-8")
    required_steps = (
        "- name: Check out repository",
        "- name: Build ingest payload",
        "- name: Run contract tests",
        "- name: Ingest Learning Log",
        "- name: Validate ingest result",
        "- name: Commit Learning Log",
        "- name: Comment success",
        "- name: Comment failure",
    )
    positions = [workflow.index(step) for step in required_steps]
    assert positions == sorted(positions), "Workflow 단계 순서가 계약과 다릅니다."
    assert "group: learning-log-main" in workflow
    assert '[[ ! -f "$TARGET_PATH" ]]' in workflow
    assert "git status --porcelain --untracked-files=all" in workflow
    assert 'if [[ "$HAS_CHANGES" == "true" ]]' in workflow
    assert "REPORT_PATH: ${{ runner.temp }}/ingest-report.md" in workflow
    assert 'fs.readFileSync(process.env.REPORT_PATH, "utf8")' in workflow
    assert "❌ Learning Log 처리 실패" in workflow
    assert "Error code: `workflow-error`" in workflow
    assert "Actions 실행 로그" in workflow


def assert_action_schema_contract() -> None:
    schema_path = (
        Path(__file__).resolve().parents[1] / "system/ACTION_SCHEMA.yaml"
    )
    schema = schema_path.read_text(encoding="utf-8")

    lines = schema.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r"^(?P<indent>\s*)(description|summary):\s*(?P<value>.*)$", line)
        if not match:
            continue
        value = match.group("value")
        if value in {">", ">-", "|", "|-"}:
            indent = len(match.group("indent"))
            folded_lines = []
            for following in lines[index + 1 :]:
                if not following.strip():
                    continue
                following_indent = len(following) - len(following.lstrip())
                if following_indent <= indent:
                    break
                folded_lines.append(following.strip())
            value = " ".join(folded_lines)
        value = value.strip("'\"")
        assert len(value) <= 300, (
            f"Custom GPT의 300자 제한 초과: line {index + 1} "
            f"({len(value)}자)"
        )

    # ChatGPT Actions requires path parameter fields to be present on the
    # operation. A reusable component parameter $ref is valid OpenAPI, but the
    # GPT editor currently skips these operations because it does not resolve
    # the ref before checking for a non-empty parameter name.
    assert "#/components/parameters/" not in schema

    issue_operations = (
        "listLearningLogIssueComments",
        "appendLearningLogChunk",
        "getLearningLogIssue",
        "closeLearningLogIssue",
    )
    for operation_id in issue_operations:
        operation_match = re.search(
            rf"(?ms)^      operationId: {re.escape(operation_id)}\n"
            rf"(?P<body>.*?)(?=^    (?:get|post|put|patch|delete):|^  /|^components:)",
            schema,
        )
        assert operation_match, f"Action operation을 찾을 수 없습니다: {operation_id}"
        body = operation_match.group("body")
        assert re.search(
            r"(?ms)^      parameters:\n"
            r"        - name: issue_number\n"
            r"          in: path\n"
            r"          required: true\n"
            r"(?:          .*\n)*?"
            r"          schema:\n"
            r"            type: integer\n",
            body,
        ), f"{operation_id}의 issue_number path parameter가 inline 형식이 아닙니다."


def assert_custom_gpt_routing_contract() -> None:
    root = Path(__file__).resolve().parents[1]
    schema = (root / "system/ACTION_SCHEMA.yaml").read_text(encoding="utf-8")
    instructions = (root / "system/CUSTOM_GPT_INSTRUCTIONS.md").read_text(
        encoding="utf-8"
    )
    entrypoint = (root / "system/CHATGPT_ENTRYPOINT.md").read_text(
        encoding="utf-8"
    )

    operation_ids = set(re.findall(r"^      operationId: (\w+)$", schema, re.M))
    required_operations = {
        "listRepositoryRoot",
        "getStudyPath",
        "createLearningLogIssue",
        "listLearningLogIssueComments",
        "appendLearningLogChunk",
        "getLearningLogIssue",
        "closeLearningLogIssue",
    }
    assert operation_ids == required_operations

    for operation_id in required_operations:
        assert f"`{operation_id}`" in instructions

    assert "state/CURRENT_LEARNING_CONTEXT.md" in schema
    assert "state/CURRENT_LEARNING_CONTEXT.md" in instructions
    assert "system/CHATGPT_ENTRYPOINT.md" in instructions

    routing_triggers = (
        "이전 공부를 이어나가자",
        "어디까지 공부했어?",
        "논문을 마저 읽자",
    )
    for trigger in routing_triggers:
        assert trigger in schema

    assert "자연어로 답하기 전에" in instructions
    assert 'getStudyPath(path="state/CURRENT_LEARNING_CONTEXT.md", ref="main")' in instructions
    assert "아래 Action을 정확히 한 번 먼저 호출한다" in instructions
    assert "세션 시작 전에 다시 읽지 않는다" in instructions
    assert "파일별 호출 문장을 대신 작성하게 하지 않는다" in instructions
    assert "Action을 호출하지 않은 채" in instructions
    assert "파일을 붙여 넣기" in instructions
    assert "Action 실행 계약" in entrypoint
    assert "GitHub 웹 검색" in entrypoint
    assert "항상 먼저 `state/CURRENT_LEARNING_CONTEXT.md` 한 파일만 읽고" in entrypoint
    assert "사용자에게 파일별 호출을 요구하지 않는다" in entrypoint

    get_study_path_description = re.search(
        r"operationId: getStudyPath.*?description: >-\n(?P<body>.*?)\n      parameters:",
        schema,
        re.S,
    )
    assert get_study_path_description
    description = " ".join(
        line.strip() for line in get_study_path_description.group("body").splitlines()
    )
    assert "path=state/CURRENT_LEARNING_CONTEXT.md" in description
    assert "then begin" in description
    assert "CHATGPT_ENTRYPOINT.md" not in description


def note(extra: str = "") -> str:
    return f"""# 학습 기록: 테스트 (Test)

## Metadata
- Date: 2026-08-09
- Topic: Test
- Document type: learning-log
- Domain: research-os
- Roadmap stage: system-development
- Status: working
- Source: conversation
- Evidence: self-explanation
- Related notes: 없음
- Last updated: 2026-08-09

## 1. 오늘 공부한 목적
저장 경로를 검증한다.

## 2. 오늘 이해한 내용
Issue와 GitHub Actions의 역할을 구분했다. {extra}

## 3. 핵심 개념
- Issue queue

## 4. 내가 처음 이해한 방식
파일을 직접 저장한다고 생각했다.

## 5. 오해 또는 불확실한 부분
없음.

## 6. 수정된 이해
CI가 파일을 만든다.

## 7. 질문
### 해결되지 않은 질문
- 없음
### 해결된 질문
- 누가 파일을 쓰는가? CI.

## 8. AI 반도체 및 SSL 목표와의 연결
연구 학습 기록의 기반이다.

## 9. 다음 행동
실제 저장을 시험한다.

## 10. 자기 설명 점검
- [x] 용어의 정의를 설명할 수 있다.
- [x] 구조 또는 동작 과정을 설명할 수 있다.
- [ ] 관련 개념과 비교할 수 있다.
- [ ] AI 반도체에서 왜 중요한지 설명할 수 있다.

## 사용자 원문
테스트 원문
"""


def payload(operation: str, expected_sha: str, body: str) -> dict:
    envelope = (
        "<!-- research-os-ingest:v1\n"
        f"operation: {operation}\n"
        "target_path: learning-logs/2026/08/2026-08-09-test.md\n"
        f"expected_sha: {expected_sha}\n"
        "-->\n"
    )
    return {
        "number": 1,
        "title": "[learning-log] 2026-08-09 test",
        "author": "thisisjskim",
        "repository_owner": "thisisjskim",
        "body": envelope + body,
        "comments": [
            {"author": "someone-else", "body": "악의적인 내용"},
            {"author": "github-actions[bot]", "body": "bot 결과"},
        ],
    }


def run_cli(payload_data: dict, root: Path) -> tuple[subprocess.CompletedProcess, Path]:
    payload_path = root / "payload.json"
    report_path = root / "report.md"
    payload_path.write_text(
        json.dumps(payload_data, ensure_ascii=False), encoding="utf-8"
    )
    script_path = Path(__file__).with_name("ingest_learning_log.py")
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            str(script_path),
            "--payload",
            str(payload_path),
            "--root",
            str(root),
            "--report",
            str(report_path),
        ],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return completed, report_path


def main() -> int:
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)

        path, operation = ingest.ingest(payload("create", "new", note()), root)
        assert operation == "create"
        target = root / path
        assert target.exists()
        content = target.read_text(encoding="utf-8")
        assert "악의적인 내용" not in content  # external comment filtering
        assert "bot 결과" not in content  # bot comment filtering
        assert ingest.markdown_heading_lines(content).count(
            "## 1. 오늘 공부한 목적"
        ) == 1

        sha = ingest.git_blob_sha(target.read_bytes())
        _, operation = ingest.ingest(payload("update", sha, note("업데이트됨.")), root)
        assert operation == "update"
        assert "업데이트됨." in target.read_text(encoding="utf-8")

        mixed_case = payload(
            "update", ingest.git_blob_sha(target.read_bytes()), note("대소문자")
        )
        mixed_case["author"] = "ThisIsJsKim"
        mixed_case["comments"] = [
            {"author": "THISISJSKIM", "body": "소유자 댓글"},
        ]
        ingest.ingest(mixed_case, root)
        assert "소유자 댓글" in target.read_text(encoding="utf-8")

        assert_rejected(
            lambda: ingest.ingest(payload("update", "0" * 40, note()), root),
            "stale SHA가 거부되지 않았습니다.",
        )

        invalid = payload("create", "new", note())
        invalid["body"] = invalid["body"].replace(
            "learning-logs/2026/08/2026-08-09-test.md", "system/RESEARCH_OS.md"
        )
        assert_rejected(
            lambda: ingest.ingest(invalid, root),
            "허용되지 않은 경로가 거부되지 않았습니다.",
        )

        invalid_envelope = payload("create", "new", note())
        invalid_envelope["body"] = invalid_envelope["body"].replace(
            "research-os-ingest:v1", "research-os-ingest:v2"
        )
        assert_rejected(
            lambda: ingest.ingest(invalid_envelope, root),
            "잘못된 envelope가 거부되지 않았습니다.",
        )

        result_comment = payload(
            "update", ingest.git_blob_sha(target.read_bytes()), note("결과 댓글 필터")
        )
        result_comment["comments"] = [
            {
                "author": "thisisjskim",
                "body": "<!-- research-os-result -->\n자동 처리 결과",
            }
        ]
        ingest.ingest(result_comment, root)
        assert "자동 처리 결과" not in target.read_text(encoding="utf-8")

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        alias = "## 1. 오늘 공부한 목표"
        canonical = "## 1. 오늘 공부한 목적"
        alias_note = note().replace(canonical, alias, 1)
        alias_note += (
            "\n일반 본문의 ## 1. 오늘 공부한 목표 표현은 유지한다.\n"
            "> ## 1. 오늘 공부한 목표\n"
            "```markdown\n"
            "## 1. 오늘 공부한 목표\n"
            "```\n"
        )
        path, _ = ingest.ingest(payload("create", "new", alias_note), root)
        normalized = (root / path).read_text(encoding="utf-8")
        assert normalized.count(canonical) == 1
        assert "일반 본문의 ## 1. 오늘 공부한 목표 표현은 유지한다." in normalized
        assert "> ## 1. 오늘 공부한 목표" in normalized
        assert "```markdown\n## 1. 오늘 공부한 목표\n```" in normalized
        independent_headings = ingest.markdown_heading_lines(normalized)
        assert alias not in independent_headings
        assert canonical in independent_headings

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        duplicate = note().replace(
            "## 1. 오늘 공부한 목적",
            "## 1. 오늘 공부한 목적\n\n## 1. 오늘 공부한 목표",
            1,
        )
        error = assert_rejected(
            lambda: ingest.ingest(payload("create", "new", duplicate), root),
            "canonical heading과 alias의 중복이 거부되지 않았습니다.",
        )
        assert error.code == "duplicate-required-heading"
        assert not (root / "learning-logs/2026/08/2026-08-09-test.md").exists()

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        unsupported = note().replace(
            "## 1. 오늘 공부한 목적", "## 1. 오늘 학습한 목적", 1
        )
        error = assert_rejected(
            lambda: ingest.ingest(payload("create", "new", unsupported), root),
            "등록되지 않은 유사 heading이 거부되지 않았습니다.",
        )
        assert error.code == "missing-required-heading"
        assert "`## 1. 오늘 공부한 목적`" in str(error)

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        report_path = root / "report.md"
        output_path = root / "github-output.txt"
        script_path = Path(__file__).with_name("ingest_learning_log.py")
        payload_path = root / "payload.json"
        payload_path.write_text(
            json.dumps(payload("create", "new", note()), ensure_ascii=False),
            encoding="utf-8",
        )
        completed = subprocess.run(
            [
                sys.executable,
                "-B",
                str(script_path),
                "--payload",
                str(payload_path),
                "--root",
                str(root),
                "--report",
                str(report_path),
                "--github-output",
                str(output_path),
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert completed.returncode == 0, completed.stderr
        assert (root / "learning-logs/2026/08/2026-08-09-test.md").exists()
        assert "<!-- research-os-result -->" in report_path.read_text(encoding="utf-8")
        outputs = output_path.read_text(encoding="utf-8")
        assert "target_path=learning-logs/2026/08/2026-08-09-test.md" in outputs
        assert "operation=create" in outputs

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        unsupported = note("SECRET-PAYLOAD-CONTENT").replace(
            "## 1. 오늘 공부한 목적", "## 1. 오늘 학습한 목적", 1
        )
        completed, report_path = run_cli(
            payload("create", "new", unsupported), root
        )
        assert completed.returncode == 1
        assert "Learning Log ingest 실패" in completed.stderr
        report = report_path.read_text(encoding="utf-8")
        assert report.startswith("<!-- research-os-result -->")
        assert "❌ Learning Log 처리 실패" in report
        assert "Error code: `missing-required-heading`" in report
        assert "`## 1. 오늘 공부한 목적`" in report
        assert "파일 저장: 수행되지 않음" in report
        assert "SECRET-PAYLOAD-CONTENT" not in report
        assert "Traceback" not in report
        assert not (root / "learning-logs/2026/08/2026-08-09-test.md").exists()

    sanitized = ingest.failure_report(
        "test-error", "첫 줄\n둘째 줄\x00" + ("가" * 400)
    )
    assert "\x00" not in sanitized
    assert "첫 줄 둘째 줄" in sanitized
    assert len(sanitized.split("- 원인: ", 1)[1].splitlines()[0]) <= 300

    assert_workflow_contract()
    assert_action_schema_contract()
    assert_custom_gpt_routing_contract()

    print("All tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
