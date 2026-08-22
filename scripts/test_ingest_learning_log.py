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


def install_metadata_schema(root: Path) -> None:
    repository_root = Path(__file__).resolve().parents[1]
    source = repository_root / "system/LEARNING_LOG_METADATA_SCHEMA.json"
    target = root / "system/LEARNING_LOG_METADATA_SCHEMA.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


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
        "- name: Preflight Learning Log",
        "- name: Ingest Learning Log",
        "- name: Validate ingest result",
        "- name: Commit Learning Log",
        "- name: Comment success",
        "- name: Comment failure",
    )
    positions = [workflow.index(step) for step in required_steps]
    assert positions == sorted(positions), "Workflow 단계 순서가 계약과 다릅니다."
    assert "group: research-os-main" in workflow
    assert "startsWith(github.event.issue.title, '[learning-log]')" in workflow
    assert workflow.count("python -B scripts/ingest_learning_log.py") == 2
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
    assert "GitHub 연결 실행 계약" in entrypoint
    assert "GitHub 웹 검색" in entrypoint
    assert "항상 먼저 `state/CURRENT_LEARNING_CONTEXT.md` 한 파일만 읽고" in entrypoint
    assert "사용자에게 파일별 호출을 요구하지 않는다" in entrypoint
    assert "system/LEARNING_LOG_ISSUE_CONTRACT.md" in entrypoint
    assert "commit ref" in entrypoint
    assert "특정 tool 이름이 항상 존재한다고 가정하지 않는다" in entrypoint
    assert "capability 기준" in entrypoint
    assert "system/LEARNING_LOG_ISSUE_CONTRACT.md" in instructions
    assert "getStudyPath" in instructions

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


def assert_learning_log_guidance_contract() -> None:
    root = Path(__file__).resolve().parents[1]
    guide = (root / "system/LEARNING_LOG_ISSUE_CONTRACT.md").read_text(
        encoding="utf-8"
    )
    authoring = (root / "system/LEARNING_LOG_AUTHORING_GUIDE.md").read_text(
        encoding="utf-8"
    )
    scenario = (root / "system/LEARNING_LOG_E2E_SCENARIO.md").read_text(
        encoding="utf-8"
    )
    schema = (root / "system/ACTION_SCHEMA.yaml").read_text(encoding="utf-8")

    contract_lines = (
        "operation: create",
        "target_path: learning-logs/YYYY/MM/YYYY-MM-DD-topic-slug.md",
        "expected_sha: new",
    )
    for line in contract_lines:
        assert line in guide
    assert "mode" in guide and "허용하지 않는다" in guide
    assert "✅ Learning Log 처리 완료" in guide
    assert "commit ref" in guide
    assert "tool-independent" in guide
    assert "Custom GPT Action interface only" in guide
    assert "일반 plugin 저장의 선행 읽기 파일이 아니다" in guide
    assert "system/LEARNING_LOG_METADATA_SCHEMA.json" in guide

    assert "evidence inventory" in authoring
    assert "assistant-explained" in authoring
    assert "claim-evidence" in authoring
    assert "과거 문장" in authoring
    assert "재사용하지 않는다" in authoring
    assert "system/LEARNING_LOG_METADATA_SCHEMA.json" in authoring
    assert "32bit register" not in authoring
    assert not (root / "system/examples/GOOD_LEARNING_LOG_ISSUE.md").exists()

    assert "mode: create" in scenario
    assert "성공 comment" in scenario
    assert "target file" in scenario
    assert "일반 plugin에서는 `ACTION_SCHEMA.yaml`을 읽을 필요가 없다" in scenario
    assert "capability 기준" in scenario

    learning_request = re.search(
        r"(?ms)^    LearningLogIssueRequest:\n(?P<body>.*?)(?=^    \w+IssueRequest:)",
        schema,
    )
    assert learning_request
    request_body = learning_request.group("body")
    assert "mode is invalid" in request_body
    assert "register-sram-circuits" not in request_body


def assert_general_session_protocol_contract() -> None:
    root = Path(__file__).resolve().parents[1]
    entrypoint = (root / "system/CHATGPT_ENTRYPOINT.md").read_text(
        encoding="utf-8"
    )
    research_os = (root / "system/RESEARCH_OS.md").read_text(encoding="utf-8")
    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    architecture = (root / "system/ARCHITECTURE.md").read_text(encoding="utf-8")
    readme = (root / "README.md").read_text(encoding="utf-8")

    required_sections = (
        "## Purpose",
        "## 세션 시작",
        "## Tutor Loop",
        "## Learning Unit",
        "## Checkpoint",
        "## Continue Session",
        "## 세션 종료와 저장",
        "## New Chat Recovery",
    )
    for section in required_sections:
        assert section in entrypoint

    assert "3~6줄" in entrypoint
    assert "Explain → Example → Ask → User explanation → Diagnose → Follow-up" in entrypoint
    assert "작은 Learning Unit 하나" in entrypoint
    assert "AI가 설명한 내용을 사용자가 이해했다는 evidence로 간주하지 않는다" in entrypoint
    assert "같은 checkpoint에서 매 턴 반복해 묻지 않는다" in entrypoint
    assert "기록은 나중에 하고 계속하자" in entrypoint
    assert "단순한 `정리해줘`" in entrypoint
    assert "공부 시작하자" in entrypoint
    assert "지난번부터 이어서 하자" in entrypoint
    assert "AI semiconductor 공부 계속하자" in entrypoint

    assert "Learning Unit은" in research_os
    assert "단순 동의나 따라 말하기만으로 완료 판정하지 않는다" in research_os
    assert "제안 없이 나온 일반적인" in research_os
    assert "작은 Learning Unit의 완료는 다음 unit으로 이동할 수 있다는 뜻" in research_os
    assert "단일 질문과 답변" in research_os
    assert "prerequisite를 건너뛴다는 뜻이 아니다" in research_os
    assert "새로운 topic·topology·physical mechanism" in research_os

    assert "일반 ChatGPT 학습 시작점" in agents
    assert "Learning Log 저장 계약: `system/LEARNING_LOG_ISSUE_CONTRACT.md`" in agents
    assert "Custom GPT Action 설정 전용" in agents
    assert "Learning Unit checkpoint" in architecture
    assert "Custom GPT Action interface에만 사용" in architecture
    assert "일반 ChatGPT 새 채팅" in readme
    assert "system/CHATGPT_ENTRYPOINT.md\n→ state/CURRENT_LEARNING_CONTEXT.md" in readme
    assert "GitHub의 ai-semiconductor-study 기반으로 공부 시작하자" in readme


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
        install_metadata_schema(root)

        invalid_domain = note().replace(
            "- Domain: research-os", "- Domain: memory", 1
        )
        error = assert_rejected(
            lambda: ingest.ingest(
                payload("create", "new", invalid_domain), root
            ),
            "허용 목록에 없는 Domain이 거부되지 않았습니다.",
        )
        assert error.code == "invalid-domain"
        assert "지원되지 않는 Domain metadata" in str(error)
        assert "memory-architecture" in str(error)
        assert not (root / "learning-logs/2026/08/2026-08-09-test.md").exists()

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

        issue_19_envelope = payload("create", "new", note())
        issue_19_envelope["body"] = issue_19_envelope["body"].replace(
            "operation: create\n", "mode: create\n"
        ).replace("expected_sha: new\n", "")
        error = assert_rejected(
            lambda: ingest.ingest(issue_19_envelope, root),
            "Issue #19 형식의 envelope가 거부되지 않았습니다.",
        )
        assert "expected_sha" in str(error)
        assert "operation" in str(error)

        unknown_field = payload("create", "new", note())
        unknown_field["body"] = unknown_field["body"].replace(
            "operation: create\n", "operation: create\nmode: create\n"
        )
        error = assert_rejected(
            lambda: ingest.ingest(unknown_field, root),
            "미등록 envelope 필드가 거부되지 않았습니다.",
        )
        assert error.code == "invalid-metadata"

        mismatched_title = payload("create", "new", note())
        mismatched_title["title"] = "[learning-log] 2026-08-09 other-slug"
        assert_rejected(
            lambda: ingest.ingest(mismatched_title, root),
            "title과 target_path의 slug 불일치가 거부되지 않았습니다.",
        )

        loose_title = payload("create", "new", note())
        loose_title["title"] = "[learning-log] test"
        assert_rejected(
            lambda: ingest.ingest(loose_title, root),
            "느슨한 title 형식이 거부되지 않았습니다.",
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
        install_metadata_schema(root)
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
        install_metadata_schema(root)
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
        install_metadata_schema(root)
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
        install_metadata_schema(root)
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
        install_metadata_schema(root)
        completed, _ = run_cli(payload("create", "new", note()), root)
        assert completed.returncode == 0, completed.stderr
        target = root / "learning-logs/2026/08/2026-08-09-test.md"
        assert target.exists()

        payload_path = root / "preflight-payload.json"
        payload_path.write_text(
            json.dumps(
                {
                    **payload("create", "new", note()),
                    "title": "[learning-log] 2026-08-10 preflight",
                    "body": payload("create", "new", note())["body"]
                    .replace("2026-08-09-test", "2026-08-10-preflight")
                    .replace("2026/08/2026-08-09-test", "2026/08/2026-08-10-preflight"),
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
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
                "--validate-only",
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        assert completed.returncode == 0, completed.stderr
        assert "Learning Log 검증 완료" in completed.stdout
        assert not (root / "learning-logs/2026/08/2026-08-10-preflight.md").exists()

    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        install_metadata_schema(root)
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
    assert_learning_log_guidance_contract()
    assert_general_session_protocol_contract()

    print("All tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
