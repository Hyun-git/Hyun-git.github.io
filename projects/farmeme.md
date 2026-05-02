---
layout: default
title: Farmeme (Farmeme)
permalink: /projects/farmeme
---

<div class="subpage">

  <a href="/projects" class="back-link">← 프로젝트 목록</a>
  <h1 class="subpage-title">Farmeme (Farmeme)</h1>
  <p class="subpage-desc">추천 밈 탐색 및 클립보드 저장 서비스</p>

  <div class="project-detail">

    <p class="pf-project-org">Mash-Up 14기 | 2024.03 — 2024.10</p>

    <section class="project-section">
      <h2>Project Overview</h2>
      <p>홈에서 추천하는 밈을 빠르게 확인하고, 키워드·카테고리로 탐색하는 밈 앱 서비스입니다. 사용자가 반응을 남기고 클립보드에 밈 이미지를 저장할 수 있는 기능을 제공합니다.</p>
    </section>

    <section class="project-section">
      <h2>Architecture</h2>
      <p>Farmeme의 전체 시스템 구조입니다. 고해상도 이미지 처리와 안정적인 배포 파이프라인 구축에 중점을 두었습니다.</p>
      <div class="architecture-diagram">
        <img src="/assets/architecture/ppac/architecture_diagram.png" alt="Farmeme Architecture Diagram">
      </div>
    </section>

    <section class="project-section">
      <h2>Key Technical Points</h2>
      <ul>
        <li>
          <strong>이미지 압축 및 처리 (Sharp / HEIC)</strong>
          <p>아이폰 등에서 업로드되는 대용량 이미지(HEIC 등)의 처리 지연 문제를 해결하기 위해, 서버 사이드에서 Sharp 라이브러리를 활용한 압축 및 포맷 변환을 적용했습니다. 이를 통해 S3 저장 비용 절감과 클라이언트 로딩 속도를 개선했습니다.</p>
        </li>
        <li>
          <strong>Layered Architecture (Express/Node.js)</strong>
          <p>Controller - Service - Model 레이어로 명확히 구분하여 비즈니스 로직의 응집도를 높이고 유지보수성을 확보했습니다.</p>
        </li>
        <li>
          <strong>CI/CD & Infrastructure</strong>
          <p>GitHub Actions를 통해 빌드, 테스트, 배포 과정을 자동화했습니다. AWS S3를 활용한 이미지 스토리지와 MongoDB Atlas를 통한 데이터 관리를 수행합니다.</p>
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
        <span class="pf-tag">AWS S3</span>
        <span class="pf-tag">Firebase (FCM)</span>
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
</style>
