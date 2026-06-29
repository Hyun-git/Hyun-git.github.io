---
layout: post
title: 분산 환경에서 결제를 안전하게 처리하는 방법 — 멱등성(Idempotency) 설계
date: 2026-06-10T10:00:00.000+09:00
---

과금 시스템을 구독제에서 사용량 기반으로 전환하면서 가장 먼저 마주친 문제는 "같은 청구가 두 번 나가면 어떡하지?"였다.

서버가 응답을 보내다가 죽는다. 클라이언트가 타임아웃으로 재시도한다. 외부 결제 모듈이 일시적으로 느려진다. 이런 상황에서 단순하게 구현하면 같은 결제가 두 번 처리된다.

이걸 막는 개념이 **멱등성(Idempotency)** 이다.

---

## 멱등성이란

같은 요청을 여러 번 보내도 결과가 달라지지 않아야 한다는 성질이다.

```
GET /user/123 → 멱등 (몇 번 호출해도 동일한 결과)
DELETE /user/123 → 멱등 (두 번째부터는 이미 없어서 동일)
POST /payment → 비멱등 (호출할 때마다 새 결제가 생긴다)
```

HTTP GET, DELETE는 기본적으로 멱등이지만 결제 같은 POST 요청은 명시적으로 설계해야 한다.

---

## 왜 분산 환경에서 더 중요한가

단일 서버라면 DB 레벨의 트랜잭션으로 어느 정도 막을 수 있다. 하지만 분산 환경에서는 다르다.

```
시나리오:
1. 사용량 집계 Cron이 실행됨
2. 외부 결제 API에 청구 요청 전송
3. 결제 API가 처리는 했지만 응답 전에 네트워크 끊김
4. Cron이 재시도
5. 결제가 두 번 처리됨
```

네트워크는 기본적으로 불신뢰(unreliable)하다. 응답을 받지 못했다고 해서 요청이 실패한 게 아닐 수 있다.

---

## 해결 방법: Idempotency Key

핵심 아이디어는 간단하다. **같은 요청을 식별할 수 있는 고유 키를 만들어서 붙인다.**

```ts
// 결제 요청 시 idempotencyKey 생성
const idempotencyKey = `billing:${userId}:${billingPeriod}`;

// Redis에 처리 여부 저장
const alreadyProcessed = await redis.get(idempotencyKey);
if (alreadyProcessed) {
  return JSON.parse(alreadyProcessed); // 이전 결과 그대로 반환
}

// 처리 전 점유 (atomic SET NX)
const acquired = await redis.set(idempotencyKey, 'processing', 'NX', 'EX', 300);
if (!acquired) {
  throw new Error('Already being processed');
}

try {
  const result = await externalPaymentApi.charge({ userId, amount });
  // 성공 결과를 저장 (TTL: 24시간)
  await redis.set(idempotencyKey, JSON.stringify(result), 'EX', 86400);
  return result;
} catch (err) {
  // 실패 시 키 삭제 (재시도 허용)
  await redis.del(idempotencyKey);
  throw err;
}
```

`SET NX`(Not Exists)를 쓰면 원자적(atomic)으로 처음 요청만 처리되도록 보장할 수 있다.

---

## Idempotency Key 설계 시 고려할 점

### 1. 키는 충분히 의미 있어야 한다

```ts
// ❌ 의미 없는 키 (재시도 시 다른 키가 생성됨)
const key = `billing:${Date.now()}`;

// ✅ 결제 주체와 기간으로 구성
const key = `billing:${userId}:${year}-${month}`;
```

### 2. 처리 중(processing) 상태를 별도로 관리한다

결제 처리 시간이 수 초 걸릴 수 있다. 이 사이에 같은 요청이 들어오면 "아직 처리 중"임을 구분할 수 있어야 한다.

```ts
type IdempotencyState = 'processing' | { result: PaymentResult };
```

### 3. TTL을 적절히 설정한다

결과를 영구적으로 보관할 필요는 없다. 합리적인 재시도 윈도우(예: 24시간) 이후엔 새 요청을 허용해도 된다.

### 4. 결제 API 자체도 Idempotency Key를 지원하는지 확인한다

Stripe 같은 외부 결제 모듈은 `Idempotency-Key` 헤더를 공식 지원한다. 우리 서버 레벨에서 막더라도, 외부 API에도 동일한 키를 전달하면 이중 보호가 된다.

```ts
await stripe.charges.create(
  { amount, currency: 'usd', source: token },
  { idempotencyKey: key }
);
```

---

## 실제 적용 후 달라진 것

Cron 재시도, 인프라 장애, 응답 타임아웃 등 다양한 실패 시나리오에서 이중 청구가 발생하지 않았다. 이전에는 중복 청구 건이 CS로 들어오면 수동으로 환불을 처리해야 했는데, 그 케이스가 사라졌다.

단순해 보이지만 결제처럼 돈이 오가는 API에서는 이 설계 하나가 신뢰성을 크게 좌우한다.

---

## 마무리

멱등성은 단순히 "중복을 막는 것"이 아니라 **"재시도를 안전하게 허용하는 것"** 이다.

재시도를 막으면 일시적인 장애에 취약해진다. 재시도를 허용하되 결과가 한 번만 일어나도록 보장하는 것이 목표다.

구독제에서 사용량 기반 과금으로 전환하면서 이 개념을 처음 제대로 설계하게 됐는데, 결제 외에도 이메일 발송, 알림 전송, 외부 API 연동 등 "딱 한 번만 일어나야 하는" 동작 어디에든 동일하게 적용된다.
