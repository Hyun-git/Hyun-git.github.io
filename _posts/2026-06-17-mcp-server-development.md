---
layout: post
title: MCP 서버를 직접 만들어보면서 알게 된 것들 — 자연어로 인프라를 제어한다는 게 실제로는 어떤 의미인가
date: 2026-06-17T10:00:00.000+09:00
---

"자연어로 컨테이너를 제어할 수 있게 해주세요."

이 한 줄의 요구사항으로 MCP(Model Context Protocol) 기반 사이드챗을 만들게 됐다. 처음엔 단순해 보였다. LLM에 도구 몇 개 연결하면 되지 않을까. 막상 해보니 생각보다 고려해야 할 게 많았다.

---

## MCP란 무엇인가

Anthropic이 공개한 MCP(Model Context Protocol)는 LLM이 외부 도구나 데이터 소스에 접근하는 방식을 표준화한 프로토콜이다.

쉽게 설명하면, LLM에게 도구 목록을 주고 "이 도구들을 필요에 따라 써서 사용자 요청을 처리해라"고 하는 것이다.

```
사용자: "내 컨테이너 몇 개야?"

LLM 판단: 컨테이너 목록을 가져오는 도구가 필요함
→ listContainers 도구 실행
→ 결과: [{ id: "c1", name: "my-api", status: "running" }, ...]
→ LLM: "현재 실행 중인 컨테이너는 1개입니다. my-api가 running 상태입니다."
```

도구 실행과 언어 처리가 분리된다는 게 핵심이다.

---

## 아키텍처: 왜 4개의 컴포넌트로 나눴나

처음엔 LLM ↔ 백엔드를 직접 연결하려 했다. 하지만 몇 가지 문제가 있었다.

**1. 보안**: LLM에 내부 인프라 API를 직접 노출하면 안 된다.  
**2. 책임 분리**: 언어 처리, 도구 결정, 인프라 제어, UI 표현이 뒤섞이면 유지보수가 어렵다.  
**3. 확장성**: 나중에 다른 LLM 모델로 교체하거나 도구를 추가할 때 영향 범위를 줄여야 한다.

결국 이렇게 나눴다.

```
Frontend (UI)
  ↕
MCP-Client (도구 판단 및 조율)
  ↕                ↕
AI-Proxy-Server   Resource Controller
  ↕
LLM (외부)
```

- **Frontend**: 대화 UI + 응답 유형에 따른 렌더링 (코드 하이라이팅, 관련 페이지 이동)
- **AI-Proxy-Server**: 프롬프트 설계, 응답 가공, 민감 정보 필터링
- **MCP-Client**: 사용자 요청 분석, 필요한 도구 선택, 컨트롤러와 AI 사이 조율
- **Resource Controller**: 실제 인프라 제어 도구 정의 및 내부 API 연동

---

## 도구 정의가 핵심이다

MCP에서 도구를 어떻게 정의하느냐가 LLM의 판단 품질을 결정한다.

```ts
const listContainersTool = {
  name: 'listContainers',
  description: '사용자의 컨테이너 목록을 가져옵니다. 컨테이너 상태 조회나 현황 파악이 필요할 때 사용합니다.',
  inputSchema: {
    type: 'object',
    properties: {
      status: {
        type: 'string',
        enum: ['running', 'stopped', 'all'],
        description: '조회할 컨테이너 상태. 기본값은 all',
      },
    },
  },
};
```

`description`을 정확하게 쓰는 게 중요하다. LLM은 이 설명을 보고 도구를 호출할지 말지 판단한다. 모호하게 적으면 엉뚱한 도구를 호출하거나 필요한 도구를 쓰지 않는다.

실제로 "실행 중인 컨테이너 목록 보여줘"와 "컨테이너 상태 어때?"가 같은 도구로 연결되도록 description을 여러 번 고쳤다.

---

## 민감 정보 필터링 — LLM에 뭘 보내면 안 되나

컨테이너 목록을 가져오면 내부 ID, IP, 환경변수 등이 함께 딸려온다. 이걸 그대로 LLM에 보내면 안 된다.

```ts
// AI-Proxy-Server에서 필터링
function sanitizeForLLM(containerData: Container[]): SafeContainerData[] {
  return containerData.map(c => ({
    name: c.name,
    status: c.status,
    lastAccessedAt: c.lastAccessedAt,
    // id, ip, env는 제외
  }));
}
```

필터링이 필요한 필드 목록을 명시적으로 관리했다. 기본은 제외, 필요한 것만 허용(allowlist) 방식으로.

---

## 도구가 필요 없을 때 프록시를 건너뛴다

모든 요청이 도구 실행을 거치는 건 낭비다. "안녕하세요"나 "컨테이너가 뭔가요?" 같은 질문은 인프라 조회 없이 LLM이 바로 답할 수 있다.

MCP-Client가 먼저 판단한다.

```ts
async function handleUserQuery(query: string) {
  const toolRequired = await llm.classify(query, availableTools);

  if (toolRequired) {
    const toolResult = await resourceController.execute(toolRequired);
    return aiProxy.generateWithContext(query, toolResult);
  } else {
    return aiProxy.generateDirect(query);
  }
}
```

이렇게 하면 불필요한 인프라 조회가 줄고, 응답 속도도 빨라진다.

---

## 실제로 막혔던 것들

### JSON-RPC 에러 처리 표준화

MCP는 JSON-RPC 2.0 스펙을 따른다. 에러 코드를 표준에 맞게 관리하지 않으면 클라이언트에서 원인 파악이 어렵다.

```ts
// JSON-RPC 표준 에러 코드
const JSONRPC_ERRORS = {
  PARSE_ERROR: -32700,
  INVALID_REQUEST: -32600,
  METHOD_NOT_FOUND: -32601,
  INVALID_PARAMS: -32602,
  INTERNAL_ERROR: -32603,
};
```

초반에 에러 형식을 통일하지 않아서 LLM이 실패 응답을 성공으로 인식하는 문제가 있었다.

### 외부 지식 베이스 응답 파편화

제품 가이드를 RAG로 연동했는데, 외부 API 응답 형식이 일정하지 않았다. 같은 질문인데 응답 구조가 달라오는 경우가 있어서 정제 레이어를 별도로 뒀다.

```ts
function normalizeKnowledgeBaseResponse(raw: KBResponse): string {
  if (Array.isArray(raw.results)) {
    return raw.results.map(r => r.content).join('\n\n');
  }
  return raw.answer ?? raw.text ?? '';
}
```

---

## 마무리

MCP를 쓰면 LLM이 알아서 판단해주기 때문에 개발이 쉬울 것 같지만, 실제로는 설계가 더 중요해진다.

도구 설명이 부정확하면 LLM이 잘못 판단한다. 필터링이 빠지면 보안 문제가 생긴다. 에러 처리가 불명확하면 LLM이 실패를 성공으로 인식한다.

결국 "LLM이 올바르게 판단할 수 있도록 컨텍스트를 얼마나 잘 설계하느냐"가 MCP 기반 서비스 개발의 핵심이었다.
