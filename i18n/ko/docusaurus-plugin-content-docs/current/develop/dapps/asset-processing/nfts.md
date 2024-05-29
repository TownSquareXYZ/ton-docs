# NFT 처리

## 개요

이 문서에서는 독자들이 대체 불가능한 토큰에 대해 더 잘 이해할 수 있도록 도와드리겠습니다. 이를 통해 독자들은 NFT와 상호작용하는 방법과 TON 블록체인에서 전송된 트랜잭션을 통해 NFT를 수락하는 방법을 배울 수 있습니다.

아래에 제공된 정보는 독자가 이미 이전 섹션을 자세히 살펴봤다고 가정합니다.
[톤코인 결제 처리 상세 설명 섹션](/개발/앱/자산 처리)을 읽었으며, 지갑 스마트 컨트랙트와 프로그래밍 방식으로 상호 작용하는 방법에 대한 기본적인 이해가 있다고 가정합니다.

## NFT의 기본 이해

TON 블록체인에서 작동하는 NFT는 [TEP-62](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md) 및 [TEP-64](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md) 표준으로 대표됩니다.

오픈 네트워크(TON) 블록체인은 고성능을 염두에 두고 설계되었으며, TON의 컨트랙트 주소를 기반으로 자동 샤딩을 활용하는 기능을 포함하고 있습니다(특정 NFT 디자인을 프로비저닝하는 데 사용됨). 최적의 성능을 달성하기 위해 개별 NFT는 자체 스마트 컨트랙트를 사용해야 합니다. 이를 통해 크든 작든 모든 규모의 NFT 컬렉션을 생성할 수 있으며, 개발 비용과 성능 문제도 줄일 수 있습니다. 그러나 이 접근 방식은 NFT 컬렉션 개발 시 새로운 고려 사항도 도입합니다.

각 NFT는 자체 스마트 컨트랙트를 사용하기 때문에 단일 컨트랙트를 사용하여 NFT 컬렉션 내의 개별 NFT에 대한 정보를 얻을 수 없습니다. 전체 컬렉션과 컬렉션 내의 각 개별 NFT에 대한 정보를 검색하려면 컬렉션 컨트랙트와 각 개별 NFT 컨트랙트를 개별적으로 쿼리해야 합니다. 같은 이유로 NFT 전송을 추적하려면 특정 컬렉션 내의 개별화된 각 NFT에 대한 모든 트랜잭션을 추적해야 합니다.

### NFT 컬렉션

NFT 컬렉션은 NFT 콘텐츠를 인덱싱하고 저장하는 역할을 하는 컨트랙트로, 다음과 같은 인터페이스를 포함해야 합니다:

#### 메서드 `get_collection_data` 가져오기

```
(int next_item_index, cell collection_content, slice owner_address) get_collection_data()
```

수집에 대한 일반 정보를 검색하며, 이는 다음과 같이 표시됩니다:

1. 다음 항목 인덱스`- 컬렉션이 정렬된 경우, 이 분류는 컬렉션의 총 NFT 수와 발행에 사용되는 다음 인덱스를 나타냅니다. 정렬되지 않은 컬렉션의 경우`next_item_index\` 값은 -1이며, 이는 컬렉션이 고유한 메커니즘(예: TON DNS 도메인의 해시)을 사용하여 NFT를 추적한다는 의미입니다.
2. 'collection_content\` - 컬렉션 콘텐츠를 TEP-64 호환 형식으로 나타내는 셀입니다.
3. '소유자_주소' - 컬렉션 소유자의 주소가 포함된 슬라이스(이 값은 비워둘 수도 있습니다).

#### 메서드 `get_nft_address_by_index` 가져오기

```
(slice nft_address) get_nft_address_by_index(int index)
```

이 방법은 NFT의 진위 여부를 확인하고 특정 컬렉션에 실제로 속하는지 확인하는 데 사용할 수 있습니다. 또한 사용자가 컬렉션의 인덱스를 제공해 NFT의 주소를 검색할 수 있습니다. 이 메서드는 제공된 인덱스에 해당하는 NFT의 주소가 포함된 슬라이스를 반환해야 합니다.

#### 메서드 `get_nft_content` 가져오기

```
(cell full_content) get_nft_content(int index, cell individual_content)
```

컬렉션은 NFT의 공통 데이터 저장소 역할을 하므로, 이 메서드는 NFT 콘텐츠를 완성하는 데 필요합니다. 이 메서드를 사용하려면 먼저 해당 `get_nft_data()` 메서드를 호출하여 NFT의 `individual_content`를 가져와야 합니다. 개별_콘텐츠`를 얻은 후 NFT 인덱스와 `individual_content`셀을 가지고`get_nft_content()\` 메서드를 호출할 수 있습니다. 이 메서드는 NFT의 전체 콘텐츠가 포함된 TEP-64 셀을 반환해야 합니다.

### NFT 아이템

기본 NFT는 구현해야 합니다:

#### 메서드 `get_nft_data()` 가져오기

```
(int init?, int index, slice collection_address, slice owner_address, cell individual_content) get_nft_data()
```

#### 전송\`에 대한 인라인 메시지 핸들러

```
transfer#5fcc3d14 query_id:uint64 new_owner:MsgAddress response_destination:MsgAddress custom_payload:(Maybe ^Cell) forward_amount:(VarUInteger 16) forward_payload:(Either Cell ^Cell) = InternalMsgBody
```

메시지를 작성하는 데 필요한 각 매개변수를 살펴보겠습니다:

1. `OP` - `0x5fcc3d14` - 전송 메시지 내에서 TEP-62 표준에 의해 정의된 상수입니다.
2. 쿼리 아이디`-`uint64\` - 메시지 추적에 사용되는 uint64 번호입니다.
3. 새로운 소유자 주소`-`메시지 주소\` - NFT를 전송하는 데 사용된 컨트랙트의 주소입니다.
4. 응답 주소`-`메시지 주소\` - 초과 자금을 이체하는 데 사용되는 주소입니다. 일반적으로 거래 수수료를 지불하고 필요한 경우 새 이체를 생성하기에 충분한 자금이 있는지 확인하기 위해 추가 금액(예: 1톤)이 NFT 컨트랙트에 전송됩니다. 트랜잭션 내에서 사용되지 않은 모든 자금은 '응답 주소'로 전송됩니다.
5. 전달 금액`-`코인`- 전달 메시지와 함께 사용되는 TON의 양(보통 0.01 TON으로 설정됨). TON은 비동기식 아키텍처를 사용하기 때문에 트랜잭션을 성공적으로 수신하는 즉시 NFT의 새 소유자에게 알림이 전송되지 않습니다. 새 소유자에게 알리기 위해 NFT 스마트 컨트랙트에서`forwardAmount`를 사용하여 표시된 값과 함께 `newOwnerAddress`로 내부 메시지를 보냅니다. 전달 메시지는 '소유권 할당' OP(`0x05138d91\`)로 시작하고, 이전 소유자의 주소와 '전달 페이로드'(있는 경우)가 뒤따릅니다.
6. 전달 페이로드`-`슬라이스 | 셀`-`소유권_지정\` 알림 메시지의 일부로 전송됩니다.

이 메시지(위에서 설명한 대로)는 위 메시지로 인해 알림을 받은 후 소유권이 변경되는 NFT와 상호작용하는 데 주로 사용되는 방법입니다.

예를 들어, 위의 메시지 유형은 종종 월렛 스마트 콘트랙트에서 NFT 아이템 스마트 콘트랙트를 전송하는 데 사용됩니다. NFT 스마트 컨트랙트가 이 메시지를 수신하고 이를 실행하면, NFT 컨트랙트의 저장소(내부 컨트랙트 데이터)가 소유자의 ID와 함께 업데이트됩니다. 이러한 방식으로 NFT 아이템(컨트랙트)의 소유자가 올바르게 변경됩니다. 이 프로세스는 표준 NFT 전송에 대해 자세히 설명합니다.

이 경우, 새로운 소유자가 소유권 이전 관련 알림을 받을 수 있도록 포지션 금액을 적절한 값(일반 지갑의 경우 0.01톤 이상, NFT를 전송하여 계약을 체결하려는 경우)으로 설정해야 합니다. 이 알림이 없으면 새 소유자는 NFT를 받았다는 알림을 받지 못하기 때문에 이는 중요합니다.

## NFT 데이터 검색

대부분의 SDK는 NFT 데이터 검색을 위해 바로 사용할 수 있는 핸들러를 사용합니다: [tonweb(js)](https://github.com/toncenter/tonweb/blob/b550969d960235314974008d2c04d3d4e5d1f546/src/contract/token/nft/NftItem.js#L38), [tonutils-go](https://github.com/xssnick/tonutils-go/blob/fb9b3fa7fcd734eee73e1a73ab0b76d2fb69bf04/ton/nft/item.go#L132), [pytonlib](https://github.com/toncenter/pytonlib/blob/d96276ec8a46546638cb939dea23612876a62881/pytonlib/client.py#L771) 등이 있습니다.

NFT 데이터를 받으려면 `get_nft_data()` 검색 메커니즘을 사용해야 합니다. 예를 들어, 다음 NFT 아이템 주소 `EQB43-VCmf17O7YMd51fAvOjcMkCw46N_3JMCoegH_ZDo40e`([foundation.ton](https://tonscan.org/address/EQB43-VCmf17O7YMd51fAvOjcMkCw46N_3JMCoegH_ZDo40e) 도메인으로도 알려져 있음)를 확인해야 합니다.

먼저 톤센터닷컴 API를 사용하여 다음과 같이 get 메서드를 실행해야 합니다.

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

응답은 일반적으로 다음과 비슷합니다:

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

매개변수를 반환합니다:

- 초기화`-`부울\` - -1은 NFT가 초기화되어 사용할 수 있음을 의미합니다.
- 인덱스`-`uint256\` - 컬렉션에 있는 NFT의 인덱스입니다. 순차적이거나 다른 방식으로 파생될 수 있습니다. 예를 들어, 이것은 TON DNS 컨트랙트에 사용되는 NFT 도먼 해시를 나타낼 수 있지만, 컬렉션에는 주어진 인덱스 내에 고유한 NFT가 하나만 있어야 합니다.
- 'collection_address\` - '셀' - NFT 컬렉션 주소가 포함된 셀(비어 있을 수 있음).
- '소유자 주소' - '셀' - 현재 소유자의 NFT 주소가 포함된 셀(비어 있을 수 있음).
- 'content\` - '셀' - NFT 항목 콘텐츠가 포함된 셀(구문 분석이 필요한 경우 TEP-64 표준을 참조해야 함).

## 컬렉션 내 모든 NFT 검색하기

컬렉션 내의 모든 NFT를 검색하는 프로세스는 컬렉션의 주문 여부에 따라 다릅니다. 아래에서 두 가지 프로세스에 대해 간략히 설명하겠습니다.

### 주문한 컬렉션

정렬된 컬렉션의 모든 NFT를 검색하는 것은 검색에 필요한 NFT의 수를 이미 알고 있고 주소를 쉽게 구할 수 있기 때문에 비교적 간단합니다. 이 프로세스를 완료하려면 다음 단계를 순서대로 따라야 합니다:

1. 수집 컨트랙트 내에서 TonCenter API를 사용하여 `get_collection_data` 메서드를 호출하고 응답에서 `next_item_index` 값을 검색합니다.
2. 인덱스 값 `i`(초기에는 0으로 설정됨)를 전달하여 `get_nft_address_by_index` 메서드를 사용하면 컬렉션에서 첫 번째 NFT의 주소를 검색할 수 있습니다.
3. 이전 단계에서 얻은 주소를 사용해 NFT 아이템 데이터를 검색합니다. 다음으로, 초기 NFT 컬렉션 스마트 컨트랙트가 NFT 아이템 자체에서 보고한 NFT 컬렉션 스마트 컨트랙트와 일치하는지 확인합니다(컬렉션이 다른 사용자의 NFT 스마트 컨트랙트를 도용하지 않았는지 확인하기 위해).
4. 이전 단계의 `i` 및 `individual_content`를 사용하여 `get_nft_content` 메서드를 호출합니다.
5. i`를 1씩 증가시키고 `i`가 `next_item_index\`와 같을 때까지 2~5단계를 반복합니다.
6. 이 시점에서 회원님은 컬렉션과 개별 항목에서 필요한 정보를 소유하게 됩니다.

### 주문하지 않은 컬렉션

정렬되지 않은 컬렉션에서 NFT 목록을 검색하는 것은 컬렉션에 속한 NFT의 주소를 얻을 수 있는 고유한 방법이 없기 때문에 더 어렵습니다. 따라서 컬렉션 컨트랙트의 모든 트랜잭션을 파싱하고 발신 메시지를 모두 확인하여 컬렉션에 속한 NFT에 해당하는 트랜잭션을 식별해야 합니다.

이를 위해서는 NFT 데이터를 검색해야 하며, 컬렉션에서 NFT가 반환한 ID로 `get_nft_address_by_index` 메서드를 호출합니다. NFT 컨트랙트 주소와 `get_nft_address_by_index` 메서드가 반환한 주소가 일치하면, 해당 NFT가 현재 컬렉션에 속해 있음을 나타냅니다. 그러나 컬렉션에 대한 모든 메시지를 구문 분석하는 데 시간이 오래 걸릴 수 있으며 아카이브 노드가 필요할 수 있습니다.

## TON 외부에서 NFT로 작업하기

### NFT 보내기

NFT 소유권을 이전하려면 전송 메시지가 포함된 셀을 생성하여 NFT 소유자의 지갑에서 NFT 컨트랙트로 내부 메시지를 보내야 합니다. 이는 특정 언어에 대한 라이브러리(예: [tonweb(js)](https://github.com/toncenter/tonweb/blob/b550969d960235314974008d2c04d3d4e5d1f546/src/contract/token/nft/NftItem.js#L65), [ton(js)](https://github.com/getgems-io/nft-contracts/blob/debcd8516b91320fa9b23bff6636002d639e3f26/packages/contracts/nft-item/NftItem.data.ts#L102), [tonutils-go(go)](https://github.com/xssnick/tonutils-go/blob/fb9b3fa7fcd734eee73e1a73ab0b76d2fb69bf04/ton/nft/item.go#L132))를 사용하여 수행할 수 있습니다.

전송 메시지가 생성되면 소유자의 지갑 컨트랙트에서 NFT 아이템 컨트랙트 주소로 전송해야 하며, 관련 거래 수수료를 충당할 수 있는 적절한 양의 TON을 포함해야 합니다.

다른 사용자로부터 본인에게 NFT를 전송하려면 TON Connect 2.0 또는 ton:// 링크가 포함된 간단한 QR 코드를 사용해야 합니다. 예:
`ton://transfer/{nft_address}?amount={message_value}&bin={base_64_url(transfer_message)}`

### NFT 수신

특정 스마트 컨트랙트 주소(예: 사용자의 지갑)로 전송된 NFT를 추적하는 과정은 결제 추적에 사용되는 메커니즘과 유사합니다. 이는 지갑의 모든 새 트랜잭션을 수신하고 이를 파싱하여 완료됩니다.

다음 단계는 특정 사용 사례에 따라 달라질 수 있습니다. 아래에서 몇 가지 다양한 시나리오를 살펴보겠습니다.

#### 알려진 NFT 주소 전송을 기다리는 서비스입니다:

- NFT 아이템 스마트 컨트랙트 주소에서 전송된 새 트랜잭션을 확인합니다.
- 메시지 본문의 첫 32비트를 `uint` 타입을 사용하여 읽고 `op::ownership_assigned()`(`0x05138d91`)와 같은지 확인합니다.
- 메시지 본문에서 다음 64비트를 `query_id`로 읽습니다.
- 메시지 본문에서 '이전_소유자_주소'로 주소를 읽습니다.
- 이제 새로운 NFT를 관리할 수 있습니다.

#### 모든 유형의 NFT 전송을 수신하는 서비스입니다:

- 모든 새 트랜잭션을 확인하고 본문 길이가 363비트(OP-32, 쿼리ID-64, 주소-267) 미만인 트랜잭션은 무시합니다.
- 위의 이전 목록에 설명된 단계를 반복합니다.
- 프로세스가 올바르게 작동하는 경우, NFT를 파싱하여 NFT의 진위 여부와 해당 NFT가 속한 컬렉션을 확인해야 합니다. 다음으로 NFT가 지정된 컬렉션에 속하는지 확인해야 합니다. 이 프로세스에 대한 자세한 내용은 '모든 컬렉션 NFT 가져오기' 섹션에서 확인할 수 있습니다. 이 과정은 NFT 또는 컬렉션의 화이트리스트를 사용하여 간소화할 수 있습니다.
- 이제 새로운 NFT를 관리할 수 있습니다.

#### NFT 전송을 내부 거래에 연결합니다:

이 유형의 트랜잭션이 수신되면 이전 목록의 단계를 반복해야 합니다. 이 프로세스가 완료되면 `prev_owner_address` 값을 읽은 후 메시지 본문에서 uint32를 읽어 `RANDOM_ID` 파라미터를 검색할 수 있습니다.

#### 알림 메시지 없이 전송된 NFT:

위에서 설명한 모든 전략은 서비스가 NFT 전송과 함께 전달 메시지를 올바르게 생성하는 데 의존합니다. 이렇게 하지 않으면 NFT를 전송했다는 사실을 알 수 없습니다. 하지만 몇 가지 해결 방법이 있습니다:

위에서 설명한 모든 전략은 서비스가 NFT 전송 내에서 전달 메시지를 올바르게 생성하는 것을 전제로 합니다. 이 프로세스가 수행되지 않으면 NFT가 올바른 당사자에게 전송되었는지 여부가 명확하지 않습니다. 하지만 이 시나리오에서 가능한 몇 가지 해결 방법이 있습니다:

- 적은 수의 NFT가 예상되는 경우 주기적으로 파싱하여 소유자가 해당 컨트랙트 유형으로 변경되었는지 확인할 수 있습니다.
- 많은 수의 NFT가 예상되는 경우, 모든 새로운 블록을 파싱하고 `op::transfer` 메서드를 사용하여 NFT 대상에게 전송된 호출이 있는지 확인할 수 있습니다. 이와 같은 트랜잭션이 시작되면 NFT 소유자를 확인하고 전송을 받을 수 있습니다.
- 전송 중에 새 블록을 파싱할 수 없는 경우, 사용자가 직접 NFT 소유권 확인 프로세스를 트리거할 수 있습니다. 이렇게 하면 알림 없이 NFT를 전송한 후 NFT 소유권 확인 프로세스를 트리거할 수 있습니다.

## 스마트 컨트랙트에서 NFT와 상호작용하기

이제 NFT를 보내고 받는 기본 사항을 살펴보았으니, [NFT 판매](https://github.com/ton-blockchain/token-contract/blob/1ad314a98d20b41241d5329e1786fc894ad811de/nft/nft-sale.fc) 컨트랙트 예시를 사용하여 스마트 컨트랙트에서 NFT를 받고 전송하는 방법을 살펴보겠습니다.

### NFT 보내기

이 예시에서 NFT 전송 메시지는 [67줄](https://www.google.com/url?q=https://github.com/ton-blockchain/token-contract/blob/1ad314a98d20b41241d5329e1786fc894ad811de/nft/nft-sale.fc%23L67\&sa=D\&source=docs\&ust=1685436161341866\&usg=AOvVaw1yuoIzcbEuvqMS4xQMqfXE)에서 찾을 수 있습니다:

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
- `store_slice(nft_address)` - 메시지 대상(NFT 주소)을 저장합니다.
- store_coins(0)`-`128\` [메시지 모드](/개발/스마트컨트랙트/메시지#메시지 모드)를 사용하여 잔액으로 메시지를 전송하기 때문에 메시지와 함께 전송할 TON의 양이 0으로 설정되어 있습니다. 사용자의 전체 잔액 이외의 금액을 보내려면 숫자를 변경해야 합니다. 이 금액은 가스 요금과 송금 금액을 모두 지불할 수 있을 만큼 충분히 커야 한다는 점에 유의하세요.
- store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1)\` - 메시지 헤더를 구성하는 나머지 구성 요소는 비워둡니다.
- `store_uint(op::transfer(), 32)` - 이것이 msg_body의 시작입니다. 여기서는 수신자가 전송 소유권 메시지를 이해할 수 있도록 전송 OP 코드를 사용하는 것부터 시작합니다.
- `store_uint(query_id, 64)` - 쿼리 ID 저장
- `store_slice(sender_address) ;; new_owner_address` - 첫 번째 저장된 주소는 NFT 전송 및 알림 전송에 사용되는 주소입니다.
- `store_slice(sender_address) ;; response_address` - 두 번째로 저장된 주소는 응답 주소입니다.
- `store_int(0, 1)` - 사용자 지정 페이로드 플래그가 0으로 설정되어 사용자 지정 페이로드가 필요하지 않음을 나타냅니다.
- `store_coins(0)` - 메시지와 함께 전달할 TON의 양입니다. 이 예시에서는 0으로 설정되어 있지만, 전달 메시지를 생성하고 새 소유자에게 NFT를 받았음을 알리려면 이 값을 더 큰 금액(예: 0.01 TON 이상)으로 설정하는 것이 좋습니다. 이 금액은 관련 수수료와 비용을 충당하기에 충분한 금액이어야 합니다.
- .store_int(0, 1)`- 사용자 정의 페이로드 플래그. 서비스에서 페이로드를 참조로 전달해야 하는 경우`1\`로 설정해야 합니다.

### NFT 수신

NFT를 전송한 후에는 새 소유자가 언제 수령했는지 확인하는 것이 중요합니다. 이를 확인하는 방법에 대한 좋은 예는 동일한 NFT 판매 스마트 컨트랙트에서 찾을 수 있습니다:

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

각 코드 줄을 다시 살펴 보겠습니다:

- `slice cs = in_msg_full.begin_parse();` - 수신 메시지를 구문 분석하는 데 사용됩니다.
- `int flags = cs~load_uint(4);` - 메시지의 처음 4비트에서 플래그를 로드하는 데 사용됩니다.
- `if (flags & 1) { return (); } ;; 반송된 모든 메시지 무시` - 메시지가 반송되지 않았는지 확인하는 데 사용됩니다. 특별한 이유가 없는 한 모든 수신 메시지에 대해 이 프로세스를 수행하는 것이 중요합니다. 반송된 메시지는 트랜잭션을 수신하려고 시도하는 동안 오류가 발생하여 발신자에게 반송된 메시지입니다.
- `슬라이스 발신자 주소 = cs~load_msg_addr();` - 다음으로 메시지 발신자 주소가 로드됩니다. 이 경우 특히 NFT 주소를 사용합니다.
- `throw_unless(500, equal_slices(sender_address, nft_address));` - 발신자가 실제로 컨트랙트를 통해 전송되어야 하는 NFT인지 확인하는 데 사용됩니다. 스마트 컨트랙트에서 NFT 데이터를 구문 분석하는 것은 매우 어렵기 때문에 대부분의 경우 NFT 주소는 컨트랙트 생성 시 미리 정의되어 있습니다.
- `int op = in_msg_body~load_uint(32);` - 메시지 OP 코드를 로드합니다.
- `throw_unless(501, op == op::ownership_assigned());` - 수신된 OP 코드가 소유권이 할당된 상수 값과 일치하는지 확인합니다.
- `slice prev_owner_address = in_msg_body~load_msg_addr();` - 수신 메시지 본문에서 추출하여 `prev_owner_address` 슬라이스 변수에 로드하는 이전 소유자 주소입니다. 이는 이전 소유자가 컨트랙트를 취소하고 NFT를 반환받기로 선택한 경우 유용할 수 있습니다.

이제 알림 메시지를 성공적으로 구문 분석하고 유효성을 검사했으므로, 판매 스마트 컨트랙트를 시작하는 데 사용되는 비즈니스 로직을 진행할 수 있습니다(getgems.io와 같은 NFT 경매의 NFT 아이템 비즈니스 판매 프로세스를 처리하는 역할을 함).
