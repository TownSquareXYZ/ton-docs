# Overlay Subnetworks

实现：

- https://github.com/ton-blockchain/ton/tree/master/overlay

## 概览

在像TON这样的多区块链系统中，即使是完整节点通常也只对获取某些分片链的更新（即新区块）感兴趣。为此，在TON网络内部，基于ADNL协议，为每个分片链构建了一个特殊的覆盖子网络 (Overlay Subnetwork)。 To this end, a special overlay subnetwork has been built
inside the TON Network, on top of the ADNL Protocol,
for each shardchain.

此外，覆盖子网络还用于TON存储、TON代理等的运行。

## ADNL 与覆盖网络

In contrast to ADNL, the TON overlay networks usually do not support
sending datagrams to other arbitrary nodes. Instead, some “semi-permanent
links” are established between certain nodes (called “neighbors” with respect to
the overlay network under consideration) and messages are usually forwarded
along these links (i.e. from a node to one of its neighbors).

每个覆盖子网络都有一个通常等于覆盖网络描述的SHA256的256位网络标识符——一个TL序列化对象。

覆盖子网络可以是公开的或私有的。

覆盖子网络根据一种特殊的[gossip协议](https://en.wikipedia.org/wiki/Gossip_protocol)工作。

:::info
在[覆盖子网络](/develop/network/overlay)文章中阅读更多关于覆盖的信息，或者在[TON白皮书](https://ton.org/docs/ton.pdf)的第3.3章中查看。
:::
