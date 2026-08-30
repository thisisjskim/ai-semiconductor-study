# 학습 기록: NVM 기초와 NVM-CIM 연결 (NVM Fundamentals)

## Metadata

- Date: 2026-08-30
- Recorded at: 2026-08-30T13:42:39Z
- Topic: NVM Fundamentals — ReRAM, MRAM, PCM과 NVM-CIM
- Document type: learning-log
- Domain: pim-cim
- Roadmap stage: Stage 6 — Foundational Papers
- Status: working
- Source: conversation
- Evidence: ReRAM/MRAM/PCM의 저장 메커니즘과 HRS/LRS를 직접 비교 설명하고, PCM SET/RESET 및 MTJ tunneling의 수정된 이해를 재설명했으며, NVM-CIM에서 V를 IA, G를 weight로 대응시키는 곱셈 직관을 스스로 연결함
- Related notes: paper-notes/foundational/2026-08-28-overview-of-cim-circuits-with-dram-and-nvm.md
- Last updated: 2026-08-30

## 1. 오늘 공부한 목적

현재 읽고 있는 CIM overview 논문의 NVM-CIM section을 이해하기 위해 ReRAM, MRAM, PCM의 device-level 기본 동작과 resistance-state sensing을 별도 prerequisite로 학습했다. 목표는 각 NVM이 어떤 물리 상태를 바꾸어 resistance를 저장하는지, HRS/LRS를 어떻게 읽는지, 그리고 그 resistance/conductance가 CIM multiplication과 어떻게 연결되는지를 이해하는 것이었다.

## 2. 오늘 이해한 내용

NVM은 ReRAM, MRAM, PCM처럼 물리적 저장 메커니즘은 서로 다르지만, 회로 관점에서는 서로 다른 resistance state를 데이터로 표현하고 read voltage에 따른 current 차이로 state를 구분한다는 공통 구조를 갖는다.

ReRAM에서는 metal-insulator-metal 구조의 oxide 내부 conductive filament가 형성되거나 약화·단절되면서 resistance가 변한다. SET은 HRS에서 LRS로 가는 방향이며 filament를 형성하거나 강화한다. RESET은 LRS에서 HRS로 가는 방향이며 filament를 약화하거나 끊는다.

MRAM의 핵심 소자는 MTJ(Magnetic Tunnel Junction)다. fixed magnetic layer와 free magnetic layer 사이에 매우 얇은 insulating tunnel barrier가 있고, 전자는 이 barrier를 quantum tunneling으로 통과할 수 있다. 두 magnetic layer가 parallel이면 spin-dependent electronic state matching이 더 유리해 tunneling conductance가 커지고 resistance가 낮아진다. Antiparallel이면 반대로 conductance가 작아지고 resistance가 높아진다.

PCM은 chalcogenide 계열 phase-change material의 atomic arrangement를 바꿔 resistance를 저장한다. Crystalline state는 일반적으로 LRS, amorphous state는 HRS에 대응한다. RESET에서는 강하고 짧은 pulse로 일부 phase-change material을 melting한 뒤 빠르게 quench해 amorphous state를 만들고, SET에서는 melting이 목적이 아니라 crystallization 가능한 온도에서 충분한 시간을 주어 원자들이 규칙적인 crystalline structure를 형성하게 한다.

세 NVM 모두 read에서는 같은 voltage를 걸었을 때 Ohm's law에 따라 LRS에서 더 큰 current, HRS에서 더 작은 current가 흐르는 차이를 sensing한다.

NVM-CIM에서는 resistance보다 conductance G=1/R로 표현하는 것이 자연스럽다. 사용자는 V를 input activation, G를 stored weight에 대응시키면 I=VG가 곱셈 역할을 할 수 있고, 여러 cell current가 column에서 합쳐지면 병렬 MAC으로 확장될 수 있다는 방향을 스스로 연결했다.

NVM-CIM의 실제 계산에서는 ideal한 I=VG 관계에서 벗어나는 nonlinearity, conductance level 간 구분이 어려워지는 low signal margin, device variation과 noise가 계산 정확도를 저하시킬 수 있다는 문제를 인식했다.

## 3. 핵심 개념

- NVM 공통 구조: physical state → resistance state → read current
- LRS / HRS와 Ohm's law 기반 current sensing
- ReRAM: MIM, metal oxide, conductive filament, SET/RESET
- MRAM: MTJ, fixed/free layer, parallel/antiparallel, spin-dependent tunneling, TMR 직관
- PCM: chalcogenide, crystalline/amorphous, Joule heating, crystallization, melting, quenching
- Conductance: G=1/R
- NVM-CIM multiplication: I=VG
- Column current summation과 MAC
- NVM-CIM의 low signal margin, nonlinearity, variation

## 4. 내가 처음 이해한 방식

- ReRAM의 SET은 filament를 강화해 HRS에서 LRS로 만들고, RESET은 filament를 제거해 LRS에서 HRS로 만든다고 이해했다.
- MRAM에서는 parallel일 때 free layer와 fixed layer의 spin 방향이 같아 전자가 더 잘 이동하고, antiparallel이면 이동이 어려워져 HRS가 된다고 이해했다.
- MTJ tunneling에 대해서는 spin 방향이 다르면 insulating barrier를 통과하기 어려운 것인지 질문했다.
- PCM RESET은 강하고 짧은 pulse로 일부를 녹인 뒤 빠르게 열 주입을 중단해 amorphous/HRS를 만들고, SET은 상대적으로 낮고 긴 pulse를 사용한다고 이해했다.
- SET에 대해서 처음에는 material을 녹인 뒤 천천히 식혀 crystalline state를 만든다고 표현했다.
- NVM-CIM에서는 I=VG에서 V를 IA, G를 NVM의 weight 표현에 대응시켜 multiplication에 응용할 수 있다고 추론했다.

## 5. 오해 또는 불확실한 부분

- MRAM의 antiparallel state를 단순히 “spin 방향이 달라 insulating barrier를 잘 통과하지 못한다”라고 이해하면 barrier 자체가 spin을 직접 차단하는 것처럼 오해할 수 있었다.
- PCM SET을 “녹인 뒤 천천히 식힌다”라고 표현했지만, SET의 핵심은 완전 melting이 아니라 crystallization 가능한 온도에서 원자 재배열에 충분한 시간을 주는 것이다.
- NVM-CIM에서 G를 “NVM의 저항”이라고 표현했지만, G는 resistance R 자체가 아니라 conductance G=1/R이다.
- 실제 NVM-CIM에서는 ideal I=VG만으로 설명되지 않으며 nonlinearity, low signal margin, variation 등의 오차원이 존재한다.

## 6. 수정된 이해

- MTJ의 매우 얇은 insulating barrier는 quantum tunneling을 허용하며, parallel/antiparallel에 따른 resistance 차이는 barrier를 단순히 통과할 수 있느냐 없느냐가 아니라 양쪽 ferromagnetic layer의 spin-dependent available states와 tunneling conductance 차이로 이해했다.
- PCM SET은 phase-change material을 완전히 녹이는 과정이 아니라 crystallization 가능한 온도 범위에서 충분한 시간을 주어 atomic arrangement가 crystalline structure를 형성하게 하는 과정으로 수정했다.
- NVM-CIM에서 weight와 직접 대응시키는 물리량은 resistance보다 conductance이며, G=1/R를 사용해 I=VG 형태의 multiplication을 해석한다.
- NVM-CIM을 볼 때 이상적 multiplication뿐 아니라 conductance state spacing, signal margin, nonlinearity와 variation이 실제 MAC accuracy를 어떻게 해치는지 함께 봐야 한다고 정리했다.

## 7. 질문

### 해결되지 않은 질문

- 현재 논문의 Section III에서 ReRAM, MRAM, PCM 기반 CIM이 각각 어떤 circuit architecture와 trade-off로 구현되는지는 아직 읽어야 한다.
- NVM-CIM에서 low signal margin과 nonlinearity를 실제 회로가 어떤 sensing, encoding, calibration 또는 architecture 기법으로 완화하는지는 이후 논문 내용과 연결해 확인한다.

### 해결된 질문

- ReRAM의 MIM 구조와 conductive filament가 HRS/LRS를 만드는 기본 원리
- MTJ가 무엇이며 insulating barrier에서 quantum tunneling이 가능한 이유
- Parallel/antiparallel alignment가 resistance 차이를 만드는 spin-dependent tunneling 직관
- Chalcogenide가 무엇이며 PCM에서 어떤 material phase를 바꾸는지
- PCM에서 Joule heating으로 temperature와 pulse duration을 제어해 SET/RESET을 만드는 이유
- ReRAM/MRAM/PCM의 물리적 저장 메커니즘 차이와 resistance-state 공통점
- NVM의 conductance가 I=VG를 통해 CIM multiplication과 연결되는 기본 직관

## 8. AI 반도체 및 SSL 목표와의 연결

이 prerequisite는 NVM을 단순한 memory device로 보는 데서 끝나지 않고, stored conductance 자체를 computation primitive로 사용하는 CIM 관점으로 연결된다. 특히 activation을 voltage로 인가하고 weight를 conductance로 저장해 cell current를 multiplication 결과로 만들고, column current summation으로 MAC을 구현한다는 구조는 AI accelerator의 matrix-vector multiplication과 직접 연결된다.

또한 ideal I=VG만 보는 것이 아니라 device variation, nonlinearity, signal margin과 sensing overhead를 함께 봐야 한다는 관점은 이후 NVM-CIM 논문의 architecture와 claimed benefit을 평가할 때 필요한 기반이다.

## 9. 다음 행동

1. 현재 읽고 있는 overview 논문의 Section III NVM-CIM으로 복귀해 NVM의 non-volatility, density, current-based computing advantage와 각 기술의 circuit-level trade-off를 user-first 방식으로 읽는다.
2. 논문에서 low signal margin, nonlinearity, variation이 실제 architecture에서 어떻게 나타나고 어떤 circuit technique으로 완화되는지 연결한다.
3. 이 Learning Log가 저장된 뒤 현재 Paper Note의 prerequisite bridge에 연결할지 별도 checkpoint로 결정한다.

## 10. 자기 설명 점검

- [x] 용어의 정의를 설명할 수 있다.
- [x] 구조 또는 동작 과정을 설명할 수 있다.
- [x] 관련 개념과 비교할 수 있다.
- [x] AI 반도체에서 왜 중요한지 설명할 수 있다.

## 사용자 원문

<details>
<summary>대화에서 제공한 원문 보기</summary>

> “LRS는 NVM에서 저항이 낮게 결정된 상태, HRS는 반대로 저항이 높게 결정된 상태야. 그래서 read voltage를 걸었을 때, LRS에는 높은 전류가 HRS는 낮은 전류가 흘러.”

> “ReRAM에서 SET은 filament를 강화하는 작용이야. 이 말은 즉슨 HRS->LRS로 만들어주는 것이지.”

> “parallel : LRS , antiparallel : HRS”

> “절연막이 절연체임에도 그 두께가 매우 얇기 때문에 전자가 터널링 할 수 있음.”

> “crystallization가능한 온도에서 일정 시간 유지함으로써, 분자 배열이 일정한 결정을 이룰 수 있도록 시간을 주는거야”

> “NVM 역시 I = VG의 연산을 하고, V를 IA, G를 NVM의 저항으로 두고 연산을 최적화 할 수 있는, 즉 이렇게 multiplication에 응용할 수 있는 방향이 아닐까”

</details>
