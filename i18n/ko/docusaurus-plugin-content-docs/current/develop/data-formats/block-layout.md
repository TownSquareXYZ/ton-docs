# 블록 레이아웃

:::info
이 페이지의 이해도를 극대화하려면 [TL-B 언어](/개발/데이터-포맷/셀-boc)를 숙지하는 것이 좋습니다.
:::

블록체인의 블록은 새로운 거래의 기록으로, 완료되면 이 탈중앙화된 원장의 영구적이고 불변하는 부분으로 블록체인에 추가됩니다. 각 블록에는 거래 데이터, 시간, 이전 블록에 대한 참조 등의 정보가 포함되어 블록 체인을 형성합니다.

TON 블록체인의 블록은 시스템의 전반적인 복잡성으로 인해 다소 복잡한 구조를 가지고 있습니다. 이 페이지에서는 이러한 블록의 구조와 레이아웃에 대해 설명합니다.

## 블록

블록의 원시 TL-B 체계는 다음과 같습니다:

```tlb
block#11ef55aa global_id:int32
    info:^BlockInfo value_flow:^ValueFlow
    state_update:^(MERKLE_UPDATE ShardState)
    extra:^BlockExtra = Block;
```

각 분야를 자세히 살펴보겠습니다.

## global_id:int32

이 블록이 생성된 네트워크의 ID입니다. 메인넷의 경우 `-239`, 테스트넷의 경우 `-3`입니다.

## 정보:^BlockInfo

이 필드에는 버전, 시퀀스 번호, 식별자 및 기타 플래그와 같은 블록에 대한 정보가 포함되어 있습니다.

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

| 필드                              | 유형                                           | 설명                                                                                        |
| ------------------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------- |
| '버전'                            | uint32                                       | 블록 구조의 버전입니다.                                                             |
| `not_master`                    | (## 1)                    | 이 블록이 마스터체인 블록인지 여부를 나타내는 플래그입니다.                                         |
| `after_merge`                   | (## 1)                    | 이 블록이 두 개의 샤드체인이 병합된 직후에 생성되어 두 개의 부모 블록을 가지고 있는지를 나타내는 플래그입니다.           |
| `before_split`                  | (## 1)                    | 해당 블록이 샤드체인 분할 직전에 생성되었는지를 나타내는 플래그입니다.                                   |
| `after_split`                   | (## 1)                    | 해당 블록이 샤드체인 분할 직후에 생성되었는지를 나타내는 플래그입니다.                                   |
| `want_split`                    | Bool                                         | 샤드체인 분할을 원하는지 여부를 나타내는 플래그입니다.                                            |
| `want_merge`                    | Bool                                         | 샤드체인 병합을 원하는지 여부를 나타내는 플래그입니다.                                            |
| `키_블록`                          | Bool                                         | 이 블록이 키 블록인지 여부를 나타내는 플래그입니다.                                             |
| `VERT_SEQNO_INCR`               | (## 1)                    | 수직 시퀀스 번호의 증분.                                                            |
| '플래그'                           | (## 8)                    | 블록에 대한 추가 플래그.                                                            |
| `seq_no`                        | #                                            | 블록과 관련된 시퀀스 번호입니다.                                                        |
| `VERT_SEQ_NO`                   | #                                            | 블록과 관련된 세로 시퀀스 번호입니다.                                                     |
| `샤드`                            | 샤드아이덴트                                       | 이 블록이 속한 샤드의 식별자입니다.                                                      |
| `gen_utime`                     | uint32                                       | 블록의 생성 시간입니다.                                                             |
| `start_lt`                      | uint64                                       | 블록과 연결된 논리적 시간을 시작합니다.                                                    |
| `END_LT`                        | uint64                                       | 블록과 관련된 논리적 시간을 종료합니다.                                                    |
| `gen_validator_list_hash_short` | uint32                                       | 이 블록을 생성하는 시점의 유효성 검사기 목록과 관련된 짧은 해시입니다.                                  |
| `GEN_CATCHAIN_SEQNO`            | uint32                                       | 이 블록과 관련된 [캐치인](/catchain.pdf) 시퀀스 번호입니다.                                 |
| `min_ref_mc_seqno`              | uint32                                       | 참조된 마스터체인 블록의 최소 시퀀스 번호입니다.                                               |
| `PREV_KEY_BLOCK_SEQNO`          | uint32                                       | 이전 키 블록의 시퀀스 번호입니다.                                                       |
| `gen_software`                  | 글로벌 버전                                       | 블록을 생성한 소프트웨어의 버전입니다. 버전`의 첫 번째 비트가 `1\`로 설정된 경우에만 표시됩니다. |
| `master_ref`                    | BlkMasterInfo                                | 블록이 마스터가 아닌 경우 마스터 블록에 대한 참조입니다. 참조 블록에 저장됩니다.            |
| `prev_ref`                      | BlkPrevInfo after_merge | 이전 블록에 대한 참조입니다. 참조에 저장됩니다.                               |
| `prev_vert_ref`                 | BlkPrevInfo 0                                | 수직 시퀀스에서 이전 블록이 있는 경우 해당 블록에 대한 참조입니다. 참조에 저장됩니다.         |

### value_flow:^ValueFlow

이 필드는 징수된 수수료와 통화와 관련된 기타 거래를 포함하여 블록 내 통화의 흐름을 나타냅니다.

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

| 필드                                                        | 유형                                                                                                                                 | 설명                                                                     |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| FROM_PREV_BLK\` | [CurrencyCollection](/개발/데이터 형식/msg-tlb#currencycollection) | 이전 블록의 통화 흐름을 나타냅니다.                                   |
| TO_NEXT_BLK\`   | [CurrencyCollection](/개발/데이터 형식/msg-tlb#currencycollection) | 다음 블록으로의 통화 흐름을 나타냅니다.                                 |
| `수입된`                                                     | [CurrencyCollection](/개발/데이터 형식/msg-tlb#currencycollection) | 블록으로 가져온 통화의 흐름을 나타냅니다.                                |
| '내보내기'                                                    | [커런시 컬렉션](/개발/데이터-포맷/msg-tlb#currencycollection)                                                                                   | 블록에서 내보낸 통화의 흐름을 나타냅니다.                                |
| `수수료_수집된`                                                 | [커런시 컬렉션](/개발/데이터-포맷/msg-tlb#currencycollection)                                                                                   | 블록에서 징수된 수수료의 총액입니다.                                   |
| `수수료_수입`                                                  | [커런시 컬렉션](/개발/데이터-포맷/msg-tlb#currencycollection)                                                                                   | 블록으로 가져온 수수료의 양입니다. 마스터체인에서만 0이 아닙니다.  |
| '복구됨'                                                     | [커런시 컬렉션](/개발/데이터-포맷/msg-tlb#currencycollection)                                                                                   | 블록에서 회수된 화폐의 양입니다. 마스터체인에서만 0이 아닙니다.   |
| 생성된\`                                                     | [커런시 컬렉션](/개발/데이터-포맷/msg-tlb#currencycollection)                                                                                   | 블록에 새로 생성된 화폐의 양입니다. 마스터체인에서만 0이 아닙니다. |
| '발행된'                                                     | [커런시 컬렉션](/개발/데이터-포맷/msg-tlb#currencycollection)                                                                                   | 블록에서 발행된 화폐의 양입니다. 마스터체인에서만 0이 아닙니다.   |

## state_update:^(머클_업데이트 샤드스테이트)

이 필드는 샤드 상태의 업데이트를 나타냅니다.

```tlb
!merkle_update#02 {X:Type} old_hash:bits256 new_hash:bits256
    old:^X new:^X = MERKLE_UPDATE X;
```

| 필드         | 유형                 | 설명                                                       |
| ---------- | ------------------ | -------------------------------------------------------- |
| `OLD_HASH` | bits256            | 샤드 상태의 이전 해시입니다.                         |
| `new_hash` | bits256            | 샤드 상태의 새 해시입니다.                          |
| `old`      | [#샤드스테이트](#샤드스테이트) | 샤드의 이전 상태입니다. 참조에 저장됩니다. |
| `새로운`      | [#샤드스테이트](#샤드스테이트) | 샤드의 새 상태입니다. 참조에 저장됩니다.  |

### 샤드 상태

샤드 상태\`에는 샤드에 대한 정보 또는 이 샤드가 분할된 경우 왼쪽과 오른쪽으로 분할된 부분에 대한 정보가 포함될 수 있습니다.

```tlb
_ ShardStateUnsplit = ShardState;
split_state#5f327da5 left:^ShardStateUnsplit right:^ShardStateUnsplit = ShardState;
```

### 샤드 상태 분할되지 않음

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

| 필드                   | 유형                                                                                                                                 | 필수  | 설명                                                                                                                             |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | --- | ------------------------------------------------------------------------------------------------------------------------------ |
| `글로벌_ID`             | int32                                                                                                                              | 예   | 이 샤드가 속한 네트워크의 ID입니다. 메인넷의 경우 `-239`, 테스트넷의 경우 `-3`입니다.                                        |
| `shard_id`           | 샤드아이덴트                                                                                                                             | 예   | 샤드의 식별자입니다.                                                                                                    |
| `seq_no`             | uint32                                                                                                                             | 예   | 이 샤드체인과 관련된 최신 시퀀스 번호입니다.                                                                                      |
| `VERT_SEQ_NO`        | #                                                                                                                                  | 예   | 이 샤드체인과 관련된 최신 수직 시퀀스 번호입니다.                                                                                   |
| `gen_utime`          | uint32                                                                                                                             | 예   | 샤드 생성과 관련된 생성 시간입니다.                                                                                           |
| `gen_lt`             | uint64                                                                                                                             | 예   | 샤드 생성과 관련된 논리적 시간입니다.                                                                                          |
| `min_ref_mc_seqno`   | uint32                                                                                                                             | 예   | 참조된 최신 마스터체인 블록의 시퀀스 번호입니다.                                                                                    |
| `OUT_MSG_QUEUE_INFO` | 아웃메시지 대기열 정보                                                                                                                       | 예   | 이 샤드의 아웃 메시지 큐에 대한 정보입니다. 참조에 저장됩니다.                                                           |
| `before_split`       | ## 1                                                                                                                               | 예   | 이 샤드체인의 다음 블록에서 분할할지 여부를 나타내는 플래그입니다.                                                                          |
| `계정`                 | 샤드 계정                                                                                                                              | 예   | 샤드에 있는 계정의 상태입니다. 참조에 저장됩니다.                                                                   |
| `오버로드_기록`            | uint64                                                                                                                             | 예   | 샤드에 대한 과부하 이벤트 기록. 샤딩을 통한 로드 밸런싱에 사용됩니다.                                                       |
| `언더로드_역사`            | uint64                                                                                                                             | 예   | 샤드에 대한 과부하 이벤트 기록. 샤딩을 통한 로드 밸런싱에 사용됩니다.                                                       |
| `총액_잔액`              | [CurrencyCollection](/개발/데이터 형식/msg-tlb#currencycollection) | 예   | 샤드의 총 잔액입니다.                                                                                                   |
| `총_검증자_수수료`          | [CurrencyCollection](/개발/데이터 형식/msg-tlb#currencycollection) | 예   | 샤드에 대한 총 유효성 검사기 수수료입니다.                                                                                       |
| `라이브러리`              | 해시맵E 256 LibDescr                                                                                                                  | 예   | 이 샤드에 있는 라이브러리 설명의 해시맵입니다. 현재 마스터체인에서만 비어 있지 않습니다.                                             |
| `master_ref`         | BlkMasterInfo                                                                                                                      | 아니요 | 마스터 블록 정보에 대한 참조입니다.                                                                                           |
| `custom`             | 맥스테이트 엑스트라                                                                                                                         | 아니요 | 샤드 상태에 대한 사용자 지정 추가 데이터. 이 필드는 마스터체인에만 존재하며 모든 마스터체인 관련 데이터를 포함합니다. 참조에 저장됩니다. |

### 샤드 상태 분할

| 필드      | 유형                          | 설명                                                            |
| ------- | --------------------------- | ------------------------------------------------------------- |
| '왼쪽'    | [#샤드스테이트언스플릿](#샤드스테이트-언스플릿) | 왼쪽 분할 샤드의 상태입니다. 레퍼런스에 저장됩니다. |
| `right` | [#샤드스테이트언스플릿](#샤드스테이트-언스플릿) | 오른쪽 분할 샤드의 상태입니다. 참조에 저장됩니다.  |

## 추가:^BlockExtra

이 필드에는 블록에 대한 추가 정보가 포함되어 있습니다.

```tlb
block_extra in_msg_descr:^InMsgDescr
    out_msg_descr:^OutMsgDescr
    account_blocks:^ShardAccountBlocks
    rand_seed:bits256
    created_by:bits256
    custom:(Maybe ^McBlockExtra) = BlockExtra;
```

| 필드                           | 유형                       | 필수  | 설명                                                                                                                          |
| ---------------------------- | ------------------------ | --- | --------------------------------------------------------------------------------------------------------------------------- |
| `IN_MSG_DESCR`               | InMsgDescr               | 예   | 블록에 들어오는 메시지에 대한 설명자입니다. 참조에 저장됩니다.                                                         |
| `OUT_MSG_DESCR`              | OutMsgDescr              | 예   | 블록에 있는 발신 메시지의 설명자입니다. 참조에 저장됩니다.                                                           |
| 계정_블록\` | 샤드 계정 블록                 | 예   | 샤드에 할당된 계정 상태의 모든 업데이트와 함께 블록에서 처리된 모든 트랜잭션의 모음입니다. 참조에 저장됩니다.                              |
| `rand_seed`                  | bits256                  | 예   | 블록의 무작위 시드입니다.                                                                                              |
| `created_by`                 | bits256                  | 예   | 블록을 생성한 엔티티(일반적으로 유효성 검사자의 공개 키)입니다.                                                     |
| `custom`                     | [맥블록엑스트라](#mcblockextra) | 아니요 | 이 필드는 마스터체인에만 존재하며 모든 마스터체인 관련 데이터를 포함합니다. 블록에 대한 사용자 지정 추가 데이터. 참조에 저장됩니다. |

### 맥블록엑스트라

이 필드에는 마스터체인 블록에 대한 추가 정보가 포함되어 있습니다.

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

| 필드                                                    | 유형               | 필수  | 설명                                                                                         |
| ----------------------------------------------------- | ---------------- | --- | ------------------------------------------------------------------------------------------ |
| `키_블록`                                                | ## 1             | 예   | 블록이 키 블록인지 여부를 나타내는 플래그입니다.                                                |
| `shard_해시`                                            | 샤드해시             | 예   | 해당 샤드체인의 최신 블록 해시입니다.                                                      |
| `shard_fees`                                          | 샤드 수수료           | 예   | 이 블록의 모든 샤드에서 징수된 총 수수료입니다.                                                |
| `prev_blk_signatures`                                 | 해시맵E 16 암호화 서명 쌍 | 예   | 이전 블록 서명.                                                                  |
| 복구_생성_메시지\` | InMsg            | 아니요 | 추가 통화 복구와 관련된 메시지(있는 경우)입니다. 참조에 저장됩니다. |
| `mint_msg`                                            | InMsg            | 아니요 | 추가 통화 발행과 관련된 메시지(있는 경우)입니다. 참조에 저장됩니다. |
| `config`                                              | 구성 매개변수          | 아니요 | 이 블록의 실제 구성 매개변수입니다. 이 필드는 `key_block`이 설정된 경우에만 표시됩니다.    |

## 참고 항목

- 백서의 [블록 레이아웃](https://docs.ton.org/tblkch.pdf#page=96\&zoom=100,148,172)에 대한 원본 설명
