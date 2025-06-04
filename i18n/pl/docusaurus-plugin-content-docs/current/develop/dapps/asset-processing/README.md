import Button from '@site/src/components/button'
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Przetwarzanie płatności

Ta strona **wyjaśnia, jak przetwarzać** (wysyłać i akceptować) "aktywa cyfrowe" na blockchainie TON.
Opisuje **głównie** jak pracować z `monetami TON`, ale **część teoretyczna** jest **ważna**, nawet jeśli chcą Państwo przetwarzać tylko `jettony`.

## Inteligentny kontrakt portfela

Inteligentne kontrakty Wallet to kontrakty w sieci TON, których zadaniem jest umożliwienie podmiotom spoza łańcucha bloków interakcji z podmiotami łańcucha bloków. Ogólnie rzecz biorąc, rozwiązują one trzy wyzwania:

- uwierzytelnia właściciela: Odmawia przetwarzania i uiszczania opłat za wnioski osób niebędących właścicielami.
- Ochrona przed powtórzeniami: Zabrania powtarzalnego wykonywania jednego żądania, na przykład wysyłania aktywów do innego inteligentnego kontraktu.
- inicjuje dowolną interakcję z innymi inteligentnymi kontraktami.

Standardowym rozwiązaniem dla pierwszego wyzwania jest kryptografia klucza publicznego: `wallet` przechowuje klucz publiczny i sprawdza, czy przychodząca wiadomość z żądaniem jest podpisana odpowiednim kluczem prywatnym, który jest znany tylko właścicielowi.

Rozwiązanie trzeciego wyzwania jest również powszechne; ogólnie rzecz biorąc, żądanie zawiera w pełni uformowaną wewnętrzną wiadomość, którą `wallet` wysyła do sieci. Jednak w przypadku ochrony przed powtórkami istnieje kilka różnych podejść.

### Portfele oparte na sekwencji

Portfele oparte na Seqno stosują najprostsze podejście do sekwencjonowania wiadomości. Każda wiadomość ma specjalną liczbę całkowitą `seqno`, która musi pokrywać się z licznikiem przechowywanym w inteligentnym kontrakcie `wallet`. `wallet` aktualizuje swój licznik przy każdym żądaniu, zapewniając w ten sposób, że jedno żądanie nie zostanie przetworzone dwukrotnie. Istnieje kilka wersji `wallet`, które różnią się publicznie dostępnymi metodami: możliwość ograniczenia żądań według czasu wygaśnięcia oraz możliwość posiadania wielu portfeli z tym samym kluczem publicznym. Jednak nieodłącznym wymogiem tego podejścia jest wysyłanie żądań jedno po drugim, ponieważ każda luka w sekwencji `seqno` spowoduje niemożność przetworzenia wszystkich kolejnych żądań.

### Portfele o dużym obciążeniu

Ten typ `wallet` stosuje podejście oparte na przechowywaniu identyfikatora niewygasłych przetworzonych żądań w pamięci smart-contract. W tym podejściu każde żądanie jest sprawdzane pod kątem bycia duplikatem już przetworzonego żądania i, jeśli zostanie wykryta powtórka, jest odrzucane. Ze względu na wygaśnięcie, kontrakt może nie przechowywać wszystkich żądań na zawsze, ale usunie te, które nie mogą zostać przetworzone ze względu na limit wygaśnięcia. Żądania do tego "portfela" mogą być wysyłane równolegle bez zakłócania siebie nawzajem; jednak takie podejście wymaga bardziej zaawansowanego monitorowania przetwarzania żądań.

### Wdrożenie portfela

Aby wdrożyć portfel za pośrednictwem TonLib, należy:

1. Proszę wygenerować parę kluczy prywatny/publiczny za pomocą funkcji [createNewKey](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L244) lub jej funkcji opakowujących (przykład w [tonlib-go](https://github.com/mercuryoio/tonlib-go/tree/master/v2#create-new-private-key)). Proszę zauważyć, że klucz prywatny jest generowany lokalnie i nie opuszcza komputera hosta.
2. Formularz [InitialAccountWallet](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L62) struktury odpowiadającej jednemu z włączonych `wallets`. Obecnie dostępne są `wallet.v3`, `wallet.v4`, `wallet.highload.v1`, `wallet.highload.v2`.
3. Proszę obliczyć adres nowego inteligentnego kontraktu `wallet` za pomocą metody [getAccountAddress](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L283). Zalecamy użycie domyślnej wersji `0`, a także wdrożenie portfeli w łańcuchu bazowym `workchain=0` w celu obniżenia opłat za przetwarzanie i przechowywanie.
4. Proszę wysłać Toncoin na obliczony adres. Proszę zauważyć, że należy wysłać je w trybie `non-bounce`, ponieważ ten adres nie ma jeszcze kodu, a zatem nie może przetwarzać przychodzących wiadomości. Flaga `non-bounce` wskazuje, że nawet jeśli przetwarzanie nie powiedzie się, pieniądze nie powinny zostać zwrócone z wiadomością bounce. Nie zalecamy używania flagi `non-bounce` w innych transakcjach, szczególnie w przypadku dużych kwot, ponieważ mechanizm bounce zapewnia pewien stopień ochrony przed błędami.
5. Proszę utworzyć żądaną [akcję](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L154), na przykład `actionNoop` tylko do wdrożenia. Następnie proszę użyć [createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L292) i [sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L300), aby zainicjować interakcję z blockchainem.
6. Proszę sprawdzić umowę w ciągu kilku sekund za pomocą metody [getAccountState](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L288).

:::tip
Proszę przeczytać więcej w [Wallet Tutorial] (/develop/smart-contracts/tutorials/wallet#-deploying-a-wallet).
:::

### Proszę sprawdzić ważność adresu portfela

Większość zestawów SDK wymusza weryfikację adresu (większość weryfikuje go podczas tworzenia portfela lub procesu przygotowywania transakcji), więc zazwyczaj nie wymaga to od użytkownika żadnych dodatkowych skomplikowanych kroków.

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
Pełny opis adresu na stronie [Smart Contract Addresses](/learn/overviews/addresses).
:::

## Praca z transferami

### Proszę sprawdzić transakcje kontraktu

Transakcje kontraktu można uzyskać za pomocą [getTransactions](https://toncenter.com/api/v2/#/accounts/get_transactions_getTransactions_get). Metoda ta pozwala uzyskać 10 transakcji od pewnego `last_transaction_id` i wcześniejszych. Aby przetworzyć wszystkie przychodzące transakcje, należy wykonać następujące kroki:

1. Najnowszy `last_transaction_id` można uzyskać za pomocą [getAddressInformation](https://toncenter.com/api/v2/#/accounts/get_address_information_getAddressInformation_get).
2. Lista 10 transakcji powinna zostać załadowana za pomocą metody `getTransactions`.
3. Przetwarzanie transakcji z niepustym źródłem w wiadomości przychodzącej i miejscem docelowym równym adresowi konta.
4. Należy wczytać kolejne 10 transakcji i powtarzać kroki 2,3,4,5 aż do przetworzenia wszystkich przychodzących transakcji.

### Proszę pobrać transakcje przychodzące/wychodzące

Możliwe jest śledzenie przepływu wiadomości podczas przetwarzania transakcji. Ponieważ przepływ wiadomości jest DAG, wystarczy pobrać bieżącą transakcję za pomocą metody [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get) i znaleźć transakcję przychodzącą przez `out_msg` za pomocą [tryLocateResultTx](https://testnet.toncenter.com/api/v2/#/transactions/get_try_locate_result_tx_tryLocateResultTx_get) lub transakcje wychodzące przez `in_msg` za pomocą [tryLocateSourceTx](https://testnet.toncenter.com/api/v2/#/transactions/get_try_locate_source_tx_tryLocateSourceTx_get).

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

### Proszę wysyłać płatności

1. Usługa powinna wdrożyć "portfel" i utrzymywać go w stanie finansowania, aby zapobiec zniszczeniu kontraktu z powodu opłat za przechowywanie. Proszę zauważyć, że opłaty za przechowywanie są zazwyczaj niższe niż 1 Toncoin rocznie.
2. Usługa powinna otrzymać od użytkownika `destination_address` i opcjonalnie `comment`. Proszę zauważyć, że w międzyczasie zalecamy zakazanie niedokończonych płatności wychodzących z tym samym zestawem (`destination_address`, `value`, `comment`) lub odpowiednie zaplanowanie tych płatności; w ten sposób następna płatność zostanie zainicjowana dopiero po potwierdzeniu poprzedniej.
3. Formularz [msg.dataText](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L103) z `komentarzem` jako tekstem.
4. Formularz [msg.message](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L113), który zawiera `destination_address`, pusty `public_key`, `amount` i `msg.dataText`.
5. Formularz [Action](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L154) zawierający zestaw wiadomości wychodzących.
6. Do wysyłania płatności wychodzących proszę używać zapytań [createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L292) i [sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L300).
7. Usługa powinna regularnie sprawdzać metodę [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get) dla kontraktu `wallet`. Dopasowanie potwierdzonych transakcji do wychodzących płatności według (`destination_address`, `value`, `comment`) pozwala oznaczyć płatności jako zakończone; wykryć i pokazać użytkownikowi odpowiedni hash transakcji i lt (czas logiczny).
8. Żądania do `v3` portfeli `high-load` mają domyślnie czas wygaśnięcia równy 60 sekund. Po tym czasie nieprzetworzone żądania mogą być bezpiecznie ponownie wysłane do sieci (proszę zobaczyć kroki 3-6).

### Proszę pobrać identyfikator transakcji

Może być niejasne, że aby uzyskać więcej informacji na temat transakcji, użytkownik musi przeskanować blockchain za pomocą funkcji [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get).
Niemożliwe jest pobranie identyfikatora transakcji natychmiast po wysłaniu wiadomości, ponieważ transakcja musi najpierw zostać potwierdzona przez sieć blockchain.
Aby zrozumieć wymagany potok, proszę uważnie przeczytać [Wyślij płatności] (https://docs.ton.org/develop/dapps/asset-processing/#send-payments), zwłaszcza punkt 7.

## Podejście oparte na fakturach

Aby akceptować płatności na podstawie załączonych komentarzy, usługa powinna

1. Proszę wdrożyć kontrakt `wallet`.
2. Proszę wygenerować unikalną `fakturę` dla każdego użytkownika. Wystarczy ciąg znaków reprezentujący uuid32.
3. Użytkownicy powinni zostać poinstruowani, aby wysłać Toncoin do umowy "portfela" usługi z załączoną "fakturą" jako komentarzem.
4. Usługa powinna regularnie sprawdzać metodę [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get) dla kontraktu `wallet`.
5. W przypadku nowych transakcji, przychodząca wiadomość powinna zostać wyodrębniona, `komentarz` dopasowany do bazy danych, a **wartość przychodzącej wiadomości** zdeponowana na koncie użytkownika.

Aby obliczyć **wartość przychodzącej wiadomości**, którą wiadomość wnosi do umowy, należy przeanalizować transakcję. Dzieje się tak, gdy wiadomość trafia do kontraktu. Transakcję można uzyskać za pomocą [getTransactions](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L268). W przypadku przychodzącej transakcji portfela prawidłowe dane składają się z jednej wiadomości przychodzącej i zero wiadomości wychodzących. W przeciwnym razie albo wiadomość zewnętrzna zostanie wysłana do portfela, w którym to przypadku właściciel wyda Toncoin, albo portfel nie zostanie wdrożony, a transakcja przychodząca zostanie odrzucona.

W każdym razie, ogólnie rzecz biorąc, kwota, którą wiadomość wnosi do kontraktu może być obliczona jako wartość wiadomości przychodzącej minus suma wartości wiadomości wychodzących minus opłata: `value_{in_msg} - SUM(value_{out_msg}) - fee`. Technicznie, reprezentacja transakcji zawiera trzy różne pola z `fee` w nazwie: `fee`, `storage_fee` i `other_fee`, czyli całkowitą opłatę, część opłaty związaną z kosztami przechowywania i część opłaty związaną z przetwarzaniem transakcji. Tylko pierwsza z nich powinna być używana.

### Faktury z TON Connect

Najlepiej nadaje się do aplikacji dApps, które muszą podpisywać wiele płatności/transakcji w ramach sesji lub muszą utrzymywać połączenie z portfelem przez pewien czas.

- ✅ Istnieje stały kanał komunikacji z portfelem, informacje o adresie użytkownika

- Użytkownicy muszą zeskanować kod QR tylko raz.

- ✅ Możliwe jest sprawdzenie, czy użytkownik potwierdził transakcję w portfelu, śledzenie transakcji przez zwrócony BOC

- Gotowe zestawy SDK i UI są dostępne dla różnych platform.

- Jeśli wystarczy wysłać tylko jedną płatność, użytkownik musi wykonać dwie czynności: połączyć portfel i potwierdzić transakcję.

- Integracja jest bardziej złożona niż link ton://

```mdx-code-block
<Button href="/develop/dapps/ton-connect/"
colorType="primary" sizeType={'lg'}>
```

Proszę dowiedzieć się więcej

```mdx-code-block
</Button>
```

### Faktury z linkiem ton://

:::warning
Ton link jest przestarzały, proszę go nie używać
:::

Jeśli potrzebują Państwo łatwej integracji dla prostego przepływu użytkowników, odpowiednie jest użycie łącza ton://.
Najlepiej nadaje się do jednorazowych płatności i faktur.

```bash
ton://transfer/<destination-address>?
    [nft=<nft-address>&]
    [fee-amount=<nanocoins>&]
    [forward-amount=<nanocoins>] 
```

- Łatwa integracja

- Nie ma potrzeby podłączania portfela

- Użytkownicy muszą zeskanować nowy kod QR dla każdej płatności.

- Nie jest możliwe śledzenie, czy użytkownik podpisał transakcję, czy nie.

- Brak informacji o adresie użytkownika

- Obejścia są potrzebne na platformach, na których takie linki nie są klikalne (np. wiadomości od botów dla klientów Telegram na komputery stacjonarne).

[Więcej informacji na temat ton linków tutaj](https://github.com/tonkeeper/wallet-api#payment-urls)

## Odkrywcy

Eksplorator blockchain to https://tonscan.org.

Aby wygenerować link do transakcji w eksploratorze, usługa musi uzyskać lt (czas logiczny), hash transakcji i adres konta (adres konta, dla którego lt i txhash zostały pobrane za pomocą metody [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get)). https://tonscan.org i https://explorer.toncoin.org/ mogą następnie wyświetlać stronę dla tego tx w następującym formacie:

`https://tonviewer.com/transaction/{txhash as base64url}`

`https://tonscan.org/tx/{lt as int}:{txhash as base64url}:{account address}`

`https://explorer.toncoin.org/transaction?account={account address}&lt={lt as int}&hash={txhash as base64url}`

## Najlepsze praktyki

### Tworzenie portfela

<Tabs groupId="example-create_wallet">
<TabItem value="JS" label="JS">

- **toncenter:**
  - [Utworzenie portfela + pobranie adresu portfela](https://github.com/toncenter/examples/blob/main/common.js)

- **ton-community/ton:**
  - [Utworzenie portfela + uzyskanie salda](https://github.com/ton-community/ton#usage)

</TabItem>

<TabItem value="Go" label="Go">

- **xssnick/tonutils-go:**.
  - [Utworzenie portfela + uzyskanie salda](https://github.com/xssnick/tonutils-go?tab=readme-ov-file#wallet)

</TabItem>

<TabItem value="Python" label="Python">

- **psylopunk/pythonlib:**
  - [Utworzenie portfela + pobranie adresu portfela](https://github.com/psylopunk/pytonlib/blob/main/examples/generate_wallet.py)
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

### Depozyty toncoinów (Zdobądź toncoiny)

<Tabs groupId="example-toncoin_deposit">
<TabItem value="JS" label="JS">

- **toncenter:**
  - [Przetwórz depozyt Toncoins](https://github.com/toncenter/examples/blob/main/deposits.js)
  - [Przetwarzaj wpłaty Toncoins w wielu portfelach] (https://github.com/toncenter/examples/blob/main/deposits-multi-wallets.js)

</TabItem>

<TabItem value="Go" label="Go">

- **xssnick/tonutils-go:**.

<details>
<summary>Depozyty czekowe</summary>

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

<summary>Depozyty czekowe</summary>

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

### Wypłaty toncoinów (proszę wysłać toncoiny)

<Tabs groupId="example-toncoin_withdrawals">
<TabItem value="JS" label="JS">

- **toncenter:**
  - [Wypłacanie toncoinów z portfela partiami](https://github.com/toncenter/examples/blob/main/withdrawals-highload-batch.js)
  - [Wypłata toncoinów z portfela](https://github.com/toncenter/examples/blob/main/withdrawals-highload.js)

- **ton-community/ton:**
  - [Wypłata toncoinów z portfela](https://github.com/ton-community/ton#usage)

</TabItem>

<TabItem value="Go" label="Go">

- **xssnick/tonutils-go:**.
  - [Wypłata toncoinów z portfela](https://github.com/xssnick/tonutils-go?tab=readme-ov-file#wallet)

</TabItem>

<TabItem value="Python" label="Python">

- **psylopunk/pythonlib:**
  - [Wypłata toncoinów z portfela](https://github.com/psylopunk/pytonlib/blob/main/examples/transactions.py)

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

### Proszę pobrać transakcje kontraktu

<Tabs groupId="example-get_transactions">
<TabItem value="JS" label="JS">

- **ton-community/ton:**
  - [Klient z metodą getTransaction](https://github.com/ton-community/ton/blob/master/src/client/TonClient.ts)

</TabItem>

<TabItem value="Go" label="Go">

- **xssnick/tonutils-go:**.
  - [Proszę pobrać transakcje](https://github.com/xssnick/tonutils-go?tab=readme-ov-file#account-info-and-transactions)

</TabItem>

<TabItem value="Python" label="Python">

- **psylopunk/pythonlib:**
  - [Proszę pobrać transakcje](https://github.com/psylopunk/pytonlib/blob/main/examples/transactions.py)
- **yungwine/pytoniq:**
  - [Proszę pobrać transakcje](https://github.com/yungwine/pytoniq/blob/master/examples/transactions.py)

</TabItem>

</Tabs>

## SDK

Listę zestawów SDK dla różnych języków (JS, Python, Golang, C#, Rust itp.) można znaleźć [tutaj] (/develop/dapps/apis/sdk).
