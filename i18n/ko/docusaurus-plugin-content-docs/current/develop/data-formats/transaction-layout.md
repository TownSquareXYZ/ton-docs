# 트랜잭션 레이아웃

:::info
이 페이지의 이해도를 극대화하려면 [TL-B 언어](/개발/데이터-포맷/셀-boc)를 숙지하는 것이 좋습니다.
:::

TON 블록체인은 계정, 메시지, 트랜잭션의 세 가지 주요 부분을 사용하여 작동합니다. 이 페이지에서는 트랜잭션의 구조와 레이아웃에 대해 설명합니다.

트랜잭션은 특정 계정과 관련된 인바운드 및 아웃바운드 메시지를 처리하여 계정 상태를 변경하고 유효성 검사자에게 수수료를 발생시킬 수 있는 작업입니다.

## 거래

```tlb
transaction$0111 account_addr:bits256 lt:uint64
    prev_trans_hash:bits256 prev_trans_lt:uint64 now:uint32
    outmsg_cnt:uint15
    orig_status:AccountStatus end_status:AccountStatus
    ^[ in_msg:(Maybe ^(Message Any)) out_msgs:(HashmapE 15 ^(Message Any)) ]
    total_fees:CurrencyCollection state_update:^(HASH_UPDATE Account)
    description:^TransactionDescr = Transaction;
```

| 필드                                                    | 유형                                                                                                                                 | 필수  | 설명                                                                                                                                                                                     |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | --- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 계정_주소\`                          | bits256                                                                                                                            | 예   | 트랜잭션이 실행된 주소의 해시 부분입니다. [주소에 대한 자세한 정보](https://docs.ton.org/learn/overviews/addresses#address-of-smart-contract)                                                      |
| `lt`                                                  | uint64                                                                                                                             | 예   | 논리적 시간_을 나타냅니다. [논리적 시간에 대해 자세히 알아보기](https://docs.ton.org/develop/smart-contracts/guidelines/message-delivery-guarantees#what-is-a-logical-time) |
| 이전_트랜스_해시\` | bits256                                                                                                                            | 예   | 이 계정에 대한 이전 거래의 해시입니다.                                                                                                                                                 |
| `prev_trans_lt`                                       | uint64                                                                                                                             | 예   | 이 계정에 대한 이전 거래의 'lt'입니다.                                                                                                                                               |
| `지금`                                                  | uint32                                                                                                                             | 예   | 이 트랜잭션을 실행할 때 설정된 `now` 값입니다. 초 단위의 유닉스 타임스탬프입니다.                                                                                                      |
| `outmsg_cnt`                                          | uint15                                                                                                                             | 예   | 이 트랜잭션을 실행하는 동안 생성된 발신 메시지 수입니다.                                                                                                                                       |
| `orig_status`                                         | [계정 상태](#accountstatus)                                                                                                            | 예   | 거래가 실행되기 전 이 계정의 상태입니다.                                                                                                                                                |
| `END_STATUS`                                          | [계정 상태](#accountstatus)                                                                                                            | 예   | 트랜잭션 실행 후 이 계정의 상태입니다.                                                                                                                                                 |
| `in_msg`                                              | (메시지 아무거나)                                                                                                      | 아니요 | 트랜잭션 실행을 트리거한 수신 메시지입니다. 참조에 저장됩니다.                                                                                                                    |
| `OUT_MSGS`                                            | 해시맵E 15 ^(메시지 임의)                                                                                               | 예   | 이 트랜잭션을 실행하는 동안 생성된 발신 메시지 목록이 포함된 딕셔너리입니다.                                                                                                                            |
| `총_수수료`                                               | [CurrencyCollection](/개발/데이터 형식/msg-tlb#currencycollection) | 예   | 이 거래를 실행하는 동안 징수된 수수료의 총액입니다. 톤코인_ 값과 일부 [추가 통화](https://docs.ton.org/develop/dapps/defi/coins#extra-currencies)로 구성됩니다.          |
| `state_update`                                        | [해시업데이트](#해시업데이트) 계정                                                                                                               | 예   | 해시업데이트\` 구조체. 참조에 저장됩니다.                                                                                                                               |
| `설명`                                                  | [트랜잭션 설명](#트랜잭션 설명 유형)                                      | 예   | 트랜잭션 실행 프로세스에 대한 자세한 설명입니다. 참조에 저장됩니다.                                                                                                                 |

## 계정 상태

```tlb
acc_state_uninit$00 = AccountStatus;
acc_state_frozen$01 = AccountStatus;
acc_state_active$10 = AccountStatus;
acc_state_nonexist$11 = AccountStatus;
```

- `[00]`: 계정이 초기화되지 않았습니다.
- `[01]`: 계정이 동결되었습니다.
- `[10]`: 계정이 활성 상태입니다.
- `[11]`: 계정이 존재하지 않습니다.

## 해시업데이트

```tlb
update_hashes#72 {X:Type} old_hash:bits256 new_hash:bits256
    = HASH_UPDATE X;
```

| 필드         | 유형      | 설명                                         |
| ---------- | ------- | ------------------------------------------ |
| `OLD_HASH` | bits256 | 트랜잭션을 실행하기 전 계정 상태의 해시입니다. |
| `new_hash` | bits256 | 트랜잭션 실행 후 계정 상태의 해시입니다.    |

## 트랜잭션 설명 유형

- [일반](#오디너리)
- [저장소](#저장소)
- [틱톡](#틱톡)
- [분할 준비](#스플릿-준비)
- [분할 설치](#분할 설치)
- [병합 준비](#병합 준비)
- [병합 설치](#병합 설치)

## 보통

가장 일반적인 트랜잭션 유형이며 대부분의 개발자의 요구를 충족합니다. 이 유형의 트랜잭션에는 정확히 하나의 수신 메시지가 있으며 여러 개의 발신 메시지를 생성할 수 있습니다.

```tlb
trans_ord$0000 credit_first:Bool
    storage_ph:(Maybe TrStoragePhase)
    credit_ph:(Maybe TrCreditPhase)
    compute_ph:TrComputePhase action:(Maybe ^TrActionPhase)
    aborted:Bool bounce:(Maybe TrBouncePhase)
    destroyed:Bool
    = TransactionDescr;
```

| 필드           | 유형             | 필수  | 설명                                                                                                                                                                                   |
| ------------ | -------------- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `크레딧_우선`     | Bool           | 예   | 수신 메시지의 `바운스` 플래그와 연관된 플래그입니다. credit_first = !bounce\`                                                                                         |
| `storage_ph` | TrStoragePhase | 아니요 | 트랜잭션 실행의 저장 단계에 대한 정보를 포함합니다. [자세한 정보](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                             |
| `credit_ph`  | TrCreditPhase  | 아니요 | 트랜잭션 실행의 신용 단계에 대한 정보를 포함합니다. [자세한 정보](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                             |
| `compute_ph` | TrComputePhase | 예   | 트랜잭션 실행의 계산 단계에 대한 정보를 포함합니다. [자세한 정보](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                             |
| `action`     | TrActionPhase  | 아니요 | 트랜잭션 실행의 액션 단계에 대한 정보를 포함합니다. [자세한 정보](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases). 참조에 저장됩니다. |
| '중단됨'        | Bool           | 예   | 트랜잭션 실행이 중단되었는지 여부를 나타냅니다.                                                                                                                                           |
| `바운스`        | TrBouncePhase  | 아니요 | 트랜잭션 실행의 바운스 단계에 대한 정보를 포함합니다. [자세한 정보](https://docs.ton.org/develop/smart-contracts/guidelines/non-bouncable-messages)                                              |
| `파괴된`        | Bool           | 예   | 실행 중에 계정이 삭제되었는지 여부를 나타냅니다.                                                                                                                                          |

## 스토리지

이 유형의 트랜잭션은 유효성 검사자가 재량에 따라 삽입할 수 있습니다. 인바운드 메시지를 처리하지 않으며 어떤 코드도 호출하지 않습니다. 이 트랜잭션의 유일한 효과는 계정에서 스토리지 대금을 수금하여 스토리지 통계와 잔액에 영향을 미치는 것입니다. 계정의 *Toncoin* 잔액이 특정 금액 이하로 떨어지면 계정이 동결되고 해당 코드와 데이터가 결합된 해시로 대체될 수 있습니다.

```tlb
trans_storage$0001 storage_ph:TrStoragePhase
    = TransactionDescr;
```

| 필드           | 유형             | 설명                                                                                                                                       |
| ------------ | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `storage_ph` | TrStoragePhase | 트랜잭션 실행의 저장 단계에 대한 정보를 포함합니다. [자세한 정보](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases) |

## 틱톡

틱`과 `톡` 트랜잭션은 각 블록에서 자동으로 호출되어야 하는 특수 시스템 스마트 컨트랙트를 위해 예약되어 있습니다. 틱` 트랜잭션은 각 마스터체인 블록의 시작에 호출되고, `톡` 트랜잭션은 마지막에 호출됩니다.

```tlb
trans_tick_tock$001 is_tock:Bool storage_ph:TrStoragePhase
    compute_ph:TrComputePhase action:(Maybe ^TrActionPhase)
    aborted:Bool destroyed:Bool = TransactionDescr;
```

| 필드           | 유형             | 필수  | 설명                                                                                                                                                                                   |
| ------------ | -------------- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `is_tock`    | Bool           | 예   | 트랜잭션 유형을 나타내는 플래그입니다. 틱`과 `톡\` 트랜잭션을 구분하는 데 사용됩니다.                                                                                                   |
| `storage_ph` | TrStoragePhase | 예   | 트랜잭션 실행의 저장 단계에 대한 정보를 포함합니다. [자세한 정보](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                             |
| `compute_ph` | TrComputePhase | 예   | 트랜잭션 실행의 계산 단계에 대한 정보를 포함합니다. [자세한 정보](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                             |
| `action`     | TrActionPhase  | 아니요 | 트랜잭션 실행의 액션 단계에 대한 정보를 포함합니다. [자세한 정보](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases). 참조에 저장됩니다. |
| '중단됨'        | Bool           | 예   | 트랜잭션 실행이 중단되었는지 여부를 나타냅니다.                                                                                                                                           |
| `파괴된`        | Bool           | 예   | 실행 중에 계정이 삭제되었는지 여부를 나타냅니다.                                                                                                                                          |

## 분할 준비

:::note
이 유형의 거래는 현재 사용되지 않습니다. 이 프로세스에 대한 정보는 제한되어 있습니다.
:::

트랜잭션 분할은 부하가 높은 상황에서 분할해야 하는 대규모 스마트 컨트랙트에서 시작됩니다. 컨트랙트는 이 트랜잭션 유형을 지원하고 부하 균형을 맞추기 위해 분할 프로세스를 관리해야 합니다.

스마트 컨트랙트를 분할해야 할 때 분할 준비 트랜잭션이 시작됩니다. 스마트 컨트랙트는 배포할 새 인스턴스의 상태를 생성해야 합니다.

```tlb
trans_split_prepare$0100 split_info:SplitMergeInfo
    storage_ph:(Maybe TrStoragePhase)
    compute_ph:TrComputePhase action:(Maybe ^TrActionPhase)
    aborted:Bool destroyed:Bool
    = TransactionDescr;
```

| 필드           | 유형             | 필수  | 설명                                                                                                                                                                                   |
| ------------ | -------------- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `스플릿_정보`     | SplitMergeInfo | 예   | 분할 프로세스에 대한 정보입니다.                                                                                                                                                   |
| `storage_ph` | TrStoragePhase | 아니요 | 트랜잭션 실행의 저장 단계에 대한 정보를 포함합니다. [자세한 정보](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                             |
| `compute_ph` | TrComputePhase | 예   | 트랜잭션 실행의 계산 단계에 대한 정보를 포함합니다. [자세한 정보](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                             |
| `action`     | TrActionPhase  | 아니요 | 트랜잭션 실행의 액션 단계에 대한 정보를 포함합니다. [자세한 정보](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases). 참조에 저장됩니다. |
| '중단됨'        | Bool           | 예   | 트랜잭션 실행이 중단되었는지 여부를 나타냅니다.                                                                                                                                           |
| `파괴된`        | Bool           | 예   | 실행 중에 계정이 삭제되었는지 여부를 나타냅니다.                                                                                                                                          |

## 분할 설치

:::note
이 유형의 거래는 현재 사용되지 않습니다. 이 프로세스에 대한 정보는 제한되어 있습니다.
:::

분할 설치 트랜잭션은 대규모 스마트 컨트랙트의 새 인스턴스를 생성하는 데 사용됩니다. 새 스마트 컨트랙트의 상태는 [분할 준비](#split-prepare) 트랜잭션에 의해 생성됩니다.

```tlb
trans_split_install$0101 split_info:SplitMergeInfo
    prepare_transaction:^Transaction
    installed:Bool = TransactionDescr;
```

| 필드                    | 유형             | 설명                                                                                         |
| --------------------- | -------------- | ------------------------------------------------------------------------------------------ |
| `스플릿_정보`              | SplitMergeInfo | 분할 프로세스에 대한 정보입니다.                                                         |
| `prepare_transaction` | [트랜잭션](#트랜잭션)  | 분할 작업을 위해 준비된 [트랜잭션](#split-prepare)에 대한 정보입니다. 참조에 저장됩니다. |
| `설치됨`                 | Bool           | 트랜잭션이 설치되었는지 여부를 나타냅니다.                                                    |

## 병합 준비

:::note
이 유형의 거래는 현재 사용되지 않습니다. 이 프로세스에 대한 정보는 제한되어 있습니다.
:::

병합 트랜잭션은 높은 부하로 인해 분할된 후 재결합해야 하는 대규모 스마트 콘트랙트에서 시작됩니다. 컨트랙트는 이 트랜잭션 유형을 지원하고 부하를 분산하기 위해 병합 프로세스를 관리해야 합니다.

병합 준비 트랜잭션은 두 스마트 컨트랙트를 병합해야 할 때 시작됩니다. 스마트 컨트랙트는 병합을 용이하게 하기 위해 자신의 다른 인스턴스에 대한 메시지를 생성해야 합니다.

```tlb
trans_merge_prepare$0110 split_info:SplitMergeInfo
    storage_ph:TrStoragePhase aborted:Bool
    = TransactionDescr;
```

| 필드           | 유형             | 설명                                                                                                                                       |
| ------------ | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `스플릿_정보`     | SplitMergeInfo | 병합 프로세스에 대한 정보입니다.                                                                                                       |
| `storage_ph` | TrStoragePhase | 트랜잭션 실행의 저장 단계에 대한 정보를 포함합니다. [자세한 정보](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases) |
| '중단됨'        | Bool           | 트랜잭션 실행이 중단되었는지 여부를 나타냅니다.                                                                                               |

## 설치 병합

:::note
이 유형의 거래는 현재 사용되지 않습니다. 이 프로세스에 대한 정보는 제한되어 있습니다.
:::

병합 설치 트랜잭션은 대규모 스마트 컨트랙트의 인스턴스를 병합하는 데 사용됩니다. 병합을 촉진하는 특수 메시지는 [병합 준비](#merge-prepare) 트랜잭션에 의해 생성됩니다.

```tlb
trans_merge_install$0111 split_info:SplitMergeInfo
    prepare_transaction:^Transaction
    storage_ph:(Maybe TrStoragePhase)
    credit_ph:(Maybe TrCreditPhase)
    compute_ph:TrComputePhase action:(Maybe ^TrActionPhase)
    aborted:Bool destroyed:Bool
    = TransactionDescr;
```

| 필드                    | 유형             | 필수  | 설명                                                                                                                                                                                   |
| --------------------- | -------------- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `스플릿_정보`              | SplitMergeInfo | 예   | 병합 프로세스에 대한 정보입니다.                                                                                                                                                   |
| `prepare_transaction` | [트랜잭션](#트랜잭션)  | 예   | 병합 작업을 위한 [준비된 트랜잭션](#merge-prepare)에 대한 정보입니다. 참조에 저장됩니다.                                                                                           |
| `storage_ph`          | TrStoragePhase | 아니요 | 트랜잭션 실행의 저장 단계에 대한 정보를 포함합니다. [자세한 정보](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                             |
| `credit_ph`           | TrCreditPhase  | 아니요 | 트랜잭션 실행의 신용 단계에 대한 정보를 포함합니다. [자세한 정보](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                             |
| `compute_ph`          | TrComputePhase | 예   | 트랜잭션 실행의 계산 단계에 대한 정보를 포함합니다. [자세한 정보](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases)                                             |
| `action`              | TrActionPhase  | 아니요 | 트랜잭션 실행의 액션 단계에 대한 정보를 포함합니다. [자세한 정보](https://docs.ton.org/learn/tvm-instructions/tvm-overview#transactions-and-phases). 참조에 저장됩니다. |
| '중단됨'                 | Bool           | 예   | 트랜잭션 실행이 중단되었는지 여부를 나타냅니다.                                                                                                                                           |
| `파괴된`                 | Bool           | 예   | 실행 중에 계정이 삭제되었는지 여부를 나타냅니다.                                                                                                                                          |

## 참고 항목

- 백서의 [트랜잭션 레이아웃](https://ton.org/docs/tblkch.pdf#page=75\&zoom=100,148,290)에 대한 원본 설명
