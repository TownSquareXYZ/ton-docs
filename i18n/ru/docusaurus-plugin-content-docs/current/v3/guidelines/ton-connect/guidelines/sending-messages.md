import Feedback from '@site/src/components/Feedback';

# Sending messages

TON Connect has more powerful options than just authenticating users in the dApp; it also allows sending outgoing messages via connected wallets.

Вы узнаете:

- как отправлять сообщения из DApp в блокчейн
- как отправить несколько сообщений в одной транзакции
- как развернуть контракт с помощью TON Connect

## Страница для экспериментов

Мы будем использовать низкоуровневый [TON Connect SDK](https://github.com/ton-connect/sdk/tree/main/packages/sdk) на JavaScript. Мы поэкспериментируем в консоли браузера на странице, где кошелек уже подключен. Вот пример страницы:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <script src="https://unpkg.com/@tonconnect/sdk@latest/dist/tonconnect-sdk.min.js"></script>
    <script src="https://unpkg.com/tonweb@0.0.41/dist/tonweb.js"></script>
  </head>
  <body>
    <script>
      window.onload = async () => {
        window.connector = new TonConnectSDK.TonConnect({
          manifestUrl: 'https://ratingers.pythonanywhere.com/ratelance/tonconnect-manifest.json'
        });
        connector.restoreConnection();
      }
    </script>
  </body>
</html>
```

Не стесняйтесь скопировать и вставить этот код в консоль вашего браузера и выполнить его.

## Отправка нескольких сообщений

### Understanding a task

We will send two messages in one transaction: one to your address, carrying 0.2 TON, and one to the other wallet address, carrying 0.1 TON.

By the way, there is a limit to the number of messages sent in one transaction:

- стандартные ([v3](/v3/documentation/smart-contracts/contracts-specs/wallet-contracts#wallet-v3)/[v4](/v3/documentation/smart-contracts/contracts-specs/wallet-contracts#wallet-v4)) кошельки: 4 исходящих сообщения;
- highload кошельки: 255 исходящих сообщений (близко к ограничениям блокчейна).

### Sending the messages

Запустите следующий код:

```js
console.log(await connector.sendTransaction({
  validUntil: Math.floor(new Date() / 1000) + 360,
  messages: [
    {
      address: connector.wallet.account.address,
      amount: "200000000"
    },
    {
      address: "EQCyoez1VF4HbNNq5Rbqfr3zKuoAjKorhK-YZr7LIIiVrSD7",
      amount: "100000000"
    }
  ]
}));
```

Вы заметите, что эта команда ничего не выводит в консоль, `null` или `undefined`, так как функции, которые ничего не возвращают, не выходят. Это означает, что `connector.sendTransaction` не завершается немедленно.

Open your wallet application, and you'll see why. There is a request showing what you are sending and where the coins would go. Please, accept it.

### Getting the result

Функция завершит работу, и будет выведен результат из блокчейна:

```json
{
  boc: "te6cckEBAwEA4QAC44gBZUPZ6qi8Dtmm1cot1P175lXUARlUVwlfMM19lkERK1oCUB3RqDxAFnPpeo191X/jiimn9Bwnq3zwcU/MMjHRNN5sC5tyymBV3SJ1rjyyscAjrDDFAIV/iE+WBySEPP9wCU1NGLsfcvVgAAACSAAYHAECAGhCAFlQ9nqqLwO2abVyi3U/XvmVdQBGVRXCV8wzX2WQRErWoAmJaAAAAAAAAAAAAAAAAAAAAGZCAFlQ9nqqLwO2abVyi3U/XvmVdQBGVRXCV8wzX2WQRErWnMS0AAAAAAAAAAAAAAAAAAADkk4U"
}
```

BoC is [bag of cells](/v3/concepts/dive-into-ton/ton-blockchain/cells-as-data-storage), the way data is stored in TON. Now, we can decode it.

Decode this BoC in the tool of your choice, and you'll get the following tree of cells:

```bash
x{88016543D9EAA8BC0ED9A6D5CA2DD4FD7BE655D401195457095F30CD7D9641112B5A02501DD1A83C401673E97A8D7DD57FE38A29A7F41C27AB7CF0714FCC3231D134DE6C0B9B72CA6055DD2275AE3CB2B1C023AC30C500857F884F960724843CFF70094D4D18BB1F72F5600000024800181C_}
 x{42005950F67AAA2F03B669B5728B753F5EF9957500465515C257CC335F6590444AD6A00989680000000000000000000000000000}
 x{42005950F67AAA2F03B669B5728B753F5EF9957500465515C257CC335F6590444AD69CC4B40000000000000000000000000000}
```

This is a serialized external message, and two references are outgoing messages representations.

```bash
x{88016543D9EAA8BC0ED9A6D5CA2DD4FD7BE655D401195457095F30CD7D964111...
  $10       ext_in_msg_info
  $00       src:MsgAddressExt (null address)
  "EQ..."a  dest:MsgAddressInt (your wallet)
  0         import_fee:Grams
  $0        (no state_init)
  $0        (body starts in this cell)
  ...
```

Returning the BoC of the sent transaction is to track it.

### Processing transactions initiated with TON Connect

To find a transaction by `extInMsg`, you need to do the following:

1. Parse the received `extInMsg` as a cell.
2. Calculate the `hash()` of the obtained cell.

:::info
The received hash is what the `sendBocReturnHash` methods of TON Center API are already returning to you.
:::

3. Search for the required transaction using this hash through an indexer:

 - Using TON Center [api_v3_transactionsByMessage_get](https://toncenter.com/api/v3/#/default/get_transactions_by_message_api_v3_transactionsByMessage_get).

 - Using the `/v2/blockchain/messages/{msg_id}/transaction` method from [TON API](https://tonapi.io/api-v2).

 - Collect transactions independently and search for the required extInMsg by its hash: [see example](/v3/guidelines/dapps/cookbook#how-to-find-transaction-for-a-certain-ton-connect-result).

It's important to note that `extInMsg` may not be unique, which means collisions can occur. However, all transactions are unique.
If you are using this for an informative display, this method should be sufficient. With standard wallet contracts, collisions can occur only in exceptional situations.

## Отправка сложных транзакций

### Сериализация ячеек

Before we proceed, let's talk about the format of the messages we will send.

- **payload** (строка base64, необязательно): необработанный BoC из одной ячейки, закодированный в Base64.
 - We will use it to store text comments on transfer
- **stateInit** (строка base64, необязательно): необработанный BoC из одной ячейки, закодированный в Base64.
 - We will use it to deploy a smart contract

After building a message, you can serialize it into BoC.

```js
TonWeb.utils.bytesToBase64(await payloadCell.toBoc())
```

### Перевод с комментарием

You can use [toncenter/tonweb](https://github.com/toncenter/tonweb) JS SDK or your favourite tool to serialize cells to BoC.

Text comments on transfer are encoded as opcode 0 (32 zero bits) + UTF-8 bytes of comment. Here's an example of how to convert it into a bag of cells.

```js
let a = new TonWeb.boc.Cell();
a.bits.writeUint(0, 32);
a.bits.writeString("TON Connect tutorial!");
let payload = TonWeb.utils.bytesToBase64(await a.toBoc());

console.log(payload);
// te6ccsEBAQEAHQAAADYAAAAAVE9OIENvbm5lY3QgMiB0dXRvcmlhbCFdy+mw
```

### Развертывание смарт-контракта

And we'll deploy an instance of super simple [chatbot Doge](https://github.com/LaDoger/doge.fc), mentioned as one of [smart contract examples](/v3/documentation/smart-contracts/overview#examples-of-smart-contracts). First of all, we load its code and store something unique in data to receive our very own instance that someone else has not deployed. Then, we combine code and data into stateInit.

```js
let code = TonWeb.boc.Cell.oneFromBoc(TonWeb.utils.base64ToBytes('te6cckEBAgEARAABFP8A9KQT9LzyyAsBAGrTMAGCCGlJILmRMODQ0wMx+kAwi0ZG9nZYcCCAGMjLBVAEzxaARfoCE8tqEssfAc8WyXP7AN4uuM8='));
let data = new TonWeb.boc.Cell();
data.bits.writeUint(Math.floor(new Date()), 64);

let state_init = new TonWeb.boc.Cell();
state_init.bits.writeUint(6, 5);
state_init.refs.push(code);
state_init.refs.push(data);

let state_init_boc = TonWeb.utils.bytesToBase64(await state_init.toBoc());
console.log(state_init_boc);
//  te6ccsEBBAEAUwAABRJJAgE0AQMBFP8A9KQT9LzyyAsCAGrTMAGCCGlJILmRMODQ0wMx+kAwi0ZG9nZYcCCAGMjLBVAEzxaARfoCE8tqEssfAc8WyXP7AAAQAAABhltsPJ+MirEd

let doge_address = '0:' + TonWeb.utils.bytesToHex(await state_init.hash());
console.log(doge_address);
//  0:1c7c35ed634e8fa796e02bbbe8a2605df0e2ab59d7ccb24ca42b1d5205c735ca
```

And it's time to send our transaction:

```js
console.log(await connector.sendTransaction({
  validUntil: Math.floor(new Date() / 1000) + 360,
  messages: [
    {
      address: "EQAcfDXtY06Pp5bgK7voomBd8OKrWdfMskykKx1SBcc1yh5O",
      amount: "69000000",
      payload: "te6ccsEBAQEAHQAAADYAAAAAVE9OIENvbm5lY3QgMiB0dXRvcmlhbCFdy+mw",
      stateInit: "te6ccsEBBAEAUwAABRJJAgE0AQMBFP8A9KQT9LzyyAsCAGrTMAGCCGlJILmRMODQ0wMx+kAwi0ZG9nZYcCCAGMjLBVAEzxaARfoCE8tqEssfAc8WyXP7AAAQAAABhltsPJ+MirEd"
    }
  ]
}));
```

:::info
Get more examples on the [Preparing Messages](/v3/guidelines/ton-connect/guidelines/preparing-messages) page for Transfer NFT and Jettons.
:::

После подтверждения мы можем увидеть нашу транзакцию завершенной на сайте [tonscan.org](https://tonscan.org/tx/pCA8LzWlCRTBc33E2y-MYC7rhUiXkhODIobrZVVGORg=).

## Что произойдет, если пользователь отклонит запрос транзакции?

It's pretty easy to handle request rejection, but it's better to know what would happen in advance when you're developing some project.

When a user clicks **Cancel** in the popup in the wallet application, an exception is thrown:

```ts
Error: [TON_CONNECT_SDK_ERROR] The Wallet declined the request 
```

This error can be considered final (unlike connection cancellation) - if it has been raised, then the requested transaction will definitely not happen until the next request is sent.

## See also

- [Preparing messages](/v3/guidelines/ton-connect/guidelines/preparing-messages)

<Feedback />

