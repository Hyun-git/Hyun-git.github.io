---
title: 크레딧 정산 배치화
layout: post
---

그 부하테스트 즈음에 크레딧 정산 쪽도 손볼 일이 있었다. 부하테스트 중에 credit 서비스로 정산 요청이 갑자기 몰리는 걸 봤는데, 원인을 찾아보니 구조 자체가 문제였다.

## 뭐가 문제였나

로그를 실측해보니 (arkain_dev.credit_logs, 2시간 구간) 정산(use) 요청이 148,100건이었고 피크였던 21:50경에는 분당 9,555건, 초당으로 치면 159건 정도가 몰렸다. 501개 계정에서 나온 트래픽이었다.

원인을 찾아 코드를 보니 `agentEventHandler.js`에서 `agent:token:usage` 이벤트, 즉 Agent가 LLM을 호출할 때마다 배치나 디바운스 없이 매번:

1. `checkCreditExists` (GET) — 잔액 확인
2. `chargeLlmUsage` (PUT) — 실제 차감
3. hardQuota 대상 유저면 `getTotalLlmUsageByUserId` (GET) — 계정 전체 누적 재조회

이렇게 세 번의 왕복을 그대로 credit 서비스로 날리고 있었다. 턴 하나에 LLM 호출이 여러 번 일어나면 그 횟수만큼 이 왕복이 그대로 곱해지는 구조라, 부하테스트로 트래픽이 올라가니까 credit 서비스 쪽이 먼저 비명을 지른 셈이다.

![]({{ '/assets/images/credit-spike-graph.svg' | relative_url }})

## 배치로 바꾸기

LLM 호출이 일어날 때마다 매번 credit 서비스를 때릴 필요는 없다는 게 핵심이었다. → 호출마다는 Redis에 로컬로만 누적해두고 → 실제 credit 서비스로의 정산(PUT)은 아래 기준 중 하나를 만족할 때만 배치로 flush하도록 바꿨다.

- 주기 (5~10초)
- 턴/세션 종료 (에러나 drained로 끝나는 경우 포함)
- hardQuota 잔여 한도에 임계치 근접
- 누적 크레딧 크기가 일정 수준 이상
- 프로세스 종료 (SIGTERM)

hardQuota 초과 판정도 원래는 매번 `getTotalLlmUsageByUserId`로 외부에 물어보고 있었는데, 이것도 로컬 누적치로 즉시 판정하도록 바꿨다. 어차피 flush 시점에 실제 값과 동기화되니까 판정 자체를 외부 호출에 의존할 이유가 없었다.

![]({{ '/assets/images/credit-batch-before-after.svg' | relative_url }})

## 신경 쓴 부분

flush가 세션 도중에도, 프로세스가 죽을 때도 일어날 수 있다 보니 멱등성이 걱정이었다. 기존에 쓰던 `agentSettlementDedup` 패턴을 그대로 flush 단위에 적용해서, 같은 정산이 중복으로 나가는 걸 막았다. gracefulShutdown(disconnectAll) 쪽에도 배치 flush를 연결해서 프로세스가 종료될 때 누적된 게 유실되지 않게 했다.

## 남는 생각

호출마다 즉시 정산하는 구조가 데이터 정합성 측면에서는 제일 단순하긴 한데, 트래픽이 커지면 그 단순함이 그대로 부하로 돌아온다는 걸 이번에 다시 느꼈다. 로컬에 누적해두고 기준에 따라 묶어서 내보내는 방식이 credit 서비스 입장에서는 훨씬 부담이 적을 것 같다. 다만 flush 기준을 몇 개나 겹쳐놨더니 각 기준이 서로 레이스를 일으키지 않는지는 계속 지켜봐야 할 부분이다.
