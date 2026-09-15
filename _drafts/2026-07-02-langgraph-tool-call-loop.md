---
title: AI 에이전트의 Tool 호출 무한루프를 막는 방법 고르기
layout: post
---

요즘 맡고 있는 AI 에이전트 백엔드는 LangGraph 기반으로 동작하는데, 에이전트가 한 턴 안에서 tool을 계속 호출하다가 멈추지 않는 경우가 있었다. 무한루프까지는 아니어도 비정상적으로 긴 tool 호출 라운드가 이어지는 케이스가 실제로 관측되면서, 이걸 어떻게 막아야 할지 정리해볼 필요가 생겼다.

처음엔 그냥 `recursionLimit`을 낮추면 되는 거 아닌가 싶었는데, 막상 코드를 들여다보니 이게 그래프 전체의 superstep 상한값이라 tool 호출만 정조준하는 장치가 아니었다. 한도에 걸리면 `GraphRecursionError`가 그냥 throw되는데, 이 코드베이스 어디서도 이걸 catch하고 있지 않아서 사실상 unhandled exception으로 죽는 구조였다. 그래서 다른 방법이 있는지 좀 더 찾아봤다.

## recursionLimit / remainingSteps / ToolCallLimitMiddleware, 뭘 써야 하나

LangGraph 쪽에 tool 호출 제한과 관련된 옵션이 세 가지 정도 있었다.

- `recursionLimit`: 이미 코드에 있던 설정. 그래프 전체 스텝 상한이라 tool 호출이 아닌 다른 원인(예: 미들웨어 버그)으로 인한 루프도 같이 잡아준다는 장점은 있는데, 딱 tool 호출만 겨냥한 건 아니다.
- `remainingSteps`: 그래프 상태에 선언해두면 "recursionLimit까지 몇 스텝 남았는지"를 매 스텝 자동 계산해주는 파생값이다. 근데 이걸로 조기종료를 하려면 라우팅 로직을 직접 새로 짜야 한다. 값만 계산해줄 뿐 종료 자체는 안 해준다는 뜻이다. 상태 스키마 추가하고 라우팅 노드도 새로 만들어야 해서 엔지니어링 비용이 상대적으로 컸다.
- `ToolCallLimitMiddleware`: `langchain` 패키지에 이미 내장돼 있는 미들웨어다. `runLimit`(현재 턴 기준 tool 호출 수 제한)이나 `threadLimit`(스레드 전체 누적)으로 tool 호출만 정확히 제한할 수 있고, 미들웨어 배열에 추가만 하면 되니 구현 비용도 제일 작았다.

결국 `ToolCallLimitMiddleware`를 채택하기로 했다. 실패 모드를 tool 호출이라는 지점에 정확히 겨냥할 수 있다는 게 제일 컸고, `remainingSteps`로 직접 라우팅을 짜는 건 이 미들웨어가 이미 공식적으로 구현해둔 걸 재발명하는 셈이라 우선순위를 낮췄다. `recursionLimit`은 없앤 게 아니라 그대로 뒀다 — tool 호출이 아닌 다른 원인의 루프에 대비한 2차 안전망 정도로 남겨두는 게 맞다고 판단했다.

## exitBehavior를 고르는 과정에서 진짜 문제가 시작됐다

`ToolCallLimitMiddleware`는 한도를 넘겼을 때 어떻게 종료할지 `exitBehavior` 옵션으로 고를 수 있다. `continue`(초과분만 에러 메시지로 막고 모델이 스스로 멈추길 기다림), `end`(에러 메시지 남기고 정상 종료), `error`(throw) 세 가지였다.

제일 확실하게 끊어줄 것 같아서 처음엔 `end`로 시도했다. 로컬에서 "한 턴에 tool 하나만 호출해서 반복해라" 같은 프롬프트로 테스트했을 때는 3번까지 정상 실행되고 4번째에서 깔끔하게 막힌 뒤 `agent:complete`로 종료되는 게 확인됐다. 여기까지만 보면 문제없어 보였는데, 코드 리뷰 과정에서 치명적인 함정이 하나 발견됐다. 전역 리미터(toolName 지정 없는)에서 한도를 넘긴 턴의 tool_calls에 서로 다른 이름이 2개 이상 섞여 있으면, 라이브러리 내부에서 정상 종료 대신 그냥 throw해버리는 분기가 있었던 거다("Cannot end execution with other tool calls pending"). 이 프로젝트는 tool이 여러 개 있고 병렬 배치에 구조적 제약이 없어서, 실제로 발생할 수 있는 조건이었다. 즉 "한 턴에 tool 하나씩" 프롬프트로만 테스트했을 때 운 좋게 안 터졌던 거였다.

그래서 이번엔 항상 throw하는 `error`로 통일하고, 애플리케이션 코드에서 `ToolCallLimitExceededError`를 잡아 정상 종료로 변환하는 방식을 시도했다. 그런데 실제 개발 클러스터에서 돌려보니 더 심각한 게 나왔다.

```
TypeError: Cannot read properties of undefined (reading 'length')
    at Topic.isAvailable (.../channels/topic.ts:90)
    at Object._prepareNextTasks (.../pregel/algo.ts:506)
    at PregelLoop._first (.../pregel/loop.ts:1130)
```

![]({{ '/assets/images/langgraph-checkpoint-corruption.svg' | relative_url }})

원인을 추적해보니 미들웨어가 throw하면 LangGraph의 PregelRunner가 `_commit` 단계에서 같은 tick의 다른 task들은 정상적으로 커밋해버리고, throw한 task의 write만 버린다는 걸 알게 됐다. 그 결과 checkpoint의 TASKS(Topic) 채널이 반쪽만 기록되는 상태로 남는다. 문제는 여기서 끝나는 게 아니라, 한도에 한 번 걸린 스레드는 그 이후로 모든 요청이 저 에러로 영구히 실패한다는 거였다. 체크포인트가 이미 손상됐으니 복구가 안 되는 거다.

> jumpTo: 'end'는 return 기반의 정상 종료 메커니즘이고, throw로 강제 종료하는 건 LangGraph의 pregel 루프 안에서 근본적으로 다르게 처리된다.

결국 절대 throw하지 않는 `continue`로 다시 바꾸고, 차단이 감지되면 throw 없이 `return { jumpTo: 'end', ... }`로 그래프를 즉시 종료시키는 보조 미들웨어를 새로 하나 만들어서 조합했다. `afterModel` 훅은 미들웨어 배열 역순으로 실행되기 때문에, 이 보조 미들웨어를 `ToolCallLimitMiddleware`보다 배열상 앞에 둬야 한다는 것도 이번에 알게 됐다.

![]({{ '/assets/images/langgraph-continue-fix.svg' | relative_url }})

실제 API로 순차 호출과 멀티툴 배치 두 시나리오를 각각 새 스레드로 재현해서 검증했는데, 둘 다 크래시 없이 정상 종료됐고 같은 스레드로 후속 요청을 보냈을 때도 문제없이 재개됐다. 차단 시 나가는 안내 메시지("Tool call limit reached...")는 모델이 다시 생성한 응답이 아니라 미들웨어가 고정 문자열로 조립해 AIMessage로 주입하는 거라, 스트림상으로는 assistant 메시지처럼 보여도 실제로는 LLM 호출이 한 번도 더 일어나지 않는다는 점도 짚어둘 만한 것 같다.

리팩터링 끝나고 기존 jest 스위트(490개)를 전부 돌려봤는데 다행히 전부 통과했다. `runLimit` 기본값은 일단 30으로 잡아뒀는데, 이건 실제 트래픽 기준으로 p95/p99를 측정해서 다시 조정해야 할 임시값이라 당장 확정된 건 아니다.

돌이켜보면 `exitBehavior` 옵션 세 개가 겉으로는 그냥 "종료 방식 취향 차이" 정도로 보였는데, 실제로는 `end`와 `error` 둘 다 내부적으로 throw 경로를 갖고 있고 그게 LangGraph의 커밋 로직과 만나면 체크포인트가 반쪽으로 손상될 수 있다는 걸 문서만 봐서는 알기 어려웠다. 라이브러리 옵션 하나를 고르는 문제가 결국 pregel 루프의 커밋 방식까지 들여다봐야 하는 문제로 이어진 셈인데, 비슷한 미들웨어를 붙일 일이 있으면 exitBehavior류 옵션은 로컬 재현만으로 판단하지 말고 실제 환경에서 스레드를 재사용하는 시나리오까지 꼭 확인해봐야 할 것 같다.
