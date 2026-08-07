# 학습 기록: Custom GPT와 GitHub 연동 (Custom GPT–GitHub Integration)

## Metadata

- Date: 2026-08-07
- Topic: Custom GPT–GitHub Integration
- Status: working
- Source: conversation
- Last updated: 2026-08-07

## 1. 오늘 공부한 목적

아직 기록되지 않음

## 2. 오늘 이해한 내용

- Custom GPT의 Actions뉼 이용하면 외부 API를 호출할 수 있다.
- GitHub Fine-grained Personal Access Token을 이용해 특정 저장소에만 권한을 줄 수 있다.
- GitHub Contents API를 통해 파일을 읽고 생성하거나 수정할 수 있다.
- GitHub API에 파일 내용을 보낼 때 `content`는 Base64로 인코딩되어야 한다.
- 기존 파일을 수정할 때는 먼저 파일을 읽고 현재 SHA를 받아야 한다.

## 3. 핵심 개념

- **Custom GPT Actions**: Custom GPT가 정의된 API 인터페이스를 통해 외부 서비스와 상호작용할 수 있게 하는 기능.
- **Fine-grained Personal Access Token (PAT)**: GitHub 저장소 및 권한 범위를 세밀하게 제한할 수 있는 인증 수단.
- **GitHub Contents API**: 저장소의 파일 내용을 조회하고 생성하거나 수정하는 데 사용할 수 있는 API.
- **Base64 Encoding**: GitHub Contents API에 파일 내용을 전달할 때 `content` 필드에 사용하는 인코딩 방식.
- **SHA**: 기존 파일을 수정할 때 현재 파일 버전을 식별하기 위해 필요한 값.

## 4. 내가 처음 이해한 방식

Custom GPT가 Actions뉼 통해 GitHub API를 호출하고, Fine-grained PAT으로 특정 저장소에 대한 권한을 제한한 뒤, Contents API를 이용해 Markdown 파일을 읽거나 생성·수정할 수 있다고 이해했다.

또핔 파일 내용을 API로 전달할 때는 Base64 인코딩이 필요하고, 기존 파일 수정 시에는 먼저 파일을 읽어 현재 SHA를 확보해야 한다고 이해했다.

## 5. 오해 또는 불확실한 부분

- Custom GPT가 언제 기존 파일을 수정하고 언제 새 파일을 만들어야 하는지에 대한 판단 기준이 아직 헷갈린다.

## 6. 수정된 이해

현재 학습 기록 관리 기준에서는 **날짜와 주제가 같은 파일이 이미 존재하는지 먼저 확인**하는 것이 핵심이다.

- 예상 경로에 파일이 없으면 새 파일을 생성한다.
- 같은 날짜와 주제의 파일이 이미 있으면 즉시 덮어쓰지 않는다.
- 기존 파일을 먼저 읽고 새로운 내용과 비교해 병합안을 만든다.
- 변경 내용을 사용자에게 설명하고 명시적인 승인을 받은 뒤, 읽어온 현재 SHA를 사용해 수정한다.

즉, “새 파일인가 수정인가”는 임의로 결정하는 것이 아니라 **정해진 파일 경로에 기존 기록이 존재하는지**를 먼저 확인하여 판단한다.

## 7. 질문

### 해결되지 않은 질문

현재 없음.

### 해결된 질문

**Q. Custom GPT는 언제 기존 파일을 수정하고 언제 새 파일을 만들어야 하는가?**

A. 먼저 날짜와 주제에 따라 예상 파일 경로를 정하고 해당 파일의 존재 여부를 확인한다. 파일이 없으면 생성하고, 이미 존재하면 기존 파일을 읽어 병합안을 만든 뒤 사용자 승인을 받아 SHA와 함께 수정한다.

## 8. AI 반도체 및 SSL 목표와의 연결

이 내용은 AI 반도체 자체의 기술 개념은 아니지만, 장기적인 연구 학습 과정을 관리하는 **Research OS의 기반 도구**와 관련된다. SRAM, DRAM, NPU, PIM/CIM 및 논문 분석 결과를 GitHub에 일관되게 축적하고 수정 이력을 관리하는 데 활용할 수 있다.

## 9. 다음 행동

1. 같은 날짜와 주제의 파일이 없는 경우 새 학습 기록이 생성되는 흐름을 확인한다.
2. 같은 파일이 이미 존재할 때 기존 내용을 읽고 SHA를 확보하는 흐름을 확인한다.
3. 기존 기록에 새 내용을 병합할 때 사용자 승인 후 수정하는 과정을 직접 확인한다.

## 10. 자기 설명 점검

- [x] 용어의 정의를 설명할 수 있다.
- [x] 구조 또는 동작 과정을 설명할 수 있다.
- [ ] 관련 개념과 비교할 수 있다.
- [ ] AI 반도체에서 왜 중요한지 설명할 수 있다.

## 사용자 원문

<details>
<summary>대화에서 제공한 원문 보기</summary>

오늘 Custom GPT와 GitHub 연동 과정을 공부했어.

내가 이해한 내용은 다음과 같아.

- Custom GPT의 Actions를 이용하면 외부 API를 호출할 수 있다.
- GitHub Fine-grained Personal Access Token을 이용해 특정 저장소에만 권한을 줄 수 있다.
- GitHub Contents API를 통해 파일을 읽고 생성하거나 수정할 수 있다.
- GitHub API에 파일 내용을 보낼 때 content는 Base64로 인코딩되어야 한다.
- 기존 파일을 수정할 때는 먼저 파일을 읽고 현재 SHA를 받아야 한다.

아직 헷갈리는 점은 Custom GPT가 언제 기존 파일을 수정하고 언제 새 파일을 만들어야 하는지에 대한 판단 기준이야.

이 내용을 오늘의 학습 기록으로 GitHub에 저장해줘.

</details>
