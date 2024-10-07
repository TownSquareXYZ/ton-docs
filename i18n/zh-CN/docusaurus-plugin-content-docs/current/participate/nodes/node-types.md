import Button from '@site/src/components/button'

# TON 节点类型

深入了解开放网络（TON）的世界时，理解不同的节点类型及其功能至关重要。本文为希望与TON区块链互动的开发者详细介绍了每种节点类型。

深入了解开放网络（TON）的世界时，理解不同的节点类型及其功能至关重要。本文为希望与TON区块链互动的开发者详细介绍了每种节点类型。

## 全节点

它保留了区块链的_当前状态_，可以包含整个区块历史或其部分。这使其成为TON区块链的支柱，促进网络的去中心化和安全。

它保留了区块链的_当前状态_，可以包含整个区块历史或其部分。这使其成为TON区块链的支柱，促进网络的去中心化和安全。

```mdx-code-block
<Button href="/participate/run-nodes/full-node"
colorType="primary" sizeType={'sm'}>
```

运行全节点

```mdx-code-block
</Button>
```

## 归档节点

TON基于权益证明机制运行，其中验证者在维护网络功能方面发挥着关键作用。验证者会因其贡献而[以Toncoin获得奖励](/participate/network-maintenance/staking-incentives)，激励网络参与并确保网络安全。

[作为验证者运行全节点](/participate/run-nodes/full-node#become-a-validator)

\<Button href="/participate/run-nodes/archive-node"
colorType="primary" sizeType={'sm'}>
Running an Archive Node </Button>

## 验证者节点

TON operates on a **Proof-of-Stake** mechanism, where `validators` are pivotal in maintaining network functionality. `Validators` are [rewarded in Toncoin](/participate/network-maintenance/staking-incentives) for their contributions, incentivizing network participation and ensuring network security.

Liteservers使与轻客户端的快速通信成为可能，便于执行检索余额或提交交易等任务，而不需要完整的区块历史。

每个支持ADNL协议的SDK都可以使用`config.json`文件作为轻客户端。`config.json`文件包含了可以用来连接TON区块链的端点列表。

## Liteserver

每个不支持ADNL的SDK通常使用HTTP中间件来连接TON区块链。它的安全性和速度不如ADNL，但使用起来更简单。

`Liteservers` enable swift communication with Lite Clients, facilitating tasks like retrieving balance or submitting transactions without necessitating the full block history.

TON基金会提供了几个公共Liteservers，集成到全局配置中，可供普遍使用。这些端点，如标准钱包使用的端点，确保即使不设置个人liteserver，也能与TON区块链进行交互。

- [公共Liteserver配置 - 主网](https://ton.org/global-config.json)
- [公共Liteserver配置 - 测试网](https://ton.org/testnet-global.config.json)

在您的应用程序中使用下载的`config.json`文件与TON SDK。

If you want to have more stable *connection*, you can run your own `Liteserver`. To run a `full node` as a `Liteserver`, simply enable the `Liteserver` mode in your node's configuration file.

\<Button href="/participate/run-nodes/full-node#enable-liteserver-mode"
colorType="primary" sizeType={'sm'}>
Enable Liteserver in your Node </Button>

## 轻客户端：与 TON 交互的SDK

Each SDK which supports ADNL protocol can be used as a `Lite Client` with `config.json` file (find how to download it [here](/participate/nodes/node-types#troubleshooting)). The `config.json` file contains a list of endpoints that can be used to connect to the TON Blockchain.

每个不支持ADNL的SDK通常使用HTTP中间件来连接TON区块链。它的安全性和速度不如ADNL，但使用起来更简单。

它会从配置文件中移除响应慢的liteservers。

### 故障排除

Below you can find approaches how to fix common nowed issues with `light clients`

### 故障排除

[在节点中启用 Liteserver](/participate/run-nodes/full-node#enable-liteserver-mode)

1. 从tontech链接下载config.json文件：

```bash
wget https://api.tontech.io/ton/wallet-mainnet.autoconf.json -O /usr/bin/ton/global.config.json
```

这种节点对于创建需要完整区块链历史的区块链浏览器或其他工具至关重要。

2. Use the downloaded config.json file in your application with [TON SDK](/develop/dapps/apis/sdk).
