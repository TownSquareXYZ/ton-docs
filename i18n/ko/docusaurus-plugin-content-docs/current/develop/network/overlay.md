# 서브네트워크 오버레이

TON의 아키텍처는 많은 체인이 동시에 독립적으로 존재할 수 있도록 구축되어 있으며, 이는 프라이빗 또는 퍼블릭이 될 수 있습니다.
노드는 어떤 샤드와 체인을 저장하고 처리할지 선택할 수 있습니다.
동시에 통신 프로토콜은 보편성 때문에 변경되지 않습니다. DHT, RLDP, 오버레이와 같은 프로토콜을 통해 이를 실현할 수 있습니다.
우리는 이미 처음 두 가지에 대해 잘 알고 있으며, 이 섹션에서는 오버레이가 무엇인지 알아보겠습니다.

오버레이는 단일 네트워크를 추가적인 하위 네트워크로 나누는 역할을 합니다. 오버레이는 누구나 연결할 수 있는 공용 네트워크와 특정 인원에게만 알려진 추가 자격 증명이 필요한 비공개 네트워크가 될 수 있습니다.

마스터체인을 포함한 TON의 모든 체인은 자체 오버레이를 사용해 통신합니다.
오버레이에 참여하려면 이미 오버레이에 있는 노드를 찾아 그들과 데이터 교환을 시작해야 합니다.
퍼블릭 오버레이의 경우 DHT를 사용해 노드를 찾을 수 있습니다.

## 오버레이 노드와의 상호작용

저희는 이미 [블록체인 상태를 저장하는 노드 검색](/개발/네트워크/dht#search-for-nodes-that-store-the-state-of-the-blockchain) 섹션의
에서 오버레이 노드를 찾는 예제를 분석했습니다.
이 섹션에서는 이들과의 상호작용에 초점을 맞추겠습니다.

DHT를 쿼리할 때 오버레이 노드의 주소를 얻게 되며, 이를 통해 [overlay.getRandomPeers](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L237) 쿼리를 사용하여 이 오버레이의 다른 노드 주소를 찾을 수 있습니다.
충분한 수의 노드에 연결하면 노드로부터 모든 블록 정보와 기타 체인 이벤트를 수신할 수 있을 뿐만 아니라 트랜잭션을 전송하여 처리할 수 있습니다.

### 더 많은 이웃 찾기

오버레이에서 노드를 가져오는 예를 살펴보겠습니다.

이렇게 하려면 오버레이의 알려진 노드에 `overlay.getRandomPeers` 요청을 보내고 TL 스키마를 직렬화합니다:

```tlb
overlay.node id:PublicKey overlay:int256 version:int signature:bytes = overlay.Node;
overlay.nodes nodes:(vector overlay.node) = overlay.Nodes;

overlay.getRandomPeers peers:overlay.nodes = overlay.Nodes;
```

피어`- 우리가 알고 있는 피어를 포함해야 하지만 아직 아는 피어가 없으므로`peers.nodes\`는 빈 배열이 됩니다.

단순히 정보를 얻는 것이 아니라 오버레이에 참여하여 브로드캐스트를 받으려면 요청을 수행하는 노드에 대한 '피어' 정보도 추가해야 합니다.
피어가 우리에 대한 정보를 얻게 되면 ADNL 또는 RLDP를 사용하여 브로드캐스트를 보내기 시작할 것입니다.

오버레이 내부의 각 요청에는 TL 스키마가 접두사로 붙어야 합니다:

```tlb
overlay.query overlay:int256 = True;
```

'오버레이'는 오버레이의 ID(`tonNode.ShardPublicOverlayId` 스키마 키의 ID)로, DHT를 검색할 때 사용한 것과 동일해야 합니다.

2개의 직렬화된 바이트 배열을 단순히 연결하여 2개의 직렬화된 스키마를 연결해야 하는데, `overlay.query`가 첫 번째, `overlay.getRandomPeers`가 두 번째가 됩니다.

결과 배열을 `adnl.message.query` 스키마로 감싸서 ADNL을 통해 전송합니다. 이에 대한 응답으로 연결할 수 있는 오버레이 노드 목록인 `overlay.nodes`를 기다리고 있으며, 필요한 경우 충분한 연결이 이루어질 때까지 새로운 오버레이 노드에 동일한 요청을 반복합니다.

### 기능 요청

연결이 설정되면 [요청](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L413) `tonNode.*`를 사용하여 오버레이 노드에 액세스할 수 있습니다.

이러한 종류의 요청에는 RLDP 프로토콜이 사용됩니다. 오버레이의 모든 쿼리에는 반드시 `overlay.query` 접두사를 사용해야 한다는 점을 잊지 마세요.

요청 자체에는 특이한 점이 없으며, 저희가 [ADNL TCP에 대한 기사에서 했던 것과 매우 유사합니다](/develop/네트워크/adnl-tcp#getmasterchaininfo).

예를 들어, `downloadBlockFull` 요청은 이미 익숙한 블록 ID 스키마를 사용합니다:

```tlb
tonNode.downloadBlockFull block:tonNode.blockIdExt = tonNode.DataFull;
```

이를 전달하면 블록에 대한 전체 정보를 다운로드할 수 있으며, 이에 대한 응답으로 받게 됩니다:

```tlb
tonNode.dataFull id:tonNode.blockIdExt proof:bytes block:bytes is_link:Bool = tonNode.DataFull;
  or
tonNode.dataFullEmpty = tonNode.DataFull;
```

있는 경우 'block' 필드에 TL-B 형식의 데이터가 포함됩니다.

따라서 노드로부터 직접 정보를 받을 수 있습니다.

## 참조

여기 [Oleg Baranov](https://github.com/xssnick)의 [원본 기사 링크](https://github.com/xssnick/ton-deep-doc/blob/master/Overlay-Network.md)가 있습니다.
