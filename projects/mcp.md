---
layout: post
title: MCP-based Container Control Sidechat
description: LLM과 컨테이너 제어 인터페이스를 연결하는 MCP(Model Context Protocol) 기반 인터페이스 개발
image: /assets/goorm/arkain.png
---

## 🚀 Project Overview

컨테이너 조작에 어려움을 느끼는 사용자의 진입 장벽을 해결하기 위해, 자연어로 대화하며 컨테이너를 생성하고 제어할 수 있는 **MCP(Model Context Protocol)** 기반의 사이드챗 시스템을 구축했습니다.

- **Focus**: LLM 인터페이스 표준화, 컨테이너 제어 자동화, DX(Developer Experience) 고도화

---

## 🛠 Key Implementations

### 1. MCP Server 아키텍처 설계
- **도구 정의 및 실행 로직**: LLM이 호출할 수 있는 도구(Tool)들을 정의하고, 이를 실제 서버 사이드 인프라와 연결하는 실행 엔진을 설계했습니다.
- **인터페이스 표준화**: LLM ↔ 컨테이너 제어 간의 통신 규격을 표준화하여, 다양한 모델에서도 동일한 제어 성능을 발휘하도록 구현했습니다.

### 2. 자연어 기반 컨테이너 제어
- 사용자가 복잡한 설정 메뉴를 찾지 않아도 "Python 환경 컨테이너 하나 만들어줘"와 같은 요청만으로 즉시 환경을 구성할 수 있는 파이프라인을 구축했습니다.

---

## 📈 Impact

- **사용자 진입 장벽 완화**: 인프라 지식이 부족한 초보 사용자도 대화만으로 클라우드 IDE 환경을 쉽게 활용 가능
- **작업 효율 개선**: 반복적인 컨테이너 설정 작업을 대화형으로 처리하여 전체적인 작업 속도 향상
