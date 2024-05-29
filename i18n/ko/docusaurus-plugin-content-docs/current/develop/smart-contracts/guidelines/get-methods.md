# 메서드 가져오기

:::note
계속 진행하기 전에 TON 블록체인의 [FunC 프로그래밍 언어](/develop/func/overview) 및 [스마트 컨트랙트 개발](/develop/smart-contracts)에 대한 기본적인 이해가 있는 독자를 권장합니다. 이렇게 하면 여기서 제공하는 정보를 보다 효과적으로 파악하는 데 도움이 될 것입니다.
:::

## 소개

Get 메서드는 스마트 콘트랙트에서 특정 데이터를 쿼리하기 위해 만들어진 특수 함수입니다. 이 메서드의 실행은 수수료가 들지 않으며 블록체인 외부에서 이루어집니다.

이러한 함수는 대부분의 스마트 컨트랙트에서 매우 일반적입니다. 예를 들어, 기본 [지갑 컨트랙트](/participate/wallets/contracts)에는 `seqno()`, `get_subwallet_id()` 및 `get_public_key()`와 같은 여러 가지 get 메서드가 있습니다. 지갑, SDK, API에서 지갑에 대한 데이터를 가져오는 데 사용됩니다.

## get 메서드에 대한 디자인 패턴

### 기본 get 메서드 디자인 패턴

1. **단일 데이터 포인트 검색**: 기본 디자인 패턴은 컨트랙트의 상태에서 개별 데이터 포인트를 반환하는 메서드를 만드는 것입니다. 이러한 메서드에는 매개변수가 없으며 단일 값을 반환합니다.

   예시:

   ```func
   int get_balance() method_id {
       return get_data().begin_parse().preload_uint(64);
   }
   ```

2. **통합 데이터 검색**: 또 다른 일반적인 패턴은 한 번의 호출로 컨트랙트 상태의 여러 데이터 포인트를 반환하는 메서드를 만드는 것입니다. 이는 특정 데이터 포인트가 일반적으로 함께 사용될 때 자주 사용됩니다. 이는 일반적으로 [제톤](#jettons) 및 [NFT](#nfts) 컨트랙트에서 사용됩니다.

   예시:

   ```func
   (int, slice, slice, cell) get_wallet_data() method_id {
       return load_data();
   }
   ```

### 고급 가져오기 메서드 디자인 패턴

1. **계산된 데이터 검색**: 경우에 따라 검색해야 하는 데이터가 컨트랙트의 상태에 직접 저장되지 않고 상태와 입력 인수를 기반으로 계산되는 경우도 있습니다.

   예시:

   ```func
   slice get_wallet_address(slice owner_address) method_id {
       (int total_supply, slice admin_address, cell content, cell jetton_wallet_code) = load_data();
       return calculate_user_jetton_wallet_address(owner_address, my_address(), jetton_wallet_code);
   }
   ```

2. **조건부 데이터 검색**: 검색해야 하는 데이터가 현재 시간과 같은 특정 조건에 따라 달라지는 경우가 있습니다.

   예시:

   ```func
   (int) get_ready_to_be_used() method_id {
       int ready? = now() >= 1686459600;
       return ready?;
   }
   ```

## 가장 일반적인 가져오기 방법

### 표준 지갑

#### seqno()

```func
int seqno() method_id {
    return get_data().begin_parse().preload_uint(32);
}
```

특정 지갑 내 트랜잭션의 시퀀스 번호를 반환합니다. 이 메서드는 주로 [리플레이 보호]에 사용됩니다(/개발/스마트 컨트랙트/자습서/지갑#리플레이 보호---seqno).

#### get_subwallet_id()

```func
int get_subwallet_id() method_id {
    return get_data().begin_parse().skip_bits(32).preload_uint(32);
}
```

- [지갑 ID란 무엇인가요?](/개발/스마트계약/자습서/지갑#서브월렛-ID란 무엇인가요?)

#### get_public_key()

```func
int get_public_key() method_id {
    var cs = get_data().begin_parse().skip_bits(64);
    return cs.preload_uint(256);
}
```

지갑과 연결된 공개 키를 검색합니다.

### Jettons

#### get_wallet_data()

```func
(int, slice, slice, cell) get_wallet_data() method_id {
    return load_data();
}
```

이 메서드는 제튼 지갑과 관련된 전체 데이터 집합을 반환합니다:

- (int) balance
- (슬라이스) 소유자_주소
- (슬라이스) 제튼_마스터_주소
- (셀) 제튼_월렛_코드

#### get_jetton_data()

```func
(int, int, slice, cell, cell) get_jetton_data() method_id {
    (int total_supply, slice admin_address, cell content, cell jetton_wallet_code) = load_data();
    return (total_supply, -1, admin_address, content, jetton_wallet_code);
}
```

총 공급량, 관리자 주소, 제트톤의 내용, 지갑 코드 등 제트톤 마스터의 데이터를 반환합니다.

#### get_wallet_address(슬라이스 소유자 주소)

```func
slice get_wallet_address(slice owner_address) method_id {
    (int total_supply, slice admin_address, cell content, cell jetton_wallet_code) = load_data();
    return calculate_user_jetton_wallet_address(owner_address, my_address(), jetton_wallet_code);
}
```

소유자의 주소가 주어지면 이 메서드는 소유자의 제튼 월렛 컨트랙트의 주소를 계산하여 반환합니다.

### NFT

#### get_nft_data()

```func
(int, int, slice, slice, cell) get_nft_data() method_id {
    (int init?, int index, slice collection_address, slice owner_address, cell content) = load_data();
    return (init?, index, collection_address, owner_address, content);
}
```

초기화 여부, 컬렉션 내 인덱스, 컬렉션의 주소, 소유자 주소, 개별 콘텐츠 등 대체 불가능한 토큰과 관련된 데이터를 반환합니다.

#### get_collection_data()

```func
(int, cell, slice) get_collection_data() method_id {
    var (owner_address, next_item_index, content, _, _) = load_data();
    slice cs = content.begin_parse();
    return (next_item_index, cs~load_ref(), owner_address);
}
```

다음 발행할 아이템의 인덱스, 컬렉션의 콘텐츠, 소유자 주소 등 NFT 컬렉션의 데이터를 반환합니다.

#### get_nft_address_by_index(int index)

```func
slice get_nft_address_by_index(int index) method_id {
    var (_, _, _, nft_item_code, _) = load_data();
    cell state_init = calculate_nft_item_state_init(index, nft_item_code);
    return calculate_nft_item_address(workchain(), state_init);
}
```

인덱스가 주어지면, 이 메서드는 이 컬렉션의 해당 NFT 아이템 컨트랙트의 주소를 계산하여 반환합니다.

#### 로열티_파라미터()

```func
(int, int, slice) royalty_params() method_id {
    var (_, _, _, _, royalty) = load_data();
    slice rs = royalty.begin_parse();
    return (rs~load_uint(16), rs~load_uint(16), rs~load_msg_addr());
}
```

NFT의 로열티 매개변수를 가져옵니다. 이러한 매개변수에는 NFT가 판매될 때마다 원래 크리에이터에게 지급되는 로열티 비율이 포함됩니다.

#### get_nft_content(int index, cell individual_nft_content)

```func
cell get_nft_content(int index, cell individual_nft_content) method_id {
    var (_, _, content, _, _) = load_data();
    slice cs = content.begin_parse();
    cs~load_ref();
    slice common_content = cs~load_ref().begin_parse();
    return (begin_cell()
            .store_uint(1, 8) ;; offchain tag
            .store_slice(common_content)
            .store_ref(individual_nft_content)
            .end_cell());
}
```

인덱스와 [개별 NFT 콘텐츠](#get_nft_data)가 주어지면, 이 메서드는 NFT의 공통 콘텐츠와 개별 콘텐츠를 결합하여 반환합니다.

## get 메서드로 작업하는 방법

### 인기 탐색기에서 get 메서드 호출하기

#### 톤뷰어

페이지 하단의 '메소드' 탭에서 get 메소드를 호출할 수 있습니다.

- https://tonviewer.com/EQAWrNGl875lXA6Fff7nIOwTIYuwiJMq0SmtJ5Txhgnz4tXI?section=Methods

#### Ton.cx

'메서드 가져오기' 탭에서 메서드를 호출할 수 있습니다.

- https://ton.cx/address/EQAWrNGl875lXA6Fff7nIOwTIYuwiJMq0SmtJ5Txhgnz4tXI

### 코드에서 get 메서드 호출하기

아래 예제에서는 자바스크립트 라이브러리와 도구를 사용하겠습니다:

- [ton](https://github.com/ton-core/ton) 라이브러리
- [블루프린트](/개발/스마트-계약/sdk/자바스크립트) SDK

다음과 같은 get 메서드를 사용하는 컨트랙트가 있다고 가정해 보겠습니다:

```func
(int) get_total() method_id {
    return get_data().begin_parse().preload_uint(32); ;; load and return the 32-bit number from the data
}
```

이 메서드는 컨트랙트 데이터에서 로드된 단일 숫자를 반환합니다.

아래 코드 스니펫은 알려진 주소에 배포된 일부 컨트랙트에서 이 get 메서드를 호출하는 데 사용할 수 있습니다:

```ts
import { Address, TonClient } from 'ton';

async function main() {
    // Create Client
    const client = new TonClient({
        endpoint: 'https://toncenter.com/api/v2/jsonRPC',
    });

    // Call get method
    const result = await client.runMethod(
        Address.parse('EQD4eA1SdQOivBbTczzElFmfiKu4SXNL4S29TReQwzzr_70k'),
        'get_total'
    );
    const total = result.stack.readNumber();
    console.log('Total:', total);
}

main();
```

이 코드는 '합계: 123'을 출력합니다. 숫자는 다를 수 있으며 이는 예시일 뿐입니다.

### get 메서드 테스트

생성된 스마트 컨트랙트를 테스트하려면 새 블루프린트 프로젝트에 기본적으로 설치되는 [샌드박스](https://github.com/ton-community/sandbox)를 사용할 수 있습니다.

먼저 컨트랙트 래퍼에 get 메서드를 실행하고 입력한 결과를 반환하는 특수 메서드를 추가해야 합니다. 컨트랙트의 이름이 _Counter_이고 저장된 숫자를 업데이트하는 메서드를 이미 구현했다고 가정해 보겠습니다. wrappers/Counter.ts\`를 열고 다음 메서드를 추가합니다:

```ts
async getTotal(provider: ContractProvider) {
    const result = (await provider.get('get_total', [])).stack;
    return result.readNumber();
}
```

get 메서드를 실행하고 결과 스택을 가져옵니다. get 메서드의 경우 스택은 기본적으로 반환된 값입니다. 이 스니펫에서는 스택에서 하나의 숫자를 읽었습니다. 한 번에 여러 값을 반환하는 더 복잡한 경우에는 `readSomething` 유형의 메서드를 여러 번 호출하여 스택에서 전체 실행 결과를 파싱할 수 있습니다.

마지막으로 이 메서드를 테스트에 사용할 수 있습니다. 'tests/Counter.spec.ts'로 이동하여 새 테스트를 추가합니다:

```ts
it('should return correct number from get method', async () => {
    const caller = await blockchain.treasury('caller');
    await counter.sendNumber(caller.getSender(), toNano('0.01'), 123);
    expect(await counter.getTotal()).toEqual(123);
});
```

터미널에서 'npx 청사진 테스트'를 실행하여 확인하고 모든 것을 올바르게 수행했다면 이 테스트는 통과로 표시되어야 합니다!

## 다른 컨트랙트에서 get 메서드 호출하기

직관적으로 보이는 것과는 달리, 블록체인 기술의 특성과 합의의 필요성으로 인해 다른 컨트랙트에서 가져오는 메서드를 호출하는 것은 온체인에서는 불가능합니다.

첫째, 다른 샤드체인에서 데이터를 가져오는 데는 시간이 필요할 수 있습니다. 블록체인 작업은 결정적이고 적시에 실행되어야 하므로 이러한 지연 시간은 컨트랙트 실행 흐름을 쉽게 방해할 수 있습니다.

둘째, 검증자 간의 합의를 달성하는 것은 문제가 될 수 있습니다. 검증자가 트랜잭션의 정확성을 검증하기 위해서는 동일한 get 메서드를 호출해야 합니다. 그러나 이렇게 여러 번 호출하는 사이에 대상 컨트랙트의 상태가 변경되면 검증자는 서로 다른 버전의 트랜잭션 결과를 얻게 될 수 있습니다.

마지막으로, TON의 스마트 컨트랙트는 순수 함수형으로 설계되어 동일한 입력에 대해 항상 동일한 출력을 생성합니다. 이 원칙은 메시지 처리 중에 간단한 합의를 가능하게 합니다. 동적으로 변하는 임의의 데이터를 런타임에 수집하는 기능을 도입하면 이 결정론적 속성이 깨지게 됩니다.

### 개발자를 위한 시사점

이러한 제한은 한 콘트랙트가 가져오는 메서드를 통해 다른 콘트랙트의 상태에 직접 접근할 수 없음을 의미합니다. 컨트랙트의 결정론적 흐름에 실시간 외부 데이터를 통합할 수 없다는 것은 제한적으로 보일 수 있습니다. 하지만 바로 이러한 제약이 블록체인 기술의 무결성과 신뢰성을 보장합니다.

### 솔루션 및 해결 방법

톤 블록체인에서 스마트 컨트랙트는 다른 컨트랙트의 메소드를 직접 호출하는 대신 메시지를 통해 통신합니다. 특정 메서드의 실행을 요청하는 메시지를 대상 컨트랙트에 전송할 수 있습니다. 이러한 요청은 일반적으로 특별한 [작업 코드](/개발/스마트 컨트랙트/가이드라인/내부 메시지)로 시작됩니다.

이러한 요청을 수락하도록 설계된 컨트랙트는 원하는 방법을 실행하고 결과를 별도의 메시지로 다시 전송합니다. 이는 복잡해 보일 수 있지만, 실제로는 컨트랙트 간의 통신을 간소화하고 블록체인 네트워크의 확장성과 성능을 향상시킵니다.

이 메시지 전달 메커니즘은 TON 블록체인의 운영에 필수적인 요소로, 샤드 간의 광범위한 동기화 없이도 확장 가능한 네트워크 성장을 위한 기반을 마련합니다.

효과적인 컨트랙트 간 커뮤니케이션을 위해서는 요청을 올바르게 수락하고 응답하도록 컨트랙트를 설계하는 것이 중요합니다. 여기에는 온체인에서 호출하여 응답을 반환할 수 있는 메서드를 지정하는 것이 포함됩니다.

간단한 예를 들어 보겠습니다:

```func
#include "imports/stdlib.fc";

int get_total() method_id {
    return get_data().begin_parse().preload_uint(32);
}

() recv_internal(int my_balance, int msg_value, cell in_msg_full, slice in_msg_body) impure {
    if (in_msg_body.slice_bits() < 32) {
        return ();
    }

    slice cs = in_msg_full.begin_parse();
    cs~skip_bits(4);
    slice sender = cs~load_msg_addr();

    int op = in_msg_body~load_uint(32); ;; load the operation code

    if (op == 1) { ;; increase and update the number
        int number = in_msg_body~load_uint(32);
        int total = get_total();
        total += number;
        set_data(begin_cell().store_uint(total, 32).end_cell());
    }
    elseif (op == 2) { ;; query the number
        int total = get_total();
        send_raw_message(begin_cell()
            .store_uint(0x18, 6)
            .store_slice(sender)
            .store_coins(0)
            .store_uint(0, 107) ;; default message headers (see sending messages page)
            .store_uint(3, 32) ;; response operation code
            .store_uint(total, 32) ;; the requested number
        .end_cell(), 64);
    }
}
```

이 예시에서 컨트랙트는 연산 코드를 해석하고, 특정 메서드를 실행하고, 적절하게 응답을 반환하여 내부 메시지를 수신하고 처리합니다:

- 연산 코드 `1`은 컨트랙트 데이터의 번호를 업데이트하라는 요청을 나타냅니다.
- 연산 코드 `2`는 컨트랙트 데이터에서 번호를 쿼리하라는 요청을 의미합니다.
- 오퍼 코드 `3`은 응답 메시지에 사용되며, 호출하는 스마트 컨트랙트가 결과를 받기 위해 처리해야 합니다.

간단하게 하기 위해 작업 코드에 숫자 1, 2, 3만 사용했습니다. 하지만 실제 프로젝트에서는 표준에 따라 설정하는 것이 좋습니다:

- [연산 코드용 CRC32 해시](/개발/데이터-포맷/crc32)

## 일반적인 함정과 이를 피하는 방법

1. **get 메서드의 오용**: 앞서 언급했듯이 get 메서드는 컨트랙트 상태의 데이터를 반환하도록 설계되었으며, 컨트랙트 상태를 변경하는 용도로 사용되지 않습니다. get 메서드 내에서 컨트랙트의 상태를 변경하려고 시도하면 실제로 변경되지 않습니다.

2. **반환 유형 무시**: 모든 get 메서드에는 검색되는 데이터와 일치하는 반환 유형이 명확하게 정의되어 있어야 합니다. 메서드가 특정 유형의 데이터를 반환할 것으로 예상되는 경우, 메서드 내의 모든 경로가 이 유형을 반환하는지 확인하세요. 일관되지 않은 반환 유형을 사용하면 컨트랙트와 상호 작용할 때 오류와 어려움이 발생할 수 있으므로 사용하지 마세요.

3. **컨트랙트 간 호출 가정**: 흔히 오해하는 것은 온체인에서 다른 컨트랙트에서 get 메서드를 호출할 수 있다는 것입니다. 그러나 앞서 설명한 것처럼 블록체인 기술의 특성과 합의의 필요성으로 인해 이는 불가능합니다. get 메서드는 오프체인에서 사용하도록 설계되었으며, 컨트랙트 간의 온체인 상호작용은 내부 메시지를 통해 이루어진다는 점을 항상 기억하시기 바랍니다.

## 결론

Get 메서드는 TON 블록체인의 스마트 컨트랙트에서 데이터를 쿼리하는 데 필수적인 도구입니다. 제한 사항이 있지만, 이러한 제한 사항을 이해하고 이를 해결하는 방법을 아는 것은 스마트 컨트랙트에서 get 메서드를 효과적으로 사용하기 위한 핵심입니다.
