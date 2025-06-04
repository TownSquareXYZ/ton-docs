import Feedback from '@site/src/components/Feedback';

# Staking incentives

## Election and staking

TON Blockchain uses the **Proof-of-stake (PoS)** consensus algorithm, meaning that, like all PoS networks, a set of network validators maintains the network's security and stability. In particular, validators propose candidates for new blocks (made up of transaction batches), while other validators *validate* and approve them via digital signatures.

Validators are chosen using a special [Elector governance contract](/v3/documentation/smart-contracts/contracts-specs/governance#elector). During each consensus round, validator candidates send an application for election along with their stake and desired *max_factor* (a parameter that regulates the amount of maintenance the validator performs per consensus round).

During the validator election process, the governance smart contract chooses the next round of validators and assigns a voting weight to each validator to maximize their total stake while also considering the validator’s stake and *max_factor*. In this respect, the higher the stake and *max_factor*, the higher the voting weight of the validator, and vice versa.

Elected validators are selected to secure the network by participating in the next consensus round. However, to achieve horizontal scalability, each validator verifies only a portion of the network, unlike many other blockchains:

Each ShardChain and MasterChain has a dedicated set of validators. Sets of master chain validators consist of up to 100 validators exhibiting the highest voting weight (defined as Network Parameter `Config16:max_main_validators`).

Each ShardChain is validated by 23 validators, as defined by Network Parameter `Config28:shard_validators_num`. These validators are rotated randomly every 1000 seconds according to Network Parameter `Config28:shard_validators_lifetime`.

## Values of stakes: max effective stake

The current `max_factor` in config is **3**, meaning the stake of the *smallest* validator cannot be more than three times less than the stake of the **largest** one.

配置参数的公式：

`max_factor` = [`max_stake_factor`](https://tonviewer.com/config#17) / [`validators_elected_for`](https://tonviewer.com/config#15)

### Selection algorithm review

这个算法由[选举智能合约](/develop/smart-contracts/governance#elector)运行，根据验证者所承诺的质押代币选择最佳的验证者候选人。以下是它的工作原理：

1. **Initial selection**: Elector considers all candidates who have staked more than a set minimum amount (300K, as specified in the [configuration](https://tonviewer.com/config#17)).

2. **Ordering candidates**: These candidates are then arranged from highest to lowest based on their stake.

3. **Narrowing down**:

- 如果候选人数量超过允许的最大验证者数量（[见配置](https://tonviewer.com/config#16)），质押代币最低的将被排除。

- 然后选举者评估每个可能的候选人组，从最大组开始逐渐减小：

    - 它检查按顺序排列的顶部候选人，一个接一个地增加数量。

    - For each candidate, Elector calculates their **effective stake**. If a candidate's stake is significantly higher than the minimum, it's adjusted down (e.g., if someone staked 310k and the minimum is 100k, but there's a rule capping at three times the minimum, their effective stake is considered as 300k).

    - 它对这个组中所有候选人的有效质押代币进行求和。

4. **Final selection**: The elector chooses the group of candidates with the highest total effective stake as the validators.

#### Validator selection algorithm

根据潜在验证者的可用质押代币，确定最小和最大质押代币的最佳值，目的是最大化总质押代币的量级：

1. 选举者考虑所有质押代币高于最低限额（[配置中的300K](https://tonviewer.com/config#17)）的申请者。

2. 选举者按质押代币_降序_排序他们。

3. 如果参与者数量超过[最大验证者数量](https://tonviewer.com/config#16)，选举者将放弃列表的尾部。然后选举者执行以下操作：

    - 对于每个循环__i__从_1至N_（剩余参与者数量），它从排序列表中取出前__i__个申请。

    - 它计算有效质押代币，考虑到`max_factor`。也就是说，如果某人质押代币310k，但`max_factor`为3，列表中的最低质押代币为100k Toncoin，那么有效质押代币将是min(310k, 3\*100k) = 300k。

    - 它计算所有__i__个参与者的总有效质押代币。

Once Elector identifies such an **i**, where the total effective stake is maximized, we declare these **i** participants as validators.

## Positive incentives

Similarly to all blockchain networks, each transaction on TON requires a computation fee called [gas](https://blog.ton.org/what-is-blockchain) to store the network and process the transaction on-chain. On TON, these fees are accumulated within the Elector contract in a reward pool.

The network also provides a subsidy for block creation by adding an amount of 1.7 TON to the reward pool for each MasterChain block and an amount equal to 1 TON for each BaseChain block (refer to Network Parameters `Config14:masterchain_block_fee` and `Config14:basechain_block_fee`). It is important to note that when a BaseChain is divided into multiple ShardChains, the subsidy for each ShardChain block is distributed accordingly. This approach helps maintain a consistent subsidy per unit of time.

:::info
TON区块链计划在2023年第二季度引入通货紧缩机制。特别是，通过网络使用产生的TON的一部分将被销毁，而不是进入奖励池。
:::

After a validation cycle lasting 65536 seconds, or approximately 18 hours (as determined by the network parameter `Config15:validators_elected_for`), staked TON is not immediately released by each validator. Instead, it is held for an additional 32768 seconds, or about 9 hours (as specified by the network parameter `Config15:stake_held_for`). During this period, slashing penalties can be imposed on the validator as a consequence for any misbehavior. Once the funds are released, validators can withdraw their staked amount along with a share of the rewards accrued during the validation round, proportional to their voting **weight**.

截至2023年4月，网络上所有验证者每轮共识的总奖励池约为40,000 TON，每个验证者的平均奖励约为120 TON（投票权重与累积奖励之间的最大差异约为3 TON）。

The total supply of Toncoin (5 billion TON) has an inflation rate of approximately 0.3-0.6% annually.

This inflation rate, however, is not always constant and may deviate depending on the network’s current state. Eventually, it will tend to deflate after the Deflation mechanism is activated and network utilization grows.

:::info
了解当前TON区块链统计数据[这里](https://tontech.io/stats/)。
:::

## Negative incentives

On TON Blockchain, there are generally two ways validators can be penalized for misbehaving: **idle** and **malicious** misbehaving. Both are prohibited and may result in fines (in a process called slashing) for their actions.

If a validator fails to participate in block creation and transaction signing for a significant period during a validation round, they may incur a fine based on the **Standard fine** parameter. As of April 2023, the Standard fine that can be accrued is 101 TON (Network Parameter `ConfigParam40:MisbehaviorPunishmentConfig`).

On the TON network, slashing penalties—also known as fines imposed on validators—allow any participant to file a complaint if they suspect a validator is misbehaving. When submitting a complaint, the participant must provide cryptographic evidence of the alleged misbehavior for submission to the Electors.

During the `stake_held_for` dispute resolution period, all validators on the network assess the validity of the complaints and vote on whether to pursue each complaint collectively. They also evaluate the legitimacy of the provided evidence and determine the appropriate penalties.

If, based on weighted votes, at least 66% of the validators approve the complaint, the slashing penalty is applied. This penalty is deducted from the offending validator's total stake. Typically, the process of penalization and resolution of complaints is managed automatically using MyTonCtrl.

## Decentralized system of penalties

:::info
The following system of penalizing poorly performing validators was fully operational on September 9, 2024.
:::

### Determination of poor work

The TON is supplied with the [lite-client](https://github.com/newton-blockchain/ton/tree/master/lite-client) utility. In lite-client, there is a `checkloadall` command.

This command analyses the number of blocks the validator should have processed and the number it actually processed in a given period of time.

If the validator processed less than 90% of the expected number of blocks during a validation round, it is considered to be performing poorly and should be penalized.

:::info
Learn more about the technical description of the process [here](https://github.com/ton-blockchain/TIPs/issues/13#issuecomment-786627474)
:::

### Complain workflow

- Anyone can make a complaint and get a reward for the right complaint.

- Validation of complaints maintained by Validators and fully decentralized.

#### Make complaint

After each validation round (~18 hours), the validator stakes of the validators who participated in that round remain on the Elector smart contract for another ~9 hours.

During this time, anyone can send a complaint against a validator who performed poorly in said round. This happens on-chain on the Elector smart contract.

#### Validation of complaint

After each validation round, validators receive a list of complaints from the Elector smart contract. They then double-check these complaints by calling `checkloadall`.

If a complaint is validated, a vote is conducted on-chain in favor of that complaint.

These actions are integrated into MyTonCtrl and occur automatically.

When a complaint receives 66% of the validators' votes (weighted by their stake), the validator's stake is penalized.

No one has the authority to impose a fine on their own.

The list of penalized validators for each round is available at [@tonstatus_notifications](https://t.me/tonstatus_notifications).

### Fine value

罚款金额是固定的，等于 101  TON （网络参数 `ConfigParam40:MisbehaviourPunishmentConfig`），大致相当于验证者每轮的收入。

The value of the fine may change due to the rapidly growing audience and the number of transactions in TON, and it is vital that the quality of work is at its best.

### Fine distribution

The fine is distributed among the validators minus network costs, and a small reward (~8 TON) is given to the first complainer who sends the correct complaint to the Elector.

### Validator guidelines

To prevent your Validator node from being fined, it is advisable to ensure that the hardware, monitoring, and validator operations are set up properly.

Please ensure you comply with the [validator maintain guidelines](/v3/guidelines/nodes/running-nodes/validator-node#maintain-guidelines).

If you don't want to do this please consider [using staking services](https://ton.org/stake).

## See also

- [Running a validator](/v3/guidelines/nodes/running-nodes/validator-node)
- [Transaction fees](/v3/documentation/smart-contracts/transaction-fees/fees)
- [什么是区块链？什么是智能合约？什么是 gas ？](https://blog.ton.org/what-is-blockchain)

<Feedback />

