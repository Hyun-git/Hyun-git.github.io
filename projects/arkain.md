---
layout: post
title: Arkain (Global Cloud IDE & Container Platform)
description: 구름 IDE의 글로벌 리브랜딩 및 컨테이너 기반 클라우드 플랫폼 개발
image: /VM.png
---

## 🚀 Project Overview

**Arkain**은 전 세계 개발자들이 언제 어디서나 클라우드 자원을 활용해 개발할 수 있도록 컨테이너와 IDE를 제공하는 플랫폼입니다. 기존 서비스를 글로벌 시장에 맞춰 리브랜딩하고, 확장성 있는 아키텍처로 재설계하여 성공적으로 글로벌 런칭을 수행했습니다.

- **Role**: Backend Engineer / Full-Stack Developer
- **Focus**: 글로벌 서비스 아키텍처, 사용량 기반 과금 시스템, 배포 자동화, AI(MCP) 통합

---

## 🛠 Tech Stack

- **Backend**: Node.js, TypeScript, NestJS, Express
- **Infrastructure**: Kubernetes (EKS), Docker, AWS
- **Data**: MongoDB, Elasticsearch, Redis
- **DevOps**: GitHub Actions, Helm, AppSmith, Slack API

---

## 🌟 Key Accomplishments

### 1. 글로벌 리브랜딩 및 인프라 마이그레이션
- **글로벌 대응**: 전 세계 유저의 응답 속도 개선을 위해 Latency 기반 도메인 라우팅을 적용하고 리전별 트래픽 최적화 수행
- **K8s 마이그레이션**: 기존 VM 기반 환경을 Kubernetes로 전환하여 운영 효율성을 40% 이상 향상시키고 인프라 비용 절감

![Infrastructure Architecture](/VM.png)
*VM 기반 환경에서 K8s로의 전환을 통한 확장성 확보*

### 2. 사용량 기반 과금 시스템 (Usage-based Billing)
- **정밀 과금**: Elasticsearch에 적재된 컨테이너 사용량 데이터를 분석하여 실사용 기준의 정밀한 과금 로직 설계
- **신뢰성 보장**: 결제 및 과금 프로세스에 **멱등성(Idempotency)** 로직을 적용하여 분산 환경에서도 중복 과금이 발생하지 않는 안정적인 결제 환경 구축

### 3. MCP 기반 AI 사이드챗 및 DX 개선
- **AI 인터페이스**: 자연어로 컨테이너를 제어할 수 있는 MCP(Model Context Protocol) 기반 사이드챗 개발로 초보 사용자의 진입 장벽 제거
- **배포 자동화**: 복잡한 K8s 설정을 추상화하여, 클릭만으로 컨테이너를 즉시 배포하고 버전 관리/롤백이 가능한 배포 파이프라인 구축

![Docker Image Management](/dockerImage.png)
*컨테이너 이미지 관리 및 배포 자동화 인터페이스*

---

## 📈 Results & Impact

- **글로벌 런칭**: 리브랜딩을 통한 성공적인 글로벌 서비스 재론칭 및 사용자 유입 증가
- **운영 효율화**: 수동으로 처리하던 환불 및 커뮤니티 관리 프로세스를 자동화(AppSmith, Slack 연동)하여 업무 시간 단축
- **안정성 강화**: 중앙화된 로깅 시스템(ELK Stack) 구축으로 장애 대응 시간(MTTR) 단축

---

> **"단순한 기능 개발을 넘어, 서비스가 자산이 될 수 있도록 견고한 아키텍처와 운영 효율을 고민했습니다."**
