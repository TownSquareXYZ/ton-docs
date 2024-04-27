# 基于 TON HTTP 的APIs

:::tip

有不同的方式连接到区块链：

1. **RPC 数据提供商或另一个 API**：在大多数情况下，您必须\*有关其稳定性和安全性。
2. ADNL 连接：您正在连接到 [liteserver](/participate/run-nodes/liteserver). 它们可能是无法访问的，但经过一定程度的验证(在图书馆中实施)是不能撒谎的。
3. Tonlib 二进制：您也正在连接到liteServer，所以所有的好处和下方都可以应用，但是您的应用程序也包含一个动态加载库在外面编译。
4. 仅限离链。 这种SDK允许创建和序列化单元格，然后你可以发送到 API。

:::

## Pros & Cons

- ✅ 习惯并适合快速启动, 这对于每个正在与TON玩的新移民来说都是完美的。

- :check_mark_buton: 网络导向。 完全可以从 Web中加载TON 智能合约数据，同时也允许在那里发送消息。

- ❌ 简化. 无法收到您需要索引TON API的信息。

- ❌ HTTP-Middleware。 您不能完全信任服务器响应，除非服务器以[Merkle proofs](/develop/data-formuls/proofs)增强区块链数据，允许验证它是真实的。

## RPC Nodes

- [GetBlock 节点](https://getblock.io/nodes/ton/) - 使用 GetBlocks 节点连接并测试您的 dapp
- [TON Access](https://www.orbs.com/ton-access/) - Open Network (TON) HTTP API。
- [Toncenter](https://toncenter.com/api/v2/) — 社区主办的 API 快速启动项目。 (Get 一个 API 密钥 [@tonapibot](https://t.me/tonapibot))
- [ton-node-docker](https://github.com/fmira21/ton-node-docker) - Docker Full Node 和 Toncent API。
- [toncenter/ton-http-api](https://github.com/toncenter/ton-http-api) - 运行你自己的 RPC 节点。
- [nownodes.io](https://nowdes.io/nodes) — 通过API，NOWNodes 完整节点和blockbook Explorers。
- [Chainbase](https://chainbase.com/chainNetwork/TON) — Node API 和开放网络的数据基础设施。

## 索引器

### Toncent TON 索引

索引器允许列出jetton钱包、NFT、某些过滤器的交易，而不仅仅是检索特定的交易。

- 可以使用公開的 TON 索引：测试和开发是免费的，生产高级版- [toncenter.com/api/v3/](https://toncenter.com/api/v3/)。
- 用 [Worker](https://github.com/toncenter/ton-index-worker/tree/36134e7376986c5517ee65e6a1ddd54b1c76c6c6c6dba)和[TON Index API wrapper](https://github.com/toncenter/ton-indexer) 运行您自己的 TON 索引。

### 图形QL节点

GraphQL节点也是索引器。

- [tvmlabs.io](https://ton-testnet.tvml.dev/graphql) (TON, testnet only at the time of writing) - 有多种交易/块数据，过滤它的方式等。
- [dton.io](https://dton.io/graphql) - 除了提供被解析为"is jetton"、"is NFT"标志的合约数据，允许模拟交易和接收执行跟踪。

## 其他 API

- [TonAPI](https://docs.tonconsole.com/tonapi/api-v2) - API 旨在为用户提供简化的体验，不要担心智能合约的低级细节。
