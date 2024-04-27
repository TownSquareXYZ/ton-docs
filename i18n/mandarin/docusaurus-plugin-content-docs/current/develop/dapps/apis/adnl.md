# TON ADNL API

:::tip

有不同的方式连接到区块链：

1. RPC 数据提供商或另一个 API: 在大多数情况下，您必须\*有关其稳定性和安全性。
2. **ADNL 连接**: 您正在连接到一个 [liteserver](/participate/run-nodes/liteserver). 它们可能是无法访问的，但经过一定程度的验证(在图书馆中实施)是不能撒谎的。
3. Tonlib 二进制：您也正在连接到liteServer，所以所有的好处和下方都可以应用，但是您的应用程序也包含一个动态加载库在外面编译。
4. 仅限离链。 这种SDK允许创建和序列化单元格，然后你可以发送到 API。

:::

客户端使用二进制协议直接连接到LiteServer(节点)。

客户端下载密钥块，当前帐户状态，以及他们的 **Merkle 证明**，它保证收到数据的有效性。

读取操作 (如get-methods 调用) 是通过启动本地TVM 并下载和验证状态进行的。 值得注意的是，无需下载区块链的完整状态， 客户端只下载操作所需的内容。

You can connect to public liteservers from the global config ([Mainnet](https://ton.org/global-config.json) or [Testnet](https://ton.org/testnet-global.config.json)) or run your own [Liteserver](/participate/nodes/node-types) and handle this with [ADNL SDKs](/develop/dapps/apis/sdk#adnl-based-sdks).

阅读更多关于 [Merkle proofs](/develop/data-formuls/proofs) 的信息[TON Whitepaper](https://ton.org/ton.pdf) 2.3.10, 2.3.11。

公开的 liteServer (来自全局配置) 可以让您快速使用 TON 开始。 它可以用来学习编程TON，或用于不需要100%更新时间的应用程序和脚本。

为了建设生产基础设施――建议使用准备完善的基础设施：

- [设置自己的 liteserver](https://docs.ton.org/participate/run-nodes/fullnode#enable-liteserver-mode),
- 使用 LiteServer 高级提供商 [@liteserver_bo](https://t.me/liteserver_bot)

## Pros & Cons

- :check_mark_buton: 可靠。 使用 API 与 Merkle 验证哈希值来验证传入的二进制数据。

- :check_mark_buton: 安全 既然它检查Merkle 证明, 你甚至可以使用不信任的留置服务器。

- :check_mark_buton: 快速. 直接连接到 TON Blockchain 节点，而不是使用 HTTP 中间件。

- :cross_mark：复制。 需要更多的时间来找出问题。

- :cross_mark：后端。 与 web 前端不兼容(为非 HTTP 协议构建)，或需要 HTTP ADNL 代理.

## API 参考

请求和对服务器的响应在 [TL](/develop/data-forms/tl) schema 中描述，它允许您为某个编程语言生成一个输入的接口。

[TonLib TL Schema](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl)
