---
layout: default
---

<div class="home">

  <section class="home-hero">
    <img src="/assets/images/profile.jpg" alt="이현광 프로필" class="home-profile-img" />
    <div class="home-hero-text">
      <div class="home-name-container">
        <h1 class="home-name">이현광</h1>
        <a href="/resume" class="home-resume-btn">Resume</a>
      </div>
      <p class="home-role">Full-Stack Developer</p>
      <p class="home-desc">코드가 부채가 아닌 자산이 될 수 있도록 노력하는 개발자</p>
      <div class="home-contact">
        <a href="mailto:mabr2845@gmail.com">mabr2845@gmail.com</a>
        <span>·</span>
        <a href="https://github.com/Hyun-git" target="_blank">GitHub</a>
      </div>
    </div>
  </section>

  <section class="home-section">
    <div class="home-section-header">
      <h2 class="home-section-title">Projects</h2>
      <a href="/projects" class="home-more-link">See more →</a>
    </div>
    
    <div class="pf-projects">
      <div class="pf-project-card">
        <div class="pf-project-thumbnail">
          <img src="/assets/images/twotoo.png" alt="Twotoo thumbnail">
        </div>
        <div class="pf-project-body">
          <div class="pf-project-header">
            <div>
              <h3 class="pf-project-name">
                <a href="/projects/twotoo" class="pf-stretched-link">Twotoo</a>
              </h3>
              <p class="pf-project-org">Mash-Up 13기</p>
            </div>
          </div>
          <p class="pf-description">연인과 함께 습관 형성을 돕는 챌린지 앱. 시스템 마이그레이션 및 운영 안정성 확보</p>
          <div class="pf-tags">
            <span class="pf-tag">Node.js</span>
            <span class="pf-tag">Express</span>
            <span class="pf-tag">MongoDB</span>
          </div>
        </div>
      </div>

      <div class="pf-project-card">
        <div class="pf-project-thumbnail">
          <img src="/assets/goorm/arkain.png" alt="Arkain thumbnail">
        </div>
        <div class="pf-project-body">
          <div class="pf-project-header">
            <div>
              <h3 class="pf-project-name">
                <a href="/projects/arkain" class="pf-stretched-link">Arkain Global Launching</a>
              </h3>
              <p class="pf-project-org">구름 (goorm)</p>
            </div>
          </div>
          <p class="pf-description">Docker 기반 레거시 인프라의 Kubernetes 전환 및 템플릿 에코시스템 구축</p>
          <div class="pf-tags">
            <span class="pf-tag">Kubernetes</span>
            <span class="pf-tag">Docker</span>
            <span class="pf-tag">Node.js</span>
          </div>
        </div>
      </div>

      <div class="pf-project-card">
        <div class="pf-project-thumbnail">
          <img src="/assets/goorm/mcp.png" alt="MCP Sidechat thumbnail">
        </div>
        <div class="pf-project-body">
          <div class="pf-project-header">
            <div>
              <h3 class="pf-project-name">
                <a href="/projects/mcp" class="pf-stretched-link">MCP Sidechat</a>
              </h3>
              <p class="pf-project-org">구름 (goorm)</p>
            </div>
          </div>
          <p class="pf-description">LLM과 MCP를 활용한 자연어 기반 클라우드 리소스 제어 인터페이스 구축</p>
          <div class="pf-tags">
            <span class="pf-tag">Node.js</span>
            <span class="pf-tag">TypeScript</span>
            <span class="pf-tag">MCP</span>
          </div>
        </div>
      </div>

      <div class="pf-project-card">
        <div class="pf-project-thumbnail">
          <img src="/assets/images/farmeme.png" alt="Farmeme thumbnail">
        </div>
        <div class="pf-project-body">
          <div class="pf-project-header">
            <div>
              <h3 class="pf-project-name">
                <a href="/projects/farmeme" class="pf-stretched-link">Farmeme</a>
              </h3>
              <p class="pf-project-org">Mash-Up 14기</p>
            </div>
          </div>
          <p class="pf-description">추천 밈 탐색 및 클립보드 저장 서비스. 대용량 이미지 처리 최적화 구현</p>
          <div class="pf-tags">
            <span class="pf-tag">Node.js</span>
            <span class="pf-tag">Express</span>
            <span class="pf-tag">TypeScript</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="home-section">
    <div class="home-section-header">
      <h2 class="home-section-title">Study</h2>
      <a href="/study" class="home-more-link">See more →</a>
    </div>

    <ul class="study-posts">
      {% for post in site.posts limit:5 %}
      <li class="study-post-item">
        <a href="{{ post.url | relative_url }}" class="study-post-title">{{ post.title }}</a>
        <span class="study-post-date">{{ post.date | date: "%Y.%m.%d" }}</span>
      </li>
      {% endfor %}
    </ul>
  </section>

</div>
