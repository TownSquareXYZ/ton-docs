# DHT

DHT는 분산 해시 테이블의 약자로, 기본적으로 네트워크의 각 구성원이 자신에 대한 정보 등을 저장할 수 있는 분산 키-값 데이터베이스(
)입니다.

TON에서 DHT의 구현은 본질적으로 IPFS에서 사용되는 [카뎀리아](https://codethechange.stanford.edu/guides/guide_kademlia.html)의 구현과 유사합니다.
모든 네트워크 구성원은 DHT 노드를 실행하고 키를 생성하고 데이터를 저장할 수 있습니다.
이를 위해서는 임의의 ID를 생성하고 다른 노드에 자신에 대해 알려야 합니다.

데이터를 저장할 노드를 결정하기 위해 노드와 키 사이의 '거리'를 결정하는 알고리즘이 사용됩니다.
알고리즘은 간단합니다. 노드의 ID와 키의 ID를 가지고 XOR 연산을 수행합니다. 값이 작을수록 노드와 키가 가까워집니다.
이 작업은 다른 네트워크 참여자가
동일한 알고리즘을 사용하여 이 키에 대한 데이터를 제공할 수 있는 노드를 찾을 수 있도록 키에 최대한 가까운 노드에 키를 저장하는 것입니다.

## 키로 값 찾기

키를 검색하여 [아무 DHT 노드에 연결하고 ADNL UDP를 통해 연결 설정](/개발/네트워크/adnl-udp#패킷-구조-통신)이라는 예제를 살펴봅시다.

예를 들어 foundation.ton 사이트를 호스팅하는 노드에 연결하기 위한 주소와 공개키를 찾고자 합니다.
DNS 컨트랙트의 Get 메서드를 실행하여 이 사이트의 ADNL 주소를 이미 얻었다고 가정해 보겠습니다.
16진수 표현의 ADNL 주소는 `516618cf6cbe9004f6883e742c9a2e3ca53ed02e3e36f4cef62a98ee1e449174`입니다.
이제 우리의 목표는 이 주소를 가진 노드의 IP, 포트, 공개키를 찾는 것입니다.

이렇게 하려면 먼저 DHT 키의 ID를 가져와야 하며, DHT 키 스키마를 채울 것입니다:

```tlb
dht.key id:int256 name:bytes idx:int = dht.Key
```

키 유형은 '이름'이며, ADNL 주소의 경우 '주소'라는 단어가 사용되며, 예를 들어 샤드체인 노드를 검색할 때는 '노드'라는 단어가 사용됩니다. 그러나 키 유형은 찾고자 하는 값에 따라 임의의 바이트 배열이 될 수 있습니다.

이 스키마를 채우면 다음과 같은 결과를 얻을 수 있습니다:

```
8fde67f6                                                           -- TL ID dht.key
516618cf6cbe9004f6883e742c9a2e3ca53ed02e3e36f4cef62a98ee1e449174   -- our searched ADNL address
07 61646472657373                                                  -- key type, the word "address" as an TL array of bytes
00000000                                                           -- index 0 because there is only 1 key
```

다음 - 위에서 직렬화된 바이트에서 키 ID, sha256 해시를 가져옵니다. b30af0538916421b46df4ce580bf3a29316831e0c3323a7f156df0236c5b2f75\`가 됩니다.

이제 검색을 시작할 수 있습니다. 이를 위해서는 [스키마](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L197)가 있는 쿼리를 실행해야 합니다:

```tlb
dht.findValue key:int256 k:int = dht.ValueResult
```

'키'는 DHT 키의 ID이고 'k'는 검색의 '폭'으로, 이 값이 작을수록 정확도는 높아지지만 쿼리할 수 있는 잠재 노드의 수는 줄어듭니다. TON의 노드에 대한 최대 k는 10이며, 일반적으로 6이 사용됩니다.

이 구조를 채우고, `adnl.message.query` 스키마를 사용하여 요청을 직렬화하여 전송해 보겠습니다. 이에 대한 자세한 내용은 [다른 문서](/개발/네트워크/adnl-udp#패킷 구조 및 통신)에서 확인할 수 있습니다.

이에 대한 답변은 다음과 같습니다:

- `dht.valueNotFound` - 값을 찾을 수 없는 경우.
- `dht.valueFound` - 이 노드에서 값을 찾은 경우.

##### dht.valueNotFound

dht.valueNotFound\`를 받으면 응답에는 요청한 노드와 알려진 노드 목록에서 요청한 키에 최대한 가까운 노드 목록이 포함됩니다. 이 경우 수신한 노드를 연결하여 우리에게 알려진 목록에 추가해야 합니다.
그런 다음 알려진 모든 노드 목록에서 가장 가깝고 접근 가능하며 아직 요청하지 않은 노드를 선택하고 동일한 요청을 수행합니다. 선택한 범위의 모든 노드를 시도하거나 새 노드 수신을 중단할 때까지 계속 반복합니다.

응답 필드와 사용된 스키마를 더 자세히 분석해 보겠습니다:

```tlb
adnl.address.udp ip:int port:int = adnl.Address;
adnl.addressList addrs:(vector adnl.Address) version:int reinit_date:int priority:int expire_at:int = adnl.AddressList;

dht.node id:PublicKey addr_list:adnl.addressList version:int signature:bytes = dht.Node;
dht.nodes nodes:(vector dht.node) = dht.Nodes;

dht.valueNotFound nodes:dht.nodes = dht.ValueResult;
```

`dht.nodes -> 노드` - DHT 노드 목록(배열).

각 노드에는 공개 키인 `id`가 있으며, 일반적으로 [pub.ed25519](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L47)가 ADNL을 통해 노드에 연결할 때 서버 키로 사용됩니다. 또한 각 노드에는 주소 목록인 `addr_list:adnl.addressList`, 버전 및 서명이 있습니다.

각 노드의 서명을 확인해야 하는데, 이를 위해 `signature` 값을 읽고 필드를 0으로 설정합니다(빈 바이트 배열로 만듭니다). 이후 - 비워진 서명이 있는 TL 구조체 `dht.node`를 직렬화하고 비우기 전의 `signature` 필드를 확인합니다.
받은 직렬화된 바이트열을 `id` 필드의 공개 키를 사용하여 확인합니다. [[구현 예시]](https://github.com/xssnick/tonutils-go/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/dht/client.go#L91)

'addrs:(vector adnl.Address)`목록에서 주소를 가져와서 공개 키인`id\`를 서버 키로 사용하여 ADNL UDP 연결을 설정하려고 합니다.

이 노드와의 '거리'를 확인하려면 `id` 필드에 있는 키에서 [key id](/develop/network/adnl-tcp#getting-key-id)를 가져와 노드의 키 ID와 원하는 키의 XOR 연산으로 거리를 확인해야 합니다.
거리가 충분히 작으면 이 노드에 동일한 요청을 할 수 있습니다. 값을 찾거나 더 이상 새로운 노드가 없을 때까지 이런 식으로 반복합니다.

##### dht.valueFound

응답에는 값 자체, 전체 키 정보, 선택적으로 서명(값 유형에 따라 다름)이 포함됩니다.

응답 필드와 사용된 스키마를 더 자세히 분석해 보겠습니다:

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

먼저 키에 대한 전체 설명, 키 자체 및 누가 어떻게 값을 업데이트할 수 있는지에 대한 정보인 `key:dht.keyDescription`을 분석해 보겠습니다.

- `key:dht.key` - 키는 검색을 위해 키 ID를 가져온 키와 일치해야 합니다.
- 'id:공개키' - 레코드 소유자의 공개키입니다.
- 업데이트 규칙\` - 업데이트 규칙을 기록합니다.
- - `dht.updateRule.signature` - 개인 키의 소유자만 레코드를 업데이트할 수 있으며, 키와 값의 `서명`이 모두 유효해야 합니다.
- - 누구나`- 누구나 레코드를 업데이트할 수 있으며,`서명\`은 비어 있고 확인되지 않습니다.
- - `dht.updateRule.overlayNodes` - 동일한 오버레이의 노드가 키를 업데이트할 수 있으며, 동일한 오버레이의 노드를 찾아 자신을 추가하는 데 사용됩니다.

###### dht.updateRule.signature

키에 대한 설명을 읽은 후 'updateRule'에 따라 동작하며, ADNL 주소 조회의 경우 유형은 항상 `dht.updateRule.signature`입니다.
지난번과 같은 방식으로 키 서명을 확인하고 서명을 빈 바이트 배열로 만든 다음 직렬화하여 확인합니다. 이후 - 값, 즉 전체 `dht.value` 객체에 대해 동일한 작업을 반복합니다(키 서명을 제자리로 반환하면서).

[[구현 예시]](https://github.com/xssnick/tonutils-go/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/dht/client.go#L331)

###### dht.updateRule.overlayNodes

네트워크의 다른 노드-워크체인의 샤드에 대한 정보를 포함하는 키에 사용되며, 값은 항상 TL 구조 'overlay.nodes'를 갖습니다.
값 필드는 비어 있어야 합니다.

```tlb
overlay.node id:PublicKey overlay:int256 version:int signature:bytes = overlay.Node;
overlay.nodes nodes:(vector overlay.node) = overlay.Nodes;
```

유효성을 확인하려면 모든 `노드`를 확인하고 각 `서명`을 해당 `ID`와 비교하여 TL 구조를 직렬화하여 확인해야 합니다:

```tlb
overlay.node.toSign id:adnl.id.short overlay:int256 version:int = overlay.node.ToSign;
```

보시다시피, id는 원래 구조에서 `id` 필드의 키 ID(해시)인 adnl.id.short로 대체되어야 합니다. 직렬화 후 - 데이터로 서명을 확인합니다.

그 결과, 필요한 워크체인 샤드에 대한 정보를 제공할 수 있는 유효한 노드 목록을 얻게 됩니다.

###### dht.updateRule.anybody

서명이 필요 없으며 누구나 업데이트할 수 있습니다.

#### 값 사용

모든 것이 확인되고 `ttl:int` 값이 만료되지 않았다면 값 자체, 즉 `value:bytes`로 작업을 시작할 수 있습니다. ADNL 주소의 경우 내부에 `adnl.addressList` 구조가 있어야 합니다.
여기에는 요청된 ADNL 주소에 해당하는 서버의 IP 주소와 포트가 포함됩니다. 저희의 경우, `foundation.ton` 서비스의 RLDP-HTTP 주소가 1개 있을 가능성이 높습니다.
서버 키는 DHT 키 정보에 있는 공개 키 `id:PublicKey`를 사용합니다.

연결이 설정되면 RLDP 프로토콜을 사용하여 사이트의 페이지를 요청할 수 있습니다. 이 단계에서 DHT 측의 작업이 완료됩니다.

### 블록체인의 상태를 저장하는 노드를 검색합니다.

DHT는 워크체인과 그 샤드의 데이터를 저장하는 노드에 대한 정보를 찾는데도 사용됩니다. 프로세스는 키를 검색할 때와 동일하며, 유일한 차이점은 키 자체의 직렬화와 응답의 유효성 검사이며, 이 섹션에서는 이러한 점을 분석할 것입니다.

예를 들어 마스터체인과 그 샤드에 대한 데이터를 얻으려면 TL 구조를 채워야 합니다:

```
tonNode.shardPublicOverlayId workchain:int shard:long zero_state_file_hash:int256 = tonNode.ShardPublicOverlayId;
```

여기서 `workchain`은 마스터체인의 경우 -1, 샤드는 -922337203685477580 (0xFFFFFFFFFFFFFFFF)이며, `zero_state_file_hash`는 체인의 제로 상태 해시(file_hash)로 다른 데이터와 마찬가지로 글로벌 네트워크 구성의 `"validator"` 필드에서 가져올 수 있습니다.

```json
"zero_state": {
  "workchain": -1,
  "shard": -9223372036854775808, 
  "seqno": 0,
  "root_hash": "F6OpKZKqvqeFp6CQmFomXNMfMj2EnaUSOXN+Mh+wVWk=",
  "file_hash": "XplPz01CXAps5qeSWUtxcyBfdAo5zVb1N979KLSKD24="
}
```

톤노드.shardPublicOverlayId\`를 채운 후, 이를 직렬화하고 (항상 그렇듯이) 해싱을 통해 키 ID를 얻습니다.

결과 키 ID를 `name`으로 사용하여 `pub.overlay name:bytes = PublicKey` 구조를 채우고 TL 바이트 배열로 감싸야 합니다. 다음으로, 이를 직렬화하여 이제 키 ID를 얻습니다.

결과 ID는 `dht.findValue`에서 사용할 키가 되고 `name` 필드의 값은 `nodes`라는 단어가 됩니다. 이전 섹션의 프로세스를 반복하면 모든 것이 지난번과 동일하지만 `updateRule`은 [dht.updateRule.overlayNodes](#dhtupdateruleoverlaynodes)가 됩니다.

유효성 검사 후 워크체인과 샤드에 대한 정보가 있는 노드의 공개 키(`ID`)를 얻게 됩니다. 노드의 ADNL 주소를 얻으려면 키에서 (해싱 방법을 사용하여) ID를 만들고 'foundation.ton' 도메인의 ADNL 주소와 마찬가지로 각 ADNL 주소에 대해 위에서 설명한 절차를 반복해야 합니다.

결과적으로 노드의 주소를 얻게 되며, 원하는 경우 [overlay.getRandomPeers](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L237)를 사용하여 이 체인의 다른 노드의 주소를 찾을 수 있습니다.
또한 이러한 노드로부터 블록에 대한 모든 정보를 받을 수 있습니다.

## 참조

여기 [Oleg Baranov](https://github.com/xssnick)의 [원본 기사 링크](https://github.com/xssnick/ton-deep-doc/blob/master/DHT.md)가 있습니다.
