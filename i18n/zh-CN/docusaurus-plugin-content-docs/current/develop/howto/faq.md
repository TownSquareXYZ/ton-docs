# 常见问题解答

本节涵盖了关于TON区块链最受欢迎的问题。

## 概述

### 能分享一下关于 TON 的简要概述吗？

- [The Open Network简介](/learn/introduction)
- [TON区块链基于PoS共识](https://blog.ton.org/the-ton-blockchain-is-based-on-pos-consensus)
- [TON白皮书](/learn/docs)

### TON 与 EVM 区块链的主要相似之处和不同之处是什么？

- [从以太坊到TON](/learn/introduction#ethereum-to-ton)
- [TON、Solana和以太坊2.0的比较](https://ton.org/comparison_of_blockchains.pdf)

### TON 有测试环境吗？

- [Testnet测试网](/develop/smart-contracts/environment/testnet)

## 区块

### 获取区块信息的RPC方法是什么？

验证者生产区块。现有区块通过Liteservers可用。Liteservers通过轻客户端访问。在轻客户端之上构建了第三方工具，如钱包、浏览器、dapps等。

1. 要访问轻客户端核心，请查看我们GitHub的这个部分：[ton-blockchain/tonlib](https://github.com/ton-blockchain/ton/tree/master/tonlib)
2. Workchains support cross-shard activity, which means that users can interact between different shardchains or workchains within the same network. In current L2 solutions, cross-shard operations are often complex and require additional bridges or interoperability solutions. In TON, for example, users can easily exchange tokens or perform other transactions between different shardchains without complex procedures.
3. Scalability is one of the main challenges for modern blockchain systems. In traditional L2 solutions, scalability is limited by the capacity of the sequencer. If the TPS (transactions per second) on L2 exceeds the sequencer's capacity, it can lead to problems. In workchains in TON, this problem is solved by dividing the shard. When the load on a shard exceeds its capacity, the shard is automatically divided into two or more shards, allowing the system to scale almost without limit.

### Is there a need for L2 on the TON?

At any transaction cost, there will always be applications that cannot sustain such a fee but can function at a much lower cost. Similarly, regardless of the latency achieved, there will always be applications that require even lower latency. Therefore, it is conceivable that there might eventually be a need for L2 solutions on the TON platform to cater to these specific requirements.

## MEV

### 区块时间

*2-5秒*

In addition, the current TON architecture lacks a market-based mechanism for determining transaction fees. Commissions are fixed and not subject to change depending on transaction priorities, which makes frontrunning less attractive. Because of the fixed fees and deterministic order of transactions, it is non-trivial to do frontrunning in TON.

## 最终确定时间

### 获取区块信息的RPC方法是什么？

验证者生产区块。现有区块通过Liteservers可用。Liteservers通过轻客户端访问。在轻客户端之上构建了第三方工具，如钱包、浏览器、dapps等。

- 要访问轻客户端核心，请查看我们GitHub的这个部分：[ton-blockchain/tonlib](https://github.com/ton-blockchain/ton/tree/master/tonlib)

此外，这里有三个高级第三方区块浏览器：

- https://explorer.toncoin.org/last
- https://toncenter.com/
- https://tonwhales.com/explorer

在我们文档的[Explorers in TON](/participate/explorers)部分阅读更多。

### 区块时间

*2-5秒*

:::info
通过阅读我们在[ton.org/analysis](https://ton.org/analysis)上的分析，比较TON的链上指标，包括区块时间和最终确定时间。
:::

### 获取交易数据的RPC方法是什么？

*小于6秒*

:::info
通过阅读我们在[ton.org/analysis](https://ton.org/analysis)上的分析，比较TON的链上指标，包括区块时间和最终确定时间。
:::

### 平均区块大小

```bash
max block size param 29
max_block_bytes:2097152
```

:::info
在[Network Configs](/develop/howto/network-configs)中找到更多实际参数。
:::

### TON 上的区块布局是怎样的？

钱包合约转账的示例（低层级）：

- https://github.com/xssnick/tonutils-go/blob/master/example/wallet/main.go

## 是否可以确定交易100%完成？查询交易级数据是否足以获得这些信息？

### 获取交易数据的RPC方法是什么？

- [请参见上面的答案](/develop/howto/faq#are-there-any-standardized-protocols-for-minting-burning-and-transferring-fungible-and-non-fungible-tokens-in-transactions)

### TON 交易是异步的还是同步的？是否有文档显示这个系统是如何工作的？

TON区块链消息是异步的：

- 发送者准备交易正文（消息boc）并通过轻客户端（或更高级工具）广播
- 轻客户端返回广播状态，而非执行交易的结果
- 发送者通过监听目标账户（地址）状态或整个区块链状态来检查期望结果

使用一个与钱包智能合约相关的例子来解释TON异步消息传递是如何工作的：

- [TON钱包如何工作，以及如何使用JavaScript访问它们](https://blog.ton.org/how-ton-wallets-work-and-how-to-access-them-from-javascript#1b-sending-a-transfer)

是的，TON上可以通过两种不同的方式实现交易批量处理：

- 通过利用TON的异步特性，即向网络发送独立的交易

### 是否可以确定交易100%完成？查询交易级数据是否足以获得这些信息？

\*\*简短回答：\*\*要确保交易已完成，必须检查接收者的账户。

默认钱包（v3/v4）也支持在一笔交易中发送多达4条消息。

- Go: [钱包示例](https://github.com/xssnick/tonutils-go/blob/master/example/wallet/main.go)
- Python: [带支付的Storefront bot](/develop/dapps/tutorials/accept-payments-in-a-telegram-bot)
- JavaScript: [饺子销售机器人](/develop/dapps/tutorials/accept-payments-in-a-telegram-bot-js)

### TON 的货币精度是多少？

*9位小数*

- [交易布局](/develop/data-formats/transaction-layout)

### 是否有标准化的协议用于铸造、销毁和交易中转移可替代和不可替代代币？

非同质化代币（NFT）：

- [TEP-62：NFT标准](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md)
- [NFT文档](/develop/dapps/defi/tokens#nft)

Jettons（代币）：

- [TEP-74：Jettons标准](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md)

其他标准：

## 标准

### 是否有用 Jettons（代币）和 NFT 解析事件的示例？

在TON上，所有数据都以boc消息的形式传输。这意味着在交易中使用NFT并不是特殊事件。相反，它是发送给或从（NFT或钱包）合约接收的常规消息，就像涉及标准钱包的交易一样。

:::info
Mainnet支持的小数位数：9位。
:::

### 是否有标准化的协议用于在交易中铸造、销毁和转移可替代和不可替代代币？

要更好地理解这个过程是如何工作的，请参阅[支付处理](/develop/dapps/asset-processing/)部分。

- [TEP-62：NFT标准](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md)
- [NFT文档](/develop/dapps/defi/tokens#nft)

Jettons（代币）：

- [智能合约地址](/learn/overviews/addresses)
- [分布式 TON 代币概述](https://telegra.ph/Scalable-DeFi-in-TON-03-30)
- [可替代代币文档（Jettons）](/develop/dapps/defi/tokens#jettons)

其他标准：

- https://github.com/ton-blockchain/TEPs

### 是否有用 Jettons（代币）和 NFT 解析事件的示例？

在TON上，所有数据都以boc消息的形式传输。这意味着在交易中使用NFT并不是特殊事件。相反，它是发送给或从（NFT或钱包）合约接收的常规消息，就像涉及标准钱包的交易一样。

然而，某些索引的API允许您查看发送到或从合约发送的所有消息，并根据您的特定需求对它们进行过滤。

- https://tonapi.io/swagger-ui

对于**Jettons**合约必须实现[标准的接口](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md)并在_get_wallet_data()_或_get_jetton_data()_方法上返回数据。

## 是否有特殊账户（例如，由网络拥有的账户）与其他账户有不同的规则或方法？

### 地址格式是什么？

- [智能合约地址](/learn/overviews/addresses)

### 是否可以拥有类似于 ENS 的命名账户

是的，请使用TON DNS：

- [TON DNS和域名](/participate/web3/dns)

### 是否可以检测到 TON 上的合约部署事件？

- [一切都是智能合约](/learn/overviews/addresses#everything-is-a-smart-contract)

### 如何判断地址是否为代币地址？

智能合约可以存在于未初始化状态，意味着其状态在区块链中不可用但合约有非零余额。初始状态本身可以稍后通过内部或外部消息发送到网络，因此可以监控这些来检测合约部署。

### Are there any special accounts (e.g. accounts owned by the network) that have different rules or methods from the rest?

There is a special master blockchain inside a TON called Masterchain. It consists of network-wide contracts with network configuration, validator-related contracts, etc:

:::info
Read more about masterchain, workchains and shardchains in TON Blockchain overview article: [Blockchain of Blockchains](/learn/overviews/ton-blockchain).
:::

是的，这是可能的。如果智能合约执行特定指令（`set_code()`），其代码可以被更新并且地址将保持不变。

- [Governance contracts](/develop/smart-contracts/governance)

## 智能合约可以被删除吗？

### Is it possible to detect contract deployment events on TON?

[Everything in TON is a smart contract](/learn/overviews/addresses#everything-is-a-smart-contract).

是的，智能合约地址是区分大小写的，因为它们是使用[base64算法](https://en.wikipedia.org/wiki/Base64)生成的。您可以在[这里](/learn/overviews/addresses)了解更多关于智能合约地址的信息。

Smart contract can exist in uninitialized state, meaning that its state is not available in blockchain but contract has non-zero balance. Initial state itself can be sent to the network later with an internal or external message, so those can be monitored to detect contract deployment.

TVM与以太坊虚拟机（EVM）不兼容，因为TON采用了完全不同的架构（TON是异步的，而以太坊是同步的）。

- [Deploying wallet via TonLib](https://ton.org/docs/develop/dapps/asset-processing/#deploying-wallet)
- [Paying for processing queries and sending responses](https://ton.org/docs/develop/smart-contracts/guidelines/processing)

### 是否可以为 TON 编写 Solidity？

相关地，TON生态系统不支持在以太坊的Solidity编程语言中开发。

但如果您在Solidity语法中添加异步消息并能够与数据进行低层级交互，那么您可以使用FunC。FunC具有大多数现代编程语言通用的语法，并专为TON上的开发设计。

1. Pay attention to projects with a good reputation and well-known development teams.
2. Reputable projects always conduct independent code audits to make sure the code is safe and reliable. Look for projects that have several completed audits from reputable auditing firms.
3. An active community and positive feedback can serve as an additional indicator of a project's reliability.
4. Examine exactly how the project implements the update process. The more transparent and decentralized the process, the less risk to users.

### 推荐的节点提供商用于数据提取包括：

API类型：

Sometimes the logic for updating may exist, but the rights to change the code may be moved to an "empty" address, which also precludes changes.

### Is it possible to re-deploy code to an existing address or does it have to be deployed as a new contract?

Yes, this is possible. If a smart contract carries out specific instructions (`set_code()`) its code can be updated and the address will remain the same.

TON社区项目目录：

### Can smart contract be deleted?

Yes, either as a result of storage fee accumulation (contract needs to reach -1 TON balance to be deleted) or by sending a message with [mode 160](https://docs.ton.org/develop/smart-contracts/messages#message-modes).

### Are smart contract addresses case sensitive?

Yes, smart contract addresses are case sensitive because they are generated using the [base64 algorithm](https://en.wikipedia.org/wiki/Base64).  You can learn more about smart contract addresses [here](/learn/overviews/addresses).

### Is the Ton Virtual Machine (TVM) EVM-compatible?

The TVM is not compatible with the Ethereum Virtual Machine (EVM) because TON leverages a completely different architecture (TON is asynchronous, while Ethereum is synchronous).

[Read more on asynchronous smart contracts](https://telegra.ph/Its-time-to-try-something-new-Asynchronous-smart-contracts-03-25).

### Is it possible to write on Solidity for TON?

Relatedly, the TON ecosystem does not support development in Ethereum’s Solidity programming language.

But if you add asynchronous messages to the Solidity syntax and the ability to interact with data at a low level, then you get FunC. FunC features a syntax that is common to most modern programming languages and is designed specifically for development on TON.

## 远程过程调用(RPC)

### 推荐的节点提供商用于数据提取包括：

API类型：

- 了解更多关于不同[API类型](/develop/dapps/apis/)（索引、HTTP和ADNL）

节点提供商合作伙伴：

- https://toncenter.com/api/v2/
- [getblock.io](https://getblock.io/)
- https://www.orbs.com/ton-access/
- [toncenter/ton-http-api](https://github.com/toncenter/ton-http-api)
- [nownodes.io](https://nownodes.io/nodes)
- https://dton.io/graphql

TON社区项目目录：

- [ton.app](https://ton.app/)

### 以下提供了两个主要资源，用于获取与TON区块链公共节点端点相关的信息（适用于TON Mainnet和TON Testnet）。

- [网络配置](/develop/howto/network-configs)
- [示例和教程](/develop/dapps/#examples)
