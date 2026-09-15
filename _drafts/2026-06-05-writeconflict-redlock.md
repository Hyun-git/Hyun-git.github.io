---
title: "[Draft] WriteConflict 재시도와 결제 동시성 락"
layout: post
---

크레딧 결제 쪽 코드를 손보다가 같은 유저가 짧은 간격으로 요청을 두 번 보내면 MongoDB에서 WriteConflict가 나는 걸 발견했고, 비슷한 시기에 이벤트 결제 중복 지급 문제도 같이 다루게 돼서 정리해둔다.

### WriteConflict부터

LLM 크레딧 차감 API(`PUT /{userId}/credit/llm/use`)는 유저 크레딧 document를 직접 업데이트하는 구조라, 동일 유저가 거의 동시에 요청을 두 개 이상 보내면 같은 document를 두 트랜잭션이 건드리게 되고 몽고DB가 WriteConflict를 던진다. 처음엔 그냥 에러를 그대로 클라이언트에 흘려보냈는데, 사이드챗에서 tool call이 여러 번 겹쳐서 나가는 케이스가 있다 보니 실패가 꽤 자주 보였다.

그래서 재시도 로직을 넣었다. exponential backoff + jitter로, 최대 5회(`WRITE_CONFLICT_MAX_RETRIES`)까지 재시도하고 기본 대기 시간은 500ms(`WRITE_CONFLICT_BASE_DELAY_MS`)로 상수화했다. jitter를 뺀 순수 backoff만 쓰면 동시에 충돌났던 두 요청이 다음 재시도 타이밍까지 똑같이 맞물려서 또 충돌하는 경우가 생길 수 있어서, 랜덤값을 섞어 재시도 시점을 흩어놓는 식으로 했다.

만료 크레딧을 정리하는 일단위 크론 쪽도 비슷한 문제가 있었는데, 여기는 여러 유저를 순차로 처리하다 보니 한 명에서 WriteConflict가 나면 그 뒤 유저들 처리가 아예 막히는 구조였다. `Promise.allSettled`로 바꿔서 한 유저 처리가 실패해도 나머지는 계속 진행되게 했다. 다만 실패한 유저에 대한 별도 로깅이 빠져 있어서 나중에 추적하려면 좀 불편할 것 같긴 하다.

![]({{ '/assets/images/writeconflict-retry-timeline.svg' | relative_url }})

### 이벤트 결제 동시성은 좀 다른 문제였다

WriteConflict 재시도는 결국 "실패해도 다시 시도하면 된다"는 전제가 깔려 있는데, 이벤트 크레딧 구매(최초 1회 한정 보너스 지급)는 그렇게 처리하면 안 되는 케이스였다. 동시에 결제 요청이 두 번 들어오면 재시도가 아니라 하나는 아예 막아야 한다.

그래서 결제 시작 시점에 Redis Redlock을 걸고, 결제 승인이 끝날 때까지 유지하다가 크레딧 지급 후에 풀어주는 방식으로 했다. 여기서 좀 애매했던 부분이, 결제 승인 자체는 FE가 PG사(Stripe 등)랑 직접 통신해서 받아오는 구조라 백엔드가 그 사이 lock 객체를 계속 메모리에 들고 있을 수가 없다는 점이었다. → lock을 걸 때 나온 random value를 그대로 버리지 않고 `ide_event_logs.lockValue`에 저장해뒀다가, 결제 완료 콜백이 왔을 때 그 값을 다시 꺼내와서 unlock 하는 식으로 처리했다.

![]({{ '/assets/images/redlock-timeline.svg' | relative_url }})

이전에 비슷한 문제를 큐로 풀지 락으로 풀지 고민했던 설계 문서가 남아있길래 봤는데, 그때는 Kafka 큐로 순차 처리하는 안이랑 Redis에 user_id 기준으로 락 거는 안을 같이 검토했었고 결국 락 쪽으로 정리된 것 같다. 큐는 이벤트 상품 아닌 일반 결제까지 전부 순차 처리를 타게 만들어야 해서 오버였다는 판단이었던 듯하다.

그 뒤로 락이 걸려서 결제가 막힌 경우 응답 코드를 500번대가 아니라 400번대로 바꾸는 작업도 따로 있었다. 서버 에러로 잡히면 불필요한 장애 알림이 날아가는데, 사실은 클라이언트 쪽 정상적인 충돌 케이스라 400으로 내려야 맞았다. 그리고 productId를 조작해서 이벤트 보너스 상품을 정상가로 결제한 것처럼 우회하는 사례도 있어서, 결제 승인 단계에서 productId validation을 추가한 기록도 있다. 국내 결제는 PG사가 productId를 따로 검사하지 않고 바로 approve로 넘어가는 구조라 서버단 검증이 빠져 있으면 그대로 뚫리는 구조였다.

락과 재시도 둘 다 결국 "동시에 같은 자원을 건드릴 때 뭘 할지" 정하는 문제인데, 재시도로 흡수해도 되는지 아니면 아예 하나를 막아야 하는지는 그 자원이 멱등하게 다시 계산될 수 있는지에 따라 갈리는 것 같다.

### 참고

- [MongoDB WriteConflict](https://www.mongodb.com/docs/manual/core/wiredtiger/#concurrency-control)
- [Redlock 알고리즘](https://redis.io/docs/latest/develop/use/patterns/distributed-locks/)
