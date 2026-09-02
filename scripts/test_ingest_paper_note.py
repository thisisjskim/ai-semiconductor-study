#!/usr/bin/env python3
"""Contract and regression tests for Paper Note ingest."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ingest_paper_note", ROOT / "scripts/ingest_paper_note.py"
)
assert SPEC and SPEC.loader
ingest = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ingest)


def replace_section(markdown: str, heading: str, next_heading: str, body: str) -> str:
    start = markdown.index(heading) + len(heading)
    end = markdown.index(next_heading, start)
    return markdown[:start] + "\n\n" + body.strip() + "\n\n" + markdown[end:]


def note(bridge: str = "") -> str:
    markdown = (ROOT / "templates/paper-note.md").read_text(encoding="utf-8")
    replacements = {
        "{Paper Title}": "Example Accelerator",
        "- Title:": "- Title: Example Accelerator",
        "- Paper type: foundational | ssl-lab | related": "- Paper type: foundational",
        "- Venue / Year:": "- Venue / Year: ExampleConf / 2026",
        "- Authors:": "- Authors: Example Author",
        "- Paper link:": "- Paper link: https://example.com/paper",
        "- Started: YYYY-MM-DD": "- Started: 2026-08-27",
        "- Resume Point:": (
            "- Resume Point: Section 3.2 / PDF p.6 / Figure 4에서 "
            "partial sum 이동을 확인하는 부분부터 재개한다."
        ),
    }
    for before, after in replacements.items():
        markdown = markdown.replace(before, after, 1)
    bridge_body = bridge or """
### 논문 안에서 해결한 선수지식

- 없음

### 별도로 이어가는 선수지식

- 없음
"""
    return replace_section(
        markdown,
        "## 3. Prerequisite Bridge",
        "## 4. Problem",
        bridge_body,
    )


def payload(
    markdown: str,
    operation: str = "create",
    expected_sha: str = "new",
    created_at: str = "2026-08-27T10:20:30Z",
    extra_envelope: str = "",
) -> dict:
    body = (
        "<!-- research-os-paper-note:v1\n"
        f"operation: {operation}\n"
        "intent: paper-reading-checkpoint\n"
        "target_path: paper-notes/foundational/2026-08-27-example-accelerator.md\n"
        f"expected_sha: {expected_sha}\n"
        f"{extra_envelope}"
        "-->\n"
        f"{markdown}"
    )
    return {
        "title": "[paper-note] example-accelerator",
        "issue_created_at": created_at,
        "author": "owner",
        "repository_owner": "owner",
        "body": body,
        "comments": [],
    }


def expect_error(function, code: str) -> None:
    try:
        function()
    except ingest.IngestError as error:
        assert error.code == code, (error.code, str(error))
    else:
        raise AssertionError(f"Expected IngestError({code})")


def assert_template_contract() -> None:
    template = (ROOT / "templates/paper-note.md").read_text(encoding="utf-8")
    assert "## 2. Reading Checkpoint" in template
    assert "- Resume Point:" in template
    assert "## 3. Prerequisite Bridge" in template
    assert "### 논문 안에서 해결한 선수지식" in template
    assert "### 별도로 이어가는 선수지식" in template
    assert "studying | paused | sufficient-for-paper" in template
    assert "저장 시 실제로 존재하는 Learning Log 경로가 하나 이상 필요하다" in template
    assert "## 17. Reading Session History" in template
    for removed in (
        "- Status: queued | reading | analyzed | revisiting",
        "- Current section:",
        "- Last completed section:",
        "- Current prerequisite gap:",
        "- Reading pass:",
        "## 15. Next Reading Action",
    ):
        assert removed not in template


def assert_repository_contract() -> None:
    workflow = (ROOT / ".github/workflows/paper-note-ingest.yml").read_text(
        encoding="utf-8"
    )
    assert "name: Paper Note Ingest" in workflow
    assert "startsWith(github.event.issue.title, '[paper-note]')" in workflow
    assert "issue_created_at: issue.created_at" in workflow
    assert "python -B scripts/test_ingest_paper_note.py" in workflow
    assert "python -B scripts/ingest_paper_note.py" in workflow
    preflight = workflow.split("- name: Preflight Paper Note", 1)[1].split(
        "- name: Ingest Paper Note", 1
    )[0]
    assert '--report "$RUNNER_TEMP/paper-note-report.md"' in preflight
    assert 'git add -- "$TARGET_PATH"' in workflow
    assert "git add -A" not in workflow
    assert "✅ Paper Note 처리 완료" in workflow
    assert "Checkpoint recorded at" in workflow
    contract = (ROOT / "system/PAPER_NOTE_ISSUE_CONTRACT.md").read_text(
        encoding="utf-8"
    )
    assert "research-os-paper-note:v1" in contract
    assert "intent: paper-reading-checkpoint" in contract
    assert "Issue의 변경되지 않는 `created_at`" in contract
    assert (ROOT / "system/PAPER_NOTE_AUTHORING_GUIDE.md").is_file()
    assert (ROOT / "paper-notes/README.md").is_file()
    entrypoint = (ROOT / "system/CHATGPT_ENTRYPOINT.md").read_text(encoding="utf-8")
    assert "Current Paper Note" in entrypoint
    assert "## Paper Reading Loop" in entrypoint
    assert "정확히 하나가 `studying`" in entrypoint
    assert "최신 Learning Log가 eDRAM·CNN 등 다른 주제여도" in entrypoint
    assert "system/PAPER_NOTE_ISSUE_CONTRACT.md" in entrypoint
    assert "변경 전·후" in entrypoint
    policy = (ROOT / "system/RESEARCH_OS.md").read_text(encoding="utf-8")
    assert "paper-notes/{foundational|ssl-lab|related}/YYYY-MM-DD-paper-slug.md" in policy
    assert ".github/workflows/paper-note-ingest.yml" in policy
    assert "### Paper Reading Recovery" in policy
    architecture = (ROOT / "system/ARCHITECTURE.md").read_text(encoding="utf-8")
    assert "scripts/ingest_paper_note.py" in architecture
    assert "최신 Learning Log나 파일명 순서는 Current Paper 선택에 사용하지 않는다" in architecture
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "Paper Reading Checkpoint 저장 계약" in agents


def assert_paper_tutoring_policy_contract() -> None:
    tutoring_path = ROOT / "system/PAPER_READING_TUTOR_POLICY.md"
    assert tutoring_path.is_file()
    tutoring = tutoring_path.read_text(encoding="utf-8")
    for required in (
        "사용자가 문장 또는 짧은 문단을 읽는다",
        "사용자가 이해한 내용을 먼저 설명한다",
        "논문 전체를 내부적으로 확인할 수는 있지만",
        "사용자가 실제로 읽은 범위까지만 평가한다",
        "잘못 이해한 개념",
        "사용자 자기 설명: 아직 확인하지 않음",
        "별도의 기계적 evidence status 필드를 새로 만들지 않고 자연어",
        "Paper claim",
        "User observation",
        "다음 내용을 설명하지 않고 기다린다",
        "Current Paper Note가 `없음`이면 현재 읽고 있는 paper가 저장되어 있지 않다고 알리고",
        "새롭게 읽을 논문의 제목이나 식별 정보를 사용자에게 요청한다",
        "사용자 승인 없이 새 Paper Note를 만들지 않는다",
        "이해 확인 질문을 하지 않는 것을 기본값으로 한다",
        "사용자가 모른다고 질문한 prerequisite를 GPT가 새로 설명했다",
        "사용자의 잘못된 이해를 이후 논문 이해에 중요한 개념 수준에서 correction했다",
        "정확하거나, 방향은 맞고 사소한 조건만 빠졌거나",
        "논문이 직접 말함",
        "이해를 위한 보충 설명",
        "GPT의 추론이며 원 논문 또는 reference 확인 필요",
        "기존 Paper Note의 기록이나 모델의 기억만으로 exact fact를 원문에서 재확인한 것처럼 표현하지 않는다",
        "exact number나 mechanism을 직접 확인했다면 불필요하게 가능성 표현으로 약화하지 않고",
        "단순 영어 문법·번역이나 기술 개념을 추가하지 않은 문장 재표현은 Bridge 후보로 만들지 않는다",
        "이 문서에 없는 새로운 user-facing pedagogical framework",
    ):
        assert required in tutoring
    assert "중요한 prerequisite나 핵심 개념은 설명 후" not in tutoring

    understanding_evidence = tutoring.split("## 7. Understanding Evidence", 1)[1].split(
        "## 8. 논문이 제공하는 정보의 한계", 1
    )[0]
    for required in (
        "자기 설명을 요청할지는 §12의 trigger를 따른다",
        "AI가 설명했지만 사용자 자기 설명은 아직 확인되지 않음",
        "검증 질문을 추가로 강제하지 않는다",
    ):
        assert required in understanding_evidence
    assert "중요한 개념은 짧은 자기 설명을 통해 검증한다" not in tutoring

    question_policy = tutoring.split("## 12. 질문 사용", 1)[1].split(
        "## 13. Paper Note와 세션 종료", 1
    )[0]
    for required in (
        "이해 확인 질문을 하지 않는 것을 기본값으로 한다",
        "사용자가 모른다고 질문한 prerequisite",
        "중요한 개념 수준에서 correction",
        "사용자가 직접 이해 확인이나 quiz를 요청했다",
        "불완전한 부분이 이후 논문 이해를 막지 않으면 자기 설명을 다시 요구하지 않는다",
    ):
        assert required in question_policy
    assert "보통 1~3개" not in question_policy

    entrypoint = (ROOT / "system/CHATGPT_ENTRYPOINT.md").read_text(encoding="utf-8")
    assert "`system/PAPER_READING_TUTOR_POLICY.md`를 반드시 처음부터 끝까지 읽고" in entrypoint
    paper_loop = entrypoint.split("## Paper Reading Loop", 1)[1].split(
        "## 일반 Tutor Loop", 1
    )[0]
    assert "user-first protocol" in paper_loop
    assert "Current Paper Note가 `없음`이면" in paper_loop
    assert "Current Paper Note가 있을 때만" in paper_loop
    assert "Explain → Example" not in paper_loop
    assert "Progression over Exhaustiveness" not in paper_loop
    general_tutor_loop = entrypoint.split("## 일반 Tutor Loop", 1)[1]
    assert "일반 Roadmap 학습과 별도 Learning Log 학습에만 적용" in general_tutor_loop
    assert "Paper Reading Loop와 논문 읽기 자체에는 적용하지 않는다" in general_tutor_loop
    assert "Progression over Exhaustiveness" in general_tutor_loop

    research_os = (ROOT / "system/RESEARCH_OS.md").read_text(encoding="utf-8")
    assert "논문 읽기와 논문 읽기 재개의 user-facing behavior" in research_os
    assert "PAPER_READING_TUTOR_POLICY.md" in research_os

    roadmap = (ROOT / "roadmap/ROADMAP.md").read_text(encoding="utf-8")
    assert "PAPER_READING_TUTOR_POLICY.md" in roadmap
    assert "논문은 다음 세 번의 pass로 읽는다" not in roadmap
    assert "영어 논문은 문장 번역보다" not in roadmap

    authoring = (ROOT / "system/PAPER_NOTE_AUTHORING_GUIDE.md").read_text(
        encoding="utf-8"
    )
    assert "별도 evidence status 필드를 추가하지 않고" in authoring
    assert "저장 전에 사용자의 짧은 자기 설명을 한 번 요청한다" not in authoring
    assert "## 7. Prerequisite Inventory와 Bridge Audit" in authoring
    assert "마지막으로 저장된 checkpoint 이후 현재 conversation" in authoring
    assert "Architecture, Method, Questions에 내용이 있다는 이유로 Bridge 반영을 생략하지 않는다" in authoring
    assert "Bridge 대상 아님`과 제외 이유" in authoring
    assert "새로운 고정 section이나 evidence status field를 추가하지 않는다" in authoring
    assert "Inventory의 모든 후보를 기존·제안 Bridge와 대조하고 누락을 보완했는가?" in authoring
    bridge_audit = authoring.split(
        "## 7. Prerequisite Inventory와 Bridge Audit", 1
    )[1].split("## 8. 저장 전 점검", 1)[0]
    for required in (
        "뜻이나 작동 원리를 질문했고 GPT가 별도로 설명한 개념",
        "중요한 개념적 오해를 correction한 내용",
        "Reference deep-dive candidate",
        "Bridge 대상 아님`과 제외 이유",
        "단순 영어 문법·번역",
        "누락을 보완한 뒤에만",
        "기존 `Questions` 또는 관련 분석 section에 자연어로 보존한다",
    ):
        assert required in bridge_audit

    paper_template = (ROOT / "templates/paper-note.md").read_text(encoding="utf-8")
    assert "Prerequisite Inventory" not in paper_template
    assert "Prerequisite Bridge audit" not in paper_template

    assert "Prerequisite Inventory를 만들고 기존·제안 Bridge와 대조" in entrypoint
    assert "Architecture, Method 또는 Questions에 기록했다는 이유로 Bridge 반영을 생략하지 않는다" in entrypoint
    assert "Prerequisite Bridge audit" in entrypoint

    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    architecture = (ROOT / "system/ARCHITECTURE.md").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for document in (agents, architecture, readme):
        assert "PAPER_READING_TUTOR_POLICY.md" in document


def assert_ingest_contract() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        target_path, operation, timestamp = ingest.ingest(payload(note()), root)
        target = root / target_path
        assert operation == "create"
        assert timestamp == "2026-08-27T10:20:30Z"
        stored = target.read_text(encoding="utf-8")
        assert "- Checkpoint recorded at: 2026-08-27T10:20:30Z" in stored
        assert "GitHub Actions가 Issue created_at" not in stored

        old_sha = ingest.git_blob_sha(target.read_bytes())
        updated = stored.replace("아직 분석하지 않음", "확인된 Problem", 1)
        result = ingest.ingest(
            payload(
                updated,
                operation="update",
                expected_sha=old_sha,
                created_at="2026-08-28T01:02:03Z",
            ),
            root,
        )
        assert result[1] == "update"
        assert "- Checkpoint recorded at: 2026-08-28T01:02:03Z" in target.read_text(
            encoding="utf-8"
        )

        expect_error(
            lambda: ingest.validate_payload(
                payload(updated, operation="update", expected_sha=old_sha), root
            ),
            "paper-note-validation-error",
        )


def assert_bridge_validation() -> None:
    two_studying = """
### 논문 안에서 해결한 선수지식

- 없음

### 별도로 이어가는 선수지식

#### CNN

- Status: studying
- 논문에서 필요한 이유: dataflow 이해
- 이 논문에 충분한 기준: convolution mapping 설명
- Learning Logs:
  - 없음

#### Quantization

- Status: studying
- 논문에서 필요한 이유: precision 이해
- 이 논문에 충분한 기준: bit-width trade-off 설명
- Learning Logs:
  - 없음
"""
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        expect_error(
            lambda: ingest.validate_payload(payload(note(two_studying)), root),
            "multiple-studying-bridges",
        )

        missing_log = two_studying.replace(
            "#### Quantization\n\n- Status: studying",
            "#### Quantization\n\n- Status: paused",
        ).replace(
            "  - 없음",
            "  - `learning-logs/2026/08/2026-08-27-cnn-foundations.md`",
            1,
        )
        expect_error(
            lambda: ingest.validate_payload(payload(note(missing_log)), root),
            "missing-related-learning-log",
        )

        invalid_status = missing_log.replace(
            "- Status: studying", "- Status: finished", 1
        ).replace(
            "  - `learning-logs/2026/08/2026-08-27-cnn-foundations.md`",
            "  - 없음",
            1,
        )
        expect_error(
            lambda: ingest.validate_payload(payload(note(invalid_status)), root),
            "invalid-bridge-status",
        )

        studying_without_log = """
### 논문 안에서 해결한 선수지식

- 없음

### 별도로 이어가는 선수지식

#### CNN

- Status: studying
- 논문에서 필요한 이유: dataflow 이해
- 이 논문에 충분한 기준: convolution mapping 설명
- Learning Logs:
  - 없음
"""
        expect_error(
            lambda: ingest.validate_payload(
                payload(note(studying_without_log)), root
            ),
            "studying-bridge-without-learning-log",
        )

        studying_without_concept = studying_without_log.replace(
            "#### CNN\n\n", "", 1
        )
        expect_error(
            lambda: ingest.validate_payload(
                payload(note(studying_without_concept)), root
            ),
            "invalid-tracked-bridge-structure",
        )

        log_path = Path(
            "learning-logs/2026/08/2026-08-27-cnn-foundations.md"
        )
        (root / log_path).parent.mkdir(parents=True, exist_ok=True)
        (root / log_path).write_text("# stored Learning Log\n", encoding="utf-8")
        studying_with_log = studying_without_log.replace(
            "  - 없음", f"  - `{log_path.as_posix()}`", 1
        )
        ingest.validate_payload(payload(note(studying_with_log)), root)

        paused_without_log = studying_without_log.replace(
            "- Status: studying", "- Status: paused", 1
        )
        ingest.validate_payload(payload(note(paused_without_log)), root)

        missing_status = paused_without_log.replace("- Status: paused\n", "", 1)
        expect_error(
            lambda: ingest.validate_payload(payload(note(missing_status)), root),
            "missing-bridge-status",
        )


def assert_identity_and_checkpoint_validation() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        wrong_owner = payload(note())
        wrong_owner["author"] = "someone-else"
        expect_error(
            lambda: ingest.validate_payload(wrong_owner, root),
            "paper-note-validation-error",
        )

        wrong_slug = payload(note())
        wrong_slug["title"] = "[paper-note] different-paper"
        expect_error(
            lambda: ingest.validate_payload(wrong_slug, root),
            "paper-note-validation-error",
        )

        missing_resume = note().replace(
            "- Resume Point: Section 3.2 / PDF p.6 / Figure 4에서 partial sum 이동을 확인하는 부분부터 재개한다.",
            "- Resume Point:",
            1,
        )
        expect_error(
            lambda: ingest.validate_payload(payload(missing_resume), root),
            "paper-note-validation-error",
        )

        wrong_started = note().replace(
            "- Started: 2026-08-27", "- Started: 2026-08-26", 1
        )
        expect_error(
            lambda: ingest.validate_payload(payload(wrong_started), root),
            "paper-note-validation-error",
        )

        bad_time = payload(note(), created_at="2026-08-27 10:20:30")
        expect_error(
            lambda: ingest.validate_payload(bad_time, root),
            "invalid-checkpoint-recorded-at",
        )


def assert_envelope_contract() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        expect_error(
            lambda: ingest.validate_payload(
                payload(note(), extra_envelope="mode: checkpoint\n"), root
            ),
            "invalid-envelope",
        )
        wrong = payload(note())
        wrong["body"] = wrong["body"].replace(
            "intent: paper-reading-checkpoint", "intent: maintenance"
        )
        expect_error(
            lambda: ingest.validate_payload(wrong, root),
            "invalid-intent",
        )


def assert_cli_report() -> None:
    assert "✅ Paper Note 처리 완료" in (
        ingest.RESULT_MARKER + "\n✅ Paper Note 처리 완료"
    )
    report = ingest.failure_report("example", "bad\nmessage")
    assert report.startswith(ingest.RESULT_MARKER)
    assert "bad message" in report


def main() -> int:
    assert_template_contract()
    assert_repository_contract()
    assert_paper_tutoring_policy_contract()
    assert_ingest_contract()
    assert_bridge_validation()
    assert_identity_and_checkpoint_validation()
    assert_envelope_contract()
    assert_cli_report()
    print("All Paper Note ingest tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
