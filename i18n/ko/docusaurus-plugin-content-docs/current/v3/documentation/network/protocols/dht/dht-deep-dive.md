# DHT

DHT(Distributed Hash Table)는 분산 키-값 데이터베이스로, 네트워크의 각 구성원이 자신에 대한 정보와 같은 것을 저장할 수 있습니다.

TON의 DHT 구현은 IPFS에서 사용되는 [Kademlia](https://codethechange.stanford.edu/guides/guide_kademlia.html)와 본질적으로 유사합니다.
모든 네트워크 구성원은 DHT 노드를 실행하고, 키를 생성하고, 데이터를 저장할 수 있습니다.
이를 위해서는 무작위 ID를 생성하고 다른 노드에게 자신을 알려야 합니다.

데이터를 저장할 노드를 결정하기 위해 노드와 키 사이의 "거리"를 결정하는 알고리즘이 사용됩니다.
알고리즘은 간단합니다: 노드의 ID와 키의 ID를 가져와서 XOR 연산을 수행합니다. 값이 작을수록 더 가깝습니다.
목표는 키를 가능한 한 키와 가까운 노드에 저장하여 다른 네트워크 참가자들이 동일한 알고리즘을 사용하여 이 키에 대한 데이터를 제공할 수 있는 노드를 찾을 수 있도록 하는 것입니다.

## 키로 값 찾기

[ADNL UDP를 통해 DHT 노드에 연결하고 연결을 설정](/v3/documentation/network/protocols/adnl/adnl-udp#packet-structure-and-communication)하는 예시를 살펴보겠습니다.

예를 들어, foundation.ton 사이트를 호스팅하는 노드에 연결하기 위한 주소와 공개 키를 찾고 싶습니다.
DNS 계약의 Get 메서드를 실행하여 이 사이트의 ADNL 주소를 이미 얻었다고 가정해 봅시다.
16진수로 표현된 ADNL 주소는 `516618cf6cbe9004f6883e742c9a2e3ca53ed02e3e36f4cef62a98ee1e449174`입니다.
이제 우리의 목표는 이 주소를 가진 노드의 ip, 포트 및 공개 키를 찾는 것입니다.

이를 위해서는 DHT 키의 ID를 얻어야 하며, 먼저 DHT 키 스키마를 채우겠습니다:

```tlb
dht.key id:int256 name:bytes idx:int = dht.Key
```

`name`은 키의 타입으로, ADNL 주소의 경우 `address`라는 단어가 사용되고, 예를 들어 샤드체인 노드를 검색할 때는 `nodes`가 사용됩니다. 하지만 키 타입은 찾고자 하는 값에 따라 어떤 바이트 배열이든 될 수 있습니다.

이 스키마를 채우면 다음과 같이 됩니다:

```
8fde67f6                                                           -- TL ID dht.key
516618cf6cbe9004f6883e742c9a2e3ca53ed02e3e36f4cef62a98ee1e449174   -- our searched ADNL address
07 61646472657373                                                  -- key type, the word "address" as an TL array of bytes
00000000                                                           -- index 0 because there is only 1 key
```

다음으로 - 위에서 직렬화된 바이트의 sha256 해시인 키 ID를 얻습니다. 결과는 `b30af0538916421b46df4ce580bf3a29316831e0c3323a7f156df0236c5b2f75`가 됩니다.

이제 검색을 시작할 수 있습니다. 이를 위해 [스키마](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L197)가 있는 쿼리를 실행해야 합니다:

```tlb
dht.findValue key:int256 k:int = dht.ValueResult
```

`key`는 우리의 DHT 키의 ID이고, `k`는 검색의 "너비"로, 작을수록 더 정확하지만 쿼리할 수 있는 잠재적 노드가 더 적습니다. TON의 노드에 대한 최대 k는 10이며, 보통 6이 사용됩니다.

이 구조를 채우고 직렬화한 다음 `adnl.message.query` 스키마를 사용하여 요청을 보냅니다. [자세한 내용은 다른 문서에서 읽을 수 있습니다](/v3/documentation/network/protocols/adnl/adnl-udp#packet-structure-and-communication).

응답으로 다음을 받을 수 있습니다:

- `dht.valueNotFound` - 값을 찾지 못한 경우
- `dht.valueFound` - 이 노드에서 값을 찾은 경우

##### dht.valueNotFound

`dht.valueNotFound`를 받으면, 응답에는 우리가 요청한 노드가 알고 있는 노드들 중에서 우리가 요청한 키에 가장 가까운 노드들의 목록이 포함됩니다. 이 경우 받은 노드들에 연결하고 우리가 알고 있는 목록에 추가해야 합니다.
그 후, 우리가 알고 있는 모든 노드 목록에서 가장 가깝고, 접근 가능하며, 아직 요청하지 않은 노드를 선택하여 동일한 요청을 합니다. 우리가 선택한 범위의 모든 노드를 시도하거나 새로운 노드를 더 이상 받지 못할 때까지 이렇게 계속합니다.

응답 필드를 더 자세히 분석해 보겠습니다. 사용된 스키마는 다음과 같습니다:

```tlb
adnl.address.udp ip:int port:int = adnl.Address;
adnl.addressList addrs:(vector adnl.Address) version:int reinit_date:int priority:int expire_at:int = adnl.AddressList;

dht.node id:PublicKey addr_list:adnl.addressList version:int signature:bytes = dht.Node;
dht.nodes nodes:(vector dht.node) = dht.Nodes;

dht.valueNotFound nodes:dht.nodes = dht.ValueResult;
```

`dht.nodes -> nodes` - DHT 노드 목록(배열).

각 노드는 보통 [pub.ed25519](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L47)인 `id` 공개 키를 가지고 있으며, ADNL을 통해 노드에 연결하기 위한 서버 키로 사용됩니다. 또한, 각 노드는 주소 목록 `addr_list:adnl.addressList`, 버전 및 서명을 가지고 있습니다.

각 노드의 서명을 확인해야 합니다. 이를 위해 `signature` 값을 읽고 필드를 0으로 설정합니다(빈 바이트 배열로 만듦). 그 후 - 빈 서명으로 `dht.node` TL 구조를 직렬화하고 비우기 전의 `signature` 필드를 확인합니다.
`id` 필드의 공개 키를 사용하여 받은 직렬화된 바이트에서 확인합니다. [[구현 예시]](https://github.com/xssnick/tonutils-go/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/dht/client.go#L91)

`addrs:(vector adnl.Address)` 목록에서 주소를 가져와서 ADNL UDP 연결을 설정하려고 시도합니다. 서버 키로는 공개 키인 `id`를 사용합니다.

이 노드까지의 "거리"를 알아내기 위해서는 - `id` 필드의 키에서 [key id](/v3/documentation/network/protocols/adnl/adnl-tcp#getting-key-id)를 가져와서 노드의 키 id와 원하는 키와의 XOR 연산으로 거리를 확인해야 합니다.
거리가 충분히 가까우면 이 노드에도 동일한 요청을 할 수 있습니다. 값을 찾거나 새로운 노드가 더 이상 없을 때까지 이렇게 계속됩니다.

##### dht.valueFound

응답에는 값 자체, 전체 키 정보, 그리고 선택적으로 서명(값 타입에 따라 다름)이 포함됩니다.

응답 필드를 자세히 분석해 보겠습니다. 사용된 스키마는 다음과 같습니다:

```tlb
adnl.address.udp ip:int port:int = adnl.Address;
adnl.addressList addrs:(vector adnl.Address) version:int reinit_date:int priority:int expire_at:int = adnl.AddressList;

dht.key id:int256 name:bytes idx:int = dht.Key;

dht.updateRule.signature = dht.UpdateRule;
dht.updateRule.anybody = dht.UpdateRule;
dht.updateRule.overlayNodes = dht.UpdateRule;

dht.keyDescription key:dht.key id:PublicKey update_rule:dht.UpdateRule signature:bytes = dht.KeyDescription;

dht.value key:dht.keyDescription value:bytes ttl:int signature:bytes = dht.Value; 

dht.valueFound value:dht.Value = dht.ValueResult;
```

먼저, `key:dht.keyDescription`을 분석해 보겠습니다. 이는 키의 완전한 설명으로, 키 자체와 누가 어떻게 값을 업데이트할 수 있는지에 대한 정보입니다.

- `key:dht.key` - 검색에 사용한 키 ID의 원본 키와 일치해야 합니다.
- `id:PublicKey` - 레코드 소유자의 공개 키.
- `update_rule:dht.UpdateRule` - 레코드 업데이트 규칙.
- - `dht.updateRule.signature` - 개인 키 소유자만 레코드를 업데이트할 수 있으며, 키와 값 모두의 `signature`가 유효해야 함
- - `dht.updateRule.anybody` - 누구나 레코드를 업데이트할 수 있으며, `signature`는 비어 있고 확인되지 않음
- - `dht.updateRule.overlayNodes` - 같은 오버레이의 노드들이 키를 업데이트할 수 있음, 같은 오버레이의 노드를 찾고 자신을 추가하는 데 사용됨

###### dht.updateRule.signature

키 설명을 읽은 후, `updateRule`에 따라 행동합니다. ADNL 주소 조회의 경우 타입은 항상 `dht.updateRule.signature`입니다.
이전과 동일한 방식으로 키 서명을 확인합니다. 서명을 빈 바이트 배열로 만들고, 직렬화한 다음 확인합니다. 그 후 - 값에 대해서도 동일한 작업을 반복합니다. 즉, 전체 `dht.value` 객체에 대해 (키 서명을 제자리에 돌려놓으면서) 수행합니다.

[[구현 예시]](https://github.com/xssnick/tonutils-go/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/dht/client.go#L331)

###### dht.updateRule.overlayNodes

네트워크의 워크체인의 다른 노드-샤드에 대한 정보를 포함하는 키에 사용되며, 값은 항상 `overlay.nodes` TL 구조를 가집니다.
value 필드는 비어 있어야 합니다.

```tlb
overlay.node id:PublicKey overlay:int256 version:int signature:bytes = overlay.Node;
overlay.nodes nodes:(vector overlay.node) = overlay.Nodes;
```

유효성을 확인하기 위해서는 모든 `nodes`를 확인하고 각각에 대해 TL 구조를 직렬화하여 `signature`를 `id`에 대해 확인해야 합니다:

```tlb
overlay.node.toSign id:adnl.id.short overlay:int256 version:int = overlay.node.ToSign;
```

보다시피, id는 원래 구조의 `id` 필드의 키 id(해시)인 adnl.id.short로 대체되어야 합니다. 직렬화 후 - 데이터로 서명을 확인합니다. 직렬화 후에는 데이터로 서명을 확인합니다.

결과적으로 우리가 필요한 워크체인 샤드에 대한 정보를 제공할 수 있는 유효한 노드 목록을 얻게 됩니다.

###### dht.updateRule.anybody

서명이 없으며 누구나 업데이트할 수 있습니다.

#### 값 사용하기

모든 것이 검증되고 `ttl:int` 값이 만료되지 않았다면, 값 자체인 `value:bytes`로 작업을 시작할 수 있습니다. ADNL 주소의 경우 내부에 `adnl.addressList` 구조가 있어야 합니다.
여기에는 요청된 ADNL 주소에 해당하는 서버의 ip 주소와 포트가 포함됩니다. 우리의 경우 대부분 `foundation.ton` 서비스의 RLDP-HTTP 주소 하나가 있을 것입니다.
서버 키로는 DHT 키 정보의 `id:PublicKey`를 사용할 것입니다.

연결이 설정되면 RLDP 프로토콜을 사용하여 사이트의 페이지를 요청할 수 있습니다. 이 단계에서 DHT 측의 작업은 완료됩니다.

### 블록체인 상태를 저장하는 노드 검색

DHT는 워크체인과 그 샤드의 데이터를 저장하는 노드에 대한 정보를 찾는 데도 사용됩니다. 프로세스는 다른 키를 검색할 때와 동일하며, 차이점은 키 자체의 직렬화와 응답의 유효성 검사에 있으며, 이 섹션에서 이러한 점들을 분석하겠습니다.

예를 들어 마스터체인과 그 샤드의 데이터를 얻기 위해서는 TL 구조를 채워야 합니다:

```
tonNode.shardPublicOverlayId workchain:int shard:long zero_state_file_hash:int256 = tonNode.ShardPublicOverlayId;
```

여기서 `workchain`은 마스터체인의 경우 -1이 되고, 샤드는 -922337203685477580 (0xFFFFFFFFFFFFFFFF)이 되며, `zero_state_file_hash`는 체인의 제로 상태 해시(file_hash)입니다. 다른 데이터와 마찬가지로 글로벌 네트워크 config의 `"validator"` 필드에서 가져올 수 있습니다.

```json
"zero_state": {
  "workchain": -1,
  "shard": -9223372036854775808, 
  "seqno": 0,
  "root_hash": "F6OpKZKqvqeFp6CQmFomXNMfMj2EnaUSOXN+Mh+wVWk=",
  "file_hash": "XplPz01CXAps5qeSWUtxcyBfdAo5zVb1N979KLSKD24="
}
```

`tonNode.shardPublicOverlayId`를 채운 후 이를 직렬화하고 해싱하여 키 id를 얻습니다(항상처럼).

이 결과 키 ID를 `pub.overlay name:bytes = PublicKey` 구조를 채우기 위한 `name`으로 사용해야 하며, TL 바이트 배열로 감쌉니다. 다음으로 이를 직렬화하고 이제 여기서 키 ID를 얻습니다.

결과적으로 생성된 ID는 다음에서 사용할 키가 됩니다:

```bash
dht.findValue
```

그리고 `name` 필드의 값은 `nodes` 단어가 됩니다. 이전 섹션의 과정을 반복하며, 마지막 때와 모든 것이 동일하지만 `updateRule`이 [dht.updateRule.overlayNodes](#dhtupdateruleoverlaynodes)가 될 것입니다.

검증 후 - 우리의 워크체인과 샤드에 대한 정보를 가진 노드들의 공개 키(`id`)를 얻게 됩니다. 노드들의 ADNL 주소를 얻으려면 키에서 ID를 만들고(해싱 방법 사용) `foundation.ton` 도메인의 ADNL 주소와 마찬가지로 각 ADNL 주소에 대해 위에서 설명한 절차를 반복해야 합니다.

결과적으로 우리는 [overlay.getRandomPeers](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L237)를 사용하여 이 체인의 다른 노드들의 주소를 알아낼 수 있는 노드들의 주소를 얻게 됩니다.
또한 이러한 노드들로부터 블록에 대한 모든 정보를 받을 수 있습니다.

## 참조

*여기 [Oleg Baranov](https://github.com/xssnick)의 [원본 문서 링크](https://github.com/xssnick/ton-deep-doc/blob/master/DHT.md)가 있습니다.*