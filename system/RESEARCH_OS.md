# AI Semiconductor Research OS

## 1. 목적

AI Semiconductor Research OS는 KAIST SSL Lab 개별연구 준비를 장기적으로 관리하기 위한 학습 및 연구 기록 시스템이다.

최종 목표는 사용자가 AI computation, Computer Architecture, Memory Architecture, NPU, PIM/CIM을 연결해서 이해하고, 관련 논문의 핵심 아이디어와 hardware architecture를 자신의 언어로 설명하며 독립적인 research question을 만들 수 있게 되는 것이다.

## 2. 기록 유형

### Learning Log

학습 당일의 사고 과정을 보존하는 작업 기록이다.

- 무엇을 공부했는지
- 처음에는 어떻게 이해했는지
- 어떤 오해나 불확실성이 있었는지
- 피드백 후 이해가 어떻게 수정되었는지
- 아직 해결되지 않은 질문이 무엇인지

Learning Log에서는 초기 오해를 지우지 않는다. 이해가 변화한 과정을 남기는 것이 목적이다.

### Foundation Note

여러 주제를 이해하는 데 반복적으로 필요한 기초 지식을 정리하는 문서다.

예:
- MAC operation
- Memory Hierarchy
- SRAM / DRAM basics
- Data Reuse
- Systolic Array

Foundation Note는 개별 학습 세션보다 안정적이고 재사용 가능한 지식 기반을 만든다.

### Final Note

하나의 개념이나 주제에 대해 충분한 학습과 검증을 거친 뒤 만드는 정제된 설명이다.

Learning Log가 "어떻게 이해하게 되었는가"를 기록한다면, Final Note는 "현재 기준으로 무엇을 이해하고 있는가"를 명확하게 전달하는 데 초점을 둔다.

### Paper Note

논문을 구조적으로 분석하기 위한 기록이다.

주요 항목:
- Problem
- Motivation
- Prerequisites
- Key Idea
- Architecture
- Method
- Experiments
- Results
- Trade-offs
- Limitations
- Questions
- Connection to My Research Interest

Paper Note의 목적은 논문 요약에 그치지 않고, 제안 구조가 왜 필요한지와 어떤 대가를 지불하는지를 분석하는 것이다.

## 3. Source of Truth

GitHub repository를 장기 학습 기록의 **Source of Truth**로 사용한다.

원칙:
- 현재 conversation은 단기 작업 맥락으로 사용한다.
- 장기적으로 유지할 학습 내용은 repository의 Markdown 문서에 기록한다.
- 기존 기록을 수정할 때는 현재 파일을 먼저 확인하고 변경점을 비교한다.
- 초기 이해, 오해, 수정된 이해를 구분해 학습의 변화 과정을 보존한다.
- 기록의 양보다 독립적인 설명 능력과 research thinking의 향상을 우선한다.

## 4. 장기 목표

Research OS는 다음 능력의 형성을 지원한다.

1. AI computation의 hardware mapping 이해
2. Computer Architecture 핵심 개념 이해
3. SRAM, DRAM, eDRAM 및 Memory Architecture 이해
4. NPU architecture와 dataflow 이해
5. PIM/CIM의 원리와 trade-off 이해
6. AI semiconductor paper의 구조적 분석
7. KAIST SSL Lab 논문의 독립적 분석
8. Research Question 도출
9. Portfolio / CV / 교수님 면담 자료로 발전

최종 성공 기준은 많은 파일을 만드는 것이 아니라, 사용자가 자신의 언어로 설명하고 비교하고 질문할 수 있게 되는 것이다.
