# TON HTTP API

:::tip

There are different ways to connect to blockchain:

1. **RPC data provider or another API**: in most cases, you have to _rely_ on its stability and security.
2. ADNL connection: you're connecting to a [liteserver](/participate/run-nodes/liteserver). They might be inaccessible, but with a certain level of validation (implemented in the library), cannot lie.
3. Tonlib binary: you're connecting to liteserver as well, so all benefits and downsides apply, but your application also contains a dynamic-loading library compiled outside.
4. Offchain-only. Such SDKs allow to create and serialize cells, which you can then send to APIs.

:::

## 优点和缺点

- ✅ 习惯性且适合快速入门，这对于每个想要尝试TON的新手来说是完美的。

- ✅ Web-oriented. Perfect to load data of TON smart contracts from Web, also allows to send messages there.

- ❌ Simplified. ❌ 简化。无法接收需要索引TON API的信息。

- ❌ HTTP-Middleware. ❌ HTTP中间件。您不能完全信任服务器响应，因为它们不包含_Merkle证明_来验证您的数据是真实的。

## RPC 节点

- [GetBlock节点](https://getblock.io/nodes/ton/) — 使用GetBlocks节点连接和测试您的dApps
- [TON Access](https://www.orbs.com/ton-access/) - The Open Network (TON)的HTTP API。
- [Toncenter](https://toncenter.com/api/v2/) — 社区托管的项目，用于API快速入门。（获取API密钥 [@tonapibot](https://t.me/tonapibot)） 获取Mainnet和Testnet的API密钥：[@tonapibot](https://t.me/tonapibot)
- [ton-node-docker](https://github.com/fmira21/ton-node-docker) - [⭐新] Docker全节点和Toncenter API。
- [toncenter/ton-http-api](https://github.com/toncenter/ton-http-api) — 运行您自己的RPC节点。
- [nownodes.io](https://nownodes.io/nodes) — 通过API使用NOWNodes全节点和blockbook探索器。
- [Chainbase](https://chainbase.com/chainNetwork/TON) — The Open Network的节点API和数据基础设施。

## Indexer

### Toncenter TON Index

Indexers allow to list jetton wallets, NFTs, transactions by certain filters, not only retrieve specific ones.

- 使用公共TON Index进行测试和开发，免费版或适用生产环境的高级版 - [toncenter.com/api/v3/](https://toncenter.com/api/v3/)
- 使用[Worker](https://github.com/toncenter/ton-index-worker/tree/36134e7376986c5517ee65e6a1ddd54b1c76cdba)和[TON Index API包装器](https://github.com/toncenter/ton-indexer)运行您自己的TON Index。

### GraphQL Nodes

GraphQL nodes act as indexers as well.

- [tvmlabs.io](https://ton-testnet.tvmlabs.dev/graphql) (for TON, testnet only at the moment of writing) - has wide variety of transaction/block data, ways to filter it, etc.
- [dton.io](https://dton.io/graphql) - as well as providing contracts data augmented with parsed "is jetton", "is NFT" flags, allows emulating transactions and receiving execution traces.

## Other APIs

- [TonAPI](https://docs.tonconsole.com/tonapi/api-v2) - API that is designed to provide users with a streamlined experience, not worrying about low-level details of smart contracts.
