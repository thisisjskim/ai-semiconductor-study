# 학습 기록: SRAM Read Disturb와 Cell Stability (SRAM Read Disturb and Cell Stability)

## Metadata

- Date: 2026-08-14
- Topic: SRAM Read Disturb와 Cell Stability
- Document type: learning-log
- Domain: sram
- Roadmap stage: Stage 3 — Memory
- Status: working
- Source: conversation
- Evidence: CMOS inverter의 discharge, 6T SRAM Hold, Read Disturb, Cell NMOS와 Access NMOS의 상대적 strength를 사용자가 Q/Q̅, BL/BL̅, WL, charge, feedback, inverter trip point와 연결해 자기 말로 설명함.
- Related notes: learning-logs/2026/08/2026-08-12-register-sram-circuits.md
- Last updated: 2026-08-14

## 1. 오늘 공부한 목적

이전 Register/SRAM 회로 학습에서 남아 있던 질문을 이어서, CMOS inverter의 output voltage 변화가 실제 charge 이동과 어떻게 연결되는지 이해하고, 이를 기반으로 6T SRAM의 Hold와 Read 동작, 특히 Read Disturb와 cell stability가 왜 발생하는지 이해하는 것이 목적이었다.

## 2. 오늘 이해한 내용

### CMOS inverter의 discharge

Vin이 1로 바뀌면 PMOS는 OFF되고 NMOS는 ON된다. 이때 Vout node에서 NMOS를 거쳐 GND로 이어지는 discharge path가 형성된다.

사용자는 이 과정을 Vout에 축적된 전하가 GND 쪽으로 빠져나가면서 Vout voltage가 낮아지는 현상으로 설명했다.

따라서 inverter의 output 변화는 단순히 logic 1과 0이 바뀌는 것으로만 보는 것이 아니라, transistor가 conduction path를 만들고 node의 charge가 변하면서 voltage가 변하는 과정으로 이해할 수 있었다.

### Cross-coupled inverter와 Hold

Q=1, Q̅=0인 상태에서 Q̅=0을 input으로 받는 inverter에서는 PMOS가 ON되어 Q를 pull-up한다.

반대쪽 inverter는 Q=1을 input으로 받아 Q̅를 낮은 상태로 유지한다.

Hold 상태에서 WL=0이 되면 access transistor가 OFF되어 bitline과 cell 내부 node가 분리된다. 이후에는 cross-coupled inverter의 feedback이 Q와 Q̅의 상태를 유지한다.

사용자는 이를 “외부 신호에는 무관해지고, feedback으로 Q=0/Q̅=1 또는 그 반대 state를 계속 유지한다”는 방식으로 설명했다.

### Read에서 bitline의 역할

처음에는 BL과 BL̅가 항상 서로 반대 값이어야 한다고 생각했다.

그러나 Read에서는 Write와 달리 값을 강제로 넣는 것이 아니라, BL과 BL̅를 같은 높은 voltage로 precharge한 뒤 cell이 어느 한쪽을 조금 discharge하는지 관찰한다.

따라서 Write에서의 “강한 bitline driver”와 Read에서의 “precharged bitline”은 역할이 다르다는 점을 구분하게 되었다.

### Read Disturb

Q=1, Q̅=0인 cell을 읽을 때 BL̅가 높은 voltage로 precharge되어 있고 WL이 켜지면, BL̅와 Q̅가 access transistor를 통해 연결된다.

Q̅는 원래 0V에 가깝지만 높은 BL̅의 영향을 받아 약간 올라갈 수 있다.

사용자는 이를 “1V가 GND 쪽으로 이동하는 경로 중간에 Q̅가 있기 때문에 Q̅가 영향을 받아 상승할 수 있다”고 설명했다.

그리고 Q̅의 상승이 너무 커지면 Q̅를 input으로 받는 inverter가 이를 잘못된 logic state로 받아들일 수 있다고 추론했다.

이 과정에서 중요한 기준은 Q̅가 정확히 1V가 되는지가 아니라 inverter trip point를 넘는지 여부라는 점을 확인했다.

### Cell NMOS와 Access NMOS의 strength

Read 중 Q̅를 높은 BL̅ 쪽으로 끌어올리는 영향과 Q̅를 GND 쪽으로 유지하려는 Cell NMOS의 pull-down이 동시에 존재한다.

사용자는 Cell NMOS가 충분히 강해야 Q̅를 GND 쪽으로 더 강하게 끌어내려 Q̅가 inverter trip point를 넘지 못하게 할 수 있다고 설명했다.

이로부터 Cell NMOS와 Access NMOS의 상대적인 strength가 SRAM read stability와 직접 연결된다는 점을 이해했다.

## 3. 핵심 개념

- CMOS inverter
- PMOS / NMOS
- Pull-up / Pull-down
- Node charge와 discharge
- Cross-coupled inverter
- Positive feedback
- 6T SRAM
- Word Line (WL)
- Bit Line (BL / BL̅)
- Access transistor
- Hold
- Read precharge
- Read Disturb
- Inverter trip point
- Cell stability
- Cell NMOS / Access NMOS strength

## 4. 내가 처음 이해한 방식

- Vin이 1로 바뀌면 PMOS가 OFF되고 NMOS가 ON되어 Vout의 전하가 GND 쪽으로 이동하면서 Vout이 0이 된다고 이해했다.
- Q=1을 유지하는 transistor는 Q̅=0을 input으로 받는 inverter의 PMOS라고 설명했다.
- Write 과정에서는 현재 Q가 1인 쪽이 더 큰 영향을 받을 것이라고 추측했지만 확신하지 못했다.
- BL과 BL̅는 원래 항상 서로 반대 값이어야 하는 것 아닌가 하는 생각이 있었다.
- bitline이 cell보다 “강하다”는 설명을 들은 뒤에는 Read 중 bitline voltage가 어떻게 떨어질 수 있는지가 혼란스러웠다.

## 5. 오해 또는 불확실한 부분

### Read에서도 BL과 BL̅가 서로 반대여야 한다는 생각

Write에서 사용하는 complementary BL/BL̅ 상태를 Read에도 그대로 적용해서 생각했다.

Read에서는 두 bitline을 먼저 같은 high voltage로 precharge할 수 있다는 점이 처음에는 명확하지 않았다.

### “강한 bitline”과 Read discharge의 충돌

Write에서는 bitline driver가 cell을 뒤집을 정도로 강하게 drive한다는 설명을 Read에도 동일하게 적용했다.

그 결과 bitline이 강하게 1로 유지된다면 왜 Read 중 voltage가 떨어지는지 의문이 생겼다.

### Q̅가 GND에 연결되어 있는데 왜 올라가는가

Q̅=0인 node가 Cell NMOS를 통해 GND 쪽에 연결되어 있는데도 높은 BL̅ 때문에 Q̅가 상승할 수 있다는 점이 처음에는 직관적으로 명확하지 않았다.

### Transistor strength의 정확한 의미

Cell NMOS가 Access NMOS보다 “강해야 한다”는 이유는 이해했지만, transistor가 강하다는 말의 정확한 회로적 의미와 이를 어떻게 설계하는지는 추가 질문으로 남았다.

## 6. 수정된 이해

- Write와 Read에서 bitline의 역할은 다르다.
  - Write에서는 외부 driver가 BL/BL̅를 강하게 구동해 cell state를 변경한다.
  - Read에서는 BL과 BL̅를 precharge한 뒤 어느 쪽이 discharge되는지를 감지한다.

- 따라서 Read 시작 시 BL과 BL̅가 모두 high인 것은 정상이다.

- Q̅=0인 node도 access transistor를 통해 높은 BL̅와 연결되면 어느 정도 상승할 수 있다.

- 이 상승 자체가 바로 오류를 의미하는 것은 아니다. Q̅가 inverter trip point를 넘을 정도로 올라가는 것이 위험하다.

- Cell NMOS가 Access NMOS의 영향보다 충분히 강하면 Q̅를 GND 쪽으로 유지해 trip point를 넘지 않도록 할 수 있다.

- 따라서 Read Disturb와 cell stability는 단순히 bitline voltage만의 문제가 아니라, access transistor와 cell pull-down transistor의 상대적인 strength와도 연결된다.

## 7. 질문

### 해결되지 않은 질문

- Cell Ratio를 transistor sizing 또는 수식 관점에서 정확히 어떻게 정의하는가?
- Sense Amplifier는 BL과 BL̅ 사이의 작은 voltage difference를 어떻게 증폭하는가?
- SRAM Read Margin과 Static Noise Margin은 어떻게 정의되고 평가되는가?
- “강한 transistor”를 만드는 방법과 그 의미를 사용자가 자신의 언어로 다시 설명할 수 있는지는 아직 확인되지 않았다.

### 해결된 질문

- Vin이 1로 바뀌면 왜 CMOS inverter의 Vout이 내려가는가?
  - PMOS가 OFF되고 NMOS가 ON되어 Vout에서 GND로 discharge path가 열리고, Vout node의 charge가 줄어들기 때문이다.

- Hold 상태에서 왜 SRAM의 값이 유지되는가?
  - WL=0으로 access transistor가 OFF되어 bitline과 cell이 분리되고, cross-coupled inverter의 feedback이 기존 Q/Q̅ 상태를 유지하기 때문이다.

- Read에서 BL과 BL̅가 왜 둘 다 high로 시작할 수 있는가?
  - Read는 외부 값을 cell에 쓰는 과정이 아니라, 두 bitline을 precharge한 뒤 어느 쪽이 discharge되는지 비교하는 과정이기 때문이다.

- Read Disturb는 왜 발생할 수 있는가?
  - 높은 precharged bitline이 access transistor를 통해 내부 low node를 끌어올릴 수 있으며, 그 상승이 inverter trip point를 넘으면 저장 state가 불안정해질 수 있기 때문이다.

- 왜 Cell NMOS가 Access NMOS보다 충분히 강해야 하는가?
  - Read 중 low storage node를 GND 방향으로 유지하여 inverter trip point를 넘지 않게 하기 위해서이다.

## 8. AI 반도체 및 SSL 목표와의 연결

이번 대화에서는 SRAM 회로 동작 자체에 대한 이해가 중심이었다.

SRAM이 AI accelerator의 on-chip memory에 사용되며 data movement를 줄이는 데 중요하다는 연결은 설명되었지만, 사용자가 이 중요성을 자기 말로 다시 설명하거나 적용한 evidence는 아직 없다.

따라서 AI 반도체와의 연결은 다음 학습에서 memory hierarchy 또는 NPU local buffer와 연결해 다시 확인할 필요가 있다.

## 9. 다음 행동

1. Cell Ratio를 transistor sizing 관점에서 학습하고, Cell NMOS와 Access NMOS의 strength 관계를 다시 자기 말로 설명한다.
2. Sense Amplifier가 precharged BL/BL̅의 작은 differential voltage를 읽는 원리를 학습한다.
3. Read Margin / Static Noise Margin을 Read Disturb와 연결해 이해한다.

## 10. 자기 설명 점검

- [ ] 용어의 정의를 설명할 수 있다.
- [x] 구조 또는 동작 과정을 설명할 수 있다.
- [ ] 관련 개념과 비교할 수 있다.
- [ ] AI 반도체에서 왜 중요한지 설명할 수 있다.

## 사용자 원문

<details>
<summary>대화에서 제공한 원문 보기</summary>

> “vin을 1로 바꾸면 PMOS는 off, NMOS는 on이 되면서, GND - NMOS - vout(capacitor)이 연결됩니다. 따라서 Vout에 축적된 전하가 GND로 이동하게 되면서 Vout이 0이 됩니다.”

> “Q를 1로 유지시키는 transistor는 PMOS야. 애초에 PMOS가 pull-up을 하기도 하고, 오른쪽 inverter에서 Qbar을 받고 있다는 것은 결국 왼쪽 인버터의 input이 0이라는 의미이기도 하고, input이 0일때는 PMOS가 활성화되기 때문”

> “Q가 강하게 받지 않을까? 왜냐하면 state가 1로 되어있기 때문. 사실 잘 모르겠음”

> “WL=0이 되면 access transistor가 off가 되어, bitline과 cross-inverter가 연결되지 않음. 그래서 외부의 신호에는 무관해져. 그리고 write 0 가 되어 Q=0 , Qbar=1이 되면 cross-coupled inverter 내의 feedback 현상으로 인하여, Q=0, Qbar=1인 state를 계속해서 유지하려고 하는 현상이 발생하게 됨.”

> “일단 BL과 BL bar는 서로 달라야하는거 아니야? 여기서 살짝 헷갈림. 그리고 bitline이 가장 강하다고 했는데, bitline의 전압이 떨어질 수 있는거야?”

> “Read를 하게 되면 BL bar에 1V의 전압을 주고, 그 1V가 살짝 떨어지는 것을 감지하여, 0or1임을 확인하는 거잖아. 그런데 이제 Qbar = 0V 를 read하기 위해 1V를 주게 되면 그 1V가 GND로 이동하게 되면서 자연스럽게 그 사이에 있는 Qbar에 영향을 주어, Qbar가 상승하게 될 수 있다는 것이지. 그리고 이 상승이 과도하면 Qbar를 input으로 받는 inverter에게 잘못된 정보(1)를 주게 될 수도 있다는 위험이 있다는 말을 하고 있는거 아니야?”

> “Cell NMOS의 힘이 더 커야지, Qbar을 GND로 끌어내리는 힘이 강해서 Qbar가 inverter trip point를 넘지 못하게 한다는 뜻이잖아.”

> “혹시 추가로 궁금한게 NMOS를 강하게 설계한다는 뜻이야. 어떻게 하면 강하게 설계할 수 있고, 강하다는 의미가 정확히 무엇인지 너무 자세하게는 말고 어느정도 직관적으로 알려주면 좋겠어.”

</details>
