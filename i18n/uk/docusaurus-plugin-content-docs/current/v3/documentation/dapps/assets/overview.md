import Feedback from '@site/src/components/Feedback';

import Button from '@site/src/components/button'
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Asset processing overview

Here you can find a **short overview** on [how TON transfers work](/v3/documentation/dapps/assets/overview#overview-on-messages-and-transactions), what [asset types](/v3/documentation/dapps/assets/overview#digital-asset-types-on-ton) can you find in TON (and what about will you read [next](/v3/documentation/dapps/assets/overview#read-next)) and how to [interact with ton](/v3/documentation/dapps/assets/overview#interaction-with-ton-blockchain) using your programming language, it's recommended to understand all information, discovered below, before going to the next pages.

## Огляд повідомлень і транзакцій

Embodying a fully asynchronous approach, TON Blockchain involves a few concepts which are uncommon to traditional blockchains. Particularly, each interaction of any actor with the blockchain consists of a graph of asynchronously transferred [messages](/v3/documentation/smart-contracts/message-management/messages-and-transactions) between smart contracts and/or the external world. Each transaction consists of one incoming message and up to 255 outgoing messages.

There are 3 types of messages, that are fully described [here](/v3/documentation/smart-contracts/message-management/sending-messages#types-of-messages). To put it briefly:

- [external message](/v3/documentation/smart-contracts/message-management/external-messages):
  - "Зовнішнє повідомлення" (іноді його називають просто "зовнішнє повідомлення") - це повідомлення, яке надсилається з *зовні* блокчейну до смарт-контракту *всередині* блокчейну.
  - "Зовнішнє вихідне повідомлення" (зазвичай його називають "повідомленням журналу") надсилається від *суб'єкта блокчейну* до *зовнішнього світу*.
- [internal message](/v3/documentation/smart-contracts/message-management/internal-messages) is sent from one *blockchain entity* to *another*, can carry some amount of digital assets and arbitrary portion of data.

Загальний шлях будь-якої взаємодії починається із зовнішнього повідомлення, надісланого до смарт-контракту "гаманця", який аутентифікує відправника повідомлення за допомогою криптографії з відкритим ключем, бере на себе оплату комісії та надсилає внутрішні блокчейн-повідомлення. Ця черга повідомлень утворює орієнтований ациклічний граф, або дерево.

Наприклад:

![](/img/docs/asset-processing/alicemsgDAG.svg)

- "Аліса" використовує, наприклад, [Tonkeeper] (https://tonkeeper.com/), щоб відправити "зовнішнє повідомлення" на свій гаманець.
- `external message` is the input message for `wallet A v4` contract with empty source (a message from nowhere, such as [Tonkeeper](https://tonkeeper.com/)).
- вихідне повідомлення" - це вихідне повідомлення для контракту "гаманець A v4" і вхідне повідомлення для контракту "гаманець B v4" з джерелом "гаманець A v4" і призначенням "гаманець B v4".

В результаті маємо 2 транзакції з їх набором вхідних та вихідних повідомлень.

Each action, when contract take message as input (triggered by it), process it and generate or not generate outgoing messages as output, called `transaction`. Read more about transactions [here](/v3/documentation/smart-contracts/message-management/messages-and-transactions#what-is-a-transaction).

Ці "транзакції" можуть охоплювати **тривалий період часу**. Технічно, транзакції з чергами повідомлень агрегуються в блоки, які обробляються валідаторами. Асинхронна природа TON Blockchain **не дозволяє передбачити хеш і lt (логічний час) транзакції** на етапі відправлення повідомлення.

Прийнята до блоку "транзакція" є остаточною і не може бути змінена.

:::info Підтвердження транзакції
Транзакції TON є незворотними після одного підтвердження. Для кращого користувацького досвіду рекомендується уникати очікування додаткових блоків після завершення транзакцій в блокчейні TON. Детальніше читайте в [Catchain.pdf] (https://docs.ton.org/catchain.pdf#page=3).
:::

Smart contracts pay several types of [fees](/v3/documentation/smart-contracts/transaction-fees/fees) for transactions (usually from the balance of an incoming message, behavior depends on [message mode](/v3/documentation/smart-contracts/message-management/sending-messages#message-modes)). Amount of fees depends on workchain configs with maximal fees on `masterchain` and substantially lower fees on `basechain`.

## Типи цифрових активів на TON

ТОН має три типи цифрових активів.

- Toncoin, основний токен мережі. Він використовується для всіх базових операцій в блокчейні, наприклад, для оплати за газ або стейкінгу для валідації.
- Contract assets, such as tokens and NFTs, which are analogous to the ERC-20/ERC-721 standards and are managed by arbitrary contracts and thus can require custom rules for processing. You can find more info on it's processing in [process NFTs](/v3/guidelines/dapps/asset-processing/nft-processing/nfts) and [process Jettons](/v3/guidelines/dapps/asset-processing/jettons) articles.
- Нативні токени (Native token) - особливий вид активів, які можуть бути прикріплені до будь-якого повідомлення в мережі. Але наразі ці активи не використовуються, оскільки функціонал для випуску нових нативних токенів закритий.

## Interaction with TON Blockchain

Basic operations on TON Blockchain can be carried out via TonLib. It is a shared library which can be compiled along with a TON node and expose APIs for interaction with the blockchain via so-called lite servers (servers for lite clients). TonLib follows a trustless approach by checking proofs for all incoming data; thus, there is no necessity for a trusted data provider. Methods available to TonLib are listed [in the TL scheme](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L234). They can be used either as a shared library via [wrappers](/v3/guidelines/dapps/asset-processing/payments-processing/#sdks).

## Читати далі

Прочитавши цю статтю, ви зможете перевірити:

1. [Payments processing](/v3/guidelines/dapps/asset-processing/payments-processing) to get how to work with `TON coins`
2. [Jetton processing](/v3/guidelines/dapps/asset-processing/jettons) to get how to work with `jettons` (sometime called `tokens`)
3. [NFT processing](/v3/guidelines/dapps/asset-processing/nft-processing/nfts) to get how to work with `NFT` (that is the special type of `jetton`)

<Feedback />

