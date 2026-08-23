# 학습 기록: SRAM-DRAM 구조 비교와 DRAM Sense Amplifier (SRAM-DRAM Comparison and DRAM Sense Amplifier)

## Metadata

- Date: 2026-08-22
- Recorded at: 2026-08-22T05:09:33Z
- Topic: SRAM-DRAM 구조 비교와 DRAM Sense Amplifier
- Document type: learning-log
- Domain: memory-architecture
- Roadmap stage: Stage 3 — Memory
- Status: working
- Source: conversation
- Evidence: self-explanation, inference, misconception-correction, comparison
- Related notes: learning-logs/2026/08/2026-08-15-sram-read-path-fundamentals.md
- Last updated: 2026-08-22

## 1. 오늘 공부한 목적

- Register와 DRAM 사이에서 SRAM이 맡는 memory hierarchy 역할을 자기 언어로 설명한다.
- SRAM 6T와 DRAM 1T1C의 저장 구조 차이에서 density, read behavior, refresh의 차이를 추론한다.
- DRAM charge sharing, destructive read, VDD/2 precharge, sense amplification과 restore의 인과관계를 이해한다.
- Sense amplifier offset과 DRAM capacitor scaling/high-k dielectric을 device-circuit 관점에서 연결한다.

## 2. 오늘 이해한 내용

### SRAM의 memory hierarchy 역할

Register는 연산 가까이에서 빠르게 데이터를 공급하지만 많은 데이터를 저장하기 어렵고 bit당 면적 비용이 높다. DRAM은 대용량 저장에는 유리하지만 접근과 data movement의 시간·에너지 비용이 크다. 사용자는 SRAM이 두 계층 사이의 가교가 되어 DRAM 접근 횟수를 줄이고 연산에 필요한 데이터를 Register/PE 쪽에 빠르게 공급한다고 설명했다.

### SRAM과 DRAM의 density trade-off

SRAM은 6T 구조이고 DRAM은 1T1C 구조이므로 SRAM cell이 구조적으로 더 큰 면적을 요구한다. 사용자는 제한된 chip area에서 SRAM만 사용하면 memory capacity가 감소하고 같은 대용량을 구현하려면 면적과 비용이 증가하므로 대용량 저장에는 DRAM이 필요하다고 설명했다.

### DRAM charge storage와 destructive read

DRAM은 capacitor charge로 bit를 표현한다. Cell capacitor는 bitline capacitance보다 작기 때문에 read 시 charge sharing으로 bitline에는 작은 전압 변화만 발생한다. 이 과정에서 cell capacitor의 원래 charge도 교란되므로 sense amplifier가 값을 판별한 뒤 restore해야 한다. 사용자는 SRAM은 cross-coupled inverter의 positive feedback으로 state를 유지하지만 DRAM은 read 시 capacitor charge가 변하기 때문에 destructive하다고 비교했다.

### VDD/2 precharge와 differential sensing

BL을 0 또는 VDD에 precharge하면 한 저장 상태에서는 voltage change가 거의 없고 반대 상태에서는 큰 charge sharing이 발생하는 비대칭성이 생긴다. VDD/2를 기준으로 하면 cell=1은 BL을 위쪽으로, cell=0은 아래쪽으로 움직여 작은 differential signal의 부호로 데이터를 판단할 수 있다.

### Cross-coupled sense amplifier와 restore

사용자는 cell=1일 때 BL이 VDD/2보다 조금 높아지면 cross-coupled sense amplifier에서 transistor current imbalance가 생기고, 한쪽 bitline의 discharge가 반대쪽 PMOS를 더 강하게 켜는 positive feedback을 만들어 BL→VDD, BL̅→0으로 증폭된다고 설명했다. WL이 연결된 상태에서 full-swing BL이 cell capacitor를 다시 충전하여 restore도 수행한다고 연결했다.

### Sense amplifier offset과 capacitor scaling

사용자는 sense amplifier mismatch가 cell이 만든 작은 ΔV보다 강하면 잘못된 방향으로 sensing하여 반대 bit를 읽고, restore 과정에서 잘못된 값을 cell에 다시 기록해 정보까지 훼손할 수 있다고 추론했다. 또한 Ccell이 작아질수록 charge sharing으로 만들어지는 ΔV가 작아져 noise와 offset의 상대적 영향이 커진다고 설명했다.

### DRAM capacitor와 high-k dielectric

Capacitance를 유지하기 위해 ε를 높이거나 dielectric thickness d를 줄이거나 실제 electrode surface area A를 확보할 수 있다. 사용자는 dielectric을 지나치게 얇게 만들면 leakage가 증가하여 retention time이 감소하고 refresh 빈도와 overhead가 증가한다고 연결했다. 처음에는 high-k를 높은 전도율로 혼동했으나, 이후 k는 유전율이며 높은 k는 polarization을 통해 외부 field를 더 많이 상쇄하여 같은 전압에서 더 많은 charge를 저장할 수 있다는 것으로 수정했다.

## 3. 핵심 개념

- Register → SRAM → DRAM memory hierarchy와 capacity/latency/area trade-off
- SRAM 6T와 DRAM 1T1C
- DRAM charge leakage, retention, refresh
- Charge sharing과 destructive read
- VDD/2 precharge와 differential sensing
- Cross-coupled regenerative sense amplifier
- Sense → Amplify → Restore
- Sense amplifier mismatch/offset과 sensing margin
- Ccell scaling과 ΔVBL
- High-k dielectric, polarization, capacitance와 leakage trade-off

## 4. 내가 처음 이해한 방식

- SRAM은 Register와 DRAM을 이어 주는 가교이며, DRAM의 높은 data movement 비용을 줄여 연산을 효율적으로 만든다고 이해했다.
- DRAM의 destructive read는 큰 bitline capacitance 때문에 cell에 저장된 값을 바꿀 가능성이 있기 때문이라고 추론했다.
- BL을 0 또는 VDD로 precharge하면 반대 상태의 cell과 연결될 때 큰 charge 이동으로 cell이 불안정해질 수 있고, 같은 전위의 state에서는 read가 제대로 일어났는지 구분하기 어렵다고 추론했다.
- Sense amplifier mismatch가 signal보다 크면 잘못된 sensing과 restore로 저장 정보 자체가 반대로 바뀔 수 있다고 추론했다.
- High-k dielectric의 k를 처음에는 전도율과 연결해 생각했다.

## 5. 오해 또는 불확실한 부분

- Sense amplifier가 BL/BL̅의 작은 전압 차이를 회로적으로 어떻게 판별하는지 처음에는 알지 못했다.
- Sense amplifier mismatch를 NMOS와 PMOS의 역할 자체가 뒤바뀌는 것으로 표현했으나, 실제 핵심은 좌우 branch의 Vth/strength mismatch가 input-referred offset을 만들어 한쪽을 선호한다는 것이다.
- Capacitance 식의 ε를 전도율로 혼동했다.
- Capacitor의 A를 줄이는 것이 Ccell 유지에 유리하다고 처음 답했으나, footprint는 줄이면서 실제 3D electrode surface area A는 크게 확보해야 한다.

## 6. 수정된 이해

- DRAM destructive read는 read 과정의 charge sharing 자체가 cell capacitor의 저장 charge를 교란하기 때문에 restore가 필요하다는 의미이다.
- DRAM sense amplifier는 별도의 숫자 비교기가 아니라 cross-coupled transistor의 작은 current imbalance와 regenerative positive feedback으로 BL/BL̅ 차이를 full swing으로 증폭한다.
- Sense amplifier offset은 실제 cell signal과 경쟁하며, offset/noise가 ΔVBL보다 커지면 read error와 잘못된 restore가 발생할 수 있다.
- Ccell 감소는 ΔVBL 감소로 이어져 sensing margin을 악화한다.
- High-k의 k는 conductivity가 아니라 relative permittivity이다. 높은 permittivity는 dielectric polarization을 통해 같은 physical thickness에서 더 큰 capacitance를 가능하게 하며, dielectric을 극단적으로 얇게 만드는 데 따른 leakage/reliability trade-off를 완화할 수 있다.

## 7. 질문

### 해결되지 않은 질문

- 지금까지의 SRAM/DRAM circuit-level 차이가 NPU on-chip SRAM buffer의 data reuse, memory bandwidth, energy와 구체적으로 어떻게 연결되는가?
- NPU의 실제 SRAM buffer hierarchy와 tiling/dataflow는 DRAM traffic을 어떻게 줄이는가?

### 해결된 질문

- 왜 SRAM은 Register와 DRAM 사이의 on-chip buffer 역할을 하는가?
- 왜 DRAM이 SRAM보다 density가 높은가?
- 왜 DRAM은 refresh가 필요한가?
- 왜 DRAM read는 destructive이고 restore가 필요한가?
- 왜 bitline을 VDD/2로 precharge하는가?
- DRAM sense amplifier는 작은 differential voltage를 어떻게 positive feedback으로 증폭하는가?
- Sense amplifier offset과 Ccell scaling은 sensing reliability에 어떤 영향을 주는가?
- High-k dielectric은 왜 DRAM capacitor scaling에 도움이 되는가?

## 8. AI 반도체 및 SSL 목표와의 연결

이번 학습은 memory device/circuit 특성이 AI accelerator의 memory hierarchy 선택으로 어떻게 연결되는지를 이해하기 위한 기반이다. SRAM의 낮은 density를 감수하고 on-chip buffer로 사용하는 이유와 DRAM을 대용량 off-chip memory로 사용하는 이유를 회로 동작에서 설명할 수 있게 되었다. 다음 학습에서는 이를 NPU data reuse, bandwidth와 data movement energy로 다시 architecture level에 연결한다.

## 9. 다음 행동

1. NPU on-chip SRAM buffer가 activation, weight, partial sum의 data reuse를 어떻게 지원하는지 학습한다.
2. SRAM capacity와 tiling이 DRAM traffic 및 memory bandwidth 요구량에 미치는 영향을 연결한다.
3. 이후 data movement energy와 compute utilization 관점에서 memory hierarchy를 분석한다.

## 10. 자기 설명 점검

- [x] 용어의 정의를 설명할 수 있다.
- [x] 구조 또는 동작 과정을 설명할 수 있다.
- [x] 관련 개념과 비교할 수 있다.
- [x] AI 반도체에서 왜 중요한지 설명할 수 있다.

## 사용자 원문

<details>
<summary>대화에서 제공한 원문 보기</summary>

> "DRAM은 많은 데이터를 저장하기는 쉬우나 반응속도가 낮고, data를 움직이는데 사용하는 비용이 많이 발생한다. 그래서 SRAM이 이 중간에서 가교 역할을 한다."

> "SRAM은 6T구조이고, DRAM은 1T1C 구조이다. Transistor만 해도 5개가 차이가 난다. 구조적으로 SRAM이 면적을 더 많이 먹을 수 밖에 없다"

> "SRAM을 read 해도, SRAM 은 cross-coupled 구조이기 때문에, 하나의 state를 읽어도 기존 state를 유지하는 positive feedback 과정이 존재해서 안정적임. 그러나 DRAM은 1T1C구조로, capacitor에 있는 전하를 읽을 때, 전하의 손실이 발생할 수 밖에 없음."

> "DRAM에서 read 연산을 하면, DRAM의 capacitor에 저장되어있는 Q가 줄어들거나 증가하게 되면서 DRAM이 불안정한 state를 유지할 수 있음. 그래서 DRAM을 read 한 후, 미세한 전압 차이를 sense amp로 확인해서 DRAM에 저장되어 있는 bit가 0인지 1인지 판단한 후, 그 판단한 값을 다시 DRAM에 덮어 씌워줌으로써 DRAM을 다시 안정한 상태로 유지시켜주는 것임."

> "C_cell이 작을 수록, read 할 때 발생하는 charge sharing으로 인하여 증감하는 폭이 매우 줄어들게 되어, BL과 /BL의 미세한 차이는 더더욱 줄어들게 될 것이다. 그렇게 되면, noise와 offset이 매우 큰 영향을 끼치게 될 것이기 때문이다."

> "k가 높다는 것은 유전율이 높다는 뜻이고, 이는 전기장이 주어졌을 때 polarization이 잘 발생한다는 뜻이다. polarization이 잘 발생하면, 내부 전기장이 강하게 생성되고, 이로 인하여 외부 전기장을 더 많이 상쇄시킨다. 따라서 주어진 전압(전기장)에 더 많은 charge를 저장할 수 있게 된다."

</details>
