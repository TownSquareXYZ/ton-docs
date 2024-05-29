# 자바스크립트 SDK와의 통합 매뉴얼

이 튜토리얼에서는 TON Connect 2.0 인증을 지원하는 샘플 웹 앱을 만들어 보겠습니다. 이를 통해 서명 확인을 통해 당사자 간의 계약 설정 없이도 사기성 신원 사칭의 가능성을 제거할 수 있습니다.

## 문서 링크

1. [톤커넥트 문서](https://www.npmjs.com/package/@tonconnect/sdk)
2. [지갑-애플리케이션 메시지 교환 프로토콜](https://github.com/ton-connect/docs/blob/main/requests-responses.md)
3. [지갑 쪽의 톤키퍼 구현](https://github.com/tonkeeper/wallet/tree/main/src/tonconnect)

## 전제 조건

앱과 지갑 간의 연결이 원활하게 이루어지려면 웹 앱에서 지갑 애플리케이션을 통해 액세스할 수 있는 매니페스트를 사용해야 합니다. 이를 위한 전제 조건은 일반적으로 정적 파일을 위한 호스트입니다. 예를 들어 개발자가 GitHub 페이지를 사용하거나 자신의 컴퓨터에서 호스팅되는 TON 사이트를 사용하여 웹사이트를 배포하고자 한다고 가정해 보겠습니다. 따라서 이는 웹 앱 사이트에 공개적으로 액세스할 수 있다는 것을 의미합니다.

## 지갑 지원 목록 가져오기

톤 블록체인의 전반적인 채택을 늘리려면 톤 커넥트 2.0이 방대한 수의 애플리케이션 및 지갑 연결 통합을 촉진할 수 있어야 합니다. 최근 TON 커넥트 2.0의 지속적인 개발을 통해 톤키퍼, 톤허브, 마이톤월렛 및 기타 지갑을 다양한 TON 생태계 앱과 연결할 수 있게 된 것은 매우 중요한 일입니다. 궁극적으로는 TON 커넥트 프로토콜을 통해 TON에 구축된 모든 지갑 유형과 애플리케이션 간에 데이터를 교환할 수 있도록 하는 것이 저희의 미션입니다. 현재로서는 TON 커넥트가 현재 TON 생태계 내에서 운영되는 광범위한 지갑 목록을 로드할 수 있는 기능을 제공함으로써 이를 실현하고 있습니다.

현재 샘플 웹 앱에서는 다음과 같은 기능을 사용할 수 있습니다:

1. 는 TON Connect SDK(통합을 간소화하기 위한 라이브러리)를 로드합니다,
2. 커넥터를 생성합니다(현재 애플리케이션 매니페스트가 없음),
3. 는 지원되는 지갑 목록을 로드합니다([GitHub의 wallets.json](https://raw.githubusercontent.com/ton-connect/wallets-list/main/wallets.json)에서).

학습을 위해 다음 코드가 설명하는 HTML 페이지를 살펴보겠습니다:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <script src="https://unpkg.com/@tonconnect/sdk@latest/dist/tonconnect-sdk.min.js" defer></script>  <!-- (1) -->
  </head>
  <body>
    <script>
      window.onload = async () => {
        const connector = new TonConnectSDK.TonConnect();  // (2)
        const walletsList = await connector.getWallets();  // (3)
        
        console.log(walletsList);
      }
    </script>
  </body>
</html>
```

브라우저에서 이 페이지를 로드하고 콘솔을 들여다보면 이와 같은 내용이 표시될 수 있습니다:

```bash
> Array [ {…}, {…} ]

0: Object { name: "Tonkeeper", imageUrl: "https://tonkeeper.com/assets/tonconnect-icon.png", aboutUrl: "https://tonkeeper.com", … }
  aboutUrl: "https://tonkeeper.com"
  bridgeUrl: "https://bridge.tonapi.io/bridge"
  deepLink: undefined
  embedded: false
  imageUrl: "https://tonkeeper.com/assets/tonconnect-icon.png"
  injected: false
  jsBridgeKey: "tonkeeper"
  name: "Tonkeeper"
  tondns: "tonkeeper.ton"
  universalLink: "https://app.tonkeeper.com/ton-connect"
```

TON Connect 2.0 사양에 따르면 지갑 앱 정보는 항상 다음 형식을 사용합니다:

```js
{
    name: string;
    imageUrl: string;
    tondns?: string;
    aboutUrl: string;
    universalLink?: string;
    deepLink?: string;
    bridgeUrl?: string;
    jsBridgeKey?: string;
    injected?: boolean; // true if this wallet is injected to the webpage
    embedded?: boolean; // true if the DAppis opened inside this wallet's browser
}
```

## 다양한 지갑 앱용 버튼 표시

버튼은 웹 애플리케이션 디자인에 따라 다를 수 있습니다.
현재 페이지는 다음과 같은 결과를 생성합니다:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <script src="https://unpkg.com/@tonconnect/sdk@latest/dist/tonconnect-sdk.min.js" defer></script>

    // highlight-start
    <style>
      body {
        width: 1000px;
        margin: 0 auto;
        font-family: Roboto, sans-serif;
      }
      .section {
        padding: 20px; margin: 20px;
        border: 2px #AEFF6A solid; border-radius: 8px;
      }
      #tonconnect-buttons>button {
        display: block;
        padding: 8px; margin-bottom: 8px;
        font-size: 18px; font-family: inherit;
      }
      .featured {
        font-weight: 800;
      }
    </style>
    // highlight-end
  </head>
  <body>
    // highlight-start
    <div class="section" id="tonconnect-buttons">
    </div>
    // highlight-end
    
    <script>
      const $ = document.querySelector.bind(document);
      
      window.onload = async () => {
        const connector = new TonConnectSDK.TonConnect();
        const walletsList = await connector.getWallets();

        // highlight-start
        let buttonsContainer = $('#tonconnect-buttons');
        
        for (let wallet of walletsList) {
          let connectButton = document.createElement('button');
          connectButton.innerText = 'Connect with ' + wallet.name;
          
          if (wallet.embedded) {
            // `embedded` means we are browsing the app from wallet application
            // we need to mark this sign-in option somehow
            connectButton.classList.add('featured');
          }
          
          if (!wallet.bridgeUrl && !wallet.injected && !wallet.embedded) {
            // no `bridgeUrl` means this wallet app is injecting JS code
            // no `injected` and no `embedded` -> app is inaccessible on this page
            connectButton.disabled = true;
          }
          
          buttonsContainer.appendChild(connectButton);
        }
	// highlight-end
      };
    </script>
  </body>
</html>
```

다음 사항에 유의하세요:

1. 지갑 애플리케이션을 통해 웹 페이지가 표시되는 경우, '임베디드' 속성을 'true'로 설정합니다. 즉, 이 로그인 옵션이 가장 일반적으로 사용되므로 강조 표시하는 것이 중요합니다.
2. 특정 지갑이 자바스크립트만 사용하여 빌드되었고(`bridgeUrl`이 없음) `injected`(또는 안전을 위해 `embedded`) 속성을 설정하지 않은 경우, 해당 지갑은 분명히 액세스할 수 없으며 버튼이 비활성화되어야 합니다.

## 앱 매니페스트 없이 연결

앱 매니페스트 없이 연결이 이루어지는 경우 스크립트를 다음과 같이 변경해야 합니다:

```js
      const $ = document.querySelector.bind(document);
      
      window.onload = async () => {
        const connector = new TonConnectSDK.TonConnect();
        const walletsList = await connector.getWallets();
        
        const unsubscribe = connector.onStatusChange(
          walletInfo => {
            console.log('Connection status:', walletInfo);
          }
        );
        
        let buttonsContainer = $('#tonconnect-buttons');

        for (let wallet of walletsList) {
          let connectButton = document.createElement('button');
          connectButton.innerText = 'Connect with ' + wallet.name;
          
          if (wallet.embedded) {
            // `embedded` means we are browsing the app from wallet application
            // we need to mark this sign-in option somehow
            connectButton.classList.add('featured');
          }
          
          // highlight-start
          if (wallet.embedded || wallet.injected) {
            connectButton.onclick = () => {
              connectButton.disabled = true;
              connector.connect({jsBridgeKey: wallet.jsBridgeKey});
            };
          } else if (wallet.bridgeUrl) {
            connectButton.onclick = () => {
              connectButton.disabled = true;
              console.log('Connection link:', connector.connect({
                universalLink: wallet.universalLink,
                bridgeUrl: wallet.bridgeUrl
              }));
            };
          } else {
            // wallet app does not provide any auth method
            connectButton.disabled = true;
          }
	  // highlight-end
          
          buttonsContainer.appendChild(connectButton);
        }
      };
```

이제 위의 프로세스가 수행되었으므로 상태 변경이 기록되고 있습니다(TON Connect의 작동 여부를 확인하기 위해). 연결용 QR 코드가 있는 모달을 표시하는 것은 이 매뉴얼의 범위를 벗어납니다. 테스트 목적으로 브라우저 확장 프로그램을 사용하거나 필요한 수단(예: 텔레그램 사용)을 통해 사용자의 휴대폰으로 연결 요청 링크를 보낼 수 있습니다.
참고: 아직 앱 매니페스트를 만들지 않았습니다. 현재로서는 이 요구사항이 충족되지 않는 경우 최종 결과를 분석하는 것이 가장 좋은 방법입니다.

### 톤키퍼로 로그인하기

Tonkeeper에 로그인하기 위해 인증을 위한 다음 링크가 생성됩니다(참고용으로 아래에 제공됨):

```
https://app.tonkeeper.com/ton-connect?v=2&id=3c12f5311be7e305094ffbf5c9b830e53a4579b40485137f29b0ca0c893c4f31&r=%7B%22manifestUrl%22%3A%22null%2Ftonconnect-manifest.json%22%2C%22items%22%3A%5B%7B%22name%22%3A%22ton_addr%22%7D%5D%7D
```

디코딩되면 `r` 매개변수는 다음과 같은 JSON 형식을 생성합니다:

```js
{"manifestUrl":"null/tonconnect-manifest.json","items":[{"name":"ton_addr"}]}
```

휴대폰 링크를 클릭하면 Tonkeeper가 자동으로 열렸다가 닫히면서 요청을 무시합니다. 또한 웹 앱 페이지 콘솔에 다음과 같은 오류가 나타납니다:
'오류: [TON_CONNECT_SDK_ERROR] null/tonconnect-manifest.json을 가져올 수 없습니다\`.

즉, 애플리케이션 매니페스트를 다운로드할 수 있어야 합니다.

## 앱 매니페스트 사용과의 연결

이 시점부터는 사용자 파일(주로 tonconnect-manifest.json)을 어딘가에 호스팅해야 합니다. 이 경우 다른 웹 애플리케이션의 매니페스트를 사용하겠습니다. 그러나 이는 프로덕션 환경에는 권장되지 않지만 테스트 목적으로는 허용됩니다.

다음 코드 스니펫입니다:

```js
      window.onload = async () => {
        const connector = new TonConnectSDK.TonConnect();
        
        const walletsList = await connector.getWallets();
        
        const unsubscribe = connector.onStatusChange(
          walletInfo => {
            console.log('Connection status:', walletInfo);
          }
        );
```

이 버전으로 교체해야 합니다:

```js
      window.onload = async () => {
        const connector = new TonConnectSDK.TonConnect({manifestUrl: 'https://ratingers.pythonanywhere.com/ratelance/tonconnect-manifest.json'});
        // highlight-next-line
        window.connector = connector;  // for experimenting in browser console
        
        const walletsList = await connector.getWallets();
        
        const unsubscribe = connector.onStatusChange(
          walletInfo => {
            console.log('Connection status:', walletInfo);
          }
        );
	// highlight-next-line
        connector.restoreConnection();
```

위의 최신 버전에서는 브라우저 콘솔에서 액세스할 수 있도록 `창`에 `connector` 변수를 저장하는 기능이 추가되었습니다. 또한 사용자가 각 웹 애플리케이션 페이지에서 로그인할 필요가 없도록 `restoreConnection`이 추가되었습니다.

### 톤키퍼로 로그인하기

지갑에서 요청을 거부하면 콘솔에 표시되는 결과는 '오류'입니다: [TON_CONNECT_SDK_ERROR] 지갑이 요청을 거부했습니다\`입니다.

따라서 링크가 저장된 경우 사용자는 동일한 로그인 요청을 수락할 수 있습니다. 즉, 웹 앱이 인증 거부를 최종 인증이 아닌 것으로 처리하여 올바르게 작동할 수 있어야 합니다.

그 후 로그인 요청이 수락되고 브라우저 콘솔에 다음과 같이 즉시 반영됩니다:

```bash
22:40:13.887 Connection status:
Object { device: {…}, provider: "http", account: {…} }
  account: Object { address: "0:b2a1ec...", chain: "-239", walletStateInit: "te6cckECFgEAAwQAAgE0ARUBFP8A9..." }
  device: Object {platform: "android", appName: "Tonkeeper", appVersion: "2.8.0.261", …}
  provider: "http"
```

위의 결과는 다음 사항을 고려한 것입니다:

1. **계정**: 정보: 주소(워크체인+해시), 네트워크(메인넷/테스트넷), 공개키 추출에 사용되는 지갑 상태 초기화(stateInit)가 포함되어 있습니다.
2. **장치**: 정보: 이름과 지갑 애플리케이션 버전(처음에 요청한 이름과 동일해야 하지만 진위 여부를 확인하기 위해 확인할 수 있음), 플랫폼 이름과 지원되는 기능 목록이 포함되어 있습니다.
3. **공급자**: 지갑과 웹 애플리케이션 간의 모든 요청과 응답이 브리지를 통해 제공될 수 있도록 하는 http가 포함되어 있습니다.

## 로그아웃하고 톤프루프 요청하기

이제 미니 앱에 로그인했지만... 백엔드에서 올바른 당사자인지 어떻게 알 수 있을까요? 이를 확인하려면 지갑 소유권 증명을 요청해야 합니다.

이 작업은 인증을 통해서만 완료할 수 있으므로 로그아웃해야 합니다. 따라서 콘솔에서 다음 코드를 실행합니다:

```js
connector.disconnect();
```

연결 해제 프로세스가 완료되면 '연결 상태: null'이 표시됩니다.

톤프루프가 추가되기 전에 현재 구현이 안전하지 않다는 것을 보여주기 위해 코드를 변경해 보겠습니다:

```js
let connHandler = connector.statusChangeSubscriptions[0];
connHandler({
  device: {
    appName: "Uber Singlesig Cold Wallet App",
    appVersion: "4.0.1",
    features: [],
    maxProtocolVersion: 3,
    platform: "ios"
  },
  account: {
    /* TON Foundation address */
    address: '0:83dfd552e63729b472fcbcc8c45ebcc6691702558b68ec7527e1ba403a0f31a8',
    chain: '-239',
    walletStateInit: 'te6ccsEBAwEAoAAFcSoCATQBAgDe/wAg3SCCAUyXuiGCATOcurGfcbDtRNDTH9MfMdcL/+ME4KTyYIMI1xgg0x/TH9Mf+CMTu/Jj7UTQ0x/TH9P/0VEyuvKhUUS68qIE+QFUEFX5EPKj+ACTINdKltMH1AL7AOjRAaTIyx/LH8v/ye1UAFAAAAAAKamjF3LJ7WtipuLroUqTuQRi56Nnd3vrijj7FbnzOETSLOL/HqR30Q=='
  },
  provider: 'http'
});
```

콘솔의 결과 코드 줄은 처음 연결을 시작할 때 표시되는 코드 줄과 거의 동일합니다. 따라서 백엔드가 예상대로 사용자 인증을 올바르게 수행하지 않는다면 제대로 작동하는지 테스트할 수 있는 방법이 필요합니다. 이를 위해 콘솔 내에서 TON 재단 역할을 수행하여 토큰 잔액과 토큰 소유권 매개변수의 적법성을 테스트할 수 있습니다. 물론 제공된 코드는 커넥터의 변수를 변경하지 않지만, 사용자는 해당 커넥터가 폐쇄로 보호되지 않는 한 원하는 대로 앱을 사용할 수 있습니다. 이 경우에도 디버거와 코딩 중단점을 사용하여 이를 추출하는 것은 어렵지 않습니다.

이제 사용자 인증이 확인되었으므로 코드 작성을 진행해 보겠습니다.

## 톤프루프를 사용한 연결

톤 커넥트의 SDK 문서에 따르면, 두 번째 인수는 지갑이 래핑하고 서명할 페이로드를 포함하는 `connect()` 메서드를 참조합니다. 따라서 결과는 새로운 연결 코드입니다:

```js
          if (wallet.embedded || wallet.injected) {
            connectButton.onclick = () => {
              connectButton.disabled = true;
              connector.connect({jsBridgeKey: wallet.jsBridgeKey},
                                {tonProof: 'doc-example-<BACKEND_AUTH_ID>'});
            };
          } else if (wallet.bridgeUrl) {
            connectButton.onclick = () => {
              connectButton.disabled = true;
              console.log('Connection link:', connector.connect({
                universalLink: wallet.universalLink,
                bridgeUrl: wallet.bridgeUrl
              }, {tonProof: 'doc-example-<BACKEND_AUTH_ID>'}));
            };
```

연결 링크:

```
https://app.tonkeeper.com/ton-connect?v=2&id=4b0a7e2af3b455e0f0bafe14dcdc93f1e9e73196ae2afaca4d9ba77e94484a44&r=%7B%22manifestUrl%22%3A%22https%3A%2F%2Fratingers.pythonanywhere.com%2Fratelance%2Ftonconnect-manifest.json%22%2C%22items%22%3A%5B%7B%22name%22%3A%22ton_addr%22%7D%2C%7B%22name%22%3A%22ton_proof%22%2C%22payload%22%3A%22doc-example-%3CBACKEND_AUTH_ID%3E%22%7D%5D%7D
```

확장되고 간소화된 `r` 매개변수:

```js
{
  "manifestUrl":
    "https://ratingers.pythonanywhere.com/ratelance/tonconnect-manifest.json",
  "items": [
    {"name": "ton_addr"},
    {"name": "ton_proof", "payload": "doc-example-<BACKEND_AUTH_ID>"}
  ]
}
```

그런 다음 URL 주소 링크가 모바일 장치로 전송되고 Tonkeeper를 사용하여 열립니다.

이 과정이 완료되면 다음과 같은 지갑 관련 정보가 수신됩니다:

```js
{
  "device": {
    "platform": "android",
    "appName": "Tonkeeper",
    "appVersion": "2.8.0.261",
    "maxProtocolVersion": 2,
    "features": [
      "SendTransaction"
    ]
  },
  "provider": "http",
  "account": {
    "address": "0:b2a1ecf5545e076cd36ae516ea7ebdf32aea008caa2b84af9866becb208895ad",
    "chain": "-239",
    "walletStateInit": "te6cckECFgEAAwQAAgE0ARUBFP8A9KQT9LzyyAsCAgEgAxACAUgEBwLm0AHQ0wMhcbCSXwTgItdJwSCSXwTgAtMfIYIQcGx1Z70ighBkc3RyvbCSXwXgA/pAMCD6RAHIygfL/8nQ7UTQgQFA1yH0BDBcgQEI9ApvoTGzkl8H4AXTP8glghBwbHVnupI4MOMNA4IQZHN0crqSXwbjDQUGAHgB+gD0BDD4J28iMFAKoSG+8uBQghBwbHVngx6xcIAYUATLBSbPFlj6Ahn0AMtpF8sfUmDLPyDJgED7AAYAilAEgQEI9Fkw7UTQgQFA1yDIAc8W9ADJ7VQBcrCOI4IQZHN0coMesXCAGFAFywVQA88WI/oCE8tqyx/LP8mAQPsAkl8D4gIBIAgPAgEgCQ4CAVgKCwA9sp37UTQgQFA1yH0BDACyMoHy//J0AGBAQj0Cm+hMYAIBIAwNABmtznaiaEAga5Drhf/AABmvHfaiaEAQa5DrhY/AABG4yX7UTQ1wsfgAWb0kK29qJoQICga5D6AhhHDUCAhHpJN9KZEM5pA+n/mDeBKAG3gQFImHFZ8xhAT48oMI1xgg0x/TH9MfAvgju/Jk7UTQ0x/TH9P/9ATRUUO68qFRUbryogX5AVQQZPkQ8qP4ACSkyMsfUkDLH1Iwy/9SEPQAye1U+A8B0wchwACfbFGTINdKltMH1AL7AOgw4CHAAeMAIcAC4wABwAORMOMNA6TIyx8Syx/L/xESExQAbtIH+gDU1CL5AAXIygcVy//J0Hd0gBjIywXLAiLPFlAF+gIUy2sSzMzJc/sAyEAUgQEI9FHypwIAcIEBCNcY+gDTP8hUIEeBAQj0UfKnghBub3RlcHSAGMjLBcsCUAbPFlAE+gIUy2oSyx/LP8lz+wACAGyBAQjXGPoA0z8wUiSBAQj0WfKnghBkc3RycHSAGMjLBcsCUAXPFlAD+gITy2rLHxLLP8lz+wAACvQAye1UAFEAAAAAKamjFyM60x2mt5eboNyOTE+5RGOe9Ee2rK1Qcb+0ZuiP9vb7QJRlz/c="
  },
  "connectItems": {
    "tonProof": {
      "name": "ton_proof",
      "proof": {
        "timestamp": 1674392728,
        "domain": {
          "lengthBytes": 28,
          "value": "ratingers.pythonanywhere.com"
        },
        "signature": "trCkHit07NZUayjGLxJa6FoPnaGHkqPy2JyNjlUbxzcc3aGvsExCmHXi6XJGuoCu6M2RMXiLzIftEm6PAoy1BQ==",
        "payload": "doc-example-<BACKEND_AUTH_ID>"
      }
    }
  }
}
```

수신된 서명을 확인해 보겠습니다. 이를 위해 서명 검증은 백엔드와 쉽게 상호작용할 수 있는 파이썬을 사용합니다. 이 프로세스를 수행하는 데 필요한 라이브러리는 `tonsdk`와 `pynacl`입니다.

다음으로 지갑의 공개키를 검색해야 합니다. 이를 위해 최종 결과를 안정적으로 신뢰할 수 없기 때문에 `tonapi.io` 또는 이와 유사한 서비스를 사용하지 않습니다. 대신 `walletStateInit`을 파싱하여 이 작업을 수행합니다.

또한 '주소'와 '지갑StateInit'이 일치하는지 확인해야 하며, 페이로드에 자신의 지갑을 'stateInit' 필드에 입력하고 다른 지갑을 '주소' 필드에 입력해 지갑 키로 서명할 수도 있습니다.

StateInit`은 코드용과 데이터용의 두 가지 참조 유형으로 구성됩니다. 여기서는 공개 키를 검색하여 두 번째 참조(데이터 참조)를 로드하는 것이 목적입니다. 그런 다음 8바이트가 건너뛰고(모든 최신 지갑 컨트랙트에서 4바이트는 `seqno`필드에, 4바이트는`subwallet_id\`에 사용됨) 다음 32바이트, 즉 공개 키가 로드됩니다(256비트).

```python
import nacl.signing
import tonsdk

import hashlib
import base64

received_state_init = 'te6cckECFgEAAwQAAgE0ARUBFP8A9KQT9LzyyAsCAgEgAxACAUgEBwLm0AHQ0wMhcbCSXwTgItdJwSCSXwTgAtMfIYIQcGx1Z70ighBkc3RyvbCSXwXgA/pAMCD6RAHIygfL/8nQ7UTQgQFA1yH0BDBcgQEI9ApvoTGzkl8H4AXTP8glghBwbHVnupI4MOMNA4IQZHN0crqSXwbjDQUGAHgB+gD0BDD4J28iMFAKoSG+8uBQghBwbHVngx6xcIAYUATLBSbPFlj6Ahn0AMtpF8sfUmDLPyDJgED7AAYAilAEgQEI9Fkw7UTQgQFA1yDIAc8W9ADJ7VQBcrCOI4IQZHN0coMesXCAGFAFywVQA88WI/oCE8tqyx/LP8mAQPsAkl8D4gIBIAgPAgEgCQ4CAVgKCwA9sp37UTQgQFA1yH0BDACyMoHy//J0AGBAQj0Cm+hMYAIBIAwNABmtznaiaEAga5Drhf/AABmvHfaiaEAQa5DrhY/AABG4yX7UTQ1wsfgAWb0kK29qJoQICga5D6AhhHDUCAhHpJN9KZEM5pA+n/mDeBKAG3gQFImHFZ8xhAT48oMI1xgg0x/TH9MfAvgju/Jk7UTQ0x/TH9P/9ATRUUO68qFRUbryogX5AVQQZPkQ8qP4ACSkyMsfUkDLH1Iwy/9SEPQAye1U+A8B0wchwACfbFGTINdKltMH1AL7AOgw4CHAAeMAIcAC4wABwAORMOMNA6TIyx8Syx/L/xESExQAbtIH+gDU1CL5AAXIygcVy//J0Hd0gBjIywXLAiLPFlAF+gIUy2sSzMzJc/sAyEAUgQEI9FHypwIAcIEBCNcY+gDTP8hUIEeBAQj0UfKnghBub3RlcHSAGMjLBcsCUAbPFlAE+gIUy2oSyx/LP8lz+wACAGyBAQjXGPoA0z8wUiSBAQj0WfKnghBkc3RycHSAGMjLBcsCUAXPFlAD+gITy2rLHxLLP8lz+wAACvQAye1UAFEAAAAAKamjFyM60x2mt5eboNyOTE+5RGOe9Ee2rK1Qcb+0ZuiP9vb7QJRlz/c='
received_address = '0:b2a1ecf5545e076cd36ae516ea7ebdf32aea008caa2b84af9866becb208895ad'

state_init = tonsdk.boc.Cell.one_from_boc(base64.b64decode(received_state_init))

address_hash_part = base64.b16encode(state_init.bytes_hash()).decode('ascii').lower()
assert received_address.endswith(address_hash_part)

public_key = state_init.refs[1].bits.array[8:][:32]

print(public_key)
# bytearray(b'#:\xd3\x1d\xa6\xb7\x97\x9b\xa0\xdc\x8eLO\xb9Dc\x9e\xf4G\xb6\xac\xadPq\xbf\xb4f\xe8\x8f\xf6\xf6\xfb')

verify_key = nacl.signing.VerifyKey(bytes(public_key))
```

위의 시퀀싱 코드가 구현된 후, 올바른 문서를 참조하여 지갑 키를 사용하여 어떤 매개변수가 확인되고 서명되었는지 확인합니다:

> ```
> message = utf8_encode("ton-proof-item-v2/") ++  
>           Address ++  
>           AppDomain ++  
>           Timestamp ++  
>           Payload
>
> signature = Ed25519Sign(
>   privkey,
>   sha256(0xffff ++ utf8_encode("ton-connect") ++ sha256(message))
> )
> ```

> 여기서
>
> - '주소'는 시퀀스로 인코딩된 지갑 주소를 나타냅니다:
>   - 워크체인\`: 32비트 부호 있는 정수 빅 엔디안;
>   - 해시\`: 256비트 부호 없는 정수 빅 엔디안;
> - '앱도메인'은 길이 ++ 인코딩된 도메인 이름입니다.
>   - 길이\`는 utf-8로 인코딩된 앱 도메인 이름 길이(바이트)의 32비트 값을 사용합니다.
>   - 인코딩된 도메인 이름`아이디`길이\`-바이트 utf-8로 인코딩된 앱 도메인 이름
> - '타임스탬프'는 서명 작업의 64비트 유닉스 에포크 시간을 나타냅니다.
> - 페이로드\`는 가변 길이 바이너리 문자열을 나타냅니다.
> - utf8_encode\`는 길이 접두사가 없는 일반 바이트 문자열을 생성합니다.

이를 파이썬으로 다시 구현해 보겠습니다.  위의 정수 중 일부는 엔디안이 지정되어 있지 않으므로 몇 가지 예를 고려해야 합니다. 몇 가지 관련 예제가 자세히 설명된 다음 Tonkeeper 구현을 참조하세요: [ConnectReplyBuilder.ts](https://github.com/tonkeeper/wallet/blob/77992c08c663dceb63ca6a8e918a2150c75cca3a/src/tonconnect/ConnectReplyBuilder.ts#L42).

```python
received_timestamp = 1674392728
signature = 'trCkHit07NZUayjGLxJa6FoPnaGHkqPy2JyNjlUbxzcc3aGvsExCmHXi6XJGuoCu6M2RMXiLzIftEm6PAoy1BQ=='

message = (b'ton-proof-item-v2/'
         + 0 .to_bytes(4, 'big') + si.bytes_hash()
         + 28 .to_bytes(4, 'little') + b'ratingers.pythonanywhere.com'
         + received_timestamp.to_bytes(8, 'little')
         + b'doc-example-<BACKEND_AUTH_ID>')
# b'ton-proof-item-v2/\x00\x00\x00\x00\xb2\xa1\xec\xf5T^\x07l\xd3j\xe5\x16\xea~\xbd\xf3*\xea\x00\x8c\xaa+\x84\xaf\x98f\xbe\xcb \x88\x95\xad\x1c\x00\x00\x00ratingers.pythonanywhere.com\x984\xcdc\x00\x00\x00\x00doc-example-<BACKEND_AUTH_ID>'

signed = b'\xFF\xFF' + b'ton-connect' + hashlib.sha256(message).digest()
# b'\xff\xffton-connectK\x90\r\xae\xf6\xb0 \xaa\xa9\xbd\xd1\xaa\x96\x8b\x1fp\xa9e\xff\xdf\x81\x02\x98\xb0)E\t\xf6\xc0\xdc\xfdx'

verify_key.verify(hashlib.sha256(signed).digest(), base64.b64decode(signature))
# b'\x0eT\xd6\xb5\xd5\xe8HvH\x0b\x10\xdc\x8d\xfc\xd3#n\x93\xa8\xe9\xb9\x00\xaaH%\xb5O\xac:\xbd\xcaM'
```

위의 매개 변수를 구현한 후 공격자가 사용자를 가장하려고 시도하고 유효한 서명을 제공하지 않으면 다음 오류가 표시됩니다: `nacl.exceptions.BadSignatureError: 서명이 위조되었거나 손상되었습니다`라는 오류가 표시됩니다.

## 다음 단계

디앱을 작성할 때는 다음 사항도 고려해야 합니다:

- 연결이 성공적으로 완료된 후(복원된 연결 또는 새 연결), 여러 개의 '연결' 버튼 대신 '연결 해제' 버튼이 표시되어야 합니다.
- 사용자가 연결을 끊은 후 '연결 끊기' 버튼을 다시 만들어야 합니다.
- 지갑 코드를 확인해야 합니다.
  - 최신 지갑 버전은 공개 키를 다른 위치에 배치하여 문제를 일으킬 수 있습니다.
  - 현재 사용자는 지갑 대신 다른 유형의 컨트랙트를 사용하여 로그인할 수 있습니다. 다행히도 여기에는 예상 위치에 공개 키가 포함되어 있습니다.

행운을 빌며 즐겁게 디앱을 제작하세요!
