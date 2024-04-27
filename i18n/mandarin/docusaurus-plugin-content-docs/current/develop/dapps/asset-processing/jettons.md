从 '@theme/Tabs'导入标签页;
从 '@theme/TabItem'导入标签页;
从'@site/src/components/buton'导入按钮;

# TON Jetton处理器

关于如何处理珠宝的最佳做法：

- [JS algo to accept jettons deposits](https://github.com/toncenter/examples/blob/main/deposits-jettons.js)

- [JS algo to jettons 提款](https://github.com/toncenter/examples/blob/main/rewals-jettons-highload.js)

- [JS 代码将从批处理中的钱包中提取(发送)jettons](https://github.com/toncenter/examples/ blob/main/rewrong-jettons-higload-batch.js)

:::info 交易确认
只有一次确认后，TON交易是不可逆的。 为了获得最好的用户体验，建议在TON Blockchain上完成交易后避免等待额外的块。 阅读更多 [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3)。
:::

在大多数情况下，这对您来说应该足够，如果没有，您可以在下面找到详细信息。

## 内容列表

本文件按顺序说明如下：

1. 概览
2. 结构
3. Jetton Master Contract (Token Minter)
4. Jetton Wallet 合同 (用户钱包)
5. 消息布局
6. 珠宝加工(脱链)
7. 珠宝加工(链上)
8. 钱包处理
9. 最佳做法

## 概览

:::info
为了明确理解，读者应熟悉[我们文件的这一部分](/develop/dapps/asset-processing/)中所述的资产处理基本原则。 尤其重要的是熟悉 [contracts](/learn/overviews/addresses#everything-is-a-smart-contract), [wallets](/develop/smart-contracts/tutorials/wallet), [messages](/develop/smart-contracts/guidelines/message-delivery-guaranteures) 和部署进程。
:::

快速跳转到珠宝处理的核心描述：

\<Button href="/develop/dapps/asset-processing/jettons#accepting-jettons-from-users-through-a-centralized-wallet" colorType={'primary'} sizeType={'sm'}>Centralized Proccessing</Button>
\<Button href="/develop/dapps/asset-processing/jettons#accepting-jettons-from-user-deposit-addresses"
colorType="secondary" sizeType={'sm'}>
On-Chain Processing </Button>

<br></br><br></br>

TON Blockchain及其基础生态系统将可互换代币归类为珠宝。 因为碎片应用于TON Blockchain，与类似的区块链模型相比，我们的可替代代币的实现是独一无二的。

在这种分析中，我们更深入地了解详细介绍jeton [behavior]的正式标准(https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md)和 [metadata](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md)。
在我们的
[jettons blog post的解析](https://blog.ton.org/how to-shard-your-ton-smart-contract-and-why-studying-the-anatomy-of-tons-jettons)中可以找到一个不太正式的焦点焦点设计概览。

我们还提供了关于我们第三方开源TON 付款处理器的具体细节([bicycle](https://github)。 它允许用户在不使用文本备忘录的情况下使用单独的存款地址存取Tonco币和珠宝。

## Jetton Arstructure

使用一套智能合约实现TON上的标准化代币，包括：

- [Jetton master](https://github.com/ton-blockchain/token-contract/blob/main/ft/jetton-minter.fc) 智能合同
- [Jetton wallet](https://github.com/ton-blockchain/token-contract/blob/main/ft/jetton-wallet.fc) 智能合同

<p align="center">
  <br />
    <img width="420" src="/img/docs/asset-processing/jetton_contracts.svg" alt="contracts scheme" />
      <br />
</p>

## Jetton master 智能合同

珠宝主智能合同储存关于珠宝的一般信息(

包括总供应、元数据链接或元数据本身)。

任何用户都可以创建一个珍贵珠宝的假冒克隆(使用任意名称、牌照、图像等) 这几乎与原来的相同。 值得庆幸的是，伪造的珠宝通过其地址加以区分，并且能够很容易地辨认出来。

消除TON用户欺诈的可能性， 请查找特定类型珠宝原始地址(Jetton master contract)，或按项目的官方社交媒体频道或网站查找正确信息。 检查资产以消除[Tonkeeper ton-assets list](https://github.com/tonkeeper/ton-assets)欺诈的可能性。

### 检索杰顿数据

要检索更具体的Jetton数据，将使用 `get_jetton_data()` 方法获取。

此方法返回以下数据：

| 名称                   | 类型      | 描述                                                                                                                                     |
| -------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `total_supply`       | `int`   | 以不可分割单位计量的发行珠宝总数。                                                                                                                      |
| `mintable`           | `int`   | 是否可以嵌入新的jetton。 此值是 -1 (可以被输入) 或 0 (无法输入)。                                                       |
| `admin_address`      | `slice` |                                                                                                                                        |
| `jetton_content`     | `cell`  | data in accordance with [TEP-64](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md). |
| `jetton_wallet_code` | `cell`  |                                                                                                                                        |

也可以使用 [Toncore API](https://toncenter.com/api/v3/#/default/get_jetton_masters_api_v3_jetton_masters_v3_jetton_masters_get) 的方法来检索已经被解码的Jetton数据和元数据。 我们还制定了一些方法（js) [tonweb](https://github.com/toncenter/tonweb/blob/master/src/contract/token/ft/JettonMinter.js#L85) 和(js) [ton-core/ton](https://github.com/ton-core/ton/blob/master/master/src/jetton/JettonMaster.ts#L28), (go) [tongo](https://github.com/tonkeeper/tongo/blob/master/liteapi/jetton)。 o#L48) 和(go) [tonutils-go](https://github.com/xssnick/tonutils-go/blob/33fd62d754d3a01329ed5c904db542ab4a11017b/ton/jetton/jetton.go#L79)，(python) [pytonlib](https://github.com/toncenter/pytonlib/blob/d96276ec8a466638cb939de23612876a6881/pytonlib/client.py#L742) 和许多其他SDKs。

使用 [Tonweb](https://github.com/toncenter/tonweb) 来运行一种方法并获取超链元数据的 url 示例：

```js
从 "tonweb"导入TonWeb ;
const tonweb = new TonWeb();
const jettonMinter = new TonWeb。 oken.jetton.JettonMinter(tonweb.provider, {address, "<JETTON_MASTER_ADDRESS>"});
const data = 等待jettonMinter. etJettonData();
console.log('总计供应:', data.total. Supply.toString());
console.log('URI to unchain metadata:', data.jettonContentUri);
```

#### Jetton 元数据

关于元数据解析的更多信息已提供 [here](/develop/dapps/asset-processing/metadata)。

## Jetton Wallet 智能合同

Jetton钱包合同用于发送、接收和烧毁珠宝。 每个_jetton钱包合同_为特定用户存储钱包余额信息。
在特定情况下，每种珠宝类型的珠宝个别持有者可使用珠宝钱包。

Jetton wallets should not be confused with wallet’s meant for blockchain interaction and storing
only the Toncoin asset (e.g., v3R2 wallets, highload wallets, and others),
which is responsible for supporting and managing only a specific jetton type.

Jetton钱包使用智能合约，并且使用
所有者的钱包和珠宝钱包之间的内部信息进行管理。 例如，说Alice是否管理内有jettons钱包。
方案如下：Alice拥有专为jetton使用设计的钱包(如钱包版本 v3r2)。
当Alice在她管理的钱包中开始发送jettons时，她会向她的钱包发送外部消息，
并因此而发送。 _her wallet_发送内部消息到 _her jeton wallet_ 和
然后jetton钱包实际执行令牌转移。

### 检索给定用户的 Jetton 钱包地址

要使用所有者地址（TON钱包地址）检索jetton钱包地址，
Jetton主合同提供获取方法`get_wallet_address(slice owners_address)`。

#### 使用 API 获取

The application serializes the owner’s address to a cell using
the `/runGetMethod` method from the [Toncenter API](https://toncenter.com/api/v3/#/default/run_get_method_api_v3_runGetMethod_post).

#### 使用 SDK 获取

这个进程也可以通过准备使用我们各种SDK中存在的方法，例如：\
使用 Tonweb SDK，这个过程可以通过输入以下字符串来启动：

```js
从 "tonweb"导入TonWeb ;
const tonweb = new TonWeb();
const jettonMinter = new TonWeb。 oken.jetton.JettonMinter(tonweb.provider, {address, "<JETTON_MASTER_ADDRESS>"});
const address = 等待jettonMinter. etJettonWalletAddress(新 TonWeb.utils)。 服装("<OWNER_WALLET_ADDRESS>");
// 必须始终检查钱包是否确实归因于所需的杰顿大师：
const jettonWallet = new TonWeb。 oken.jetton.JettonWallet(tonweb.provider, Aconstrucer, {
  address: jettonWalletAddress
});
const jettonData = 等待jettonWallet.getData();
if (jettonData.jettonMinterAddress.toString(false) !== new TonWeb.utils.Address(info)。 ddress).toString(false)) Windows
  抛出新的错误('jeton minter address from jeton walling does not t match configur');
}

console.log('Jeton ware地址:', address.toString(true), true);
```

:::tip
更多示例改为[TON Cookbook](/develop/dapps/cookbook#how to calculate-users-jetton-wallet-address)。
:::

### 获取特定Jetton钱包的数据

要检索钱包账户余额，所有者身份信息以及与特定的杰顿钱包合同相关的其他信息， `get_wallet_data()` 方法用于jetton钱包合同。

此方法返回以下数据：

| 名称                                                           | 类型  |
| ------------------------------------------------------------ | --- |
| 余额                                                           | 整数  |
| 所有者                                                          | 切片  |
| 吉普车                                                          | 切片  |
| jetton_wallet_code | 单元格 |

也可以使用 `/jetton/wallets` 获取方法 [Toncore API](https://toncenter)。 om/api/v3/#/default/get_jetton_wallets_api_v3_jetton_wallets_get，检索先前解码的杰顿钱包数据(或SDK中的方法)。 例如，使用 Tonweb：

```js
从 "tonweb"导入TonWeb ;
const tonweb = new TonWeb();
const walletAddress = "EQBYc3DSi36qur7-DLDYd-AmRb4-zk6VkzX0etv5Pa-Bq4Y";
const jettonWallet = new TonWeb. oken.jetton.JettonWallet(tonweb.provider,{address: walletAddress});
const data = 等待jettonWallet etData();
console.log('Jetton balanc:', data.balanc.toString());
console.log('Jetton owners address:', data.owners. Address. oString(true，true));
// 必须始终检查Jeton Maston 确实确认钱包
const jettonMinter = new TonWeb。 oken.jetton.JettonMinter(tonweb.provider, {ton: data.jettonMinterAddress.toString(false)});
const expectedJettonWalletAddress = 等待jettonMinter.getJettonWalletAddress(data.owners.toString(false));
if expectedJettonWalletAddress. oString(false) !== new TonWeb.utils.Address(walletAddress).toString(false))
  扔出新的错误('jeton minter不识别钱包')；
}

控制台。 og('Jetton master address:', data.jettonMinterAddress.toString(true, true));
```

### Jetton Wallet 部署

在钱包之间传输jetton时， 交易(消息)需要一定数量的 TON
作为支付网络煤气费和根据Jeton 钱包合同的代码执行操作。
这意味着收款人在接收珠宝之前不需要部署jetton钱包。
只要发件人在钱包中持有足够的TON
支付所需的煤气费，收件人的珠宝钱包就会自动部署。

## 消息布局

:::tip 留言
Read more about Messages [here](/develop/smart-contracts/guidelines/message-delivery-guarantees).
:::

Jetton钱包与 TON 钱包之间的通信通过以下通信序列进行：

![](/img/docs/asset-processing/jetton_transfer.svg)

`Sender -> sender' jeton wallet` 是指_transfer_message body 包含以下数据：

| 名称                     | 类型     |
| ---------------------- | ------ |
| `query_id `            | uint64 |
| `amount `              | 硬币     |
| `目的`                   | 地址     |
| `response_destination` | 地址     |
| `custom_payload `      | 单元格    |
| `forward_ton_amount`   | 硬币     |
| `forward_payload`      | 单元格    |

“收款人”jetton钱包 -> 收款人”是指消息通知机构包含以下数据：

| 名称                                | 类型     |
| --------------------------------- | ------ |
| 查询ID                              | uint64 |
| 金额                                | 硬币     |
| 发件人\`                             | 地址     |
| 前进_payload\` | 单元格    |

"收款人" jetton钱包 -> Sender" 是指超量的消息正文包含以下数据：

| 名称         | 类型     |
| ---------- | ------ |
| `query_id` | uint64 |

Jetton钱包合同字段的详细描述可在 [TEP-74](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md) Jetton标准接口描述。

使用 `Transfer notification` 和 `Excesses`参数的消息是可选的，取决于`Transfer`消息所附的 TON
数量和`forward_ton_amount`字段的值。

`query_id`标识符允许应用程序将三种消息类型`Transfer`、`Transfer notification`和`Excesses`连接'。
为了正确执行此进程，建议总是使用一个唯一的查询ID。

### 如何发送带有评论和通知的Jetton transfers

为了进行带有通知的转移（然后在钱包中用于通知目的）；
必须通过设置一个非零`forward_ton_amount`
值将足够的TON附加到正在发送的消息。 如有必要，在`forward_payload`中附上文本注释。
在发送 Toncoin 时，文本注释的编码类似于文本注释。

[发送犹太人的费用](https://docs.ton.org/develop/smart-contracts/fees#fees-for-sending-jettons)

然而，该委员会取决于若干因素，包括《杰顿代码》的细节以及为收款人部署一个新的杰顿钱包的必要性。
因此，建议将Tonco币附加一个比值，然后将地址设置为 "response_destination"
来检索“过剩”信息。 例如，在 "forward_ton_amount"
值设置为 0时，0.05 TON 可以附加到消息中。 1 TON (这个数量的TON将附加到 `Transferfacation`消息)。

[使用Tonweb SDK的评论示例的Jeton transfer](https://github.com/toncenter/tonweb/blob/b550969d960235314974008d2c04d3d4e5d1f546/src/test-jetton.js#L128):

```js
// first 4 bytes are tag of text comment
const comment = new Uint8Array([... new Uint8Array(4), ... new TextEncoder().encode('text comment')]);

await wallet.methods.transfer({
    secretKey: keyPair.secretKey,
    toAddress: JETTON_WALLET_ADDRESS, // address of Jetton wallet of Jetton sender
    amount: TonWeb.utils.toNano('0.05'), // total amount of TONs attached to the transfer message
    seqno: seqno,
    payload: await jettonWallet.createTransferBody({
        jettonAmount: TonWeb.utils.toNano('500'), // Jetton amount (in basic indivisible units)
        toAddress: new TonWeb.utils.Address(WALLET2_ADDRESS), // recepient user's wallet address (not Jetton wallet)
        forwardAmount: TonWeb.utils.toNano('0.01'), // some amount of TONs to invoke Transfer notification message
        forwardPayload: comment, // text comment for Transfer notification message
        responseAddress: walletAddress // return the TONs after deducting commissions back to the sender's wallet address
    }),
    sendMode: 3,
}).send()
```

:::tip
将更多例子改为[TON Cookbook](/develop/dapps/cookbook#how to construct-a-message-fora-jetton-transfer-with a comment).
:::

## 焦炭脱链处理

:::info 交易确认
只有一次确认后，TON交易是不可逆的。 为了获得最好的用户体验，建议在TON Blockchain上完成交易后避免等待额外的块。 阅读更多 [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3)。
:::

允许使用者接受犹太人的几种情况是可能的。 犹太人可以在一个集中的热钱包中被接受； 此外，他们也可以使用一个为每个用户设有单独地址的钱包接受他们。

要处理Jetton，就需要一个热钱包，不像个性化的 TON 处理 (v3R2, 此外还有
的杰顿钱包或多个杰顿钱包。 我们文档的[钱包部署](/develop/dapps/asset-processing/#wallet-support)描述了杰顿热钱包的部署。
尽管如此，仍然不需要按照[杰顿钱包部署](#jetton-wallet-supplement)标准部署杰顿钱包。
然而，当犹太人被接纳时，将自动部署犹太人钱包。 意味着当犹太人被撤除时，
将假定他们已经在用户手中。

出于安全原因，最好拥有独立的热钱包，供独立的犹太人(每一类资产都有许多钱包)。

处理资金时， 还建议提供冷钱包，储存不参加自动存款和提款过程的多余资金。

### 添加新的犹太人用于资产处理和初步验证

1. 要找到正确的智能合同代币主地址，请参阅以下来源：[如何找到正确的Jetton master contract](#jetton-master-smart-contract)
2. 此外，要检索特定Jetton的元数据，请查阅以下来源：[如何接收Jetton元数据](#retrieving-jetton-data.
   为了正确地向用户展示新的犹太人，需要正确的“小数”和“符号”。

为了我们所有用户的安全，必须避免可能被假冒的犹太人。 例如，
Jettons with `symbol`==`TON` 或者那些包含系统通知消息的人，例如:
`ERROR`, `SYSTEM` 和其他人。 请务必检查jetton在您的接口中显示的方式能够使他们不能被
与TON传输混合起来。 系统通知等。 有时，甚至连符号`、`name`和`image\`
都会被创建，看起来与原来的内容几乎完全相同，有误导用户的希望。

### 接收传输通知消息时识别一个未知Jeton

1. 如果在你的钱包里收到了一个未知的 Jetton 的转移通知消息， 然后你的钱包
   已经创建来保持特定的Jetton。 其次，必须进行几项核查工作。
2. 包含`Transfer notification`的内部消息的发件人地址是新的Jetton钱包的地址。
   不要与 `Transfer notification`实体中的`sender`字段混淆， Jetton 钱包
   的地址是来自消息来源的地址。
3. 检索新的Jetton钱包的Jetton主地址：[如何检索Jetton钱包的数据](#retrieving-jetton-data.
   要执行此进程，需要`jetton`参数，是构成Jetton主合同的地址。
4. 使用 Jetton master contract: [如何检索给定用户的 Jetton 钱包地址] (#retrieving-jetton-wallet-address-for-a give-user) 获取你钱包地址的 Jeton 钱包地址 (作为所有者)
5. 比较主合同返回的地址和钱包代币的实际地址。
   如果它们匹配，它是理想的。 如果没有，你很可能会收到一个伪装的骗子令牌。
6. 检索杰顿元数据：[如何接收杰顿元数据](#retrieving-jetton-data)。
7. 检查 `symbol` 和 `name` 字段以获取垃圾邮件的信号。 必要时警告用户。 [增加一个新的犹太人，用于处理和初步检查](#adding-new-jettons-for-asset-processing-initial-chalisation)。

### 通过集中钱包接受用户的 Jettons

:::info
为了防止进入单个钱包的交易出现瓶颈， 建议接受多个钱包的存款并根据需要扩大这些钱包的数量。
:::

在这种情况下， 付款服务为每个发件人创建一个独特的备忘录标识符，透露
集中钱包地址和发送的金额。 发件人通过评论中的必修备备忘录将代币
发送到指定的集中地址。

**支持此方法：** 此方法非常简单，因为接受令牌时没有额外的费用，并且直接从热钱包中获取。

**此方法的含义：** 此方法要求所有用户在传输时附上评论，这可能导致更多的存款错误 (忘记了memos, ) 不正确的备忘录等 也就是说支助人员的工作量增加。

Tonweb 示例：

1. [接受Jeton 存款到个人HOT 钱包，并附有评论(emo)](https://github.com/toncenter/exampes/ blob/main/deposits-jettons-sin-sin-wallet.js)
2. [Jettons 提款示例](https://github.com/toncenter/examples/blob/main/jettons-rewals.js)

#### 筹备工作

1. 编写一份被接受的犹太人名单：[增加新的犹太人以供处理和初步核实](#adding-new-jettons-for-asset-processing-initial-cherchation)。
2. 热钱包部署 (使用v3R2 ，如果预计不会有Jetton 提款；高负载v2 - 如果预计会有Jetton提款的话) [Wallet 部署](/develop/dapps/asset-processing/#wallet-app)。
3. 使用热钱包地址进行测试以初始化钱包。

#### 正在处理进来的犹太人

1. 加载被接受的犹太人列表
2. 为你部署的热钱包获取一个Jetton钱包地址：[如何为给定的用户检索Jetton钱包地址](#retrieving-jetton-wallet-address-for-a assigne-user)
3. 为每个Jetton钱包检索一个Jetton主地址：[如何检索一个Jetton钱包的数据](#检索专门的jetton-wallet)。
   要执行此进程，需要`jetton`参数(实际上是Jetton主合同的
   地址)。
4. 将Jetton master contracts的地址与第1步相比较。 和第3步(直接以上)。
   如果地址不匹配，必须报告Jetton地址验证错误。
5. 通过热钱包账户获取最新未处理交易的列表和
   迭代它(通过每笔交易逐个排序)。 见：[检查合同的交易](https://docs.ton.org/develop/dapps/asset-processing/#checking-contracts-transactions)，
   或使用 [Tonweb 示例](https://github.com/toncenter/example](https://github.com/toncentes/blob/9f20f710441171793dfbbdf07f0ca4860f12de2/deposits-sin-sinwallet.js#L43)
   或使用 Toncenter API `/getTransactions` 方法。
6. 检查输入消息 (in_msg) 的交易并从输入消息中检索源地址。 [Tonweb example](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbbdf07f0ca4860f12de2/deposits-jettons-sin-single-wallet.js#L84)
7. 如果源地址与Jetton钱包中的地址匹配，则需要继续处理交易。
   如果没有，则跳过交易处理并检查下一个交易。
8. 确保消息主体不是空的，消息的前32位匹配`transfer notification`0x7362d09c\`。
   [Tonweb 示例](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbbdf07f0ca4860f12de2/deposits-jettons-sin-single-wallet.js#L91)
   如果消息内容是空的或是操作代码无效 - 跳过交易。
9. 读取消息主体的其他数据，包括`query_id`、`amount`、`sender`、`forward_payload`。
   [Jetton contracts message layouts](#jetton-contract-message-layouts), [Tonweb example](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbdf07f0ca4860f12de2/deposits-jettons-sin-sin-wallet.js#L105)
10. 尝试从 "forward_payload " 数据检索文本注释。 前32位必须匹配
    文本注释操作代码 `0x00000000` 和剩余的 UTF-8 编码文本。
    [Tonweb 示例](https://github.com/toncenter/examples/blob/9f20f7104411771793dfbbbdf07f0ca4860f12de2/deposits-jettons-sin-single-wallet.js#L110)
11. 如果"forward_payload"数据为空或op代码无效 - 跳过交易。
12. 将收到的评论与保存的备忘录进行比较。 如果有匹配项 (用户标识总是可能) - 交存传输。
13. 从第5步重启并重复该进程，直到你走遍整个交易列表。

### 接受用户存款地址

接受用户存款地址中的犹太人， 付款服务必须为每个参与者汇款创建自己的
个人地址(存款)。 在这种情况下，提供的服务涉及
执行几个平行程序，包括创建新的存款， 扫描交易块，
从存款提取资金到热钱包等等。

因为一个热钱包可以为每个Jetton类型使用一个Jetton钱包 需要创建多个
钱包来启动存款。 为了创建大量钱包，但同时使用
一个种子短语(或私钥)来管理他们， 需要在创建钱包时指定不同的 `subwallet_id` 。
在TON上，创建子钱包所需的功能由版本 v3 钱包及更高版本的钱包支持。

#### 在Tonweb 中创建子钱包

```Tonweb
const WalletClass = tonweb.wallet.all['v3R2'];
const 钱包 = new WalletClass(tonweb.provider, p.
    publicKey: keyPair.publicKey,
    wc: 0,
    walletId: <SUBWALLET_ID>,
});
```

#### 准备工作

1. 编制一份被接受的犹太人名单：[添加新的犹太人进行处理和初步检查](#adding-new-jettons-for-asset-processing-initial-cherchation)
2. 热钱包 [钱包部署](/develop/dapps/asset-processing/#wallet-deplement)

#### 创建存款

1. 接受为用户创建新存款的请求。
2. 基于热钱包种子生成一个新的子钱包 (v3R2) 地址。 [在 Tonweb中创建一个子钱包](#creating-a-subwallet-in-tonweb)
3. 接收地址可以提供给用户，作为Jetton矿床使用的地址(这是
   的地址，是Jetton钱包所有者的地址)。 钱包初始化是不需要的，这可以是
   从保证金中提取犹太人时完成。
4. 对于这个地址，必须通过Jetton master contract计算Jetton钱包的地址。
   [如何检索给定用户的 Jetton 钱包地址](#retrieving-jetton-wallet-address-for-a give-user)。
5. 将Jetton钱包地址添加到地址池中，以监测交易并保存子钱包地址。

#### 处理交易

:::info 交易确认
只有一次确认后，TON交易是不可逆的。 为了获得最好的用户体验，建议在TON Blockchain上完成交易后避免等待额外的块。 阅读更多 [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3)。
:::

并不总是能够确定从该电文中收到的犹太人的确切数量。 因为Jetton
钱包可能无法发送 `transfer notification`, `excesses`, 和 `internal transfer` 消息不标准化。 这意味着
无法保证内部传输消息可以被解码。

因此，为了确定钱包中收到的金额，需要使用获取方法要求余额。
为了在请求余额时检索关键数据，根据特定区块在链上的状态使用块。
[准备使用 Tonweb接受块](https://github.com/toncenter/tonweb/blob/master/src/test-blockcribe.js)。

这一进程的实施方式如下：

1. 准备区块接受（通过系统准备接受新区块）。
2. 检索一个新块并保存上一个块ID。
3. 接收来自方块的交易。
4. 筛选只使用来自宝石钱包存款地址的交易。
5. 使用 "transfer notification" 正文解码消息来接收更详细的数据，包括
   "sender" 地址、Jeton `amount` 和注释。 (见：[处理进来的犹太人](#加工-incoming-jettons))
6. 如果至少有一个交易具有不可解码的消息(消息主体不包含
   `transferation notification` 和 'exces\`optodes 代码)，或者没有存在于
   帐户中的消息, 然后必须使用当前方块的获取方法请求Jetton余额， 而上一个
   区块用来计算余额差额。 Now the total balance deposit changes are revealed due
   to the transactions being conducted within the block.
7. 作为犹太人身份不明的转移的识别符号(没有\`转移通知')， 交易数据
   可以在存在这样一个交易或阻止数据时使用(如果有几个数据存在于一个区块中)。
8. 现在需要检查以确保存款余额正确。 如果存款余额足以启动热钱包和现有Jetton钱包之间的转移， 犹太人需要撤出，以确保钱包余额减少。
9. 从第2步重新启动并重复整个进程。

#### 从存款中提款

不应从存款转账到每次存款充资的热钱包。
因为TON中的一个佣金用于转让操作(支付网络煤气费)。
必须确定一定数量的犹太人，以便使
转账具有价值(因而也是存款价值)。

默认情况下，Jetton存款钱包的钱包所有者未初始化。 这是因为没有预先确定的
要求支付存储费用。 当发送带有一个
`transfer` 实体的消息时，Jetton 存款钱包可以被部署，然后立即销毁。 要做到这一点，工程师必须使用特殊的
机制发送信息：128 + 32。

1. 检索标记提取到热钱包的存款列表
2. 检索每笔存款保存的所有者地址
3. 然后将消息发送到每个所有者的地址(通过将多个这样的消息合并成批) 从高载
   钱包和附加的TON Jetton金额。 这是通过添加用于v3R2钱包
   初始化+发送消息的费用来确定的。传输正文+与"forward_ton_amount"
   (如果有必要)相关的 TON。 所附的TON金额是通过添加v3R2钱包初始化(值)+
   的费用来确定的。发送带有`transfer`body`(值)+任意TON金额 
   的`forward_ton_amount\`(如果必要)的信息的费用。
4. 当地址余额变为非零时，账户状态会发生变化。 等待几秒钟并检查帐户的状态
   ，不久它将从 '不存在' 状态更改为 'uninit'。
5. 对于每个所有者的地址(具有`uninit`状态), 必须发送带有v3R2钱包
   的外部消息，并且正文包含`transfer`消息存入Jetton钱包=128 + 32。 对于`transfer`,
   用户必须指定热钱包的地址作为`destination` 和 `response destination` 。
   可以添加文本注释，使其更容易识别传输。
6. 考虑到[这里发现的犹太人信息的处理](#processing-incoming-jettons)，可以使用
   到热钱包地址的存款地址验证犹太人的交付。

### 石头提款

若要取出Jetton，钱包将带有`transfer`实体'的消息发送给对应的 Jetton 钱包。
然后，Jetton 钱包将犹太人发送给收款人。 本着诚意，必须将一些TON
附加为 `forward_ton_amount` (和可选的 `forward_payload`) 来触发一个 `transferation` 。
见：[Jetton contracts message layouts](#jetton-contract-message-layouts)

#### 准备工作

1. 编制一份撤离犹太人名单：[增加新的犹太人以供处理和初步核查](#adding-new-jettons-for-asset-processing-initial-cherchation)
2. 已启动热钱包部署。 建议高加载 v2。 [钱包部署](/develop/dapps/asset-processing/#wallet-部署)
3. 使用热钱包地址进行一次Jetton转账以初始化Jetton钱包并补充其余额。

#### 正在处理提款

1. 加载已处理的犹太人列表
2. 为已部署的热钱包获取Jetton钱包地址：[如何为给定用户检索Jetton钱包地址](#retrieving-jetton-wallet-address-for-a-user)
3. 检索每个Jetton钱包的 Jeton master 地址：[如何检索Jeton wallets](#retrieving-data-for a specific-jetton-wallet).
   需要一个“jetton”参数(实际上是Jetton master contracts的地址)。
4. 从第1步比较Jetton master contracts的地址。 和第3步： 如果地址不匹配，则应报告Jetton地址验证错误。
5. 收到的提款请求实际上表明了犹太人的类型、转移的金额以及接收方的钱包地址。
6. 检查Jetton钱包的余额以确保有足够的资金进行提款。
7. 填写所需字段，包括query_id，使用Jetton`transfer`实体生成一条消息， 正在发送的金额，
   目的地(收件人的非Jetton钱包地址)， 响应目标 (建议指定用户的热钱包),
   forward_ton_amount (建议至少将其设置为 0)。 5 TON to calling a `transfer notification`), `forward_payload`
   (可选，如果需要发送评论的话)。 [Jetton contracts message layouts](#jetton-contract-message-layouts),
   [Tonweb example](https://github.com/toncenter/examples/blob/9f7f7104411771793dfbbdf07f0ca4860f12de2/jettons-drawals. s#L69)
   为了检查交易的成功验证。 它需要为每条消息分配一个唯一的值给
   `query_id` 。
8. 使用高速加载钱包时， 建议收集一批信息，每次发送一批信息，以优化费用。
9. 保存发送外部消息的到期时间(这是钱包成功
   处理消息的时间) 完成后，钱包将不再接受消息)
10. 发送单条消息或多条消息(短信)。
11. 获取热钱包账户中最新未处理的交易列表并进行迭代。
    在这里了解更多: [检查合同的交易](/develop/dapps/asset-processing/#checking-contracts-transactions),
    [Tonweb example](https://github.com/toncenter/examples/blob/9f20f74411771793dbbbd07f07f0ca4860f12de2/deposits-sin-lallet.js#L43) 或
    使用 Toncenter API `/getTransactions` 方法。
12. 查看帐户中的发送消息。
13. 如果消息与 `transfer` op代码存在, 那么它应该被解码以检索`query_id` 值。
    检索的 \`query_id' 需要标记为成功发送。
14. 如果处理当前扫描的交易所需时间大于
    则找不到指定的`query_id`
    的过期时间和发出的信息。 然后请求应该(这是可选的) 标记为过期，并且应该安全地重新安置。
15. 在帐户中寻找收到的消息。
16. 如果存在一个使用 'excesses' 操作代码的消息，则该消息应该解码，并且应该获取 'query_id'
    值。 找到的 `query_id` 必须标记为成功交付。
17. 转到第5步。 未成功发送过期请求应被推回到退出列表。

## 链上的焦炭处理

:::info 交易确认
只有一次确认后，TON交易是不可逆的。 为了获得最好的用户体验，建议在TON Blockchain上完成交易后避免等待额外的块。 阅读更多 [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3)。
:::

一般来说，要接受和处理jetton，一个负责内部消息的消息处理程序使用 "op=0x7362d09c" op 代码。

下面列出了在进行上链珠宝加工时必须考虑的建议：

1. 使用他们的钱包类型来识别传入的jettons，而不是他们的Jetton主合同。 换言之， 您的合同应该与特定的jetton钱包交互(接收和发送消息) (不是与某个未知钱包使用特定Jetton主合同)。
2. 连接Jetton Wallet 和 Jetton Master时，检查这个连接是否是双向的，钱包承认主合同，反之亦然。 例如， 如果您的合同系统收到了Jetton钱包的通知(它认为它的MySuperJetton是它的主合同)，它的转移信息必须显示给用户， 在显示 MySuperJeton 合同的 `symbol`、`name` 和 `image`
   之前，请检查MySuperJeton 钱包是否使用了正确的合同系统。 反过来, 如果您的合同系统出于某种原因需要使用MySuperJetton或MySuperJetton主合同发送jetton，则使用相同的合同参数验证钱包X。
   此外，在将 'transfer' 请求发送到 X，请确保它承认MySuperJeton 是它的主人。
3. 分散融资的真正实力取决于能否将协议堆叠在一起，如大腿块。 例如，Jeton A被换成B型珠宝，而B型珠宝又被吞并。 然后用作贷款协议中的杠杆(当用户供应流动性时)，然后用来购买NFT... 等等。 因此，考虑合同如何能够为非链式用户提供服务。 但在链上的实体也通过在传输通知中附加标记化的值，并添加一个可与传输通知一起发送的自定义有效载荷。
4. 请注意，并非所有合同都遵循同样的标准。 遗憾的是，有些喷气式飞机可能具有敌意(使用攻击性矢量)，制造这些喷气式飞机的唯一目的是攻击毫无疑义的用户。 为了安全起见，如果有关协议包含许多合同，则不会创建大量同类珠宝钱包。 特别是不在协议内在存款合同、保险库合同或用户帐户合同等之间发送珠宝。 攻击者可能通过伪造传输通知、珠宝数量或有效载荷参数故意干扰合同逻辑。 通过每个焦炭系统中只使用一个钱包来降低攻击潜力(所有存款和提款)。
5. 为每个个人化的喷气式飞机创立分包合同以减少地址伪装的机会也常常是一个好主意（例如）。 当转让电文使用预定用于jettonA的合同发送给jettonB时。
6. 强烈建议在合同一级与不可分割的珠宝单位合作。 与十进制相关的逻辑通常被用来增强阴道的用户界面 (UI)，与数字链上的记录保存无关。
7. 要了解更多关于[CertiK在 FunC 中安全智能合同编程](https://blog.ton.org/secure-smart-contract-programming-infunction)的信息，请随意阅读此资源。 建议开发者处理所有智能合同异常，这样他们就不会在应用程序开发过程中跳过。

## Jetton 钱包处理

一般而言，用于非链珠宝加工的所有核实程序也适用于钱包。 对于杰顿钱包的处理，我们最重要的建议如下：

1. 当一个钱包收到一个未知jetton钱包的转移通知， 信任珠宝钱包及其主地址至关重要，因为它可能是恶意假冒。 为了保护自己，请检查Jetton Master (主合同)，使用其提供的地址来确保您的验证过程承认jetton钱包是合法的。 当你信任钱包并且它被验证为合法后，你可以允许它访问你的帐户余额和其他钱包数据。 如果Jetton Master 不承认这个钱包，建议不要启动或透露您的珠宝转账，只显示传入的TON转账(附加到传输通知的Tonco币)。
2. 在实际操作中，如果用户想要与杰顿而不是珠宝交互。 换言之，用户发送 wTON/oUSDT/jUSDT, jUSDC, jDAI 而不是 `EQAjN...`/`EQBLE...`
   等. 这常常意味着当用户开始喷射时， 钱包询问相应的jettonmaster (用户拥有)启动转账请求的jettonmaster。 重要的是，绝不能盲目地相信大师的数据(总合同)。 在将转账请求发送到jetton钱包之前， 总是确保珠宝钱包确实属于它声称属于的杰顿大师。
3. 意识到敌意的杰顿大师/杰顿钱包可能会随着时间的推移改变他们的钱包/米斯特。 因此，用户必须尽职尽责，在每次使用之前检查他们与任何钱包互动的合法性。
4. 总是确保您在接口中以不会与 TON 传输、系统通知等混合的方式显示jetton。 甚至连`符号`、`name`和`image`
   参数都可以被制作成误导用户，使那些受影响的人成为潜在欺诈受害者。 曾发生过几起恶意喷气式飞机被用来假冒TON转移、通知错误、奖励收益或资产冻结公告的情况。
5. 经常发现潜在的恶意行为者制造假冒珠宝， 让用户拥有在主用户界面中消除不想要的喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式

Authored by [kosrk](https://github.com/kosrk), [krigga](https://github.com/krigga), [EmelyanenkoK](https://github.com/EmelyanenkoK/) and [tolya-yanot](https://github.com/tolya-yanot/).

## 最佳做法

这里我们提供了由TON Community members创建的jetton代码处理的几个例子：

<Tabs groupId="code-examples">
<TabItem value="tonweb" label="JS (tonweb)">

```js
const transfer = 等待wallet.methods.transfer(Windows
  secretKey: keyPair)。 ecretKey,
  toAddress: jettonWaletAddress,
  amount: 0,
  seqno: seqno,
  发送模式：128 + 32, // 模式128用于保留所有余额的信息； 模式32意味着，如果当前账户的余额为零，则必须销毁。
  有效载荷：等待jettonWallet。 ReateTransferBody(请注意，
    queryId：seqno，// 任意号码
    jettonamount：jettonBalance, // 以单位
    toAddress: new TonWeb为单位的jeton amount 倾斜。 dress(MY_HOT_WALLET_ADDRESS,
    responseAddress: new TonWeb.utils.Address(MY_HOT_WALLET_ADDRESS,
  }),
});
等待转移.send();
```


<TabItem value="tonutils-go" label="Golang">

```go
client := liteclient.NewConnectionPool()

// connect to testnet lite server
err := client.AddConnectionsFromConfigUrl(context.Background(), "https://ton.org/global.config.json")
if err != nil {
   panic(err)
}

ctx := client.StickyContext(context.Background())

// initialize ton api lite connection wrapper
api := ton.NewAPIClient(client)

// seed words of account, you can generate them with any wallet or using wallet.NewSeed() method
words := strings.Split("birth pattern then forest walnut then phrase walnut fan pumpkin pattern then cluster blossom verify then forest velvet pond fiction pattern collect then then", " ")

w, err := wallet.FromSeed(api, words, wallet.V3R2)
if err != nil {
   log.Fatalln("FromSeed err:", err.Error())
   return
}

token := jetton.NewJettonMasterClient(api, address.MustParseAddr("EQD0vdSA_NedR9uvbgN9EikRX-suesDxGeFg69XQMavfLqIw"))

// find our jetton wallet
tokenWallet, err := token.GetJettonWallet(ctx, w.WalletAddress())
if err != nil {
   log.Fatal(err)
}

amountTokens := tlb.MustFromDecimal("0.1", 9)

comment, err := wallet.CreateCommentCell("Hello from tonutils-go!")
if err != nil {
   log.Fatal(err)
}

// address of receiver's wallet (not token wallet, just usual)
to := address.MustParseAddr("EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N")
transferPayload, err := tokenWallet.BuildTransferPayload(to, amountTokens, tlb.ZeroCoins, comment)
if err != nil {
   log.Fatal(err)
}

// your TON balance must be > 0.05 to send
msg := wallet.SimpleMessage(tokenWallet.Address(), tlb.MustFromTON("0.05"), transferPayload)

log.Println("sending transaction...")
tx, _, err := w.SendWaitTransaction(ctx, msg)
if err != nil {
   panic(err)
}
log.Println("transaction confirmed, hash:", base64.StdEncoding.EncodeToString(tx.Hash))
```


<TabItem value="TonTools" label="Python">

```py
my_wareb = Wallet(provider=client, mnemonics=my_wallet_mnemonics, version='v4r2')

# for TonCenterClient and LsClient
等待my_wallet.transfer_jetton(destation_address='address', jetton_master_address=jetton. ddress, jettons_amount=1000, fee=0.15 


等待所有客户端的my_wallet.transfer_jetton_by_jetton_wallet(destination_address='address', jetton_wallet='your jettons', jettons_amount=1000, fe=0.1)  
```




### 以评论解析为焦点转移器

```ts
import {
    Address,
    TonClient,
    Cell,
    beginCell,
    storeMessage,
    JettonMaster,
    OpenedContract,
    JettonWallet,
    Transaction
} from '@ton/ton';


export async function retry<T>(fn: () => Promise<T>, options: { retries: number, delay: number }): Promise<T> {
    let lastError: Error | undefined;
    for (let i = 0; i < options.retries; i++) {
        try {
            return await fn();
        } catch (e) {
            if (e instanceof Error) {
                lastError = e;
            }
            await new Promise(resolve => setTimeout(resolve, options.delay));
        }
    }
    throw lastError;
}

export async function tryProcessJetton(orderId: string) : Promise<string> {

    const client = new TonClient({
        endpoint: 'https://toncenter.com/api/v2/jsonRPC',
        apiKey: 'TONCENTER-API-KEY', // https://t.me/tonapibot
    });

    interface JettonInfo {
        address: string;
        decimals: number;
    }

    interface Jettons {
        jettonMinter : OpenedContract<JettonMaster>,
        jettonWalletAddress: Address,
        jettonWallet: OpenedContract<JettonWallet>
    }

    const MY_WALLET_ADDRESS = 'INSERT-YOUR-HOT-WALLET-ADDRESS'; // your HOT wallet

    const JETTONS_INFO : Record<string, JettonInfo> = {
        'jUSDC': {
            address: 'EQB-MPwrd1G6WKNkLz_VnV6WqBDd142KMQv-g1O-8QUA3728', //
            decimals: 6
        },
        'jUSDT': {
            address: 'EQBynBO23ywHy_CgarY9NK9FTz0yDsG82PtcbSTQgGoXwiuA',
            decimals: 6
        },
    }
    const jettons: Record<string, Jettons> = {};

    const prepare = async () => {
        for (const name in JETTONS_INFO) {
            const info = JETTONS_INFO[name];
            const jettonMaster = client.open(JettonMaster.create(Address.parse(info.address)));
            const userAddress = Address.parse(MY_WALLET_ADDRESS);

            const jettonUserAddress =  await jettonMaster.getWalletAddress(userAddress);
          
            console.log('My jetton wallet for ' + name + ' is ' + jettonUserAddress.toString());

            const jettonWallet = client.open(JettonWallet.create(jettonUserAddress));

            //const jettonData = await jettonWallet;
            const jettonData = await client.runMethod(jettonUserAddress, "get_wallet_data")

            jettonData.stack.pop(); //skip balance
            jettonData.stack.pop(); //skip owneer address
            const adminAddress = jettonData.stack.readAddress();


            if (adminAddress.toString() !== (Address.parse(info.address)).toString()) {
                throw new Error('jetton minter address from jetton wallet doesnt match config');
            }

            jettons[name] = {
                jettonMinter: jettonMaster,
                jettonWalletAddress: jettonUserAddress,
                jettonWallet: jettonWallet
            };
        }
    }

    const jettonWalletAddressToJettonName = (jettonWalletAddress : Address) => {
        const jettonWalletAddressString = jettonWalletAddress.toString();
        for (const name in jettons) {
            const jetton = jettons[name];

            if (jetton.jettonWallet.address.toString() === jettonWalletAddressString) {
                return name;
            }
        }
        return null;
    }

    // Subscribe

    const Subscription = async ():Promise<Transaction[]> =>{

      const client = new TonClient({
        endpoint: 'https://toncenter.com/api/v2/jsonRPC',
        apiKey: 'TONCENTER-API-KEY', // https://t.me/tonapibot
      });

        const myAddress = Address.parse('INSERT-YOUR-HOT-WALLET'); // Address of receiver TON wallet
        const transactions = await client.getTransactions(myAddress, {
            limit: 5,
        });
        return transactions;
    }




    return retry(async () => {

        await prepare();
       const Transactions = await Subscription();

        for (const tx of Transactions) {

            const sourceAddress = tx.inMessage?.info.src;
            if (!sourceAddress) {
                // external message - not related to jettons
                continue;
            }

            if (!(sourceAddress instanceof Address)) {
                continue;
            }

            const in_msg = tx.inMessage;

            if (in_msg?.info.type !== 'internal') {
                // external message - not related to jettons
                continue;
            }

            // jetton master contract address check
            const jettonName = jettonWalletAddressToJettonName(sourceAddress);
            if (!jettonName) {
                // unknown or fake jetton transfer
                continue;
            }

            if (tx.inMessage === undefined || tx.inMessage?.body.hash().equals(new Cell().hash())) {
                // no in_msg or in_msg body
                continue;
            }

            const msgBody = tx.inMessage;
            const sender = tx.inMessage?.info.src;
            const originalBody = tx.inMessage?.body.beginParse();
            let body = originalBody?.clone();
            const op = body?.loadUint(32);
            if (!(op == 0x7362d09c)) {
                continue; // op == transfer_notification
            }

            console.log('op code check passed', tx.hash().toString('hex'));

            const queryId = body?.loadUint(64);
            const amount = body?.loadCoins();
            const from = body?.loadAddress();
            const maybeRef = body?.loadBit();
            const payload = maybeRef ? body?.loadRef().beginParse() : body;
            const payloadOp = payload?.loadUint(32);
            if (!(payloadOp == 0)) {
                console.log('no text comment in transfer_notification');
                continue;
            }

            const comment = payload?.loadStringTail();
            if (!(comment == orderId)) {
                continue;
            }
            
            console.log('Got ' + jettonName + ' jetton deposit ' + amount?.toString() + ' units with text comment "' + comment + '"');
            const txHash = tx.hash().toString('hex');
            return (txHash);
        }
        throw new Error('Transaction not found');
    }, {retries: 30, delay: 1000});
}

```

## 另见：

- [付款处理](/develop/dapps/asset-processing/)
- [NFT processing on TON](/develop/dapps/asset-processing/nfs)
- [TON上的元数据解析](/develop/dapps/asset-processing/metadata)
