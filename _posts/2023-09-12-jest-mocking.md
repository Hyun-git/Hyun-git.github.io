---
title: Jest_mocking
layout: post
---

### mocking
먼저 `mock`이란 모조품이라는 뜻으로 `mocking`은 테스트를 독립시키기 위해 의존성(일반적으로 import하는 모듈들)들을 개발자가 컨트롤하고 검사할 수 있는 오브젝트로 바꾸는 것을 말한다.

만약 `mocking`을 하지 않고 직접 의존성들을 사용해서 테스트를 하게 되면 아래와 같은 문제점이 있을 수 있다.
- 의존성(예를들어 데이터베이스나 다른 앱)들에서 정보를 가져오는 것은 속도가 확실히 느리기에 Testing 속도를 현저하게 저하 시킬 수 있다.
- 또한 테스트에서 사용했던 정보들을 다시 초기화 해줘야하는 것에 많은 노력과 시간이 들어간다.
- 테스트를 위한 직접적인 코드를 작성해 줘야하는데 노력과 시간이 들어간다. 의존성에서 문제가 생기면 테스트 자체가 무의미해진다.
- 이중 제일 문제는 특정 로직만을 테스트를 하기 원하는 단위 테스트의 본질에서 벗어난다.

`mocking`은 이런 상황에서 실제 처럼 행동하는 것처럼 보이는 가짜 객체를 생성해준다. 또한 테스트가 존재하는 동안 해당 객체가 어떤 동작을 했는지 기억하기에 검증을 진행할 수 있게 해준다.


### jset.fn()
jest에서는 mock function을 생성할 수 있도록 `jest.fn()`함수를 제공합니다.
```
const mockFn = jest.fn();

mockFn() //undefined
mockFn(1) //undefined
mockFn("a") //undefined
```
아직 어떤 결과같을 가질지 알려주지 않았기에 결과값은 모두 `undefined`로 나오게 된다.
```
mockFn.mockReturnValue("I am a mock!");
mockFn() // I am a mock

mockFn.mockResolvedValue("I am a mock!");
mockFn().then((result) =>
	console.log(result) // I am a mock!
}
mockFn.mockImplementation((name) => `I am ${name}!`);
console.log(mockFn("Dale")); // I am Dale!
```
`mockReturnValue` 이걸로 mock 함수의 return 값을 선언해줄 수 있다.
`mockResolvedValue` 이걸로는 Promise로 return 하는 값을 선언해줄 수 있다.
`mockImplementation` 이걸로는 아예 함수를 구현해볼 수 있다.


### jest.spyOn()
jest에서 일부 함수들의 구현을 가짜로 대체하지 않고 해당 함수의 호출 여부와 어떻게 호출 되었는지만을 알아내야할 때 사용한다. 즉 기존 함수에 spy를 붙여 어떻게 실행이 됐는지 감시를 할 수 있게 한다고 보면 된다.
```
const calculator = {
  add: (a, b) => a + b,
};

const spyFn = jest.spyOn(calculator, "add");

const result = calculator.add(2, 3);

expect(spyFn).toBeCalledTimes(1); //true
expect(spyFn).toBeCalledWith(2, 3); //true
expect(result).toBe(5); //true
```

### jest.fn() vs jest.spyOn()
- `jest.fn()`는 새로운 가짜 함수를 생성하고 주로 함수를 완전히 대체 하거나 함수 호출에 대한 반환값을 제어하기 위해 사용된다.
- `jest.spyOn()`은 이미 존재하는 객체의 메서드 또는 함수를  mocking 하거나 추적하기 위해 사용 된다.
	- 이때 실제 구현은 유지한 체ㅐ로 해당 함수 호출 정보를 추첮하고 반환값을 조작할 수 있다.

둘다 사용하는 예제
```
// 외부 의존성: axios 모듈을 모의(Mock)화
const axios = require('axios');

// 내부 메서드: 특정 기능을 수행하는 함수
function fetchDataFromAPI() {
  return axios.get('https://api.example.com/data');
}

// 테스트 스위트
describe('Example Test Suite', () => {
  // axios.get을 모의(Mock)하고 반환값 설정
  const axiosGetMock = jest.fn();
  axios.get = axiosGetMock;

  // fetchDataFromAPI 함수 내부에서 axios.get을 스파이(Spy)
  test('fetchDataFromAPI should make a network request', async () => {
    // axios.get 스파이(Spy) 설정
    axiosGetMock.mockResolvedValue({ data: 'mocked data' });

    // fetchDataFromAPI 함수 호출
    const result = await fetchDataFromAPI();

    // axios.get이 호출되었는지 확인
    expect(axiosGetMock).toHaveBeenCalled();

    // 결과 확인
    expect(result.data).toBe('mocked data');
  });

  // 내부 메서드의 동작 테스트
  test('internal method should work', () => {
    // 내부 메서드 호출
    const result = internalMethod();

    // 결과 확인 및 검증 로직 추가
    expect(result).toEqual(/* 기대값 */);
  });
});
```

참조
- [Jest의 jest.fn(), jest.spyOn()를 이용한 함수 모킹](https://www.daleseo.com/jest-fn-spy-on/)
- [[번역] Jest Mocks에 대한 이해](https://minoo.medium.com/%EB%B2%88%EC%97%AD-jest-mocks%EC%97%90-%EB%8C%80%ED%95%9C-%EC%9D%B4%ED%95%B4-34f75b0f7dbe)
