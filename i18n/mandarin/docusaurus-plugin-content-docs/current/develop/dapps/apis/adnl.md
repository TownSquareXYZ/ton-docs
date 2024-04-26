# TON ADNL API

:::tip

There are different ways to connect to blockchain:

1. RPC data provider or another API: in most cases, you have to _rely_ on its stability and security.
2. **ADNL connection**: you're connecting to a [liteserver](/participate/run-nodes/liteserver). They might be inaccessible, but with a certain level of validation (implemented in the library), cannot lie.
3. Tonlib binary: you're connecting to liteserver as well, so all benefits and downsides apply, but your application also contains a dynamic-loading library compiled outside.
4. Offchain-only. Such SDKs allow to create and serialize cells, which you can then send to APIs.

:::

客户端使用二进制协议直接连接到Liteservers（节点）。

客户端下载关键区块、账户的当前状态及其**Merkle证明**，这保证了接收数据的有效性。

读操作（如调用get-method）是通过下载并验证状态后启动本地TVM（TON虚拟机）来完成的。 It's worth noting that there is no need to download the full state of the blockchain, the client downloads only what is needed for the operation.

您可以从全局配置（[Mainnet](https://ton.org/global-config.json)或[Testnet](https://ton.org/testnet-global.config.json)）连接到公共liteservers，或运行您自己的[Liteserver](/participate/nodes/node-types)，并使用[ADNL SDKs](/develop/dapps/apis/sdk#adnl-based-sdks)来处理这些操作。

更多关于Merkle证明的信息，请参阅[TON白皮书](https://ton.org/ton.pdf) 2.3.10, 2.3.11。

Public liteservers (from the global config) exist to get you started with TON quickly. It can be used for learning to program in TON, or for applications and scripts that do not require 100% uptime.

For building production infrastructure - it is suggested use well prepared infrastructure:

- [set up own liteserver](https://docs.ton.org/participate/run-nodes/full-node#enable-liteserver-mode),
- use Liteserver premium providers [@liteserver_bot](https://t.me/liteserver_bot)

## 优点和缺点

- ✅ Reliable. ✅ 可靠。使用带有Merkle证明哈希的API来验证传入的二进制数据。

- ✅ Secure. ✅ 安全。由于它检查Merkle证明，即使使用不受信任的liteservers也可以。

- ✅ Fast. ✅ 快速。直接连接到TON区块链节点，而不是使用HTTP中间件。

- ❌ Complicated. More time is required to figure things out.

- ❌ Back-end first. Not compatible with web frontends (built for non-HTTP protocol), or requires HTTP-ADNL proxy.

## API 参考

对服务器的请求和响应由TL模式描述，允许您为某种编程语言生成类型化接口。

[TonLib TL模式](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl)
