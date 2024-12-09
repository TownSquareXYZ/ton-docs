# ADNL UDP - 노드 간 통신

ADNL over UDP는 노드와 TON 컴포넌트가 서로 통신하는 데 사용됩니다. DHT와 RLDP 같은 더 높은 수준의 TON 프로토콜이 작동하는 기반이 되는 낮은 수준의 프로토콜입니다.
이 글에서는 노드 간 기본 통신을 위한 UDP 기반 ADNL의 작동 방식을 알아보겠습니다.

ADNL over TCP와 달리 UDP 구현에서는 핸드셰이크가 다른 형태로 이루어지고 채널 형태의 추가 레이어가 사용됩니다. 하지만 다른 원리는 비슷합니다:
암호화 키는 우리의 개인 키와 미리 config에서 알고 있거나 다른 네트워크 노드로부터 받은 피어의 공개 키를 기반으로 생성됩니다.

ADNL의 UDP 버전에서는 이니시에이터가 'create channel' 메시지를 보내면 동시에 피어로부터 초기 데이터를 수신하면서 연결이 설정됩니다. 채널 키가 계산되고 채널 생성이 확인됩니다.
채널이 설정되면 이후의 통신은 그 안에서 계속됩니다.

## 패킷 구조와 통신

### 첫 번째 패킷

프로토콜의 작동 방식을 이해하기 위해 DHT 노드와의 연결 초기화와 서명된 주소 목록 가져오기를 분석해 보겠습니다.

[global config](https://ton-blockchain.github.io/global.config.json)의 `dht.nodes` 섹션에서 원하는 노드를 찾으세요. 예시:

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

1. ED25519 키 `fZnkoIAxrTd4xeBgVpZFRm5SvVvSx7eN3Vbe8c83YMk`를 가져와서 base64에서 디코딩합니다
2. IP 주소 `1091897261`를 [서비스](https://www.browserling.com/tools/dec-to-ip)를 사용하거나 리틀 엔디안 바이트로 변환하여 이해 가능한 형식으로 변환하면 `65.21.7.173`이 됩니다
3. 포트와 결합하여 `65.21.7.173:15813`을 얻고 UDP 연결을 설정합니다.

노드와 통신하기 위해 채널을 열고 정보를 얻고자 하며, 주요 작업으로 서명된 주소 목록을 받고자 합니다. 이를 위해 2개의 메시지를 생성할 것입니다. 첫 번째는 [채널 생성](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L129)입니다:

```tlb
adnl.message.createChannel key:int256 date:int = adnl.Message
```

여기에는 key와 date 두 가지 매개변수가 있습니다. date로는 현재 unix 타임스탬프를 지정합니다. key의 경우 - 채널용으로 새로운 ED25519 개인+공개 키 쌍을 생성해야 합니다. 이는 [공개 암호화 키](/v3/documentation/network/protocols/adnl/adnl-tcp#getting-a-shared-key-using-ecdh) 초기화에 사용됩니다. 메시지의 `key` 매개변수에 생성한 공개 키를 사용하고 개인 키는 일단 저장해 둡니다.

채워진 TL 구조를 직렬화하면 다음과 같이 됩니다:

```
bbc373e6                                                         -- TL ID adnl.message.createChannel 
d59d8e3991be20b54dde8b78b3af18b379a62fa30e64af361c75452f6af019d7 -- key
555c8763                                                         -- date
```

다음으로 메인 쿼리 - [주소 목록 가져오기](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L198)로 넘어갑니다.
실행하려면 먼저 TL 구조를 직렬화해야 합니다:

```tlb
dht.getSignedAddressList = dht.Node
```

매개변수가 없으므로 ID만 직렬화하면 됩니다 - `ed4879a9`.

다음으로 이것이 DHT 프로토콜의 더 높은 레벨 요청이므로 먼저 `adnl.message.query` TL 구조로 래핑해야 합니다:

```tlb
adnl.message.query query_id:int256 query:bytes = adnl.Message
```

`query_id`로 무작위 32바이트를 생성하고, `query`로는 [바이트 배열로 래핑된](/v3/documentation/data-formats/tl#encoding-bytes-array) 메인 요청을 사용합니다.
다음과 같이 됩니다:

```
7af98bb4                                                         -- TL ID adnl.message.query
d7be82afbc80516ebca39784b8e2209886a69601251571444514b7f17fcd8875 -- query_id
04 ed4879a9 000000                                               -- query
```

### 패킷 구축

모든 통신은 [TL 구조](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L81)의 내용을 가진 패킷을 통해 이루어집니다:

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

보내려는 모든 메시지를 직렬화했으니 패킷 구축을 시작할 수 있습니다.
채널로 보내는 패킷은 채널 초기화 전에 보내는 패킷과 내용이 다릅니다.
먼저 초기화에 사용되는 메인 패킷을 분석해 보겠습니다.

초기 데이터 교환 중에는 채널 외부에서 직렬화된 패킷 내용 구조 앞에 피어의 공개 키 32바이트가 붙습니다.
우리의 공개 키 32바이트, 직렬화된 TL 패킷 내용 구조의 sha256 해시 32바이트.
패킷의 내용은 우리의 개인 키와 서버의 공개 키로부터 얻은 [공유 키](/v3/documentation/network/protocols/adnl/adnl-tcp#getting-a-shared-key-using-ecdh)를 사용하여 암호화됩니다.

패킷 내용 구조를 직렬화하고 바이트별로 파싱해 보겠습니다:

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

직렬화 후 - 이전에 생성하고 저장한 우리의 클라이언트(채널이 아닌) ED25519 개인 키로 결과 바이트 배열에 서명해야 합니다.
서명(64바이트 크기)을 생성한 후에는 패킷에 추가하고 다시 직렬화해야 하는데, 이번에는 서명의 존재를 의미하는 11번째 비트를 플래그에 추가합니다:

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

이제 조립, 서명 및 직렬화된 패킷이 바이트 배열로 되어있습니다.
수신자가 이후 무결성을 확인할 수 있도록 패킷의 sha256 해시를 계산해야 합니다. 예를 들어 `408a2a4ed623b25a2e2ba8bbe92d01a3b5dbd22c97525092ac3203ce4044dcd2`가 됩니다.

이제 우리의 개인 키와 피어의 공개 키(채널의 키가 아님)로부터 얻은 [공유 키](/v3/documentation/network/protocols/adnl/adnl-tcp#getting-a-shared-key-using-ecdh)를 사용하여 AES-CTR 암호로 패킷의 내용을 암호화합니다.

거의 전송할 준비가 되었고, ED25519 피어 키의 [ID를 계산](/v3/documentation/network/protocols/adnl/adnl-tcp#getting-key-id)하고 모든 것을 함께 연결하기만 하면 됩니다:

```
daa76538d99c79ea097a67086ec05acca12d1fefdbc9c96a76ab5a12e66c7ebb  -- server Key ID
afc46336dd352049b366c7fd3fc1b143a518f0d02d9faef896cb0155488915d6  -- our public key
408a2a4ed623b25a2e2ba8bbe92d01a3b5dbd22c97525092ac3203ce4044dcd2  -- sha256 content hash (before encryption)
...                                                               -- encrypted content of the packet
```

이제 구축된 패킷을 UDP를 통해 피어에게 보내고 응답을 기다릴 수 있습니다.

응답으로 비슷한 구조지만 다른 메시지를 가진 패킷을 받게 됩니다. 다음으로 구성됩니다:

```
68426d4906bafbd5fe25baf9e0608cf24fffa7eca0aece70765d64f61f82f005  -- ID of our key
2d11e4a08031ad3778c5e060569645466e52bd1bd2c7b78ddd56def1cf3760c9  -- server public key, for shared key
f32fa6286d8ae61c0588b5a03873a220a3163cad2293a5dace5f03f06681e88a  -- sha256 content hash (before encryption)
...                                                               -- the encrypted content of the packet
```

서버에서 오는 패킷의 역직렬화는 다음과 같이 진행됩니다:

1. 패킷의 키 ID를 확인하여 패킷이 우리를 위한 것인지 확인합니다
2. 패킷의 서버 공개 키와 우리의 개인 키를 사용하여 공유 키를 계산하고 패킷 내용을 복호화합니다
3. 전송된 sha256 해시를 복호화된 데이터에서 얻은 해시와 비교하여 일치해야 합니다
4. `adnl.packetContents` TL 스키마를 사용하여 패킷 내용 역직렬화를 시작합니다

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

서버가 우리에게 두 개의 메시지로 응답했습니다: `adnl.message.confirmChannel`과 `adnl.message.answer`.
`adnl.message.answer`는 단순합니다. 이는 우리의 `dht.getSignedAddressList` 요청에 대한 응답이며 DHT 관련 글에서 분석할 예정입니다.

`adnl.message.confirmChannel`에 집중해 보겠습니다. 이는 피어가 채널 생성을 확인하고 자신의 공개 채널 키를 보냈다는 의미입니다. 이제 우리의 개인 채널 키와 피어의 공개 채널 키가 있으므로 [공유 키](/v3/documentation/network/protocols/adnl/adnl-tcp#getting-a-shared-key-using-ecdh)를 계산할 수 있습니다.

이제 공유 채널 키를 계산했으니, 이를 2개의 키로 만들어야 합니다 - 하나는 발신 메시지 암호화용, 다른 하나는 수신 메시지 복호화용입니다.
2개의 키를 만드는 것은 꽤 간단합니다. 두 번째 키는 공유 키를 역순으로 쓴 것과 같습니다. 예시:

```
Shared key : AABB2233

First key: AABB2233
Second key: 3322BBAA
```

어떤 키를 어디에 사용할지 결정하는 것만 남았습니다. 우리의 공개 채널 키 ID와 서버 채널의 공개 키 ID를 uint256 숫자 형식으로 변환하여 비교하면 됩니다. 이 방식은 서버와 클라이언트가 어떤 키를 무엇에 사용할지 결정하는 것을 보장하기 위해 사용됩니다. 서버가 첫 번째 키를 암호화에 사용한다면 이 방식으로 클라이언트는 항상 그것을 복호화에 사용할 것입니다.

사용 조건:

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

### 채널 내 통신

이후의 모든 패킷 교환은 채널 내에서 이루어지며 채널 키가 암호화에 사용됩니다.
차이점을 보기 위해 새로 생성된 채널 내에서 동일한 `dht.getSignedAddressList` 요청을 보내보겠습니다.

동일한 `adnl.packetContents` 구조를 사용하여 채널용 패킷을 구축해 보겠습니다:

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

채널 내 패킷은 꽤 단순하며 본질적으로 시퀀스(seqno)와 메시지로만 구성됩니다.

직렬화 후에는 이전처럼 패킷의 sha256 해시를 계산합니다. 그런 다음 채널의 발신 패킷을 위한 채널 키로 패킷을 암호화합니다.
우리의 발신 메시지 암호화 키의 `pub.aes` [ID를 계산](/v3/documentation/network/protocols/adnl/adnl-tcp#getting-key-id)하고 패킷을 구축합니다:

```
bcd1cf47b9e657200ba21d94b822052cf553a548f51f539423c8139a83162180 -- ID of encryption key of our outgoing messages 
6185385aeee5faae7992eb350f26ba253e8c7c5fa1e3e1879d9a0666b9bd6080 -- sha256 content hash (before encryption)
...                                                              -- the encrypted content of the packet
```

UDP를 통해 패킷을 보내고 응답을 기다립니다. 응답으로 우리가 보낸 것과 동일한 타입의 패킷을 받게 되지만, `dht.getSignedAddressList` 요청에 대한 답변이 포함됩니다.

## 기타 메시지 타입

기본 통신을 위해서는 위에서 논의한 `adnl.message.query`와 `adnl.message.answer` 같은 메시지가 사용되지만, 특정 상황을 위한 다른 타입의 메시지도 있으며 이 섹션에서 설명하겠습니다.

### adnl.message.part

이 메시지 타입은 `adnl.message.answer`와 같은 다른 가능한 메시지 타입의 일부입니다. 메시지가 단일 UDP 데이터그램으로 전송하기에 너무 큰 경우에 사용됩니다.

```tlb
adnl.message.part 
hash:int256            -- sha256 hash of the original message
total_size:int         -- original message size
offset:int             -- offset according to the beginning of the original message
data:bytes             -- piece of data of the original message
   = adnl.Message;
```

따라서 원본 메시지를 조립하려면 여러 부분을 받아서 오프셋에 따라 단일 바이트 배열로 연결해야 합니다.
그리고 나서 메시지로 처리합니다(이 바이트 배열의 ID 접두사에 따라).

### adnl.message.custom

```tlb
adnl.message.custom data:bytes = adnl.Message;
```

이러한 메시지는 상위 레벨의 로직이 요청-응답 형식과 일치하지 않을 때 사용됩니다. 이 타입의 메시지는 query_id와 다른 필드 없이 바이트 배열만 전달하므로 처리를 완전히 상위 레벨로 이동할 수 있습니다.
이 타입의 메시지는 예를 들어 RLDP에서 사용됩니다. 많은 요청에 대해 하나의 응답만 있을 수 있기 때문에 이 로직은 RLDP 자체에 의해 제어됩니다.

### 결론

이후의 통신은 이 글에서 설명한 로직을 기반으로 이루어지지만,
패킷의 내용은 DHT와 RLDP 같은 상위 레벨 프로토콜에 따라 달라집니다.

## 참조

*여기 [Oleg Baranov](https://github.com/xssnick)의 [원본 문서 링크](https://github.com/xssnick/ton-deep-doc/blob/master/ADNL-UDP-Internal.md)가 있습니다.*
