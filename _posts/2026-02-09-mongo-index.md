---
title: MongoDB 인덱스 정리하다가 알게 된 복합 인덱스와 prefix rule
layout: post
---

최근 MongoDB 인덱스를 정리하면서 생각보다 많은 인덱스가 **의미 없이 중복**되어 있다는 걸 알게 됐다.

문제의 시작은 대부분 같았다. 복합 인덱스를 만들어두고,  “혹시 몰라서” single 인덱스를 같이 만들어 둔 상태였다.

---

### 내가 마주했던 인덱스 구조

실제로 이런 인덱스들이 있었다.

```js
{ userId: 1 }
{ userId: 1, isActive: 1 }
{ userId: 1, inviteeUsers.userId: 1, inviteeUsers.firstPurchase: 1 }
````

겉으로 보면 문제 없어 보이지만, 여기서 핵심은 **복합 인덱스가 이미 있다는 점**이다.

---

### 복합 인덱스는 어떻게 동작할까?

MongoDB의 복합 인덱스는 **왼쪽 필드부터 순서대로 조건이 맞아야 사용**된다.

예를 들어 인덱스가 아래와 같다면

```js
{ userId: 1, isActive: 1 }
```

MongoDB는 이 인덱스를 다음 두 가지 형태로 사용할 수 있다.

1. `{ userId }`
2. `{ userId, isActive }`

이걸 MongoDB에서는 **prefix rule**이라고 부른다.

---

### prefix rule 때문에 생기는 착각

이 규칙 때문에 아래 쿼리는

```js
{ userId: "u1" }
```

이미

```js
{ userId: 1, isActive: 1 }
```

이 복합 인덱스로 처리된다.

즉,

```js
{ userId: 1 }
```

이라는 single 인덱스는 **이미 역할이 겹친 상태**가 된다.

이걸 모르고 있으면 “userId로 자주 조회하니까 인덱스 하나 더 있어야겠지”라는 판단을 하게 된다.

결과는 중복 인덱스다.

---

### prefix rule이 안 먹히는 경우

prefix rule은 **왼쪽부터**라는 조건이 매우 중요하다.

```js
{ userId: 1, isActive: 1 }
```

이 인덱스가 있을 때

```js
{ isActive: true }
```

이 쿼리는 위의 인덱스를 탈 수 없다.

또한

```js
{ isActive: true, userId: "u1" }
```

처럼 조건이 있어도 **인덱스의 첫 필드가 빠지면 사용 불가**다.

쿼리의 작성 순서가 아니라 **인덱스 정의 순서**가 기준이다.

---

### 그래서 single 인덱스는 언제 필요할까?

복합인덱스에 설정이 되어있는 상태에서 single인덱스가 또 필요한 경우는 아래와 같다.

* 복합 인덱스가 아예 없을 때
* 복합 인덱스의 첫 필드가 아닐 때

그 외에는 대부분 복합 인덱스의 prefix로 충분히 커버된다.

---

### index: true가 만든 중복 인덱스

이번 정리에서 가장 아쉬웠던 부분은 이거였다.

```ts
@Prop({ index: true })
userId: string;
```

이 한 줄 때문에 MongoDB는 자동으로

```js
{ userId: 1 }
```

single 인덱스를 생성한다.

이 상태에서 schema-level로 복합 인덱스를 추가하면 의도하지 않은 중복 인덱스가 만들어진다.

---

### unique 인덱스는 예외
```js
{ code: 1, unique: true }
```

unique 인덱스는 조회 성능을 위한 최적화라기보다, 데이터 무결성을 강제하기 위한 제약이다.

MongoDB에서 unique 제약은 인덱스를 통해서만 보장되기 때문에, 조회 패턴과 상관없이 유지하는 것이 기본이다.

또한 unique는 single 인덱스뿐 아니라 복합 인덱스에도 적용할 수 있다.

예를 들어 아래 인덱스는
```js
{ userId: 1, provider: 1, unique: true }
```

userId와 provider의 조합이 중복되지 않도록 보장한다.

즉, unique 인덱스는 “쿼리에 쓰이냐”로 판단하기보다 도메인 제약(중복 허용 여부) 관점에서 유지 여부를 결정해야 한다.

---

### 한 줄 결론

> 복합 인덱스는 생각보다 많은 쿼리를 처리한다.
> prefix rule을 이해하면 불필요한 인덱스가 보이기 시작한다.
