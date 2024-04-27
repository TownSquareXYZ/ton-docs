# GetBlock 的 TON API

本指南将涵盖GetBlock获取和使用私有RPC端点以访问TON区块链的必要步骤。

:::info
[GetBlock](https://getblock.io/) 是一个 Web3 基础结构提供商，为客户端提供基于 HTTP 的 API 端点，以便与包括TON在内的各种区块链网络交互。
:::

## 如何访问 TON Blockchain 端点

若要开始使用 GetBlock的端点，用户需要登录到他们的帐户，请检索TON 端点URL，他们很好了。 跟随更详细的指导。

### 1. 创建 GetBlock 帐户

访问 GetBlock [website](https://getblock.io/?utm_source=external\&utm_medium=article\&utm_campaign=ton_docs) 并在主页上找到"免费开始"按钮。 使用您的电子邮件地址或连接MetaMask钱包注册账户。

![GetBlock.io\_main\_page](/img/docs/getblock-img/unnamed-2.png?=RAW)

### 2. 选择 TON Blockchain

登录后，您将被重定向到仪表板。 定位标题为“我的端点”的部分，并在“协议”下拉菜单中选择“TON”。

选择所需的网络和 API 类型 (JSON-RPC 或 JSON-RPC(v2) )。

![GetBlock\_account\_\_dashboard](/img/docs/getblock-img/unnamed-4.png)

### 3. 生成您的端点URL

点击“获取”按钮生成您的TON区块链端点URL。

GetBlock API 中的所有端点都遵循一个一致的结构：`https://go.getblock.io/[ACCESS TOKEN]/`。

这些访问令牌是每个用户或应用程序的唯一标识符，包含将请求路由到适当端点所必需的信息，而不会透露敏感细节。 它基本上取代了单独授权头或 API 密钥。

用户可以灵活生成多个端点，在损坏时滚动令牌，或删除未使用的端点。

![GetBlock\_account\_endpoints](/img/docs/getblock-img/unnamed-3.png)

现在，您可以使用这些URL与TON blockchain、查询数据、发送交易进行交互。 并建立分散的应用程序，而不需要基础设施的安装和维护。

### 免费请求和用户限制

请注意，每个注册的 GetBlock 用户都收到40 000个免费请求，上限为60个RPS (每秒请求)。 请求余额每天更新，可以在支持区块链的任何共享端点上使用。

为了增强功能和能力，用户可以选择探索付费的备选办法，下文将概述这些办法。

GetBlock.io提供两种计划：共享节点和专用节点。 客户可以根据自己的要求和预算选择关税。

### 共享节点

- 进入一级的机会，让几个客户同时使用同一节点；
- 费率限制增加到200个RPS；
- 与全面规模的生产应用程序相比，适合个人使用或交易量和所需资源较低的应用程序；
- 对于预算有限的个人开发者或小型团队来说，一个更负担得起的选择。

共享节点为无需大量预付投资或承付就可以进入TON区块链基础设施提供成本效益高的解决办法。

随着开发者扩大其应用程序并需要额外资源，他们可以在必要时轻松地升级其订阅计划或过渡到专用节点。

### 专用节点

- 一个节点仅分配给一个客户端；
  没有请求限制；
- 打开存档节点、各种服务器位置和自定义设置的访问权限；
- 保证向客户提供溢价服务和支助。

这是开发者的下一级解决方案和需要提高产出的分散应用 (dApps) 节点连接的速度较高，并随着资源的规模而得到保证。

## 如何使用 GetBlock 的 TON HTTP API

在本节中，我们将深入探讨GetBlock提供的 TON HTTP API 的实际使用情况。 我们将探索示例来展示如何有效地利用生成的终点来进行您的 blockchain 交互。

### 常见的 API 调用示例

让我们从一个简单的例子开始，使用“/getAddressBalance”方法来检索一个特定地址的余额，使用curl命令进行检索。

```
curl --location --request GET 'https://go.getblock.io/<ACCESS-TOKEN>/getAddressBalance?address=EQDXZ2c5LnA12Eum-DlguTmfYkMOvNeFCh4rBD0tgmwjcFI-' \

--header 'Content-Type: application/json'
```

请确保使用 GetBlock提供的实际访问令牌替换 `ACCES-TOKEN` 。

这将输出notons

![getAddressBalance\_response\_on\_TON\_blockchain](/img/docs/getblock-img/unnamed-2.png)

查询TON区块链的其他可用方法：

| # | 方法 | Endpoint           | 描述                                                   |
| - | -- | ------------------ | ---------------------------------------------------- |
| 1 | 获取 | getAddressState    | 返回 TON 区块链上指定地址的当前状态 (未初始化、活动或冻结) |
| 2 | 获取 | getMasterchainInfo | 获取大师链状态信息                                            |
| 3 | 获取 | getTokenData       | 获取与 TON 帐户相关的 NFT 或 Jeton 详细信息                       |
| 4 | 获取 | 软件包地址              | 将 TON 地址从原始格式转换为可读的格式                                |
| 5 | 帖子 | sendBoc            | 将序列化的 BOC 文件和外部消息一起发送到区块链以执行                         |

请参考GetBlock的 [documentation](https://getblock.io/docs/ton/json-rpc/ton_jsonrpc/) 获取一个包含示例和附加方法列表的 API 参考信息。

### 部署智能合同

开发者可以使用相同的端点URL来无缝地使用TON库将合同部署到TON区块链。

库将初始化客户端通过GetBlock HTTP API 端点连接到网络。

![来自TON蓝图IDE](/img/docs/getblock-img/unnamed-6.png)

这个教程应该为寻求有效使用 GetBlock 的 API 和 TON Blockchain 的开发人员提供一个全面的指南。

请随时从 [website](https://getblock.io/?utm_source=external\&utm_medium=article\&utm_campaign=ton_docs) 中学习更多信息，或通过实时聊天、 [Telegram](https://t.me/GetBlock_Support_Bot)或网站表单向GetBlock提供支持。
