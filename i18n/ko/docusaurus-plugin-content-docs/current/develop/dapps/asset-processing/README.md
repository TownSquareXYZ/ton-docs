import Button from '@site/src/components/button'
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# 결제 처리

이 페이지는 TON 블록체인에서 `디지털 자산`을 처리하는 방법을 **설명**합니다 (전송 및 수신). 주로 `TON 코인`과 관련된 내용을 다루지만, **이론적인 부분**은 `jettons`만 처리하고자 할 때에도 **중요**합니다.

## 지갑 스마트 컨트랙트

지갑 스마트 계약은 TON 네트워크에서 블록체인 외부의 사용자들이 블록체인 내의 엔티티와 상호작용할 수 있도록 하는 계약입니다. 일반적으로 다음 세 가지 문제를 해결합니다:

- 소유자 인증: 소유자가 아닌 사용자의 요청은 처리 및 수수료 지불을 거부합니다.
- 재생 보호: 동일한 요청을 반복적으로 실행하는 것을 금지합니다. 예를 들어, 자산을 다른 스마트 계약으로 전송하는 경우.
- 다른 스마트 계약과의 임의 상호작용을 시작합니다.

첫 번째 문제에 대한 표준 해결책은 공개 키 암호화입니다. `지갑`은 공개 키를 저장하고, 요청이 소유자만 알고 있는 개인 키로 서명되었는지 확인합니다.

세 번째 문제에 대한 해결책은 일반적으로 요청에 네트워크에 보낼 내부 메시지가 포함된다는 점에서 동일합니다. 하지만 재생 보호를 위해서는 몇 가지 다른 접근 방식이 있습니다.

### Seqno 기반 지갑

Seqno 기반 지갑은 메시지를 순차적으로 처리하는 가장 단순한 접근 방식을 따릅니다. 각 메시지에는 `seqno`라는 정수가 포함되어 있으며, 이는 `지갑` 스마트 계약에 저장된 카운터와 일치해야 합니다. `지갑`은 각 요청에서 카운터를 업데이트하여 동일한 요청이 두 번 처리되지 않도록 합니다. Seqno 기반 지갑은 공개적으로 사용 가능한 메서드에 따라 몇 가지 버전이 있습니다: 요청을 만료 시간으로 제한하는 기능, 동일한 공개 키로 여러 지갑을 사용하는 기능 등. 하지만 이 접근 방식은 요청을 하나씩 전송해야 한다는 본질적인 요구 사항이 있으며, seqno 순서에 공백이 생기면 이후의 모든 요청을 처리할 수 없게 됩니다.

### 고부하 지갑

이 지갑 유형은 스마트 계약 저장소에 만료되지 않은 요청 식별자를 저장하는 방식에 기반한 접근 방식을 따릅니다. 이 방식에서는 모든 요청이 이미 처리된 요청과 중복 여부를 확인하고, 중복이 감지되면 요청을 삭제합니다. 만료로 인해 스마트 계약은 모든 요청을 영구적으로 저장하지 않으며, 만료 제한으로 인해 처리할 수 없는 요청은 제거됩니다. 이 지갑에 대한 요청은 서로 간섭하지 않고 병렬로 전송될 수 있습니다. 하지만 이 접근 방식은 요청 처리에 대한 더 정교한 모니터링이 필요합니다.

### 지갑 배포

TonLib를 통해 지갑을 배포하려면:

1. [createNewKey](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L244) 또는 그 래퍼 함수를 통해 개인/공개 키 쌍을 생성합니다 (예시: [tonlib-go](https://github.com/mercuryoio/tonlib-go/tree/master/v2#create-new-private-key)). 개인 키는 로컬에서 생성되며, 호스트 머신을 벗어나지 않습니다.
2. 하나의 `지갑` 활성화에 해당하는 [InitialAccountWallet](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L62) 구조를 형성합니다. 현재는 `wallet.v3`, `wallet.v4`, `wallet.highload.v1`, `wallet.highload.v2`가 사용 가능합니다.
3. [getAccountAddress](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L283) 메서드를 통해 새 `지갑` 스마트 계약의 주소를 계산합니다. 기본 개정 `0`을 사용하는 것을 권장하며, 처리 및 저장 비용을 낮추기 위해 `basechain workchain=0`에 지갑을 배포하는 것이 좋습니다.
4. 계산된 주소로 약간의 Toncoin을 전송합니다. 이 주소는 아직 코드가 없기 때문에 수신 메시지를 처리할 수 없으므로 `non-bounce` 모드로 전송해야 합니다. `non-bounce` 플래그는 처리 실패 시에도 돈이 반송되지 않아야 함을 나타냅니다. 특히 큰 금액을 포함하는 거래에서는 `non-bounce` 플래그 사용을 권장하지 않으며, 반송 메커니즘은 실수로부터 어느 정도 보호를 제공합니다.
5. 원하는 [action](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L154)을 형성합니다. 예를 들어 배포만을 위한 `actionNoop`을 사용할 수 있습니다. 그런 다음 [createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L292) 및 [sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L300)로 블록체인과 상호작용을 시작합니다.
6. 몇 초 후 [getAccountState](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L288) 메서드를 사용하여 계약을 확인합니다.

:::tip
[지갑 튜토리얼](/develop/smart-contracts/tutorials/wallet#-deploying-a-wallet)에서 자세히 읽어보세요.
:::

### 지갑 주소 유효성 확인

대부분의 SDK는 주소를 확인하도록 되어 있으며, 보통 지갑 생성 또는 거래 준비 과정에서 이를 확인합니다. 따라서 별도의 복잡한 단계를 수행할 필요는 거의 없습니다.

<Tabs groupId="address-examples">

  <TabItem value="Tonweb" label="JS (Tonweb)">

```js
  const TonWeb = require("tonweb")
  TonWeb.utils.Address.isValid('...')
```

  </TabItem>
  <TabItem value="GO" label="tonutils-go">

```python
package main

import (
  "fmt"
  "github.com/xssnick/tonutils-go/address"
)

if _, err := address.ParseAddr("EQCD39VS5j...HUn4bpAOg8xqB2N"); err != nil {
  return errors.New("invalid address")
}
```

  </TabItem>
  <TabItem value="Java" label="Ton4j">

```javascript
try {
  Address.of("...");
  } catch (e) {
  // not valid address
}
```

  </TabItem>
  <TabItem value="Kotlin" label="ton-kotlin">

```javascript
  try {
    AddrStd("...")
  } catch(e: IllegalArgumentException) {
      // not valid address
  }
```

  </TabItem>
</Tabs>

:::tip
[스마트 계약 주소](/learn/overviews/addresses) 페이지에서 전체 주소 설명을 확인하세요.
:::

## 송금 작업

### 컨트랙트의 거래 확인

컨트랙트의 거래는 [getTransactions](https://toncenter.com/api/v2/#/accounts/get_transactions_getTransactions_get) 메서드를 통해 얻을 수 있습니다. 이 메서드는 `last_transaction_id`와 그 이전의 10개의 거래를 가져옵니다. 모든 수신 거래를 처리하려면 다음 단계를 따르세요:

1. 최신 `last_transaction_id`는 [getAddressInformation](https://toncenter.com/api/v2/#/accounts/get_address_information_getAddressInformation_get)에서 얻을 수 있습니다.
2. `getTransactions` 메서드를 사용하여 10개의 거래 목록을 로드합니다.
3. 수신 메시지에 빈 소스가 없는 거래를 처리하고, 목적지가 계정 주소와 일치하는지 확인합니다.
4. 다음 10개의 거래를 로드하고, 2, 3, 4 단계를 반복하여 모든 수신 거래를 처리합니다.

### 수신/발신 거래 확인

거래 처리 중 메시지 흐름을 추적할 수 있습니다. 메시지 흐름은 DAG이므로, 현재 거래를 [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get) 메서드를 사용하여 가져오고, [tryLocateResultTx](https://testnet.toncenter.com/api/v2/#/transactions/get_try_locate_result_tx_tryLocateResultTx_get)에서 `out_msg`로 수신 거래를 찾거나 [tryLocateSourceTx](https://testnet.toncenter.com/api/v2/#/transactions/get_try_locate_source_tx_tryLocateSourceTx_get)에서 `in_msg`로 발신 거래를 찾을 수 있습니다.

<Tabs groupId="example-outgoing-transaction">
<TabItem value="JS" label="JS">

```ts
import { TonClient, Transaction } from '@ton/ton';
import { getHttpEndpoint } from '@orbs-network/ton-access';
import { CommonMessageInfoInternal } from '@ton/core';

async function findIncomingTransaction(client: TonClient, transaction: Transaction): Promise<Transaction | null> {
  const inMessage = transaction.inMessage?.info;
  if (inMessage?.type !== 'internal') return null;
  return client.tryLocateSourceTx(inMessage.src, inMessage.dest, inMessage.createdLt.toString());
}

async function findOutgoingTransactions(client: TonClient, transaction: Transaction): Promise<Transaction[]> {
  const outMessagesInfos = transaction.outMessages.values()
    .map(message => message.info)
    .filter((info): info is CommonMessageInfoInternal => info.type === 'internal');
  
  return Promise.all(
    outMessagesInfos.map((info) => client.tryLocateResultTx(info.src, info.dest, info.createdLt.toString())),
  );
}

async function traverseIncomingTransactions(client: TonClient, transaction: Transaction): Promise<void> {
  const inTx = await findIncomingTransaction(client, transaction);
  // now you can traverse this transaction graph backwards
  if (!inTx) return;
  await traverseIncomingTransactions(client, inTx);
}

async function traverseOutgoingTransactions(client: TonClient, transaction: Transaction): Promise<void> {
  const outTxs = await findOutgoingTransactions(client, transaction);
  // do smth with out txs
  for (const out of outTxs) {
    await traverseOutgoingTransactions(client, out);
  }
}

async function main() {
  const endpoint = await getHttpEndpoint({ network: 'testnet' });
  const client = new TonClient({
    endpoint,
    apiKey: '[API-KEY]',
  });
  
  const transaction: Transaction = ...; // Obtain first transaction to start traversing
  await traverseIncomingTransactions(client, transaction);
  await traverseOutgoingTransactions(client, transaction);
}

main();
```

</TabItem>
</Tabs>

### 결제 전송

1. 서비스는 `지갑`을 배포하고, 스토리지 비용으로 인한 계약 파괴를 방지하기 위해 이를 자금으로 유지해야 합니다. 스토리지 비용은 일반적으로 연간 1 Toncoin 미만입니다.
2. 서비스는 사용자로부터 `destination_address`와 선택적 `comment`를 받아야 합니다. 같은 (`destination_address`, `value`, `comment`) 집합을 가진 미완료 발신 결제를 금지하거나, 결제가 확인된 후에만 다음 결제를 시작하도록 적절히 예약할 것을 권장합니다.
3. `comment`를 텍스트로 작성한 [msg.dataText](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L103)를 형성합니다.
4. `destination_address`, 빈 `public_key`, 금액, `msg.dataText`를 포함한 [msg.message](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L113)를 형성합니다.
5. 발신 메시지 세트를 포함한 [Action](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L154)을 형성합니다.
6. 발신 결제를 전송하려면 [createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L292) 및 [sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L300) 쿼리를 사용합니다.
7. 서비스는 `wallet` 계약에 대해 [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get) 메서드를 정기적으로 폴링해야 합니다. (`destination_address`, `value`, `comment`)와 일치하는 확인된 거래를 통해 결제가 완료되었음을 표시할 수 있으며, 사용자에게 해당 거래 해시와 lt(논리 시간)를 표시할 수 있습니다.
8. `v3`의 `high-load` 지갑에 대한 요청의 만료 시간은 기본적으로 60초입니다. 이 시간이 지나면 처리되지 않은 요청은 네트워크에 안전하게 다시 보낼 수 있습니다(3~6단계 참조).

### 트랜잭션 ID 가져오기

트랜잭션에 대한 더 많은 정보를 얻으려면 사용자가 [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get) 기능을 통해 블록체인을 스캔해야 한다는 것이 명확하지 않을 수 있습니다.
메시지를 보낸 직후에 트랜잭션 ID를 즉시 가져오는 것은 불가능합니다. 트랜잭션이 먼저 블록체인 네트워크에 의해 확인되어야 합니다.
필요한 파이프라인을 이해하려면 [Send payments](https://docs.ton.org/develop/dapps/asset-processing/#send-payments)를 주의 깊게 읽고, 특히 7번째 포인트를 확인하세요.

## 송장 기반 접근 방식

첨부된 댓글을 기반으로 결제를 수락하려면 서비스는 다음을 수행해야 합니다.

1. `wallet` 컨트랙트를 배포합니다.
2. 각 사용자에게 고유한 `invoice`를 생성합니다. uuid32의 문자열 표현이면 충분합니다.
3. 사용자는 `invoice`를 댓글로 첨부하여 Toncoin을 서비스의 `wallet` 컨트랙트로 전송하도록 지시받아야 합니다.
4. 서비스는 `wallet` 컨트랙트에 대해 [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get) 메서드를 정기적으로 폴링해야 합니다.
5. 새로운 트랜잭션에 대해, 들어오는 메시지를 추출하고, `comment`를 데이터베이스와 일치시킨 후 **들어오는 메시지 값**을 사용자의 계정에 입금합니다.

메시지가 컨트랙트에 도달할 때 거래를 구문 분석하여 **들어오는 메시지 값**을 계산해야 합니다. 거래는 [getTransactions](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L268)으로 얻을 수 있습니다. 들어오는 지갑 거래의 경우 하나의 들어오는 메시지와 0개의 나가는 메시지로 구성된 데이터가 정확합니다. 그렇지 않으면 지갑에 외부 메시지가 전송되어 소유자가 Toncoin을 소비하거나, 지갑이 배포되지 않아 들어오는 트랜잭션이 반송됩니다.

어쨌든 일반적으로 메시지가 컨트랙트에 가져오는 금액은 들어오는 메시지의 값에서 나가는 메시지들의 값의 합계와 수수료를 뺀 값입니다: `value_{in_msg} - SUM(value_{out_msg}) - fee`. 기술적으로 거래 표현에는 `fee`라는 이름을 가진 세 가지 다른 필드가 있습니다: `fee`, `storage_fee`, 및 `other_fee`, 즉 총 수수료, 저장 비용과 관련된 수수료, 트랜잭션 처리와 관련된 수수료입니다. 첫 번째 것만 사용해야 합니다.

### TON Connect를 사용한 송장

여러 결제/트랜잭션을 세션 내에서 서명해야 하거나 지갑과의 연결을 일정 시간 유지해야 하는 dApp에 적합합니다.

- ✅ 지갑과의 영구적인 통신 채널, 사용자 주소 정보가 제공됩니다.

- ✅ 사용자는 QR 코드를 한 번만 스캔하면 됩니다.

- ✅ 사용자가 지갑에서 거래를 확인했는지 여부를 확인할 수 있으며, 반환된 BOC로 트랜잭션을 추적할 수 있습니다.

- ✅ 다양한 플랫폼용 SDK 및 UI 키트가 제공됩니다.

- ❌ 한 번의 결제만 필요하다면 사용자는 두 가지 작업을 해야 합니다: 지갑을 연결하고 트랜잭션을 확인합니다.

- ❌ 통합이 ton:// 링크보다 더 복잡합니다.

```mdx-code-block
<Button href="/develop/dapps/ton-connect/"
colorType="primary" sizeType={'lg'}>
```

자세히 알아보기

```mdx-code-block
</Button>
```

### ton:// 링크를 이용한 송장

:::warning
Ton 링크는 더 이상 사용되지 않으며, 사용을 피하는 것이 좋습니다.
:::

단순한 사용자 흐름을 위한 쉬운 통합이 필요할 경우, ton:// 링크를 사용하는 것이 적합합니다.
일회성 결제 및 송장에 가장 적합합니다.

```bash
ton://transfer/<destination-address>?
    [nft=<nft-address>&]
    [fee-amount=<nanocoins>&]
    [forward-amount=<nanocoins>] 
```

- ✅ 쉬운 통합

- ✅ 지갑을 연결할 필요가 없습니다.

- ❌ 각 결제마다 새로운 QR 코드를 스캔해야 합니다.

- ❌ 사용자가 트랜잭션을 서명했는지 여부를 추적할 수 없습니다.

- ❌ 사용자의 주소 정보가 없습니다.

- ❌ 그러한 링크를 클릭할 수 없는 플랫폼(예: Telegram 데스크톱 클라이언트에서 봇의 메시지)의 경우 우회 방법이 필요합니다.

[ton 링크에 대해 더 알아보기](https://github.com/tonkeeper/wallet-api#payment-urls)

## 탐색기

블록체인 탐색기는 https://tonscan.org입니다.

탐색기에서 트랜잭션 링크를 생성하려면, 서비스는 lt(논리 시간), 트랜잭션 해시, 계정 주소(계정 주소는 [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get) 메서드를 통해 얻은 lt와 txhash로 검색)를 얻어야 합니다. https://tonscan.org 및 https://explorer.toncoin.org는 다음 형식으로 해당 tx 페이지를 보여줄 수 있습니다:

`https://tonviewer.com/transaction/{txhash as base64url}`

`https://tonscan.org/tx/{lt as int}:{txhash as base64url}:{account address}`

`https://explorer.toncoin.org/transaction?account={account address}&lt={lt as int}&hash={txhash as base64url}`

## 모범 사례

### 지갑 생성

<Tabs groupId="example-create_wallet">
<TabItem value="JS" label="JS">

- **toncenter:**
  - [지갑 생성 + 지갑 주소 가져오기](https://github.com/toncenter/examples/blob/main/common.js)

- **ton-community/ton:**
  - [지갑 생성 + 잔액 확인](https://github.com/ton-community/ton#usage)

</TabItem>

<TabItem value="Go" label="Go">

- **xssnick/tonutils-go:**
  - [지갑 생성 + 잔액 확인](https://github.com/xssnick/tonutils-go?tab=readme-ov-file#wallet)

</TabItem>

<TabItem value="Python" label="Python">

- **psylopunk/pythonlib:**
  - [지갑 생성 + 지갑 주소 가져오기](https://github.com/psylopunk/pytonlib/blob/main/examples/generate_wallet.py)
- **yungwine/pytoniq:**

```py
import asyncio

from pytoniq.contract.wallets.wallet import WalletV4R2
from pytoniq.liteclient.balancer import LiteBalancer


async def main():
    provider = LiteBalancer.from_mainnet_config(2)
    await provider.start_up()

    mnemonics, wallet = await WalletV4R2.create(provider)
    print(f"{wallet.address=} and {mnemonics=}")

    await provider.close_all()


if __name__ == "__main__":
    asyncio.run(main())
```

</TabItem>

</Tabs>

### Toncoin 입금 (Toncoins 받기)

<Tabs groupId="example-toncoin_deposit">
<TabItem value="JS" label="JS">

- **toncenter:**
  - [토큰 입금 처리](https://github.com/toncenter/examples/blob/main/deposits.js)
  - [다중 지갑의 토큰 입금 처리](https://github.com/toncenter/examples/blob/main/deposits-multi-wallets.js)

</TabItem>

<TabItem value="Go" label="Go">

- **xssnick/tonutils-go:**

<details>
<summary>입금 확인</summary>

```go
package main 

import (
	"context"
	"encoding/base64"
	"log"

	"github.com/xssnick/tonutils-go/address"
	"github.com/xssnick/tonutils-go/liteclient"
	"github.com/xssnick/tonutils-go/ton"
)

const (
	num = 10
)

func main() {
	client := liteclient.NewConnectionPool()
	err := client.AddConnectionsFromConfigUrl(context.Background(), "https://ton.org/global.config.json")
	if err != nil {
		panic(err)
	}

	api := ton.NewAPIClient(client, ton.ProofCheckPolicyFast).WithRetry()

	accountAddr := address.MustParseAddr("0QA__NJI1SLHyIaG7lQ6OFpAe9kp85fwPr66YwZwFc0p5wIu")

	// we need fresh block info to run get methods
	b, err := api.CurrentMasterchainInfo(context.Background())
	if err != nil {
		log.Fatal(err)
	}

	// we use WaitForBlock to make sure block is ready,
	// it is optional but escapes us from liteserver block not ready errors
	res, err := api.WaitForBlock(b.SeqNo).GetAccount(context.Background(), b, accountAddr)
	if err != nil {
		log.Fatal(err)
	}

	lastTransactionId := res.LastTxHash
	lastTransactionLT := res.LastTxLT

	headSeen := false

	for {
		trxs, err := api.ListTransactions(context.Background(), accountAddr, num, lastTransactionLT, lastTransactionId)
		if err != nil {
			log.Fatal(err)
		}

		for i, tx := range trxs {
			// should include only first time lastTransactionLT
			if !headSeen {
				headSeen = true
			} else if i == 0 {
				continue
			}

			if tx.IO.In == nil || tx.IO.In.Msg.SenderAddr().IsAddrNone() {
				// external message should be omitted
				continue
			}

      if tx.IO.Out != nil {
				// no outgoing messages - this is incoming Toncoins
				continue
			}

			// process trx
			log.Printf("found in transaction hash %s", base64.StdEncoding.EncodeToString(tx.Hash))
		}

		if len(trxs) == 0 || (headSeen && len(trxs) == 1) {
			break
		}

		lastTransactionId = trxs[0].Hash
		lastTransactionLT = trxs[0].LT
	}
}
```

</details>
</TabItem>

<TabItem value="Python" label="Python">

- **yungwine/pytoniq:**

<summary>입금 확인</summary>

```python
import asyncio

from pytoniq_core import Transaction

from pytoniq import LiteClient, Address

MY_ADDRESS = Address("kf8zMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM_BP")


async def main():
    client = LiteClient.from_mainnet_config(ls_i=0, trust_level=2)

    await client.connect()

    last_block = await client.get_trusted_last_mc_block()

    _account, shard_account = await client.raw_get_account_state(MY_ADDRESS, last_block)
    assert shard_account

    last_trans_lt, last_trans_hash = (
        shard_account.last_trans_lt,
        shard_account.last_trans_hash,
    )

    while True:
        print(f"Waiting for{last_block=}")

        transactions = await client.get_transactions(
            MY_ADDRESS, 1024, last_trans_lt, last_trans_hash
        )
        toncoin_deposits = [tx for tx in transactions if filter_toncoin_deposit(tx)]
        print(f"Got {len(transactions)=} with {len(toncoin_deposits)=}")

        for deposit_tx in toncoin_deposits:
            # Process toncoin deposit transaction
            print(deposit_tx.cell.hash.hex())

        last_trans_lt = transactions[0].lt
        last_trans_hash = transactions[0].cell.hash


def filter_toncoin_deposit(tx: Transaction):
    if tx.out_msgs:
        return False

    if tx.in_msg:
        return False

    return True


if __name__ == "__main__":
    asyncio.run(main())
```

</TabItem>
</Tabs>

### Toncoin 출금 (Toncoins 보내기)

<Tabs groupId="example-toncoin_withdrawals">
<TabItem value="JS" label="JS">

- **toncenter:**
  - [지갑에서 Toncoins를 일괄 인출하기](https://github.com/toncenter/examples/blob/main/withdrawals-highload-batch.js)
  - [지갑에서 Toncoins 인출하기](https://github.com/toncenter/examples/blob/main/withdrawals-highload.js)

- **ton-community/ton:**
  - [지갑에서 Toncoins 인출하기](https://github.com/ton-community/ton#usage)

</TabItem>

<TabItem value="Go" label="Go">

- **xssnick/tonutils-go:**
  - [지갑에서 Toncoins 인출하기](https://github.com/xssnick/tonutils-go?tab=readme-ov-file#wallet)

</TabItem>

<TabItem value="Python" label="Python">

- **psylopunk/pythonlib:**
  - [지갑에서 Toncoins 인출하기](https://github.com/psylopunk/pytonlib/blob/main/examples/transactions.py)

- **yungwine/pytoniq:**

```python
import asyncio

from pytoniq_core import Address
from pytoniq.contract.wallets.wallet import WalletV4R2
from pytoniq.liteclient.balancer import LiteBalancer


MY_MNEMONICS = "one two tree ..."
DESTINATION_WALLET = Address("Destination wallet address")


async def main():
    provider = LiteBalancer.from_mainnet_config()
    await provider.start_up()

    wallet = await WalletV4R2.from_mnemonic(provider, MY_MNEMONICS)

    await wallet.transfer(DESTINATION_WALLET, 5)
    
    await provider.close_all()


if __name__ == "__main__":
    asyncio.run(main())
```

</TabItem>

</Tabs>

### 컨트랙트의 트랜잭션 가져오기

<Tabs groupId="example-get_transactions">
<TabItem value="JS" label="JS">

- **ton-community/ton:**
  - [getTransaction 메소드가 있는 클라이언트](https://github.com/ton-community/ton/blob/master/src/client/TonClient.ts)

</TabItem>

<TabItem value="Go" label="Go">

- **xssnick/tonutils-go:**
  - [트랜잭션 가져오기](https://github.com/xssnick/tonutils-go?tab=readme-ov-file#account-info-and-transactions)

</TabItem>

<TabItem value="Python" label="Python">

- **psylopunk/pythonlib:**
  - [트랜잭션 가져오기](https://github.com/psylopunk/pytonlib/blob/main/examples/transactions.py)
- **yungwine/pytoniq:**
  - [트랜잭션 가져오기](https://github.com/yungwine/pytoniq/blob/master/examples/transactions.py)

</TabItem>

</Tabs>

## SDKs

다양한 언어(JS, Python, Golang, C#, Rust 등)에 대한 SDK 목록은 [여기](/develop/dapps/apis/sdk)에서 확인할 수 있습니다.
