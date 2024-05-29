# 파이브 및 TVM 어셈블리

Fift는 스택 기반 프로그래밍 언어로 TON 전용 기능이 있어 셀과 함께 작동할 수 있습니다. TVM 어셈블리 역시 스택 기반 프로그래밍 언어로, 역시 TON에 특화되어 있으며 셀과 함께 작동할 수 있습니다. 그렇다면 이 둘의 차이점은 무엇일까요?

## 차이점

Fift는 컴파일 타임에 **실행됩니다** - 컴파일러가 스마트 컨트랙트 코드 BOC를 빌드할 때, FunC 코드가 처리된 후 실행됩니다. Fift는 다르게 보일 수 있습니다:

```
// tuple primitives
x{6F0} @Defop(4u) TUPLE
x{6F00} @Defop NIL
x{6F01} @Defop SINGLE
x{6F02} dup @Defop PAIR @Defop CONS
```

> Asm.fif의 TVM 연산자 코드 정의

```
"Asm.fif" include
<{ SETCP0 DUP IFNOTRET // return if recv_internal
   DUP 85143 INT EQUAL OVER 78748 INT EQUAL OR IFJMP:<{ // "seqno" and "get_public_key" get-methods
     1 INT AND c4 PUSHCTR CTOS 32 LDU 32 LDU NIP 256 PLDU CONDSEL  // cnt or pubk
   }>
   INC 32 THROWIF	// fail unless recv_external
   9 PUSHPOW2 LDSLICEX DUP 32 LDU 32 LDU 32 LDU 	//  signature in_msg subwallet_id valid_until msg_seqno cs
   NOW s1 s3 XCHG LEQ 35 THROWIF	//  signature in_msg subwallet_id cs msg_seqno
   c4 PUSH CTOS 32 LDU 32 LDU 256 LDU ENDS	//  signature in_msg subwallet_id cs msg_seqno stored_seqno stored_subwallet public_key
   s3 s2 XCPU EQUAL 33 THROWIFNOT	//  signature in_msg subwallet_id cs public_key stored_seqno stored_subwallet
   s4 s4 XCPU EQUAL 34 THROWIFNOT	//  signature in_msg stored_subwallet cs public_key stored_seqno
   s0 s4 XCHG HASHSU	//  signature stored_seqno stored_subwallet cs public_key msg_hash
   s0 s5 s5 XC2PU	//  public_key stored_seqno stored_subwallet cs msg_hash signature public_key
   CHKSIGNU 35 THROWIFNOT	//  public_key stored_seqno stored_subwallet cs
   ACCEPT
   WHILE:<{
     DUP SREFS	//  public_key stored_seqno stored_subwallet cs _51
   }>DO<{	//  public_key stored_seqno stored_subwallet cs
     8 LDU LDREF s0 s2 XCHG	//  public_key stored_seqno stored_subwallet cs _56 mode
     SENDRAWMSG
   }>	//  public_key stored_seqno stored_subwallet cs
   ENDS SWAP INC	//  public_key stored_subwallet seqno'
   NEWC 32 STU 32 STU 256 STU ENDC c4 POP
}>c
```

> wallet_v3_r2.5

마지막 코드 조각은 TVM 어셈블리처럼 보이며 대부분 실제로도 그렇습니다! 어떻게 이런 일이 일어날 수 있을까요?

수습 프로그래머에게 "이제 함수 끝에 이렇게, 저렇게 하는 명령을 추가하세요"라고 말한다고 상상해 보세요. 여러분의 명령은 결국 연수생의 프로그램에 들어가게 됩니다. 여기서처럼 대문자로 된 연산자 코드(SETCP0, DUP 등)는 Fift와 TVM에서 두 번 처리됩니다.

훈련생에게 높은 수준의 추상화를 설명할 수 있으며, 결국에는 훈련생이 이를 이해하고 사용할 수 있게 됩니다. 또한 Fift는 확장성이 뛰어나 자신만의 명령을 정의할 수 있습니다. 실제로 Asm[Tests].fif는 TVM 옵코드를 정의하는 데 사용됩니다.

반면에 TVM 옵코드는 **런타임**에 실행되며, 스마트 콘트랙트 코드입니다. 트레이너의 프로그램이라고 생각할 수 있습니다. TVM 어셈블리는 더 적은 일을 할 수 있지만(예: 블록체인에서 TVM이 하는 모든 일은 공개되어 있기 때문에 데이터 서명을 위한 기본 요소가 없습니다), 실제로 환경과 상호작용할 수 있습니다.

## 스마트 컨트랙트에서의 사용

### [다섯째] - 대규모 BOC 계약 체결

톤클리`를 사용하는 경우 가능합니다. 다른 컴파일러를 사용하여 컨트랙트를 빌드하는 경우, 큰 BOC를 포함하는 다른 방법이 있을 수 있습니다.
스마트 컨트랙트 코드를 빌드할 때 `fift/blob.fif`가 포함되도록 `project.yaml\`을 편집하세요:

```
contract:
  fift:
    - fift/blob.fif
  func:
    - func/code.fc
```

다섯/블롭.boc`에 BOC를 넣은 다음 `fift/블롭.fif\`에 다음 코드를 추가합니다:

```
<b 8 4 u, 8 4 u, "fift/blob.boc" file>B B>boc ref, b> <s @Defop LDBLOB
```

이제 스마트 컨트랙트에서 이 블롭을 추출할 수 있습니다:

```
cell load_blob() asm "LDBLOB";

() recv_internal() {
    send_raw_message(load_blob(), 160);
}
```

### [TVM 어셈블리] - 정수를 문자열로 변환하기

"슬프게도", 파이브 프리미티브를 사용한 int에서 문자열로의 변환 시도가 실패했습니다.

```
slice int_to_string(int x) asm "(.) $>s PUSHSLICE";
```

그 이유는 분명합니다. Fift는 컴파일 타임에 계산을 수행하는데, 아직 변환에 사용할 수 있는 `x`가 없기 때문입니다. 상수가 아닌 정수를 문자열 슬라이스로 변환하려면 TVM 어셈블리가 필요합니다. 예를 들어, 다음은 TON 스마트 챌린지 3 참가자 중 한 명이 작성한 코드입니다:

```
tuple digitize_number(int value)
  asm "NIL WHILE:<{ OVER }>DO<{ SWAP TEN DIVMOD s1 s2 XCHG TPUSH }> NIP";

builder store_number(builder msg, tuple t)
  asm "WHILE:<{ DUP TLEN }>DO<{ TPOP 48 ADDCONST ROT 8 STU SWAP }> DROP";

builder store_signed(builder msg, int v) inline_ref {
  if (v < 0) {
    return msg.store_uint(45, 8).store_number(digitize_number(- v));
  } elseif (v == 0) {
    return msg.store_uint(48, 8);
  } else {
    return msg.store_number(digitize_number(v));
  }
}
```

### [TVM 어셈블리] - 저렴한 모듈로 곱하기

```
int mul_mod(int a, int b, int m) inline_ref {               ;; 1232 gas units
  (_, int r) = muldivmod(a % m, b % m, m);
  return r;
}
int mul_mod_better(int a, int b, int m) inline_ref {        ;; 1110 gas units
  (_, int r) = muldivmod(a, b, m);
  return r;
}
int mul_mod_best(int a, int b, int m) asm "x{A988} s,";     ;; 65 gas units
```

x{A988}`는 [5.2 나눗셈](/learn/tvm-instruction/instruction#52-division)에 따라 형식이 지정된 연산자입니다: 사전 곱셈을 사용한 나눗셈, 여기서 반환되는 유일한 결과는 나머지 모듈로 세 번째 인수입니다. 그러나 연산자는 스마트 컨트랙트 코드에 들어가야 하는데, `s,\`는 스택 위에 있는 슬라이스를 약간 아래 빌더에 저장하는 역할을 합니다.
