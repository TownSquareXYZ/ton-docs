# 블록 랜덤 시드 생성

:::caution
이 정보는 작성 시점 기준으로 최신입니다. 네트워크 업그레이드 시 변경될 수 있습니다.
:::

TON에서는 가끔 복권 컨트랙트가 생성됩니다. 보통 안전하지 않은 방식으로 무작위성을 처리하므로, 생성된 값을 사용자가 예측할 수 있어 복권이 고갈될 수 있습니다.

하지만 무작위 숫자 생성의 취약점을 이용하는 것은 보통 무작위 값이 올바른 경우 메시지를 전달하는 프록시 컨트랙트를 사용하는 것을 포함합니다. 온체인에서 임의의 코드(물론 사용자가 지정하고 서명한)를 실행할 수 있는 지갑 컨트랙트에 대한 제안이 있지만, 가장 인기 있는 지갑 버전은 이를 지원하지 않습니다. 그렇다면 복권이 도박꾼이 지갑 컨트랙트를 통해 참여하는지 확인하는 경우 안전할까요?

또는 이 질문은 다음과 같이 작성될 수 있습니다. 무작위 값이 발신자가 필요로 하는 것과 정확히 일치하는 블록에 외부 메시지가 포함될 수 있나요?

물론 발신자는 무작위성에 어떤 식으로든 영향을 미치지 않습니다. 하지만 블록을 생성하고 제안된 외부 메시지를 포함하는 검증자는 영향을 미칩니다.

## 검증자가 시드에 미치는 영향

[TON 백서](https://docs.ton.org/ton.pdf)에도 블록 무작위성에 대한 정보가 많지 않아 대부분의 개발자가 혼란스러워합니다. 다음이 블록 무작위성에 대한 유일한 언급입니다:

> 각 샤드(w, s)에 대한 검증자 태스크 그룹을 선택하는 데 사용되는 알고리즘은 결정적 의사 무작위입니다. **검증자가 각 마스터체인 블록에 임베드한 의사 무작위 숫자(임계값 서명을 사용하여 합의로 생성됨)를 사용하여 무작위 시드를 생성하고**, 그런 다음 각 검증자에 대해 예를 들어 Hash(code(w). code(s).validator_id.rand_seed)를 계산합니다.

하지만 진실되고 최신임이 보장된 유일한 것은 코드입니다. 그러니 [collator.cpp](https://github.com/ton-blockchain/ton/blob/f59c363ab942a5ddcacd670c97c6fbd023007799/validator/impl/collator.cpp#L1590)를 살펴보겠습니다:

```cpp
  {
    // generate rand seed
    prng::rand_gen().strong_rand_bytes(rand_seed->data(), 32);
    LOG(DEBUG) << "block random seed set to " << rand_seed->to_hex();
  }
```

이것은 블록의 무작위 시드를 생성하는 코드입니다. 이는 블록을 생성하는 당사자에 의해 필요하기 때문에 collator 코드에 있습니다(lite 검증자에게는 필요하지 않음).

보시다시피 시드는 단일 검증자나 collator가 블록과 함께 생성합니다. 다음 질문은:

## 시드를 알고 난 후에 외부 메시지 포함에 대한 결정을 내릴 수 있나요?

네, 가능합니다. 증명은 다음과 같습니다: 외부 메시지가 가져와지면 실행이 성공적이어야 합니다. 실행은 무작위 값에 의존할 수 있으므로 블록 시드는 미리 알려져 있어야 합니다.

따라서 발신자가 검증자와 협력할 수 있다면 "안전하지 않은"(메시지를 보낸 후 블록의 정보를 사용하지 않기 때문에 single-block이라고 부르겠습니다) 무작위를 해킹할 방법이 **있습니다**. `randomize_lt()`가 사용되더라도 마찬가지입니다. 검증자는 발신자에게 적합한 시드를 생성하거나 모든 조건을 만족하는 블록에 제안된 외부 메시지를 포함할 수 있습니다. 이렇게 하는 검증자도 여전히 공정한 것으로 간주됩니다. 이것이 탈중앙화의 본질입니다.

그리고 이 글이 무작위성을 완전히 다루기 위해 한 가지 질문이 더 있습니다.

## 블록 시드는 컨트랙트의 무작위성에 어떤 영향을 미치나요?

검증자가 생성한 시드는 모든 컨트랙트에서 직접 사용되지 않습니다. 대신 [계정 주소와 해시](https://github.com/ton-blockchain/ton/blob/f59c363ab942a5ddcacd670c97c6fbd023007799/crypto/block/transaction.cpp#L876)됩니다.

```cpp
bool Transaction::prepare_rand_seed(td::BitArray<256>& rand_seed, const ComputePhaseConfig& cfg) const {
  // we might use SHA256(block_rand_seed . addr . trans_lt)
  // instead, we use SHA256(block_rand_seed . addr)
  // if the smart contract wants to randomize further, it can use RANDOMIZE instruction
  td::BitArray<256 + 256> data;
  data.bits().copy_from(cfg.block_rand_seed.cbits(), 256);
  (data.bits() + 256).copy_from(account.addr_rewrite.cbits(), 256);
  rand_seed.clear();
  data.compute_sha256(rand_seed);
  return true;
}
```

그런 다음 [TVM 명령어](/v3/documentation/tvm/instructions#F810) 페이지에 설명된 절차에 따라 의사 무작위 숫자가 생성됩니다:

> **x\{F810} RANDU256**\
> 새로운 의사 무작위 부호 없는 256비트 정수 x를 생성합니다. 알고리즘은 다음과 같습니다: r이 무작위 시드의 이전 값이고 32바이트 배열로 간주되면(부호 없는 256비트 정수의 빅엔디안 표현을 구성함), sha512(r)이 계산됩니다; 이 해시의 첫 32바이트는 무작위 시드의 새 값 r'로 저장되고, 나머지 32바이트는 다음 무작위 값 x로 반환됩니다.

우리는 [컨트랙트의 c7 준비](https://github.com/ton-blockchain/ton/blob/master/crypto/block/transaction.cpp#L903)(c7은 컨트랙트 주소, 시작 잔액, 무작위 시드 등을 저장하는 임시 데이터용 튜플)와 [무작위 값 자체의 생성](https://github.com/ton-blockchain/ton/blob/master/crypto/vm/tonops.cpp#L217-L268)의 코드를 보고 이를 확인할 수 있습니다.

## 결론

TON의 어떤 무작위성도 예측 불가능성 측면에서 완전히 안전하지 않습니다. 이는 **여기서는 완벽한 복권이 존재할 수 없으며**, 어떤 복권도 공정하다고 믿을 수 없다는 것을 의미합니다.

PRNG의 일반적인 사용에는 `randomize_lt()`가 포함될 수 있지만, 이러한 컨트랙트에 메시지를 보내기 위해 올바른 블록을 선택함으로써 속일 수 있습니다. 이에 대한 제안된 해결책은 다른 workchain으로 메시지를 보내고, 응답을 받아 블록을 건너뛰는 등입니다... 하지만 이는 단지 위협을 미룰 뿐입니다. 실제로 어떤 검증자든(즉, TON 블록체인의 1/250) 복권 컨트랙트에 요청을 보내는 올바른 시간을 선택하여 다른 workchain의 응답이 자신이 생성한 블록에 도착하게 할 수 있으며, 그러면 원하는 블록 시드를 자유롭게 선택할 수 있습니다. collator가 메인넷에 등장하면 위험은 더 커질 것입니다. 왜냐하면 이들은 Elector 컨트랙트에 어떤 스테이크도 넣지 않기 때문에 표준 불만사항으로 벌금을 부과할 수 없기 때문입니다.

<!-- TODO: find an example contract using random without any additions, show how to find result of RANDU256 knowing block random seed (implies link on dton.io to show generated value) -->

<!-- TODO: next article. "Let's proceed to writing tool that will exploit this. It will be attached to validator and put proposed external messages in blocks satisfying some conditions - provided some fee is paid." -->
