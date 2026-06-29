---
layout: post
title: 에러 로그 수백 건을 10건으로 줄인 방법 — Elasticsearch 로그 중앙화와 노이즈 제거
date: 2026-06-12T10:00:00.000+09:00
---

온콜 알림이 울렸다. Elasticsearch 대시보드를 열면 에러 로그가 수백 건씩 쌓여 있다. 그런데 정작 **진짜 장애**가 어디에 있는지 바로 보이지 않는다.

이게 한동안 반복됐다. 알림의 양이 많다 보니 점점 무감각해지고, 실제로 중요한 에러를 놓치는 일도 생겼다.

로그를 정리하기로 했다.

---

## 문제 진단: 노이즈가 많아진 원인

로그를 분석해보니 몇 가지 패턴이 반복됐다.

### 1. 재시도로 해결되는 일시적 오류

```
MongoNetworkError: connection timed out
```

MongoDB 커넥션 풀 재연결 과정에서 발생하는 일시적 에러였다. 3~5초 뒤 자동으로 복구되는데 에러 로그는 그대로 남는다. 실제 장애가 아니지만 로그는 매번 쌓인다.

### 2. 클라이언트 실수로 발생하는 4xx

```
400 Bad Request - Missing required field
401 Unauthorized - Token expired
```

서버 문제가 아닌데 error 레벨로 찍혀 있었다. 4xx는 기본적으로 클라이언트의 잘못이다.

### 3. 중복 로그

서비스 간 HTTP 호출에서 요청 서버와 응답 서버 양쪽이 같은 에러를 각각 기록하고 있었다.

---

## 접근 방법: 분류 → 필터링 → 집약

### 1단계: 에러를 분류한다

모든 에러를 같은 레벨로 다루지 않는다.

```
CRITICAL  → 즉시 대응 필요 (데이터 손실, 결제 실패, 서비스 중단)
ERROR     → 확인 필요 (예상치 못한 서버 오류)
WARN      → 알고는 있지만 자동 복구됨 (재시도 성공, 커넥션 재연결)
INFO      → 참고 정보 (일반 요청/응답)
```

기존에는 WARN 레벨이어야 할 것들이 ERROR로 찍혀 있었다.

### 2단계: 알려진 노이즈를 필터링한다

```ts
const NOISE_PATTERNS = [
  /connection timed out/,
  /ECONNRESET/,
  /socket hang up/,
];

function shouldSkip(errorMessage: string): boolean {
  return NOISE_PATTERNS.some(pattern => pattern.test(errorMessage));
}
```

재시도로 복구되는 일시적 네트워크 오류는 WARN으로 내리고, Elasticsearch에 별도 인덱스로 보낸다. 대시보드에서 기본으로 보이지 않게 한다.

### 3단계: 4xx는 에러로 취급하지 않는다

```ts
// Express 글로벌 에러 핸들러
app.use((err, req, res, next) => {
  const status = err.status || 500;

  if (status >= 500) {
    logger.error({ err, req }, 'Server error');
  } else if (status >= 400) {
    logger.warn({ err, req }, 'Client error'); // warn으로 내림
  }

  res.status(status).json({ message: err.message });
});
```

### 4단계: 로그 구조를 표준화한다

각 서비스마다 로그 포맷이 달랐다. 어떤 서비스는 `err.message`만, 어떤 서비스는 스택트레이스 전체를 문자열로 찍었다.

```ts
// 통일된 로그 포맷
logger.error({
  level: 'error',
  service: 'container-api',
  traceId: req.headers['x-trace-id'],
  userId: req.user?.id,
  error: {
    name: err.name,
    message: err.message,
    stack: err.stack,
  },
  request: {
    method: req.method,
    path: req.path,
    status,
  },
  timestamp: new Date().toISOString(),
});
```

`traceId`를 붙이면 여러 서비스에 걸친 요청을 하나로 추적할 수 있다.

---

## Elasticsearch 설정

### 인덱스 전략

에러 레벨별로 인덱스를 분리했다.

```
logs-critical-YYYY.MM
logs-error-YYYY.MM
logs-warn-YYYY.MM
```

대시보드 기본 뷰는 `logs-critical-*`, `logs-error-*`만 보이도록 설정한다. WARN은 별도로 조회할 때만 열어본다.

### 알림 임계값 조정

기존에는 에러 로그가 1건만 발생해도 알림이 왔다. 이걸 조정했다.

```
CRITICAL → 즉시 알림
ERROR → 5분 내 10건 이상 → 알림
WARN → 알림 없음 (대시보드에서만 확인)
```

---

## 결과

정리 전 / 후:

| | 전 | 후 |
|--|--|--|
| 일일 ERROR 로그 수 | 수백 건 | 10건 내외 |
| 온콜 알림 | 수시로 울림 | 실제 문제일 때만 |
| 장애 감지 시간 | 로그 뒤지다 파악 | 알림 → 즉시 특정 |

수치보다 실질적인 변화는 **로그를 신뢰하게 됐다는 것**이다. 알림이 오면 "또 노이즈겠지"가 아니라 실제로 확인해야 하는 상황이라는 공감대가 생겼다.

---

## 마무리

로그 정리는 코드를 바꾸는 작업이 아니다. 그래서 우선순위에서 밀리기 쉽다.

하지만 에러 대응이 느려지는 이유 중 하나는 정보가 부족해서가 아니라 **정보가 너무 많아서**다. 중요한 신호를 잡으려면 먼저 노이즈를 줄여야 한다.
