---
layout: default
title: Twotoo (투투)
permalink: /projects/twotoo
---

<div class="subpage">

  <a href="/projects" class="back-link">← 프로젝트 목록</a>
  <div class="project-title-container" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; margin-bottom: 0.5rem;">
    <h1 class="subpage-title" style="margin-bottom: 0;">Twotoo (투투)</h1>
    <div class="pf-project-links">
      <a href="https://github.com/team-twotoo" target="_blank" class="pf-link">GitHub</a>
      <a href="https://twotoo-landing.vercel.app/" target="_blank" class="pf-link">홈페이지</a>
    </div>
  </div>
  <p class="subpage-desc">연인과 함께 22일간의 최소 목표 기간을 기반으로 새로운 습관 형성을 돕는 챌린지·기록 앱</p>

  <div class="project-detail">

    <p class="pf-project-org">Mash-Up 13기 | 2023.03 — 진행중</p>

    <section class="project-section">
      <h2>Project Overview</h2>
      <p>Twotoo는 연인이 서로의 습관 형성을 독려하고 기록하는 서비스입니다. 22일이라는 최소 목표 기간을 설정하여 작은 습관부터 차근차근 만들어갈 수 있도록 돕습니다. 챌린지 생성, 인증샷 기록, 서로 찌르기(알림) 등의 기능을 제공합니다.</p>
      <div class="project-stats">
        <div class="stat-item">
          <span class="stat-number">5,000+</span>
          <span class="stat-label">가입 유저</span>
        </div>
        <div class="stat-item">
          <span class="stat-number">40,000+</span>
          <span class="stat-label">챌린지 인증 수</span>
        </div>
      </div>
    </section>

    <section class="project-section">
      <h2>Architecture</h2>
      <p>Twotoo의 서버 아키텍처입니다. 서비스의 지속 가능성과 유지보수 효율을 높이기 위한 구조로 설계되었습니다.</p>
      <div class="architecture-diagram">
        <img src="/assets/architecture/twotoo/twotoo_full_architecture.png" alt="Twotoo Architecture Diagram">
      </div>
    </section>

    <section class="project-section">
      <h2>Key Technical Points</h2>
      <ul>
        <li>
          <strong>아키텍처 마이그레이션 (NestJS → Express)</strong>
          <p>초기 NestJS/Docker/ECR 기반 구조에서 서비스 규모와 팀의 운영 편의성을 고려하여 Express/TypeScript/PM2 구조로 마이그레이션을 진행했습니다. 이를 통해 빌드 및 배포 속도를 개선하고, 장기적인 유지보수 효율을 확보했습니다.</p>
        </li>
        <li>
          <strong>서버리스 알림 시스템 (AWS Lambda & EventBridge)</strong>
          <p>사용자의 챌린지 참여를 독려하는 정기 알림 기능을 AWS Lambda와 EventBridge를 활용한 서버리스 구조로 분리했습니다. 메인 서버의 부하를 줄이고 독립적인 스케줄링 관리가 가능하도록 구축했습니다.</p>
        </li>
        <li>
          <strong>데이터 가시성 확보 및 성과 (MongoDB Atlas Charts)</strong>
          <p>MongoDB Atlas Charts를 활용하여 실시간 유저 활동 및 챌린지 현황 대시보드를 구축했습니다. 이를 통해 <strong>가입 유저 5,000명 돌파, 인증 수 40,000건 이상</strong> 등의 주요 지표를 실시간으로 모니터링하며 서비스 성장을 추적했습니다. 개발자뿐만 아니라 기획, 디자인 파트에서도 서비스 지표를 쉽게 확인하고 의사결정에 활용할 수 있는 환경을 제공했습니다.</p>
          <div class="architecture-diagram">
            <img src="/assets/architecture/twotoo/mongo_chart.png" alt="Twotoo MongoDB Atlas Chart">
          </div>
        </li>
        <li>
          <strong>로그 관리 자동화</strong>
          <p>PM2-Logrotate와 Cron Job을 활용하여 로컬 로그 파일의 생명주기를 관리하고, 중요한 로그는 S3에 백업하는 프로세스를 자동화하여 안정적인 운영 환경을 구축했습니다.</p>
        </li>
      </ul>
    </section>

    <section class="project-section">
      <h2>Tech Stack</h2>
      <div class="pf-tags">
        <span class="pf-tag">Node.js</span>
        <span class="pf-tag">Express</span>
        <span class="pf-tag">TypeScript</span>
        <span class="pf-tag">MongoDB Atlas</span>
        <span class="pf-tag">AWS EC2 (Ubuntu)</span>
        <span class="pf-tag">AWS S3</span>
        <span class="pf-tag">AWS Lambda</span>
        <span class="pf-tag">AWS EventBridge</span>
        <span class="pf-tag">Firebase (FCM)</span>
        <span class="pf-tag">PM2</span>
        <span class="pf-tag">GitHub Actions</span>
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
.project-stats {
  display: flex;
  gap: 2rem;
  margin-top: 1.2rem;
  padding: 1rem 1.5rem;
  background: var(--bg-secondary, #f8f8f8);
  border-radius: 8px;
  border: 1px solid var(--border-color);
}
.stat-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.stat-number {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--text-color);
  line-height: 1.2;
}
.stat-label {
  font-size: 0.8rem;
  color: var(--meta-color);
  margin-top: 0.2rem;
}
</style>
