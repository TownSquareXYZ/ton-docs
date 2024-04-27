# 交易布局

:::info
为了最大限度地理解这个页面，强烈建议您熟悉[TL-B 语言](/develop/data-formats/cell-boc)。
:::

TON 区块链运作依赖于三个关键部分：账户、消息和交易。本页面描述了交易的结构和布局。

交易是一种操作，处理与特定账户相关的进出消息，改变其状态，并可能为验证者生成费用。

## 交易

```tlb
transaction$0111 account_addr:bits256 lt:uint64
    prev_trans_hash:bits256 prev_trans_lt:uint64 now:uint32
    outmsg_cnt:uint15
    orig_status:AccountStatus end_status:AccountStatus
    ^[ in_msg:(Maybe ^(Message Any)) out_msgs:(HashmapE 15 ^(Message Any)) ]
    total_fees:CurrencyCollection state_update:^(HASH_UPDATE Account)
    description:^TransactionDescr = Transaction;
```

| 字段                | 类型                                                                     | 必需 | 描述                                                                                                                                                |
| ----------------- | ---------------------------------------------------------------------- | -- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `account_addr`    | bits256                                                                | 是  | 执行交易的地址的哈希部分。[更多关于地址](https://docs.ton.org/learn/overviews/addresses#address-of-smart-contract)                                                   |
| `lt`              | uint64                                                                 | 是  | 代表 _逻辑时间_。[更多关于逻辑时间](https://docs.ton.org/develop/smart-contracts/guidelines/message-delivery-guarantees#what-is-a-logical-time)                  |
| `prev_trans_hash` | bits256                                                                | 是  | 该账户上一个交易的哈希。                                                                                                                                      |
| `prev_trans_lt`   | uint64                                                                 | 是  | 该账户上一个交易的 `lt`。                                                                                                                                   |
| `now`             | uint32                                                                 | 是  | 执行此交易时设置的 `now` 值。它是以秒为单位的Unix时间戳。                                                                                                                |
| `outmsg_cnt`      | uint15                                                                 | 是  | 执行此交易时创建的输出消息数量。                                                                                                                                  |
| `orig_status`     | [AccountStatus](#accountstatus)                                        | 是  | 执行交易前该账户的状态。                                                                                                                                      |
| `end_status`      | [AccountStatus](#accountstatus)                                        | 是  | 执行交易后该账户的状态。                                                                                                                                      |
| `in_msg`          | (Message Any)                                       | 否  | 触发执行交易的输入消息。存储在一个引用中。                                                                                                                             |
| `out_msgs`        | HashmapE 15 ^(Message Any)                          | 是  | 包含执行此交易时创建的输出消息列表的字典。                                                                                                                             |
| `total_fees`      | [CurrencyCollection](/develop/data-formats/msg-tlb#currencycollection) | 是  | 执行此交易时收集的总费用。它包括_Toncoin_值和可能的一些[额外代币](https://docs.ton.org/develop/dapps/defi/coins#extra-currencies)。 |
| `state_update`    | [HASH_UPDATE](#hash_update) Account               | 是  | `HASH_UPDATE` 结构。存储在一个引用中。                                                                                                                        |
| `description`     | [TransactionDescr](#transactiondescr-types)                            | 是  | 交易执行过程的详细描述。存储在一个引用中。                                                                                                                             |

## AccountStatus

```tlb
acc_state_uninit$00 = AccountStatus;
acc_state_frozen$01 = AccountStatus;
acc_state_active$10 = AccountStatus;
acc_state_nonexist$11 = AccountStatus;
```

- `[00]`：账户未初始化
- `[01]`：账户被冻结
- `[10]`：账户活跃
- `[11]`：账户不存在

## HASH_UPDATE

```tlb
update_hashes#72 {X:Type} old_hash:bits256 new_hash:bits256
    = HASH_UPDATE X;
```

| Field      | Type    | Description                                                                     |
| ---------- | ------- | ------------------------------------------------------------------------------- |
| `old_hash` | bits256 | The hash of the account state before executing the transaction. |
| `new_hash` | bits256 | The hash of the account state after executing the transaction.  |

## TransactionDescr Types

- [Ordinary](#ordinary)
- [Storage](#storage)
- [Tick-tock](#tick-tock)
- [Split prepare](#split-prepare)
- [Split install](#split-install)
- [Merge prepare](#merge-prepare)
- [Merge install](#merge-install)

## Ordinary

This is the most common type of transaction and it fulfills most developers' needs. Transactions of this type have exactly one incoming message and can create several outgoing messages.

```tlb
trans_ord$0000 credit_first:Bool
    storage_ph:(Maybe TrStoragePhase)
    credit_ph:(Maybe TrCreditPhase)
    compute_ph:TrComputePhase action:(Maybe ^TrActionPhase)
    aborted:Bool bounce:(Maybe TrBouncePhase)
    destroyed:Bool
    = TransactionDescr;
```

| Field          | Type           | Required | Description                                                                                                                                                                                                                               |
| -------------- | -------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `credit_first` | Bool           | Yes      | A flag that correlates with `bounce` flag of an incoming message. `credit_first = !bounce`                                                                                                                                |
| `storage_ph`   | TrStoragePhase | No       | Contains information about storage phase of a transaction execution. [More Info](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                                        |
| `credit_ph`    | TrCreditPhase  | No       | Contains information about credit phase of a transaction execution. [More Info](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                                         |
| `compute_ph`   | TrComputePhase | Yes      | Contains information about compute phase of a transaction execution. [More Info](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                                        |
| `action`       | TrActionPhase  | No       | Contains information about action phase of a transaction execution. [More Info](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases). Stored in a reference. |
| `aborted`      | Bool           | Yes      | Indicates whether the transaction execution was aborted.                                                                                                                                                                  |
| `bounce`       | TrBouncePhase  | No       | Contains information about bounce phase of a transaction execution. [More Info](https://docs.ton.org/develop/smart-contracts/guidelines/non-bouncable-messages)                                                           |
| `destroyed`    | Bool           | Yes      | Indicates whether the account was destroyed during the execution.                                                                                                                                                         |

## Storage

Transactions of this type can be inserted by validators at their discretion. They do not process any inbound messages and do not invoke any code. Their only effect is to collect storage payments from an account, affecting its storage statistics and balance. If the resulting _Toncoin_ balance of the account drops below a certain amount, the account may be frozen, and its code and data replaced by their combined hash.

```tlb
trans_storage$0001 storage_ph:TrStoragePhase
    = TransactionDescr;
```

| Field        | Type           | Description                                                                                                                                                                        |
| ------------ | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `storage_ph` | TrStoragePhase | Contains information about storage phase of a transaction execution. [More Info](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases) |

## Tick-tock

`Tick` and `Tock` transactions are reserved for special system smart contracts that are required to be automatically invoked in each block. `Tick` transactions are invoked at the beginning of each masterchain block, and `Tock` transactions are invoked at the end.

```tlb
trans_tick_tock$001 is_tock:Bool storage_ph:TrStoragePhase
    compute_ph:TrComputePhase action:(Maybe ^TrActionPhase)
    aborted:Bool destroyed:Bool = TransactionDescr;
```

| Field        | Type           | Required | Description                                                                                                                                                                                                                               |
| ------------ | -------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `is_tock`    | Bool           | Yes      | A flag indicating the type of transaction. Used to separate `Tick` and `Tock` transactions                                                                                                                                |
| `storage_ph` | TrStoragePhase | Yes      | Contains information about storage phase of a transaction execution. [More Info](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                                        |
| `compute_ph` | TrComputePhase | Yes      | Contains information about compute phase of a transaction execution. [More Info](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                                        |
| `action`     | TrActionPhase  | No       | Contains information about action phase of a transaction execution. [More Info](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases). Stored in a reference. |
| `aborted`    | Bool           | Yes      | Indicates whether the transaction execution was aborted.                                                                                                                                                                  |
| `destroyed`  | Bool           | Yes      | Indicates whether the account was destroyed during the execution.                                                                                                                                                         |

## Split Prepare

:::note
This type of transaction is currently not in use. Information about this process is limited.
:::

Split transactions are initiated on large smart contracts that need to be divided under high load. The contract should support this transaction type and manage the splitting process to balance the load.

在需要因高负载而拆分的大型智能合约上启动拆分交易。合约应支持此类型的交易并管理拆分过程以平衡负载。

```tlb
trans_split_prepare$0100 split_info:SplitMergeInfo
    storage_ph:(Maybe TrStoragePhase)
    compute_ph:TrComputePhase action:(Maybe ^TrActionPhase)
    aborted:Bool destroyed:Bool
    = TransactionDescr;
```

| Field        | Type           | Required | Description                                                                                                                                                                                                                               |
| ------------ | -------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `split_info` | SplitMergeInfo | Yes      | Information about split process.                                                                                                                                                                                          |
| `storage_ph` | TrStoragePhase | No       | Contains information about storage phase of a transaction execution. [More Info](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                                        |
| `compute_ph` | TrComputePhase | Yes      | Contains information about compute phase of a transaction execution. [More Info](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                                        |
| `action`     | TrActionPhase  | No       | Contains information about action phase of a transaction execution. [More Info](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases). Stored in a reference. |
| `aborted`    | Bool           | Yes      | Indicates whether the transaction execution was aborted.                                                                                                                                                                  |
| `destroyed`  | Bool           | Yes      | Indicates whether the account was destroyed during the execution.                                                                                                                                                         |

## Split install

:::note
This type of transaction is currently not in use. Information about this process is limited.
:::

Split Install transactions are used for creating new instances of large smart contracts. The state for the new smart contract is generated by a [Split Prepare](#split-prepare) transaction.

```tlb
trans_split_install$0101 split_info:SplitMergeInfo
    prepare_transaction:^Transaction
    installed:Bool = TransactionDescr;
```

| Field                 | Type                        | Description                                                                                                                                  |
| --------------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `split_info`          | SplitMergeInfo              | Information about split process.                                                                                             |
| `prepare_transaction` | [Transaction](#transaction) | Information about the [transaction prepared](#split-prepare) for the split operation. Stored in a reference. |
| `installed`           | Bool                        | Indicates whether the transaction was installed.                                                                             |

## Merge prepare

:::note
This type of transaction is currently not in use. Information about this process is limited.
:::

Merge transactions are initiated on large smart contracts that need to recombine after being split due to high load. The contract should support this transaction type and manage the merging process to balance the load.

在需要因高负载而重新组合的大型智能合约上启动合并交易。合约应支持此类型的交易并管理合并过程以平衡负载。

```tlb
trans_merge_prepare$0110 split_info:SplitMergeInfo
    storage_ph:TrStoragePhase aborted:Bool
    = TransactionDescr;
```

| Field        | Type           | Description                                                                                                                                                                        |
| ------------ | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `split_info` | SplitMergeInfo | Information about merge process.                                                                                                                                   |
| `storage_ph` | TrStoragePhase | Contains information about storage phase of a transaction execution. [More Info](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases) |
| `aborted`    | Bool           | Indicates whether the transaction execution was aborted.                                                                                                           |

## Merge install

:::note
This type of transaction is currently not in use. Information about this process is limited.
:::

Merge Install transactions are used for merging instances of large smart contracts. The special message facilitating the merge is generated by a [Merge Prepare](#merge-prepare) transaction.

```tlb
trans_merge_install$0111 split_info:SplitMergeInfo
    prepare_transaction:^Transaction
    storage_ph:(Maybe TrStoragePhase)
    credit_ph:(Maybe TrCreditPhase)
    compute_ph:TrComputePhase action:(Maybe ^TrActionPhase)
    aborted:Bool destroyed:Bool
    = TransactionDescr;
```

| Field                 | Type                        | Required | Description                                                                                                                                                                                                                               |
| --------------------- | --------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `split_info`          | SplitMergeInfo              | Yes      | Information about merge process.                                                                                                                                                                                          |
| `prepare_transaction` | [Transaction](#transaction) | Yes      | Information about the [transaction prepared](#merge-prepare) for the merge operation. Stored in a reference.                                                                                              |
| `storage_ph`          | TrStoragePhase              | No       | Contains information about storage phase of a transaction execution. [More Info](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                                        |
| `credit_ph`           | TrCreditPhase               | No       | Contains information about credit phase of a transaction execution. [More Info](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                                         |
| `compute_ph`          | TrComputePhase              | Yes      | Contains information about compute phase of a transaction execution. [More Info](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                                        |
| `action`              | TrActionPhase               | No       | Contains information about action phase of a transaction execution. [More Info](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases). Stored in a reference. |
| `aborted`             | Bool                        | Yes      | Indicates whether the transaction execution was aborted.                                                                                                                                                                  |
| `destroyed`           | Bool                        | Yes      | Indicates whether the account was destroyed during the execution.                                                                                                                                                         |

## See also

- Original description of [Transaction layout](https://ton.org/docs/tblkch.pdf#page=75\&zoom=100,148,290) from whitepaper
