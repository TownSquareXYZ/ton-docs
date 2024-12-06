# 스토리지 제공자

*스토리지 제공자*는 요금을 받고 파일을 저장하는 서비스입니다.

## 바이너리

Linux/Windows/MacOS용 `storage-daemon` 및 `storage-daemon-cli` 바이너리는 [TON Auto Builds](https://github.com/ton-blockchain/ton/releases/latest)에서 다운로드할 수 있습니다.

## 소스에서 컴파일하기

이 [지침](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#storage-daemon)을 사용하여 `storage-daemon` 및 `storage-damon-cli`를 소스에서 컴파일할 수 있습니다.

## 주요 개념

스토리지 요청을 수락하고 클라이언트의 지불을 관리하는 스마트 컨트랙트와 파일을 업로드하고 클라이언트에게 제공하는 애플리케이션으로 구성됩니다. 작동 방식은 다음과 같습니다:

1. 제공자의 소유자가 `storage-daemon`을 실행하고, 메인 스마트 컨트랙트를 배포하며, 매개변수를 설정합니다. 컨트랙트의 주소는 잠재적 클라이언트와 공유됩니다.
2. 클라이언트는 `storage-daemon`을 사용하여 파일에서 Bag을 생성하고 제공자의 스마트 컨트랙트에 특별한 내부 메시지를 보냅니다.
3. 제공자의 스마트 컨트랙트는 이 특정 Bag을 처리하기 위한 스토리지 컨트랙트를 생성합니다.
4. 제공자는 블록체인에서 요청을 발견하면 Bag을 다운로드하고 스토리지 컨트랙트를 활성화합니다.
5. 그런 다음 클라이언트는 스토리지 비용을 스토리지 컨트랙트로 이체할 수 있습니다. 지불을 받기 위해 제공자는 정기적으로 Bag을 계속 저장하고 있다는 증명을 컨트랙트에 제시합니다.
6. 스토리지 컨트랙트의 자금이 소진되면 컨트랙트는 비활성화된 것으로 간주되며 제공자는 더 이상 Bag을 저장할 필요가 없습니다. 클라이언트는 컨트랙트를 재충전하거나 파일을 검색할 수 있습니다.

:::info
클라이언트는 소유권 증명을 스토리지 컨트랙트에 제공하여 언제든지 파일을 검색할 수도 있습니다. 그러면 컨트랙트는 파일을 클라이언트에게 해제하고 자체적으로 비활성화됩니다.
:::

## 스마트 컨트랙트

[스마트 컨트랙트 소스 코드](https://github.com/ton-blockchain/ton/tree/master/storage/storage-daemon/smartcont).

## 클라이언트의 제공자 사용

스토리지 제공자를 사용하려면 해당 스마트 컨트랙트의 주소를 알아야 합니다. 클라이언트는 `storage-daemon-cli`에서 다음 명령으로 제공자의 매개변수를 얻을 수 있습니다:

```
get-provider-params <address>
```

### 제공자의 매개변수:

- 새로운 스토리지 컨트랙트 수락 여부
- 최소 및 최대 *Bag* 크기(바이트 단위)
- 요금 - 스토리지 비용. 일당 메가바이트당 nanoTON으로 지정됨
- 최대 스팬 - 제공자가 얼마나 자주 *Bag* 저장 증명을 제공해야 하는지

### 저장 요청

*Bag*을 생성하고 다음 명령으로 메시지를 생성해야 합니다:

```
new-contract-message <BagID> <file> --query-id 0 --provider <address>
```

### 정보:

이 명령을 실행하는 데는 큰 *Bag*의 경우 시간이 걸릴 수 있습니다. 메시지 본문이 `<file>`에 저장됩니다(전체 내부 메시지가 아님). 쿼리 ID는 0에서 `2^64-1` 사이의 아무 숫자나 될 수 있습니다. 메시지에는 제공자의 매개변수(요금 및 최대 스팬)가 포함됩니다. 이러한 매개변수는 명령 실행 후 출력되므로 보내기 전에 다시 확인해야 합니다. 제공자의 소유자가 매개변수를 변경하면 메시지가 거부되므로 새 스토리지 컨트랙트의 조건은 클라이언트가 예상한 것과 정확히 일치하게 됩니다.

그런 다음 클라이언트는 이 본문이 포함된 메시지를 제공자의 주소로 보내야 합니다. 오류가 발생하면 메시지가 발신자에게 반환됩니다(바운스). 그렇지 않으면 새 스토리지 컨트랙트가 생성되고 클라이언트는 [`op=0xbf7bd0c1`](https://github.com/ton-blockchain/ton/tree/testnet/storage/storage-daemon/smartcont/constants.fc#L3)와 동일한 쿼리 ID를 가진 메시지를 받게 됩니다.

이 시점에서 컨트랙트는 아직 활성화되지 않았습니다. 제공자가 *Bag*을 다운로드하면 스토리지 컨트랙트를 활성화하고 클라이언트는 [`op=0xd4caedcd`](https://github.com/SpyCheese/ton/blob/tonstorage/storage/storage-daemon/smartcont/constants.fc#L4)가 포함된 메시지를 받게 됩니다(역시 스토리지 컨트랙트에서).

스토리지 컨트랙트에는 "클라이언트 잔액"이 있습니다 - 이는 클라이언트가 컨트랙트로 이체했지만 아직 제공자에게 지불되지 않은 자금입니다. 자금은 점진적으로 이 잔액에서 차감됩니다(일당 메가바이트당 요금과 동일한 속도로). 초기 잔액은 클라이언트가 스토리지 컨트랙트 생성 요청과 함께 이체한 금액입니다. 그런 다음 클라이언트는 스토리지 컨트랙트에 단순 이체를 하여 잔액을 충전할 수 있습니다(이는 어떤 주소에서나 할 수 있습니다). 남은 클라이언트 잔액은 [`get_storage_contract_data`](https://github.com/ton-blockchain/ton/tree/testnet/storage/storage-daemon/smartcont/storage-contract.fc#L222) get 메소드에 의해 두 번째 값(`balance`)으로 반환됩니다.

### 다음과 같은 경우 컨트랙트가 종료될 수 있습니다:

:::info
스토리지 컨트랙트가 종료되는 경우, 클라이언트는 남은 잔액과 [`op=0xb6236d63`](https://github.com/ton-blockchain/ton/tree/testnet/storage/storage-daemon/smartcont/constants.fc#L6)가 포함된 메시지를 받습니다.
:::

- 활성화 전, 생성 직후, 제공자가 컨트랙트 수락을 거부하는 경우(제공자의 한도 초과 또는 기타 오류)
- 클라이언트 잔액이 0에 도달
- 제공자가 자발적으로 컨트랙트를 종료할 수 있음
- 클라이언트는 자신의 주소에서 [`op=0x79f937ea`](https://github.com/ton-blockchain/ton/tree/testnet/storage/storage-daemon/smartcont/constants.fc#L2)와 임의의 쿼리 ID가 포함된 메시지를 보내 자발적으로 컨트랙트를 종료할 수 있음

## 제공자 실행 및 구성

스토리지 제공자는 `storage-daemon`의 일부이며 `storage-daemon-cli`로 관리됩니다. `storage-daemon`은 `-P` 플래그와 함께 시작해야 합니다.

### 메인 스마트 컨트랙트 생성

`storage-daemon-cli`에서 이렇게 할 수 있습니다:

```
deploy-provider
```

:::info 중요!
제공자를 초기화하기 위해 지정된 주소로 1 TON이 포함된 바운스 불가능한 메시지를 보내도록 요청받을 것입니다. `get-provider-info` 명령을 사용하여 컨트랙트가 생성되었는지 확인할 수 있습니다.
:::

기본적으로 컨트랙트는 새로운 스토리지 컨트랙트를 수락하지 않도록 설정되어 있습니다. 활성화하기 전에 제공자를 구성해야 합니다. 제공자의 설정은 `storage-daemon`에 저장된 구성과 블록체인에 저장된 컨트랙트 매개변수로 구성됩니다.

### 구성:

- `max contracts` - 동시에 존재할 수 있는 최대 스토리지 컨트랙트 수
- `max total size` - 스토리지 컨트랙트의 *Bag* 최대 총 크기
  구성 값은 `get-provider-info`로 볼 수 있고, 다음과 같이 변경할 수 있습니다:

```
set-provider-config --max-contracts 100 --max-total-size 100000000000
```

### 컨트랙트 매개변수:

- `accept` - 새로운 스토리지 컨트랙트 수락 여부
- `max file size`, `min file size` - 하나의 *Bag*에 대한 크기 제한
- `rate` - 저장 비용(일당 메가바이트당 nanoTON으로 지정)
- `max span` - 제공자가 얼마나 자주 저장 증명을 제출해야 하는지

매개변수는 `get-provider-info`로 볼 수 있고, 다음과 같이 변경할 수 있습니다:

```
set-provider-params --accept 1 --rate 1000000000 --max-span 86400 --min-file-size 1024 --max-file-size 1000000000
```

### 주목할 만한 사항

참고: `set-provider-params` 명령에서는 일부 매개변수만 지정할 수 있습니다. 나머지는 현재 매개변수에서 가져옵니다. 블록체인의 데이터는 즉시 업데이트되지 않으므로 연속적인 여러 `set-provider-params` 명령은 예상치 못한 결과를 초래할 수 있습니다.

스토리지 컨트랙트 작업에 대한 수수료를 충당할 수 있도록 제공자의 잔액에 처음에 1 TON 이상을 넣는 것이 좋습니다. 하지만 첫 번째 바운스 불가능한 메시지와 함께 너무 많은 TON을 보내지 마십시오.

`accept` 매개변수를 `1`로 설정한 후, 스마트 컨트랙트는 클라이언트의 요청을 수락하고 스토리지 컨트랙트를 생성하기 시작하며, 스토리지 데몬은 자동으로 이를 처리합니다: *Bag*의 다운로드 및 배포, 저장 증명 생성.

## 제공자와의 추가 작업

### 기존 스토리지 컨트랙트 목록

```
get-provider-info --contracts --balances
```

각 스토리지 컨트랙트에는 `Client$` 및 `Contract$` 잔액이 나열되어 있습니다. 이들 간의 차이는 `withdraw <address>` 명령으로 메인 제공자 컨트랙트로 인출할 수 있습니다.

`withdraw-all` 명령은 사용 가능한 `1 TON` 이상이 있는 모든 컨트랙트에서 자금을 인출합니다.

모든 스토리지 컨트랙트는 `close-contract <address>` 명령으로 종료할 수 있습니다. 이렇게 하면 자금도 메인 컨트랙트로 이체됩니다. 클라이언트의 잔액이 소진되면 자동으로 동일한 일이 발생합니다. 이 경우 *Bag* 파일은 삭제됩니다(동일한 *Bag*을 사용하는 다른 컨트랙트가 없는 경우).

### 이체

메인 스마트 컨트랙트에서 아무 주소로나 자금을 이체할 수 있습니다(금액은 nanoTON으로 지정):

```
send-coins <address> <amount>
send-coins <address> <amount> --message "Some message"
```

:::info
제공자가 저장한 모든 *Bag*은 `list` 명령으로 사용할 수 있으며, 평소와 같이 사용할 수 있습니다. 제공자의 작업을 방해하지 않기 위해 이들을 삭제하거나 이 스토리지 데몬을 다른 *Bag*과 함께 작업하는 데 사용하지 마십시오.
:::
