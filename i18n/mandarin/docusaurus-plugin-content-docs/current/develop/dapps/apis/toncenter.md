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

- ✅ 面向Web。非常适合与TON交易、智能合约进行Web交互。

- ❌ 简化。无法接收需要索引TON API的信息。

- ❌ HTTP中间件。您不能完全信任服务器响应，因为它们不包含_Merkle证明_来验证您的数据是真实的。

## Toncenter API

- [GetBlock Nodes](https://getblock.io/nodes/ton/) — connect and test your dApps using GetBlocks Nodes
- [TON Access](https://www.orbs.com/ton-access/) - HTTP API for The Open Network (TON).
- [Toncenter](https://toncenter.com/api/v2/) — community-hosted project for Quick Start with API. (Get an API key [@tonapibot](https://t.me/tonapibot))
- [ton-node-docker](https://github.com/fmira21/ton-node-docker) - Docker Full Node and Toncenter API.
- [toncenter/ton-http-api](https://github.com/toncenter/ton-http-api) — run your own RPC node.
- [nownodes.io](https://nownodes.io/nodes) — NOWNodes full Nodes and blockbook Explorers via API.
- [Chainbase](https://chainbase.com/chainNetwork/TON) — Node API and data infrastructure for The Open Network.

## Indexer

### Toncenter HTTP API

客户端连接到[ton-http-api](https://github.com/toncenter/ton-http-api)服务器，该服务器使用TonLib将请求代理到liteserver（节点）。

- Public TON Index can be used: tests and development are for free, [premium](https://t.me/tonapibot) for production - [toncenter.com/api/v3/](https://toncenter.com/api/v3/).
- Run your own TON Index with [Worker](https://github.com/toncenter/ton-index-worker/tree/36134e7376986c5517ee65e6a1ddd54b1c76cdba) and [TON Index API wrapper](https://github.com/toncenter/ton-indexer).

### 获取 API 密钥

要使用公共TonCenter API，您需要一个API密钥：

- 获取Mainnet和Testnet的API密钥：[@tonapibot](https://t.me/tonapibot)
- [dton.io](https://dton.io/graphql) - as well as providing contracts data augmented with parsed "is jetton", "is NFT" flags, allows emulating transactions and receiving execution traces.

## 参阅

- [TON ADNL API](/develop/dapps/apis/adnl)
