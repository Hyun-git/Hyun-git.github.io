---
layout: default
title: Arkain Global Launching
permalink: /projects/arkain
---

<div class="subpage">

  <a href="/projects" class="back-link">← 프로젝트 목록</a>
  <div class="project-title-container" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; margin-bottom: 0.5rem;">
    <h1 class="subpage-title" style="margin-bottom: 0;">Arkain Global Launching</h1>
    <div class="pf-project-links">
      <a href="https://arkain.io/" target="_blank" class="pf-link">Official Site</a>
    </div>
  </div>
  <p class="subpage-desc">글로벌 클라우드 IDE 환경 구축 및 템플릿 에코시스템 런칭</p>

  <div class="project-detail">

    <p class="pf-project-org">구름 (goorm) | 2023.01 — 재직중</p>

    <section class="project-section">
      <h2>Project Overview</h2>
      <p>기존 Docker 기반의 단일 컨테이너 제공 서비스를 글로벌 시장에 적합한 확장성과 안정성을 갖춘 Kubernetes 기반 클라우드 플랫폼으로 현대화하고, 유저 간 개발 환경을 공유할 수 있는 템플릿 시스템을 구축한 프로젝트입니다.</p>
    </section>

    <section class="project-section">
      <h2>Key Technical Points</h2>
      <ul>
        <li>
          <strong>Infrastructure Modernization (Docker → Kubernetes)</strong>
          <p>레거시 Docker 환경을 Kubernetes(EKS)로 전환하여 고가용성(HA)과 자동 확장성(HPA)을 확보했습니다. Latency 기반 도메인 라우팅(Route53)을 적용하여 글로벌 사용자에게 최적화된 응답 속도를 제공하고, 멀티 리전 운영 비용을 절감했습니다. 일본 사이버대학 IDE 및 카카오 크램폴린 IDE 구축·유지보수도 함께 수행했습니다.</p>
        </li>
        <li>
          <strong>Deploy & Version Management (배포 기능)</strong>
          <p>IDE 환경을 넘어 실서비스 배포가 가능하도록 Deploy, Version, Image 관리 기능을 통합 설계했습니다. 복잡한 인프라 설정을 UI로 추상화하여 비전문가도 클릭만으로 서비스 운영 및 이전 버전으로의 롤백이 가능한 환경을 구축했습니다.</p>
          <div class="architecture-diagram">
            <img src="/assets/images/deploy.png" alt="Arkain Deploy Feature UI">
          </div>
        </li>
        <li>
          <strong>Template Ecosystem & API Integration</strong>
          <p>Docker 및 Project 메타데이터 자동 수집을 통해 사용자 입력 부하를 최소화한 템플릿 생성/수정 API(PUT)를 통합 구현했습니다. 유저 간 최적의 개발 환경을 손쉽게 공유하고 재사용할 수 있는 기반을 마련했습니다.</p>
          <div class="architecture-diagram">
            <img src="/assets/goorm/template.png" alt="Arkain Template System Interface">
          </div>
        </li>
        <li>
          <strong>Secure Media Pipeline & State Management</strong>
          <p>S3 Presigned URL 기반의 이미지 업로드 아키텍처와 보안 검수 API 콜백 연동을 통해, 업로드 데이터의 보안을 보장하고 검수 결과에 따른 템플릿의 상태 전이를 비동기로 처리합니다.</p>
        </li>
        <li>
          <strong>Operations Automation (Slack Webhook & AppSmith)</strong>
          <p>사용자 신고 및 운영 이슈 발생 시 Slack 웹훅을 통해 실시간 알림을 전달하고, Slack 내 인터페이스에서 즉시 상태 변경이 가능하도록 운영 자동화 시스템을 구축했습니다. AppSmith 기반 통합 환불 대시보드를 구축하여 운영팀의 정책 검증 및 환불 처리 업무 시간을 단축했습니다.</p>
          <div class="architecture-diagram">
            <img src="/assets/goorm/slack_report.png" alt="Slack Webhook Integration for Operations">
          </div>
        </li>
      </ul>
    </section>

    <section class="project-section">
      <h2>Billing System — 사용량 기반 과금 전환</h2>
      <p>구독제에서 컨테이너 실사용량 기반 과금 체계로 전환한 프로젝트입니다. 과금 공정성 및 정확도 향상이 목표였습니다.</p>
      <ul>
        <li>
          <strong>결제 멱등성(Idempotency) 보장</strong>
          <p>분산 환경에서 Cron 재시도, 네트워크 타임아웃 등 다양한 실패 시나리오에서 이중 청구가 발생하지 않도록 Redis 기반 Idempotency Key 설계를 적용했습니다. 같은 빌링 주기에 대한 결제 요청은 항상 한 번만 처리되도록 원자적(atomic) 보장 로직을 구현했습니다.</p>
        </li>
        <li>
          <strong>실사용량 집계 (Elasticsearch + Cron)</strong>
          <p>컨테이너 사용 이벤트를 Elasticsearch에 누적하고, 정산 Cron이 주기적으로 집계하여 과금하는 파이프라인을 구성했습니다. 집계 로직에 멱등성을 보장하여 Cron이 재실행되어도 중복 청구 없이 안전하게 동작합니다.</p>
        </li>
        <li>
          <strong>초과 과금 방지 알림 시스템</strong>
          <p>LLM 및 컨테이너 리소스 사용량을 실시간으로 모니터링하여, 예산 임계값에 근접할 때 사전 알림을 발송하는 시스템을 구축했습니다. 사용자가 예상치 못한 과금 청구를 받는 상황을 방지합니다.</p>
          <div class="architecture-diagram">
            <img src="/assets/images/billing.png" alt="Arkain Billing Dashboard">
          </div>
        </li>
      </ul>
    </section>

    <section class="project-section">
      <h2>Logging — 에러 로그 중앙화 및 노이즈 제거</h2>
      <p>분산된 서비스의 로그를 Elasticsearch로 중앙화하고, 실질적인 장애 대응 집중도를 높였습니다.</p>
      <ul>
        <li>
          <strong>로그 구조 표준화</strong>
          <p>서비스마다 다른 형식으로 찍히던 로그를 파일 기반으로 통일하고 Elasticsearch로 수집하는 구조를 구축했습니다. traceId를 도입하여 여러 서비스에 걸친 요청을 단일 쿼리로 추적할 수 있도록 했습니다.</p>
        </li>
        <li>
          <strong>에러 노이즈 제거 (수백 건 → 10건 내외)</strong>
          <p>재시도로 자동 복구되는 일시적 오류, 클라이언트 실수로 발생하는 4xx 에러를 ERROR 레벨에서 분리하고 별도 인덱스로 라우팅했습니다. 온콜 알림이 실제 장애 상황에서만 발생하도록 정책을 정비하여 장애 감지 시간을 크게 단축했습니다.</p>
        </li>
      </ul>
    </section>

    <section class="project-section">
      <h2>Tech Stack</h2>
      <div class="pf-tags">
        <span class="pf-tag">Node.js</span>
        <span class="pf-tag">NestJS</span>
        <span class="pf-tag">TypeScript</span>
        <span class="pf-tag">Kubernetes (EKS)</span>
        <span class="pf-tag">Docker</span>
        <span class="pf-tag">MongoDB</span>
        <span class="pf-tag">Elasticsearch</span>
        <span class="pf-tag">AWS S3</span>
        <span class="pf-tag">Slack API</span>
      </div>
    </section>

  </div>

</div>

<style>
.project-detail h2 {
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.5rem;
  margin-top: 2.5rem;
}
.architecture-diagram {
  margin: 1.5rem 0;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1rem;
  background: white;
}
.project-section ul {
  padding-left: 1.2rem;
}
.project-section li {
  margin-bottom: 1rem;
}
.project-section li strong {
  display: block;
  font-size: 1.05rem;
  margin-bottom: 0.2rem;
}
.project-section li p {
  margin: 0;
  font-size: 0.93rem;
  color: var(--meta-color);
}
</style>
