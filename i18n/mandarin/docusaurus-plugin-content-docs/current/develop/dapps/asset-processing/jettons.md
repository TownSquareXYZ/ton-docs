import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import Button from '@site/src/components/button';

# 处理 TON Jetton

处理 jettons 的最佳实践及注释：

- [接受 jettons 存款的 JS 算法](https://github.com/toncenter/examples/blob/main/deposits-jettons.js)

- [jettons 提款的 JS 算法](https://github.com/toncenter/examples/blob/main/withdrawals-jettons.js)

- [JS code to withdraw (send) jettons from a wallet in batches](https://github.com/toncenter/examples/blob/main/withdrawals-jettons-highload-batch.js)

:::info Transaction Confirmation
TON transactions are irreversible after just one confirmation. For the best user experience, it is suggested to avoid waiting on additional blocks once transactions are finalized on the TON Blockchain. Read more in the [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3).
:::

In most cases, this should be enough for you, if not, you can find detailed information below.

## Content List

This document describes the following in order:

1. Overview
2. Architecture
3. Jetton Master Contract (Token Minter)
4. Jetton Wallet Contract (User Wallet)
5. Message Layouts
6. Jetton Processing (off-chain)
7. Jetton Processing (on-chain)
8. Wallet processing
9. Best Practices

## Overview

:::info
For clear understanding, the reader should be familiar with the basic principles of asset processing described in [this section of our documentation](/develop/dapps/asset-processing/). In particular, it is important to be familiar with [contracts](/learn/overviews/addresses#everything-is-a-smart-contract), [wallets](/develop/smart-contracts/tutorials/wallet), [messages](/develop/smart-contracts/guidelines/message-delivery-guarantees) and deployment process.
:::

\<Button href="/develop/dapps/asset-processing/jettons#accepting-jettons-from-users-through-a-centralized-wallet" colorType={'primary'} sizeType={'sm'}>集中处理</Button>
\<Button href="/develop/dapps/asset-processing/jettons#accepting-jettons-from-user-deposit-addresses"
colorType="secondary" sizeType={'sm'}>
链上处理 </Button>

<br></br><br></br>

TON 区块链及其底层生态系统将可替代代币（FTs）分类为 jettons。因为 TON 区块链应用了分片，我们对可替代代币的实现在与类似的区块链模型相比时是独特的。

在这项分析中，我们深入探讨了详细规定 jetton [行为](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md)和[元数据](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md)的正式标准。
我们还在我们的[分片聚焦的 jetton 架构概述博客文章](https://blog.ton.org/how-to-shard-your-ton-smart-contract-and-why-studying-the-anatomy-of-tons-jettons)中提供了关于 jetton 架构的非正式详情。
我们还讨论了我们的第三方开源 TON 支付处理程序（[bicycle](https://github.com/gobicycle/bicycle)）的特定详情，该处理程序允许用户使用单独的存款地址存取 Toncoin 和 jettons，无需使用文本备注。

In this analysis, we take a deeper dive into the formal standards detailing jetton [behavior](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md) and [metadata](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md).
A less formal sharding-focused overview of jetton architecture can be found in our
[anatomy of jettons blog post](https://blog.ton.org/how-to-shard-your-ton-smart-contract-and-why-studying-the-anatomy-of-tons-jettons).

TON 上的标准化代币使用一组智能合约来实现，包括：

## Jetton Architecture

Standardized tokens on TON are implemented using a set of smart contracts, including:

- [Jetton master](https://github.com/ton-blockchain/token-contract/blob/main/ft/jetton-minter.fc) smart contract
- [Jetton wallet](https://github.com/ton-blockchain/token-contract/blob/main/ft/jetton-wallet.fc) smart contracts

<p align="center">
  <br />
    <img width="420" src="/img/docs/asset-processing/jetton_contracts.svg" alt="contracts scheme" />
      <br />
</p>

## Jetton master smart contract

为了消除 TON 用户的欺诈可能性，请查找特定 jetton 类型的原始 jetton 地址（Jetton 主合约），或关注项目的官方社交媒体频道或网站以找到正确信息。检查资产以消除 [Tonkeeper ton-assets list](https://github.com/tonkeeper/ton-assets)的欺诈可能性。

including the total supply, a metadata link, or the metadata itself).

要检索更具体的 Jetton 数据，使用 `get_jetton_data()` 获取方法。

此方法返回以下数据：

### Retrieving Jetton data

也可以使用 [Toncenter API](https://toncenter.com/api/v3/#/default/get_jetton_masters_api_v3_jetton_masters_get) 中的方法 `/jetton/masters` 来检索已解码的 Jetton 数据和元数据。我们还为 (js) [tonweb](https://github.com/toncenter/tonweb/blob/master/src/contract/token/ft/JettonMinter.js#L85) 和 (js) [ton-core/ton](https://github.com/ton-core/ton/blob/master/src/jetton/JettonMaster.ts#L28)，(go) [tongo](https://github.com/tonkeeper/tongo/blob/master/liteapi/jetton.go#L48) 和 (go) [tonutils-go](https://github.com/xssnick/tonutils-go/blob/33fd62d754d3a01329ed5c904db542ab4a11017b/ton/jetton/jetton.go#L79)，(python) [pytonlib](https://github.com/toncenter/pytonlib/blob/d96276ec8a46546638cb939dea23612876a62881/pytonlib/client.py#L742) 以及许多其他 SDK 开发了方法。

使用 [Tonweb](https://github.com/toncenter/tonweb) 运行 get 方法并获取链下元数据的 url 的示例：

| Name                 | Type    | Description                                                                                                                                                                              |
| -------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `total_supply`       | `int`   | the total number of issued jettons measured in indivisible units.                                                                                                        |
| `mintable`           | `int`   | details whether new jettons can be minted or not. This value is either -1 (can be minted) or 0 (cannot be minted). |
| `admin_address`      | `slice` |                                                                                                                                                                                          |
| `jetton_content`     | `cell`  | data in accordance with [TEP-64](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md).                                                   |
| `jetton_wallet_code` | `cell`  |                                                                                                                                                                                          |

It is also possible to use the method `/jetton/masters` from the [Toncenter API](https://toncenter.com/api/v3/#/default/get_jetton_masters_api_v3_jetton_masters_get) to retrieve the already decoded Jetton data and metadata. We have also developed methods for (js) [tonweb](https://github.com/toncenter/tonweb/blob/master/src/contract/token/ft/JettonMinter.js#L85) and (js) [ton-core/ton](https://github.com/ton-core/ton/blob/master/src/jetton/JettonMaster.ts#L28), (go) [tongo](https://github.com/tonkeeper/tongo/blob/master/liteapi/jetton.go#L48) and (go) [tonutils-go](https://github.com/xssnick/tonutils-go/blob/33fd62d754d3a01329ed5c904db542ab4a11017b/ton/jetton/jetton.go#L79), (python) [pytonlib](https://github.com/toncenter/pytonlib/blob/d96276ec8a46546638cb939dea23612876a62881/pytonlib/client.py#L742) and many other SDKs.

[这里](/develop/dapps/asset-processing/metadata)提供了有关解析元数据的更多信息。

```js
import TonWeb from "tonweb";
const tonweb = new TonWeb();
const jettonMinter = new TonWeb.token.jetton.JettonMinter(tonweb.provider, {address: "<JETTON_MASTER_ADDRESS>"});
const data = await jettonMinter.getJettonData();
console.log('Total supply:', data.totalSupply.toString());
console.log('URI to off-chain metadata:', data.jettonContentUri);
```

#### Jetton metadata

Jetton 钱包不应与仅用于区块链交互和只存储 Toncoin 资产（例如，v3R2 钱包、高负载钱包等）的钱包混淆，它负责支持和管理只有特定 jetton 类型的。

## Jetton Wallet smart contracts

Jetton wallet contracts are used to send, receive, and burn jettons. Each _jetton wallet contract_ stores wallet balance information for specific users.
In specific instances, jetton wallets are used for individual jetton holders for each jetton type.

要使用所有者地址（TON 钱包地址）检索 jetton 钱包地址，
Jetton 主合约提供了 get 方法 `get_wallet_address(slice owner_address)`。

Jetton wallets make use of smart contracts and are managed using internal messages between
the owner's wallet and the jetton wallet. For instance, say if Alice manages a wallet with jettons inside,
the scheme is as follows: Alice owns a wallet designed specifically for jetton use (such as wallet version v3r2).
When Alice initiates the sending of jettons in a wallet she manages, she sends external messages to her wallet,
and as a result, _her wallet_ sends an internal message to _her jetton wallet_ and
then the jetton wallet actually executes the token transfer.

### Retrieving Jetton wallet addresses for a given user

To retrieve a jetton wallet address using an owner address (a TON Wallet address),
the Jetton master contract provides the get method `get_wallet_address(slice owner_address)`.

#### Retrieve using API

The application serializes the owner’s address to a cell using
the `/runGetMethod` method from the [Toncenter API](https://toncenter.com/api/v3/#/default/run_get_method_api_v3_runGetMethod_post).

#### Retrieve using SDK

This process can also be initiated using ready to use methods present in our various SDKs, for instance,\
using the Tonweb SDK, this process can be initiated by entering the following strings:

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
For more examples read the [TON Cookbook](/develop/dapps/cookbook#how-to-calculate-users-jetton-wallet-address).
:::

### Retrieving data for a specific Jetton wallet

也可以使用 [Toncenter API](https://toncenter.com/api/v3/#/default/get_jetton_wallets_api_v3_jetton_wallets_get) 的 `/jetton/wallets` get 方法来检索先前解码的 jetton 钱包数据（或 SDK 中的方法）。例如，使用 Tonweb：

This method returns the following data:

| Name                                                         | Type  |
| ------------------------------------------------------------ | ----- |
| balance                                                      | int   |
| owner                                                        | slice |
| jetton                                                       | slice |
| jetton_wallet_code | cell  |

在钱包之间转移 jettons 时，交易（消息）需要一定量的 TON作为网络gas费和根据 Jetton 钱包合约代码执行操作的支付。这意味着接收者在接收 jettons 之前不需要部署 jetton 钱包。只要发送方的钱包中有足够的 TON支付所需的gas费，接收者的 jetton 钱包将自动部署。

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

### Jetton Wallet Deployment

Jetton 钱包和 TON 钱包之间的通信是通过以下通信序列进行的：

## Message Layouts

:::tip Messages
Read more about Messages [here](/develop/smart-contracts/guidelines/message-delivery-guarantees).
:::

Communication between Jetton wallets and TON wallets occurs through the following communication sequence:

`收款人' jetton 钱包 -> 收款人`  意味着消息通知体包含以下数据：

`Sender -> sender' jetton wallet` means the _transfer_ message body contains the following data:

| Name                   | Type    |
| ---------------------- | ------- |
| `query_id `            | uint64  |
| `amount  `             | coins   |
| `destination  `        | address |
| `response_destination` | address |
| `custom_payload  `     | cell    |
| `forward_ton_amount`   | coins   |
| `forward_payload`      | cell    |

`payee' jetton wallet -> payee`  means the message notification body contains the following data:

| Name                                   | Type    |
| -------------------------------------- | ------- |
| query_id    \`    | uint64  |
| amount   \`                            | coins   |
| sender  \`                             | address |
| forward_payload\` | cell    |

使用 `Transfer notification` 和 `Excesses` 参数的消息是可选的，取决于附着在 `Transfer` 消息上的 TON 的数量以及 `forward_ton_amount` 字段的值。

| Name       | Type   |
| ---------- | ------ |
| `query_id` | uint64 |

A detailed description of the jetton wallet contract fields can be found in the [TEP-74](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md) Jetton standard interface description.

为了进行附带通知的转账（随后在钱包内用于通知目的），必须通过设置非零的 `forward_ton_amount` 值附加足够数量的TON到发送的消息中，并且如有必要，将文本评论附加到 `forward_payload`。文本评论的编码方式与发送Toncoin时的文本评论类似。

[发送Jettons的费用](https://docs.ton.org/develop/smart-contracts/fees#fees-for-sending-jettons)

### How to send Jetton transfers with comments and notifications

[使用Tonweb SDK的Jetton带评论转账示例](https://github.com/toncenter/tonweb/blob/b550969d960235314974008d2c04d3d4e5d1f546/src/test-jetton.js#L128):

[Fees for sending Jettons](https://docs.ton.org/develop/smart-contracts/fees#fees-for-sending-jettons)

However, the commission depends on several factors including the Jetton code details and the need to deploy a new Jetton wallet for recipients.
Therefore, it is recommended to attach Toncoin with a margin and then set the address as the  `response_destination`
to retrieve `Excesses` messages. For example, 0.05 TON can be attached to the message while setting the `forward_ton_amount`
value to 0.01 TON (this amount of TON will be attached to the `Transfer notification` message).

[Jetton transfers with comment examples using the Tonweb SDK](https://github.com/toncenter/tonweb/blob/b550969d960235314974008d2c04d3d4e5d1f546/src/test-jetton.js#L128):

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

:::tip
For more examples read the [TON Cookbook](/develop/dapps/cookbook#how-to-construct-a-message-for-a-jetton-transfer-with-a-comment).
:::

## Jetton off-chain processing

:::info Transaction Confirmation
TON transactions are irreversible after just one confirmation. For the best user experience, it is suggested to avoid waiting on additional blocks once transactions are finalized on the TON Blockchain. Read more in the [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3).
:::

在处理资金时，也建议提供一个冷钱包用于存储不参与自动存款和提款过程的额外资金。

To process Jettons, unlike individualized TON processing, a hot wallet is required (a v3R2, highload wallet) in addition
to a Jetton wallet or more than one Jetton wallet. Jetton hot wallet deployment is described in the [wallet deployment](/develop/dapps/asset-processing/#wallet-deployment) of our documentation.
That said, deployment of Jetton wallets according to the [Jetton wallet deployment](#jetton-wallet-deployment) criteria is not required.
However, when Jettons are received, Jetton wallets are deployed automatically, meaning that when Jettons are withdrawn,
it is assumed that they are already in the user’s possession.

For security reasons it is preferable to be in possession of separate hot wallets for separate Jettons (many wallets for each asset type).

为了确保所有用户的安全，至关重要的是避免可能被伪造（假冒）的Jettons。例如，`symbol`==`TON` 的Jettons或那些包含系统通知消息的Jettons，例如：`ERROR`、`SYSTEM` 等。务必确保jettons以这样的方式在你的界面中显示，以便它们不能与TON转账、系统通知等混淆。有时，即使`symbol`、`name`和`image`被设计得几乎与原始的一模一样，也是只是希望误导用户的。

### 在收到转账通知消息时识别未知的 Jetton

1. 如果在你的钱包内收到了关于未知Jetton的转账通知消息，那么你的钱包就被创建为持有特定Jetton的钱包。接下来，进行几个验证过程很重要。
2. 包含 `Transfer notification` 体的内部消息的发送地址是新的Jetton钱包的地址。不要与 `Transfer notification` 体内的 `sender` 字段混淆，Jetton钱包的地址是消息来源的地址。

For the safety of all of our users, it is critical to avoid Jettons that could be  counterfeited (fake). For example,
Jettons with the  `symbol`==`TON` or those that contain system notification messages, such as:
`ERROR`, `SYSTEM`, and others. Be sure to check that jettons are displayed in your interface in such a way that they cannot
be mixed with TON transfers, system notifications, etc.. At times, even the `symbol`,`name` and `image`
will be created to look nearly identical to the original with the hopes of misleading users.

### Identification of an unknown Jetton when receiving a transfer notification message

1. If a transfer notification message is received within your wallet regarding an unknown Jetton, then your wallet
   has been created to hold the specific Jetton. Next, it is important to perform several verification processes.
2. The sender address of the internal message containing the `Transfer notification` body is the address of the new Jetton wallet.
   Not to be confused with the `sender` field in the `Transfer notification`  body, the address of the Jetton wallet
   is the address from the source of the message.
3. Retrieving the Jetton master address for the new Jetton wallet: [How to retrieve data for the Jetton wallet](#retrieving-jetton-data).
   To carry out this process, the `jetton` parameter is required and is the address that makes up the Jetton master contract.
4. Retrieving the Jetton wallet address for your wallet address (as an owner) using the Jetton master contract: [How to retrieve Jetton wallet address for a given user](#retrieving-jetton-wallet-addresses-for-a-given-user)
5. Compare the address returned by the master contract and the actual address of the wallet token.
   If they match, it’s ideal. If not, then you likely received a scam token that is counterfeit.
6. Retrieving Jetton metadata: [How to receive Jetton metadata](#retrieving-jetton-data).
7. Check the `symbol` and `name` fields for signs of a scam. Warn the user if necessary. [Adding a new Jettons for processing and initial checks](#adding-new-jettons-for-asset-processing-and-initial-verification).

### Accepting Jettons from users through a centralized wallet

:::info
To prevent a bottleneck in incoming transactions to a single wallet, it is suggested to accept deposits across multiple wallets and to expand the number of these wallets as needed.
:::

In this scenario, the payment service creates a unique memo identifier for each sender disclosing
the address of the centralized wallet and the amounts being sent. The sender sends the tokens
to the specified centralized address with the obligatory memo in the comment.

**Pros of this method:** this method is very simple because there are no additional fees when accepting tokens and they are retrieved directly in the hot wallet.

**Cons of this method:** this method requires that all users attach a comment to the transfer which can lead to a greater number of deposit mistakes (forgotten memos, incorrect memos, etc.), meaning a higher workload for support staff.

Tonweb examples:

1. 加载接受的Jettons列表
2. 检索你部署的热钱包的Jetton钱包地址：[如何检索特定用户的Jetton钱包地址](#retrieving-jetton-wallet-addresses-for-a-given-user)

#### 通过用户存款地址接收 Jettons

1. Prepare a list of accepted Jettons: [Adding new Jettons for processing and initial verification](#adding-new-jettons-for-asset-processing-and-initial-verification).
2. Hot wallet deployment (using v3R2 if no Jetton withdrawals are expected; highload v2 - if Jetton withdrawals are expected) [Wallet deployment](/develop/dapps/asset-processing/#wallet-deployment).
3. Perform a test Jetton transfer using the hot wallet address to initialize the wallet.

#### Processing incoming Jettons

1. Load the list of accepted Jettons
2. Retrieve a Jetton wallet address for your deployed hot wallet: [How to retrieve a Jetton wallet address for a given user](#retrieving-jetton-wallet-addresses-for-a-given-user)
3. Retrieve a Jetton master address for each Jetton wallet: [How to retrieve data for a Jetton wallet](#retrieving-data-for-a-specific-jetton-wallet).
   To carry out this process, the `jetton` parameter is required (which is actually the address
   of the Jetton master contract).
4. Compare the addresses of the Jetton master contracts from step 1. and step 3 (directly above).
   If the addresses do not match, a Jetton address verification error must be reported.
5. Retrieve a list of the most recent unprocessed transactions using a hot wallet account and
   iterate it (by sorting through each transaction one by one). See:  [Checking contract's transactions](https://docs.ton.org/develop/dapps/asset-processing/#checking-contracts-transactions),
   or use the [Tonweb example](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-single-wallet.js#L43)
   or use Toncenter API `/getTransactions` method.
6. Check the input message (in_msg) for transactions and retrieve the source address from the input message. [Tonweb example](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-jettons-single-wallet.js#L84)
7. If the source address matches the address within a Jetton wallet, then it is necessary to continue processing the transaction.
   If not, then skip processing the transaction and check the next transaction.
8. Ensure that the message body is not empty and that the first 32 bits of the message match the `transfer notification` op code `0x7362d09c`.
   [Tonweb example](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-jettons-single-wallet.js#L91)
   If the message body is empty or the op code is invalid - skip the transaction.
9. Read the message body’s other data, including the `query_id`, `amount`, `sender`, `forward_payload`.
   [Jetton contracts message layouts](#jetton-contract-message-layouts), [Tonweb example](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-jettons-single-wallet.js#L105)
10. Try to retrieve text comments from the `forward_payload` data. The first 32 bits must match
    the text comment op code `0x00000000` and the remaining - UTF-8 encoded text.
    [Tonweb example](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-jettons-single-wallet.js#L110)
11. If the `forward_payload` data is empty or the op code is invalid - skip the transaction.
12. Compare the received comment with the saved memos. If there is a match (user identification is always possible) - deposit the transfer.
13. Restart from step 5 and repeat the process until you have walked through the entire list of transactions.

### Accepting Jettons from user deposit addresses

To accept Jettons from user deposit addresses, it is necessary that the payment service creates its
own individual address (deposit) for each participant sending funds. The service provision in this case involves
the execution of several parallel processes including creating new deposits, scanning blocks for transactions,
withdrawing funds from deposits to a hot wallet, and so on.

Because a hot wallet can make use of one Jetton wallet for each Jetton type, it is necessary to create multiple
wallets to initiate deposits. In order to create a large number of wallets, but at the same time manage them with
one seed phrase (or private key), it is necessary to specify a different `subwallet_id` when creating a wallet.
On TON, the functionality required to create a subwallet is supported by version v3 wallets and higher.

#### 创建存款

```Tonweb
const WalletClass = tonweb.wallet.all['v3R2'];
const wallet = new WalletClass(tonweb.provider, {
    publicKey: keyPair.publicKey,
    wc: 0,
    walletId: <SUBWALLET_ID>,
});
```

#### 处理交易

1. Prepare a list of accepted Jettons: [Adding new Jettons for processing and initial checks](#adding-new-jettons-for-asset-processing-and-initial-verification)
2. Hot wallet [Wallet Deployment](/develop/dapps/asset-processing/#wallet-deployment)

#### Creating deposits

1. Accept a request to create a new deposit for the user.
2. Generate a new subwallet (v3R2) address based on the hot wallet seed. [Creating a subwallet in Tonweb](#creating-a-subwallet-in-tonweb)
3. The receiving address can be given to the user as the address used for Jetton deposits (this is the address of
   the owner of the deposit Jetton wallet). Wallet initialization is not required, this can be
   accomplished when withdrawing Jettons from the deposit.
4. For this address, it is necessary to calculate the address of the Jetton wallet through the Jetton master contract.
   [How to retrieve a Jetton wallet address for a given user](#retrieving-jetton-wallet-addresses-for-a-given-user).
5. Add the Jetton wallet address to the address pool for transaction monitoring and save the subwallet address.

#### Processing transactions

:::info Transaction Confirmation
TON transactions are irreversible after just one confirmation. For the best user experience, it is suggested to avoid waiting on additional blocks once transactions are finalized on the TON Blockchain. Read more in the [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3).
:::

It is not always possible to determine the exact amount of Jettons received from the message, because Jetton
wallets may not send `transfer notification`, `excesses`, and `internal transfer` messages are not standardized. This means
that there is no guarantee that the `internal transfer` message can be decoded.

不应从每次存款充值时都将存款转至热钱包，因为转账操作会收取TON手续费（以网络gas费支付）。
重要的是确定一定数量的Jettons，这些Jettons是必需的，才能使转账变得划算（从而存入）。

默认情况下，Jetton存款钱包的所有者不会初始化。这是因为没有预定的必须支付存储费。在发送带有
`transfer`正文的消息时，可以部署Jetton存款钱包，然后立即销毁它。为此，工程师必须使用发送消息的特殊机制：128 + 32。

1. 检索标记为要提取到热钱包的存款列表
2. 为每个存款检索保存的所有者地址
3. 然后将消息发送到每个所有者地址（通过将几条这样的消息组合成一批），从高负载钱包附加TON Jetton数量。这是通过添加用于v3R2钱包初始化的费用+发送带有`transfer`正文的消息的费用+任意TON数量的`forward_ton_amount`
   （如有必要）。附加的TON数量是通过添加用于v3R2钱包初始化的费用（值）+ 发送带有`transfer`正文的消息的费用（值）+ 任意TON数量的
   `forward_ton_amount`（值）（如果需要）来确定的。
4. 当地址上的余额变为非零时，帐户状态发生改变。等待几秒钟，然后检查帐户状态，它很快会从`nonexists`状态变为`uninit`。
5. 对于每个所有者地址（处于`uninit`状态），需要发送一条带有v3R2钱包
   init和带有`transfer`消息的正文进行存入Jetton钱包的外部消息= 128 + 32。对于`transfer`，
   用户必须将热钱包地址指定为`destination`和`response destination`。
   可以添加文字评论以简化转账识别。
6. 可以使用存款地址到热钱包地址的Jetton传送进行验证，通过考虑
   [这里找到的处理传入Jettons信息](#处理传入-jettons)。
7. As an identifier for an unidentified transfer of Jettons (without a `transfer notification`), transaction data
   can be used if there is one such transaction or block data present (if several are present within a block).
8. Now it’s necessary to check to ensure the deposit balance is correct. If the deposit balance is sufficient enough to initiate a transfer between a hot wallet and the existing Jetton wallet, Jettons need to be withdrawn to ensure the wallet balance has decreased.
9. Restart from step 2 and repeat the entire process.

#### Jetton 提款

要提取Jettons，钱包发送带有`transfer`正文的消息到其对应的Jetton钱包。
然后Jetton钱包将Jettons发送给收件人。本着诚信，重要的是要附上一些TON
作为`forward_ton_amount`（并选择性附上评论到`forward_payload`）以触发`transfer notification`。
参见：[Jetton合约消息布局](#jetton-合约消息布局)

By default, wallet owners of Jetton deposit wallets are not initialized. This is because there is no predetermined
requirement to pay storage fees. Jetton deposit wallets can be deployed when sending messages with a
`transfer`  body which can then be destroyed immediately. To do this, the engineer must use a special
mechanism for sending messages: 128 + 32.

1. 准备用于提款的Jettons列表：[为处理和初步验证添加新的Jettons](#为资产处理和初始验证添加新的-jettons)
2. 启动热钱包部署。推荐使用Highload v2。[钱包部署](/develop/dapps/asset-processing/#wallet-deployment)
3. 使用热钱包地址进行Jetton转账，以初始化Jetton钱包并补充其余额。
4. When the balance on the address becomes non-zero, the account status changes. Wait a few seconds and check the status
   of the account, it will soon change from the `nonexists` state to `uninit`.
5. For each owner address (with `uninit` status), it is necessary to send an external message with the v3R2 wallet
   init and body with the `transfer` message for depositing into the Jetton wallet = 128 + 32. For the `transfer`,
   the user must specify the address of the hot wallet as the `destination` and `response destination`.
   A text comment can be added  to make it simpler to identify the transfer.
6. It is possible to verify Jetton delivery using the deposit address to the hot wallet address by
   taking into consideration the [processing of incoming Jettons info found here](#processing-incoming-jettons).

### 处理提款

To withdraw Jettons, the wallet sends messages with the `transfer` body to its corresponding Jetton wallet.
The Jetton wallet then sends the Jettons to the recipient. In good faith, it is important to attach some TON
as the  `forward_ton_amount` (and optional comment to `forward_payload`) to trigger a `transfer notification`.
See: [Jetton contracts message layouts](#jetton-contract-message-layouts)

#### 在链上处理 Jetton

1. Prepare a list of Jettons for withdrawals: [Adding new Jettons for processing and initial verification](#adding-new-jettons-for-asset-processing-and-initial-verification)
2. Hot wallet deployment is initiated. Highload v2 is recommended. [Wallet Deployment](/develop/dapps/asset-processing/#wallet-deployment)
3. Carry out a Jetton transfer using a hot wallet address to initialize the Jetton wallet and replenish its balance.

#### Processing withdrawals

1. Load a list of processed Jettons
2. Retrieve Jetton wallet addresses for the deployed hot wallet: [How to retrieve Jetton wallet addresses for a given user](#retrieving-jetton-wallet-addresses-for-a-given-user)
3. Retrieve Jetton master addresses for each Jetton wallet: [How to retrieve data for Jetton wallets](#retrieving-data-for-a-specific-jetton-wallet).
   A `jetton` parameter is required (which is actually the address of Jetton master contract).
4. Compare the addresses from Jetton master contracts from step 1. and step 3. If the addresses do not match, then a Jetton address verification error should be reported.
5. Withdrawal requests are received which actually indicate the type of Jetton, the amount being transferred, and the recipient wallet address.
6. Check the balance of the Jetton wallet to ensure there are enough funds present to carry out withdrawal.
7. Generate a message using the Jetton `transfer` body by filling in the required fields, including: the query_id, amount being sent,
   destination (the recipient's non-Jetton wallet address), response_destination (it is recommended to specify the user’s hot wallet),
   forward_ton_amount (it is recommended to set this to at least 0.05 TON to invoke a `transfer notification`), `forward_payload`
   (optional, if sending a comment is needed). [Jetton contracts message layouts](#jetton-contract-message-layouts),
   [Tonweb example](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/jettons-withdrawals.js#L69)
   In order to check the successful validation of the transaction, it is necessary to assign a unique value to the
   `query_id` for each message.
8. When using a highload wallet, it is recommended that a batch of messages is collected and that one batch at a time is sent to optimize fees.
9. Save the expiration time for outgoing external messages (this is the time until the wallet successfully
   processes the message, after this is completed, the wallet will no longer accept the message)
10. Send a single message or more than one message (batch messaging).
11. Retrieve the list of the latest unprocessed transactions within the hot wallet account and iterate it.
    Learn more here: [Checking contract's transactions](/develop/dapps/asset-processing/#checking-contracts-transactions),
    [Tonweb example](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-single-wallet.js#L43) or
    use the Toncenter API `/getTransactions` method.
12. Look at outgoing messages in the account.
13. If a message exists with the `transfer` op code, then it should be decoded to retrieve the `query_id` value.
    Retrieved `query_id`s  need to be marked as successfully sent.
14. If the time it takes for the current scanned transaction to be processed is greater than
    the expiration time and the outgoing message with the given `query_id`
    is not found, then the request should (this is optional) be marked as expired and should be safely resent.
15. Look for incoming messages in the account.
16. If a message exists that uses the `excesses` op code, the message should be decoded and the `query_id`
    value should be retrieved. A found `query_id` must be marked as successfully delivered.
17. Go to step 5. Expired requests that have not been successfully sent should be pushed back to the withdrawal list.

## Jetton processing on-chain

:::info Transaction Confirmation
TON transactions are irreversible after just one confirmation. For the best user experience, it is suggested to avoid waiting on additional blocks once transactions are finalized on the TON Blockchain. Read more in the [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3).
:::

通常，用于链下jetton处理的所有验证程序都适用于钱包。对于Jetton钱包处理，我们最重要的建议如下：

Below is a list of recommendations that must be considered when carrying out on-chain jetton processing:

1. Identify incoming jettons using their wallet type, not their Jetton master contract. In other words, your contract should interact (receive and send messages) with a specific jetton wallet (not with some unknown wallet using a specific Jetton master contract).
2. When linking a Jetton Wallet and a Jetton Master, check that this connection is bidirectional where the wallet recognizes the master contract and vice versa. For instance, if your contract-system receives a notification from a jetton wallet (which considers its MySuperJetton as its master contract) its transfer information must be displayed to the user, prior to showing the `symbol`, `name` and `image`
   of the MySuperJetton contract, check that the MySuperJetton wallet uses the correct contract system. In turn, if your contract system for some reason needs to send jettons using the MySuperJetton or MySuperJetton master contracts verify that wallet X as is the wallet using the same contract parameters.
   Additionally, prior to sending a  `transfer` request to X, make sure it recognizes MySuperJetton as its master.
3. The true power of decentralized finance (DeFi) is based on the ability to stack protocols on top of each other like lego blocks. For instance, say jetton A is swapped for jetton B, which in turn, is then used as leverage within a lending protocol (when a user supplies liquidity) which is then used to buy an NFT .... and so on. Therefore, consider how the contract is able to serve, not only off-chain users, but on-chain entities as well by attaching tokenized value to a transfer notification, adding a custom payload that can be sent with a transfer notification.
4. Be aware that not all contracts follow the same standards. Unfortunately, some jettons may be hostile (using attack-based vectors) and created for the sole purposes of attacking unsuspecting users. For security purposes, if the protocol in question consists of many contracts, do not create a large number of jetton wallets of the same type. In particular, do not send jettons inside the protocol between the deposit contract, vault contract, or user account contract etc. Attackers may intentionally interfere with contract logic by forging transfer notifications, jetton amounts, or payload parameters. Reduce the potential for attack potential by using only one wallet in the system per jetton (for all deposits and withdrawals).
5. It is also often a good idea to create subcontracts for each individualized jetton to reduce the chances of address spoofing (for example, when a transfer message is sent to jetton B using a contract intended for jetton A).
6. It is strongly recommended to work with indivisible jetton units on the contract level. Decimal-related logic is typically used to enhance the diplay’s user interface (UI), and is not related to numerical on-chain record keeping.
7. To learn more about [Secure Smart Contract Programming in FunC by CertiK](https://blog.ton.org/secure-smart-contract-programming-in-func), feel free to read this resource. It is recommended that developers handle all smart contract exceptions so they are never skipped during application development.

## 最佳实践

在此我们提供了一些由TON社区成员创建的jetton代码处理的示例：

1. When a wallet receives a transfer notification from an unknown jetton wallet, it is vitally important to trust the jetton wallet and its master address because it could be a malicious counterfeit. To protect yourself, check the Jetton Master (the master contract) using its provided address to ensure your verification processes recognize the jetton wallet as legitimate. After you trust the wallet and it is verified as legitimate, you can allow it to access your account balances and other in-wallet data. If the Jetton Master does not recognize this wallet it is recommended to not initiate or disclose your jetton transfers at all and to only show incoming TON transfers (of Toncoin attached to the transfer notifications) only.
2. In practice, if the user wants to interact with a Jetton and not a jetton wallet. In other words, users send wTON/oUSDT/jUSDT, jUSDC, jDAI instead of `EQAjN...`/`EQBLE...`
   etc.. Often this means that when a user is initiating a jetton transfer, the wallet asks the corresponding jetton master which jetton wallet (owned by the user) should initiate the transfer request. It is important to never blindly trust this data from the Master (the master contract). Prior to sending the transfer request to a jetton wallet, always ensure that the jetton wallet indeed belongs to the Jetton Master it claims to belong to.
3. Be aware that hostile Jetton Masters/jetton wallets may change their wallets/Masters over time. Therefore, it is imperative that users do their due diligence and check the legitimacy of any wallets they interact with prior to each use.
4. Always ensure that you display jettons in your interface in a manner that will not mix with TON transfers, system notifications, etc.. Even the `symbol`,`name` and `image`
   parameters can be crafted to mislead users, leaving those affected as potential fraud victims. There have been several instances, when malicious jettons were used to impersonate TON transfers, notification errors, reward earnings, or asset freezing announcements.
5. Always be on the lookout for potential malicious actors that create counterfeit jettons, it is always a good idea to give users the functionality needed to eliminate unwanted jettons in their main user interface.

Authored by [kosrk](https://github.com/kosrk), [krigga](https://github.com/krigga), [EmelyanenkoK](https://github.com/EmelyanenkoK/) and [tolya-yanot](https://github.com/tolya-yanot/).

## Best Practices

Here we have provided several examples of jetton code processing created by TON Community members:

<Tabs groupId="code-examples">
<TabItem value="tonweb" label="JS (tonweb)">

```js
my_wallet = Wallet(provider=client, mnemonics=my_wallet_mnemonics, version='v4r2')

# 对于TonCenterClient和LsClient
await my_wallet.transfer_jetton(destination_address='address', jetton_master_address=jetton.address, jettons_amount=1000, fee=0.15) 

# 对于所有客户端
await my_wallet.transfer_jetton_by_jetton_wallet(destination_address='address', jetton_wallet='your jetton wallet address', jettons_amount=1000, fee=0.1)  
```


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


<TabItem value="TonTools" label="Python">

```py
my_wallet = Wallet(provider=client, mnemonics=my_wallet_mnemonics, version='v4r2')

# for TonCenterClient and LsClient
await my_wallet.transfer_jetton(destination_address='address', jetton_master_address=jetton.address, jettons_amount=1000, fee=0.15) 

# for all clients
await my_wallet.transfer_jetton_by_jetton_wallet(destination_address='address', jetton_wallet='your jetton wallet address', jettons_amount=1000, fee=0.1)  
```




### Jetton Transfer with Comment parse

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

## See Also

- [Payments Processing](/develop/dapps/asset-processing/)
- [NFT processing on TON](/develop/dapps/asset-processing/nfts)
- [Metadata parsing on TON](/develop/dapps/asset-processing/metadata)
