# ADNL TCP - 라이트서버

이것은 TON 네트워크의 모든 상호 작용이 구축되는 로우 레벨 프로토콜로, 모든 프로토콜 위에서 작동할 수 있지만 가장 자주 사용되는 프로토콜은 TCP와 UDP입니다. UDP는 노드 간의 통신에 사용되며, TCP는 라이트 서버와의 통신에 사용됩니다.

이제 TCP를 통해 실행되는 ADNL을 분석하고 라이트 서버와 직접 상호 작용하는 방법을 배워보겠습니다.

TCP 버전의 ADNL에서 네트워크 노드는 공개 키 ed25519를 주소로 사용하고 타원 곡선 디피-헬만 절차(ECDH)를 사용하여 얻은 공유 키를 사용하여 연결을 설정합니다.

## 패킷 구조

핸드셰이크를 제외한 각 ADNL TCP 패킷은 다음과 같은 구조를 가집니다:

- 리틀 엔디안(N) 단위의 4바이트 패킷 크기
- 32바이트 논스 [[?]](## "체크섬 공격으로부터 보호하기 위한 임의의 바이트")
- (N - 64) 페이로드 바이트
- 논스 및 페이로드의 32바이트 SHA256 체크섬

크기를 포함한 전체 패킷은 **AES-CTR**로 암호화됩니다.
복호화 후에는 체크섬이 데이터와 일치하는지 확인해야 하며, 이를 확인하려면 직접 체크섬을 계산하고 그 결과를 패킷에 있는 것과 비교하기만 하면 됩니다.

핸드셰이크 패킷은 예외로, 부분적으로 암호화되지 않은 형태로 전송되며 다음 장에서 설명합니다.

## 연결 설정하기

연결을 설정하려면 서버의 IP, 포트, 공개 키를 알고 있어야 하며, 자체 개인 및 공개 키 ed25519를 생성해야 합니다.

IP, 포트, 키와 같은 공용 서버 데이터는 [global config](https://ton-blockchain.github.io/global.config.json)에서 얻을 수 있습니다. 설정의 IP가 숫자 형식인 경우 [이 도구](https://www.browserling.com/tools/dec-to-ip)를 사용하여 일반 형식으로 가져올 수 있습니다. 구성의 공개 키는 base64 형식으로 되어 있습니다.

클라이언트는 160개의 무작위 바이트를 생성하며, 이 중 일부는 당사자가 AES 암호화의 기초로 사용합니다.

이 중 2개의 영구 AES-CTR 암호가 생성되어 핸드셰이크 후 당사자가 메시지를 암호화/복호화하는 데 사용됩니다.

- 암호 A - 키 0 - 31 바이트, iv 64 - 79 바이트
- 암호 B - 키 32 - 63 바이트, iv 80 - 95 바이트

암호는 이 순서대로 적용됩니다:

- 암호 A는 서버가 보내는 메시지를 암호화하는 데 사용됩니다.
- 암호 A는 클라이언트에서 수신된 메시지를 해독하는 데 사용됩니다.
- 암호 B는 클라이언트가 보내는 메시지를 암호화하는 데 사용됩니다.
- 암호 B는 서버에서 수신된 메시지를 해독하는 데 사용됩니다.

연결을 설정하려면 클라이언트는 다음이 포함된 핸드셰이크 패킷을 보내야 합니다:

- [32바이트] **서버 키 ID** [[세부 정보]](#getting-key-id)
- [32바이트] **공개 키는 ed25519**입니다.
- [32바이트] **160바이트의 SHA256 해시**\*\*
- [160바이트] **160바이트 암호화** [[세부 정보]](#핸드셰이크-패킷-데이터-암호화)

핸드셰이크 패킷을 수신하면 서버는 동일한 작업을 수행하여 ECDH 키를 수신하고 160바이트를 해독한 후 2개의 영구 키를 생성합니다. 모든 것이 정상적으로 작동하면 서버는 페이로드가 없는 빈 ADNL 패킷으로 응답하여 영구 암호 중 하나를 사용하여 해독해야 하는 패킷(및 후속 패킷)을 해독합니다.

이 시점부터 연결이 설정된 것으로 간주할 수 있습니다.

연결이 설정되면 정보 수신을 시작할 수 있으며, TL 언어를 사용하여 데이터를 직렬화할 수 있습니다.

[TL에 대한 자세한 정보](/개발/데이터-포맷/tl)

## 핑&퐁

핑 패킷은 5초에 한 번씩 전송하는 것이 가장 좋습니다. 이는 데이터가 전송되지 않는 동안 연결을 유지하는 데 필요하며, 그렇지 않으면 서버가 연결을 종료할 수 있습니다.

핑 패킷은 다른 모든 패킷과 마찬가지로 [위](#패킷구조)에서 설명한 표준 스키마에 따라 구축되며 요청 ID와 핑 ID를 페이로드 데이터로 전달합니다.

여기](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L35)에서 핑 요청에 대해 원하는 스키마를 찾아
`crc32_IEEE("tcp.ping random_id:long = tcp.Pong")`로 스키마 아이디를 계산해 보겠습니다. 작은 엔디안 바이트로 변환하면 **9a2b084d**가 됩니다.

따라서 ADNL 핑 패킷은 다음과 같은 모양이 됩니다:

- 4바이트의 패킷 크기(리틀 엔디안) -> 64 + (4+8) = **76**.
- 32바이트 논스 -> 랜덤 32바이트
- 4바이트의 ID TL 스키마 -> **9a2b084d**
- 8바이트의 요청 ID -> 임의의 uint64 숫자
- 논스 및 페이로드의 32바이트 SHA256 체크섬

패킷을 보내고 [tcp.pong](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L23)을 기다리면 `random_id`는 핑 패킷에서 보낸 것과 동일합니다.

## 라이트서버에서 정보 수신

블록체인에서 정보를 얻기 위한 모든 요청은 [Liteserver 쿼리](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/lite_api.tl#L83) 스키마로 래핑되며, 이는 다시 [ADNL 쿼리](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/lite_api.tl#L22) 스키마로 래핑됩니다.

LiteQuery:
`liteServer.query 데이터:바이트 = 객체`, id **df068c79**

ADNLQuery:
`adnl.message.query 쿼리_id:int256 쿼리:바이트 = adnl.Message`, id **7af98bb4**

LiteQuery는 `query:bytes`로 ADNLQuery 내부에 전달되고, 최종 쿼리는 `data:bytes`로 LiteQuery 내부에 전달됩니다.

[TL에서 인코딩 바이트 구문 분석](/개발/데이터-포맷/tl)

### getMasterchainInfo

이제 라이트 API용 TL 패킷을 생성하는 방법을 이미 알고 있으므로, 현재 TON 마스터체인 블록에 대한 정보를 요청할 수 있습니다.
마스터체인 블록은 정보가 필요한 상태(순간)를 나타내는 입력 파라미터로 여러 추가 요청에서 사용됩니다.

필요한 TL 스키마](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/lite_api.tl#L60)를 찾고 ID를 계산하여 패킷을 빌드합니다:

- 4바이트의 패킷 크기(리틀 엔디안) -> 64 + (4+32+(1+4+(1+4+3)+3)) = **116**.
- 32바이트 논스 -> 랜덤 32바이트
- 4바이트의 ID ADNLQuery 스키마 -> **7af98bb4**
- 32바이트 `query_id:int256` -> 임의 32바이트
- - 1바이트 배열 크기 -> **12**
- - 4바이트의 ID 라이트쿼리 스키마 -> **df068c79**
- - - 1바이트 배열 크기 -> **4**
- - - 4바이트의 ID getMasterchainInfo 스키마 -> **2ee6b589**
- - - 0 바이트의 패딩 3 개 (8로 정렬)
- - 0 바이트의 패딩 3 개 (16으로 정렬)
- 논스 및 페이로드의 32바이트 체크섬 SHA256

16진수 패킷 예제:

```
74000000                                                             -> packet size (116)
5fb13e11977cb5cff0fbf7f23f674d734cb7c4bf01322c5e6b928c5d8ea09cfd     -> nonce
  7af98bb4                                                           -> ADNLQuery
  77c1545b96fa136b8e01cc08338bec47e8a43215492dda6d4d7e286382bb00c4   -> query_id
    0c                                                               -> array size
    df068c79                                                         -> LiteQuery
      04                                                             -> array size
      2ee6b589                                                       -> getMasterchainInfo
      000000                                                         -> 3 bytes of padding
    000000                                                           -> 3 bytes of padding
ac2253594c86bd308ed631d57a63db4ab21279e9382e416128b58ee95897e164     -> sha256
```

이에 대한 응답으로 마지막:[ton.blockIdExt](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/tonlib_api.tl#L51) state_root_hash:int256 및 init:[tonNode.zeroStateIdExt](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L359)로 구성된 [liteServer.masterchainInfo](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/lite_api.tl#L30)를 수신할 것으로 예상합니다.

수신된 패킷은 전송된 패킷과 동일한 방식으로 역직렬화되며, 알고리즘은 동일하지만 응답이 [ADNLAnswer](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/lite_api.tl#L23)로만 래핑된다는 점을 제외하면 반대 방향으로 역직렬화됩니다.

응답을 디코딩한 후 형식의 패킷을 얻습니다:

```
20010000                                                                  -> packet size (288)
5558b3227092e39782bd4ff9ef74bee875ab2b0661cf17efdfcd4da4e53e78e6          -> nonce
  1684ac0f                                                                -> ADNLAnswer
  77c1545b96fa136b8e01cc08338bec47e8a43215492dda6d4d7e286382bb00c4        -> query_id (identical to request)
    b8                                                                    -> array size
    81288385                                                              -> liteServer.masterchainInfo
                                                                          last:tonNode.blockIdExt
        ffffffff                                                          -> workchain:int
        0000000000000080                                                  -> shard:long
        27405801                                                          -> seqno:int   
        e585a47bd5978f6a4fb2b56aa2082ec9deac33aaae19e78241b97522e1fb43d4  -> root_hash:int256
        876851b60521311853f59c002d46b0bd80054af4bce340787a00bd04e0123517  -> file_hash:int256
      8b4d3b38b06bb484015faf9821c3ba1c609a25b74f30e1e585b8c8e820ef0976    -> state_root_hash:int256
                                                                          init:tonNode.zeroStateIdExt 
        ffffffff                                                          -> workchain:int
        17a3a92992aabea785a7a090985a265cd31f323d849da51239737e321fb05569  -> root_hash:int256      
        5e994fcf4d425c0a6ce6a792594b7173205f740a39cd56f537defd28b48a0f6e  -> file_hash:int256
    000000                                                                -> 3 bytes of padding
520c46d1ea4daccdf27ae21750ff4982d59a30672b3ce8674195e8a23e270d21          -> sha256
```

### runSmcMethod

마스터체인 블록을 가져오는 방법을 이미 알고 있으므로 이제 라이트 서버 메서드를 호출할 수 있습니다.
스마트 컨트랙트에서 함수를 호출하고 결과를 반환하는 메서드인 **runSmcMethod**를 분석해 보겠습니다. 여기서 우리는 [TL-B](/develop/data-formats/tl-b), [Cell](/develop/data-formats/cell-boc#cell), [BoC](/develop/data-formats/cell-boc#bag-of-cells) 같은 새로운 데이터 타입을 이해해야 합니다.

스마트 컨트랙트 방식을 실행하려면 TL 스키마를 사용하여 요청을 작성하고 전송해야 합니다:

```tlb
liteServer.runSmcMethod mode:# id:tonNode.blockIdExt account:liteServer.accountId method_id:long params:bytes = liteServer.RunMethodResult
```

그리고 스키마로 응답을 기다립니다:

```tlb
liteServer.runMethodResult mode:# id:tonNode.blockIdExt shardblk:tonNode.blockIdExt shard_proof:mode.0?bytes proof:mode.0?bytes state_proof:mode.1?bytes init_c7:mode.3?bytes lib_extras:mode.4?bytes exit_code:int result:mode.2?bytes = liteServer.RunMethodResult;
```

요청에는 다음 필드가 표시됩니다:

1. mode:# - 응답에서 보려는 항목의 uint32 비트마스크(예: `result:mode.2?bytes`는 인덱스가 2인 비트가 1로 설정된 경우에만 응답에 표시됩니다.
2. id:tonNode.blockIdExt - 이전 장에서 얻은 마스터 블록 상태입니다.
3. 계정:[liteServer.accountId](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/lite_api.tl#L27) - 워크체인 및 스마트 컨트랙트 주소 데이터입니다.
4. method_id:long - 8바이트, 호출된 메서드를 대신하여 XMODEM 테이블이 있는 crc16이 쓰여진 + 비트 17이 설정된 [[계산]](https://github.com/xssnick/tonutils-go/blob/88f83bc3554ca78453dd1a42e9e9ea82554e3dd2/ton/runmethod.go#L16)
5. params:바이트 - 메서드를 호출할 인수를 포함하는 [BoC](/develop/data-formats/cell-boc#bag-of-cells)에 직렬화된 [Stack](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/crypto/block/block.tlb#L783). [[구현 예제]](https://github.com/xssnick/tonutils-go/blob/88f83bc3554ca78453dd1a42e9e9ea82554e3dd2/tlb/stack.go)

예를 들어 `result:mode.2?bytes`만 있으면 모드가 0b100, 즉 4가 됩니다. 이에 대한 응답으로 다음과 같은 결과를 얻게 됩니다:

1. 모드:# -> 전송된 내용 - 4.
2. id:tonNode.blockIdExt -> 메서드가 실행된 마스터 블록입니다.
3. shardblk:tonNode.blockIdExt -> 컨트랙트 계정이 위치한 블록을 샤드합니다.
4. exit_code:int -> 메서드 실행 시 종료 코드인 4바이트입니다. 모든 것이 성공하면 = 0이고, 그렇지 않으면 예외 코드와 같습니다.
5. 결과:모드.2?바이트 -> [스택](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/crypto/block/block.tlb#L783) 메서드가 반환한 값을 포함하는 [BoC](/develop/data-formats/cell-boc#bag-of-cells)로 직렬화됩니다.

컨트랙트 `EQBL2_3lMiyywU17g-or8N7v9hDmPCpttzBPE2isF2GTzpK4`의 `a2` 메서드에서 호출을 분석하고 결과를 가져와 보겠습니다:

메서드 코드의 FunC:

```func
(cell, cell) a2() method_id {
  cell a = begin_cell().store_uint(0xAABBCC8, 32).end_cell();
  cell b = begin_cell().store_uint(0xCCFFCC1, 32).end_cell();
  return (a, b);
}
```

요청을 작성하세요:

- 모드`= 4, 결과 ->`04000000\`만 필요합니다.
- `id` = 실행 결과 getMasterchainInfo
- 계정`= 워크체인 0(4바이트`00000000`), int256 [컨트랙트 주소에서 얻은](/개발/데이터-포맷/tl-b#주소), 즉 32바이트 `4bdbfde5322cb2c14d7b83ea2bf0deeff610e63c2a6db7304f1368ac176193ce\`로 구성됩니다.
- method_id`= [computed](https://github.com/xssnick/tonutils-go/blob/88f83bc3554ca78453dd1a42e9e9ea82554e3dd2/ton/runmethod.go#L16) id from`a2`->`0a2e010000000000\`
- params:bytes` = 이 메서드는 입력 매개변수를 허용하지 않으므로 [BoC](/develop/data-formats/cell-boc#bag-of-cells)에서 직렬화된 빈 스택(`000000`, 셀 3바이트 - 스택 깊이 0)을 전달해야 합니다 -> `b5ee9c72010101010005000006000000`-> 바이트로 직렬화하고`10b5ee9c7241010101000500000600000000\` 0x10 - 크기, 마지막 3바이트 - 패딩을 얻습니다.

이에 대한 답변은 다음과 같습니다:

- `모드:#` -> 흥미롭지 않음
- `id:tonNode.blockIdExt` -> 흥미롭지 않음
- `shardblk:tonNode.blockIdExt` -> 흥미롭지 않음
- `exit_code:int` -> 실행에 성공하면 0입니다.
- 결과:모드.2?바이트\` -> [스택](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/crypto/block/block.tlb#L783) 메서드가 반환한 데이터를 [BoC](/develop/data-formats/cell-boc#bag-of-cells) 형식의 데이터로 압축을 해제합니다.

결과`안에`b5ee9c7201010501001b000208000002030102020203030400080ccffcc1000000080aabbcc8\`이 들어있는 [BoC](/develop/data-formats/cell-boc#bag-of-cells) 데이터를 받았습니다. 역직렬화하면 셀을 얻을 수 있습니다:

```json
32[00000203] -> {
  8[03] -> {
    0[],
    32[0AABBCC8]
  },
  32[0CCFFCC1]
}
```

이를 구문 분석하면 FunC 메서드가 반환하는 셀 유형의 값 2개를 얻을 수 있습니다.
루트 셀 `000002`의 처음 3바이트는 스택의 깊이, 즉 2입니다. 즉, 이 메서드는 2개의 값을 반환합니다.

구문 분석을 계속하면 다음 8비트(1바이트)는 현재 스택 레벨의 값 유형입니다. 일부 유형의 경우 2바이트가 걸릴 수 있습니다. 가능한 옵션은 [스키마](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/crypto/block/block.tlb#L766)에서 확인할 수 있습니다.
우리의 경우 `03`이 있습니다:

```tlb
vm_stk_cell#03 cell:^Cell = VmStackValue;
```

따라서 우리 값의 유형은 셀이며 스키마에 따르면 값 자체를 참조로 저장합니다. 하지만 스택 요소 저장 스키마를 살펴보면 다음과 같습니다:

```tlb
vm_stk_cons#_ {n:#} rest:^(VmStackList n) tos:VmStackValue = VmStackList (n + 1);
```

첫 번째 링크인 `rest:^(VmStackList n)`은 스택에서 다음 값의 셀이고, `tos:VmStackValue` 값이 두 번째이므로 값을 얻으려면 두 번째 링크, 즉 `32[0CCFFCC1]`을 읽어야 하며, 이것이 컨트랙트가 반환한 첫 번째 셀입니다.

이제 더 깊이 들어가 스택의 두 번째 요소를 가져와 첫 번째 링크를 살펴볼 수 있습니다:

```json
8[03] -> {
    0[],
    32[0AABBCC8]
  }
```

동일한 과정을 반복합니다. 첫 번째 8비트 = `03`, 즉 다시 셀입니다. 두 번째 참조는 `32[0AABBCC8]` 값이며 스택 깊이가 2이므로 패스를 완료합니다. 총 2개의 값, 즉 `32[0CCFFCC1]`과 `32[0AABBCC8`이 컨트랙트에 의해 반환됩니다.

역순이라는 점에 유의하세요. 같은 방식으로 함수를 호출할 때 인수를 전달할 때도 FunC 코드에 표시된 것과 역순으로 전달해야 합니다.

[구현 예시](https://github.com/xssnick/tonutils-go/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/ton/runmethod.go#L24)

### 계정 상태 가져오기

잔액, 코드, 컨트랙트 데이터와 같은 계정 상태 데이터를 가져오려면 [getAccountState](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/lite_api.tl#L68)를 사용하면 됩니다. 요청을 위해서는 [fresh 마스터 블록](#getmasterchaininfo)과 계정 주소가 필요합니다. 이에 대한 응답으로 TL 구조 [AccountState](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/lite_api.tl#L38)를 받게 됩니다.

AccountState TL 스키마를 분석해 보겠습니다:

```tlb
liteServer.accountState id:tonNode.blockIdExt shardblk:tonNode.blockIdExt shard_proof:bytes proof:bytes state:bytes = liteServer.AccountState;
```

1. 'id\` - 데이터를 가져온 마스터 블록입니다.
2. 'shardblk\` - 데이터를 수신한 계정이 위치한 워크체인 샤드 블록입니다.
3. `shard_proof` - 샤드 블록의 머클 증명.
4. '증명' - 계정 상태의 머클 증명.
5. 상태\` - [BoC](/개발/데이터-포맷/셀-boc#백오브셀) TL-B [계정 상태 체계](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/crypto/block/block.tlb#L232).

이 모든 데이터 중에서 우리에게 필요한 것은 주에 있으며, 우리는 그것을 분석할 것입니다.

예를 들어, 계정 `EQAhE3sLxHZpsyZ_HecMuwzvXHKLjYx4kEUehhOy2JmCcHCT`의 상태는 (이 글을 작성하는 현재) `상태`가 되어 있다고 가정합니다:

```hex
b5ee9c720102350100051e000277c0021137b0bc47669b3267f1de70cbb0cef5c728b8d8c7890451e8613b2d899827026a886043179d3f6000006e233be8722201d7d239dba7d818134001020114ff00f4a413f4bcf2c80b0d021d0000000105036248628d00000000e003040201cb05060013a03128bb16000000002002012007080043d218d748bc4d4f4ff93481fd41c39945d5587b8e2aa2d8a35eaf99eee92d9ba96004020120090a0201200b0c00432c915453c736b7692b5b4c76f3a90e6aeec7a02de9876c8a5eee589c104723a18020004307776cd691fbe13e891ed6dbd15461c098b1b95c822af605be8dc331e7d45571002000433817dc8de305734b0c8a3ad05264e9765a04a39dbe03dd9973aa612a61f766d7c02000431f8c67147ceba1700d3503e54c0820f965f4f82e5210e9a3224a776c8f3fad1840200201200e0f020148101104daf220c7008e8330db3ce08308d71820f90101d307db3c22c00013a1537178f40e6fa1f29fdb3c541abaf910f2a006f40420f90101d31f5118baf2aad33f705301f00a01c20801830abcb1f26853158040f40e6fa120980ea420c20af2670edff823aa1f5340b9f2615423a3534e2a2d2b2c0202cc12130201201819020120141502016616170003d1840223f2980bc7a0737d0986d9e52ed9e013c7a21c2b2f002d00a908b5d244a824c8b5d2a5c0b5007404fc02ba1b04a0004f085ba44c78081ba44c3800740835d2b0c026b500bc02f21633c5b332781c75c8f20073c5bd0032600201201a1b02012020210115bbed96d5034705520db3c8340201481c1d0201201e1f0173b11d7420c235c6083e404074c1e08075313b50f614c81e3d039be87ca7f5c2ffd78c7e443ca82b807d01085ba4d6dc4cb83e405636cf0069006031003daeda80e800e800fa02017a0211fc8080fc80dd794ff805e47a0000e78b64c00015ae19574100d56676a1ec40020120222302014824250151b7255b678626466a4610081e81cdf431c24d845a4000331a61e62e005ae0261c0b6fee1c0b77746e102d0185b5599b6786abe06fedb1c68a2270081e8f8df4a411c4605a400031c34410021ae424bae064f613990039e2ca840090081e886052261c52261c52265c4036625ccd88302d02012026270203993828290111ac1a6d9e2f81b609402d0015adf94100cc9576a1ec1840010da936cf0557c1602d0015addc2ce0806ab33b50f6200220db3c02f265f8005043714313db3ced542d34000ad3ffd3073004a0db3c2fae5320b0f26212b102a425b3531cb9b0258100e1aa23a028bcb0f269820186a0f8010597021110023e3e308e8d11101fdb3c40d778f44310bd05e254165b5473e7561053dcdb3c54710a547abc2e2f32300020ed44d0d31fd307d307d33ff404f404d10048018e1a30d20001f2a3d307d3075003d70120f90105f90115baf2a45003e06c2170542013000c01c8cbffcb0704d6db3ced54f80f70256e5389beb198106e102d50c75f078f1b30542403504ddb3c5055a046501049103a4b0953b9db3c5054167fe2f800078325a18e2c268040f4966fa52094305303b9de208e1638393908d2000197d3073016f007059130e27f080705926c31e2b3e63006343132330060708e2903d08308d718d307f40430531678f40e6fa1f2a5d70bff544544f910f2a6ae5220b15203bd14a1236ee66c2232007e5230be8e205f03f8009322d74a9802d307d402fb0002e83270c8ca0040148040f44302f0078e1771c8cb0014cb0712cb0758cf0158cf1640138040f44301e201208e8a104510344300db3ced54925f06e234001cc8cb1fcb07cb07cb3ff400f400c9
```

[이 BoC](/개발/데이터-형식/cell-boc#bag-of-cells)를 파싱하여 다음을 얻습니다.

<details>
  <summary>대형 셀</summary>

```json
473[C0021137B0BC47669B3267F1DE70CBB0CEF5C728B8D8C7890451E8613B2D899827026A886043179D3F6000006E233BE8722201D7D239DBA7D818130_] -> {
  80[FF00F4A413F4BCF2C80B] -> {
    2[0_] -> {
      4[4_] -> {
        8[CC] -> {
          2[0_] -> {
            13[D180],
            141[F2980BC7A0737D0986D9E52ED9E013C7A218] -> {
              40[D3FFD30730],
              48[01C8CBFFCB07]
            }
          },
          6[64] -> {
            178[00A908B5D244A824C8B5D2A5C0B5007404FC02BA1B048_],
            314[085BA44C78081BA44C3800740835D2B0C026B500BC02F21633C5B332781C75C8F20073C5BD00324_]
          }
        },
        2[0_] -> {
          2[0_] -> {
            84[BBED96D5034705520DB3C_] -> {
              112[C8CB1FCB07CB07CB3FF400F400C9]
            },
            4[4_] -> {
              2[0_] -> {
                241[AEDA80E800E800FA02017A0211FC8080FC80DD794FF805E47A0000E78B648_],
                81[AE19574100D56676A1EC0_]
              },
              458[B11D7420C235C6083E404074C1E08075313B50F614C81E3D039BE87CA7F5C2FFD78C7E443CA82B807D01085BA4D6DC4CB83E405636CF0069004_] -> {
                384[708E2903D08308D718D307F40430531678F40E6FA1F2A5D70BFF544544F910F2A6AE5220B15203BD14A1236EE66C2232]
              }
            }
          },
          2[0_] -> {
            2[0_] -> {
              323[B7255B678626466A4610081E81CDF431C24D845A4000331A61E62E005AE0261C0B6FEE1C0B77746E0_] -> {
                128[ED44D0D31FD307D307D33FF404F404D1]
              },
              531[B5599B6786ABE06FEDB1C68A2270081E8F8DF4A411C4605A400031C34410021AE424BAE064F613990039E2CA840090081E886052261C52261C52265C4036625CCD882_] -> {
                128[ED44D0D31FD307D307D33FF404F404D1]
              }
            },
            4[4_] -> {
              2[0_] -> {
                65[AC1A6D9E2F81B6090_] -> {
                  128[ED44D0D31FD307D307D33FF404F404D1]
                },
                81[ADF94100CC9576A1EC180_]
              },
              12[993_] -> {
                50[A936CF0557C14_] -> {
                  128[ED44D0D31FD307D307D33FF404F404D1]
                },
                82[ADDC2CE0806AB33B50F60_]
              }
            }
          }
        }
      },
      872[F220C7008E8330DB3CE08308D71820F90101D307DB3C22C00013A1537178F40E6FA1F29FDB3C541ABAF910F2A006F40420F90101D31F5118BAF2AAD33F705301F00A01C20801830ABCB1F26853158040F40E6FA120980EA420C20AF2670EDFF823AA1F5340B9F2615423A3534E] -> {
        128[DB3C02F265F8005043714313DB3CED54] -> {
          128[ED44D0D31FD307D307D33FF404F404D1],
          112[C8CB1FCB07CB07CB3FF400F400C9]
        },
        128[ED44D0D31FD307D307D33FF404F404D1],
        40[D3FFD30730],
        640[DB3C2FAE5320B0F26212B102A425B3531CB9B0258100E1AA23A028BCB0F269820186A0F8010597021110023E3E308E8D11101FDB3C40D778F44310BD05E254165B5473E7561053DCDB3C54710A547ABC] -> {
          288[018E1A30D20001F2A3D307D3075003D70120F90105F90115BAF2A45003E06C2170542013],
          48[01C8CBFFCB07],
          504[5230BE8E205F03F8009322D74A9802D307D402FB0002E83270C8CA0040148040F44302F0078E1771C8CB0014CB0712CB0758CF0158CF1640138040F44301E2],
          856[DB3CED54F80F70256E5389BEB198106E102D50C75F078F1B30542403504DDB3C5055A046501049103A4B0953B9DB3C5054167FE2F800078325A18E2C268040F4966FA52094305303B9DE208E1638393908D2000197D3073016F007059130E27F080705926C31E2B3E63006] -> {
            112[C8CB1FCB07CB07CB3FF400F400C9],
            384[708E2903D08308D718D307F40430531678F40E6FA1F2A5D70BFF544544F910F2A6AE5220B15203BD14A1236EE66C2232],
            504[5230BE8E205F03F8009322D74A9802D307D402FB0002E83270C8CA0040148040F44302F0078E1771C8CB0014CB0712CB0758CF0158CF1640138040F44301E2],
            128[8E8A104510344300DB3CED54925F06E2] -> {
              112[C8CB1FCB07CB07CB3FF400F400C9]
            }
          }
        }
      }
    }
  },
  114[0000000105036248628D00000000C_] -> {
    7[CA] -> {
      2[0_] -> {
        2[0_] -> {
          266[2C915453C736B7692B5B4C76F3A90E6AEEC7A02DE9876C8A5EEE589C104723A1800_],
          266[07776CD691FBE13E891ED6DBD15461C098B1B95C822AF605BE8DC331E7D45571000_]
        },
        2[0_] -> {
          266[3817DC8DE305734B0C8A3AD05264E9765A04A39DBE03DD9973AA612A61F766D7C00_],
          266[1F8C67147CEBA1700D3503E54C0820F965F4F82E5210E9A3224A776C8F3FAD18400_]
        }
      },
      269[D218D748BC4D4F4FF93481FD41C39945D5587B8E2AA2D8A35EAF99EEE92D9BA96000]
    },
    74[A03128BB16000000000_]
  }
}
```

</details>

이제 TL-B 구조에 따라 셀을 파싱해야 합니다:

```tlb
account_none$0 = Account;

account$1 addr:MsgAddressInt storage_stat:StorageInfo
          storage:AccountStorage = Account;
```

저희의 구조는 다음과 같은 다른 구조를 참조합니다:

```tlb
anycast_info$_ depth:(#<= 30) { depth >= 1 } rewrite_pfx:(bits depth) = Anycast;
addr_std$10 anycast:(Maybe Anycast) workchain_id:int8 address:bits256  = MsgAddressInt;
addr_var$11 anycast:(Maybe Anycast) addr_len:(## 9) workchain_id:int32 address:(bits addr_len) = MsgAddressInt;
   
storage_info$_ used:StorageUsed last_paid:uint32 due_payment:(Maybe Grams) = StorageInfo;
storage_used$_ cells:(VarUInteger 7) bits:(VarUInteger 7) public_cells:(VarUInteger 7) = StorageUsed;
  
account_storage$_ last_trans_lt:uint64 balance:CurrencyCollection state:AccountState = AccountStorage;

currencies$_ grams:Grams other:ExtraCurrencyCollection = CurrencyCollection;
           
var_uint$_ {n:#} len:(#< n) value:(uint (len * 8)) = VarUInteger n;
var_int$_ {n:#} len:(#< n) value:(int (len * 8)) = VarInteger n;
nanograms$_ amount:(VarUInteger 16) = Grams;  
           
account_uninit$00 = AccountState;
account_active$1 _:StateInit = AccountState;
account_frozen$01 state_hash:bits256 = AccountState;
```

보시다시피 셀에는 많은 데이터가 포함되어 있지만 주요 사례를 분석하고 균형을 잡을 것입니다. 나머지도 비슷한 방식으로 분석할 수 있습니다.

구문 분석을 시작해 보겠습니다. 루트 셀 데이터에 있습니다:

```
C0021137B0BC47669B3267F1DE70CBB0CEF5C728B8D8C7890451E8613B2D899827026A886043179D3F6000006E233BE8722201D7D239DBA7D818130_
```

바이너리 형식으로 변환하여 가져옵니다:

```
11000000000000100001000100110111101100001011110001000111011001101001101100110010011001111111000111011110011100001100101110110000110011101111010111000111001010001011100011011000110001111000100100000100010100011110100001100001001110110010110110001001100110000010011100000010011010101000100001100000010000110001011110011101001111110110000000000000000000000110111000100011001110111110100001110010001000100000000111010111110100100011100111011011101001111101100000011000000100110
```

기본 TL-B 구조를 살펴보면, `account_none$0` 또는 `account$1`의 두 가지 옵션이 있음을 알 수 있습니다. 기호 $ 뒤에 선언된 접두사(이 경우 1비트)를 읽으면 어떤 옵션이 있는지 이해할 수 있습니다. 0이 있으면 `account_none`, 1이 있으면 `account`입니다.

위 데이터의 첫 번째 비트는 1이므로 `account$1`로 작업하고 스키마를 사용합니다:

```tlb
account$1 addr:MsgAddressInt storage_stat:StorageInfo
          storage:AccountStorage = Account;
```

다음으로 `addr:MsgAddressInt`가 있는데, MsgAddressInt에는 몇 가지 옵션이 있습니다:

```tlb
addr_std$10 anycast:(Maybe Anycast) workchain_id:int8 address:bits256  = MsgAddressInt;
addr_var$11 anycast:(Maybe Anycast) addr_len:(## 9) workchain_id:int32 address:(bits addr_len) = MsgAddressInt;
```

어떤 것을 작업할지 이해하기 위해 지난번과 마찬가지로 접두사 비트를 읽고 이번에는 2 비트를 읽습니다. 이미 읽은 비트를 잘라내고 `1000000...`이 남고, 처음 2비트를 읽고 `10`을 얻는데, 이는 `addr_std$10`으로 작업하고 있음을 의미합니다.

다음으로 `anycast:(Maybe Anycast)`를 파싱해야 하는데, Maybe는 1비트를 읽어야 한다는 뜻이고, 1이면 Anycast를 읽고, 그렇지 않으면 건너뜁니다. 남은 비트는 `00000...`이고, 1비트를 읽으면 0이므로 애니캐스트를 건너뜁니다.

다음으로 `workchain_id: int8`이 있는데, 여기서 모든 것이 간단하며 8비트를 읽으면 워크체인 ID가 됩니다. 다음 8비트를 모두 0으로 읽으므로 워크체인은 0이 됩니다.

다음으로 `workchain_id`와 같은 방식으로 주소의 256비트인 `address:bits256`을 읽습니다. 읽으면 `21137B0BC47669B3267F1DE70CBB0CEF5C728B8D8C7890451E8613B2D8998270`이 16진수 표현으로 표시됩니다.

주소 `addr:MsgAddressInt`를 읽은 다음 기본 구조에서 `storage_stat:StorageInfo`가 있으며, 그 스키마는 다음과 같습니다:

```tlb
storage_info$_ used:StorageUsed last_paid:uint32 due_payment:(Maybe Grams) = StorageInfo;
```

먼저 스키마와 함께 `used:StorageUsed`가 나옵니다:

```tlb
storage_used$_ cells:(VarUInteger 7) bits:(VarUInteger 7) public_cells:(VarUInteger 7) = StorageUsed;
```

계정 데이터를 저장하는 데 사용되는 셀과 비트 수입니다. 각 필드는 동적 크기의 정수를 의미하지만 최대 7비트를 의미하는 '변수 정수 7'로 정의됩니다. 스키마에 따라 어떻게 배열되는지 이해할 수 있습니다:

```tlb
var_uint$_ {n:#} len:(#< n) value:(uint (len * 8)) = VarUInteger n;
```

이 경우 n은 7과 같습니다. len에는 `(#< 7)`이 있는데, 이는 최대 7까지 숫자를 담을 수 있는 비트 수를 의미합니다. 7-1=6을 2진법으로 변환하면 `110`이 되므로 길이 len = 3비트를 구할 수 있습니다. 그리고 값은 `(uint (len * 8))`입니다. 이를 결정하려면 길이의 3비트를 읽고 숫자를 구한 다음 8을 곱해야 하며, 이것이 `value`의 크기, 즉 VarUInteger의 값을 얻기 위해 읽어야 하는 비트 수가 됩니다.

셀:(VarUInteger 7)`을 읽고, 루트 셀에서 다음 비트를 가져와서 다음 16비트를 보면 `0010011010101000`이 됩니다. len의 처음 3비트를 읽으면 `001`, 즉 1이 되고, 크기(uint (1 * 8))를 얻으면 uint 8이 되고, 8비트를 읽으면 `cells`, `00110101`, 즉 10진수 형식의 53이 됩니다. bits`와 `public_cells`에 대해서도 동일한 작업을 수행합니다.

사용된:저장소사용`을 성공적으로 읽었고, 다음으로 `last_paid:uint32`가 있으며, 32비트를 읽습니다. 여기서 `due_payment:(Maybe Grams)`를 사용하면 모든 것이 간단합니다. 어쩌면 0이 될 것이므로 Grams는 건너뜁니다. 그러나 Maybe가 1이면 Grams `amount:(VarUInteger 16) = Grams\` 스키마를 보고 이미 이 스키마로 작업하는 방법을 알고 있다는 것을 즉시 이해할 수 있습니다. 지난번과 마찬가지로 7 대신 16이 있습니다.

다음으로 스키마가 있는 `storage:AccountStorage`가 있습니다:

```tlb
account_storage$_ last_trans_lt:uint64 balance:CurrencyCollection state:AccountState = AccountStorage;
```

마지막 계정 트랜잭션의 lt를 저장하는 64비트인 `last_trans_lt:uint64`를 읽습니다. 마지막으로 스키마로 표시되는 잔액입니다:

```tlb
currencies$_ grams:Grams other:ExtraCurrencyCollection = CurrencyCollection;
```

여기에서 나노톤 단위의 계정 잔액이 될 `그램:그램`을 읽습니다.
그램:그램`은 `변수 16`으로 16(이진 형식 `10000`에서 1을 빼면 `1111\`이 됨)을 저장한 다음 처음 4비트를 읽고 결과 값에 8을 곱한 다음 수신된 비트 수를 읽으면 잔액이 됩니다.

데이터에 따라 남은 비트를 분석해 보겠습니다:

```
100000000111010111110100100011100111011011101001111101100000011000000100110
```

처음 4비트인 `1000`을 읽으면 8입니다. 8\*8=64, 다음 64비트 = `0000011101011111010010001110011101101110100111110110000001100000`을 읽고 여분의 0비트를 제거하면 `11101011111010010001110011101101110100111110110000001100000`이 되며, 이는 `531223439883591776`와 같고, 나노에서 톤으로 변환하면 `531223439.883591776`이 됩니다.

이미 모든 주요 사례를 분석했기 때문에 나머지는 우리가 분석한 것과 비슷한 방식으로 얻을 수 있으므로 여기서 멈추겠습니다. 또한 TL-B 구문 분석에 대한 추가 정보는 [공식 문서](/개발/데이터-포맷/tl-b-language)에서 확인할 수 있습니다.

### 기타 방법

이제 모든 정보를 공부했으니 다른 라이트 서버 메소드에 대해서도 응답을 호출하고 처리할 수 있습니다. 같은 원리 :)

## 핸드셰이크의 추가 기술 세부 정보

### 키 ID 가져오기

키 ID는 직렬화된 TL 스키마의 SHA256 해시입니다.

키에 가장 일반적으로 사용되는 TL 스키마는 다음과 같습니다:

```tlb
pub.ed25519 key:int256 = PublicKey -- ID c6b41348
pub.aes key:int256 = PublicKey     -- ID d4adbc2d
pub.overlay name:bytes = PublicKey -- ID cb45ba34
pub.unenc data:bytes = PublicKey   -- ID 0a451fb6
pk.aes key:int256 = PrivateKey     -- ID 3751e8a5
```

예를 들어 핸드셰이크에 사용되는 ED25519 유형의 키의 경우 키 ID는
**[0xC6, 0xB4, 0x13, 0x48]** 및 **공개 키**(36바이트 배열, 접두사 + 키)의 SHA256 해시가 됩니다.

[코드 예시](https://github.com/xssnick/tonutils-go/blob/2b5e5a0e6ceaf3f28309b0833cb45de81c580acc/liteclient/crypto.go#L16)

### 핸드셰이크 패킷 데이터 암호화

핸드셰이크 패킷은 반개방 형식으로 전송되며, 160바이트만 암호화되어 영구 암호에 대한 정보가 포함되어 있습니다.

이를 암호화하려면 AES-CTR 암호가 필요하며, 이를 얻으려면 160바이트의 SHA256 해시와 [ECDH 공유 키](#getting-a-shared-key-using-ecdh)가 필요합니다.

암호는 다음과 같이 구성됩니다:

- 키 = (0 - 15바이트의 공개 키) + (16 - 31바이트의 해시)
- iv = (0 - 3 해시 바이트) + (20 - 31 공개 키 바이트)

암호가 조합된 후에는 160바이트를 암호화합니다.

[코드 예시](https://github.com/xssnick/tonutils-go/blob/2b5e5a0e6ceaf3f28309b0833cb45de81c580acc/liteclient/connection.go#L361)

### ECDH를 사용하여 공유 키 받기

공유 키를 계산하려면 개인 키와 서버의 공개 키가 필요합니다.

DH의 핵심은 개인 정보를 공개하지 않고 공유 비밀 키를 얻는 것입니다. 가장 간단한 형태로 이것이 어떻게 발생하는지 예를 들어 보겠습니다. 우리와 서버 간에 공유 키를 생성해야 한다고 가정하면 프로세스는 다음과 같습니다:

1. 6\*\*, **7**와 같은 비밀 번호와 공개 번호를 생성합니다.
2. 서버는 **5**, **15**와 같은 비밀 번호와 공개 번호를 생성합니다.
3. 서버와 공개 번호를 교환하고 **7**을 서버로 보내면 서버는 **15**을 보냅니다.
4. 계산합니다: **7^6 mod 15 = 4**
5. 서버가 계산합니다: **7^5 mod 15 = 7**
6. 수신된 번호를 교환하여 서버에 **4**를 주면 서버는 **7**를 줍니다.
7. 7^6 mod 15 = 4\*\*를 계산합니다.
8. 서버가 계산합니다: **4^5 mod 15 = 4**
9. 공유 키 = **4**

ECDH 자체에 대한 자세한 설명은 단순화를 위해 생략하겠습니다. 곡선에서 공통점을 찾아 비공개와 공개 키 2개를 사용하여 계산합니다. 관심이 있으시다면 별도로 읽어보시는 것이 좋습니다.

[코드 예시](https://github.com/xssnick/tonutils-go/blob/2b5e5a0e6ceaf3f28309b0833cb45de81c580acc/liteclient/crypto.go#L32)

## 참조

여기 [Oleg Baranov](https://github.com/xssnick)의 [원본 기사 링크](https://github.com/xssnick/ton-deep-doc/blob/master/ADNL-TCP-Liteserver.md)가 있습니다.
