# Staking Incentives

## 选举和质押

TON区块链使用权益证明（PoS）共识算法，这意味着与所有PoS网络一样，网络的安全和稳定性由一组网络验证者维护。特别是，验证者提出新区块（由交易批组成）的候选人，而其他验证者通过数字签名_验证_并批准它们。 In particular, validators propose candidates for new blocks (made up of transaction batches), while other validators _validate_ and approve them via digital signatures.

Validators are chosen using special [Elector governance contract](/develop/smart-contracts/governance#elector). 验证者是使用特殊的[选举治理合约](/develop/smart-contracts/governance#elector)选择的。在每个共识轮次中，验证者候选人发送选举申请，连同他们的质押代币和期望的_max_factor_（调节验证者每轮共识维护量的参数）。

在验证者选举过程中，治理智能合约选择下一轮验证者，并根据验证者的质押代币和_max_factor_为每个验证者分配投票权重，以最大化他们的总质押代币。在这方面，质押代币和_max_factor_越高，验证者的投票权重越高，反之亦然。 In this respect, the higher the stake and _max_factor_, the higher the voting weight of the validator and vice versa.

Validators that are elected are chosen to secure the network by participating in the next consensus round. 被选中的验证者被选为通过参与下一个共识轮次来保护网络。然而，与许多其他区块链不同，为实现水平扩展，每个验证者只验证网络的一部分：

For each shardchain and masterchain a dedicated set of validators exists. 对于每个分片链和主链，都有专门的验证者集合。主链验证者集合由最高投票权重的多达100个验证者组成（定义为网络参数`Config16:max_main_validators`）。

相比之下，每个分片链由一组23个验证者（定义为网络参数`Config28:shard_validators_num`）验证，并且每1000秒（网络参数`Config28:shard_validators_lifetime`）随机轮换一次。

## 质押代币的价值：最大有效质押代币

当前配置中的`max_factor`为__3__，意味着_最小_验证者的质押代币不能比_最大_验证者的质押代币多三倍。

配置参数的公式：

`max_factor` = [`max_stake_factor`](https://tonviewer.com/config#17) / [`validators_elected_for`](https://tonviewer.com/config#15)

### （简化的）选择算法

这个算法由[选举智能合约](/develop/smart-contracts/governance#elector)运行，根据验证者所承诺的质押代币选择最佳的验证者候选人。以下是它的工作原理： Here's a breakdown of how it works:

1. **初始选择**：选举者考虑所有承诺超过设定最低金额（300K，如[配置](https://tonviewer.com/config#17)所述）的候选人。

2. **排序候选人**：这些候选人根据他们的质押代币从高到低进行排列。

3. **缩小范围**：
   - 如果候选人数量超过允许的最大验证者数量（[见配置](https://tonviewer.com/config#16)），质押代币最低的将被排除。
   - 然后选举者评估每个可能的候选人组，从最大组开始逐渐减小：
     - 它检查按顺序排列的顶部候选人，一个接一个地增加数量。
     - For each candidate, Elector calculates their 'effective stake'. If a candidate's stake is significantly higher than the minimum, it's adjusted down (e.g., if someone staked 310k and the minimum is 100k, but there's a rule capping at three times the minimum, their effective stake is considered as 300k).
     - 它对这个组中所有候选人的有效质押代币进行求和。

4. **最终选择**：有效质押代币总和最高的候选人组被选举者选为验证者。

#### 验证者选择算法

根据潜在验证者的可用质押代币，确定最小和最大质押代币的最佳值，目的是最大化总质押代币的量级：

1. 选举者考虑所有质押代币高于最低限额（[配置中的300K](https://tonviewer.com/config#17)）的申请者。
2. Elector sorts them in _descending_ order of stake.
3. 如果参与者数量超过[最大验证者数量](https://tonviewer.com/config#16)，选举者将放弃列表的尾部。然后选举者执行以下操作： Then Elector does the following:

   - 对于每个循环__i__从_1至N_（剩余参与者数量），它从排序列表中取出前__i__个申请。
   - It calculates the effective stake, considering the `max_factor`. 它计算有效质押代币，考虑到`max_factor`。也就是说，如果某人质押代币310k，但`max_factor`为3，列表中的最低质押代币为100k Toncoin，那么有效质押代币将是min(310k, 3\*100k) = 300k。
   - 它计算所有__i__个参与者的总有效质押代币。

一旦选举者找到这样的__i__，使得总有效质押代币最大，我们就宣布这些__i__个参与者为验证者。

## 积极激励

与所有区块链网络一样，TON上的每笔交易都需要一个称为[ gas ](https://blog.ton.org/what-is-blockchain)的计算费用，用于进行网络存储和链上交易处理。在TON上，这些费用积累在选举者合约中的奖励池中。 On TON, these fees are accumulated within the Elector contract in a reward pool.

网络还通过向奖励池添加补贴来补贴区块创建，每个主链块1.7 TON，每个基本链块1 TON（网络参数`Config14:masterchain_block_fee`和`Config14:basechain_block_fee`）。请注意，当将基本链分割为多个分片链时，每个分片链块的补贴相应分割。这个过程允许每单位时间的补贴保持接近恒定。 Note, that when splitting a basechain into more than one shardchain, the subsidy per shardchain block is split accordingly. This process allows the subsidy per unit of time to be kept near constant.

:::info
TON Blockchain is planning to introduce a deflationary mechanism in Q2 of 2023. In particular, a portion of TON generated via network use will be burned instead of going to the rewards pool.
:::

经过65536秒或约18小时的验证周期轮次（网络参数`Config15:validators_elected_for`），验证者中的质押TON并未立即释放，而是持有额外的32768秒或约9小时（网络参数`Config15:stake_held_for`）。在此期间，可以从验证者中扣除削减（对行为不端验证者的惩罚机制）罚款。在资金释放后，验证者可以提取他们在验证轮次期间累积的奖励池份额，与他们的投票_权重_成比例。 During this period, slashing (a penalization mechanism for misbehaving validators) penalties can be deducted from the validator. After funds are released, validators can withdraw their stake along with a share of the reward pool accrued during the validation round proportional to their voting _weight_.

截至2023年4月，网络上所有验证者每轮共识的总奖励池约为40,000 TON，每个验证者的平均奖励约为120 TON（投票权重与累积奖励之间的最大差异约为3 TON）。

考虑到Toncoin（50亿TON）的总供应量，其年通胀率约为0.3-0.6%。

然而，这一通胀率并非始终恒定，可能会根据网络的当前状态而有所偏差。最终，在通货紧缩机制启动和网络利用率增长后，它将趋于通货紧缩。 Eventually it will tend to deflation after Deflation mechanism activation and growth of network utilization.

:::info
了解当前TON区块链统计数据[这里](https://tontech.io/stats/)。
:::

## 负面激励

在TON区块链上，通常有两种方式可以对行为不端的验证者进行处罚：闲置和恶意行为；这两种行为都是被禁止的，可能会因其行为而被罚款（在所谓的削减过程中）。

如果验证者在验证轮次期间长时间不参与区块创建和交易签名，它可能会使用_标准罚款_参数被罚款。截至2023年4月，标准罚款累积为101 TON（网络参数`ConfigParam40:MisbehaviourPunishmentConfig`）。 As of April 2023, the Standard fine accrued is 101 TON (Network Parameter `ConfigParam40:MisbehaviourPunishmentConfig`).

On TON, slashing penalties (fines given to validators) allow any network participant to file a complaint if they believe a validator is misbehaving. During this process, the participant issuing the complaint must attach cryptographic proofs of misbehavior for Elector submission. During the `stake_held_for` dispute resolution period, all validators operating on the network check the validity of complaints and vote whether they will pursue the complaint collectively (while determining the legitimacy of misbehaving proofs and fine allotment).

一旦获得66%验证者批准（通过相等的投票权重衡量），削减罚款将从验证者中扣除，并从验证者的总质押代币中提取。对于处罚和投诉解决的验证过程通常使用 MyTonCtrl 自动进行。 The validation process for penalization and complaint resolution is typically conducted automatically using the MyTonCtrl.

## 参阅

- [运行全节点（验证者）](/participate/run-nodes/full-node)
- [交易费用](/develop/smart-contracts/fees)
- [What is blockchain? What is a smart contract? [什么是区块链？什么是智能合约？什么是 gas ？](https://blog.ton.org/what-is-blockchain)
