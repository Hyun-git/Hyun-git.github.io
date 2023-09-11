---
title: Put Vs Patch
layout: post
---

코드리뷰를 진행하면서 CRUD의 HTTP update메소드인 Put 과 Patch가 헷갈리기 시작해서 관련 글을 쓰게 되었다.

먼저 CRUD의 Http 메소드에는 각각 뭐가 있는지 확안해보자


| CRUD OPERATION | HTTP REQUEST METHOD |
| -------- | -------- |
| Create    | post   |
|Read | get    |
| Update    | put, patch   |
| Delete    | delete    |

[RFC PATCH](https://datatracker.ietf.org/doc/html/rfc5789)
> Several applications extending the Hypertext Transfer Protocol (HTTP)
   require a feature to do partial resource modification.  The existing
   HTTP PUT method only allows a complete replacement of a document.
   This proposal adds a new HTTP method, PATCH, to modify an existing
   HTTP resource.

RFC 문서의 PTACH 메서드에 관한 내용을보면 Put 메서드는 온전한 Document의 update만을 허용한다고 말하고 Patch는 기존에 존재하는 HTTP resource를 수정한다고 말한다.

이걸 보면 나는 지금까지 update를 진행할 때는 patch 메서드만을 사용했어야하지 않나 싶다. Document를 통으로 바꿀일은 거의 없으니...

### PUT 메서드의 두가지 상황
1. 업데이트 할 Document가 존재하지 않을 경우

		단순히 POST 요청과 같게 넘겨준 정보들을 토대로 새로운 Document를 만들어 저장하고 HTTP Status Code 는 `201(CREATED)` 를 보내게 된다.
	
2. 업데이트 할 Document가 존재하는 경우

		payload에 담기 정보를  통해 새로운 Document를 만들어 기존에 존재하던 Document를 대체 한다. 이때 응답은 200(OK), 204(No Content)를 통해 알려주면 된다.
		
### PUT 메서드 사용 상황
PUT은 해당 정보가 없으면 생성해줘야하는 상황에서 사용하면 될 것 같다. 예를 들어 조직에 User를 초대하는 상황이 있다면 유저의 정보가 없다면 Document를 추가해주고 만약 권한 수정과 같은 상황에서도 사용하면 될 것 같다.
```
{
	id: userID,
	orgId: organizationID,
	permission: userPermission
}
```

위와 같은 field값을 가진 Document가 있다고 하면 아래와 같이 사용할 수 있을 것같다.
```
------- OrgUserRouter.js
app.put('/org/user', orgUserController.updateOrgUser);

------- orgUserController.js
exports const updateOrgUser = async (req, res) => {
	const { userId, orgId, permission } = req.body;
	
	const ret = await userService.updateOrgUser(userId, orgId, permission);
	
	res.json(ret);
}
```

### PUT 사용시 주의 사항
- PUT 메서드는 payload로만으로도 정보의 전체 상태를 나타낼 수 있어야한다.
- payload가 기존 정보를 대체하도록 구현되어있다면 일부 정보를 뺴고 보낸다면 일부 field값들이 null로 변경 될 수 있다.

### PATCH 사용
PATCH는 내가 생각하던 update와 똑같이 동작한다. 필요한 값들만을 보내 해당 값들에 해당하는 것만 update하게 된다. 물론 없던 값이라면 무시를 하고 PUT메서드와 다르게 추가를 하는 역할을 하지는 않는다. 

유저정보 수정과 같이 POST를 통해 Document를 생성하고 해당 정보를 수정할 때 많이 사용할 수 있을 것 같다.
```
{
	id: userID,
	pw: userPW,
	name: userName,
	email: userEamil,
	nickname: userNickname
}
-------- userRouter.js
app.update('/user', userController.updateUserNickname);

-------- userController.js
exports const updateUserNickname = async (req, res) => {
	const { nickname} = req.body;
	
	cosnt ret = await userService.updateUserNickname(nickname);
	
	res.json(ret)
}
```

### MongoDB의 $set
나는 주로 mongodb를 사용하는 입장에서 update 쿼리에서 `$set` 의 용도를 알고 싶었다.

#### `$set` 이 없는 경우
	PATCH 메서드 처럼 주어진 값만 업데이트를 하게 된다. 즉 없는 field값을 업데이트를 하려고 하면 무시를 하고 진행을 한다.

#### `$set`이 있는 경우
	PUT메서드처럼 Document 전체를 바꾸지는 않지만 없는 field를 넣게 되면 새로 만들어주는 역할을 하게 된다. Nosql이기에 field에 대한 자유도 때문에 만들어준 것 같다.
		
### 결론
`PUT과 PATCH를 잘 구별하자 PUT을 사용할 때는 더욱 조심하자!`
