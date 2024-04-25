# Governance Contracts

在TON中，与TVM、catchain、费用和链拓扑（以及这些参数如何存储和更新）有关的节点操作共识参数由一组特殊的智能合约控制（与前几代区块链采用的旧式和不灵活的硬编码这些参数的方式不同）。通过这种方式，TON实现了全面透明的链上治理。这组特殊合约本身受参数控制，目前包括选举人、配置合约和DNS合约，将来将通过额外的货币铸币和其他合约进行扩展。 That way, TON implements comprehensive and transparent on-chain governance. The set of special contracts itself is governed by parameters and currently includes the Elector, Config, and DNS contracts and in future will be extended by extra-currency Minter and others.

## 选举人(Elector)

The Elector smart contract controls the way how rounds of validation change each other, who gets the duty to validate the blockchain, and how rewards for validation would be distributed. If you want to become a validator and interact with Elector, check [validator instrucitons](https://ton.org/validator).

选举人存储未提取的Toncoin数据在`credits`哈希表中，新的申请在`elect`哈希表中，以及关于以往选举的信息在 _past\_elections_ 哈希表中（后者存储在关于验证者不当行为的 _complaints_ 和_frozen_-已完成轮次的验证者质押中，这些质押被扣留用于 `stake_held_for`（配置参数15））。选举人合约有三个目的： The Elector contract has three purposes:

- 处理验证者选举的申请
- 举行选举
- 处理验证者不当行为的报告
- 分配验证奖励

### 处理申请

To create an application, a future validator needs to form a special message that contains the corresponding parameters (ADNL address, public key, `max_factor`, etc.), attach it to some sum of TON (called a stake), and send it to the Elector. In turn, the Elector checks those parameters and either registers an application or immediately returns the stake back to the sender. Note that applications are only accepted from addresses on the masterchain.

### 举行选举

The Elector is a special smart contract that has the option to be forcedly invoked at the beginning and end of each block (so-called Tick and Tock transactions). The Elector, indeed, is invoked on each block and checks whether it is time to conduct a new election.

选举过程的总体概念是考虑所有申请，特别是它们的TON数量和`max_factor`（此申请人同意做的验证工作与最弱验证者做的验证工作相比的最大比例），并按照TON数量为每个验证者设置权重，但要满足所有`max_factor`条件。

技术实现如下：

1. 选举人取出所有质押金额高于当前网络最低`min_stake`（配置参数17）的申请。
2. It sorts them by stake in descending order.
3. 如果参与者多于验证者的最大数量（`max_validators` 配置参数16），则舍弃名单尾部。
4. 从`1`循环到`N`（剩余参与者数量）。

- 取名单中按降序排列的第`i`个元素
- 假设第_i_个候选人将是最后一个被接受的（因此权重最低），并根据`max_factor`计算有效质押（`true_stake`）。换句话说，第_j_个（`j<i`）申请人的有效质押计算为`min(stake[i]*max_factor[j], stake[j])`。 这样，如果我们有9个候选人，每个人有100,000和2.7的因子，最后一个参与者不会被选举：没有他，有效质押将是900,000，有他，只有9 \* 27,000 + 10,000 = 253,000。相反，如果我们有一个候选人有100,000和2.7的因子和9个参与者各有10,000，他们都将成为验证者。但是，第一个候选人只会质押10\*2.7 = 27,000 TON，多出的73,000 TON进入`credits`。
- Calculate the total effective stake (TES) of participants from 1 to _i_-th. 计算第1个到第_i_个参与者的总有效质押（TES）。如果这个TES高于先前已知的最大TES，则将其视为当前最佳权重配置。

5. 获取当前最佳配置，即最大化利用质押的权重配置，并将其发送给配置合约（下面的配置合约）以成为新的验证者集合。
6. 将所有未使用的质押，例如那些没有成为验证者的申请人和多余的部分（如果有的话）`stake[j]-min(stake[i]*max_factor[j], stake[j])`放入`credits`表中，申请人可以从中请求拿回它们。

That way, if we have nine candidates with 100,000 and a factor of 2.7 and one participant with 10,000. The last participant will not be elected: Without him, an effective stake would be 900,000, and with him, only 9 \* 27,000 + 10,000 = 253,000. In contrast, if we have one candidate with 100,000 and a factor of 2.7 and nine participants with 10,000, they all become validators. However, the first candidate will only stake 10\*2.7 = 27,000 TON with the excess of 73,000 TON going into `credits`.

请注意，对结果验证集有一些限制（显然由TON配置参数控制），特别是`min_validators`、`max_validators`（配置参数16）、`min_stake`、`max_stake`、`min_total_stake`、`max_stake_factor`（配置参数17）。如果目前的申请无法满足这些条件，选举将被推迟。 If there is no way to meet those conditions with the current applications, elections will be postponed.

### 报告验证者不当行为的过程

Each validator, from time to time, is randomly assigned to create a new block (if the validator fails after a few seconds, this duty is passed to the next validator). The frequency of such assignments is determined by the validator's weight. So, anyone can get the blocks from the previous validation round and check whether the expected number of generated blocks is close to the real number of blocks. A statistically significant deviation (when the number of generated blocks is less than expected) means that a validator is misbehaving. On TON, it is relatively easy to prove misbehavior using Merkle proofs. The Elector contract accepts such proof with a suggested fine from anyone who is ready to pay for its storage and registers the complaint. Then, every validator of the current round checks the complaint, and if it is correct and the suggested fine corresponds to the severity of the misbehavior, they vote for it. Upon getting more than 2/3 of the votes with respect to the weight, the complaint gets accepted, and the fine is withheld from the `frozen` hashmap of the corresponding element of `past_elections`.

### 分配验证奖励

与检查是否是进行新选举的时候一样，选举人在每个区块中都会检查是否是释放`frozen`中存储的`past_elections`的资金的时候。在相应的区块中，选举人将相应验证轮次积累的收益（gas费和区块创建奖励）按验证者权重比例分配给该轮次的验证者。之后，质押和奖励被添加到`credits`表中，选举从`past_elections`表中删除。 At the corresponding block, the Elector distributes accumulated earnings from corresponding validation rounds (gas fees and block creation rewards) to validators of that round proportional to validator weights. After that, stakes with rewards are added to the `credits` table, and the election gets removed from `past_elections` table.

## 配置(Config)

Config smart contract controls TON configuration parameters. Its logic determines who and under what conditions has permission to change some of those parameters. It also implements a proposal/voting mechanism and validator set rolling updates.

### 验证者集合滚动更新

Once the Config contract gets a special message from the Elector contract that notifies it of a new validator set being elected, Config puts a new validator set to ConfigParam 36 (next validators). 一旦配置合约从选举人合约收到特殊消息，通知其新的验证者集合已经被选举出来，配置将新的验证者集合放到配置参数36（下一个验证者）。然后，在每个区块的TickTock交易期间，配置检查是否是应用新验证者集合的时候（验证者集合本身嵌入了时间`utime_since`），并将之前的集合从配置参数34（当前验证者）移动到配置参数32（之前的验证者），并从配置参数36设置到配置参数34。

### 提案/投票机制

Anyone who is ready to pay the storage fee for storing the proposal may propose a change of one or more configuration parameters by sending corresponding messages to the Config contract. In turn, any validator in the current set may vote for this proposal by signing an approval message with their private key (note that the corresponding public key is stored in ConfigParam 34). On gaining or not gaining 3/4 of the votes (with respect to validators' weight), the proposal wins or loses the round. Upon winning a critical number of rounds (`min_wins` ConfigParam 11), the proposal is accepted; upon losing a critical number of rounds (`max_losses` ConfigParam 11), it gets discarded.
Note that some of the parameters are considered critical (the set of critical parameters is itself a configuration parameter ConfigParam 10) and, thus require more rounds to be accepted.

配置参数索引`-999`、`-1000`、`-1001`预留用于投票紧急更新机制和更新配置和选举人合约的代码。当相应索引的提案在足够多轮次中获得足够的投票时，配置合约的代码或选举人合约的代码将被更新。 When the proposal with the corresponding indexes gains enough votes in enough rounds corresponding to the emergency key, the code of the Config contract or the code of the Elector contract gets updated.

#### 紧急更新

Validators may vote to assign a special public key to be able to update configuration parameters when it cannot be done via the voting mechanism. This is a temporary measure that is necessary during the active development of the network. It is expected that as the network matures, this measure will be phased out. As soon as it’s developed and tested, the key will be transferred to a multisignature solution. And once the network has proven its stability, the emergency mechanism will be completely discarded.

验证者确实在2021年7月投票将该密钥分配给TON基金会（主链区块`12958364`）。请注意，这样的密钥只能用来加速配置更新。它无法干预任何链上的任何合约的代码、存储和余额。 Note that such a key can only be used to speed up configuration updates. It has no ability to interfere with the code, storage, and balances of any contract on any chain.

紧急更新的历史：

- On April 17, 2022, the number of applications for the election grew big enough that the election could not be conducted under gas limits at that moment. In particular, elections required more than 10 million of gas, while the block `soft_limit` and `hard_limit` were set to `10m` and `20m`  (ConfigParam 22), `special_gas_limit` and `block_gas_limit` were set to `10m` and `10m`, respectively (ConfigParam 20). That way, new validators cannot be set, and due to reaching the block gas limit, transactions that process internal messages on the masterchain could not be included in the block. In turn, that leads to the inability to vote for configuration updates (it was impossible to win the required number of rounds since the current round was unable to finish). An emergency key was used to update ConfigParam 22 `soft_limit` to 22m and `hard_limit` to 25m (in block `19880281`) and ConfigParam 20 `special_gas_limit` to 20m and `block_gas_limit` to 22m (in block `19880300`). As a result, the election was successfully conducted, the next block consumed `10 001 444` gas. The total postponement of elections was about 6 hours, and the functionality of the base chain was unaffected.
- On March 2, 2023, the number of applications for the election grew big enough that even `20m` were not enough to conduct election. However, this time masterchain continue to process external messages due to higher `hard_limit`. An emergency key was used to update ConfigParam 20 `special_gas_limit` to 25m and `block_gas_limit` to 27m (in block `27747086`). As a result, the election was successfully conducted in next block. The total postponement of elections was about 6 hours, besides elections, functionality of the both master chain and base chain was unaffected.
- 2023年11月22日，密钥被用于[放弃自己](https://t.me/tonblockchain/221)（在区块`34312810`中）。结果，公钥被替换为32个零字节。 As a result, public key was replaced with 32 zero bytes.
- 由于切换到OpenSSL实现的Ed25519签名验证，检查特殊情况[所有公钥字节都相同](https://github.com/ton-blockchain/ton/blob/7fcf26771748338038aec4e9ec543dc69afeb1fa/crypto/ellcurve/Ed25519.cpp#L57C1-L57C1)被禁用。因此，针对零公钥的检查按预期停止工作。利用这个问题，紧急密钥在12月9日[再次更新](https://t.me/tonstatus/80)（在区块`34665437`，[交易](https://tonscan.org/tx/MU%2FNmSFkC0pJiCi730Fmt6PszBooRZkzgiQMv0sExfY=)），为 nothing-in-my-sleeve字节序列`82b17caadb303d53c3286c06a6e1affc517d1bc1d3ef2e4489d18b873f5d7cd1`，这是`sha256("Not a valid curve point")`。现在，更新网络配置参数的唯一方法是通过验证者共识。 As a result, check agaisnt zero public key stopped work as intended. Using this issue, emergency key was [updated on December 9](https://t.me/tonstatus/80) yet another time (in block `34665437`, [tx](https://tonscan.org/tx/MU%2FNmSFkC0pJiCi730Fmt6PszBooRZkzgiQMv0sExfY=)) to nothing-in-my-sleeve byte-sequence `82b17caadb303d53c3286c06a6e1affc517d1bc1d3ef2e4489d18b873f5d7cd1` that is `sha256("Not a valid curve point")`. Now, the only way to update network configuration parameters is through validator consensus.

## See Also

- [Precompiled Contracts](/develop/smart-contracts/core-contracts/precompiled)
