# 학습 기록: SRAM Cell Ratio와 SNM (SRAM Cell Ratio and Static Noise Margin)

## Metadata

- Date: 2026-08-15
- Topic: SRAM Cell Ratio와 SNM
- Document type: learning-log
- Domain: sram
- Roadmap stage: Stage 3 — Memory
- Status: working
- Source: conversation
- Evidence: 사용자가 Read Disturb, transistor sizing, inverter switching threshold, SNM, Butterfly Curve의 관계를 반복적으로 자기 언어로 설명하고 오해를 수정함
- Related notes: learning-logs/2026/08/2026-08-14-sram-read-disturb-cell-stability.md
- Last updated: 2026-08-15

## 1. 오늘 공부한 목적

SRAM Read Disturb의 연장선에서 Cell Ratio를 transistor sizing 관점으로 이해하고, Pull-down NMOS·Access NMOS·Pull-up PMOS의 strength trade-off를 Read/Write 동작과 연결한다. 이어서 MOSFET threshold voltage와 CMOS inverter switching threshold를 구분하고, SNM과 Butterfly Curve가 SRAM 안정성을 어떻게 정량화하는지 이해한다.

## 2. 오늘 이해한 내용

### Cell Ratio와 Read Disturb

사용자는 Read 시 precharged Bitline과 Q=0 storage node가 Access NMOS를 통해 연결되면 Q가 올라가려 하고, Pull-down NMOS가 GND 쪽으로 Q를 유지하려 한다는 경쟁 구조를 설명했다. Pull-down NMOS가 Access NMOS보다 충분히 강해야 Q의 상승이 제한되고, inverter의 switching boundary를 넘어 state가 뒤집히는 Read Disturb를 막을 수 있다고 설명했다.

Cell Ratio가 커지면 Pull-down NMOS의 상대적인 strength가 커져 Read Disturb가 감소하고 Read Stability가 좋아진다는 점을 이해했다. 반대로 Cell Ratio를 지나치게 크게 하면 기존 state를 유지하려는 힘이 강해져 Write가 느려지거나 어려워질 수 있다는 trade-off도 설명했다.

### Write Ability와 Pull-up PMOS

초기에는 Cell NMOS가 너무 강하면 Write가 어려워진다는 관점에 집중했지만, 사용자는 스스로 "실제 write에서는 Q=1을 Q=0으로 끌어내리는 과정이 핵심이라면 Pull-up PMOS와 Access NMOS의 경쟁이 더 직접적이지 않은가"라고 문제를 제기했다.

이후 Write 시 Access NMOS가 storage node를 low bitline에 연결해 전압을 내리려 할 때 Pull-up PMOS가 VDD로 끌어올리며 기존 1을 유지하려 하므로, Access NMOS가 Pull-up PMOS보다 충분히 강해야 Write가 쉬워진다는 구조를 이해했다. 이를 Read의 `Pull-down NMOS > Access NMOS`, Write의 `Access NMOS > Pull-up PMOS`와 연결해 대표적인 sizing 방향 `Pull-down NMOS > Access NMOS > Pull-up PMOS`를 설명했다.

### MOSFET Vth와 Inverter Switching Threshold VM

사용자는 처음에 "0에서 1로 판단하는 것은 NMOS가 특정 gate voltage 이상에서 channel을 형성하기 때문이고, 그 민감도가 threshold일 것 같다"고 설명했다. 이는 개별 MOSFET의 threshold voltage Vth에 가까운 설명이었다.

이후 디지털 관점의 ON/OFF 모델과 달리 실제 CMOS inverter의 전이 영역에서는 NMOS와 PMOS가 동시에 유의미한 전류를 흘릴 수 있고, inverter switching threshold VM은 두 소자의 pull-up/pull-down strength가 균형을 이루는 동작점이라는 점으로 이해를 수정했다. 사용자는 이후 "inverter에서 VM은 MOSFET의 Vth와는 다르고, PMOS와 NMOS가 균형을 이루는 지점"이라고 자기 언어로 다시 설명했다.

### SNM과 Butterfly Curve

사용자는 SNM을 "SRAM이 noise를 견딜 수 있는 척도이며 SNM이 크면 큰 noise를 견딜 수 있다는 뜻"으로 설명했다. Hold 상태에서는 WL=0으로 Bitline과 분리되어 외부 disturb가 적으므로 Hold SNM이 Read SNM보다 크다고 설명했다.

Butterfly Curve의 최대 정사각형에 대해서는 처음에는 왜 정사각형의 한 변이 SNM을 의미하는지 이해가 부족하다고 질문했다. 이후 최대 정사각형의 크기가 안정 상태에서 불안정 경계까지의 최소 noise margin을 나타내며, 정사각형이 클수록 더 큰 교란을 견딜 수 있다는 의미로 이해했다. 사용자는 SRAM A의 SNM이 100 mV, SRAM B가 250 mV일 때 B가 더 큰 noise를 견딜 수 있으므로 더 안정적이라고 설명했다.

### Cell Ratio와 SNM 연결

사용자는 한 번 `Cell Ratio 증가 → noise 영향 감소 → SNM 감소`라고 결론을 반대로 말했지만, SNM의 정의가 "견딜 수 있는 최대 noise"라는 점을 다시 적용하여 결론을 수정했다. 최종적으로 Cell Ratio가 증가하면 Pull-down NMOS가 Q=0을 더 강하게 유지하고 Read Disturb에 의한 Q 상승을 줄이므로 불안정 경계에 도달하기 어려워지고, 결과적으로 Read SNM이 증가한다는 인과관계를 이해했다.

## 3. 핵심 개념

- 6T SRAM Read Disturb
- Cell Ratio
- Pull-down NMOS와 Access NMOS의 strength 경쟁
- Pull-up PMOS와 Access NMOS의 Write 경쟁
- 대표적인 transistor sizing 방향
- MOSFET threshold voltage (Vth)
- CMOS inverter switching threshold (VM)
- Cross-coupled inverter positive feedback
- Stable / unstable equilibrium
- Static Noise Margin (SNM)
- Hold SNM과 Read SNM
- Butterfly Curve와 최대 정사각형

## 4. 내가 처음 이해한 방식

- Cell NMOS를 크게 만들면 주로 면적이 증가하는 것이 가장 큰 문제일 것이라고 생각했다.
- Write가 어려워지는 이유를 주로 매우 강한 Cell NMOS가 Q=0을 유지하기 때문이라고 보았다.
- Inverter가 0/1을 판단하는 threshold를 NMOS가 channel을 형성하는 gate threshold와 거의 같은 개념으로 생각했다.
- Butterfly Curve의 최대 정사각형이 SNM이라는 정의는 알고 있었지만, VTC 사이의 간격과 정사각형 크기가 물리적으로 무엇을 의미하는지 명확하지 않았다.

## 5. 오해 또는 불확실한 부분

- Write Ability를 Cell NMOS 하나의 strength만으로 설명하면 불완전하며, 실제로 1→0 write 시 Pull-up PMOS와 Access NMOS의 경쟁을 직접적으로 봐야 한다.
- MOSFET Vth와 inverter VM을 같은 threshold 개념으로 보았던 부분을 수정할 필요가 있었다.
- `Cell Ratio 증가 → SNM 감소`라고 한 번 반대로 결론 내렸으며, 이는 SNM 정의를 적용하는 과정의 부호 혼동이었다.
- Butterfly Curve 내부 전체를 곧바로 "안정한 실제 SRAM state들의 영역"이라고 보는 해석은 부정확하며, 핵심은 두 VTC가 만드는 noise margin과 안정/불안정 경계 사이의 여유를 보는 것이다.

## 6. 수정된 이해

- Read 시에는 Pull-down NMOS가 Access NMOS보다 충분히 강해야 Q=0 node의 상승을 억제하고 Read Disturb를 줄일 수 있다.
- Write 시에는 Access NMOS가 Pull-up PMOS를 이겨 storage node를 충분히 낮춰야 state flip을 시작할 수 있다. Pull-down NMOS의 strength도 전체 regenerative behavior에 영향을 주지만 Write Ability의 직접적인 경쟁은 Pull-up PMOS와 Access NMOS에서 중요하다.
- MOSFET Vth는 개별 transistor 특성이고, inverter VM은 PMOS/NMOS strength와 회로 동작에 의해 정해지는 inverter의 switching point이다.
- SNM은 Cell이 견딜 수 있는 DC noise margin이며, Butterfly Curve의 최대 정사각형은 이 최소 noise margin을 기하학적으로 측정한 값이다.
- Cell Ratio가 커지면 Read Disturb가 줄어들고 더 큰 noise를 견딜 수 있으므로 Read SNM은 증가한다.

## 7. 질문

### 해결되지 않은 질문

- Sense Amplifier는 BL과 BL̅ 사이의 작은 differential voltage를 어떻게 증폭하는가?
- Differential sensing은 single-ended sensing에 비해 왜 유리한가?
- Read Margin과 SNM은 실제 회로 시뮬레이션과 측정에서 어떻게 구분되고 연결되는가?
- Process Variation과 Monte Carlo 분석은 SNM 분포를 어떻게 변화시키는가?

### 해결된 질문

- Pull-down NMOS가 Access NMOS보다 강해야 하는 이유는 무엇인가?
- Cell Ratio를 무한히 크게 만들지 않는 이유는 무엇인가?
- Write Ability에서 Pull-up PMOS와 Access NMOS의 경쟁은 왜 중요한가?
- MOSFET Vth와 inverter switching threshold VM은 어떻게 다른가?
- Hold SNM이 Read SNM보다 큰 이유는 무엇인가?
- Butterfly Curve의 최대 정사각형은 물리적으로 무엇을 의미하는가?
- Cell Ratio 증가가 Read SNM 증가로 이어지는 이유는 무엇인가?

## 8. AI 반도체 및 SSL 목표와의 연결

SRAM은 AI accelerator와 NPU의 local buffer, cache, on-chip memory에 널리 사용된다. Read Stability와 Write Ability는 대규모 SRAM array의 동작 전압, 수율, 성능, 전력에 직접 영향을 주므로, Cell Ratio와 SNM을 이해하는 것은 AI 반도체 memory subsystem을 회로 수준에서 이해하기 위한 기반이 된다.

## 9. 다음 행동

1. Sense Amplifier가 precharged BL/BL̅의 작은 differential voltage를 증폭하는 원리를 학습한다.
2. Differential sensing과 precharge가 Read latency와 noise immunity에 주는 이점을 설명한다.
3. 이후 Read Margin과 SNM을 연결하고 Process Variation에 따른 SNM 분포로 확장한다.

## 10. 자기 설명 점검

- [x] 용어의 정의를 설명할 수 있다.
- [x] 구조 또는 동작 과정을 설명할 수 있다.
- [x] 관련 개념과 비교할 수 있다.
- [x] AI 반도체에서 왜 중요한지 설명할 수 있다.

## 사용자 원문

<details>
<summary>대화에서 제공한 원문 보기</summary>

> "Cell NMOS가 Access NMOS보다 강해야 하는 이유는, Cell NMOS가 더 강해야 Q node가 GND와 강하게 연결되어 0을 유지하려고 하기 때문이다."

> "write에서는 Q=0 -> Q=1 동작보다 Q=1 -> Q=0으로 끌어내려지는 동작을 통해 반대쪽 inverter도 바뀌는 걸로 기억하고 있는데... 그러면 NMOS의 역할이 그렇게 크게 작용하는지 모르겠음."

> "inverter에서 VM은 mosfet에서의 Vth와는 달라. digital에서는 CMOS의 동작이 PMOS, NMOS가 on,off로 구별되지만 analog에서는 NMOS, PMOS 둘다 Vth를 넘겨서 작동되는 경우가 발생할 수 있고, 그 때 PMOS와 NMOS가 균형을 이루는 지점을 VM이라고 해."

> "hold SNM이 더 크지. 왜냐하면 hold되어있으면 WL=0이 되어 bitline과 분리되기 때문에, 내부가 안정한 상태를 더 잘 유지할 수 있어서..."

> "SNM은 SRAM이 noise를 견딜 수 있는 척도이며, SNM이 크다는 것은 곧 SRAM이 큰 noise를 견딜 수 있다는 뜻이야."

> "정사각형의 크기가 SRAM B에서 더 크고, 이 뜻은 SRAM B는 250mV 이상의 noise가 발생해야지 state가 변하게 되는 것이야."

> "cell ratio를 크게 하면 read를 할 때는 분명 좋아... 그렇지만 cell ratio를 무작정 크게 한다면 write를 할 때 문제가 발생해."

</details>
