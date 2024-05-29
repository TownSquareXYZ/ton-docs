# RLDP

대용량 데이터 블록을 전송하는 데 사용되는 ADNL UDP 위에 실행되는 프로토콜로,
에는 상대방의 승인 패킷을 대체하는 순방향 오류 수정(FEC) 알고리즘이 포함되어 있습니다.
이를 통해 네트워크 구성 요소 간에 데이터를 보다 효율적으로 전송할 수 있지만 트래픽 소비량이 늘어납니다.

예를 들어 다른 노드에서 블록을 다운로드하고 데이터를 전송하기 위해
, TON 웹사이트 및 TON 스토리지에 액세스하기 위해 등 TON 인프라의 모든 곳에서 RLDP가 사용됩니다.

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

직렬화된 구조는 `adnl.message.custom` TL 스키마로 래핑되어 ADNL UDP를 통해 전송됩니다.
RLDP 전송은 빅 데이터 전송에 사용되며, 임의의 `transfer_id`가 생성되고 데이터 자체는 FEC 알고리즘에 의해 처리됩니다.
결과 조각은 `rldp.messagePart` 구조로 래핑되어 상대방이 `rldp.complete`를 보내거나 시간 초과가 발생할 때까지 상대방에게 전송됩니다.

수신자가 완전한 메시지를 조립하는 데 필요한 `rldp.messagePart` 조각을 수집하면, 이를 모두 연결하고 FEC를 사용하여 디코딩한 다음
결과 바이트 배열을 유형(tl 접두사 id)에 따라 `rldp.query` 또는 `rldp.answer` 구조 중 하나로 역직렬화합니다.

### FEC

RLDP와 함께 사용할 수 있는 유효한 순방향 오류 수정 알고리즘은 RoundRobin, Online 및 RaptorQ입니다.
현재 데이터 인코딩에는 [RaptorQ](https://www.qualcomm.com/media/documents/files/raptorq-technical-overview.pdf)가 사용됩니다.

#### 랩터큐

RaptorQ의 핵심은 데이터가 동일한 미리 정해진 크기의 블록인 소위 심볼로 나뉘어져 있다는 것입니다.

행렬은 블록에서 생성되고 이산 수학 연산이 적용됩니다. 이를 통해 동일한 데이터에서 거의 무한대에 가까운 수의 심볼(
)을 생성할 수 있습니다. 모든 심볼이 혼합되어 있으므로 동일한 조각을 반복해서 보낼 때보다 적은 패킷을 사용하면서 서버에 추가 데이터를 요청하지 않고도 손실된 패킷을 복구할 수 있습니다.

생성된 심볼은 동일한 개별 연산을 적용하여 모든 데이터가 수신 및 복원(디코딩)되었다고 보고할 때까지 피어에게 전송됩니다.

[[골랑에서 랩터큐의 구현 예]](https://github.com/xssnick/tonutils-go/tree/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/rldp/raptorq)

## RLDP-HTTP

TON 사이트와 상호 작용하기 위해 RLDP로 래핑된 HTTP가 사용됩니다. 호스트는 HTTP 웹서버에서 자신의 사이트를 실행하고 그 옆에서 rldp-http-proxy를 시작합니다.
TON 네트워크의 모든 요청은 RLDP 프로토콜을 통해 프록시로 전달되며, 프록시는 요청을 간단한 HTTP로 재조합하여 로컬로 원본 웹 서버를 호출합니다.

자신의 측 사용자가 프록시(예: [Tonutils Proxy](https://github.com/xssnick/TonUtils-Proxy)를 실행하고 '.ton' 사이트를 사용하면 모든 트래픽이 역순으로 래핑되고 요청은 로컬 HTTP 프록시로 이동한 후 RLDP를 통해 원격 TON 사이트로 전송됩니다.

RLDP 내부의 HTTP는 TL 구조를 사용하여 구현됩니다:

```tlb
http.header name:string value:string = http.Header;
http.payloadPart data:bytes trailer:(vector http.header) last:Bool = http.PayloadPart;
http.response http_version:string status_code:int reason:string headers:(vector http.header) no_payload:Bool = http.Response;

http.request id:int256 method:string url:string http_version:string headers:(vector http.header) = http.Response;
http.getNextPayloadPart id:int256 seqno:int max_chunk_size:int = http.PayloadPart;
```

이것은 텍스트 형식의 순수한 HTTP가 아니며, 모든 것이 바이너리 TL로 래핑되고 프록시 자체에서 웹 서버나 브라우저로 전송하기 위해 다시 래핑이 해제됩니다.

작업 계획은 다음과 같습니다:

- 클라이언트가 `http.request`를 전송합니다.
- 서버는 요청을 받을 때 `Content-Length` 헤더를 확인합니다.
- - 0이 아닌 경우, 클라이언트에 `http.getNextPayloadPart` 요청을 보냅니다.
- - 요청을 받으면 클라이언트는 `seqno`와 `max_chunk_size`에 따라 요청된 본문 부분인 `http.payloadPart`를 전송합니다.
- - 서버는 클라이언트로부터 모든 청크를 받을 때까지, 즉 마지막으로 받은 청크의 `last:Bool` 필드가 참이 될 때까지 `seqno`를 증가시키며 요청을 반복합니다.
- 요청을 처리한 후 서버는 `http.response`를 보내고, 클라이언트는 `Content-Length` 헤더를 확인합니다.
- - 0이 아닌 경우 서버에 `http.getNextPayloadPart` 요청을 보내면 클라이언트의 경우와 마찬가지로 작업이 반복되지만 그 반대의 경우도 마찬가지입니다.

## TON 사이트 요청하기

RLDP가 어떻게 작동하는지 이해하기 위해 TON 사이트 'foundation.ton'에서 데이터를 가져오는 예시를 살펴보겠습니다.
NFT-DNS 컨트랙트의 Get 메서드를 호출하여 ADNL 주소를 이미 가지고 있고, [DHT를 사용하여 RLDP 서비스의 주소와 포트를 확인](https://github.com/xssnick/ton-deep-doc/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/DHT.md)하고, [ADNL UDP를 통해 연결](https://github.com/xssnick/ton-deep-doc/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/ADNL-UDP-Internal.md)했다고 가정해 보겠습니다.

### 'foundation.ton'으로 GET 요청 보내기

이렇게 하려면 구조를 채우세요:

```tlb
http.request id:int256 method:string url:string http_version:string headers:(vector http.header) = http.Response;
```

필드를 채워서 `http.request`를 직렬화합니다:

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

이제 직렬화된 `http.request`를 `rldp.query`로 감싸서 직렬화해 보겠습니다:

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

이제 이 데이터에 FEC 랩터큐 알고리즘을 적용해야 합니다.

인코더를 만들어 보겠습니다. 이를 위해 결과 바이트 배열을 고정된 크기의 심볼로 바꿔야 합니다. TON에서 심볼 크기는 768바이트입니다.
이를 위해 배열을 768바이트 조각으로 분할해 보겠습니다. 마지막 조각에서 768보다 작게 나오면 필요한 크기로 0바이트를 추가해야 합니다.

배열의 크기는 156바이트이므로 1개만 존재하며, 612개의 0바이트로 768의 크기로 채워야 합니다.

또한 데이터와 심볼의 크기에 따라 인코더에 상수가 선택되며, 이에 대한 자세한 내용은 RaptorQ 자체 문서에서 확인할 수 있지만 수학적 정글에 빠지지 않으려면 이러한 인코딩을 구현하는 기성 라이브러리를 사용하는 것이 좋습니다.
[인코더 생성 예제]](https://github.com/xssnick/tonutils-go/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/rldp/raptorq/encoder.go#L15) 및 [[심볼 인코딩 예제]](https://github.com/xssnick/tonutils-go/blob/be3411cf412f23e6889bf0b648904306a15936e7/adnl/rldp/raptorq/solver.go#L26)를 참조하세요.

심볼은 라운드 로빈 방식으로 인코딩되어 전송됩니다. 처음에는 0인 'seqno'를 정의하고 인코딩된 패킷이 연속적으로 전송될 때마다 1씩 증가합니다. 예를 들어, 2개의 심볼이 있는 경우 첫 번째 심볼을 인코딩하여 전송하고, 두 번째 심볼을 인코딩하고 seqno를 1씩 증가시킨 다음, 다시 첫 번째 심볼을 인코딩하고 현재 이미 2와 같은 seqno를 1씩 증가시킵니다.
이렇게 해서 상대방이 데이터를 수락했다는 메시지를 받을 때까지 반복합니다.

이제 인코더를 만들었으면 데이터를 전송할 준비가 된 것이므로 TL 스키마를 채울 것입니다:

```tlb
fec.raptorQ data_size:int symbol_size:int symbols_count:int = fec.Type;

rldp.messagePart transfer_id:int256 fec_type:fec.Type part:int total_size:long seqno:int data:bytes = rldp.MessagePart;
```

- transfer_id\` - 임의의 int256, 동일한 데이터 전송 내의 모든 메시지 파트에 대해 동일합니다.
- fec_type`은 `fec.raptorQ\`입니다.
- - 데이터 크기\` = 156
- - 심볼 크기\` = 768
- - 심볼_수\` = 1
- 이 경우 `part`는 항상 0이며, 크기 제한에 도달한 전송에 사용할 수 있습니다.
- 총_크기\` = 156. 전송 데이터의 크기입니다.
- 첫 번째 패킷은 0이고 이후 패킷마다 1씩 증가하며, 심볼을 디코딩하고 인코딩하는 매개변수로 사용됩니다.
- 데이터\` - 768바이트 크기의 인코딩된 기호입니다.

rldp.messagePart`를 직렬화한 후 `adnl.message.custom\`로 래핑하여 ADNL UDP를 통해 전송합니다.

상대방으로부터 `rldp.complete` 메시지를 기다리거나 시간 초과로 멈출 때까지 패킷을 반복해서 보내면서 항상 seqno를 증가시킵니다. 심볼 수와 동일한 수의 패킷을 전송한 후에는 속도를 늦추고 10밀리초 이하로 한 번씩 추가 패킷을 전송할 수 있습니다.
UDP는 빠르지만 불안정한 프로토콜이므로 추가 패킷은 데이터 손실 시 복구에 사용됩니다.

[[구현 예시]](https://github.com/xssnick/tonutils-go/blob/be3411cf412f23e6889bf0b648904306a15936e7/adnl/rldp/rldp.go#L249)

### foundation.ton\`의 응답 처리하기

전송하는 동안 이미 서버로부터 응답을 기대할 수 있으며, 우리의 경우 `http.response`가 포함된 `rldp.answer`를 기다리고 있습니다.
이 응답은 요청 시 전송된 것과 동일한 방식으로 RLDP 전송의 형태로 우리에게 오지만, `transfer_id`는 반전됩니다(각 바이트 XOR 0xFF).
rldp.messagePart`가 포함된 `adnl.message.custom\` 메시지를 받게 됩니다.

먼저 전송의 첫 번째 수신 메시지에서 FEC 정보, 특히 `fec.raptorQ` 메시지 파트 구조에서 `data_size`, `symbol_size` 및 `symbols_count` 파라미터를 가져와야 합니다.
이 매개변수는 RaptorQ 디코더를 초기화하는 데 필요합니다. [[Example]](https://github.com/xssnick/tonutils-go/blob/be3411cf412f23e6889bf0b648904306a15936e7/adnl/rldp/rldp.go#L137)

초기화 후, 수신된 심볼을 `seqno`와 함께 디코더에 추가하고 `symbols_count`와 같은 최소 요구 개수가 누적되면 전체 메시지를 디코딩할 수 있습니다. 성공하면 `rldp.complete`를 전송합니다. [[Example]](https://github.com/xssnick/tonutils-go/blob/be3411cf412f23e6889bf0b648904306a15936e7/adnl/rldp/rldp.go#L168)

결과는 우리가 보낸 `rldp.query`와 동일한 query_id를 가진 `rldp.answer` 메시지가 됩니다. 데이터에는 `http.response`가 포함되어야 합니다.

```tlb
http.response http_version:string status_code:int reason:string headers:(vector http.header) no_payload:Bool = http.Response;
```

주요 필드를 사용하면 모든 것이 명확하다고 생각하며 본질은 HTTP에서와 동일합니다.
여기서 흥미로운 플래그는 `no_payload`이며, 이 플래그가 참이면 응답에 본문이 없습니다(`Content-Length` = 0).
서버의 응답이 수신된 것으로 간주할 수 있습니다.

no_payload`= false이면 응답에 콘텐츠가 있는 것이므로 이를 가져와야 합니다. 
이렇게 하려면`rldp.query`로 래핑된 TL 스키마 `http.getNextPayloadPart\`로 요청을 보내야 합니다.

```tlb
http.getNextPayloadPart id:int256 seqno:int max_chunk_size:int = http.PayloadPart;
```

id`는 `http.request`에서 보낸 것과 동일해야 하며, `seqno`는 0, 다음 부분마다 +1이 있어야 합니다. 최대 청크 크기`는 허용할 수 있는 최대 청크 크기이며, 일반적으로 128KB(131072바이트)가 사용됩니다.

이에 대한 응답을 받습니다:

```tlb
http.payloadPart data:bytes trailer:(vector http.header) last:Bool = http.PayloadPart;
```

마지막\` = 참이면 끝에 도달한 것이고, 모든 조각을 조합하여 완전한 응답 본문(예: HTML)을 얻을 수 있습니다.

## 참조

여기 [Oleg Baranov](https://github.com/xssnick)의 [원본 기사 링크](https://github.com/xssnick/ton-deep-doc/blob/master/RLDP.md)가 있습니다.
