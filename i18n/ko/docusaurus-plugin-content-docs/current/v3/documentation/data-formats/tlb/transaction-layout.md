# 트랜잭션 레이아웃

:::info
이 페이지를 더 잘 이해하기 위해서는 [TL-B 언어](/v3/documentation/data-formats/tlb/cell-boc)에 대한 이해가 권장됩니다.
:::

TON 블록체인은 계정, 메시지, 트랜잭션이라는 세 가지 핵심 부분을 사용하여 작동합니다. 이 페이지는 트랜잭션의 구조와 레이아웃을 설명합니다.

트랜잭션은 특정 계정과 관련된 인바운드 및 아웃바운드 메시지를 처리하는 작업으로, 계정의 상태를 변경하고 검증자에게 수수료를 생성할 수 있습니다.

## 트랜잭션

```tlb
transaction$0111 account_addr:bits256 lt:uint64
    prev_trans_hash:bits256 prev_trans_lt:uint64 now:uint32
    outmsg_cnt:uint15
    orig_status:AccountStatus end_status:AccountStatus
    ^[ in_msg:(Maybe ^(Message Any)) out_msgs:(HashmapE 15 ^(Message Any)) ]
    total_fees:CurrencyCollection state_update:^(HASH_UPDATE Account)
    description:^TransactionDescr = Transaction;
```

| 필드                | 타입                                                                                  | 필수  | 설명                                                                                                                                                                                                    |
| ----------------- | ----------------------------------------------------------------------------------- | --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `account_addr`    | bits256                                                                             | 예   | 트랜잭션이 실행된 주소의 해시 부분. [주소에 대해 자세히 보기](/v3/documentation/smart-contracts/addresses#address-of-smart-contract)                                                                           |
| `lt`              | uint64                                                                              | 예   | _논리적 시간_을 나타냅니다. [논리적 시간에 대해 자세히 보기](/v3/documentation/smart-contracts/message-management/messages-and-transactions#what-is-a-logical-time) |
| `prev_trans_hash` | bits256                                                                             | 예   | 이 계정의 이전 트랜잭션 해시                                                                                                                                                                                      |
| `prev_trans_lt`   | uint64                                                                              | 예   | 이 계정의 이전 트랜잭션의 `lt`                                                                                                                                                                                   |
| `now`             | uint32                                                                              | 예   | 이 트랜잭션을 실행할 때 설정된 `now` 값. 초 단위의 Unix 타임스탬프입니다                                                                                                                                        |
| `outmsg_cnt`      | uint15                                                                              | 예   | 이 트랜잭션을 실행하는 동안 생성된 발신 메시지의 수                                                                                                                                                                         |
| `orig_status`     | [AccountStatus](#accountstatus)                                                     | 예   | 트랜잭션이 실행되기 전 이 계정의 상태                                                                                                                                                                                 |
| `end_status`      | [AccountStatus](#accountstatus)                                                     | 예   | 트랜잭션 실행 후 이 계정의 상태                                                                                                                                                                                    |
| `in_msg`          | (Message Any)                                                    | 아니오 | 트랜잭션 실행을 트리거한 수신 메시지. 참조에 저장됨                                                                                                                                                         |
| `out_msgs`        | HashmapE 15 ^(Message Any)                                       | 예   | 이 트랜잭션을 실행하는 동안 생성된 발신 메시지 목록이 포함된 딕셔너리                                                                                                                                                               |
| `total_fees`      | [CurrencyCollection](/v3/documentation/data-formats/tlb/msg-tlb#currencycollection) | 예   | 이 트랜잭션을 실행하는 동안 수집된 총 수수료 금액. *톤코인* 값과 일부 [Extra-currencies](/v3/documentation/dapps/defi/coins#extra-currencies)로 구성됨                                                                |
| `state_update`    | [HASH_UPDATE](#hash_update) Account                            | 예   | `HASH_UPDATE` 구조. 참조에 저장됨                                                                                                                                                             |
| `description`     | [TransactionDescr](#transactiondescr-types)                                         | 예   | 트랜잭션 실행 프로세스에 대한 자세한 설명. 참조에 저장됨                                                                                                                                                      |

## AccountStatus

```tlb
acc_state_uninit$00 = AccountStatus;
acc_state_frozen$01 = AccountStatus;
acc_state_active$10 = AccountStatus;
acc_state_nonexist$11 = AccountStatus;
```

- `[00]`: 계정이 초기화되지 않음
- `[01]`: 계정이 동결됨
- `[10]`: 계정이 활성화됨
- `[11]`: 계정이 존재하지 않음

## HASH_UPDATE

```tlb
update_hashes#72 {X:Type} old_hash:bits256 new_hash:bits256
    = HASH_UPDATE X;
```

| 필드         | 타입      | 설명                  |
| ---------- | ------- | ------------------- |
| `old_hash` | bits256 | 트랜잭션 실행 전 계정 상태의 해시 |
| `new_hash` | bits256 | 트랜잭션 실행 후 계정 상태의 해시 |

## TransactionDescr 타입

- [일반](#ordinary)
- [저장소](#storage)
- [틱톡](#tick-tock)
- [분할 준비](#split-prepare)
- [분할 설치](#split-install)
- [병합 준비](#merge-prepare)
- [병합 설치](#merge-install)

## 일반

이것은 가장 일반적인 트랜잭션 유형이며 대부분의 개발자 요구를 충족시킵니다. 이 유형의 트랜잭션은 정확히 하나의 수신 메시지를 가지며 여러 발신 메시지를 생성할 수 있습니다.

```tlb
trans_ord$0000 credit_first:Bool
    storage_ph:(Maybe TrStoragePhase)
    credit_ph:(Maybe TrCreditPhase)
    compute_ph:TrComputePhase action:(Maybe ^TrActionPhase)
    aborted:Bool bounce:(Maybe TrBouncePhase)
    destroyed:Bool
    = TransactionDescr;
```

| 필드             | 타입             | 필수  | 설명                                                                                                                                      |
| -------------- | -------------- | --- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `credit_first` | Bool           | 예   | 수신 메시지의 `bounce` 플래그와 상관관계가 있는 플래그. `credit_first = !bounce`                                                            |
| `storage_ph`   | TrStoragePhase | 아니오 | 트랜잭션 실행의 저장소 단계에 대한 정보 포함. [자세히 보기](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                         |
| `credit_ph`    | TrCreditPhase  | 아니오 | 트랜잭션 실행의 크레딧 단계에 대한 정보 포함. [자세히 보기](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                         |
| `compute_ph`   | TrComputePhase | 예   | 트랜잭션 실행의 계산 단계에 대한 정보 포함. [자세히 보기](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                          |
| `action`       | TrActionPhase  | 아니오 | 트랜잭션 실행의 액션 단계에 대한 정보 포함. [자세히 보기](/v3/documentation/tvm/tvm-overview#transactions-and-phases). 참조에 저장됨 |
| `aborted`      | Bool           | 예   | 트랜잭션 실행이 중단되었는지 여부를 나타냄                                                                                                                 |
| `bounce`       | TrBouncePhase  | 아니오 | 트랜잭션 실행의 반송 단계에 대한 정보 포함. [자세히 보기](/v3/documentation/smart-contracts/message-management/non-bounceable-messages)        |
| `destroyed`    | Bool           | 예   | 실행 중에 계정이 파괴되었는지 여부를 나타냄                                                                                                                |

## 저장소

이 유형의 트랜잭션은 검증자가 자신의 재량으로 삽입할 수 있습니다. 어떤 인바운드 메시지도 처리하지 않고 어떤 코드도 호출하지 않습니다. 유일한 효과는 계정에서 저장소 지불금을 수집하여 저장소 통계와 잔액에 영향을 미치는 것입니다. 결과적으로 계정의 *톤코인* 잔액이 특정 금액 아래로 떨어지면 계정이 동결되고 코드와 데이터가 결합된 해시로 대체될 수 있습니다.

```tlb
trans_storage$0001 storage_ph:TrStoragePhase
    = TransactionDescr;
```

| 필드           | 타입             | 설명                                                                                                               |
| ------------ | -------------- | ---------------------------------------------------------------------------------------------------------------- |
| `storage_ph` | TrStoragePhase | 트랜잭션 실행의 저장소 단계에 대한 정보를 포함. [자세히 보기](/v3/documentation/tvm/tvm-overview#transactions-and-phases) |

## 틱톡

`Tick`과 `Tock` 트랜잭션은 각 블록에서 자동으로 호출되어야 하는 특수 시스템 스마트 계약을 위해 예약되어 있습니다. `Tick` 트랜잭션은 각 마스터체인 블록의 시작 시에 호출되고, `Tock` 트랜잭션은 끝에 호출됩니다.

```tlb
trans_tick_tock$001 is_tock:Bool storage_ph:TrStoragePhase
    compute_ph:TrComputePhase action:(Maybe ^TrActionPhase)
    aborted:Bool destroyed:Bool = TransactionDescr;
```

| 필드           | 타입             | 필수  | 설명                                                                                                                                      |
| ------------ | -------------- | --- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `is_tock`    | Bool           | 예   | 트랜잭션 유형을 나타내는 플래그. `Tick`과 `Tock` 트랜잭션을 구분하는 데 사용됨                                                                      |
| `storage_ph` | TrStoragePhase | 예   | 트랜잭션 실행의 저장소 단계에 대한 정보 포함. [자세히 보기](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                         |
| `compute_ph` | TrComputePhase | 예   | 트랜잭션 실행의 계산 단계에 대한 정보 포함. [자세히 보기](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                          |
| `action`     | TrActionPhase  | 아니오 | 트랜잭션 실행의 액션 단계에 대한 정보 포함. [자세히 보기](/v3/documentation/tvm/tvm-overview#transactions-and-phases). 참조에 저장됨 |
| `aborted`    | Bool           | 예   | 트랜잭션 실행이 중단되었는지 여부를 나타냄                                                                                                                 |
| `destroyed`  | Bool           | 예   | 실행 중에 계정이 파괴되었는지 여부를 나타냄                                                                                                                |

## 분할 준비

:::note
이 유형의 트랜잭션은 현재 사용되지 않습니다. 이 프로세스에 대한 정보는 제한적입니다.
:::

분할 트랜잭션은 높은 부하로 인해 분할이 필요한 대형 스마트 계약에서 시작됩니다. 계약은 이 트랜잭션 유형을 지원하고 부하를 균형있게 하기 위해 분할 프로세스를 관리해야 합니다.

분할 준비 트랜잭션은 스마트 계약을 분할해야 할 때 시작됩니다. 스마트 계약은 배포될 새로운 인스턴스의 상태를 생성해야 합니다.

```tlb
trans_split_prepare$0100 split_info:SplitMergeInfo
    storage_ph:(Maybe TrStoragePhase)
    compute_ph:TrComputePhase action:(Maybe ^TrActionPhase)
    aborted:Bool destroyed:Bool
    = TransactionDescr;
```

| 필드           | 타입             | 필수  | 설명                                                                                                                                      |
| ------------ | -------------- | --- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `split_info` | SplitMergeInfo | 예   | 분할 프로세스에 대한 정보                                                                                                                          |
| `storage_ph` | TrStoragePhase | 아니오 | 트랜잭션 실행의 저장소 단계에 대한 정보 포함. [자세히 보기](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                         |
| `compute_ph` | TrComputePhase | 예   | 트랜잭션 실행의 계산 단계에 대한 정보 포함. [자세히 보기](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                          |
| `action`     | TrActionPhase  | 아니오 | 트랜잭션 실행의 액션 단계에 대한 정보 포함. [자세히 보기](/v3/documentation/tvm/tvm-overview#transactions-and-phases). 참조에 저장됨 |
| `aborted`    | Bool           | 예   | 트랜잭션 실행이 중단되었는지 여부를 나타냄                                                                                                                 |
| `destroyed`  | Bool           | 예   | 실행 중에 계정이 파괴되었는지 여부를 나타냄                                                                                                                |

## 분할 설치

:::note
이 유형의 트랜잭션은 현재 사용되지 않습니다. 이 프로세스에 대한 정보는 제한적입니다.
:::

분할 설치 트랜잭션은 대형 스마트 계약의 새로운 인스턴스를 생성하는 데 사용됩니다. 새 스마트 계약의 상태는 [분할 준비](#split-prepare) 트랜잭션에 의해 생성됩니다.

```tlb
trans_split_install$0101 split_info:SplitMergeInfo
    prepare_transaction:^Transaction
    installed:Bool = TransactionDescr;
```

| 필드                    | 타입                          | 설명                                                                   |
| --------------------- | --------------------------- | -------------------------------------------------------------------- |
| `split_info`          | SplitMergeInfo              | 분할 프로세스에 대한 정보                                                       |
| `prepare_transaction` | [Transaction](#transaction) | 분할 작업을 위해 [준비된 트랜잭션](#split-prepare)에 대한 정보. 참조에 저장됨 |
| `installed`           | Bool                        | 트랜잭션이 설치되었는지 여부를 나타냄                                                 |

## 병합 준비

:::note
이 유형의 트랜잭션은 현재 사용되지 않습니다. 이 프로세스에 대한 정보는 제한적입니다.
:::

병합 트랜잭션은 높은 부하로 인해 분할된 후 재결합이 필요한 대형 스마트 계약에서 시작됩니다. 계약은 이 트랜잭션 유형을 지원하고 부하를 균형있게 하기 위해 병합 프로세스를 관리해야 합니다.

병합 준비 트랜잭션은 두 스마트 계약을 병합해야 할 때 시작됩니다. 스마트 계약은 병합을 용이하게 하기 위해 자신의 다른 인스턴스에 대한 메시지를 생성해야 합니다.

```tlb
trans_merge_prepare$0110 split_info:SplitMergeInfo
    storage_ph:TrStoragePhase aborted:Bool
    = TransactionDescr;
```

| 필드           | 타입             | 설명                                                                                                              |
| ------------ | -------------- | --------------------------------------------------------------------------------------------------------------- |
| `split_info` | SplitMergeInfo | 병합 프로세스에 대한 정보                                                                                                  |
| `storage_ph` | TrStoragePhase | 트랜잭션 실행의 저장소 단계에 대한 정보 포함. [자세히 보기](/v3/documentation/tvm/tvm-overview#transactions-and-phases) |
| `aborted`    | Bool           | 트랜잭션 실행이 중단되었는지 여부를 나타냄                                                                                         |

## 병합 설치

:::note
이 유형의 트랜잭션은 현재 사용되지 않습니다. 이 프로세스에 대한 정보는 제한적입니다.
:::

병합 설치 트랜잭션은 대형 스마트 계약의 인스턴스를 병합하는 데 사용됩니다. 병합을 용이하게 하는 특별한 메시지는 [병합 준비](#merge-prepare) 트랜잭션에 의해 생성됩니다.

```tlb
trans_merge_install$0111 split_info:SplitMergeInfo
    prepare_transaction:^Transaction
    storage_ph:(Maybe TrStoragePhase)
    credit_ph:(Maybe TrCreditPhase)
    compute_ph:TrComputePhase action:(Maybe ^TrActionPhase)
    aborted:Bool destroyed:Bool
    = TransactionDescr;
```

| 필드                    | 타입                          | 필수  | 설명                                                                                                                                      |
| --------------------- | --------------------------- | --- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `split_info`          | SplitMergeInfo              | 예   | 병합 프로세스에 대한 정보                                                                                                                          |
| `prepare_transaction` | [Transaction](#transaction) | 예   | 병합 작업을 위해 [준비된 트랜잭션](#merge-prepare)에 대한 정보. 참조에 저장됨                                                                    |
| `storage_ph`          | TrStoragePhase              | 아니오 | 트랜잭션 실행의 저장소 단계에 대한 정보 포함. [자세히 보기](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                         |
| `credit_ph`           | TrCreditPhase               | 아니오 | 트랜잭션 실행의 크레딧 단계에 대한 정보 포함. [자세히 보기](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                         |
| `compute_ph`          | TrComputePhase              | 예   | 트랜잭션 실행의 계산 단계에 대한 정보 포함. [자세히 보기](/v3/documentation/tvm/tvm-overview#transactions-and-phases)                          |
| `action`              | TrActionPhase               | 아니오 | 트랜잭션 실행의 액션 단계에 대한 정보 포함. [자세히 보기](/v3/documentation/tvm/tvm-overview#transactions-and-phases). 참조에 저장됨 |
| `aborted`             | Bool                        | 예   | 트랜잭션 실행이 중단되었는지 여부를 나타냄                                                                                                                 |
| `destroyed`           | Bool                        | 예   | 실행 중에 계정이 파괴되었는지 여부를 나타냄                                                                                                                |

## 참고

- 백서의 트랜잭션 레이아웃 원본 설명
