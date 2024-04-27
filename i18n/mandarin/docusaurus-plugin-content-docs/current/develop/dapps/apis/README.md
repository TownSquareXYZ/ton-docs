# API 类型

**高可用性区块链API是安全、方便和快速开发有效应用的核心元素。**

- [TON HTTP API](/develop/dapps/apis/toncenter) — API 允许使用 _indexed blockchain 信息_。
- [TON ADNL API](/develop/dapps/apis/adnl) — secure API 以便基于ADNL 协议与TON进行通信。

## Toncent APIs

- [TON Index](https://toncenter.com/api/v3/) - TON Index 从一个完整节点收集数据到 PostgreSQL 数据库，并为索引区块链提供便捷的 API。
- [toncenter/v2](https://toncenter)。 om/) - 此 API 允许访问 TON blockchain - 获取帐户和钱包信息 查找块和交易，发送消息到区块链，调用智能合约等方法。

## 第三方APIs

- [tonapi.io](https://docs.tonconsole.com/tonapi/api-v2) - 快速索引API，提供有关账户、交易、块、应用程序的 NFT、拍卖、Jettons, TON DNS、订阅的基本数据。 它还提供了关于交易链的附加说明的数据。
- [dton.io](https://dton)。 o/graphql/) - GraphQL API，可以提供帐户、交易和块的数据 以及关于NFT、拍卖、犹太人和TON DNS的具体应用数据。
- [ton-api-v4](https://mainnet-v4.tonhubapi.com) - 另一个Lite-api通过在 CDN 中的主动提现注重速度。
- [docs.nftscan.com](https://docs.nftscan.com/reference/ton/model/asset-modell) - 用于TON blockchain的 NFT API。
- [evercloud.dev](https://ton-mainnet.evercloud.dev/graphql) - GraphQL API for basic questions in TON。
- [everspace.center](https://everspace.center/toncoin) - 访问 TON Blockchain的简单RPC API。

## 附加APIs

### Tonco币率 APIs

- https://tonapi.io/v2/rates?tokens=ton&curcies=ton%2Cusd%2Crub
- https://coinmarketcap.com/api/documentation/v1/
- https://apiguide.coingecko.com/getting-starting-started

### 地址转换 API

:::info
最好是通过本地算法转换地址，在文档的 [Addresses](/learn/overviews/addresses) 部分中阅读更多内容。
:::

#### 从友好到原始表单

/api/v2/unpackAddress

曲线

```curl
curl -X 'GET' \
'https://toncenter.com/api/v2/unpackAddress?address=EQApAj3rEnJJSxEjEHVKrH3QZgto_MQMOmk8l72azaXlY1zB' \
-H 'accept: application/json'
```

响应体

```curl
{
"ok": true,
"result": "0:29023deb1272494b112310754aac7dd0660b68fcc40c3a693c97bd9acda5e563"
}
```

#### 从友好到原始表单

/api/v2/packaddress

曲线

```curl
curl -X 'GET' \
'https://toncenter.com/api/v2/packAddress?address=0%3A29023deb1272494b112310754aac7dd0660b68fcc40c3a693c97bd9acda5e563' \
-H 'accept: application/json'
```

响应体

```json
{
  "ok": true,
  "result": "EQApAj3rEnJJSxEjEHVKrH3QZgto/MQMOmk8l72azaXlY1zB"
}
```

## 另见：

- [TON HTTP API](/develop/dapps/apis/toncenter)
- [列出SDK](/develop/dapps/apis/sdk)
- [TON Cookbook](/develop/dapps/cookbook)
