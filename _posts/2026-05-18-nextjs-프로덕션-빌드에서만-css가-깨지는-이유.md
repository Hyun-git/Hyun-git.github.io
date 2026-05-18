---
layout: post
title: Next.js 프로덕션 빌드에서만 CSS가 깨지는 이유 — CSS 모듈 선언 순서 함정
date: 2026-05-18T18:00:00.000+09:00
---

## 증상

`npm run dev`에서는 멀쩡하던 버튼이 프로덕션 빌드 후 실행하면 갑자기 `2rem × 2rem` 크기로 쪼그라들며 다른 요소에 덮히는 현상이 발생했다. 더 이상한 건 **항상** 깨지는 게 아니라 특정 페이지 진입 경로에서만 재현된다는 점이었다.

---

## 원인 분석

### 1. 해시된 클래스명으로 단서 찾기

프로덕션 빌드에서 DevTools로 해당 버튼을 확인하니 `.mJbdX2`라는 해시된 클래스가 붙어 있었고, 이 스타일이 버튼 크기를 덮어쓰고 있었다.

```css
.mJbdX2 {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2rem;
    height: 2rem;
    padding: 0;
}
```

이 스타일은 개발 환경에서는 `IconButton_IconButton__xxxx`로 사람이 읽을 수 있는 이름이지만, 프로덕션에서는 짧게 해시된다. 소스를 추적하니 `IconButton.module.scss`의 base 클래스였다.

```scss
/* IconButton.module.scss */
.IconButton {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 2rem;
    height: 2rem;
    padding: 0;
}
```

### 2. 충돌 구조 파악

문제의 버튼은 두 개의 CSS 모듈 클래스를 동시에 가지고 있었다.

```
IconButton_IconButton__7ndGq          → width: 2rem  (IconButton.module.scss)
SettingsLinkCopyAndRefreshRow__copyBtn__img_wrapper__FUSbj → width: 8.75rem (SettingsLinkCopyAndRefreshRow.module.scss)
```

`IconButton` 컴포넌트 내부에서 `classnames(className, style.IconButton)`으로 두 클래스를 합치는 구조였다.

```tsx
// IconButton.tsx
<Button
    className={cx(className, style.IconButton, style[`IconButton--${size}`])}
    ...
>
```

**두 클래스 모두 단일 클래스 선택자(specificity: 0,1,0)** 로 동일한 우선순위를 가진다. 이 경우 CSS 캐스케이드는 **스타일시트 내 선언 순서**가 우선순위를 결정한다.

> DOM의 class 속성에서 클래스 순서는 CSS 우선순위에 영향을 주지 않는다. 오직 스타일시트 내 선언 순서만 중요하다.

---

### 3. dev vs prod 동작 차이

| 환경 | CSS 처리 방식 | 결과 |
|------|-------------|------|
| dev | 모듈별로 `<style>` 태그를 순서대로 주입 | `SettingsLinkCopyAndRefreshRow.module.scss`가 나중에 로드 → `8.75rem` 적용 ✅ |
| prod | 모든 CSS를 하나의 번들로 병합 | `IconButton` 스타일이 번들 내 더 나중 위치 → `2rem`으로 덮어씀 ❌ |

Next.js는 프로덕션 빌드 시 CSS 모듈을 페이지 단위 청크로 추출하고 합친다. 이 과정에서 **CSS 파일 병합 순서**가 개발 환경과 달라질 수 있다.

---

### 4. 왜 특정 시나리오에서만 깨지는가?

Next.js의 클라이언트 사이드 네비게이션(CSN) 방식 때문이다.

```
시나리오 A: 대시보드 직접 접근 (주소 입력 / 새로고침)
→ 페이지 CSS 번들이 한 번에 로드됨
→ 번들 내 IconButton이 나중에 선언됨 → width: 2rem 덮어씀 ❌

시나리오 B: 다른 페이지 → 대시보드 클라이언트 사이드 네비게이션
→ 이미 로드된 CSS 청크가 존재
→ 새 청크가 append되는 순서에 따라 copyBtn__img_wrapper가 더 나중 선언 → 정상 ✅
```

CSS 청크가 DOM에 주입되는 **시점과 순서가 진입 경로마다 다르기** 때문에 "가끔만" 재현되는 것처럼 보인다. 이것이 Next.js CSS ordering 이슈의 전형적인 패턴이다.

---

## 해결 방법 검토

### 방법 1: `!important` 사용

```scss
&__img_wrapper {
    width: 8.75rem !important;
    height: 100% !important;
}
```

간단하지만 CSS 유지보수성이 떨어진다. 추후 다른 재정의가 필요할 때 `!important` 연쇄가 생길 수 있다.

### 방법 2: specificity 올리기

```scss
&__img_wrapper:not(#_) {
    width: 8.75rem;
    height: 100%;
}
```

`:not(#_)` 가짜 id 선택자로 specificity를 `(0,2,1)`로 높여 `IconButton`의 `(0,1,0)`을 이기게 한다. 동작은 하지만 의도를 숨기는 트릭이다.

### 방법 3: 올바른 컴포넌트 사용 (채택)

근본 원인을 보면, 이 버튼은 **아이콘 + 텍스트** 조합인데 아이콘 전용 컴포넌트인 `IconButton`을 `tag`로 사용하고 있었다. 컴포넌트 선택 자체가 잘못된 것이다.

```jsx
// Before
<CopyButton
    tag={IconButton}   // ← 아이콘 전용 컴포넌트
    color="secondary"
    className={style.SettingsLinkCopyAndRefreshRow__copyBtn__img_wrapper}
    size={isPc ? 'md' : 'lg'}
>
    <CopyIcon />
    {!isMobile ? intl.formatMessage({ id: '...' }) : ''}
</CopyButton>

// After
<CopyButton
    tag={Button}       // ← 일반 버튼 컴포넌트
    color="secondary"
    className={style.SettingsLinkCopyAndRefreshRow__copyBtn__img_wrapper}
    size={isPc ? 'md' : 'lg'}
>
    <CopyIcon />
    {!isMobile ? intl.formatMessage({ id: '...' }) : ''}
</CopyButton>
```

`Button`은 이미 `@goorm-dev/vapor-components`에서 import되어 있었으므로, `IconButton` import 제거 + `tag` 변경만으로 충돌 원인 자체를 제거했다.

---

## 핵심 교훈

1. **CSS 모듈 클래스 간 specificity가 같으면 번들 순서에 의존하게 된다.** 프로덕션에서 클래스 간 순서는 보장되지 않는다.

2. **외부에서 재정의가 필요한 스타일을 컴포넌트 base 클래스에 넣지 말 것.** `IconButton`의 `width/height`처럼 외부에서 오버라이드해야 하는 값은 modifier 클래스(`--md`, `--lg`)에 분리하는 것이 안전하다.

3. **"dev에서는 되는데 prod에서만 깨진다"는 증상은 CSS 선언 순서 문제일 가능성이 높다.** 특히 진입 경로에 따라 재현 여부가 달라진다면 Next.js CSS 청크 로딩 순서를 의심하라.

4. **근본 원인을 먼저 확인하라.** `!important`나 specificity 트릭으로 덮기 전에, 컴포넌트 사용 자체가 올바른지 검토하면 더 깔끔한 해결책을 찾을 수 있다.
