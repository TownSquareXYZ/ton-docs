# 설정 매개변수

:::info
[tonviewer](https://tonviewer.com/config)를 통해 실시간 값을 읽어보세요
:::

## 👋 소개

이 페이지에서는 TON 블록체인에서 사용되는 설정 매개변수에 대한 설명을 찾을 수 있습니다.
TON은 많은 기술적 매개변수가 있는 복잡한 설정을 가지고 있습니다: 일부는 블록체인 자체에서 사용되고, 일부는 생태계에서 사용됩니다. 하지만 이러한 매개변수의 의미를 이해하는 사람은 많지 않습니다. 이 글은 사용자에게 매개변수와 그 목적을 쉽게 이해할 수 있는 방법을 제공하기 위해 필요합니다.

## 💡 전제조건

이 자료는 매개변수 목록과 함께 읽어야 합니다.
[현재 설정](https://explorer.toncoin.org/config)에서 매개변수 값을 볼 수 있으며, [cells](/v3/concepts/dive-into-ton/ton-blockchain/cells-as-data-storage)에 쓰이는 방식은 [TL-B](/v3/documentation/data-formats/tlb/tl-b-language) 형식의 [block.tlb](https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb) 파일에 설명되어 있습니다.

:::info
TON 블록체인 매개변수 끝의 이진 인코딩은 설정의 직렬화된 이진 표현으로, 설정의 효율적인 저장이나 전송을 가능하게 합니다. 직렬화의 정확한 세부사항은 TON 블록체인이 사용하는 특정 인코딩 체계에 따라 다릅니다.
:::

## 🚀 시작하겠습니다!

모든 매개변수는 순서대로 되어 있어 헷갈리지 않을 것입니다. 빠른 탐색을 위해 오른쪽 사이드바를 사용하세요.

## Param 0

이 매개변수는 블록체인의 설정을 저장하는 특별한 스마트 컨트랙트의 주소입니다. 설정은 검증자 투표 중 로딩과 수정을 단순화하기 위해 컨트랙트에 저장됩니다.

:::info
설정 매개변수에는 주소의 해시 부분만 기록되는데, 이는 컨트랙트가 항상 [마스터체인](/v3/concepts/dive-into-ton/ton-blockchain/blockchain-of-blockchains#masterchain-blockchain-of-blockchains)(워크체인 -1)에 있기 때문입니다. 따라서 컨트랙트의 전체 주소는 `-1:<설정 매개변수의 값>`으로 작성됩니다.
:::

## Param 1

이 매개변수는 검증자 임명, 보상 분배, 블록체인 매개변수 변경에 대한 투표를 담당하는 [선거인](/v3/documentation/smart-contracts/contracts-specs/governance#elector) 스마트 컨트랙트의 주소입니다.

## Param 2

이 매개변수는 새로운 TON을 발행하고 블록체인 검증에 대한 보상으로 보내는 시스템의 주소를 나타냅니다.

:::info
매개변수 2가 없으면 매개변수 0이 대신 사용됩니다(새로 발행된 TON은 설정 스마트 컨트랙트에서 나옴).
:::

## Param 3

이 매개변수는 트랜잭션 수수료 수집기의 주소입니다.

:::info
매개변수 3이 없는 경우(현재 상황), 트랜잭션 수수료는 선거인 스마트 컨트랙트(매개변수 1)로 보내집니다.
:::

## Param 4

이 매개변수는 TON 네트워크의 루트 DNS 컨트랙트의 주소입니다.

:::info
자세한 정보는 [TON DNS & 도메인](/v3/guidelines/web3/ton-dns/dns) 문서와 더 자세한 원본 설명인 [여기](https://github.com/ton-blockchain/TEPs/blob/master/text/0081-dns-standard.md)에서 찾을 수 있습니다.
이 컨트랙트는 .ton 도메인 판매를 담당하지 않습니다.
:::

## Param 6

이 매개변수는 새로운 화폐 발행 수수료를 담당합니다.

:::info
Currently, minting additional currency is not implemented and does not work. The implementation and launch of the minter are planned.

문제와 전망에 대해 [관련 문서](/v3/documentation/infra/minter-flow)에서 자세히 알아볼 수 있습니다.
:::

## Param 7

이 매개변수는 유통 중인 각 추가 화폐의 양을 저장합니다. 데이터는 [딕셔너리](/v3/documentation/data-formats/tlb/tl-b-types#hashmap-parsing-example)(이진 트리; TON 개발 중에 이 구조가 실수로 hashmap으로 명명된 것 같음) `extracurrency_id -> amount` 형태로 저장되며, 금액은 `VarUint 32` - `0`에서 `2^248` 사이의 정수로 표시됩니다.

## Param 8

이 매개변수는 네트워크 버전과 검증자가 지원하는 추가 기능을 나타냅니다.

:::info
검증자는 새 블록을 생성하고 트랜잭션을 확인하는 책임이 있는 블록체인 네트워크의 노드입니다.
:::

- `version`: 이 필드는 버전을 지정합니다.

- `capabilities`: 이 필드는 특정 기능이나 성능의 존재 또는 부재를 나타내는 데 사용되는 플래그 세트입니다.

따라서 네트워크를 업데이트할 때 검증자들은 매개변수 8을 변경하는 데 투표할 것입니다. 이런 방식으로 TON 네트워크는 다운타임 없이 업데이트될 수 있습니다.

## Param 9

이 매개변수는 필수 매개변수 목록(이진 트리)을 포함합니다. 매개변수 9가 변경될 때까지 설정 변경 제안으로 제거할 수 없는 특정 설정 매개변수가 항상 존재하도록 보장합니다.

## Param 10

이 매개변수는 변경이 네트워크에 크게 영향을 미치는 중요한 TON 매개변수 목록(이진 트리)을 나타내므로 더 많은 투표 라운드가 열립니다.

## Param 11

이 매개변수는 TON 설정 변경 제안이 어떤 조건에서 수락되는지를 나타냅니다.

- `min_tot_rounds` - 제안을 적용할 수 있는 최소 라운드 수
- `max_tot_rounds` - 도달하면 제안이 자동으로 거부되는 최대 라운드 수
- `min_wins` - 필요한 승리 수(검증자의 3/4이 담보금 합계로 찬성 투표해야 함)
- `max_losses` - 도달하면 제안이 자동으로 거부되는 최대 패배 수
- `min_store_sec`와 `max_store_sec`는 제안이 저장될 수 있는 가능한 시간 간격을 결정
- `bit_price`와 `cell_price`는 제안의 1비트나 1셀을 저장하는 비용을 나타냄

## Param 12

이 매개변수는 TON 블록체인의 워크체인 설정을 나타냅니다. TON 블록체인의 워크체인은 병렬로 작동할 수 있는 독립적인 블록체인으로 설계되어 TON이 매우 많은 트랜잭션과 스마트 컨트랙트를 처리할 수 있게 합니다.

## 워크체인 설정 매개변수

- `enabled_since`: 이 워크체인이 활성화된 순간의 UNIX 타임스탬프

- `actual_min_split`: 검증자가 지원하는 이 워크체인의 최소 분할(샤딩) 깊이

- `min_split`: 설정에 의해 설정된 이 워크체인의 최소 분할 깊이

- `max_split`: 이 워크체인의 최대 분할 깊이

- `basic`: 이 워크체인이 기본(TON 코인 처리, TON 가상 머신 기반 스마트 컨트랙트)인지 나타내는 부울 플래그(true는 1, false는 0)

- `active`: 이 워크체인이 현재 활성 상태인지 나타내는 부울 플래그

- `accept_msgs`: 이 워크체인이 현재 메시지를 수락하고 있는지 나타내는 부울 플래그

- `flags`: 워크체인의 추가 플래그(예약됨, 현재 항상 0)

- `zerostate_root_hash`와 `zerostate_file_hash`: 워크체인의 첫 번째 블록 해시

- `version`: 워크체인의 버전

- `format`: vm_version과 vm_mode를 포함하는 워크체인의 형식 - 거기서 사용되는 가상 머신

## Param 13

이 매개변수는 [선거인](/v3/documentation/smart-contracts/contracts-specs/governance#elector) 컨트랙트에서 검증자의 잘못된 작동에 대한 불만을 제기하는 비용을 정의합니다.

## Param 14

이 매개변수는 TON 블록체인에서 블록 생성에 대한 보상을 나타냅니다. 나노그램은 nanoTON이므로, 마스터체인의 블록 생성 보상은 1.7 TON이고, 기본 워크체인에서는 1.0 TON입니다(한편, 워크체인이 분할되는 경우 블록 보상도 분할됩니다: 워크체인에 두 개의 샤드체인이 있으면 샤드 블록 보상은 0.5 TON이 됩니다).

## Param 15

이 매개변수는 TON 블록체인에서 선거와 검증자 작업의 다른 단계의 기간을 포함합니다.

각 검증 기간에는 검증 시작 시 UNIX 형식 시간과 동일한 `election_id`가 있습니다.
선거인 컨트랙트의 각각의 get-methods `active_election_id`와 `past_election_ids`를 호출하여 현재 `election_id`(선거가 진행 중인 경우) 또는 이전 id를 얻을 수 있습니다.

## 워크체인 설정 매개변수

- `validators_elected_for`: 선출된 검증자 세트가 역할을 수행하는 초 단위 시간(한 라운드)

- `elections_start_before`: 현재 라운드 종료 몇 초 전에 다음 기간의 선거 과정이 시작될지

- `elections_end_before`: 현재 라운드 종료 몇 초 전에 다음 라운드의 검증자가 선택될지

- `stake_held_for`: 라운드가 만료된 후 불만 처리를 위해 검증자의 스테이크가 보류되는 기간

:::info
인수의 각 값은 `uint32` 데이터 유형으로 결정됩니다.
:::

### 예시

TON 블록체인에서는 검증 기간을 짝수와 홀수로 관례적으로 나누는 것이 일반적입니다. 이러한 라운드는 서로 이어집니다. 다음 라운드에 대한 투표가 이전 라운드 중에 이루어지므로, 검증자는 두 라운드 모두에 참여할 기회를 가지기 위해 자금을 두 풀로 나눠야 합니다.

#### 메인넷

현재 값:

```python
constants = {
    'validators_elected_for': 65536,  # 18.2 hours
    'elections_start_before': 32768,  # 9.1 hours
    'elections_end_before': 8192,     # 2.2 hours
    'stake_held_for': 32768           # 9.1 hours
}
```

스키마:

![image](/img/docs/blockchain-configs/config15-mainnet.png)

#### 기간은 어떻게 계산하나요?

`election_id = validation_start = 1600032768`이라고 가정해 보겠습니다. 그러면:

```python
election_start = election_id - constants['elections_start_before'] = 1600032768 - 32768 = 1600000000
election_end = delay_start = election_id - constants['elections_end_before'] = 1600032768 - 8192 = 1600024576
hold_start = validation_end = election_id + constants['validators_elected_for'] = 1600032768 + 65536 = 1600098304
hold_end = hold_start + constants['stake_held_for'] = 1600098304 + 32768 = 1600131072
```

따라서 현재 한 패리티의 한 라운드 길이는 `1600131072 - 1600000000 = 131072초 = 36.40888... 시간`입니다.

#### 테스트넷

##### 현재 값:

```python
constants = {
    'validators_elected_for': 7200,  # 2 hours
    'elections_start_before': 2400,  # 40 minutes
    'elections_end_before': 180,     # 3 minutes
    'stake_held_for': 900            # 15 minutes
}
```

##### 스키마

![image](/img/docs/blockchain-configs/config15-testnet.png)

###### 기간은 어떻게 계산하나요?

`election_id = validation_start = 160002400`이라고 가정해 보겠습니다. 그러면:

```python
election_start = election_id - constants['elections_start_before'] = 160002400 - 2400 = 1600000000
election_end = delay_start = election_id - constants['elections_end_before'] = 160002400 - 180 = 160002220
hold_start = validation_end = election_id + constants['validators_elected_for'] = 160002400 + 7200 = 160009600
hold_end = hold_start + constants['stake_held_for'] = 160009600 + 900 = 160010500
```

따라서 현재 한 패리티의 한 라운드 길이는 `160010500 - 1600000000 = 10500초 = 175분 = 2.91666... 시간`입니다.

## Param 16

이 매개변수는 TON 블록체인의 검증자 수에 대한 제한을 나타냅니다. 선거인 스마트 컨트랙트에서 직접 사용됩니다.

### 선거를 위한 검증자 수 설정 매개변수:

- `max_validators`: 네트워크 운영에 참여할 수 있는 최대 검증자 수를 나타냅니다.

- `max_main_validators`: 마스터체인 검증자의 최대 수를 나타냅니다.

- `min_validators`: 네트워크 운영을 지원해야 하는 최소 검증자 수를 나타냅니다.

1. 최대 검증자 수는 마스터체인 검증자의 최대 수보다 크거나 같아야 합니다.
2. 마스터체인 검증자의 최대 수는 최소 검증자 수보다 크거나 같아야 합니다.
3. 최소 검증자 수는 1 이상이어야 합니다.

## Param 17

이 매개변수는 TON 블록체인의 스테이크 매개변수 설정을 나타냅니다. 지분증명이나 위임된 지분증명 합의 알고리즘을 사용하는 많은 블록체인 시스템에서, 네트워크 고유의 암호화폐 소유자는 검증자가 되어 보상을 얻기 위해 토큰을 "스테이크"할 수 있습니다.

## 설정 매개변수:

- `min_stake`: 검증 과정에 참여하기 위해 관심 있는 당사자가 스테이크해야 하는 최소 TON 양을 나타냅니다.

- `max_stake`: 관심 있는 당사자가 스테이크할 수 있는 최대 TON 양을 나타냅니다.

- `min_total_stake`: 선택된 검증자 세트가 보유해야 하는 최소 총 TON 양을 나타냅니다.

- `max_stake_factor`: 최대 유효 스테이크(담보)가 다른 검증자가 보낸 최소 스테이크를 초과할 수 있는 배수를 나타내는 승수입니다.

:::info
인수의 각 값은 `uint32` 데이터 유형으로 결정됩니다.
:::

## Param 18

이 매개변수는 TON 블록체인의 데이터 저장 비용을 결정하는 설정을 나타냅니다. 이는 스팸을 방지하고 네트워크 유지를 장려하는 수단으로 작용합니다.

### 저장소 수수료 매개변수 딕셔너리:

- `utime_since`: 지정된 가격이 적용되는 초기 Unix 타임스탬프를 제공합니다.

- `bit_price_ps`와 `cell_price_ps`: TON 블록체인의 주요 워크체인에서 65536초 동안 1비트나 1셀의 정보에 대한 저장 가격을 나타냅니다.

- `mc_bit_price_ps`와 `mc_cell_price_ps`: 65536초 동안 TON 마스터체인에서의 컴퓨팅 자원 가격을 나타냅니다.

:::info

각 인수의 값은 `uint32` 데이터 유형으로 결정됩니다.

나머지는 `uint64` 데이터 타입으로 값을 받습니다.
:::

## Param 20과 21

이 매개변수들은 TON 네트워크에서 연산 비용을 정의합니다. 모든 연산의 복잡성은 가스 단위로 추정됩니다.

- `flat_gas_limit`와 `flat_gas_price`: `flat_gas_price` 가격으로 제공되는 특정 시작 가스량(TON 가상 머신 실행 비용을 상쇄하기 위함)

- `gas_price`: 이 매개변수는 네트워크의 가스 가격을 반영하며, 65536 가스 단위당 나노톤 단위입니다.

- `gas_limit`: 트랜잭션당 소비할 수 있는 최대 가스량을 나타냅니다.

- `special_gas_limit`: 특별한(시스템) 컨트랙트의 트랜잭션당 소비할 수 있는 가스량 제한을 나타냅니다.

- `gas_credit`: 외부 메시지 확인을 위해 트랜잭션에 제공되는 가스 단위의 크레딧을 나타냅니다.

- `block_gas_limit`: 단일 블록 내에서 소비할 수 있는 최대 가스량을 나타냅니다.

- `freeze_due_limit`와 `delete_due_limit`: 컨트랙트가 동결되고 삭제되는 누적 저장 수수료의 한도(나노TON 단위)입니다.

:::info
`gas_credit`과 다른 매개변수에 대한 자세한 내용은 외부 메시지 섹션 [여기](/v3/documentation/smart-contracts/transaction-fees/accept-message-effects#external-messages)를 참조하세요.
:::

## Param 22와 23

이 매개변수들은 블록에 대한 제한을 설정하며, 이 제한에 도달하면 블록이 종료되고 남은 메시지의 콜백(있는 경우)이 다음 블록으로 이월됩니다.

### 설정 매개변수:

- `bytes`: 바이트 단위로 블록 크기의 제한을 설정합니다.

- `underload`: 언더로드는 샤드가 부하가 없음을 인식하고 이웃 샤드가 기꺼이 받아들일 경우 병합하려는 상태입니다.

- `soft_limit`: 소프트 제한 - 이 제한에 도달하면 내부 메시지 처리가 중단됩니다.

- `hard_limit`: 하드 제한 - 이것은 절대적인 최대 크기입니다.

- `gas`: 블록이 소비할 수 있는 가스양에 대한 제한을 설정합니다. 블록체인 맥락에서 가스는 연산 작업의 지표입니다. 언더로드, 소프트 및 하드 제한에 대한 제한은 바이트 크기와 동일하게 작동합니다.

- `lt_delta`: 첫 번째와 마지막 트랜잭션 사이의 논리적 시간 차이에 대한 제한을 설정합니다. 논리적 시간은 TON 블록체인에서 이벤트를 정렬하는 데 사용되는 개념입니다. 언더로드, 소프트 및 하드 제한에 대한 제한은 바이트 크기와 가스와 동일하게 작동합니다.

:::info
샤드의 부하가 부족하고 그에 따라 이웃과 병합하고자 하는 경우, `soft_limit`는 내부(internal) 메시지가 처리를 중단하지만 외부(external) 메시지는 계속되는 상태를 정의합니다. 외부(external) 메시지는 `(soft_limit + hard_limit)/2`와 같은 제한에 도달할 때까지 처리됩니다.
:::

## Param 24와 25

매개변수 24는 TON 블록체인의 마스터체인에서 메시지 전송 비용에 대한 설정을 나타냅니다.

매개변수 25는 다른 모든 경우의 메시지 전송 비용에 대한 설정을 나타냅니다.

### 전달 비용을 정의하는 설정 매개변수:

- `lump_price`: 메시지 크기나 복잡성에 관계없이 메시지를 전달하는 기본 가격을 의미합니다.

- `bit_price`: 메시지 전달의 비트당 비용을 나타냅니다.

- `cell_price`: 셀당 메시지 전달 비용을 반영합니다. 셀은 TON 블록체인의 기본 데이터 저장 단위입니다.

- `ihr_price_factor`: 즉시 하이퍼큐브 라우팅(IHR) 비용을 계산하는 데 사용되는 요소입니다.
    :::info
    IHR은 메시지가 수신자의 샤드 체인으로 직접 전송되는 TON 블록체인 네트워크의 메시지 전달 방법입니다.
    :::

- `first_frac`: 메시지 경로를 따라 첫 번째 전환에 사용될 남은 잔액의 분율을 정의합니다.

- `next_frac`: 메시지 경로를 따라 후속 전환에 사용될 남은 잔액의 분율을 정의합니다.

## Param 28

이 매개변수는 TON 블록체인의 Catchain 프로토콜 설정을 제공합니다. Catchain은 검증자 간의 합의를 달성하기 위해 TON에서 사용되는 가장 낮은 수준의 합의 프로토콜입니다.

### 설정 매개변수:

- `flags`: 다양한 이진 매개변수를 설정하는 데 사용할 수 있는 일반 필드. 이 경우 0과 같으며, 특정 플래그가 설정되지 않았음을 의미합니다.

- `shuffle_mc_validators`: 마스터체인 검증자를 섞을지 여부를 나타내는 부울 값. 이 매개변수가 1로 설정되면 검증자가 섞입니다.

- `mc_catchain_lifetime`: 마스터체인 catchain 그룹의 수명(초)

- `shard_catchain_lifetime`: 샤드체인 catchain 그룹의 수명(초)

- `shard_validators_lifetime`: 샤드체인 검증자 그룹의 수명(초)

- `shard_validators_num`: 각 샤드체인 검증 그룹의 검증자 수

## Param 29

이 매개변수는 TON 블록체인의 catchain([Param 28](#param-28)) 위의 합의 프로토콜에 대한 설정을 제공합니다. 합의 프로토콜은 블록체인 네트워크의 중요한 구성 요소이며, 모든 노드가 분산 원장의 상태에 동의하도록 보장합니다.

### 설정 매개변수:

- `flags`: 다양한 이진 매개변수를 설정하는 데 사용할 수 있는 일반 필드. 이 경우 0과 같으며, 특정 플래그가 설정되지 않았음을 의미합니다.

- `new_catchain_ids`: 새 Catchain 식별자를 생성할지 여부를 나타내는 부울 값. 이 매개변수가 1로 설정되면 새 식별자가 생성됩니다. 이 경우 1의 값이 할당되어 새 식별자가 생성됨을 의미합니다.

- `round_candidates`: 합의 프로토콜의 각 라운드에서 고려될 후보자 수. 여기서는 3으로 설정됩니다.

- `next_candidate_delay_ms`: 블록 후보 생성 권한이 다음 검증자에게 넘어가기 전의 지연 시간(밀리초). 여기서는 2000ms(2초)로 설정됩니다.

- `consensus_timeout_ms`: 블록 합의에 대한 타임아웃(밀리초). 여기서는 16000ms(16초)로 설정됩니다.

- `fast_attempts`: 합의에 도달하기 위한 "빠른" 시도 횟수. 여기서는 3으로 설정됩니다.

- `attempt_duration`: 각 합의 시도의 지속 시간. 여기서는 8로 설정됩니다.

- `catchain_max_deps`: Catchain 블록의 최대 의존성 수. 여기서는 4로 설정됩니다.

- `max_block_bytes`: 블록의 최대 크기(바이트). 여기서는 2097152바이트(2MB)로 설정됩니다.

- `max_collated_bytes`: 직렬화된 블록 정확성 증명의 최대 크기(바이트). 여기서는 2097152바이트(2MB)로 설정됩니다.

- `proto_version`: 프로토콜 버전. 여기서는 2로 설정됩니다.

- `catchain_max_blocks_coeff`: Catchain의 블록 생성 속도를 제한하는 계수, [설명](https://github.com/ton-blockchain/ton/blob/master/doc/catchain-dos.md). 여기서는 10000으로 설정됩니다.

## Param 31

이 매개변수는 가스나 저장소 모두에 대해 수수료가 부과되지 않고 틱톡 트랜잭션을 생성할 수 있는 스마트 컨트랙트 주소의 설정을 나타냅니다. 목록에는 일반적으로 거버넌스 컨트랙트가 포함됩니다. 매개변수는 이진 트리 구조 - 주소의 256비트 표현이 키인 트리(HashMap 256)로 표시됩니다. 이 목록에는 마스터체인의 주소만 있을 수 있습니다.

## Param 32, 34 및 36

이전(32), 현재(34) 및 다음(36) 라운드의 검증자 목록입니다. 매개변수 36은 선거 끝부터 라운드 시작까지 설정됩니다.

### 설정 매개변수:

- `cur_validators`: 현재 검증자 목록입니다. 검증자는 일반적으로 블록체인 네트워크에서 트랜잭션을 검증하는 책임이 있습니다.

- `utime_since`와 `utime_until`: 이 검증자들이 활성화되는 기간을 제공합니다.

- `total`과 `main`: 네트워크의 총 검증자 수와 마스터체인을 검증하는 검증자 수를 제공합니다.

- `total_weight`: 검증자의 가중치를 합산합니다.

- `list`: `id->validator-data` 트리 형식의 검증자 목록: `validator_addr`, `public_key`, `weight`, `adnl_addr`: 각 검증자에 대한 세부 정보 - 마스터체인의 256 주소, 공개 키, 가중치, ADNL 주소(TON의 네트워크 수준에서 사용되는 주소)를 제공합니다.

## Param 40

이 매개변수는 부적절한 행동(비검증)에 대한 처벌 설정의 구조를 정의합니다. 매개변수가 없는 경우 기본 벌금 크기는 101 TON입니다.

## 설정 매개변수:

**`MisbehaviourPunishmentConfig`**: 이 데이터 구조는 시스템의 부적절한 행동이 어떻게 처벌되는지 정의합니다.

다음 필드를 포함합니다:

- `default_flat_fine`: 스테이크 크기와 무관한 벌금 부분입니다.

- `default_proportional_fine`: 검증자의 스테이크 크기에 비례하는 벌금 부분입니다.

- `severity_flat_mult`: 검증자의 심각한 위반에 대해 `default_flat_fine` 값에 적용되는 승수입니다.

- `severity_proportional_mult`: 검증자의 심각한 위반에 대해 `default_proportional_fine` 값에 적용되는 승수입니다.

- `unpunishable_interval`: 임시 네트워크 문제나 다른 이상을 제거하기 위해 위반자가 처벌받지 않는 기간을 나타냅니다.

- `long_interval`, `long_flat_mult`, `long_proportional_mult`: "긴" 기간과 부적절한 행동에 대한 정액 및 비례 벌금의 승수를 정의합니다.

- `medium_interval`, `medium_flat_mult`, `medium_proportional_mult`: 유사하게 "중간" 기간과 부적절한 행동에 대한 정액 및 비례 벌금의 승수를 정의합니다.

## Param 43

이 매개변수는 계정과 메시지의 다양한 크기 제한과 다른 특성에 관련됩니다.

### 설정 매개변수:

- `max_msg_bits`: 최대 메시지 크기(비트)

- `max_msg_cells`: 메시지가 차지할 수 있는 최대 셀(저장 단위의 한 형태) 수

- `max_library_cells`: 라이브러리 셀에 사용할 수 있는 최대 셀 수

- `max_vm_data_depth`: 메시지와 계정 상태의 최대 셀 깊이

- `max_ext_msg_size`: 최대 외부 메시지 크기(비트)

- `max_ext_msg_depth`: 최대 외부 메시지 깊이. 메시지 내 데이터 구조의 깊이를 의미할 수 있습니다.

- `max_acc_state_cells`: 계정 상태가 차지할 수 있는 최대 셀 수

- `max_acc_state_bits`: 최대 계정 상태 크기(비트)

없는 경우 기본 매개변수가 사용됩니다:

- `max_size` = 65535
- `max_depth` = 512
- `max_msg_bits` = 1 << 21
- `max_msg_cells` = 1 << 13
- `max_library_cells` = 1000
- `max_vm_data_depth` = 512
- `max_acc_state_cells` = 1 << 16
- `max_acc_state_bits` = (1 << 16) \* 1023

:::info
소스 코드에서 [여기](https://github.com/ton-blockchain/ton/blob/fc9542f5e223140fcca833c189f77b1a5ae2e184/crypto/block/mc-config.h#L379)에서 표준 매개변수에 대해 자세히 볼 수 있습니다.
:::

## Param 44

이 매개변수는 `suspended_until`까지 초기화할 수 없는 일시 중단된 주소 목록을 정의합니다. 아직 초기화되지 않은 계정에만 적용됩니다. 이는 토큰노믹스를 안정화하기 위한 조치입니다(초기 마이너 제한). 설정되지 않은 경우 - 제한이 없습니다. 각 주소는 이 트리의 끝 노드로 표현되며, 트리와 같은 구조를 통해 주소의 존재 여부를 효과적으로 확인할 수 있습니다.

:::info
토큰노믹스의 안정화는 "The Open Network" 텔레그램 채널의 [공식 보고서](https://t.me/tonblockchain/178)에서 자세히 설명됩니다.
:::

## Param 45

미리 컴파일된 컨트랙트 목록은 마스터체인 설정에 저장됩니다:

```
precompiled_smc#b0 gas_usage:uint64 = PrecompiledSmc;
precompiled_contracts_config#c0 list:(HashmapE 256 PrecompiledSmc) = PrecompiledContractsConfig;
_ PrecompiledContractsConfig = ConfigParam 45;
```

미리 컴파일된 컨트랙트에 대한 자세한 내용은 [이 페이지](/v3/documentation/smart-contracts/contracts-specs/precompiled-contracts)를 참조하세요.

## Param 71 - 73

이 매개변수는 다른 네트워크에서 TON을 래핑하기 위한 브릿지에 관한 것입니다:

- ETH-TON **(71)**
- BSC-TON **(72)**
- Polygon-TON **(73)**

### 설정 매개변수:

- `bridge_address`: 다른 네트워크에서 래핑된 TON을 발행하기 위해 TON을 수락하는 브릿지 컨트랙트 주소입니다.

- `oracle_multisig_address`: 브릿지 관리 지갑 주소입니다. 멀티시그 지갑은 트랜잭션 승인을 위해 여러 당사자의 서명이 필요한 디지털 지갑 유형입니다. 보안을 강화하기 위해 자주 사용됩니다. 오라클이 당사자 역할을 합니다.

- `oracles`: `id->address` 형태의 트리로된 오라클 목록

- `external_chain_address`: 해당 외부 블록체인의 브릿지 컨트랙트 주소입니다.

## Param 79, 81 및 82

이 매개변수는 다른 네트워크의 토큰을 TON 네트워크의 토큰으로 래핑하기 위한 브릿지에 관한 것입니다:

- ETH-TON **(79)**
- BSC-TON **(81)**
- Polygon-TON **(82)**

### 설정 매개변수:

- `bridge_address`와 `oracles_address`: 브릿지와 브릿지 관리 컨트랙트(오라클 멀티시그)의 블록체인 주소입니다.

- `oracles`: `id->address` 형태의 트리로된 오라클 목록

- `state_flags`: 상태 플래그. 이 매개변수는 개별 브릿지 기능의 활성화/비활성화를 담당합니다.

- `prices`: 이 매개변수는 `bridge_burn_fee`, `bridge_mint_fee`, `wallet_min_tons_for_storage`, `wallet_gas_consumption`, `minter_min_tons_for_storage`, `discover_gas_consumption` 같은 브릿지와 관련된 다양한 작업이나 수수료에 대한 가격 목록이나 딕셔너리를 포함합니다.

- `external_chain_address`: 다른 블록체인의 브릿지 컨트랙트 주소입니다.

## 음수 매개변수

:::info
음수 매개변수와 양수 매개변수의 차이는 검증자의 검증 필요성입니다; 일반적으로 특정한 할당된 역할이 없습니다.
:::

## 다음 단계

이 글을 깊이 있게 살펴본 후에는 다음 문서들을 더 자세히 공부하는 것이 강력히 권장됩니다:

- [whitepaper.pdf](https://ton.org/whitepaper.pdf)와 [tblkch.pdf](/tblkch.pdf)의 원본이지만 제한적인 설명.

- [mc-config.h](https://github.com/ton-blockchain/ton/blob/fc9542f5e223140fcca833c189f77b1a5ae2e184/crypto/block/mc-config.h), [block.tlb](https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb) 및 [BlockMasterConfig Type](https://docs.evercloud.dev/reference/graphql-api/field_descriptions#blockmasterconfig-type).

## 📖 참고

이 페이지에서 TON 블록체인의 활성 네트워크 설정을 찾을 수 있습니다:

- 메인넷: https://ton.org/global-config.json
- 테스트넷: https://ton.org/testnet-global.config.json
- [러시아어 버전](https://github.com/delovoyhomie/description-config-for-TON-Blockchain/blob/main/Russian-version.md).
