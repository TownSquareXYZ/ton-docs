# 블록 레이아웃

:::info
이 페이지를 더 잘 이해하기 위해서는 [TL-B 언어](/v3/documentation/data-formats/tlb/cell-boc)에 대한 이해가 권장됩니다.
:::

블록체인의 블록은 완성되면 분산 원장의 영구적이고 불변한 부분으로 추가되는 새로운 트랜잭션의 기록입니다. 각 블록은 트랜잭션 데이터, 시간, 이전 블록에 대한 참조 등의 정보를 포함하여 블록 체인을 형성합니다.

TON 블록체인의 블록들은 시스템의 전반적인 복잡성으로 인해 꽤 복잡한 구조를 가지고 있습니다. 이 페이지는 이러한 블록들의 구조와 레이아웃을 설명합니다.

## 블록

블록의 Raw TL-B 스키마는 다음과 같습니다:

```tlb
block#11ef55aa global_id:int32
    info:^BlockInfo value_flow:^ValueFlow
    state_update:^(MERKLE_UPDATE ShardState)
    extra:^BlockExtra = Block;
```

각 필드를 자세히 살펴보겠습니다.

## global_id:int32

이 블록이 생성된 네트워크의 ID입니다. 메인넷의 경우 `-239`, 테스트넷의 경우 `-3`입니다.

## info:^BlockInfo

이 필드는 블록의 버전, 시퀀스 번호, 식별자 및 기타 플래그와 같은 블록에 대한 정보를 포함합니다.

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

| 필드                              | 타입                                           | 설명                                                                         |
| ------------------------------- | -------------------------------------------- | -------------------------------------------------------------------------- |
| `version`                       | uint32                                       | 블록 구조의 버전                                                                  |
| `not_master`                    | (## 1)                    | 이 블록이 마스터체인 블록인지 나타내는 플래그                                                  |
| `after_merge`                   | (## 1)                    | 이 블록이 두 샤드체인의 병합 직후 생성되었는지를 나타내는 플래그로, 두 개의 부모 블록을 가짐                      |
| `before_split`                  | (## 1)                    | 이 블록이 샤드체인 분할 직전에 생성되었는지를 나타내는 플래그                                         |
| `after_split`                   | (## 1)                    | 이 블록이 샤드체인 분할 직후에 생성되었는지를 나타내는 플래그                                         |
| `want_split`                    | Bool                                         | 샤드체인 분할이 필요한지를 나타내는 플래그                                                    |
| `want_merge`                    | Bool                                         | 샤드체인 병합이 필요한지를 나타내는 플래그                                                    |
| `key_block`                     | Bool                                         | 이 블록이 키 블록인지를 나타내는 플래그                                                     |
| `vert_seqno_incr`               | (## 1)                    | 수직 시퀀스 번호의 증가값                                                             |
| `flags`                         | (## 8)                    | 블록에 대한 추가 플래그                                                              |
| `seq_no`                        | #                                            | 블록과 관련된 시퀀스 번호                                                             |
| `vert_seq_no`                   | #                                            | 블록과 관련된 수직 시퀀스 번호                                                          |
| `shard`                         | ShardIdent                                   | 이 블록이 속한 샤드의 식별자                                                           |
| `gen_utime`                     | uint32                                       | 블록의 생성 시간                                                                  |
| `start_lt`                      | uint64                                       | 블록과 관련된 시작 논리 시간                                                           |
| `end_lt`                        | uint64                                       | 블록과 관련된 종료 논리 시간                                                           |
| `gen_validator_list_hash_short` | uint32                                       | 이 블록 생성 시점의 검증자 목록과 관련된 짧은 해시                                              |
| `gen_catchain_seqno`            | uint32                                       | 이 블록과 관련된 [Catchain](/catchain.pdf) 시퀀스 번호                                 |
| `min_ref_mc_seqno`              | uint32                                       | 참조된 마스터체인 블록의 최소 시퀀스 번호                                                    |
| `prev_key_block_seqno`          | uint32                                       | 이전 키 블록의 시퀀스 번호                                                            |
| `gen_software`                  | GlobalVersion                                | 블록을 생성한 소프트웨어의 버전. `version`의 첫 번째 비트가 `1`로 설정된 경우에만 표시    |
| `master_ref`                    | BlkMasterInfo                                | 블록이 마스터가 아닌 경우 마스터 블록에 대한 참조. 참조에 저장됨                      |
| `prev_ref`                      | BlkPrevInfo after_merge | 이전 블록에 대한 참조. 참조에 저장됨                                      |
| `prev_vert_ref`                 | BlkPrevInfo 0                                | 수직 시퀀스에서 이전 블록에 대한 참조(존재하는 경우). 참조에 저장됨 |

### value_flow:^ValueFlow

이 필드는 수집된 수수료와 통화가 관련된 기타 트랜잭션을 포함하여 블록 내의 통화 흐름을 나타냅니다.

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

| 필드               | 타입                                                                                  | 설명                                               |
| ---------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------ |
| `from_prev_blk`  | [CurrencyCollection](/v3/documentation/data-formats/tlb/msg-tlb#currencycollection) | 이전 블록에서의 통화 흐름을 나타냄                              |
| `to_next_blk`    | [CurrencyCollection](/v3/documentation/data-formats/tlb/msg-tlb#currencycollection) | 다음 블록으로의 통화 흐름을 나타냄                              |
| `imported`       | [CurrencyCollection](/v3/documentation/data-formats/tlb/msg-tlb#currencycollection) | 블록으로 가져온 통화의 흐름을 나타냄                             |
| `exported`       | [CurrencyCollection](/v3/documentation/data-formats/tlb/msg-tlb#currencycollection) | 블록에서 내보낸 통화의 흐름을 나타냄                             |
| `fees_collected` | [CurrencyCollection](/v3/documentation/data-formats/tlb/msg-tlb#currencycollection) | 블록에서 수집된 총 수수료                                   |
| `fees_imported`  | [CurrencyCollection](/v3/documentation/data-formats/tlb/msg-tlb#currencycollection) | 블록으로 가져온 수수료 양. 마스터체인에서만 0이 아님   |
| `recovered`      | [CurrencyCollection](/v3/documentation/data-formats/tlb/msg-tlb#currencycollection) | 블록에서 복구된 통화 양. 마스터체인에서만 0이 아님    |
| `created`        | [CurrencyCollection](/v3/documentation/data-formats/tlb/msg-tlb#currencycollection) | 블록에서 새로 생성된 통화 양. 마스터체인에서만 0이 아님 |
| `minted`         | [CurrencyCollection](/v3/documentation/data-formats/tlb/msg-tlb#currencycollection) | 블록에서 발행된 통화 양. 마스터체인에서만 0이 아님    |

## state_update:^(MERKLE_UPDATE ShardState)

이 필드는 샤드 상태의 업데이트를 나타냅니다.

```tlb
!merkle_update#02 {X:Type} old_hash:bits256 new_hash:bits256
    old:^X new:^X = MERKLE_UPDATE X;
```

| 필드         | 타입                        | 설명                                  |
| ---------- | ------------------------- | ----------------------------------- |
| `old_hash` | bits256                   | 샤드 상태의 이전 해시                        |
| `new_hash` | bits256                   | 샤드 상태의 새로운 해시                       |
| `old`      | [ShardState](#shardstate) | 샤드의 이전 상태. 참조에 저장됨  |
| `new`      | [ShardState](#shardstate) | 샤드의 새로운 상태. 참조에 저장됨 |

### ShardState

`ShardState`는 샤드에 대한 정보를 포함하거나, 이 샤드가 분할된 경우 왼쪽과 오른쪽으로 분할된 부분에 대한 정보를 포함할 수 있습니다.

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

| 필드                     | 타입                                                                                  | 필수  | 설명                                                                                                      |
| ---------------------- | ----------------------------------------------------------------------------------- | --- | ------------------------------------------------------------------------------------------------------- |
| `global_id`            | int32                                                                               | 예   | 이 샤드가 속한 네트워크의 ID. 메인넷은 `-239`, 테스트넷은 `-3`                                              |
| `shard_id`             | ShardIdent                                                                          | 예   | 샤드의 식별자                                                                                                 |
| `seq_no`               | uint32                                                                              | 예   | 이 샤드체인과 관련된 최신 시퀀스 번호                                                                                   |
| `vert_seq_no`          | #                                                                                   | 예   | 이 샤드체인과 관련된 최신 수직 시퀀스 번호                                                                                |
| `gen_utime`            | uint32                                                                              | 예   | 샤드 생성과 관련된 생성 시간                                                                                        |
| `gen_lt`               | uint64                                                                              | 예   | 샤드 생성과 관련된 논리 시간                                                                                        |
| `min_ref_mc_seqno`     | uint32                                                                              | 예   | 참조된 최신 마스터체인 블록의 시퀀스 번호                                                                                 |
| `out_msg_queue_info`   | OutMsgQueueInfo                                                                     | 예   | 이 샤드의 아웃 메시지 큐에 대한 정보. 참조에 저장됨                                                          |
| `before_split`         | ## 1                                                                                | 예   | 이 샤드체인의 다음 블록에서 분할이 발생할지를 나타내는 플래그                                                                      |
| `accounts`             | ShardAccounts                                                                       | 예   | 샤드의 계정 상태. 참조에 저장됨                                                                      |
| `overload_history`     | uint64                                                                              | 예   | 샤드의 과부하 이벤트 기록. 샤딩을 통한 로드 밸런싱에 사용됨                                                      |
| `underload_history`    | uint64                                                                              | 예   | 샤드의 저부하 이벤트 기록. 샤딩을 통한 로드 밸런싱에 사용됨                                                      |
| `total_balance`        | [CurrencyCollection](/v3/documentation/data-formats/tlb/msg-tlb#currencycollection) | 예   | 샤드의 총 잔액                                                                                                |
| `total_validator_fees` | [CurrencyCollection](/v3/documentation/data-formats/tlb/msg-tlb#currencycollection) | 예   | 샤드의 총 검증자 수수료                                                                                           |
| `libraries`            | HashmapE 256 LibDescr                                                               | 예   | 이 샤드의 라이브러리 설명 해시맵. 현재는 마스터체인에서만 비어있지 않음                                                |
| `custom`               | McStateExtra                                                                        | 아니오 | 샤드 상태에 대한 커스텀 추가 데이터. 이 필드는 마스터체인에서만 존재하며 모든 마스터체인 특화 데이터를 포함함. 참조에 저장됨 |
| `custom`               | McStateExtra                                                                        | 아니요 | 샤드 상태에 대한 커스텀 추가 데이터. 이 필드는 마스터체인에서만 존재하며 모든 마스터체인 특화 데이터를 포함함. 참조에 저장됨 |

### ShardState Splitted

| 필드      | 타입                                          | 설명                                        |
| ------- | ------------------------------------------- | ----------------------------------------- |
| `left`  | [ShardStateUnsplit](#shardstate-unsplitted) | 왼쪽으로 분할된 샤드의 상태. 참조에 저장됨  |
| `right` | [ShardStateUnsplit](#shardstate-unsplitted) | 오른쪽으로 분할된 샤드의 상태. 참조에 저장됨 |

## extra:^BlockExtra

이 필드는 블록에 대한 추가 정보를 포함합니다.

```tlb
block_extra in_msg_descr:^InMsgDescr
    out_msg_descr:^OutMsgDescr
    account_blocks:^ShardAccountBlocks
    rand_seed:bits256
    created_by:bits256
    custom:(Maybe ^McBlockExtra) = BlockExtra;
```

| 필드               | 타입                            | 필수  | 설명                                                                                                   |
| ---------------- | ----------------------------- | --- | ---------------------------------------------------------------------------------------------------- |
| `in_msg_descr`   | InMsgDescr                    | 예   | 블록의 인커밍 메시지 설명자. 참조에 저장됨                                                             |
| `out_msg_descr`  | OutMsgDescr                   | 예   | 블록의 아웃고잉 메시지 설명자. 참조에 저장됨                                                            |
| `account_blocks` | ShardAccountBlocks            | 예   | 블록에서 처리된 모든 트랜잭션과 샤드에 할당된 계정 상태의 모든 업데이트 컬렉션. 참조에 저장됨                                |
| `rand_seed`      | bits256                       | 예   | 블록의 랜덤 시드                                                                                            |
| `created_by`     | bits256                       | 예   | 블록을 생성한 엔티티(일반적으로 검증자의 공개 키)                                                      |
| `custom`         | [McBlockExtra](#mcblockextra) | 아니오 | 이 필드는 마스터체인에서만 존재하며 모든 마스터체인 특화 데이터를 포함함. 블록에 대한 커스텀 추가 데이터. 참조에 저장됨 |

### McBlockExtra

이 필드는 마스터체인 블록에 대한 추가 정보를 포함합니다.

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

| 필드                    | 타입                              | 필수  | 설명                                                                   |
| --------------------- | ------------------------------- | --- | -------------------------------------------------------------------- |
| `key_block`           | ## 1                            | 예   | 블록이 키 블록인지를 나타내는 플래그                                                 |
| `shard_hashes`        | ShardHashes                     | 예   | 해당 샤드체인의 최신 블록들의 해시                                                  |
| `shard_fees`          | ShardFees                       | 예   | 이 블록에서 모든 샤드로부터 수집된 총 수수료                                            |
| `prev_blk_signatures` | HashmapE 16 CryptoSignaturePair | 예   | 이전 블록 서명들                                                            |
| `recover_create_msg`  | InMsg                           | 아니오 | 추가 통화 복구와 관련된 메시지(있는 경우). 참조에 저장됨 |
| `mint_msg`            | InMsg                           | 아니오 | 추가 통화 발행과 관련된 메시지(있는 경우). 참조에 저장됨 |
| `config`              | ConfigParams                    | 아니오 | 이 블록에 대한 실제 구성 파라미터. 이 필드는 `key_block`이 설정된 경우에만 존재함 |

## 참고 자료

- 백서의 [Block layout](https://docs.ton.org/tblkch.pdf#page=96\&zoom=100,148,172) 원본 설명
