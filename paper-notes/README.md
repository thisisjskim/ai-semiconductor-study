# Paper Notes

이 directory는 논문 한 편마다 하나의 living Paper Note를 보존한다. 매일 새 파일을 만들지 않고 Paper Reading Checkpoint마다 같은 파일을 갱신한다.

## 경로

```text
paper-notes/{foundational|ssl-lab|related}/YYYY-MM-DD-paper-slug.md
```

- 날짜는 Paper Note를 처음 만든 날짜이며 이후 수정해도 파일명을 바꾸지 않는다.
- 하위 directory는 첫 Paper Note를 저장할 때 Workflow가 자동 생성한다.
- 현재 읽는 논문은 파일 수정 시각이나 최신 Learning Log가 아니라 Workflow가 기록한 `Checkpoint recorded at`으로 결정한다.
- Paper Note의 상세 형식은 `templates/paper-note.md`를 따른다.

## 기록 원칙

- `Resume Point`는 다음에 다시 읽을 정확한 위치와 아직 확인할 내용을 함께 적는다.
- 논문 안에서 해결한 선수지식은 사용자의 자기 설명과 논문 속 의미를 Paper Note에 직접 기록한다.
- 별도로 이어가는 선수지식은 Learning Log 경로를 연결하며 `studying`, `paused`, `sufficient-for-paper` 중 하나로 표시한다.
- `studying`인 선수지식은 한 Paper Note에서 최대 하나만 허용한다.
- Paper Note 저장과 수정은 사용자 승인 후 Issue → GitHub Actions 경로를 사용한다.
