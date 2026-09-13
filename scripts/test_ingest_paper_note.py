#!/usr/bin/env python3
"""Contract and regression tests for Paper Note ingest."""

from __future__ import annotations

import importlib.util
import json
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_PAPER_SOURCE_IMMEDIATE_SECTIONS = (
    "Problem",
    "Key Idea",
    "Architecture",
    "Method",
    "Experiments",
    "Results",
    "Trade-offs",
    "Paper-Reported Limitations",
)
EXPECTED_PAPER_SOURCE_IMMEDIATE_POLICY = (
    "**Paper-source immediate sections:** "
    + ", ".join(EXPECTED_PAPER_SOURCE_IMMEDIATE_SECTIONS)
)
EXPECTED_PAPER_SOURCE_IMMEDIATE_AUTHORING = (
    "**Paper-source immediate sections:** "
    + ", ".join(f"`{section}`" for section in EXPECTED_PAPER_SOURCE_IMMEDIATE_SECTIONS)
)
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
        "## 2. Prerequisite Bridge",
        "## 3. Problem",
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


def delta_payload(
    delta: dict,
    expected_sha: str,
    created_at: str = "2026-08-28T01:02:03Z",
) -> dict:
    body = (
        "<!-- research-os-paper-note:v2\n"
        "operation: checkpoint-update\n"
        "intent: paper-reading-checkpoint\n"
        "target_path: paper-notes/foundational/2026-08-27-example-accelerator.md\n"
        f"expected_sha: {expected_sha}\n"
        "-->\n"
        + json.dumps(delta, ensure_ascii=False)
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
    assert len(EXPECTED_PAPER_SOURCE_IMMEDIATE_SECTIONS) == 8
    assert len(template.encode("utf-8")) < 7000
    assert len(template.splitlines()) < 280
    assert "## 1. Citation" not in template
    assert "## 1. Reading Checkpoint" in template
    assert "- Resume Point:" in template
    assert "## 2. Prerequisite Bridge" in template
    assert "### 논문 안에서 해결한 선수지식" in template
    assert "- 실제 정의:" in template
    assert "### 별도로 이어가는 선수지식" in template
    assert "studying | paused | sufficient-for-paper" in template
    assert "## 3. Problem" in template
    assert "**Problem being addressed:**" in template
    assert "**Limitations of existing approaches:**" in template
    assert "**Why this problem matters:**" in template
    assert "이 논문이 해결하려는 문제는 무엇인가?" not in template
    assert "## 4. Motivation and Prior-Work Gap" not in template
    assert "## 4. Prerequisites" not in template
    assert "| Prerequisite | 현재 상태 | 필요한 보충 |" not in template
    assert "## 4. Key Idea" in template
    assert "**Proposed approach:**" in template
    assert "**Key mechanism:**" in template
    assert "**What is novel or different:**" in template
    assert "> 한 문장 요약:" not in template
    assert "## 9. Trade-offs" in template
    assert "| Structure / Approach | Benefit (Gain) | Trade-off / Cost | Evidence |" in template
    assert "| Gain | Cost / Trade-off | Evidence |" not in template
    assert "## 5. Architecture" in template
    assert "### Overall Architecture" in template
    assert "### {Architecture Family 또는 System Level}" in template
    assert "#### {Figure N(a) 또는 Structure Name}" in template
    for architecture_field in (
        "- 근거 위치: Section / PDF p. / Figure",
        "- 논문 내 역할:",
        "- Main Structure (Components):",
        "- Operation Overview:",
        "- Data / Signal Flow:",
        "- Benefits:",
        "- Challenges / Trade-offs:",
        "- 논문이 제공하지 않은 세부사항:",
    ):
        assert architecture_field in template
    assert "## 6. Method" in template
    for method_field in (
        "- Architecture reference:",
        "- Method purpose:",
        "- Input / Initial state:",
        "- Core operation:",
        "- Operation mechanism:",
        "- Output / State change:",
        "- Required conditions or assumptions:",
        "- Benefits:",
        "- Limitations / Trade-offs:",
        "- 근거 위치: Section / PDF p. / Figure / Equation",
    ):
        assert method_field in template
    assert "## 10. Limitations" in template
    assert "### Authors' Limitations" not in template
    assert "### My Observations" not in template
    assert "### Paper-Reported Limitations" in template
    assert "#### Structure-specific Capability / Applicability Limits" in template
    assert "##### {Architecture Family — Figure N(a) 또는 Structure Name}" in template
    assert "#### System- or Paper-level Capability / Applicability Limits" in template
    assert "##### {Limitation Name}" in template
    for limitation_field in (
        "- Related Architecture / Method:",
        "- Limited capability or applicability:",
        "- Applicable condition:",
        "- Consequence:",
        "- 근거 위치: Section / PDF p. / Figure / Table",
    ):
        assert limitation_field in template
    assert "### User-Identified Limitations" in template
    for user_limitation_field in (
        "- 사용자가 지적한 limitation:",
        "- 사용자가 근거로 사용한 paper content:",
        "- Paper에서 직접 확인된 내용:",
        "- 추가 확인이 필요한 부분:",
    ):
        assert user_limitation_field in template
    assert "## 11. Questions" in template
    for question_category in (
        "### 이해를 위한 질문",
        "### 비판적 질문",
        "### 후속 연구 질문",
    ):
        assert question_category in template
    for question_field in (
        "- 사용자의 질문:",
        "- 질문이 발생한 위치 또는 맥락:",
        "- 선정 이유:",
        "- 해결 과정:",
        "- 해결하며 알게 된 내용:",
        "- 해결 상태: resolved | partially-resolved | unresolved",
        "- 해결하지 못한 부분:",
        "- 해결에 사용한 근거:",
        "- Paper direct evidence:",
        "- GPT supplementary explanation:",
        "- User interpretation / hypothesis:",
    ):
        assert template.count(question_field) == 3, question_field
    assert "- Question Selection Gate를 통과한 질문과 해결 상태:" in template
    assert "- 새롭게 발생한 질문:" not in template
    assert "## 12. Connection to My Research Direction" in template
    assert "## 12. Connection to My Research Interest" not in template
    for connection_field in (
        "- 사용자가 표현한 research interest 또는 goal:",
        "- 연결되는 Paper element:",
        "- 연결 근거 위치: Section / PDF p. / Figure / Table / Equation",
        "- 연결 방식:",
        "- 이 논문이 내 연구 방향에서 수행하는 역할:",
        "- 기존 Questions / Limitations와의 관계:",
        "- 연결의 경계 또는 아직 확인되지 않은 부분:",
        "- 향후 활용: comparison paper | anchor paper | portfolio evidence | research framing | 기타 사용자 확인 내용",
    ):
        assert connection_field in template, connection_field
    for removed_connection_field in (
        "- 흥미로운 점:",
        "- 더 탐구하고 싶은 부분:",
        "- 다른 논문과의 연결:",
        "- 가능한 research direction:",
    ):
        assert removed_connection_field not in template
    assert "## 12. Connection to My Research Direction" in ingest.REQUIRED_HEADINGS
    assert "## 12. Connection to My Research Interest" not in ingest.REQUIRED_HEADINGS
    assert "## 13. Final Summary" in template
    assert "부분 분석 중이면 확인된 항목만 작성" not in template
    for final_summary_heading in (
        "### Problem",
        "### Key Idea",
        "### Architecture",
        "### Main Claim / Result and Supporting Evidence",
        "### Main Trade-off",
        "### Limitation",
        "### 내가 기억할 한 문장",
    ):
        assert final_summary_heading in template
    assert "\n### Main Result\n" not in template
    for main_claim_rule in (
        "- Main claim / result:",
        "- Representative supporting evidence or synthesis basis:",
        "- Evidence conditions / scope:",
        "- 근거 위치: Section / PDF p. / Figure / Table / Equation",
    ):
        assert main_claim_rule in template, main_claim_rule
    for policy_text in (
        "**Paper-source immediate sections**",
        "### Question Selection Gate",
        "### Research Connection Gate",
        "**Reading-completion synthesis**",
        "PDF Source Gate를 통과한 뒤",
        "GPT가 서로 떨어진 장점과 단점을 임의로 조합하지 않는다",
        "논문을 처음 받았을 때 자동으로 만들지 않는다",
        "완독 전에는 일부 field를 먼저 채우지 않고",
    ):
        assert policy_text not in template, policy_text
    assert "## 14. Reading Session History" in template
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
    assert "python -B scripts/test_ingest_paper_note.py" not in workflow
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
    assert "research-os-paper-note:v2" in contract
    assert "intent: paper-reading-checkpoint" in contract
    assert "Issue의 변경되지 않는 `created_at`" in contract
    assert "사용자가 직접 PB 기록을 요청했거나 GPT의 제안에 명시적으로 동의한 개념만 포함한다" in contract
    assert "checkpoint 전체의 저장 승인을 지정되지 않은 PB 항목 추가 승인으로 사용하지 않는다" in contract
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
        "사용자가 제공한 PDF 전체를 내부적으로 확인할 수는 있지만",
        "사용자가 실제로 읽은 범위까지만 평가한다",
        "잘못 이해한 개념",
        "사용자 자기 설명: 아직 확인하지 않음",
        "별도의 기계적 evidence status 필드를 새로 만들지 않고 자연어",
        "Paper claim",
        "User observation",
        "`pending verification`이 없으면 다음 내용을 설명하거나 질문하지 않고 기다린다",
        "Current Paper Note가 `없음`이면 현재 읽고 있는 paper가 저장되어 있지 않다고 알리고",
        "새롭게 읽을 논문의 제목이나 식별 정보와 PDF를 사용자에게 요청한다",
        "사용자 승인 없이 새 Paper Note를 만들지 않는다",
        "이해 확인 질문을 하지 않는 것을 기본값으로 한다",
        "사용자가 모른다고 질문한 prerequisite를 GPT가 새로 설명했다",
        "사용자의 개념적 오해 또는 이후 논문 이해를 실제로 방해하는 핵심 누락을 correction했다",
        "정확하거나, 방향은 맞고 사소한 조건만 빠졌거나",
        "논문이 직접 말함",
        "이해를 위한 보충 설명",
        "GPT의 추론이며 원 논문 또는 reference 확인 필요",
        "기존 Paper Note, 사용자가 붙여 넣은 문장, DOI·웹페이지·abstract, GPT가 찾은 다른 사본이나 모델의 기억만으로 exact fact를 원문에서 재확인한 것처럼 표현하지 않는다",
        "exact number나 mechanism을 직접 확인했다면 불필요하게 가능성 표현으로 약화하지 않고",
        "사용자가 직접 PB 기록을 요청했거나 GPT의 PB 제안에 동의한 개념만 임시 PB Inventory로 모은다",
        "이 문서에 없는 새로운 user-facing pedagogical framework",
    ):
        assert required in tutoring
    assert "중요한 prerequisite나 핵심 개념은 설명 후" not in tutoring

    source_gate = tutoring.split("### PDF Source Gate", 1)[1].split(
        "## 3. Current Reading Boundary", 1
    )[0]
    for required in (
        "Paper Note는 논문 identity, 사용자의 학습 evidence와 Resume Point를 복구하는 기록이지 논문 원문을 대체하는 source가 아니다",
        "현재 conversation에 직접 첨부한 PDF",
        "새 채팅마다 PDF를 다시 첨부받는다",
        "PDF를 실제로 열고 읽을 수 있다",
        "제목·저자·DOI 또는 다른 identifier",
        "사용자가 현재 읽는 section과 판단에 필요한 인접 문맥을 실제로 확인한다",
        "붙여 넣은 문장",
        "GPT가 찾은 다른 사본",
        "paper tutoring을 중단한다",
        "페이지 이미지나 supplementary 자료는 이미 올바른 PDF가 제공된 상태에서",
        "정확·불완전·잘못 이해한 내용으로 판정",
        "논문에서 분리한 일반 prerequisite 학습은 진행할 수 있다",
    ):
        assert required in source_gate
    assert "현재 접근 가능한 PDF·full text" not in tutoring

    primary_policy = tutoring.split("## 1. 최우선 원칙", 1)[1].split(
        "## 2. 세션 시작과 상태 복구", 1
    )[0]
    for required in (
        "§12의 `pending verification`이 없으면",
        "계속 읽겠다는 말 자체를 명시적인 검증 거부로 간주하지 않고",
        "같은 핵심 자기 설명을 한 번만 다시 요청한다",
        "한 번 재요청한 뒤에도 자기 설명 없이 계속 진행하겠다고 하면",
        "미확인 상태로 기록한 뒤 다음 읽기를 기다린다",
    ):
        assert required in primary_policy

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

    evaluation_policy = tutoring.split("## 5. 사용자 설명 평가", 1)[1].split(
        "## 6. Prerequisite 처리", 1
    )[0]
    for required in (
        "인과관계, 동작 원리, 비교 기준 또는 논문의 주장 범위를 잘못 해석하게 되는 누락",
        "§12의 correction trigger에 따라",
        "사소한 누락을 검증 질문을 하기 위해 `잘못 이해한 내용`으로 바꾸지 않는다",
        "PDF Source Gate를 통과하고",
        "현재 section과 필요한 인접 문맥을 실제로 확인한 뒤에만",
    ):
        assert required in evaluation_policy
    assert "중요한 개념 공백이면 그 이유를 짧게 밝히고 필요한 설명 뒤 자기 설명을 한 번 요청할 수 있다" not in tutoring

    question_policy = tutoring.split("## 12. 질문 사용", 1)[1].split(
        "## 13. Paper Note와 세션 종료", 1
    )[0]
    for required in (
        "이해 확인 질문을 하지 않는 것을 기본값으로 한다",
        "사용자가 모른다고 질문한 prerequisite",
        "개념적 오해 또는 이후 논문 이해를 실제로 방해하는 핵심 누락",
        "사용자가 직접 이해 확인이나 quiz를 요청했다",
        "자기 설명이 아직 확인되지 않은 상태를 `pending verification`",
        "불완전한 부분이 이후 논문 이해를 막지 않으면 자기 설명을 다시 요구하지 않는다",
        "수정된 오해 또는 보완된 핵심 누락",
        "계속 읽겠다는 말 자체를 명시적인 검증 거부로 간주하지 않고",
        "같은 핵심 자기 설명을 한 번만 다시 요청한다",
        "한 번 재요청한 뒤에도 자기 설명 없이 계속 진행하겠다고 하면",
        "사용자 자기 설명이 확인되지 않은 상태로 기록하고 다음 읽기를 기다린다",
        "tutoring verification 질문은 그 자체로 Paper Note의 `Questions`가 아니다",
        "§13의 Question Selection Gate를 통과한 경우에만 기록 후보",
    ):
        assert required in question_policy
    assert "보통 1~3개" not in question_policy
    assert "다만 중요한 prerequisite의 이해를 확인하지 않으면" not in question_policy

    paper_note_policy = tutoring.split("## 13. Paper Note와 세션 종료", 1)[1].split(
        "## 14. Resume Point", 1
    )[0]
    for required in (
        "### Paper Note section lifecycle boundary",
        EXPECTED_PAPER_SOURCE_IMMEDIATE_POLICY,
        "**Conversation-derived sections:** User-Identified Limitations, Questions와 Connection to My Research Direction",
        "**Reading-completion synthesis:** Final Summary",
        "checkpoint evidence가 마지막 본문 section까지의 읽기 완료를 뒷받침",
        "PDF 전체 분석만으로 미리 작성하지 않는다",
        "PDF를 받거나 전체 분석했다는 이유만으로 자동 작성하지 않는다",
        "Conversation-derived section은 PDF 분석만으로 사용자의 observation, question 또는 research connection을 만들어내지 않는다",
        "### Paper-source section의 no-inference rule",
        "합리적으로 추론할 수 있는 내용도 paper fact가 아니다",
        "정확히 `논문에서 언급되지 않음`으로 표시",
        "### Full-paper source synthesis",
        "사용자 진도와 별개인 paper-source synthesis 영역",
        "첨부 PDF 전체의 관련 section, figure, subfigure, caption, table, equation과 연결된 본문",
        "여덟 영역의 초안을 바로 작성한다",
        "영구 저장 승인을 대신하지 않으며",
        "architecture family를 먼저 나누고",
        "서로 다른 구성·동작·trade-off를 보이는 subfigure",
        "Result plot, dataset 예시와 배경 설명용 figure",
        "Main Structure (Components)",
        "Challenges / Trade-offs",
        "Method는 Architecture의 architecture family와 structure heading, 이름과 순서를 그대로 따른다",
        "Operation은 MAC에 한정하지 않고 arithmetic, logic, memory",
        "GPT가 별개의 장점과 단점을 임의로 결합하지 않는다",
        "Gain–Cost 관계는 Trade-offs에만 두고 Limitations에 반복하지 않으며",
        "단순한 challenge나 Gain–Cost 관계는 Limitation으로 승격하지 않는다",
        "### User-Identified Limitations의 지연 업데이트",
        "논문을 처음 받았을 때 자동으로 작성하지 않는다",
        "단순한 질문은 limitation으로 확정하지 않고 `Questions`에 유지한다",
        "사용자가 학습 세션을 마무리하면",
        "### Questions의 selection gate와 지연 업데이트",
        "`Questions`의 update source는 실제 사용자–ChatGPT 학습 대화다",
        "PDF 자체는 Question 생성 trigger가 아니다",
        "마지막 checkpoint 이후 사용자가 실제로 질문한 항목",
        "사용자가 명시적으로 채택해 실제로 탐구한 항목만 Question Inventory",
        "GPT가 사용자가 하지 않은 질문을 만들거나 제안만 한 질문을 기록해서는 안 된다",
        "특정 figure·table·equation·claim",
        "다음 세션에서 복구할 가치",
        "같은 질문의 재표현이나 발전형은 새 항목으로 만들지 않고 기존 질문에 통합",
        "기술 의미를 바꾸지 않는 번역·문법 질문",
        "해결 과정`, `해결하며 알게 된 내용`, `해결 상태`, `해결하지 못한 부분",
        "`resolved`, 중요한 일부가 남은 `partially-resolved`, 핵심 답을 확인하지 못한 `unresolved`",
        "Paper direct evidence, GPT supplementary explanation, User interpretation / hypothesis를 분리",
        "GPT 설명을 사용자 이해 evidence로 승격하지 않는다",
        "대화에서 해결 과정이나 사용자 해석이 확인되지 않은 field",
        "해당 category에 통과한 질문이 없으면 질문 record를 만들지 않고 `선정된 질문 없음`",
        "### Connection to My Research Direction의 selection gate와 지연 업데이트",
        "update source는 실제 사용자–ChatGPT 학습 대화다",
        "PDF 자체는 Research Connection 생성 trigger가 아니며",
        "Research Connection Inventory",
        "keyword 유사성이 아니라",
        "Questions에는 알아내야 할 gap과 해결 상태를 기록하고",
        "Research Connection에는 그 질문이나 Paper element가 사용자의 연구 방향에서 중요한 이유와 역할",
        "사용자가 받아들이지 않은 GPT 제안",
        "`확인된 연구 연결 없음`",
        "추가·갱신·제외 후보와 이유를 보여 준 뒤 사용자 승인 후에만 저장",
        "### Final Summary의 reading-completion gate",
        "사용자가 현재 논문 본문을 끝까지 읽었다고 명시",
        "Reading Checkpoint, Resume Point와 Reading Session History",
        "paper-source immediate sections를 완성했다는 사실은 이 gate를 통과시키지 않는다",
        "Final Summary 일부 field를 먼저 채우지 않고 section 전체를 `아직 분석하지 않음`",
        "중간 요약을 요청하면 현재 읽은 범위 안에서 대화로 답할 수 있지만 canonical Final Summary에는 저장하지 않는다",
        "`Main Claim / Result and Supporting Evidence`에는 논문의 primary claim 또는 result 하나",
        "대표 evidence 또는 synthesis basis 1~3개만 기록",
        "Evidence의 baseline, workload, dataset, precision, evaluation method와 scope",
        "서로 다른 결과를 조합해 논문이 하지 않은 claim을 만들거나 evidence보다 넓게 일반화하지 않는다",
        "Overview/review paper에는 신규 실험 result를 만들지 않고",
        "Detailed Results는 전체 evidence inventory이고 Final Summary는 primary claim과 대표 support의 압축본",
        "Results의 수치와 figure를 그대로 복사하지 않는다",
        "`내가 기억할 한 문장`은 실제 대화에서 확인된 내용만 기록",
        "reading coverage evidence일 뿐",
        "mastery evidence가 아니다",
        "Source-grounded field에는 GPT의 추론을 label과 함께 넣는 방식도 허용하지 않는다",
        "사용자의 자기 설명이나 이해 확인 evidence가 아니다",
    ):
        assert required in paper_note_policy

    behavior_scenarios = tutoring.split("## 18. 행동 점검 시나리오", 1)[1]
    for required in (
        "`pending verification`이 없으면 다음 내용을 설명하거나 질문하지 않고 기다린다",
        "명시적으로 거부하거나 재요청 뒤에도 계속 진행하면 미확인 상태로 기록하고 더 반복하지 않는다",
        "새 채팅에 PDF가 없으면 Paper Note에서 identity와 Resume Point만 복구하고",
        "첨부 PDF를 실제로 열어 제목·저자·identifier",
        "correction, exact number 또는 architecture mechanism 판정에는 확인한 PDF page 또는 section",
        "PDF Source Gate를 통과하면 Problem, Key Idea, Architecture, Method, Experiments, Results, Trade-offs와 Paper-Reported Limitations 초안을 바로 만들고",
        "Method는 Architecture와 같은 family·structure heading, 이름과 순서를 따른다",
        "Trade-off는 논문이 직접 연결한 Gain–Cost 쌍만 기록하고",
        "같은 Gain–Cost 관계를 Trade-offs와 Limitations에 중복 기록하지 않는다",
        "User-Identified Limitations는 사용자가 직접 limitation을 제기한 경우에만 후보로 모아 학습 세션 종료 시 업데이트",
        "Questions는 마지막 checkpoint 이후의 실제 사용자 질문에 selection gate를 적용해 학습 세션 종료 시 업데이트",
        "GPT가 제안만 한 질문, 사소한 질문, meta 질문과 중복 질문은 기록하지 않으며",
        "Connection to My Research Direction은 대화에서 확인된 사용자 관심과 구체적인 Paper anchor가 모두 있을 때만",
        "Research Connection은 관련 Question이나 Limitation을 복사하지 않고",
        "Final Summary는 사용자의 완독 선언과 마지막 본문 범위까지의 checkpoint가 모두 확인된 경우에만",
        "Final Summary 작성이나 완독 사실을 사용자의 전체 이해 또는 mastery evidence로 기록하지 않는다",
        "Full-paper source synthesis를 사용자가 해당 범위를 읽거나 이해했다는 evidence로 기록하지 않는다",
    ):
        assert required in behavior_scenarios

    entrypoint = (ROOT / "system/CHATGPT_ENTRYPOINT.md").read_text(encoding="utf-8")
    assert "`system/PAPER_READING_TUTOR_POLICY.md`를 반드시 처음부터 끝까지 읽고" in entrypoint
    paper_loop = entrypoint.split("## Paper Reading Loop", 1)[1].split(
        "## 일반 Tutor Loop", 1
    )[0]
    assert "user-first protocol" in paper_loop
    assert "Current Paper Note가 `없음`이면" in paper_loop
    assert "Current Paper Note가 있을 때만" in paper_loop
    assert "Resume Point를 paper reading boundary로 복구하되 PDF Source Gate를 통과하기 전에는" in paper_loop
    assert "Paper Note 복구는 원문 확인이 아니다" in paper_loop
    assert "현재 conversation에 사용자가 직접 첨부한 PDF가 없으면" in paper_loop
    assert "PDF 재첨부를 요청하고 Paper Reading Loop를 중단한다" in paper_loop
    assert "붙여 넣은 문장, GPT가 찾은 사본이나 Paper Note로 PDF를 대체하지 않는다" in paper_loop
    assert "논문에서 분리한 일반 prerequisite 학습은 진행할 수 있다" in paper_loop
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
    assert "반복 가능한 record shape만 정의하는 간결한 output schema" in authoring
    assert "생성된 Paper Note에 정책 문단을 복사하지 않는다" in authoring
    assert "Template의 placeholder는 실제 항목으로 교체" in authoring
    assert "별도 evidence status 필드를 추가하지 않고" in authoring
    assert "저장 전에 사용자의 짧은 자기 설명을 한 번 요청한다" not in authoring
    assert "## 2. 첨부 PDF에서 논문 identity를 확인한다" in authoring
    assert "PDF 첨부 여부와 접근 가능성은 영구 상태가 아니라" in authoring
    assert "PDF access" not in authoring
    assert "임시 경로나 과거 conversation의 attachment URL을 영구 경로처럼 기록하지 않는다" in authoring
    assert "Paper Note의 identity가 있다는 사실 자체는 원문 접근 evidence가 아니다" in authoring
    assert "PB 기록은 사용자가 자연어로 직접 요청하거나 GPT의 PB 제안에 명시적으로 동의한 경우에만 수행한다" in tutoring
    assert "사용자의 명시적 요청이나 GPT 제안에 대한 동의 없이 prerequisite를 PB에 자동 추가하지 않는다" in tutoring
    assert "### Paper-source section의 evidence boundary" in authoring
    assert "합리적으로 추론할 수 있어도 paper fact로 작성하지 않는다" in authoring
    assert "## 8. Full-paper source synthesis와 conversation-following sections" in authoring
    architecture_authoring = authoring.split(
        "## 8. Full-paper source synthesis와 conversation-following sections", 1
    )[1].split("## 9. 사용자 선택 PB Inventory와 Bridge Audit", 1)[0]
    for required in (
        "### Section lifecycle boundary",
        EXPECTED_PAPER_SOURCE_IMMEDIATE_AUTHORING,
        "**Conversation-derived sections:** `User-Identified Limitations`, `Questions`, `Connection to My Research Direction`",
        "**Reading-completion synthesis:** `Final Summary`",
        "checkpoint evidence가 마지막 본문 section까지의 읽기 완료를 뒷받침",
        "GPT가 PDF 전체를 분석했다는 사실만으로 작성하지 않는다",
        "실제 사용자–ChatGPT 학습 대화에서 발생하고 확인된 내용만 후보",
        "PDF 전체를 분석했다는 이유로 사용자가 제기하지 않은 User-Identified Limitation, Question 또는 Research Connection을 만들지 않는다",
        "사용자의 읽기 진도에서 수집한 이해 evidence를 기다려 채우는 section이 아니다",
        "`## 3. Problem`, `## 4. Key Idea`, `## 5. Architecture`, `## 6. Method`, `## 7. Experiments`, `## 8. Results`, `## 9. Trade-offs`와 `Paper-Reported Limitations`",
        "여덟 영역의 초안을 바로 작성한다",
        "사용자의 실제 읽기 범위나 이해 evidence로 승격하지 않는다",
        "Overview/review paper",
        "서로 다른 구성, 동작 또는 trade-off를 갖는 figure·subfigure",
        "Figure가 없어도 이름이 붙은 새로운 circuit 또는 structure",
        "Result plot, dataset 예시와 배경 설명용 figure",
        "Operation Overview",
        "Method는 Architecture의 architecture family와 structure heading, 이름과 순서를 그대로 사용한다",
        "Operation은 MAC으로 한정하지 않으며 arithmetic, logic, memory",
        "일반적인 pipeline을 완성하기 위해 precharge, encoding, accumulation, sensing, conversion 또는 post-processing 단계를 임의로 추가하지 않는다",
        "Challenges / Trade-offs",
        "논문에서 언급되지 않음",
        "### Trade-offs",
        "둘의 관계를 직접 연결한 경우에만 선정한다",
        "GPT가 서로 떨어진 장점과 단점을 하나의 교환 관계로 조합하지 않는다",
        "### Paper-Reported Limitations",
        "단순한 Gain–Cost 관계이거나 Trade-offs에 같은 내용이 있으면 제외",
        "`challenge`라고 표현했더라도 제한되는 capability 또는 applicability를 설명하지 않았다면 Limitation으로 승격하지 않는다",
        "### User-Identified Limitations",
        "이 subsection은 사용자의 학습과 대화를 따라 업데이트한다",
        "논문을 처음 받았을 때 자동 생성하지 않는다",
        "단순한 질문이나 GPT의 correction은 limitation으로 확정하지 않고",
        "학습 세션을 마무리할 때",
        "### Questions",
        "Questions는 full-paper source synthesis 영역이 아니라 실제 사용자–ChatGPT 학습 대화를 source로 삼는 지연 업데이트 영역",
        "질문의 답을 확인할 때 Paper 근거를 사용할 수 있지만, 질문 후보 자체는 대화에서 발생해야 한다",
        "**Origin Gate:**",
        "**Paper Grounding Gate:**",
        "**Learning Value Gate:**",
        "**Persistence Gate:**",
        "**Deduplication Gate:**",
        "GPT가 제안만 한 질문도 제외",
        "§12의 tutoring verification 질문도",
        "이해를 위한 질문`, `비판적 질문`, `후속 연구 질문",
        "`해결 과정`, `해결하며 알게 된 내용`, `해결 상태`, `해결하지 못한 부분`",
        "`resolved`: 질문의 핵심 답",
        "`partially-resolved`:",
        "`unresolved`:",
        "GPT 설명만으로 사용자의 이해가 확인되었다고 기록하지 않는다",
        "대화에서 해결 과정이나 사용자 해석을 확인할 수 없는 field",
        "placeholder record를 만들지 않고 `선정된 질문 없음`",
        "기존 질문의 후속 대화가 생기면 원래 질문과 이전 해결 이력을 보존",
        "### Connection to My Research Direction",
        "Paper를 처음 받았을 때 자동으로 작성하지 않으며",
        "Research Connection Inventory",
        "**User-Origin Gate:**",
        "**Paper-Anchor Gate:**",
        "**Mechanism Gate:**",
        "**Directional-Value Gate:**",
        "**Non-Duplication Gate:**",
        "Questions는 알아내야 할 epistemic gap과 그 해결 상태를 기록한다",
        "이 논문이 사용자 연구 방향에서 수행하는 역할",
        "단순한 흥미 표현",
        "`사용자가 표현한 research interest 또는 goal`",
        "새 Paper Note에서 통과한 connection이 없으면 `확인된 연구 연결 없음`",
        "기존 Paper Note에서 이번 세션에 새로운 connection이 없으면 기존 기록을 그대로 보존",
        "새 connection, 기존 connection 갱신, 제외 후보와 제외 이유를 저장안에 보여 준 뒤 사용자 승인 후에만",
        "### Final Summary",
        "Final Summary는 full-paper source synthesis로 미리 채우는 section도, 각 학습 세션에서 부분적으로 누적하는 section도 아니다",
        "사용자가 현재 논문 본문을 끝까지 읽었다고 명시했다",
        "Reading Checkpoint, Resume Point와 Reading Session History",
        "Final Summary에 포함할 Paper claim을 현재 conversation의 첨부 PDF에서 직접 확인",
        "Final Summary 전체를 `아직 분석하지 않음`",
        "full-paper source synthesis로 작성했더라도 Final Summary 작성 조건을 충족한 것이 아니다",
        "`Main Claim / Result and Supporting Evidence`",
        "primary claim 또는 result 하나만 선정",
        "대표 evidence 또는 synthesis basis를 1~3개",
        "baseline, workload, dataset, precision, array size, technology, measured/simulated 여부",
        "Claim의 범위를 evidence보다 넓히거나",
        "Overview/review paper는 신규 실험 결과를 만들어 넣지 않고",
        "Detailed Results는 주요 figure, table, metric과 조건을 보존하는 전체 evidence inventory",
        "Final Summary는 이를 복사하지 않고 primary claim 하나와 가장 대표적인 support만 압축",
        "`내가 기억할 한 문장`이 사용자 대화에서 확인되지 않았다면 GPT가 대신 만들지 않고 `대화에서 확인되지 않음`",
        "완독은 reading coverage evidence일 뿐",
    ):
        assert required in architecture_authoring, required
    assert "## 9. 사용자 선택 PB Inventory와 Bridge Audit" in authoring
    assert "마지막으로 저장된 checkpoint 이후 현재 conversation" in authoring
    assert "새로운 고정 section이나 evidence status field를 추가하지 않는다" in authoring
    assert "사용자가 명시적으로 선택한 개념만 PB Inventory에 넣었는가?" in authoring
    assert "일반적인 Paper Note 저장 승인을 지정되지 않은 PB 추가 승인으로 확대하지 않았는가?" in authoring
    bridge_audit = authoring.split(
        "## 9. 사용자 선택 PB Inventory와 Bridge Audit", 1
    )[1].split("## 10. 저장 전 점검", 1)[0]
    for required in (
        "사용자가 `PB`, `Prerequisite Bridge`, `선수지식` 등으로 남겨 달라고",
        "GPT가 PB 기록을 제안한 뒤 사용자가 명시적으로 동의한 개념",
        "사용자가 동의하기 전에는 PB Inventory나 저장안에 넣지 않는다",
        "질문한 것, GPT가 개념을 설명한 것, 중요한 오해를 correction한 것",
        "일반적인 `Paper Note를 저장해줘` 또는 checkpoint 저장 승인",
        "Reference deep-dive candidate",
        "기존 `Questions` 또는 관련 분석 section에만 자연어로 보존한다",
        "사용자가 직접 선택한 PB:",
        "GPT 제안 후 승인된 PB:",
    ):
        assert required in bridge_audit
    for removed in (
        "Architecture, Method, Questions에 내용이 있다는 이유로 Bridge 반영을 생략하지 않는다",
        "Inventory의 각 후보가 Bridge 신규 추가",
        "누락을 보완한 뒤에만",
    ):
        assert removed not in authoring

    paper_template = (ROOT / "templates/paper-note.md").read_text(encoding="utf-8")
    assert "Prerequisite Inventory" not in paper_template
    assert "Prerequisite Bridge audit" not in paper_template

    assert "사용자가 직접 PB 기록을 요청했거나 GPT의 PB 제안에 명시적으로 동의한 개념만" in entrypoint
    assert "질문·설명·correction 또는 reference 후보가 있었다는 이유만으로 자동 추가하지 않으며" in entrypoint
    assert "일반적인 Paper Note 저장 승인을 지정되지 않은 PB 항목의 추가 승인으로 확대하지 않는다" in entrypoint
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


def assert_delta_checkpoint_contract() -> None:
    delta = {
        "resume_point": "Section 4 / PDF p.7의 첫 문장부터 재개한다.",
        "reading_session_history": {
            "date": "2026-08-28",
            "read_range": "Section 3.2까지 읽음",
            "understood": "partial sum 이동을 사용자 언어로 설명함",
            "questions": "선정된 질문 없음",
            "bridge_changes": "변경 없음",
            "ending_resume_point": "Section 4 / PDF p.7의 첫 문장",
        },
        "user_analysis_evidence": ["“partial sum은 local buffer를 거쳐 이동한다.”"],
        "prerequisite_bridge": {
            "resolved_upsert": [
                {
                    "concept": "Partial sum",
                    "location": "Section 3.2",
                    "reason": "dataflow를 이해하기 위해 필요",
                    "definition": "부분 곱을 누적하는 중간 결과",
                    "user_understanding": "사용자가 자기 언어로 설명함",
                }
            ],
            "tracked_upsert": [
                {
                    "concept": "NoC fundamentals",
                    "status": "studying",
                    "reason": "tile 간 이동을 이해하기 위해 필요",
                    "sufficient_criterion": "routing과 flow control의 차이를 설명함",
                    "learning_logs": [
                        "learning-logs/2026/08/2026-08-28-noc-fundamentals.md"
                    ],
                }
            ],
        },
        "user_identified_limitations_upsert": [
            {
                "title": "Inter-tile movement overhead",
                "limitation": "tile 간 partial sum 이동이 병목이 될 수 있음",
                "related_architecture_method": "Figure 4 tiled accelerator",
                "user_basis": "local accumulation 이후 global 이동 경로",
                "paper_direct": "Section 3.2에서 계층적 이동을 설명함",
                "needs_confirmation": "정량적 overhead는 추가 확인 필요",
            }
        ],
        "questions_upsert": [
            {
                "category": "understanding",
                "title": "Partial sum movement",
                "user_question": "partial sum은 어디에서 합쳐지는가?",
                "context": "Section 3.2 / Figure 4",
                "selection_reason": "dataflow 이해에 직접 필요",
                "resolution_process": "Figure와 연결 본문을 함께 확인함",
                "learned": "local buffer와 global accumulation을 구분함",
                "resolution_status": "partially-resolved",
                "unresolved": "NoC arbitration 방식",
                "evidence": {
                    "paper_direct": "Section 3.2의 계층적 accumulation 설명",
                    "gpt_supplementary": "NoC의 일반 역할 설명",
                    "user_interpretation": "이동량이 병목 후보라는 사용자 해석",
                },
            }
        ],
        "research_connections_upsert": [
            {
                "title": "Data movement-aware PIM",
                "user_interest": "PIM 내부 이동 비용을 연구하고 싶음",
                "paper_element": "hierarchical partial sum accumulation",
                "evidence_location": "Section 3.2 / Figure 4",
                "connection": "연산 위치와 이동량의 관계를 비교할 수 있음",
                "role": "후속 비교 논문의 기준점",
                "questions_limitations_relation": "Partial sum movement 질문과 연결",
                "boundary": "정량 결과는 아직 확인되지 않음",
                "future_use": "research framing",
            }
        ],
    }
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        target = root / "paper-notes/foundational/2026-08-27-example-accelerator.md"
        target.parent.mkdir(parents=True)
        learning_log = root / "learning-logs/2026/08/2026-08-28-noc-fundamentals.md"
        learning_log.parent.mkdir(parents=True)
        learning_log.write_text("# stored Learning Log\n", encoding="utf-8")
        original = ingest.set_checkpoint_recorded_at(note(), "2026-08-27T10:20:30Z")
        target.write_text(original, encoding="utf-8")
        original_sections = ingest.parse_sections(original)
        sha = ingest.git_blob_sha(target.read_bytes())

        path, operation, timestamp = ingest.ingest(delta_payload(delta, sha), root)
        assert path == target.relative_to(root).as_posix()
        assert operation == "checkpoint-update"
        assert timestamp == "2026-08-28T01:02:03Z"
        stored = target.read_text(encoding="utf-8")
        assert "- Resume Point: Section 4 / PDF p.7의 첫 문장부터 재개한다." in stored
        assert "### 2026-08-28" in stored
        assert "- 읽은 범위: Section 3.2까지 읽음" in stored
        assert "> “partial sum은 local buffer를 거쳐 이동한다.”" in stored
        assert "#### Partial sum" in stored
        assert "- 실제 정의: 부분 곱을 누적하는 중간 결과" in stored
        assert "#### NoC fundamentals" in stored
        assert "- Status: studying" in stored
        assert "`learning-logs/2026/08/2026-08-28-noc-fundamentals.md`" in stored
        assert "#### Inter-tile movement overhead" in stored
        assert "#### Partial sum movement" in stored
        assert "- 해결 상태: partially-resolved" in stored
        assert "### Data movement-aware PIM" in stored
        assert "- Checkpoint recorded at: 2026-08-28T01:02:03Z" in stored

        stored_sections = ingest.parse_sections(stored)
        for heading in (
            "## 3. Problem",
            "## 4. Key Idea",
            "## 5. Architecture",
            "## 6. Method",
            "## 13. Final Summary",
        ):
            assert stored_sections[heading] == original_sections[heading]
        original_paper_limits = original_sections["## 10. Limitations"].split(
            "### User-Identified Limitations", 1
        )[0]
        stored_paper_limits = stored_sections["## 10. Limitations"].split(
            "### User-Identified Limitations", 1
        )[0]
        assert stored_paper_limits == original_paper_limits

        follow_up = json.loads(json.dumps(delta))
        follow_up["reading_session_history"]["date"] = "2026-08-29"
        follow_up["prerequisite_bridge"]["tracked_upsert"][0]["status"] = (
            "sufficient-for-paper"
        )
        follow_up["prerequisite_bridge"]["tracked_upsert"][0][
            "sufficient_criterion"
        ] = "routing과 flow control을 사용자 언어로 설명함"
        follow_up["questions_upsert"][0]["resolution_status"] = "resolved"
        follow_up["questions_upsert"][0]["unresolved"] = "해당 없음"
        current_sha = ingest.git_blob_sha(target.read_bytes())
        ingest.ingest(
            delta_payload(
                follow_up, current_sha, created_at="2026-08-29T01:02:03Z"
            ),
            root,
        )
        followed = target.read_text(encoding="utf-8")
        assert followed.count("#### NoC fundamentals") == 1
        assert "- Status: sufficient-for-paper" in followed
        assert "- 이 논문에 충분한 기준: routing과 flow control을 사용자 언어로 설명함" in followed
        assert followed.count("#### Inter-tile movement overhead") == 1
        assert followed.count("#### Partial sum movement") == 1
        assert followed.count("### Data movement-aware PIM") == 1
        assert "- 해결 상태: resolved" in followed

        expect_error(
            lambda: ingest.validate_payload(delta_payload(delta, sha), root),
            "paper-note-validation-error",
        )

        invalid = dict(delta)
        invalid["unexpected"] = "value"
        current_sha = ingest.git_blob_sha(target.read_bytes())
        expect_error(
            lambda: ingest.validate_payload(delta_payload(invalid, current_sha), root),
            "invalid-delta",
        )


def assert_bridge_validation() -> None:
    resolved_concept = """
### 논문 안에서 해결한 선수지식

#### Readout margin

- 등장 위치: Section III-A
- 논문에서 필요한 이유: sensing state 구분을 이해하기 위해 필요
- 실제 정의: 서로 다른 sensing state의 출력 사이에 확보되는 구분 간격
- 사용자의 이해: AI 설명을 들었고 자기 설명은 아직 확인하지 않음

### 별도로 이어가는 선수지식

- 없음
"""
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
        ingest.validate_payload(payload(note(resolved_concept)), root)

        missing_definition = resolved_concept.replace(
            "- 실제 정의: 서로 다른 sensing state의 출력 사이에 확보되는 구분 간격\n",
            "",
            1,
        )
        expect_error(
            lambda: ingest.validate_payload(payload(note(missing_definition)), root),
            "missing-resolved-bridge-field",
        )

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


def assert_fenced_code_is_not_document_structure() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        metadata_example = note().replace(
            "## 6. Method",
            """````markdown
## Metadata
- Title: This is an example, not Paper Note metadata
```python
## 1. Reading Checkpoint
```
````

## 6. Method""",
            1,
        )
        ingest.validate_payload(payload(metadata_example), root)

        bridge_with_example_then_invalid_concept = """
### 논문 안에서 해결한 선수지식

- 없음

### 별도로 이어가는 선수지식

```text
## Example only
#### Example prerequisite
- Status: paused
```

#### CNN

- Status: studying
- 논문에서 필요한 이유: dataflow 이해
- 이 논문에 충분한 기준: convolution mapping 설명
- Learning Logs:
  - 없음
"""
        expect_error(
            lambda: ingest.validate_payload(
                payload(note(bridge_with_example_then_invalid_concept)), root
            ),
            "studying-bridge-without-learning-log",
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
    assert_delta_checkpoint_contract()
    assert_bridge_validation()
    assert_identity_and_checkpoint_validation()
    assert_envelope_contract()
    assert_fenced_code_is_not_document_structure()
    assert_cli_report()
    print("All Paper Note ingest tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
