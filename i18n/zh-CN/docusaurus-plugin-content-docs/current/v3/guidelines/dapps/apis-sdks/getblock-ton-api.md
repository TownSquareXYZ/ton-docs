import Feedback from '@site/src/components/Feedback';

# HTTP API by GetBlock

:::tip TON infrastructure status

- [status.toncenter](https://status.toncenter.com/) - Provides various statistics of node activity in the last hour.
- [Tonstat.us](https://tonstat.us/) - A real-time Grafana dashboard that updates every 5 minutes.
  :::

This guide covers essential steps in acquiring and using private RPC endpoints by GetBlock to access TON Blockchain.

:::info
[GetBlock](https://getblock.io/) is a Web3 infrastructure provider that offers HTTP-based API endpoints for clients to interact with multiple blockchain networks, including TON.
:::

## How to access TON Blockchain endpoints

To start using GetBlock’s endpoints, users need to log in to their accounts, and retrieve a TON endpoint URL. Follow these instructions:

### 1. Create a GetBlock account

Visit the GetBlock website and click on the "Get Started for Free" button. Sign up using your email address or by connecting your MetaMask wallet.

登录后，您将被重定向到仪表板。找到 "My Endpoints" 部分，在 "Protocols" 下拉菜单中选择 "TON"。

### 2. Select TON Blockchain

After signing in, go to the "My Endpoints" section. Choose TON from the "Protocols" dropdown menu and select the desired network and API type (JSON-RPC or JSON-RPC(v2)).

点击 “Get” 按钮生成 TON 区块链端点 URL。

### 3. Generate your endpoint URL

Click the **Get** button to generate your TON Blockchain endpoint URL. The structure of the endpoint will be: `https://go.getblock.io/[ACCESS TOKEN]/`.

Access tokens act as unique identifiers for your requests, eliminating the need for separate API keys or authorization headers.

现在，您可以使用这些 URL 与 TON 区块链进行交互、查询数据、发送交易以及构建去中心化应用程序，而无需进行繁琐的基础设施设置和维护。

![GetBlock_account_endpoints](/img/docs/getblock-img/unnamed-3.png)

Now, you can use these URLs to interact with TON Blockchain, query data, send transactions, and build decentralized applications without the hassle of infrastructure setup and maintenance.

### Free requests and user limits

Each registered user receives 40,000 free requests per day, with a cap of 60 requests per second (RPS). This balance is renewed daily and can be used for any supported blockchain.

### Shared nodes

- 多个客户同时使用同一节点的初级机会；
- 速率限制增至 200 RPS；
- 非常适合个人使用，或与全面扩展的生产应用相比，交易量和资源需求较低的应用；
- 对于预算有限的个人开发者或小型团队来说，这是一个更经济实惠的选择。

Shared nodes provide a cost-effective solution for accessing TON Blockchain infrastructure without the need for significant upfront investment or commitment.

当开发人员扩展其应用程序并需要更多资源时，他们可以轻松升级订阅计划，或在必要时过渡到专用节点。

### Dedicated nodes

- One node is exclusively allocated to a single client;
- No request limits;
- 打开对存档节点、各种服务器位置和自定义设置的访问；
- 保证为客户提供优质服务和支持。

在本节中，我们将深入探讨 GetBlock 提供的 TON HTTP API 的实际用法。我们将通过实例来展示如何有效利用生成的端点进行区块链交互。

## 常见应用程序接口调用示例

In this section, we delve into the practical usage of the TON HTTP API provided by GetBlock. We explore the examples to showcase how to effectively utilize the generated endpoints for your blockchain interactions.

### 常见应用程序接口调用示例

You can use the `/getAddressBalance` method to get the balance for a specific TON address:

```
curl --location --request GET 'https://go.getblock.io/[ACCESS-TOKEN]/getAddressBalance?address=EQDXZ2c5LnA12Eum-DlguTmfYkMOvNeFCh4rBD0tgmwjcFI-' \    
--header 'Content-Type: application/json' 
```

![getAddressBalance\_response\_on\_TON\_blockchain](/img/docs/getblock-img/unnamed-2.png)

查询 TON 区块链的其他一些可用方法：

![getAddressBalance_response_on_TON_Blockchain](/img/docs/getblock-img/unnamed-2.png)

请参阅 GetBlock 的 [文档](https://getblock.io/docs/ton/json-rpc/ton_jsonrpc/)，以获取包含示例和附加方法列表的全面 API 参考。

| # | 方法   | Endpoint           | 说明                                                                                                                      |
| - | ---- | ------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| 1 | GET  | getAddressState    | Returns the current state of a specified address (uninitialized, active, or frozen). |
| 2 | GET  | getMasterchainInfo | Fetches the state of the masterchain.                                                                   |
| 3 | GET  | getTokenData       | Retrieves details about an NFT or jetton associated with the address.                                   |
| 4 | GET  | packAddress        | Converts a TON address from raw format to human-readable format.                                        |
| 5 | POST | sendBoc            | Sends serialized BOC files with external messages for blockchain execution.                             |

For a comprehensive list of methods and detailed API documentation, please refer to GetBlock's [documentation](https://getblock.io/docs/ton/json-rpc/ton_jsonrpc/).

### 部署智能合约

Developers can utilize the TON library to deploy and interact with contracts. The library will initialize a client to connect to the network via the GetBlock HTTP API endpoints.

欢迎通过 网站 了解更多信息，或通过即时聊天、Telegram或网站表格向 GetBlock 支持人员留言。

By following this guide, developers can easily access TON Blockchain using GetBlock's infrastructure. Whether you're working on decentralized applications (dApps) or simply querying data, GetBlock simplifies the process by offering ready-to-use HTTP API endpoints with various features.

Feel free to learn more at the website or drop a line to GetBlock’s support via live chat, Telegram, or a website form.

<Feedback />

