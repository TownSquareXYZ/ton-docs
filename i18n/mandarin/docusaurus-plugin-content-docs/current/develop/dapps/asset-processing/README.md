从 '@site/src/components/buton' 导入按钮

# 付款处理

此页面包含一个概述和具体细节来解释如何处理 (发送和接受) TON blockchain上的数字资产。

:::info 交易确认
只有一次确认后，TON交易是不可逆的。 为了获得最好的用户体验，建议在TON Blockchain上完成交易后避免等待额外的块。 阅读更多 [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3)。
:::

## 最佳做法

### 钱包的基础

- [创建密钥对，一个钱包并获取一个钱包地址](https://github.com/toncenter/examples/blob/main/common.js)

### Toncoin

#### Tonco币存款

:::info
建议您接受多个钱包的存款。
:::

- [[JS 代码接受Toncoin 存款](https://github.com/toncenter/examples es/blob/main/deposits.js)

#### Tonco币提款

- [JS 代码将从批处理中的钱包中提取(发送) Toncode ](https://github.com/toncenter/exampes/ blob/main/removals-higload-batch.js)

- [JS 代码要从钱包中提取(发送) Toncoins](https://github.com/toncenter/examples/blob/main/removals-higload.js)

- [详细信息](https://docs.ton.org/develop/dapps/asset-processing#global-overview)

### 杰顿

#### Jeton Deposits

:::info
建议您接受多个钱包的存款。
:::

- [接受jettons deposits的JS代码](https://github.com/toncenter/examples/blob/main/deposits-jettons.js)

#### 石头提款

- [JS 代码要从钱包中提取(发送) jettons](https://github.com/toncenter/examples/blob/main/rewals-jettons-highload.js)

- [JS 代码将从批处理中的钱包中提取(发送)jettons](https://github.com/toncenter/examples/ blob/main/rewrong-jettons-higload-batch.js)

- [详细信息](https://docs.ton.org/develop/dapps/asset-processing/jettons)

## 其他例子

### 自托管服务

#### 由社区制作的

[Gobicycle](https://github.com/gobicycle/bicycle) 服务侧重于充值用户余额和向区块链账户付款。 TON和Jettons都得到支持。 服务写入了许多陷阱，考虑到开发者可能遇到(所有的首饰检查)。 正确的操作状态检查，重新发送消息，当区块链被碎片拆分时的高负载性能)。 提供关于新付款的简单HTTP API、rabbit和web钩子通知。

### JavaScript

#### 由社区制作的

使用 ton.js SDK (TON社区支持)：

- format@@0(https://github.com/ton-community/ton#usage)

### Python

#### 由社区制作的

使用 psylopunk/pytonlib (Simple Python 客户端用于 Open Network)：

- [正在发送交易](https://github.com/psylopunk/pytonlib/blob/main/examples es/transactions.py)

使用 tonsdk 库 (类似于tonweb)：

- [[Init wallet, 创建外部消息来部署钱包](https://github.com/tonfacty/tonsdk#create-mnemonic-init-wallet-class-create-external-message-to-departy-the-wallet)

### Golang

#### 由社区制作的

- [见完整的例子列表](https://github.com/xssnick/tonutils-go#how to-use)

## A. 全球概览

TON Blockchain 显示完全异步的方法，涉及一些与传统区块链不同的概念。 尤其是，任何行为者与区块链的每个互动都包括智能合约和/或外部世界之间异步传输消息的图形。 任何互动的共同路径始于发送给一个 `wallet` 智能合约的外部消息。 它使用公用钥匙加密来验证消息发送者，收取费用，并发送内部区块链信息。 这样做， TON网络上的交易并不是用户与 blockchain 交互的同义词，只是消息图的节点：通过智能合约接受和处理消息的结果。 可能导致或不会导致出现新的信息。 这种互动可能包括任意数量的信息和交易，时间很长。 从技术上来说，与邮件队列的交易被归类为验证器处理的块。 TON Blockchain 的异步性质**不允许在发送消息阶段预测交易的散列和lt (逻辑时间)**。 接受到方块的交易是最终的，无法修改。

\*\*每个内部区块链消息都是从一个智能合约到另一个智能合约的消息。 \*\* 本文件载有一定数量的数字资产以及数据的任意部分。

智能合同准则建议将数据有效载荷作为一个可读的文字信息处理，从32个二进制零开始。 大多数软件，如钱包和库； 支持此规格并允许与Tonco币一起发送文本评论以及在其他消息中显示评论。

智能合同 **支付交易费用** (通常来自收到信件的余额) 和 **存储合同代码和数据的存储费** 。 收费取决于工作链配置，最大收费在 `masterchain` 和 `basechain` 大幅降低。

## TON 上的数字资产

TON有三种类型的数字资产。

- Toncoin，网络的主要令牌。 它用于区块链上的所有基本操作，例如支付煤气费或挂卡进行验证。
- 本地令牌是特殊类型的资产，可以附加到网络上的任何消息。 由于发行新本地令牌的功能已经关闭，这些资产目前尚未使用。
- 合同资产，如代币和净现值， 这些标准类似于ERC-20/ERC-721标准，并由任意合同管理，因此可能需要习惯规则进行处理。 您可以在[processe NFTs](/develop/dapps/asset-processing/nfts)和[processe Jettons](/develop/dapps/asset-processing/jettons)文章中找到更多关于它的处理信息。

### 简单的Tonco币传输

若要发送Toncoin，用户需要通过外部信息发送请求，即： 一个来自外部世界到区块链的消息到一个特殊的 `wallet` 智能合约(见下文)。 收到此请求时，`wallet`将发送一个内部消息，包含所需的资源和可选的数据有效载荷，例如文本注释。

## 钱包智能合同

钱包智能合同是 TON 网络上的合同，用于让区块链外的行为者与区块链实体交互的任务。 一般而言，它解决了三个挑战：

- 认证所有者: 拒绝处理非所有者的请求并支付费用。
- 保护再放：禁止重复执行一个请求，例如发送资产到其他一些智能合同。
- 启动与其他智能合约的任意互动。

第一个挑战的标准解决方案是公用钥匙加密：`wallet`储存公用钥匙，并检查收到请求的消息是否由对应的私钥签名，而私钥只有所有者才知晓。 解决第三个挑战的办法也是常见的；一般而言，请求包含一个完全形成的内部消息“wallet”发送到网络。 然而，为了保护回放，有几种不同的做法。

### 基于 Seqno的钱包

基于 Seqno的钱包采用最简单的方法来排序信息。 每个消息都有一个特殊的`seqno`整数，必须与存储在 `wallet` 智能合同中的计数器重合。 `wallet` 在每个请求上更新计数器，从而确保一个请求不会被处理两次。 在公开可用的方法中有几个`wallet`版本不同：在到期前限制请求的能力 和拥有多个拥有相同公钥的钱包的能力。 然而，这种做法的一项固有要求是逐一发出请求。 因为`seqno`序列中的任何空白将导致无法处理所有其后的请求。

### 高负载钱包

这种“钱包”类型遵循一种基于在智能合同存储中存储未过期处理请求的标识符的方法。 在这个方法中，将检查任何请求是否与已处理过的请求重复，如果检测到重播，则丢弃。 由于到期，这项合同可能无法将所有请求永远存放，但它将删除由于过期限制而无法处理的请求。 对此钱包的请求可以同时发送，而不相互干扰；然而，这种方法需要对请求的处理进行更加复杂的监测。

## 与 blockchain 的互动

TON Blockchain 上的基本操作可以通过 TonLib进行。 这是一个共享的库，可以与TON节点一起编译，并透露API，通过所谓的 lite 服务器与区块链进行交互(针对简单客户端的服务器)。 Tonlib 通过检查所有收到数据的证据来遵循一种不可信的做法；因此，没有必要设立一个受信任的数据提供者。 TonLib 可用的方法[TL模式](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L234)。 它们可以用作一个共享库，通过封装程序如 [pyTON](https://github.com/EmelyanenkoK/pyTON) 或 [tonlib-go](https://github)。 om/mercuryoio/tonlib-go/tree/master/v2) (技术上是`tonlibjson`的包装器)或通过 `tonlib-clif`。

## 钱包部署

要通过 Tonlib 部署一个钱包，需要：

1. 通过 [createNewKey](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L213)或其包装器函数(例如在 [tonlib-go](https://github.com/mercuryoio/tonlib-go/tree/master/v2#create-new-private-key)生成私有/公钥对。 请注意，私钥是本地生成的，不会离开主机机。
2. 表格 [InitialAccountWallet](https://github.com/ton-blockchain/ton/blob/master/tl/generate/tonlib_api.tl#L60) 与已启用的 `wallets` 之一相对应的结构。 当前`wallet.v3`, `wallet.higload.v1`, `wallet.higload.v2` 是可用的。
3. 通过 [getAccountAddress](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L249)计算新的 `wallet` 智能合同的地址。 我们建议使用默认修订版 `0` 并同时在 basechain `workchain=0` 中部署钱包，用于较低的处理和存储费用。
4. 发送一些Tonco币到计算地址。 请注意，您需要以`non-bounce`模式发送它们，因为此地址还没有代码，因此无法处理收到的消息。 `non-bounce`旗帜表示，即使处理失败，也不应在退回退信中退款。 我们不建议在其他交易中使用`non-bounce`旗帜，特别是当携带大额款项时， 因为退信机制提供了一定程度的保护，以免出现错误。
5. 格式化所需的 [action](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L148)，例如只部署了 `actionNoop` 。 然后使用 [createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L255) 和 [sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L260) 发起与blockchain的交互。
6. 在 [getAccountState](https://github.com/ton-blockchain/ton/blob/master/tl/generate/libton_api.tl#L254) 方法几秒钟内检查合同。

:::tip
在钱包教程中阅读更多信息](/develop/smart-contracts/tutorials/wallet#-deping-a-wallet)
:::

## 传入的消息值

为了计算电文给合同带来的接收值，需要解析交易。 这种情况发生在电文撞击合同时。 可以通过 [getTransactions]获取交易(https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L236)。 对于收到的钱包交易，正确的数据包含一个收到的消息和零发出的消息。 否则，就会向钱包发送外部消息，在这种情况下，所有者会花费Toncoin， 或者钱包未被部署，收到的交易将退回。

Anyway, in general, the amount that a message brings to the contract can be calculated as the value of the incoming message minus the sum of the values of the outgoing messages minus the fee: `value_{in_msg} - SUM(value_{out_msg}) - fee`. 从技术上讲，交易表述包含三个不同的领域，名称为“fee”、“storage_fee”和“other_fee”， 也就是说，总收费、一部分费用与储存费用有关，一部分费用与交易处理有关。 只能使用第一个。

## 正在检查合同的交易

可以通过 [getTransactions]获得合同交易(https://github.com/ton-blockchain/ton/blob/master/tl/generate/libton_api.tl#L236)。 此方法允许从 'transactionId' 和更早的 10 笔交易。 为了处理所有入账交易，应遵循下列步骤：

1. 最新的`last_transaction_id`可以通过 [getAccountState]获取(https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L235)
2. 应该通过 `getTransactions` 方法加载10个交易列表。
3. 应处理此列表中未查看的交易。
4. 收取付款是指收到消息的来源地址的交易； 发送付款是指收到的消息没有源地址的交易，也是指发出的信息。 应相应处理这些交易。
5. 如果所有这10项交易都未见过，则应加载今后10项交易，并应重复步骤2 3 4 5。

## 接受付款

在接受付款方面有几种不同的区分用户的方法。

### 基于发票的办法

若要根据所附评论接受付款，服务应该：

1. 部署钱包合同。
2. 为每个用户生成一个唯一的\`发票'。 uuid32的精致代表就够了。
3. 应指示用户发送Tonco币给服务的`wallet`合同，并附上\`发票'。
4. 服务应该定期投票`wallet`合同的 getTransactions 方法。
5. 对于新的交易，应提取收到的信息，\`评注'与数据库匹配。 和存入用户账户的值(见**传入消息值** 段落)。

## 发票

### 带有音调//链接的发票

如果您需要简单的用户流程整合，它适合使用 ton:// 链接。
最适合一次性付款和发票。

```bash
ton://transfer/<destination-address>?
    [nft=<nft-address>&]
    [收费金额=<nanocoins>&]
    [前导金额=<nanocoins>] 
```

- :check_mark_buton: 简单集成

- :check_mark_buton: 无需连接钱包

- ❌ 用户需要扫描每笔付款的新二维码

- :cross_mark：无法跟踪用户是否签名交易

- :cross_mark：没有关于用户地址的信息

- ❌ 在无法点击此链接的平台上需要工作条件(如Telegram 桌面客户端的机器人消息)

\<Button href="https://github.com/tonkeeper/wallet-api#payment-urls"
colorType="primary" sizeType={'lg'}>
了解更多 </Button>

### TON Connect 的发票

最适合于需要在会话中签署多笔付款/交易或需要在一段时间内保持与钱包的连接。

- :check_mark_buton: 钱包有一个永久的通讯频道，用户地址信息

- ✅ 用户只需要扫描二维码

- :check_mark_buton: 可以找到用户是否确认了钱包中的交易，通过退回的 BOC 跟踪交易

- :check_mark_buton: 已就绪的 SDKs 和 UI 套件可用于不同的平台

- ❌ 如果您只需要一次付款，用户需要采取两项动作: 连接钱包并确认交易

- ❌ 集成比音调// 链接更复杂.

\<Button href="/develop/dapps/ton-connect/"
colorType="primary" sizeType={'lg'}>
了解更多 </Button>

## 发送付款

1. 服务应该部署一个“钱包”并保持其资金，以防止由于储存费而破坏合同。 请注意储存费每年一般低于1吨币。
2. 服务应该从用户 `destination_address` 和可选的 `comment` 中获取。 请注意，在这段时间里，我们要么建议禁止使用同样的（“目的地地址”、“价值”、“评论”）或适当安排这些付款的时间； 这样，下一次付款只是在上一次付款得到确认之后才开始支付。
3. 表格 [msg.dataText](https://github.com/ton-blockchain/ton/blob/master/tl/generate/tonlib_api.tl#L98)，将“comment”作为文本。
4. 表格 [msg.message](https://github.com/ton-blockchain/ton/blob/master/tl/generate/tonlib_api.tl#L108)，其中包含 `destination_address`, 空 `public_key`, `amount` 和 `msg.dataText`)。
5. 表格 [Action](https://github.com/ton-blockchain/ton/blob/master/tl/generate/tonlib_api.tl#L149)，其中包含一组传出消息。
6. 使用 [createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L255) 和 [sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L260)
7. 服务应该定期投票`wallet`合同的 getTransactions 方法。 通过`destination_address`, `value`, `comment`) 将已确认的交易与已完成的付款匹配起来； 检测并向用户显示相应的交易哈希和空调(逻辑时间)。
8. `load`钱包`v3`的请求默认有60秒的到期时间。 此后未处理的请求可以安全地转回网络（见步骤3-6）。

## 探险家

区块链浏览器是 https://tonscan.org。

要在探险者中生成交易链接，服务需要获取 lt (逻辑时间)，交易哈希。 和帐户地址 (通过getTransaction方法检索lt 和 txhash的帐户地址)。 https://tonscan.org 和 https://explorer.toncoin.org/ 然后可以以下格式显示该页面：

`https://tonviewer.com/transaction/{txhash as base64url}`

`https://tonscan.org/tx/{lt as int}:{txhash as base64url}:{account address}`

\`https://explorer.toncoin.org/transaction?account={account address}&lt={lt as int}&hash={txhash as base64url}
