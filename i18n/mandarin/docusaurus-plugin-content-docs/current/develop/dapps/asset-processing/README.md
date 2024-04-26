import Button from '@site/src/components/button'

# 支付处理

本页面包含了关于在TON区块链上处理（发送和接收）数字资产的概览和具体细节。

:::info 如果这10笔交易都是未见过的，应加载接下来的10笔交易，重复步骤2、3、4、5。
TON transactions are irreversible after just one confirmation. For the best user experience, it is suggested to avoid waiting on additional blocks once transactions are finalized on the TON Blockchain. Read more in the [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3).
:::

## Best Practices

### 基于 Seqno 的钱包

- [创建密钥对、钱包并获取钱包地址](https://github.com/toncenter/examples/blob/main/common.js)

### 关于Toncoin处理的最佳实践和评论：

#### 本地代币，这是可以附加到网络上任何消息的特殊类型资产。由于发行新本地代币的功能已关闭，这些资产目前未被使用。

:::info
It is suggested to accept deposits across multiple wallets on your side.
:::

- [JS代码接受Toncoin存款](https://github.com/toncenter/examples/blob/main/deposits.js)

#### 关于处理jettons的最佳实践：

- 向计算出的地址发送一些Toncoin。注意，您需要以`non-bounce`模式发送它们，因为该地址尚无代码，因此无法处理传入消息。`non-bounce`标志表示，即使处理失败，资金也不应通过反弹消息返回。我们不建议对其他交易使用`non-bounce`标志，尤其是在处理大笔资金时，因为反弹机制提供了一定程度的防错保护。

- [JS代码从钱包中提取（发送）Toncoins](https://github.com/toncenter/examples/blob/main/withdrawals.js)

- [详细信息](https://docs.ton.org/develop/dapps/asset-processing#global-overview)

### Jetton

#### Jetton Deposits

:::info
It is suggested to accept deposits across multiple wallets on your side.
:::

- [JS代码接受jettons存款](https://github.com/toncenter/examples/blob/main/deposits-jettons.js)

#### Jetton Withdrawals

- [JS代码从钱包中提取（发送）jettons](https://github.com/toncenter/examples/blob/main/withdrawals-jettons.js)

- 如果您需要为简单用户流程进行简便集成，使用ton://链接是合适的。
  最适合一次性支付和发票。

- [详细信息](https://docs.ton.org/develop/dapps/asset-processing/jettons)

## 其他示例

### 自托管服务

#### 社区制作

[Gobicycle](https://github.com/gobicycle/bicycle) 服务专注于补充用户余额和向区块链账户发送支付。支持TONs和Jettons。该服务考虑了开发人员可能遇到的许多陷阱（所有jettons的检查、正确的操作状态检查、消息重发、区块链被分片时的高负载性能）。提供简单的HTTP API、rabbit和webhook通知新支付。 Both TONs and Jettons are supported. The service is written with numerous pitfalls in mind that a developer might encounter (all checks for jettons, correct operations status check, resending messages, performance during high load when blockchain is splitted by shards). Provide simple HTTP API, rabbit and webhook notifications about new payments.

### JavaScript

#### 社区制作

使用TON社区支持的ton.js SDK：

- [创建钱包，获取余额，进行转账](https://github.com/ton-community/ton#usage)

### Python

#### 社区制作

使用psylopunk/pytonlib（The Open Network的简单Python客户端）：

- [发送交易](https://github.com/psylopunk/pytonlib/blob/main/examples/transactions.py)

使用tonsdk库（类似于tonweb）：

- [初始化钱包，创建外部消息部署钱包](https://github.com/tonfactory/tonsdk#create-mnemonic-init-wallet-class-create-external-message-to-deploy-the-wallet)

### Golang

#### 社区制作

- [查看完整示例列表](https://github.com/xssnick/tonutils-go#how-to-use)

## 全局概览

Embodying a fully asynchronous approach, TON Blockchain involves a few concepts which are uncommon to traditional blockchains. Particularly, each interaction of any actor with the blockchain consists of a graph of asynchronously transferred messages between smart contracts and/or the external world. The common path of any interaction starts with an external message sent to a `wallet` smart contract, which authenticates the message sender using public-key cryptography, takes charge of fee payment, and sends inner blockchain messages. That way, transactions on the TON network are not synonymous with user interaction with the blockchain but merely nodes of the message graph: the result of accepting and processing a message by a smart contract, which may or may not lead to the emergence of new messages. The interaction may consist of an arbitrary number of messages and transactions and span a prolonged period of time. Technically, transactions with queues of messages are aggregated into blocks processed by validators. The asynchronous nature of the TON Blockchain **does not allow to predict the hash and lt (logical time) of a transaction** at the stage of sending a message. The transaction accepted to the block is final and cannot be modified.

**每个内部区块链消息都是从一个智能合约到另一个智能合约的消息，携带一定数量的数字资产以及任意部分数据。**

智能合约指南建议将以32个二进制零开头的数据负载视为可读文本消息。大多数软件，如钱包和库，支持此规范，并允许在Toncoin中发送文本评论以及显示其他消息中的评论。 Most software, such as wallets and libraries, support this specification and allow to send text comments along with Toncoin as well as display comments in other messages.

智能合约**支付交易费用**（通常来自输入消息的余额）以及**存储合约存储的代码和数据的存储费用**。费用取决于workchain配置，`masterchain`上的最大费用明显低于`basechain`。 Fees depend on workchain configs with maximal fees on `masterchain` and substantially lower fees on `basechain`.

## TON 上的数字资产

TON拥有三种类型的数字资产。

- Toncoin，网络的主要代币。它用于区块链上的所有基本操作，例如支付gas费或用于验证的质押。 It is used for all basic operations on the blockchain, for example, paying gas fees or staking for validation.
- Native tokens, which are special kinds of assets that can be attached to any message on the network. These assets are currently not in use since the functionality for issuing new native tokens is closed.
- Contract assets, such as tokens and NFTs, which are analogous to the ERC-20/ERC-721 standards and are managed by arbitrary contracts and thus can require custom rules for processing. 合约资产，如代币和NFT，类似于ERC-20/ERC-721标准，由任意合约管理，因此可能需要自定义处理规则。你可以在[处理NFTs](/develop/dapps/asset-processing/nfts)和[处理Jettons](/develop/dapps/asset-processing/jettons)文章中找到更多信息。

### 简单的 Toncoin 转账

要发送Toncoin，用户需要通过外部消息发送请求，即从外部世界到区块链的消息，到一个特殊的`钱包`智能合约（见下文）。接收到此请求后，`钱包`将发送带有所需资产量和可选数据负载的内部消息，例如文本评论。 Upon receiving this request, `wallet` will send an inner message with the desired amount of assets and optional data payload, for instance a text comment.

## 钱包智能合约

钱包智能合约是TON网络上的合约，其任务是允许区块链外的参与者与区块链实体互动。通常，它解决三个挑战： Generally, it solves three challenges:

- 认证所有者：拒绝处理和支付非所有者请求的费用。
- 重放保护：禁止重复执行一个请求，例如向某个智能合约发送资产。
- 启动与其他智能合约的任意互动。

解决第一个挑战的标准解决方案是公钥密码学：`钱包`存储公钥并检查传入消息是否由相应的私钥签名，而该私钥仅由所有者知晓。第三个挑战的解决方案也很常见；通常，请求包含`钱包`向网络发送的完整内部消息。然而，对于重放保护，有几种不同的方法。 The solution to the third challenge is common as well; generally, a request contains a fully formed inner message `wallet` sends to the network. However, for replay protection, there are a few different approaches.

### 基于Seqno的钱包采用最简单的消息排序方法。每条消息都有一个特殊的`seqno`整数，必须与`钱包`智能合约中存储的计数器相符。`钱包`在每个请求上更新其计数器，从而确保一个请求不会被重复处理。有几个`钱包`版本在公开可用方法方面有所不同：限制请求的过期时间的能力，以及拥有相同公钥的多个钱包的能力。然而，这种方法的固有要求是逐一发送请求，因为`seqno`序列中的任何间隙都将导致无法处理所有后续请求。

Seqno-based wallets follow the most simple approach to sequencing messages. Each message has a special `seqno` integer that must coincide with the counter stored in the `wallet` smart contract. `wallet` updates its counter on each request, thus ensuring that one request will not be processed twice. There are a few `wallet` versions that differ in publicly available methods: the ability to limit requests by expiration time, and the ability to have multiple wallets with the same public key. However, an inherent requirement of that approach is to send requests one by one, since any gap in `seqno` sequence will result in the inability to process all subsequent requests.

### 高负载钱包

This `wallet` type follows an approach based on storing the identifier of the non-expired processed requests in smart-contract storage. In this approach, any request is checked for being a duplicate of an already processed request and, if a replay is detected, dropped. Due to expiration, the contract may not store all requests forever, but it will remove those that cannot be processed due to the expiration limit. Requests to this `wallet` may be sent in parallel without interfering with each other; however, this approach requires more sophisticated monitoring of request processing.

## 与区块链的互动

Basic operations on TON Blockchain can be carried out via TonLib. It is a shared library which can be compiled along with a TON node and expose APIs for interaction with the blockchain via so-called lite servers (servers for lite clients). TonLib follows a trustless approach by checking proofs for all incoming data; thus, there is no necessity for a trusted data provider. 可以通过TonLib在TON区块链上进行基本操作。TonLib是一个共享库，可以与TON节点一起编译，并通过所谓的lite服务器（轻客户端服务器）公开API以与区块链互动。TonLib通过检查所有传入数据的证明采取无信任方法；因此，不需要可信数据提供者。TonLib的可用方法列在[TL方案中](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L234)。它们可以通过像[pyTON](https://github.com/EmelyanenkoK/pyTON)或[tonlib-go](https://github.com/mercuryoio/tonlib-go/tree/master/v2)（技术上这些是`tonlibjson`的包装器）这样的包装器或通过`tonlib-cli`使用共享库。 They can be used either as a shared library via wrappers like [pyTON](https://github.com/EmelyanenkoK/pyTON) or [tonlib-go](https://github.com/mercuryoio/tonlib-go/tree/master/v2) (technically those are the wrappers for `tonlibjson`) or through `tonlib-cli`.

## 钱包部署

要通过TonLib部署钱包，需要：

1. 通过[createNewKey](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L213)或其包装函数生成私钥/公钥对（例如在[tonlib-go](https://github.com/mercuryoio/tonlib-go/tree/master/v2#create-new-private-key)中）。注意，私钥是在本地生成的，不会离开主机。 Note that the private key is generated locally and does not leave the host machine.
2. 形成对应于已启用`钱包`之一的[InitialAccountWallet](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L60)结构。目前可用的`wallet.v3`、`wallet.highload.v1`、`wallet.highload.v2`。 Currently `wallet.v3`, `wallet.highload.v1`, `wallet.highload.v2` are available.
3. 通过[getAccountAddress](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L249)方法计算新`钱包`智能合约的地址。我们建议使用默认修订版`0`，并且还在`basechain` `workchain=0`中部署钱包，以降低处理和存储费用。 We recommend using a default revision `0` and also deploying wallets in the basechain `workchain=0` for lower processing and storage fees.
4. 渠道，关于用户地址的信息 Note that you need to send them in `non-bounce` mode since this address has no code yet and thus cannot process incoming messages. `non-bounce` flag indicates that even if processing fails, money should not be returned with a bounce message. We do not recommend using the `non-bounce` flag for other transactions, especially when carrying large sums, since the bounce mechanism provides some degree of protection against mistakes.
5. 形成所需的[action](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L148)，例如仅用于部署的`actionNoop`。然后使用[createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L255)和[sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L260)启动与区块链的互动。 TON区块链采用完全异步的方法，涉及一些与传统区块链不同的概念。特别是，任何参与者与区块链的每次互动都包括在智能合约和/或外部世界之间异步传输消息。任何互动的常见路径始于向`钱包`智能合约发送外部消息，该合约使用公钥密码学认证消息发送者，负责支付费用，并发送内部区块链消息。因此，在TON网络上的交易不等同于用户与区块链的互动，而仅是消息图的节点：智能合约接受和处理消息的结果，可能会或可能不会产生新消息。互动可能包括任意数量的消息和交易，并持续一段较长的时间。技术上，带有消息队列的交易被聚合到由验证者处理的区块中。TON区块链的异步性质**不允许在发送消息阶段预测交易的哈希和lt（逻辑时间）**。被接受到区块中的交易是最终的，且不能被修改。
6. 几秒钟后使用[getAccountState](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L254)方法检查合约。

:::tip
在[钱包教程](/develop/smart-contracts/tutorials/wallet#-deploying-a-wallet)中阅读更多
:::

## 接收消息价值

To calculate the incoming value that the message brings to the contract, one needs to parse the transaction. It happens when the message hits the contract. 可以使用[getTransactions](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L236)获取合约的交易。此方法允许从某个`transactionId`和更早的时间获取10笔交易。要处理所有传入交易，应遵循以下步骤： For an incoming wallet transaction, the correct data consists of one incoming message and zero outgoing messages. /tl/generate/scheme/tonlib_api.tl#L236)获得交易。对于传入钱包的交易，正确的数据包括一个传入消息和零个传出消息。否则，要么是外部消息发送到钱包，在这种情况下，所有者会花费Toncoin，要么钱包未部署，传入交易会反弹回去。

无论如何，一般来说，消息带给合约的金额可以计算为传入消息的价值减去传出消息的价值总和减去费用：`value_{in_msg} - SUM(value_{out_msg}) - fee`。技术上，交易表示包含三个不同的带有`费用`名称的字段：`费用`、`存储费用`和`其他费用`，即总费用、与存储成本相关的费用部分和与交易处理相关的费用部分。只应使用第一个。 Technically, transaction representation contains three different fields with `fee` in name: `fee`, `storage_fee`, and `other_fee`, that is, a total fee, a part of the fee related to storage costs, and a part of the fee related to transaction processing. Only the first one should be used.

## 检查合约的交易

要计算消息带给合约的接收值，需要解析交易。这发生在消息触及合约时。可以使用[getTransactions](https://github.com/ton-blockchain/ton/blob/master This method allows to get 10 transactions from some `transactionId` and earlier. To process all incoming transactions, the following steps should be followed:

1. 最新的`last_transaction_id`可以使用[getAccountState](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L235)获得
2. 应通过`getTransactions`方法加载10笔交易。
3. 应处理此列表中未见过的交易。
4. 传入支付是传入消息具有来源地址的交易；传出支付是传入消息没有来源地址并且还存在传出消息的交易。这些交易应相应处理。 These transactions should be processed accordingly.
5. If all of those 10 transactions are unseen, the next 10 transactions should be loaded and steps 2,3,4,5 should be repeated.

## 接受支付

接受支付有几种方法，它们在区分用户的方法上有所不同。

### 基于发票的方法

要基于附加评论接受支付，服务应：

1. 部署`钱包`合约。
2. Generate a unique `invoice` for each user. String representation of uuid32 will be enough.
3. 用户应被指示向服务的`钱包`合约发送Toncoin，并附加`发票`作为评论。
4. 服务应定期轮询`钱包`合约的getTransactions方法。
5. 对于新交易，应提取传入消息，将`评论`与数据库匹配，并将值（见**接收消息价值**段落）存入用户账户。

## 发票

### 带有ton://链接的发票

If you need an easy integration for a simple user flow, it is suitable to use the ton:// link.
Best suited for one-time payments and invoices.

```bash
ton://transfer/<destination-address>?
    [nft=<nft-address>&]
    [fee-amount=<nanocoins>&]
    [forward-amount=<nanocoins>] 
```

- ✅ 简单集成

- ✅ 无需连接钱包

- ❌ 用户需要为每次支付扫描新的二维码

- ❌ 无法追踪用户是否已签署交易

- ❌ 关于用户地址的信息

- ❌ 在某些平台不可点击此类链接（例如Telegram桌面客户端的机器人消息）时需要变通方法

\<Button href="https://github.com/tonkeeper/wallet-api#payment-urls"
colorType="primary" sizeType={'lg'}>
了解更多 </Button>

### 带有 TON Connect 的发票

最适合需要在会话中签署多个支付/交易的dApps，或需要一段时间保持与钱包的连接。

- ✅ 与钱包有永久通信

- ✅ 用户只需扫描一次二维码

- ✅ 可以了解用户在钱包中是否确认了交易，通过返回的BOC追踪交易

- ✅ 不同平台的现成SDK和UI工具包

- ❌ 如果您只需要发送一次支付，用户需要进行两个操作：连接钱包和确认交易

- ❌ 集成比ton://链接更复杂

\<Button href="/develop/dapps/ton-connect/"
colorType="primary" sizeType={'lg'}>
了解更多 </Button>

## 发送支付

1. 服务应部署`钱包`并保持其资金，以防止合约因存储费用而被销毁。注意，存储费通常少于每年1 Toncoin。 Note that storage fees are generally less than 1 Toncoin per year.
2. 服务应从用户获取`destination_address`和可选的`comment`。注意，目前我们建议要么禁止未完成的同一(`destination_address`、`value`、`comment`)集合的传出支付，要么适当安排这些支付；这样，下一个支付只有在前一个确认后才启动。 Note that for the meantime, we recommend either prohibiting unfinished outgoing payments with the same (`destination_address`, `value`, `comment`) set or proper scheduling of those payments; that way, the next payment is initiated only after the previous one is confirmed.
3. 用`comment`作为文本形成[msg.dataText](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L98)。
4. 形成包含`destination_address`、空`public_key`、`amount`和`msg.dataText`的[msg.message](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L108)。
5. 形成包含一组传出消息的[Action](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L149)。
6. 使用[createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L255)和[sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L260)查询发送传出支付。
7. 这种类型的`钱包`采用基于存储智能合约存储中非过期处理请求的标识符的方法。在这种方法中，任何请求都会被检查是否是已处理请求的重复，如果检测到重放，则丢弃。由于过期，合约可能不会永远存储所有请求，但它会删除由于过期限制而无法处理的请求。向此`钱包`发送请求可以并行进行，彼此不干扰；然而，这种方法需要更复杂的请求处理监控。 服务应定期轮询`钱包`合约的getTransactions方法。通过(`destination_address`、`value`、`comment`)匹配确认的交易与传出支付，可以将支付标记为完成；检测并向用户显示相应的交易哈希和lt（逻辑时间）。
8. 对`v3`或`high-load`钱包的请求默认有60秒的过期时间。在此时间后，未处理的请求可以安全地重新发送到网络（见步骤3-6）。 After that time unprocessed requests can be safely resent to the network (see steps 3-6).

## 浏览器

区块链浏览器是https://tonscan.org。

To generate a transaction link in the explorer, the service needs to get the lt (logic time), transaction hash, and account address (account address for which lt and txhash were retrieved via the getTransactions method). 要在浏览器中生成交易链接，服务需要获取lt（逻辑时间）、交易哈希和账户地址（通过getTransactions方法检索到的用于lt和txhash的账户地址）。然后https://tonscan.org和https://explorer.toncoin.org/可以以以下格式显示该tx的页面：

为每个用户生成唯一的`发票`。uuid32的字符串表示形式就足够了。

`https://tonscan.org/tx/{lt as int}:{txhash as base64url}:{account address}`

`https://explorer.toncoin.org/transaction?account={account address}&lt={lt as int}&hash={txhash as base64url}`
