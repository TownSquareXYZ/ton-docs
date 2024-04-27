# 区块布局

:::info
为了最大限度地理解本页内容，强烈建议您熟悉 [TL-B 语言](/develop/data-formats/cell-boc)。
:::

区块链中的一个区块是一条新交易记录，一旦完成，就会作为这个去中心化账本的永久且不可更改的一部分被添加到区块链上。每个区块包含交易数据、时间以及对前一个区块的引用等信息，从而形成一个区块链。

TON 区块链中的区块由于系统的整体复杂性而具有相当复杂的结构。本页描述了这些区块的结构和布局。

## 区块

一个区块的原始 TL-B 方案如下：

```tlb
block#11ef55aa global_id:int32
    info:^BlockInfo value_flow:^ValueFlow
    state_update:^(MERKLE_UPDATE ShardState)
    extra:^BlockExtra = Block;
```

让我们仔细看看每个字段。

## global_id:int32

创建此区块的网络的 ID。主网为 `-239`，测试网为 `-3`。

## info:^BlockInfo

此字段包含关于区块的信息，如其版本、序列号、标识符和其他标志位。

```tlb
block_info#9bc7a987 version:uint32
    not_master:(## 1)
    after_merge:(## 1) before_split:(## 1)
    after_split:(## 1)
    want_split:Bool want_merge:Bool
    key_block:Bool vert_seqno_incr:(## 1)
    flags:(## 8) { flags <= 1 }
    seq_no:# vert_seq_no:# { vert_seq_no >= vert_seqno_incr }
    { prev_seq_no:# } { ~prev_seq_no + 1 = seq_no }
    shard:ShardIdent gen_utime:uint32
    start_lt:uint64 end_lt:uint64
    gen_validator_list_hash_short:uint32
    gen_catchain_seqno:uint32
    min_ref_mc_seqno:uint32
    prev_key_block_seqno:uint32
    gen_software:flags . 0?GlobalVersion
    master_ref:not_master?^BlkMasterInfo
    prev_ref:^(BlkPrevInfo after_merge)
    prev_vert_ref:vert_seqno_incr?^(BlkPrevInfo 0)
    = BlockInfo;
```

| 字段                              | 类型                                           | 描述                                                                                                                                                    |
| ------------------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `version`                       | uint32                                       | 区块结构的版本。                                                                                                                                              |
| `not_master`                    | (## 1)                    | 标志位，表示此区块是否为主链区块。                                                                                                                                     |
| `after_merge`                   | (## 1)                    | 标志位，表示此区块是否在两个分片链合并后创建，因此它有两个父区块。                                                                                                                     |
| `before_split`                  | (## 1)                    | 标志位，表示此区块是否在其分片链分裂前创建。                                                                                                                                |
| `after_split`                   | (## 1)                    | 标志位，表示此区块是否在其分片链分裂后创建。                                                                                                                                |
| `want_split`                    | Bool                                         | 标志位，表示是否希望分片链分裂。                                                                                                                                      |
| `want_merge`                    | Bool                                         | 标志位，表示是否希望分片链合并。                                                                                                                                      |
| `key_block`                     | Bool                                         | 标志位，表示此区块是否为关键区块。                                                                                                                                     |
| `vert_seqno_incr`               | (## 1)                    | 垂直序列号的增量。                                                                                                                                             |
| `flags`                         | (## 8)                    | 区块的附加标志位。                                                                                                                                             |
| `seq_no`                        | #                                            | 与区块相关的序列号。                                                                                                                                            |
| `vert_seq_no`                   | #                                            | 与区块相关的垂直序列号。                                                                                                                                          |
| `shard`                         | ShardIdent                                   | The identifier of the shard where this block belongs.                                                                                 |
| `gen_utime`                     | uint32                                       | The generation time of the block.                                                                                                     |
| `start_lt`                      | uint64                                       | Start logical time associated with the block.                                                                                         |
| `end_lt`                        | uint64                                       | End logical time associated with the block.                                                                                           |
| `gen_validator_list_hash_short` | uint32                                       | Short hash related to the list of validators at the moment of generation of this block.                                               |
| `gen_catchain_seqno`            | uint32                                       | [Catchain](/catchain.pdf) sequence number related to this block.                                                                      |
| `min_ref_mc_seqno`              | uint32                                       | Minimum sequence number of referenced masterchain block.                                                                              |
| `prev_key_block_seqno`          | uint32                                       | Sequence number of the previous key block.                                                                                            |
| `gen_software`                  | GlobalVersion                                | The version of the software that generated the block. Only presented if the first bit of the `version` is set to `1`. |
| `master_ref`                    | BlkMasterInfo                                | A reference to the master block if the block is not a master. Stored in a reference. block.           |
| `prev_ref`                      | BlkPrevInfo after_merge | A reference to the previous block. Stored in a reference.                                                             |
| `prev_vert_ref`                 | BlkPrevInfo 0                                | A reference to the previous block in the vertical sequence if it exists. Stored in a reference.                       |

### value_flow:^ValueFlow

This field represents the flow of currency within the block, including fees collected and other transactions involving currency.

```tlb
value_flow#b8e48dfb ^[ from_prev_blk:CurrencyCollection
    to_next_blk:CurrencyCollection
    imported:CurrencyCollection
    exported:CurrencyCollection ]
    fees_collected:CurrencyCollection
    ^[
    fees_imported:CurrencyCollection
    recovered:CurrencyCollection
    created:CurrencyCollection
    minted:CurrencyCollection
    ] = ValueFlow;
```

| Field            | Type                                                                   | Description                                                                                                      |
| ---------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `from_prev_blk`  | [CurrencyCollection](/develop/data-formats/msg-tlb#currencycollection) | Represents the flow of currencies from the previous block.                                       |
| `to_next_blk`    | [CurrencyCollection](/develop/data-formats/msg-tlb#currencycollection) | Represents the flow of currencies to the next block.                                             |
| `imported`       | [CurrencyCollection](/develop/data-formats/msg-tlb#currencycollection) | Represents the flow of currencies imported to the block.                                         |
| `exported`       | [CurrencyCollection](/develop/data-formats/msg-tlb#currencycollection) | Represents the flow of currencies exported from the block.                                       |
| `fees_collected` | [CurrencyCollection](/develop/data-formats/msg-tlb#currencycollection) | The total amount of fees collected in the block.                                                 |
| `fees_imported`  | [CurrencyCollection](/develop/data-formats/msg-tlb#currencycollection) | The amount of fees imported into the block. Non-zero only in masterchain.        |
| `recovered`      | [CurrencyCollection](/develop/data-formats/msg-tlb#currencycollection) | The amount of currencies recovered in the block. Non-zero only in masterchain.   |
| `created`        | [CurrencyCollection](/develop/data-formats/msg-tlb#currencycollection) | The amount of new currencies created in the block. Non-zero only in masterchain. |
| `minted`         | [CurrencyCollection](/develop/data-formats/msg-tlb#currencycollection) | The amount of currencies minted in the block. Non-zero only in masterchain.      |

## state_update:^(MERKLE_UPDATE ShardState)

This field represents the update of the shard state.

```tlb
!merkle_update#02 {X:Type} old_hash:bits256 new_hash:bits256
    old:^X new:^X = MERKLE_UPDATE X;
```

| Field      | Type                      | Description                                                                        |
| ---------- | ------------------------- | ---------------------------------------------------------------------------------- |
| `old_hash` | bits256                   | The old hash of the shard state.                                   |
| `new_hash` | bits256                   | The new hash of the shard state.                                   |
| `old`      | [ShardState](#shardstate) | The old state of the shard. Stored in a reference. |
| `new`      | [ShardState](#shardstate) | The new state of the shard. Stored in a reference. |

### ShardState

`ShardState` can contain either information about the shard, or, in case if this shard is splitted, information about left and right splitted parts.

```tlb
_ ShardStateUnsplit = ShardState;
split_state#5f327da5 left:^ShardStateUnsplit right:^ShardStateUnsplit = ShardState;
```

### ShardState Unsplitted

```tlb
shard_state#9023afe2 global_id:int32
    shard_id:ShardIdent
    seq_no:uint32 vert_seq_no:#
    gen_utime:uint32 gen_lt:uint64
    min_ref_mc_seqno:uint32
    out_msg_queue_info:^OutMsgQueueInfo
    before_split:(## 1)
    accounts:^ShardAccounts
    ^[ overload_history:uint64 underload_history:uint64
    total_balance:CurrencyCollection
    total_validator_fees:CurrencyCollection
    libraries:(HashmapE 256 LibDescr)
    master_ref:(Maybe BlkMasterInfo) ]
    custom:(Maybe ^McStateExtra)
    = ShardStateUnsplit;
```

| Field                  | Type                                                                   | Required | Description                                                                                                                                                                                                 |
| ---------------------- | ---------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `global_id`            | int32                                                                  | Yes      | An ID of the network where this shard belongs. `-239` for mainnet and `-3` for testnet.                                                                                     |
| `shard_id`             | ShardIdent                                                             | Yes      | The identifier of the shard.                                                                                                                                                                |
| `seq_no`               | uint32                                                                 | Yes      | The latest sequence number associated with this shardchain.                                                                                                                                 |
| `vert_seq_no`          | #                                                                      | Yes      | The latest vertical sequence number associated with this shardchain.                                                                                                                        |
| `gen_utime`            | uint32                                                                 | Yes      | The generation time associated with the creation of the shard.                                                                                                                              |
| `gen_lt`               | uint64                                                                 | Yes      | The logical time associated with the creation of the shard.                                                                                                                                 |
| `min_ref_mc_seqno`     | uint32                                                                 | Yes      | Sequence number of the latest referenced masterchain block.                                                                                                                                 |
| `out_msg_queue_info`   | OutMsgQueueInfo                                                        | Yes      | Information about the out message queue of this shard. Stored in a reference.                                                                                               |
| `before_split`         | ## 1                                                                   | Yes      | A flag indicating whether a split will in the next block of this shardchain.                                                                                                                |
| `accounts`             | ShardAccounts                                                          | Yes      | The state of accounts in the shard. Stored in a reference.                                                                                                                  |
| `overload_history`     | uint64                                                                 | Yes      | History of overload events for the shard. Used for load balancing through sharding.                                                                                         |
| `underload_history`    | uint64                                                                 | Yes      | History of underload events for the shard. Used for load balancing through sharding.                                                                                        |
| `total_balance`        | [CurrencyCollection](/develop/data-formats/msg-tlb#currencycollection) | Yes      | Total balance for the shard.                                                                                                                                                                |
| `total_validator_fees` | [CurrencyCollection](/develop/data-formats/msg-tlb#currencycollection) | Yes      | Total validator fees for the shard.                                                                                                                                                         |
| `libraries`            | HashmapE 256 LibDescr                                                  | Yes      | A hashmap of library descriptions in this shard. Currently, non-empty only in the masterchain.                                                                              |
| `master_ref`           | BlkMasterInfo                                                          | No       | A reference to the master block info.                                                                                                                                                       |
| `custom`               | McStateExtra                                                           | No       | Custom extra data for the shard state. This field is present only in the masterchain and contains all the masterchain-specific data. Stored in a reference. |

### ShardState Splitted

| Field   | Type                                        | Description                                                                                |
| ------- | ------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `left`  | [ShardStateUnsplit](#shardstate-unsplitted) | The state of the left split shard. Stored in a reference.  |
| `right` | [ShardStateUnsplit](#shardstate-unsplitted) | The state of the right split shard. Stored in a reference. |

## extra:^BlockExtra

This field contains extra information about the block.

```tlb
block_extra in_msg_descr:^InMsgDescr
    out_msg_descr:^OutMsgDescr
    account_blocks:^ShardAccountBlocks
    rand_seed:bits256
    created_by:bits256
    custom:(Maybe ^McBlockExtra) = BlockExtra;
```

| Field            | Type                          | Required | Description                                                                                                                                                                                           |
| ---------------- | ----------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `in_msg_descr`   | InMsgDescr                    | Yes      | Descriptor of the incoming messages in the block. Stored in a reference.                                                                                              |
| `out_msg_descr`  | OutMsgDescr                   | Yes      | Descriptor of the outgoing messages in the block. Stored in a reference.                                                                                              |
| `account_blocks` | ShardAccountBlocks            | Yes      | The collection of all transactions processed in the block along with all updates of the states of the accounts assigned to the shard. Stored in a reference.          |
| `rand_seed`      | bits256                       | Yes      | The random seed for the block.                                                                                                                                                        |
| `created_by`     | bits256                       | Yes      | The entity (usually a validator's public key) that created the block.                                                                                              |
| `custom`         | [McBlockExtra](#mcblockextra) | No       | This field is present only in the masterchain and contains all the masterchain-specific data. Custom extra data for the block. Stored in a reference. |

### McBlockExtra

This field contains extra information about the masterchain block.

```tlb
masterchain_block_extra#cca5
    key_block:(## 1)
    shard_hashes:ShardHashes
    shard_fees:ShardFees
    ^[ prev_blk_signatures:(HashmapE 16 CryptoSignaturePair)
    recover_create_msg:(Maybe ^InMsg)
    mint_msg:(Maybe ^InMsg) ]
    config:key_block?ConfigParams
    = McBlockExtra;
```

| Field                 | Type                            | Required | Description                                                                                                                           |
| --------------------- | ------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `key_block`           | ## 1                            | Yes      | Flag indicating whether the block is a key block.                                                                     |
| `shard_hashes`        | ShardHashes                     | Yes      | The hashes of the latest blocks of the corresponding shardchains.                                                     |
| `shard_fees`          | ShardFees                       | Yes      | The total fees collected from all shards in this block.                                                               |
| `prev_blk_signatures` | HashmapE 16 CryptoSignaturePair | Yes      | Previous block signatures.                                                                                            |
| `recover_create_msg`  | InMsg                           | No       | The message related to recovering extra-currencies, if any. Stored in a reference.                    |
| `mint_msg`            | InMsg                           | No       | The message related to minting extra-currencies, if any. Stored in a reference.                       |
| `config`              | ConfigParams                    | No       | The actual configuration parameters for this block. This field is present only if `key_block` is set. |

## See also

- Original description of [Block layout](https://docs.ton.org/tblkch.pdf#page=96\&zoom=100,148,172) from whitepaper
