# 블록 랜덤 시드 생성

:::caution
이 정보는 작성 시점의 최신 정보입니다. 네트워크 업그레이드 시 변경될 수 있습니다.
:::

가끔씩 TON에서 추첨 컨트랙트가 생성됩니다. 일반적으로 무작위성을 처리하는 안전하지 않은 방법을 사용하므로 사용자가 생성된 값을 예측하고 복권을 소진할 수 있습니다.

그러나 난수 생성의 약점을 악용하기 위해서는 난수 값이 올바른지 메시지를 전달하는 프록시 콘트랙트를 사용하는 경우가 많습니다. 물론 사용자가 지정하고 서명한 임의의 코드를 온체인에서 실행할 수 있는 지갑 콘트랙트에 대한 제안이 존재하지만, 대부분의 대중적인 지갑 버전은 이를 지원하지 않습니다. 그렇다면 겜블러가 지갑 컨트랙트를 통해 참여 여부를 확인한다면 안전한가요?

또는 이 질문은 다음과 같이 작성할 수 있습니다. 발신자가 필요로 하는 임의의 값을 블록에 포함시킬 수 있나요?

물론 발신자는 어떤 방식으로든 무작위성에 영향을 미치지 않습니다. 하지만 블록을 생성하고 제안된 외부 메시지를 포함하는 유효성 검사기는 영향을 미칩니다.

## 유효성 검사기가 시드에 미치는 영향

백서에도 이에 대한 정보가 많지 않아 대부분의 개발자가 혼란스러워합니다. 블록 랜덤에 대한 유일한 언급은 [TON 백서](https://docs.ton.org/ton.pdf)에서 확인할 수 있습니다:

> 각 샤드(w, s)에 대한 검증자 작업 그룹을 선택하는 데 사용되는 알고리즘은 결정론적 의사 난수입니다. **검증자가 각 마스터체인 블록에 삽입한 의사 난수(임계값 서명을 사용한 합의에 의해 생성됨)를 사용하여 무작위 시드**를 생성한 다음, 각 검증자에 대해 해시(코드(w). 코드(s).검증자_id.rand_seed) 등을 계산합니다.

그러나 진실성과 최신성을 보장하는 유일한 것은 코드뿐입니다. 그럼 [collator.cpp](https://github.com/ton-blockchain/ton/blob/f59c363ab942a5ddcacd670c97c6fbd023007799/validator/impl/collator.cpp#L1590)를 살펴봅시다:

```cpp
  {
    // generate rand seed
    prng::rand_gen().strong_rand_bytes(rand_seed->data(), 32);
    LOG(DEBUG) << "block random seed set to " << rand_seed->to_hex();
  }
```

블록의 무작위 시드를 생성하는 코드입니다. 블록을 생성하는 당사자에게 필요하기 때문에 콜레이터 코드에 있습니다(라이트 검증자에는 필요하지 않음).

보시다시피, 시드는 단일 검증자 또는 콜레이터에 의해 블록으로 생성됩니다. 다음 질문은

## 시드가 알려진 후에 외부 메시지 포함 여부를 결정할 수 있나요?

네, 가능합니다. 외부 메시지를 가져온 경우 실행이 성공해야 한다는 증거는 다음과 같습니다. 실행은 임의의 값에 따라 달라질 수 있으므로 블록 시드를 미리 알 수 있어야 합니다.

따라서 발신자가 검증자와 협력할 수 있다면 "안전하지 않은"(메시지를 보낸 후 블록의 정보를 사용하지 않으므로 단일 블록이라고 부르겠습니다) 무작위로 해킹하는 방법은 **있다**고 할 수 있습니다. 랜덤라이즈_엘티()\`를 사용하더라도 마찬가지입니다. 검증자는 발신자에게 적합한 시드를 생성하거나 모든 조건을 만족하는 외부 제안 메시지를 블록에 포함할 수 있습니다. 이렇게 하는 검증자는 여전히 공정한 것으로 간주됩니다. 이것이 탈중앙화의 본질입니다.

그리고 이 글에서 무작위성을 충분히 다루기 위해 질문이 하나 더 있습니다.

## 블록 시드는 컨트랙트에서 무작위성에 어떤 영향을 미치나요?

검증자가 생성한 시드는 모든 컨트랙트에서 직접 사용되지는 않습니다. 대신 [계정 주소로 해시]됩니다(https://github.com/ton-blockchain/ton/blob/f59c363ab942a5ddcacd670c97c6fbd023007799/crypto/block/transaction.cpp#L876).

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

그런 다음 [TVM 지침](/학습/tvm-지침/지침#112-의사 난수 생성기 프리미티브) 페이지에 설명된 절차에 따라 의사 난수를 생성합니다:

> **x{F810} RANDU256**\
> 새로운 의사 랜덤 부호 없는 256비트 정수 x를 생성합니다. 알고리즘은 다음과 같습니다: r이 32바이트 배열로 간주되는 랜덤 시드의 이전 값인 경우(부호 없는 256비트 정수의 빅 엔디안 표현을 구성하여), 그 sha512(r)를 계산하고 이 해시의 첫 32바이트는 랜덤 시드의 새 값 r' 로 저장되며 나머지 32바이트는 다음 랜덤 값 x로 반환합니다.

컨트랙트의 c7 준비](https://github.com/ton-blockchain/ton/blob/master/crypto/block/transaction.cpp#L903)(c7은 임시 데이터의 튜플이며, 컨트랙트 주소, 시작 잔액, 랜덤 시드 등을 저장합니다)와 [랜덤 값 자체 생성](https://github.com/ton-blockchain/ton/blob/master/crypto/vm/tonops.cpp#L217-L268) 코드를 살펴보면 이를 확인할 수 있습니다.

## 결론

예측 불가능성이라는 점에서 TON의 랜덤은 완전히 안전하지 않습니다. 즉, **완벽한 복권은 존재할 수 없으며**, 어떤 복권도 공정하다고 믿을 수 없습니다.

PRNG의 일반적인 사용법에는 `randomize_lt()`가 포함될 수 있지만, 올바른 블록을 선택하여 메시지를 보내면 이러한 컨트랙트를 속일 수 있습니다. 이에 대한 해결책으로 제안된 것은 다른 워크체인에 메시지를 보내고, 응답을 받아 블록을 건너뛰는 것 등이 있지만, 이는 위협을 미루는 것일 뿐입니다. 실제로 모든 검증자(즉, TON 블록체인의 1/250)는 자신이 생성한 블록에 다른 워크체인의 응답이 도착하도록 추첨 계약에 요청을 보내는 정확한 시간을 선택할 수 있으며, 이후에는 자신이 원하는 블록 시드를 자유롭게 선택할 수 있습니다. 콜레이터가 메인넷에 등장하면 선거인 계약에 지분을 넣지 않기 때문에 일반적인 불만 제기로 벌금을 부과할 수 없기 때문에 위험은 더욱 커질 것입니다.

<!-- TODO: find an example contract using random without any additions, show how to find result of RANDU256 knowing block random seed (implies link on dton.io to show generated value) -->

<!-- TODO: next article. "Let's proceed to writing tool that will exploit this. It will be attached to validator and put proposed external messages in blocks satisfying some conditions - provided some fee is paid." -->
