import Feedback from '@site/src/components/Feedback';

# چیدمان تراکنش

:::info
It's highly recommended that you familiarize yourself with the [TL-B language](/v3/documentation/data-formats/tlb/cell-boc) to better understand this page.
:::

The TON blockchain functions through three main components: accounts, messages, and transactions. This section outlines the structure and organization of transactions.

A transaction is an action that handles incoming and outgoing messages for a particular account, modifying its state and potentially generating fees for validators.

## تراکنش

```tlb
transaction$0111 account_addr:bits256 lt:uint64
    prev_trans_hash:bits256 prev_trans_lt:uint64 now:uint32
    outmsg_cnt:uint15
    orig_status:AccountStatus end_status:AccountStatus
    ^[ in_msg:(Maybe ^(Message Any)) out_msgs:(HashmapE 15 ^(Message Any)) ]
    total_fees:CurrencyCollection state_update:^(HASH_UPDATE Account)
    description:^TransactionDescr = Transaction;
```

| فیلد              | نوع                                                                           | ضروری | توضیحات                                                                                                                                                                                       |
| ----------------- | ----------------------------------------------------------------------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `account_addr`    | bits256                                                                       | بله   | The hash of the address where the transaction was executed. [Learn more about addresses](/v3/documentation/smart-contracts/addresses#address-of-smart-contract)               |
| `lt`              | uint64                                                                        | بله   | Represents *Logical time*. [Learn more about logical time](/v3/documentation/smart-contracts/message-management/messages-and-transactions#what-is-a-logical-time)             |
| `prev_trans_hash` | bits256                                                                       | بله   | The hash of the previous transaction for this account.                                                                                                                        |
| `prev_trans_lt`   | uint64                                                                        | بله   | The `lt` of the previous transaction for this account.                                                                                                                        |
| `now`             | uint32                                                                        | بله   | The `now`  value set during the transaction execution. It is a UNIX timestamp in seconds.                                                                     |
| `outmsg_cnt`      | uint15                                                                        | بله   | The count of outgoing messages generated during the transaction execution.                                                                                                    |
| `orig_status`     | [وضعیت حساب](#accountstatus)                                                  | بله   | وضعیت این حساب قبل از اجرای تراکنش.                                                                                                                                           |
| `end_status`      | [وضعیت حساب](#accountstatus)                                                  | بله   | The status of the account after the transaction was executed.                                                                                                                 |
| `in_msg`          | (هر پیامی)                                                 | خیر   | The incoming message that triggered the transaction execution. Stored as a reference.                                                                         |
| `out_msgs`        | HashmapE 15 ^(هر پیامی)                                    | بله   | A dictionary containing the outgoing messages created during the transaction execution.                                                                                       |
| `total_fees`      | [مجموعه‌ارزها](/v3/documentation/data-formats/tlb/msg-tlb#currencycollection) | بله   | The total fees collected during the transaction execution, including *TON coin* and potentially some [extra-currencies](/v3/documentation/dapps/defi/coins#extra-currencies). |
| `state_update`    | [به‌روزرسانی_هش](#hash_update) حساب                      | بله   | The `HASH_UPDATE` structure represents the state change. Stored as a reference.                                                                               |
| `description`     | [توضیحات تراکنش](#transactiondescr-types)                                     | بله   | A detailed description of the transaction execution process. Stored as a reference.                                                                           |

## وضعیت حساب

```tlb
acc_state_uninit$00 = AccountStatus;
acc_state_frozen$01 = AccountStatus;
acc_state_active$10 = AccountStatus;
acc_state_nonexist$11 = AccountStatus;
```

- `[00]`: Account is uninitialized
- `[01]`: Account is frozen
- `[10]`: Account is active
- `[11]`: Account does not exist

## به‌روزرسانی_هش

```tlb
update_hashes#72 {X:Type} old_hash:bits256 new_hash:bits256
    = HASH_UPDATE X;
```

| فیلد       | نوع     | توضیحات                                                                                |
| ---------- | ------- | -------------------------------------------------------------------------------------- |
| `old_hash` | bits256 | The hash represents the account state before transaction execution.    |
| `new_hash` | bits256 | The hash represents the account state following transaction execution. |

## TransactionDescr types

- [عادی](#ordinary)
- [ذخیره سازی](#storage)
- [تیک‌تاک](#tick-tock)
- [آماده‌سازی تقسیم](#split-prepare)
- [نصب تقسیم](#split-install)
- [آماده‌سازی ادغام](#merge-prepare)
- [نصب ادغام](#merge-install)

## معمولی

This is the most common transaction type, meeting most developers' requirements. Transactions of this type have a single incoming message and can generate multiple outgoing messages.

```tlb
trans_ord$0000 credit_first:Bool
    storage_ph:(Maybe TrStoragePhase)
    credit_ph:(Maybe TrCreditPhase)
    compute_ph:TrComputePhase action:(Maybe ^TrActionPhase)
    aborted:Bool bounce:(Maybe TrBouncePhase)
    destroyed:Bool
    = TransactionDescr;
```

| فیلد           | نوع            | ضروری | توضیحات                                                                                                                                                                                                                       |
| -------------- | -------------- | ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `credit_first` | باینری         | بله   | A flag related to the `bounce` flag of an incoming message. `credit_first = !bounce`.                                                                                                         |
| `storage_ph`   | TrStoragePhase | خیر   | Contains information about the storage phase during the transaction execution. [More info](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                                                        |
| `credit_ph`    | TrCreditPhase  | خیر   | Contains information about the credit phase during the transaction execution. [More info](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                                                         |
| `compute_ph`   | TrComputePhase | بله   | Contains information about the compute phase during the transaction execution. [More info](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                                                        |
| `action`       | TrActionPhase  | خیر   | Contains information about the action phase during the transaction execution. [More info](/v3/documentation/tvm/tvm-overview#transactions-and-phases). Stored in a reference. |
| `aborted`      | Bool           | بله   | نشان می‌دهد آیا اجرای تراکنش متوقف شده است یا خیر.                                                                                                                                                            |
| `bounce`       | TrBouncePhase  | خیر   | Contains information about the bounce phase during the transaction execution. [More info](/v3/documentation/smart-contracts/message-management/non-bounceable-messages)                                       |
| `destroyed`    | Bool           | بله   | نشان می‌دهد آیا حساب در طول اجرا نابود شده است یا خیر.                                                                                                                                                        |

## ذخیره‌سازی

Validators can add transactions of this type as they see fit. They do not handle incoming messages or trigger codes. Their sole purpose is to collect storage fees from an account, impacting its storage statistics and balance. If the resulting *TON coin* balance of the account falls below a specified threshold, the account may be frozen, and its code and data will be replaced with their combined hash.

```tlb
trans_storage$0001 storage_ph:TrStoragePhase
    = TransactionDescr;
```

| فیلد         | نوع            | توضیحات                                                                                                                                                          |
| ------------ | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `storage_ph` | TrStoragePhase | Contains information about the storage phase of a transaction execution. [More Info](/v3/documentation/tvm/tvm-overview#transactions-and-phases) |

## تیک‌تاک

`Tick` and `Tock` transactions are designated for special system smart contracts that must be automatically invoked in every block. `Tick` transactions are executed at the start of each MasterChain block, while `Tock` transactions are initiated at the end.

```tlb
trans_tick_tock$001 is_tock:Bool storage_ph:TrStoragePhase
    compute_ph:TrComputePhase action:(Maybe ^TrActionPhase)
    aborted:Bool destroyed:Bool = TransactionDescr;
```

| فیلد         | نوع            | ضروری | توضیحات                                                                                                                                                                                                                   |
| ------------ | -------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `is_tock`    | Bool           | بله   | A flag that indicates the type of transaction used to distinguish between `Tick` and `Tock` transactions.                                                                                                 |
| `storage_ph` | TrStoragePhase | بله   | Provides information about the storage phase of the transaction execution. [More info](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                                                        |
| `compute_ph` | TrComputePhase | بله   | Provides information about the compute phase of the transaction execution. [More info](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                                                        |
| `action`     | TrActionPhase  | خیر   | Provides information about the action phase of the transaction execution. [More info](/v3/documentation/tvm/tvm-overview#transactions-and-phases). Stored as a reference. |
| `aborted`    | Bool           | بله   | نشان می‌دهد آیا اجرای تراکنش متوقف شده است یا خیر.                                                                                                                                                        |
| `destroyed`  | Bool           | بله   | Indicates whether the account was destroyed during execution.                                                                                                                                             |

## Split prepare

:::note
This type of transaction is currently not in use, and details about its implementation are limited.
:::

Split transactions are designed for large smart contracts that must be divided due to high load. The contract must support this transaction type and manage the splitting process to distribute the load effectively.

**Split prepare** transactions are triggered when a smart contract needs to be split. The smart contract should generate the state necessary to create a new instance that will be deployed.

```tlb
trans_split_prepare$0100 split_info:SplitMergeInfo
    storage_ph:(Maybe TrStoragePhase)
    compute_ph:TrComputePhase action:(Maybe ^TrActionPhase)
    aborted:Bool destroyed:Bool
    = TransactionDescr;
```

| فیلد         | نوع            | ضروری | توضیحات                                                                                                                                                                                                                   |
| ------------ | -------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `split_info` | SplitMergeInfo | بله   | Contains information about the split process.                                                                                                                                                             |
| `storage_ph` | TrStoragePhase | No    | Provides details about the storage phase during transaction execution. [More info](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                                                            |
| `compute_ph` | TrComputePhase | Yes   | CContains details about the compute phase during transaction execution. [More info](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                                                           |
| `action`     | TrActionPhase  | No    | Provides information about the action phase during transaction execution. [More info](/v3/documentation/tvm/tvm-overview#transactions-and-phases). Stored as a reference. |
| `aborted`    | Bool           | Yes   | Indicates whether the transaction execution was aborted.                                                                                                                                                  |
| `destroyed`  | Bool           | Yes   | Indicates whether the account was destroyed during execution.                                                                                                                                             |

## Split install

:::note
This transaction type is currently unavailable, and available information is limited.
:::

**Split install** transactions are used to deploy new instances of large smart contracts. A [split prepare](#split-prepare) transaction generates the state for the new contract.

```tlb
trans_split_install$0101 split_info:SplitMergeInfo
    prepare_transaction:^Transaction
    installed:Bool = TransactionDescr;
```

| فیلد                  | نوع                                                         | توضیحات                                                                                                                                      |
| --------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `split_info`          | اطلاعات جداسازی و ادغام (SplitMergeInfo) | Information about the split process.                                                                                         |
| `prepare_transaction` | [تراکنش](#transaction)                                      | Information about the [transaction prepared](#split-prepare) for the split operation. Stored as a reference. |
| `installed`           | بول (Bool)                               | نشان می‌دهد که آیا تراکنش نصب شده است یا خیر.                                                                                |

## آماده‌سازی تلفیق

:::note
This transaction type is currently unavailable, and available information is limited.
:::

Merge transactions are triggered for large smart contracts that need to recombine after being split under high load. The contract must support this transaction type and handle the merging process to help balance system resources.

**Merge prepare** transactions are initiated when two smart contracts are set to merge. The contract should generate a message to the other instance to initiate and facilitate the merge process.

```tlb
trans_merge_prepare$0110 split_info:SplitMergeInfo
    storage_ph:TrStoragePhase aborted:Bool
    = TransactionDescr;
```

| فیلد         | نوع                                                         | توضیحات                                                                                                                                                            |
| ------------ | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `split_info` | اطلاعات جداسازی و ادغام (SplitMergeInfo) | Information about the merge process.                                                                                                               |
| `storage_ph` | مرحله ذخیره‌سازی تراکنش (TrStoragePhase) | Contains information about the storage phase during transaction execution. [More info](/v3/documentation/tvm/tvm-overview#transactions-and-phases) |
| `aborted`    | بول (Bool)                               | نشان می‌دهد که آیا اجری تراکنش متوقف‌شده است.                                                                                                      |

## نصب تلفیق

:::note
This transaction type is currently unavailable, and available information is limited.
:::

**Merge install** transactions are used to merge instances of large smart contracts. A [merge prepare](#merge-prepare) transaction generates a special message that facilitates the merge.

```tlb
trans_merge_install$0111 split_info:SplitMergeInfo
    prepare_transaction:^Transaction
    storage_ph:(Maybe TrStoragePhase)
    credit_ph:(Maybe TrCreditPhase)
    compute_ph:TrComputePhase action:(Maybe ^TrActionPhase)
    aborted:Bool destroyed:Bool
    = TransactionDescr;
```

| فیلد                  | نوع                                                         | ضروری | توضیحات                                                                                                                                                                                                               |
| --------------------- | ----------------------------------------------------------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `split_info`          | اطلاعات جداسازی و ادغام (SplitMergeInfo) | بله   | Information about the merge process.                                                                                                                                                                  |
| `prepare_transaction` | [تراکنش](#transaction)                                      | بله   | Information about the [transaction prepared](#merge-prepare) for the merge operation. Stored as a reference.                                                                          |
| `storage_ph`          | مرحله ذخیره‌سازی تراکنش (TrStoragePhase) | خیر   | Contains information about the storage phase of transaction execution. [More info](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                                                        |
| `credit_ph`           | مرحله اعتباردهی تراکنش (TrCreditPhase)   | خیر   | Contains information about the credit phase of transaction execution. [More info](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                                                         |
| `compute_ph`          | مرحله محاسبه تراکنش (TrComputePhase)     | بله   | Contains information about the compute phase of transaction execution. [More info](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                                                        |
| `action`              | مرحله اقدام تراکنش (TrActionPhase)       | خیر   | Contains information about the action phase of transaction execution. [More info](/v3/documentation/tvm/tvm-overview#transactions-and-phases). Stored as a reference. |
| `aborted`             | بول (Bool)                               | بله   | Indicates whether the transaction was aborted during execution.                                                                                                                                       |
| `destroyed`           | بول (Bool)                               | بله   | Indicates whether the account was destroyed during execution.                                                                                                                                         |

## همچنین ببینید

- The initial explanation of the transaction layout from the whitepaper.

<Feedback />

