# TON Connect SDKs

## SDK 列表

:::info
如果可能，建议使用 [@tonconnect/ui-react] (/develop/dapps/ton-connect/developers#ton-connect-ui-react) 工具包用于您的 dApp。 只切换到更低级别的 SDK 或重新实现您的协议版本，如果您的产品真有必要。
:::

此页面包含TON连接的有用库列表。

- [TON Connect React](/develop/dapps/ton-connect/developers#ton-connect-react)
- [TON Connect JSSDK](/develop/dapps/ton-connect/developers#ton-connect-js-sdk)
- [TON Connect Python SDK](/develop/dapps/ton-connect/developers#ton-connect-python)
- [TON Connect Dar](/develop/dapps/ton-connect/developers#ton-connect-dart)
- [TON Connect C#](/develop/dapps/ton-connect/developers#ton-connect-c)
- [TON Connect Unity](/develop/dapps/ton-connect/developers#ton-connect-unity)
- [TON Connect Go](/develop/dapps/ton-connect/developers#ton-connect-go)

## TON连接React

- [@tonconnect/ui-react](/develop/dapps/ton-connect/developers#ton-connect-ui-react) - React应用的TON Connect 用户界面 (UI)

TonConnect UI React是 TonConnect SDK 的React UI 包。 在React应用中使用 TonConnect 协议将您的应用连接到 TON 钱包.

- `@tonconnect/ui-react`的应用程序示例： [GitHub](https://github.com/ton-connect/demo-dapp-with-react-ui)
- 部署的`demo-dapp-with-react-ui`: [GitHub](https://ton-connect.github.io/demo-dapp-with-react-ui/)

```bash
npm i @tonconnect/ui-response
```

- [GitHub](https://github.com/ton-connect/sdk/tree/main/packes/ui-react)
- [NPM](https://www.npmjs.com/package/@tonconnect/ui-react)
- [API 文档](https://ton-connect.github.io/sdk/modules/_tonconnect_ui_react.html)

## TON 连接 JSSDK

TON Connect 仓库包含以下主要软件包：

- [@tonconnect/ui](/develop/dapps/ton-connect/developers#ton-connect-ui) - TON Connect 用户界面 (UI)
- [@tonconnect/sdk](/develop/dapps/ton-connect/developers#ton-connect-sdk) - TON Connect SDK
- [@tonconnect/protocol](/develop/dapps/ton-connect/developers#ton-connect-protocol-models) - TON Connect 协议规格。

### TON Connect UI

TonConnect UI 是 TonConnect SDK 的 UI 包。 使用 TonConnect 协议将您的应用连接到 TON 钱包. 它允许您使用我们的用户界面元素，例如“连接钱包按钮”、“选择钱包对话”和确认模式，将TonConnect整合到您的应用中。

```bash
npm i @tonconnect/ui
```

- [GitHub](https://github.com/ton-connect/sdk/tree/main/packes/ui)
- [NPM](https://www.npmjs.com/package/@tonconnect/ui)
- [API 文档](https://ton-connect.github.io/sdk/modules/_tonconnect_ui.html)

TON Connect User Interface (UI) 是一个允许开发者改进应用程序用户体验(UX)的框架。

TON Connect 可以很容易地与应用集成，使用简单的界面元素，如“连接钱包按钮”、“选择钱包对话”和确认模式。 以下是三个主要示例说明TON Connect 如何改进应用程序中的 UX：

- DAppbrowser应用功能示例： [GitHub](https://ton-connect.github.io/demo-dapp/)
- 上述应用的后端分区示例： [GitHub](https://github.com/ton-connect/demo-dapp-backend)
- 使用 Go: [GitHub]桥接服务器 (https://github.com/ton-connect/bridge)

这个工具包将简化TON Blockchain应用程序中的 TON Connect 的实现。 标准前端框架以及不使用预定框架的应用程序都得到支持。

### TON 连接 SDK

帮助开发者整合TON Connect到他们的应用程序的三个框架中最低级别的是TON Connect SDK。 它主要用于通过 TON Connect 协议将应用连接到 TON Wallet

- [GitHub](https://github.com/ton-connect/sdk/tree/main/packes/sdk)
- [NPM](https://www.npmjs.com/package/@tonconnect/sdk)

### TON Connect 协议模型

此包包含协议请求、协议响应、事件模型、编码和解码函数。 它可以用于集成TON Connect 到 TypeScript 写入的钱包应用。 为了将TON Connect 整合到一个 DApp中，应使用[@tonconnect/sdk](https://www.npmjs.com/package/@tonconnect/sdk)。

- [GitHub](https://github.com/ton-connect/sdk/tree/main/packes/protocol)
- [NPM](https://www.npmjs.com/package/@tonconnect/protocol)

## TON Connect Python

### pytonconnect

TON 连接 2.0 的 Python SDK `@tonconnect/sdk`库的模拟。

使用 TonConnect 协议将您的应用连接到 TON 钱包.

```bash
pip3 安装 pytonconnect
```

- [GitHub](https://github.com/XaBbl4/pytonconnect)

### ClickoTON-Foundation tonconnect

连接到 Python 应用程序的 TON 连接

```bash
git 克隆https://github.com/ClickotoN-Foundation/tonconnect.git
pip-e tonconnect
```

[GitHub](https://github.com/ClickotoN-Foundation/tonconnect)

## TON Connect Dart

显示 TON 连接 2.0 的 SDK 文件。 `@tonconnect/sdk`库的模拟。

使用 TonConnect 协议将您的应用连接到 TON 钱包.

```bash
 $ dart pub 添加黑色连接
```

- [GitHub](https://github.com/romanovichim/dartTonconnect)

## TON Connect C\#

TON Connect 2.0的C# SDK。 `@tonconnect/sdk`库的模拟。

使用 TonConnect 协议将您的应用连接到 TON 钱包.

```bash
 $ dotnet 添加 TonSdk.Connect
```

- [GitHub](https://github.com/continuation-team/TonSdk.NET/tree/main/TonSDK.Connect)

## TON Connect Go

访问 SDK 获取TON 连接 2.0。

使用 TonConnect 协议将您的应用连接到 TON 钱包.

```bash
 github.com/cameo-engineering/tonconnect
```

- [GitHub](https://github.com/cameo-engineering/tonconnect)

## 一般性问题和关注

如果我们的开发者或社区成员在实现TON Connect 2.0期间遇到任何其他问题，请联系[Tonkeeper developer](https://t.me/tonkeeperdev)频道。

如果您遇到任何其他问题，或想要就如何改进TON Connect 2提出建议。 ，请通过相应的 [GitHub 目录](https://github.com/ton-connect/) 直接联系我们。

## TON Connect Unity

:::danger
This library is outdated at the moment.

请使用 [@ton-connect/ui](https://www.npmjs.com/package/@tonconnect/ui) 来获取您的 Unity 应用程序。
:::

TON Connect 2.0 的Unity asset。 使用 "continuation-team/TonSdk.NET/tree/main/TonSDK.Connect"。

使用它来集成TonConnect 协议和你的游戏。

- [GitHub](https://github.com/continuation-team/unity-ton-connect)

## 另见：

- [一步一步一步建立您的第一个网页客户端](https://ton-community.github.io/tutorials/03-client/)
- [[YouTube] TON Smart Contracts | 10 | Telegram DApp[EN]](https://www.youtube.com/watch?v=D6t3eZPdgAU\&t=254s\&ab_channel=AlefmanVladimir%5BEN%5D)
- [Ton Connect Getting started](https://github.com/ton-connect/sdk/tree/main/packes/sdk)
- [集成手册](/develop/dapps/ton-connect/integration)
- [[YouTube] TON Dev Study TON Connect Protocol [RU]](https://www.youtube.com/paylist?list=PLyDBPwv9EPsCJ226xS5_dKmXXxWx1CKz_)
