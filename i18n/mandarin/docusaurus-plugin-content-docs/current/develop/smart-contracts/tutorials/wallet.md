---
description: 在本教程中，您将学习如何完全使用钱包、交易和智能合约进行工作。
---

import Tabs from'@theme/Tabs';
import TabItem from'@theme/TabItem';

# 使用钱包智能合约的工作

## 👋 介绍

在开始智能合约开发之前，学习 TON 上的钱包和交易如何工作是必不可少的。这些知识将帮助开发者了解钱包、交易和智能合约之间的交互，以实现特定的开发任务。

在本节中，我们将学习如何创建操作，而不使用预配置的函数，以了解开发工作流程。本教程的所有必要参考资料都位于参考章节。

## 💡 必要条件

这个教程需要对 JavaScript、TypeScript 和 Golang 有基本的了解。同时至少需要持有 3 个 TON（可以存储在交易所账户、非托管钱包中，或使用电报机器人钱包进行存储）。此外，还需要对 [cell（单元）](/learn/overviews/cells)、[TON 地址](/learn/overviews/addresses) 和[区块链的区块链](/learn/overviews/ton-blockchain) 有基本的了解，以理解本教程。

:::info 主网开发至关重要
在 TON 测试网上工作往往会导致部署错误、难以跟踪交易以及不稳定的网络功能。因此，完成大部分开发工作时间可能好处是建议在 TON Mainnet 上完成，以避免这些问题，这可能需要减少交易数量，从而可能减小费用。
:::

## 源代码

本教程中使用的所有代码示例都可以在以下 [GitHub 存储库](https://github.com/aSpite/wallet-tutorial) 中找到。

## ✍️ 您开始所需的内容

- 确保 NodeJS 已安装。
- 需要特定的 Ton 库，包括：@ton/ton 13.5.1+、@ton/core 0.49.2+ 和 @ton/crypto 3.2.0+。

**可选**: 如果您喜欢使用 Golang 而不是使用 JS，那么需要安装 [tonutils-go](https://github.com/xssnick/tonutils-go) 库以及 GoLand IDE，用于进行 TON 开发。本教程中将使用这个库来进行 Golang 版本的操作。

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```bash
npm i --save @ton/ton @ton/core @ton/crypto
```


<TabItem value="go" label="Golang">

```bash
go get github.com/xssnick/tonutils-go
go get github.com/xssnick/tonutils-go/adnl
go get github.com/xssnick/tonutils-go/address
```




## ⚙ 设置您的环境

为了创建一个 TypeScript 项目，必须按照以下步骤进行操作：

1. 创建一个空文件夹（我们将其命名为 WalletsTutorial）。
2. 使用 CLI 打开项目文件夹。
3. 使用以下命令来设置项目：

```bash
npm init -y
npm install typescript @types/node ts-node nodemon --save-dev
npx tsc --init --rootDir src --outDir build \ --esModuleInterop --target es2020 --resolveJsonModule --lib es6 \ --module commonjs --allowJs true --noImplicitAny false --allowSyntheticDefaultImports true --strict false
```

:::info
为了帮助我们完成下一个流程，我们使用了 `ts-node` 来直接执行 TypeScript 代码，而无需预编译。当检测到目录中的文件更改时，`nodemon` 会自动重新启动节点应用程序。
:::

```json
  "files": [
    "\\",
    "\\"
  ]
```

5. 然后，在项目根目录中创建 `nodemon.json` 配置文件，内容如下：

```json
{
  "watch": ["src"],
  "ext": ".ts,.js",
  "ignore": [],
  "exec": "npx ts-node ./src/index.ts"
}
```

6. 在 `package.json` 中添加以下脚本到 "test" 脚本的位置：

```json
"start:dev": "npx nodemon"
```

7. 在项目根目录中创建 `src` 文件夹，然后在该文件夹中创建 `index.ts` 文件。
8. 接下来，添加以下代码：

```ts
async function main() {
  console.log("Hello, TON!");
}

main().finally(() => console.log("Exiting..."));
```

9. 使用终端运行以下代码：

```bash
npm run start:dev
```

10. 最后，控制台将输出以下内容。

![](/img/docs/how-to-wallet/wallet_1.png)

:::tip Blueprint
TON 社区创建了一个优秀的工具来自动化所有开发过程（部署、合约编写、测试）称为 [Blueprint](https://github.com/ton-org/blueprint)。然而，我们在本教程中不需要这么强大的工具，所以建议遵循上述说明。
:::

**可选:** 当使用 Golang 时，请按照以下说明进行操作：

1. 安装 GoLand IDE。
2. 使用以下内容创建项目文件夹和 `go.mod` 文件（如果使用的当前版本已过时，则可能需要更改 Go 版本）：

```
module main

go 1.20
```

3. 在终端中输入以下命令：

```bash
go get github.com/xssnick/tonutils-go
```

4. 在项目根目录中创建 `main.go` 文件，内容如下：

```go
package main

import (
	"log"
)

func main() {
	log.Println("Hello, TON!")
}
```

5. 将 `go.mod` 中的模块名称更改为 `main`。
6. 运行上述代码，直到在终端中显示输出。

:::info
也可以使用其他 IDE，因为 GoLand 不是免费的，但建议使用 GoLand。
:::

:::warning 注意

另外，下面的每个新部分将指定每个新部分所需的特定代码部分，并且需要将新的导入与旧导入合并起来。\
:::

## 🚀 让我们开始！

在本教程中，我们将学习在 TON 区块链上最常使用的钱包（版本 3 和 4），并了解它们的智能合约是如何工作的。这将使开发人员更好地理解 TON 平台上的不同类型的交易，以便更简单地创建交易、将其发送到区块链、部署钱包，并最终能够处理高负载的钱包。

我们的主要任务是使用 @ton/ton、@ton/core、@ton/crypto 的各种对象和函数构建交易，以了解大规模交易是怎样的。为了完成这个过程，我们将使用两个主要的钱包版本（v3 和 v4），因为交易所、非托管钱包和大多数用户仅使用这些特定版本。

:::note
There may be occasions in this tutorial when there is no explanation for particular details. In these cases, more details will be provided in later stages of this tutorial.

**重要:** 在本教程中，我们使用了 [wallet v3 代码](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet3-code.fc) 来更好地理解钱包开发过程。需要注意的是，v3 版本有两个子版本：r1 和 r2。目前，只使用第二个版本，这意味着当我们在本文档中提到 v3 时，它指的是 v3r2。
:::

## 💎 TON 区块链钱包

在 TON 区块链上运行的所有钱包实际上都是智能合约，与 TON 上的一切都是智能合约的方式相同。与大多数区块链一样，可以在网络上部署智能合约并根据不同的用途自定义它们。由于这个特性，**完全自定义的钱包是可能的**。
在 TON 上，钱包智能合约帮助平台与其他智能合约类型进行通信。然而，重要的是要考虑钱包通信是如何进行的。

### 钱包通信

通常，在 TON 区块链上有两种交易类型：`internal` 和 `external`。外部交易允许从外部世界向区块链发送消息，从而与接受此类交易的智能合约进行通信。负责执行此过程的函数如下：

```func
() recv_external(slice in_msg) impure {
    ;; 一些代码
}
```

在我们深入研究钱包之前，让我们先看看钱包如何接受外部交易。在 TON 上，所有钱包都持有所有者的 `公钥`、`seqno` 和 `subwallet_id`。接收到外部交易时，钱包使用 `get_data()` 方法从钱包的存储部分中检索数据。然后进行多个验证流程，并决定是否接受此交易。这个过程的完成如下：

```func
() recv_external(slice in_msg) impure {
  var signature = in_msg~load_bits(512); ;; 从消息体中获取签名
  var cs = in_msg;
  var (subwallet_id, valid_until, msg_seqno) = (cs~load_uint(32), cs~load_uint(32), cs~load_uint(32));  ;; 从消息体中获取其他值
  throw_if(35, valid_until <= now()); ;; 检查交易的有效性
  var ds = get_data().begin_parse(); ;; 从存储获取数据并将其转换为可读取值的切片
  var (stored_seqno, stored_subwallet, public_key) = (ds~load_uint(32), ds~load_uint(32), ds~load_uint(256)); ;; 从存储中读取值
  ds.end_parse(); ;; 确保变量 ds 中没有任何数据
  throw_unless(33, msg_seqno == stored_seqno);
  throw_unless(34, subwallet_id == stored_subwallet);
  throw_unless(35, check_signature(slice_hash(in_msg), signature, public_key));
  accept_message();
```

> 💡 有用的链接:
>
> [“load_bits()（文档）](/develop/func/stdlib/#load_bits)
>
> [“get_data()（文档）](/develop/func/stdlib/#load_bits)
>
> [“begin_parse()（文档）](/develop/func/stdlib/#load_bits)
>
> [“end_parse()（文档）](/develop/func/stdlib/#end_parse)
>
> [“load_int()（文档）](/develop/func/stdlib/#load_int)
>
> [“load_uint()（文档）](/develop/func/stdlib/#load_int)
>
> [“check_signature()（文档）](/develop/func/stdlib/#check_signature)
>
> [“slice_hash()（文档）](/develop/func/stdlib/#slice_hash)
>
> [“accept_message()（文档）](/develop/func/stdlib/#accept_message)

接下来，我们来详细看一下。

### 重放保护 - Seqno

钱包智能合约中的交易重放保护与交易 seqno（序列号）直接相关，它跟踪哪些交易以什么顺序发送。不能重复发送钱包中的单个交易非常重要，因为这会完全破坏系统的完整性。如果进一步检查智能合约代码，通常会处理 `seqno` 如下：

```func
throw_unless(33, msg_seqno == stored_seqno);
```

上述代码将检查在交易中获得的 `seqno` 是否与存储在智能合约中的 `seqno` 相匹配。如果不匹配，则合约返回带有 `33 exit code` 的错误。因此，如果发送者传递了无效的 `seqno`，则意味着他在交易序列中犯了一些错误，合约保护了这些情况。

:::note
还需要确认外部消息可以由任何人发送。这意味着如果您向某人发送 1 TON，其他人也可以重复该消息。但是，当 seqno 增加时，以前的外部消息失效，并且没有人可以重复该消息，从而防止窃取您的资金。
:::

### 签名

如前所述，钱包智能合约接受外部交易。然而，这些交易来自外部世界，这些数据不能 100% 可信。因此，每个钱包都存储所有者的公钥。当钱包接收到所有者使用私钥签名的外部交易时，智能合约使用公钥验证交易签名的合法性。这样可以验证交易实际上是来自合约所有者的。

要执行此过程，首先钱包需要从传入消息中获取签名，从存储中加载公钥，并使用以下过程验证签名：

```func
var signature = in_msg~load_bits(512);
var ds = get_data().begin_parse();
var (stored_seqno, stored_subwallet, public_key) = (ds~load_uint(32), ds~load_uint(32), ds~load_uint(256));
throw_unless(35, check_signature(slice_hash(in_msg), signature, public_key));
```

如果所有验证流程都顺利完成，智能合约接受消息并对其进行处理：

```func
accept_message();
```

:::info accept_message()
由于交易来自外部世界，它不包含支付交易费用所需的 Toncoin。在使用 accept_message() 函数发送 TON 时，应用gas_credit（在写入时其值为10,000 gas单位），并且只要gas不超过 gas_credit 值，就允许免费进行必要的计算。使用 accept_message() 函数后，从智能合约的账户余额中收取所有已花费的gas（以 TON 计）。可以在[此处](/develop/smart-contracts/guidelines/accept)了解有关此过程的更多信息。
:::

### 交易过期

用于检查外部交易的有效性的另一步是 `valid_until` 字段。从变量名称可以看出，这是交易在 UNIX 中在有效之前的时间。如果此验证过程失败，则合约完成交易处理并返回 32 退出码，如下所示：

```func
var (subwallet_id, valid_until, msg_seqno) = (cs~load_uint(32), cs~load_uint(32), cs~load_uint(32));
throw_if(35, valid_until <= now());
```

此算法用于在交易不再有效但仍然以未知原因发送到区块链时，防范各种错误的易受攻击性。

### 钱包 v3 和钱包 v4 的区别

钱包 v3 和钱包 v4 之间的唯一区别是钱包 v4 使用可以安装和删除的 `插件`。插件是特殊的智能合约，可以从钱包智能合约请求在特定时间从指定数量的 TON 中。钱包智能合约将相应地发送所需数量的 TON，而无需所有者参与。这类似于为插件创建的 **订阅模型**。我们不会在本教程中详细介绍这些细节，因为这超出了本教程的范围。

Wallet smart contracts, in turn, will send the required amount of TON in response without the need for the owner to participate. This is similar to the **subscription model** for which plugins are created. We will not learn these details, because this is out of the scope of this tutorial.

### How Wallets facilitate communication with Smart Contracts

As we discussed earlier, a wallet smart contract accepts external transactions, validates them and accepts them if all checks are passed. The contract then starts the loop of retrieving messages from the body of external messages then creates internal messages and sends them to the blockchain as follows:

```func
cs~touch();
while (cs.slice_refs()) {
    var mode = cs~load_uint(8); ;; load transaction mode
    send_raw_message(cs~load_ref(), mode); ;; get each new internal message as a cell with the help of load_ref() and send it
}
```

:::tip touch()
On TON, all smart contracts run on the stack-based TON Virtual Machine (TVM). ~ touch() places the variable `cs` on top of the stack to optimize the running of code for less gas.
:::

Since a **maximum of 4 references** can be stored in one cell, we can send a maximum of 4 internal messages per external message.

> 💡 Useful links:
>
> ["slice_refs()" in docs](/develop/func/stdlib/#slice_refs)
>
> ["send_raw_message() and transaction modes" in docs](/develop/func/stdlib/#send_raw_message)
>
> ["load_ref()" in docs](/develop/func/stdlib/#load_ref)

## 📬  External and Internal Transactions

为了完成此过程，需要使用一个预先制作的钱包使任务变得更容易。为此：

To carry out this process it is necessary to make use of a ready-made wallet to make the task easier. To accomplish this:

1. Install the [wallet app](/participate/wallets/apps) (e.g., Tonkeeper is used by the author)
2. Switch wallet app to v3r2 address version
3. Deposit 1 TON into the wallet
4. Send the transaction to another address (you can send to yourself, to the same wallet).

This way, the Tonkeeper wallet app will deploy the wallet contract and we can use it for the following steps.

:::note
At the time of writing, most wallet apps on TON by default use the wallet v4 version. Plugins are not required in this tutorial and we’ll make use of the functionality provided by wallet v3. During use, Tonkeeper allows the user to choose the version of the wallet they want. Therefore, it is recommended to deploy wallet version 3 (wallet v3).
:::

### TL-B

在本节中，我们将详细研究 [block.tlb](https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb)。在将来的开发中，此文件将非常有用，因为它描述了不同cell的组装方式。在我们的情况下，它详细描述了内部和外部交易的复杂性。

In this section, we’ll examine [block.tlb](https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb). This file will be very useful during future development, as it describes how different cells should be assembled. In our case specifically, it details the intricacies of internal and external transactions.

:::info
Basic information will be provided within this guide. For further details, please refer to our TL-B [documentation](/develop/data-formats/tl-b-language) to learn more about TL-B.
:::

### CommonMsgInfo

通过阅读 `block.tlb` 文件，我们可以注意到 CommonMsgInfo有三种不同的类型：`int_msg_info$0`、`ext_in_msg_info$10`、`ext_out_msg_info$11`。我们将不对 `ext_out_msg_info` 的 TL-B 结构的具体细节进行详细解释。但需要注意的是，它是由智能合约发送的外部交易类型，用作外部日志。要查看此格式的示例，请仔细查看 [Elector](https://tonscan.org/address/Ef8zMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM0vF) 合约。

您可以从 [TL-B](https://github.com/ton-blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L127-L128) 中看到，**仅在与 ext_in_msg_info 类型一起使用时才可以使用 CommonMsgInfo**。因为交易类型字段，如 `src`、`created_lt`、`created_at` 等，由验证者在交易处理期间进行重写。在这种情况下，`src` 交易类型最重要，因为当发送交易时，发送者是未知的，验证者在验证期间对其在 `src` 字段中的地址进行重写。这样确保 `src` 字段中的地址是正确的，并且不能被操纵。

但是，`CommonMsgInfo` 结构仅支持 `MsgAddress` 规格，但通常情况下发送方的地址是未知的，并且需要写入 `addr_none`（两个零位 `00`）。在这种情况下，使用 `CommonMsgInfoRelaxed` 结构，该结构支持 `addr_none` 地址。对于 `ext_in_msg_info`（用于传入的外部消息），使用 `CommonMsgInfo` 结构，因为这些消息类型不使用sender，始终使用 [MsgAddressExt](https://hub.com/ton/ton.blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L100) 结构（`addr_none$00` 表示两个零位），因此无需覆盖数据。

However, the `CommonMsgInfo` structure only supports the `MsgAddress` specification, but the sender’s address is typically unknown and it is required to write the `addr_none` (two zero bits `00`). In this case, the `CommonMsgInfoRelaxed` structure is used, which supports the `addr_none` address. For the `ext_in_msg_info` (used for incoming external messages), the `CommonMsgInfo` structure is used because these message types don’t make use of a sender and always use the [MsgAddressExt](https://hub.com/ton/ton.blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L100) structure (the `addr_none$00` meaning two zero bits), which means there is no need to overwrite the data.

:::note
The numbers after `$` symbol are the bits that are required to store at the beginning of a certain structure, for further identification of these structures during reading (deserialization).
:::

### Internal Transaction Creation

Internal transactions are used to send messages between contracts. When analyzing various contract types (such as [NFTs](https://github.com/ton-blockchain/token-contract/blob/f2253cb0f0e1ae0974d7dc0cef3a62cb6e19f806/nft/nft-item.fc#L51-L56) and [Jetons](https://github.com/ton-blockchain/token-contract/blob/f2253cb0f0e1ae0974d7dc0cef3a62cb6e19f806/ft/jetton-wallet.fc#L139-L144)) that send messages where the writing of contracts is considered, the following lines of code are often used:

```func
var msg = begin_cell()
  .store_uint(0x18, 6) ;; or 0x10 for non-bounce
  .store_slice(to_address)
  .store_coins(amount)
  .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; default message headers (see sending messages page)
  ;; store something as a body
```

Let’s first consider `0x18` and `0x10` (x - hexadecimal), which are hexadecimal numbers laid out in the following manner (given that we allocate 6 bits): `011000` and `010000`. This means that the code above can be overwritten as follows:

```func
var msg = begin_cell()
  .store_uint(0, 1) ;; this bit indicates that we send an internal message according to int_msg_info$0  
  .store_uint(1, 1) ;; IHR Disabled
  .store_uint(1, 1) ;; or .store_uint(0, 1) for 0x10 | bounce
  .store_uint(0, 1) ;; bounced
  .store_uint(0, 2) ;; src -> two zero bits for addr_none
  .store_slice(to_address)
  .store_coins(amount)
  .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; default message headers (see sending messages page)
  ;; store something as a body
```

Now let’s go through each option in detail:

|    Option    |                                                                                                                                                                                                                                                                           Explanation                                                                                                                                                                                                                                                                          |
| :----------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| IHR Disabled |                               Currently, this option is disabled (which means we store 1) because Instant Hypercube Routing is not fully implemented. In addition, this will be needed when a large number of [Shardchains](/learn/overviews/ton-blockchain#many-accountchains-shards) are live on the network. More can be read about the IHR Disabled option in the [tblkch.pdf](https://ton.org/tblkch.pdf) (chapter 2).                              |
|    Bounce    | While sending transactions, a variety of errors can occur during smart contract processing. To avoid losing TON, it is necessary to set the Bounce option to 1 (true). In this case, if any contract errors occur during transaction processing, the transaction will be returned to the sender, and the same amount of TON will be received minus fees. More can be read about non-bounceable messages [here](/develop/smart-contracts/guidelines/non-bouncable-messages). |
|    Bounced   |                                                                                                                                                Bounced transactions are transactions that are returned to the sender because an error occurred while processing the transaction with a smart contract. This option tells you whether the transaction received is bounced or not.                                                                                                                                               |
|      Src     |                                                                                                                                                                                                           The Src is the sender address. In this case, two zero bits are written to indicate the `addr_none` address.                                                                                                                                                                                                          |

The next two lines of code:

```func
...
.store_slice(to_address)
.store_coins(amount)
...
```

- we specify the recipient and the number of TON to be sent.

Finally, let’s look at the remaining lines of code:

```func
...
  .store_uint(0, 1) ;; Extra currency
  .store_uint(0, 4) ;; IHR fee
  .store_uint(0, 4) ;; Forwarding fee
  .store_uint(0, 64) ;; Logical time of creation
  .store_uint(0, 32) ;; UNIX time of creation
  .store_uint(0, 1) ;; State Init
  .store_uint(0, 1) ;; Message body
  ;; store something as a body
```

|          Option          |                                                                                                                                                                                        Explanation                                                                                                                                                                                        |
| :----------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|      Extra currency      |                                                                                                                                              This is a native implementation of existing jettons and is not currently in use.                                                                                                                                             |
|          IHR fee         |                                                             As mentioned, the IHR is not currently in use, so this fee is always zero. More can be read about this in the [tblkch.pdf](https://ton.org/tblkch.pdf) (3.1.8).                                                            |
|      Forwarding fee      |                                                                                                         A forwarding message fee. More can be read about this in the [fees documentation](/develop/howto/fees-low-level#transactions-and-phases).                                                                                                         |
| Logical time of creation |                                                                                                                                                           The time used to create the correct transaction queue.                                                                                                                                                          |
|   UNIX tome of creation  |                                                                                                                                                               The time the transaction was created in UNIX.                                                                                                                                                               |
|        State Init        |     Code and source data for deploying a smart contract. If the bit is set to `0`, it means that we do not have a State Init. But if it is set to `1`, then another bit needs to be written which indicates whether the State Init is stored in the same cell (0) or written as a reference (1).    |
|       Message body       | This part defines how the message body is stored. At times the message body is too large to fit into the message itself. In this case, it should be stored as a **reference** whereby the bit is set to `1` to show that the body is used as a reference. If the bit is `0`, the body is in the same cell as the message. |

接下来，我们将开始准备一个交易，该交易将向另一个钱包 v3 发送 Toncoins。首先，假设用户想要向自己发送 0.5 TON，并附带文本“**你好，TON！**”，请参阅本文档的这一部分来了解[如何发送带有评论的消息](/develop/func/cookbook#how-to-send-a-simple-message)。

:::note
If the number value fits within fewer bits than is specified, then the missing zeros are added to the left side of the value. For example, 0x18 fits within 5 bits -> `11000`. However, since 6 bits were specified, the end result becomes `011000`.
:::

Next, we’ll begin preparing a transaction, which will be sent Toncoins to another wallet v3.
First, let’s say a user wants to send 0.5 TON to themselves with the text "**Hello, TON!**", refer to this section of our documentation to learn ([How to send message with a comment](/develop/func/cookbook#how-to-send-a-simple-message)).

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
	"github.com/xssnick/tonutils-go/tvm/cell"
)

internalMessageBody := cell.BeginCell().
  MustStoreUInt(0, 32). // 写入 32 个零位以指示接下来将有文本注释
  MustStoreStringSnake("你好，TON！"). // 写入我们的文本注释
  EndCell()
```


<TabItem value="go" label="Golang">

```go
import (
	"github.com/xssnick/tonutils-go/tvm/cell"
)

internalMessageBody := cell.BeginCell().
  MustStoreUInt(0, 32). // write 32 zero bits to indicate that a text comment will follow
  MustStoreStringSnake("Hello, TON!"). // write our text comment
  EndCell()
```




Above we created an `InternalMessageBody` in which the body of our message is stored. Note that when storing text that does not fit into a single Cell (1023 bits), it is necessary **to split the data into several cells** according to [the following documentation](/develop/smart-contracts/guidelines/internal-messages). However, in this case the high-level libraries creates cells according to requirements, so at this stage there is no need to worry about it.

Next, the `InternalMessage` is created according to the information we have studied earlier as follows:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/tlb"
)

walletAddress := address.MustParseAddr("把你的钱包地址放这里")

internalMessage := cell.BeginCell().
  MustStoreUInt(0, 1). // 表示它是一条内部消息 -> int_msg_info$0
  MustStoreBoolBit(true). // 禁用 IHR
  MustStoreBoolBit(true). // bounce
  MustStoreBoolBit(false). // bounced
  MustStoreUInt(0, 2). // src -> addr_none
  MustStoreAddr(walletAddress).
  MustStoreCoins(tlb.MustFromTON("0.2").NanoTON().Uint64()). // 数量
  MustStoreBoolBit(false). // Extra 货币
  MustStoreCoins(0). // IHR 费用
  MustStoreCoins(0). // Forwarding 费用
  MustStoreUInt(0, 64). // 创建的逻辑时间
  MustStoreUInt(0, 32). // 创建的 UNIX 时间
  MustStoreBoolBit(false). // 没有 State Init
  MustStoreBoolBit(true). // 我们将 Message Body 存储为引用
  MustStoreRef(internalMessageBody). // 将 Message Body 存储为引用
  EndCell()
```


<TabItem value="go" label="Golang">

```go
import (
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/tlb"
)

walletAddress := address.MustParseAddr("put your address")

internalMessage := cell.BeginCell().
  MustStoreUInt(0, 1). // indicate that it is an internal message -> int_msg_info$0
  MustStoreBoolBit(true). // IHR Disabled
  MustStoreBoolBit(true). // bounce
  MustStoreBoolBit(false). // bounced
  MustStoreUInt(0, 2). // src -> addr_none
  MustStoreAddr(walletAddress).
  MustStoreCoins(tlb.MustFromTON("0.2").NanoTON().Uint64()).   // amount
  MustStoreBoolBit(false). // Extra currency
  MustStoreCoins(0). // IHR Fee
  MustStoreCoins(0). // Forwarding Fee
  MustStoreUInt(0, 64). // Logical time of creation
  MustStoreUInt(0, 32). // UNIX time of creation
  MustStoreBoolBit(false). // No State Init
  MustStoreBoolBit(true). // We store Message Body as a reference
  MustStoreRef(internalMessageBody). // Store Message Body as a reference
  EndCell()
```




### Creating a Message

It is necessary to retrieve the `seqno` (sequence number) of our wallet smart contract. To accomplish this, a `Client` is created which will be used to send a request to run the Get method "seqno" of our wallet. It is also necessary to add a seed phrase (which you saved during creating a wallet [here](#--external-and-internal-transactions)) to sign our transaction via the following steps:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "context"
  "crypto/ed25519"
  "crypto/hmac"
  "crypto/sha512"
  "github.com/xssnick/tonutils-go/liteclient"
  "github.com/xssnick/tonutils-go/ton"
  "golang.org/x/crypto/pbkdf2"
  "log"
  "strings"
)

mnemonic := strings.Split("put your mnemonic", " ") // get our mnemonic as array

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection) // create client

block, err := client.CurrentMasterchainInfo(context.Background()) // get current block, we will need it in requests to LiteServer
if err != nil {
  log.Fatalln("CurrentMasterchainInfo err:", err.Error())
  return
}

getMethodResult, err := client.RunGetMethod(context.Background(), block, walletAddress, "seqno") // run "seqno" GET method from your wallet contract
if err != nil {
  log.Fatalln("RunGetMethod err:", err.Error())
  return
}
seqno := getMethodResult.MustInt(0) // get seqno from response

// The next three lines will extract the private key using the mnemonic phrase. We will not go into cryptographic details. With the tonutils-go library, this is all implemented, but we’re doing it again to get a full understanding.
mac := hmac.New(sha512.New, []byte(strings.Join(mnemonic, " ")))
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // In TON libraries "TON default seed" is used as salt when getting keys

privateKey := ed25519.NewKeyFromSeed(k)
```


<TabItem value="go" label="Golang">

```go
import (
  "context"
  "crypto/ed25519"
  "crypto/hmac"
  "crypto/sha512"
  "github.com/xssnick/tonutils-go/liteclient"
  "github.com/xssnick/tonutils-go/ton"
  "golang.org/x/crypto/pbkdf2"
  "log"
  "strings"
)

mnemonic := strings.Split("put your mnemonic", " ") // get our mnemonic as array

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection) // create client

block, err := client.CurrentMasterchainInfo(context.Background()) // get current block, we will need it in requests to LiteServer
if err != nil {
  log.Fatalln("CurrentMasterchainInfo err:", err.Error())
  return
}

getMethodResult, err := client.RunGetMethod(context.Background(), block, walletAddress, "seqno") // run "seqno" GET method from your wallet contract
if err != nil {
  log.Fatalln("RunGetMethod err:", err.Error())
  return
}
seqno := getMethodResult.MustInt(0) // get seqno from response

// The next three lines will extract the private key using the mnemonic phrase. We will not go into cryptographic details. With the tonutils-go library, this is all implemented, but we’re doing it again to get a full understanding.
mac := hmac.New(sha512.New, []byte(strings.Join(mnemonic, " ")))
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // In TON libraries "TON default seed" is used as salt when getting keys

privateKey := ed25519.NewKeyFromSeed(k)
```




Therefore, the `seqno`, `keys`, and `internal message` need to be sent. Now we need to create a [message](/develop/smart-contracts/messages) for our wallet and store the data in this message in the sequence used at the beginning of the tutorial. This is accomplished as follows:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "time"
)

toSign := cell.BeginCell().
  MustStoreUInt(698983191, 32). // subwallet_id | We consider this further
  MustStoreUInt(uint64(time.Now().UTC().Unix()+60), 32). // Transaction expiration time, +60 = 1 minute
  MustStoreUInt(seqno.Uint64(), 32). // store seqno
  MustStoreUInt(3, 8). // store mode of our internal transaction
  MustStoreRef(internalMessage) // store our internalMessage as a reference

signature := ed25519.Sign(privateKey, toSign.EndCell().Hash()) // get the hash of our message to wallet smart contract and sign it to get signature

body := cell.BeginCell().
  MustStoreSlice(signature, 512). // store signature
  MustStoreBuilder(toSign). // store our message
  EndCell()
```


<TabItem value="go" label="Golang">

```go
import (
  "time"
)

toSign := cell.BeginCell().
  MustStoreUInt(698983191, 32). // subwallet_id | We consider this further
  MustStoreUInt(uint64(time.Now().UTC().Unix()+60), 32). // Transaction expiration time, +60 = 1 minute
  MustStoreUInt(seqno.Uint64(), 32). // store seqno
  MustStoreUInt(uint64(3), 8). // store mode of our internal transaction
  MustStoreRef(internalMessage) // store our internalMessage as a reference

signature := ed25519.Sign(privateKey, toSign.EndCell().Hash()) // get the hash of our message to wallet smart contract and sign it to get signature

body := cell.BeginCell().
  MustStoreSlice(signature, 512). // store signature
  MustStoreBuilder(toSign). // store our message
  EndCell()
```




Note that here no `.endCell()` was used in the definition of the `toSign`. The fact is that in this case it is necessary **to transfer toSign content directly to the message body**. If writing a cell was required, it would have to be stored as a reference.

:::tip Wallet V4
In addition to basic verification process we learned bellow for the Wallet V3, Wallet V4 smart contracts [extracts the opcode to determine whether a simple translation or a transaction associated with the plugin](https://github.com/ton-blockchain/wallet-contract/blob/4111fd9e3313ec17d99ca9b5b1656445b5b49d8f/func/wallet-v4-code.fc#L94-L100) is required. To match this version, it is necessary to add the `storeUint(0, 8).` (JS/TS), `MustStoreUInt(0, 8).` (Golang) functions after writing the seqno (sequence number) and before specifying the transaction mode.
:::

### External Transaction Creation

To deliver any internal message to a blockchain from the outside world, it is necessary to send it within an external transaction. As we have previously considered, it is necessary to only make use of the `ext_in_msg_info$10` structure, as the goal is to send an external message to our contract. Now, let's create an external message that will be sent to our wallet:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
externalMessage := cell.BeginCell().
  MustStoreUInt(0b10, 2). // 0b10 -> 10 in binary
  MustStoreUInt(0, 2). // src -> addr_none
  MustStoreAddr(walletAddress). // Destination address
  MustStoreCoins(0). // Import Fee
  MustStoreBoolBit(false). // No State Init
  MustStoreBoolBit(true). // We store Message Body as a reference
  MustStoreRef(body). // Store Message Body as a reference
  EndCell()
```


<TabItem value="go" label="Golang">

```go
externalMessage := cell.BeginCell().
  MustStoreUInt(0b10, 2). // 0b10 -> 10 in binary
  MustStoreUInt(0, 2). // src -> addr_none
  MustStoreAddr(walletAddress). // Destination address
  MustStoreCoins(0). // Import Fee
  MustStoreBoolBit(false). // No State Init
  MustStoreBoolBit(true). // We store Message Body as a reference
  MustStoreRef(body). // Store Message Body as a reference
  EndCell()
```




|    Option    |                                                                                                                                                          Explanation                                                                                                                                                          |
| :----------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|      Src     | The sender address. Since an incoming external message cannot have a sender, there will always be 2 zero bits (an addr_none [TL-B](https://github.com/ton-blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L100)). |
|  Import Fee  |                                                                                                                         The fee used to pay for importing incoming external messages.                                                                                                                         |
|  State Init  |                             Unlike the Internal Message, the State Init within the external message is needed **to deploy a contract from the outside world**. The State Init used in conjunction with the Internal Message allows one contract to deploy another.                            |
| Message Body |                                                                                                                         The message that must be sent to the contract for processing.                                                                                                                         |

:::tip 0b10
0b10 (b - binary) denotes a binary record. In this process, two bits are stored: `1` and `0`. Thus we specify that it's `ext_in_msg_info$10`.
:::

Now we have a completed message that is ready to be sent to our contract. To accomplish this, it should first be serialized to a `BOC` ([Bag of Cells](/develop/data-formats/cell-boc#bag-of-cells)), then be sent using the following code:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "encoding/base64"
  "github.com/xssnick/tonutils-go/tl"
)

log.Println(base64.StdEncoding.EncodeToString(externalMessage.ToBOCWithFlags(false)))

var resp tl.Serializable
err = client.Client().QueryLiteserver(context.Background(), ton.SendMessage{Body: externalMessage.ToBOCWithFlags(false)}, &resp)

if err != nil {
  log.Fatalln(err.Error())
  return
}
```


<TabItem value="go" label="Golang">

```go
import (
  "encoding/base64"
  "github.com/xssnick/tonutils-go/tl"
)

log.Println(base64.StdEncoding.EncodeToString(externalMessage.ToBOCWithFlags(false)))

var resp tl.Serializable
err = client.Client().QueryLiteserver(context.Background(), ton.SendMessage{Body: externalMessage.ToBOCWithFlags(false)}, &resp)

if err != nil {
  log.Fatalln(err.Error())
  return
}
```




> 💡 Useful link:
>
> [More about Bag of Cells](/develop/data-formats/cell-boc#bag-of-cells)

我们已经学会了创建消息的基础知识，这对于部署钱包非常有帮助。 以前，我们通过钱包应用程序部署钱包，但在这种情况下，我们将需要手动部署钱包。

## 👛 Deploying a Wallet

We have learned the basics of creating messages, which will now be helpful for deploying the wallet. In the past, we have deployed wallet via wallet app, but in this case we’ll need to deploy our wallet manually.

正确定义钱包所需的第一件事是检索`private`和`public`密钥。为了完成这个任务，需要生成助记词种子短语，然后使用加密库提取私钥和公钥。

### Generating a Mnemonic

The first thing needed to correctly create a wallet is to retrieve a `private` and `public` key. To accomplish this task it is necessary to generate a mnemonic seed phrase and then extract private and public keys using cryptographic libraries.

This is accomplished as follows:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
	"crypto/ed25519"
	"crypto/hmac"
	"crypto/sha512"
	"log"
	"github.com/xssnick/tonutils-go/ton/wallet"
	"golang.org/x/crypto/pbkdf2"
	"strings"
)

// mnemonic := strings.Split("put your mnemonic", " ") // get our mnemonic as array
mnemonic := wallet.NewSeed() // get new mnemonic

// The following three lines will extract the private key using the mnemonic phrase. We will not go into cryptographic details. It has all been implemented in the tonutils-go library, but it immediately returns the finished object of the wallet with the address and ready methods. So we’ll have to write the lines to get the key separately. Goland IDE will automatically import all required libraries (crypto, pbkdf2 and others).
mac := hmac.New(sha512.New, []byte(strings.Join(mnemonic, " "))) 
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // In TON libraries "TON default seed" is used as salt when getting keys
// 32 is a key len 

privateKey := ed25519.NewKeyFromSeed(k) // get private key
publicKey := privateKey.Public().(ed25519.PublicKey) // get public key from private key
log.Println(publicKey) // print publicKey so that at this stage the compiler does not complain that we do not use our variable
log.Println(mnemonic) // if we want, we can print our mnemonic
```


<TabItem value="go" label="Golang">

```go
import (
	"crypto/ed25519"
	"crypto/hmac"
	"crypto/sha512"
	"log"
	"github.com/xssnick/tonutils-go/ton/wallet"
	"golang.org/x/crypto/pbkdf2"
	"strings"
)

// mnemonic := strings.Split("put your mnemonic", " ") // get our mnemonic as array
mnemonic := wallet.NewSeed() // get new mnemonic

// The following three lines will extract the private key using the mnemonic phrase. We will not go into cryptographic details. It has all been implemented in the tonutils-go library, but it immediately returns the finished object of the wallet with the address and ready methods. So we’ll have to write the lines to get the key separately. Goland IDE will automatically import all required libraries (crypto, pbkdf2 and others).
mac := hmac.New(sha512.New, []byte(strings.Join(mnemonic, " "))) 
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // In TON libraries "TON default seed" is used as salt when getting keys
// 32 is a key len 

privateKey := ed25519.NewKeyFromSeed(k) // get private key
publicKey := privateKey.Public().(ed25519.PublicKey) // get public key from private key
log.Println(publicKey) // print publicKey so that at this stage the compiler does not complain that we do not use our variable
log.Println(mnemonic) // if we want, we can print our mnemonic
```




The private key is needed to sign transactions and the public key is stored in the wallet’s smart contract.

:::danger IMPORTANT
It is necessary to output the generated mnemonic seed phrase to the console then save and use it (as detailed in the previous section) in order to use the same key pair each time the wallet’s code is run.
:::

### Subwallet IDs

根据TON区块链的源代码中的[代码行](https://github.com/ton-blockchain/ton/blob/4b940f8bad9c2d3bf44f196f6995963c7cee9cc3/tonlib/tonlib/TonlibClient.cpp#L2420)，默认的`subwallet_id`值为`698983191`：

By changing just one bit within the stateInit, a different address can be generated. That is why the `subwallet_id` was initially created. The  `subwallet_id` is stored in the contract storage and it can be used to create many different wallets (with different subwallet IDs) with one private key. This functionality can be very useful when integrating various wallet types with centralized service such as exchanges.

可以从[配置文件](https://ton.org/global-config.json)中获取创世块信息（zero_state）。了解其复杂性和细节并非必要，但重要的是要记住`subwallet_id`的默认值为`698983191`。

```cpp
res.wallet_id = td::as<td::uint32>(res.config.zero_state_id.root_hash.as_slice().data());
```

It is possible to retrieve genesis block information (zero_state) from the [configuration file](https://ton.org/global-config.json). Understanding the complexities and details of this is not necessary but it's important to remember that the default value of the `subwallet_id` is `698983191`.

我们需要将以上的值添加到合约的初始数据中，所以变量需要保存如下：

```func
var (subwallet_id, valid_until, msg_seqno) = (cs~load_uint(32), cs~load_uint(32), cs~load_uint(32));
var (stored_seqno, stored_subwallet, public_key) = (ds~load_uint(32), ds~load_uint(32), ds~load_uint(256));
throw_unless(34, subwallet_id == stored_subwallet);
```

We will need to add the above value to the initial data of the contract, so the variable needs to be saved as follows:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
var subWallet uint64 = 698983191
```


<TabItem value="go" label="Golang">

```go
var subWallet uint64 = 698983191
```




### Compiling Wallet Code

Now that we have the private and public keys and the subwallet_id clearly defined we need to compile the wallet code. To accomplish this, we’ll use the [wallet v3 code](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet3-code.fc) from the official repository.

我们将仅使用JavaScript来编译代码，因为用于编译代码的库基于JavaScript。
但是，一旦编译完成，只要我们拥有编译后的cell的**base64输出**，就可以在其他编程语言（如Go等）中使用这些编译后的代码。

```bash
npm i --save @ton-community/func-js
```

现在，我们为我们正在创建的项目有了以下结构：

First, we need to create two files: `wallet_v3.fc` and `stdlib.fc`. The compiler works with the stdlib.fc library. All necessary and basic functions, which correspond with the `asm` instructions were created in the library. The stdlib.fc file can be downloaded [here](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/stdlib.fc). In the  `wallet_v3.fc` file it is necessary to copy the code above.

Now we have the following structure for the project we are creating:

```
.
├── src/
│   ├── main.ts
│   ├── wallet_v3.fc
│   └── stdlib.fc
├── nodemon.json
├── package-lock.json
├── package.json
└── tsconfig.json
```

:::info
It’s fine if your IDE plugin conflicts with the `() set_seed(int) impure asm "SETRAND";` in the `stdlib.fc` file.
:::

现在，让我们编写代码来编译我们的智能合约并使用`npm run start:dev`来运行它：

```func
import { compileFunc } from '@ton-community/func-js';
import fs from 'fs'; // 我们使用fs来读取文件内容
import { Cell } from '@ton/core';

const result = await compileFunc({
  targets: ['wallet_v3.fc'], // 您的项目的目标
  sources: {
    "stdlib.fc": fs.readFileSync('./src/stdlib.fc', { encoding: 'utf-8' }),
    "wallet_v3.fc": fs.readFileSync('./src/wallet_v3.fc', { encoding: 'utf-8' }),
  }
});

if (result.status === 'error') {
  console.error(result.message)
  return;
}

const codeCell = Cell.fromBoc(Buffer.from(result.codeBoc, "base64"))[0]; // 从base64编码的BOC中获取缓冲区，并从该缓冲区获取cell

// 现在我们获得了包含编译代码的base64编码的BOC
console.log('Code BOC: ' + result.codeBoc);
console.log('\nHash: ' + codeCell.hash().toString('base64')); // 获取cell的哈希并将其转换为base64编码的字符串。我们将会在后面需要它
```

终端的输出结果如下：

```js
Code BOC: te6ccgEBCAEAhgABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQCW8oMI1xgg0x/TH9MfAvgju/Jj7UTQ0x/TH9P/0VEyuvKhUUS68qIE+QFUEFX5EPKj+ACTINdKltMH1AL7AOgwAaTIyx/LH8v/ye1UAATQMAIBSAYHABe7Oc7UTQ0z8x1wv/gAEbjJftRNDXCx+A==

Hash: idlku00WfSC36ujyK2JVT92sMBEpCNRUXOGO4sJVBPA=
```

完成后，可以使用其他库和语言使用我们的钱包代码检索相同的cell（使用base64编码的输出）：

```text
Code BOC: te6ccgEBCAEAhgABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQCW8oMI1xgg0x/TH9MfAvgju/Jj7UTQ0x/TH9P/0VEyuvKhUUS68qIE+QFUEFX5EPKj+ACTINdKltMH1AL7AOgwAaTIyx/LH8v/ye1UAATQMAIBSAYHABe7Oc7UTQ0z8x1wv/gAEbjJftRNDXCx+A==

Hash: idlku00WfSC36ujyK2JVT92sMBEpCNRUXOGO4sJVBPA=
```

Once this is completed it is possible to retrieve the same cell (using the base64 encoded output) with our wallet code using other libraries and languages:

<Tabs groupId="code-examples">
<TabItem value="go" label="Golang">

```go
import (
  "encoding/base64"
  "github.com/xssnick/tonutils-go/tvm/cell"
)

base64BOC := "te6ccgEBCAEAhgABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQCW8oMI1xgg0x/TH9MfAvgju/Jj7UTQ0x/TH9P/0VEyuvKhUUS68qIE+QFUEFX5EPKj+ACTINdKltMH1AL7AOgwAaTIyx/LH8v/ye1UAATQMAIBSAYHABe7Oc7UTQ0z8x1wv/gAEbjJftRNDXCx+A==" // save our base64 encoded output from compiler to variable
codeCellBytes, _ := base64.StdEncoding.DecodeString(base64BOC) // decode base64 in order to get byte array
codeCell, err := cell.FromBOC(codeCellBytes) // get cell with code from byte array
if err != nil { // check if there are any error
  panic(err) 
}

log.Println("Hash:", base64.StdEncoding.EncodeToString(codeCell.Hash())) // get the hash of our cell, encode it to base64 because it has []byte type and output to the terminal
```




完成上述过程后，确认我们的cell中正在使用正确的代码，因为哈希值相匹配。

```text
idlku00WfSC36ujyK2JVT92sMBEpCNRUXOGO4sJVBPA=
```

在构建交易之前，了解State Init非常重要。首先让我们了解[TL-B方案](https://github.com/ton-blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L141-L143)：

### Creating the State Init for Deployment

接下来我们将准备“初始数据”，这将在部署后立即出现在我们合约的存储中：

|              Option              |                                                                                                                                                                                                                                                           Explanation                                                                                                                                                                                                                                                          |
| :------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| split_depth |             This option is intended for highly loaded smart contracts that can be split and located on several [shardchains](/learn/overviews/ton-blockchain#many-accountchains-shards).  More information detailing how this works can be found in the [tblkch.pdf](https://ton.org/tblkch.pdf) (4.1.6).  Only a `0` bit is stored since it is being used only within a wallet smart contract.             |
|              special             | Used for TicTok. These smart contracts are automatically called for each block and are not needed for regular smart contracts. Information about this can be found in [this section](/develop/data-formats/transaction-layout#tick-tock) or in [tblkch.pdf](https://ton.org/tblkch.pdf) (4.1.6). Only a `0` bit is stored within this specification because we do not need such a function. |
|               code               |                                                                                                                                                                                                                      `1` bit means the presence of the smart contract code as a reference.                                                                                                                                                                                                                     |
|               data               |                                                                                                                                                                                                                      `1` bit means the presence of the smart contract data as a reference.                                                                                                                                                                                                                     |
|              library             |                                           A library that operates on the [masterchain](/learn/overviews/ton-blockchain#masterchain-blockchain-of-blockchains)  and can be used by different smart contracts. This will not be used for wallet, so its bit is set to `0`. Information about this can be found in [tblkch.pdf](https://ton.org/tblkch.pdf) (1.8.4).                                           |

Next we’ll prepare the `initial data`, which will be present in our contract’s storage immediately after deployment:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
dataCell := cell.BeginCell().
  MustStoreUInt(0, 32). // Seqno
  MustStoreUInt(698983191, 32). // Subwallet ID
  MustStoreSlice(publicKey, 256). // Public Key
  EndCell()
```


<TabItem value="go" label="Golang">

```go
dataCell := cell.BeginCell().
  MustStoreUInt(0, 32). // Seqno
  MustStoreUInt(698983191, 32). // Subwallet ID
  MustStoreSlice(publicKey, 256). // Public Key
  EndCell()
```




At this stage, both the contract `code` and its `initial data` is present. With this data, we can produce our **wallet address**. The address of the wallet depends on the State Init, which includes the code and initial data.

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "github.com/xssnick/tonutils-go/address"
)

stateInit := cell.BeginCell().
  MustStoreBoolBit(false). // 没有split_depth
  MustStoreBoolBit(false). // 没有special
  MustStoreBoolBit(true). // 表示有代码
  MustStoreRef(codeCell).
  MustStoreBoolBit(true). // 表示有数据
  MustStoreRef(dataCell).
  MustStoreBoolBit(false). // 没有library
  EndCell()

contractAddress := address.NewAddress(0, 0, stateInit.Hash()) // 获取stateInit的哈希，以获取我们的智能合约在`ID`为0的工作链中的地址
log.Println("Contract address:", contractAddress.String()) // 将智能合约地址输出到控制台
```


<TabItem value="go" label="Golang">

```go
import (
  "github.com/xssnick/tonutils-go/address"
)

stateInit := cell.BeginCell().
  MustStoreBoolBit(false). // No split_depth
  MustStoreBoolBit(false). // No special
  MustStoreBoolBit(true). // We have code
  MustStoreRef(codeCell).
  MustStoreBoolBit(true). // We have data
  MustStoreRef(dataCell).
  MustStoreBoolBit(false). // No library
  EndCell()

contractAddress := address.NewAddress(0, 0, stateInit.Hash()) // get the hash of stateInit to get the address of our smart contract in workchain with ID 0
log.Println("Contract address:", contractAddress.String()) // Output contract address to console
```




Using the State Init, we can now build the transaction and send it to the blockchain. To carry out this process **a minimum wallet balance of 0.1 TON** (the balance can be less, but this amount is guaranteed to be sufficient) is required. To accomplish this, we’ll need to run the code mentioned earlier in the tutorial, get the correct wallet address and send 0.1 TON to this address.

Let’s start with building the transaction similar to the one we built **in the previous section**:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "github.com/xssnick/tonutils-go/tlb"
  "time"
)

internalMessageBody := cell.BeginCell().
  MustStoreUInt(0, 32).
  MustStoreStringSnake("Hello, TON!").
  EndCell()

internalMessage := cell.BeginCell().
  MustStoreUInt(0x10, 6). // 没有反弹
  MustStoreAddr(address.MustParseAddr("put your first wallet address from were you sent 0.1 TON")).
  MustStoreBigCoins(tlb.MustFromTON("0.03").NanoTON()).
  MustStoreUInt(1, 1 + 4 + 4 + 64 + 32 + 1 + 1). // 保存1表示body是引用
  MustStoreRef(internalMessageBody).
  EndCell()

// 用于我们的钱包的交易
toSign := cell.BeginCell().
  MustStoreUInt(subWallet, 32).
  MustStoreUInt(uint64(time.Now().UTC().Unix()+60), 32).
  MustStoreUInt(0, 32). // 我们将seqno设置为0，因为在部署之后，钱包将将0存储为seqno
  MustStoreUInt(3, 8).
  MustStoreRef(internalMessage)

signature := ed25519.Sign(privateKey, toSign.EndCell().Hash())
body := cell.BeginCell().
  MustStoreSlice(signature, 512).
  MustStoreBuilder(toSign).
	EndCell()
```


<TabItem value="go" label="Golang">

```go
import (
  "github.com/xssnick/tonutils-go/tlb"
  "time"
)

internalMessageBody := cell.BeginCell().
  MustStoreUInt(0, 32).
  MustStoreStringSnake("Hello, TON!").
  EndCell()

internalMessage := cell.BeginCell().
  MustStoreUInt(0x10, 6). // no bounce
  MustStoreAddr(address.MustParseAddr("put your first wallet address from were you sent 0.1 TON")).
  MustStoreBigCoins(tlb.MustFromTON("0.03").NanoTON()).
  MustStoreUInt(1, 1 + 4 + 4 + 64 + 32 + 1 + 1). // We store 1 that means we have body as a reference
  MustStoreRef(internalMessageBody).
  EndCell()

// transaction for our wallet
toSign := cell.BeginCell().
  MustStoreUInt(subWallet, 32).
  MustStoreUInt(uint64(time.Now().UTC().Unix()+60), 32).
  MustStoreUInt(0, 32). // We put seqno = 0, because after deploying wallet will store 0 as seqno
  MustStoreUInt(3, 8).
  MustStoreRef(internalMessage)

signature := ed25519.Sign(privateKey, toSign.EndCell().Hash())
body := cell.BeginCell().
  MustStoreSlice(signature, 512).
  MustStoreBuilder(toSign).
	EndCell()
```




主要的区别将在外部消息的存在上，因为State Init被存储用于正确的合约部署。由于合约尚无自己的代码，因此无法处理任何内部消息。因此，接下来，我们将在成功部署后发送其代码和初始数据，以便可处理我们带有“Hello, TON！”评论的消息：

### Sending An External Transaction

The **main difference** will be in the presence of the external message, because the State Init is stored to help carry out correct contract deployment. Since the contract does not have its own code yet, it cannot process any internal messages. Therefore, next we send its code and the initial data **after it is successfully deployed so it can process our message** with "Hello, TON!" comment:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
externalMessage := cell.BeginCell().
  MustStoreUInt(0b10, 2). // 表示它是一笔外部传入的交易
  MustStoreUInt(0, 2). // src -> addr_none
  MustStoreAddr(contractAddress).
  MustStoreCoins(0). // 导入费用
  MustStoreBoolBit(true). // 我们有State Init
  MustStoreBoolBit(true).  // 我们将State Init存储为引用
  MustStoreRef(stateInit). // 将State Init存储为引用
  MustStoreBoolBit(true). // 我们将消息体存储为引用
  MustStoreRef(body). // 将消息体存储为引用
  EndCell()
```


<TabItem value="go" label="Golang">

```go
externalMessage := cell.BeginCell().
  MustStoreUInt(0b10, 2). // indicate that it is an incoming external transaction
  MustStoreUInt(0, 2). // src -> addr_none
  MustStoreAddr(contractAddress).
  MustStoreCoins(0). // Import fee
  MustStoreBoolBit(true). // We have State Init
  MustStoreBoolBit(true).  // We store State Init as a reference
  MustStoreRef(stateInit). // Store State Init as a reference
  MustStoreBoolBit(true). // We store Message Body as a reference
  MustStoreRef(body). // Store Message Body as a reference
  EndCell()
```




Finally, we can send our transaction to the blockchain to deploy our wallet and use it.

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "context"
  "github.com/xssnick/tonutils-go/liteclient"
  "github.com/xssnick/tonutils-go/tl"
  "github.com/xssnick/tonutils-go/ton"
)

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection)

var resp tl.Serializable
err = client.Client().QueryLiteserver(context.Background(), ton.SendMessage{Body: externalMessage.ToBOCWithFlags(false)}, &resp)
if err != nil {
  log.Fatalln(err.Error())
  return
}
```


<TabItem value="go" label="Golang">

```go
import (
  "context"
  "github.com/xssnick/tonutils-go/liteclient"
  "github.com/xssnick/tonutils-go/tl"
  "github.com/xssnick/tonutils-go/ton"
)

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection)

var resp tl.Serializable
err = client.Client().QueryLiteserver(context.Background(), ton.SendMessage{Body: externalMessage.ToBOCWithFlags(false)}, &resp)
if err != nil {
  log.Fatalln(err.Error())
  return
}
```




Note that we have sent an internal message using mode `3`. If it is necessary to repeat the deployment of the same wallet, **the smart contract can be destroyed**. To accomplish this, set the mode correctly by adding 128 (take the entire balance of the smart contract) + 32 (destroy the smart contract) which will = `160` to retrieve the remaining TON balance and deploy the wallet again.

It's important to note that for each new transaction the **seqno will need to be increased by one**.

:::info
The contract code we used is [verified](https://tonscan.org/tx/BL9T1i5DjX1JRLUn4z9JOgOWRKWQ80pSNevis26hGvc=), so you can see an example [here](https://tonscan.org/address/EQDBjzo_iQCZh3bZSxFnK9ue4hLTOKgsCNKfC8LOUM4SlSCX#source).
:::

## 同时发送多条消息

正如您可能已经知道的，[一个cell可以存储最多1023位的数据和最多4个指向其他cells的引用](develop/data-formats/cell-boc#cell)。在本教程的第一部分中，我们详细介绍了内部消息是如何以“整体”循环作为链接发送的。这意味着可以**在外部消息内存储多达4条内部消息**。这允许同时发送四笔交易。

### Sending Multiple Messages Simultaneously

As you may already know, [one cell can store up to 1023 bits of data and up to 4 references](develop/data-formats/cell-boc#cell) to other cells. In the first section of this tutorial we detailed how internal messages are delivered in a ‘whole’ loop as a link and sent. This means it is possible to **store up to 4 internal messages inside the external** message. This allows four transactions to be sent at the same time.

To accomplish this, it is necessary to create 4 different internal messages. We can do this manually or through a `loop`. We need to define 3 arrays: array of TON amount, array of comments, array of messages. For messages, we need to prepare another one array - internalMessages.

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "github.com/xssnick/tonutils-go/tvm/cell"
)

internalMessagesAmount := [4]string{"0.01", "0.02", "0.03", "0.04"}
internalMessagesComment := [4]string{
  "Hello, TON! #1",
  "Hello, TON! #2",
  "", // 我们让第三笔交易不留评论
  "Hello, TON! #4",
}
destinationAddresses := [4]string{
  "输入属于你的任何地址",
  "输入属于你的任何地址",
  "输入属于你的任何地址",
  "输入属于你的任何地址",
} // 所有4个地址可以相同

var internalMessages [len(internalMessagesAmount)]*cell.Cell // 存储我们内部消息的数组
```


<TabItem value="go" label="Golang">

```go
import (
  "github.com/xssnick/tonutils-go/tvm/cell"
)

internalMessagesAmount := [4]string{"0.01", "0.02", "0.03", "0.04"}
internalMessagesComment := [4]string{
  "Hello, TON! #1",
  "Hello, TON! #2",
  "", // Let's leave the third transaction without comment
  "Hello, TON! #4",
}
destinationAddresses := [4]string{
  "Put any address that belongs to you",
  "Put any address that belongs to you",
  "Put any address that belongs to you",
  "Put any address that belongs to you",
} // All 4 addresses can be the same

var internalMessages [len(internalMessagesAmount)]*cell.Cell // array for our internal messages
```




[Sending mode](/develop/smart-contracts/messages#message-modes) for all messages is set to `mode 3`.  However, if different modes are required an array can be created to fulfill different purposes.

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/tlb"
)

for i := 0; i < len(internalMessagesAmount); i++ {
  amount := internalMessagesAmount[i]

  internalMessage := cell.BeginCell().
    MustStoreUInt(0x18, 6). // bounce
    MustStoreAddr(address.MustParseAddr(destinationAddresses[i])).
    MustStoreBigCoins(tlb.MustFromTON(amount).NanoTON()).
    MustStoreUInt(0, 1+4+4+64+32+1)

  /*
      在这个阶段，并不清楚我们是否会有一个消息体。
      所以只设置stateInit的一位，如果我们有评论，那意味着
      我们有一个消息体。在这种情况下，将位设置为1并将
      体作为引用存储。
  */

  if internalMessagesComment[i] != "" {
    internalMessage.MustStoreBoolBit(true) // 我们将消息体作为引用存储

    internalMessageBody := cell.BeginCell().
      MustStoreUInt(0, 32).
      MustStoreStringSnake(internalMessagesComment[i]).
      EndCell()

    internalMessage.MustStoreRef(internalMessageBody)
  } else {
    /*
        由于我们没有消息体，我们表明这个消息
        中有消息体，但不写入，意味着它不存在。
        在这种情况下，只需设置位为0。
    */
    internalMessage.MustStoreBoolBit(false)
  }
  internalMessages[i] = internalMessage.EndCell()
}
```


<TabItem value="go" label="Golang">

```go
import (
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/tlb"
)

for i := 0; i < len(internalMessagesAmount); i++ {
  amount := internalMessagesAmount[i]

  internalMessage := cell.BeginCell().
    MustStoreUInt(0x18, 6). // bounce
    MustStoreAddr(address.MustParseAddr(destinationAddresses[i])).
    MustStoreBigCoins(tlb.MustFromTON(amount).NanoTON()).
    MustStoreUInt(0, 1+4+4+64+32+1)

  /*
      At this stage, it is not clear if we will have a message body. 
      So put a bit only for stateInit, and if we have a comment, in means 
      we have a body message. In that case, set the bit to 1 and store the 
      body as a reference.
  */

  if internalMessagesComment[i] != "" {
    internalMessage.MustStoreBoolBit(true) // we store Message Body as a reference

    internalMessageBody := cell.BeginCell().
      MustStoreUInt(0, 32).
      MustStoreStringSnake(internalMessagesComment[i]).
      EndCell()

    internalMessage.MustStoreRef(internalMessageBody)
  } else {
    /*
        Since we do not have a message body, we indicate that
        the message body is in this message, but do not write it,
        which means it is absent. In that case, just set the bit to 0.
    */
    internalMessage.MustStoreBoolBit(false)
  }
  internalMessages[i] = internalMessage.EndCell()
}
```




Now let's use our knowledge from [chapter two](/develop/smart-contracts/tutorials/wallet#-deploying-our-wallet) to build a transaction for our wallet that can send 4 transactions simultaneously:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
	"context"
	"crypto/ed25519"
	"crypto/hmac"
	"crypto/sha512"
	"github.com/xssnick/tonutils-go/liteclient"
	"github.com/xssnick/tonutils-go/ton"
	"golang.org/x/crypto/pbkdf2"
	"log"
	"strings"
	"time"
)

walletAddress := address.MustParseAddr("输入你的钱包地址")

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection)

mnemonic := strings.Split("输入你的助记词", " ") // word1 word2 word3
// 以下三行代码将使用助记词提取私钥。
// 我们不会深入讲解密码学细节。在tonutils-go库中，这一切都已经实现，
// 但它立即返回带有地址和现成方法的钱包对象。
// 所以我们必须单独编写获取密钥的代码行。Goland IDE会自动导入
// 所需的库（crypto, pbkdf2等）。
mac := hmac.New(sha512.New, []byte(strings.Join(mnemonic, " ")))
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // 在TON库中使用"TON default seed"作为提取密钥时的salt
// 32是密钥长度
privateKey := ed25519.NewKeyFromSeed(k)              // 获取私钥

block, err := client.CurrentMasterchainInfo(context.Background()) // 获取当前区块，我们在向LiteServer请求时会用到它
if err != nil {
  log.Fatalln("CurrentMasterchainInfo err:", err.Error())
  return
}

getMethodResult, err := client.RunGetMethod(context.Background(), block, walletAddress, "seqno") // 从你的钱包合约运行"seqno"GET方法
if err != nil {
  log.Fatalln("RunGetMethod err:", err.Error())
  return
}
seqno := getMethodResult.MustInt(0) // 从响应中获取seqno

toSign := cell.BeginCell().
  MustStoreUInt(698983191, 32). // subwallet_id | 我们之后考虑这个
  MustStoreUInt(uint64(time.Now().UTC().Unix()+60), 32). // 交易过期时间，+60 = 1分钟
  MustStoreUInt(seqno.Uint64(), 32) // 存储seqno
  // 别忘了，如果我们使用Wallet V4，我们需要添加 MustStoreUInt(0, 8). 
```


<TabItem value="go" label="Golang">

```go
import (
	"context"
	"crypto/ed25519"
	"crypto/hmac"
	"crypto/sha512"
	"github.com/xssnick/tonutils-go/liteclient"
	"github.com/xssnick/tonutils-go/ton"
	"golang.org/x/crypto/pbkdf2"
	"log"
	"strings"
	"time"
)

walletAddress := address.MustParseAddr("put your wallet address")

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection)

mnemonic := strings.Split("put your mnemonic", " ") // word1 word2 word3
// The following three lines will extract the private key using the mnemonic phrase.
// We will not go into cryptographic details. In the library tonutils-go, it is all implemented,
// but it immediately returns the finished object of the wallet with the address and ready-made methods.
// So we’ll have to write the lines to get the key separately. Goland IDE will automatically import
// all required libraries (crypto, pbkdf2 and others).
mac := hmac.New(sha512.New, []byte(strings.Join(mnemonic, " ")))
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // In TON libraries "TON default seed" is used as salt when getting keys
// 32 is a key len
privateKey := ed25519.NewKeyFromSeed(k)              // get private key

block, err := client.CurrentMasterchainInfo(context.Background()) // get current block, we will need it in requests to LiteServer
if err != nil {
  log.Fatalln("CurrentMasterchainInfo err:", err.Error())
  return
}

getMethodResult, err := client.RunGetMethod(context.Background(), block, walletAddress, "seqno") // run "seqno" GET method from your wallet contract
if err != nil {
  log.Fatalln("RunGetMethod err:", err.Error())
  return
}
seqno := getMethodResult.MustInt(0) // get seqno from response

toSign := cell.BeginCell().
  MustStoreUInt(698983191, 32). // subwallet_id | We consider this further
  MustStoreUInt(uint64(time.Now().UTC().Unix()+60), 32). // transaction expiration time, +60 = 1 minute
  MustStoreUInt(seqno.Uint64(), 32) // store seqno
  // Do not forget that if we use Wallet V4, we need to add MustStoreUInt(0, 8). 
```




Next, we’ll add our messages that we built earlier in the loop:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
for i := 0; i < len(internalMessages); i++ {
		internalMessage := internalMessages[i]
		toSign.MustStoreUInt(3, 8) // 存储我们内部交易的mode
		toSign.MustStoreRef(internalMessage) // 将我们的内部消息作为引用存储
}
```


<TabItem value="go" label="Golang">

```go
for i := 0; i < len(internalMessages); i++ {
		internalMessage := internalMessages[i]
		toSign.MustStoreUInt(3, 8) // store mode of our internal transaction
		toSign.MustStoreRef(internalMessage) // store our internalMessage as a reference
}
```




Now that the above processes are complete, let’s **sign** our message, **build an external message** (as outlined in previous sections of this tutorial) and **send it** to the blockchain:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "github.com/xssnick/tonutils-go/tl"
)

signature := ed25519.Sign(privateKey, toSign.EndCell().Hash()) // 获取我们钱包智能合约的消息的哈希并签名以获得签名

body := cell.BeginCell().
  MustStoreSlice(signature, 512). // 存储签名
  MustStoreBuilder(toSign). // 存储我们的消息
  EndCell()

externalMessage := cell.BeginCell().
  MustStoreUInt(0b10, 2). // ext_in_msg_info$10
  MustStoreUInt(0, 2). // src -> addr_none
  MustStoreAddr(walletAddress). // 目的地址
  MustStoreCoins(0). // 引入费
  MustStoreBoolBit(false). // 无State Init
  MustStoreBoolBit(true). // 我们将消息体作为引用存储
  MustStoreRef(body). // 将消息体作为引用存储
  EndCell()

var resp tl.Serializable
err = client.Client().QueryLiteserver(context.Background(), ton.SendMessage{Body: externalMessage.ToBOCWithFlags(false)}, &resp)

if err != nil {
  log.Fatalln(err.Error())
  return
}
```


<TabItem value="go" label="Golang">

```go
import (
  "github.com/xssnick/tonutils-go/tl"
)

signature := ed25519.Sign(privateKey, toSign.EndCell().Hash()) // get the hash of our message to wallet smart contract and sign it to get signature

body := cell.BeginCell().
  MustStoreSlice(signature, 512). // store signature
  MustStoreBuilder(toSign). // store our message
  EndCell()

externalMessage := cell.BeginCell().
  MustStoreUInt(0b10, 2). // ext_in_msg_info$10
  MustStoreUInt(0, 2). // src -> addr_none
  MustStoreAddr(walletAddress). // Destination address
  MustStoreCoins(0). // Import Fee
  MustStoreBoolBit(false). // No State Init
  MustStoreBoolBit(true). // We store Message Body as a reference
  MustStoreRef(body). // Store Message Body as a reference
  EndCell()

var resp tl.Serializable
err = client.Client().QueryLiteserver(context.Background(), ton.SendMessage{Body: externalMessage.ToBOCWithFlags(false)}, &resp)

if err != nil {
  log.Fatalln(err.Error())
  return
}
```




:::info Connection error
If an error related to the lite-server connection (Golang) occurs, the code must be run until the transaction can be sent. This is because the tonutils-go library uses several different lite-servers through the global configuration that have been specified in the code. However, not all lite-servers can accept our connection.
:::

除了常规交易之外，用户经常彼此发送 NFT。不幸的是，并非所有库都包含为这种智能合约量身定制的方法。因此，我们需要创建代码，使我们能够构建发送 NFT 的交易。首先，让我们更熟悉 TON NFT [标准](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md)。

### NFT Transfers

In addition to regular transactions, users often send NFTs to each other. Unfortunately, not all libraries contain methods that are tailored for use with this type of smart contract. Therefore, it is necessary to create code that will allow us to build a transaction for sending NFTs. First, let's become more familiar with the TON NFT [standard](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md).

现在让我们构建交易本身：

- `query_id`: Query ID has no value in terms of transaction processing. The NFT contract doesn't validate it; it only reads it. This value can be useful when a service wants to assign a specific query ID to each of its transactions for identification purposes. Therefore, we will set it to 0.

- `response_destination`: After processing the ownership change transaction there will be extra TON. They will be sent to this address, if specified, otherwise remain on the NFT balance.

- `custom_payload`: The custom_payload is needed to carry out specific tasks and is not used with ordinary NFTs.

- `forward_amount`: If the forward_amount isn’t zero, the specified TON amount will be sent to the new owner. That way the new owner will be notified that they received something.

- `forward_payload`: The forward_payload is additional data that can be sent to the new owner together with the forward_amount. For example, using forward_payload allows users to [add a comment during the transfer of the NFT](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md#forward_payload-format), as shown in the tutorial earlier. However, although the forward_payload is written within TON’s NFT standard, blockchain explorers do not fully support displaying various details. The same problem also exists when displaying Jettons.

Now let's build the transaction itself:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/tlb"
  "github.com/xssnick/tonutils-go/tvm/cell"
)

destinationAddress := address.MustParseAddr("put your wallet where you want to send NFT")
walletAddress := address.MustParseAddr("put your wallet which is the owner of NFT")
nftAddress := address.MustParseAddr("put your nft address")

// 我们可以添加评论，但因为目前不支持，所以不会显示在浏览器中。
forwardPayload := cell.BeginCell().
  MustStoreUInt(0, 32).
  MustStoreStringSnake("Hello, TON!").
  EndCell()

transferNftBody := cell.BeginCell().
  MustStoreUInt(0x5fcc3d14, 32). // NFT 转移的操作码
  MustStoreUInt(0, 64). // query_id
  MustStoreAddr(destinationAddress). // new_owner
  MustStoreAddr(walletAddress). // response_destination 的超额部分
  MustStoreBoolBit(false). // 我们没有 custom_payload
  MustStoreBigCoins(tlb.MustFromTON("0.01").NanoTON()). // forward_amount
  MustStoreBoolBit(true). // 我们以引用的形式存储 forward_payload
  MustStoreRef(forwardPayload). // 以引用的形式存储 forward_payload
  EndCell()

internalMessage := cell.BeginCell().
  MustStoreUInt(0x18, 6). // 弹回
  MustStoreAddr(nftAddress).
  MustStoreBigCoins(tlb.MustFromTON("0.05").NanoTON()).
  MustStoreUInt(1, 1 + 4 + 4 + 64 + 32 + 1 + 1). // 我们存储 1 表示我们有body作为引用
  MustStoreRef(transferNftBody).
  EndCell()
```


<TabItem value="go" label="Golang">

```go
import (
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/tlb"
  "github.com/xssnick/tonutils-go/tvm/cell"
)

destinationAddress := address.MustParseAddr("put your wallet where you want to send NFT")
walletAddress := address.MustParseAddr("put your wallet which is the owner of NFT")
nftAddress := address.MustParseAddr("put your nft address")

// We can add a comment, but it will not be displayed in the explorers,
// as it is not supported by them at the time of writing the tutorial.
forwardPayload := cell.BeginCell().
  MustStoreUInt(0, 32).
  MustStoreStringSnake("Hello, TON!").
  EndCell()

transferNftBody := cell.BeginCell().
  MustStoreUInt(0x5fcc3d14, 32). // Opcode for NFT transfer
  MustStoreUInt(0, 64). // query_id
  MustStoreAddr(destinationAddress). // new_owner
  MustStoreAddr(walletAddress). // response_destination for excesses
  MustStoreBoolBit(false). // we do not have custom_payload
  MustStoreBigCoins(tlb.MustFromTON("0.01").NanoTON()). // forward_amount
  MustStoreBoolBit(true). // we store forward_payload as a reference
  MustStoreRef(forwardPayload). // store forward_payload as a reference
  EndCell()

internalMessage := cell.BeginCell().
  MustStoreUInt(0x18, 6). // bounce
  MustStoreAddr(nftAddress).
  MustStoreBigCoins(tlb.MustFromTON("0.05").NanoTON()).
  MustStoreUInt(1, 1 + 4 + 4 + 64 + 32 + 1 + 1). // We store 1 that means we have body as a reference
  MustStoreRef(transferNftBody).
  EndCell()
```




The NFT transfer opcode comes from [the same standard](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md#tl-b-schema).
Now let's complete the transaction, as is laid out in the previous sections of this tutorial. The correct code needed to complete the transaction is found in the [GitHub repository](/develop/smart-contracts/tutorials/wallet#source-code).

智能合约经常使用 [GET 方法](/develop/smart-contracts/guidelines/get-methods)，但它们不在区块链内部运行，而是在客户端上运行。GET 方法有许多用途，为智能合约提供对不同数据类型的访问。例如，NFT 智能合约中的 [get_nft_data() 方法](https://github.com/ton-blockchain/token-contract/blob/991bdb4925653c51b0b53ab212c53143f71f5476/nft/nft-item.fc#L142-L145) 允许用户检索特定的内容、所有者和 NFT 集合信息。

### Wallet v3 and Wallet v4 Get Methods

Smart contracts often make use of [GET methods](/develop/smart-contracts/guidelines/get-methods), however, they don’t run inside the blockchain but instead on the client side. GET methods have many uses and provide accessibility to different data types for smart contracts. For example, the [get_nft_data() method in NFT smart contracts](https://github.com/ton-blockchain/token-contract/blob/991bdb4925653c51b0b53ab212c53143f71f5476/nft/nft-item.fc#L142-L145) allows users to retrieve specific content, owner, and NFT collection information.

现在，我们转向只有 V4 钱包使用的方法：

|                                                                方法                                                                |                                                         说明                                                        |
| :------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------: |
|                        int get_subwallet_id()                       |                              教程前面已经考虑过这个。此方法允许您检索 subwallet_id。                              |
| int is_plugin_installed(int wc, int addr_hash) | 让我们知道插件是否已安装。调用此方法时，需要传递 [工作链](/learn/overviews/ton-blockchain#workchain-blockchain-with-your-own-rules) 和插件地址哈希。 |

让我们考虑 `get_public_key` 和 `is_plugin_installed` 方法。选择这两种方法是因为，首先我们需要从 256 位数据中获取公钥，然后我们需要学习如何向 GET 方法传递切片和不同类型的数据。这对于我们正确使用这些方法非常有用。

|                                                              Method                                                              |                                                                                                                     Explanation                                                                                                                    |
| :------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|                        int get_subwallet_id()                       |                                                  Earlier in the tutorial we considered this. This method allows you to retrive subwallet_id.                                                  |
| int is_plugin_installed(int wc, int addr_hash) | Let’s us know if the plugin has been installed. To call this method it’s necessary to pass the  [workchain](/learn/overviews/ton-blockchain#workchain-blockchain-with-your-own-rules) and the plugin address hash. |
|                       tuple get_plugin_list()                       |                                                                                 This method returns the address of the plugins that are installed.                                                                                 |

Let’s consider the `get_public_key` and the `is_plugin_installed` methods. These two methods were chosen because at first we would have to get a public key from 256 bits of data, and after that we would have to learn how to pass a slice and different types of data to GET methods. This is very useful to help us learn how to properly make use of these methods.

First we need a client that is capable of sending requests. Therefore, we’ll use a specific wallet address ([EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF](https://tonscan.org/address/EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF)) as an example:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "context"
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/liteclient"
  "github.com/xssnick/tonutils-go/ton"
  "log"
)

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection)

block, err := client.CurrentMasterchainInfo(context.Background()) // 获取当前区块， 我们将需要它用于向 LiteServer 发送请求
if err != nil {
  log.Fatalln("CurrentMasterchainInfo err:", err.Error())
  return
}

walletAddress := address.MustParseAddr("EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF") // 以我的钱包地址为例
```


<TabItem value="go" label="Golang">

```go
import (
  "context"
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/liteclient"
  "github.com/xssnick/tonutils-go/ton"
  "log"
)

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection)

block, err := client.CurrentMasterchainInfo(context.Background()) // get current block, we will need it in requests to LiteServer
if err != nil {
  log.Fatalln("CurrentMasterchainInfo err:", err.Error())
  return
}

walletAddress := address.MustParseAddr("EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF") // my wallet address as an example
```




Now we need to call the GET method wallet.

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
getResult, err := client.RunGetMethod(context.Background(), block, walletAddress, "get_public_key") // 运行 get_public_key GET 方法
if err != nil {
	log.Fatalln("RunGetMethod err:", err.Error())
	return
}

// 我们有一个包含值的数组作为回应，并且在读取它时应该指定索引
// 在 get_public_key 的情况下，我们只有一个返回值，存储在 0 索引处
publicKeyUInt := getResult.MustInt(0) // 读取包含 uint256 的回答
publicKey := publicKeyUInt.Text(16)   // 从 bigint（uint256）获取十六进制字符串
log.Println(publicKey)
```


<TabItem value="go" label="Golang">

```go
getResult, err := client.RunGetMethod(context.Background(), block, walletAddress, "get_public_key") // run get_public_key GET Method
if err != nil {
	log.Fatalln("RunGetMethod err:", err.Error())
	return
}

// We have a response as an array with values and should specify the index when reading it
// In the case of get_public_key, we have only one returned value that is stored at 0 index
publicKeyUInt := getResult.MustInt(0) // read answer that contains uint256
publicKey := publicKeyUInt.Text(16)   // get hex string from bigint (uint256)
log.Println(publicKey)
```




After the call is successfully completed the end result is an extremely large 256 bit number which must be translated into a hex string. The resulting hex string for the wallet address we provided above is as follows: `430db39b13cf3cb76bfa818b6b13417b82be2c6c389170fbe06795c71996b1f8`.
Next, we leverage the [TonAPI](https://tonapi.io/swagger-ui) (/v1/wallet/findByPubkey method), by inputting the obtained hex string into the system and it is immediately clear that the first element in the array within the answer will identify my wallet.

Then we switch to the `is_plugin_installed` method. As an example, we’ll again use the wallet we used earlier ([EQAM7M--HGyfxlErAIUODrxBA3yj5roBeYiTuy6BHgJ3Sx8k](https://tonscan.org/address/EQAM7M--HGyfxlErAIUODrxBA3yj5roBeYiTuy6BHgJ3Sx8k)) and the plugin ([EQBTKTis-SWYdupy99ozeOvnEBu8LRrQP_N9qwOTSAy3sQSZ](https://tonscan.org/address/EQBTKTis-SWYdupy99ozeOvnEBu8LRrQP_N9qwOTSAy3sQSZ)):

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
oldWalletAddress := address.MustParseAddr("EQAM7M--HGyfxlErAIUODrxBA3yj5roBeYiTuy6BHgJ3Sx8k")
subscriptionAddress := address.MustParseAddr("EQBTKTis-SWYdupy99ozeOvnEBu8LRrQP_N9qwOTSAy3sQSZ") // 已经安装在钱包上的订阅插件地址
```


<TabItem value="go" label="Golang">

```go
oldWalletAddress := address.MustParseAddr("EQAM7M--HGyfxlErAIUODrxBA3yj5roBeYiTuy6BHgJ3Sx8k")
subscriptionAddress := address.MustParseAddr("EQBTKTis-SWYdupy99ozeOvnEBu8LRrQP_N9qwOTSAy3sQSZ") // subscription plugin address which is already installed on the wallet
```




Now we need to retrieve the plugin’s hash address so the address can be translated into a number and sent to the GET Method.

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "math/big"
)

hash := big.NewInt(0).SetBytes(subscriptionAddress.Data())
// runGetMethod 会自动识别传递值的类型
getResult, err = client.RunGetMethod(context.Background(), block, oldWalletAddress,
  "is_plugin_installed",
  0,    // 传递工作链
  hash) // 传递插件地址
if err != nil {
  log.Fatalln("RunGetMethod err:", err.Error())
  return
}

log.Println(getResult.MustInt(0)) // -1
```


<TabItem value="go" label="Golang">

```go
import (
  "math/big"
)

hash := big.NewInt(0).SetBytes(subscriptionAddress.Data())
// runGetMethod will automatically identify types of passed values
getResult, err = client.RunGetMethod(context.Background(), block, oldWalletAddress,
  "is_plugin_installed",
  0,    // pass workchain
  hash) // pass plugin address
if err != nil {
  log.Fatalln("RunGetMethod err:", err.Error())
  return
}

log.Println(getResult.MustInt(0)) // -1
```




在第三章中，我们部署了一个钱包。为此，我们最初发送了一些TON，然后从钱包发送了一笔交易以部署一个智能合约。然而，这个过程并不常用于外部交易，通常主要用于钱包。在开发合约时，部署过程是通过发送内部消息来初始化的。

### Contract Deployment via Wallet

In chapter three, we deployed a wallet. To accomplish this, we initially sent some TON and then a transaction from the wallet to deploy a smart contract. However, this process is not broadly used with external transactions and is often primarily used for wallets only. While developing contracts, the deployment process is initialized by sending internal messages.

To accomplish this, will use the V3R2 wallet smart contract that was used in [the third chapter](/develop/smart-contracts/tutorials/wallet#compiling-our-wallet-code).
In this case, we’ll set the `subwallet_id` to `3` or any other number needed to retrieve another address when using the same private key (it's changeable):

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "crypto/ed25519"
  "crypto/hmac"
  "crypto/sha512"
  "encoding/base64"
  "github.com/xssnick/tonutils-go/tvm/cell"
  "golang.org/x/crypto/pbkdf2"
  "strings"
)

mnemonicArray := strings.Split("put your mnemonic", " ")
// 下面的三行将使用助记词短语提取私钥。
// 我们不会深入讨论加密细节。在tonutils-go库中，这些都已实现，
// 但它直接返回的是带有地址和准备好的方法的完成的钱包对象。
// 因此，我们必须单独编写代码行来获取密钥。Goland IDE将自动导入
// 所需的所有库（crypto, pbkdf2等）。
mac := hmac.New(sha512.New, []byte(strings.Join(mnemonicArray, " ")))
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // 在TON库中，使用"TON default seed"作为获取密钥时的salt
// 32 是密钥长度
privateKey := ed25519.NewKeyFromSeed(k)              // 获取私钥
publicKey := privateKey.Public().(ed25519.PublicKey) // 从私钥获取公钥

BOCBytes, _ := base64.StdEncoding.DecodeString("te6ccgEBCAEAhgABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQCW8oMI1xgg0x/TH9MfAvgju/Jj7UTQ0x/TH9P/0VEyuvKhUUS68qIE+QFUEFX5EPKj+ACTINdKltMH1AL7AOgwAaTIyx/LH8v/ye1UAATQMAIBSAYHABe7Oc7UTQ0z8x1wv/gAEbjJftRNDXCx+A==")
codeCell, _ := cell.FromBOC(BOCBytes)
dataCell := cell.BeginCell().
  MustStoreUInt(0, 32).           // Seqno
  MustStoreUInt(3, 32).           // 子钱包ID
  MustStoreSlice(publicKey, 256). // 公钥
  EndCell()

stateInit := cell.BeginCell().
  MustStoreBoolBit(false). // 没有 split_depth
  MustStoreBoolBit(false). // 没有特殊
  MustStoreBoolBit(true).  // 我们有代码
  MustStoreRef(codeCell).
  MustStoreBoolBit(true). // 我们有数据
  MustStoreRef(dataCell).
  MustStoreBoolBit(false). // 没有库
  EndCell()
```


<TabItem value="go" label="Golang">

```go
import (
  "crypto/ed25519"
  "crypto/hmac"
  "crypto/sha512"
  "encoding/base64"
  "github.com/xssnick/tonutils-go/tvm/cell"
  "golang.org/x/crypto/pbkdf2"
  "strings"
)

mnemonicArray := strings.Split("put your mnemonic", " ")
// The following three lines will extract the private key using the mnemonic phrase.
// We will not go into cryptographic details. In the library tonutils-go, it is all implemented,
// but it immediately returns the finished object of the wallet with the address and ready-made methods.
// So we’ll have to write the lines to get the key separately. Goland IDE will automatically import
// all required libraries (crypto, pbkdf2 and others).
mac := hmac.New(sha512.New, []byte(strings.Join(mnemonicArray, " ")))
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // In TON libraries "TON default seed" is used as salt when getting keys
// 32 is a key len
privateKey := ed25519.NewKeyFromSeed(k)              // get private key
publicKey := privateKey.Public().(ed25519.PublicKey) // get public key from private key

BOCBytes, _ := base64.StdEncoding.DecodeString("te6ccgEBCAEAhgABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQCW8oMI1xgg0x/TH9MfAvgju/Jj7UTQ0x/TH9P/0VEyuvKhUUS68qIE+QFUEFX5EPKj+ACTINdKltMH1AL7AOgwAaTIyx/LH8v/ye1UAATQMAIBSAYHABe7Oc7UTQ0z8x1wv/gAEbjJftRNDXCx+A==")
codeCell, _ := cell.FromBOC(BOCBytes)
dataCell := cell.BeginCell().
  MustStoreUInt(0, 32).           // Seqno
  MustStoreUInt(3, 32).           // Subwallet ID
  MustStoreSlice(publicKey, 256). // Public Key
  EndCell()

stateInit := cell.BeginCell().
  MustStoreBoolBit(false). // No split_depth
  MustStoreBoolBit(false). // No special
  MustStoreBoolBit(true).  // We have code
  MustStoreRef(codeCell).
  MustStoreBoolBit(true). // We have data
  MustStoreRef(dataCell).
  MustStoreBoolBit(false). // No library
  EndCell()
```




Next we’ll retrieve the address from our contract and build the InternalMessage. Also we add the "Deploying..." comment to our transaction.

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/tlb"
  "log"
)

contractAddress := address.NewAddress(0, 0, stateInit.Hash()) // 获取stateInit的哈希来获取我们的智能合约在工作链ID为0的地址
log.Println("合约地址:", contractAddress.String())   // 输出合约地址到控制台

internalMessageBody := cell.BeginCell().
  MustStoreUInt(0, 32).
  MustStoreStringSnake("Deploying...").
  EndCell()

internalMessage := cell.BeginCell().
  MustStoreUInt(0x10, 6). // 不反弹
  MustStoreAddr(contractAddress).
  MustStoreBigCoins(tlb.MustFromTON("0.01").NanoTON()).
  MustStoreUInt(0, 1+4+4+64+32).
  MustStoreBoolBit(true).            // 我们有State Init
  MustStoreBoolBit(true).            // 我们将State Init作为引用存储
  MustStoreRef(stateInit).           // 将State Init作为引用存储
  MustStoreBoolBit(true).            // 我们将消息体作为引用存储
  MustStoreRef(internalMessageBody). // 将消息体Init作为引用存储
  EndCell()
```


<TabItem value="go" label="Golang">

```go
import (
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/tlb"
  "log"
)

contractAddress := address.NewAddress(0, 0, stateInit.Hash()) // get the hash of stateInit to get the address of our smart contract in workchain with ID 0
log.Println("Contract address:", contractAddress.String())   // Output contract address to console

internalMessageBody := cell.BeginCell().
  MustStoreUInt(0, 32).
  MustStoreStringSnake("Deploying...").
  EndCell()

internalMessage := cell.BeginCell().
  MustStoreUInt(0x10, 6). // no bounce
  MustStoreAddr(contractAddress).
  MustStoreBigCoins(tlb.MustFromTON("0.01").NanoTON()).
  MustStoreUInt(0, 1+4+4+64+32).
  MustStoreBoolBit(true).            // We have State Init
  MustStoreBoolBit(true).            // We store State Init as a reference
  MustStoreRef(stateInit).           // Store State Init as a reference
  MustStoreBoolBit(true).            // We store Message Body as a reference
  MustStoreRef(internalMessageBody). // Store Message Body Init as a reference
  EndCell()
```




:::info
Note that above, the bits have been specified and that the stateInit and internalMessageBody have been saved as references. Since the links are stored separately, we could write 4 (0b100) + 2 (0b10) + 1 (0b1) -> (4 + 2 + 1, 1 + 4 + 4 + 64 + 32 + 1 + 1 + 1) which means (0b111, 1 + 4 + 4 + 64 + 32 + 1 + 1 + 1) and then save two references.
:::

Next, we’ll prepare a message for our wallet and send it:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "context"
  "github.com/xssnick/tonutils-go/liteclient"
  "github.com/xssnick/tonutils-go/tl"
  "github.com/xssnick/tonutils-go/ton"
  "time"
)

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection)

block, err := client.CurrentMasterchainInfo(context.Background()) // 获取当前区块，我们在请求LiteServer时需要它
if err != nil {
  log.Fatalln("CurrentMasterchainInfo 错误:", err.Error())
  return
}

walletMnemonicArray := strings.Split("put your mnemonic", " ")
mac = hmac.New(sha512.New, []byte(strings.Join(walletMnemonicArray, " ")))
hash = mac.Sum(nil)
k = pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // 在TON库中，使用"TON default seed"作为获取密钥时的salt
// 32 是密钥长度
walletPrivateKey := ed25519.NewKeyFromSeed(k) // 获取私钥
walletAddress := address.MustParseAddr("用来部署的你的钱包地址")

getMethodResult, err := client.RunGetMethod(context.Background(), block, walletAddress, "seqno") // 从你的钱包合约运行"seqno" GET方法
if err != nil {
  log.Fatalln("RunGetMethod 错误:", err.Error())
  return
}
seqno := getMethodResult.MustInt(0) // 从回应中获取seqno

toSign := cell.BeginCell().
  MustStoreUInt(698983191, 32).                          // 子钱包id | 我们稍后考虑这个
  MustStoreUInt(uint64(time.Now().UTC().Unix()+60), 32). // 交易过期时间, +60 = 1 分钟
  MustStoreUInt(seqno.Uint64(), 32).                     // 存储seqno
  // 不要忘记如果我们使用钱包V4，我们需要添加MustStoreUInt(0, 8).
  MustStoreUInt(3, 8).          // 存储我们内部交易的模式
  MustStoreRef(internalMessage) // 将我们的内部消息作为引用存储

signature := ed25519.Sign(walletPrivateKey, toSign.EndCell().Hash()) // 获取我们发往钱包智能合约的消息hash并签名以获取签名

body := cell.BeginCell().
  MustStoreSlice(signature, 512). // 存储签名
  MustStoreBuilder(toSign).       // 存储我们的消息
  EndCell()

externalMessage := cell.BeginCell().
  MustStoreUInt(0b10, 2).       // ext_in_msg_info$10
  MustStoreUInt(0, 2).          // src -> addr_none
  MustStoreAddr(walletAddress). // 目的地址
  MustStoreCoins(0).            // 导入费
  MustStoreBoolBit(false).      // 没有State Init
  MustStoreBoolBit(true).       // 我们将消息体作为引用存储
  MustStoreRef(body).           // 将消息体作为引用存储
  EndCell()

var resp tl.Serializable
err = client.Client().QueryLiteserver(context.Background(), ton.SendMessage{Body: externalMessage.ToBOCWithFlags(false)}, &resp)

if err != nil {
  log.Fatalln(err.Error())
  return
}
```


<TabItem value="go" label="Golang">

```go
import (
  "context"
  "github.com/xssnick/tonutils-go/liteclient"
  "github.com/xssnick/tonutils-go/tl"
  "github.com/xssnick/tonutils-go/ton"
  "time"
)

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection)

block, err := client.CurrentMasterchainInfo(context.Background()) // get current block, we will need it in requests to LiteServer
if err != nil {
  log.Fatalln("CurrentMasterchainInfo err:", err.Error())
  return
}

walletMnemonicArray := strings.Split("put your mnemonic", " ")
mac = hmac.New(sha512.New, []byte(strings.Join(walletMnemonicArray, " ")))
hash = mac.Sum(nil)
k = pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // In TON libraries "TON default seed" is used as salt when getting keys
// 32 is a key len
walletPrivateKey := ed25519.NewKeyFromSeed(k) // get private key
walletAddress := address.MustParseAddr("put your wallet address with which you will deploy")

getMethodResult, err := client.RunGetMethod(context.Background(), block, walletAddress, "seqno") // run "seqno" GET method from your wallet contract
if err != nil {
  log.Fatalln("RunGetMethod err:", err.Error())
  return
}
seqno := getMethodResult.MustInt(0) // get seqno from response

toSign := cell.BeginCell().
  MustStoreUInt(698983191, 32).                          // subwallet_id | We consider this further
  MustStoreUInt(uint64(time.Now().UTC().Unix()+60), 32). // transaction expiration time, +60 = 1 minute
  MustStoreUInt(seqno.Uint64(), 32).                     // store seqno
  // Do not forget that if we use Wallet V4, we need to add MustStoreUInt(0, 8).
  MustStoreUInt(3, 8).          // store mode of our internal transaction
  MustStoreRef(internalMessage) // store our internalMessage as a reference

signature := ed25519.Sign(walletPrivateKey, toSign.EndCell().Hash()) // get the hash of our message to wallet smart contract and sign it to get signature

body := cell.BeginCell().
  MustStoreSlice(signature, 512). // store signature
  MustStoreBuilder(toSign).       // store our message
  EndCell()

externalMessage := cell.BeginCell().
  MustStoreUInt(0b10, 2).       // ext_in_msg_info$10
  MustStoreUInt(0, 2).          // src -> addr_none
  MustStoreAddr(walletAddress). // Destination address
  MustStoreCoins(0).            // Import Fee
  MustStoreBoolBit(false).      // No State Init
  MustStoreBoolBit(true).       // We store Message Body as a reference
  MustStoreRef(body).           // Store Message Body as a reference
  EndCell()

var resp tl.Serializable
err = client.Client().QueryLiteserver(context.Background(), ton.SendMessage{Body: externalMessage.ToBOCWithFlags(false)}, &resp)

if err != nil {
  log.Fatalln(err.Error())
  return
}
```




在某些情况下，可能需要一次发送大量的交易。如前所述，普通钱包支持一次发送最多4笔交易，这是通过在单个cell中存储[最多4个引用](/develop/data-formats/cell-boc#cell)来支持的。高负载钱包则允许一次发送255笔交易。这个限制的存在是因为区块链的配置设置中对外部消息（动作）的最大数量设定为255。

## 🔥 High-Load Wallets

In some situations, sending a large number of transactions per message may be necessary. As previously mentioned, ordinary wallets support sending up to 4 transactions at a time by storing [a maximum of 4 references](/develop/data-formats/cell-boc#cell) in a single cell. High-load wallets only allow 255 transactions to be sent at once. This restriction exists because the maximum number of outgoing messages (actions) in the blockchain’s config settings is set to 255.

首先，让我们查看[高负载钱包智能合约的代码结构](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/highload-wallet-v2-code.fc)：

### High-load wallet FunC code

First, let’s examine [the code structure of high-load wallet smart contract](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/highload-wallet-v2-code.fc):

```func
() recv_external(slice in_msg) impure {
  var signature = in_msg~load_bits(512); ;; get signature from the message body
  var cs = in_msg;
  var (subwallet_id, query_id) = (cs~load_uint(32), cs~load_uint(64)); ;; get rest values from the message body
  var bound = (now() << 32); ;; bitwise left shift operation
  throw_if(35, query_id < bound); ;; throw an error if transaction has expired
  var ds = get_data().begin_parse();
  var (stored_subwallet, last_cleaned, public_key, old_queries) = (ds~load_uint(32), ds~load_uint(64), ds~load_uint(256), ds~load_dict()); ;; read values from storage
  ds.end_parse(); ;; make sure we do not have anything in ds
  (_, var found?) = old_queries.udict_get?(64, query_id); ;; check if we have already had such a request
  throw_if(32, found?); ;; if yes throw an error
  throw_unless(34, subwallet_id == stored_subwallet);
  throw_unless(35, check_signature(slice_hash(in_msg), signature, public_key));
  var dict = cs~load_dict(); ;; get dictionary with messages
  cs.end_parse(); ;; make sure we do not have anything in cs
  accept_message();
```

> 💡 Useful links:
>
> ["Bitwise operations" in docs](/develop/func/stdlib/#dict_get)
>
> ["load_dict()" in docs](/develop/func/stdlib/#load_dict)
>
> ["udict_get?()" in docs](/develop/func/stdlib/#dict_get)

如我们之前讨论的，普通钱包在每次交易后 seqno 增加 `1`。在使用钱包序列时，我们必须等待这个值更新，然后使用 GET 方法检索它并发送新的交易。
这个过程需要很长时间，高负载钱包不是为此设计的（如上所述，它们旨在快速发送大量交易）。因此，TON上的高负载钱包使用了 `query_id`。

### Using a Query ID In Place Of a Seqno

As we previously discussed, ordinary wallet seqno increase by `1` after each transaction. While using a wallet sequence we had to wait until this value was updated, then retrieve it using the GET method and send a new transaction.
This process takes a significant amount of time which high-load wallets are not designed for (as discussed above, they are meant to send a large number of transactions very quickly). Therefore, high-load wallets on TON make use of the `query_id`.

通过这种方式，我们**被保护免受重复交易的影响**，这是普通钱包中 seqno 的作用。

```func
var (stored_subwallet, last_cleaned, public_key, old_queries) = (ds~load_uint(32), ds~load_uint(64), ds~load_uint(256), ds~load_dict()); ;; read values from storage
ds.end_parse(); ;; make sure we do not have anything in ds
(_, var found?) = old_queries.udict_get?(64, query_id); ;; check if we have already had such a request
throw_if(32, found?); ;; if yes throw an error
```

合约接受外部消息后，将开始循环，在循环中取出存储在字典中的 `slices`。这些切片存储了交易模式和交易本身。发送新交易一直进行，直到字典为空。

### Sending Transactions

After the contract has accepted the external message, a loop starts, in which the `slices` stored in the dictionary are taken. These slices store transaction modes and the transactions themselves. Sending new transactions takes place until the dictionary is empty.

```func
int i = -1; ;; we write -1 because it will be the smallest value among all dictionary keys
do {
  (i, var cs, var f) = dict.idict_get_next?(16, i); ;; get the key and its corresponding value with the smallest key, which is greater than i
  if (f) { ;; check if any value was found
    var mode = cs~load_uint(8); ;; load transaction mode
    send_raw_message(cs~load_ref(), mode); ;; load transaction itself and send it
  }
} until (~ f); ;; if any value was found continue
```

> 💡 Useful link:
>
> ["idict_get_next()" in docs](/develop/func/stdlib/#dict_get_next)

通常情况下，[TON上的智能合约需要为自己的存储付费](develop/smart-contracts/fees#storage-fee)。这意味着智能合约可以存储的数据量是有限的，以防止高网络交易费用。为了让系统更高效，超过 64 秒的交易将从存储中移除。按照以下方式进行：

### Removing Expired Queries

Typically, [smart contracts on TON pay for their own storage](develop/smart-contracts/fees#storage-fee). This means that the amount of data smart contracts can store is limited to prevent high network transaction fees. To allow the system to be more efficient, transactions that are more than 64 seconds old are removed from the storage. This is conducted as follows:

```func
bound -= (64 << 32);   ;; clean up records that have expired more than 64 seconds ago
old_queries~udict_set_builder(64, query_id, begin_cell()); ;; add current query to dictionary
var queries = old_queries; ;; copy dictionary to another variable
do {
  var (old_queries', i, _, f) = old_queries.udict_delete_get_min(64);
  f~touch();
  if (f) { ;; check if any value was found
    f = (i < bound); ;; check if more than 64 seconds have elapsed after expiration
  }
  if (f) { 
    old_queries = old_queries'; ;; if yes save changes in our dictionary
    last_cleaned = i; ;; save last removed query
  }
} until (~ f);
```

> 💡 Useful link:
>
> ["udict_delete_get_min()" in docs](/develop/func/stdlib/#dict_delete_get_min)

如果您之前没有使用过位运算，那么这个部分可能会显得有些复杂。在智能合约代码中可以看到以下代码行：

### Bitwise Operations

结果，在右侧的数字上添加了 32 位。这意味着 **现有值向左移动 32 位**。举例来说，让我们考虑数字 3 并将其翻译成二进制形式，结果是 11。应用 `3 << 2` 操作，11 移动了 2 位。这意味着在字符串的右侧添加了两位。最后，我们得到了 1100，即 12。

```func
var bound = (now() << 32); ;; bitwise left shift operation
```

接下来，让我们考虑以下代码行：

The first thing to understand about this process is to remember that the `now()` function returns a result of uint32, meaning that the resulting value will be 32 bits. By shifting 32 bits to the left, space is opened up for another uint32, resulting in the correct query_id. This way, the **timestamp and query_id can be combined** within one variable for optimization.

在上面，我们执行了一个操作，将数字 64 向左移动 32 位，以**减去 64 秒**的时间戳。这样我们就可以比较过去的 query_ids，看看它们是否小于接收到的值。如果是这样，它们就超过了 64 秒：

```func
if (f) { ;; 检查是否找到了任何值
  f = (i < bound); ;; 检查是否超过 64 秒后过期
}
```

为了更好地理解，让我们使用 `1625918400` 作为时间戳的示例。它的二进制表示（左侧添加零以得到 32 位）是 01100000111010011000101111000000。执行 32 位位左移操作后，我们数字的二进制表示末尾会出现 32 个零。

```func
if (f) { ;; check if any value has been found
  f = (i < bound); ;; check if more than 64 seconds have elapsed after expiration
}
```

To understand this better, let’s use the number `1625918400` as an example of a timestamp. Its binary representation (with the left-handed addition of zeros for 32 bits) is 01100000111010011000101111000000. By performing a 32 bit bitwise left shift, the result is 32 zeros at the end of the binary representation of our number.

所有操作完成后，剩下的唯一任务就是将新的值保存在存储中：

### Storage Updates

After all operations are complete, the only task remaining is to save the new values in the storage:

```func
  set_data(begin_cell()
    .store_uint(stored_subwallet, 32)
    .store_uint(last_cleaned, 64)
    .store_uint(public_key, 256)
    .store_dict(old_queries)
    .end_cell());
}
```

### GET Methods

让我们仔细看看 `int processed?(int query_id)` 方法，以帮助我们了解为什么我们需要使用 last_cleaned：

|                                       Method                                      |                                                                                                                                                         Explanation                                                                                                                                                        |
| :-------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|        int processed?(int query_id)       | Notifies the user if a particular request has been processed. This means it returns `-1` if the request has been processed and `0` if it has not. Also, this method may return `1` if the answer is unknown since the request is old and no longer stored in the contract. |
| int get_public_key() |                                                                                                                 Rerive a public key. We have considered this method before.                                                                                                                |

`last_cleaned` 从合约的存储和旧查询字典中检索。如果找到了查询，它应返回 true；如果没有，则表达式 `- (query_id <= last_cleaned)`。last_cleaned 包含最后一个被删除的、**时间戳最高**的请求，因为我们开始时从最小时间戳删除请求。

```func
int processed?(int query_id) method_id {
  var ds = get_data().begin_parse();
  var (_, last_cleaned, _, old_queries) = (ds~load_uint(32), ds~load_uint(64), ds~load_uint(256), ds~load_dict());
  ds.end_parse();
  (_, var found) = old_queries.udict_get?(64, query_id);
  return found ? true : - (query_id <= last_cleaned);
}
```

The `last_cleaned` is retrieved from the storage of the contract and a dictionary of old queries. If the query is found, it is to be returned true, and if not, the expression `- (query_id <= last_cleaned)`. The last_cleaned contains the last removed request **with the highest timestamp**, as we started with the minimum timestamp when deleting the requests.

为了部署高负载钱包，必须提前生成一个助记词密钥，用户将使用此密钥。可以使用在本教程之前部分中使用的相同密钥。

### Deploying High-Load Wallets

In order to deploy a high-load wallet it is necessary to generate a mnemonic key in advance, which will be used by the user. It is possible to use the same key that was used in previous sections of this tutorial.

To begin the process required to deploy a high-load wallet it's necessary to copy [the code of the smart contract](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/highload-wallet-v2-code.fc) to the same directory where the stdlib.fc and wallet_v3 are located and remember to add `#include "stdlib.fc";` to the beginning of the code. Next we’ll compile the high-load wallet code like we did in [section three](/develop/smart-contracts/tutorials/wallet#compiling-wallet-code):

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { compileFunc } from '@ton-community/func-js';
import fs from 'fs'
import { Cell } from '@ton/core';

const result = await compileFunc({
    targets: ['highload_wallet.fc'], // targets of your project
    sources: {
        'stdlib.fc': fs.readFileSync('./src/stdlib.fc', { encoding: 'utf-8' }),
        'highload_wallet.fc': fs.readFileSync('./src/highload_wallet.fc', { encoding: 'utf-8' }),
    }
});

if (result.status === 'error') {
console.error(result.message)
return;
}

const codeCell = Cell.fromBoc(Buffer.from(result.codeBoc, 'base64'))[0];

// now we have base64 encoded BOC with compiled code in result.codeBoc
console.log('Code BOC: ' + result.codeBoc);
console.log('\nHash: ' + codeCell.hash().toString('base64')); // get the hash of cell and convert in to base64 encoded string

```




在上述结果的基础上，我们可以使用base64编码的输出，在其他库和语言中检索包含我们钱包代码的cell，具体操作如下：

```text
Code BOC: te6ccgEBCQEA5QABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQHq8oMI1xgg0x/TP/gjqh9TILnyY+1E0NMf0z/T//QE0VNggED0Dm+hMfJgUXO68qIH+QFUEIf5EPKjAvQE0fgAf44WIYAQ9HhvpSCYAtMH1DAB+wCRMuIBs+ZbgyWhyEA0gED0Q4rmMQHIyx8Tyz/L//QAye1UCAAE0DACASAGBwAXvZznaiaGmvmOuF/8AEG+X5dqJoaY+Y6Z/p/5j6AmipEEAgegc30JjJLb/JXdHxQANCCAQPSWb6VsEiCUMFMDud4gkzM2AZJsIeKz

Hash: lJTRzI7fEvBWcaGpugmSEJbrUIEeGSTsZcPGKfu4CBI=
```

With the above result it is possible to use the base64 encoded output to retrieve the cell with our wallet code in other libraries and languages as follows:

<Tabs groupId="code-examples">
<TabItem value="go" label="Golang">

```go
import (
  "encoding/base64"
  "github.com/xssnick/tonutils-go/tvm/cell"
  "log"
)

base64BOC := "te6ccgEBCQEA5QABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQHq8oMI1xgg0x/TP/gjqh9TILnyY+1E0NMf0z/T//QE0VNggED0Dm+hMfJgUXO68qIH+QFUEIf5EPKjAvQE0fgAf44WIYAQ9HhvpSCYAtMH1DAB+wCRMuIBs+ZbgyWhyEA0gED0Q4rmMQHIyx8Tyz/L//QAye1UCAAE0DACASAGBwAXvZznaiaGmvmOuF/8AEG+X5dqJoaY+Y6Z/p/5j6AmipEEAgegc30JjJLb/JXdHxQANCCAQPSWb6VsEiCUMFMDud4gkzM2AZJsIeKz" // save our base64 encoded output from compiler to variable
codeCellBytes, _ := base64.StdEncoding.DecodeString(base64BOC) // decode base64 in order to get byte array
codeCell, err := cell.FromBOC(codeCellBytes) // get cell with code from byte array
if err != nil { // check if there is any error
  panic(err) 
}

log.Println("Hash:", base64.StdEncoding.EncodeToString(codeCell.Hash())) // get the hash of our cell, encode it to base64 because it has []byte type and output to the terminal
```




Now we need to retrieve a cell composed of its initial data, build a State Init, and calculate a high-load wallet address. After studying the smart contract code it became clear that the subwallet_id, last_cleaned, public_key and old_queries are sequentially stored in the storage:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "crypto/ed25519"
  "crypto/hmac"
  "crypto/sha512"
  "github.com/xssnick/tonutils-go/address"
  "golang.org/x/crypto/pbkdf2"
  "strings"
)

highloadMnemonicArray := strings.Split("put your mnemonic that you have generated and saved before", " ") // 单词1 单词2 单词3
mac := hmac.New(sha512.New, []byte(strings.Join(highloadMnemonicArray, " ")))
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // 在TON库中，获取钥匙时使用的salt是"TON default seed"
// 钥匙长度为32
highloadPrivateKey := ed25519.NewKeyFromSeed(k)                      // 获取私钥
highloadPublicKey := highloadPrivateKey.Public().(ed25519.PublicKey) // 从私钥获取公钥

dataCell := cell.BeginCell().
  MustStoreUInt(698983191, 32).           // 子钱包ID
  MustStoreUInt(0, 64).                   // 上次清理时间
  MustStoreSlice(highloadPublicKey, 256). // 公钥
  MustStoreBoolBit(false).                // 表示字典为空
  EndCell()

stateInit := cell.BeginCell().
  MustStoreBoolBit(false). // 无split_depth
  MustStoreBoolBit(false). // 无special
  MustStoreBoolBit(true).  // 我们有代码
  MustStoreRef(codeCell).
  MustStoreBoolBit(true). // 我们有数据
  MustStoreRef(dataCell).
  MustStoreBoolBit(false). // 无库
  EndCell()

contractAddress := address.NewAddress(0, 0, stateInit.Hash()) // 获取stateInit的哈希值以获得我们智能合约在工作链ID为0的地址
log.Println("Contract address:", contractAddress.String())    // 输出合约地址到控制台
```


<TabItem value="go" label="Golang">

```go
import (
  "crypto/ed25519"
  "crypto/hmac"
  "crypto/sha512"
  "github.com/xssnick/tonutils-go/address"
  "golang.org/x/crypto/pbkdf2"
  "strings"
)

highloadMnemonicArray := strings.Split("put your mnemonic that you have generated and saved before", " ") // word1 word2 word3
mac := hmac.New(sha512.New, []byte(strings.Join(highloadMnemonicArray, " ")))
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // In TON libraries "TON default seed" is used as salt when getting keys
// 32 is a key len
highloadPrivateKey := ed25519.NewKeyFromSeed(k)                      // get private key
highloadPublicKey := highloadPrivateKey.Public().(ed25519.PublicKey) // get public key from private key

dataCell := cell.BeginCell().
  MustStoreUInt(698983191, 32).           // Subwallet ID
  MustStoreUInt(0, 64).                   // Last cleaned
  MustStoreSlice(highloadPublicKey, 256). // Public Key
  MustStoreBoolBit(false).                // indicate that the dictionary is empty
  EndCell()

stateInit := cell.BeginCell().
  MustStoreBoolBit(false). // No split_depth
  MustStoreBoolBit(false). // No special
  MustStoreBoolBit(true).  // We have code
  MustStoreRef(codeCell).
  MustStoreBoolBit(true). // We have data
  MustStoreRef(dataCell).
  MustStoreBoolBit(false). // No library
  EndCell()

contractAddress := address.NewAddress(0, 0, stateInit.Hash()) // get the hash of stateInit to get the address of our smart contract in workchain with ID 0
log.Println("Contract address:", contractAddress.String())    // Output contract address to console
```


 

现在，让我们编程高负载钱包同时发送多条消息。例如，让我们每条消息发送12笔交易，这样gas费用就很小。

### Sending High-Load Wallet Transactions

每条消息携带其自己的含代码的评论，目的地址将是我们部署的钱包：

:::info High-load balance
To complete the transaction, the balance of the contract must be at least 0.5 TON.
:::

Each message carry its own comment with code and the destination address will be the wallet from which we deployed:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "fmt"
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/tlb"
  "github.com/xssnick/tonutils-go/tvm/cell"
)

var internalMessages []*cell.Cell
wallletAddress := address.MustParseAddr("put your wallet address from which you deployed high-load wallet")

for i := 0; i < 12; i++ {
  comment := fmt.Sprintf("Hello, TON! #%d", i)
  internalMessageBody := cell.BeginCell().
    MustStoreUInt(0, 32).
    MustStoreBinarySnake([]byte(comment)).
    EndCell()

  internalMessage := cell.BeginCell().
    MustStoreUInt(0x18, 6). // 弹回
    MustStoreAddr(wallletAddress).
    MustStoreBigCoins(tlb.MustFromTON("0.001").NanoTON()).
    MustStoreUInt(0, 1+4+4+64+32).
    MustStoreBoolBit(false). // 我们没有State Init
    MustStoreBoolBit(true). // 我们将消息体存储为引用
    MustStoreRef(internalMessageBody). // 将消息体Init存储为引用
    EndCell()

  messageData := cell.BeginCell().
    MustStoreUInt(3, 8). // 交易mode
    MustStoreRef(internalMessage).
    EndCell()

	internalMessages = append(internalMessages, messageData)
}
```


<TabItem value="go" label="Golang">

```go
import (
  "fmt"
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/tlb"
  "github.com/xssnick/tonutils-go/tvm/cell"
)

var internalMessages []*cell.Cell
wallletAddress := address.MustParseAddr("put your wallet address from which you deployed high-load wallet")

for i := 0; i < 12; i++ {
  comment := fmt.Sprintf("Hello, TON! #%d", i)
  internalMessageBody := cell.BeginCell().
    MustStoreUInt(0, 32).
    MustStoreBinarySnake([]byte(comment)).
    EndCell()

  internalMessage := cell.BeginCell().
    MustStoreUInt(0x18, 6). // bounce
    MustStoreAddr(wallletAddress).
    MustStoreBigCoins(tlb.MustFromTON("0.001").NanoTON()).
    MustStoreUInt(0, 1+4+4+64+32).
    MustStoreBoolBit(false). // We do not have State Init
    MustStoreBoolBit(true). // We store Message Body as a reference
    MustStoreRef(internalMessageBody). // Store Message Body Init as a reference
    EndCell()

  messageData := cell.BeginCell().
    MustStoreUInt(3, 8). // transaction mode
    MustStoreRef(internalMessage).
    EndCell()

	internalMessages = append(internalMessages, messageData)
}
```




After completing the above process, the result is an array of internal messages. Next, it's necessary to create a dictionary for message storage and prepare and sign the message body. This is completed as follows:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "crypto/ed25519"
  "crypto/hmac"
  "crypto/sha512"
  "golang.org/x/crypto/pbkdf2"
  "log"
  "math/big"
  "math/rand"
  "strings"
  "time"
)

dictionary := cell.NewDict(16) // 创建一个空字典，键为数字，值为cell
for i := 0; i < len(internalMessages); i++ {
  internalMessage := internalMessages[i]                             // 从数组中获取消息
  err := dictionary.SetIntKey(big.NewInt(int64(i)), internalMessage) // 在字典中保存消息
  if err != nil {
    return
  }
}

queryID := rand.Uint32()
timeout := 120                                                               // 消息过期的超时时间，120秒 = 2分钟
now := time.Now().Add(time.Duration(timeout)*time.Second).UTC().Unix() << 32 // 获取当前时间戳 + 超时时间
finalQueryID := uint64(now) + uint64(queryID)                                // 获取最终的query_id
log.Println(finalQueryID)                                                    // 打印query_id。使用此query_id我们可以调用GET方法检查请求是否已处理

toSign := cell.BeginCell().
  MustStoreUInt(698983191, 32). // subwallet_id
  MustStoreUInt(finalQueryID, 64).
  MustStoreDict(dictionary)

highloadMnemonicArray := strings.Split("put your high-load wallet mnemonic", " ") // word1 word2 word3
mac := hmac.New(sha512.New, []byte(strings.Join(highloadMnemonicArray, " ")))
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // 在TON库中，“TON default seed”被用作获取密钥时的salt
// 32是密钥长度
highloadPrivateKey := ed25519.NewKeyFromSeed(k) // 获取私钥
highloadWalletAddress := address.MustParseAddr("put your high-load wallet address")

signature := ed25519.Sign(highloadPrivateKey, toSign.EndCell().Hash())
```


<TabItem value="go" label="Golang">

```go
import (
  "crypto/ed25519"
  "crypto/hmac"
  "crypto/sha512"
  "golang.org/x/crypto/pbkdf2"
  "log"
  "math/big"
  "math/rand"
  "strings"
  "time"
)

dictionary := cell.NewDict(16) // create an empty dictionary with the key as a number and the value as a cell
for i := 0; i < len(internalMessages); i++ {
  internalMessage := internalMessages[i]                             // get our message from an array
  err := dictionary.SetIntKey(big.NewInt(int64(i)), internalMessage) // save the message in the dictionary
  if err != nil {
    return
  }
}

queryID := rand.Uint32()
timeout := 120                                                               // timeout for message expiration, 120 seconds = 2 minutes
now := time.Now().Add(time.Duration(timeout)*time.Second).UTC().Unix() << 32 // get current timestamp + timeout
finalQueryID := uint64(now) + uint64(queryID)                                // get our final query_id
log.Println(finalQueryID)                                                    // print query_id. With this query_id we can call GET method to check if our request has been processed

toSign := cell.BeginCell().
  MustStoreUInt(698983191, 32). // subwallet_id
  MustStoreUInt(finalQueryID, 64).
  MustStoreDict(dictionary)

highloadMnemonicArray := strings.Split("put your high-load wallet mnemonic", " ") // word1 word2 word3
mac := hmac.New(sha512.New, []byte(strings.Join(highloadMnemonicArray, " ")))
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // In TON libraries "TON default seed" is used as salt when getting keys
// 32 is a key len
highloadPrivateKey := ed25519.NewKeyFromSeed(k) // get private key
highloadWalletAddress := address.MustParseAddr("put your high-load wallet address")

signature := ed25519.Sign(highloadPrivateKey, toSign.EndCell().Hash())
```




:::note IMPORTANT
Note that while using JavaScript and TypeScript that our messages were saved into an array without using a send mode. This occurs because during using @ton/ton library, it is expected that developer will implement process of serialization and deserialization by own hands. Therefore, a method is passed that first saves the transaction mode after it saves the transaction itself. If we make use of the `Dictionary.Values.Cell()` specification for the value method, it saves the entire message as a cell reference without saving the mode separately.
:::

Next we’ll create an external message and send it to the blockchain using the following code:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import (
  "context"
  "github.com/xssnick/tonutils-go/liteclient"
  "github.com/xssnick/tonutils-go/tl"
  "github.com/xssnick/tonutils-go/ton"
)

body := cell.BeginCell().
  MustStoreSlice(signature, 512). // 存储签名
  MustStoreBuilder(toSign). // 存储我们的消息
  EndCell()

externalMessage := cell.BeginCell().
  MustStoreUInt(0b10, 2). // ext_in_msg_info$10
  MustStoreUInt(0, 2). // src -> addr_none
  MustStoreAddr(highloadWalletAddress). // 目标地址
  MustStoreCoins(0). // 导入费用
  MustStoreBoolBit(false). // 无State Init
  MustStoreBoolBit(true). // 我们以引用形式存储消息体
  MustStoreRef(body). // 以引用形式存储消息体
  EndCell()

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection)

var resp tl.Serializable
err = client.Client().QueryLiteserver(context.Background(), ton.SendMessage{Body: externalMessage.ToBOCWithFlags(false)}, &resp)

if err != nil {
  log.Fatalln(err.Error())
  return
}
```


<TabItem value="go" label="Golang">

```go
import (
  "context"
  "github.com/xssnick/tonutils-go/liteclient"
  "github.com/xssnick/tonutils-go/tl"
  "github.com/xssnick/tonutils-go/ton"
)

body := cell.BeginCell().
  MustStoreSlice(signature, 512). // store signature
  MustStoreBuilder(toSign). // store our message
  EndCell()

externalMessage := cell.BeginCell().
  MustStoreUInt(0b10, 2). // ext_in_msg_info$10
  MustStoreUInt(0, 2). // src -> addr_none
  MustStoreAddr(highloadWalletAddress). // Destination address
  MustStoreCoins(0). // Import Fee
  MustStoreBoolBit(false). // No State Init
  MustStoreBoolBit(true). // We store Message Body as a reference
  MustStoreRef(body). // Store Message Body as a reference
  EndCell()

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection)

var resp tl.Serializable
err = client.Client().QueryLiteserver(context.Background(), ton.SendMessage{Body: externalMessage.ToBOCWithFlags(false)}, &resp)

if err != nil {
  log.Fatalln(err.Error())
  return
}
```




这个教程让我们更好地理解了TON区块链上不同钱包类型的运作方式。它还让我们学会了如何创建外部和内部消息，而不使用预定义的库方法。

## 🏁 Conclusion

This tutorial provided us with a better understanding of how different wallet types operate on TON Blockchain. It also allowed us to learn how to create external and internal messages without using predefined library methods.

阅读上述文档是一项复杂的任务，人们难以完全理解TON平台的全部内容。然而，这对于那些热衷于在TON上建设的人来说是一个很好的练习。另一个建议是开始学习如何在TON上编写智能合约，可以参考以下资源：[FunC概览](https://docs.ton.org/develop/func/overview)，[最佳实践](https://docs.ton.org/develop/smart-contracts/guidelines)，[智能合约示例](https://docs.ton.org/develop/smart-contracts/examples)，[FunC开发手册](https://docs.ton.org/develop/func/cookbook)

## 🧩 Next Steps

Reading the documentation provided above is a complex undertaking and it’s difficult to understand the entirety of the TON platform. However, it is a good exercise for those passionate about building on the TON. Another suggestion is to begin learning about how to write smart contracts on TON by consulting the following resources: [FunC Overview](https://docs.ton.org/develop/func/overview), [Best Practices](https://docs.ton.org/develop/smart-contracts/guidelines), [Examples of Smart Contracts](https://docs.ton.org/develop/smart-contracts/examples), [FunC Cookbook](https://docs.ton.org/develop/func/cookbook)

如果您有任何问题、评论或建议，请通过 [Telegram](https://t.me/aspite) (@aSpite 或 @SpiteMoriarty) 或 [GitHub](https://github.com/aSpite) 联系本文档部分的作者。

## 📖 参阅

If you have any questions, comments, or suggestions please reach out to the author of this documentation section on [Telegram](https://t.me/aspite) (@aSpite or @SpiteMoriarty) or [GitHub](https://github.com/aSpite).

## 📖 See Also

- [@ton/ton (JS/TS)](https://github.com/ton-org/ton)

- [@ton/core (JS/TS)](https://github.com/ton-org/ton-core)

官方文档：

- [内部消息](/develop/smart-contracts/guidelines/internal-messages)
- [外部消息](/develop/smart-contracts/guidelines/external-messages)
- [钱包合约类型](/participate/wallets/contracts#wallet-v4)
- [TL-B](/develop/data-formats/tl-b-language)

外部参考：

- [Ton Deep](https://github.com/xssnick/ton-deep-doc)

- [Block.tlb](https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb)

- [TON中的标准](https://github.com/ton-blockchain/TEPs)

- [TL-B](/develop/data-formats/tl-b-language)

- [Blockchain of Blockchains](https://docs.ton.org/learn/overviews/ton-blockchain)

External references:

- [Ton Deep](https://github.com/xssnick/ton-deep-doc)

- [Block.tlb](https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb)

- [Standards in TON](https://github.com/ton-blockchain/TEPs)
