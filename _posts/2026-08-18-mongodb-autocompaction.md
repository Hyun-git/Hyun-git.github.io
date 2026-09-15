---
title: MongoDB AutoCompaction
layout: post
---

프로덕션 MongoDB 클러스터에서 TTL Index로 대량 삭제를 했는데 디스크 사용량이 그대로인 걸 보고 이상해서 들여다보게 되었다. 삭제된 문서 수는 0이 됐는데 왜 디스크는 그대로인지 궁금해서 원인을 찾아보기로 했다.

## 재현부터

말로만 봐서는 확신이 안 서서 직접 테스트 컬렉션을 만들어 재현해봤다. 더미 문서를 GB 단위로 쌓고 TTL Index를 걸어서 일정 시간 뒤 자동 삭제되게 한 다음, 삭제 전후로 `db.stats()`, `db.collection.stats()` 지표를 비교하는 방식이다. 처음엔 5GB로, 그 다음엔 12GB로 규모를 키워서 두 번 돌려봤다.

![]({{ '/assets/images/mongo-autocompaction-disk-trend.svg' | relative_url }})

1차 테스트에서 TTL로 문서를 전부 지우고 나서 확인해보니 `count`는 0인데 `storageSize`는 3.4GB 그대로였다. `freeStorageSize`가 3.2GB로 잡혀있어서 내부적으로는 "재사용 가능"한 공간으로 표시는 되어 있는데, 실제 파일 크기(`fsUsedSize`)는 꿈쩍도 안 했다.

## compact를 먼저 의심했다

디스크가 안 줄어드는 거니까 가장 먼저 떠오른 건 수동 compact였다. `db.runCommand({compact: "test", force: true})`로 돌려봤는데 `bytesFreed: 0`. 완전히 빈 컬렉션인데도 회수되는 바이트가 0이라는 게 이해가 안 갔다.

![]({{ '/assets/images/mongo-autocompaction-stats-compare.svg' | relative_url }})

혹시 백업 커서나 오래 걸리는 트랜잭션이 물고 있는 건 아닌가 싶어서 `db.currentOp()`도 확인했는데 그런 것도 없었다.

## autoCompact 설정도 봤다

MongoDB 8.0부터 `autoCompact`라는 옵션이 생겼다는 걸 알게 되어서, 검증을 위해 dev 클러스터를 8.0으로 올리고 켜봤다. Production은 아직 7.0대였어서 이 기능 자체를 쓸 수 없는 상태였다. autoCompact를 켜고 한참 관찰했는데 자동으로 회수되는 게 전혀 없었다. 세 개 노드 다 마찬가지였다.

이 시점에서 test 컬렉션 자체가 문제가 아닐 수도 있겠다는 생각이 들어서 `db.test.drop()`으로 확인해봤다. 그런데 drop을 했는데도 `fsUsedSize`가 거의 안 줄어드는 걸 보고 당황했다. 즉 디스크를 잡아먹고 있던 3.4GB 대부분이 애초에 test 컬렉션이 아니었다는 뜻이다.

## oplog 쪽으로 의심이 넘어갔다

그래서 `local.oplog.rs`를 봤더니 `storageSize`가 설정된 `maxSize`(990MB) 대비 3배 넘는 3.09GB였다. `rs.printReplicationInfo()`로 oplog window를 확인해보니 91.67시간이었는데, Atlas 콘솔에 설정된 "Set Minimum Oplog Window"는 24시간이었다. 거의 4배 차이가 나는 셈이다.

replSetResizeOplog로 강제로 줄여보려고 했는데 atlasAdmin 같은 최상위 역할로도 이 명령어 자체가 Unauthorized로 막혀 있었다. 권한 문제가 아니라 Atlas가 구조적으로 이 명령어를 차단하는 것 같다.

12GB 규모로 2차 테스트를 반복해봤는데 비슷한 패턴이 더 크게 나타났다. oplog가 2.88GB에서 15.08GB까지 커졌고, TTL 삭제가 다 끝난 뒤에도 그대로 유지됐다. 그리고 이 테스트 도중에 Storage Auto Scaling이 프로비저닝 용량을 자동으로 41.77GB에서 55.73GB로 늘리는 것도 확인했다(수동으로 건드린 적 없음). 실사용량은 TTL 삭제로 줄어들어도 프로비저닝 용량은 그대로 유지되는 걸 보고, 이 서비스가 늘리기만 하고 줄이지는 않는 구조라는 걸 체감했다.

## compact는 예측이 안 됐다

수동 compact를 반복해봤는데 결과가 매번 달랐다. 1차 시도에서는 9.26GB가 회수돼서 거의 "재사용 가능" 표시량과 일치했다. 그런데 바로 이어서 2차, 3차 시도에서는 0바이트, 24KB처럼 사실상 아무것도 회수되지 않았다. 심지어 한참 뒤에 다시 확인해보니 4.12GB였던 storageSize가 10.35GB로 다시 커져 있었다. autoCompact가 켜진 채로 자체적으로 재정리를 시도하다가 오히려 파일을 다시 키운 게 아닌가 싶다.

![]({{ '/assets/images/mongo-autocompaction-compact-timeline.svg' | relative_url }})

## WiredTiger 공식 문서에서 답을 찾았다

여기까지 오고 나서야 WiredTiger 문서를 제대로 찾아봤다. compaction은 "best-effort" 프로세스라 파일 크기 축소를 보장하지 않는다고 명시되어 있었다. 조건이 꽤 까다로운데, 파일 앞쪽 80% 안에 전체 여유 공간의 20% 이상이 있거나 앞쪽 90% 안에 10% 이상이 있어야 뒤쪽을 잘라낼 수 있다고 한다. free space 비율이 99.9999%여도 이 조건을 못 맞추면 실패한다는 게 우리가 본 것과 정확히 일치했다. WiredTiger가 블록을 재사용할 때 "가장 딱 맞는 작은 블록"을 골라 쓰는 방식이라 여유 공간이 파일 뒤쪽에 몰리지 않고 전체에 흩어지기 때문이라고 한다.

혹시나 해서 MongoDB 공식 버그 트래커(JIRA)도 뒤져봤는데 SERVER-54196에 거의 같은 증상이 보고되어 있었다. free space 19GB인데 bytesFreed는 315KB. 별다른 해결책 없이 종료되어 있는 이슈였다. 우리 환경만의 문제가 아니라 WiredTiger 자체가 갖고 있는 알려진 한계인 것 같다.

확실하게 회수되는 방법을 정리해보면 이렇다.

| 방법 | 결과 |
|---|---|
| 수동 compact | 성공할 때도 있고 0바이트일 때도 있음, 예측 불가 |
| autoCompact | 관찰 기간 내내 자체 회수 0 |
| drop() 후 재생성 | 100% 확실하게 회수됨 |
| mongodump/restore, `$out` | drop과 마찬가지로 확실함 |

drop을 실행해보니 `fsUsedSize`가 즉시 약 10.78GB 줄었는데, compact를 반복해도 남아있던 잔여물(약 10.35GB)과 거의 정확하게 맞아떨어졌다. compact는 어디까지나 best-effort고, 진짜로 디스크를 돌려받으려면 drop 말고는 답이 없다는 걸 이번에 확인한 셈이다.

oplog가 왜 이렇게 부풀고 왜 다시 안 줄어드는지는 아직 다 이해한 건 아니다. Atlas 콘솔에서 "Set Minimum Oplog Window" 값을 건드려서 재저장하면 줄어드는지 시도해볼 여지가 남아있고, 그래도 안 되면 Atlas Support에 문의를 넣어봐야 할 것 같다.
