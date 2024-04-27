# 协议规范

了解TON Connect 如何在这个尺寸下工作。

## 本节适用于谁？

- 如果你实现了一个钱包
- 如果你开发了 SDK
- 如果您想要学习TON Connect 如何工作

## 班级概览

- [Protocol workflows](/develop/dapps/ton-connect/protocol/workflow) 是TON Connect所涉所有协议的概述。
- [Bridge API](/develop/dapps/ton-connect/protocol/bridge)指定了如何在应用程序和钱包之间传输数据。
- [Session protocol](/develop/dapps/ton-connect/protocol/session) 确保网上端到端的加密通信。
- [请求协议](/develop/dapps/ton-connect/protocol/requests-responses) 定义了应用程序和钱包的请求和响应。
- [钱包指南](/develop/dapps/ton-connect/protocol/wallet-guidelines) 定义了钱包开发者的指南。

## 常见问题

#### 我正在构建一个 HTML/JS 应用程序，我应该阅读什么？

只需使用 [支持的 SDKs](/develop/dapps/ton-connect/developers) 就可以不担心潜在的协议。

#### 我需要我最喜欢的语言的 SDK

请将[JSSDK](/develop/dapps/ton-connect/developers)作为参考并查看上面的协议文档。

#### 您如何检测应用程序是否嵌入钱包？

JS SDK 为你这样做；只需获取钱包列表`connector.getWallets()`并检查相应列表项的`嵌入`属性。 如果你构建了自己的 SDK，你应该检查 `window。[targetWalletJsBridgeKey].tonconnect.isWaletBrowser` 。

#### 你如何检测钱包是一个浏览器扩展？

像内嵌应用一样(见上文)，JSSDK通过相应的 `connector.getWallets()` 列表中的 `injected` 属性检测到它。 如果你构建了自己的 SDK，你应该检查 `windows。[targetWalletJsBridgeKey].tonconnect` 是否存在。

#### 如何使用tonconnect来执行后端授权？

[见一个 dapp-backend](https://github.com/ton-connect/demo-dapp-backend)

#### 我如何建立自己的桥梁？

除非你正在构建钱包，否则你不需要了。

如果你构建了一个钱包，你需要提供一个桥梁。 请参阅我们的 [reference implementation in Go](https://github.com/ton-connect/bridge)。

请记住，钱包里的 API 的一面没有授权。

为了快速启动，您可以使用通用的 TON Connect 桥https://bridge.tonapio/bridge。

#### 我制作一个钱包，我如何将它添加到钱包列表中？

提交一个 [wallets-list]的拉取请求 (https://github.com/ton-blockchain/wallets-list) 仓库并填写我们所有必要的元数据。

应用程序也可以直接通过 SDK 添加钱包。
