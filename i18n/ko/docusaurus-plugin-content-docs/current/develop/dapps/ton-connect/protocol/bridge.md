# 브리지 API

브리지는 앱에서 지갑으로 또는 그 반대로 메시지를 전달하는 전송 메커니즘입니다.

- **브릿지는 지갑 제공업체에서 유지 관리합니다**. 앱 개발자는 브릿지를 선택하거나 구축할 필요가 없습니다. 각 지갑의 브릿지는 [지갑 목록](https://github.com/ton-blockchain/wallets-list) 설정에 나열되어 있습니다.
- **메시지는 종단 간 암호화됩니다.** Bridge는 앱이나 지갑의 내용이나 장기 식별자를 볼 수 없습니다.
- \*\*Bridge는 앱과 지갑을 구분하지 않습니다. 둘 다 단순히 클라이언트일 뿐입니다.
- Bridge는 각 수신자의 **클라이언트 ID**에 대해 별도의 메시지 대기열을 유지합니다.

Bridge는 두 가지 버전으로 제공됩니다:

- [HTTP 브리지](#http-bridge): 외부 앱 및 서비스용입니다.
- [JS 브리지](#js-bridge): 지갑 내에서 열린 앱의 경우 또는 지갑이 브라우저 확장 프로그램인 경우.

## HTTP 브리지

ID가 **A**인 클라이언트가 브리지에 연결하여 수신 요청을 수신 대기합니다.

**고객 ID는 반비공개:** 앱과 지갑은 예기치 않게 메시지가 삭제되는 것을 방지하기 위해 다른 단체와 ID를 공유해서는 안 됩니다.

**클라이언트는 몇 개의 클라이언트 ID로 구독할 수 있습니다** - 이 경우 쉼표로 구분된 ID를 열거해야 합니다. 예: `?client_id=<A1>,<A2>,<A3>`

```tsx
request
    GET /events?client_id=<to_hex_str(A)>

    Accept: text/event-stream
```

**브릿지 두 번째 (다른) 시간 구독하기**

```tsx
request
    GET /events?client_id=<to_hex_str(A)>&last_event_id=<lastEventId>

    Accept: text/event-stream
```

**마지막 이벤트아이디** - 마지막 SSE 이벤트 지갑의 이벤트아이디가 브리지를 통과했습니다. 이 경우 지갑은 마지막 연결 이후에 발생한 모든 이벤트를 가져옵니다.

클라이언트 A에서 클라이언트 B로 메시지를 보내는 중 TTL이 너무 높으면 브리지가 오류를 반환합니다.

```tsx
request
    POST /message?client_id=<to_hex_str(A)>?to=<to_hex_str(B)>&ttl=300&topic=<sendTransaction|signData>

    body: <base64_encoded_message>
```

주제`[선택 사항] 쿼리 매개변수는 브리지에서 지갑에 푸시 알림을 전달하는 데 사용할 수 있습니다. 매개변수가 제공되면 암호화된`메시지\` 내부에서 호출되는 RPC 메서드와 일치해야 합니다.

브리지는 메시지를 최대 TTL(초 단위)까지 버퍼링하지만 수신자가 메시지를 수신하는 즉시 메시지를 제거합니다.

TTL이 브리지 서버의 하드 제한을 초과하는 경우 HTTP 400으로 응답해야 합니다. 브리지는 최소 300초 TTL을 지원해야 합니다.

브리지는 클라이언트 `A`에서 클라이언트 `B`로 주소가 지정된 `base64_encoded_message` 메시지를 수신하면 `BridgeMessage` 메시지를 생성합니다:

```js
{
  "from": <to_hex_str(A)>,
  "message": <base64_encoded_message>
}
```

를 생성하고 SSE 연결을 통해 클라이언트 B로 전송합니다.

```js
resB.write(BridgeMessage)
```

### 하트비트

연결을 유지하기 위해 브리지 서버는 주기적으로 SSE 채널에 "하트비트" 메시지를 보내야 합니다. 클라이언트는 이러한 메시지를 무시해야 합니다.
따라서 브리지 하트비트 메시지는 '하트비트'라는 단어가 포함된 문자열입니다.

## 유니버설 링크

앱이 연결을 시작하면 QR코드 또는 범용 링크를 통해 지갑으로 직접 전송합니다.

```bash
https://<wallet-universal-url>?
                               v=2&
                               id=<to_hex_str(A)>&
                               r=<urlsafe(json.stringify(ConnectRequest))>&
                               ret=back
```

매개변수 **v**는 프로토콜 버전을 지정합니다. 지원되지 않는 버전은 지갑에서 허용되지 않습니다.

매개변수 **id**는 앱의 클라이언트 ID를 16진수로 인코딩('0x' 접두사 제외)하여 지정합니다.

매개변수 **r**는 URL-안전 json [ConnectRequest](/develop/dapps/ton-connect/pro 프로토콜/requests-responses#initiating-connection)를 지정합니다.

매개변수 **ret**(선택 사항)는 사용자가 요청에 서명/거부할 때 딥링크의 반환 전략을 지정합니다.

- '뒤로'(기본값)는 딥링크 점프를 초기화한 앱(예: 브라우저, 기본 앱 등)으로 돌아간다는 의미입니다,
- '없음'은 사용자 작업 후 점프가 없음을 의미합니다;
- URL: 지갑은 사용자의 작업을 완료한 후 이 URL을 열 것입니다. 웹페이지인 경우 앱의 URL을 전달해서는 안 된다는 점에 유의하세요. 이 옵션은 네이티브 앱에서 '뒤로' 옵션으로 발생할 수 있는 OS 관련 문제를 해결하려면 이 옵션을 사용해야 합니다.

빈 딥링크에는 `ret` 매개변수가 지원되어야 하며, 다른 작업 확인(트랜잭션 보내기, 원시 서명 등) 후 지갑 동작을 지정하는 데 사용할 수 있습니다.

```bash
https://<wallet-universal-url>?ret=back
```

링크는 QR코드에 삽입하거나 직접 클릭할 수 있습니다.

초기 요청은 (1) 아직 전송되는 개인 데이터가 없고, (2) 앱이 지갑의 신원조차 알지 못하기 때문에 암호화되지 않습니다.

### 통합 디딤링크 `tc`

지갑은 자체 유니버설 링크 외에도 통합된 딥링크를 지원해야 합니다.

이를 통해 애플리케이션은 모든 지갑에 연결하는 데 사용할 수 있는 단일 QR 코드를 생성할 수 있습니다.

보다 구체적으로, 지갑은 자체 `<wallet-universal-url>`뿐만 아니라 `tc://` 디플링크를 지원해야 합니다.

따라서 지갑에서 다음 '연결 요청'을 처리해야 합니다:

```bash
tc://?
       v=2&
       id=<to_hex_str(A)>&
       r=<urlsafe(json.stringify(ConnectRequest))>&
       ret=back
```

## JS 브리지

임베디드 앱은 삽입된 바인딩 `window.<wallet-js-bridge-key>.tonconnect`를 통해 사용합니다.

지갑 목록](https://github.com/ton-blockchain/wallets-list)에서 `wallet-js-bridge-key`를 지정할 수 있습니다.

JS 브릿지는 지갑과 앱이 같은 기기에서 실행되므로 통신이 암호화되지 않습니다.

이 앱은 세션 키와 암호화 없이 일반 텍스트 요청 및 응답으로 직접 작동합니다.

```tsx
interface TonConnectBridge {
    deviceInfo: DeviceInfo; // see Requests/Responses spec
    walletInfo?: WalletInfo;
    protocolVersion: number; // max supported Ton Connect version (e.g. 2)
    isWalletBrowser: boolean; // if the page is opened into wallet's browser
    connect(protocolVersion: number, message: ConnectRequest): Promise<ConnectEvent>;
    restoreConnection(): Promise<ConnectEvent>;
    send(message: AppRequest): Promise<WalletResponse>;
    listen(callback: (event: WalletEvent) => void): () => void;
}
```

HTTP 브릿지와 마찬가지로, 브릿지의 지갑 쪽은 사용자가 세션을 확인할 때까지 [ConnectRequest](/develop/dapps/ton-connect/protocol/requests-responses#initiating-connection)를 제외한 앱 요청을 수신하지 않습니다. 기술적으로는 웹뷰에서 브리지 컨트롤러로 메시지가 도착하지만 조용히 무시됩니다.

자동 연결()\*\* 및 \*\*연결()\*\*을 무음 및 비무음 연결 시도로 구현하는 SDK입니다.

### 지갑 정보(선택 사항)

지갑 메타데이터를 나타냅니다. 지갑이 [wallets-list.json](https://github.com/ton-blockchain/wallets-list)에 나열되어 있지 않더라도 인젝터블 지갑이 TonConnect에서 작동하도록 정의할 수 있습니다.

지갑 메타데이터 형식:

```ts
interface WalletInfo {
    name: string;
    image: <png image url>;
    tondns?:  string;
    about_url: <about page url>;
}
```

자세한 속성 설명: https://github.com/ton-blockchain/wallets-list#entry-format.

톤커넥트브리지 지갑정보`가 정의되어 있고 지갑이 [wallets-list.json](https://github.com/ton-blockchain/wallets-list)에 나열되어 있는 경우, `톤커넥트브리지 지갑정보\` 속성이 지갑 목록의 해당 지갑 속성을 재정의합니다.

### connect()

연결 요청을 시작하며, 이는 HTTP 브리지를 사용할 때 QR/링크와 유사합니다.

앱이 이전에 현재 계정에 대해 승인된 경우 - ConnectEvent와 자동으로 연결합니다. 그렇지 않으면 사용자에게 확인 대화 상자를 표시합니다.

명시적인 사용자 작업(예: 연결 버튼 클릭) 없이 `connect` 메서드를 사용해서는 안 됩니다. 이전 연결을 자동으로 복원하려면 `restoreConnection` 메서드를 사용해야 합니다.

### 복원 연결()

이전 연결을 복원하려고 시도합니다.

앱이 이전에 현재 계정에 대해 승인된 경우 - '톤_주소' 데이터 항목만 있는 새로운 '연결 이벤트'와 자동으로 연결됩니다.

그렇지 않으면 오류 코드 100(알 수 없는 앱)과 함께 `ConnectEventError`를 반환합니다.

### send()

ConnectRequest를 제외한 [메시지](/개발/앱/톤-연결/프로토콜/요청-응답#메시지)를 브리지로 전송합니다(HTTP 브리지를 사용할 때는 QR 코드로, JS 브리지를 사용할 때는 연결로 이동).
WalletResponse로 직접 프로미스를 반환하므로 `listen`으로 응답을 기다릴 필요가 없습니다;

### listen()

지갑에서 이벤트 리스너를 등록합니다.

구독 취소 함수를 반환합니다.

현재는 '연결 해제' 이벤트만 진행 중입니다. 추후 계정 전환 이벤트 및 기타 지갑 이벤트가 추가될 예정입니다.
