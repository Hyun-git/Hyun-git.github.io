---
title: "[Draft] socket.io transports 옵션과 sticky session"
layout: post
---

AI 사이드챗 소켓 연결이 가끔 느리거나 끊긴다는 이슈가 올라와서 들여다보다가, socket.io 클라이언트 쪽에 `transports` 옵션이 아예 빠져 있는 걸 발견해서 정리하게 되었다.

## 증상과 원인

문제의 소켓 생성 코드는 이랬다.

```javascript
const socket = io('/agent', {
  withCredentials: true,
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionAttempts: 10,
});
```

`transports`를 안 넘기면 socket.io v4 기본값인 `['polling', 'websocket']`이 적용된다. 즉 처음엔 polling으로 연결하고, 이후에 websocket으로 업그레이드하는 방식이다. 그런데 이 polling → websocket 업그레이드 과정은 핸드셰이크를 구성하는 여러 HTTP 요청이 반드시 같은 서버 인스턴스로 가야 한다는 전제가 깔려 있다. 다른 인스턴스로 튀면 `Session ID unknown` 에러가 난다.

![]({{ '/assets/images/socketio-handshake-fail.svg' | relative_url }})

우리 쪽엔 `@socket.io/redis-adapter`가 붙어 있어서 처음엔 "그럼 문제없는 거 아닌가" 싶었는데, redis adapter는 인스턴스 간 이벤트 브로드캐스트만 처리할 뿐 핸드셰이크가 같은 인스턴스로 가야 하는 문제 자체는 해결해주지 않는다. 지금은 그냥 ALB의 sticky session(로드밸런서 쿠키)에 의존해서 같은 파드로 계속 붙게 만드는 구조였다.

- [Socket.IO - Using multiple nodes](https://socket.io/docs/v4/using-multiple-nodes/)
- [Socket.IO - client initialization](https://socket.io/docs/v4/client-initialization/)

## sticky session이 안 먹히는 경우

dev 환경 ALB 타겟그룹을 실측해보니 쿠키 지속시간이 60초였다. 핸드셰이크 자체는 보통 수초 안에 끝나니까 대부분은 커버가 되긴 하는데, 그래도 몇 가지 구멍이 있었다.

→ 60초 안에 websocket 업그레이드가 안 끝나고 polling 통신이 이어지는 경우
→ sticky 대상 파드가 스케일인이나 노드 축출로 사라지는 경우
→ 클라이언트가 애초에 쿠키를 안 보내는 경우

이럴 때 요청이 다른 파드로 튈 확률은 대략 1/파드수다. 파드가 2개면 50%, 10개면 10%, 20개면 5%. 부하 테스트 기준(500명 회차)으로 HPA max가 20파드라서, 스케일이 늘어날수록 오히려 확률이 낮아지는 구조이긴 했다. socket.io가 핸드셰이크 실패 시 재시도는 해주기 때문에 연결 자체가 완전히 막히는 건 아니고, 재시도 횟수와 지연이 늘어나는 정도였다.

## 영향 범위가 생각보다 넓었다

`/agent` 네임스페이스만 고칠까 하다가, 혹시나 해서 같은 패턴이 코드베이스에 더 있는지 찾아봤다. `io()`를 호출하는 지점이 세 곳 있었는데 셋 다 `transports`가 빠져 있었다.

→ `/agent` 네임스페이스 소켓 (AI 사이드챗)
→ OT 협업 소켓 (별도 호스트로 붙는 크로스 오리진 연결)
→ 여러 도메인에서 재사용되는 공용 소켓 래퍼 클래스

이 중 공용 래퍼는 여러 곳에서 재사용되고 있어서 파급 범위가 제일 컸다. 반대로 서버-서버 내부 통신용 소켓 하나는 `transports: ['websocket', 'polling']`을 명시적으로 지정해두고 있어서 그건 문제가 없었다.

![]({{ '/assets/images/socketio-three-sockets.svg' | relative_url }})

## 적용한 수정과 트레이드오프

결국 세 곳 모두 `transports: ['websocket']`로 고정하는 쪽으로 갔다. polling 핸드셰이크 자체를 생략하니 sticky session 의존이 사라진다.

```javascript
const socket = io('/agent', {
  transports: ['websocket'],
  withCredentials: true,
  reconnection: true,
  reconnectionDelay: 1000,
  reconnectionAttempts: 10,
});
```

근데 이게 공짜는 아니었다. websocket이 막힌 네트워크(사내 프록시나 방화벽 같은)에서는 원래 polling으로라도 fallback돼서 느리게나마 연결이 됐는데, 이제는 fallback 자체가 없어서 연결이 완전히 실패한다. 별도 에러 UX도 없다 보니 그런 네트워크의 사용자한테는 기능이 조용히 안 되는 것처럼 보일 수 있다는 게 제일 걸리는 부분이었다.

그래서 `connect_error`를 서버로 올려서 error 레벨로 남기는 로그를 같이 추가했다. 원래는 `console.warn`으로만 찍혀서 서버 쪽에서 집계가 전혀 안 되고 있었다. 배포 후에 컨텍스트별(에이전트 소켓/협업 소켓/공용 소켓) 실패율을 실측해보고, websocket이 막힌 네트워크의 비중이 실제로 얼마나 되는지 지켜봐야 할 것 같다.

## 남는 확인 사항

협업 소켓은 크로스 오리진이라 첫 요청부터 바로 websocket 핸드셰이크가 되는데, 이 경우 인증 쿠키가 정상적으로 붙는지는 아직 별도로 확인하지 못했다. 또 `pingInterval`/`pingTimeout`을 커스텀하지 않아서 socket.io 기본값(25초/20초)을 쓰고 있는데, ALB idle timeout이 이보다 짧으면 유휴 상태의 websocket이 끊길 수 있고 지금은 fallback이 없으니 재연결이 온전히 websocket 재핸드셰이크에만 의존하게 된다. 이 부분은 인프라 쪽에 ALB idle timeout 값을 확인해달라고 요청해둔 상태다.
