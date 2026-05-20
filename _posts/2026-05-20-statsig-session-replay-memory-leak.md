---
layout: post
title: Statsig Session Replay가 SPA를 2GB 먹던 날 — 브라우저 메모리 스냅샷으로 범인 찾기
date: 2026-05-20T12:00:00.000+09:00
---

## 발견

대시보드에서 인증 팝업창을 띄워놓고 원래 창을 보고 있었다. 로딩 스피너가 돌아가는 걸 기다리는 중이었는데, 시간이 지날수록 스피너 애니메이션이 점점 버벅이기 시작했다. 닫았다가 열어도 마찬가지였다.

Chrome DevTools의 Performance Monitor를 열어보니 JS heap size가 수백 MB에서 내려오지 않고 계속 우상향하고 있었다. 새로고침하면 정상, 탭을 전환하면 다시 폭증. 단순한 렌더링 이슈가 아니었다.

![Performance Monitor — JS heap size가 수백 MB에서 내려오지 않는다]({{ '/assets/images/brower_memory.png' | relative_url }})

---

## Step 1 — Heap Snapshot으로 무엇이 메모리를 먹는지 확인

Chrome DevTools → Memory 탭 → Heap Snapshot을 찍었다.

탭 전환 전과 후, 두 번 스냅샷을 찍고 Comparison 모드로 비교하자 두 개의 항목이 눈에 띄었다.

```
_saveFailedLogsToStorage    ~401 MB
wrap(e, t)                  ~400 MB
```

![Heap Snapshot Comparison — _saveFailedLogsToStorage와 wrap(e, t)가 400MB씩 차지]({{ '/assets/images/brower_memory2.png' | relative_url }})

두 항목 모두 Statsig SDK 내부에서 올라오고 있었다. `_saveFailedLogsToStorage`는 이름 그대로 "실패한 로그를 스토리지에 저장하는 함수"다.

Statsig SDK 소스를 추적해보니 흐름은 이랬다.

1. Statsig가 이벤트 로그를 서버로 flush 시도
2. flush 실패 시 localStorage에 백업 저장 시도
3. localStorage가 꽉 차면 (`QuotaExceededError`) → 메모리에 계속 쌓임
4. 동시에 rrweb이 DOM 변경사항을 끊임없이 캡처 → 버퍼가 계속 증가

`wrap(e, t)`는 rrweb의 이벤트 래핑 함수였다. rrweb은 `StatsigSessionReplayPlugin`이 내부적으로 사용하는 DOM 캡처 라이브러리다.

---

## Step 2 — rrweb이 왜 이렇게 많이 쌓이는가

`StatsigSessionReplayPlugin`은 초기화되는 순간부터 모든 DOM 변경을 연속으로 캡처한다. 이 서비스는 복잡한 SPA 대시보드로, 탭을 전환할 때마다 수백 개의 컴포넌트가 마운트/언마운트된다. rrweb 입장에서는 매번 거대한 DOM mutation event가 쏟아지는 것이다.

rrweb에는 sampling 옵션이 있다.

```js
rrwebConfig: {
  sampling: {
    mousemove: false,
    scroll: 300,
    input: 'last',
  },
}
```

하지만 이 옵션들은 포인터/스크롤/입력 이벤트에만 적용된다. DOM mutation 자체에는 throttle이 없다. 탭 전환 시 발생하는 대규모 렌더링은 sampling 설정과 무관하게 전부 캡처된다.

---

## Step 3 — 시도한 해결책들과 왜 안 됐는가

### 시도 1: production 환경에서만 Session Replay 활성화

dev 환경에서는 Statsig 서버와의 통신이 CORS 등의 이유로 실패하는 경우가 많다. 그래서 flush 실패 → localStorage 백업 실패 → 메모리 잔류라는 흐름이 dev에서만 발생하는 문제일 수 있다고 판단했다.

```js
const isProduction = process.env.NODE_ENV === 'production';

plugins: [
  ...(isProduction ? [new StatsigSessionReplayPlugin(...)] : []),
]
```

효과 없음. production 빌드에서도 동일하게 메모리가 폭증했다. 통신 실패가 원인이 아니라 rrweb의 연속 캡처 자체가 문제였다.

### 시도 2: 메모리 임계치 도달 시 `client.shutdown()` + reinit

```js
useEffect(() => {
  const checkAndReset = async () => {
    if (window.performance.memory.usedJSHeapSize < THRESHOLD) return;

    await client.shutdown();
    await client.initializeAsync();
  };

  const interval = setInterval(checkAndReset, 3000);
  return () => clearInterval(interval);
}, [client]);
```

200MB 임계치를 설정하고 초과 시 client를 재초기화했다. 로그상으로는 reset이 실행됐지만 결과는 이랬다.

```
[Statsig] heap: 2435.5MB → resetting
[Statsig] heap: 2860.0MB → resetting
[Statsig] heap:  573.0MB  ← GC가 한 번 돌았을 뿐
[Statsig] heap:  996.0MB  ← 다시 증가
```

`shutdown()` 이후에도 rrweb이 재초기화되면서 DOM 캡처를 즉시 재개했고, 탭 전환의 mutation 속도가 reset 속도를 압도했다. 수도꼭지를 잠그지 않고 물을 퍼내는 격이었다.

---

## 근본 원인

문제의 구조를 정리하면 이렇다.

```
탭 전환
  └→ 수백 컴포넌트 마운트/언마운트
       └→ 대규모 DOM mutation
            └→ rrweb이 모두 캡처 (버퍼에 적재)
                 └→ flush 실패 시 localStorage 백업 시도
                      └→ QuotaExceededError → 메모리에 잔류
                           └→ 힙 2GB+
```

`StatsigSessionReplayPlugin`은 세션 전체를 연속 녹화하는 방식이다. 단순한 정적 페이지에서는 문제가 없지만, 복잡한 SPA에서 빈번한 탭 전환이 발생하면 rrweb 버퍼가 감당할 수 없을 만큼 불어난다.

현재는 rrweb의 DOM mutation 캡처 자체를 제한하거나, 탭 전환 시점에 Session Replay를 일시 중단하는 방향을 검토 중이다. Statsig SDK가 이 수준의 제어를 공식적으로 지원하는지 확인이 필요하다.

---

## 핵심 교훈

1. **"Session Replay" SDK를 붙일 때는 연속 녹화인지 확인하라.** rrweb 계열 라이브러리는 DOM 전체를 실시간으로 직렬화한다. 복잡한 SPA에서 연속 녹화는 생각보다 훨씬 비싸다.

2. **rrweb의 sampling 옵션은 DOM mutation에는 적용되지 않는다.** `mousemove: false`, `scroll: 300` 같은 옵션은 포인터/스크롤/입력 이벤트에만 해당한다. 컴포넌트 마운트/언마운트로 발생하는 DOM 변경은 샘플링 없이 전부 캡처된다.

3. **Heap Snapshot Comparison 모드는 강력하다.** "뭔가 메모리를 많이 쓰는 것 같다"는 느낌을 실제 함수 이름과 크기로 특정하는 데 가장 효율적인 방법이었다. 버그 재현 전후로 스냅샷 두 장만 찍으면 범인이 보인다.

4. **메모리 누수는 막는 것이 퍼내는 것보다 낫다.** 주기적 reset, 임계치 reset 모두 근본 원인을 두고 증상만 건드린 것이었다.
