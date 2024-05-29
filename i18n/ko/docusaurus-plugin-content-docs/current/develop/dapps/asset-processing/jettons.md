'@theme/Tabs'에서 탭 가져오기;
'@theme/TabItem'에서 탭 항목 가져오기;
'@site/src/components/button'에서 버튼 가져오기;

# 제톤 처리

## 제톤 처리 모범 사례

제톤은 톤 블록체인의 토큰으로, 이더리움의 ERC-20 토큰과 비슷하게 생각할 수 있습니다.

:::info 거래 확인
TON 거래는 한 번만 확인하면 되돌릴 수 없습니다. 최상의 UX/UI를 위해 추가 대기를 피하세요.
:::

#### 출금

[하이로드 월렛 v3](/참여하기/월렛/계약#하이로드-월렛-v3) - 제톤 출금의 표준이 되는 톤 블록체인의 최신 솔루션입니다. 일괄 인출을 활용할 수 있습니다.

[일괄 출금](https://github.com/toncenter/examples/blob/main/withdrawals-jettons-highload-batch.js) - 여러 개의 출금이 일괄적으로 전송되어 빠르고 저렴하게 출금할 수 있습니다.

#### 예금

:::info
더 나은 성능을 위해 여러 개의 메모 입금 지갑을 설정하는 것이 좋습니다.
:::

[메모 입금](https://github.com/toncenter/examples/blob/main/deposits-jettons.js) - 하나의 입금 지갑을 보관할 수 있으며, 사용자가 시스템에서 식별할 수 있도록 메모를 추가합니다. 즉, 전체 블록체인을 스캔할 필요는 없지만 사용자에게는 약간 덜 쉽습니다.

[메모 없는 입금](https://github.com/gobicycle/bicycle) - 이 솔루션도 존재하지만 통합하기가 더 어렵습니다. 하지만 이 방법을 원하신다면 저희가 도와드릴 수 있습니다. 이 방식을 도입하기로 결정하기 전에 미리 알려주시기 바랍니다.

### 추가 정보

:::caution 거래 알림
사용자가 제톤을 출금할 때 사용자 지정 메모를 설정할 수 있도록 허용하는 경우 - 메모(텍스트 코멘트)가 첨부될 때마다 forwardAmount를 0.000000001 톤(1나노톤)으로 설정해야 합니다. 그렇지 않으면 표준을 준수하지 않으며 다른 CEX 및 기타 서비스에서 이체를 처리할 수 없게 됩니다.
:::

- TON 재단의 공식 JS 라이브러리인 [tonweb](https://github.com/toncenter/tonweb)에서 JS 라이브러리 예제를 확인하시기 바랍니다.

- Java를 사용하려면 [ton4j](https://github.com/neodix42/ton4j/tree/main)를 살펴보세요.

- Go의 경우 [tonutils-go](https://github.com/xssnick/tonutils-go)를 고려해야 합니다. 현재로서는 JS 라이브러리를 권장합니다.

## CEX를 위한 준비된 솔루션

### 토나피 임베드

토나피 임베디드 - 입출금과 함께 작동하도록 설계된 온프레미스 솔루션으로, 고성능의 가벼운 배포를 보장합니다.

- 모든 톤 라이트서버에서 실행되는 신뢰 없는 시스템.
- 톤코인 및 제톤에 대한 입금 및 출금도 유지합니다.
- TF 코어 팀에서 제공하는 권장 MEMO 입금 및 고부하 출금 가이드라인에 따라 개발된 솔루션입니다.

협조가 필요한 경우 [@tonrostislav](https://t.me/tonrostislav)로 문의하시기 바랍니다.

## 제튼 프로세싱 글로벌 개요

### 콘텐츠 목록

:::tip
다음 문서에서는 제톤 아키텍처 전반에 대한 자세한 설명과 EVM 및 다른 블록체인과 다를 수 있는 TON의 핵심 개념에 대해 설명합니다. 이는 TON을 제대로 이해하기 위해 반드시 읽어야 할 중요한 문서이며, 여러분에게 큰 도움이 될 것입니다.
:::

이 문서에서는 다음 내용을 순서대로 설명합니다:

1. 소개
2. 아키텍처
3. 제톤 마스터 계약(토큰 마이너)
4. 제톤 월렛 계약(사용자 월렛)
5. 메시지 레이아웃
6. 제톤 처리(오프체인)
7. 제톤 처리(온체인)
8. 지갑 처리
9. 모범 사례

### 소개

:::info
TON 트랜잭션은 한 번만 확인하면 되돌릴 수 없습니다.
명확한 이해를 위해 [이 문서 섹션](/개발/앱/자산 처리/)에 설명된 자산 처리의 기본 원칙을 숙지하고 있어야 합니다. 특히 [컨트랙트](/학습/개요/주소#모든 것이 스마트 컨트랙트), [지갑](/개발/스마트 컨트랙트/자습서/지갑), [메시지](/개발/스마트 컨트랙트/가이드라인/메시지 전달 보장) 및 배포 프로세스에 대해 숙지하는 것이 중요합니다.
:::

제톤 처리에 대한 핵심 설명으로 빠르게 이동합니다:

```mdx-code-block
<Button href="/develop/dapps/asset-processing/jettons#accepting-jettons-from-users-through-a-centralized-wallet" colorType={'primary'} sizeType={'sm'}>
```

중앙 집중식 처리

```mdx-code-block
</Button>
```

```mdx-code-block
<Button href="/develop/dapps/asset-processing/jettons#accepting-jettons-from-user-deposit-addresses"
        colorType="secondary" sizeType={'sm'}>
```

온체인 처리

```mdx-code-block
</Button>
```

<br></br><br></br>

TON 블록체인과 그 기반 생태계는 대체 가능한 토큰(FT)을 제톤으로 분류합니다. TON 블록체인에는 샤딩이 적용되기 때문에 대체 가능한 토큰의 구현은 유사한 블록체인 모델과 비교할 때 고유합니다.

이 분석에서는 제톤 [동작](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md) 및 [메타데이터](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md)를 자세히 설명하는 공식 표준에 대해 자세히 살펴봅니다.
샤딩에 초점을 맞춘 제튼 아키텍처의 덜 공식적인 개요는
[제튼의 해부학 블로그 게시물](https://blog.ton.org/how-to-shard-your-ton-smart-contract-and-why-studying-the-anatomy-of-tons-jettons)에서 확인할 수 있습니다.

또한, 사용자가 문자 메모를 사용하지 않고 별도의 입금 주소를 사용하여 톤코인과 제톤을 모두 입출금할 수 있는 타사 오픈소스 톤 결제 프로세서([자전거](https://github.com/gobicycle/bicycle)에 대한 구체적인 내용도 안내해드렸습니다.

## 제튼 아키텍처

TON의 표준화된 토큰은 다음과 같은 스마트 컨트랙트 세트를 사용하여 구현됩니다:

- [제톤 마스터](https://github.com/ton-blockchain/token-contract/blob/main/ft/jetton-minter.fc) 스마트 컨트랙트
- [제튼 월렛](https://github.com/ton-blockchain/token-contract/blob/main/ft/jetton-wallet.fc) 스마트 컨트랙트

```mdx-code-block
<p align="center">
  <br />
    <img width="420" src="/img/docs/asset-processing/jetton_contracts.svg" alt="contracts scheme" />
      <br />
</p>
```

## 제톤 마스터 스마트 컨트랙트

젯튼 마스터 스마트 컨트랙트는 젯튼에 대한 일반 정보를 저장합니다(

총 공급량, 메타데이터 링크 또는 메타데이터 자체 포함).

모든 사용자가 진품과 거의 동일한 위조 제톤(임의의 이름, 티커, 이미지 등을 사용하여)을 만들 수 있습니다. 다행히도 위조 제톤은 주소로 구별할 수 있으며 아주 쉽게 식별할 수 있습니다.

톤 사용자의 사기 가능성을 없애기 위해 특정 톤 유형에 대한 원본 제톤 주소(제톤 마스터 계약서)를 조회하거나 프로젝트의 공식 소셜 미디어 채널 또는 웹사이트를 팔로우하여 정확한 정보를 확인하시기 바랍니다. 톤키퍼 톤 자산 목록](https://github.com/tonkeeper/ton-assets)을 통해 사기 가능성을 제거하기 위한 자산을 확인하세요.

### Jetton 데이터 검색

보다 구체적인 Jetton 데이터를 검색하려면 `get_jetton_data()` get 메서드를 사용합니다.

이 메서드는 다음 데이터를 반환합니다:

| 이름              | 유형     | 설명                                                                                                                                                                                                                    |
| --------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `총공급`           | `int`  | 분할할 수 없는 단위로 측정된 발행된 총 제톤 수입니다.                                                                                                                                                                       |
| `mintable`      | `int`  | 는 새 제톤을 발행할 수 있는지 여부를 자세히 설명합니다. 이 값은 -1(발행 가능) 또는 0(발행 불가) 중 하나입니다.                                                                            |
| `admin_address` | `슬라이스` |                                                                                                                                                                                                                       |
| `제톤_콘텐츠`        | `셀`    | TEP-64](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md)에 따른 데이터입니다. |
| `제톤_지갑_코드`      | `셀`    |                                                                                                                                                                                                                       |

톤센터 API](https://toncenter.com/api/v3/#/default/get_jetton_masters_api_v3_jetton_masters_get)에서 `/jetton/masters` 메서드를 사용하여 이미 디코딩된 Jetton 데이터와 메타데이터를 검색할 수도 있습니다. 또한 (js) [tonweb](https://github.com/toncenter/tonweb/blob/master/src/contract/token/ft/JettonMinter.js#L85) 및 (js) [ton-core/ton](https://github.com/ton-core/ton/blob/master/src/jetton/JettonMaster.ts#L28), (go) [tongo](https://github.com/tonkeeper/tongo/blob/master/liteapi/jetton.go#L48) 및 (go) [tonutils-go](https://github.com/xssnick/tonutils-go/blob/33fd62d754d3a01329ed5c904db542ab4a11017b/ton/jetton/jetton.go#L79), (python) [pytonlib](https://github.com/toncenter/pytonlib/blob/d96276ec8a46546638cb939dea23612876a62881/pytonlib/client.py#L742) 및 기타 여러 SDK에 대한 메서드도 개발했습니다.

톤웹](https://github.com/toncenter/tonweb)을 사용하여 get 메서드를 실행하고 오프체인 메타데이터의 URL을 가져오는 예시입니다:

```js
import TonWeb from "tonweb";
const tonweb = new TonWeb();
const jettonMinter = new TonWeb.token.jetton.JettonMinter(tonweb.provider, {address: "<JETTON_MASTER_ADDRESS>"});
const data = await jettonMinter.getJettonData();
console.log('Total supply:', data.totalSupply.toString());
console.log('URI to off-chain metadata:', data.jettonContentUri);
```

#### 제톤 메타데이터

메타데이터 파싱에 대한 자세한 정보는 [여기](/개발/앱/자산-처리/메타데이터)에서 확인할 수 있습니다.

## 제튼 월렛 스마트 컨트랙트

제톤 지갑 컨트랙트는 제톤을 보내고, 받고, 소각하는 데 사용됩니다. 각 _제톤 지갑 컨트랙트_는 특정 사용자의 지갑 잔액 정보를 저장합니다.
특정 경우, 제톤 지갑은 각 제톤 유형에 대한 개별 제톤 보유자를 위해 사용됩니다.

제톤 지갑은 특정 제톤 유형만을 지원하고 관리하는
, 블록체인 상호작용을 위한 지갑과 톤코인 자산(예: v3R2 지갑, 하이로드 지갑 등)만 저장하는
지갑을 혼동해서는 안 됩니다.

제톤 지갑은 스마트 컨트랙트를 사용하며, 소유자의 지갑(
)과 제톤 지갑 간의 내부 메시지를 통해 관리됩니다. 예를 들어 앨리스가 내부에 제톤이 있는 지갑(
)을 관리한다고 가정하면 다음과 같습니다: 앨리스는 제튼 전용으로 설계된 지갑(예: 지갑 버전 v3r2)을 소유하고 있습니다.
앨리스가 관리하는 지갑에서 제톤 전송을 시작하면, 앨리스는 자신의 지갑(
)으로 외부 메시지를 보내고, 그 결과 _그녀의 지갑_이 _그녀의 제톤 지갑_으로 내부 메시지를 보내고
그러면 제톤 지갑이 실제로 토큰 전송을 실행합니다.

### 특정 사용자의 Jetton 지갑 주소 검색하기

소유자 주소(톤 지갑 주소)를 사용하여 젯튼 지갑 주소를 검색하려면
젯튼 마스터 컨트랙트는 `get_wallet_address(slice owner_address)`라는 get 메서드를 제공합니다.

#### API를 사용하여 검색

애플리케이션은 [Toncenter API](https://toncenter.com/api/v3/#/default/run_get_method_api_v3_runGetMethod_post)의 `/runGetMethod` 메서드(
)를 사용하여 소유자의 주소를 셀에 직렬화합니다.

#### SDK를 사용하여 검색

이 프로세스는 다양한 SDK에 있는 즉시 사용 가능한 방법을 사용하여 시작할 수도 있습니다(예: Tonweb SDK를 사용하는\
). 이 프로세스는 다음 문자열을 입력하여 시작할 수 있습니다:

```js
import TonWeb from "tonweb";
const tonweb = new TonWeb();
const jettonMinter = new TonWeb.token.jetton.JettonMinter(tonweb.provider, {address: "<JETTON_MASTER_ADDRESS>"});
const address = await jettonMinter.getJettonWalletAddress(new TonWeb.utils.Address("<OWNER_WALLET_ADDRESS>"));
// It is important to always check that wallet indeed is attributed to desired Jetton Master:
const jettonWallet = new TonWeb.token.jetton.JettonWallet(tonweb.provider, {
  address: jettonWalletAddress
});
const jettonData = await jettonWallet.getData();
if (jettonData.jettonMinterAddress.toString(false) !== new TonWeb.utils.Address(info.address).toString(false)) {
  throw new Error('jetton minter address from jetton wallet doesnt match config');
}

console.log('Jetton wallet address:', address.toString(true, true, true));
```

:::tip
더 많은 예제는 [TON 쿡북](/개발/앱/쿡북#사용자-제톤-지갑-주소 계산 방법)을 참조하세요.
:::

### 특정 Jetton 지갑에 대한 데이터 검색하기

지갑의 계정 잔액, 소유자 식별 정보, 특정 젯튼 지갑 컨트랙트와 관련된 기타 정보를 검색하려면 젯튼 지갑 컨트랙트 내에서 `get_wallet_data()` get 메서드를 사용합니다.

이 메서드는 다음 데이터를 반환합니다:

| 이름                                                 | 유형   |
| -------------------------------------------------- | ---- |
| balance                                            | int  |
| 소유자                                                | 슬라이스 |
| jetton                                             | 슬라이스 |
| 제튼_월렛_코드 | 셀    |

톤센터 API](https://toncenter.com/api/v3/#/default/get_jetton_wallets_api_v3_jetton_wallets_get)를 사용하여 `/jetton/wallets` get 메서드를 사용하여 이전에 디코딩된 젯튼 지갑 데이터를 검색할 수도 있습니다(또는 SDK 내의 메서드). 예를 들어, 톤웹을 사용합니다:

```js
import TonWeb from "tonweb";
const tonweb = new TonWeb();
const walletAddress = "EQBYc3DSi36qur7-DLDYd-AmRRb4-zk6VkzX0etv5Pa-Bq4Y";
const jettonWallet = new TonWeb.token.jetton.JettonWallet(tonweb.provider,{address: walletAddress});
const data = await jettonWallet.getData();
console.log('Jetton balance:', data.balance.toString());
console.log('Jetton owner address:', data.ownerAddress.toString(true, true, true));
// It is important to always check that Jetton Master indeed recognize wallet
const jettonMinter = new TonWeb.token.jetton.JettonMinter(tonweb.provider, {address: data.jettonMinterAddress.toString(false)});
const expectedJettonWalletAddress = await jettonMinter.getJettonWalletAddress(data.ownerAddress.toString(false));
if (expectedJettonWalletAddress.toString(false) !== new TonWeb.utils.Address(walletAddress).toString(false)) {
  throw new Error('jetton minter does not recognize the wallet');
}

console.log('Jetton master address:', data.jettonMinterAddress.toString(true, true, true));
```

### 제튼 월렛 배포

지갑 간에 제톤을 전송할 때 트랜잭션(메시지)에는 네트워크 가스 요금과 제톤 지갑 컨트랙트 코드에 따른 작업 실행에 대한 지불로 일정 금액의 TON
이 필요합니다.
즉, 수신자는 제톤을 받기 전에 제톤 지갑을 배포할 필요가 없습니다.
발신자가 지갑에 필요한 가스 요금을 지불하기에 충분한 TON
을 보유하고 있는 한 수신자의 제톤 지갑은 자동으로 배포됩니다.

## 메시지 레이아웃

:::tip 메시지
메시지[여기](/개발/스마트-계약/가이드라인/메시지-전달-보증)에 대해 자세히 알아보세요.
:::

제톤 지갑과 TON 지갑 간의 통신은 다음과 같은 통신 순서를 통해 이루어집니다:

![](/img/docs/asset-processing/jetton_transfer.svg)

'발신자 -> 발신자' 제튼 월렛\`은 *전송* 메시지 본문에 다음 데이터가 포함되어 있음을 의미합니다:

| 이름                               | 유형     |
| -------------------------------- | ------ |
| `QUERY_ID `                      | uint64 |
| `금액`                             | 코인     |
| `대상`                             | 주소     |
| `응답_대상`                          | 주소     |
| 커스텀_페이로드 \` | 셀      |
| `전송_톤_금액`                        | 코인     |
| `전송_페이로드`                        | 셀      |

'수취인' 제튼 월렛 -> 수취인\`은 메시지 알림 본문에 다음 데이터가 포함되어 있음을 의미합니다:

| 이름                             | 유형     |
| ------------------------------ | ------ |
| 쿼리_ID \`  | uint64 |
| 금액 \`                          | 코인     |
| 보낸 사람 \`                       | 주소     |
| 전진_페이로드\` | 셀      |

'페이티' 제튼 월렛 -> 발신자\`는 초과 메시지 본문에 다음 데이터가 포함되어 있음을 의미합니다:

| 이름         | 유형     |
| ---------- | ------ |
| `query_id` | uint64 |

젯튼 지갑 컨트랙트 필드에 대한 자세한 설명은 [TEP-74](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md)에서 확인할 수 있습니다. 젯튼 표준 인터페이스 설명.

전송 알림`및`초과`매개변수를 사용하는 메시지는 선택 사항이며`전송`메시지에 
첨부된 TON의 양과`전송_톤_양\` 필드 값에 따라 달라집니다.

쿼리 아이디`식별자를 사용하면 애플리케이션에서`전송`, `전송 알림`, `초과\`의 세 가지 메시징 유형을 서로 연결할 수 있습니다.
이 프로세스를 올바르게 수행하려면 항상 고유한 쿼리 ID를 사용하는 것이 좋습니다.

### 댓글 및 알림과 함께 Jetton 전송을 보내는 방법

알림으로 송금하려면(알림 목적으로 지갑 내에서 사용됨),
보내는 메시지에 0이 아닌 `전송 톤 금액`
값을 설정하고 필요한 경우 `전송 페이로드`에 텍스트 댓글을 첨부하여 충분한 양의 TON을 첨부해야 합니다.
텍스트 코멘트는 톤코인 전송 시 텍스트 코멘트와 유사하게 인코딩됩니다.

[제톤 전송 수수료](https://docs.ton.org/develop/smart-contracts/fees#fees-for-sending-jettons)

그러나 수수료는 수신자를 위해 새로운 Jetton 지갑을 배포해야 하는지와 같은 여러 요인에 따라 달라집니다.
따라서 톤코인을 여백을 두고 첨부한 다음 주소를 '응답_대상'
으로 설정하여 `초과` 메시지를 검색하는 것이 좋습니다. 예를 들어, `forward_ton_amount`
값을 0.01톤으로 설정하면서 0.05톤을 메시지에 첨부할 수 있습니다(이 금액의 톤이 `이체 알림` 메시지에 첨부됩니다).

[톤웹 SDK를 사용한 댓글 예제가 포함된 제톤 전송](https://github.com/toncenter/tonweb/blob/b550969d960235314974008d2c04d3d4e5d1f546/src/test-jetton.js#L128):

```js
// first 4 bytes are tag of text comment
const comment = new Uint8Array([... new Uint8Array(4), ... new TextEncoder().encode('text comment')]);

await wallet.methods.transfer({
    secretKey: keyPair.secretKey,
    toAddress: JETTON_WALLET_ADDRESS, // address of Jetton wallet of Jetton sender
    amount: TonWeb.utils.toNano('0.05'), // total amount of TONs attached to the transfer message
    seqno: seqno,
    payload: await jettonWallet.createTransferBody({
        jettonAmount: TonWeb.utils.toNano('500'), // Jetton amount (in basic indivisible units)
        toAddress: new TonWeb.utils.Address(WALLET2_ADDRESS), // recipient user's wallet address (not Jetton wallet)
        forwardAmount: TonWeb.utils.toNano('0.01'), // some amount of TONs to invoke Transfer notification message
        forwardPayload: comment, // text comment for Transfer notification message
        responseAddress: walletAddress // return the TONs after deducting commissions back to the sender's wallet address
    }),
    sendMode: 3,
}).send()
```

:::tip
더 많은 예제는 [TON 쿡북](/develop/dapps/cookbook#how-to-construct-a-message-for-a-jetton-transfer-with-a-comment)을 참조하세요.
:::

## 제튼 오프체인 처리

:::info 거래 확인
TON 트랜잭션은 한 번만 확인하면 되돌릴 수 없습니다. 최상의 사용자 경험을 위해 TON 블록체인에서 트랜잭션이 완료되면 추가 블록을 기다리지 않는 것이 좋습니다. 자세한 내용은 [캐치체인.pdf](https://docs.ton.org/catchain.pdf#page=3)에서 확인하세요.
:::

사용자가 제톤을 수락할 수 있는 시나리오는 여러 가지가 있습니다. 중앙화된 핫월렛 내에서 제톤을 수락할 수도 있고, 개별 사용자마다 별도의 주소가 있는 지갑을 사용해 제톤을 수락할 수도 있습니다.

제톤을 처리하려면 개별화된 TON 처리와 달리 제톤 지갑 또는 둘 이상의 제톤 지갑(
) 외에 핫월렛(v3R2, 고부하 지갑)이 필요합니다. Jetton 핫월렛 배포는 [지갑 배포](/개발/앱/자산 처리/#월렛 배포) 문서에 설명되어 있습니다.
즉, [제톤 지갑 배포](#젯톤-지갑-배포) 기준에 따라 제톤 지갑을 배포할 필요는 없습니다.
그러나 제톤을 받으면 제톤 지갑이 자동으로 배포되므로, 제톤을 출금(
)하면 이미 사용자가 소유하고 있는 것으로 간주합니다.

보안상의 이유로 별도의 제톤을 위한 별도의 핫월렛을 보유하는 것이 좋습니다(자산 유형별로 여러 개의 지갑을 보유하는 것이 좋습니다).

자금을 처리할 때 자동 입출금 프로세스에 참여하지 않는 초과 자금을 보관할 수 있는 콜드월렛을 제공하는 것도 좋습니다.

### 자산 처리 및 초기 검증을 위한 새로운 제톤 추가

1. 올바른 스마트 컨트랙트 토큰 마스터 주소를 찾으려면 다음 소스를 참조하세요: [올바른 젯튼 마스터 컨트랙트를 찾는 방법](#jetton-master-smart-contract)
2. 또한 특정 Jetton의 메타데이터를 검색하려면 다음 소스를 참조하세요: [제톤 메타데이터를 받는 방법](#retrieving-jetton-data)을 참조하세요.
   사용자에게 새 제톤을 올바르게 표시하려면 올바른 '소수점'과 '기호'가 필요합니다.

모든 사용자의 안전을 위해 위조(가짜) 가능성이 있는 제톤을 피하는 것이 중요합니다. 예를 들어, `심볼`==`TON`이 포함된
제톤이나 시스템 알림 메시지가 포함된 제톤은 피해야 합니다:
오류`, `시스템`등. 제톤이 TON 전송, 시스템 알림 등과 섞이지 않도록 
인터페이스에 표시되는지 확인하세요. 때때로`심볼`, `이름`, `이미지\`(
)도 사용자를 오도하기 위해 원본과 거의 동일하게 보이도록 만들기도 합니다.

### 전송 알림 메시지 수신 시 알 수 없는 제톤 식별

1. 지갑에서 알 수 없는 제톤에 대한 이체 알림 메시지가 수신되면 특정 제톤을 보관하기 위해
   지갑이 생성된 것입니다. 다음으로 몇 가지 확인 절차를 수행해야 합니다.
2. 전송 알림` 본문이 포함된 내부 메시지의 발신자 주소는 새 Jetton 지갑의 주소입니다. 
   전송 알림` 본문의 `발신자` 필드와 혼동하지 마세요. Jetton 지갑의 주소
   는 메시지 출처의 주소입니다.
3. 새 Jetton 지갑의 Jetton 마스터 주소 검색하기: [Jetton 지갑의 데이터를 검색하는 방법](#retrieving-jetton-data)을 참조하세요.
   이 프로세스를 수행하려면 `jetton` 매개변수가 필요하며, 이는 Jetton 마스터 컨트랙트를 구성하는 주소입니다.
4. 젯튼 마스터 컨트랙트를 사용하여 지갑 주소(소유자)의 젯튼 지갑 주소 검색하기: [특정 사용자의 젯튼 지갑 주소 검색 방법](#retrieving-jetton-wallet-addresses-for-a-given-user)
5. 마스터 컨트랙트가 반환한 주소와 지갑 토큰의 실제 주소를 비교합니다.
   일치한다면 이상적입니다. 그렇지 않다면 위조된 사기 토큰을 받았을 가능성이 높습니다.
6. 제톤 메타데이터 검색하기: [Jetton 메타데이터를 받는 방법](#retrieving-jetton-data).
7. 심볼`및`이름\` 필드에서 사기의 징후가 있는지 확인합니다. 필요한 경우 사용자에게 경고하세요. [처리 및 초기 확인을 위한 새 제톤 추가하기](#adding-new-jettons-for-asset-processing-and-initial-verification).

### 중앙 지갑을 통해 사용자로부터 제톤 수락하기

:::info
단일 지갑으로 들어오는 거래의 병목 현상을 방지하려면 여러 지갑에서 입금을 수락하고 필요에 따라 지갑의 수를 확장하는 것이 좋습니다.
:::

:::caution 거래 알림
사용자가 제톤을 출금할 때 사용자 지정 메모를 설정할 수 있도록 허용하는 경우 - 메모(텍스트 코멘트)가 첨부될 때마다 forwardAmount를 0.000000001 톤(1나노톤)으로 설정해야 합니다. 그렇지 않으면 표준을 준수하지 않으며 다른 CEX 및 기타 서비스에서 이체를 처리할 수 없게 됩니다.
:::

이 시나리오에서 결제 서비스는 각 발신자에 대해 고유한 메모 식별자를 생성하여
중앙 지갑의 주소와 송금 금액을 공개합니다. 발신자는 댓글에 필수 메모와 함께 지정된 중앙 집중식 주소로
토큰을 보냅니다.

\*\*이 방법의 장점: \*\*이 방법은 토큰을 받을 때 추가 수수료가 없고 핫월렛에서 직접 토큰을 가져오기 때문에 매우 간단합니다.

\*\*이 방법의 단점: \*\*이 방법은 모든 사용자가 송금에 댓글을 첨부해야 하므로 입금 실수(잊어버린 메모, 잘못된 메모 등)가 더 많이 발생할 수 있어 지원 담당자의 업무량이 늘어날 수 있습니다.

톤웹 예시:

1. [댓글(메모)로 개인 HOT 지갑에 제톤 입금 받기](https://github.com/toncenter/examples/blob/main/deposits-jettons.js)
2. [제톤 출금 예시](https://github.com/toncenter/examples/blob/main/withdrawals-jettons.js)

#### 준비 사항

1. 수락된 제톤 목록 준비: [처리 및 초기 검증을 위해 새 제톤 추가하기](#adding-new-jettons-for-자산 처리 및 초기 검증).
2. 핫월렛 배포(Jetton 출금이 예상되지 않는 경우 v3R2 사용, Jetton 출금이 예상되는 경우 하이로드 v2 사용) [지갑 배포](/개발/앱/자산-처리/#월렛-배포).
3. 핫월렛 주소를 사용하여 테스트 제톤 송금을 수행하여 지갑을 초기화합니다.

#### 수신되는 제톤 처리

1. 수락된 제톤 목록 로드
2. 배포된 핫월렛에 대한 Jetton 지갑 주소를 검색합니다: [특정 사용자의 Jetton 지갑 주소를 검색하는 방법](#retrieving-jetton-wallet-addresses-for-a-given-user)
3. 각 Jetton 지갑에 대한 Jetton 마스터 주소를 검색합니다: [Jetton 지갑의 데이터를 검색하는 방법](#retrieving-data-for-a-specific-jetton-wallet)을 참조하세요.
   이 프로세스를 수행하려면 `jetton` 매개변수가 필요합니다(실제로는 Jetton 마스터 컨트랙트의 주소
   ).
4. 1단계와 3단계(바로 위)에서 Jetton 마스터 계약의 주소를 비교합니다.
   주소가 일치하지 않으면 Jetton 주소 확인 오류를 보고해야 합니다.
5. 핫월렛 계정을 사용하여 가장 최근에 처리되지 않은 거래 목록을 검색하고
   각 거래를 하나씩 정렬하여 반복합니다. 참조:  [컨트랙트 트랜잭션 확인](https://docs.ton.org/develop/dapps/asset-processing/#checking-contracts-transactions),
   또는 [톤웹 예시](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-single-wallet.js#L43)
   또는 톤센터 API `/getTransactions` 메서드를 사용하세요.
6. 트랜잭션에 대한 입력 메시지(in_msg)를 확인하고 입력 메시지에서 소스 주소를 검색합니다. [톤웹 예시](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-jettons-single-wallet.js#L84)
7. 소스 주소가 Jetton 지갑 내 주소와 일치하면 트랜잭션 처리를 계속 진행해야 합니다.
   그렇지 않은 경우 트랜잭션 처리를 건너뛰고 다음 트랜잭션을 확인합니다.
8. 메시지 본문이 비어 있지 않은지, 메시지의 첫 32비트가 `전송 알림` 연산 코드 `0x7362d09c`와 일치하는지 확인합니다.
   [톤웹 예시](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-jettons-single-wallet.js#L91)
   메시지 본문이 비어 있거나 연산 코드가 유효하지 않은 경우 - 트랜잭션을 건너뜁니다.
9. 쿼리 아이디`, `금액`, `발신자`, `전송 페이로드\`를 포함한 메시지 본문의 다른 데이터를 읽습니다.
   [젯튼 계약 메시지 레이아웃](#jetton-contract-message-layouts), [톤웹 예시](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-jettons-single-wallet.js#L105)
10. forward_payload`데이터에서 텍스트 코멘트를 검색해 보세요. 처음 32비트는 
    텍스트 주석 연산 코드`0x00000000\`과 나머지 UTF-8 인코딩된 텍스트와 일치해야 합니다.
    [톤웹 예시](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-jettons-single-wallet.js#L110)
11. 전달_페이로드\` 데이터가 비어 있거나 연산 코드가 유효하지 않은 경우 트랜잭션을 건너뜁니다.
12. 받은 댓글과 저장된 메모를 비교합니다. 일치하는 댓글이 있으면(사용자 식별이 항상 가능) 송금을 입금합니다.
13. 5단계부터 다시 시작하여 전체 거래 목록을 살펴볼 때까지 이 과정을 반복합니다.

### 사용자 입금 주소에서 제톤 수락

사용자 입금 주소에서 제톤을 수락하려면 결제 서비스에서 자금을 송금하는 각 참가자에 대해
자체 개별 주소(입금)를 생성해야 합니다. 이 경우 서비스 제공에는
새 입금 생성, 거래 블록 스캔,
입금에서 핫월렛으로 자금 인출 등 여러 병렬 프로세스의 실행이 포함됩니다.

핫월렛은 각 제톤 유형별로 하나의 제톤 지갑을 사용할 수 있으므로 입금을 시작하려면 여러 개의
지갑을 만들어야 합니다. 다수의 지갑을 생성하면서 동시에
하나의 시드 문구(또는 개인키)로 관리하기 위해서는 지갑 생성 시 다른 `subwallet_id`를 지정해야 합니다.
TON에서 하위 지갑 생성에 필요한 기능은 v3 지갑 이상 버전에서 지원됩니다.

#### 톤웹에서 하위 지갑 만들기

```Tonweb
const WalletClass = tonweb.wallet.all['v3R2'];
const wallet = new WalletClass(tonweb.provider, {
    publicKey: keyPair.publicKey,
    wc: 0,
    walletId: <SUBWALLET_ID>,
});
```

#### 준비

1. 수락된 제톤 목록 준비: [처리 및 초기 확인을 위해 새 제톤 추가하기](#adding-new-jettons-for-자산-처리-and-초기-확인)
2. 핫월렛 [지갑 배포](/개발/앱/자산-처리/#월렛-배포)

#### 예금 만들기

1. 사용자를 위한 새 입금 생성 요청을 수락합니다.
2. 핫월렛 시드를 기반으로 새 하위지갑(v3R2) 주소를 생성합니다. [톤웹에서 하위 지갑 만들기](#creating-a-subwallet-in-tonweb)
3. 수신 주소는 제톤 입금에 사용된 주소로 사용자에게 제공할 수 있습니다(입금 제톤 지갑의 소유자인
   주소입니다). 지갑 초기화는 필요하지 않으며, 예치금에서 제톤을 출금할 때
   에서 수행할 수 있습니다.
4. 이 주소의 경우, 젯튼 마스터 컨트랙트를 통해 젯튼 지갑 주소를 계산해야 합니다.
   [특정 사용자의 Jetton 지갑 주소를 검색하는 방법](#retrieving-jetton-wallet-addresses-for-a-given-user)을 참조하세요.
5. 거래 모니터링을 위해 주소 풀에 제톤 지갑 주소를 추가하고 하위 지갑 주소를 저장합니다.

#### 거래 처리

:::info 거래 확인
TON 트랜잭션은 한 번만 확인하면 되돌릴 수 없습니다. 최상의 사용자 경험을 위해 TON 블록체인에서 트랜잭션이 완료되면 추가 블록을 기다리지 않는 것이 좋습니다. 자세한 내용은 [캐치체인.pdf](https://docs.ton.org/catchain.pdf#page=3)에서 확인하세요.
:::

제톤
지갑은 `이체 알림`, `초과`, `내부 이체` 메시지를 보내지 않을 수 있으며 `내부 이체` 메시지는 표준화되어 있지 않기 때문에 메시지에서 받은 제톤의 정확한 양을 항상 확인할 수 있는 것은 아닙니다. 즉,
`내부 전송` 메시지가 해독될 수 있다는 보장이 없습니다.

따라서 지갑에 수령한 금액을 확인하려면 get 메서드를 사용하여 잔액을 요청해야 합니다.
잔액을 요청할 때 주요 데이터를 검색하기 위해 온체인에서 특정 블록의 계정 상태에 따라 블록이 사용됩니다.
[톤웹을 이용한 블록 승인 준비](https://github.com/toncenter/tonweb/blob/master/src/test-block-subscribe.js) 참조.

이 프로세스는 다음과 같이 진행됩니다:

1. 블록 수락 준비(시스템이 새 블록을 수락할 수 있도록 준비).
2. 새 블록을 검색하고 이전 블록 ID를 저장합니다.
3. 블록에서 트랜잭션을 수신합니다.
4. 예치금 Jetton 지갑 풀의 주소로만 사용되는 거래를 필터링합니다.
5. 전송 알림`본문을 사용하여 메시지를 디코딩하면 `발신자`주소, 제톤`금액\`, 댓글 등 더 자세한 데이터를 받을 수 있습니다. (참고: [수신 제톤 처리하기](#processing-incoming-jettons))
6. 디코딩할 수 없는 아웃 메시지(메시지 본문에
   `이체 알림`에 대한 연산 코드와 `초과`에 대한 연산 코드가 포함되지 않음)가 있거나
   계정 내에 아웃 메시지가 없는 거래가 하나 이상 있는 경우, 현재 블록의 get 메서드를 사용하여 제톤 잔액을 요청해야 하며 이전
   블록을 사용하여 잔액의 차이를 계산합니다. 이제 블록 내에서 수행되는 트랜잭션으로 인해 총 잔액 입금액이
   으로 변경됩니다.
7. '전송 알림'이 없는 미확인 제톤 전송의 식별자로 트랜잭션 데이터
   는 해당 트랜잭션 또는 블록 데이터가 하나 있는 경우(한 블록 내에 여러 개가 있는 경우) 사용할 수 있습니다.
8. 이제 입금 잔액이 정확한지 확인해야 합니다. 입금 잔액이 핫월렛과 기존 제톤 지갑 간에 이체를 시작할 수 있을 만큼 충분한 경우, 지갑 잔액이 감소했는지 확인하기 위해 제톤을 출금해야 합니다.
9. 2단계부터 다시 시작하여 전체 과정을 반복합니다.

#### 예금에서 출금

예치금에서 핫월렛(
)으로 이체할 때마다 이체 작업에 대한 수수료(네트워크 가스 수수료로 지불)가 발생하므로 예치금을 보충할 때마다 이체해서는 안 됩니다.이체(따라서 입금)를 가치 있게 만드는 데 필요한 최소한의 제톤을 결정하는 것이 중요합니다.

기본적으로 Jetton 입금 지갑의 지갑 소유자는 초기화되지 않습니다. 이는 보관 수수료를 지불하기 위해 미리 정해진
요구사항이 없기 때문입니다. Jetton 입금 지갑은
`전송` 본문이 포함된 메시지를 전송할 때 배포할 수 있으며, 이후 즉시 삭제할 수 있습니다. 이를 위해 엔지니어는 메시지를 전송할 때 특별한
메커니즘을 사용해야 합니다: 128 + 32.

1. 핫월렛으로 출금하도록 표시된 입금 목록을 검색합니다.
2. 각 입금에 대해 저장된 소유자 주소 검색
3. 그런 다음 TON 제톤 금액이 첨부된 하이로드
   지갑에서 각 소유자 주소로 메시지가 전송됩니다(여러 개의 메시지를 일괄적으로 결합하여). 이는 v3R2 지갑
   초기화에 사용된 수수료 + '전송' 본문이 포함된 메시지 전송 수수료 + '전달_톤_금액'
   (필요한 경우)과 관련된 임의의 TON 금액을 추가하여 결정됩니다. 첨부된 TON 금액은 v3R2 지갑 초기화 수수료(값) +
   'transfer' 본문이 포함된 메시지 전송 수수료(값) + 'forward_ton_amount'(값)에 대한 임의의 TON 금액
   (필요한 경우)을 더하여 결정됩니다.
4. 주소의 잔액이 0이 아닌 상태가 되면 계정 상태가 변경됩니다. 몇 초간 기다렸다가 계정의 상태
   를 확인하면 곧 '존재하지 않음' 상태에서 '사용 안 함'으로 변경됩니다.
5. 각 소유자 주소(`uninit` 상태)에 대해 v3R2 지갑
   init과 본문에는 제톤 지갑에 입금하기 위한 `transfer` 메시지 = 128 + 32가 포함된 외부 메시지를 보내야 합니다. '전송'의 경우
   사용자는 핫월렛의 주소를 '목적지'와 '응답 대상'으로 지정해야 합니다.
   텍스트 코멘트를 추가하면 송금을 더 쉽게 식별할 수 있습니다.
6. 입금 주소를 이용해 핫월렛 주소로 제톤을 전송한 경우,
   에서 [수신 제톤 정보 처리 중](#처리중-수신 제톤)을 참고해 제톤 전송을 확인할 수 있습니다.

### 제톤 인출

제톤을 출금하기 위해 지갑은 해당 제톤 지갑으로 '전송' 본문이 포함된 메시지를 보냅니다.
그러면 제톤 지갑이 수신자에게 제톤을 전송합니다. '송금 알림'을 트리거하려면 `전송_톤_금액`(및 `전송_페이로드`에 대한 선택적 코멘트)으로
을 첨부하는 것이 중요합니다.
참조: [젯톤 계약 메시지 레이아웃](#jetton-contract-message-layouts)

#### 준비

1. 출금할 제톤 목록 준비: [처리 및 초기 확인을 위해 새 제톤 추가하기](#추가-자산 처리 및 초기 확인을 위해-새-제톤-추가하기)
2. 핫월렛 배포가 시작됩니다. 하이로드 v2를 권장합니다. [지갑 배포](/개발/앱/자산 처리/#월렛 배포)
3. 핫월렛 주소를 사용하여 Jetton 송금을 수행하여 Jetton 지갑을 초기화하고 잔액을 보충하세요.

#### 출금 처리

1. 처리된 제톤 목록 로드
2. 배포된 핫월렛에 대한 Jetton 지갑 주소를 검색합니다: [특정 사용자의 Jetton 지갑 주소를 검색하는 방법](#retrieving-jetton-wallet-addresses-for-a-given-user)
3. 각 Jetton 지갑에 대한 Jetton 마스터 주소를 검색합니다: [Jetton 지갑에 대한 데이터 검색 방법](#retrieving-data-for-a-specific-jetton-wallet)을 참조하세요.
   'jetton\` 매개변수(실제로는 Jetton 마스터 컨트랙트의 주소)가 필요합니다.
4. 1단계와 3단계에서 Jetton 마스터 계약의 주소를 비교합니다. 주소가 일치하지 않으면 Jetton 주소 확인 오류를 보고해야 합니다.
5. 출금 요청이 접수되면 실제로 제톤의 유형, 송금할 금액, 수취인 지갑 주소가 표시됩니다.
6. 제톤 지갑의 잔액을 확인하여 인출할 수 있는 충분한 자금이 있는지 확인하세요.
7. 쿼리 아이디, 송금 금액,
   destination(수신자의 Jetton 지갑이 아닌 지갑 주소), response_destination(사용자의 핫월렛을 지정하는 것이 좋습니다),
   forward_ton_amount(`이체 알림`을 호출하려면 최소 0.05 TON으로 설정하는 것이 좋습니다), `forward_payload`
   (댓글 전송이 필요한 경우 옵션)을 포함한 필수 필드를 채워 Jetton `transfer` 본문을 사용하여 메시지를 생성합니다. [젯튼 컨트랙트 메시지 레이아웃](#jetton-contract-message-layouts),
   [톤웹 예시](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/jettons-withdrawals.js#L69)
   거래의 성공적인 검증을 확인하려면 각 메시지마다
   `query_id`에 고유 값을 할당해야 합니다.
8. 부하가 많은 지갑을 사용할 때는 수수료를 최적화하기 위해 메시지를 일괄적으로 수집하고 한 번에 한 개씩 전송하는 것이 좋습니다.
9. 발신 외부 메시지의 만료 시간 저장(지갑이
   메시지를 성공적으로 처리할 때까지의 시간이며, 이 시간이 지나면 지갑은 더 이상 메시지를 수락하지 않습니다.)
10. 단일 메시지 또는 두 개 이상의 메시지(일괄 메시지)를 보냅니다.
11. 핫월렛 계정 내에서 처리되지 않은 최신 트랜잭션 목록을 검색하고 반복합니다.
    여기에서 자세히 알아보세요: [컨트랙트 트랜잭션 확인](/개발/앱/자산-처리/#체킹-컨트랙트-트랜잭션),
    [톤웹 예시](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-single-wallet.js#L43) 또는
    톤센터 API `/getTransactions` 메서드를 사용하세요.
12. 계정에서 발신 메시지를 확인합니다.
13. 전송`연산 코드가 포함된 메시지가 있는 경우 이를 디코딩하여`query_id`값을 검색해야 합니다.
    검색된`query_id\`는 성공적으로 전송된 것으로 표시해야 합니다.
14. 현재 스캔한 트랜잭션이 처리되는 데 걸리는 시간이 만료 시간
    보다 길고 지정된 `query_id`
    가 포함된 발신 메시지를 찾을 수 없는 경우, 요청을 만료된 것으로 표시하고 안전하게 다시 보내야 합니다(이는 선택 사항입니다).
15. 계정에서 수신 메시지를 찾습니다.
16. excesses`연산 코드를 사용하는 메시지가 있으면 메시지를 디코딩하고`query_id`값을 검색해야 합니다. 검색된`query_id\`는 성공적으로 전달된 것으로 표시해야 합니다.
17. 5단계로 이동합니다. 성공적으로 전송되지 않은 만료된 요청은 출금 목록으로 다시 푸시되어야 합니다.

## 제톤 온체인 처리

:::info 거래 확인
TON 트랜잭션은 한 번만 확인하면 되돌릴 수 없습니다. 최상의 사용자 경험을 위해 TON 블록체인에서 트랜잭션이 완료되면 추가 블록을 기다리지 않는 것이 좋습니다. 자세한 내용은 [캐치체인.pdf](https://docs.ton.org/catchain.pdf#page=3)에서 확인하세요.
:::

일반적으로 내부 메시지를 담당하는 메시지 핸들러는 제톤을 수락하고 처리하기 위해 `op=0x7362d09c` 연산 코드를 사용합니다.

다음은 온체인 제톤 처리를 수행할 때 고려해야 할 권장 사항 목록입니다:

1. 수신되는 제톤을 제톤 마스터 컨트랙트가 아닌 지갑 유형으로 식별합니다. 즉, 컨트랙트는 특정 젯튼 마스터 컨트랙트를 사용하는 알 수 없는 지갑이 아닌 특정 젯튼 지갑과 상호작용(메시지 수신 및 전송)해야 합니다.
2. 젯튼 월렛과 젯튼 마스터를 연결할 때, 이 연결이 양방향인지, 월렛이 마스터 컨트랙트를 인식하고 그 반대의 경우도 마찬가지인지 확인하세요. 예를 들어, 여러분의 컨트랙트 시스템이 (마이슈퍼젯튼을 마스터 컨트랙트로 간주하는) 젯튼 월렛으로부터 알림을 받으면 사용자에게 전송 정보를 표시해야 하는 경우, 마이슈퍼젯튼 컨트랙트의 `심볼`, `이름` 및 `이미지`
   를 표시하기 전에 마이슈퍼젯튼 월렛이 올바른 컨트랙트 시스템을 사용하는지 확인하시기 바랍니다. 또한, 어떤 이유로 인해 컨트랙트 시스템이 MySuperJetton 또는 MySuperJetton 마스터 컨트랙트를 사용하여 제톤을 전송해야 하는 경우 지갑 X가 동일한 컨트랙트 파라미터를 사용하는 지갑인지 확인합니다.
   또한, X로 '전송' 요청을 보내기 전에, X가 MySuperJetton을 마스터로 인식하는지 확인하세요.
3. 탈중앙화 금융(DeFi)의 진정한 힘은 프로토콜을 레고 블록처럼 쌓아올리는 능력에 기반합니다. 예를 들어, 제튼 A를 제튼 B로 스왑한 다음, 사용자가 유동성을 공급하면 대출 프로토콜 내에서 레버리지로 사용되어 NFT(....)를 구매하는 데 사용된다고 가정해 보겠습니다. 따라서 토큰화된 가치를 전송 알림에 첨부하고 전송 알림과 함께 전송할 수 있는 사용자 지정 페이로드를 추가하여 오프체인 사용자뿐만 아니라 온체인 주체에게도 컨트랙트를 제공할 수 있는 방법을 고려하세요.
4. 모든 계약이 동일한 기준을 따르는 것은 아니라는 점에 유의하세요. 안타깝게도 일부 제톤은 공격 기반 벡터를 사용해 의심하지 않는 사용자를 공격할 목적으로만 생성된 적대적인 제톤일 수 있습니다. 보안을 위해 해당 프로토콜이 많은 컨트랙트로 구성된 경우, 동일한 유형의 제톤 지갑을 많이 생성하지 마세요. 특히 프로토콜 내에서 예금 컨트랙트, 볼트 컨트랙트, 사용자 계정 컨트랙트 등 사이에 제톤을 보내지 마세요. 공격자는 전송 알림, 제톤 금액 또는 페이로드 매개변수를 위조하여 의도적으로 컨트랙트 로직을 방해할 수 있습니다. 시스템에서 제톤당 하나의 지갑만 사용함으로써 공격 가능성을 줄입니다(모든 입출금에 대해).
5. 또한 주소 스푸핑의 가능성을 줄이기 위해 개별화된 각 젯톤에 대해 하위 계약을 생성하는 것도 좋은 방법입니다(예: 젯톤 A를 위한 계약을 사용하여 젯톤 B에게 전송 메시지를 보내는 경우).
6. 컨트랙트 레벨에서는 분할 불가능한 제튼 단위로 작업할 것을 강력히 권장합니다. 소수점 관련 로직은 일반적으로 디플레이의 사용자 인터페이스(UI)를 개선하는 데 사용되며, 숫자 온체인 기록 보관과는 관련이 없습니다.
7. CertiK의 [FunC에서 안전한 스마트 컨트랙트 프로그래밍](https://blog.ton.org/secure-smart-contract-programming-in-func)에 대해 자세히 알아보려면 이 리소스를 읽어보세요. 개발자는 애플리케이션 개발 중에 스마트 컨트랙트 예외가 생략되지 않도록 모든 스마트 컨트랙트 예외를 처리하는 것이 좋습니다.

## 제톤 지갑 처리

일반적으로 오프체인 제톤 처리에 사용되는 모든 검증 절차는 지갑에도 적합합니다. 젯튼 지갑 처리의 경우 가장 중요한 권장 사항은 다음과 같습니다:

1. 지갑이 알 수 없는 제톤 지갑으로부터 이체 알림을 받으면 악의적인 위조일 수 있으므로 제톤 지갑과 마스터 주소를 신뢰하는 것이 매우 중요합니다. 자신을 보호하려면 제공된 주소를 사용하여 젯톤 마스터(마스터 계약)를 확인하여 인증 프로세스에서 젯톤 지갑을 합법적인 것으로 인식하는지 확인하세요. 지갑을 신뢰하고 합법적인 것으로 확인되면 지갑이 계정 잔액과 기타 지갑 내 데이터에 액세스할 수 있도록 허용할 수 있습니다. 젯톤 마스터가 이 지갑을 인식하지 못하면 젯톤 이체를 전혀 시작하거나 공개하지 말고 수신되는 TON 이체(이체 알림에 첨부된 톤코인)만 표시하는 것이 좋습니다.
2. 실제로 사용자가 제톤 지갑이 아닌 제톤과 상호 작용하고자 하는 경우. 즉, 사용자는 `EQAjN...`/`EQBLE...`
   등이 아닌 wTON/oUSDT/jUSDT, jUSDC, jDAI를 전송합니다. 이는 종종 사용자가 제톤 전송을 시작할 때 지갑이 해당 제톤 마스터에게 어떤 제톤 지갑(사용자 소유)이 전송 요청을 시작해야 하는지 묻는 것을 의미합니다. 마스터(마스터 컨트랙트)의 이 데이터를 맹목적으로 신뢰하지 않는 것이 중요합니다. 젯튼 지갑으로 전송 요청을 보내기 전에 항상 젯튼 지갑이 실제로 해당 젯튼 마스터에 속해 있는지 확인하세요.
3. 적대적인 제톤 마스터/제톤 지갑은 시간이 지남에 따라 지갑/마스터를 변경할 수 있다는 점에 유의하세요. 따라서 사용자는 매번 사용하기 전에 거래하는 모든 지갑의 적법성을 꼼꼼히 확인하고 확인해야 합니다.
4. 항상 TON 전송, 시스템 알림 등과 섞이지 않는 방식으로 인터페이스에 제톤을 표시해야 합니다. 심볼`, `이름`, `이미지\`
   매개변수조차도 사용자를 오도하도록 조작할 수 있으며, 이로 인해 영향을 받는 사용자는 잠재적인 사기 피해자로 남을 수 있습니다. 악성 제톤이 TON 전송, 알림 오류, 보상 획득 또는 자산 동결 공지를 사칭하는 데 사용된 사례가 여러 차례 있었습니다.
5. 위조 제톤을 생성하는 잠재적인 악의적 행위자를 항상 경계해야 하며, 기본 사용자 인터페이스에서 원치 않는 제톤을 제거하는 데 필요한 기능을 사용자에게 제공하는 것이 좋습니다.

kosrk](https://github.com/kosrk), [krigga](https://github.com/krigga), [EmelyanenkoK](https://github.com/EmelyanenkoK/), [tolya-yanot](https://github.com/tolya-yanot/)가 작성했습니다.

## 모범 사례

여기에서는 TON 커뮤니티 회원이 만든 제튼 코드 처리의 몇 가지 예를 제공합니다:

<Tabs groupId="code-examples">
<TabItem value="tonweb" label="JS (tonweb)">

```js
const transfer = await wallet.methods.transfer({
  secretKey: keyPair.secretKey,
  toAddress: jettonWalletAddress,
  amount: 0,
  seqno: seqno,
  sendMode: 128 + 32, // mode 128 is used for messages that are to carry all the remaining balance; mode 32 means that the current account must be destroyed if its resulting balance is zero;
  payload: await jettonWallet.createTransferBody({
    queryId: seqno, // any number
    jettonAmount: jettonBalance, // jetton amount in units
    toAddress: new TonWeb.utils.Address(MY_HOT_WALLET_ADDRESS),
    responseAddress: new TonWeb.utils.Address(MY_HOT_WALLET_ADDRESS),
  }),
});
await transfer.send();
```

</TabItem>
<TabItem value="tonutils-go" label="Golang">

```go
client := liteclient.NewConnectionPool()

// connect to testnet lite server
err := client.AddConnectionsFromConfigUrl(context.Background(), "https://ton.org/global.config.json")
if err != nil {
   panic(err)
}

ctx := client.StickyContext(context.Background())

// initialize ton api lite connection wrapper
api := ton.NewAPIClient(client)

// seed words of account, you can generate them with any wallet or using wallet.NewSeed() method
words := strings.Split("birth pattern then forest walnut then phrase walnut fan pumpkin pattern then cluster blossom verify then forest velvet pond fiction pattern collect then then", " ")

w, err := wallet.FromSeed(api, words, wallet.V3R2)
if err != nil {
   log.Fatalln("FromSeed err:", err.Error())
   return
}

token := jetton.NewJettonMasterClient(api, address.MustParseAddr("EQD0vdSA_NedR9uvbgN9EikRX-suesDxGeFg69XQMavfLqIw"))

// find our jetton wallet
tokenWallet, err := token.GetJettonWallet(ctx, w.WalletAddress())
if err != nil {
   log.Fatal(err)
}

amountTokens := tlb.MustFromDecimal("0.1", 9)

comment, err := wallet.CreateCommentCell("Hello from tonutils-go!")
if err != nil {
   log.Fatal(err)
}

// address of receiver's wallet (not token wallet, just usual)
to := address.MustParseAddr("EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N")
transferPayload, err := tokenWallet.BuildTransferPayload(to, amountTokens, tlb.ZeroCoins, comment)
if err != nil {
   log.Fatal(err)
}

// your TON balance must be > 0.05 to send
msg := wallet.SimpleMessage(tokenWallet.Address(), tlb.MustFromTON("0.05"), transferPayload)

log.Println("sending transaction...")
tx, _, err := w.SendWaitTransaction(ctx, msg)
if err != nil {
   panic(err)
}
log.Println("transaction confirmed, hash:", base64.StdEncoding.EncodeToString(tx.Hash))
```

</TabItem>
<TabItem value="TonTools" label="Python">

```py
my_wallet = Wallet(provider=client, mnemonics=my_wallet_mnemonics, version='v4r2')

# for TonCenterClient and LsClient
await my_wallet.transfer_jetton(destination_address='address', jetton_master_address=jetton.address, jettons_amount=1000, fee=0.15) 

# for all clients
await my_wallet.transfer_jetton_by_jetton_wallet(destination_address='address', jetton_wallet='your jetton wallet address', jettons_amount=1000, fee=0.1)  
```

</TabItem>
</Tabs>

### 댓글 파싱을 통한 제톤 전송

```ts
import {
    Address,
    TonClient,
    Cell,
    beginCell,
    storeMessage,
    JettonMaster,
    OpenedContract,
    JettonWallet,
    Transaction
} from '@ton/ton';


export async function retry<T>(fn: () => Promise<T>, options: { retries: number, delay: number }): Promise<T> {
    let lastError: Error | undefined;
    for (let i = 0; i < options.retries; i++) {
        try {
            return await fn();
        } catch (e) {
            if (e instanceof Error) {
                lastError = e;
            }
            await new Promise(resolve => setTimeout(resolve, options.delay));
        }
    }
    throw lastError;
}

export async function tryProcessJetton(orderId: string) : Promise<string> {

    const client = new TonClient({
        endpoint: 'https://toncenter.com/api/v2/jsonRPC',
        apiKey: 'TONCENTER-API-KEY', // https://t.me/tonapibot
    });

    interface JettonInfo {
        address: string;
        decimals: number;
    }

    interface Jettons {
        jettonMinter : OpenedContract<JettonMaster>,
        jettonWalletAddress: Address,
        jettonWallet: OpenedContract<JettonWallet>
    }

    const MY_WALLET_ADDRESS = 'INSERT-YOUR-HOT-WALLET-ADDRESS'; // your HOT wallet

    const JETTONS_INFO : Record<string, JettonInfo> = {
        'jUSDC': {
            address: 'EQB-MPwrd1G6WKNkLz_VnV6WqBDd142KMQv-g1O-8QUA3728', //
            decimals: 6
        },
        'jUSDT': {
            address: 'EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA',
            decimals: 6
        },
    }
    const jettons: Record<string, Jettons> = {};

    const prepare = async () => {
        for (const name in JETTONS_INFO) {
            const info = JETTONS_INFO[name];
            const jettonMaster = client.open(JettonMaster.create(Address.parse(info.address)));
            const userAddress = Address.parse(MY_WALLET_ADDRESS);

            const jettonUserAddress =  await jettonMaster.getWalletAddress(userAddress);
          
            console.log('My jetton wallet for ' + name + ' is ' + jettonUserAddress.toString());

            const jettonWallet = client.open(JettonWallet.create(jettonUserAddress));

            //const jettonData = await jettonWallet;
            const jettonData = await client.runMethod(jettonUserAddress, "get_wallet_data")

            jettonData.stack.pop(); //skip balance
            jettonData.stack.pop(); //skip owneer address
            const adminAddress = jettonData.stack.readAddress();


            if (adminAddress.toString() !== (Address.parse(info.address)).toString()) {
                throw new Error('jetton minter address from jetton wallet doesnt match config');
            }

            jettons[name] = {
                jettonMinter: jettonMaster,
                jettonWalletAddress: jettonUserAddress,
                jettonWallet: jettonWallet
            };
        }
    }

    const jettonWalletAddressToJettonName = (jettonWalletAddress : Address) => {
        const jettonWalletAddressString = jettonWalletAddress.toString();
        for (const name in jettons) {
            const jetton = jettons[name];

            if (jetton.jettonWallet.address.toString() === jettonWalletAddressString) {
                return name;
            }
        }
        return null;
    }

    // Subscribe

    const Subscription = async ():Promise<Transaction[]> =>{

      const client = new TonClient({
        endpoint: 'https://toncenter.com/api/v2/jsonRPC',
        apiKey: 'TONCENTER-API-KEY', // https://t.me/tonapibot
      });

        const myAddress = Address.parse('INSERT-YOUR-HOT-WALLET'); // Address of receiver TON wallet
        const transactions = await client.getTransactions(myAddress, {
            limit: 5,
        });
        return transactions;
    }




    return retry(async () => {

        await prepare();
       const Transactions = await Subscription();

        for (const tx of Transactions) {

            const sourceAddress = tx.inMessage?.info.src;
            if (!sourceAddress) {
                // external message - not related to jettons
                continue;
            }

            if (!(sourceAddress instanceof Address)) {
                continue;
            }

            const in_msg = tx.inMessage;

            if (in_msg?.info.type !== 'internal') {
                // external message - not related to jettons
                continue;
            }

            // jetton master contract address check
            const jettonName = jettonWalletAddressToJettonName(sourceAddress);
            if (!jettonName) {
                // unknown or fake jetton transfer
                continue;
            }

            if (tx.inMessage === undefined || tx.inMessage?.body.hash().equals(new Cell().hash())) {
                // no in_msg or in_msg body
                continue;
            }

            const msgBody = tx.inMessage;
            const sender = tx.inMessage?.info.src;
            const originalBody = tx.inMessage?.body.beginParse();
            let body = originalBody?.clone();
            const op = body?.loadUint(32);
            if (!(op == 0x7362d09c)) {
                continue; // op == transfer_notification
            }

            console.log('op code check passed', tx.hash().toString('hex'));

            const queryId = body?.loadUint(64);
            const amount = body?.loadCoins();
            const from = body?.loadAddress();
            const maybeRef = body?.loadBit();
            const payload = maybeRef ? body?.loadRef().beginParse() : body;
            const payloadOp = payload?.loadUint(32);
            if (!(payloadOp == 0)) {
                console.log('no text comment in transfer_notification');
                continue;
            }

            const comment = payload?.loadStringTail();
            if (!(comment == orderId)) {
                continue;
            }
            
            console.log('Got ' + jettonName + ' jetton deposit ' + amount?.toString() + ' units with text comment "' + comment + '"');
            const txHash = tx.hash().toString('hex');
            return (txHash);
        }
        throw new Error('Transaction not found');
    }, {retries: 30, delay: 1000});
}

```

## 참고 항목

- [결제 처리](/개발/앱/자산 처리/)
- [TON에서 NFT 처리](/개발/앱/자산 처리/nfts)
- [TON에서 메타데이터 파싱](/개발/앱/자산 처리/메타데이터)
