---
title: 소켓 재연결과 lastEventId
layout: post
---

AI 채팅 기능에서 연결이 끊겼다가 재연결될 때 이벤트를 처음부터 다시 받아오는 문제가 있었는데, 이걸 고치는 과정에서 SSE랑 헷갈리는 부분이 있어서 정리하게 되었다.

상황은 이랬다. AI 채팅 기능이 재연결될 때마다 서버는 해당 대화의 이벤트를 처음(스트림 시작 지점)부터 다시 보내주고 있었다. 대화가 길어질수록, 그리고 재연결이 잦을수록 다시 보내는 양이 늘어나는 구조라 부하 테스트를 앞두고 문제로 제기됐다.

## "서버는 손댈 필요 없다"는 의견

이슈에 처음 달린 의견은 서버 쪽 수정이 필요 없다는 것이었다. 근거는 다른 스트림 기능이 이미 클라이언트가 마지막으로 받은 이벤트 id를 들고 있다가 재구독할 때 같이 보내는 방식으로 동작하고 있으니, AI 채팅 기능도 클라이언트 쪽에서 lastEventId만 들고 있으면 된다는 논리였다.

그럴듯해 보여서 실제 재구독 코드를 봤다.

```javascript
// 재구독 시 보내는 payload
socketRef.current.emit('agent:subscribe', { roomId, messageId });
```

lastEventId 자체가 없다. 서버는 lastEventId를 optional로 받아서 없으면 그냥 `'0-0'`(스트림 맨 처음)으로 처리하고 있었으니, 클라이언트가 안 보내면 무조건 전체 재전송이 되는 구조였다.

![]({{ '/assets/images/sidechat-reconnect-before.svg' | relative_url }})

## SSE는 원래 이런 걸 프로토콜이 챙겨준다

여기서 "다른 스트림 기능은 왜 서버 변경 없이 되는거지" 싶어서 그쪽을 다시 봤는데, 그건 진짜 SSE(Server-Sent Events)였다. SSE는 스펙 자체에 이벤트마다 `id:` 필드가 있고, 브라우저의 `EventSource`가 마지막으로 받은 id를 기억했다가 재연결할 때 `Last-Event-ID` 헤더에 자동으로 실어서 보낸다. 그러니까 클라이언트 코드가 따로 뭘 안 해도 "마지막으로 어디까지 봤는지"가 프로토콜 차원에서 왕복된다.

- [MDN - Using server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events)
- [WHATWG - Server-sent events (Last-Event-ID)](https://html.spec.whatwg.org/multipage/server-sent-events.html)

근데 AI 채팅 기능은 SSE가 아니었다. 소켓 위에 올린 커스텀 이벤트(`ws_event`)였다. 소켓 이벤트에는 SSE 같은 `id:` 개념이 프로토콜 차원에서 존재하지 않는다. 서버가 emit하는 payload에 명시적으로 id를 실어주지 않으면 클라이언트는 그 이벤트에 id가 있었는지조차 알 방법이 없다.

![]({{ '/assets/images/sidechat-sse-vs-socket.svg' | relative_url }})

실제로 서버 코드에서 이벤트를 내보내는 부분을 다 확인해봤는데, 세 곳 모두 payload가 `{event, data, roomId, messageId}` 뿐이었고 id 필드가 아예 없었다. 클라이언트도 마찬가지로 이벤트를 받을 때 `{event, data}`만 구조분해할당하고 있어서 id를 보내줬어도 애초에 보지 않는 상태였다.

즉 "클라이언트가 lastEventId를 들고 있다가 보내면 된다"는 전제 자체가 성립하지 않았다. 클라이언트는 애초에 lastEventId를 알 방법이 없었으니까. 서버 쪽 수정이 필요 없다는 판단은 틀렸던 거고, 서버가 id를 내려주는 것부터 먼저 되어야 했다.

## 실제로 고친 부분

서버는 이벤트를 emit하는 세 곳에 `id: event.id`를 추가했다.

```javascript
// 수정 후
socket.emit('ws_event', { event: eventType, data, roomId, messageId, id: event.id });
```

클라이언트는 messageId별로 마지막 이벤트 id를 기억하는 Map을 하나 두고, 이벤트를 받을 때마다 갱신하고, 재구독할 때 저장된 값이 있으면 payload에 실어 보내도록 바꿨다.

```javascript
// 재구독 시 보내는 payload (수정 후)
const lastEventId = lastEventIdByMessageIdRef.current.get(messageId);
socketRef.current.emit('agent:subscribe', { roomId, messageId, lastEventId });
```

서버가 lastEventId를 optional로 받아서 없으면 `'0-0'`으로 처리하는 부분은 원래도 있었으니 그건 그대로 뒀다. 그 부분에 대한 원래 판단은 맞았던 셈이다.

![]({{ '/assets/images/sidechat-reconnect-after.svg' | relative_url }})

## 남는 걱정

바꾸고 나서 좀 걸리는 부분이 하나 있었다. 원래는 재연결마다 통째로 다시 받아오다 보니, 클라이언트가 어떤 이벤트 처리에 조용히 실패해도 다음 재연결 때 우연히 복구가 되는 효과가 있었다. lastEventId를 보내기 시작하면 "여기까지 봤다"고 서버에 알려주는 셈이라 그 구멍을 재연결이 더 이상 자동으로 메워주지 않는다. 지금 코드에 그런 조용한 실패 사례가 실제로 있는지는 확인하지 못했고, 오히려 같은 id를 중복으로 받아도 무시하도록 되어 있는 걸 보면 어느 정도는 의도된 동작이었을 수도 있겠다 싶다. 이 부분은 좀 더 지켜봐야 할 것 같다.

![]({{ '/assets/images/sidechat-resend-comparison.svg' | relative_url }})

돌아보면 "비슷하게 생긴 다른 기능이 이렇게 동작하니까 우리도 그럴 것"이라는 유추가 문제였다. SSE와 커스텀 소켓 이벤트는 겉보기엔 둘 다 "서버가 클라이언트로 이벤트를 계속 밀어준다"는 점에서 비슷해 보이지만, "어디까지 받았는지"를 프로토콜이 대신 챙겨주느냐 아니냐는 완전히 다른 문제였다.
