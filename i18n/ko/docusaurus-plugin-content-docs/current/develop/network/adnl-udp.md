# ADNL UDP - 인터노드

ADNL over UDP는 노드와 TON 구성 요소가 서로 통신하는 데 사용됩니다. 이는 DHT 및 RLDP와 같은 다른 상위 수준의 TON 프로토콜이 작동하는 하위 수준 프로토콜입니다.
이 문서에서는 노드 간의 기본적인 통신을 위해 ADNL over UDP가 어떻게 작동하는지 알아보겠습니다.

UDP 구현에서 핸드셰이크는 다른 형태로 이루어지며 채널의 형태로 추가 계층이 사용되지만 다른 원칙은 비슷합니다.
암호화 키는 구성에서 미리 알고 있거나 다른 네트워크 노드에서 받은 개인 키와 상대방의 공개 키를 기반으로 생성됩니다.

UDP 버전의 ADNL에서는 개시자가 '채널 생성' 메시지를 보내면 피어로부터 초기 데이터 수신과 동시에 연결이 설정되고, 채널의 키가 계산되어 채널 생성이 확인됩니다.
채널이 설정되면 채널 내에서 추가 통신이 계속됩니다.

## 패킷 구조 및 통신

### 첫 패킷

프로토콜의 작동 방식을 이해하기 위해 DHT 노드와의 연결 초기화를 분석하고 주소의 서명된 목록을 가져와 보겠습니다.

글로벌 설정](https://ton-blockchain.github.io/global.config.json)의 `dht.nodes` 섹션에서 원하는 노드를 찾습니다. 예를 들어

```json
{
  "@type": "dht.node",
  "id": {
    "@type": "pub.ed25519",
    "key": "fZnkoIAxrTd4xeBgVpZFRm5SvVvSx7eN3Vbe8c83YMk="
  },
  "addr_list": {
    "@type": "adnl.addressList",
    "addrs": [
      {
        "@type": "adnl.address.udp",
        "ip": 1091897261,
        "port": 15813
      }
    ],
    "version": 0,
    "reinit_date": 0,
    "priority": 0,
    "expire_at": 0
  },
  "version": -1,
  "signature": "cmaMrV/9wuaHOOyXYjoxBnckJktJqrQZ2i+YaY3ehIyiL3LkW81OQ91vm8zzsx1kwwadGZNzgq4hI4PCB/U5Dw=="
}
```

1. ED25519 키인 `fZnkoIAxrTd4xeBgVpZFRm5SvVvSx7eN3Vbe8c83YMk`를 base64에서 디코딩해 보겠습니다.
2. IP 주소 `1091897261`를 [서비스](https://www.browserling.com/tools/dec-to-ip) 또는 작은 엔디안 바이트로 변환을 사용하여 이해하기 쉬운 형식으로 변환하면 `65.21.7.173`이 나옵니다.
3. 포트와 결합하여 `65.21.7.173:15813`을 얻은 후 UDP 연결을 설정합니다.

우리는 노드와 통신하고 일부 정보를 얻기 위해 채널을 열고 주요 작업으로 서명 된 주소 목록을 수신하려고합니다. 이를 위해 첫 번째 메시지인 [채널 만들기](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L129)를 생성합니다:

```tlb
adnl.message.createChannel key:int256 date:int = adnl.Message
```

여기에는 키와 날짜라는 두 가지 매개변수가 있습니다. 날짜는 현재 유닉스 타임스탬프를 지정합니다. 그리고 키의 경우 채널 전용으로 새로운 ED25519 개인+공개 키 쌍을 생성해야 하며, 이는 [공개 암호화 키] 초기화에 사용됩니다(/develop/network/adnl-tcp#getting-a-shared-key-using-ecdh). 생성된 공개 키는 메시지의 `key` 파라미터에 사용하고, 지금은 개인 키만 저장합니다.

채워진 TL 구조를 직렬화하고 다음을 얻습니다:

```
bbc373e6                                                         -- TL ID adnl.message.createChannel 
d59d8e3991be20b54dde8b78b3af18b379a62fa30e64af361c75452f6af019d7 -- key
555c8763                                                         -- date
```

다음으로 메인 쿼리인 [주소 목록 가져오기](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L198)로 이동해 보겠습니다.
이를 실행하려면 먼저 TL 구조를 직렬화해야 합니다:

```tlb
dht.getSignedAddressList = dht.Node
```

매개 변수가 없으므로 그냥 직렬화합니다. 'ed4879a9'라는 ID만 사용됩니다.

다음으로, 이것은 DHT 프로토콜의 상위 수준 요청이므로 먼저 `adnl.message.query` TL 구조로 래핑해야 합니다:

```tlb
adnl.message.query query_id:int256 query:bytes = adnl.Message
```

query_id`는 임의의 32바이트를 생성하고, `query\`는 기본 요청인 [바이트 배열로 래핑](/develop/data-formats/tl#encoding-bytes-array)을 사용합니다.
우리는 얻을 것입니다:

```
7af98bb4                                                         -- TL ID adnl.message.query
d7be82afbc80516ebca39784b8e2209886a69601251571444514b7f17fcd8875 -- query_id
04 ed4879a9 000000                                               -- query
```

### 패킷 구축

모든 통신은 패킷을 사용하여 수행되며, 그 내용은 [TL 구조](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L81)입니다:

```tlb
adnl.packetContents 
  rand1:bytes                                     -- random 7 or 15 bytes
  flags:#                                         -- bit flags, used to determine the presence of fields further
  from:flags.0?PublicKey                          -- sender's public key
  from_short:flags.1?adnl.id.short                -- sender's ID
  message:flags.2?adnl.Message                    -- message (used if there is only one message)
  messages:flags.3?(vector adnl.Message)          -- messages (if there are > 1)
  address:flags.4?adnl.addressList                -- list of our addresses
  priority_address:flags.5?adnl.addressList       -- priority list of our addresses
  seqno:flags.6?long                              -- packet sequence number
  confirm_seqno:flags.7?long                      -- sequence number of the last packet received
  recv_addr_list_version:flags.8?int              -- address version 
  recv_priority_addr_list_version:flags.9?int     -- priority address version
  reinit_date:flags.10?int                        -- connection reinitialization date (counter reset)
  dst_reinit_date:flags.10?int                    -- connection reinitialization date from the last received packet
  signature:flags.11?bytes                        -- signature
  rand2:bytes                                     -- random 7 or 15 bytes
        = adnl.PacketContents
        
```

보내려는 모든 메시지를 직렬화했으면 패킷을 만들 수 있습니다.
채널로 전송되는 패킷은 채널이 초기화되기 전에 전송되는 패킷과 내용이 다릅니다.
먼저 초기화에 사용되는 메인 패킷을 분석해 보겠습니다.

초기 데이터 교환 시 채널 외부에서 패킷의 직렬화된 콘텐츠 구조에는 32바이트의 피어 공개 키가 접두사로 붙습니다.
공개 키는 32바이트, 패킷 콘텐츠 구조의 직렬화된 TL의 sha256 해시 - 32바이트입니다.
패킷의 내용은 개인 키와 서버의 공개 키에서 얻은 [공유 키](/develop/network/adnl-tcp#getting-a-shared-key-using-ecdh)를 사용하여 암호화됩니다.

패킷 콘텐츠 구조를 직렬화하고 바이트 단위로 구문 분석합니다:

```
89cd42d1                                                               -- TL ID adnl.packetContents
0f 4e0e7dd6d0c5646c204573bc47e567                                      -- rand1, 15 (0f) random bytes
d9050000                                                               -- flags (0x05d9) -> 0b0000010111011001
                                                                       -- from (present because flag's zero bit = 1)
c6b41348                                                                  -- TL ID pub.ed25519
   afc46336dd352049b366c7fd3fc1b143a518f0d02d9faef896cb0155488915d6       -- key:int256
                                                                       -- messages (present because flag's third bit = 1)
02000000                                                                  -- vector adnl.Message, size = 2 messages   
   bbc373e6                                                                  -- TL ID adnl.message.createChannel
   d59d8e3991be20b54dde8b78b3af18b379a62fa30e64af361c75452f6af019d7          -- key
   555c8763                                                                  -- date (date of creation)
   
   7af98bb4                                                                  -- TL ID [adnl.message.query](/)
   d7be82afbc80516ebca39784b8e2209886a69601251571444514b7f17fcd8875          -- query_id
   04 ed4879a9 000000                                                        -- query (bytes size 4, padding 3)
                                                                       -- address (present because flag's fourth bit = 1), without TL ID since it is specified explicitly
00000000                                                                  -- addrs (empty vector, because we are in client mode and do not have an address on wiretap)
555c8763                                                                  -- version (usually initialization date)
555c8763                                                                  -- reinit_date (usually initialization date)
00000000                                                                  -- priority
00000000                                                                  -- expire_at

0100000000000000                                                       -- seqno (present because flag's sixth bit = 1)
0000000000000000                                                       -- confirm_seqno (present because flag's seventh bit = 1)
555c8763                                                               -- recv_addr_list_version (present because flag's eighth bit = 1, usually initialization date)
555c8763                                                               -- reinit_date (present because flag's tenth bit = 1, usually initialization date)
00000000                                                               -- dst_reinit_date (present because flag's tenth bit = 1)
0f 2b6a8c0509f85da9f3c7e11c86ba22                                      -- rand2, 15 (0f) random bytes
```

직렬화 후 - 이전에 생성하고 저장한 비공개 클라이언트의 (채널이 아닌) ED25519 키로 결과 바이트 배열에 서명해야 합니다.
서명(64바이트 크기)을 생성한 후에는 패킷에 서명을 추가하고 다시 직렬화하되, 이제 서명의 존재를 의미하는 11번째 비트를 플래그에 추가해야 합니다:

```
89cd42d1                                                               -- TL ID adnl.packetContents
0f 4e0e7dd6d0c5646c204573bc47e567                                      -- rand1, 15 (0f) random bytes
d90d0000                                                               -- flags (0x0dd9) -> 0b0000110111011001
                                                                       -- from (present because flag's zero bit = 1)
c6b41348                                                                  -- TL ID pub.ed25519
   afc46336dd352049b366c7fd3fc1b143a518f0d02d9faef896cb0155488915d6       -- key:int256
                                                                       -- messages (present because flag's third bit = 1)
02000000                                                                  -- vector adnl.Message, size = 2 message   
   bbc373e6                                                                  -- TL ID adnl.message.createChannel
   d59d8e3991be20b54dde8b78b3af18b379a62fa30e64af361c75452f6af019d7          -- key
   555c8763                                                                  -- date (date of creation)
   
   7af98bb4                                                                  -- TL ID adnl.message.query
   d7be82afbc80516ebca39784b8e2209886a69601251571444514b7f17fcd8875          -- query_id
   04 ed4879a9 000000                                                        -- query (bytes size 4, padding 3)
                                                                       -- address (present because flag's fourth bit = 1), without TL ID since it is specified explicitly
00000000                                                                  -- addrs (empty vector, because we are in client mode and do not have an address on wiretap)
555c8763                                                                  -- version (usually initialization date)
555c8763                                                                  -- reinit_date (usually initialization date)
00000000                                                                  -- priority
00000000                                                                  -- expire_at

0100000000000000                                                       -- seqno (present because flag's sixth bit = 1)
0000000000000000                                                       -- confirm_seqno (present because flag's seventh bit = 1)
555c8763                                                               -- recv_addr_list_version (present because flag's eighth bit = 1, usually initialization date)
555c8763                                                               -- reinit_date (present because flag's tenth bit = 1, usually initialization date)
00000000                                                               -- dst_reinit_date (present because flag's tenth bit = 1)
40 b453fbcbd8e884586b464290fe07475ee0da9df0b8d191e41e44f8f42a63a710    -- signature (present because flag's eleventh bit = 1), (bytes size 64, padding 3)
   341eefe8ffdc56de73db50a25989816dda17a4ac6c2f72f49804a97ff41df502    --
   000000                                                              --
0f 2b6a8c0509f85da9f3c7e11c86ba22                                      -- rand2, 15 (0f) random bytes
```

이제 바이트 배열인 패킷이 조립되고 서명되고 직렬화되었습니다.
이후 수신자가 패킷의 무결성을 확인하려면 패킷의 sha256 해시를 계산해야 합니다. 예를 들어, `408a2a4ed623b25a2e2ba8bbe92d01a3b5dbd22c97525092ac3203ce4044dcd2`가 되겠습니다.

이제 개인 키와 (채널의 키가 아닌) 피어의 공개 키에서 얻은 [공유 키](/develop/네트워크/adnl-tcp#getting-a-shared-key-using-ecdh)를 사용하여 패킷의 내용을 AES-CTR 암호로 암호화해 보겠습니다.

ED25519 피어 키의 [ID 계산](/develop/네트워크/adnl-tcp#getting-key-id)과 모든 것을 연결하기만 하면 전송 준비가 거의 완료됩니다:

```
daa76538d99c79ea097a67086ec05acca12d1fefdbc9c96a76ab5a12e66c7ebb  -- server Key ID
afc46336dd352049b366c7fd3fc1b143a518f0d02d9faef896cb0155488915d6  -- our public key
408a2a4ed623b25a2e2ba8bbe92d01a3b5dbd22c97525092ac3203ce4044dcd2  -- sha256 content hash (before encryption)
...                                                               -- encrypted content of the packet
```

이제 빌드한 패킷을 UDP를 통해 피어에게 전송하고 응답을 기다릴 수 있습니다.

이에 대한 응답으로 비슷한 구조이지만 다른 메시지가 포함된 패킷을 받게 됩니다. 패킷은 다음과 같이 구성됩니다:

```
68426d4906bafbd5fe25baf9e0608cf24fffa7eca0aece70765d64f61f82f005  -- ID of our key
2d11e4a08031ad3778c5e060569645466e52bd1bd2c7b78ddd56def1cf3760c9  -- server public key, for shared key
f32fa6286d8ae61c0588b5a03873a220a3163cad2293a5dace5f03f06681e88a  -- sha256 content hash (before encryption)
...                                                               -- the encrypted content of the packet
```

서버에서 패킷을 역직렬화하는 방법은 다음과 같습니다:

1. 패킷에서 키의 ID를 확인하여 해당 패킷이 저희를 위한 것임을 파악합니다.
2. 패킷에서 서버의 공개 키와 개인 키를 사용하여 공유 키를 계산하고 패킷의 내용을 복호화합니다.
3. 당사에 전송된 sha256 해시와 복호화된 데이터에서 받은 해시를 비교하여 일치해야 합니다.
4. adnl.packetContents\` TL 스키마를 사용하여 패킷 콘텐츠 역직렬화를 시작합니다.

패킷의 내용은 다음과 같습니다:

```
89cd42d1                                                               -- TL ID adnl.packetContents
0f 985558683d58c9847b4013ec93ea28                                      -- rand1, 15 (0f) random bytes
ca0d0000                                                               -- flags (0x0dca) -> 0b0000110111001010
daa76538d99c79ea097a67086ec05acca12d1fefdbc9c96a76ab5a12e66c7ebb       -- from_short (because flag's first bit = 1)
02000000                                                               -- messages (present because flag's third bit = 1)
   691ddd60                                                               -- TL ID adnl.message.confirmChannel 
   db19d5f297b2b0d76ef79be91ad3ae01d8d9f80fab8981d8ed0c9d67b92be4e3       -- key (server channel public key)
   d59d8e3991be20b54dde8b78b3af18b379a62fa30e64af361c75452f6af019d7       -- peer_key (our public channel key)
   94848863                                                               -- date
   
   1684ac0f                                                               -- TL ID adnl.message.answer 
   d7be82afbc80516ebca39784b8e2209886a69601251571444514b7f17fcd8875       -- query_id
   90 48325384c6b413487d99e4a08031ad3778c5e060569645466e52bd5bd2c7b       -- answer (the answer to our request, we will analyze its content in an article about DHT)
      78ddd56def1cf3760c901000000e7a60d67ad071541c53d0000ee354563ee       --
      35456300000000000000009484886340d46cc50450661a205ad47bacd318c       --
      65c8fd8e8f797a87884c1bad09a11c36669babb88f75eb83781c6957bc976       --
      6a234f65b9f6e7cc9b53500fbe2c44f3b3790f000000                        --
      000000                                                              --
0100000000000000                                                       -- seqno (present because flag's sixth bit = 1)
0100000000000000                                                       -- confirm_seqno (present because flag's seventh bit = 1)
94848863                                                               -- recv_addr_list_version (present because flag's eighth bit = 1, usually initialization date)
ee354563                                                               -- reinit_date (present because flag's tenth bit = 1, usually initialization date)
94848863                                                               -- dst_reinit_date (present because flag's tenth bit = 1)
40 5c26a2a05e584e9d20d11fb17538692137d1f7c0a1a3c97e609ee853ea9360ab6   -- signature (present because flag's eleventh bit = 1), (bytes size 64, padding 3)
   d84263630fe02dfd41efb5cd965ce6496ac57f0e51281ab0fdce06e809c7901     --
   000000                                                              --
0f c3354d35749ffd088411599101deb2                                      -- rand2, 15 (0f) random bytes
```

서버는 두 개의 메시지로 응답했습니다: adnl.message.confirmChannel`과 `adnl.message.answer`입니다. 
adnl.message.answer`를 사용하면 모든 것이 간단합니다. 이것은 우리의 요청 `dht.getSignedAddressList`에 대한 답변이며, DHT에 대한 기사에서 분석 할 것입니다.

피어에서 채널 생성을 확인하고 공개 채널 키를 보냈다는 의미의 `adnl.message.confirmChannel`에 집중해 보겠습니다. 이제 우리의 비공개 채널 키와 피어의 공개 채널 키가 있으므로 [공유 키](/develop/network/adnl-tcp#getting-a-shared-key-using-ecdh)를 계산할 수 있습니다.

이제 공유 채널 키를 계산했으면, 발신 메시지 암호화용 키와 수신 메시지 암호 해독용 키 두 개를 만들어야 합니다.
2개의 키를 만드는 것은 매우 간단하며, 두 번째 키는 역순으로 작성된 공유 키와 동일합니다. 예시:

```
Shared key : AABB2233

First key: AABB2233
Second key: 3322BBAA
```

어떤 키를 무엇에 사용할지 결정해야 하는데, 공개 채널 키의 아이디와 서버 채널의 공개 키의 아이디를 비교하여 숫자 형식인 uint256으로 변환하여 이를 결정할 수 있습니다. 이 접근 방식은 서버와 클라이언트 모두 어떤 키를 어떤 용도로 사용할지 결정하기 위해 사용됩니다. 서버가 암호화에 첫 번째 키를 사용하는 경우, 이 접근 방식을 사용하면 클라이언트는 항상 암호 해독에 이 키를 사용합니다.

이용 약관은 다음과 같습니다:

```
The server id is smaller than our id:
Encryption: First Key
Decryption: Second Key

The server id is larger than our id:
Encryption: Second Key
Decryption: First Key

If the ids are equal (nearly impossible):
Encryption: First Key
Decryption: First Key
```

[[구현 예시]](https://github.com/xssnick/tonutils-go/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/adnl.go#L502)

### 채널 내 커뮤니케이션

이후의 모든 패킷 교환은 채널 내에서 이루어지며, 채널 키는 암호화에 사용됩니다.
새로 생성된 채널 내에서 동일한 `dht.getSignedAddressList` 요청을 전송하여 차이점을 확인해 보겠습니다.

동일한 `adnl.packetContents` 구조를 사용하여 채널의 패킷을 빌드해 보겠습니다:

```
89cd42d1                                                               -- TL ID adnl.packetContents
0f c1fbe8c4ab8f8e733de83abac17915                                      -- rand1, 15 (0f) random bytes
c4000000                                                               -- flags (0x00c4) -> 0b0000000011000100
                                                                       -- message (because second bit = 1)
7af98bb4                                                                  -- TL ID adnl.message.query
fe3c0f39a89917b7f393533d1d06b605b673ffae8bbfab210150fe9d29083c35          -- query_id
04 ed4879a9 000000                                                        -- query (our dht.getSignedAddressList packed in bytes with padding 3)
0200000000000000                                                       -- seqno (because flag's sixth bit = 1), 2 because it is our second message
0100000000000000                                                       -- confirm_seqno (flag's seventh bit = 1), 1 because it is the last seqno received from the server
07 e4092842a8ae18                                                      -- rand2, 7 (07) random bytes
```

채널의 패킷은 매우 간단하며 기본적으로 시퀀스(seqno)와 메시지 자체로 구성됩니다.

직렬화 후 지난번과 마찬가지로 패킷의 sha256 해시를 계산합니다. 그런 다음 채널의 발신 패킷을 위한 키를 사용하여 패킷을 암호화합니다.
[계산](/develop/network/adnl-tcp#getting-key-id) `pub.aes` 발신 메시지의 암호화 키 ID를 사용하여 패킷을 작성합니다:

```
bcd1cf47b9e657200ba21d94b822052cf553a548f51f539423c8139a83162180 -- ID of encryption key of our outgoing messages 
6185385aeee5faae7992eb350f26ba253e8c7c5fa1e3e1879d9a0666b9bd6080 -- sha256 content hash (before encryption)
...                                                              -- the encrypted content of the packet
```

UDP를 통해 패킷을 전송하고 응답을 기다립니다. 응답으로 우리가 보낸 것과 동일한 유형(동일한 필드)의 패킷을 받게 되지만, 요청에 대한 응답은 `dht.getSignedAddressList`입니다.

## 기타 메시지 유형

기본 통신에는 위에서 설명한 `adnl.message.query` 및 `adnl.message.answer`와 같은 메시지가 사용되지만 일부 상황에서는 다른 유형의 메시지도 사용되며 이 섹션에서 설명합니다.

### adnl.message.part

이 메시지 유형은 `adnl.message.answer`와 같은 다른 가능한 메시지 유형 중 하나입니다. 이 데이터 전송 방법은 메시지가 너무 커서 단일 UDP 데이터그램으로 전송할 수 없을 때 사용됩니다.

```tlb
adnl.message.part 
hash:int256            -- sha256 hash of the original message
total_size:int         -- original message size
offset:int             -- offset according to the beginning of the original message
data:bytes             -- piece of data of the original message
   = adnl.Message;
```

따라서 원본 메시지를 조합하려면 여러 부분을 가져와서 오프셋에 따라 단일 바이트 배열로 연결해야 합니다.
그런 다음 이 바이트 배열의 ID 접두사에 따라 메시지로 처리합니다(이 바이트 배열의 접두사에 따라).

### adnl.message.custom

```tlb
adnl.message.custom data:bytes = adnl.Message;
```

이러한 메시지는 상위 레벨의 논리가 요청-응답 형식과 일치하지 않을 때 사용되며, 이 유형의 메시지는 쿼리 ID 및 기타 필드 없이 바이트 배열만 전달하므로 처리를 상위 레벨로 완전히 이동할 수 있습니다.
이 유형의 메시지는 예를 들어 많은 요청에 대해 하나의 응답만 있을 수 있으므로 이 로직은 RLDP 자체에 의해 제어되기 때문에 RLDP에서 사용됩니다.

### 결론

추가 통신은 이 문서(
)에 설명된 로직을 기반으로 이루어지지만 패킷의 내용은 DHT 및 RLDP와 같은 상위 수준 프로토콜에 따라 달라집니다.

## 참조

여기 [Oleg Baranov](https://github.com/xssnick)의 [원본 기사 링크](https://github.com/xssnick/ton-deep-doc/blob/master/ADNL-UDP-Internal.md)가 있습니다.
