# 내부 메시지

## 개요

스마트 콘트랙트는 소위 **내부 메시지**를 전송하여 서로 상호 작용합니다. 내부 메시지가 의도한 대상에 도달하면 대상 계정을 대신하여 일반 트랜잭션이 생성되고, 내부 메시지는 코드와 이 계정의 영구 데이터(스마트 컨트랙트)에 지정된 대로 처리됩니다.

:::info
특히 처리 트랜잭션은 하나 또는 여러 개의 아웃바운드 내부 메시지를 생성할 수 있으며, 이 중 일부는 처리 중인 내부 메시지의 소스 주소로 주소가 지정될 수 있습니다. 이는 쿼리가 내부 메시지로 캡슐화되어 다른 스마트 콘트랙트로 전송되면, 쿼리를 처리하고 다시 내부 메시지로 응답을 보내는 간단한 "클라이언트-서버 애플리케이션"을 만드는 데 사용할 수 있습니다.
:::

이러한 접근 방식은 내부 메시지가 '쿼리'인지, '응답'인지, 아니면 '단순 송금'과 같이 추가 처리가 필요하지 않은 것인지 구분해야 할 필요성을 초래합니다. 또한 응답이 수신되면 어떤 쿼리에 해당하는지 파악할 수 있는 수단이 있어야 합니다.

이 목표를 달성하기 위해 내부 메시지 레이아웃에 대해 다음과 같은 접근 방식을 사용할 수 있습니다(TON 블록체인은 메시지 본문에 대한 제한을 적용하지 않으므로 이는 실제로 권장 사항일 뿐입니다).

### 내부 메시지 구조

메시지 본문은 메시지 자체에 포함되거나 TL-B 스키마 조각으로 표시된 것처럼 메시지에서 참조되는 별도의 셀에 저장될 수 있습니다:

```tlb
message$_ {X:Type} ... body:(Either X ^X) = Message X;
```

수신 스마트 콘트랙트는 최소한 메시지 본문이 포함된 내부 메시지를 수락해야 합니다(메시지가 포함된 셀에 맞을 때마다). 별도의 셀에 있는 메시지 본문을 허용하는 경우(`(X ^ X)`의 `right` 생성자를 사용), 인바운드 메시지 처리는 메시지 본문에 대해 선택한 특정 임베딩 옵션에 의존하지 않아야 합니다. 반면에 간단한 쿼리 및 응답의 경우 별도의 셀에 메시지 본문을 전혀 지원하지 않는 것도 완벽하게 유효합니다.

### 내부 메시지 본문

메시지 본문은 일반적으로 다음 필드로 시작됩니다:

```
* A 32-bit (big-endian) unsigned integer `op`, identifying the `operation` to be performed, or the `method` of the smart contract to be invoked.
* A 64-bit (big-endian) unsigned integer `query_id`, used in all query-response internal messages to indicate that a response is related to a query (the `query_id` of a response must be equal to the `query_id` of the corresponding query). If `op` is not a query-response method (e.g., it invokes a method that is not expected to send an answer), then `query_id` may be omitted.
* The remainder of the message body is specific for each supported value of `op`.
```

### 댓글이 포함된 간단한 메시지

op`이 0이면 메시지는 "댓글이 포함된 단순 전송 메시지"입니다. 주석은 메시지 본문의 나머지 부분에 포함됩니다(`query_id`필드 없이, 즉 다섯 번째 바이트부터 시작). 바이트`0xff\`로 시작하지 않으면 주석은 텍스트이며, 지갑의 최종 사용자에게 "있는 그대로" 표시될 수 있습니다(유효하지 않은 문자와 제어 문자를 필터링하고 유효한 UTF-8 문자열인지 확인한 후).

댓글이 셀에 맞지 않을 정도로 길면 셀의 첫 번째 참조에 맞지 않는 줄의 끝이 배치됩니다. 이 프로세스는 두 개 이상의 셀에 맞지 않는 코멘트를 설명하기 위해 재귀적으로 계속됩니다:

```
root_cell("0x00000000" - 32 bit, "string" up to 123 bytes)
         ↳1st_ref("string continuation" up to 127 bytes)
                 ↳1st_ref("string continuation" up to 127 bytes)
                         ↳....
```

NFT 및 [jetton](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md#forward_payload-format) 전송에 대한 댓글에도 동일한 형식이 사용됩니다.

예를 들어, 사용자는 이 텍스트 필드에 자신의 지갑에서 다른 사용자의 지갑으로 단순 송금하는 목적을 표시할 수 있습니다. 반면에 댓글이 바이트 '0xff'로 시작하는 경우, 나머지는 최종 사용자에게 텍스트로 표시되어서는 안 되는 "바이너리 댓글"입니다(필요한 경우 16진수 덤프로만 표시). "바이너리 코멘트"의 용도는 예를 들어 스토어에서 결제를 위한 구매 식별자를 포함하는 것으로, 스토어 소프트웨어에서 자동으로 생성하고 처리하는 것입니다.

대부분의 스마트 콘트랙트는 "단순 전송 메시지" 수신 시 사소하지 않은 작업을 수행하거나 인바운드 메시지를 거부해서는 안 됩니다. 이러한 방식으로 `op`가 0으로 확인되면 인바운드 내부 메시지를 처리하는 스마트 컨트랙트 함수(일반적으로 `recv_internal()`이라고 함)는 성공을 나타내는 0 종료 코드(예: 스마트 컨트랙트에 사용자 지정 예외 처리기가 설치되지 않은 경우 예외 `0`을 던짐)로 즉시 종료되어야 합니다. 이렇게 하면 수신 계정에 추가 효과 없이 메시지로 전송된 값이 입금됩니다.

### 암호화된 댓글이 포함된 메시지

op`가 `0x2167da4b\`이면 메시지는 "암호화된 댓글이 포함된 전송 메시지"입니다. 이 메시지는 다음과 같이 직렬화됩니다:

입력:

- 'pub_1`및`priv_1\` - 발신자의 공개 키와 비공개 키, 각각 32바이트씩 Ed25519.
- `pub_2` - 수신자의 Ed25519 공개 키, 32바이트.
- `msg` - 암호화할 메시지, 임의의 바이트 문자열. `len(msg) <= 960`.

암호화 알고리즘은 다음과 같습니다:

1. priv_1`과 `pub_2`를 사용하여 `shared_secret\`을 계산합니다.
2. 소금`은 발신자 지갑 주소의 [bas64url 표현](https://docs.ton.org/learn/overviews/addresses#user-friendly-address)을 `isBounceable=1`및`isTestnetOnly=0\`으로 설정합니다.
3. 16에서 31 사이의 길이로 `len(접두사+msg)`를 16으로 나눌 수 있는 길이의 바이트 문자열 `prefix`를 선택합니다. 접두사`의 첫 바이트는 `len(접두사)`와 같고 다른 바이트는 무작위입니다. 데이터 = 접두사 + 메시지`로 합니다.
4. msg_key`는 `hmac_sha512(salt, data)\`의 처음 16바이트로 합니다.
5. x = hmac_sha512(shared_secret, msg_key)`를 계산합니다. key=x[0:32]`와 `iv=x[32:48]`로 합니다.
6. CBC 모드에서 `키` 및 `iv`와 함께 AES-256을 사용하여 `데이터`를 암호화합니다.
7. 암호화된 댓글을 작성합니다:
   1. pub_xor = pub_1 ^ pub_2\` - 32바이트. 이렇게 하면 각 당사자는 상대방의 공개키를 조회하지 않고도 메시지를 해독할 수 있습니다.
   2. `msg_key` - 16바이트.
   3. 암호화된 '데이터'.
8. 메시지 본문은 4바이트 태그 '0x2167da4b'로 시작합니다. 그런 다음 이 암호화된 댓글이 저장됩니다:
   1. 바이트 문자열은 세그먼트로 나뉘며 `c_1,...,c_k` 셀 체인에 저장됩니다(`c_1`은 본문의 루트입니다). 각 셀(마지막 셀 제외)에는 다음 셀에 대한 참조가 있습니다.
   2. '_c_1'은 최대 35바이트(4바이트 태그 제외)를 포함하며, 다른 모든 셀은 최대 127바이트를 포함합니다.
   3. 이 형식에는 다음과 같은 제한 사항이 있습니다: `k <= 16`, 최대 문자열 길이는 1024입니다.

NFT 및 제톤 전송에 대한 코멘트에는 동일한 형식이 사용되며, 제톤 지갑 주소가 아닌 발신자 주소와 수신자 주소의 공개 키를 사용해야 한다는 점에 유의하세요.

:::info
Learn from examples of the message encryption algorithm:

- [encryption.js](https://github.com/toncenter/ton-wallet/blob/master/src/js/util/encryption.js)
- [SimpleEncryption.cpp](https://github.com/ton-blockchain/ton/blob/master/tonlib/tonlib/keys/SimpleEncryption.cpp)
  :::

### 댓글 없는 간단한 메시지 전송

"댓글이 없는 단순 전송 메시지"는 본문이 비어 있습니다(`op` 필드도 없음). 위의 고려 사항은 이러한 메시지에도 적용됩니다. 이러한 메시지는 메시지 셀에 본문이 포함되어야 합니다.

### 쿼리 메시지와 응답 메시지의 차이점

"쿼리" 메시지는 고차 비트가 지워진, 즉 `1 .. 2^31-1` 범위의 `op`를, "응답" 메시지는 고차 비트가 설정된, 즉 `2^31 .. 2^32-1` 범위의 `op`를 가질 것으로 예상합니다. 메서드가 쿼리도 응답도 아닌 경우(해당 메시지 본문에 `query_id` 필드가 포함되지 않는 경우), "쿼리" 범위 `1 .. 2^31 - 1`의 `op`를 사용해야 합니다.

### 표준 응답 메시지 처리

op`가 `0xffffff`및`0xfffffffe`와 같은 일부 "표준" 응답 메시지가 있습니다. 일반적으로 `0xfffffff0`부터 `0xffffff`까지의 `op\` 값은 이러한 표준 응답을 위해 예약되어 있습니다.

```
* `op` = `0xffffffff` means "operation not supported". It is followed by the 64-bit `query_id` extracted from the original query, and the 32-bit `op` of the original query. All but the simplest smart contracts should return this error when they receive a query with an unknown `op` in the range `1 .. 2^31-1`.
* `op` = `0xfffffffe` means "operation not allowed". It is followed by the 64-bit `query_id` of the original query, followed by the 32-bit `op` extracted from the original query.
```

알 수 없는 '응답'('2^31 .. 2^32-1' 범위에 `op`가 있는 경우)은 예상치 못한 반송된 메시지('반송' 플래그가 설정된 경우)와 마찬가지로 무시해야 합니다(특히 `op`가 `0xffffff`인 응답은 생성해서는 안 됩니다).
