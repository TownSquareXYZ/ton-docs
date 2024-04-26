# Blockchain of Blockchains

:::tip
本文档中，“**智能合约**”、“**账户**”和“**Actor**”这几个术语可互换使用，用以描述区块链实体。
:::

## 单一Actor

让我们考虑一个智能合约。

In TON, it is a _thing_ with properties like `address`, `code`, `data`, `balance` and others. In other words, it is an object which has some _storage_ and _behavior_.
That behavior has the following pattern:

- 发生某事（最常见的情况是合约收到一条消息）
- 合约根据自身属性通过在TON虚拟机中执行其`代码`来处理该事件。
- 合约修改自身属性（`代码`、`数据`等）
- 合约可选地生成传出消息
- 合约进入待机模式，直到下一个事件发生

这些步骤的组合被称为一次**交易**。重要的是，事件是依次处理的，因此_交易_是严格有序的，不能相互打断。 将传入和传出消息的队列也包含在_区块_中是有益的。在这样的情况下，一个_区块_将包含决定和描述智能合约在该区块期间所发生的全部信息。

这种行为模式众所周知，被称为“Actor”。

### 最低层级：账户链

一系列的_交易_ `Tx1 -> Tx2 -> Tx3 -> ....` 可以被称为一条**链**。在这个例子下，它被称为**账户链 (AccountChain)**，以强调这是单个账户的_交易链_。 为了使分割和合并具有确定性，将账户链聚合成分片是基于账户地址的位表示。例如，地址会看起来像`(分片前缀, 地址)`这种形式。这样，分片链中的所有账户将具有完全相同的二进制前缀（例如所有地址都以`0b00101`开头）。

现在，由于处理交易的节点时不时需要协调智能合约的状态（达成关于状态的_共识_），这些_交易_被批量处理：
`[Tx1 -> Tx2] -> [Tx3 -> Tx4 -> Tx5] -> [] -> [Tx6]`。
批处理不干预排序，每个交易仍然只有一个“前一交易”和至多一个“下一交易”，但现在这个序列被切割成了**区块**。
Batching does not intervene in sequencing, each transaction still has only one 'prev tx' and at most one 'next tx', but now this sequence is cut into the **blocks**.

It is also expedient to include queues of incoming and outgoing messages to _blocks_. In that case, a _block_ will contain a full set of information which determines and describes what happened to the smart contract during that block.

## Many AccountChains: Shards

Now let's consider many accounts. 现在让我们考虑有许多账户的情况。我们得到一些_账户链_并将它们存储在一起，这样的一组_账户链_被称为**分片链 (ShardChain)**。同样地，我们可以将**分片链**切割成**分片区块**，这些区块是个别_账户区块_的聚合。 同样地，如果某些分片变得过于空闲，它们可以被**合并**为一个更大的分片。

### 分片链的动态拆分与合并

Note that since a _ShardChain_ consists of easily distinguished _AccountChains_, we can easily split it. 请注意，由于_分片链_由容易区分的_账户链_组成，我们可以轻松地将其分割。这样，如果我们有1个_分片链_，描述了100万个账户的事件，且每秒交易量过多，无法由一个节点处理和存储，那么我们就将该链分割（或**拆分**）为两个较小的_分片链_，每条链处理50万个账户，每条链在一组独立的节点上处理。

Analogously, if some shards became too unoccupied they can be **merged** into one bigger shard.

显然有两个极限情况：分片只包含一个账户（因此无法进一步分割）以及当分片包含所有账户。

Accounts can interact with each other by sending messages. There is a special mechanism of routing which move messages from outgoing queues to corresponding incoming queues and ensures that 1) all messages will be delivered 2) messages will be delivered consecutively (the message sent earlier will reach the destination earlier).

:::info SIDE NOTE
To make splitting and merging deterministic, an aggregation of AccountChains into shards is based on the bit-representation of account addresses. For example, address looks like `(shard prefix, address)`. That way, all accounts in the shardchain will have exactly the same binary prefix (for instance all addresses will start with `0b00101`).
:::

## Blockchain

包含所有账户并按照一套规则运行的所有分片的集合被称为**区块链**。

在TON中，可以有许多套规则，因此允许多个区块链同时运行，并通过发送跨链消息相互交互，就像同链的账户之间的交互一样。

### 工作链：有自己规则的区块链

If you want to customize rules of the group of Shardchains, you could create a **Workchain**. 如果你想自定义一组分片链的规则，你可以创建一个**工作链 (Workchain)**。一个很好的例子是创建一个基于EVM的工作链，在其上运行Solidity智能合约。

区块链之链 理论上，社区中的每个人都可以创建自己的工作链。事实上，构建它是一个相当复杂的任务，在此之前还要支付创建它的（昂贵）费用，并获得验证者的2/3的票数来批准创建你的工作链。

TON允许创建多达`2^32`个工作链，每个工作链则可以细分为多达`2^60`个分片。

如今，在TON中只有2个工作链：主链和基本链。

基本链用于日常交易，因为它相对便宜，而主链对于TON具有至关重要的功能，所以让我们来了解它的作用！

### Masterchain: Blockchain of Blockchains

There is a necessity for the synchronization of message routing and transaction execution. In other words, nodes in the network need a way to fix some 'point' in a multichain state and reach a consensus about that state. In TON, a special chain called **MasterChain** is used for that purpose. Blocks of _masterchain_ contain additional information (latest block hashes) about all other chains in the system, thus any observer unambiguously determines the state of all multichain systems at a single masterchain block.
