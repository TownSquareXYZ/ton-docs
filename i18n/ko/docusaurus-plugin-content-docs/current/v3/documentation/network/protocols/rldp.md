# RLDP

구현:

- https://github.com/ton-blockchain/ton/tree/master/rldp
- https://github.com/ton-blockchain/ton/tree/master/rldp2
- https://github.com/ton-blockchain/ton/tree/master/rldp-http-proxy

## 개요

RLDP(Reliable Large Datagram Protocol)는 ADNL UDP 위에서 실행되는 프로토콜로, 큰 데이터 블록을 전송하는 데 사용되며 다른 쪽의 확인 패킷을 대체하는 전방 오류 정정(FEC) 알고리즘을 포함합니다.
이를 통해 더 많은 트래픽을 소비하지만 네트워크 구성 요소 간에 데이터를 더 효율적으로 전송할 수 있습니다.

RLDP는 다른 노드에서 블록을 다운로드하고 데이터를 전송하거나, TON 웹사이트와 TON Storage에 접근하는 등 TON 인프라 전반에서 사용됩니다.

## 프로토콜

RLDP는 통신을 위해 다음 TL 구조를 사용합니다:

```tlb
fec.raptorQ data_size:int symbol_size:int symbols_count:int = fec.Type;
fec.roundRobin data_size:int symbol_size:int symbols_count:int = fec.Type;
fec.online data_size:int symbol_size:int symbols_count:int = fec.Type;

rldp.messagePart transfer_id:int256 fec_type:fec.Type part:int total_size:long seqno:int data:bytes = rldp.MessagePart;
rldp.confirm transfer_id:int256 part:int seqno:int = rldp.MessagePart;
rldp.complete transfer_id:int256 part:int = rldp.MessagePart;

rldp.message id:int256 data:bytes = rldp.Message;
rldp.query query_id:int256 max_answer_size:long timeout:int data:bytes = rldp.Message;
rldp.answer query_id:int256 data:bytes = rldp.Message;
```

직렬화된 구조는 `adnl.message.custom` TL 스키마로 감싸져서 ADNL UDP를 통해 전송됩니다.
RLDP 전송은 큰 데이터를 전송하는 데 사용되며, 무작위 `transfer_id`가 생성되고 데이터 자체는 FEC 알고리즘에 의해 처리됩니다.
결과 조각들은 `rldp.messagePart` 구조로 감싸져서 피어가 `rldp.complete`를 보내거나 타임아웃될 때까지 피어에게 전송됩니다.

수신자가 전체 메시지를 조립하는 데 필요한 `rldp.messagePart` 조각들을 수집하면, 이들을 모두 연결하고 FEC를 사용하여 디코딩한 다음
결과 바이트 배열을 타입(tl 접두사 id)에 따라 `rldp.query` 또는 `rldp.answer` 구조 중 하나로 역직렬화합니다.

### FEC

RLDP와 함께 사용할 수 있는 유효한 전방 오류 정정 알고리즘은 RoundRobin, Online 및 RaptorQ입니다.
현재 데이터 인코딩에는 [RaptorQ](https://www.qualcomm.com/media/documents/files/raptorq-technical-overview.pdf)가 사용됩니다.

#### RaptorQ

RaptorQ의 본질은 데이터를 심볼이라고 하는 동일한 미리 정해진 크기의 블록으로 나누는 것입니다.

블록에서 행렬이 생성되고 이산 수학 연산이 적용됩니다. 이를 통해 동일한 데이터에서 거의 무한한 수의 심볼을 생성할 수 있습니다.
모든 심볼이 혼합되며, 서버에 추가 데이터를 요청하지 않고도 손실된 패킷을 복구할 수 있으며, 동일한 조각을 루프로 보내는 것보다 더 적은 패킷을 사용할 수 있습니다.

생성된 심볼은 피어가 동일한 이산 연산을 적용하여 모든 데이터가 수신되고 복원(디코딩)되었다고 보고할 때까지 피어에게 전송됩니다.

[[Golang의 RaptorQ 구현 예시]](https://github.com/xssnick/tonutils-go/tree/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/rldp/raptorq)

## RLDP-HTTP

TON 사이트와 상호작용하기 위해 RLDP로 감싼 HTTP가 사용됩니다. 호스터는 HTTP 웹서버에서 사이트를 실행하고 그 옆에 rldp-http-proxy를 시작합니다.
TON 네트워크의 모든 요청은 RLDP 프로토콜을 통해 프록시로 들어오고, 프록시는 요청을 단순 HTTP로 재조립하여 로컬에서 원래 웹 서버를 호출합니다.

사용자 측에서는 프록시(예: [Tonutils Proxy](https://github.com/xssnick/TonUtils-Proxy))를 실행하고 `.ton` 사이트를 사용하며, 모든 트래픽은 역순으로 감싸집니다. 요청은 로컬 HTTP 프록시로 가고, 프록시는 RLDP를 통해 원격 TON 사이트로 전송합니다.

RLDP 내의 HTTP는 TL 구조를 사용하여 구현됩니다:

```tlb
http.header name:string value:string = http.Header;
http.payloadPart data:bytes trailer:(vector http.header) last:Bool = http.PayloadPart;
http.response http_version:string status_code:int reason:string headers:(vector http.header) no_payload:Bool = http.Response;

http.request id:int256 method:string url:string http_version:string headers:(vector http.header) = http.Response;
http.getNextPayloadPart id:int256 seqno:int max_chunk_size:int = http.PayloadPart;
```

이는 텍스트 형식의 순수 HTTP가 아니라 모든 것이 이진 TL로 감싸지고 다시 풀어져서 프록시 자체에 의해 웹 서버나 브라우저로 전송됩니다.

작동 방식은 다음과 같습니다:

- 클라이언트가 `http.request` 전송
- 서버가 요청을 받을 때 `Content-Length` 헤더를 확인
- - 0이 아니면 클라이언트에 `http.getNextPayloadPart` 요청 전송
- - 요청을 받으면 클라이언트는 `seqno`와 `max_chunk_size`에 따라 요청된 본문 조각인 `http.payloadPart` 전송
- - 서버는 클라이언트로부터 모든 청크를 받을 때까지, 즉 마지막으로 받은 청크의 `last:Bool` 필드가 true가 될 때까지 `seqno`를 증가시키며 요청을 반복
- 요청 처리 후 서버가 `http.response` 전송, 클라이언트는 `Content-Length` 헤더 확인
- - 0이 아니면 서버에 `http.getNextPayloadPart` 요청을 보내고, 클라이언트의 경우처럼 반대 순서로 작업이 반복됨

## TON 사이트 요청하기

RLDP가 어떻게 작동하는지 이해하기 위해 TON 사이트 `foundation.ton`에서 데이터를 가져오는 예시를 살펴보겠습니다.
NFT-DNS 계약의 Get 메서드를 호출하여 이미 ADNL 주소를 얻었고, [DHT를 사용하여 RLDP 서비스의 주소와 포트를 결정](https://github.com/xssnick/ton-deep-doc/blob/master/DHT.md)했으며, [ADNL UDP로 연결](https://github.com/xssnick/ton-deep-doc/blob/master/ADNL-UDP-Internal.md)했다고 가정해 봅시다.

### `foundation.ton`에 GET 요청 보내기

이를 위해 구조를 채웁니다:

```tlb
http.request id:int256 method:string url:string http_version:string headers:(vector http.header) = http.Response;
```

필드를 채워 `http.request`를 직렬화합니다:

```
e191b161                                                           -- TL ID http.request      
116505dac8a9a3cdb464f9b5dd9af78594f23f1c295099a9b50c8245de471194   -- id           = {random}
03 474554                                                          -- method       = string `GET`
16 687474703a2f2f666f756e646174696f6e2e746f6e2f 00                 -- url          = string `http://foundation.ton/`
08 485454502f312e31 000000                                         -- http_version = string `HTTP/1.1`
01000000                                                           -- headers (1)
   04 486f7374 000000                                              -- name         = Host
   0e 666f756e646174696f6e2e746f6e 00                              -- value        = foundation.ton
```

이제 직렬화된 `http.request`를 `rldp.query`로 감싸고 이것도 직렬화합니다:

```
694d798a                                                              -- TL ID rldp.query
184c01cb1a1e4dc9322e5cabe8aa2d2a0a4dd82011edaf59eb66f3d4d15b1c5c      -- query_id        = {random}
0004040000000000                                                      -- max_answer_size = 257 KB, can be any sufficient size that we accept as headers
258f9063                                                              -- timeout (unix)  = 1670418213
34 e191b161116505dac8a9a3cdb464f9b5dd9af78594f23f1c295099a9b50c8245   -- data (http.request)
   de4711940347455416687474703a2f2f666f756e646174696f6e2e746f6e2f00
   08485454502f312e310000000100000004486f73740000000e666f756e646174
   696f6e2e746f6e00 000000
```

### 패킷 인코딩 및 전송

이제 이 데이터에 FEC RaptorQ 알고리즘을 적용해야 합니다.

인코더를 생성해봅시다. 이를 위해 결과 바이트 배열을 고정 크기의 심볼로 바꿔야 합니다. TON에서는 심볼 크기가 768바이트입니다.
이를 위해 배열을 768바이트 크기의 조각으로 나눕니다. 마지막 조각이 768보다 작으면 필요한 크기까지 0 바이트로 패딩해야 합니다.

우리의 배열은 156바이트 크기이므로 1개의 조각만 있을 것이고, 768 크기까지 612개의 0 바이트로 패딩해야 합니다.

또한 데이터와 심볼의 크기에 따라 인코더의 상수가 선택됩니다. RaptorQ 자체의 문서에서 이에 대해 더 자세히 알아볼 수 있지만, 수학적 정글에 빠지지 않기 위해 이러한 인코딩을 구현하는 준비된 라이브러리를 사용하는 것을 추천합니다.
[[인코더 생성 예시]](https://github.com/xssnick/tonutils-go/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/rldp/raptorq/encoder.go#L15)와 [[심볼 인코딩 예시]](https://github.com/xssnick/tonutils-go/blob/be3411cf412f23e6889bf0b648904306a15936e7/adnl/rldp/raptorq/solver.go#L26).

심볼은 라운드 로빈 방식으로 인코딩되고 전송됩니다: 처음에는 `seqno`를 0으로 정의하고, 후속 인코딩된 패킷마다 1씩 증가시킵니다. 예를 들어, 2개의 심볼이 있다면 첫 번째 것을 인코딩하여 보내고 seqno를 1 증가시킨 다음, 두 번째 것을 보내고 seqno를 1 증가시키고, 다시 첫 번째 것을 보내고 이 시점에서 이미 2인 seqno를 다시 1 증가시킵니다.
그리고 피어가 데이터를 수락했다는 메시지를 받을 때까지 이렇게 계속합니다.

이제 인코더를 생성했으니 데이터를 보낼 준비가 되었습니다. TL 스키마를 채워보겠습니다:

```tlb
fec.raptorQ data_size:int symbol_size:int symbols_count:int = fec.Type;

rldp.messagePart transfer_id:int256 fec_type:fec.Type part:int total_size:long seqno:int data:bytes = rldp.MessagePart;
```

- `transfer_id` - 동일한 데이터 전송 내의 모든 messagePart에 대해 동일한 무작위 int256입니다
- `fec_type`은 `fec.raptorQ`입니다
- - `data_size` = 156
- - `symbol_size` = 768
- - `symbols_count` = 1
- `part`는 우리의 경우 항상 0이며, 크기 제한에 도달한 전송에 사용할 수 있습니다
- `total_size` = 156. 전송 데이터의 크기입니다
- `seqno` - 첫 번째 패킷은 0이 되고, 이후 각 패킷마다 1씩 증가하며, 심볼을 디코딩하고 인코딩하는 매개변수로 사용됩니다
- `data` - 우리가 인코딩한 심볼로, 768바이트 크기입니다

`rldp.messagePart`를 직렬화한 후 `adnl.message.custom`으로 감싸서 ADNL UDP를 통해 전송합니다.

피어로부터 `rldp.complete` 메시지를 받거나 타임아웃이 될 때까지 seqno를 계속 증가시키면서 패킷을 루프로 보냅니다. 우리의 심볼 수와 같은 수의 패킷을 보낸 후에는 속도를 늦추고 예를 들어 10밀리초 또는 더 적은 간격으로 추가 패킷을 보낼 수 있습니다.
추가 패킷은 UDP가 빠르지만 신뢰할 수 없는 프로토콜이므로 데이터 손실을 복구하는 데 사용됩니다.

[[구현 예시]](https://github.com/xssnick/tonutils-go/blob/be3411cf412f23e6889bf0b648904306a15936e7/adnl/rldp/rldp.go#L249)

### `foundation.ton`의 응답 처리하기

전송하는 동안 이미 서버의 응답을 기대할 수 있으며, 우리의 경우 내부에 `http.response`가 있는 `rldp.answer`를 기다리고 있습니다.
요청을 보낼 때와 같은 방식으로 RLDP 전송 형태로 오지만, `transfer_id`는 반전됩니다(각 바이트 XOR 0xFF).
`rldp.messagePart`를 포함하는 `adnl.message.custom` 메시지를 받게 됩니다.

먼저 전송의 첫 번째 수신된 메시지에서 FEC 정보, 특히 `rldp.messagePart` 구조의 `data_size`, `symbol_size`, `symbols_count` 매개변수를 얻어야 합니다.
이들은 RaptorQ 디코더를 초기화하는 데 필요합니다. [[예시]](https://github.com/xssnick/tonutils-go/blob/be3411cf412f23e6889bf0b648904306a15936e7/adnl/rldp/rldp.go#L137)

초기화 후, 받은 심볼들을 `seqno`와 함께 디코더에 추가하고, `symbols_count`와 같은 최소 필요 수를 축적하면 전체 메시지를 디코딩할 수 있습니다. 성공하면 `rldp.complete`를 보냅니다. [[예시]](https://github.com/xssnick/tonutils-go/blob/be3411cf412f23e6889bf0b648904306a15936e7/adnl/rldp/rldp.go#L168)

결과는 우리가 보낸 `rldp.query`와 같은 query_id를 가진 `rldp.answer` 메시지가 될 것입니다. 데이터는 `http.response`를 포함해야 합니다.

```tlb
http.response http_version:string status_code:int reason:string headers:(vector http.header) no_payload:Bool = http.Response;
```

주요 필드와 관련하여 모든 것이 명확하며, 본질은 HTTP와 같습니다.
여기서 흥미로운 플래그는 `no_payload`입니다. true이면 응답에 본문이 없다는 의미입니다(`Content-Length` = 0).
서버로부터의 응답을 받은 것으로 간주할 수 있습니다.

`no_payload` = false이면 응답에 내용이 있으며, 이를 가져와야 합니다.
이를 위해 `rldp.query`로 감싼 `http.getNextPayloadPart` TL 스키마로 요청을 보내야 합니다.

```tlb
http.getNextPayloadPart id:int256 seqno:int max_chunk_size:int = http.PayloadPart;
```

`id`는 우리가 `http.request`에서 보낸 것과 같아야 하고, `seqno`는 0이며, 다음 부분마다 +1입니다. `max_chunk_size`는 우리가 받아들일 수 있는 최대 청크 크기이며, 일반적으로 128 KB(131072바이트)가 사용됩니다.

응답으로 다음을 받습니다:

```tlb
http.payloadPart data:bytes trailer:(vector http.header) last:Bool = http.PayloadPart;
```

`last` = true이면 끝에 도달한 것이므로, 모든 조각을 모아서 예를 들어 html과 같은 완전한 응답 본문을 얻을 수 있습니다.

## 참조

*여기 [Oleg Baranov](https://github.com/xssnick)의 [원본 문서 링크](https://github.com/xssnick/ton-deep-doc/blob/master/RLDP.md)가 있습니다.*
