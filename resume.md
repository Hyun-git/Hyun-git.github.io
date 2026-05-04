---
layout: default
title: Resume
permalink: /resume
---

<div class="subpage">

  <a href="/" class="back-link">← 홈</a>
  <h1 class="subpage-title">Resume</h1>
  <p class="subpage-desc">경력, 학력 및 주요 업무 경험</p>

  <section class="pf-section">
    <h2 class="pf-section-title">소개</h2>
    <div class="pf-about">
      <p><strong>"작성한 코드가 부채가 아닌 자산이 될 수 있도록 노력하는 개발자입니다."</strong></p>
      <p>오래된 서비스를 유지/보수해온 경험을 바탕으로 에러 로깅, 트러블슈팅, 빠른 장애 대응에 강점을 가지고 있습니다. 기존 서비스를 리팩토링 및 리브랜딩하여 <strong>글로벌 서비스(Arkain)로 재출시</strong>한 경험을 통해 협업을 위한 가독성과 유지보수성의 중요성을 깊이 인지하고 있습니다.</p>
      <p>새로운 기술을 도입하고 시도하며, 제가 만든 기능을 사용자들이 편리하게 사용했을 때 큰 보람을 느낍니다. 앞으로도 다양한 동료들과 협업하며 즐겁게 가치 있는 서비스를 만들어 가고 싶습니다.</p>
    </div>
  </section>

  <section class="pf-section">
    <h2 class="pf-section-title">기술 스택</h2>
    <div class="pf-work-item">
      <div class="pf-tags">
        <span class="pf-tag">Node.js</span>
        <span class="pf-tag">TypeScript</span>
        <span class="pf-tag">NestJS</span>
        <span class="pf-tag">Express</span>
        <span class="pf-tag">MongoDB</span>
        <span class="pf-tag">Elasticsearch</span>
        <span class="pf-tag">Redis</span>
        <span class="pf-tag">Kubernetes</span>
        <span class="pf-tag">Docker</span>
      </div>
    </div>
  </section>

  <hr class="pf-divider">

  <section class="pf-section">
    <h2 class="pf-section-title">경력</h2>

    <div class="pf-timeline">

      <div class="pf-timeline-item">
        <div class="pf-timeline-header">
          <div>
            <h3 class="pf-org">구름 (goorm)</h3>
            <p class="pf-role-sm">Full-Stack Developer</p>
          </div>
          <span class="pf-period">2023.01 — 재직중</span>
        </div>
        <p class="pf-description">
          컨테이너 및 IDE를 제공하는 클라우드 개발 환경 서비스 운영. 글로벌 리브랜딩 프로젝트 <strong>Arkain</strong>의 핵심 백엔드 개발을 담당하며, 개발자 경험(DX) 향상을 위한 기능 고도화와 운영 효율화에 집중하고 있습니다.
        </p>

        <div class="pf-work-items">

          <div class="pf-work-item">
            <h4>MCP 기반 컨테이너 제어 사이드챗 개발</h4>
            <div class="pf-tags">
              <span class="pf-tag">MCP</span>
              <span class="pf-tag">LLM</span>
              <span class="pf-tag">UX 개선</span>
            </div>
            <ul>
              <li>자연어 기반 컨테이너 제어를 위해 MCP(Model Context Protocol) 기반 사이드챗 구축</li>
              <li>MCP Server의 도구 정의 및 실행 로직 설계, LLM ↔ 컨테이너 간 인터페이스 표준화로 작업 효율 개선</li>
            </ul>
          </div>

          <div class="pf-work-item">
            <h4>배포 기능 개발 (컨테이너 서비스 운영 자동화)</h4>
            <div class="pf-tags">
              <span class="pf-tag">배포 자동화</span>
              <span class="pf-tag">컨테이너</span>
              <span class="pf-tag">DX 개선</span>
            </div>
            <ul>
              <li>IDE 환경을 넘어 실서비스 배포가 가능하도록 <strong>Deploy, Version, Image 관리 기능</strong> 통합 설계</li>
              <li>복잡한 인프라 설정을 UI로 추상화하여 비전문가도 클릭만으로 서비스 운영 및 롤백이 가능한 환경 구축</li>
            </ul>
          </div>

          <div class="pf-work-item">
            <h4>사용량 기반 과금 시스템 설계 및 도입</h4>
            <div class="pf-tags">
              <span class="pf-tag">과금/정산</span>
              <span class="pf-tag">Elasticsearch</span>
              <span class="pf-tag">Cron</span>
              <span class="pf-tag">멱등성</span>
            </div>
            <ul>
              <li>구독제에서 컨테이너 실사용량 기반 과금 체계로 전환하여 과금 공정성 및 정확도 향상</li>
              <li>분산 환경에서의 <strong>결제 멱등성(Idempotency)</strong> 보장 로직을 설계하여 데이터 신뢰성 확보</li>
              <li>LLM 및 리소스 사용량 실시간 모니터링을 통한 초과 과금 방지 알림 시스템 구축</li>
            </ul>
          </div>

          <div class="pf-work-item">
            <h4>로깅 구조 개선 및 에러 대응 효율화</h4>
            <div class="pf-tags">
              <span class="pf-tag">Elasticsearch</span>
              <span class="pf-tag">로깅</span>
              <span class="pf-tag">중앙화</span>
            </div>
            <ul>
              <li>분산된 로그 구조를 파일 기반으로 통일하고 중앙화된 Elasticsearch 관리 체계 구축</li>
              <li>에러 로그 필터링 및 노이즈 제거 정책을 통해 실질 장애 대응 집중도 향상 (수백 건 → 10건 내외)</li>
            </ul>
          </div>

          <div class="pf-work-item">
            <h4>자동화 및 외부 서비스 연동</h4>
            <div class="pf-tags">
              <span class="pf-tag">AppSmith</span>
              <span class="pf-tag">Slack API</span>
              <span class="pf-tag">운영 효율화</span>
            </div>
            <ul>
              <li>AppSmith 기반 통합 환불 대시보드를 구축하여 정책 검증 및 환불 프로세스 업무 시간 단축</li>
              <li>Slack 연동 실시간 커뮤니티 신고 처리 기능을 구축하여 운영 환경 제약 해소</li>
            </ul>
          </div>

          <div class="pf-work-item">
            <h4>인프라 최적화 및 구축 프로젝트</h4>
            <div class="pf-tags">
              <span class="pf-tag">Kubernetes</span>
              <span class="pf-tag">마이그레이션</span>
              <span class="pf-tag">비용 절감</span>
            </div>
            <ul>
              <li>VM 기반 환경을 Kubernetes로 마이그레이션하여 확장성 및 운영 안정성 확보</li>
              <li>Latency 기반 도메인 라우팅 분리를 통해 글로벌 응답 속도 개선 및 인프라 비용 절감</li>
              <li>일본 사이버대학 IDE 및 카카오 크램폴린 IDE 구축/유지보수 수행</li>
            </ul>
          </div>

        </div>
      </div>

    </div>
  </section>

  <hr class="pf-divider">

  <section class="pf-section">
    <h2 class="pf-section-title">학력</h2>
    <div class="pf-timeline">
      <div class="pf-timeline-item">
        <div class="pf-timeline-header">
          <div>
            <h3 class="pf-org">서울시립대학교</h3>
            <p class="pf-role-sm">컴퓨터과학부</p>
          </div>
          <span class="pf-period">2017.03 — 2023.01</span>
        </div>
      </div>
    </div>
  </section>

</div>
