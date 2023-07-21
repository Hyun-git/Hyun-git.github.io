---
title: Mongodb lean() And exec()
layout: post
---

## 목차
- [Lean](#lean)
- [Exec](#exec)


`mongoose` 쿼리를 보게 되면 `<query>.lean().exec()` 과 같이 쿼리 뒤에 `lean(), exec()` 메소드가 붙어 있는 경우를 볼 수 있다. 해당 메소드들에 대해  궁굼한 점이 생겨 공부를 하게  되었다.
# Lean
- [공식문서](https://mongoosejs.com/docs/tutorials/lean.html)
- [참고한 블로그](https://choonse.com/2022/02/23/1000/)

`mongoose`의 리턴값은 `Document` 클래스의 인스턴스라고 한다.

해당 인스턴스는 많은 `state`를 가지고 있어 다양한 작업을 가능하게 한다.

예를 들어 `.get(), .set(), .toObject() ...`과 같이 리턴값에 대한 메소드 사용이 가능하고 해당 메소드에 대한 결과로 다시 쿼리를 진행하는 방식도 가능하다.

하지만 단지 결과 데이터를 목적으로 하는 `find()` 쿼리과 같은 작업에서는 결과값에 대해 추가로 작업을 하지는 않는다 . 이때 `lean()`을 사용하게 된다.

쿼리에  `lean()`을 추가하게 되면 인스턴스가 아닌 `POJO(Plain Old Javascript Object)`를 리턴하게 한다. 

> [POJO](https://ko.wikipedia.org/wiki/Plain_Old_Java_Object)  객체 지향적인 원리에 충실하면서 환경과 기술에 종속되지 않고, 필요에 따라 재활용될 수 있는 방식으로 설계된 오브젝트를 의미한다. 이러한 POJO에 애플리케이션의 핵심 로직과 기능을 담아 설계하고 개발하는 방법을 POJO 프로그래밍이라고 한다.

즉 메서드와 같은 데이터를 함께 반환하지 않으니 속도와 메모리면에서 큰 장점을 가지고 쿼리를 날릴 수 있게 되는 것이다.

# Exec
- [공식문서](https://mongoosejs.com/docs/tutorials/lean.html)
- [참고한 블로그](https://tesseractjh.tistory.com/166)

`find(), findOne() ...` 등의 리턴값은 `query`이다. 몽구스의 쿼리는 프로미스가 아닌 `then()`을 사용하는 유사 프로미스라고한다.

실제 뒤에 `exec()`를 붙이든 안붙이든 기능은 동일하다. 하지만 붙이게 되면 유사 프로미스가 아닌 완전한 프로미스를 얻을 수 있고 에러가 났을 때 `stacktrace`에 오류가 발생한 코드의 위치가 포함 되기에 공식 문서에서도 `exec()`를 사용할 것을 권장하고 있다.
