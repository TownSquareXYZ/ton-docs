# 난수 생성

난수 생성은 다양한 프로젝트에서 필요한 일반적인 작업입니다. FunC 문서에서 `random()` 함수를 이미 보셨을 수도 있지만, 추가적인 트릭을 사용하지 않는 한 그 결과를 쉽게 예측할 수 있다는 점에 유의하세요.

## 난수를 어떻게 예측할 수 있나요?

컴퓨터는 사용자의 지시를 따르기만 하기 때문에 무작위 정보를 생성하는 데는 서툴습니다. 하지만 사람들은 난수를 자주 필요로 하기 때문에 '의사 난수'를 생성하는 다양한 방법을 고안해냈습니다.

이러한 알고리즘은 일반적으로 일련의 _의사 난수_를 생성하는 데 사용할 *시드* 값을 제공해야 합니다. 따라서 동일한 _seed_로 동일한 프로그램을 여러 번 실행하면 지속적으로 동일한 결과를 얻을 수 있습니다. TON에서 _seed_는 각 블록마다 다릅니다.

- [블록 랜덤 시드 생성](/개발/스마트 컨트랙트/보안/랜덤)

따라서 스마트 콘트랙트에서 '랜덤()\` 함수의 결과를 예측하려면 블록의 현재 '시드'만 알면 되는데, 검증자가 아니라면 불가능합니다.

## 무작위화_lt()\`를 사용하면 됩니다.

난수 생성을 예측할 수 없게 하려면 현재 [논리적 시간](/개발/스마트 컨트랙트/가이드라인/메시지 전달 보장#논리적 시간)을 시드에 추가하면 트랜잭션마다 다른 시드와 결과를 갖게 됩니다.

난수를 생성하기 전에 `randomize_lt()` 호출을 추가하면 난수를 예측할 수 없게 됩니다:

```func
randomize_lt();
int x = random(); ;; users can't predict this number
```

그러나 유효성 검사기나 콜레이터는 현재 블록의 시드를 결정하므로 난수 결과에 여전히 영향을 미칠 수 있다는 점에 유의해야 합니다.

## 유효성 검사자의 조작으로부터 보호할 수 있는 방법이 있나요?

유효성 검사기에 의한 시드 대체를 방지하거나 최소한 복잡하게 만들려면 더 복잡한 방식을 사용할 수 있습니다. 예를 들어 난수를 생성하기 전에 한 블록을 건너뛸 수 있습니다. 한 블록을 건너뛰면 시드가 예측하기 어려운 방식으로 변경됩니다.

블록을 건너뛰는 것은 복잡한 작업이 아닙니다. 마스터체인으로 메시지를 보내고 다시 컨트랙트의 워크체인으로 메시지를 보내기만 하면 됩니다. 간단한 예를 살펴보겠습니다!

:::caution
실제 프로젝트에서는 이 예시 계약서를 사용하지 마시고 직접 작성하세요.
:::

### 모든 워크체인의 메인 컨트랙트

간단한 복권 계약을 예로 들어보겠습니다. 사용자가 1톤을 보내면 50%의 확률로 2톤을 돌려받게 됩니다.

```func
;; set the echo-contract address
const echo_address = "Ef8Nb7157K5bVxNKAvIWreRcF0RcUlzcCA7lwmewWVNtqM3s"a;

() recv_internal (int msg_value, cell in_msg_full, slice in_msg_body) impure {
    var cs = in_msg_full.begin_parse();
    var flags = cs~load_uint(4);
    if (flags & 1) { ;; ignore bounced messages
        return ();
    }
    slice sender = cs~load_msg_addr();

    int op = in_msg_body~load_uint(32);
    if ((op == 0) & equal_slice_bits(in_msg_body, "bet")) { ;; bet from user
        throw_unless(501, msg_value == 1000000000); ;; 1 TON

        send_raw_message(
            begin_cell()
                .store_uint(0x18, 6)
                .store_slice(echo_address)
                .store_coins(0)
                .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; default message headers (see sending messages page)
                .store_uint(1, 32) ;; let 1 be echo opcode in our contract
                .store_slice(sender) ;; forward user address
            .end_cell(),
            64 ;; send the remaining value of an incoming msg
        );
    }
    elseif (op == 1) { ;; echo
        throw_unless(502, equal_slice_bits(sender, echo_address)); ;; only accept echoes from our echo-contract

        slice user = in_msg_body~load_msg_addr();

        {-
            at this point we have skipped 1+ blocks
            so let's just generate the random number
        -}
        randomize_lt();
        int x = rand(2); ;; generate a random number (either 0 or 1)
        if (x == 1) { ;; user won
            send_raw_message(
                begin_cell()
                    .store_uint(0x18, 6)
                    .store_slice(user)
                    .store_coins(2000000000) ;; 2 TON
                    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; default message headers (see sending messages page)
                .end_cell(),
                3 ;; ignore errors & pay fees separately
            );
        }
    }
}
```

이 컨트랙트를 필요한 모든 워크체인(아마도 베이스체인)에 배포하면 완료됩니다!

## 이 방법은 100% 안전한가요?

물론 도움이 되긴 하지만, 침입자가 여러 검증자를 동시에 제어할 수 있는 경우 조작의 가능성이 여전히 존재합니다. 이 경우, 어느 정도 확률로 난수가 의존하는 _seed_에 [영향](/개발/스마트계약/보안/랜덤#결론)을 줄 수 있습니다. 이 확률이 극히 적더라도 고려할 가치가 있습니다.

최신 TVM 업그레이드를 통해 `c7` 레지스터에 새로운 값을 도입하면 난수 생성의 보안을 더욱 강화할 수 있습니다. 특히, 이번 업그레이드는 마지막 16개의 마스터체인 블록에 대한 정보를 `c7` 레지스터에 추가합니다.

마스터체인 블록 정보는 끊임없이 변화하는 특성으로 인해 난수 생성을 위한 엔트로피의 추가 소스로 사용될 수 있습니다. 이 데이터를 무작위성 알고리즘에 통합하면 잠재적인 공격자가 예측하기 어려운 숫자를 생성할 수 있습니다.

이번 TVM 업그레이드에 대한 자세한 내용은 [TVM 업그레이드](/learn/tvm-instructions/tvm-upgrade-2023-07)를 참조하세요.
