# 내부 메시지

## 개요

스마트 컨트랙트는 **내부 메시지**라고 하는 것을 보내서 서로 상호작용합니다. 내부 메시지가 의도한 목적지에 도달하면, 해당 목적지 계정을 대신하여 일반적인 트랜잭션이 생성되고, 내부 메시지는 이 계정(스마트 컨트랙트)의 코드와 영구 데이터에 지정된 대로 처리됩니다.

:::info
특히, 처리 트랜잭션은 하나 또는 여러 개의 발신 내부 메시지를 생성할 수 있으며, 이 중 일부는 처리 중인 내부 메시지의 소스 주소로 전달될 수 있습니다. 이는 쿼리가 내부 메시지에 캡슐화되어 다른 스마트 컨트랙트로 전송되고, 해당 컨트랙트가 쿼리를 처리하여 다시 내부 메시지로 응답을 보내는 간단한 "클라이언트-서버 애플리케이션"을 만드는 데 사용될 수 있습니다.
:::

이 접근 방식은 내부 메시지가 "쿼리", "응답" 또는 추가 처리가 필요하지 않은 메시지("단순 자금 이체"와 같은)인지 구분해야 할 필요성으로 이어집니다. 또한 응답을 받았을 때, 어떤 쿼리에 해당하는지 이해할 수 있는 수단이 있어야 합니다.

이 목표를 달성하기 위해 다음과 같은 내부 메시지 레이아웃 접근 방식을 사용할 수 있습니다(TON 블록체인은 메시지 본문에 대한 제한을 강제하지 않으므로 이는 단지 권장사항일 뿐입니다).

### 내부 메시지 구조

메시지 본문은 메시지 자체에 포함되거나, 메시지에서 참조하는 별도의 셀에 저장될 수 있으며, 이는 TL-B 스키마 조각에 표시된 대로입니다:

```tlb
message$_ {X:Type} ... body:(Either X ^X) = Message X;
```

수신하는 스마트 컨트랙트는 최소한 메시지 본문이 포함된 내부 메시지(메시지를 포함하는 셀에 맞을 때마다)를 수락해야 합니다. 별도의 셀에서 메시지 본문을 수락하는 경우(`(Either X ^X)`의 `right` 생성자 사용), 수신 메시지의 처리는 메시지 본문에 대해 선택된 특정 임베딩 옵션에 의존하지 않아야 합니다. 반면에 더 단순한 쿼리와 응답의 경우 별도 셀의 메시지 본문을 전혀 지원하지 않는 것도 완벽하게 유효합니다.

### 내부 메시지 본문

메시지 본문은 일반적으로 다음 필드로 시작합니다:

```
* A 32-bit (big-endian) unsigned integer `op`, identifying the `operation` to be performed, or the `method` of the smart contract to be invoked.
* A 64-bit (big-endian) unsigned integer `query_id`, used in all query-response internal messages to indicate that a response is related to a query (the `query_id` of a response must be equal to the `query_id` of the corresponding query). If `op` is not a query-response method (e.g., it invokes a method that is not expected to send an answer), then `query_id` may be omitted.
* The remainder of the message body is specific for each supported value of `op`.
```

### 코멘트가 있는 단순 메시지

`op`가 0인 경우, 메시지는 "코멘트가 있는 단순 전송 메시지"입니다. 코멘트는 메시지 본문의 나머지 부분에 포함됩니다(`query_id` 필드 없이, 즉 다섯 번째 바이트부터 시작). `0xff` 바이트로 시작하지 않는 경우, 코멘트는 텍스트이며 지갑의 최종 사용자에게 "있는 그대로" 표시될 수 있습니다(잘못된 문자와 제어 문자를 필터링하고 유효한 UTF-8 문자열인지 확인한 후).

코멘트가 길어서 셀에 맞지 않을 때는 줄의 맞지 않는 끝 부분이 셀의 첫 번째 참조에 들어갑니다. 이 과정은 두 개 이상의 셀에 맞지 않는 코멘트를 설명하기 위해 재귀적으로 계속됩니다:

```
root_cell("0x00000000" - 32 bit, "string" up to 123 bytes)
         ↳1st_ref("string continuation" up to 127 bytes)
                 ↳1st_ref("string continuation" up to 127 bytes)
                         ↳....
```

동일한 형식이 NFT와 [jetton](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md#forward_payload-format) 전송의 코멘트에도 사용됩니다.

예를 들어, 사용자는 이 텍스트 필드에 다른 사용자의 지갑으로 단순 이체의 목적을 표시할 수 있습니다. 반면에, 코멘트가 `0xff` 바이트로 시작하면 나머지는 "이진 코멘트"이며, 최종 사용자에게 텍스트로 표시되지 않아야 합니다(필요한 경우 16진수 덤프로만 표시). "이진 코멘트"의 의도된 사용은 예를 들어, 상점의 소프트웨어에 의해 자동으로 생성되고 처리되는 상점 결제의 구매 식별자를 포함하는 것입니다.

대부분의 스마트 컨트랙트는 "단순 전송 메시지"를 받을 때 중요한 작업을 수행하거나 수신 메시지를 거부해서는 안 됩니다. 이런 방식으로, `op`가 0임이 확인되면 수신 내부 메시지를 처리하는 스마트 컨트랙트 함수(일반적으로 `recv_internal()`이라고 함)는 성공을 나타내는 0 종료 코드로 즉시 종료해야 합니다(예: 스마트 컨트랙트에 의해 사용자 정의 예외 처리기가 설치되지 않은 경우 예외 `0`을 발생시킴). 이는 추가적인 효과 없이 메시지로 전송된 값이 수신 계정에 입금되도록 합니다.

### 암호화된 코멘트가 있는 메시지

`op`가 `0x2167da4b`인 경우, 메시지는 "암호화된 코멘트가 있는 전송 메시지"입니다. 이 메시지는 다음과 같이 직렬화됩니다:

입력:

- `pub_1`과 `priv_1` - 발신자의 Ed25519 공개 키와 개인 키, 각각 32바이트
- `pub_2` - 수신자의 Ed25519 공개 키, 32바이트
- `msg` - 암호화할 메시지, 임의의 바이트 문자열. `len(msg) <= 960`

암호화 알고리즘은 다음과 같습니다:

1. `priv_1`과 `pub_2`를 사용하여 `shared_secret`를 계산합니다.
2. `salt`를 `isBounceable=1`과 `isTestnetOnly=0`를 가진 발신자 지갑 주소의 [bas64url 표현](/v3/documentation/smart-contracts/addresses#user-friendly-address)으로 합니다.
3. `len(prefix+msg)`가 16으로 나누어지도록 16에서 31 바이트 길이의 `prefix` 바이트 문자열을 선택합니다. `prefix`의 첫 번째 바이트는 `len(prefix)`와 같고, 다른 바이트는 무작위입니다. `data = prefix + msg`로 합니다.
4. `msg_key`를 `hmac_sha512(salt, data)`의 첫 16바이트로 합니다.
5. `x = hmac_sha512(shared_secret, msg_key)`를 계산합니다. `key=x[0:32]`와 `iv=x[32:48]`로 합니다.
6. `key`와 `iv`를 사용하여 CBC 모드의 AES-256으로 `data`를 암호화합니다.
7. 암호화된 코멘트를 다음과 같이 구성합니다:
   1. `pub_xor = pub_1 ^ pub_2` - 32바이트. 이를 통해 각 당사자는 상대방의 공개 키를 찾아보지 않고도 메시지를 복호화할 수 있습니다.
   2. `msg_key` - 16바이트.
   3. 암호화된 `data`.
8. 메시지 본문은 4바이트 태그 `0x2167da4b`로 시작합니다. 그런 다음 이 암호화된 코멘트가 저장됩니다:
   1. 바이트 문자열은 세그먼트로 나뉘어 셀 체인 `c_1,...,c_k`에 저장됩니다(`c_1`은 본문의 루트). 각 셀(마지막 셀 제외)은 다음 셀에 대한 참조를 갖습니다.
   2. `c_1`은 최대 35바이트를 포함하고(4바이트 태그 제외), 다른 모든 셀은 최대 127바이트를 포함합니다.
   3. 이 형식은 다음과 같은 제한이 있습니다: `k <= 16`, 최대 문자열 길이는 1024입니다.

동일한 형식이 NFT와 jetton 전송의 코멘트에도 사용되며, 발신자 주소와 수신자 주소(jetton-지갑 주소가 아님)의 공개 키가 사용되어야 합니다.

:::info
Learn from examples of the message encryption algorithm:

- [encryption.js](https://github.com/toncenter/ton-wallet/blob/master/src/js/util/encryption.js)
- [SimpleEncryption.cpp](https://github.com/ton-blockchain/ton/blob/master/tonlib/tonlib/keys/SimpleEncryption.cpp)
  :::

### 코멘트 없는 단순 전송 메시지

"코멘트 없는 단순 전송 메시지"는 빈 본문을 가집니다(`op` 필드조차 없음). 위의 고려사항들이 이러한 메시지에도 적용됩니다. 이러한 메시지는 메시지 셀에 본문이 포함되어야 합니다.

### 쿼리와 응답 메시지의 구분

"쿼리" 메시지는 최상위 비트가 0인 `op`를 가져야 합니다(즉, `1 .. 2^31-1` 범위에서), "응답" 메시지는 최상위 비트가 1인 `op`를 가져야 합니다(즉, `2^31 .. 2^32-1` 범위에서). 메서드가 쿼리도 응답도 아닌 경우(따라서 해당 메시지 본문에 `query_id` 필드가 포함되지 않음), "쿼리" 범위 `1 .. 2^31 - 1`의 `op`를 사용해야 합니다.

### 표준 응답 메시지 처리

`op`가 `0xffffffff`와 `0xfffffffe`인 몇 가지 "표준" 응답 메시지가 있습니다. 일반적으로 `0xfffffff0`부터 `0xffffffff`까지의 `op` 값은 이러한 표준 응답을 위해 예약되어 있습니다.

```
* `op` = `0xffffffff` means "operation not supported". It is followed by the 64-bit `query_id` extracted from the original query, and the 32-bit `op` of the original query. All but the simplest smart contracts should return this error when they receive a query with an unknown `op` in the range `1 .. 2^31-1`.
* `op` = `0xfffffffe` means "operation not allowed". It is followed by the 64-bit `query_id` of the original query, followed by the 32-bit `op` extracted from the original query.
```

알 수 없는 "응답"(범위 `2^31 .. 2^32-1`의 `op`)은 무시되어야 합니다(특히, 이들에 대한 응답으로 `op`가 `0xffffffff`인 응답이 생성되어서는 안 됨). 이는 예상치 못한 반송된 메시지("반송됨" 플래그가 설정된)와 마찬가지입니다.
