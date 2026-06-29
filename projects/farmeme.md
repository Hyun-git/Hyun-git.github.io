---
layout: default
title: Farmeme
permalink: /projects/farmeme
---

<div class="subpage">

  <a href="/projects" class="back-link">← 프로젝트 목록</a>
  <div class="project-title-container" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; margin-bottom: 0.5rem;">
    <h1 class="subpage-title" style="margin-bottom: 0;">Farmeme</h1>
    <div class="pf-project-links">
      <a href="https://github.com/mash-up-kr/ppac-server" target="_blank" class="pf-link">GitHub</a>
      <a href="https://play.google.com/store/apps/details?id=team.ppac.app&hl=ko" target="_blank" class="pf-link">Android</a>
    </div>
  </div>
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
          <strong>이미지 압축 및 처리 파이프라인 (Sharp / HEIC)</strong>
          <p>아이폰에서 촬영된 HEIC 포맷 이미지를 비롯한 대용량 이미지가 그대로 업로드되면서 응답 지연과 S3 저장 비용 증가가 발생했습니다. 서버 사이드에서 Sharp 라이브러리를 활용해 포맷 변환 및 품질 압축 파이프라인을 구성하여 이미지 처리 흐름을 표준화했습니다.</p>
        </li>
        <li>
          <strong>Layered Architecture (Controller - Service - Model)</strong>
          <p>Controller - Service - Model 레이어를 명확히 분리하여 비즈니스 로직의 응집도를 높이고 유지보수성을 확보했습니다. 밈 추천 로직과 검색 로직을 Service 레이어에서 독립적으로 관리하여 각 기능의 수정이 다른 레이어에 영향을 주지 않도록 설계했습니다.</p>
        </li>
        <li>
          <strong>CI/CD 자동화 (GitHub Actions)</strong>
          <p>Pull Request 생성 시 lint, 타입 검사, 단위 테스트를 자동 실행하고, main 브랜치 병합 시 EC2 자동 배포까지 이어지는 파이프라인을 구성했습니다. 배포 과정의 수동 개입을 없애 개발 사이클을 단축했습니다.</p>
        </li>
      </ul>
    </section>

    <section class="project-section">
      <h2>Technical Challenges</h2>
      <ul>
        <li>
          <strong>PNG 이미지 압축 — quality를 낮춰도 크기가 안 줄었던 이유</strong>
          <p>Sharp로 PNG 이미지를 처리할 때 <code>quality(80)</code> 옵션을 설정했음에도 파일 크기가 전혀 줄지 않는 현상을 발견했습니다. 원인은 PNG의 무손실(lossless) 압축 방식에 있었습니다. PNG는 quality 옵션이 적용되지 않으며, 파일 크기를 줄이려면 WebP 또는 JPEG로 포맷 자체를 변환해야 합니다. (<a href="/png-압축-quality를-낮춰도-크기가-안-줄었던-이유.html">관련 글</a>)</p>
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
