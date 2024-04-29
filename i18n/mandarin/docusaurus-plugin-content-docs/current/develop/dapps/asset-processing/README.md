import Button from '@site/src/components/button'

# 支付处理

本页面包含了关于在TON区块链上处理（发送和接收）数字资产的概览和具体细节。

:::info Transaction Confirmation
TON transactions are irreversible after just one confirmation. For the best user experience, it is suggested to avoid waiting on additional blocks once transactions are finalized on the TON Blockchain. Read more in the [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3).
:::

## Best Practices

### Toncoin

#### Toncoin Deposits

:::info
It is suggested to set several MEMO deposit wallets for better performance.
:::

- [MEMO Deposits](https://github.com/toncenter/examples/blob/main/deposits.js)

#### 社区制作

- [Batched withdrawals](https://github.com/toncenter/examples/blob/main/withdrawals-highload-batch.js)

- [Withdrawals](https://github.com/toncenter/examples/blob/main/withdrawals-highload.js)

- [Detailed info](/develop/dapps/asset-processing#global-overview)

### JavaScript

- [Read Jetton Proccesing](/develop/dapps/asset-processing/jettons)

### Made by TON Community

#### GO

- [Gobicycle](https://github.com/gobicycle/bicycle) - service is focused on replenishing user balances and sending payments to blockchain accounts. Both TONs and Jettons are supported. The service is written with numerous pitfalls in mind that a developer might encounter (all checks for jettons, correct operations status check, resending messages, performance during high load when blockchain is splitted by shards). Provide simple HTTP API, rabbit and webhook notifications about new payments.
- [GO examples](https://github.com/xssnick/tonutils-go#how-to-use)

#### 社区制作

使用psylopunk/pytonlib（The Open Network的简单Python客户端）：

- [发送交易](https://github.com/psylopunk/pytonlib/blob/main/examples/transactions.py)
- [Create a wallet, get its balance, make a transfer](https://github.com/ton-community/ton#usage)

#### Python

Using tonsdk library (similar to tonweb):

- [Init wallet, create external message to deploy the wallet](https://github.com/tonfactory/tonsdk#create-mnemonic-init-wallet-class-create-external-message-to-deploy-the-wallet)

## 社区制作

Embodying a fully asynchronous approach, TON Blockchain involves a few concepts which are uncommon to traditional blockchains. Particularly, each interaction of any actor with the blockchain consists of a graph of asynchronously transferred messages between smart contracts and/or the external world. The common path of any interaction starts with an external message sent to a `wallet` smart contract, which authenticates the message sender using public-key cryptography, takes charge of fee payment, and sends inner blockchain messages. That way, transactions on the TON network are not synonymous with user interaction with the blockchain but merely nodes of the message graph: the result of accepting and processing a message by a smart contract, which may or may not lead to the emergence of new messages. The interaction may consist of an arbitrary number of messages and transactions and span a prolonged period of time. Technically, transactions with queues of messages are aggregated into blocks processed by validators. The asynchronous nature of the TON Blockchain **does not allow to predict the hash and lt (logical time) of a transaction** at the stage of sending a message. The transaction accepted to the block is final and cannot be modified.

**Each inner blockchain message is a message from one smart contract to another, which bears some amount of digital assets, as well as an arbitrary portion of data.**

TON区块链采用完全异步的方法，涉及一些与传统区块链不同的概念。特别是，任何参与者与区块链的每次互动都包括在智能合约和/或外部世界之间异步传输消息。任何互动的常见路径始于向`钱包`智能合约发送外部消息，该合约使用公钥密码学认证消息发送者，负责支付费用，并发送内部区块链消息。因此，在TON网络上的交易不等同于用户与区块链的互动，而仅是消息图的节点：智能合约接受和处理消息的结果，可能会或可能不会产生新消息。互动可能包括任意数量的消息和交易，并持续一段较长的时间。技术上，带有消息队列的交易被聚合到由验证者处理的区块中。TON区块链的异步性质**不允许在发送消息阶段预测交易的哈希和lt（逻辑时间）**。被接受到区块中的交易是最终的，且不能被修改。

**每个内部区块链消息都是从一个智能合约到另一个智能合约的消息，携带一定数量的数字资产以及任意部分数据。**

## Digital assets on TON

智能合约**支付交易费用**（通常来自输入消息的余额）以及**存储合约存储的代码和数据的存储费用**。费用取决于workchain配置，`masterchain`上的最大费用明显低于`basechain`。

- Toncoin, the main token of the network. It is used for all basic operations on the blockchain, for example, paying gas fees or staking for validation.
- Native tokens, which are special kinds of assets that can be attached to any message on the network. These assets are currently not in use since the functionality for issuing new native tokens is closed.
- Contract assets, such as tokens and NFTs, which are analogous to the ERC-20/ERC-721 standards and are managed by arbitrary contracts and thus can require custom rules for processing. You can find more info on it's processin in [process NFTs](/develop/dapps/asset-processing/nfts) and [process Jettons](/develop/dapps/asset-processing/jettons) articles.

### Simple Toncoin transfer

To send Toncoin, the user needs to send a request via an external message, that is, a message from the outside world to the blockchain, to a special `wallet` smart contract (see below). Upon receiving this request, `wallet` will send an inner message with the desired amount of assets and optional data payload, for instance a text comment.

## 简单的 Toncoin 转账

要发送Toncoin，用户需要通过外部消息发送请求，即从外部世界到区块链的消息，到一个特殊的`钱包`智能合约（见下文）。接收到此请求后，`钱包`将发送带有所需资产量和可选数据负载的内部消息，例如文本评论。

- authenticates owner: Rejects to process and pay fees for non-owners' requests.
- replays protection: Prohibits the repetitive execution of one request, for instance sending assets to some other smart contract.
- initiates arbitrary interaction with other smart contracts.

钱包智能合约是TON网络上的合约，其任务是允许区块链外的参与者与区块链实体互动。通常，它解决三个挑战：

### Seqno-based wallets

解决第一个挑战的标准解决方案是公钥密码学：`钱包`存储公钥并检查传入消息是否由相应的私钥签名，而该私钥仅由所有者知晓。第三个挑战的解决方案也很常见；通常，请求包含`钱包`向网络发送的完整内部消息。然而，对于重放保护，有几种不同的方法。

### 基于 Seqno 的钱包

基于Seqno的钱包采用最简单的消息排序方法。每条消息都有一个特殊的`seqno`整数，必须与`钱包`智能合约中存储的计数器相符。`钱包`在每个请求上更新其计数器，从而确保一个请求不会被重复处理。有几个`钱包`版本在公开可用方法方面有所不同：限制请求的过期时间的能力，以及拥有相同公钥的多个钱包的能力。然而，这种方法的固有要求是逐一发送请求，因为`seqno`序列中的任何间隙都将导致无法处理所有后续请求。

## 高负载钱包

这种类型的`钱包`采用基于存储智能合约存储中非过期处理请求的标识符的方法。在这种方法中，任何请求都会被检查是否是已处理请求的重复，如果检测到重放，则丢弃。由于过期，合约可能不会永远存储所有请求，但它会删除由于过期限制而无法处理的请求。向此`钱包`发送请求可以并行进行，彼此不干扰；然而，这种方法需要更复杂的请求处理监控。

## 与区块链的互动

可以通过TonLib在TON区块链上进行基本操作。TonLib是一个共享库，可以与TON节点一起编译，并通过所谓的lite服务器（轻客户端服务器）公开API以与区块链互动。TonLib通过检查所有传入数据的证明采取无信任方法；因此，不需要可信数据提供者。TonLib的可用方法列在[TL方案中](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L234)。它们可以通过像[pyTON](https://github.com/EmelyanenkoK/pyTON)或[tonlib-go](https://github.com/mercuryoio/tonlib-go/tree/master/v2)（技术上这些是`tonlibjson`的包装器）这样的包装器或通过`tonlib-cli`使用共享库。

1. Generate a private/public key pair via [createNewKey](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L213) or its wrapper functions (example in [tonlib-go](https://github.com/mercuryoio/tonlib-go/tree/master/v2#create-new-private-key)). Note that the private key is generated locally and does not leave the host machine.
2. Form [InitialAccountWallet](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L60) structure corresponding to one of the enabled `wallets`. Currently `wallet.v3`, `wallet.highload.v1`, `wallet.highload.v2` are available.
3. Calculate the address of a new `wallet` smart contract via the [getAccountAddress](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L249) method. We recommend using a default revision `0` and also deploying wallets in the basechain `workchain=0` for lower processing and storage fees.
4. Send some Toncoin to the calculated address. Note that you need to send them in `non-bounce` mode since this address has no code yet and thus cannot process incoming messages. `non-bounce` flag indicates that even if processing fails, money should not be returned with a bounce message. We do not recommend using the `non-bounce` flag for other transactions, especially when carrying large sums, since the bounce mechanism provides some degree of protection against mistakes.
5. Form the desired [action](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L148), for instance `actionNoop` for deploy only. Then use [createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L255) and [sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L260) to initiate interactions with the blockchain.
6. Check the contract in a few seconds with [getAccountState](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L254) method.

:::tip
Read more in the [Wallet Tutorial](/develop/smart-contracts/tutorials/wallet#-deploying-a-wallet)
:::

## Incoming message value

To calculate the incoming value that the message brings to the contract, one needs to parse the transaction. It happens when the message hits the contract. A transaction can be obtained using [getTransactions](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L236). For an incoming wallet transaction, the correct data consists of one incoming message and zero outgoing messages. Otherwise, either an external message is sent to the wallet, in which case the owner spends Toncoin, or the wallet is not deployed and the incoming transaction bounces back.

Anyway, in general, the amount that a message brings to the contract can be calculated as the value of the incoming message minus the sum of the values of the outgoing messages minus the fee: `value_{in_msg} - SUM(value_{out_msg}) - fee`. Technically, transaction representation contains three different fields with `fee` in name: `fee`, `storage_fee`, and `other_fee`, that is, a total fee, a part of the fee related to storage costs, and a part of the fee related to transaction processing. Only the first one should be used.

## Checking contract's transactions

/tl/generate/scheme/tonlib_api.tl#L236)获得交易。对于传入钱包的交易，正确的数据包括一个传入消息和零个传出消息。否则，要么是外部消息发送到钱包，在这种情况下，所有者会花费Toncoin，要么钱包未部署，传入交易会反弹回去。

1. The latest `last_transaction_id` can be obtained using [getAccountState](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L235)
2. List of 10 transactions should be loaded via the `getTransactions` method.
3. Unseen transactions from this list should be processed.
4. Incoming payments are transactions in which the incoming message has a source address; outgoing payments are transactions in which the incoming message has no source address and also presents the outgoing messages. These transactions should be processed accordingly.
5. If all of those 10 transactions are unseen, the next 10 transactions should be loaded and steps 2,3,4,5 should be repeated.

## 检查合约的交易

可以使用[getTransactions](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L236)获取合约的交易。此方法允许从某个`transactionId`和更早的时间获取10笔交易。要处理所有传入交易，应遵循以下步骤：

### Invoice-based approach

To accept payments based on attached comments, the service should

1. Deploy the `wallet` contract.
2. Generate a unique `invoice` for each user. String representation of uuid32 will be enough.
3. Users should be instructed to send Toncoin to the service's `wallet` contract with an attached `invoice` as a comment.
4. Service should regularly poll the getTransactions method for the `wallet` contract.
5. For new transactions, the incoming message should be extracted, `comment` matched against the database, and the value (see **Incoming message value** paragraph) deposited to the user's account.

## 基于发票的方法

### Invoices with ton:// link

If you need an easy integration for a simple user flow, it is suitable to use the ton:// link.
Best suited for one-time payments and invoices.

```bash
ton://transfer/<destination-address>?
    [nft=<nft-address>&]
    [fee-amount=<nanocoins>&]
    [forward-amount=<nanocoins>] 
```

- ✅ Easy integration

- ✅ No need to connect a wallet

- ❌ Users need to scan a new QR code for each payment

- ❌ It's not possible to track whether the user has signed the transaction or not

- ❌ No information about the user's address

- ❌ Workarounds are needed on platforms where such links are not clickable (e.g. messages from bots for Telegram desktop clients )

如果您需要为简单用户流程进行简便集成，使用ton://链接是合适的。
最适合一次性支付和发票。

### Invoices with TON Connect

Best suited for dApps that need to sign multiple payments/transactions within a session or need to maintain a connection to the wallet for some time.

- ✅ There's a permanent communication channel with the wallet, information about the user's address

- ✅ Users only need to scan a QR code once

- ✅ It's possible to find out whether the user confirmed the transaction in the wallet, track the transaction by the returned BOC

- ✅ Ready-made SDKs and UI kits are available for different platforms

- ❌ If you only need to send one payment, the user needs to take two actions: connect the wallet and confirm the transaction

- ❌ Integration is more complex than the ton:// link

\<Button href="/develop/dapps/ton-connect/"
colorType="primary" sizeType={'lg'}>
Learn More </Button>

## Sending payments

1. ✅ 与钱包有永久通信
2. Service should get from the user `destination_address` and optional `comment`. Note that for the meantime, we recommend either prohibiting unfinished outgoing payments with the same (`destination_address`, `value`, `comment`) set or proper scheduling of those payments; that way, the next payment is initiated only after the previous one is confirmed.
3. Form [msg.dataText](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L98) with `comment` as text.
4. Form [msg.message](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L108) which contains `destination_address`, empty `public_key`, `amount` and `msg.dataText`.
5. Form [Action](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L149) which contains a set of outgoing messages.
6. Use [createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L255) and [sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L260) queries to send outgoing payments.
7. Service should regularly poll the getTransactions method for the `wallet` contract. Matching confirmed transactions with the outgoing payments by (`destination_address`, `value`, `comment`) allows to mark payments as finished; detect and show the user the corresponding transaction hash and lt (logical time).
8. Requests to `v3` of `high-load` wallets have an expiration time equal to 60 seconds by default. After that time unprocessed requests can be safely resent to the network (see steps 3-6).

## Explorers

The blockchain explorer is https://tonscan.org.

\<Button href="/develop/dapps/ton-connect/"
colorType="primary" sizeType={'lg'}>
了解更多 </Button>

`https://tonviewer.com/transaction/{txhash as base64url}`

`https://tonscan.org/tx/{lt as int}:{txhash as base64url}:{account address}`

`https://explorer.toncoin.org/transaction?account={account address}&lt={lt as int}&hash={txhash as base64url}`
