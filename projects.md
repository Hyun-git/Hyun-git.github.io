---
layout: default
title: Projects
permalink: /projects
---

<div class="subpage">

  <a href="/" class="back-link">← 홈</a>
  <h1 class="subpage-title">Projects</h1>
  <p class="subpage-desc">사이드 프로젝트 및 개인 작업물</p>

  <div class="pf-projects">

    <div class="pf-project-card">
      <div class="pf-project-thumbnail">
        <img src="/assets/goorm/arkain.png" alt="Arkain thumbnail">
      </div>
      <div class="pf-project-header">
        <div>
          <h3 class="pf-project-name">
            <a href="/projects/arkain" class="pf-stretched-link">Arkain Template System</a>
          </h3>
          <p class="pf-project-org">구름 (goorm) — Global IDE Ecosystem</p>
        </div>
        <span class="pf-period">2023.01 — 재직중</span>
      </div>
      <p class="pf-description">Docker 기반의 기존 서비스를 Kubernetes로 전환하고, 글로벌 환경 공유를 위한 템플릿 에코시스템을 구축한 리브랜딩 프로젝트입니다.</p>
      <ul>
        <li>Docker 기반 인프라의 Kubernetes 전환을 통한 고가용성 및 확장성 확보</li>
        <li>컨테이너 이미지 저장 및 공유를 위한 템플릿 시스템(API 통합, S3 업로드 파이프라인) 구축</li>
        <li>Slack API 연동을 통한 실시간 운영 자동화 시스템 구축</li>
      </ul>
      <div class="pf-project-links">
        <a href="https://arkain.io/" target="_blank" class="pf-link">Official Site (arkain.io)</a>
      </div>
    </div>

    <div class="pf-project-card">
      <div class="pf-project-thumbnail">
        <img src="/assets/goorm/arkain.png" alt="Arkain Nexus thumbnail">
      </div>
      <div class="pf-project-header">
        <div>
          <h3 class="pf-project-name">
            <a href="/projects/mcp" class="pf-stretched-link">Arkain Nexus (AI Console MCP)</a>
          </h3>
          <p class="pf-project-org">구름 (goorm) — AI Console Assistant</p>
        </div>
        <span class="pf-period">2024.11 — 2025.02</span>
      </div>
      <p class="pf-description">LLM과 MCP(Model Context Protocol)를 활용하여 자연어 기반의 클라우드 콘솔 제어 및 사용자 지원 시스템을 구축했습니다.</p>
      <ul>
        <li>템플릿 추천, 크레딧 계산, 컨테이너 제어 등 인프라 조작을 위한 스마트 도구(Tools) 구현</li>
        <li>GitBook AI 연동을 통한 RAG 기반 제품 가이드 및 릴리즈 노트 자동 답변 시스템 구축</li>
        <li>보안을 위한 userId 필터링 및 분산 서버 간 인터페이스 표준화</li>
      </ul>
      <div class="pf-project-links">
        <a href="/projects/mcp" class="pf-link">Case Study</a>
      </div>
    </div>

    <div class="pf-project-card">
      <div class="pf-project-thumbnail">
        <img src="/assets/images/farmeme.png" alt="Farmeme thumbnail">
      </div>
      <div class="pf-project-header">
        <div>
          <h3 class="pf-project-name">
            <a href="/projects/farmeme" class="pf-stretched-link">Farmeme</a>
          </h3>
          <p class="pf-project-org">Mash-Up 14기</p>
        </div>
        <span class="pf-period">2024.03 — 2024.10</span>
      </div>
      <p class="pf-description">홈에서 추천하는 밈을 빠르게 확인하고, 키워드·카테고리로 탐색하는 밈 앱. 반응을 남기고 클립보드에 밈 이미지를 저장할 수 있는 서비스.</p>
      <ul>
        <li>아이폰 대용량 이미지 업로드 지연 문제를 이미지 압축 처리로 해결</li>
        <li>짧은 기간 내 다수의 API 개발과 백오피스 작업, 주간 스크럼을 통한 효율적 업무 분배</li>
      </ul>
      <div class="pf-project-links">
        <a href="https://github.com/mash-up-kr/ppac-server" target="_blank" class="pf-link">GitHub</a>
        <a href="https://play.google.com/store/apps/details?id=team.ppac.app&hl=ko" target="_blank" class="pf-link">Android</a>
      </div>
    </div>

    <div class="pf-project-card">
      <div class="pf-project-thumbnail">
        <img src="/assets/images/twotoo.png" alt="Twotoo thumbnail">
      </div>
      <div class="pf-project-header">
        <div>
          <h3 class="pf-project-name">
            <a href="/projects/twotoo" class="pf-stretched-link">Twotoo</a>
          </h3>
          <p class="pf-project-org">Mash-Up 13기 — 커플 챌린지 앱</p>
        </div>
        <span class="pf-period">2023.03 — 진행중</span>
      </div>
      <p class="pf-description">연인과 함께 22일간의 최소 목표 기간을 기반으로 새로운 습관 형성을 돕는 챌린지·기록 앱.</p>
      <ul>
        <li>Nest/Docker/ECR → Express/TypeScript/PM2 마이그레이션으로 장기 유지보수 효율 향상</li>
        <li>MongoDB Atlas Chart 대시보드 구축 및 가입 유저 5,000명, 인증 수 40,000건 돌파</li>
      </ul>
      <div class="pf-project-links">
        <a href="https://github.com/team-twotoo" target="_blank" class="pf-link">GitHub</a>
        <a href="https://twotoo-landing.vercel.app/" target="_blank" class="pf-link">홈페이지</a>
      </div>
    </div>

  </div>

</div>
