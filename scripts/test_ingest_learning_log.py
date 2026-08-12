#!/usr/bin/env python3
"""Contract tests for ingest_learning_log.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import ingest_learning_log as ingest


def assert_rejected(action, message: str) -> None:
    try:
        action()
    except ingest.IngestError:
        return
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
        payload_path = root / "payload.json"
        report_path = root / "report.md"
        output_path = root / "github-output.txt"
        payload_path.write_text(
            json.dumps(payload("create", "new", note()), ensure_ascii=False),
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

    assert_workflow_contract()

    print("All tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
