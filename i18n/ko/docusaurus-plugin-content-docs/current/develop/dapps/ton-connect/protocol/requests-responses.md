# 요청 및 응답

앱이 지갑에 요청을 보냅니다. 지갑은 앱에 응답과 이벤트를 보냅니다.

```tsx
type AppMessage = ConnectRequest | AppRequest;

type WalletMessage = WalletResponse | WalletEvent;
```

### 앱 매니페스트

앱이 지갑에 메타 정보를 전달하려면 매니페스트가 있어야 합니다. 매니페스트는 다음 형식의 'tonconnect-manifest.json'이라는 JSON 파일입니다:

```json
{
  "url": "<app-url>",                        // required
  "name": "<app-name>",                      // required
  "iconUrl": "<app-icon-url>",               // required
  "termsOfUseUrl": "<terms-of-use-url>",     // optional
  "privacyPolicyUrl": "<privacy-policy-url>" // optional
}
```

매니페스트를 앱의 루트(예: `https://myapp.com/tonconnect-manifest.json`)에 배치하는 것이 가장 좋습니다. 이를 통해 지갑이 앱을 더 잘 처리하고 앱에 연결된 UX를 개선할 수 있습니다.
해당 URL로 매니페스트를 GET할 수 있는지 확인하세요.

#### 필드 설명

- `url` -- 앱 URL. 디앱 식별자로 사용됩니다. 지갑에서 아이콘을 클릭한 후 디앱을 여는 데 사용됩니다. 'https://mydapp.com/' 대신 'https://mydapp.com'와 같이 닫는 슬래시 없이 URL을 전달하는 것이 좋습니다.
- 이름\` -- 앱 이름. 단순할 수 있으며 식별자로 사용되지 않습니다.
- `iconUrl` -- 앱 아이콘의 URL입니다. PNG, ICO, ... 형식이어야 합니다. SVG 아이콘은 지원되지 않습니다. 180x180px PNG 아이콘에 URL을 완벽하게 전달합니다.
- `termsOfUseUrl` -- (선택 사항) 이용약관 문서의 URL입니다. 일반 앱의 경우 선택 사항이지만 Tonkeeper 추천 앱 목록에 있는 앱의 경우 필수입니다.
- `개인정보보호정책URL` -- (선택 사항) 개인정보 보호정책 문서의 URL. 일반 앱의 경우 선택 사항이지만 Tonkeeper 추천 앱 목록에 있는 앱의 경우 필수입니다.

### 연결 시작

앱의 요청 메시지는 **초기 요청**입니다.

```tsx
type ConnectRequest = {
  manifestUrl: string;
  items: ConnectItem[], // data items to share with the app
}

// In the future we may add other personal items.
// Or, instead of the wallet address we may ask for per-service ID.
type ConnectItem = TonAddressItem | TonProofItem | ...;

type TonAddressItem = {
  name: "ton_addr";
}
type TonProofItem = {
  name: "ton_proof";
  payload: string; // arbitrary payload, e.g. nonce + expiration timestamp.
}
```

연결 요청 설명:

- manifestUrl\`: 앱의 톤커넥트-매니페스트.json 링크
- '항목': 앱과 공유할 데이터 항목입니다.

사용자가 요청을 승인하면 월렛은 **ConnectEvent** 메시지로 응답합니다.

```tsx
type ConnectEvent = ConnectEventSuccess | ConnectEventError;

type ConnectEventSuccess = {
  event: "connect";
  id: number; // increasing event counter
  payload: {
      items: ConnectItemReply[];
      device: DeviceInfo;   
  }
}
type ConnectEventError = {
  event: "connect_error",
  id: number; // increasing event counter
  payload: {
      code: number;
      message: string;
  }
}

type DeviceInfo = {
  platform: "iphone" | "ipad" | "android" | "windows" | "mac" | "linux";
  appName:      string; // e.g. "Tonkeeper"  
  appVersion:  string; // e.g. "2.3.367"
  maxProtocolVersion: number;
  features: Feature[]; // list of supported features and methods in RPC
                                // Currently there is only one feature -- 'SendTransaction'; 
}

type Feature = { name: 'SendTransaction', maxMessages: number } | // `maxMessages` is maximum number of messages in one `SendTransaction` that the wallet supports
        { name: 'SignData' };

type ConnectItemReply = TonAddressItemReply | TonProofItemReply ...;

// Untrusted data returned by the wallet. 
// If you need a guarantee that the user owns this address and public key, you need to additionally request a ton_proof.
type TonAddressItemReply = {
  name: "ton_addr";
  address: string; // TON address raw (`0:<hex>`)
  network: NETWORK; // network global_id
  publicKey: string; // HEX string without 0x
  walletStateInit: string; // Base64 (not url safe) encoded stateinit cell for the wallet contract
}

type TonProofItemReply = TonProofItemReplySuccess | TonProofItemReplyError;

type TonProofItemReplySuccess = {
  name: "ton_proof";
  proof: {
    timestamp: string; // 64-bit unix epoch time of the signing operation (seconds)
    domain: {
      lengthBytes: number; // AppDomain Length
      value: string;  // app domain name (as url part, without encoding) 
    };
    signature: string; // base64-encoded signature
    payload: string; // payload from the request
  }
}

type TonProofItemReplyError = {
  name: "ton_addr";
  error: {
      code: ConnectItemErrorCode;
      message?: string;
  }
}

enum NETWORK {
  MAINNET = '-239',
  TESTNET = '-3'
}
```

**연결 이벤트 오류 코드:**

| 코드  | 설명                               |
| --- | -------------------------------- |
| 0   | 알 수 없는 오류                        |
| 1   | 잘못된 요청                           |
| 2   | 앱 매니페스트를 찾을 수 없음                 |
| 3   | 앱 매니페스트 콘텐츠 오류                   |
| 100 | 알 수 없는 앱                         |
| 300 | 사용자가 연결을 거부했습니다. |

**연결 항목 오류 코드:**

| 코드  | 설명                              |
| --- | ------------------------------- |
| 0   | 알 수 없는 오류                       |
| 400 | 메서드가 지원되지 않습니다. |

지갑이 요청된 '연결 항목'을 지원하지 않는 경우(예: "ton_proof"), 요청된 항목에 해당하는 다음 연결 항목 응답을 다음 구조의
으로 보내야 합니다:

```ts
type ConnectItemReplyError = {
  name: "<requested-connect-item-name>";
  error: {
      code: 400;
      message?: string;
  }
}
```

### 주소 증명 서명 (`ton_proof`)

톤증명항목\`이 요청되면 지갑은 선택한 계정의 키에 대한 소유권을 증명합니다. 서명된 메시지는 바인딩됩니다:

- 온체인 메시지와 메시지를 구분하기 위한 고유 접두사. (`ton-connect`)
- 지갑 주소.
- 앱 도메인
- 서명 타임스탬프
- 앱의 사용자 지정 페이로드(서버가 논스, 쿠키 ID, 만료 시간을 저장할 수 있는 위치).

```
message = utf8_encode("ton-proof-item-v2/") ++ 
          Address ++
          AppDomain ++
          Timestamp ++  
          Payload 
signature = Ed25519Sign(privkey, sha256(0xffff ++ utf8_encode("ton-connect") ++ sha256(message)))
```

어디에:

- '주소'는 시퀀스로 인코딩된 지갑 주소입니다:
  - 워크체인\`: 32비트 부호 있는 정수 빅 엔디안;
  - 해시\`: 256비트 부호 없는 정수 빅 엔디안;
- 앱 도메인\`은 길이 ++ 인코딩된 도메인 이름입니다.
  - 길이\`는 utf-8로 인코딩된 앱 도메인 이름 길이(바이트)의 32비트 값입니다.
  - 인코딩된 도메인 이름`아이디`길이\`-바이트 utf-8로 인코딩된 앱 도메인 이름
- 서명 작업의 `타임스탬프` 64비트 유닉스 에포크 시간
- 페이로드\`는 가변 길이 바이너리 문자열입니다.

참고: 페이로드는 가변 길이의 신뢰할 수 없는 데이터입니다. 불필요한 길이 접두사를 사용하지 않으려면 메시지 마지막에 넣으면 됩니다.

서명은 공개 키로 확인해야 합니다:

1. 먼저, '주소'에 배포된 스마트 컨트랙트에서 `get_public_key` get-method를 통해 공개키를 가져옵니다.

2. 스마트 컨트랙트가 아직 배포되지 않았거나 get 메서드가 누락된 경우 필요합니다:

   1. 톤어드레스아이템응답.walletStateInit`을 파싱하고 stateInit에서 공개키를 가져옵니다. 지갑 상태 초기화 코드`를 표준 지갑 컨트랙트의 코드와 비교하고 찾은 지갑 버전에 따라 데이터를 파싱할 수 있습니다.

   2. 톤 주소 항목 회신\`이 획득한 공개 키와 동일한지 확인합니다.

   3. 톤어드레스아이템리플리.지갑스테이트인잇.해시()`가 `톤어드레스아이템리플리.주소`와 같은지 확인합니다. .hash()`는 BoC 해시를 의미합니다.

## 메시지

- 앱에서 지갑으로 전송되는 모든 메시지는 작업 요청입니다.
- 지갑에서 애플리케이션으로 보내는 메시지는 앱 요청에 대한 응답이거나 지갑 측면에서 사용자 행동에 의해 트리거되는 이벤트일 수 있습니다.

**사용 가능한 작업:**

- sendTransaction
- signData
- 연결 끊기

**사용 가능한 이벤트:**

- 연결
- connect_error
- 연결 끊기

### 구조

**모든 앱 요청의 구조는 다음과 같습니다(예: json-rpc 2.0)**.

```tsx
interface AppRequest {
	method: string;
	params: string[];
	id: string;
}
```

Where

- 메소드\`: 작업 이름('sendTransaction', 'signMessage', ...)
- `params`: 작업별 매개변수 배열
- `id`: 요청과 응답을 일치시킬 수 있는 식별자 증가

**지갑 메시지는 응답 또는 이벤트입니다.**

응답은 json-rpc 2.0 응답으로 형식이 지정된 객체입니다. 응답 `id`는 요청의 아이디와 일치해야 합니다.

지갑은 해당 세션에서 마지막으로 처리된 요청 ID보다 크지 않은 ID의 요청은 수락하지 않습니다.

```tsx
type WalletResponse = WalletResponseSuccess | WalletResponseError;

interface WalletResponseSuccess {
    result: string;
    id: string;
}

interface WalletResponseError {
    error: { code: number; message: string; data?: unknown };
    id: string;
}
```

이벤트는 이벤트 이름과 동일한 `event` 속성, 이벤트 카운터를 증가시키는 `id`(이벤트 요청이 없으므로 `request.id`와 \*\*관련 없음), 이벤트 추가 데이터를 포함하는 `payload`를 가진 객체입니다.

```tsx
interface WalletEvent {
    event: WalletEventName;
    id: number; // increasing event counter
    payload: <event-payload>; // specific payload for each event
}

type WalletEventName = 'connect' | 'connect_error' | 'disconnect';
```

지갑은 새 이벤트를 생성하는 동안 `id`를 증가시켜야 합니다. (모든 다음 이벤트에는 `id` > 이전 이벤트 `id`가 있어야 합니다).

DApp은 해당 세션에서 마지막으로 처리된 이벤트 ID보다 크지 않은 ID를 가진 이벤트는 수락하지 않습니다.

### 방법

#### 거래 서명 및 전송

앱이 **SendTransactionRequest**를 전송합니다:

```tsx
interface SendTransactionRequest {
	method: 'sendTransaction';
	params: [<transaction-payload>];
	id: string;
}
```

여기서 `<transaction-payload>`는 다음 속성을 가진 JSON입니다:

- valid_until\`(정수, 선택 사항): 유닉스 타임스탬프. 이 순간 이후 트랜잭션은 유효하지 않습니다.
- '네트워크'(네트워크, 선택 사항): 디앱이 트랜잭션을 전송할 네트워크(메인넷 또는 테스트넷)입니다. 설정하지 않으면 현재 지갑에 설정된 네트워크로 트랜잭션이 전송되지만, 이는 안전하지 않으므로 디앱은 항상 네트워크를 설정하기 위해 노력해야 합니다. 네트워크\` 매개변수가 설정되어 있지만 지갑에 다른 네트워크가 설정되어 있는 경우, 지갑은 경고와 함께 이 트랜잭션 전송을 허용하지 않음을 표시해야 합니다.
- 발신자(`<wc>:<hex>` 형식의 문자열, 선택 사항) - 디앱이 트랜잭션을 전송할 발신자 주소입니다. 설정하지 않으면 지갑은 트랜잭션 승인 시점에 사용자가 발신자 주소를 선택할 수 있도록 허용합니다. 'from` 파라미터를 설정하면 지갑은 사용자가 발신자 주소를 선택할 수 없도록 하고, 지정된 주소에서 전송이 불가능한 경우 경고와 함께 이 트랜잭션의 전송을 허용하지 않음을 표시해야 합니다.
- 메시지\`(메시지 배열): 지갑 컨트랙트에서 다른 계정으로 보내는 1~4개의 발신 메시지. 모든 메시지는 순서대로 전송되지만 **월렛은 메시지가 동일한 순서로 전달되고 실행될 것이라고 보장할 수 없습니다**.

메시지 구조:

- 주소\` (문자열): 메시지 대상
- 금액\`(십진수 문자열): 전송할 나노코인의 개수입니다.
- 페이로드\`(문자열 base64, 선택 사항): Base64로 인코딩된 원시 1셀 BoC입니다.
- stateInit\`(문자열 base64, 선택 사항): Base64로 인코딩된 원시 일회성 셀 BoC입니다.

#### 일반적인 사례

1. 페이로드 없음, 상태 초기화 없음: 메시지 없이 간편하게 전송할 수 있습니다.
2. 페이로드에는 32개의 0비트가 접두사로 붙으며 상태 초기화: 문자 메시지를 통한 간단한 전송이 없습니다.
3. 페이로드가 없거나 32개의 0비트로 접두사가 붙은 상태Init이 존재합니다: 컨트랙트의 배포.

<details>
<summary>예</summary>

```json5
{
  "valid_until": 1658253458,
  "network": "-239", // enum NETWORK { MAINNET = '-239', TESTNET = '-3'}
  "from": "0:348bcf827469c5fc38541c77fdd91d4e347eac200f6f2d9fd62dc08885f0415f",
  "messages": [
    {
      "address": "0:412410771DA82CBA306A55FA9E0D43C9D245E38133CB58F1457DFB8D5CD8892F",
      "amount": "20000000",
      "stateInit": "base64bocblahblahblah==" //deploy contract
    },{
      "address": "0:E69F10CC84877ABF539F83F879291E5CA169451BA7BCE91A37A5CED3AB8080D3",
      "amount": "60000000",
      "payload": "base64bocblahblahblah==" //transfer nft to new deployed account 0:412410771DA82CBA306A55FA9E0D43C9D245E38133CB58F1457DFB8D5CD8892F
    }
  ]
}
```

</details>

월렛이 **SendTransactionResponse**로 응답합니다:

```tsx
type SendTransactionResponse = SendTransactionResponseSuccess | SendTransactionResponseError; 

interface SendTransactionResponseSuccess {
    result: <boc>;
    id: string;
	
}

interface SendTransactionResponseError {
   error: { code: number; message: string };
   id: string;
}
```

**오류 코드:**

| 코드  | 설명                               |
| --- | -------------------------------- |
| 0   | 알 수 없는 오류                        |
| 1   | 잘못된 요청                           |
| 100 | 알 수 없는 앱                         |
| 300 | 사용자가 거래를 거부했습니다. |
| 400 | 지원되지 않는 방법                       |

#### 서명 데이터(실험적)

> 경고: 이 방법은 현재 실험적인 방법이며 향후 변경될 수 있습니다.

앱이 **SignDataRequest**를 전송합니다:

```tsx
interface SignDataRequest {
	method: 'signData';
	params: [<sign-data-payload>];
	id: string;
}
```

여기서 `<sign-data-payload>`는 다음 속성을 가진 JSON입니다:

- `schema_crc`(정수): 도메인 분리를 정의하는 페이로드 셀의 레이아웃을 나타냅니다.
- 셀\`(문자열, base64로 인코딩된 셀): TL-B 정의에 따라 임의의 데이터를 포함합니다.
- 공개키`(0x가 없는 HEX 문자열, 선택 사항): DApp이 데이터에 서명할 키 쌍의 공개 키입니다. 설정하지 않으면 지갑이 서명할 키 쌍에 제한이 없습니다. 공개키` 파라미터를 설정하면 지갑은 이 공개키에 해당하는 키쌍으로 서명해야 하며, 지정된 키쌍으로 서명이 불가능하면 경고 메시지를 표시하고 이 데이터에 서명을 허용하지 않아야 합니다.

서명은 다음과 같은 방식으로 계산됩니다:
`ed25519(uint32be(schema_crc) ++ uint64be(timestamp) ++ cell_hash(X), privkey)`.

[자세한 내용 보기](https://github.com/oleganza/TEPs/blob/datasig/text/0000-data-signatures.md)

지갑은 스키마_rc에 따라 셀을 디코딩하고 사용자에게 해당 데이터를 표시해야 합니다.
지갑에서 스키마_rc를 알 수 없는 경우, 지갑은 사용자에게 위험 알림/UI를 표시해야 합니다.

월렛이 **SignDataResponse**로 응답합니다:

```tsx
type SignDataResponse = SignDataResponseSuccess | SignDataResponseError; 

interface SignDataResponseSuccess {
    result: {
      signature: string; // base64 encoded signature 
      timestamp: string; // UNIX timestamp in seconds (UTC) at the moment on creating the signature.
    };
    id: string;
}

interface SignDataResponseError {
   error: { code: number; message: string };
   id: string;
}
```

**오류 코드:**

| 코드  | 설명                               |
| --- | -------------------------------- |
| 0   | 알 수 없는 오류                        |
| 1   | 잘못된 요청                           |
| 100 | 알 수 없는 앱                         |
| 300 | 사용자가 요청을 거부했습니다. |
| 400 | 지원되지 않는 방법                       |

#### 연결 해제 작업

사용자가 디앱에서 지갑 연결을 끊으면 디앱은 지갑이 리소스를 절약하고 불필요한 세션을 삭제할 수 있도록 지갑에 알려야 합니다.
지갑이 연결이 끊긴 상태로 인터페이스를 업데이트할 수 있도록 합니다.

```tsx
interface DisconnectRequest {
	method: 'disconnect';
	params: [];
	id: string;
}
```

지갑이 **연결 끊김 응답**으로 응답합니다:

```ts
type DisconnectResponse = DisconnectResponseSuccess | DisconnectResponseError; 

interface DisconnectResponseSuccess {
    id: string;
    result: { };
}

interface DisconnectResponseError {
   error: { code: number; message: string };
   id: string;
}
```

디앱에 의해 연결 해제가 초기화된 경우 지갑은 '연결 해제' 이벤트를 발생시키지 않아야 합니다.

**오류 코드:**

| 코드  | 설명         |
| --- | ---------- |
| 0   | 알 수 없는 오류  |
| 1   | 잘못된 요청     |
| 100 | 알 수 없는 앱   |
| 400 | 지원되지 않는 방법 |

### 지갑 이벤트

<ins>연결 해제</ins>

사용자가 지갑에서 앱을 삭제하면 이벤트가 발생합니다. 앱은 이벤트에 반응하여 저장된 세션을 삭제해야 합니다. 사용자가 앱 측에서 지갑 연결을 끊으면 이벤트가 발생하지 않으며 세션 정보는 로컬 저장소에 남아 있습니다.

```tsx
interface DisconnectEvent {
	type: "disconnect",
	id: number; // increasing event counter
	payload: { }
}
```

<ins>연결</ins>

```tsx
type ConnectEventSuccess = {
    event: "connect",
    id: number; // increasing event counter
    payload: {
        items: ConnectItemReply[];
        device: DeviceInfo;
    }
}
type ConnectEventError = {
    event: "connect_error",
    id: number; // increasing event counter
    payload: {
        code: number;
        message: string;
    }
}
```
