# 持久状态

Nodes store snapshots of states of the blockchain periodically. Each state is created at some masterchain block and has some TTL. The block and TTL are chosen using the following algorithm:

Only key blocks can be chosen. A block has some timestamp `ts`. There are periods of time of length `2^17` seconds (approximately up to 1.5 days). 只有关键区块可以被选择。一个区块有一个时间戳`ts`。时间段的长度为`2^17`秒（大约1.5天）。时间戳`ts`的区块的时间段为`x = floor(ts / 2^17)`。每个时间段的第一个关键区块被选择用来创建持久状态。 The first key block from each period is chosen to create a persistent state.

时间段`x`的状态的TTL等于`2^(18 + ctz(x))`，其中`ctz(x)`是`x`的二进制表示中的尾随零的数量（即最大的`y`使得`x`可以被`2^y`整除）。

这意味着每1.5天会创建一个持久状态，其中一半的状态具有`2^18`秒（3天）的TTL，剩余状态的一半具有`2^19`秒（6天）的TTL，依此类推。

2022年有以下长期（至少3个月）的持久状态（未来的时间是大致的）：

| Block seqno |                                                区块时间 |   TTL |                                          Expires at |
| ----------: | --------------------------------------------------: | ----: | --------------------------------------------------: |
|    18155329 | 2022-02-07 01:31:53 |  777天 | 2024-03-24 18:52:57 |
|    19365422 | 2022-03-27 14:36:58 |   97天 | 2022-07-02 16:47:06 |
|             | 2022-05-14 20:00:00 |  194天 | 2022-11-24 23:00:00 |
|             | 2022-07-02 09:00:00 |   97天 | 2022-10-07 10:00:00 |
|             | 2022-08-19 22:00:00 |  388天 | 2023-09-12 06:00:00 |
|             | 2022-10-07 11:00:00 |   97天 | 2023-01-12 12:00:00 |
|             | 2022-11-25 00:00:00 |  194天 | 2023-06-07 03:00:00 |
|             | 2022-11-25 00:00:00 |  194天 | 2023-06-07 03:00:00 |
|    27747086 | 2022-03-02 05:08:11 | 1553天 | 2027-06-02 18:50:19 |

When the node starts for the first time, it has to download a persistent state. 当节点第一次启动时，它必须下载一个持久状态。这在[validator/manager-init.cpp](https://github.com/ton-blockchain/ton/blob/master/validator/manager-init.cpp)中实现。

Starting from the init block, the node downloads all newer key blocks. 从初始化区块开始，节点下载所有更新的关键区块。它选择最近的具有仍然存在的持久状态的关键区块（使用上述公式），然后下载相应的主链状态和所有分片的状态（或仅下载此节点所需的分片）。
