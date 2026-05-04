---
layout: post
title: Arkain (Global Container Platform Modernization)
description: Docker 기반 레거시 인프라의 Kubernetes 전환 및 글로벌 템플릿 에코시스템 구축
image: /assets/goorm/arkain.png
---

## 🚀 Project Overview

**Arkain** 프로젝트는 기존 Docker 기반의 단일 컨테이너 제공 서비스를 글로벌 시장에 적합한 확장성과 안정성을 갖춘 **Kubernetes 기반 클라우드 플랫폼**으로 현대화하고, 유저 간 개발 환경을 공유할 수 있는 **템플릿 시스템**을 구축한 리브랜딩 프로젝트입니다.

- **Official Site**: [https://arkain.io/](https://arkain.io/)
- **Focus**: Infrastructure Migration (Docker to K8s), Global Scalability, Template Ecosystem

---

## 🛠 핵심 성과 및 구현 내용

### 1. 인프라 현대화: Docker → Kubernetes 전환
기존 Docker 기반 운영 방식의 한계를 극복하고 글로벌 서비스의 확장성을 확보하기 위해 Kubernetes로의 전체 인프라 전환을 주도했습니다.
- **확장성 확보**: 트래픽 증가에 따른 자동 확장(Auto-scaling) 및 고가용성(High Availability) 아키텍처 구현
- **운영 최적화**: 컨테이너 오케스트레이션을 통해 서비스 배포, 롤백, 리소스 관리를 표준화하여 인프라 운영 효율 40% 이상 향상
- **글로벌 라우팅**: Latency 기반 도메인 분리 로직을 적용하여 전 세계 사용자에게 최적화된 응답 속도 제공

### 2. 템플릿 시스템: 컨테이너 이미지 저장 및 공유 에코시스템
사용자가 구성한 최적의 개발 환경을 템플릿화하여 저장하고, 이를 글로벌 유저들과 공유할 수 있는 신규 기능을 설계 및 개발했습니다.
- **템플릿 생명주기 관리**: Docker/Project 메타데이터 자동 수집을 통한 원클릭 템플릿 생성 API 및 관리 기능 구축
- **안전한 이미지 관리**: S3 Presigned URL 기반 업로드 및 외부 보안 검수 API 콜백 연동을 통한 비동기 상태 전이 처리
- **운영 자동화 연동**: Slack 웹훅을 활용하여 사용자 신고 대응 및 템플릿 상태 관리를 실시간으로 처리할 수 있는 운영 도구 구축

---

## 🏗 시스템 아키텍처 (Technical Stack)

| 구분 | 주요 기술 |
| :--- | :--- |
| **Orchestration** | Kubernetes (EKS), Docker |
| **API Server** | Node.js, NestJS, TypeScript |
| **Storage & DB** | S3 (Media), MongoDB, Elasticsearch |
| **Ops Tool** | AppSmith, Slack API, ELK Stack |

---

## 📈 Impact

- **인프라 안정성**: Kubernetes 전환을 통해 단일 장애점(SPOF) 제거 및 무중단 배포 환경 구축
- **사용자 참여 증대**: 템플릿 공유 기능을 통해 개발 환경 구축의 진입 장벽을 낮추고 유저 간 상호작용 활성화
- **글로벌 시장 안착**: 리브랜딩과 함께 안정적인 인프라 환경을 바탕으로 성공적인 글로벌 런칭 수행

---

> **"레거시 인프라의 기술 부채를 해결하고, 사용자가 가치를 재생산할 수 있는 플랫폼의 기반을 만들었습니다."**
