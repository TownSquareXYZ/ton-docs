# 단계별 심층 분석

:::caution
이 섹션에서는 낮은 수준에서 TON과 상호 작용하기 위한 지침 및 매뉴얼을 설명합니다.
:::

이 문서의 목적은 TON 블록체인 라이트 클라이언트 및 관련 소프트웨어를 사용하여 TON 블록체인 테스트 네트워크에서 간단한 스마트 컨트랙트(간편 지갑)를 컴파일하고 생성하는 단계별 지침을 제공하는 것입니다.

여기서는 라이트 클라이언트가 이미 제대로 다운로드, 컴파일 및 설치되었다고 가정합니다.

> 이 튜토리얼은 테스트넷을 위한 것이므로 다음 구성을 사용해야 합니다: https://ton.org/testnet-global.config.json

## 1. 스마트 컨트랙트 주소

:::tip 새 버전 사용 가능
새로운 버전의 [스마트 컨트랙트 주소](/학습/개요/주소) 문서를 읽어주세요.
:::

TON 네트워크의 스마트 컨트랙트 주소는 두 부분으로 구성됩니다:

(a) 워크체인 ID(부호화된 32비트 정수) 및

(b) 워크체인 내부의 주소(워크체인에 따라 64-512비트).

현재 TON 블록체인 네트워크에서는 마스터체인(workchain_id=-1)과 가끔 기본 워크체인(workchain_id=0)만 실행되고 있습니다. 둘 다 256비트 주소를 가지고 있으므로, 이제부터는 workchain_id가 0 또는 -1이고 워크체인 내부의 주소가 정확히 256비트라고 가정합니다.

위에 명시된 조건에서 스마트 컨트랙트 주소는 다음과 같은 형식으로 표현할 수 있습니다:

A) "원시": < decimal workchain_id>:<64 hexadecimal digits with address>

B) '사용자 친화적'은 첫 번째 생성을 통해 얻을 수 있습니다:

- 태그 바이트 1개("바운스 가능" 주소의 경우 0x11, "바운스 불가능" 주소의 경우 0x51, 프로덕션 네트워크에서 실행 중인 소프트웨어에서 주소를 허용하지 않아야 하는 경우 +0x80 추가).
- workchain_id와 함께 부호화된 8비트 정수가 포함된 1바이트(기본 워크체인의 경우 0x00, 마스터체인의 경우 0xff).
- 워크체인 내부의 스마트 컨트랙트 주소 256비트를 포함하는 32바이트(빅엔디안)
- 이전 34바이트의 CRC16-CCITT를 포함하는 2바이트

B)의 경우, 얻은 36바이트는 base64(즉, 숫자, 라틴 대문자 및 소문자, '/' 및 '+' 포함) 또는 base64url('/' 및 '+' 대신 '_' 및 '-' 포함)을 사용하여 인코딩되어 48개의 인쇄 가능한 비공백 문자를 생성합니다.

예시:

"테스트 제공자"(요청하는 모든 사람에게 최대 20개의 테스트 코인을 제공하는 테스트 네트워크의 마스터체인에 있는 특별한 스마트 컨트랙트)가 주소를 가지고 있습니다:

`-1:fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232260`

를 '원시' 형태로 입력합니다('a'...'f' 대신 라틴 대문자 'A'...'F'를 사용할 수 있음),

그리고:

`kf/8uRo6OBbQ97jCx2EIuKm8Wmt6Vb15-KsQHFLbKSMiYIny` (base64)

`kf_8uRo6OBbQ97jCx2EIuKm8Wmt6Vb15-KsQHFLbKSMiYIny` (base64url)

를 '사용자 친화적' 양식(사용자 친화적 클라이언트가 표시할 양식)에 입력합니다. 두 양식(base64 및 base64url) 모두 유효하며 반드시 수락해야 합니다.

참고로, TON 블록체인과 관련된 다른 바이너리 데이터는 첫 바이트만 다를 뿐 유사한 "아머드" 베이스64 표현을 가지고 있습니다. 예를 들어, 유비쿼터스 256비트 Ed25519 공개 키는 다음과 같이 36바이트 시퀀스를 먼저 생성하여 표현합니다:

- 하나의 태그 바이트 0x3E, 즉 공개 키임을 의미합니다.
- 하나의 태그 바이트 0xE6, 즉 Ed25519 공개 키입니다.
- Ed25519 공개 키의 표준 바이너리 표현을 포함하는 32바이트
- 이전 34바이트의 CRC16-CCITT의 빅 엔디안 표현을 포함하는 2바이트

결과 36바이트 시퀀스는 표준 방식에 따라 48자 base64 또는 base64url 문자열로 변환됩니다. 예를 들어, Ed25519 공개 키 `E39ECDA0A7B0C60A7107EC43967829DBE8BC356A49B9DFC6186B3EAC74B5477D`(일반적으로 32바이트 `0xE3, 0x9E, ..., 0x7D` 시퀀스로 표시)는 다음과 같은 "아머드" 표현을 가집니다:

`Pubjns2gp7DGCnEH7EOWeCnb6Lw1akm538YYaz6sdLVHfRB2`

## 2. 스마트 컨트랙트 상태 검사하기

TON 라이트 클라이언트의 도움으로 스마트 컨트랙트의 상태를 쉽게 확인할 수 있습니다. 위에서 설명한 샘플 스마트 컨트랙트의 경우, 라이트 클라이언트를 실행하고 다음 명령을 입력합니다:

```func
> last
...
> getaccount -1:fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232260
or
> getaccount kf_8uRo6OBbQ97jCx2EIuKm8Wmt6Vb15-KsQHFLbKSMiYIny
```

다음과 같은 내용이 표시됩니다:

:::info
코드, 주석 및/또는 문서에는 "그램", "나노그램" 등의 매개변수, 방법, 정의가 포함될 수 있음을 참고해 주세요. 이는 텔레그램에서 개발한 오리지널 TON 코드의 유산입니다. 그램 암호화폐는 발행된 적이 없습니다. TON의 통화는 톤코인이며, TON 테스트넷의 통화는 테스트 톤코인입니다.
:::

```cpp
got account state for -1 : FCB91A3A3816D0F7B8C2C76108B8A9BC5A6B7A55BD79F8AB101C52DB29232260 with respect to blocks (-1,8000000000000000,2075):BFE876CE2085274FEDAF1BD80F3ACE50F42B5A027DF230AD66DCED1F09FB39A7:522C027A721FABCB32574E3A809ABFBEE6A71DE929C1FA2B1CD0DDECF3056505
account state is (account
  addr:(addr_std
    anycast:nothing workchain_id:-1 address:xFCB91A3A3816D0F7B8C2C76108B8A9BC5A6B7A55BD79F8AB101C52DB29232260)
  storage_stat:(storage_info
    used:(storage_used
      cells:(var_uint len:1 value:3)
      bits:(var_uint len:2 value:707)
      public_cells:(var_uint len:0 value:0)) last_paid:1568899526
    due_payment:nothing)
  storage:(account_storage last_trans_lt:2310000003
    balance:(currencies
      grams:(nanograms
        amount:(var_uint len:6 value:9998859500889))
      other:(extra_currencies
        dict:hme_empty))
    state:(account_active
      (
        split_depth:nothing
        special:nothing
        code:(just
          value:(raw@^Cell 
            x{}
             x{FF0020DD2082014C97BA9730ED44D0D70B1FE0A4F260D31F01ED44D0D31FD166BAF2A1F8000120D74A8E11D307D459821804A817C80073FB0201FB00DED1A4C8CB1FC9ED54}
            ))
        data:(just
          value:(raw@^Cell 
            x{}
             x{00009A15}
            ))
        library:hme_empty))))
x{CFFFCB91A3A3816D0F7B8C2C76108B8A9BC5A6B7A55BD79F8AB101C52DB2923226020680B0C2EC1C0E300000000226BF360D8246029DFF56534_}
 x{FF0020DD2082014C97BA9730ED44D0D70B1FE0A4F260D31F01ED44D0D31FD166BAF2A1F8000120D74A8E11D307D459821804A817C80073FB0201FB00DED1A4C8CB1FC9ED54}
 x{00000003}
last transaction lt = 2310000001 hash = 73F89C6F8910F598AD84504A777E5945C798AC8C847FF861C090109665EAC6BA
```

첫 번째 정보 행 `계정 상태 가져옴 ...에 대해 ...`에는 계정 주소와 계정 상태가 덤프된 마스터체인 블록 식별자가 표시됩니다. 후속 블록에서 계정 상태가 변경되더라도 `last` 명령으로 참조 블록이 최신 값으로 업데이트되기 전까지는 `getaccount xxx` 명령은 동일한 결과를 반환합니다. 이러한 방식으로 모든 계정의 상태를 조사하여 일관된 결과를 얻을 수 있습니다.

계정 상태는 (계정 ...)\` 줄은 계정 상태의 예쁘게 인쇄된 역직렬화된 보기를 시작합니다. 이는 톤 블록체인 문서에 설명된 대로 톤 블록체인에서 계정 상태를 표현하는 데 사용되는 TL-B 데이터 타입 Account의 역직렬화입니다. (역직렬화에 사용된 TL-B 스키마는 소스 파일 'crypto/block/block.tlb'에서 확인할 수 있으며, 스키마가 오래된 경우 역직렬화에 문제가 있을 수 있습니다).

마지막으로 `x{CFF...`로 시작하는 마지막 몇 줄("원시 덤프")에는 셀 트리로 표시되는 것과 동일한 정보가 포함되어 있습니다. 이 경우 데이터 비트 `CFF...34_`(밑줄은 마지막 이진수 1과 그 이후의 모든 이진수 0을 제거해야 함을 의미하므로 16진수 `4_`는 이진수 `0`에 해당)를 포함하는 루트 셀 1개와 그 하위 셀 2개(한 칸 들여쓰기로 표시됨)가 있습니다.

{FF0020DD20...}`가 이 스마트 컨트랙트의 코드임을 알 수 있습니다. TON 가상 머신 설명서의 부록 A를 참고하면 이 코드를 분해할 수도 있습니다: FF00`은 `SETCP 0`, `20`은 `DUP`, `DD`는 `IFNOTRET`, `20`은 `DUP` 등입니다. (참고로, 이 스마트 컨트랙트의 소스 코드는 소스 파일 `crypto/block/new-testgiver.fif`에서 찾을 수 있습니다).

또한 `x{00009A15}`(실제 값은 다를 수 있음)가 이 스마트 컨트랙트의 영구 데이터라는 것을 알 수 있습니다. 이는 실제로 스마트 콘트랙트에서 지금까지 수행한 작업의 카운터로 사용되는 부호 없는 32비트 정수입니다. 이 값은 TON 블록체인 내의 모든 정수와 마찬가지로 빅엔디안(즉, 3은 `x{03000000}`가 아닌 `x{00000003}`로 인코딩됨)이라는 점에 유의하시기 바랍니다. 이 경우 카운터는 `0x9A15` = `39445`와 같습니다.

스마트 콘트랙트의 현재 잔액은 출력의 예쁘게 인쇄된 부분에서 쉽게 확인할 수 있습니다. 이 경우 `... balance:(currencies:(grams:(nanograms:(... value:1000000000000000...))))`가 표시되며, 이는 (테스트) 나노톤(이 예에서는 백만 테스트 톤코인, 실제 표시되는 수치는 더 작을 수 있음) 단위의 계정 잔액입니다. 크립토/블록/스킴.tlb\`에서 제공하는 TL-B 스킴을 공부하면 원시 덤프 부분에서도 이 숫자(10^15)를 이진 빅엔디안 형식으로 찾을 수 있습니다(루트 셀의 데이터 비트 끝 근처에 위치).

## 3. 새 스마트 컨트랙트 컴파일하기

새로운 스마트 컨트랙트를 톤 블록체인에 업로드하기 전에 코드와 데이터를 확인하고 직렬화된 형태로 파일("백 오브 셀" 또는 BOC 파일이라고 하며, 보통 .boc 접미사가 붙습니다)에 저장해야 합니다. 32비트 연산 카운터와 소유자의 256비트 Ed25519 공개 키를 영구 데이터에 저장하는 간단한 지갑 스마트 컨트랙트의 경우를 예로 들어보겠습니다.

스마트 컨트랙트를 개발하려면 당연히 TON 스마트 컨트랙트 컴파일러와 같은 도구가 필요합니다. 기본적으로 TON 스마트 컨트랙트 컴파일러는 특수한 고급 프로그래밍 언어로 스마트 컨트랙트의 소스를 읽고 이 소스에서 .boc 파일을 생성하는 프로그램입니다.

이러한 도구 중 하나는 이 배포판에 포함되어 있으며 간단한 스마트 컨트랙트를 만드는 데 도움이 될 수 있는 Fift 인터프리터입니다. 더 큰 규모의 스마트 컨트랙트는 더 정교한 도구를 사용하여 개발해야 합니다(예: 이 배포판에 포함된 FunC 컴파일러는 FunC 소스 파일에서 Fift 어셈블러 파일을 생성하며, 일부 FunC 스마트 컨트랙트 소스는 `crypto/smartcont` 디렉터리에서 찾을 수 있습니다). 그러나 데모용으로는 Fift만으로도 충분합니다.

간단한 지갑 스마트 컨트랙트의 소스가 포함된 파일 'new-wallet.fif'(일반적으로 소스 디렉터리 기준으로는 `crypto/smartcont/new-wallet.fif`에 위치)를 예로 들어보겠습니다:

```cpp
#!/usr/bin/env fift -s
"TonUtil.fif" include
"Asm.fif" include

{ ."usage: " @' $0 type ." <workchain-id> [<filename-base>]" cr
  ."Creates a new wallet in specified workchain, with private key saved to or loaded from <filename-base>.pk" cr
  ."('new-wallet.pk' by default)" cr 1 halt
} : usage
$# 1- -2 and ' usage if

$1 parse-workchain-id =: wc    // set workchain id from command line argument
def? $2 { @' $2 } { "new-wallet" } cond constant file-base

."Creating new wallet in workchain " wc . cr

// Create new simple wallet
<{ SETCP0 DUP IFNOTRET // return if recv_internal
   DUP 85143 INT EQUAL IFJMP:<{ // "seqno" get-method
     DROP c4 PUSHCTR CTOS 32 PLDU  // cnt
   }>
   INC 32 THROWIF  // fail unless recv_external
   512 INT LDSLICEX DUP 32 PLDU   // sign cs cnt
   c4 PUSHCTR CTOS 32 LDU 256 LDU ENDS  // sign cs cnt cnt' pubk
   s1 s2 XCPU            // sign cs cnt pubk cnt' cnt
   EQUAL 33 THROWIFNOT   // ( seqno mismatch? )
   s2 PUSH HASHSU        // sign cs cnt pubk hash
   s0 s4 s4 XC2PU        // pubk cs cnt hash sign pubk
   CHKSIGNU              // pubk cs cnt ?
   34 THROWIFNOT         // signature mismatch
   ACCEPT
   SWAP 32 LDU NIP 
   DUP SREFS IF:<{
     // 3 INT 35 LSHIFT# 3 INT RAWRESERVE    // reserve all but 103 coins from the balance
     8 LDU LDREF         // pubk cnt mode msg cs
     s0 s2 XCHG SENDRAWMSG  // pubk cnt cs ; ( message sent )
   }>
   ENDS
   INC NEWC 32 STU 256 STU ENDC c4 POPCTR
}>c // >libref
// code
<b 0 32 u, 
   file-base +".pk" load-generate-keypair
   constant wallet_pk
   B, 
b> // data
null // no libraries
// Libs{ x{ABACABADABACABA} drop x{AAAA} s>c public_lib x{1234} x{5678} |_ s>c public_lib }Libs
<b b{0011} s, 3 roll ref, rot ref, swap dict, b>  // create StateInit
dup ."StateInit: " <s csr. cr
dup hash wc swap 2dup 2constant wallet_addr
."new wallet address = " 2dup .addr cr
2dup file-base +".addr" save-address-verbose
."Non-bounceable address (for init): " 2dup 7 .Addr cr
."Bounceable address (for later access): " 6 .Addr cr
<b 0 32 u, b>
dup ."signing message: " <s csr. cr
dup hash wallet_pk ed25519_sign_uint rot
<b b{1000100} s, wallet_addr addr, b{000010} s, swap <s s, b{0} s, swap B, swap <s s, b>
dup ."External message for initialization is " <s csr. cr
2 boc+>B dup Bx. cr
file-base +"-query.boc" tuck B>file
."(Saved wallet creating query to file " type .")" cr
```

(배포판의 실제 소스 파일은 약간 다를 수 있습니다.) 기본적으로 새로 생성된 키쌍으로 제어되는 이 스마트 컨트랙트의 새 인스턴스를 생성하기 위한 완전한 파이브 스크립트입니다. 이 스크립트는 명령줄 인수를 허용하므로 새 지갑을 만들 때마다 소스 파일을 편집할 필요가 없습니다.

이제 Fift 바이너리를 컴파일했다면(일반적으로 빌드 디렉터리에 대해 `crypto/fift`로 위치) 실행할 수 있습니다:

```bash
$ crypto/fift -I<source-directory>/crypto/fift/lib -s <source-directory>/crypto/smartcont/new-wallet.fif 0 my_wallet_name
```

여기서 0은 새 지갑을 포함할 워크체인(0 = 베이스체인, -1 = 마스터체인)이고, `my_wallet_name`은 이 지갑과 연결하려는 식별자입니다. 새 지갑의 주소는 `my_wallet_name.addr` 파일에 저장되고, 새로 생성된 개인 키는 `my_wallet_name.pk`에 저장되며(이 파일이 이미 존재하지 않으면 이 파일에서 키가 대신 로드됩니다), 외부 메시지는 `my_wallet_name-query.boc`에 저장됩니다. 지갑 이름을 지정하지 않으면(위 예시에서는 `my_wallet_name`) 기본 이름인 `new-wallet`이 사용됩니다.

FIFTPATH환경 변수를`<source-directory>/crypto/fift/lib:<source-directory>/crypto/smartcont`, `Fift.fif`및`Asm.fif`라이브러리 파일과 샘플 스마트 컨트랙트 소스가 각각 포함된 디렉토리로 설정할 수 있으며, Fift 인터프리터에`-I`인수를 생략할 수 있습니다. Fift 바이너리`crypto/fift`를 `PATH`에 포함된 디렉토리(예: `/usr/bin/fift\`)에 설치한 경우 다음을 간단히 호출할 수 있습니다:

```bash
$ fift -s new-wallet.fif 0 my_wallet_name
```

명령줄에 전체 검색 경로를 표시하는 대신 검색어를 입력하세요.

모든 것이 정상적으로 작동하면 다음과 같은 화면이 표시됩니다:

```cpp
Creating new wallet in workchain 0 
Saved new private key to file my_wallet_name.pk
StateInit: x{34_}
 x{FF0020DD2082014C97BA9730ED44D0D70B1FE0A4F260810200D71820D70B1FED44D0D31FD3FFD15112BAF2A122F901541044F910F2A2F80001D31F3120D74A96D307D402FB00DED1A4C8CB1FCBFFC9ED54}
 x{00000000C59DC52962CC568AC5E72735EABB025C5BDF457D029AEEA6C2FFA5EB2A945446}

new wallet address = 0:2ee9b4fd4f077c9b223280c35763df9edab0b41ac20d36f4009677df95c3afe2 
(Saving address to file my_wallet_name.addr)
Non-bounceable address (for init): 0QAu6bT9Twd8myIygMNXY9-e2rC0GsINNvQAlnfflcOv4uVb
Bounceable address (for later access): kQAu6bT9Twd8myIygMNXY9-e2rC0GsINNvQAlnfflcOv4rie
signing message: x{00000000}

External message for initialization is x{88005DD369FA9E0EF93644650186AEC7BF3DB5616835841A6DE8012CEFBF2B875FC41190260D403E40B2EE8BEB2855D0F4447679D9B9519BE64BE421166ABA2C66BEAAAF4EBAF8E162886430243216DDA10FCE68C07B6D7DDAA3E372478D711E3E1041C00000001_}
 x{FF0020DD2082014C97BA9730ED44D0D70B1FE0A4F260810200D71820D70B1FED44D0D31FD3FFD15112BAF2A122F901541044F910F2A2F80001D31F3120D74A96D307D402FB00DED1A4C8CB1FCBFFC9ED54}
 x{00000000C59DC52962CC568AC5E72735EABB025C5BDF457D029AEEA6C2FFA5EB2A945446}

B5EE9C724104030100000000E50002CF88005DD369FA9E0EF93644650186AEC7BF3DB5616835841A6DE8012CEFBF2B875FC41190260D403E40B2EE8BEB2855D0F4447679D9B9519BE64BE421166ABA2C66BEAAAF4EBAF8E162886430243216DDA10FCE68C07B6D7DDAA3E372478D711E3E1041C000000010010200A2FF0020DD2082014C97BA9730ED44D0D70B1FE0A4F260810200D71820D70B1FED44D0D31FD3FFD15112BAF2A122F901541044F910F2A2F80001D31F3120D74A96D307D402FB00DED1A4C8CB1FCBFFC9ED54004800000000C59DC52962CC568AC5E72735EABB025C5BDF457D029AEEA6C2FFA5EB2A945446BCF59C17
(Saved wallet creating query to file my_wallet_name-query.boc)
```

간단히 말해, `Asm.fif` include 줄에 로드된 Fift 어셈블러는 스마트 콘트랙트의 소스 코드(`<{ SETCP0 ... c4 POPCTR }>` 줄에 포함됨)를 내부 표현으로 컴파일하는 데 사용됩니다. 스마트 컨트랙트의 초기 데이터도 32비트 시퀀스 번호(0과 같음)와 새로 생성된 Ed25519 키쌍의 256비트 공개 키를 포함하는 (`<b 0 32 u, ... b>` 줄에 의해) 생성됩니다. 해당 개인 키는 이미 존재하지 않는 한 `my_wallet_name.pk` 파일에 저장됩니다(같은 디렉토리에서 이 코드를 두 번 실행하면 이 파일에서 개인 키가 대신 로드됩니다).

새 스마트 콘트랙트의 코드와 데이터는 (다음 줄에서) `StateInit` 구조로 결합되고, 새 스마트 콘트랙트의 주소(이 `StateInit` 구조의 해시와 동일)가 계산되어 출력되며, 새 스마트 콘트랙트의 주소와 동일한 대상 주소의 외부 메시지가 생성됩니다. 이 외부 메시지에는 새 스마트 콘트랙트에 대한 올바른 `StateInit`과 사소하지 않은 페이로드(올바른 개인 키로 서명)가 모두 포함됩니다.

마지막으로, 외부 메시지는 `B5EE...BE63`으로 표시되는 셀 백으로 직렬화되고 `my_wallet_name-query.boc` 파일에 저장됩니다. 기본적으로 이 파일은 TON 블록체인에 업로드하는 데 필요한 모든 추가 정보가 포함된 컴파일된 스마트 컨트랙트입니다.

## 4. 새로운 스마트 컨트랙트로 일부 자금 이체

라이트 클라이언트를 실행하고 입력하여 새 스마트 컨트랙트를 즉시 업로드할 수 있습니다:

```
> sendfile new-wallet-query.boc
```

또는

```
> sendfile my_wallet_name-query.boc
```

지갑 이름을 'my_wallet_name'으로 선택한 경우.

안타깝게도 스마트 콘트랙트는 데이터를 블록체인에 저장하고 처리하는 데 드는 비용을 지불할 수 있는 양의 잔고가 있어야 하기 때문에 이 방법은 작동하지 않습니다. 따라서 생성 시 `-1:60c0...c0d0`(원시 형태) 및 `0f9...EKD`(사용자 친화적인 형태)로 표시되는 새 스마트 컨트랙트 주소로 일부 자금을 이체해야 합니다.

실제 시나리오에서는 기존 지갑에서 톤코인을 이체하거나 친구에게 요청하거나 암호화폐 거래소에서 톤코인을 구매하여 새 톤코인을 이체할 계정으로 '0f9...EKD'를 표시합니다.

테스트 네트워크에서는 '테스트 제공자'에게 테스트 톤코인(최대 20개)을 요청할 수 있는 또 다른 옵션이 있습니다. 방법을 설명해드리겠습니다.

## 5. 테스트 제공자 스마트 컨트랙트 사용

테스트 제공자 스마트 컨트랙트의 주소를 알아야 합니다. 앞의 예시 중 하나에 표시된 것처럼 `-1:fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232260` 또는 이와 동등한 `kf_8uRo6OBbQ97jCx2EIuKm8Wmt6Vb15-KsQHFLbKSMiYIny`라고 가정하겠습니다. 라이트 클라이언트에서 다음과 같이 입력하여 이 스마트 컨트랙트의 상태를 확인할 수 있습니다:

```
> last
> getaccount kf_8uRo6OBbQ97jCx2EIuKm8Wmt6Vb15-KsQHFLbKSMiYIny
```

를 입력합니다. 출력에서 필요한 유일한 숫자는 스마트 컨트랙트 데이터에 저장된 32비트 시퀀스 번호입니다(위 예시에서는 `0x9A15`이지만 일반적으로는 다를 수 있습니다). 이 시퀀스 번호의 현재 값을 얻는 더 간단한 방법은 입력하는 것입니다:

```
> last
> runmethod kf_8uRo6OBbQ97jCx2EIuKm8Wmt6Vb15-KsQHFLbKSMiYIny seqno
```

올바른 값 39445 = 0x9A15를 생성합니다:

```cpp
got account state for -1 : FCB91A3A3816D0F7B8C2C76108B8A9BC5A6B7A55BD79F8AB101C52DB29232260 with respect to blocks (-1,8000000000000000,2240):18E6DA7707191E76C71EABBC5277650666B7E2CFA2AEF2CE607EAFE8657A3820:4EFA2540C5D1E4A1BA2B529EE0B65415DF46BFFBD27A8EB74C4C0E17770D03B1
creating VM
starting VM to run method `seqno` (85143) of smart contract -1:FCB91A3A3816D0F7B8C2C76108B8A9BC5A6B7A55BD79F8AB101C52DB29232260
...
arguments:  [ 85143 ] 
result:  [ 39445 ] 
```

다음으로, 테스트 제공자에게 지정된 양의 테스트 토큰을 전달하는 (초기화되지 않은) 스마트 컨트랙트에 다른 메시지를 보내도록 요청하는 외부 메시지를 생성합니다. 이 외부 메시지를 생성하기 위한 특별한 파이브 스크립트는 `crypto/smartcont/testgiver.fif`에 있습니다:

```cpp
#!/usr/bin/env fift -s
"TonUtil.fif" include

{ ."usage: " @' $0 type ." <dest-addr> <seqno> <amount> [<savefile>]" cr
  ."Creates a request to TestGiver and saves it into <savefile>.boc" cr
  ."('testgiver-query.boc' by default)" cr 1 halt
} : usage

$# 3 - -2 and ' usage if

// "testgiver.addr" load-address 
Masterchain 0xfcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232260
2constant giver_addr
 ."Test giver address = " giver_addr 2dup .addr cr 6 .Addr cr

$1 true parse-load-address =: bounce 2=: dest_addr
$2 parse-int =: seqno
$3 $>GR =: amount
def? $4 { @' $4 } { "testgiver-query" } cond constant savefile

."Requesting " amount .GR ."to account "
dest_addr 2dup bounce 7 + .Addr ." = " .addr
."seqno=0x" seqno x. ."bounce=" bounce . cr

// create a message (NB: 01b00.., b = bounce)
<b b{01} s, bounce 1 i, b{000100} s, dest_addr addr, 
   amount Gram, 0 9 64 32 + + 1+ 1+ u, "GIFT" $, b>
<b seqno 32 u, 1 8 u, swap ref, b>
dup ."enveloping message: " <s csr. cr
<b b{1000100} s, giver_addr addr, 0 Gram, b{00} s,
   swap <s s, b>
dup ."resulting external message: " <s csr. cr
2 boc+>B dup Bx. cr
savefile +".boc" tuck B>file
."(Saved to file " type .")" cr
```

이 스크립트에 필요한 매개 변수를 명령줄 인수로 전달할 수 있습니다.

```bash
$ crypto/fift -I<include-path> -s <path-to-testgiver-fif> <dest-addr> <testgiver-seqno> <coins-amount> [<savefile>]
```

예를 들어

```bash
$ crypto/fift -I<source-directory>/crypto/fift/lib:<source-directory>/crypto/smartcont -s testgiver.fif 0QAu6bT9Twd8myIygMNXY9-e2rC0GsINNvQAlnfflcOv4uVb 0x9A15 6.666 wallet-query
```

또는 간단히:

```bash
$ fift -s testgiver.fif 0QAu6bT9Twd8myIygMNXY9-e2rC0GsINNvQAlnfflcOv4uVb 0x9A15 6.666 wallet-query
```

환경 변수 `FIFTPATH`를 `<source-directory>/crypto/fift/lib:<source-directory>/crypto/smartcont`로 설정하고 파이브 바이너리를 `/usr/bin/fift`(또는 `PATH`의 다른 위치에)에 설치했다면 말입니다.

새 스마트 컨트랙트에 새로 생성된 메시지는 반송 비트가 지워져야 하며, 그렇지 않으면 전송이 발신자에게 반송됩니다. 이것이 바로 새로운 지갑 스마트 컨트랙트의 반송 불가 주소인 `0QAu6bT9Twd8myIygMNXY9-e2rC0GsINNvQAlnfflcOv4uVb`를 전달한 이유입니다.

이 파이브 코드는 테스트 제공자 스마트 컨트랙트에서 6.666 테스트 톤(약 20톤까지 다른 금액을 입력할 수 있음)이 담긴 새로운 스마트 컨트랙트의 주소로 내부 메시지를 생성합니다. 그런 다음 이 메시지는 테스트 제공자에게 전달되는 외부 메시지에 포함됩니다. 이 외부 메시지에는 테스트 제공자의 정확한 시퀀스 번호도 포함되어야 합니다. 테스트 제공자는 이러한 외부 메시지를 수신하면 시퀀스 번호가 자신의 퍼시스턴트 데이터에 저장된 것과 일치하는지 확인하고, 일치하는 경우 필요한 양의 테스트 톤이 포함된 내부 메시지를 대상(이 경우 스마트 컨트랙트)에게 보냅니다.

외부 메시지가 직렬화되어 `wallet-query.boc` 파일에 저장됩니다. 이 과정에서 일부 출력이 생성됩니다:

```cpp
Test giver address = -1:fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232260 
kf_8uRo6OBbQ97jCx2EIuKm8Wmt6Vb15-KsQHFLbKSMiYIny
Requesting GR$6.666 to account 0QAu6bT9Twd8myIygMNXY9-e2rC0GsINNvQAlnfflcOv4uVb = 0:2ee9b4fd4f077c9b223280c35763df9edab0b41ac20d36f4009677df95c3afe2 seqno=0x9a15 bounce=0 
enveloping message: x{00009A1501}
 x{42001774DA7EA783BE4D91194061ABB1EFCF6D585A0D61069B7A004B3BEFCAE1D7F1280C6A98B4000000000000000000000000000047494654}

resulting external message: x{89FF02ACEEB6F264BCBAC5CE85B372D8616CA2B4B9A5E3EC98BB496327807E0E1C1A000004D0A80C_}
 x{42001774DA7EA783BE4D91194061ABB1EFCF6D585A0D61069B7A004B3BEFCAE1D7F1280C6A98B4000000000000000000000000000047494654}

B5EE9C7241040201000000006600014F89FF02ACEEB6F264BCBAC5CE85B372D8616CA2B4B9A5E3EC98BB496327807E0E1C1A000004D0A80C01007242001774DA7EA783BE4D91194061ABB1EFCF6D585A0D61069B7A004B3BEFCAE1D7F1280C6A98B4000000000000000000000000000047494654AFC17FA4
(Saved to file wallet-query.boc)
```

## 6. 테스트 제공자 스마트 컨트랙트에 외부 메시지 업로드하기

이제 라이트 클라이언트를 호출하고 테스트 제공자의 상태를 확인한 다음(시퀀스 번호가 변경된 경우 외부 메시지가 실패합니다) 입력하면 됩니다:

```bash
> sendfile wallet-query.boc
```

결과물을 확인할 수 있습니다:

```bash
... external message status is 1
```

는 외부 메시지가 콜레이터 풀에 전달되었음을 의미합니다. 이후 콜레이터 중 한 명이 이 외부 메시지를 블록에 포함하도록 선택하여 테스트 제공자 스마트 콘트랙트가 이 외부 메시지를 처리할 트랜잭션을 생성할 수 있습니다. 테스트 제공자의 상태가 변경되었는지 확인할 수 있습니다:

```bash
> last
> getaccount kf_8uRo6OBbQ97jCx2EIuKm8Wmt6Vb15-KsQHFLbKSMiYIny
```

(`마지막`을 입력하는 것을 잊으면 테스트 제공자 스마트 컨트랙트의 변경되지 않은 상태가 표시될 수 있습니다). 결과 출력은 다음과 같습니다:

```cpp
got account state for -1 : FCB91A3A3816D0F7B8C2C76108B8A9BC5A6B7A55BD79F8AB101C52DB29232260 with respect to blocks (-1,8000000000000000,2240):18E6DA7707191E76C71EABBC5277650666B7E2CFA2AEF2CE607EAFE8657A3820:4EFA2540C5D1E4A1BA2B529EE0B65415DF46BFFBD27A8EB74C4C0E17770D03B1
account state is (account
  addr:(addr_std
    anycast:nothing workchain_id:-1 address:xFCB91A3A3816D0F7B8C2C76108B8A9BC5A6B7A55BD79F8AB101C52DB29232260)
  storage_stat:(storage_info
    used:(storage_used
      cells:(var_uint len:1 value:3)
      bits:(var_uint len:2 value:707)
      public_cells:(var_uint len:0 value:0)) last_paid:0
    due_payment:nothing)
  storage:(account_storage last_trans_lt:10697000003
    balance:(currencies
      grams:(nanograms
        amount:(var_uint len:7 value:999993280210000))
      other:(extra_currencies
        dict:hme_empty))
    state:(account_active
      (
        split_depth:nothing
        special:nothing
        code:(just
          value:(raw@^Cell 
            x{}
             x{FF0020DDA4F260D31F01ED44D0D31FD166BAF2A1F80001D307D4D1821804A817C80073FB0201FB00A4C8CB1FC9ED54}
            ))
        data:(just
          value:(raw@^Cell 
            x{}
             x{00009A16}
            ))
        library:hme_empty))))
x{CFF8156775B79325E5D62E742D9B96C30B6515A5CD2F1F64C5DA4B193C03F070E0D2068086C00000000000000009F65D110DC0E35F450FA914134_}
 x{FF0020DDA4F260D31F01ED44D0D31FD166BAF2A1F80001D307D4D1821804A817C80073FB0201FB00A4C8CB1FC9ED54}
 x{00000001}
```

영구 데이터에 저장된 시퀀스 번호가 변경되고(이 예에서는 0x9A16 = 39446으로) 'last_trans_lt' 필드(이 계정의 마지막 거래의 논리적 시간)가 늘어난 것을 확인할 수 있습니다.

이제 새로운 스마트 컨트랙트의 상태를 검사할 수 있습니다:

```cpp
> getaccount 0QAu6bT9Twd8myIygMNXY9-e2rC0GsINNvQAlnfflcOv4uVb
or
> getaccount 0:2ee9b4fd4f077c9b223280c35763df9edab0b41ac20d36f4009677df95c3afe2
```

이제 알겠습니다:

```cpp
got account state for 0:2EE9B4FD4F077C9B223280C35763DF9EDAB0B41AC20D36F4009677DF95C3AFE2 with respect to blocks (-1,8000000000000000,16481):890F4D549428B2929F5D5E0C5719FBCDA60B308BA4B907797C9E846E644ADF26:22387176928F7BCEF654411CA820D858D57A10BBF1A0E153E1F77DE2EFB2A3FB and (-1,8000000000000000,16481):890F4D549428B2929F5D5E0C5719FBCDA60B308BA4B907797C9E846E644ADF26:22387176928F7BCEF654411CA820D858D57A10BBF1A0E153E1F77DE2EFB2A3FB
account state is (account
  addr:(addr_std
    anycast:nothing workchain_id:0 address:x2EE9B4FD4F077C9B223280C35763DF9EDAB0B41AC20D36F4009677DF95C3AFE2)
  storage_stat:(storage_info
    used:(storage_used
      cells:(var_uint len:1 value:1)
      bits:(var_uint len:1 value:111)
      public_cells:(var_uint len:0 value:0)) last_paid:1553210152
    due_payment:nothing)
  storage:(account_storage last_trans_lt:16413000004
    balance:(currencies
      grams:(nanograms
        amount:(var_uint len:5 value:6666000000))
      other:(extra_currencies
        dict:hme_empty))
    state:account_uninit))
x{CFF60C04141C6A7B96D68615E7A91D265AD0F3A9A922E9AE9C901D4FA83F5D3C0D02025BC2E4A0D9400000000F492A0511406354C5A004_}
```

새로운 스마트 컨트랙트에는 (6.666 테스트 톤코인 중) 일부 양의 잔액이 있지만 코드나 데이터는 없습니다(`state:account_uninit`에 반영됨).

## 7. 새 스마트 컨트랙트의 코드와 데이터 업로드하기

이제 코드와 데이터가 포함된 새 스마트 컨트랙트의 `StateInit`을 사용하여 외부 메시지를 업로드할 수 있습니다:

```cpp
> sendfile my_wallet_name-query.boc
... external message status is 1
> last
...
> getaccount 0QAu6bT9Twd8myIygMNXY9-e2rC0GsINNvQAlnfflcOv4uVb
...
got account state for 0:2EE9B4FD4F077C9B223280C35763DF9EDAB0B41AC20D36F4009677DF95C3AFE2 with respect to blocks (-1,8000000000000000,16709):D223B25D8D68401B4AA19893C00221CF9AB6B4E5BFECC75FD6048C27E001E0E2:4C184191CE996CF6F91F59CAD9B99B2FD5F3AA6F55B0B6135069AB432264358E and (-1,8000000000000000,16709):D223B25D8D68401B4AA19893C00221CF9AB6B4E5BFECC75FD6048C27E001E0E2:4C184191CE996CF6F91F59CAD9B99B2FD5F3AA6F55B0B6135069AB432264358E
account state is (account
  addr:(addr_std
    anycast:nothing workchain_id:0 address:x2EE9B4FD4F077C9B223280C35763DF9EDAB0B41AC20D36F4009677DF95C3AFE2)
  storage_stat:(storage_info
    used:(storage_used
      cells:(var_uint len:1 value:3)
      bits:(var_uint len:2 value:963)
      public_cells:(var_uint len:0 value:0)) last_paid:1553210725
    due_payment:nothing)
  storage:(account_storage last_trans_lt:16625000002
    balance:(currencies
      grams:(nanograms
        amount:(var_uint len:5 value:5983177000))
      other:(extra_currencies
        dict:hme_empty))
    state:(account_active
      (
        split_depth:nothing
        special:nothing
        code:(just
          value:(raw@^Cell 
            x{}
             x{FF0020DDA4F260810200D71820D70B1FED44D0D7091FD709FFD15112BAF2A122F901541044F910F2A2F80001D7091F3120D74A97D70907D402FB00DED1A4C8CB1FCBFFC9ED54}
            ))
        data:(just
          value:(raw@^Cell 
            x{}
             x{00000001F61CF0BC8E891AD7636E0CD35229D579323AA2DA827EB85D8071407464DC2FA3}
            ))
        library:hme_empty))))
x{CFF60C04141C6A7B96D68615E7A91D265AD0F3A9A922E9AE9C901D4FA83F5D3C0D020680F0C2E4A0EB280000000F7BB57909405928024A134_}
 x{FF0020DDA4F260810200D71820D70B1FED44D0D7091FD709FFD15112BAF2A122F901541044F910F2A2F80001D7091F3120D74A97D70907D402FB00DED1A4C8CB1FCBFFC9ED54}
 x{00000001F61CF0BC8E891AD7636E0CD35229D579323AA2DA827EB85D8071407464DC2FA3}
```

외부 메시지의 'StateInit'의 코드와 데이터를 사용하여 스마트 컨트랙트가 초기화되었으며, 처리 수수료로 인해 잔액이 약간 감소한 것을 확인할 수 있습니다. 이제 실행이 완료되었으며, 라이트 클라이언트의 `sendfile` 명령을 사용하여 새로운 외부 메시지를 생성하고 TON 블록체인에 업로드하여 활성화할 수 있습니다.

## 8. 간편 지갑 스마트 컨트랙트 사용

실제로 이 예시에서 사용한 간편 지갑 스마트 콘트랙트는 테스트 토큰을 다른 계정으로 이체하는 데 사용할 수 있습니다. 이 점에서 위에서 설명한 테스트 제공자 스마트 콘트랙트와 유사하지만, (소유자의) 올바른 개인 키로 서명된 외부 메시지만 처리한다는 차이점이 있습니다. 저희의 경우, 스마트 컨트랙트 컴파일 시 `my_wallet_name.pk` 파일에 저장된 개인 키입니다(섹션 3 참조).

이 스마트 컨트랙트를 사용하는 방법에 대한 예시는 샘플 파일 `crypto/smartcont/wallet.fif`에 나와 있습니다:

```cpp
#!/usr/bin/env fift -s
"TonUtil.fif" include

{ ."usage: " @' $0 type ." <filename-base> <dest-addr> <seqno> <amount> [-B <body-boc>] [<savefile>]" cr
  ."Creates a request to simple wallet created by new-wallet.fif, with private key loaded from file <filename-base>.pk "
  ."and address from <filename-base>.addr, and saves it into <savefile>.boc ('wallet-query.boc' by default)" cr 1 halt
} : usage
$# dup 4 < swap 5 > or ' usage if
def? $6 { @' $5 "-B" $= { @' $6 =: body-boc-file [forget] $6 def? $7 { @' $7 =: $5 [forget] $7 } { [forget] $5 } cond
  @' $# 2- =: $# } if } if

true constant bounce

$1 =: file-base
$2 bounce parse-load-address =: bounce 2=: dest_addr
$3 parse-int =: seqno
$4 $>GR =: amount
def? $5 { @' $5 } { "wallet-query" } cond constant savefile

file-base +".addr" load-address
2dup 2constant wallet_addr
."Source wallet address = " 2dup .addr cr 6 .Addr cr
file-base +".pk" load-keypair nip constant wallet_pk

def? body-boc-file { @' body-boc-file file>B B>boc } { <b "TEST" $, b> } cond
constant body-cell

."Transferring " amount .GR ."to account "
dest_addr 2dup bounce 7 + .Addr ." = " .addr 
."seqno=0x" seqno x. ."bounce=" bounce . cr
."Body of transfer message is " body-cell <s csr. cr
  
// create a message
<b b{01} s, bounce 1 i, b{000100} s, dest_addr addr, amount Gram, 0 9 64 32 + + 1+ u, 
  body-cell <s 2dup s-fits? not rot over 1 i, -rot { drop body-cell ref, } { s, } cond
b>
<b seqno 32 u, 1 8 u, swap ref, b>
dup ."signing message: " <s csr. cr
dup hash wallet_pk ed25519_sign_uint
<b b{1000100} s, wallet_addr addr, 0 Gram, b{00} s,
   swap B, swap <s s, b>
dup ."resulting external message: " <s csr. cr
2 boc+>B dup Bx. cr
savefile +".boc" tuck B>file
."(Saved to file " type .")" cr
```

이 스크립트는 다음과 같이 호출할 수 있습니다:

```bash
$ fift -I<source-directory>/crypto/fift/lib:<source-directory>/crypto/smartcont -s wallet.fif <your-wallet-id> <destination-addr> <your-wallet-seqno> <coins-amount>
```

또는 간단히:

```bash
$ fift -s wallet.fif <your-wallet-id> <destination-addr> <your-wallet-seqno> <coins-amount>
```

경로`와 `파이프 경로\`를 올바르게 설정했는지 확인하세요.

예를 들어

```bash
$ fift -s wallet.fif my_wallet_name kf8Ty2EqAKfAksff0upF1gOptUWRukyI9x5wfgCbh58Pss9j 1 .666
```

여기서 `my_wallet_name`은 이전에 `new-wallet.fif`와 함께 사용한 지갑의 식별자입니다. 테스트 지갑의 주소와 개인 키는 현재 디렉터리에 있는 파일 `my_wallet_name.addr`과 `my_wallet_name.pk`에서 로드됩니다.

이 코드를 실행하면(파이브 인터프리터를 호출하여) 지갑 스마트 컨트랙트의 주소와 동일한 목적지를 가진 외부 메시지를 생성하고, 올바른 Ed25519 서명, 시퀀스 번호, 임의의 값을 첨부하고 임의의 페이로드가 포함된 지갑 스마트 컨트랙트의 내부 메시지를 `dest_addr`에 표시된 스마트 컨트랙트로 봉투에 넣어 전송합니다. 스마트 콘트랙트가 이 외부 메시지를 수신하고 처리할 때, 먼저 서명과 시퀀스 번호를 확인합니다. 서명과 시퀀스 번호가 맞으면 외부 메시지를 수락하고, 임베드된 내부 메시지를 자신으로부터 의도한 목적지로 전송하며, 영구 데이터의 시퀀스 번호를 증가시킵니다(이는 이 샘플 지갑 스마트 컨트랙트 코드가 실제 지갑 애플리케이션에서 사용될 경우를 대비해 리플레이 공격을 방지하기 위한 간단한 조치입니다).

물론 진정한 TON 블록체인 지갑 애플리케이션은 위에서 설명한 모든 중간 단계를 숨길 것입니다. 먼저 사용자에게 새로운 스마트 콘트랙트의 주소를 전달하고, 다른 지갑이나 암호화폐 거래소로부터 표시된 주소(반송이 불가능한 사용자 친화적인 형태로 표시됨)로 일부 자금을 이체하도록 요청한 다음, 현재 잔액을 표시하고 사용자가 원하는 다른 주소로 자금을 이체할 수 있는 간단한 인터페이스를 제공할 것입니다. (이 문서의 목적은 사용자 친화적인 지갑 애플리케이션 대신 라이트 클라이언트를 사용하는 방법을 설명하는 것이 아니라, 새로운 스마트 컨트랙트를 생성하고 TON 블록체인 테스트 네트워크를 실험하는 방법을 설명하는 것입니다).

마지막으로 한 가지 더 말씀드리겠습니다: 위의 예시에서는 기본 워크체인(워크체인 0)에서 스마트 콘트랙트를 사용했습니다. 마스터체인(워크체인 -1)에서도 첫 번째 인자로 0 대신 워크체인 식별자 -1을 `new-wallet.fif`에 전달하면 정확히 동일한 방식으로 작동할 것입니다. 유일한 차이점은 기본 워크체인의 처리 및 저장 수수료가 마스터체인보다 100~1,000배 낮다는 것입니다. 검증인 선거 스마트 콘트랙트와 같은 일부 스마트 콘트랙트는 마스터체인 스마트 콘트랙트에서만 전송을 허용하므로, 자신의 검증인을 대신하여 지분을 만들고 선거에 참여하려면 마스터체인에 지갑이 있어야 합니다.
