# ADNL 协议

:::tip

客户端下载关键区块、账户的当前状态及其**Merkle证明**，这保证了接收数据的有效性。

1. RPC data provider or another API: in most cases, you have to _rely_ on its stability and security.
2. **ADNL connection**: you're connecting to a [liteserver](/participate/run-nodes/liteserver). They might be inaccessible, but with a certain level of validation (implemented in the library), cannot lie.
3. Tonlib binary: you're connecting to liteserver as well, so all benefits and downsides apply, but your application also contains a dynamic-loading library compiled outside.
4. Offchain-only. Such SDKs allow to create and serialize cells, which you can then send to APIs.

:::

这是一个基于**UDP**在**IPv4**（将来是IPv6）之上运行的覆盖层、点对点、不可靠（小尺寸）数据报协议，如果UDP不可用，可以选择**TCP备选**。

更多关于Merkle证明的信息，请参阅[TON白皮书](https://ton.org/ton.pdf) 2.3.10, 2.3.11。

每个参与者都有一个256位的ADNL地址。

ADNL协议允许您仅使用ADNL地址发送（不可靠）和接收数据报。IP地址和端口由ADNL协议隐藏。

ADNL地址本质上等同于一个256位的ECC公钥。这个公钥可以任意生成，从而为节点创建尽可能多的不同网络身份。然而，为了接收（并解密）发给接收地址的消息，必须知道相应的私钥。

实际上，ADNL地址不是公钥本身；相反，它是一个序列化TL对象的256位SHA256哈希，该对象可以根据其构造器来描述几种类型的公钥和地址。

[TonLib TL模式](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl)

- [set up own liteserver](https://docs.ton.org/participate/run-nodes/full-node#enable-liteserver-mode),
- use Liteserver premium providers [@liteserver_bot](https://t.me/liteserver_bot)

## 邻居表

- ✅ Reliable. Uses API with Merkle proof hashes to verify incoming binary data.

- ✅ Secure. Since it checks Merkle proofs, you can even use untrusted liteservers.

- ✅ Fast. Connects directly to TON Blockchain nodes, instead of using HTTP middleware.

- ❌ Complicated. More time is required to figure things out.

- ❌ Back-end first. Not compatible with web frontends (built for non-HTTP protocol), or requires HTTP-ADNL proxy.

## API reference

还可以在ADNL之上构建类TCP的流协议。

[TonLib TL Schema](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl)
