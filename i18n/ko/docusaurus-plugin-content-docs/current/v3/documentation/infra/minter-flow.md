# 추가 화폐 발행

## 추가 화폐

[Ton 블록체인 백서 3.1.6](https://ton-blockchain.github.io/docs/tblkch.pdf#page=55)에 따르면, TON 블록체인은 사용자가 특정 조건을 충족하는 경우 Toncoin 외에 임의의 암호화폐나 토큰을 정의할 수 있게 합니다. 이러한 추가 화폐는 32비트 _currency_ids_로 식별됩니다. 정의된 추가 화폐 목록은 마스터체인에 저장된 블록체인 설정의 일부입니다.
각 내부 메시지와 계정 잔액은 `ExtraCurrencyCollection`(메시지에 첨부되거나 잔액에 보관된 추가 화폐 세트)을 위한 특별한 필드를 포함합니다:

```tlb
extra_currencies$_ dict:(HashmapE 32 (VarUInteger 32)) = ExtraCurrencyCollection;
currencies$_ grams:Grams other:ExtraCurrencyCollection = CurrencyCollection;
```

## 추가 화폐 설정

발행되어야 할 모든 화폐의 딕셔너리, 정확히는 `ExtraCurrencyCollection`이 `ConfigParam7`에 저장됩니다:

```tlb
_ to_mint:ExtraCurrencyCollection = ConfigParam 7;
```

`ConfigParam 6`은 발행과 관련된 데이터를 포함합니다:

```tlb
_ mint_new_price:Grams mint_add_price:Grams = ConfigParam 6;
```

`ConfigParam2`는 *발행자* 주소를 포함합니다.

## 저수준 발행 흐름

각 블록에서 콜레이터는 이전 블록 끝의 모든 화폐의 글로벌 잔액(구 글로벌 잔액)과 `ConfigParam7`을 비교합니다. `ConfigParam7`의 어떤 화폐의 금액이 글로벌 잔액보다 적으면 설정이 유효하지 않습니다. `ConfigParam7`의 어떤 화폐의 금액이 글로벌 잔액보다 높으면 발행 메시지가 생성됩니다.

이 발행 메시지는 소스가 `-1:0000000000000000000000000000000000000000000000000000000000000000`이고 `ConfigParam2`의 _발행자_가 대상이며 구 글로벌 잔액을 초과하는 `ConfigParam7`의 추가 화폐를 포함합니다.

여기서 문제는 발행 메시지가 추가 화폐만 포함하고 TON 코인은 포함하지 않는다는 점입니다. 즉, _발행자_가 기본 스마트 컨트랙트(`ConfigParam31`에 있음)로 설정되어 있더라도 발행 메시지는 중단된 트랜잭션을 발생시킵니다: `compute_ph:(tr_phase_compute_skipped reason:cskip_no_gas)`.

## 고수준 발행 흐름

*발행자* 스마트 컨트랙트는 새 추가 화폐 생성이나 기존 화폐의 추가 토큰 발행 요청을 받으면:

1. `ConfigParam6`에 정의된 수수료를 요청 메시지에서 공제할 수 있는지 확인
2. 1. 기존 토큰의 경우: 발행 권한 확인(_소유자_만 새로운 토큰 발행 가능)
   2. 새 화폐 생성의 경우: 화폐 id가 사용되지 않았는지 확인하고 새 화폐의 소유자 저장
3. 설정 컨트랙트에 메시지 전송(`ConfigParam7`의 `ExtraCurrencyCollection`에 추가되어야 함)
4. `0:0000...0000`(다음 블록이나 그 이후 블록에서 반드시 바운스됨)에 extra_currency id와 함께 메시지 전송

`0:0000...0000`에서 메시지를 받으면:

1. 바운스된 메시지에서 extra_currency id 읽기
2. 발행자 잔액에 해당 id의 토큰이 있으면 `ok` 메시지와 함께 해당 화폐 소유자에게 전송
3. 그렇지 않으면 화폐 소유자에게 `fail` 메시지 전송

## 해결해야 할 문제

1. 요청 처리 연기를 위해 `0:0000...0000`에 메시지를 보내는 우회 방법은 매우 지저분합니다.
2. 발행이 실패하는 경우를 고려해야 합니다. 현재로서는 화폐 금액이 0이거나 현재 잔액과 발행된 금액의 합이 `(VarUInteger 32)`에 맞지 않는 경우만 가능해 보입니다.
3. 소각은 어떻게 할까요? 첫 눈에 보기에는 방법이 없어 보입니다.
4. 발행 수수료가 금지적이어야 할까요? 다시 말해, 수백만 개의 추가 화폐를 갖는 것이 위험할까요(큰 설정, 콜레이션 시 제한되지 않은 dict 연산 수로 인한 잠재적 DoS?)
