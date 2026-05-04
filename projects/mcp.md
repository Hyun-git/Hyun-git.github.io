---
layout: default
title: Arkain Nexus (AI Console MCP)
permalink: /projects/mcp
---

<div class="subpage">

  <a href="/projects" class="back-link">← 프로젝트 목록</a>
  <h1 class="subpage-title">Arkain Nexus (AI Console MCP)</h1>
  <p class="subpage-desc">LLM과 MCP를 연동한 차세대 인텔리전트 클라우드 콘솔 제어 시스템</p>

  <div class="project-detail">

    <p class="pf-project-org">구름 (goorm) | 2024.11 — 2025.02</p>

    <section class="project-section">
      <h2>Project Overview</h2>
      <p><strong>Arkain Nexus</strong>는 복잡한 클라우드 콘솔 조작을 자연어 인터페이스로 혁신한 프로젝트입니다. 사용자의 질의를 LLM이 이해하고, MCP(Model Context Protocol)를 통해 실시간 컨테이너 상태 조회, 크레딧 계산, 템플릿 추천 등의 액션을 직접 수행합니다.</p>
      <p>단순한 챗봇을 넘어, 서버 인프라와 LLM 사이의 가교 역할을 하는 분산 아키텍처를 설계하고 구현하는 데 집중했습니다.</p>
    </section>

    <section class="project-section">
      <h2>System Architecture</h2>
      <p>네 개의 주요 컴포넌트가 유기적으로 통신하는 분산 시스템을 구축하여 보안과 확장성을 확보했습니다.</p>
      <ul>
        <li><strong>ide-site (Interface):</strong> 유저 Chat UI 및 응답 유형별 뷰(하이라이팅, 페이지 이동) 처리</li>
        <li><strong>LLM-API-Server:</strong> 프롬프트 설계, 응답 가공 및 보안을 위한 개인정보(userId 등) 필터링 담당</li>
        <li><strong>MCP-Client:</strong> 유저 쿼리에 최적화된 Tool을 판단하고 MCP-Server와 AI 사이의 응답 조율</li>
        <li><strong>nexus-console-server (MCP-Server):</strong> 실질적인 동작(Tool) 정의 및 Arkain 내부 API 연동 처리</li>
      </ul>
    </section>

    <section class="project-section">
      <h2>Key Features (Phase 1)</h2>
      <ul>
        <li>
          <strong>지능형 템플릿 추천 및 탐색</strong>
          <p>사용자의 니즈(예: "포트폴리오 만들고 싶어")를 분석하여 메타데이터 기반의 최적화된 템플릿을 추천하고 관련 리스트 뷰로 자동 유도합니다.</p>
        </li>
        <li>
          <strong>사용량 기반 크레딧 예측 및 계산</strong>
          <p>현재 실행 중인 컨테이너 스펙과 보유 크레딧을 실시간으로 대조하여, 특정 환경에서 사용 가능한 시간을 예측해주는 복합 계산 로직을 구현했습니다.</p>
        </li>
        <li>
          <strong>RAG 기반 제품 가이드 제공 (GitBook AI 연동)</strong>
          <p>Arkain 공식 가이드 문서를 LLM이 검색 및 요약하여 답변하도록 GitBook AI API를 연동했습니다. 이를 통해 최신 제품 사양과 릴리즈 노트를 즉시 안내합니다.</p>
        </li>
        <li>
          <strong>실시간 컨테이너 조회 및 상태 모니터링</strong>
          <p>동면 상태나 마지막 접속일 등 유저의 인프라 현황을 즉시 조회하고, 특정 컨테이너를 UI 상에서 하이라이팅 처리하여 조작 편의성을 높였습니다.</p>
        </li>
      </ul>
    </section>

    <section class="project-section">
      <h2>Technical Challenges & Solutions</h2>
      <ul>
        <li>
          <strong>보안 및 어뷰징 방지</strong>
          <p>사용자 정보 유출을 막기 위해 LLM 질의 전 단계에서 userId 필터링을 적용했으며, 도구(Tools)가 호출되는 경우에만 LLM-API-Server가 동작하도록 설계하여 불필요한 비용과 리스크를 최소화했습니다.</p>
        </li>
        <li>
          <strong>응답 가공 및 스트리밍 최적화</strong>
          <p>GitBook AI 등 외부 API의 파편화된 응답 형식을 정제하고, 유저에게 최종적으로 전달될 마크다운 기반의 데이터 구조를 정의하여 일관된 인터페이스를 제공했습니다.</p>
        </li>
        <li>
          <strong>표준 에러 핸들링</strong>
          <p>JSON-RPC 표준 규격을 준수하여 Method not found, Internal error 등 서버 에러 상황에 대한 예외 처리를 체계화했습니다.</p>
        </li>
      </ul>
    </section>

    <section class="project-section">
      <h2>Tech Stack</h2>
      <div class="pf-tags">
        <span class="pf-tag">Node.js</span>
        <span class="pf-tag">TypeScript</span>
        <span class="pf-tag">MCP (Model Context Protocol)</span>
        <span class="pf-tag">LLM (Claude/OpenAI)</span>
        <span class="pf-tag">GitBook AI API</span>
        <span class="pf-tag">Mermaid Diagram</span>
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
