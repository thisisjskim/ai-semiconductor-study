# Custom GPT Setup and Verification

## 등록

- Instructions: `system/CUSTOM_GPT_INSTRUCTIONS.md`의 본문 전체
- Actions: `system/ACTION_SCHEMA.yaml`
- Authentication: API Key / Bearer / repository-scoped fine-grained PAT
- PAT permissions: Contents read-only, Issues read/write, Metadata read-only
- Knowledge: 변경되는 repository 문서의 사본을 업로드하지 않음

Instructions나 Action schema를 바꾼 뒤에는 반드시 **업데이트**를 누르고 완전히 새 대화를 만든다. 기존 대화는 변경 전 tool context를 유지할 수 있으므로 검증에 사용하지 않는다.

## 검증 순서

### 1. Action 단위 테스트

GPT 편집기의 `getStudyPath` 테스트에서 다음 입력을 사용한다.

```text
path: state/CURRENT_LEARNING_CONTEXT.md
ref: main
```

HTTP 200과 `content`, `encoding: base64`, `path`, `sha`가 반환되어야 한다.

### 2. 명시적 호출 테스트

새 대화에서 다음을 입력한다.

```text
getStudyPath Action으로 state/CURRENT_LEARNING_CONTEXT.md를 main에서 읽고 Current Topic만 알려줘.
```

기대 결과는 `Register와 SRAM 회로 기초`다. GitHub 웹 검색으로 대신 읽었다는 답변은 실패다.

### 3. 자연어 routing 테스트

다시 완전히 새 대화를 만들어 다음 한 문장만 입력한다.

```text
이전 공부를 이어나가자.
```

성공 기준:

- 답변 전에 `getStudyPath(path="state/CURRENT_LEARNING_CONTEXT.md", ref="main")`를 실제로 한 번 호출함
- 현재 위치를 `Register와 SRAM 회로 기초`로 복구함
- Current Learning Context의 Next Action 또는 Open Questions를 근거로 CMOS inverter의 charge/discharge 또는 6T SRAM 학습을 즉시 시작함
- 최신 실제 Learning Log는 정확한 근거가 추가로 필요할 때만 조회함
- 파일을 붙여 달라고 요청하지 않음
- 사용자에게 파일별 Action 호출을 요청하지 않음
- 연속 Action을 호출할 수 없다는 이유로 학습 시작을 거부하지 않음
- 실제 오류 없이 Action이 없다고 주장하지 않음

## 실패 분류

- Action Test가 401: PAT 또는 Bearer 인증 문제
- Action Test가 403: fine-grained PAT 권한 문제
- Action Test가 404: path, ref 또는 repository scope 문제
- Action Test는 200이지만 명시적 호출 실패: GPT 업데이트/새 대화 또는 Action 등록 문제
- 명시적 호출은 성공하지만 자연어 routing 실패: Instructions 또는 schema relevance description 문제
