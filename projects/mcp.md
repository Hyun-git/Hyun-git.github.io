---
layout: default
title: MCP-based Container Control Sidechat
permalink: /projects/mcp
---

<div class="subpage">

  <a href="/projects" class="back-link">← 프로젝트 목록</a>
  <h1 class="subpage-title">MCP Container Sidechat</h1>
  <p class="subpage-desc">LLM과 컨테이너 제어 인터페이스를 연결하는 MCP 기반 인터페이스 개발</p>

  <div class="project-detail">

    <p class="pf-project-org">구름 (goorm) | 2024.11 — 2025.02</p>

    <section class="project-section">
      <h2>Project Overview</h2>
      <p>컨테이너 조작에 어려움을 느끼는 사용자의 진입 장벽을 해결하기 위해, 자연어로 대화하며 컨테이너를 생성하고 제어할 수 있는 MCP(Model Context Protocol) 기반의 사이드챗 시스템을 구축했습니다.</p>
    </section>

    <section class="project-section">
      <h2>Key Technical Points</h2>
      <ul>
        <li>
          <strong>MCP Server Architecture Design</strong>
          <p>LLM이 호출할 수 있는 도구(Tool)들을 정의하고, 이를 실제 서버 사이드 인프라와 연결하는 실행 엔진을 설계했습니다. 이를 통해 AI가 직접 인프라를 제어할 수 있는 구조를 마련했습니다.</p>
        </li>
        <li>
          <strong>Interface Standardization</strong>
          <p>LLM과 컨테이너 제어 시스템 간의 통신 규격을 표준화하여, 다양한 LLM 모델에서도 일관된 제어 성능과 보안을 유지할 수 있도록 구현했습니다.</p>
        </li>
        <li>
          <strong>Conversational DX (Developer Experience)</strong>
          <p>복잡한 설정 UI를 거치지 않고 "Python 환경 컨테이너 하나 만들어줘"와 같은 자연어 명령만으로 즉시 개발 환경을 구성할 수 있는 파이프라인을 구축하여 사용자 경험을 고도화했습니다.</p>
        </li>
      </ul>
    </section>

    <section class="project-section">
      <h2>Tech Stack</h2>
      <div class="pf-tags">
        <span class="pf-tag">Node.js</span>
        <span class="pf-tag">TypeScript</span>
        <span class="pf-tag">MCP (Model Context Protocol)</span>
        <span class="pf-tag">LLM Integration</span>
        <span class="pf-tag">Container Control API</span>
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
