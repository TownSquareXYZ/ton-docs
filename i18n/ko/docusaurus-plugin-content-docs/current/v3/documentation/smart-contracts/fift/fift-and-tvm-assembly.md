# Fift와 TVM 어셈블리

Fift는 TON 관련 기능이 있는 스택 기반 프로그래밍 언어로 셀을 처리할 수 있습니다. TVM 어셈블리도 TON에 특화된 스택 기반 프로그래밍 언어이며 셀을 처리할 수 있습니다. 그렇다면 이들의 차이점은 무엇일까요?

## 차이점

Fift는 **컴파일 타임**에 실행됩니다 - 컴파일러가 FunC 코드 처리 후 스마트 컨트랙트 코드 BOC를 빌드할 때입니다. Fift는 다음과 같은 모습을 가질 수 있습니다:

```
// tuple primitives
x{6F0} @Defop(4u) TUPLE
x{6F00} @Defop NIL
x{6F01} @Defop SINGLE
x{6F02} dup @Defop PAIR @Defop CONS
```

> Asm.fif의 TVM 옵코드 정의

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

> wallet_v3_r2.fif

마지막 코드 조각이 TVM 어셈블리처럼 보이고, 대부분이 실제로 그렇습니다! 어떻게 이런 일이 가능할까요?

초보 프로그래머에게 "이제 이것, 저것, 저것을 수행하는 명령을 함수 끝에 추가하라"고 말하는 것을 상상해보세요. 당신의 명령이 초보자의 프로그램에 들어가게 됩니다. 여기서도 마찬가지로 대문자로 된 옵코드(SETCP0, DUP 등)는 Fift와 TVM 모두에서 두 번 처리됩니다.

초보자에게 고수준 추상화를 설명하면 결국 이해하고 사용할 수 있게 됩니다. Fift도 확장 가능합니다 - 자신만의 명령을 정의할 수 있습니다. 사실 Asm[Tests].fif는 TVM 옵코드를 정의하는 것이 전부입니다.

반면 TVM 옵코드는 **런타임**에 실행됩니다 - 스마트 컨트랙트의 코드입니다. 초보자의 프로그램처럼 생각할 수 있습니다 - TVM 어셈블리는 더 적은 일을 할 수 있지만(예: TVM이 블록체인에서 하는 모든 것이 공개되므로 데이터 서명을 위한 내장 기본형이 없음), 실제로 환경과 상호작용할 수 있습니다.

## 스마트 컨트랙트에서의 사용

### [Fift] - 큰 BOC를 컨트랙트에 넣기

`toncli`를 사용하는 경우 가능합니다. 다른 컴파일러로 컨트랙트를 빌드하는 경우 큰 BOC를 포함하는 다른 방법이 있을 수 있습니다.
스마트 컨트랙트 코드를 빌드할 때 `fift/blob.fif`가 포함되도록 `project.yaml`을 편집하세요:

```
contract:
  fift:
    - fift/blob.fif
  func:
    - func/code.fc
```

BOC를 `fift/blob.boc`에 넣고 `fift/blob.fif`에 다음 코드를 추가하세요:

```
<b 8 4 u, 8 4 u, "fift/blob.boc" file>B B>boc ref, b> <s @Defop LDBLOB
```

이제 스마트 컨트랙트에서 이 blob을 추출할 수 있습니다:

```
cell load_blob() asm "LDBLOB";

() recv_internal() {
    send_raw_message(load_blob(), 160);
}
```

### [TVM 어셈블리] - 정수를 문자열로 변환

"안타깝게도" Fift 기본형을 사용한 정수-문자열 변환 시도는 실패합니다.

```
slice int_to_string(int x) asm "(.) $>s PUSHSLICE";
```

이유는 명확합니다: Fift는 변환을 위한 `x`가 아직 없는 컴파일 타임에 계산을 수행합니다. 상수가 아닌 정수를 문자열 슬라이스로 변환하려면 TVM 어셈블리가 필요합니다. 예를 들어, 이는 TON Smart Challenge 3 참가자 중 한 명의 코드입니다:

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

### [TVM 어셈블리] - 저비용 모듈로 곱셈

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

`x{A988}`은 [5.2 Division](/v3/documentation/tvm/instructions#A988)에 따라 포맷된 옵코드입니다: 세 번째 인수로 나눈 나머지만 반환되는 사전 곱셈이 있는 나눗셈입니다. 하지만 옵코드는 스마트 컨트랙트 코드에 들어가야 합니다 - 이것이 `s,`가 하는 일입니다: 약간 아래에 있는 빌더에 스택 최상위의 슬라이스를 저장합니다.
