# TON Connect SDK들

## SDK 목록

:::info
가능하다면 dApp 개발 시 [@tonconnect/ui-react](https://github.com/ton-connect/sdk/tree/main/packages/ui-react) 키트 사용을 권장합니다. 제품에 정말 필요한 경우에만 하위 레벨 SDK를 사용하거나 프로토콜 구현을 직접 하시기 바랍니다.
:::

TON Connect를 위한 유용한 라이브러리 목록입니다.

- [TON Connect React](/v3/guidelines/ton-connect/guidelines/developers#ton-connect-react)
- [TON Connect JS SDK](/v3/guidelines/ton-connect/guidelines/developers#ton-connect-js-sdk)
- [TON Connect Vue](/v3/guidelines/ton-connect/guidelines/developers#ton-connect-vue)
- [TON Connect Python SDK](/v3/guidelines/ton-connect/guidelines/developers#ton-connect-python)
- [TON Connect Dart](/v3/guidelines/ton-connect/guidelines/developers#ton-connect-dart)
- [TON Connect C#](/v3/guidelines/ton-connect/guidelines/developers#ton-connect-c)
- [TON Connect Unity](/v3/guidelines/ton-connect/guidelines/developers#ton-connect-unity)
- [TON Connect Go](/v3/guidelines/ton-connect/guidelines/developers#ton-connect-go)

## TON Connect React

- [@tonconnect/ui-react](https://github.com/ton-connect/sdk/tree/main/packages/ui-react) - React 애플리케이션을 위한 TON Connect 사용자 인터페이스(UI)

TonConnect UI React는 TonConnect SDK를 위한 React UI 키트입니다. React 앱에서 TonConnect 프로토콜을 통해 TON 지갑에 연결할 때 사용합니다.

- `@tonconnect/ui-react` DApp 예시: [GitHub](https://github.com/ton-connect/demo-dapp-with-react-ui)
- `demo-dapp-with-react-ui` 배포 예시: [GitHub](https://ton-connect.github.io/demo-dapp-with-react-ui/)

```bash
npm i @tonconnect/ui-react
```

- [GitHub](https://github.com/ton-connect/sdk/tree/main/packages/ui-react)
- [NPM](https://www.npmjs.com/package/@tonconnect/ui-react)
- [API 문서](https://ton-connect.github.io/sdk/modules/_tonconnect_ui_react.html)

## TON Connect JS SDK

TON Connect 저장소에는 다음과 같은 주요 패키지들이 포함되어 있습니다:

- [@tonconnect/ui](/v3/guidelines/ton-connect/guidelines/developers#ton-connect-ui) - TON Connect 사용자 인터페이스(UI)
- [@tonconnect/sdk](/v3/guidelines/ton-connect/guidelines/developers#ton-connect-sdk) - TON Connect SDK
- [@tonconnect/protocol](/v3/guidelines/ton-connect/guidelines/developers#ton-connect-protocol-models) - TON Connect 프로토콜 사양

### TON Connect UI

TonConnect UI는 TonConnect SDK를 위한 UI 키트입니다. "지갑 연결 버튼", "지갑 선택 대화상자", 확인 모달과 같은 UI 요소들을 사용하여 TonConnect를 앱에 더 쉽게 통합할 수 있습니다.

```bash
npm i @tonconnect/ui
```

- [GitHub](https://github.com/ton-connect/sdk/tree/main/packages/ui)
- [NPM](https://www.npmjs.com/package/@tonconnect/ui)
- [API 문서](https://ton-connect.github.io/sdk/modules/_tonconnect_ui.html)

TON Connect 사용자 인터페이스(UI)는 개발자가 애플리케이션 사용자의 경험(UX)을 개선할 수 있게 해주는 프레임워크입니다.

TON Connect는 "지갑 연결 버튼", "지갑 선택 대화상자", 확인 모달과 같은 간단한 UI 요소를 사용하여 앱과 쉽게 통합할 수 있습니다. 다음은 TON Connect가 앱의 UX를 개선하는 세 가지 주요 예시입니다:

- DApp 브라우저에서의 앱 기능 예시: [GitHub](https://ton-connect.github.io/demo-dapp/)
- 위 DApp의 백엔드 부분 예시: [GitHub](https://github.com/ton-connect/demo-dapp-backend)
- Go를 사용한 브릿지 서버: [GitHub](https://github.com/ton-connect/bridge)

이 키트는 TON 블록체인용으로 구축된 앱에서 TON Connect 구현을 단순화합니다. 표준 프론트엔드 프레임워크뿐만 아니라 미리 정의된 프레임워크를 사용하지 않는 애플리케이션도 지원됩니다.

### TON Connect SDK

TON Connect SDK는 개발자가 TON Connect를 애플리케이션에 통합하는 데 도움을 주는 세 가지 프레임워크 중 가장 로우레벨입니다. 주로 TON Connect 프로토콜을 통해 앱을 TON 지갑에 연결하는 데 사용됩니다.

- [GitHub](https://github.com/ton-connect/sdk/tree/main/packages/sdk)
- [NPM](https://www.npmjs.com/package/@tonconnect/sdk)

### TON Connect 프로토콜 모델

이 패키지는 프로토콜 요청, 프로토콜 응답, 이벤트 모델, 인코딩 및 디코딩 함수를 포함합니다. TypeScript로 작성된 지갑 앱에 TON Connect를 통합하는 데 사용할 수 있습니다. DApp에 TON Connect를 통합하려면 [@tonconnect/sdk](https://www.npmjs.com/package/@tonconnect/sdk)를 사용해야 합니다.

- [GitHub](https://github.com/ton-connect/sdk/tree/main/packages/protocol)
- [NPM](https://www.npmjs.com/package/@tonconnect/protocol)

## TON Connect Vue

TonConnect UI Vue는 TonConnect SDK를 위한 Vue UI 키트입니다. Vue 앱에서 TonConnect 프로토콜을 통해 TON 지갑에 연결할 때 사용합니다.

- `@townsquarelabs/ui-vue` DApp 예시: [GitHub](https://github.com/TownSquareXYZ/demo-dapp-with-vue-ui)
- `demo-dapp-with-vue-ui` 배포 예시: [GitHub](https://townsquarexyz.github.io/demo-dapp-with-vue-ui/)

```bash
npm i @townsquarelabs/ui-vue
```

- [GitHub](https://github.com/TownSquareXYZ/tonconnect-ui-vue)
- [NPM](https://www.npmjs.com/package/@townsquarelabs/ui-vue)

## TON Connect Python

### pytonconnect

TON Connect 2.0을 위한 Python SDK입니다. `@tonconnect/sdk` 라이브러리의 유사품입니다.

TonConnect 프로토콜을 통해 앱을 TON 지갑에 연결할 때 사용합니다.

```bash
pip3 install pytonconnect
```

- [GitHub](https://github.com/XaBbl4/pytonconnect)

### ClickoTON-Foundation tonconnect

Python 앱에 TON Connect를 연결하기 위한 라이브러리입니다.

```bash
git clone https://github.com/ClickoTON-Foundation/tonconnect.git
pip install -e tonconnect
```

[GitHub](https://github.com/ClickoTON-Foundation/tonconnect)

## TON Connect Dart

TON Connect 2.0을 위한 Dart SDK입니다. `@tonconnect/sdk` 라이브러리의 유사품입니다.

TonConnect 프로토콜을 통해 앱을 TON 지갑에 연결할 때 사용합니다.

```bash
 $ dart pub add darttonconnect
```

- [GitHub](https://github.com/romanovichim/dartTonconnect)

## TON Connect C\#

TON Connect 2.0을 위한 C# SDK입니다. `@tonconnect/sdk` 라이브러리의 유사품입니다.

TonConnect 프로토콜을 통해 앱을 TON 지갑에 연결할 때 사용합니다.

```bash
 $ dotnet add package TonSdk.Connect
```

- [GitHub](https://github.com/continuation-team/TonSdk.NET/tree/main/TonSDK.Connect)

## TON Connect Go

TON Connect 2.0을 위한 Go SDK입니다.

TonConnect 프로토콜을 통해 앱을 TON 지갑에 연결할 때 사용합니다.

```bash
 go get github.com/cameo-engineering/tonconnect
```

- [GitHub](https://github.com/cameo-engineering/tonconnect)

## 일반적인 질문과 우려사항

개발자나 커뮤니티 구성원이 TON Connect 2.0 구현 중 추가 문제가 발생하면 [Tonkeeper 개발자](https://t.me/tonkeeperdev) 채널에 문의하시기 바랍니다.

추가 문제가 발생하거나 TON Connect 2.0을 개선하는 방안을 제시하고 싶다면 [GitHub 디렉토리](https://github.com/ton-connect/)를 통해 직접 문의해 주시기 바랍니다.

## TON Connect Unity

TON Connect 2.0을 위한 Unity 애셋입니다. `continuation-team/TonSdk.NET/tree/main/TonSDK.Connect`를 사용합니다.

TonConnect 프로토콜을 게임에 통합할 때 사용합니다.

- [GitHub](https://github.com/continuation-team/unity-ton-connect)
- [문서](https://docs.tonsdk.net/user-manual/unity-tonconnect-2.0/getting-started)

## 참고 자료

- [첫 웹 클라이언트 구축을 위한 단계별 가이드](https://ton-community.github.io/tutorials/03-client/)
- [[YouTube] TON 스마트 컨트랙트 | 10 | 텔레그램 DApp[EN]](https://www.youtube.com/watch?v=D6t3eZPdgAU\&t=254s\&ab_channel=AlefmanVladimir%5BEN%5D)
- [Ton Connect 시작하기](https://github.com/ton-connect/sdk/tree/main/packages/sdk)
- [통합 매뉴얼](/v3/guidelines/ton-connect/guidelines/integration-with-javascript-sdk)
- [[YouTube] TON Dev Study TON Connect 프로토콜 [RU]](https://www.youtube.com/playlist?list=PLyDBPwv9EPsCJ226xS5_dKmXXxWx1CKz_)
