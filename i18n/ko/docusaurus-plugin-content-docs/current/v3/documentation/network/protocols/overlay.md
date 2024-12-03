# 오버레이 서브네트워크

구현:

- https://github.com/ton-blockchain/ton/tree/master/overlay

## 개요

TON의 아키텍처는 여러 체인이 동시에 독립적으로 존재할 수 있도록 구축되었으며 - 이들은 private 또는 public일 수 있습니다.
노드들은 어떤 샤드와 체인을 저장하고 처리할지 선택할 수 있습니다.
동시에 통신 프로토콜은 그 보편성으로 인해 변경되지 않습니다. DHT, RLDP, Overlay와 같은 프로토콜이 이를 가능하게 합니다.
처음 두 개는 이미 알고 있으므로 이 섹션에서는 Overlay가 무엇인지 알아보겠습니다.

오버레이는 단일 네트워크를 추가 서브네트워크로 분할하는 역할을 담당합니다. 오버레이는 누구나 연결할 수 있는 public 또는 특정 사람들에게만 알려진 추가 자격 증명이 필요한 private일 수 있습니다.

마스터체인을 포함한 TON의 모든 체인은 자체 오버레이를 사용하여 통신합니다.
오버레이에 참여하려면 이미 오버레이에 있는 노드를 찾아 데이터 교환을 시작해야 합니다.
public 오버레이의 경우 DHT를 사용하여 노드를 찾을 수 있습니다.

## ADNL vs 오버레이 네트워크

ADNL과 달리 TON 오버레이 네트워크는 일반적으로 다른 임의 노드로 데이터그램을 보내는 것을 지원하지 않습니다. 대신, 특정 노드들(해당 오버레이 네트워크와 관련하여 "이웃"이라고 함) 사이에 "반영구적 링크"가 설정되고 메시지는 보통 이러한 링크를 따라 전달됩니다(즉, 노드에서 이웃 중 하나로).

각 오버레이 서브네트워크는 일반적으로 오버레이 네트워크 설명(TL-직렬화된 객체)의 SHA256과 같은 256비트 네트워크 식별자를 가집니다.

오버레이 서브네트워크는 public 또는 private일 수 있습니다.

오버레이 서브네트워크는 특별한 [가십](https://en.wikipedia.org/wiki/Gossip_protocol) 프로토콜에 따라 작동합니다.

## 오버레이 노드와의 상호작용

DHT에 대한 글의 [블록체인 상태를 저장하는 노드 검색](/v3/documentation/network/protocols/dht/dht-deep-dive#search-for-nodes-that-store-the-state-of-the-blockchain) 섹션에서 오버레이 노드를 찾는 예시를 이미 분석했습니다.
이 섹션에서는 이들과의 상호작용에 중점을 둘 것입니다.

DHT를 쿼리하면 오버레이 노드의 주소를 얻게 되며, [overlay.getRandomPeers](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L237) 쿼리를 사용하여 이 오버레이의 다른 노드들의 주소를 알아낼 수 있습니다.
충분한 수의 노드에 연결하면 이들로부터 모든 블록 정보와 다른 체인 이벤트를 받을 수 있으며, 처리를 위해 우리의 트랜잭션을 보낼 수도 있습니다.

### 더 많은 이웃 찾기

오버레이에서 노드를 가져오는 예시를 살펴보겠습니다.

이를 위해 오버레이의 알려진 노드에 `overlay.getRandomPeers` 요청을 보내고 TL 스키마를 직렬화합니다:

```tlb
overlay.node id:PublicKey overlay:int256 version:int signature:bytes = overlay.Node;
overlay.nodes nodes:(vector overlay.node) = overlay.Nodes;

overlay.getRandomPeers peers:overlay.nodes = overlay.Nodes;
```

`peers` - 우리가 아는 피어들을 포함해야 하므로 그들을 다시 받지 않지만, 아직 아는 피어가 없으므로 `peers.nodes`는 빈 배열이 될 것입니다.

단순히 정보를 얻는 것이 아니라 오버레이에 참여하고 브로드캐스트를 받고 싶다면, `peers`에 요청을 하는 우리 노드에 대한 정보도 추가해야 합니다.
피어들이 우리에 대한 정보를 얻으면 ADNL이나 RLDP를 사용하여 브로드캐스트를 보내기 시작할 것입니다.

오버레이 내의 각 요청은 TL 스키마로 접두사를 붙여야 합니다:

```tlb
overlay.query overlay:int256 = True;
```

`overlay`는 오버레이의 id여야 합니다 - `tonNode.ShardPublicOverlayId` 스키마 키의 id - DHT 검색에 사용한 것과 동일합니다.

2개의 직렬화된 스키마를 단순히 2개의 직렬화된 바이트 배열을 연결하여 합쳐야 합니다. `overlay.query`가 먼저 오고 `overlay.getRandomPeers`가 두 번째로 옵니다.

결과 배열을 `adnl.message.query` 스키마로 감싸고 ADNL을 통해 전송합니다. 응답으로는 `overlay.nodes`를 기다립니다 - 이는 우리가 연결할 수 있는 오버레이 노드의 목록이며, 필요한 경우 충분한 연결을 얻을 때까지 새로운 노드에 동일한 요청을 반복할 수 있습니다.

### 기능 요청

연결이 설정되면 [요청](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L413) `tonNode.*`을 사용하여 오버레이 노드에 접근할 수 있습니다.

이런 종류의 요청에는 RLDP 프로토콜이 사용됩니다. 그리고 `overlay.query` 접두사를 잊지 않는 것이 중요합니다 - 오버레이의 모든 쿼리에 사용해야 합니다.

요청 자체에는 특별한 것이 없으며, [ADNL TCP에 대한 글에서 했던 것](/v3/documentation/network/protocols/adnl/adnl-tcp#getmasterchaininfo)과 매우 유사합니다.

예를 들어, `downloadBlockFull` 요청은 이미 친숙한 블록 id 스키마를 사용합니다:

```tlb
tonNode.downloadBlockFull block:tonNode.blockIdExt = tonNode.DataFull;
```

이를 전달하면 블록에 대한 전체 정보를 다운로드할 수 있으며, 응답으로 다음을 받게 됩니다:

```tlb
tonNode.dataFull id:tonNode.blockIdExt proof:bytes block:bytes is_link:Bool = tonNode.DataFull;
  or
tonNode.dataFullEmpty = tonNode.DataFull;
```

있다면 `block` 필드는 TL-B 형식의 데이터를 포함합니다.

이렇게 노드에서 직접 정보를 받을 수 있습니다.

## 참조

*여기 [Oleg Baranov](https://github.com/xssnick)의 [원본 문서 링크](https://github.com/xssnick/ton-deep-doc/blob/master/Overlay-Network.md)가 있습니다.*
