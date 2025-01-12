import Button from '@site/src/components/button'
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Обробка платежів

Ця сторінка пояснює, як обробляти\*\* (відправляти і приймати) "цифрові активи" в блокчейні TON.
В основному тут описано, як працювати з монетами TON, але теоретична частина важлива, навіть якщо ви хочете обробляти тільки джеттони.

## Смарт-контракт гаманця

Смарт-контракти гаманців - це контракти в мережі TON, які слугують для того, щоб дозволити суб'єктам за межами блокчейну взаємодіяти з об'єктами блокчейну. Загалом, вони вирішують три завдання:

- аутентифікує власника: Відмовляється обробляти та сплачувати збори за запити невласників.
- захист від повторів: Забороняє повторне виконання одного запиту, наприклад, надсилання активів іншому смарт-контракту.
- ініціює довільну взаємодію з іншими смарт-контрактами.

Стандартним рішенням для першої проблеми є криптографія з відкритим ключем: "гаманець" зберігає відкритий ключ і перевіряє, що вхідне повідомлення із запитом підписане відповідним закритим ключем, який відомий лише власнику.

Вирішення третьої проблеми також є поширеним: зазвичай запит містить повністю сформоване внутрішнє повідомлення, яке "гаманець" надсилає в мережу. Однак, для захисту від повторного відтворення існує декілька різних підходів.

### Гаманці на основі Seqno

Гаманці на основі Seqno використовують найпростіший підхід до впорядкування повідомлень. Кожне повідомлення має спеціальне ціле число `seqno`, яке повинно збігатися з лічильником, що зберігається в смарт-контракті `гаманця`. Гаманець оновлює свій лічильник при кожному запиті, таким чином гарантуючи, що один запит не буде оброблений двічі. Існує кілька версій "гаманця", які відрізняються загальнодоступними методами: можливість обмежувати запити за часом дії та можливість мати кілька гаманців з одним і тим же публічним ключем. Однак, невід'ємною вимогою такого підходу є надсилання запитів по одному, оскільки будь-яка прогалина в послідовності `seqno` призведе до неможливості обробки всіх наступних запитів.

### Гаманці з високим навантаженням

Цей тип "гаманця" використовує підхід, заснований на зберіганні ідентифікатора оброблених запитів, термін дії яких не закінчився, у сховищі смарт-контрактів. У цьому підході будь-який запит перевіряється на наявність дублікату вже обробленого запиту і, якщо виявлено повторення, відхиляється. Через закінчення терміну дії контракт не може зберігати всі запити вічно, але він буде видаляти ті, які не можуть бути оброблені через обмеження терміну дії. Запити до цього "гаманця" можуть надсилатися паралельно, не заважаючи один одному, але такий підхід вимагає більш складного моніторингу обробки запитів.

### Розгортання гаманця

Для розгортання гаманця через TonLib потрібно зробити наступне:

1. Згенеруйте пару приватний/відкритий ключ за допомогою [createNewKey](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L244) або його функцій-обгорток (приклад у [tonlib-go](https://github.com/mercuryoio/tonlib-go/tree/master/v2#create-new-private-key)). Зверніть увагу, що приватний ключ генерується локально і не залишає хост-машину.
2. Сформуйте структуру [InitialAccountWallet](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L62), що відповідає одному з увімкнених `гаманців`. Наразі доступні `wallet.v3`, `wallet.v4`, `wallet.highload.v1`, `wallet.highload.v2`.
3. Обчисліть адресу нового смарт-контракту `гаманця` за допомогою методу [getAccountAddress](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L283). Ми рекомендуємо використовувати ревізію за замовчуванням `0`, а також розгортати гаманці в базовому ланцюжку `workchain=0` для зниження витрат на обробку та зберігання.
4. Надішліть трохи Toncoin на розраховану адресу. Зверніть увагу, що ви повинні відправити їх в режимі `non-bounce`, оскільки ця адреса ще не має коду і не може обробляти вхідні повідомлення. Прапорець `non-bounce` вказує на те, що навіть у разі невдалої обробки, гроші не повинні повертатися з повідомленням про відмову. Ми не рекомендуємо використовувати прапорець `non-bounce` для інших транзакцій, особливо при переказі великих сум, оскільки механізм відмов забезпечує певний захист від помилок.
5. Сформуйте потрібну [action](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L154), наприклад, `actionNoop` тільки для розгортання. Потім використовуйте [createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L292) і [sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L300), щоб ініціювати взаємодію з блокчейном.
6. Перевірте контракт за кілька секунд за допомогою методу [getAccountState](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L288).

:::tip
Дізнайтеся більше в [Навчальному посібнику з гаманця] (/develop/smart-contracts/tutorials/wallet#-deploying-a-wallet)
:::

### Перевірте дійсність адреси гаманця

Більшість SDK вимагають верифікації адреси (більшість перевіряє її під час створення гаманця або підготовки транзакції), тому, як правило, це не вимагає від вас ніяких додаткових складних кроків.

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
Повний опис адрес на сторінці [Адреси смарт-контрактів](/learn/overviews/addresses).
:::

## Робота з переказами

### Перевірте транзакції за контрактом

Транзакції контракту можна отримати за допомогою [getTransactions](https://toncenter.com/api/v2/#/accounts/get_transactions_getTransactions_get). Цей метод дозволяє отримати 10 транзакцій, починаючи з деякого `last_transaction_id` і раніше. Щоб обробити всі отримані транзакції, слід виконати наступні кроки:

1. Останній `last_transaction_id` можна отримати за допомогою [getAddressInformation](https://toncenter.com/api/v2/#/accounts/get_address_information_getAddressInformation_get)
2. Список з 10 транзакцій повинен бути завантажений за допомогою методу `getTransactions`.
3. Обробляти транзакції з не порожнім джерелом у вхідному повідомленні та призначенням, що дорівнює адресі акаунта.
4. Завантажте наступні 10 транзакцій і повторіть кроки 2,3,4,5, поки не обробите всі вхідні транзакції.

### Отримуйте вхідні/вихідні транзакції

Під час обробки транзакцій можна відстежувати потік повідомлень. Оскільки потік повідомлень є DAG, достатньо отримати поточну транзакцію методом [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get) і знайти вхідну транзакцію за `out_msg` за допомогою [tryLocateResultTx](https://testnet.toncenter.com/api/v2/#/transactions/get_try_locate_result_tx_tryLocateResultTx_get) або вихідну за `in_msg` за допомогою [tryLocateSourceTx](https://testnet.toncenter.com/api/v2/#/transactions/get_try_locate_source_tx_tryLocateSourceTx_get).

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

### Надсилайте платежі

1. Сервіс повинен розгорнути "гаманець" і підтримувати його фінансування, щоб запобігти розірванню контракту через плату за зберігання. Зауважте, що плата за зберігання зазвичай становить менше 1 тонкоїна на рік.
2. Сервіс повинен отримувати від користувача `адреса_призначення` та необов'язковий `коментар`. Зауважте, що поки що ми рекомендуємо або заборонити незавершені вихідні платежі з однаковим набором (`адреса_призначення`, `вартість`, `коментар`), або правильно розпланувати ці платежі - так, щоб наступний платіж ініціювався лише після підтвердження попереднього.
3. Сформуйте [msg.dataText](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L103) з `comment` як текстом.
4. Сформуйте [msg.message](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L113), що містить `адресу_одержувача`, порожній `публічний_ключ`, `суму` та `msg.dataText`.
5. Форма [Дія](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L154), яка містить набір вихідних повідомлень.
6. Для відправки вихідних платежів використовуйте запити [createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L292) та [sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L300).
7. Сервіс повинен регулярно опитувати метод [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get) для контракту `гаманця`. Зіставлення підтверджених транзакцій з вихідними платежами за (`адреса_призначення`, `вартість`, `коментар`) дозволяє позначати платежі як завершені; визначати та показувати користувачеві відповідний хеш транзакції та lt (логічний час).
8. Запити до `v3` гаманців з високим навантаженням за замовчуванням мають термін дії, що дорівнює 60 секундам. Після закінчення цього часу необроблені запити можуть бути безпечно відправлені в мережу (див. кроки 3-6).

### Отримати ідентифікатор транзакції

Може бути незрозуміло, що для отримання додаткової інформації про транзакцію користувач повинен просканувати блокчейн за допомогою функції [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get).
Неможливо отримати ідентифікатор транзакції одразу після відправлення повідомлення, оскільки транзакція повинна бути підтверджена мережею блокчейн.
Щоб зрозуміти необхідний конвеєр, уважно прочитайте [Send payments](https://docs.ton.org/develop/dapps/asset-processing/#send-payments), особливо 7-й пункт.

## Підхід на основі рахунків-фактур

Щоб приймати платежі на основі прикріплених коментарів, сервіс повинен

1. Розгорніть контракт "гаманця".
2. Згенеруйте унікальний `invoice` для кожного користувача. Рядкового представлення uuid32 буде достатньо.
3. Користувачам слід проінструктувати, щоб вони надсилали Toncoin на контракт "гаманця" сервісу з прикріпленим "рахунком-фактурою" в якості коментаря.
4. Сервіс повинен регулярно опитувати метод [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get) для контракту `гаманця`.
5. Для нових транзакцій вхідне повідомлення має бути витягнуто, `коментар` перевірено за базою даних, а **значення вхідного повідомлення** занесено до облікового запису користувача.

Щоб обчислити **значення вхідного повідомлення**, яке повідомлення приносить контракту, потрібно розібрати транзакцію. Це відбувається, коли повідомлення потрапляє в контракт. Транзакцію можна отримати за допомогою [getTransactions](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L268). Для вхідної транзакції гаманця правильні дані складаються з одного вхідного повідомлення і нуля вихідних повідомлень. В іншому випадку, або на гаманець надсилається зовнішнє повідомлення, і тоді власник витрачає Toncoin, або гаманець не розгортається і вхідна транзакція повертається назад.

Так чи інакше, в загальному випадку суму, яку приносить повідомлення в контракт, можна розрахувати як вартість вхідного повідомлення мінус сума вартостей вихідних повідомлень мінус комісія: `value_{in_msg} - SUM(value_{out_msg}) - fee`. Технічно представлення транзакції містить три різних поля з `fee` в назві: `fee`, `storage_fee` та `other_fee`, тобто загальну комісію, частину комісії, пов'язану з витратами на зберігання, та частину комісії, пов'язану з обробкою транзакції. Використовувати слід тільки першу з них.

### Інвойси з TON Connect

Найкраще підходить для dApps, яким потрібно підписувати кілька платежів/транзакцій протягом сесії або підтримувати з'єднання з гаманцем протягом певного часу.

- ✅ Є постійний канал зв'язку з гаманцем, інформація про адресу користувача

- ✅ Користувачам потрібно відсканувати QR-код лише один раз

- ✅ Можна дізнатися, чи підтвердив користувач транзакцію в гаманці, відстежити транзакцію за поверненою BOC

- ✅ Готові SDK та набори інтерфейсів доступні для різних платформ

- ❌ Якщо потрібно відправити лише один платіж, користувачеві потрібно виконати дві дії: підключити гаманець і підтвердити транзакцію

- ❌ Інтеграція складніша, ніж посилання ton://

```mdx-code-block
<Button href="/develop/dapps/ton-connect/"
colorType="primary" sizeType={'lg'}>
```

Дізнатися більше

```mdx-code-block
</Button>
```

### Інвойси з посиланням ton://

:::warning
Посилання Ton застаріле, не використовуйте його
:::

Якщо вам потрібна легка інтеграція для простого потоку користувачів, підійде посилання ton://.
Найкраще підходить для одноразових платежів та інвойсів.

```bash
ton://transfer/<destination-address>?
    [nft=<nft-address>&]
    [fee-amount=<nanocoins>&]
    [forward-amount=<nanocoins>] 
```

- ✅ Легка інтеграція

- ✅ Не потрібно підключати гаманець

- ❌ Користувачі повинні сканувати новий QR-код для кожного платежу

- ❌ Неможливо відстежити, чи підписав користувач транзакцію чи ні

- ❌ Немає інформації про адресу користувача

- ❌ Обхідні шляхи потрібні на платформах, де такі посилання не можна натискати (наприклад, повідомлення від ботів для десктопних клієнтів Telegram)

[Дізнайтеся більше про тонни посилань тут] (https://github.com/tonkeeper/wallet-api#payment-urls)

## Дослідники

Дослідник блокчейну - https://tonscan.org.

Щоб згенерувати посилання на транзакцію в провіднику, сервіс має отримати lt (логічний час), хеш транзакції та адресу акаунта (адресу акаунта, для якого lt і txhash було отримано за допомогою методу [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get)). https://tonscan.org і https://explorer.toncoin.org/ можуть показати сторінку для цього tx у наступному форматі:

`https://tonviewer.com/transaction/{txhash as base64url}`

`https://tonscan.org/tx/{lt as int}:{txhash as base64url}:{account address}`

`https://explorer.toncoin.org/transaction?account={account address}&lt={lt as int}&hash={txhash as base64url}`.

## Найкращі практики

### Створення гаманця

<Tabs groupId="example-create_wallet">
<TabItem value="JS" label="JS">

- **toncenter:**
  - [Створення гаманця + отримання адреси гаманця](https://github.com/toncenter/examples/blob/main/common.js)

- **тон-спільнота/тон:**.
  - [Створення гаманця + отримання балансу](https://github.com/ton-community/ton#usage)

</TabItem>

<TabItem value="Go" label="Go">

- **xssnick/tonutils-go:**
  - [Створення гаманця + отримання балансу](https://github.com/xssnick/tonutils-go?tab=readme-ov-file#wallet)

</TabItem>

<TabItem value="Python" label="Python">

- **psylopunk/pythonlib:**
  - [Створення гаманця + отримання адреси гаманця](https://github.com/psylopunk/pytonlib/blob/main/examples/generate_wallet.py)
- **юнгвин/пітонік:**

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

### Депозити в тонкоїнах (отримати тонкоїни)

<Tabs groupId="example-toncoin_deposit">
<TabItem value="JS" label="JS">

- **toncenter:**
  - [Обробка депозиту Toncoins](https://github.com/toncenter/examples/blob/main/deposits.js)
  - [Процес поповнення мультигаманців Toncoins](https://github.com/toncenter/examples/blob/main/deposits-multi-wallets.js)

</TabItem>

<TabItem value="Go" label="Go">

- **xssnick/tonutils-go:**

<details>
<summary>Перевірка депозитів</summary>

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

- **юнгвин/пітонік:**

<summary>Перевірка депозитів</summary>

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

### Виведення токенів (надсилання токенів)

<Tabs groupId="example-toncoin_withdrawals">
<TabItem value="JS" label="JS">

- **toncenter:**
  - [Виводьте тонкоїни з гаманця партіями](https://github.com/toncenter/examples/blob/main/withdrawals-highload-batch.js)
  - [Вивести тонкоїни з гаманця](https://github.com/toncenter/examples/blob/main/withdrawals-highload.js)

- **тон-спільнота/тон:**.
  - [Вивести тонкоїни з гаманця](https://github.com/ton-community/ton#usage)

</TabItem>

<TabItem value="Go" label="Go">

- **xssnick/tonutils-go:**
  - [Вивести тонкоїни з гаманця](https://github.com/xssnick/tonutils-go?tab=readme-ov-file#wallet)

</TabItem>

<TabItem value="Python" label="Python">

- **psylopunk/pythonlib:**
  - [Вивести тонкоїни з гаманця](https://github.com/psylopunk/pytonlib/blob/main/examples/transactions.py)

- **юнгвин/пітонік:**

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

### Отримуйте транзакції за контрактом

<Tabs groupId="example-get_transactions">
<TabItem value="JS" label="JS">

- **тон-спільнота/тон:**.
  - [Клієнт з методом getTransaction](https://github.com/ton-community/ton/blob/master/src/client/TonClient.ts)

</TabItem>

<TabItem value="Go" label="Go">

- **xssnick/tonutils-go:**
  - [Отримати транзакції](https://github.com/xssnick/tonutils-go?tab=readme-ov-file#account-info-and-transactions)

</TabItem>

<TabItem value="Python" label="Python">

- **psylopunk/pythonlib:**
  - [Отримати транзакції](https://github.com/psylopunk/pytonlib/blob/main/examples/transactions.py)
- **юнгвин/пітонік:**
  - [Отримати транзакції](https://github.com/yungwine/pytoniq/blob/master/examples/transactions.py)

</TabItem>

</Tabs>

## SDK

Список SDK для різних мов (JS, Python, Golang, C#, Rust і т.д.) можна знайти [тут](/develop/dapps/apis/sdk).
