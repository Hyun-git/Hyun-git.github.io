---
layout: default
title: Arkain Template System
permalink: /projects/arkain
---

<div class="subpage">

  <a href="/projects" class="back-link">← 프로젝트 목록</a>
  <h1 class="subpage-title">Arkain Template System</h1>
  <p class="subpage-desc">글로벌 클라우드 IDE 환경의 공유 및 재사용을 위한 템플릿 에코시스템 구축</p>

  <div class="project-detail">

    <p class="pf-project-org">구름 (goorm) | 2023.01 — 재직중</p>

    <section class="project-section">
      <h2>Project Overview</h2>
      <p>기존 Docker 기반의 단일 컨테이너 제공 서비스를 글로벌 시장에 적합한 확장성과 안정성을 갖춘 Kubernetes 기반 클라우드 플랫폼으로 현대화하고, 유저 간 개발 환경을 공유할 수 있는 템플릿 시스템을 구축한 프로젝트입니다.</p>
      <p><a href="https://arkain.io/" target="_blank" class="pf-link">공식 홈페이지: arkain.io</a></p>
    </section>

    <section class="project-section">
      <h2>Key Technical Points</h2>
      <ul>
        <li>
          <strong>Infrastructure Modernization (Docker → Kubernetes)</strong>
          <p>레거시 Docker 환경을 Kubernetes로 전환하여 고가용성(HA)과 자동 확장성(Auto-scaling)을 확보했습니다. Latency 기반 도메인 라우팅을 적용하여 글로벌 사용자에게 최적화된 응답 속도를 제공합니다.</p>
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
          <strong>Operations Automation (Slack Webhook)</strong>
          <p>사용자 신고 및 운영 이슈 발생 시 Slack 웹훅을 통해 실시간 알림을 전달하고, Slack 내 인터페이스에서 즉시 상태 변경이 가능하도록 운영 자동화 시스템을 구축했습니다.</p>
          <div class="architecture-diagram">
            <img src="/assets/goorm/slack_report.png" alt="Slack Webhook Integration for Operations">
          </div>
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
