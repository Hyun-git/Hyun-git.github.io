---
title: NestJS에서 파라미터 검증 순서 이해하기
layout: post
---

### Global Pipe가 먼저 실행된다는 사실이 만드는 차이

NestJS에서 요청 파라미터를 검증할 때 우리는 보통 `Pipe`를 사용한다.
하지만 **Pipe가 어떤 순서로 실행되는지**를 정확히 이해하지 못하면,
불필요한 로직이 실행되거나 성능상 손해를 보는 구조가 될 수 있다.

이번 글에서는 실제 코드 리뷰에서 받은 피드백을 계기로,
**NestJS의 파라미터 검증 순서(Request Lifecycle)**와
**Global Pipe와 Route Param Pipe의 차이**를 정리해본다.

---

## 문제의 시작: Param Pipe에 모든 책임을 맡긴 구조

초기 구현은 아래와 같았다.

```ts
@Post(':userId')
async getOrCreateReferralCode(
  @Param('userId', UserExistsPipe) userId: string,
): Promise<ReferralCodeResponse> {
  const referralUser =
    await this.referralService.getOrCreateReferralCode(userId);
}
```

`UserExistsPipe`는 다음과 같은 책임을 가지고 있었다.

* `userId`가 유효한 형식인지 확인
* 실제로 해당 유저가 존재하는지 DB 조회

겉보기에는 문제 없어 보이지만, 코드 리뷰에서 다음과 같은 코멘트를 받았다.

---

## 코드 리뷰 피드백 핵심

> global pipe가 route params pipe 보다 더 먼저 동작하기 때문에
> params를 dto로 만들어 기본적인 것들을 미리 검증하면
> global pipe에서 먼저 걸러져서 불필요한 UserExistsPipe 로직 실행을 막을 수 있을 것 같아요.

이 코멘트의 핵심은 **NestJS의 Pipe 실행 순서**에 있다.

---

## NestJS Request Lifecycle과 Pipe 실행 순서

NestJS에서 요청이 들어오면, 대략 아래 순서로 처리된다.

1. **Middleware**
2. **Guard**
3. **Interceptor (before)**
4. **Pipe**

   * Global Pipe
   * Controller
   * Route Pipe
   * Param Pipe
5. **Controller Handler 실행**
6. **Interceptor (after)**

**중요한 포인트**

> **Global Pipe는 Param Pipe보다 먼저 실행된다**

즉,

* `@Param('userId', UserExistsPipe)` → **Global ValidationPipe 이후에 실행**
* `@Param() DTO`→ **Global ValidationPipe 단계에서 검증 가능**

---

## 기존 코드의 문제점

기존 구조에서는 이런 일이 발생한다.

`userId`가 숫자가 아닌 문자열이거나 아예 형식이 잘못된 값이 와도 **UserExistsPipe가 무조건 실행됨**
→ DB 조회 발생

즉, **형식 검증과 비즈니스 검증이 섞여 있고**,
DB 조회가 필요 없는 경우에도 실행이 된다고 생각이 되었다.

---

## 해결 전략: Param을 DTO로 만들고 검증 책임 분리

리뷰를 반영해, 파라미터를 DTO로 분리했다.

### Param DTO

```ts
export class ReferralUserParamDto {
  @IsString()
  @IsNotEmpty()
  userId: string;
}
```

### 변경된 컨트롤러 코드

```ts
@Post(':userId')
@UsePipes(UserExistsPipe)
async getOrCreateReferralCode(
  @Param() params: ReferralUserParamDto,
): Promise<ReferralCodeResponse> {
  const referralUser =
    await this.referralService.getOrCreateReferralCode(params.userId);
}
```

---

## 이 구조의 실행 흐름

요청이 들어오면 다음 순서로 동작한다.

1. **Global ValidationPipe**

   * `ReferralUserParamDto` 검증
   * `userId` 타입 / 빈 값 여부 확인
   *  실패 시 여기서 바로 400 응답
2. **UserExistsPipe 실행**

   * DTO 검증을 통과한 경우에만 실행
   * 실제 유저 존재 여부 확인
3. **Controller Handler 실행**

결과적으로,

* 잘못된 요청은 **DB 조회 없이 차단**
* Pipe의 역할이 명확해짐

  * DTO: 구조·형식 검증
  * UserExistsPipe: 비즈니스 검증

---

## 얻은 인사이트

### 1. Pipe는 “무엇을 검증하는가”보다 “언제 실행되는가”가 중요하다

NestJS에서는 **실행 순서를 모르면 설계가 꼬이기 쉽다.**

### 2. Param Pipe에 모든 검증을 몰아넣지 말자

* 형식 검증 → DTO + Global Pipe
* 비즈니스 검증 → Custom Pipe

### 3. DTO는 Body뿐 아니라 Param에서도 적극적으로 쓰자

특히 **트래픽이 많거나 DB 조회가 포함된 Pipe**라면 필수에 가깝다.
