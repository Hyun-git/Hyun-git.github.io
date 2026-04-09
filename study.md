---
layout: default
title: Study
permalink: /study
---

<div class="subpage">

  <a href="/" class="back-link">← 홈</a>
  <h1 class="subpage-title">Study</h1>
  <p class="subpage-desc">기술 학습 및 블로그 글 모음</p>

  <ul class="study-posts">
    {% for post in site.posts %}
    <li class="study-post-item">
      <a href="{{ post.url | relative_url }}" class="study-post-title">{{ post.title }}</a>
      <span class="study-post-date">{{ post.date | date: "%Y.%m.%d" }}</span>
    </li>
    {% endfor %}
  </ul>

</div>
