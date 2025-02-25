# 라이브러리 셀

## 소개

TON이 셀에 데이터를 저장하는 방식의 핵심 기능 중 하나는 중복 제거입니다. 저장소, 메시지, 블록, 트랜잭션 등에서 중복된 셀은 한 번만 저장됩니다. 이는 직렬화된 데이터의 크기를 크게 줄이고, 단계별로 업데이트되는 데이터를 효율적으로 저장할 수 있게 합니다.

같은 이유로 TON의 많은 구조는 동시에 풍부하고, 편리하며 효율적입니다. 블록 구조는 메시지 큐, 트랜잭션 목록, 머클 업데이트 등 여러 곳에 동일한 메시지 사본을 포함합니다. 중복에 따른 오버헤드가 없으므로 필요한 곳에 데이터를 여러 번 저장할 수 있습니다.

라이브러리 셀은 온체인 중복 제거 메커니즘을 사용하여 이 기술을 커스텀 스마트 계약에 통합할 수 있게 합니다.
:::info
예를 들어 제톤-월렛 코드를 라이브러리 셀(~20개 셀과 6000비트 대신 1개 셀과 256+8비트)로 저장하면 `init_code`가 포함된 메시지의 전달 수수료가 0.011에서 0.003 TON으로 감소합니다.
:::

## 일반 정보

블록 1,000,000에서 1,000,001로의 베이스체인 단계를 고려해봅시다. 각 블록은 적은 양의 데이터(보통 1000개 미만의 트랜잭션)를 포함하지만, 전체 베이스체인 상태는 수백만 개의 계정을 포함하며 블록체인은 데이터의 무결성을 유지해야 하므로(특히 전체 상태의 머클 루트 해시를 블록에 커밋) 상태의 전체 트리를 업데이트해야 합니다.

이전 세대 블록체인의 경우, 각 블록에 대해 별도의 체인 상태를 저장하려면 너무 많은 공간이 필요하기 때문에 일반적으로 최근 상태만 추적합니다. 하지만 TON 블록체인에서는 중복 제거 덕분에 각 블록에 대해 새로운 셀만 저장소에 추가됩니다. 이는 처리 속도를 높일 뿐만 아니라 많은 오버헤드 없이 잔액, 상태를 확인하고 심지어 기록의 모든 지점에서 get 메서드를 실행할 수 있게 합니다!

유사한 계약들의 경우(예: 제톤-월렛), 노드는 중복 데이터(각 제톤-월렛의 동일한 코드)를 한 번만 저장합니다. 라이브러리 셀을 사용하면 이러한 계약에 대해 중복 제거 메커니즘을 활용하여 저장소와 전달 수수료를 줄일 수 있습니다.

:::info 상위 수준 비유
라이브러리 셀은 C++ 포인터처럼 생각할 수 있습니다: 많은 참조를 가진 더 큰 셀을 가리키는 작은 셀입니다. 참조된 셀(라이브러리 셀이 가리키는 셀)은 존재하고 공개 컨텍스트에 등록되어 있어야 합니다(*"게시됨"*).
:::

## 라이브러리 셀의 구조

라이브러리 셀은 다른 정적 셀에 대한 참조를 포함하는 [이국적인 셀](/v3/documentation/data-formats/tlb/exotic-cells)입니다. 특히 참조된 셀의 256비트 해시를 포함합니다.

TVM의 경우, 라이브러리 셀은 다음과 같이 작동합니다: TVM이 셀을 슬라이스로 여는 명령을 받을 때마다(TVM 명령어: `CTOS`, funC 메서드: `.begin_parse()`), 마스터체인 라이브러리 컨텍스트에서 라이브러리 셀의 해당 해시를 가진 셀을 검색합니다. 찾으면 참조된 셀을 열고 해당 슬라이스를 반환합니다.

라이브러리 셀을 여는 비용은 일반 셀을 여는 것과 같으므로, 훨씬 적은 공간을 차지하는(따라서 저장 및 전송 수수료가 적게 드는) 정적 셀의 투명한 대체제로 사용할 수 있습니다.

다른 라이브러리 셀을 참조하는 라이브러리 셀을 만들 수 있으며, 이는 다시 다른 셀을 참조할 수 있습니다. 이런 경우 `.begin_parse()`는 예외를 발생시킵니다. 하지만 이러한 라이브러리는 `XLOAD` 연산코드로 단계별로 풀 수 있습니다.

라이브러리 셀의 또 다른 중요한 특징은 참조된 셀의 해시를 포함하므로 일부 정적 데이터에 대한 궁극적인 참조라는 점입니다. 이 라이브러리 셀이 참조하는 데이터를 변경할 수 없습니다.

마스터체인 라이브러리 컨텍스트에서 찾을 수 있고 따라서 라이브러리 셀에 의해 참조되려면, 소스 셀이 마스터체인에 게시되어야 합니다. 이는 마스터체인에 존재하는 스마트 계약이 이 셀을 `public=true` 플래그와 함께 상태에 추가해야 함을 의미합니다. 이는 `SETLIBCODE` 연산코드를 사용하여 수행할 수 있습니다.

## 스마트 계약에서 사용

라이브러리 셀은 수수료 계산을 제외한 모든 컨텍스트에서 참조하는 일반 셀과 동일하게 동작하므로 정적 데이터가 있는 셀 대신 사용할 수 있습니다. 예를 들어, 제톤-월렛 코드를 라이브러리 셀로 저장할 수 있습니다(일반적인 ~20개 셀과 6000비트 대신 1개 셀과 256+8비트). 이는 저장소와 전달 수수료가 크게 감소합니다. 특히 `init_code`를 포함하는 `internal_transfer` 메시지의 전달 수수료가 0.011에서 0.003 TON으로 감소합니다.

### 라이브러리 셀에 데이터 저장

수수료를 줄이기 위해 제톤-월렛 코드를 라이브러리 셀로 저장하는 예제를 살펴보겠습니다. 먼저 제톤-월렛을 코드를 포함하는 일반 셀로 컴파일해야 합니다.

그런 다음 일반 셀에 대한 참조가 있는 라이브러리 셀을 만들어야 합니다. 라이브러리 셀은 라이브러리의 8비트 태그 `0x02`와 그 뒤에 참조된 셀 해시의 256비트를 포함합니다.

### Fift에서 사용

기본적으로 빌더에 태그와 해시를 넣은 다음 "빌더를 이국적인 셀로 닫아야" 합니다.

이는 [이와 같은](https://github.com/ton-blockchain/multisig-contract-v2/blob/master/contracts/auto/order_code.func) Fift-asm 구성으로 수행할 수 있습니다. [여기](https://github.com/ton-blockchain/multisig-contract-v2/blob/master/wrappers/Order.compile.ts)에서 일부 계약을 직접 라이브러리 셀로 컴파일하는 예제를 볼 수 있습니다.

```fift
;; https://docs.ton.org/tvm.pdf, page 30
;; Library reference cell — Always has level 0, and contains 8+256 data bits, including its 8-bit type integer 2 
;; and the representation hash Hash(c) of the library cell being referred to. When loaded, a library
;; reference cell may be transparently replaced by the cell it refers to, if found in the current library context.

cell order_code() asm "<b 2 8 u, 0x6305a8061c856c2ccf05dcb0df5815c71475870567cab5f049e340bcf59251f3 256 u, b>spec PUSHREF";
```

### @ton/ton에서 사용

또는 Blueprint에서 `@ton/ton` 라이브러리를 사용하여 ts 레벨에서 라이브러리 셀을 완전히 형성할 수 있습니다:

```ts
import { Cell, beginCell } from '@ton/core';

let lib_prep = beginCell().storeUint(2,8).storeBuffer(jwallet_code_raw.hash()).endCell();
jwallet_code = new Cell({ exotic:true, bits: lib_prep.bits, refs:lib_prep.refs});
```

- [여기](https://github.com/ton-blockchain/stablecoin-contract/blob/de08b905214eb253d27009db6a124fd1feadbf72/sandbox_tests/JettonWallet.spec.ts#L104C1-L105C90)에서 소스를 확인하세요.

### 마스터체인 라이브러리 컨텍스트에 일반 셀 게시

실제 예제는 [여기](https://github.com/ton-blockchain/multisig-contract-v2/blob/master/contracts/helper/librarian.func)에서 확인할 수 있습니다. 이 계약의 핵심은 `set_lib_code(lib_to_publish, 2);`입니다 - 게시해야 하는 일반 셀과 flag=2(모든 사람이 사용할 수 있음을 의미)를 입력으로 받습니다.

셀을 게시하는 계약이 저장 비용을 지불하며 마스터체인의 저장 비용은 베이스체인보다 1000배 높다는 점에 유의하세요. 따라서 라이브러리 셀 사용은 수천 명의 사용자가 사용하는 계약에서만 효율적입니다.

### Blueprint에서 테스트

Blueprint에서 라이브러리 셀을 사용하는 계약을 테스트하려면 참조된 셀을 blueprint 에뮬레이터의 라이브러리 컨텍스트에 수동으로 추가해야 합니다. 다음과 같이 수행할 수 있습니다:

1. 라이브러리 컨텍스트 딕셔너리(해시맵) `uint256->Cell`을 만들어야 합니다. 여기서 `uint256`은 해당 셀의 해시입니다.
2. 에뮬레이터 설정에 라이브러리 컨텍스트를 설치합니다.

[여기](https://github.com/ton-blockchain/stablecoin-contract/blob/de08b905214eb253d27009db6a124fd1feadbf72/sandbox_tests/JettonWallet.spec.ts#L100C9-L103C32)에서 수행 방법의 예제를 볼 수 있습니다.

:::info
현재 blueprint 버전(`@ton/blueprint:0.19.0`)은 에뮬레이션 중에 일부 계약이 새 라이브러리를 게시할 경우 라이브러리 컨텍스트를 자동으로 업데이트하지 않으며, 수동으로 수행해야 합니다.
2024년 4월 현재 기준이며 가까운 미래에 개선될 예정입니다.
:::

### 라이브러리 셀 기반 계약의 Get 메서드

라이브러리 셀에 저장된 코드를 가진 제톤-월렛이 있고 잔액을 확인하고 싶습니다.

잔액을 확인하려면 코드에서 get 메서드를 실행해야 합니다. 이는 다음을 포함합니다:

- 라이브러리 셀 접근
- 참조된 셀의 해시 검색
- 마스터체인의 라이브러리 컬렉션에서 해당 해시를 가진 셀 찾기
- 해당 코드 실행

계층화된 솔루션(LS)에서는 이 모든 프로세스가 사용자가 특정 코드 저장 방법을 알 필요 없이 백그라운드에서 발생합니다.

하지만 로컬에서 작업할 때는 다릅니다. 예를 들어, 탐색기나 지갑을 사용할 때 계정 상태를 가져와서 NFT, 지갑, 토큰 또는 경매 등 그 유형을 확인하려고 할 수 있습니다.

일반 계약의 경우 사용 가능한 get 메서드, 즉 인터페이스를 살펴보고 이해할 수 있습니다. 또는 계정 상태를 로컬 의사 네트워크로 "가져와서" 거기서 메서드를 실행할 수 있습니다.

라이브러리 셀의 경우, 자체 데이터를 포함하지 않기 때문에 이것이 불가능합니다. 컨텍스트에서 필요한 셀을 수동으로 감지하고 검색해야 합니다. 이는 LS를 통해(바인딩이 아직 지원하지 않더라도) 또는 DTon을 통해 수행할 수 있습니다.

#### Liteserver로 라이브러리 셀 검색

Liteserver는 get 메서드를 실행할 때 자동으로 올바른 라이브러리 컨텍스트를 설정합니다. get 메서드로 계약 유형을 감지하거나 로컬에서 getmethods를 실행하려면 LS 메서드 [liteServer.getLibraries](https://github.com/ton-blockchain/ton/blob/4cfe1d1a96acf956e28e2bbc696a143489e23631/tl/generate/scheme/lite_api.tl#L96)를 통해 해당 셀을 다운로드해야 합니다.

#### DTon으로 라이브러리 셀 검색

[dton.io/graphql](https://dton.io/graphql)에서도 라이브러리를 가져올 수 있습니다:

```
{
  get_lib(
    lib_hash: "<HASH>"
  )
}
```

또한 특정 마스터체인 블록의 라이브러리 목록:

```
{
  blocks{
    libs_publishers
    libs_hash
  }
}
```

## 참고

- [이국적인 셀](/v3/documentation/data-formats/tlb/exotic-cells)
- [TVM 명령어](/v3/documentation/tvm/instructions)
