---
layout: default
title: MCP Sidechat
permalink: /projects/mcp
image: /assets/goorm/mcp.png
---

<div class="subpage">

  <a href="/projects" class="back-link">← 프로젝트 목록</a>
  <h1 class="subpage-title">MCP Sidechat</h1>
  <p class="subpage-desc">LLM과 MCP를 연동한 클라우드 콘솔 제어 인터페이스 개발</p>

  <div class="project-detail">

    <p class="pf-project-org">Project Arkain | 2024.11 — 2025.02</p>

    <section class="project-section">
      <h2>Project Overview</h2>
      <p><strong>MCP Sidechat</strong>은 복잡한 클라우드 콘솔 조작을 대화형 인터페이스로 풀어낸 프로젝트입니다. MCP(Model Context Protocol)를 활용하여 LLM이 실시간 리소스 상태를 조회하고, 사용자의 요청에 따라 직접 인프라를 제어할 수 있는 환경을 구축했습니다.</p>
    </section>

    <section class="project-section">
      <h2>System Architecture</h2>
      <p>네 개의 주요 컴포넌트가 유기적으로 통신하는 분산 시스템을 구축하여 보안과 확장성을 확보했습니다.</p>
      
      <div class="mermaid">
      sequenceDiagram
          participant User as 유저 (User)
          participant Frontend as 프론트엔드 (UI)
          participant MCPClient as MCP-Client
          participant Controller as 리소스 컨트롤러 (Controller)
          participant AIProxy as AI-Proxy-Server
          participant LLM as 외부 AI 모델 (LLM)

          User->>Frontend: 1. 자연어 쿼리 입력
          Frontend->>MCPClient: 2. 도구(Tool) 실행 필요성 판단
          
          alt 도구 호출 필요 시
              MCPClient->>Controller: 3. 인프라 조작/조회 요청
              Controller->>Frontend: 4. 실시간 상태 데이터 Fetch
              Frontend-->>Controller: 데이터 응답
              Controller-->>MCPClient: 조작 결과 반환
          else 도구 불필요 시
              Note over MCPClient: 일반 대화 모드로 진행
          end

          MCPClient->>AIProxy: 5. 실행 결과 및 컨텍스트 전달
          AIProxy->>LLM: 6. 최종 프롬프트 질의 (RAG 적용)
          LLM-->>AIProxy: 응답 생성
          AIProxy->>Frontend: 7. 가공된 최적 응답 전달
          Frontend-->>User: 8. UI 반영 및 자동 액션 수행
      </div>

      <ul>
        <li><strong>Frontend (UI):</strong> 대화형 인터페이스 제공 및 응답 유형별 뷰(하이라이팅, 페이지 이동) 처리</li>
        <li><strong>AI-Proxy-Server:</strong> 프롬프트 설계, 응답 가공 및 보안을 위한 데이터 필터링 담당</li>
        <li><strong>MCP-Client:</strong> 유저 쿼리에 최적화된 도구를 판단하고 리소스 컨트롤러와 AI 사이의 조율</li>
        <li><strong>Resource Controller:</strong> 실질적인 인프라 제어 도구 정의 및 내부 시스템 API 연동 처리</li>
      </ul>
    </section>

    <section class="project-section">
      <h2>Key Features</h2>
      <ul>
        <li>
          <strong>지능형 리소스 추천 및 환경 구성</strong>
          <p>사용자의 개발 목적(예: "웹 포트폴리오 구축")을 분석하여 최적화된 개발 환경 템플릿을 추천하고 관련 리소스로 자동 안내합니다.</p>
        </li>
        <li>
          <strong>실시간 비용 예측 및 자원 모니터링</strong>
          <p>현재 사용 중인 인프라 스펙과 잔여 예산을 실시간으로 대조하여, 예상 사용 가능 시간을 산출해주는 복합 계산 로직을 구현했습니다.</p>
        </li>
        <li>
          <strong>RAG 기반 제품 가이드 시스템</strong>
          <p>방대한 제품 가이드와 기술 문서를 LLM이 검색 및 요약하여 답변하도록 지식 베이스(Knowledge Base) API를 연동했습니다.</p>
        </li>
        <li>
          <strong>인프라 가시성 확보</strong>
          <p>리소스의 상태(활성/비활성)와 마지막 접근일 등 현황을 즉시 조회하고, UI 상에서 관련 자원을 강조 표시하여 관리 편의성을 높였습니다.</p>
        </li>
      </ul>
    </section>

    <section class="project-section">
      <h2>Technical Challenges & Solutions</h2>
      <ul>
        <li>
          <strong>데이터 보안 및 필터링</strong>
          <p>민감 정보 유출을 방지하기 위해 AI 모델 전달 전 단계에서 식별자 필터링을 적용했으며, 도구가 호출되는 필요한 경우에만 프록시 서버를 거치도록 설계하여 리스크를 최소화했습니다.</p>
        </li>
        <li>
          <strong>비정형 데이터 정제 및 가공</strong>
          <p>외부 지식 베이스의 파편화된 응답 형식을 정제하고, 사용자에게 전달될 최종 응답의 일관성을 위해 데이터 구조를 표준화했습니다.</p>
        </li>
        <li>
          <strong>에러 핸들링 표준화</strong>
          <p>JSON-RPC 표준 규격을 준수하여 네트워크 및 로직 에러 상황에 대한 예외 처리를 체계화하여 서비스 안정성을 높였습니다.</p>
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
        <span class="pf-tag">Distributed Systems</span>
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
