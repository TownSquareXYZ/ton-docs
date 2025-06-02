import Feedback from '@site/src/components/Feedback';

# Config parameters

:::info
You can view live values by using [Tonviewer](https://tonviewer.com/config).
:::

## Introduction

This page provides a description of the configuration parameters used in the TON Blockchain.

TON features a complex configuration consisting of many technical parameters, some of which are utilized by the blockchain itself, while others serve the ecosystem. However, only a limited number of individuals fully understand the significance of these parameters. This article aims to offer users a straightforward explanation of each parameter and its purpose.

## Prerequisites

This material should be read alongside the parameter list.

You can view the parameter values in the [current configuration](https://explorer.toncoin.org/config), and the method of writing them into [cells](/v3/concepts/dive-into-ton/ton-blockchain/cells-as-data-storage) is outlined in the [block.tlb](https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb) file in [TL-B](/v3/documentation/data-formats/tlb/tl-b-language) format.

:::info
The binary encoding found at the end of the TON Blockchain parameter represents a serialized binary format of its configuration. This allows for efficient storage and transmission of the configuration data. The specific details of the serialization process vary depending on the encoding scheme utilized by the TON Blockchain.
:::

All parameters are in place, and you won't get lost. For your convenience, please use the right sidebar for quick navigation.

## 参数 0

此参数是一个特殊智能合约的地址，该合约存储区块链的配置。配置存储在合约中，以简化其在验证者投票期间的加载和修改。

:::info
In the configuration parameter, only the hash portion of the address is recorded, as the contract always resides in the [MasterChain](/v3/concepts/dive-into-ton/ton-blockchain/blockchain-of-blockchains#masterchain-blockchain-of-blockchains) (WorkChain -1). Therefore, the full address of the contract will be written as `-1:<value of the configuration parameter>`.
:::

## 参数 1

This parameter is the address of the [elector smart contract](/v3/documentation/smart-contracts/contracts-specs/governance#elector), responsible for appointing validators, distributing rewards, and voting on changes to blockchain parameters.

## 参数 2

This parameter represents the address of the system, on behalf of which new Toncoins are minted and sent as rewards for validating the blockchain.

:::info
If the parameter 2 is missing, the parameter 0 is used instead (newly minted Toncoins come from the configuration smart contract).
:::

## 参数 3

此参数是交易费收集者的地址。

:::info
If the this parameter is missing (for the time being), transaction fees are directed to the elector smart contract (parameter 1).
:::

## 参数 4

此参数是TON网络的根DNS合约地址。

:::info
More detailed information, please see the [TON DNS & Domains](/v3/guidelines/web3/ton-dns/dns) documentation and in a more detailed original description [here](https://github.com/ton-blockchain/TEPs/blob/master/text/0081-dns-standard.md).

This contract is not responsible for selling **.ton** domains.
:::

## 参数 6

此参数负责新代币的铸造费用。

:::info
Currently, the minting of additional currency is not implemented and does not function. The implementation and launch of the minter are planned for the future.

You can learn more about the issues and prospects in the [relevant documentation](/v3/documentation/infra/minter-flow).
:::

## 参数 7

This parameter stores the volume of each additional currency in circulation. The data is organized as a dictionary (also referred to as a **hashmap**, although this name may be a typo during the TON Blockchain's development). The structure uses the format `extracurrency_id -> amount`, where the amount is represented as a `VarUint 32`, which is an integer ranging from `0` to `2^248`.

## 参数 8

此参数指示网络版本和验证者支持的额外功能。

:::info
Validators are nodes in the TON Blockchain network that are responsible for creating new blocks and verifying transactions.
:::

- `version`：此字段指定版本。

- `capabilities`：此字段是一组标志，用于指示某些功能或能力的存在或缺失。

Thus, when updating the network, validators will vote to change parameter 8. This way, the TON Blockchain network can be updated without downtime.

## 参数 9

此参数包含一个强制性参数的列表（二叉树）。它确保某些配置参数始终存在，并且在参数 9 变更之前，不能通过提案被删除。

## 参数 10

This parameter represents a list (binary tree) of critical TON parameters whose change significantly affects the network, so more voting rounds are held.

## 参数 11

此参数指出更改TON配置的提案在何种条件下被接受。

- `min_tot_rounds`: The minimum number of rounds before a proposal can be applied

- `max_tot_rounds`: The maximum number of rounds, upon reaching which the proposal will automatically be rejected

- `min_wins`: The required number of wins (3/4 of validators by the sum of the pledge must vote in favor)

- `max_losses`: The maximum number of losses, upon reaching which the proposal will automatically be rejected

- `min_store_sec` 和 `max_store_sec` 确定提案被存储的可能的时间间隔

- `bit_price` 和 `cell_price` 指出存储提案的一个位或一个cell的价格

## 参数 12

This parameter represents the configuration of a WorkChain in the TON Blockchain. WorkChains are designed as independent blockchains that can operate in parallel, allowing TON to scale and process a large number of transactions and smart contracts.

### WorkChain configuration parameters

- `enabled_since`: A UNIX timestamp of the moment this WorkChain was enabled.

- `actual_min_split`: The minimum depth of the split (sharding) of this WorkChain, supported by validators.

- `min_split`: The minimum depth of the split of this WorkChain, set by the configuration.

- `max_split`: The maximum depth of the split of this WorkChain.

- `basic`: A boolean flag (1 for true, 0 for false) indicating whether this WorkChain is basic (handles TON coins, smart contracts based on the TON Virtual Machine).

- `active`: A boolean flag indicating whether this WorkChain is active at the moment.

- `accept_msgs`: A boolean flag indicating whether this WorkChain is accepting messages at the moment.

- `flags`: Additional flags for the WorkChain (reserved, currently always 0).

- `zerostate_root_hash` and `zerostate_file_hash`: Hashes of the first block of the WorkChain.

- `version`: Version of the WorkChain.

- `format`: The format of the WorkChain, which includes `vm_version` and `vm_mode` - the virtual machine used there.

## 参数 13

This parameter defines the cost of filing complaints about incorrect operation of validators in the [elector smart contract](/v3/documentation/smart-contracts/contracts-specs/governance#elector).

## 参数 14

This parameter indicates the reward for creating a block in the TON Blockchain. Nanograms represent nanoToncoins. Therefore, the reward for block creation in the MasterChain is 1.7 Toncoins, while in the basic WorkChain, it is 1.0 Toncoins. In the event of a WorkChain split, the block reward is also divided: if there are two ShardChains within the WorkChain, then the reward for each shard block will be 0.5 Toncoins.

## 参数 15

此参数包含TON区块链中不同选举阶段和验证者工作的持续时间。

For each validation period, there is an `election_id` equal to the UNIX-format time at the start of the validation.

You can get the current `election_id` (if elections are ongoing) or the past one by invoking the elector smart contract's respective get-methods `active_election_id` and `past_election_ids`.

### WorkChain configuration parameters

- `validators_elected_for`: The number of seconds the elected set of validators perform their role (one round).

- `elections_start_before`: The seconds before the end of the current round the election process for the next period will start.

- `elections_end_before`: The seconds before the end of the current round, the validators for the next round will be chosen.

- `stake_held_for`: The period for which a validator's stake is held (for handling complaints) after the round expires.

:::info
参数中的每个值都由 `uint32` 数据类型确定。
:::

### 示例

In the TON Blockchain, validation periods are typically divided into **even** and **odd** rounds that alternate. Voting for the next round occurs during the previous one, so a validator must allocate their funds into two separate pools to participate in both rounds.

#### 主网

当前值：

```python
constants = {
    'validators_elected_for': 65536,  # 18.2 hours
    'elections_start_before': 32768,  # 9.1 hours
    'elections_end_before': 8192,     # 2.2 hours
    'stake_held_for': 32768           # 9.1 hours
}
```

方案：

![image](/img/docs/blockchain-configs/config15-mainnet.png)

#### 如何计算周期？

假设 `election_id = validation_start = 1600032768`。那么：

```python
election_start = election_id - constants['elections_start_before'] = 1600032768 - 32768 = 1600000000
election_end = delay_start = election_id - constants['elections_end_before'] = 1600032768 - 8192 = 1600024576
hold_start = validation_end = election_id + constants['validators_elected_for'] = 1600032768 + 65536 = 1600098304
hold_end = hold_start + constants['stake_held_for'] = 1600098304 + 32768 = 1600131072
```

Therefore, at this time, the length of one round of one parity is `1600131072 - 1600000000 = 131072 seconds = 36.40888... hours`

#### 测试网

当前值：

```python
constants = {
    'validators_elected_for': 7200,  # 2 hours
    'elections_start_before': 2400,  # 40 minutes
    'elections_end_before': 180,     # 3 minutes
    'stake_held_for': 900            # 15 minutes
}
```

Scheme:

![image](/img/docs/blockchain-configs/config15-testnet.png)

#### 如何计算周期？

假设 `election_id = validation_start = 160002400`。那么：

```python
election_start = election_id - constants['elections_start_before'] = 160002400 - 2400 = 1600000000
election_end = delay_start = election_id - constants['elections_end_before'] = 160002400 - 180 = 160002220
hold_start = validation_end = election_id + constants['validators_elected_for'] = 160002400 + 7200 = 160009600
hold_end = hold_start + constants['stake_held_for'] = 160009600 + 900 = 160010500
```

Therefore, at this time, the length of one round of one parity is `160010500 - 1600000000 = 10500 seconds = 175 minutes = 2.91666... hours`

## 参数 16

This parameter represents the limits on the number of validators in the TON Blockchain. It is directly used by the elector smart contract.

### Configuration parameters for the number of validators for elections

- `max_validators`：此参数代表任何给定时间可以参与网络运营的验证者的最大数量。

- `max_main_validators`：此参数代表主链验证者的最大数量。

- `min_validators`：此参数代表必须支持网络运营的最小验证者数量。

#### Notes

- The maximum number of validators is greater than or equal to the maximum number of MasterChain validators.

- The maximum number of MasterChain validators must be greater than or equal to the minimum number of validators.

- 验证者的最小数量不得少于1。

## 参数 17

此参数代表TON区块链中的质押参数配置。在许多区块链系统中，特别是使用权益证明或委托权益证明共识算法的系统中，网络原生加密货币的所有者可以“质押”他们的代币成为验证者并获得奖励。

### Configuration parameters

- `min_stake`: This parameter represents the minimum amount of Toncoins that an interested party needs to stake to participate in the validation process.

- `max_stake`: This parameter represents the maximum amount of Toncoins that an interested party can stake.

- `min_total_stake`: This parameter represents the minimum total amount of Toncoins that the chosen set of validators must hold.

- `max_stake_factor`：此参数是一个乘数，指示最大有效质押（抵押）可以超过任何其他验证者发送的最小质押的多少倍。

:::info
参数中的每个值都由 `uint32` 数据类型确定。
:::

## 参数 18

此参数代表确定TON区块链中数据存储价格的配置。这作为一种防止垃圾信息的措施，并鼓励网络维护。

### Dictionary of storage fee parameters

- `utime_since`：此参数提供指定价格适用的初始Unix时间戳。

- `bit_price_ps` and `cell_price_ps`: These parameters represent the storage prices for one bit or one cell of information in the main WorkChains of the TON Blockchain for 65536 seconds

- `mc_bit_price_ps` and `mc_cell_price_ps`: These parameters represent the prices for computational resources specifically in the TON MasterChain for 65536 seconds

:::info
`utime_since` accepts values in the `uint32` data type.

其余接受 `uint64` 数据类型的值。
:::

## 参数 20 和 21

这些参数定义了TON网络中计算的成本。任何计算的复杂性都以gas单位估计。

- `flat_gas_limit` 和 `flat_gas_price`：提供了一定数量的起始gas，价格为 `flat_gas_price`（用于抵消启动TON虚拟机的成本）。

- `gas_price`：此参数反映了网络中gas的价格，单位是每65536gas单位的nanotons。

- `gas_limit`：此参数代表每笔交易可消耗的最大gas量。

- `special_gas_limit`：此参数代表特殊（系统）合约每笔交易可消耗的gas量限制。

- `gas_credit`: This parameter represents a credit in gas units provided to transactions to check an external message.

- `block_gas_limit`：此参数代表单个区块内可消耗的最大gas量。

- `freeze_due_limit` and `delete_due_limit`: Limits of accumulated storage fees (in nanoToncoin) at which a contract is frozen and deleted, respectively.

:::info
You can find more about `gas_credit` and other parameters in the section of external messages [here](/v3/documentation/smart-contracts/transaction-fees/accept-message-effects#external-messages).
:::

## 参数 22 和 23

这些参数设置了区块的限制，达到这些限制时，区块将被完成，剩余消息的回调（如果有的话）将延续到下一个区块。

### Configuration parameters

- `bytes`：此部分设置了区块大小的字节限制。

- `underload`：负载不足是指分片意识到没有负载，并倾向于合并（如果相邻的分片愿意的话）。

- `soft_limit`：软限制 - 达到此限制时，内部消息停止处理。

- `hard_limit`：硬限制 - 这是绝对最大大小。

- `gas`: This section sets the limits on the amount of gas that a block can consume. Gas, in the context of blockchain, is an indicator of computational work. The limits on underload, soft and hard limits, work the same as for size in bytes.

- `lt_delta`: This section sets the limits on the difference in logical time between the first and last transaction. Logical time is a concept used in the TON Blockchain for ordering events. The limits on underload, soft and hard limits, work the same as for size in bytes and gas.

:::info
If a shard has insufficient load and there is an intention to merge with a neighboring shard, the `soft_limit` indicates a threshold. When this threshold is exceeded, internal messages will stop being processed, while external messages will still be handled. External messages will continue to be processed until the total reaches a limit that is equal to half the sum of the `soft_limit` and `hard_limit`, or `(soft_limit + hard_limit) / 2`.
:::

## 参数 24 和 25

Parameter 24 represents the configuration for the cost of sending messages in the MasterChain of the TON Blockchain.

参数 25 代表了所有其他情况下发送消息的成本配置。

### Configuration parameters defining the costs of forwarding

- `lump_price`：此参数表示转发消息的基础价格，无论其大小或复杂性如何。

- `bit_price`：此参数代表每位消息转发的成本。

- `cell_price`：此参数反映了每个cell消息转发的成本。cell是TON区块链上数据存储的基本单位。

- `ihr_price_factor`: This is a factor used to calculate the cost of immediate hypercube routing (IHR).

:::info
IHR is a method of message delivery in the TON Blockchain network, where messages are sent directly to the recipient's ShardChain.
:::

- `first_frac`：此参数定义了沿消息路线的第一次转换将使用的剩余的remainder的部分。

- `next_frac`：此参数定义了沿消息路线的后续转换将使用的剩余的remainder的部分。

## 参数 28

This parameter provides the configuration for the `Catchain` protocol in the TON Blockchain. `Catchain` is the lowest-level consensus protocol used in the TON to achieve agreement among validators.

### Configuration parameters

- `flags`：一个通用字段，可用于设置各种二进制参数。在这种情况下，它等于0，这意味着没有设置特定的标志。

- `shuffle_mc_validators`：一个布尔值，指示是否打乱主链验证者。如果此参数设置为1，则验证者将被打乱；否则，他们不会。

- `mc_catchain_lifetime`: The lifetime of MasterChain's `Catchain` groups in seconds.

- `shard_catchain_lifetime`: The lifetime of ShardChain's `Catchain` groups in seconds.

- `shard_validators_lifetime`: The lifetime of a ShardChain's validators group in seconds.

- `shard_validators_num`: The number of validators in each ShardChain validation group.

## 参数 29

This parameter provides the configuration for the consensus protocol above `Catchain` ([Param 28](#param-28)) in the TON Blockchain. The consensus protocol is a crucial component of a blockchain network, and it ensures that all nodes agree on the state of the distributed ledger.

### Configuration parameters

- `flags`：一个通用字段，可用于设置各种二进制参数。在这种情况下，它等于0，这意味着没有设置特定的标志。

- `new_catchain_ids`: A Boolean value indicating whether to generate new `Catchain` identifiers. If this parameter is set to 1, new identifiers will be generated. In this case, it is assigned the value of 1, which means that new identifiers will be generated.

- `round_candidates`：共识协议每轮考虑的候选人数量。这里设置为3。

- `next_candidate_delay_ms`：在生成区块候选权转移到下一个验证者之前的延迟（毫秒）。这里设置为2000毫秒（2秒）。

- `consensus_timeout_ms`：区块共识的超时时间（毫秒）。这里设置为16000毫秒（16秒）。

- `fast_attempts`：达成共识的“快速”尝试次数。这里设置为3。

- `attempt_duration`：每次达成一致的尝试持续时间。这里设置为8。

- `catchain_max_deps`：Catchain区块的最大依赖数量。这里设置为4。

- `max_block_bytes`：区块的最大大小（字节）。这里设置为2097152字节（2MB）。

- `max_collated_bytes`：序列化的区块正确性证明的最大大小（字节）。这里设置为2097152字节（2MB）。

- `proto_version`：协议版本。这里设置为2。

- `catchain_max_blocks_coeff`: The coefficient limiting the rate of block generation in `Catchain`, [description](https://github.com/ton-blockchain/ton/blob/master/doc/catchain-dos.md). Here, it is set to 10000.

## 参数 31

This parameter represents the configuration of smart contract addresses from which no fees are charged for either gas or storage and where **tick-tok** transactions can be created. The list usually includes governance contracts. The parameter is presented as a binary tree structure — a tree (HashMap 256), where the keys are a 256-bit representation of the address. Only addresses in the MasterChain can be present in this list.

## 参数 32、34 和 36

来自上一轮（32）、当前轮（34）和下一轮（36）的验证者列表。参数 36 负责从选举结束到轮次开始时设置。

### Configuration parameters

- `cur_validators`：这是当前的验证者列表。验证者通常负责在区块链网络中验证交易。

- `utime_since` 和 `utime_until`：这些参数提供了这些验证者活跃的时间段。

- `total` and `main`: These parameters provide the total number of validators and the number of validators validating the MasterChain in the network.

- `total_weight`：这将验证者的权重加起来。

- `list`: A list of validators in the tree format `id->validator-data`: `validator_addr`, `public_key`, `weight`, `adnl_addr`: These parameters provide details about each validator - their 256 addresses in the MasterChain, public key, weight, ADNL address (the address used at the network level of the TON).

## 参数 40

This parameter defines the structure of the configuration for punishment for improper behavior (non-validation). In the absence of the parameter, the default fine size is 101 Toncoins.

### Configuration parameters

`MisbehaviourPunishmentConfig`: This data structure defines how improper behavior in the system is punished.

它包含几个字段：

- `default_flat_fine`：这部分罚款与质押大小无关。

- `default_proportional_fine`：这部分罚款与验证者的质押大小成比例。

- `severity_flat_mult`：这是应用于验证者重大违规行为的 `default_flat_fine` 值的乘数。

- `severity_proportional_mult`：这是应用于验证者重大违规行为的 `default_proportional_fine` 值的乘数。

- `unpunishable_interval`：此参数代表违规者不受惩罚的期间，以消除临时网络问题或其他异常。

- `long_interval`、`long_flat_mult`、`long_proportional_mult`：这些参数定义了一个“长”时间段及其对不当行为的持平和比例罚款的乘数。

- `medium_interval`、`medium_flat_mult`、`medium_proportional_mult`：同样，它们定义了一个“中等”时间段及其对不当行为的持平和比例罚款的乘数。

## 参数 43

This parameter relates to the size limits and other features of accounts and messages.

### Configuration parameters

- `max_msg_bits`: Maximum message size in bits.

- `max_msg_cells`: Maximum number of cells (a form of storage unit) a message can occupy.

- `max_library_cells`: Maximum number of cells that can be used for library cells.

- `max_vm_data_depth`: Maximum cell depth in messages and account state.

- `max_ext_msg_size`: Maximum external message size in bits.

- `max_ext_msg_depth`: Maximum external message depth. This could refer to the depth of the data structure within the message.

- `max_acc_state_cells`: Maximum number of cells that an account state can occupy.

- `max_acc_state_bits`: Maximum account state size in bits.

如果缺失，默认参数为：

- `max_size` = 65535

- `max_depth` = 512

- `max_msg_bits` = 1 \<\< 21

- `max_msg_cells` = 1 \<\< 13

- `max_library_cells` = 1000

- `max_vm_data_depth` = 512

- `max_acc_state_cells` = 1 \<\< 16

- `max_acc_state_bits` = (1 \<\< 16) \* 1023

:::info
您可以在源代码[这里](https://github.com/ton-blockchain/ton/blob/fc9542f5e223140fcca833c189f77b1a5ae2e184/crypto/block/mc-config.h#L379)查看有关标准参数的更多详情。
:::

## 参数 44

此参数定义了被暂停的地址列表，这些地址在`suspended_until`之前不能被初始化。它仅适用于尚未启动的账户。这是稳定代币经济学的一种措施（限制早期矿工）。如果未设置 - 则没有限制。每个地址都表示为此树的一个终端节点，树状结构允许有效地检查地址在列表中的存在与否。

:::info
The stabilization of the tokenomics is further described in the [official report](https://t.me/tonblockchain/178) of the **@tonblockchain** Telegram channel.
:::

## 参数 71 - 73

The list of precompiled contracts is stored in the MasterChain config:

```
precompiled_smc#b0 gas_usage:uint64 = PrecompiledSmc;
precompiled_contracts_config#c0 list:(HashmapE 256 PrecompiledSmc) = PrecompiledContractsConfig;
_ PrecompiledContractsConfig = ConfigParam 45;
```

More details about precompiled contracts are on [this page](/v3/documentation/smart-contracts/contracts-specs/precompiled-contracts).

## 参数 71 - 73

This parameter pertains to bridges for wrapping Toncoins in other networks:

- ETH-TON **(71)**

- BSC-TON **(72)**

- Polygon-TON **(73)**

### Configuration parameters

- `bridge_address`: This is the bridge contract address that accepts TON to issue wrapped Toncoins in other networks.

- `oracle_multisig_address`: 这是 bridge 管理钱包地址。 多重钱包是一种数字钱包类型，需要多方签名授权交易。 它常常被用来加强安全，Oracle充当这些方面的角色。

- `oracles`: List of oracles in the form of a tree `id->address`

- `external_chain_address`：对应外部区块链中的桥合约地址。

## 参数 79, 81 和 82

This parameter relates to bridges for wrapping tokens from other networks into tokens on the TON network:

- ETH-TON **(79)**

- BSC-TON **(81)**

- Polygon-TON **(82)**

### Configuration parameters

- `bridge_address` 和 `oracles_address`：这些是桥和桥管理合约（预言机多签）的区块链地址。

- `oracles`: List of oracles in the form of a tree `id->address`

- `state_flags`：状态标志。该参数负责启用/禁用不同的 bridge 功能。

- `prices`：此参数包含用于桥的不同操作或费用的价格列表或字典，例如 `bridge_burn_fee`、`bridge_mint_fee`、`wallet_min_tons_for_storage`、`wallet_gas_consumption`、`minter_min_tons_for_storage`、`discover_gas_consumption`。

- `external_chain_address`：另一区块链中的桥合约地址。

## Negative parameters

:::info
The distinction between negative and positive parameters lies in the necessity for validators to verify them; negative parameters typically lack a specific assigned role.
:::

## Next steps

After thoroughly reviewing this article, it is highly recommended that you dedicate time for a more in-depth study of the following documents:

- The original descriptions are present, but they may be limited, in the documents:
    - [The Open Network Whitepaper](https://ton.org/whitepaper.pdf)
    - [Telegram Open Network Blockchain](/tblkch.pdf)

- Source code:
    - [mc-config.h](https://github.com/ton-blockchain/ton/blob/fc9542f5e223140fcca833c189f77b1a5ae2e184/crypto/block/mc-config.h)
    - [block.tlb](https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb)
    - [BlockMasterConfig Type](https://docs.evercloud.dev/reference/graphql-api/field_descriptions#blockmasterconfig-type)

## See also

On these pages, you can find active network configurations of the TON Blockchain:

- [Mainnet configuration](https://ton.org/global-config.json)
- [Testnet configuration](https://ton.org/testnet-global.config.json)
- [Russian version](https://github.com/delovoyhomie/description-config-for-TON-Blockchain/blob/main/Russian-version.md)

<Feedback />

