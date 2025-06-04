# NFT 처리

## 개요

이 문서 섹션에서는 독자에게 NFT를 더 잘 이해할 수 있도록 도와줍니다. 독자는 NFT와 상호작용하고 TON 블록체인에서 전송된 트랜잭션을 통해 NFT를 수락하는 방법을 배우게 될 것입니다.

아래 제공된 정보는 독자가 [Toncoin 결제 처리에 대한 세부 설명](/develop/dapps/asset-processing) 섹션을 이미 충분히 이해하고 있으며, 스마트 계약 프로그램을 통해 지갑과 상호작용하는 기본 지식을 가지고 있다는 것을 전제로 합니다.

## NFT의 기본 이해

TON 블록체인에서 운영되는 NFT는 [TEP-62](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md) 및 [TEP-64](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md) 표준으로 표현됩니다.

The Open Network (TON) 블록체인은 고성능을 염두에 두고 설계되었으며, 특정 NFT 디자인을 지원하기 위해 TON의 계약 주소 기반으로 자동 샤딩을 사용하는 기능을 포함합니다. 최적의 성능을 달성하려면 개별 NFT가 자체 스마트 계약을 사용해야 합니다. 이를 통해 대규모 또는 소규모의 NFT 컬렉션을 생성할 수 있으며 개발 비용 및 성능 문제를 줄일 수 있습니다. 그러나 이러한 접근 방식은 NFT 컬렉션 개발에 있어 새로운 고려 사항을 도입하게 됩니다.

각 NFT가 자체 스마트 계약을 사용하기 때문에, 단일 계약을 통해 컬렉션 내 각 개별 NFT에 대한 정보를 얻는 것은 불가능합니다. 전체 컬렉션 및 컬렉션 내 각 개별 NFT에 대한 정보를 검색하려면 컬렉션 계약과 각 개별 NFT 계약을 모두 개별적으로 쿼리해야 합니다. 같은 이유로, NFT 전송을 추적하려면 특정 컬렉션 내 각 개별 NFT의 모든 트랜잭션을 추적해야 합니다.

### NFT 컬렉션

NFT 컬렉션은 NFT 콘텐츠를 인덱싱하고 저장하는 역할을 하는 계약이며 다음 인터페이스를 포함해야 합니다:

#### Get 메서드 `get_collection_data`

```
(int next_item_index, cell collection_content, slice owner_address) get_collection_data()
```

컬렉션에 대한 일반 정보를 검색하며, 다음과 같은 정보를 제공합니다:

1. `next_item_index` - 컬렉션이 순서가 있는 경우, 이 분류는 컬렉션 내 NFT 총 개수와 민팅에 사용되는 다음 인덱스를 나타냅니다. 순서가 없는 컬렉션의 경우, `next_item_index` 값은 -1이며, 이는 컬렉션이 고유한 메커니즘을 사용하여 NFT를 추적함을 의미합니다 (예: TON DNS 도메인의 해시).
2. `collection_content` - TEP-64 호환 형식으로 표현된 컬렉션 콘텐츠를 나타내는 셀입니다.
3. `owner_address` - 컬렉션 소유자의 주소를 포함하는 슬라이스입니다 (이 값은 비어 있을 수도 있습니다).

#### Get 메서드 `get_nft_address_by_index`

```
(slice nft_address) get_nft_address_by_index(int index)
```

이 메서드는 특정 컬렉션에 속하는 NFT인지 확인하고, 컬렉션 내 인덱스를 제공하여 NFT의 주소를 가져올 수 있습니다. 메서드는 제공된 인덱스에 해당하는 NFT의 주소를 포함하는 슬라이스를 반환해야 합니다.

#### Get 메서드 `get_nft_content`

```
(cell full_content) get_nft_content(int index, cell individual_content)
```

컬렉션이 NFT의 공통 데이터 저장소 역할을 하기 때문에, 이 메서드는 NFT 콘텐츠를 완성하는 데 필요합니다. 이 메서드를 사용하려면 먼저 해당 NFT의 `individual_content`를 `get_nft_data()` 메서드를 호출하여 얻어야 합니다. `individual_content`를 얻은 후, `get_nft_content()` 메서드를 NFT 인덱스와 `individual_content` 셀과 함께 호출할 수 있습니다. 메서드는 NFT의 전체 콘텐츠를 포함하는 TEP-64 셀을 반환해야 합니다.

### NFT 아이템

기본 NFT는 다음을 구현해야 합니다:

#### Get 메서드 `get_nft_data()`

```
(int init?, int index, slice collection_address, slice owner_address, cell individual_content) get_nft_data()
```

#### `transfer`를 위한 인라인 메시지 핸들러

```
transfer#5fcc3d14 query_id:uint64 new_owner:MsgAddress response_destination:MsgAddress custom_payload:(Maybe ^Cell) forward_amount:(VarUInteger 16) forward_payload:(Either Cell ^Cell) = InternalMsgBody
```

메시지에서 채워야 할 각 매개변수는 다음과 같습니다:

1. `OP` - `0x5fcc3d14` - 전송 메시지 내 TEP-62 표준에 의해 정의된 상수입니다.
2. `queryId` - `uint64` - 메시지 추적에 사용되는 uint64 숫자입니다.
3. `newOwnerAddress` - `MsgAddress` - NFT를 전송할 계약의 주소입니다.
4. `responseAddress` - `MsgAddress` - 남은 자금을 전송하는 데 사용되는 주소입니다. 일반적으로 NFT 계약에 트랜잭션 수수료를 지불하고 필요한 경우 새 전송을 생성할 수 있도록 충분한 자금 (예: 1 TON)이 추가로 전송됩니다. 트랜잭션 내 사용되지 않은 모든 자금은 `responseAddress`로 전송됩니다.
5. `forwardAmount` - `Coins` - 전달 메시지와 함께 사용되는 TON 금액 (일반적으로 0.01 TON으로 설정). TON은 비동기식 아키텍처를 사용하므로, 새 소유자는 트랜잭션을 성공적으로 수신한 즉시 알림을 받지 않습니다. 새 소유자에게 알리기 위해, NFT 스마트 계약에서 `newOwnerAddress`로 내부 메시지가 보내지며, 이때 `forwardAmount`로 표시된 값이 사용됩니다. 전달 메시지는 `ownership_assigned` OP (`0x05138d91`)로 시작하며, 이전 소유자의 주소와 (있을 경우) `forwardPayload`를 포함합니다.
6. `forwardPayload` - `Slice | Cell` - `ownership_assigned` 알림 메시지의 일부로 전송됩니다.

위 메시지는 알림을 받은 후 소유권이 변경된 NFT와 상호작용하는 주요 방법입니다.

예를 들어, 위 메시지 유형은 종종 지갑 스마트 계약에서 NFT 항목 스마트 계약으로 메시지를 보낼 때 사용됩니다. NFT 스마트 계약이 이 메시지를 수신하고 실행하면, NFT 계약의 저장소 (내부 계약 데이터)가 업데이트되며, 소유자의 ID도 업데이트됩니다. 이러한 방식으로 NFT 항목 (계약)이 올바르게 소유자를 변경합니다. 이는 표준 NFT 전송 과정을 설명합니다.

이 경우, 새로운 소유자가 소유권 전송 알림을 받을 수 있도록 전달 금액을 적절한 값으로 설정해야 합니다 (일반 지갑의 경우 0.01 TON, NFT를 전송하여 계약을 실행하려는 경우 더 많은 금액). 이는 새 소유자가 알림 없이 NFT를 수신했다는 사실을 알 수 없기 때문입니다.

## NFT 데이터 검색

대부분의 SDK는 NFT 데이터를 검색하기 위해 사용할 수 있는 핸들러를 제공하며, [tonweb(js)](https://github.com/toncenter/tonweb/blob/b550969d960235314974008d2c04d3d4e5d1f546/src/contract/token/nft/NftItem.js#L38), [tonutils-go](https://github.com/xssnick/tonutils-go/blob/fb9b3fa7fcd734eee73e1a73ab0b76d2fb69bf04/ton/nft/item.go#L132), [pytonlib](https://github.com/toncenter/pytonlib/blob/d96276ec8a46546638cb939dea23612876a62881/pytonlib/client.py#L771) 등이 이에 포함됩니다.

NFT 데이터를 수신하려면 `get_nft_data()` 검색 메커니즘을 사용해야 합니다. 예를 들어, 아래 NFT 항목 주소 `EQB43-VCmf17O7YMd51fAvOjcMkCw46N_3JMCoegH_ZDo40e` (TON DNS 도메인인 [foundation.ton](https://tonscan.org/address/EQB43-VCmf17O7YMd51fAvOjcMkCw46N_3JMCoegH_ZDo40e)로도 알려짐)를 확인해야 합니다.

먼저, toncenter.com API를 사용하여 get 메서드를 실행해야 합니다:

```
curl -X 'POST' \
  'https://toncenter.com/api/v2/runGetMethod' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "address": "EQB43-VCmf17O7YMd51fAvOjcMkCw46N_3JMCoegH_ZDo40e",
  "method": "get_nft_data",
  "stack": []
}'
```

응답은 일반적으로 다음과 유사합니다:

```json
{
  "ok": true,
  "result": {
    "@type": "smc.runResult",
    "gas_used": 1581,
    "stack": [
      // init
      [ "num", "-0x1" ],
      // index
      [ "num", "0x9c7d56cc115e7cf6c25e126bea77cbc3cb15d55106f2e397562591059963faa3" ],
      // collection_address
      [ "cell", { "bytes": "te6cckEBAQEAJAAAQ4AW7psr1kCofjDYDWbjVxFa4J78SsJhlfLDEm0U+hltmfDtDcL7" } ],
      // owner_address
      [ "cell", { "bytes": "te6cckEBAQEAJAAAQ4ATtS415xpeB1e+YRq/IsbVL8tFYPTNhzrjr5dcdgZdu5BlgvLe" } ],
      // content
      [ "cell", { "bytes": "te6cckEBCQEA7AABAwDAAQIBIAIDAUO/5NEvz/d9f/ZWh+aYYobkmY5/xar2cp73sULgTwvzeuvABAIBbgUGAER0c3/qevIyXwpbaQiTnJ1y+S20wMpSzKjOLEi7Jwi/GIVBAUG/I1EBQhz26hlqnwXCrTM5k2Qg5o03P1s9x0U4CBUQ7G4HAUG/LrgQbAsQe0P2KTvsDm8eA3Wr0ofDEIPQlYa5wXdpD/oIAEmf04AQe/qqXMblNo5fl5kYi9eYzSLgSrFtHY6k/DdIB0HmNQAQAEatAVFmGM9svpAE9og+dCyaLjylPtAuPjb0zvYqmO4eRJF0AIDBvlU=" } ]
    ],
    "exit_code": 0,
    "@extra": "1679535187.3836682:8:0.06118075068995321"
  }
}
```

반환 매개변수:

- `init` - `boolean` - -1은 NFT가 초기화되어 사용 가능함을 의미합니다.
- `index` - `uint256` - 컬렉션 내 NFT의 인덱스입니다. 순차적일 수도 있고 다른 방식으로 도출될 수도 있습니다. 예를 들어, 이는 TON DNS 계약과 함께 사용되는 NFT 도메인 해시를 나타낼 수 있으며, 컬렉션은 지정된 인덱스 내에 고유한 NFT만 가질 수 있습니다.
- `collection_address` - `Cell` - NFT 컬렉션 주소를 포함하는 셀입니다 (비어 있을 수 있습니다).
- `owner_address` - `Cell` - 현재 소유자의 NFT 주소를 포함하는 셀입니다 (비어 있을 수 있습니다).
- `content` - `Cell` - NFT 항목 콘텐츠를 포함하는 셀이며, 파싱이 필요한 경우 TEP-64 표준을 참조해야 합니다.

## 컬렉션 내의 모든 NFT 조회

컬렉션이 정렬되어 있는지 여부에 따라 모든 NFT를 조회하는 프로세스는 다릅니다. 아래에서 각각의 프로세스를 설명합니다.

### 정렬된 컬렉션

정렬된 컬렉션의 모든 NFT를 조회하는 것은 비교적 간단합니다. 필요한 NFT의 수가 이미 알려져 있고, 해당 주소를 쉽게 얻을 수 있기 때문입니다. 이 과정은 다음 단계에 따라 진행됩니다:

1. TonCenter API를 사용하여 `get_collection_data` 메서드를 호출하고 응답에서 `next_item_index` 값을 가져옵니다.
2. `get_nft_address_by_index` 메서드를 사용하여 인덱스 값 `i` (처음에는 0)를 전달하여 컬렉션 내 첫 번째 NFT의 주소를 조회합니다.
3. 이전 단계에서 얻은 주소를 사용하여 NFT 아이템 데이터를 조회합니다. 다음으로, 초기 NFT 컬렉션 스마트 컨트랙트가 NFT 아이템이 보고한 NFT 컬렉션 스마트 컨트랙트와 일치하는지 확인합니다(컬렉션이 다른 사용자의 NFT 스마트 컨트랙트를 탈취하지 않았는지 확인).
4. `get_nft_content` 메서드를 `i`와 이전 단계에서 얻은 `individual_content`와 함께 호출합니다.
5. `i` 값을 1씩 증가시키고 2-5단계를 `i`가 `next_item_index`와 같아질 때까지 반복합니다.
6. 이 시점에서 컬렉션 및 개별 아이템에 대한 필요한 정보를 모두 확보하게 됩니다.

### 비정렬된 컬렉션

비정렬된 컬렉션에서 NFT 목록을 조회하는 것은 더 어렵습니다. 컬렉션에 속한 NFT의 주소를 얻을 수 있는 고유한 방법이 없기 때문입니다. 따라서 컬렉션 컨트랙트의 모든 트랜잭션을 파싱하고, 컬렉션에 속하는 NFT와 일치하는 모든 아웃고잉(outgoing) 메시지를 확인해야 합니다.

이 경우, NFT 데이터를 조회하고 NFT에서 반환된 ID를 사용하여 컬렉션에서 `get_nft_address_by_index` 메서드를 호출해야 합니다. NFT 컨트랙트 주소와 `get_nft_address_by_index` 메서드에서 반환된 주소가 일치하면 해당 NFT가 현재 컬렉션에 속함을 나타냅니다. 그러나 컬렉션으로의 모든 메시지를 파싱하는 것은 시간이 많이 걸릴 수 있으며, 아카이브 노드가 필요할 수 있습니다.

## TON 외부에서 NFT 작업

### NFT 전송

NFT 소유권을 이전하려면 소유자의 지갑에서 NFT 컨트랙트로 내부 메시지를 전송하여 전송 메시지를 포함하는 셀을 생성해야 합니다. 이를 위해 특정 언어에 맞는 라이브러리([tonweb(js)](https://github.com/toncenter/tonweb/blob/b550969d960235314974008d2c04d3d4e5d1f546/src/contract/token/nft/NftItem.js#L65), [ton(js)](https://github.com/getgems-io/nft-contracts/blob/debcd8516b91320fa9b23bff6636002d639e3f26/packages/contracts/nft-item/NftItem.data.ts#L102), [tonutils-go(go)](https://github.com/xssnick/tonutils-go/blob/fb9b3fa7fcd734eee73e1a73ab0b76d2fb69bf04/ton/nft/item.go#L132))를 사용할 수 있습니다.

전송 메시지가 생성되면 소유자의 지갑 컨트랙트에서 NFT 아이템 컨트랙트 주소로 충분한 TON을 함께 보내어 관련된 트랜잭션 수수료를 충당해야 합니다.

다른 사용자로부터 NFT를 자신에게 전송하려면 TON Connect 2.0이나 단순한 QR 코드를 사용하여 ton:// 링크를 포함해야 합니다. 예를 들어:
`ton://transfer/{nft_address}?amount={message_value}&bin={base_64_url(transfer_message)}`

### NFT 수신

특정 스마트 컨트랙트 주소(즉, 사용자의 지갑)에 전송된 NFT를 추적하는 과정은 결제를 추적하는 메커니즘과 유사합니다. 이는 지갑의 모든 새로운 트랜잭션을 감시하고 이를 파싱하는 방식으로 이루어집니다.

다음 단계는 특정 사용 사례에 따라 다를 수 있습니다. 몇 가지 다른 시나리오를 살펴보겠습니다.

#### 알려진 NFT 주소 전송을 기다리는 서비스:

- NFT 아이템 스마트 컨트랙트 주소에서 전송된 새로운 트랜잭션을 확인합니다.
- 메시지 본문에서 첫 번째 32비트를 `uint` 타입으로 읽고, `op::ownership_assigned()`(`0x05138d91`)와 일치하는지 확인합니다.
- 메시지 본문에서 다음 64비트를 `query_id`로 읽습니다.
- 메시지 본문에서 주소를 `prev_owner_address`로 읽습니다.
- 이제 새로운 NFT를 관리할 수 있습니다.

#### 모든 유형의 NFT 전송을 감시하는 서비스:

- 모든 새로운 트랜잭션을 확인하고, 본문 길이가 363비트보다 짧은 트랜잭션은 무시합니다 (OP - 32, QueryID - 64, Address - 267).
- 위 목록에 상세히 설명된 단계를 반복합니다.
- 프로세스가 정상적으로 작동하는 경우, NFT와 소속된 컬렉션을 파싱하여 NFT의 진위 여부를 확인합니다. 이후 NFT가 지정된 컬렉션에 속하는지 확인해야 합니다. 이 과정에 대한 자세한 정보는 `Getting all collection NFTs` 섹션에서 확인할 수 있습니다. 이 프로세스는 NFT 또는 컬렉션의 화이트리스트를 사용하여 간소화할 수 있습니다.
- 이제 새로운 NFT를 관리할 수 있습니다.

#### NFT 전송을 내부 트랜잭션과 연결하기:

이 유형의 트랜잭션이 수신되면, 이전 목록의 단계를 반복해야 합니다. 이 과정이 완료되면 `prev_owner_address` 값을 읽은 후 메시지 본문에서 `RANDOM_ID` 매개변수를 `uint32`로 읽어올 수 있습니다.

#### 알림 메시지 없이 전송된 NFT:

위의 모든 전략은 서비스가 올바르게 NFT 전송 내에서 전달 메시지를 생성하는지에 의존합니다. 이 작업이 수행되지 않으면 우리가 NFT를 수신했는지 알 수 없습니다. 그러나 다음과 같은 몇 가지 해결 방법이 있습니다:

위에서 설명한 모든 전략은 서비스가 NFT 전송 내에서 전달 메시지를 올바르게 생성하는 것을 전제로 합니다. 이 프로세스가 수행되지 않으면 NFT가 올바른 당사자에게 전송되었는지 여부가 명확하지 않습니다. 하지만 이 시나리오에서 가능한 몇 가지 해결 방법이 있습니다:

- 적은 수의 NFT가 예상되는 경우, 이를 주기적으로 파싱하여 소유자가 해당 계약 유형으로 변경되었는지 확인할 수 있습니다.
- 많은 수의 NFT가 예상되는 경우, 모든 새로운 블록을 파싱하여 `op::transfer` 메서드를 사용하여 NFT 목적지로 보낸 호출이 있었는지 확인할 수 있습니다. 이와 같은 트랜잭션이 시작되면 NFT 소유자를 확인하고 전송을 받을 수 있습니다.
- 전송 내에서 새로운 블록을 파싱할 수 없는 경우, 사용자가 스스로 NFT 소유권 확인 프로세스를 트리거할 수 있습니다. 이렇게 하면 알림 메시지 없이 NFT를 전송한 후에도 NFT 소유권 확인 프로세스를 트리거할 수 있습니다.

## 스마트 컨트랙트에서 NFT와 상호작용

이제 NFT를 보내고 받는 기본 사항을 다뤘으므로, [NFT Sale](https://github.com/ton-blockchain/token-contract/blob/1ad314a98d20b41241d5329e1786fc894ad811de/nft/nft-sale.fc) 컨트랙트 예제를 사용하여 스마트 컨트랙트에서 NFT를 받고 전송하는 방법을 살펴보겠습니다.

### NFT 전송

이 예제에서 NFT 전송 메시지는 [67번째 줄](https://www.google.com/url?q=https://github.com/ton-blockchain/token-contract/blob/1ad314a98d20b41241d5329e1786fc894ad811de/nft/nft-sale.fc%23L67\&sa=D\&source=docs\&ust=1685436161341866\&usg=AOvVaw1yuoIzcbEuvqMS4xQMqfXE)에 있습니다:

```
var nft_msg = begin_cell()
  .store_uint(0x18, 6)
  .store_slice(nft_address)
  .store_coins(0)
  .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; default message headers (see sending messages page)
  .store_uint(op::transfer(), 32)
  .store_uint(query_id, 64)
  .store_slice(sender_address) ;; new_owner_address
  .store_slice(sender_address) ;; response_address
  .store_int(0, 1) ;; empty custom_payload
  .store_coins(0) ;; forward amount to new_owner_address
  .store_int(0, 1); ;; empty forward_payload


send_raw_message(nft_msg.end_cell(), 128 + 32);
```

각 코드 줄을 살펴 보겠습니다:

- `store_uint(0x18, 6)` - 메시지 플래그를 저장합니다.
- `store_slice(nft_address)` - 메시지의 목적지(NFT 주소)를 저장합니다.
- `store_coins(0)` - 메시지와 함께 보낼 TON의 양을 0으로 설정합니다. 이는 잔여 잔액으로 메시지를 보내기 위해 `128` [메시지 모드](/develop/smart-contracts/messages#message-modes)가 사용됩니다. 사용자의 전체 잔액이 아닌 다른 금액을 보내려면 이 숫자를 변경해야 합니다. 이 값은 가스 요금 및 기타 전송 비용을 지불하기에 충분해야 합니다.
- `store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1)` - 메시지 헤더의 나머지 구성 요소를 비워 둡니다.
- `store_uint(op::transfer(), 32)` - 메시지 본문의 시작입니다. 여기서 우리는 수신자가 소유권 전송 메시지임을 이해할 수 있도록 전송 OP 코드를 사용하여 시작합니다.
- `store_uint(query_id, 64)` - query_id를 저장합니다.
- `store_slice(sender_address) ;; new_owner_address` - 첫 번째 저장된 주소는 NFT를 전송하고 알림을 보내는 데 사용된 주소입니다.
- `store_slice(sender_address) ;; response_address` - 두 번째 저장된 주소는 응답 주소입니다.
- `store_int(0, 1)` - 커스텀 페이로드 플래그를 0으로 설정하여 커스텀 페이로드가 필요하지 않음을 나타냅니다.
- `store_coins(0)` - 메시지와 함께 전달할 TON의 양. 이 예에서는 0으로 설정되어 있지만, 새 소유자에게 NFT가 전송되었음을 알리기 위해 전달 메시지를 생성하려면 이 값을 더 높은 값(예: 최소 0.01 TON)으로 설정하는 것이 좋습니다. 이 금액은 관련된 모든 수수료 및 비용을 충당할 수 있을 정도로 충분해야 합니다.
- `.store_int(0, 1)` - 커스텀 페이로드 플래그입니다. 서비스가 페이로드를 참조로 전달해야 하는 경우 `1`로 설정해야 합니다.

### NFT 수신

NFT를 보낸 후에는 새로운 소유자가 NFT를 수신했는지 확인하는 것이 중요합니다. 이에 대한 좋은 예는 동일한 NFT 판매 스마트 컨트랙트에서 찾을 수 있습니다:

```
slice cs = in_msg_full.begin_parse();
int flags = cs~load_uint(4);

if (flags & 1) {  ;; ignore all bounced messages
    return ();
}
slice sender_address = cs~load_msg_addr();
throw_unless(500, equal_slices(sender_address, nft_address));
int op = in_msg_body~load_uint(32);
throw_unless(501, op == op::ownership_assigned());
int query_id = in_msg_body~load_uint(64);
slice prev_owner_address = in_msg_body~load_msg_addr();
```

다시 각 코드 줄을 살펴보겠습니다:

- `slice cs = in_msg_full.begin_parse();` - 수신 메시지를 파싱하는 데 사용됩니다.
- `int flags = cs~load_uint(4);` - 메시지의 첫 4비트에서 플래그를 로드하는 데 사용됩니다.
- `if (flags & 1) { return (); } ;; 모든 반송된 메시지는 무시` - 메시지가 반송되지 않았는지 확인하는 데 사용됩니다. 다른 이유가 없는 한 모든 수신 메시지에 대해 이 작업을 수행하는 것이 중요합니다. 반송된 메시지는 트랜잭션 수신 중 오류가 발생하여 발신자에게 반환된 메시지입니다.
- `slice sender_address = cs~load_msg_addr();` - 다음으로 메시지 발신자를 로드합니다. 이 경우 특정하게 NFT 주소를 사용합니다.
- `throw_unless(500, equal_slices(sender_address, nft_address));` - 발신자가 실제로 컨트랙트를 통해 전송된 NFT인지 확인합니다. 스마트 컨트랙트에서 NFT 데이터를 파싱하는 것은 매우 어렵기 때문에 대부분의 경우 NFT 주소는 계약 생성 시 사전에 정의됩니다.
- `int op = in_msg_body~load_uint(32);` - 메시지 OP 코드를 로드합니다.
- `throw_unless(501, op == op::ownership_assigned());` - 수신된 OP 코드가 소유권 할당 상수 값과 일치하는지 확인합니다.
- `slice prev_owner_address = in_msg_body~load_msg_addr();` - 이전 소유자 주소는 수신 메시지 본문에서 추출되어 `prev_owner_address` 슬라이스 변수에 로드됩니다. 이는 이전 소유자가 계약을 취소하고 NFT를 반환받고자 할 때 유용할 수 있습니다.

이제 알림 메시지를 성공적으로 파싱하고 검증했으므로 NFT 경매(getgems.io와 같은 NFT 아이템 비즈니스 판매 프로세스를 처리하는)와 같은 판매 스마트 계약을 시작하는 데 사용되는 비즈니스 로직을 진행할 수 있습니다.
