# 发送消息

TON Connect 2.0 不仅仅提供了在 dApp 中认证用户的强大选项：它还可以通过已连接的钱包发送外部消息！

您将了解到：

- 如何从 DApp 发送消息到区块链
- 如何在一次交易中发送多条消息
- 如何使用 TON Connect 部署合约

## 演示页面

我们将使用 JavaScript 的低级 [TON Connect SDK](https://github.com/ton-connect/sdk/tree/main/packages/sdk) 。我们将在钱包已连接的页面上的浏览器控制台上做实验。以下是示例页面：

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

随意将其复制粘贴到您的浏览器控制台并运行。

## 发送多条消息

### 1. 了解任务

我们将在一次交易中发送两条独立的消息：一条发送到您自己的地址，携带 0.2 TON，另一条发送到其他钱包地址，携带 0.1 TON。

顺便说一下，一次交易中发送的消息有限制：

- 标准 ([v3](/participate/wallets/contracts#wallet-v3)/[v4](/participate/wallets/contracts#wallet-v4)) 钱包：4 条传出消息；
- 高负载钱包：255 条传出消息（接近区块链限制）。

### 2. 发送消息

运行以下代码：

```js
console.log(await connector.sendTransaction({
  validUntil: Math.floor(new Date() / 1000) + 360,
  messages: [
    {
      address: connector.wallet.account.address,
      amount: "200000000"
    },
    {
      address: "0:b2a1ecf5545e076cd36ae516ea7ebdf32aea008caa2b84af9866becb208895ad",
      amount: "100000000"
    }
  ]
}));
```

您会注意到这个命令没有在控制台打印任何东西，像返回无内容的函数一样，`null` 或 `undefined`。这意味着 `connector.sendTransaction` 不会立即退出。

打开您的钱包应用，您会看到原因。有一个请求，显示您要发送的内容以及coin将会去向哪里。请接受它。

### 3. 获取结果

函数将退出，并且区块链的输出将被打印：

```json
{
  boc: "te6cckEBAwEA4QAC44gBZUPZ6qi8Dtmm1cot1P175lXUARlUVwlfMM19lkERK1oCUB3RqDxAFnPpeo191X/jiimn9Bwnq3zwcU/MMjHRNN5sC5tyymBV3SJ1rjyyscAjrDDFAIV/iE+WBySEPP9wCU1NGLsfcvVgAAACSAAYHAECAGhCAFlQ9nqqLwO2abVyi3U/XvmVdQBGVRXCV8wzX2WQRErWoAmJaAAAAAAAAAAAAAAAAAAAAGZCAFlQ9nqqLwO2abVyi3U/XvmVdQBGVRXCV8wzX2WQRErWnMS0AAAAAAAAAAAAAAAAAAADkk4U"
}
```

BOC 是 [Bag of Cells](/learn/overviews/cells)，这是 TON 中存储数据的方式。现在我们可以解码它。

在您选择的工具中解码这个 BOC，您将得到以下cell树：

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

返回发送交易的 BOC 的目的是跟踪它。

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

The purpose of returning BOC of the sent transaction is to track it.

## Sending complex transactions

### Serialization of cells

构建消息后，您可以将其序列化为 BOC。

- **payload** (string base64, optional): raw one-cell BoC encoded in Base64.
  - we will use it to store text comment on transfer
- **stateInit** (string base64, optional): raw one-cell BoC encoded in Base64.
  - we will use it to deploy a smart contract

After building a message, you can serialize it into BOC.

```js
TonWeb.utils.bytesToBase64(await payloadCell.toBoc())
```

### Transfer with comment

You can use [toncenter/tonweb](https://github.com/toncenter/tonweb) JS SDK or your favourite tool to serialize cells to BOC.

Text comment on transfer is encoded as opcode 0 (32 zero bits) + UTF-8 bytes of comment. Here's an example of how to convert it into a bag of cells.

```js
let a = new TonWeb.boc.Cell();
a.bits.writeUint(0, 32);
a.bits.writeString("TON Connect 2 tutorial!");
let payload = TonWeb.utils.bytesToBase64(await a.toBoc());

console.log(payload);
// te6ccsEBAQEAHQAAADYAAAAAVE9OIENvbm5lY3QgMiB0dXRvcmlhbCFdy+mw
```

### Smart contract deployment

现在，是时候发送我们的交易了！

```js
console.log(await connector.sendTransaction({
  validUntil: Math.floor(new Date() / 1000) + 360,
  messages: [
    {
      address: "0:1c7c35ed634e8fa796e02bbbe8a2605df0e2ab59d7ccb24ca42b1d5205c735ca",
      amount: "69000000",
      payload: "te6ccsEBAQEAHQAAADYAAAAAVE9OIENvbm5lY3QgMiB0dXRvcmlhbCFdy+mw",
      stateInit: "te6ccsEBBAEAUwAABRJJAgE0AQMBFP8A9KQT9LzyyAsCAGrTMAGCCGlJILmRMODQ0wMx+kAwi0ZG9nZYcCCAGMjLBVAEzxaARfoCE8tqEssfAc8WyXP7AAAQAAABhltsPJ+MirEd"
    }
  ]
}));
```

And, it's time to send our transaction!

```js
console.log(await connector.sendTransaction({
  validUntil: Math.floor(new Date() / 1000) + 360,
  messages: [
    {
      address: "0:1c7c35ed634e8fa796e02bbbe8a2605df0e2ab59d7ccb24ca42b1d5205c735ca",
      amount: "69000000",
      payload: "te6ccsEBAQEAHQAAADYAAAAAVE9OIENvbm5lY3QgMiB0dXRvcmlhbCFdy+mw",
      stateInit: "te6ccsEBBAEAUwAABRJJAgE0AQMBFP8A9KQT9LzyyAsCAGrTMAGCCGlJILmRMODQ0wMx+kAwi0ZG9nZYcCCAGMjLBVAEzxaARfoCE8tqEssfAc8WyXP7AAAQAAABhltsPJ+MirEd"
    }
  ]
}));
```

:::info
Get more examples in [Preparing Messages](/develop/dapps/ton-connect/message-builders) page for Transfer NFT and Jettons.
:::

处理请求拒绝相当简单，但当您正在开发某个项目时，最好提前知道会发生什么。

## What happens if the user rejects a transaction request?

It's pretty easy to handle request rejection, but when you're developing some project it's better to know what would happen in advance.

When a user clicks "Cancel" in the popup in the wallet application, an exception is thrown: `Error: [TON_CONNECT_SDK_ERROR] Wallet declined the request`. This error can be considered final (unlike connection cancellation) - if it has been raised, then the requested transaction will definitely not happen until the next request is sent.

## See Also

- [Preparing Messages](/develop/dapps/ton-connect/message-builders)
