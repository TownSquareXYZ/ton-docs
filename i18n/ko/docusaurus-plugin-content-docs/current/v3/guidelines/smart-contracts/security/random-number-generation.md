# 무작위 숫자 생성

무작위 숫자 생성은 많은 프로젝트에서 필요한 일반적인 작업입니다. FunC 문서에서 `random()` 함수를 이미 보셨을 수 있지만, 추가적인 기법을 사용하지 않으면 그 결과를 쉽게 예측할 수 있다는 점에 유의하세요.

## 어떻게 무작위 숫자를 예측할 수 있나요?

컴퓨터는 사용자의 지시를 따르기만 하기 때문에 무작위 정보 생성에 취약합니다. 하지만 사람들은 자주 무작위 숫자가 필요하기 때문에 *의사 무작위* 숫자를 생성하는 다양한 방법을 고안했습니다.

이러한 알고리즘은 일반적으로 *의사 무작위* 숫자 시퀀스를 생성하는 데 사용될 *시드* 값을 제공해야 합니다. 따라서 동일한 _시드_로 같은 프로그램을 여러 번 실행하면 항상 동일한 결과를 얻게 됩니다. TON에서는 각 블록마다 _시드_가 다릅니다.

- [블록 무작위 시드 생성](/v3/guidelines/smart-contracts/security/random)

따라서 스마트 컨트랙트의 `random()` 함수 결과를 예측하려면 블록의 현재 `시드`만 알면 됩니다. 검증자가 아니라면 이는 불가능합니다.

## 단순히 `randomize_lt()` 사용하기

무작위 숫자 생성을 예측할 수 없게 만들기 위해 현재 [논리적 시간](/v3/documentation/smart-contracts/message-management/messages-and-transactions#what-is-a-logical-time)을 시드에 추가할 수 있어서, 서로 다른 트랜잭션은 서로 다른 시드와 결과를 가지게 됩니다.

무작위 숫자를 생성하기 전에 `randomize_lt()` 호출만 추가하면 무작위 숫자가 예측 불가능해집니다:

```func
randomize_lt();
int x = random(); ;; users can't predict this number
```

하지만 검증자나 collator가 현재 블록의 시드를 결정하므로 여전히 무작위 숫자의 결과에 영향을 미칠 수 있다는 점에 유의해야 합니다.

## 검증자의 조작을 막는 방법이 있나요?

검증자에 의한 시드 대체를 방지(또는 최소한 복잡하게)하기 위해 더 복잡한 구성을 사용할 수 있습니다. 예를 들어 무작위 숫자를 생성하기 전에 한 블록을 건너뛸 수 있습니다. 블록을 건너뛰면 시드가 덜 예측 가능한 방식으로 변경됩니다.

블록을 건너뛰는 것은 복잡한 작업이 아닙니다. 단순히 마스터체인으로 메시지를 보내고 컨트랙트의 workchain으로 다시 보내면 됩니다. 간단한 예시를 살펴보겠습니다!

:::caution
이 예시 컨트랙트를 실제 프로젝트에서 사용하지 마시고, 대신 직접 작성하세요.
:::

### 모든 workchain의 메인 컨트랙트

예시로 간단한 복권 컨트랙트를 작성해보겠습니다. 사용자가 1 TON을 보내면 50% 확률로 2 TON을 돌려받습니다.

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

이 컨트랙트를 필요한 workchain(아마도 Basechain)에 배포하면 완료됩니다!

## 이 방법이 100% 안전한가요?

이는 분명히 도움이 되지만, 침입자가 여러 검증자를 동시에 제어할 수 있다면 여전히 조작 가능성이 있습니다. 이 경우 어느 정도 확률로 무작위 숫자가 의존하는 _시드_에 [영향](/v3/guidelines/smart-contracts/security/random#conclusion)을 미칠 수 있습니다. 이 확률이 매우 작더라도 고려할 가치가 있습니다.

최신 TVM 업그레이드에서는 `c7` 레지스터에 새 값을 도입하여 무작위 숫자 생성의 보안을 더욱 강화할 수 있습니다. 구체적으로 업그레이드는 마지막 16개의 마스터체인 블록에 대한 정보를 `c7` 레지스터에 추가합니다.

마스터체인 블록 정보는 지속적으로 변화하는 특성으로 인해 무작위 숫자 생성의 추가 엔트로피 소스로 사용될 수 있습니다. 이 데이터를 무작위성 알고리즘에 통합하면 잠재적 적대자가 예측하기 더 어려운 숫자를 만들 수 있습니다.

이 TVM 업그레이드에 대한 자세한 정보는 [TVM 업그레이드](/v3/documentation/tvm/changelog/tvm-upgrade-2023-07)를 참조하세요.
