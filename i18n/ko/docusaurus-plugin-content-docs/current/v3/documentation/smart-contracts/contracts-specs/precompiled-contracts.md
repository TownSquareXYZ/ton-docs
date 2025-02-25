# 미리 컴파일된 컨트랙트

*미리 컴파일된 스마트 컨트랙트*는 노드에 C++ 구현이 있는 컨트랙트입니다.
검증자가 이러한 스마트 컨트랙트에서 트랜잭션을 실행할 때, TVM 대신 이 구현을 실행할 수 있습니다.
이는 성능을 향상시키고 계산 수수료를 줄일 수 있게 합니다.

## 구성

미리 컴파일된 컨트랙트 목록은 마스터체인 구성에 저장됩니다:

```
precompiled_smc#b0 gas_usage:uint64 = PrecompiledSmc;
precompiled_contracts_config#c0 list:(HashmapE 256 PrecompiledSmc) = PrecompiledContractsConfig;
_ PrecompiledContractsConfig = ConfigParam 45;
```

`list:(HashmapE 256 PrecompiledSmc)`는 `(code_hash -> precomplied_smc)` 맵입니다.
컨트랙트의 코드 해시가 이 맵에서 발견되면 해당 컨트랙트는 *미리 컴파일된* 것으로 간주됩니다.

## 컨트랙트 실행

*미리 컴파일된 스마트 컨트랙트*(`ConfigParam 45`에서 찾은 코드 해시가 있는 모든 컨트랙트)의 모든 트랜잭션은 다음과 같이 실행됩니다:

1. 마스터체인 구성에서 `gas_usage`를 가져옵니다.
2. 잔액이 `gas_usage` 가스를 지불하기에 충분하지 않으면 계산 단계가 건너뛰기 이유 `cskip_no_gas`로 실패합니다.
3. 코드는 두 가지 방식으로 실행될 수 있습니다:
4. 미리 컴파일된 실행이 비활성화되었거나 현재 노드 버전에서 C++ 구현을 사용할 수 없는 경우 TVM이 평소처럼 실행됩니다. TVM의 가스 제한은 트랜잭션 가스 제한(1M 가스)으로 설정됩니다.
5. 미리 컴파일된 구현이 활성화되고 사용 가능한 경우 C++ 구현이 실행됩니다.
6. [계산 단계 값](https://github.com/ton-blockchain/ton/blob/dd5540d69e25f08a1c63760d3afb033208d9c99b/crypto/block/block.tlb#L308) 재정의: `gas_used`를 `gas_usage`로 설정; `vm_steps`, `vm_init_state_hash`, `vm_final_state_hash`를 0으로 설정.
7. 계산 수수료는 실제 TVM 가스 사용량이 아닌 `gas_usage`를 기반으로 합니다.

미리 컴파일된 컨트랙트가 TVM에서 실행될 때, `c7`의 17번째 요소는 `gas_usage`로 설정되며 `GETPRECOMPILEDGAS` 명령어로 검색할 수 있습니다. 미리 컴파일되지 않은 컨트랙트의 경우 이 값은 `null`입니다.

미리 컴파일된 컨트랙트의 실행은 기본적으로 비활성화되어 있습니다. `--enable-precompiled-smc` 플래그와 함께 `validator-engine`을 실행하여 활성화할 수 있습니다.

미리 컴파일된 컨트랙트를 실행하는 두 가지 방법 모두 동일한 트랜잭션을 생성한다는 점에 유의하세요.
따라서 C++ 구현이 있는 검증자와 없는 검증자가 네트워크에서 안전하게 공존할 수 있습니다.
이는 모든 검증자가 노드 소프트웨어를 즉시 업데이트할 필요 없이 `ConfigParam 45`에 새 항목을 추가할 수 있게 합니다.

## 사용 가능한 구현

여기에 용이 있습니다.

## 참조

- [Governance Contracts](/v3/documentation/smart-contracts/contracts-specs/governance)
