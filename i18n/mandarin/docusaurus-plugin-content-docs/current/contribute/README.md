# 概述

## 支付处理

**简而言之:**

- [TON浏览器](/participate/explorers)
- [钱包应用（开发者用）](/participate/wallets/apps)
- [钱包合约类型](/participate/wallets/contracts)
- 请查看 GitHub 库中的[issues](https://github.com/ton-community/ton-docs/issues)。
- 了解文档的可用的[开发奖金](https://github.com/ton-society/ton-footsteps/issues?q=documentation)。

## 加入TON社区

- [TON增强提案（TEP）](https://github.com/ton-blockchain/TEPs)
- [在answers.ton.org上提问关于TON的问题](https://answers.ton.org/)
- [与TON提名人共同质押](/participate/network-maintenance/nominators)

## 跨链桥

### 安装

在终端运行以下命令以创建一个新项目，并按照屏幕上的指示操作：

[![在 Gitpod 中打开](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/ton-community/ton-docs)

### 参与TON Web3

- [TON Web3概述](/participate/web3/overview)
- [使用TON DNS为您的域名](/participate/web3/dns)

JS SDK 为你做了这件事; 只需获取钱包列表 `connector.getWallets()` 并检查相应列表项的 `embedded` 属性。如果你构建自己的 SDK，你应该检查 `window.[targetWalletJsBridgeKey].tonconnect.isWalletBrowser`。

### 技术栈

如同嵌入式应用（见上文），JS SDK 通过相应的 `connector.getWallets()` 列表项的 `injected` 属性为你提供检测。如果你构建自己的 SDK，你应该检查 `window.[targetWalletJsBridgeKey].tonconnect` 是否存在。

提交拉取请求时，请确保以下内容：

1. [Node.js](https://nodejs.org)的最新版本，如v18，使用`node -v`验证版本
2. 支持TypeScript和FunC的IDE，如[Visual Studio Code](https://code.visualstudio.com/)，配备[FunC插件](https://marketplace.visualstudio.com/items?itemName=tonwhales.func-vscode)
3. **测试你的更改**。在拉取请求的描述中讲述你的测试计划。

使用psylopunk/pytonlib（The Open Network的简单Python客户端）：

## 从原始形式到友好形式

如果你构建一个钱包，你需要提供一个bridge。请参见我们的 [Go 参考实现](https://github.com/ton-connect/bridge)。
