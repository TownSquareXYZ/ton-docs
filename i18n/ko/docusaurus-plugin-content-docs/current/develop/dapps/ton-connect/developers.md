# TON Connect SDK

## SDK 목록

:::info
가능하면 dApp에 [@tonconnect/ui-react](/develop/dapps/ton-connect/developers#ton-connect-ui-react) 키트를 사용하는 것이 좋습니다. 제품에 꼭 필요한 경우에만 낮은 수준의 SDK로 전환하거나 프로토콜 버전을 다시 구현하세요.
:::

이 페이지에는 TON Connect에 유용한 라이브러리 목록이 나와 있습니다.

- [톤 커넥트 리액트](/개발/앱/톤-커넥트/개발자#톤-커넥트-리액트)
- [톤 커넥트 JS SDK](/개발/앱/톤-커넥트/개발자#톤-커넥트-js-sdk)
- [톤 커넥트 파이썬 SDK](/개발/앱/톤 커넥트/개발자#톤 커넥트 파이썬)
- [톤 커넥트 다트](/개발/앱/톤-커넥트/개발자#톤-커넥트-다트)
- [톤 커넥트 C#](/개발/앱/톤-커넥트/개발자#톤-커넥트-c)
- [톤 커넥트 유니티](/개발/앱/톤-커넥트/개발자#톤-커넥트-유니티)
- [톤 커넥트 고](/개발/앱/톤-커넥트/개발자#톤-커넥트-고)

## 톤 커넥트 리액트

- [톤커넥트/유아이-리액트](/개발/앱/톤커넥트/개발자#톤커넥트-유아이-리액트) - React 애플리케이션을 위한 TON Connect 사용자 인터페이스(UI)

톤커넥트 UI 리액트는 톤커넥트 SDK를 위한 리액트 UI 키트입니다. 이를 사용하여 React 앱에서 TonConnect 프로토콜을 통해 앱을 TON 지갑에 연결할 수 있습니다.

- 톤커넥트/ui-react\`를 사용한 DApp의 예시: [깃허브](https://github.com/ton-connect/demo-dapp-with-react-ui)
- 배포된 `demo-dapp-with-react-ui`의 예시: [GitHub](https://ton-connect.github.io/demo-dapp-with-react-ui/)

```bash
npm i @tonconnect/ui-react
```

- [깃허브](https://github.com/ton-connect/sdk/tree/main/packages/ui-react)
- [NPM](https://www.npmjs.com/package/@tonconnect/ui-react)
- [API 문서](https://ton-connect.github.io/sdk/modules/_tonconnect_ui_react.html)

## TON Connect JS SDK

TON Connect 리포지토리에는 다음과 같은 주요 패키지가 포함되어 있습니다:

- [톤커넥트/ui](/개발/앱/톤커넥트/개발자#톤커넥트-ui) - 톤 커넥트 사용자 인터페이스(UI)
- [톤커넥트/개발자](/개발/앱/톤커넥트/개발자#톤커넥트-sdk) - TON 커넥트 SDK
- [톤커넥트/프로토콜](/개발/앱/톤커넥트/개발자#톤커넥트-프로토콜-모델) - TON 커넥트 프로토콜 사양

### TON Connect UI

톤커넥트 UI는 톤커넥트 SDK를 위한 UI 키트입니다. 톤커넥트 프로토콜을 통해 앱을 톤 지갑에 연결할 때 사용합니다. "지갑 연결 버튼", "지갑 선택 대화 상자", 확인 모달과 같은 UI 요소를 사용하여 앱에 TonConnect를 쉽게 통합할 수 있습니다.

```bash
npm i @tonconnect/ui
```

- [깃허브](https://github.com/ton-connect/sdk/tree/main/packages/ui)
- [NPM](https://www.npmjs.com/package/@tonconnect/ui)
- [API 문서](https://ton-connect.github.io/sdk/modules/_tonconnect_ui.html)

TON Connect 사용자 인터페이스(UI)는 개발자가 애플리케이션 사용자의 사용자 경험(UX)을 개선할 수 있는 프레임워크입니다.

'지갑 연결 버튼', '지갑 선택 대화상자', 확인 모달과 같은 간단한 UI 요소를 사용해 앱과 TON 커넥트를 쉽게 통합할 수 있습니다. 다음은 TON Connect가 앱의 UX를 개선하는 세 가지 주요 예시입니다:

- 디앱브라우저의 앱 기능 예시: [깃허브](https://ton-connect.github.io/demo-dapp/)
- 위 디앱의 백엔드 파티션 예시: [깃허브](https://github.com/ton-connect/demo-dapp-backend)
- Go를 사용하는 브릿지 서버: [GitHub](https://github.com/ton-connect/bridge)

이 키트는 톤 블록체인용으로 제작된 앱에서 톤 커넥트 구현을 간소화합니다. 표준 프론트엔드 프레임워크는 물론, 미리 정해진 프레임워크를 사용하지 않는 애플리케이션도 지원됩니다.

### TON Connect SDK

개발자가 TON 커넥트를 애플리케이션에 통합하는 데 도움이 되는 세 가지 프레임워크 중 가장 낮은 수준의 프레임워크는 TON 커넥트 SDK입니다. 주로 TON 커넥트 프로토콜을 통해 앱을 TON 월렛에 연결하는 데 사용됩니다.

- [깃허브](https://github.com/ton-connect/sdk/tree/main/packages/sdk)
- [NPM](https://www.npmjs.com/package/@tonconnect/sdk)

### TON Connect 프로토콜 모델

이 패키지에는 프로토콜 요청, 프로토콜 응답, 이벤트 모델, 인코딩 및 디코딩 함수가 포함되어 있습니다. 이 패키지는 타입스크립트로 작성된 지갑 앱에 TON 커넥트를 통합하는 데 사용할 수 있습니다. TON 커넥트를 디앱에 통합하려면 [@tonconnect/sdk](https://www.npmjs.com/package/@tonconnect/sdk)를 사용해야 합니다.

- [깃허브](https://github.com/ton-connect/sdk/tree/main/packages/protocol)
- [NPM](https://www.npmjs.com/package/@tonconnect/protocol)

## TON 연결 파이썬

### 파이톤커넥트

톤 커넥트 2.0용 파이썬 SDK. 톤 커넥트 2.0의 `@tonconnect/sdk` 라이브러리와 유사합니다.

톤커넥트 프로토콜을 통해 앱을 톤 지갑에 연결할 때 사용합니다.

```bash
pip3 install pytonconnect
```

- [깃허브](https://github.com/XaBbl4/pytonconnect)

### ClickoTON-파운데이션 톤커넥트

TON Connect를 Python 앱에 연결하기 위한 라이브러리

```bash
git clone https://github.com/ClickoTON-Foundation/tonconnect.git
pip install -e tonconnect
```

[깃허브](https://github.com/ClickoTON-Foundation/tonconnect)

## 톤 커넥트 다트

톤 커넥트 2.0용 다트 SDK. 톤 커넥트 라이브러리의 아날로그 버전입니다.

톤커넥트 프로토콜을 통해 앱을 톤 지갑에 연결할 때 사용합니다.

```bash
 $ dart pub add darttonconnect
```

- [깃허브](https://github.com/romanovichim/dartTonconnect)

## TON Connect C\#

톤 커넥트 2.0용 C# SDK. 톤 커넥트 2.0의 `@tonconnect/sdk` 라이브러리와 유사합니다.

톤커넥트 프로토콜을 통해 앱을 톤 지갑에 연결할 때 사용합니다.

```bash
 $ dotnet add package TonSdk.Connect
```

- [깃허브](https://github.com/continuation-team/TonSdk.NET/tree/main/TonSDK.Connect)

## TON Connect Go

TON Connect 2.0용 Go SDK.

톤커넥트 프로토콜을 통해 앱을 톤 지갑에 연결할 때 사용합니다.

```bash
 go get github.com/cameo-engineering/tonconnect
```

- [깃허브](https://github.com/cameo-engineering/tonconnect)

## 일반적인 질문 및 우려 사항

톤 커넥트 2.0을 구현하는 동안 개발자나 커뮤니티 회원 중 추가적인 문제가 발생하면 [톤키퍼 개발자](https://t.me/tonkeeperdev) 채널로 문의해 주세요.

추가적인 문제가 발생하거나 TON Connect 2.0 개선에 대한 제안을 하고 싶으신 경우 해당 [GitHub 디렉토리](https://github.com/ton-connect/)를 통해 직접 문의해 주세요.

## 톤 커넥트 유니티

TON Connect 2.0용 Unity 에셋입니다. 계속팀/TonSdk.NET/tree/main/TonSDK.Connect\`를 사용합니다.

톤커넥트 프로토콜을 게임에 통합하는 데 사용하세요.

- [깃허브](https://github.com/continuation-team/unity-ton-connect)
- [문서](https://docs.tonsdk.net/user-manual/unity-tonconnect-2.0/getting-started)

## 참고 항목

- [첫 웹 클라이언트 구축을 위한 단계별 가이드](https://ton-community.github.io/tutorials/03-client/)
- [[유튜브] TON 스마트 컨트랙트 | 10 | 텔레그램 디앱[EN]](https://www.youtube.com/watch?v=D6t3eZPdgAU\&t=254s\&ab_channel=AlefmanVladimir%5BEN%5D)
- [톤 커넥트 시작하기](https://github.com/ton-connect/sdk/tree/main/packages/sdk)
- [연동 매뉴얼](/개발/앱/톤-연결/연동)
- [유튜브] TON 개발자 스터디 TON 커넥트 프로토콜 [RU]](https://www.youtube.com/playlist?list=PLyDBPwv9EPsCJ226xS5_dKmXXxWx1CKz_)
