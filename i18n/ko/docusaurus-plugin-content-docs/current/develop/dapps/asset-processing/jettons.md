import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import Button from '@site/src/components/button';

# TON Jetton 처리

:::info
독자가 이 문서를 명확하게 이해하기 위해서는 [자산 처리 섹션](/develop/dapps/asset-processing/)에 설명된 자산 처리의 기본 원칙을 숙지하고 있어야 합니다.
:::

Jetton은 TON 블록체인에서 사용되는 토큰으로, 이더리움의 ERC-20 토큰과 유사하게 생각할 수 있습니다.

이 분석에서는 Jetton의 [동작](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md) 및 [메타데이터](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md)에 대한 공식 표준을 자세히 살펴봅니다.
샤딩 중심의 비공식적인 Jetton 아키텍처 개요는 [Jetton 해부 블로그 게시물](https://blog.ton.org/how-to-shard-your-ton-smart-contract-and-why-studying-the-anatomy-of-tons-jettons)에서 확인할 수 있습니다.

또한, Jetton 인출을 처리하는 두 가지 접근 방식이 있다는 점을 염두에 두어야 합니다:

- [메모 입금](https://github.com/toncenter/examples/blob/main/deposits-jettons.js) - 하나의 입금 지갑을 유지하고, 사용자가 메모를 추가하여 시스템에서 식별될 수 있습니다. 이를 통해 블록체인 전체를 스캔할 필요는 없지만, 사용자에게는 다소 불편할 수 있습니다.
- [메모 없는 입금](https://github.com/gobicycle/bicycle) - 이 솔루션도 존재하지만 통합이 더 어렵습니다. 그러나 이 경로를 선택하고자 한다면 저희가 도움을 드릴 수 있습니다. 이 방법을 구현하기로 결정하기 전에 저희에게 알려주시기 바랍니다.

## Jetton 아키텍처

TON의 표준화된 토큰은 다음 스마트 계약 세트를 사용하여 구현됩니다:

- [Jetton 마스터](https://github.com/ton-blockchain/token-contract/blob/main/ft/jetton-minter.fc) 스마트 컨트랙트
- [Jetton 지갑](https://github.com/ton-blockchain/token-contract/blob/main/ft/jetton-wallet.fc) 스마트 컨트랙트

<p align="center">
  <br />
    <img width="420" src="/img/docs/asset-processing/jetton_contracts.svg" alt="contracts scheme" />
      <br /></p>

## Jetton 마스터 스마트 계약

Jetton 마스터 스마트 계약은 Jetton에 대한 일반 정보를 저장합니다 (총 공급량, 메타데이터 링크 또는 메타데이터 자체 포함).

:::warning Jetton 사기에 주의

어떤 사용자가 가치 있는 Jetton의 **복제본**을 임의의 이름, 티커, 이미지 등을 사용하여 **원본과 거의 동일하게** 만들 수 있습니다. 다행히도, 복제된 Jetton은 **주소로 구별**할 수 있으며 쉽게 식별할 수 있습니다.
`TON`이라는 `심볼`을 가진 Jetton 또는 `ERROR`, `SYSTEM` 등 시스템 알림 메시지를 포함하는 Jetton에 주의하십시오. Jetton이 TON 전송, 시스템 알림 등과 혼동되지 않도록 인터페이스에 표시되도록 하십시오. 때로는 `심볼`, `이름`, `이미지`조차도 사용자를 혼동시키기 위해 원본과 거의 동일하게 만들어질 수 있습니다.

TON 사용자의 사기 가능성을 없애기 위해 특정 Jetton 유형에 대한 **원본 Jetton 주소**(Jetton 마스터 계약)를 조회하거나 **프로젝트의 공식 소셜 미디어** 채널 또는 웹사이트를 통해 **정확한 정보**를 확인하십시오. [Tonkeeper ton-assets 리스트](https://github.com/tonkeeper/ton-assets)로 자산을 확인하여 사기 가능성을 제거하십시오.
:::

### Jetton 데이터 조회

구체적인 Jetton 데이터를 조회하려면 계약의 *get* 메서드인 `get_jetton_data()`를 사용하십시오.

이 메서드는 다음 데이터를 반환합니다:

| 이름                   | 유형      | 설명                                                                                                                                                                                                                |
| -------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `total_supply`       | `int`   | 발행된 Jetton의 총 수량을 불가분 단위로 측정한 값.                                                                                                                                                                  |
| `mintable`           | `int`   | 새로운 Jetton을 발행할 수 있는지 여부를 나타냅니다. 이 값은 -1 (발행 가능) 또는 0 (발행 불가)입니다.                                                                           |
| `admin_address`      | `slice` |                                                                                                                                                                                                                   |
| `jetton_content`     | `cell`  | [TEP-64](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md)에 따라 데이터가 포함되어 있으며, 자세한 내용은 [Jetton 메타데이터 분석 페이지](/develop/dapps/asset-processing/metadata)를 참조하십시오. |
| `jetton_wallet_code` | `cell`  |                                                                                                                                                                                                                   |

이를 [Toncenter API](https://toncenter.com/api/v3/#/default/get_jetton_masters_api_v3_jetton_masters_get) 또는 [SDK](https://docs.ton.org/develop/dapps/apis/sdk) 중 하나를 통해 호출할 수 있습니다.

<Tabs groupId="get-jetton_data">
<TabItem value="API" label="API">

> [Toncenter API](https://toncenter.com/api/v3/#/default/get_jetton_masters_api_v3_jetton_masters_get)에서 `jetton/masters` 메서드를 실행하십시오.

</TabItem>
<TabItem value="js" label="js">

```js
import TonWeb from "tonweb";
const tonweb = new TonWeb();
const jettonMinter = new TonWeb.token.jetton.JettonMinter(tonweb.provider, {address: "<JETTON_MASTER_ADDRESS>"});
const data = await jettonMinter.getJettonData();
console.log('Total supply:', data.totalSupply.toString());
console.log('URI to off-chain metadata:', data.jettonContentUri);
```

</TabItem>
</Tabs>

### Jetton 민터

앞서 언급했듯이, Jetton은 `발행 가능` 또는 `발행 불가`일 수 있습니다.

발행 불가인 경우, 추가 토큰을 발행할 수 없습니다. 첫 Jetton을 발행하려면 [첫 Jetton 발행](/develop/dapps/tutorials/jetton-minter) 페이지를 참조하십시오.

발행 가능인 경우, 추가 Jetton을 발행할 수 있는 [민터 컨트랙트](https://github.com/ton-blockchain/minter-contract/blob/main/contracts/jetton-minter.fc)에 특별한 함수가 있습니다. 이 함수는 관리 주소에서 지정된 opcode로 `내부 메시지`를 보내 호출할 수 있습니다.

Jetton 관리자가 Jetton 생성 제한을 원할 경우, 세 가지 방법이 있습니다:

1. 컨트랙트 코드를 업데이트할 수 없거나 원하지 않는 경우, 관리자가 현재 관리 주소를 영 주소로 전송해야 합니다. 이렇게 하면 유효한 관리자가 없게 되어 누구도 Jetton을 발행할 수 없습니다. 그러나 Jetton 메타데이터 변경도 불가능해집니다.
2. 소스 코드에 접근하여 변경할 수 있는 경우, 호출 후 모든 발행 프로세스를 중단하는 플래그를 설정하는 메서드를 계약에 생성하고, 발행 함수에서 이 플래그를 확인하는 문을 추가할 수 있습니다.
3. 컨트랙트 코드를 업데이트할 수 있는 경우, 이미 배포된 컨트랙트의 코드를 업데이트하여 제한을 추가할 수 있습니다.

## Jetton 지갑 스마트 컨트랙트

`Jetton 지갑` 컨트랙트는 **전송**, **수신** 및 **소각**에 사용됩니다. 각 *Jetton 지갑 컨트랙트* 는 특정 사용자의 지갑 잔액 정보를 저장합니다.
특정 경우, Jetton 지갑은 각 Jetton 유형의 개별 Jetton 보유자에게 사용됩니다.

`Jetton 지갑`은 TON코인 자산만을 저장하고 블록체인과 상호작용하기 위한 지갑 (예: v3R2 지갑, 하이로드 지갑 등)과 **혼동해서는 안됩니다**.
이들은 **특정 Jetton 유형**만을 지원하고 관리하는 역할을 합니다.

### Jetton Wallet 배포

지갑 간에 `jetton 전송`을 할 때, 트랜잭션(메시지)은 네트워크 **가스 요금** 및 Jetton 지갑 컨트랙트 코드에 따른 작업 실행을 위해 일정량의 TON을 필요로 합니다. 이는 **수신자가 jetton을 받기 전에 jetton 지갑을 배포할 필요가 없다는 것**을 의미합니다. 송신자가 필요한 가스 요금을 지불할 만큼 충분한 TON을 지갑에 보유하고 있는 한, 수신자의 jetton 지갑은 자동으로 배포됩니다.

### 특정 사용자의 Jetton 지갑 주소 조회

`소유자 주소`(TON 지갑 주소)를 사용하여 `jetton 지갑` `주소`를 조회하려면, `Jetton 마스터 계약`의 `get_wallet_address(slice owner_address)` 메서드를 사용합니다.

<Tabs groupId="retrieve-wallet-address">
<TabItem value="api" label="API">

> `get_wallet_address(slice owner_address)` 메서드를 [Toncenter API](https://toncenter.com/api/v3/#/default/run_get_method_api_v3_runGetMethod_post)의 `/runGetMethod` 메서드를 통해 실행하세요. 실제 상황에서는 (테스트가 아닌 경우) 지갑이 원하는 Jetton 마스터에 실제로 연결되어 있는지 항상 확인하는 것이 중요합니다. 더 많은 코드 예시를 확인하세요.

</TabItem>
<TabItem value="js" label="js">

```js
import TonWeb from 'tonweb';
const tonweb = new TonWeb();
const jettonMinter = new TonWeb.token.jetton.JettonMinter(tonweb.provider, { address: '<JETTON_MASTER_ADDRESS>' });
const jettonWalletAddress = await jettonMinter.getJettonWalletAddress(new TonWeb.utils.Address('<OWNER_WALLET_ADDRESS>'));

// It is important to always check that wallet indeed is attributed to desired Jetton Master:
const jettonWallet = new TonWeb.token.jetton.JettonWallet(tonweb.provider, {
  address: jettonWalletAddress
});
const jettonData = await jettonWallet.getData();
if (jettonData.jettonMinterAddress.toString(false) !== jettonMinter.address.toString(false)) {
  throw new Error('jetton minter address from jetton wallet doesnt match config');
}

console.log('Jetton wallet address:', jettonWalletAddress.toString(true, true, true));
```

</TabItem>
</Tabs>

### 특정 Jetton 지갑의 데이터 조회

지갑의 계좌 잔액, 소유자 식별 정보 및 특정 jetton 지갑 계약과 관련된 기타 정보를 조회하려면 jetton 지갑 계약 내의 `get_wallet_data()` get 메서드를 사용하십시오.

이 메서드는 다음 데이터를 반환합니다:

| 이름                   | 유형        |
| -------------------- | --------- |
| `balance`            | int       |
| `owner`              | 슬라이스slice |
| `jetton`             | slice     |
| `jetton_wallet_code` | cell      |

<Tabs groupId="retrieve-jetton-wallet-data">
<TabItem value="api" label="API">

> [Toncenter API](https://toncenter.com/api/v3/#/default/get_jetton_wallets_api_v3_jetton_wallets_get)의 `/jetton/wallets` get 메서드를 사용하여 이전에 디코딩된 jetton 지갑 데이터를 조회하십시오.

</TabItem>

<TabItem value="js" label="js">

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

</TabItem>
</Tabs>

## Jetton 지갑 간의 통신 개요

Jetton 지갑과 TON 지갑 간의 통신은 다음 통신 순서를 통해 이루어집니다:

![](/img/docs/asset-processing/jetton_transfer.svg)

#### 메시지 0

`발신자 -> 발신자의 jetton 지갑`. *전송* 메시지에는 다음 데이터가 포함됩니다:

| 이름                     | 유형         | 설명                                                                                                                                             |
| ---------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `query_id`             | uint64     | 애플리케이션이 `전송`, `전송 알림`, `과잉` 메시지 유형을 서로 연결할 수 있게 합니다. 이 프로세스가 올바르게 수행되도록 하려면 **항상 고유한 query id를 사용하는 것이 좋습니다**. |
| `amount`               | coins      | 메시지와 함께 전송될 총 `ton 코인` 금액.                                                                                                     |
| `destination`          | address    | Jetton의 새로운 소유자의 주소.                                                                                                           |
| `response_destination` | address    | 과잉 메시지로 남은 ton 코인을 반환할 지갑 주소.                                                                                                  |
| `custom_payload`       | maybe cell | 항상 크기가 >= 1 비트. (보낸 사람 또는 받는 사람의 jetton 지갑의 내부 논리에서 사용되는) 사용자 정의 데이터.                       |
| `forward_ton_amount`   | coins      | 0이어야 합니다. 이는 **`amount` 값의 일부**이며 **`amount`보다 작아야 합니다**.                                                      |
| `forward_payload`      | maybe cell | 항상 크기가 >= 1 비트. 처음 32비트가 0x0이면 단순한 메시지입니다.                                                                     |

#### 메시지 2'

`수취인의 jetton 지갑 -> 수취인`. 전송 알림 메시지. **단,** `forward_ton_amount`가 0이 아닌 경우에만 전송됩니다. 다음 데이터를 포함합니다:

| 이름                | 유형      |
| ----------------- | ------- |
| `query_id`        | uint64  |
| `amount`          | coins   |
| `sender`          | address |
| `forward_payload` | cell    |

여기서 `sender` 주소는 Alice의 `Jetton 지갑`의 주소입니다.

#### 메시지 2''

`수취인의 jetton 지갑 -> 발신자`. 과잉 메시지 본문. **요금을 지불한 후 남은 ton 코인이 있는 경우에만 전송됩니다.** 다음 데이터를 포함합니다:

| 이름         | 유형     |
| ---------- | ------ |
| `query_id` | uint64 |

:::tip Jettons 표준
Jetton 지갑 계약 필드에 대한 자세한 설명은 [TEP-74](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md) `Jetton 표준` 인터페이스 설명에서 찾을 수 있습니다.
:::

## 주석을 포함한 Jetton 전송

Jetton을 전송할 때는 **수수료**와 선택적으로 **전송 알림 메시지**(forward amount 필드를 확인하세요)를 위해 TON 코인이 필요합니다.

주석을 포함하려면 `forward payload`를 설정해야 합니다. 첫 32비트를 `0x0`으로 설정하고 텍스트를 추가합니다.

`forward payload`는 `전송 알림` 내부 메시지로 전송됩니다. 이는 `forward amount`가 0보다 큰 경우에만 생성됩니다.

`Excess` 메시지를 수신하려면 `response destination`을 설정해야 합니다.

Jetton을 전송할 때 `709` 오류를 만날 수 있습니다. 이 오류는 메시지에 첨부된 Toncoin의 값이 전송하기에 충분하지 않다는 의미입니다. `Toncoin > to_nano(TRANSFER_CONSUMPTION) + forward_ton_amount`를 확인해야 합니다. 대부분의 경우 `TRANSFER_CONSUMPTION`은 `forward_payload`가 너무 크지 않다면 0.037일 수 있습니다. 또한 `forward_ton_amount`를 충분히 첨부하는 것을 잊지 마세요. 첨부된 값이 너무 적으면 `cskip_no_gas` 오류가 발생할 수 있습니다.

:::tip
"주석과 함께 Jetton 전송" 예제를 보려면 [best practices](/develop/dapps/asset-processing/jettons#best-practices)를 확인하세요.
:::

## Jetton 오프체인 처리

:::info 거래 확인
TON 거래는 한 번 확인되면 되돌릴 수 없습니다. 최고의 사용자 경험을 위해, TON 블록체인에서 거래가 완료되면 추가 블록을 기다리지 않는 것이 좋습니다. 자세한 내용은 [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3)에서 확인하세요.
:::

Jetton을 수락하는 두 가지 방법이 있습니다:

- **중앙화된 핫 월렛** 내에서.
- 각 사용자를 위한 **개별 주소**를 사용하여.

보안상의 이유로, 별도의 Jetton에 대해 별도의 핫 월렛을 보유하는 것이 좋습니다(각 자산 유형에 대해 여러 월렛을 보유).

자금을 처리할 때는 자동 입출금 과정에 참여하지 않는 초과 자금을 저장하기 위한 콜드 월렛을 제공하는 것이 좋습니다.

### 자산 처리 및 초기 확인을 위한 새로운 Jetton 추가

1. 올바른 [스마트 컨트랙트 주소](/develop/dapps/asset-processing/jettons#jetton-master-smart-contract)를 찾습니다.
2. [메타데이터](/develop/dapps/asset-processing/jettons#retrieving-jetton-data)를 가져옵니다.
3. [사기](/develop/dapps/asset-processing/jettons#jetton-master-smart-contract) 여부를 확인합니다.

### 전송 알림 메시지를 수신할 때 알려지지 않은 Jetton 식별

지갑 내에서 알려지지 않은 Jetton에 대한 전송 알림 메시지를 수신한 경우, 해당 Jetton을 보유하도록 지갑이 생성된 것입니다.

`전송 알림` 본문을 포함하는 내부 메시지의 발신자 주소는 새로운 Jetton 지갑의 주소입니다. 이는 `전송 알림` [본문](/develop/dapps/asset-processing/jettons#jetton-wallets-communication-overview)의 `발신자` 필드와 혼동해서는 안 됩니다.

1. [지갑 데이터 가져오기](/develop/dapps/asset-processing/jettons#retrieving-data-for-a-specific-jetton-wallet)를 통해 새로운 Jetton 지갑의 Jetton 마스터 주소를 가져옵니다.
2. Jetton 마스터 컨트랙트 사용하여 [사용자에 대한 Jetton 지갑 주소를 가져오는 방법](#retrieving-jetton-wallet-addresses-for-a-given-user)을 사용하여 지갑 주소의 Jetton 지갑 주소를 가져옵니다.
3. 마스터 컨트래트에서 반환된 주소와 실제 지갑 토큰의 주소를 비교합니다.
   일치하면 이상적입니다. 그렇지 않으면 가짜 토큰을 받은 것일 수 있습니다.
4. Jetton 메타데이터를 가져옵니다: [Jetton 메타데이터 수신 방법](#retrieving-jetton-data).
5. `심볼` 및 `이름` 필드를 사기 여부를 확인합니다. 필요시 사용자에게 경고합니다. [자산 처리 및 초기 확인을 위한 새로운 Jetton 추가](#adding-new-jettons-for-asset-processing-and-initial-verification)를 참조하세요.

### 중앙화된 지갑을 통한 사용자로부터의 Jetton 수락

:::info
단일 지갑으로 들어오는 거래의 병목 현상을 방지하기 위해, 여러 지갑에 걸쳐 입금을 수락하고 필요에 따라 지갑의 수를 늘리는 것이 좋습니다.
:::

이 시나리오에서는 결제 서비스가 발신자에게 중앙화된 지갑의 주소와 보낼 금액을 공개하는 고유 메모 식별자를 생성합니다. 발신자는 중앙화된 주소로 토큰을 지정된 메모와 함께 전송합니다.

**이 방법의 장점:** 이 방법은 추가 수수료가 없으며 토큰이 직접 핫 월렛에 수신되기 때문에 매우 간단합니다.

**이 방법의 단점:** 이 방법은 모든 사용자가 전송 시 주석을 첨부해야 하기 때문에 더 많은 입금 실수(메모 누락, 잘못된 메모 등)가 발생할 수 있으며, 이는 지원 직원의 작업 부담을 증가시킵니다.

Tonweb 예제:

1. [주석(메모)을 포함한 개별 HOT 월렛으로의 Jetton 입금 수락](https://github.com/toncenter/examples/blob/main/deposits-jettons.js)
2. [Jetton 출금 예제](https://github.com/toncenter/examples/blob/main/withdrawals-jettons.js)

#### 준비 사항

1. [허용된 Jetton 목록 준비](/develop/dapps/asset-processing/jettons#adding-new-jettons-for-asset-processing-and-initial-verification) (Jetton 마스터 주소).
2. 핫 월렛 배포 (Jetton 출금이 예상되지 않는 경우 v3R2 사용; Jetton 출금이 예상되는 경우 고부하 v3 사용). [지갑 배포](/develop/dapps/asset-processing/#wallet-deployment).
3. 핫 월렛 주소를 사용하여 테스트 Jetton 전송을 수행하여 지갑을 초기화합니다.

#### 수신되는 Jetton 처리

1. 허용된 Jetton 목록을 로드합니다.
2. 배포된 핫 월렛에 대한 [Jetton 지갑 주소 가져오기](#retrieving-jetton-wallet-addresses-for-a-given-user).
3. [지갑 데이터 가져오기](/develop/dapps/asset-processing/jettons#retrieving-data-for-a-specific-jetton-wallet)를 사용하여 각 Jetton 지갑의 Jetton 마스터 주소를 가져옵니다.
4. 1단계와 바로 위의 3단계의 Jetton 마스터 컨트랙트의 주소를 비교합니다.
   주소가 일치하지 않으면 Jetton 주소 확인 오류를 보고해야 합니다.
5. 핫 월렛 계정을 사용하여 가장 최근에 처리되지 않은 거래 목록을 가져오고
   이를 반복합니다 (각 거래를 하나씩 확인). [계약의 거래 확인](https://docs.ton.org/develop/dapps/asset-processing/#checking-contracts-transactions)을 참조하세요.
6. 거래의 입력 메시지(in_msg)를 확인하고 입력 메시지에서 소스 주소를 가져옵니다. [Tonweb 예제](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-jettons-single-wallet.js#L84)
7. 소스 주소가 Jetton 지갑 내의 주소와 일치하면 거래를 계속 처리해야 합니다.
   일치하지 않으면 거래 처리를 건너뛰고 다음 거래를 확인합니다.
8. 메시지 본문이 비어 있지 않고 메시지의 첫 32비트가 `전송 알림` 연산 코드 `0x7362d09c`와 일치하는지 확인합니다.
   [Tonweb 예제](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-jettons-single-wallet.js#L91)
   메시지 본문이 비어 있거나 연산 코드가 잘못된 경우 - 거래를 건너뜁니다.
9. 메시지 본문의 다른 데이터를 읽습니다. 여기에는 `query_id`, `amount`, `sender`, `forward_payload`가 포함됩니다.
   [Jetton 컨트랙트 메시지 레이아웃](#jetton-contract-message-layouts), [Tonweb 예제](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-jettons-single-wallet.js#L105)
10. `forward_payload` 데이터에서 텍스트 주석을 가져오려고 합니다. 첫 32비트는
    텍스트 주석 연산 코드 `0x00000000`과 일치해야 하며, 나머지는 UTF-8로 인코딩된 텍스트입니다.
    [Tonweb 예제](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-jettons-single-wallet.js#L110)
11. `forward_payload` 데이터가 비어 있거나 연산 코드가 잘못된 경우 - 거래를 건너뜁니다.
12. 수신된 주석과 저장된 메모를 비교합니다. 일치하는 경우 (사용자 식별이 항상 가능) - 전송을 입금합니다.
13. 5단계부터 시작하여 전체 거래 목록을 순회할 때까지 과정을 반복합니다.

### 사용자 입금 주소에서 Jetton 수락

사용자 입금 주소에서 Jetton을 수락하려면, 결제 서비스가 자금을 송금하는 각 참가자를 위한 개별 주소(입금 주소)를 생성해야 합니다. 이 경우 서비스 제공에는 새로운 입금 생성, 거래 블록 스캔, 입금에서 핫 월렛으로 자금 인출 등의 여러 병렬 프로세스가 포함됩니다.

핫 월렛은 각 Jetton 유형에 대해 하나의 Jetton 지갑을 사용할 수 있기 때문에 여러 지갑을 만들어 입금을 시작해야 합니다. 많은 수의 지갑을 생성하면서도 하나의 시드 문구(또는 개인 키)로 이를 관리하려면, 지갑 생성 시 다른 `subwallet_id`를 지정해야 합니다. TON에서는 버전 v3 지갑 이상에서 서브월렛 생성을 지원합니다.

#### Tonweb에서 서브월렛 생성

```js
const WalletClass = tonweb.wallet.all['v3R2'];
const wallet = new WalletClass(tonweb.provider, {
    publicKey: keyPair.publicKey,
    wc: 0,
    walletId: <SUBWALLET_ID>,
});
```

#### 준비 사항

1. [허용된 Jetton 목록 준비](#adding-new-jettons-for-asset-processing-and-initial-verification).
2. 핫 월렛 배포 (Jetton 출금이 예상되지 않는 경우 v3R2 사용; Jetton 출금이 예상되는 경우 고부하 v3 사용). [지갑 배포](/develop/dapps/asset-processing/#wallet-deployment).

#### 입금 생성

1. 사용자의 새로운 입금 요청을 수락합니다.
2. 핫 월렛 시드를 기반으로 새 서브월렛(v3R2) 주소를 생성합니다. [Tonweb에서 서브월렛 생성](#creating-a-subwallet-in-tonweb)
3. 수신 주소는 사용자에게 Jetton 입금에 사용할 주소로 제공될 수 있습니다 (이는 입금 Jetton 지갑 소유자의 주소입니다). 지갑 초기화는 필요하지 않으며, 입금에서 Jetton을 인출할 때 수행할 수 있습니다.
4. 이 주소에 대해 Jetton 마스터 계약을 통해 Jetton 지갑 주소를 계산해야 합니다.
   [주어진 사용자에 대한 Jetton 지갑 주소를 가져오는 방법](#retrieving-jetton-wallet-addresses-for-a-given-user).
5. 거래 모니터링을 위한 주소 풀에 Jetton 지갑 주소를 추가하고 서브월렛 주소를 저장합니다.

#### 거래 처리

:::info 거래 확인
TON 거래는 한 번 확인되면 되돌릴 수 없습니다. 최고의 사용자 경험을 위해, TON 블록체인에서 거래가 완료되면 추가 블록을 기다리지 않는 것이 좋습니다. 자세한 내용은 [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3)에서 확인하세요.
:::

메시지에서 받은 Jetton의 정확한 양을 항상 확인할 수 있는 것은 아닙니다. Jetton 지갑이 `전송 알림`, `초과`, 및 `내부 전송` 메시지를 보내지 않을 수 있기 때문입니다. 이들은 표준화되지 않았습니다. 이는 `내부 전송` 메시지를 디코딩할 수 있다는 보장이 없음을 의미합니다.

따라서, 지갑에서 받은 양을 확인하기 위해서는 잔액을 get 메서드를 사용하여 요청해야 합니다. 잔액을 요청할 때 필요한 주요 데이터를 가져오기 위해 블록이 사용됩니다. 특정 블록 온체인의 계정 상태에 따라 블록을 준비합니다. [Tonweb을 사용한 블록 수락 준비](https://github.com/toncenter/tonweb/blob/master/src/test-block-subscribe.js).

이 과정은 다음과 같이 진행됩니다:

1. 블록 수락 준비 (새 블록을 수락할 수 있도록 시스템을 준비).
2. 새 블록을 가져와 이전 블록 ID를 저장합니다.
3. 블록에서 거래를 수신합니다.
4. 입금 Jetton 지갑 풀의 주소로만 사용된 거래를 필터링합니다.
5. 메시지를 `전송 알림` 본문을 사용하여 디코딩하여 자세한 데이터를 수신합니다. 여기에는 `발신자` 주소, Jetton `양` 및 주석이 포함됩니다. (참조: [들어오는 Jetton 처리](#processing-incoming-jettons))
6. 디코딩할 수 없는 출력 메시지가 포함된 거래가 하나라도 있는 경우 (메시지 본문에 `전송 알림` 연산 코드와 `초과` 연산 코드가 포함되지 않은 경우) 또는 계정 내 출력 메시지가 없는 경우, 현재 블록에 대해 Jetton 잔액을 get 메서드를 사용하여 요청해야 하며, 이전 블록을 사용하여 잔액 변화를 계산합니다. 이제 블록 내에서 수행된 거래로 인한 총 잔액 입금 변화를 드러낼 수 있습니다.
7. 식별되지 않은 Jetton 전송(`전송 알림`이 없는 경우)에 대한 식별자로서, 거래 데이터가 하나만 있는 경우 해당 거래 데이터를 사용할 수 있습니다.
8. 이제 입금 잔액이 정확한지 확인해야 합니다. 입금 잔액이 핫 월렛과 기존 Jetton 지갑 간의 전송을 시작할 만큼 충분한 경우, Jetton을 인출하여 지갑 잔액이 감소했는지 확인해야 합니다.
9. 2단계부터 다시 시작하여 전체 과정을 반복합니다.

#### 예금에서 출금

각 예금 보충 시 예금에서 핫 월렛으로의 전송이 이루어지지 않도록 해야 합니다. 이는 전송 작업에 대한 TON 수수료(네트워크 가스 요금으로 지불)가 발생하기 때문입니다. 전송이 가치 있도록 하기 위해 필요한 최소한의 Jetton 양을 결정하는 것이 중요합니다.

기본적으로, Jetton 예금 지갑의 지갑 소유자는 초기화되지 않습니다. 이는 저장 수수료를 사전에 지불할 필요가 없기 때문입니다. Jetton 예금 지갑은 `transfer` 본문이 포함된 메시지를 보낼 때 배포되며, 이후 즉시 파괴될 수 있습니다. 이를 위해 엔지니어는 메시지를 보내는 특별한 메커니즘을 사용해야 합니다: [128 + 32](/develop/smart-contracts/messages#message-modes).

1. 핫 월렛으로 인출을 표시한 예금 목록을 가져옵니다.
2. 각 예금에 대한 소유자 주소를 저장된 정보를 바탕으로 가져옵니다.
3. 메시지는 각 소유자 주소로 전송되며, 이러한 메시지 여러 개를 묶어서 배치(batch) 형태로 고성능(highload) 지갑에서 전송합니다. 이때 첨부되는 TON Jetton 양은 v3R2 지갑 초기화에 필요한 수수료 + `transfer` 메시지 본문을 전송하는 데 필요한 수수료 + `forward_ton_amount`와 관련된 임의의 TON 양(필요한 경우)을 더하여 결정됩니다. 첨부된 TON 양은 v3R2 지갑 초기화에 필요한 수수료(값) + `transfer` 메시지 본문을 전송하는 데 필요한 수수료(값) + `forward_ton_amount`를 위한 임의의 TON 양(값)(필요한 경우)을 더하여 결정됩니다.
4. 주소의 잔액이 0이 아닌 경우 계정 상태가 변경됩니다. 몇 초 기다린 후 계정 상태를 확인하여 `nonexists` 상태에서 `uninit` 상태로 변경되는지 확인합니다.
5. 각 소유자 주소(`uninit` 상태)에 v3R2 지갑 초기화 및 Jetton 지갑에 예금을 위한 `transfer` 메시지를 포함한 외부 메시지를 보내야 합니다. `transfer`의 경우 핫 월렛 주소를 `destination` 및 `response destination`으로 지정해야 합니다. 전송을 식별하기 쉽게 하기 위해 텍스트 코멘트를 추가할 수 있습니다.
6. Jetton 지갑 주소에서 핫 월렛 주소로 Jetton이 전달되는지 확인할 수 있습니다. 자세한 내용은 [여기](#processing-incoming-jettons)에서 확인할 수 있습니다.

### Jetton 인출

:::info 중요

이 섹션을 읽기 전에 [jetton 전송 작동 방식](#jetton-wallets-communication-overview) 및 [코멘트와 함께 jetton 보내기](#jetton-off-chain-processing) 기사들을 읽고 이해하는 것이 **권장**됩니다.

Jetton을 인출하려면 지갑이 해당 Jetton 지갑으로 `transfer` 본문이 포함된 메시지를 보냅니다. Jetton 지갑은 수신자에게 Jetton을 보냅니다. 신뢰성을 위해 `forward_ton_amount` (선택적으로 `forward_payload`에 코멘트 추가)와 함께 일부 TON을 첨부하는 것이 중요합니다. 자세한 내용은 [Jetton 계약 메시지 레이아웃](#jetton-contract-message-layouts)을 참조하십시오.

#### 준비 사항

1. 인출할 Jetton 목록을 준비합니다: [자산 처리 및 초기 검증을 위한 새로운 Jetton 추가](#adding-new-jettons-for-asset-processing-and-initial-verification)
2. 핫 월렛 배포를 시작합니다. 고부하 v3을 권장합니다. [지갑 배포](#wallet-deployment)
3. Jetton 지갑을 초기화하고 잔액을 보충하기 위해 핫 월렛 주소를 사용하여 Jetton 전송을 수행합니다.

#### 출금 처리

1. 처리된 Jetton 목록을 불러옵니다.
2. 배포된 핫 월렛에 대한 Jetton 지갑 주소를 가져옵니다: [사용자에 대한 Jetton 지갑 주소를 가져오는 방법](#retrieving-jetton-wallet-addresses-for-a-given-user)
3. 각 Jetton 지갑의 Jetton 마스터 주소를 가져옵니다: [특정 Jetton 지갑의 데이터 가져오기](#retrieving-data-for-a-specific-jetton-wallet). `jetton` 매개변수가 필요합니다 (실제로 Jetton 마스터 계약의 주소입니다).
4. 1단계와 3단계에서 얻은 Jetton 마스터 계약의 주소를 비교합니다. 주소가 일치하지 않으면 Jetton 주소 검증 오류를 보고해야 합니다.
5. 인출 요청을 받아 실제로 전송되는 Jetton의 종류, 금액 및 수신자 지갑 주소를 나타냅니다.
6. 인출을 수행하기에 충분한 자금이 있는지 확인하기 위해 Jetton 지갑 잔액을 확인합니다.
7. [메시지 생성](#message-0).
8. 고부하 지갑을 사용할 때는 수수료 최적화를 위해 메시지를 일괄 처리하여 한 번에 한 배치씩 보내는 것이 좋습니다.
9. 외부 메시지의 만료 시간을 저장합니다 (이 시간 동안 지갑이 메시지를 성공적으로 처리한 후 지갑은 더 이상 메시지를 수락하지 않습니다).
10. 단일 메시지 또는 여러 메시지(배치 메시지)를 보냅니다.
11. 핫 월렛 계정 내 처리되지 않은 최신 거래 목록을 검색하고 이를 반복합니다. 자세한 내용은 [계약의 거래 확인](#checking-contracts-transactions), [Tonweb 예제](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-single-wallet.js#L43)를 참조하거나 Toncenter API `/getTransactions` 메서드를 사용합니다.
12. 계정에서 나가는 메시지를 확인합니다.
13. `transfer` 연산 코드가 포함된 메시지가 있으면 이를 디코딩하여 `query_id` 값을 가져옵니다. 가져온 `query_id`는 성공적으로 전송된 것으로 표시해야 합니다.
14. 현재 스캔된 거래를 처리하는 데 걸리는 시간이 만료 시간보다 길고 해당 `query_id`가 있는 나가는 메시지가 발견되지 않으면 요청이 만료된 것으로 표시하고 안전하게 다시 전송해야 합니다 (선택 사항).
15. 계정에서 들어오는 메시지를 확인합니다.
16. `excesses` 연산 코드를 사용하는 메시지가 있으면 메시지를 디코딩하여 `query_id` 값을 가져옵니다. 발견된 `query_id`는 성공적으로 전달된 것으로 표시해야 합니다.
17. 5단계로 돌아갑니다. 성공적으로 전송되지 않은 만료된 요청은 인출 목록으로 다시 푸시해야 합니다.

## Jetton 온체인 처리

일반적으로, jetton을 수락하고 처리하기 위해 내부 메시지에 대한 메시지 핸들러는 `op=0x7362d09c` 연산 코드를 사용합니다.

:::info 거래 확인
TON 거래는 한 번의 확인 후에는 되돌릴 수 없습니다. 최고의 사용자 경험을 위해, TON 블록체인에서 거래가 완료된 후 추가 블록을 기다리지 않는 것이 좋습니다. 자세한 내용은 [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3)를 참조하십시오.
:::

### 온체인 처리 권장 사항

아래는 **온체인 jetton 처리**를 수행할 때 고려해야 할 `권장 사항 목록`입니다:

1. Jetton 마스터 계약이 아닌, 지갑 유형을 사용하여 **들어오는 Jetton을 식별**합니다. 다시 말해, 귀하의 계약은 특정 Jetton 지갑과 상호 작용해야 하며(메시지 수신 및 전송) 특정 Jetton 마스터 계약을 사용하는 알 수 없는 지갑과 상호 작용해서는 안 됩니다.
2. Jetton 지갑과 Jetton 마스터를 연결할 때, **이 연결이 양방향인지 확인**하십시오. 지갑이 마스터 계약을 인식하고 그 반대도 마찬가지여야 합니다. 예를 들어, 귀하의 계약 시스템이 Jetton 지갑으로부터 알림을 받을 경우(해당 지갑이 MySuperJetton을 마스터 계약으로 간주하는 경우), 그 이전에 `심볼`, `이름` 및 `이미지`를 표시하기 전에 MySuperJetton 지갑이 올바른 계약 시스템을 사용하는지 확인해야 합니다. 또한, 귀하의 계약 시스템이 MySuperJetton 또는 MySuperJetton 마스터 계약을 사용하여 Jetton을 전송해야 하는 경우, 지갑 X가 동일한 계약 매개변수를 사용하는지 확인하십시오. X에 `전송` 요청을 보내기 전에, 해당 지갑이 MySuperJetton을 마스터로 인식하는지 확인하십시오.
3. 탈중앙화 금융(DeFi)의 **진정한 힘**은 레고 블록처럼 프로토콜을 쌓을 수 있는 능력에 기반합니다. 예를 들어, Jetton A가 Jetton B로 교환되고, 이 Jetton B가 대출 프로토콜 내에서 레버리지로 사용되며(사용자가 유동성을 공급할 때) 그 후 NFT를 구매하는 데 사용됩니다. 따라서, 계약이 온체인 사용자뿐만 아니라 오프체인 사용자도 지원할 수 있도록 고려해야 하며, 전송 알림에 토큰화된 가치를 첨부하거나 전송 알림과 함께 전송될 수 있는 맞춤형 페이로드를 추가해야 합니다.
4. **모든 계약이 동일한 표준을 따르는 것은 아니라는 점**을 인지하십시오. 불행히도, 일부 Jetton은 공격 벡터를 사용하여 순진한 사용자를 공격하기 위해 생성된 악의적인 계약일 수 있습니다. 보안상의 이유로, 프로토콜이 여러 계약으로 구성된 경우 동일한 유형의 Jetton 지갑을 대량으로 생성하지 마십시오. 특히, 프로토콜 내에서 입금 계약, 금고 계약 또는 사용자 계정 계약 간에 Jetton을 전송하지 마십시오. 공격자는 전송 알림, Jetton 양 또는 페이로드 매개변수를 위조하여 계약 논리를 의도적으로 방해할 수 있습니다. 시스템 내에서 Jetton당 하나의 지갑만 사용하여 공격 가능성을 줄이십시오(모든 입출금을 위한).
5. 주소 스푸핑의 가능성을 줄이기 위해 각 개별 Jetton에 대한 하위 계약을 생성하는 것이 **종종 좋은 방법**입니다(예: Jetton A용으로 의도된 계약을 사용하여 Jetton B에 전송 메시지를 보낼 때).
6. 계약 수준에서 불가분의 Jetton 단위를 사용하는 것이 **강력히 권장**됩니다. 소수점 관련 로직은 일반적으로 사용자 인터페이스(UI)를 개선하기 위해 사용되며, 온체인 기록 유지와는 관련이 없습니다.

**자세히 알아보고자** 한다면 [CertiK의 FunC에서 안전한 스마트 계약 프로그래밍](https://blog.ton.org/secure-smart-contract-programming-in-func)을 읽어보세요. 개발자들이 **모든 스마트 계약 예외를 처리**하도록 권장하며, 이는 애플리케이션 개발 중에 절대 건너뛰어서는 안 됩니다.

## Jetton 지갑 처리 권장사항

일반적으로, 오프체인 Jetton 처리에 사용되는 모든 검증 절차는 지갑에도 적합합니다. Jetton 지갑 처리에 있어 가장 중요한 권장 사항은 다음과 같습니다:

1. 지갑이 알 수 없는 Jetton 지갑으로부터 전송 알림을 받을 때, 해당 Jetton 지갑과 그 마스터 주소를 신뢰하는 것이 **매우 중요**합니다. 악의적인 위조일 수 있기 때문입니다. 스스로를 보호하기 위해, 제공된 주소를 사용하여 Jetton 마스터(마스터 계약)를 확인하고, 귀하의 검증 절차가 해당 Jetton 지갑을 정당한 것으로 인식하는지 확인하십시오. 지갑을 신뢰하고 정당한 것으로 확인된 후에만 계좌 잔액 및 기타 지갑 내 데이터를 접근할 수 있도록 허용하십시오. Jetton 마스터가 해당 지갑을 인식하지 못하면, Jetton 전송을 전혀 시작하거나 공개하지 않는 것이 좋으며, 전송 알림에 첨부된 Toncoin의 TON 전송만 표시하십시오.
2. 실제로, 사용자가 Jetton 지갑이 아닌 Jetton과 상호작용하기를 원할 때가 있습니다. 다시 말해, 사용자는 `EQAjN...`/`EQBLE...` 등이 아닌 wTON/oUSDT/jUSDT, jUSDC, jDAI 등을 전송합니다. 이는 종종 사용자가 Jetton 전송을 시작할 때, 지갑이 해당 Jetton 마스터에게(사용자가 소유한) 어떤 Jetton 지갑이 전송 요청을 시작해야 하는지를 묻는다는 것을 의미합니다. 이때 **마스터(마스터 계약)로부터 받은 데이터**를 무작정 신뢰해서는 안 됩니다. Jetton 지갑에 전송 요청을 보내기 전에, 해당 Jetton 지갑이 실제로 자신이 속해 있다고 주장하는 Jetton 마스터에 속하는지 확인하십시오.
3. **적대적인 Jetton 마스터/Jetton 지갑이** 시간이 지남에 따라 **지갑/마스터를 변경할 수 있다**는 점을 인지하십시오. 따라서 사용자는 각 사용 전에 상호작용하는 지갑의 정당성을 철저히 확인하는 것이 필수적입니다.
4. 인터페이스에 Jetton을 표시할 때 **TON 전송** 및 시스템 알림 등과 **혼동되지 않도록** 항상 주의하십시오. 심지어 `심볼`, `이름` 및 `이미지` 매개변수도 사용자를 오도하도록 조작될 수 있으며, 그 결과 피해자는 잠재적인 사기 피해자가 될 수 있습니다. 악의적인 Jetton이 TON 전송, 알림 오류, 보상 수익, 자산 동결 발표를 사칭하는 데 사용된 사례가 여러 번 있었습니다.
5. **악의적인 행위자들이** 위조된 Jetton을 생성할 가능성에 **항상 주의하십시오**. 사용자가 주요 사용자 인터페이스에서 원하지 않는 Jetton을 제거할 수 있는 기능을 제공하는 것이 좋습니다.

작가: [kosrk](https://github.com/kosrk), [krigga](https://github.com/krigga), [EmelyanenkoK](https://github.com/EmelyanenkoK/), [tolya-yanot](https://github.com/tolya-yanot/)

## 모범 사례

테스트 가능한 예제를 원한다면 [SDKs](/develop/dapps/asset-processing/jettons#sdks)에서 확인하고 실행해보세요. 아래는 코드 예제를 통해 Jetton 처리를 이해하는 데 도움이 될 코드 스니펫입니다.

### 주석과 함께 Jetton 전송하기

<Tabs groupId="code-examples">
<TabItem value="tonweb" label="JS (tonweb)">

<details>
<summary>
소스 코드
</summary>

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
    toAddress: new TonWeb.utils.Address(WALLET2_ADDRESS), // recepient user's wallet address (not Jetton wallet)
    forwardAmount: TonWeb.utils.toNano('0.01'), // some amount of TONs to invoke Transfer notification message
    forwardPayload: comment, // text comment for Transfer notification message
    responseAddress: walletAddress // return the TONs after deducting commissions back to the sender's wallet address
  }),
  sendMode: 3,
}).send()
```

</details>

</TabItem>
<TabItem value="tonutils-go" label="Golang">

<details>
<summary>
소스 코드
</summary>

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

</details>

</TabItem>
<TabItem value="TonTools" label="Python">

<details>
<summary>
소스 코드
</summary>

```py
my_wallet = Wallet(provider=client, mnemonics=my_wallet_mnemonics, version='v4r2')

# for TonCenterClient and LsClient
await my_wallet.transfer_jetton(destination_address='address', jetton_master_address=jetton.address, jettons_amount=1000, fee=0.15) 

# for all clients
await my_wallet.transfer_jetton_by_jetton_wallet(destination_address='address', jetton_wallet='your jetton wallet address', jettons_amount=1000, fee=0.1)  
```

</details>

</TabItem>

<TabItem value="pytoniq" label="Python">

<details>
<summary>
소스 코드
</summary>

```py
from pytoniq import LiteBalancer, WalletV4R2, begin_cell
import asyncio

mnemonics = ["your", "mnemonics", "here"]

async def main():
    provider = LiteBalancer.from_mainnet_config(1)
    await provider.start_up()

    wallet = await WalletV4R2.from_mnemonic(provider=provider, mnemonics=mnemonics)
    USER_ADDRESS = wallet.address
    JETTON_MASTER_ADDRESS = "EQBlqsm144Dq6SjbPI4jjZvA1hqTIP3CvHovbIfW_t-SCALE"
    DESTINATION_ADDRESS = "EQAsl59qOy9C2XL5452lGbHU9bI3l4lhRaopeNZ82NRK8nlA"

    USER_JETTON_WALLET = (await provider.run_get_method(address=JETTON_MASTER_ADDRESS,
                                                        method="get_wallet_address",
                                                        stack=[begin_cell().store_address(USER_ADDRESS).end_cell().begin_parse()]))[0].load_address()
    forward_payload = (begin_cell()
                      .store_uint(0, 32) # TextComment op-code
                      .store_snake_string("Comment")
                      .end_cell())
    transfer_cell = (begin_cell()
                    .store_uint(0xf8a7ea5, 32)          # Jetton Transfer op-code
                    .store_uint(0, 64)                  # query_id
                    .store_coins(1 * 10**9)             # Jetton amount to transfer in nanojetton
                    .store_address(DESTINATION_ADDRESS) # Destination address
                    .store_address(USER_ADDRESS)        # Response address
                    .store_bit(0)                       # Custom payload is None
                    .store_coins(1)                     # Ton forward amount in nanoton
                    .store_bit(1)                       # Store forward_payload as a reference
                    .store_ref(forward_payload)         # Forward payload
                    .end_cell())

    await wallet.transfer(destination=USER_JETTON_WALLET, amount=int(0.05*1e9), body=transfer_cell)
    await provider.close_all()

asyncio.run(main())
```

</details>

</TabItem>
</Tabs>

### 주석을 해석하여 Jetton 전송 수락하기

<Tabs groupId="parse-code-examples">
<TabItem value="tonweb" label="JS (tonweb)">

<details>
<summary>
소스 코드
</summary>

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
                continue; // op != transfer_notification
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

</details>

</TabItem>
<TabItem value="tonutils-go" label="Golang">

<details>
<summary>
소스 코드
</summary>

```go
import (
	"context"
	"fmt"
	"log"

	"github.com/xssnick/tonutils-go/address"
	"github.com/xssnick/tonutils-go/liteclient"
	"github.com/xssnick/tonutils-go/tlb"
	"github.com/xssnick/tonutils-go/ton"
	"github.com/xssnick/tonutils-go/ton/jetton"
	"github.com/xssnick/tonutils-go/tvm/cell"
)

const (
	MainnetConfig   = "https://ton.org/global.config.json"
	TestnetConfig   = "https://ton.org/global.config.json"
	MyWalletAddress = "INSERT-YOUR-HOT-WALLET-ADDRESS"
)

type JettonInfo struct {
	address  string
	decimals int
}

type Jettons struct {
	jettonMinter        *jetton.Client
	jettonWalletAddress string
	jettonWallet        *jetton.WalletClient
}

func prepare(api ton.APIClientWrapped, jettonsInfo map[string]JettonInfo) (map[string]Jettons, error) {
	userAddress := address.MustParseAddr(MyWalletAddress)
	block, err := api.CurrentMasterchainInfo(context.Background())
	if err != nil {
		return nil, err
	}

	jettons := make(map[string]Jettons)

	for name, info := range jettonsInfo {
		jettonMaster := jetton.NewJettonMasterClient(api, address.MustParseAddr(info.address))
		jettonWallet, err := jettonMaster.GetJettonWallet(context.Background(), userAddress)
		if err != nil {
			return nil, err
		}

		jettonUserAddress := jettonWallet.Address()

		jettonData, err := api.RunGetMethod(context.Background(), block, jettonUserAddress, "get_wallet_data")
		if err != nil {
			return nil, err
		}

		slice := jettonData.MustCell(0).BeginParse()
		slice.MustLoadCoins() // skip balance
		slice.MustLoadAddr()  // skip owneer address
		adminAddress := slice.MustLoadAddr()

		if adminAddress.String() != info.address {
			return nil, fmt.Errorf("jetton minter address from jetton wallet doesnt match config")
		}

		jettons[name] = Jettons{
			jettonMinter:        jettonMaster,
			jettonWalletAddress: jettonUserAddress.String(),
			jettonWallet:        jettonWallet,
		}
	}

	return jettons, nil
}

func jettonWalletAddressToJettonName(jettons map[string]Jettons, jettonWalletAddress string) string {
	for name, info := range jettons {
		if info.jettonWallet.Address().String() == jettonWalletAddress {
			return name
		}
	}
	return ""
}

func GetTransferTransactions(orderId string, foundTransfer chan<- *tlb.Transaction) {
	jettonsInfo := map[string]JettonInfo{
		"jUSDC": {address: "EQB-MPwrd1G6WKNkLz_VnV6WqBDd142KMQv-g1O-8QUA3728", decimals: 6},
		"jUSDT": {address: "EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA", decimals: 6},
	}

	client := liteclient.NewConnectionPool()

	cfg, err := liteclient.GetConfigFromUrl(context.Background(), MainnetConfig)
	if err != nil {
		log.Fatalln("get config err: ", err.Error())
	}

	// connect to lite servers
	err = client.AddConnectionsFromConfig(context.Background(), cfg)
	if err != nil {
		log.Fatalln("connection err: ", err.Error())
	}

	// initialize ton api lite connection wrapper
	api := ton.NewAPIClient(client, ton.ProofCheckPolicySecure).WithRetry()
	master, err := api.CurrentMasterchainInfo(context.Background())
	if err != nil {
		log.Fatalln("get masterchain info err: ", err.Error())
	}

	// address on which we are accepting payments
	treasuryAddress := address.MustParseAddr("EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N")

	acc, err := api.GetAccount(context.Background(), master, treasuryAddress)
	if err != nil {
		log.Fatalln("get masterchain info err: ", err.Error())
	}

	jettons, err := prepare(api, jettonsInfo)
	if err != nil {
		log.Fatalln("can't prepare jettons data: ", err.Error())
	}

	lastProcessedLT := acc.LastTxLT

	transactions := make(chan *tlb.Transaction)

	go api.SubscribeOnTransactions(context.Background(), treasuryAddress, lastProcessedLT, transactions)

	log.Println("waiting for transfers...")

	// listen for new transactions from channel
	for tx := range transactions {
		if tx.IO.In == nil || tx.IO.In.MsgType != tlb.MsgTypeInternal {
			// external message - not related to jettons
			continue
		}

		msg := tx.IO.In.Msg
		sourceAddress := msg.SenderAddr()

		// jetton master contract address check
		jettonName := jettonWalletAddressToJettonName(jettons, sourceAddress.String())
		if len(jettonName) == 0 {
			// unknown or fake jetton transfer
			continue
		}

		if msg.Payload() == nil || msg.Payload() == cell.BeginCell().EndCell() {
			// no in_msg body
			continue
		}

		msgBodySlice := msg.Payload().BeginParse()

		op := msgBodySlice.MustLoadUInt(32)
		if op != 0x7362d09c {
			continue // op != transfer_notification
		}

		// just skip bits
		msgBodySlice.MustLoadUInt(64)
		amount := msgBodySlice.MustLoadCoins()
		msgBodySlice.MustLoadAddr()

		payload := msgBodySlice.MustLoadMaybeRef()
		payloadOp := payload.MustLoadUInt(32)
		if payloadOp == 0 {
			log.Println("no text comment in transfer_notification")
			continue
		}

		comment := payload.MustLoadStringSnake()
		if comment != orderId {
			continue
		}

		// process transaction
		log.Printf("Got %s jetton deposit %d units with text comment %s\n", jettonName, amount, comment)
		foundTransfer <- tx
	}
}
```

</details>
</TabItem>

<TabItem value="pythoniq" label="Python">

<details>
<summary>
소스 코드
</summary>

```py
import asyncio

from pytoniq import LiteBalancer, begin_cell

MY_WALLET_ADDRESS = "EQAsl59qOy9C2XL5452lGbHU9bI3l4lhRaopeNZ82NRK8nlA"


async def parse_transactions(provider: LiteBalancer, transactions):
    for transaction in transactions:
        if not transaction.in_msg.is_internal:
            continue
        if transaction.in_msg.info.dest.to_str(1, 1, 1) != MY_WALLET_ADDRESS:
            continue

        sender = transaction.in_msg.info.src.to_str(1, 1, 1)
        value = transaction.in_msg.info.value_coins
        if value != 0:
            value = value / 1e9

        if len(transaction.in_msg.body.bits) < 32:
            print(f"TON transfer from {sender} with value {value} TON")
            continue

        body_slice = transaction.in_msg.body.begin_parse()
        op_code = body_slice.load_uint(32)
        if op_code != 0x7362D09C:
            continue

        body_slice.load_bits(64)  # skip query_id
        jetton_amount = body_slice.load_coins() / 1e9
        jetton_sender = body_slice.load_address().to_str(1, 1, 1)
        if body_slice.load_bit():
            forward_payload = body_slice.load_ref().begin_parse()
        else:
            forward_payload = body_slice

        jetton_master = (
            await provider.run_get_method(
                address=sender, method="get_wallet_data", stack=[]
            )
        )[2].load_address()
        jetton_wallet = (
            (
                await provider.run_get_method(
                    address=jetton_master,
                    method="get_wallet_address",
                    stack=[
                        begin_cell()
                        .store_address(MY_WALLET_ADDRESS)
                        .end_cell()
                        .begin_parse()
                    ],
                )
            )[0]
            .load_address()
            .to_str(1, 1, 1)
        )

        if jetton_wallet != sender:
            print("FAKE Jetton Transfer")
            continue

        if len(forward_payload.bits) < 32:
            print(
                f"Jetton transfer from {jetton_sender} with value {jetton_amount} Jetton"
            )
        else:
            forward_payload_op_code = forward_payload.load_uint(32)
            if forward_payload_op_code == 0:
                print(
                    f"Jetton transfer from {jetton_sender} with value {jetton_amount} Jetton and comment: {forward_payload.load_snake_string()}"
                )
            else:
                print(
                    f"Jetton transfer from {jetton_sender} with value {jetton_amount} Jetton and unknown payload: {forward_payload} "
                )

        print(f"Transaction hash: {transaction.cell.hash.hex()}")
        print(f"Transaction lt: {transaction.lt}")


async def main():
    provider = LiteBalancer.from_mainnet_config(1)
    await provider.start_up()
    transactions = await provider.get_transactions(address=MY_WALLET_ADDRESS, count=5)
    await parse_transactions(provider, transactions)
    await provider.close_all()


if __name__ == "__main__":
    asyncio.run(main())
```

</details>
</TabItem>
</Tabs>

## SDKs

여기에서 다양한 언어(js, python, golang, C#, Rust 등)를 위한 SDK 목록을 확인할 수 있습니다: [여기](/develop/dapps/apis/sdk).

## 참고 항목

- [결제 처리](/develop/dapps/asset-processing/)
- [TON에서 NFT 처리](/develop/dapps/asset-processing/nfts)
- [TON에서 메타데이터 파싱](/develop/dapps/asset-processing/metadata)
