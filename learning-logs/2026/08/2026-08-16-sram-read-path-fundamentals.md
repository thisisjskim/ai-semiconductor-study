# 학습 기록: SRAM Read Path 기초 (SRAM Read Path Fundamentals)

## Metadata

- Date: 2026-08-16
- Topic: SRAM Read Path Fundamentals
- Document type: learning-log
- Domain: sram
- Roadmap stage: Stage 3 — Memory
- Status: working
- Source: conversation
- Evidence: Cell Ratio, SNM, Butterfly Curve, precharge/equalization, differential sensing, Sense Amplifier와 offset까지 사용자가 자기 언어로 반복 설명하고 오해를 수정함
- Related notes: learning-logs/2026/08/2026-08-14-sram-read-disturb-cell-stability.md
- Last updated: 2026-08-16

## 1. 오늘 공부한 목적

이전 checkpoint 이후 SRAM Read Path를 회로 수준에서 확장하여, Cell Ratio와 Read Stability에서 시작해 SNM, Butterfly Curve, precharge/equalization, differential sensing, Sense Amplifier의 regeneration, mismatch와 input-referred offset까지 하나의 인과관계로 연결한다.

## 2. 오늘 이해한 내용

### Cell Ratio와 Read Stability

사용자는 Read 시 precharged Bitline이 Access NMOS를 통해 Q=0 node를 끌어올리려 하고, Pull-down NMOS가 Q를 GND 쪽으로 유지하려는 경쟁이 생긴다고 설명했다. Pull-down NMOS가 Access NMOS보다 충분히 강해야 Q의 상승을 억제하여 Read Disturb와 Cell Flip을 막을 수 있다고 이해했다.

또한 Cell Ratio를 크게 하면 Read에는 유리하지만, Pull-down strength가 지나치게 커지면 기존 state를 유지하려는 힘이 강해져 Write가 어려워질 수 있다는 trade-off를 설명했다. Write 동작에서는 특히 Access NMOS와 Pull-up PMOS의 직접적인 strength 경쟁이 중요하다는 점도 구분했다.

### MOSFET Vth와 Inverter VM

처음에는 inverter가 0/1을 판단하는 threshold를 NMOS가 channel을 형성하기 시작하는 gate threshold와 거의 같은 개념으로 생각했다. 이후 MOSFET Vth는 개별 transistor의 특성이고, inverter VM은 PMOS와 NMOS의 effective pull-up/pull-down strength가 균형을 이루는 switching point라는 점으로 이해를 수정했다.

사용자는 이후 “inverter에서 VM은 MOSFET의 Vth와는 다르고, PMOS와 NMOS가 균형을 이루는 지점”이라고 자기 말로 다시 설명했다.

### SNM과 Butterfly Curve

사용자는 SNM을 SRAM이 noise를 견딜 수 있는 척도로 설명했고, SNM이 클수록 더 큰 noise에도 state를 유지할 수 있다고 이해했다. Hold 상태에서는 WL=0으로 Bitline과 분리되어 외부 disturb가 적기 때문에 Hold SNM이 Read SNM보다 크다고 설명했다.

Butterfly Curve의 최대 정사각형이 왜 SNM을 의미하는지 처음에는 이해가 부족했지만, 이후 정사각형 크기를 안정 상태와 불안정 경계 사이의 최소 noise margin을 기하학적으로 측정하는 값으로 이해했다. 정사각형이 클수록 더 큰 교란에도 unstable boundary를 넘지 않는다고 설명했다.

### Precharge와 Equalization

사용자는 Read 전에 BL과 BL̅를 동일한 전압으로 초기화해야 이전 Read에서 남은 ΔV가 다음 Read의 판정에 영향을 주지 않는다고 설명했다. Sense Amplifier는 작은 전압차에도 민감하므로, 이전 differential residue가 남아 있으면 새 Cell이 만든 정보가 아니라 이전 state에 의해 잘못 regeneration될 수 있다는 점을 이해했다.

또한 BL과 BL̅를 high로 precharge한 뒤 Cell이 한쪽 Bitline만 조금 방전시키는 방식이, 큰 Bitline capacitance를 full swing으로 변화시키는 것보다 빠르고 효율적이라고 설명했다.

### Differential Sensing과 Sense Amplifier

사용자는 Sense Amplifier의 본질을 절대 전압 측정보다 “대칭성이 어느 방향으로 깨졌는지 판단하는 것”에 가깝다고 설명했다. SRAM Cell이 작은 ΔV를 만들고, Sense Amplifier가 cross-coupled positive feedback을 통해 그 작은 차이를 full-swing digital output으로 regeneration한다는 구조를 이해했다.

또한 SRAM Cell은 안정한 state를 유지해야 하므로 unstable equilibrium에서 멀리 있는 것이 유리한 반면, Sense Amplifier는 작은 ΔV에도 빠르게 반응해야 하므로 metastable/unstable point 근처에서 regeneration을 시작한다는 차이를 설명했다.

### Sense Amplifier Offset과 Mismatch

사용자는 실제 Sense Amplifier에서 device mismatch 때문에 너무 작은 ΔV는 잘못된 방향으로 증폭될 수 있다고 추론했다. 이후 W/L, Vth, parasitic 등의 차이가 두 branch의 effective strength를 다르게 만들고, 이를 입력 전압 차이로 환산한 것이 input-referred offset이라는 점을 이해했다.

Sense Amp를 너무 일찍 enable하면 ΔV가 offset과 noise margin보다 작아 Read Error가 증가할 수 있고, 너무 늦게 enable하면 Bitline capacitance 때문에 Read Latency와 dynamic energy가 증가한다는 timing trade-off도 설명했다.

## 3. 핵심 개념

- 6T SRAM Read Disturb
- Cell Ratio와 transistor sizing
- Pull-down NMOS vs Access NMOS
- Access NMOS vs Pull-up PMOS
- MOSFET threshold voltage (Vth)
- CMOS inverter switching threshold (VM)
- Static Noise Margin (SNM)
- Hold SNM vs Read SNM
- Butterfly Curve
- Stable / unstable equilibrium
- Bitline precharge
- Bitline equalization
- Differential sensing
- Sense Amplifier regeneration
- Device mismatch
- Effective strength
- Input-referred offset
- Sense Amp enable timing

## 4. 내가 처음 이해한 방식

- Cell Ratio를 지나치게 키우는 문제를 주로 transistor width 증가와 area 문제로 먼저 생각했다.
- Write가 어려워지는 이유를 주로 강한 Cell NMOS가 Q=0을 계속 유지하기 때문이라고 보았다.
- Inverter switching threshold를 MOSFET의 channel 형성 threshold와 거의 같은 개념으로 생각했다.
- Butterfly Curve 안의 최대 정사각형이 SNM이라는 정의는 알고 있었지만, VTC 사이 간격의 물리적 의미와 정사각형이 왜 noise margin을 나타내는지는 명확하지 않았다.
- Precharge는 Read를 시작한다는 것을 확실히 표시하고 noise를 방지하기 위한 동작이라고 처음 추측했다.
- Sense Amplifier가 1V에서 조금 떨어진 값을 곧바로 0으로 “인식”하는 것처럼 생각했다.

## 5. 오해 또는 불확실한 부분

- Cell NMOS strength만으로 Write Ability를 설명하면 불완전하며, 실제 1→0 write에서는 Access NMOS와 Pull-up PMOS의 경쟁이 더 직접적이다.
- MOSFET Vth와 inverter VM은 서로 다른 개념이다.
- `Cell Ratio 증가 → SNM 감소`라고 한 번 결론을 반대로 말했으나, SNM이 “견딜 수 있는 최대 noise”라는 정의를 다시 적용해 수정했다.
- Butterfly Curve 내부 전체를 곧바로 “실제 안정 state 영역”이라고 보는 해석은 부정확하다. 핵심은 두 VTC가 형성하는 noise margin과 stable/unstable boundary 사이의 여유다.
- Precharge의 목적은 Read 여부를 표시하는 것이 아니라, 매 Read를 동일한 초기조건과 ΔV=0 상태에서 시작하게 하는 것이다.
- Sense Amplifier는 절대 전압이 특정 threshold를 넘었는지 보는 장치라기보다 두 branch의 작은 differential signal을 positive feedback으로 증폭하는 회로다.

## 6. 수정된 이해

- Read 시 Pull-down NMOS가 Access NMOS보다 충분히 강해야 Q=0 node 상승을 억제하고 Read Disturb를 줄일 수 있다.
- Cell Ratio가 증가하면 Read Disturb가 감소하고 더 큰 noise를 견딜 수 있으므로 Read SNM은 증가한다.
- Write에서는 Access NMOS가 Pull-up PMOS를 이겨 storage node를 충분히 낮출 수 있어야 state flip이 시작된다.
- MOSFET Vth는 개별 소자의 conduction 특성이고, inverter VM은 두 branch의 strength 균형에 의해 정해지는 switching point이다.
- Butterfly Curve의 최대 정사각형은 안정 상태에서 불안정 경계까지의 최소 DC noise margin을 나타낸다.
- Precharge와 Equalization은 BL과 BL̅를 같은 초기전압으로 맞춰 이전 differential residue를 제거하고 새 Cell이 만든 ΔV만 Sense Amplifier에 전달하기 위한 과정이다.
- Sense Amplifier는 BL/BL̅의 절대값보다 어느 쪽이 더 높고 낮은지를 판정하며, cross-coupled positive feedback으로 작은 ΔV를 full swing으로 regeneration한다.
- Device mismatch는 branch 간 effective strength 차이를 만들고, 이를 입력 전압 차이로 환산한 값이 input-referred offset이다. 따라서 실제 sensing에는 offset보다 충분히 큰 ΔV와 추가 noise margin이 필요하다.

## 7. 질문

### 해결되지 않은 질문

- SRAM Write Path에서 실제 state flip은 어떤 node의 pull-down을 기점으로 시작되는가?
- Write Margin은 어떤 방식으로 정의하고 측정하는가?
- Write Failure와 Write Assist 기법은 Cell Ratio 및 Pull-up Ratio와 어떻게 연결되는가?
- Process Variation과 Monte Carlo 분석에서 SNM 및 Sense Amp Offset 분포를 어떻게 해석하는가?

### 해결된 질문

- Pull-down NMOS가 Access NMOS보다 강해야 하는 이유는 무엇인가?
- Cell Ratio를 무한히 크게 만들지 않는 이유는 무엇인가?
- MOSFET Vth와 inverter switching threshold VM은 어떻게 다른가?
- Hold SNM이 Read SNM보다 큰 이유는 무엇인가?
- Butterfly Curve 최대 정사각형의 물리적 의미는 무엇인가?
- Cell Ratio 증가가 Read SNM 증가로 이어지는 이유는 무엇인가?
- 왜 BL과 BL̅를 precharge 및 equalize해야 하는가?
- 왜 Bitline을 full discharge시키지 않고 작은 ΔV만 만든 뒤 Sense Amplifier를 사용하는가?
- Sense Amplifier가 작은 differential signal을 어떻게 full-swing output으로 만드는가?
- Sense Amplifier offset과 device mismatch는 왜 Read Error를 유발할 수 있는가?

## 8. AI 반도체 및 SSL 목표와의 연결

SRAM은 AI accelerator와 NPU의 local buffer, cache, on-chip memory에서 핵심적인 비중을 차지한다. Read Stability, Bitline Swing, Sense Amplifier timing과 offset은 SRAM array의 latency, energy, yield에 직접 연결되므로, 이 Read Path를 회로 수준에서 이해하는 것은 AI 반도체 memory subsystem을 설계하고 논문을 해석하기 위한 기반이 된다.

## 9. 다음 행동

1. SRAM Write Path를 학습하고 1→0 pull-down과 positive feedback에 의한 state flip 과정을 설명한다.
2. Write Margin과 Write Failure를 transistor strength 관점에서 이해한다.
3. 이후 Process Variation, Monte Carlo, SNM/Offset distribution과 SRAM yield로 확장한다.

## 10. 자기 설명 점검

- [x] 용어의 정의를 설명할 수 있다.
- [x] 구조 또는 동작 과정을 설명할 수 있다.
- [x] 관련 개념과 비교할 수 있다.
- [ ] AI 반도체에서 왜 중요한지 설명할 수 있다.

## 사용자 원문

<details>
<summary>대화에서 제공한 원문 보기</summary>

> “Cell NMOS가 Access NMOS보다 강해야 하는 이유는, Cell NMOS가 더 강해야 Q node가 GND와 강하게 연결되어 0을 유지하려고 하기 때문이다.”

> “write에서는 Q=0 -> Q=1 동작보다 Q=1 -> Q=0으로 끌어내려지는 동작을 통해 반대쪽 inverter도 바뀌는 걸로 기억하고 있는데... 그러면 NMOS의 역할이 그렇게 크게 작용하는지 모르겠음.”

> “inverter에서 VM은 mosfet에서의 Vth와는 달라... PMOS와 NMOS가 균형을 이루는 지점을 VM이라고 해.”

> “hold SNM이 더 크지. 왜냐하면 hold되어있으면 WL=0이 되어 bitline과 분리되기 때문에, 내부가 안정한 상태를 더 잘 유지할 수 있어서...”

> “나의 이해에 따르면 SNM은 SRAM이 noise를 견딜 수 있는 척도이며, SNM이 크다는 것은 곧 SRAM이 큰 noise를 견딜 수 있다는 뜻이야.”

> “read를 하게 되면 일단 Q가 살짝 증가하게 될꺼야 bitline에서 1이라는 state를 주기 때문에... Q를 input으로 받는 CMOS inverter에서 PMOS의 힘이 살짝 약해지고, NMOS의 힘이 살짝 강해짐으로 Qbar가 살짝 감소하게 됨.”

> “대칭성이 어느 방향으로 깨졌는지 판단하는 것.”

> “BL를 초기화시켜주지 않으면... 이전의 전압차이로 바로 0,1을 구분해버리는 오류가 발생할 수도 있기 때문이지. sense amp는 불안정하기 때문에 이전의 작은 전압차이라도, 초기화시키지 않고 재사용한다면, 오류를 범할 가능성이 높아.”

> “SRAM Cell에 저장된 데이터는 변해서는 안됨... 그러나 sense amp는 BL의 미세한 변화를 측정하여 어디가 0이고 1인지 빠르게 판단을 해야함. 그래서 아주 작은 변화에도 민감하게 feedback을 할 수 있도록 불안정 평형점 근처에 의도적으로 놓여있어야함.”

> “차이가 너무 작으면 틀리게 읽을 수도 있을 것 같아.”

> “이상적인 상황에서는 괜찮지만, 실제 상황에서는 noise도 다수 발생하고 inverter 별로 MOS의 크기가 달라서(mismatch)... 그래서 offset 보다 여유있게 큰 delta V를 요구해야해.”

</details>
