---
description: 在本教程中，您将学习如何完全使用钱包、交易和智能合约进行工作。
---

import Tabs from'@theme/Tabs';
import TabItem from'@theme/TabItem';

# 使用钱包智能合约的工作

## 👋 介绍

在开始智能合约开发之前，学习 TON 上的钱包和交易如何工作是必不可少的。这些知识将帮助开发者了解钱包、交易和智能合约之间的交互，以实现特定的开发任务。 用于TicTok。这些智能合约会在每个区块自动调用，常规智能合约不需要。关于此的信息可以在[此章节中](/develop/data-formats/transaction-layout#tick-tock)或[tblkch.pdf](https://ton.org/tblkch.pdf) 中找到。此规范中仅存储`0`，因为我们不需要此功能。

在本节中，我们将学习如何创建操作，而不使用预配置的函数，以了解开发工作流程。本教程的所有必要参考资料都位于参考章节。 All references necessary for the analysis of this tutorial are located in the references chapter.

## 💡 必要条件

这个教程需要对 JavaScript、TypeScript 和 Golang 有基本的了解。同时至少需要持有 3 个 TON（可以存储在交易所账户、非托管钱包中，或使用电报机器人钱包进行存储）。此外，还需要对 [cell（单元）](/learn/overviews/cells)、[TON 地址](/learn/overviews/addresses) 和[区块链的区块链](/learn/overviews/ton-blockchain) 有基本的了解，以理解本教程。 It is also necessary to hold at least 3 TON (which can be stored in an exchange account, a non-custodial wallet, or by using the telegram bot wallet). It is necessary to have a basic understanding of [cell](/learn/overviews/cells), [addresses in TON](/learn/overviews/addresses), [blockchain of blockchains](/learn/overviews/ton-blockchain) to understand this tutorial.

:::info 主网开发至关重要
在 TON 测试网上工作往往会导致部署错误、难以跟踪交易以及不稳定的网络功能。因此，完成大部分开发工作时间可能好处是建议在 TON Mainnet 上完成，以避免这些问题，这可能需要减少交易数量，从而可能减小费用。 Therefore, it could be beneficial to complete most development on the TON Mainnet to potentially avoid these issues, which might be necessary to reduce the number of transactions and thereby possibly minimize fees.
:::

## 源代码

本教程中使用的所有代码示例都可以在以下 [GitHub 存储库](https://github.com/aSpite/wallet-tutorial) 中找到。

## ✍️ 您开始所需的内容

- 确保 NodeJS 已安装。
- 需要特定的 Ton 库，包括：@ton/ton 13.5.1+、@ton/core 0.49.2+ 和 @ton/crypto 3.2.0+。

**可选**: 如果您喜欢使用 Golang 而不是使用 JS，那么需要安装 [tonutils-go](https://github.com/xssnick/tonutils-go) 库以及 GoLand IDE，用于进行 TON 开发。本教程中将使用这个库来进行 Golang 版本的操作。 This library will be used in this tutorial for the GO version.

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
为了帮助我们完成下一个流程，我们使用了 `ts-node` 来直接执行 TypeScript 代码，而无需预编译。当检测到目录中的文件更改时，`nodemon` 会自动重新启动节点应用程序。 `nodemon` is used to restart the node application automatically when file changes in the directory are detected.
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
TON 社区创建了一个优秀的工具来自动化所有开发过程（部署、合约编写、测试）称为 [Blueprint](https://github.com/ton-org/blueprint)。然而，我们在本教程中不需要这么强大的工具，所以建议遵循上述说明。 However, we will not be needing such a powerful tool, so it is suggested that the instructions above are followed.
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

:::warning 重要

另外，下面的每个新部分将指定每个新部分所需的特定代码部分，并且需要将新的导入与旧导入合并起来。\
:::\
:::

## 🚀 让我们开始！

在本教程中，我们将学习在 TON 区块链上最常使用的钱包（版本 3 和 4），并了解它们的智能合约是如何工作的。这将使开发人员更好地理解 TON 平台上的不同类型的交易，以便更简单地创建交易、将其发送到区块链、部署钱包，并最终能够处理高负载的钱包。 如我们之前讨论的，普通钱包在每次交易后 seqno 增加 `1`。在使用钱包序列时，我们必须等待这个值更新，然后使用 GET 方法检索它并发送新的交易。
这个过程需要很长时间，高负载钱包不是为此设计的（如上所述，它们旨在快速发送大量交易）。因此，TON上的高负载钱包使用了 `query_id`。

我们的主要任务是使用 @ton/ton、@ton/core、@ton/crypto 的各种对象和函数构建交易，以了解大规模交易是怎样的。为了完成这个过程，我们将使用两个主要的钱包版本（v3 和 v4），因为交易所、非托管钱包和大多数用户仅使用这些特定版本。 to understand what transactions look like on a bigger scale. To carry out this process we'll make use of two main wallet versions (v3 and v4) because of the fact that exchanges, non-custodial wallets, and most users only used these specific versions.

:::note
There may be occasions in this tutorial when there is no explanation for particular details. In these cases, more details will be provided in later stages of this tutorial.

**重要:** 在本教程中，我们使用了 [wallet v3 代码](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet3-code.fc) 来更好地理解钱包开发过程。需要注意的是，v3 版本有两个子版本：r1 和 r2。目前，只使用第二个版本，这意味着当我们在本文档中提到 v3 时，它指的是 v3r2。
::: It should be noted that version v3 has two sub-versions: r1 and r2. Currently, only the second version is being used, this means that when we refer to v3 in this document it means v3r2.
:::

## 💎 TON 区块链钱包

在 TON 区块链上运行的所有钱包实际上都是智能合约，与 TON 上的一切都是智能合约的方式相同。与大多数区块链一样，可以在网络上部署智能合约并根据不同的用途自定义它们。由于这个特性，**完全自定义的钱包是可能的**。
在 TON 上，钱包智能合约帮助平台与其他智能合约类型进行通信。然而，重要的是要考虑钱包通信是如何进行的。 Like most blockchains, it is possible to deploy smart contracts on the network and customize them for different uses. Thanks to this feature, **full wallet customization is possible**.
On TON wallet smart contracts help the platform communicate with other smart contract types. However, it is important to consider how wallet communication takes place.

### 钱包通信

通常，在 TON 区块链上有两种交易类型：`internal` 和 `external`。外部交易允许从外部世界向区块链发送消息，从而与接受此类交易的智能合约进行通信。负责执行此过程的函数如下： External transactions allow for the ability to send messages to the blockchain from the outside world, thus allowing for the communication with smart contracts that accept such transactions. The function responsible for carrying out this process is as follows:

```func
() recv_external(slice in_msg) impure {
    ;; 一些代码
}
```

Before we dive into more details concerning wallets, let’s look at how wallets accept external transactions. On TON, all wallets hold the owner’s `public key`, `seqno`, and `subwallet_id`. When receiving an external transaction, the wallet uses the `get_data()` method to retrieve data from the storage portion of the wallet. It then conducts several verification procedures and decides whether to accept the transaction or not. 位运算

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

> 💡 有用的链接：
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

Now let’s take a closer look.

### 重放保护 - Seqno

Transaction replay protection in the wallet smart contract is directly related to the transaction seqno (Sequence Number) which keeps track of which transactions are sent in which order. It is very important that a single transaction is not repeated from a wallet because it throws off the integrity of the system entirely. If we further examine smart contract code within a wallet, the `seqno` is typically handled as follows:

```func
throw_unless(33, msg_seqno == stored_seqno);
```

上述代码将检查在交易中获得的 `seqno` 是否与存储在智能合约中的 `seqno` 相匹配。如果不匹配，则合约返回带有 `33 exit code` 的错误。因此，如果发送者传递了无效的 `seqno`，则意味着他在交易序列中犯了一些错误，合约保护了这些情况。 The contract returns an error with `33 exit code` if they do not match. So if the sender passed invalid seqno, it means that he made some mistake in the transaction sequence, and the contract protects against such cases.

:::note
It's also essential to consider that external messages can be sent by anyone. This means that if you send 1 TON to someone, someone else can repeat this message. However, when the seqno increases, the previous external message becomes invalid, and no one will be able to repeat it, thus preventing the possibility of stealing your funds.
:::

### 签名

As mentioned earlier, wallet smart contracts accept external transactions. However, these transactions come from the outside world and that data cannot be 100% trusted. Therefore, each wallet stores the owner's public key. The smart contract uses a public key to verify the legitimacy of the transaction signature when receiving an external transaction that the owner signed with the private key. This verifies that the transaction is actually from the contract owner.

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
Because the transaction comes from the outside world, it does not contain the Toncoin required to pay the transaction fee. 由于交易来自外部世界，它不包含支付交易费用所需的 Toncoin。在使用 accept_message() 函数发送 TON 时，应用gas_credit（在写入时其值为10,000 gas单位），并且只要gas不超过 gas_credit 值，就允许免费进行必要的计算。使用 accept_message() 函数后，从智能合约的账户余额中收取所有已花费的gas（以 TON 计）。可以在[此处](/develop/smart-contracts/guidelines/accept)了解有关此过程的更多信息。 发送交易时，在处理智能合约期间可能发生各种错误。为了避免失去 TON，需要将 Bounce 选项设置为 1（true）。在这种情况下，如果在交易处理过程中发生任何合约错误，该交易将返回给发送者，并会收到总量减去手续费的 TON。有关无法反弹的消息的更多信息，请参阅 [此处](/develop/smart-contracts/guidelines/non-bouncable-messages)。 More can be read about this process [here](/develop/smart-contracts/guidelines/accept).
:::

### 交易过期

用于检查外部交易的有效性的另一步是 `valid_until` 字段。从变量名称可以看出，这是交易在 UNIX 中在有效之前的时间。如果此验证过程失败，则合约完成交易处理并返回 32 退出码，如下所示： As you can see from the variable name, this is the time in UNIX before the transaction is valid. If this verification process fails, the contract completes the processing of the transaction and returns the 32 exit code follows:

```func
var (subwallet_id, valid_until, msg_seqno) = (cs~load_uint(32), cs~load_uint(32), cs~load_uint(32));
throw_if(35, valid_until <= now());
```

此算法用于在交易不再有效但仍然以未知原因发送到区块链时，防范各种错误的易受攻击性。

### 钱包 v3 和钱包 v4 的区别

钱包 v3 和钱包 v4 之间的唯一区别是钱包 v4 使用可以安装和删除的 `插件`。插件是特殊的智能合约，可以从钱包智能合约请求在特定时间从指定数量的 TON 中。钱包智能合约将相应地发送所需数量的 TON，而无需所有者参与。这类似于为插件创建的 **订阅模型**。我们不会在本教程中详细介绍这些细节，因为这超出了本教程的范围。 These plugins are special smart contracts which are able to request a specific number of TON at a specific time from a wallet smart contract.

Wallet smart contracts, in turn, will send the required amount of TON in response without the need for the owner to participate. This is similar to the **subscription model** for which plugins are created. We will not learn these details, because this is out of the scope of this tutorial.

### 钱包如何促进与智能合约的交流

如前所述，钱包智能合约接受外部交易。然而，这些交易来自外部世界，这些数据不能 100% 可信。因此，每个钱包都存储所有者的公钥。当钱包接收到所有者使用私钥签名的外部交易时，智能合约使用公钥验证交易签名的合法性。这样可以验证交易实际上是来自合约所有者的。 正如我们之前讨论的那样，钱包智能合约接受外部交易，验证它们，如果通过了所有检查，则接受它们。然后，合约开始从外部消息的主体中检索消息，然后创建内部消息并将其发送到区块链，如下所示：

```func
cs~touch();
while (cs.slice_refs()) {
    var mode = cs~load_uint(8); ;; 加载交易模式
    send_raw_message(cs~load_ref(), mode); ;; 使用 load_ref() 将每一个新的内部消息作为一个带有 load_ref() 的cell，并发送它
}
```

:::tip touch()
在 TON 上，所有智能合约都在基于堆栈的 TON 虚拟机（TVM）上运行。~ touch() 将变量 `cs` 放置在堆栈的顶部，以优化代码运行以节省 gas。 ~ touch() places the variable `cs` on top of the stack to optimize the running of code for less gas.
:::

由于一个cell中最多可以存储 4 个引用，我们可以每个外部消息发送最多 4 个内部消息。

> 💡 有用的链接：
>
> [slice_refs()](/develop/func/stdlib/#slice_refs)
>
> [send_raw_message() and transaction modes](/develop/func/stdlib/#send_raw_message)
>
> [load_ref()](/develop/func/stdlib/#load_ref)

## 📬 外部和内部交易

在本节中，我们将学习有关 `internal` 和 `external` 交易的更多信息，并创建交易并将其发送到网络中以尽量减少使用预先创建的函数。

为了完成此过程，需要使用一个预先制作的钱包使任务变得更容易。为此： To accomplish this:

1. 安装 [wallet 应用程序](/participate/wallets/apps)（例如，Tonkeeper 是作者使用的）。
2. 将钱包应用切换到 v3r2 地址版本。
3. 向钱包存入 1 TON。
4. 将交易发送到另一个地址（可以发送给自己，发送到同一个钱包）。

这样，Tonkeeper 钱包应用程序将部署钱包合约，我们可以在以下步骤中使用它。

:::note
在撰写本文时，TON 上的大多数钱包应用程序默认使用钱包 v4 版本。在本教程中，不需要使用插件的功能，因此我们将使用钱包 v3 提供的功能。在使用过程中，Tonkeeper 允许用户选择他们想要的钱包版本。因此，建议部署钱包版本 3（wallet v3）。 Plugins are not required in this tutorial and we’ll make use of the functionality provided by wallet v3. During use, Tonkeeper allows the user to choose the version of the wallet they want. Therefore, it is recommended to deploy wallet version 3 (wallet v3).
:::

### TL-B

As noted, everything in TON Blockchain is a smart contract consisting of cells. To properly serialize and deserialize the data we need standards. To accomplish the serialization and deserialization process, `TL-B` was created as a universal tool to describe different data types in different ways with different sequences inside cells.

在本节中，我们将详细研究 [block.tlb](https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb)。在将来的开发中，此文件将非常有用，因为它描述了不同cell的组装方式。在我们的情况下，它详细描述了内部和外部交易的复杂性。 This file will be very useful during future development, as it describes how different cells should be assembled. In our case specifically, it details the intricacies of internal and external transactions.

:::info
Basic information will be provided within this guide. 本指南将提供基本信息。有关更多详细信息，请参阅我们的 TL-B [文档](/develop/data-formats/tl-b-language)，以了解更多关于 TL-B 的知识。
:::

### CommonMsgInfo

首先，每个消息必须首先存储 `CommonMsgInfo`（[TL-B](https://github.com/ton-blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L123-L130)）或 `CommonMsgInfoRelaxed`（[TL-B](https://github.com/ton-blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L132-L137)）。这允许我们定义与交易类型、交易时间、接收者地址、技术标志位和费用相关的技术细节。 This allows us to define technical details that relate to the transaction type, transaction time, recipient address, technical flags, and fees.

通过阅读 `block.tlb` 文件，我们可以注意到 CommonMsgInfo有三种不同的类型：`int_msg_info$0`、`ext_in_msg_info$10`、`ext_out_msg_info$11`。我们将不对 `ext_out_msg_info` 的 TL-B 结构的具体细节进行详细解释。但需要注意的是，它是由智能合约发送的外部交易类型，用作外部日志。要查看此格式的示例，请仔细查看 [Elector](https://tonscan.org/address/Ef8zMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM0vF) 合约。 We will not go into specific details detailing the specificities of the `ext_out_msg_info` TL-B structure. That said, it is an external transaction type that a smart contract can send for using as external logs. For examples of this format, consider having a closer look at the [Elector](\(https://tonscan.org/address/Ef8zMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM0vF\)) contract.

您可以从 [TL-B](https://github.com/ton-blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L127-L128) 中看到，**仅在与 ext_in_msg_info 类型一起使用时才可以使用 CommonMsgInfo**。因为交易类型字段，如 `src`、`created_lt`、`created_at` 等，由验证者在交易处理期间进行重写。在这种情况下，`src` 交易类型最重要，因为当发送交易时，发送者是未知的，验证者在验证期间对其在 `src` 字段中的地址进行重写。这样确保 `src` 字段中的地址是正确的，并且不能被操纵。 This is because transaction type fields such as `src`, `created_lt`, `created_at`, and others are rewritten by validators during transaction handling. In this case, the `src` transaction type is most important because when transactions are sent, the sender is unknown, and is written by validators during verification. This ensures that the address in the `src` field is correct and cannot be manipulated.

但是，`CommonMsgInfo` 结构仅支持 `MsgAddress` 规格，但通常情况下发送方的地址是未知的，并且需要写入 `addr_none`（两个零位 `00`）。在这种情况下，使用 `CommonMsgInfoRelaxed` 结构，该结构支持 `addr_none` 地址。对于 `ext_in_msg_info`（用于传入的外部消息），使用 `CommonMsgInfo` 结构，因为这些消息类型不使用sender，始终使用 [MsgAddressExt](https://hub.com/ton/ton.blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L100) 结构（`addr_none$00` 表示两个零位），因此无需覆盖数据。 In this case, the `CommonMsgInfoRelaxed` structure is used, which supports the `addr_none` address. `0b10` (b表示二进制）表示一个二进制记录。在此过程中，存储了两个位：`1` 和 `0`，因此我们指定为 `ext_in_msg_info$10`。

:::note
`$`符号后面的数字是在某个结构的开始处所要求存储的位，以便在读取时（反序列化）可进一步识别这些结构。
:::

### 创建内部交易

Internal transactions are used to send messages between contracts. 内部交易用于在合约之间发送消息。当分析发送使用合约进行编写的各种合约类型（例如 [NFTs](https://github.com/ton-blockchain/token-contract/blob/f2253cb0f0e1ae0974d7dc0cef3a62cb6e19f806/nft/nft-item.fc#L51-L56) 和 [Jetons](https://github.com/ton-blockchain/token-contract/blob/f2253cb0f0e1ae0974d7dc0cef3a62cb6e19f806/ft/jetton-wallet.fc#L139-L144)），常常会使用以下代码行：

```func
var msg = begin_cell()
  .store_uint(0x18, 6) ;; 或者 0x10 代表不可弹回
  .store_slice(to_address)
  .store_coins(amount)
  .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; 默认的消息头（请参阅发送消息页面）
  ;; 作为存储体
```

让我们首先考虑 `0x18` 和 `0x10`（x - 16 进制），这些十六进制数是按以下方式排列的（考虑到我们分配了 6 个位）：`011000` 和 `010000`。这意味着，可以将上述代码重写为以下内容： This means that the code above can be overwritten as follows:

```func
var msg = begin_cell()
  .store_uint(0, 1) ;; 这个位表示我们发送了一个内部消息，与 int_msg_info$0 对应
  .store_uint(1, 1) ;; IHR 禁用
  .store_uint(1, 1) ;; 或者 .store_uint(0, 1) 对于 0x10 | 退回
  .store_uint(0, 1) ;; 退回
  .store_uint(0, 2) ;; src -> 两个零位代表 addr_none
  .store_slice(to_address)
  .store_coins(amount)
  .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; 默认的消息头（请参阅发送消息页面）
  ;; 作为存储体
```

现在我们来详细解释每个选项：

|      选项      |                                                                                                                                                                                                                                                                               说明                                                                                                                                                                                                                                                                               |
| :----------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| IHR Disabled |                               Currently, this option is disabled (which means we store 1) because Instant Hypercube Routing is not fully implemented. In addition, this will be needed when a large number of [Shardchains](/learn/overviews/ton-blockchain#many-accountchains-shards) are live on the network. More can be read about the IHR Disabled option in the [tblkch.pdf](https://ton.org/tblkch.pdf) (chapter 2).                              |
|    Bounce    | While sending transactions, a variety of errors can occur during smart contract processing. To avoid losing TON, it is necessary to set the Bounce option to 1 (true). In this case, if any contract errors occur during transaction processing, the transaction will be returned to the sender, and the same amount of TON will be received minus fees. More can be read about non-bounceable messages [here](/develop/smart-contracts/guidelines/non-bouncable-messages). |
|    Bounced   |                                                                                                                                                                                                          弹回交易是发送者返回的交易，因为在处理交易时与智能合约发生了错误。此选项告诉您接收到的交易是否被弹回。 This option tells you whether the transaction received is bounced or not.                                                                                                                                                                                                         |
|      Src     |                                                                                                                                                                                         Src 是发送者地址。在这种情况下，写入了两个零位以指示 `addr_none` 地址。 为了更好地理解，让我们使用 `1625918400` 作为时间戳的示例。它的二进制表示（左侧添加零以得到 32 位）是 01100000111010011000101111000000。执行 32 位位左移操作后，我们数字的二进制表示末尾会出现 32 个零。                                                                                                                                                                                         |

接下来的两行代码:

```func
...
.store_slice(to_address)
.store_coins(amount)
...
```

- 我们指定了接收方和要发送的 TON 数量。

最后，我们来看剩下的代码行：

```func
...
  .store_uint(0, 1) ;; Extra currency
  .store_uint(0, 4) ;; IHR fee
  .store_uint(0, 4) ;; Forwarding fee
  .store_uint(0, 64) ;; Logical time of creation
  .store_uint(0, 32) ;; UNIX time of creation
  .store_uint(0, 1) ;; State Init
  .store_uint(0, 1) ;; Message body
  ;; 作为存储体
```

|            选项            |                                                                                                                                                                                             说明                                                                                                                                                                                            |
| :----------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|      Extra currency      |                                                                                                                                                                                这是现有 jettons 的本地实现，目前没有在使用中。                                                                                                                                                                               |
|          IHR fee         |                                                                                                                      如前所述，目前未使用 IHR，因此该费用始终为零。更多信息请参阅 [tblkch.pdf](https://ton.org/tblkch.pdf)（3.1.8）。 接下来，我们来详细看一下。                                                                                                                      |
|      Forwarding fee      |                                                                                                                                 A forwarding message fee. 转发消息费用。有关更多信息，请参阅 [费用文档](/develop/howto/fees-low-level#transactions-and-phases)。                                                                                                                                |
| Logical time of creation |                                                                                                                                                                                      用于创建正确的交易队列的时间。                                                                                                                                                                                      |
|   UNIX time of creation  |                                                                                                                                                                                      交易在 UNIX 中的创建时间。                                                                                                                                                                                     |
|        State Init        |                                                        Code and source data for deploying a smart contract. If the bit is set to `0`, it means that we do not have a State Init. 用于部署智能合约的代码和源数据。如果此位设为 `0`，则表示我们没有 State Init。但如果设为 `1`，则需要写入另一个位，该位指示 State Init 是否存储在同一个cell中（`0`）或作为引用写入（`1`）。                                                        |
|       Message body       | This part defines how the message body is stored. At times the message body is too large to fit into the message itself. In this case, it should be stored as a **reference** whereby the bit is set to `1` to show that the body is used as a reference. If the bit is `0`, the body is in the same cell as the message. |

上述值（包括 Src）具有以下特征，但不包括 State Init 和 Message Body 位，由验证者重写。

:::note
If the number value fits within fewer bits than is specified, then the missing zeros are added to the left side of the value. For example, 0x18 fits within 5 bits -> `11000`. However, since 6 bits were specified, the end result becomes `011000`.
:::

接下来，我们将开始准备一个交易，该交易将向另一个钱包 v3 发送 Toncoins。首先，假设用户想要向自己发送 0.5 TON，并附带文本“**你好，TON！**”，请参阅本文档的这一部分来了解[如何发送带有评论的消息](/develop/func/cookbook#how-to-send-a-simple-message)。
First, let’s say a user wants to send 0.5 TON to themselves with the text "**Hello, TON!**", refer to this section of our documentation to learn ([How to send message with a comment](/develop/func/cookbook#how-to-send-a-simple-message)).

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { beginCell } from'@ton/core';

let internalMessageBody = beginCell().
  storeUint(0, 32). // 写入 32 个零位以指示接下来将有文本注释
  storeStringTail("你好，TON！"). // 写入我们的文本注释
  endCell();
```


<TabItem value="go" label="Golang">

```go
import (
	"github.com/xssnick/tonutils-go/tvm/cell"
)

internalMessageBody := cell.BeginCell().
  MustStoreUInt(0, 32). // 写入 32 个零位以指示接下来将有文本注释
  MustStoreStringSnake("你好，TON！"). // 写入我们的文本注释
  EndCell()
```




Above we created an `InternalMessageBody` in which the body of our message is stored. Note that when storing text that does not fit into a single Cell (1023 bits), it is necessary **to split the data into several cells** according to [the following documentation](/develop/smart-contracts/guidelines/internal-messages). However, in this case the high-level libraries creates cells according to requirements, so at this stage there is no need to worry about it.

接下来，根据我们之前学习的信息，创建 `InternalMessage` 如下所示：

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { toNano, Address, beginCell } from'@ton/ton';

const walletAddress = Address.parse('把你的钱包地址放这里');

let internalMessage = beginCell().
  storeUint(0, 1). // 表示它是一条内部消息 -> int_msg_info$0
  storeBit(1). // 禁用 IHR 
  storeBit(1). // bounce
  storeBit(0). // bounced
  storeUint(0, 2). // src -> addr_none
  storeAddress(walletAddress).
  storeCoins(toNano("0.2")). // 金额
  storeBit(0). // Extra currency
  storeCoins(0). // IHR 费用
  storeCoins(0). // Forwarding 费用
  storeUint(0, 64). // 创建的逻辑时间
  storeUint(0, 32). // 创建的 UNIX 时间
  storeBit(0). // 没有 State Init
  storeBit(1). // 我们将 Message Body 存储为引用
  storeRef(internalMessageBody). // 将 Message Body 存储为引用
  endCell();
```


<TabItem value="go" label="Golang">

```go
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




### 创建消息

It is necessary to retrieve the `seqno` (sequence number) of our wallet smart contract. To accomplish this, a `Client` is created which will be used to send a request to run the Get method "seqno" of our wallet. 有必要检索我们的钱包智能合约的`seqno`（序列号）。为此，我们创建了一个`Client`，用于发送请求以运行我们的钱包的Get方法“seqno”。还需要添加种子短语（在创建钱包时保存的种子短语）以通过以下步骤对我们的交易进行签名：

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { TonClient } from '@ton/ton';
import { mnemonicToWalletKey } from '@ton/crypto';

const client = new TonClient({
  endpoint: "https://toncenter.com/api/v2/jsonRPC",
  apiKey: "put your api key" // you can get an api key from @tonapibot bot in Telegram
});

const mnemonic = 'put your mnemonic'; // word1 word2 word3
let getMethodResult = await client.runMethod(walletAddress, "seqno"); // run "seqno" GET method from your wallet contract
let seqno = getMethodResult.stack.readNumber(); // get seqno from response

const mnemonicArray = mnemonic.split(' '); // get array from string
const keyPair = await mnemonicToWalletKey(mnemonicArray); // get Secret and Public keys from mnemonic 
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




Therefore, the `seqno`, `keys`, and `internal message` need to be sent. 因此，需要发送`seqno`，`keys` 和 `internal message`。现在需要为我们的钱包创建一条 [message](/develop/smart-contracts/messages)，并将数据存储在此消息中以在教程开始时使用的序列中。操作步骤如下： This is accomplished as follows:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { sign } from '@ton/crypto';

let toSign = beginCell().
  storeUint(698983191, 32). // subwallet_id | We consider this further
  storeUint(Math.floor(Date.now() / 1e3) + 60, 32). // Transaction expiration time, +60 = 1 minute
  storeUint(seqno, 32). // store seqno
  storeUint(3, 8). // store mode of our internal transaction
  storeRef(internalMessage); // store our internalMessage as a reference

let signature = sign(toSign.endCell().hash(), keyPair.secretKey); // get the hash of our message to wallet smart contract and sign it to get signature

let body = beginCell().
  storeBuffer(signature). // store signature
  storeBuilder(toSign). // store our message
  endCell();
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
  MustStoreUInt(3, 8). // store mode of our internal transaction
  MustStoreRef(internalMessage) // store our internalMessage as a reference

signature := ed25519.Sign(privateKey, toSign.EndCell().Hash()) // get the hash of our message to wallet smart contract and sign it to get signature

body := cell.BeginCell().
  MustStoreSlice(signature, 512). // store signature
  MustStoreBuilder(toSign). // store our message
  EndCell()
```




注意，这里在`toSign`的定义中没有使用 `.endCell()`。事实上，在这种情况下，**需要将`toSign`的内容直接传递给消息主体**。如果需要编写cell，必须将其保存为引用。 The fact is that in this case it is necessary **to transfer toSign content directly to the message body**. If writing a cell was required, it would have to be stored as a reference.

:::tip 钱包 V4
除了我们在钱包 V3中所学习到的基本验证流程，钱包 V4智能合约提取了操作码以确定是否需要简单转换或与插件相关的交易。为了匹配这个版本，需要在写入seqno（序列号）之后并在指定交易模式之前添加 `storeUint(0, 8).`（JS/TS），`MustStoreUInt(0, 8).`（Golang）函数。 To match this version, it is necessary to add the `storeUint(0, 8).` (JS/TS), `MustStoreUInt(0, 8).` (Golang) functions after writing the seqno (sequence number) and before specifying the transaction mode.
:::

### 外部交易的创建

要从外部世界将任何内部消息传递到区块链中，需要将其包含在外部交易中发送。正如我们之前讨论的那样，仅需要使用 `ext_in_msg_info$10` 结构，因为目标是将外部消息发送到我们的合约中。现在，我们创建一个外部消息，将发送到我们的钱包： As we have previously considered, it is necessary to only make use of the `ext_in_msg_info$10` structure, as the goal is to send an external message to our contract. 还需要确认外部消息可以由任何人发送。这意味着如果您向某人发送 1 TON，其他人也可以重复该消息。但是，当 seqno 增加时，以前的外部消息失效，并且没有人可以重复该消息，从而防止窃取您的资金。

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
let externalMessage = beginCell().
  storeUint(0b10, 2). // 0b10 -> 10 in binary
  storeUint(0, 2). // src -> addr_none
  storeAddress(walletAddress). // Destination address
  storeCoins(0). // Import Fee
  storeBit(0). // No State Init
  storeBit(1). // We store Message Body as a reference
  storeRef(body). // Store Message Body as a reference
  endCell();
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




|      选项      |                                                                                                                        说明                                                                                                                       |
| :----------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|      Src     | The sender address. 发送者地址。因为传入的外部消息不能有发送者，所以始终存在2个零位（`\u0000`）数据类型的数组（addr_none [TL-B](https://github.com/ton-blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L100)）。 |
|  Import Fee  |                                                                                                               用于支付导入传入的外部消息的费用的费用。                                                                                                              |
|  State Init  |                     和内部消息不同，外部消息中的State Init需要**从外部世界部署合约**。将State Init与内部消息一起使用，可以使一个合约可以部署另一个合约。 主要的区别将在外部消息的存在上，因为State Init被存储用于正确的合约部署。由于合约尚无自己的代码，因此无法处理任何内部消息。因此，接下来，我们将在成功部署后发送其代码和初始数据，以便可处理我们带有“Hello, TON！”评论的消息：                    |
| Message Body |                                                                                                                 必须发送到合约以进行处理的消息。                                                                                                                |

:::tip `0b10`
0b10 (b - binary) denotes a binary record. In this process, two bits are stored: `1` and `0`. Thus we specify that it's `ext_in_msg_info$10`.
:::

Now we have a completed message that is ready to be sent to our contract. 现在我们有一条准备好发送给我们的合约的消息。为此，首先需要将其序列化为 `BOC`（[cell集合](/develop/data-formats/cell-boc#bag-of-cells)），然后使用以下代码将其发送：

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
console.log(externalMessage.toBoc().toString("base64"))

client.sendFile(externalMessage.toBoc());
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




> 💡 有用的链接：
>
> [更多关于cell集合的信息](/develop/data-formats/cell-boc#bag-of-cells)

As a result, we got the output of our BOC in the console and the transaction sent to our wallet. 结果是，在控制台上得到了我们Boc的输出，并将交易发送到我们的钱包。您可以复制 base64 编码的字符串，然后可以[手动发送我们的交易并使用 toncenter 检索哈希](https://toncenter.com/api/v2/#/send/send_boc_return_hash_sendBocReturnHash_post)。

## 👛 部署钱包

我们已经学会了创建消息的基础知识，这对于部署钱包非常有帮助。 以前，我们通过钱包应用程序部署钱包，但在这种情况下，我们将需要手动部署钱包。 In the past, we have deployed wallet via wallet app, but in this case we’ll need to deploy our wallet manually.

下面我们将了解 V3 和 V4 钱包使用的 GET 方法的基础知识： 在这个阶段，智能合约`代码`和`初始数据`都存在。有了这些数据，我们可以生成我们的**钱包地址**。钱包的地址取决于State Init，其中包括代码和初始数据。

### 生成助记词

正确定义钱包所需的第一件事是检索`private`和`public`密钥。为了完成这个任务，需要生成助记词种子短语，然后使用加密库提取私钥和公钥。 To accomplish this task it is necessary to generate a mnemonic seed phrase and then extract private and public keys using cryptographic libraries.

This is accomplished as follows:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { mnemonicToWalletKey, mnemonicNew } from '@ton/crypto';

// const mnemonicArray = 'put your mnemonic'.split(' ') // get our mnemonic as array
const mnemonicArray = await mnemonicNew(24); // 24 is the number of words in a seed phrase
const keyPair = await mnemonicToWalletKey(mnemonicArray); // extract private and public keys from mnemonic
console.log(mnemonicArray) // if we want, we can print our mnemonic
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




私钥用于签署交易，公钥存储在钱包的智能合约中。

:::danger 注意
需要将生成的助记词种子短语输出到控制台，然后保存和使用它（如前面的部分中所述），以便每次运行钱包代码时都使用同一对密钥。
:::

### 子钱包 ID

钱包作为智能合约的最显着优势之一是能够仅使用一个私钥创建**大量的钱包**。这是因为TON区块链上的智能合约地址是使用多个因素计算出来的，其中包括`stateInit`。stateInit包含了`代码`和`初始数据`，这些数据存储在区块链的智能合约存储中。 This is because the addresses of smart contracts on TON Blockchain are computed using several factors including the `stateInit`. The stateInit contains the `code` and `initial data`, which is stored in the blockchain’s smart contract storage.

By changing just one bit within the stateInit, a different address can be generated. That is why the `subwallet_id` was initially created. 通过在stateInit中只更改一个位，可以生成一个不同的地址。这就是为什么最初创建了`subwallet_id`。`subwallet_id`存储在合约存储中，可以用于使用一个私钥创建许多不同的钱包（具有不同的子钱包ID）。当将不同钱包类型与交易所等集中服务集成时，这种功能非常有用。 This functionality can be very useful when integrating various wallet types with centralized service such as exchanges.

根据TON区块链的源代码中的[代码行](https://github.com/ton-blockchain/ton/blob/4b940f8bad9c2d3bf44f196f6995963c7cee9cc3/tonlib/tonlib/TonlibClient.cpp#L2420)，默认的`subwallet_id`值为`698983191`：

```cpp
res.wallet_id = td::as<td::uint32>(res.config.zero_state_id.root_hash.as_slice().data());
```

可以从[配置文件](https://ton.org/global-config.json)中获取创世块信息（zero_state）。了解其复杂性和细节并非必要，但重要的是要记住`subwallet_id`的默认值为`698983191`。 Understanding the complexities and details of this is not necessary but it's important to remember that the default value of the `subwallet_id` is `698983191`.

每个钱包合约都会检查外部交易的subwallet_id字段，以避免将请求发送到具有不同ID的钱包的情况：

```func
var (subwallet_id, valid_until, msg_seqno) = (cs~load_uint(32), cs~load_uint(32), cs~load_uint(32));
var (stored_seqno, stored_subwallet, public_key) = (ds~load_uint(32), ds~load_uint(32), ds~load_uint(256));
throw_unless(34, subwallet_id == stored_subwallet);
```

我们需要将以上的值添加到合约的初始数据中，所以变量需要保存如下：

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
const subWallet = 698983191;
```


<TabItem value="go" label="Golang">

```go
var subWallet uint64 = 698983191
```




### 编译钱包代码

在我们深入研究钱包之前，让我们先看看钱包如何接受外部交易。在 TON 上，所有钱包都持有所有者的 `公钥`、`seqno` 和 `subwallet_id`。接收到外部交易时，钱包使用 `get_data()` 方法从钱包的存储部分中检索数据。然后进行多个验证流程，并决定是否接受此交易。这个过程的完成如下： 既然我们已经明确定义了私钥、公钥和子钱包ID，我们需要编译钱包代码。为此，我们将使用官方库中的[钱包v3代码](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet3-code.fc)。

为了编译钱包代码，我们需要使用[@ton-community/func-js](https://github.com/ton-community/func-js)库。使用这个库，我们可以编译FunC代码并检索包含代码的cell。要开始使用，需要安装库并将其保存（--save）到`package.json`中，如下所示：
Using this library it allows us to compile FunC code and retrieve a cell containing the code. To get started, it is necessary to install the library and save (--save) it to the `package.json` as follows:

```bash
npm i --save @ton-community/func-js
```

我们将仅使用JavaScript来编译代码，因为用于编译代码的库基于JavaScript。
但是，一旦编译完成，只要我们拥有编译后的cell的**base64输出**，就可以在其他编程语言（如Go等）中使用这些编译后的代码。
结果，在右侧的数字上添加了 32 位。这意味着 **现有值向左移动 32 位**。举例来说，让我们考虑数字 3 并将其翻译成二进制形式，结果是 11。应用 `3 << 2` 操作，11 移动了 2 位。这意味着在字符串的右侧添加了两位。最后，我们得到了 1100，即 12。

First, we need to create two files: `wallet_v3.fc` and `stdlib.fc`. The compiler works with the stdlib.fc library. All necessary and basic functions, which correspond with the `asm` instructions were created in the library. 首先，我们需要创建两个文件：`wallet_v3.fc`和`stdlib.fc`。编译器和stdlib.fc库一起使用。库中创建了所有必需的基本函数，这些函数对应于`asm`指令。可以从[这里](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/stdlib.fc)下载stdlib.fc文件。在`wallet_v3.fc`文件中，需要复制上面的代码。 In the  `wallet_v3.fc` file it is necessary to copy the code above.

现在，我们为我们正在创建的项目有了以下结构：

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
如果您的IDE插件与`stdlib.fc`文件中的`() set_seed(int) impure asm "SETRAND";`冲突，这没关系。
:::

请记住，在`wallet_v3.fc`文件的开头添加以下行，以指示将在下面使用stdlib中的函数：

```func
#include "stdlib.fc";
```

现在，让我们编写代码来编译我们的智能合约并使用`npm run start:dev`来运行它：

```js
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

```text
Code BOC: te6ccgEBCAEAhgABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQCW8oMI1xgg0x/TH9MfAvgju/Jj7UTQ0x/TH9P/0VEyuvKhUUS68qIE+QFUEFX5EPKj+ACTINdKltMH1AL7AOgwAaTIyx/LH8v/ye1UAATQMAIBSAYHABe7Oc7UTQ0z8x1wv/gAEbjJftRNDXCx+A==

Hash: idlku00WfSC36ujyK2JVT92sMBEpCNRUXOGO4sJVBPA=
```

完成后，可以使用其他库和语言使用我们的钱包代码检索相同的cell（使用base64编码的输出）：

<Tabs groupId="code-examples">
<TabItem value="go" label="Golang">

```go
import (
  "encoding/base64"
  "github.com/xssnick/tonutils-go/tvm/cell"
)

base64BOC := "te6ccgEBCAEAhgABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQCW8oMI1xgg0x/TH9MfAvgju/Jj7UTQ0x/TH9P/0VEyuvKhUUS68qIE+QFUEFX5EPKj+ACTINdKltMH1AL7AOgwAaTIyx/LH8v/ye1UAATQMAIBSAYHABe7Oc7UTQ0z8x1wv/gAEbjJftRNDXCx+A==" // 保存我们从编译器保存的base64编码输出到变量
codeCellBytes, _ := base64.StdEncoding.DecodeString(base64BOC) // 解码base64以获取字节数组
codeCell, err := cell.FromBOC(codeCellBytes) // 从字节数组获取包含代码的cell
if err != nil { // 检查是否有任何错误
  panic(err) 
}

log.Println("Hash:", base64.StdEncoding.EncodeToString(codeCell.Hash())) // 获取cell的哈希，将其编码为base64，因为它具有[]byte类型，并输出到终端
```




将会在终端输出以下内容：

```text
idlku00WfSC36ujyK2JVT92sMBEpCNRUXOGO4sJVBPA=
```

完成上述过程后，确认我们的cell中正在使用正确的代码，因为哈希值相匹配。

### 创建部署的初始化状态

Before building a transaction it is important to understand what a State Init is. 在构建交易之前，了解State Init非常重要。首先让我们了解[TL-B方案](https://github.com/ton-blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L141-L143)：

|                选项                |                                                                                                                                                                                                                                                                      说明                                                                                                                                                                                                                                                                     |
| :------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| split_depth | 此选项适用于可以拆分并位于多个[分片链](/learn/overviews/ton-blockchain#many-accountchains-shards)上的高负载智能合约。有关此工作原理的更多详细信息，请参见[tblkch.pdf](https://ton.org/tblkch.pdf)（4.1.6）。只存储`0`，因为它仅在钱包智能合约内使用。  More information detailing how this works can be found in the [tblkch.pdf](https://ton.org/tblkch.pdf) (4.1.6).  Only a `0` bit is stored since it is being used only within a wallet smart contract. |
|              special             |        Used for TicTok. These smart contracts are automatically called for each block and are not needed for regular smart contracts. Information about this can be found in [this section](/develop/data-formats/transaction-layout#tick-tock) or in [tblkch.pdf](https://ton.org/tblkch.pdf) (4.1.6). Only a `0` bit is stored within this specification because we do not need such a function.       |
|               code               |                                                                                                                                                                                                                                                               `1`位表示智能合约代码的存在。                                                                                                                                                                                                                                                              |
|               data               |                                                                                                                                                                                                                                                               `1`位表示智能合约数据的存在。                                                                                                                                                                                                                                                              |
|              library             |                            操作[主链](/learn/overviews/ton-blockchain#masterchain-blockchain-of-blockchains)上的库，可以由不同的智能合约使用。对于钱包，不会使用它，因此设置为`0`。有关此的信息可以在[tblkch.pdf](https://ton.org/tblkch.pdf)（1.8.4）中找到。 This will not be used for wallet, so its bit is set to `0`. Information about this can be found in [tblkch.pdf](https://ton.org/tblkch.pdf) (1.8.4).                           |

接下来我们将准备“初始数据”，这将在部署后立即出现在我们合约的存储中：

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { beginCell } from '@ton/core';

const dataCell = beginCell().
  storeUint(0, 32). // Seqno
  storeUint(698983191, 32). // Subwallet ID
  storeBuffer(keyPair.publicKey). // Public Key
  endCell();
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
import { Address } from '@ton/core';

const stateInit = beginCell().
  storeBit(0). // 没有split_depth
  storeBit(0). // 没有special
  storeBit(1). // 表示有代码
  storeRef(codeCell).
  storeBit(1). // 表示有数据
  storeRef(dataCell).
  storeBit(0). // 没有library
  endCell();

const contractAddress = new Address(0, stateInit.hash()); // 获取stateInit的哈希，以获取我们的智能合约在`ID`为0的工作链中的地址
console.log(`Contract address: ${contractAddress.toString()}`); // 将智能合约地址输出到控制台
```


<TabItem value="go" label="Golang">

```go
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




使用State Init，我们现在可以构建交易并发送到区块链。要执行此过程，需要一个最低交易余额为0.1 TON（余额可以更低，但此金额足够）。要完成这个操作，我们需要运行教程中提到的代码，获取正确的钱包地址，并向该地址发送0.1 TON。 To carry out this process **a minimum wallet balance of 0.1 TON** (the balance can be less, but this amount is guaranteed to be sufficient) is required. 调用成功完成后，最终结果是一个极大的 256 位数，必须转换为十六进制字符串。对于我们提供的钱包地址，结果十六进制字符串如下：`430db39b13cf3cb76bfa818b6b13417b82be2c6c389170fbe06795c71996b1f8`。
接下来，我们使用 [TonAPI](https://tonapi.io/swagger-ui)（/v1/wallet/findByPubkey 方法），通过输入获得的十六进制字符串到系统中，立即就可以清楚，答复内数组的第一个元素将识别我的钱包。

让我们从构建类似于我们在**上一节**构建的交易开始：

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { sign } from '@ton/crypto';
import { toNano } from '@ton/core';

const internalMessageBody = beginCell().
  storeUint(0, 32).
  storeStringTail("Hello, TON!").
  endCell();

const internalMessage = beginCell().
  storeUint(0x10, 6). // 不使用反弹
  storeAddress(Address.parse("put your first wallet address from were you sent 0.1 TON")).
  storeCoins(toNano("0.03")).
  storeUint(1, 1 + 4 + 4 + 64 + 32 + 1 + 1). // 保存1表示body是引用
  storeRef(internalMessageBody).
  endCell();

// 用于我们的钱包的交易
const toSign = beginCell().
  storeUint(subWallet, 32).
  storeUint(Math.floor(Date.now() / 1e3) + 60, 32).
  storeUint(0, 32). // 我们将seqno设置为0，因为在部署之后，钱包将将0存储为seqno
  storeUint(3, 8).
  storeRef(internalMessage);

const signature = sign(toSign.endCell().hash(), keyPair.secretKey);
const body = beginCell().
  storeBuffer(signature).
  storeBuilder(toSign).
  endCell();
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




完成后，结果是正确的State Init和消息体。

### 发送外部交易

此部分定义了如何存储消息体。有时，消息体太大而无法适合消息本身。在这种情况下，它应该作为一个**引用**存储，通过将位设置为 `1` 来显示该body作为引用使用。如果位为 `0`，则body在与消息相同的cell中。 Since the contract does not have its own code yet, it cannot process any internal messages. Therefore, next we send its code and the initial data **after it is successfully deployed so it can process our message** with "Hello, TON!" comment:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
const externalMessage = beginCell().
  storeUint(0b10, 2). // 表示它是一笔外部传入的交易
  storeUint(0, 2). // src -> addr_none
  storeAddress(contractAddress).
  storeCoins(0). // 导入费用
  storeBit(1). // 我们有State Init
  storeBit(1). // 我们将State Init存储为引用
  storeRef(stateInit). // 将State Init存储为引用
  storeBit(1). // 我们将消息体存储为引用
  storeRef(body). // 将消息体存储为引用
  endCell();
```


<TabItem value="go" label="Golang">

```go
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




最后，我们可以将我们的交易发送到区块链上部署我们的钱包并使用它。

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { TonClient } from '@ton/ton';

const client = new TonClient({
  endpoint: "https://toncenter.com/api/v2/jsonRPC",
  apiKey: "put your api key" // 你可以从Telegram中的@tonapibot获得API密钥
});

client.sendFile(externalMessage.toBoc());
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




Note that we have sent an internal message using mode `3`. If it is necessary to repeat the deployment of the same wallet, **the smart contract can be destroyed**. 请注意，我们使用mode`3`发送了一个内部消息。如果需要重复部署相同的钱包，**智能合约将被销毁**。为此，请正确设置的mode，通过添加128（取整个智能合约的余额）+ 32（销毁智能合约），以获取剩余的TON余额并再次部署钱包。

重要说明：对于每个新的交易，**seqno需要增加1**。

:::info
我们使用的合约代码是[已验证的](https://tonscan.org/tx/BL9T1i5DjX1JRLUn4z9JOgOWRKWQ80pSNevis26hGvc=)，因此您可以在此处查看一个[示例](https://tonscan.org/address/EQDBjzo_iQCZh3bZSxFnK9ue4hLTOKgsCNKfC8LOUM4SlSCX#source)。
:::

## 💸 使用钱包智能合约

在完成本教程的前半部分后，我们现在对钱包智能合约以及它们的开发和使用有了更深入的了解。我们学习了如何部署和销毁它们，以及如何在不依赖预配置的库函数的情况下发送消息。为了更多地应用我们上面学到的知识，在下一部分中，我们将专注于构建和发送更复杂的消息。 We learned how to deploy and destroy them and send messages without depending on pre-configured library functions. To apply more of what we learned above, in the next section, we’ll focus on building and sending more complex messages.

### 同时发送多条消息

正如您可能已经知道的，[一个cell可以存储最多1023位的数据和最多4个指向其他cells的引用](develop/data-formats/cell-boc#cell)。在本教程的第一部分中，我们详细介绍了内部消息是如何以“整体”循环作为链接发送的。这意味着可以**在外部消息内存储多达4条内部消息**。这允许同时发送四笔交易。 In the first section of this tutorial we detailed how internal messages are delivered in a ‘whole’ loop as a link and sent. This means it is possible to **store up to 4 internal messages inside the external** message. This allows four transactions to be sent at the same time.

To accomplish this, it is necessary to create 4 different internal messages. We can do this manually or through a `loop`. 为了实现这一点，需要创建4个不同的内部消息。我们可以手动创建，也可以通过`循环(loop)`来创建。我们需要定义3个数组：TON金额数组，评论数组，消息数组。对于消息，我们需要准备另一个数组 - internalMessages。 上面我们创建了 `InternalMessageBody`，其中存储了消息的正文。请注意，在存储不能适合单个cell的文本（1023 位）的情况下，根据[以下文档](/develop/smart-contracts/guidelines/internal-messages) 中的要求，需要**将数据拆分为多个cell**。但是，在此阶段，高层级库根据要求创建cell，因此现阶段无需担心这个问题。

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { Cell } from '@ton/core';

const internalMessagesAmount = ["0.01", "0.02", "0.03", "0.04"];
const internalMessagesComment = [
  "Hello, TON! #1",
  "Hello, TON! #2",
  "", // 我们让第三笔交易不留评论
  "Hello, TON! #4" 
]
const destinationAddresses = [
  "输入属于你的任何地址",
  "输入属于你的任何地址",
  "输入属于你的任何地址",
  "输入属于你的任何地址"
] // 所有4个地址可以相同

let internalMessages:Cell[] = []; // 存储我们内部消息的数组
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




所有消息的[发送模式](/develop/smart-contracts/messages#message-modes)都设置为`mode 3`。但是，如果需要不同的模式，则可以创建一个数组来满足不同的目的。  However, if different modes are required an array can be created to fulfill different purposes.

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { Address, beginCell, toNano } from '@ton/core';

for (let index = 0; index < internalMessagesAmount.length; index++) {
  const amount = internalMessagesAmount[index];
  
  let internalMessage = beginCell().
      storeUint(0x18, 6). // bounce
      storeAddress(Address.parse(destinationAddresses[index])).
      storeCoins(toNano(amount)).
      storeUint(0, 1 + 4 + 4 + 64 + 32 + 1);
      
  /*
      在这个阶段，并不清楚我们是否会有一个消息体。
      所以只设置stateInit的一位，如果我们有评论，那意味着
      我们有一个消息体。在这种情况下，将位设置为1并将
      体作为引用存储。
  */

  if(internalMessagesComment[index] != "") {
    internalMessage.storeBit(1) // 我们将消息体作为引用存储

    let internalMessageBody = beginCell().
      storeUint(0, 32).
      storeStringTail(internalMessagesComment[index]).
      endCell();

    internalMessage.storeRef(internalMessageBody);
  } 
  else 
    /*
        由于我们没有消息体，我们表明这个消息
        中有消息体，但不写入，意味着它不存在。
        在这种情况下，只需设置位为0。
    */
    internalMessage.storeBit(0);
  
  internalMessages.push(internalMessage.endCell());
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




现在让我们利用[第二章](/develop/smart-contracts/tutorials/wallet#-deploying-our-wallet)的知识，为我们的钱包构建一个可以同时发送4笔交易的交易：

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { TonClient } from '@ton/ton';
import { mnemonicToWalletKey } from '@ton/crypto';

const walletAddress = Address.parse('输入你的钱包地址');
const client = new TonClient({
  endpoint: "https://toncenter.com/api/v2/jsonRPC",
  apiKey: "输入你的api密钥" // 你可以从Telegram中的@tonapibot机器人获取api密钥
});

const mnemonic = '输入你的助记词'; // word1 word2 word3
let getMethodResult = await client.runMethod(walletAddress, "seqno"); // 从你的钱包合约运行"seqno"GET方法
let seqno = getMethodResult.stack.readNumber(); // 从响应中获取seqno

const mnemonicArray = mnemonic.split(' '); // 从字符串获取数组
const keyPair = await mnemonicToWalletKey(mnemonicArray); // 从助记词获取密钥对

let toSign = beginCell().
  storeUint(698983191, 32). // subwallet_id
  storeUint(Math.floor(Date.now() / 1e3) + 60, 32). // 交易过期时间，+60 = 1分钟
  storeUint(seqno, 32); // 存储seqno
  // 别忘了，如果我们使用Wallet V4，我们需要添加 storeUint(0, 8). 
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




接下来，我们将在循环中添加之前构建的消息：

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
for (let index = 0; index < internalMessages.length; index++) {
  const internalMessage = internalMessages[index];
  toSign.storeUint(3, 8) // 存储我们内部交易的mode
  toSign.storeRef(internalMessage) // 将我们的内部消息作为引用存储
}
```


<TabItem value="go" label="Golang">

```go
for i := 0; i < len(internalMessages); i++ {
		internalMessage := internalMessages[i]
		toSign.MustStoreUInt(3, 8) // 存储我们内部交易的mode
		toSign.MustStoreRef(internalMessage) // 将我们的内部消息作为引用存储
}
```




完成上述过程后，让我们**签名**我们的消息，**构建一个外部消息**（如本教程前几节所述）并**将其发送**到区块链：

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { sign } from '@ton/crypto';

let signature = sign(toSign.endCell().hash(), keyPair.secretKey); // 获取我们钱包智能合约的消息的哈希并签名以获得签名

let body = beginCell().
    storeBuffer(signature). // 存储签名
    storeBuilder(toSign). // 存储我们的消息
    endCell();

let externalMessage = beginCell().
    storeUint(0b10, 2). // ext_in_msg_info$10
    storeUint(0, 2). // src -> addr_none
    storeAddress(walletAddress). // 目的地址
    storeCoins(0). // 引入费
    storeBit(0). // 无State Init
    storeBit(1). // 我们将消息体作为引用存储
    storeRef(body). // 将消息体作为引用存储
    endCell();

client.sendFile(externalMessage.toBoc());
```


<TabItem value="go" label="Golang">

```go
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




:::info 连接错误
如果出现与轻服务器(lite-server)连接相关的错误（Golang），必须重复运行代码，直到能够发送交易。这是因为tonutils-go库通过代码中指定的全局配置使用了几个不同的轻服务器，但并非所有轻服务器都能接受我们的连接。 This is because the tonutils-go library uses several different lite-servers through the global configuration that have been specified in the code. However, not all lite-servers can accept our connection.
:::

完成此过程后，可以使用TON区块链浏览器来验证钱包是否已向之前指定的地址发送了四笔交易。

### NFT 转移

In addition to regular transactions, users often send NFTs to each other. Unfortunately, not all libraries contain methods that are tailored for use with this type of smart contract. Therefore, it is necessary to create code that will allow us to build a transaction for sending NFTs. 除了常规交易之外，用户经常彼此发送 NFT。不幸的是，并非所有库都包含为这种智能合约量身定制的方法。因此，我们需要创建代码，使我们能够构建发送 NFT 的交易。首先，让我们更熟悉 TON NFT [标准](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md)。

特别是，我们需要详细了解用于 [NFT 转移](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md#1-transfer) 的 TL-B。

- `query_id`：查询 ID 在交易处理方面没有价值。NFT 合约不验证它；它只是读取它。当服务希望为其每个交易分配特定的查询 ID 以供识别之用时，此值可能会有用。因此，我们将其设置为 0。 The NFT contract doesn't validate it; it only reads it. This value can be useful when a service wants to assign a specific query ID to each of its transactions for identification purposes. Therefore, we will set it to 0.

- `response_destination`：处理所有权变更交易后会有额外的 TON。它们将发送到此地址，如果指定了的话，否则保留在 NFT 余额中。 They will be sent to this address, if specified, otherwise remain on the NFT balance.

- `custom_payload`：custom_payload 需要用来执行特定任务，并且不与普通 NFT 一起使用。

- `forward_amount`：如果 forward_amount 不为零，指定的 TON 数量将发送给新所有者。这样，新所有者将被通知他们收到了某物。 That way the new owner will be notified that they received something.

- `forward_payload`: The forward_payload is additional data that can be sent to the new owner together with the forward_amount. `forward_payload`：forward_payload 是可以与 forward_amount 一起发送给新所有者的附加数据。例如，使用 forward_payload 允许用户在转移 NFT 时[添加评论](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md#forward_payload-format)，如本教程前面所示。然而，尽管 TON 的 NFT 标准中写有 forward_payload，区块链浏览器并不完全支持显示各种细节。显示 Jettons 时也存在同样的问题。 However, although the forward_payload is written within TON’s NFT standard, blockchain explorers do not fully support displaying various details. The same problem also exists when displaying Jettons.

现在让我们构建交易本身：

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { Address, beginCell, toNano } from '@ton/core';

const destinationAddress = Address.parse("put your wallet where you want to send NFT");
const walletAddress = Address.parse("put your wallet which is the owner of NFT")
const nftAddress = Address.parse("put your nft address");

// 我们可以添加评论，但由于目前尚未得到支持，因此不会在浏览器中显示。
const forwardPayload = beginCell().
  storeUint(0, 32).
  storeStringTail("Hello, TON!").
  endCell();

const transferNftBody = beginCell().
  storeUint(0x5fcc3d14, 32). // NFT 转移的操作码
  storeUint(0, 64). // query_id
  storeAddress(destinationAddress). // new_owner
  storeAddress(walletAddress). // response_destination 的超额部分
  storeBit(0). // 我们没有 custom_payload
  storeCoins(toNano("0.01")). // forward_amount
  storeBit(1). // 我们以引用的形式存储 forward_payload
  storeRef(forwardPayload). // 以引用的形式存储 forward_payload
  endCell();

const internalMessage = beginCell().
  storeUint(0x18, 6). // 弹回
  storeAddress(nftAddress).
  storeCoins(toNano("0.05")).
  storeUint(1, 1 + 4 + 4 + 64 + 32 + 1 + 1). // 我们存储 1 表示我们有body作为引用
  storeRef(transferNftBody).
  endCell();
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




NFT 转移操作码来自[相同的标准](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md#tl-b-schema)。
现在让我们完成交易，按本教程前面部分的布局。完成交易所需的正确代码可在 [GitHub 库](/develop/smart-contracts/tutorials/wallet#source-code)中找到。
Now let's complete the transaction, as is laid out in the previous sections of this tutorial. 完成此过程后，我们可以查看我们的钱包并验证我们的钱包上发送了12个传出交易。使用我们最初在控制台中使用的query_id，也可以调用`processed?` GET方法。如果此请求已正确处理，它会提供`-1`（真）的结果。

The same procedure can be completed with Jettons. 使用 Jettons 也可以完成相同的程序。要进行此过程，请阅读有关 jettons 转移的 TL-B [标准](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md)。特别是，NFT 和 Jettons 转移之间存在一些小差异。 To this point specifically, a small difference between NFT and Jettons transfers exists.

### Wallet v3 和 Wallet v4 的 Get 方法

智能合约经常使用 [GET 方法](/develop/smart-contracts/guidelines/get-methods)，但它们不在区块链内部运行，而是在客户端上运行。GET 方法有许多用途，为智能合约提供对不同数据类型的访问。例如，NFT 智能合约中的 [get_nft_data() 方法](https://github.com/ton-blockchain/token-contract/blob/991bdb4925653c51b0b53ab212c53143f71f5476/nft/nft-item.fc#L142-L145) 允许用户检索特定的内容、所有者和 NFT 集合信息。 GET methods have many uses and provide accessibility to different data types for smart contracts. For example, the [get_nft_data() method in NFT smart contracts](https://github.com/ton-blockchain/token-contract/blob/991bdb4925653c51b0b53ab212c53143f71f5476/nft/nft-item.fc#L142-L145) allows users to retrieve specific content, owner, and NFT collection information.

如前所述，TON 区块链上的所有内容都是由cell组成的智能合约。为了正确进行序列化和反序列化过程，创建了 `TL-B` 作为一种通用工具，用于以不同的方式、不同的顺序来描述cell中的不同数据类型。 Let’s start with the methods that are the same for both wallet versions:

|                                         方法                                        |                                                                                                           说明                                                                                                           |
| :-------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|                           int seqno()                          |                                         该方法需要用来接收当前的 seqno 并发送带有正确值的交易。在本教程的前几节中，该方法被频繁调用。 In previous sections of this tutorial, this method was called often.                                        |
| int get_public_key() | This method is used to retrive a public key. 该方法用于检索公钥。get_public_key() 并不广泛使用，可以被不同的服务使用。例如，一些 API 服务允许检索具有相同公钥的多个钱包 检索公钥。我们之前已经讨论过这个方法。 |

现在，我们转向只有 V4 钱包使用的方法：

|                                                                方法                                                                |                                                                                         说明                                                                                        |
| :------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|                        int get_subwallet_id()                       |                                Earlier in the tutorial we considered this. 教程前面已经考虑过这个。此方法允许您检索 subwallet_id。                                |
| int is_plugin_installed(int wc, int addr_hash) | Let’s us know if the plugin has been installed. 让我们知道插件是否已安装。调用此方法时，需要传递 [工作链](/learn/overviews/ton-blockchain#workchain-blockchain-with-your-own-rules) 和插件地址哈希。 |
|                       tuple get_plugin_list()                       |                                                                                   此方法返回已安装插件的地址。                                                                                  |

让我们考虑 `get_public_key` 和 `is_plugin_installed` 方法。选择这两种方法是因为，首先我们需要从 256 位数据中获取公钥，然后我们需要学习如何向 GET 方法传递切片和不同类型的数据。这对于我们正确使用这些方法非常有用。 These two methods were chosen because at first we would have to get a public key from 256 bits of data, and after that we would have to learn how to pass a slice and different types of data to GET methods. This is very useful to help us learn how to properly make use of these methods.

First we need a client that is capable of sending requests. 首先，我们需要一个能够发送请求的客户端。因此，我们将使用特定的钱包地址（[EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF](https://tonscan.org/address/EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF)）作为例子：

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { TonClient } from '@ton/ton';
import { Address } from '@ton/core';

const client = new TonClient({
    endpoint: "https://toncenter.com/api/v2/jsonRPC",
    apiKey: "put your api key" // 你可以从 Telegram 中的 @tonapibot 机器人获取 api 密钥
});

const walletAddress = Address.parse("EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF"); // 以我的钱包地址为例
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

block, err := client.CurrentMasterchainInfo(context.Background()) // 获取当前区块， 我们将需要它用于向 LiteServer 发送请求
if err != nil {
  log.Fatalln("CurrentMasterchainInfo err:", err.Error())
  return
}

walletAddress := address.MustParseAddr("EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF") // 以我的钱包地址为例
```




现在我们需要调用钱包的 GET 方法。

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
// 我总是调用 runMethodWithError 而不是 runMethod，以便能够检查被调用方法的 exit_code。
let getResult = await client.runMethodWithError(walletAddress, "get_public_key"); // 运行 get_public_key GET 方法
const publicKeyUInt = getResult.stack.readBigNumber(); // 读取包含 uint256 的回答
const publicKey = publicKeyUInt.toString(16); // 从 bigint（uint256）获取十六进制字符串
console.log(publicKey)
```


<TabItem value="go" label="Golang">

```go
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




After the call is successfully completed the end result is an extremely large 256 bit number which must be translated into a hex string. The resulting hex string for the wallet address we provided above is as follows: `430db39b13cf3cb76bfa818b6b13417b82be2c6c389170fbe06795c71996b1f8`.
Next, we leverage the [TonAPI](https://tonapi.io/swagger-ui) (/v1/wallet/findByPubkey method), by inputting the obtained hex string into the system and it is immediately clear that the first element in the array within the answer will identify my wallet.

Then we switch to the `is_plugin_installed` method. 然后我们转向 `is_plugin_installed` 方法。作为例子，我们将再次使用之前使用的钱包（[EQAM7M--HGyfxlErAIUODrxBA3yj5roBeYiTuy6BHgJ3Sx8k](https://tonscan.org/address/EQAM7M--HGyfxlErAIUODrxBA3yj5roBeYiTuy6BHgJ3Sx8k)）和插件（[EQBTKTis-SWYdupy99ozeOvnEBu8LRrQP_N9qwOTSAy3sQSZ](https://tonscan.org/address/EQBTKTis-SWYdupy99ozeOvnEBu8LRrQP_N9qwOTSAy3sQSZ)）：

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
const oldWalletAddress = Address.parse("EQAM7M--HGyfxlErAIUODrxBA3yj5roBeYiTuy6BHgJ3Sx8k"); // 我的旧钱包地址
const subscriptionAddress = Address.parseFriendly("EQBTKTis-SWYdupy99ozeOvnEBu8LRrQP_N9qwOTSAy3sQSZ"); // 已经安装在钱包上的订阅插件地址
```


<TabItem value="go" label="Golang">

```go
oldWalletAddress := address.MustParseAddr("EQAM7M--HGyfxlErAIUODrxBA3yj5roBeYiTuy6BHgJ3Sx8k")
subscriptionAddress := address.MustParseAddr("EQBTKTis-SWYdupy99ozeOvnEBu8LRrQP_N9qwOTSAy3sQSZ") // 已经安装在钱包上的订阅插件地址
```




现在我们需要检索插件的哈希地址，以便地址可以转换成数字并发送给 GET 方法。

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
const hash = BigInt(`0x${subscriptionAddress.address.hash.toString("hex")}`) ;

getResult = await client.runMethodWithError(oldWalletAddress, "is_plugin_installed", 
[
    {type: "int", value: BigInt("0")}, // 作为 int 传递 workchain
    {type: "int", value: hash} // 作为 int 传递插件地址哈希
]);
console.log(getResult.stack.readNumber()); // -1
```


<TabItem value="go" label="Golang">

```go
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




The response must be `-1`, meaning the result is true. It is also possible to send a slice and a cell if required. It would be enough to create a Slice or Cell and transfer it instead of using the BigInt, specifying the appropriate type.

### 通过钱包部署合约

In chapter three, we deployed a wallet. 在第三章中，我们部署了一个钱包。为此，我们最初发送了一些TON，然后从钱包发送了一笔交易以部署一个智能合约。然而，这个过程并不常用于外部交易，通常主要用于钱包。在开发合约时，部署过程是通过发送内部消息来初始化的。 However, this process is not broadly used with external transactions and is often primarily used for wallets only. While developing contracts, the deployment process is initialized by sending internal messages.

为了完成这个过程，我们将使用在[第三章](/develop/smart-contracts/tutorials/wallet#compiling-our-wallet-code)中使用的V3R2钱包智能合约。在这种情况下，我们将`subwallet_id`设置为`3`或者使用相同的私钥检索另一个地址时需要的任何其他数字（它是可变的）：
如果数字值适合的位数比指定的位数少，则在值的左侧添加缺少的零位。例如，0x18 适合 5 位 -> `11000`。然而，由于指定了 6 位，最终结果变为 `011000`。

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { beginCell, Cell } from '@ton/core';
import { mnemonicToWalletKey } from '@ton/crypto';

const mnemonicArray = 'put your mnemonic'.split(" ");
const keyPair = await mnemonicToWalletKey(mnemonicArray); // 从助记词提取私钥和公钥

const codeCell = Cell.fromBase64('te6ccgEBCAEAhgABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQCW8oMI1xgg0x/TH9MfAvgju/Jj7UTQ0x/TH9P/0VEyuvKhUUS68qIE+QFUEFX5EPKj+ACTINdKltMH1AL7AOgwAaTIyx/LH8v/ye1UAATQMAIBSAYHABe7Oc7UTQ0z8x1wv/gAEbjJftRNDXCx+A==');
const dataCell = beginCell().
    storeUint(0, 32). // Seqno
    storeUint(3, 32). // 子钱包ID
    storeBuffer(keyPair.publicKey). // 公钥
    endCell();

const stateInit = beginCell().
    storeBit(0). // 没有 split_depth
    storeBit(0). // 没有特殊
    storeBit(1). // 我们有代码
    storeRef(codeCell).
    storeBit(1). // 我们有数据
    storeRef(dataCell).
    storeBit(0). // 没有库
    endCell();
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




接下来我们将从我们的合约中获取地址并构建内部消息。同时，我们将向我们的交易中添加"Deploying..."评论。 Also we add the "Deploying..." comment to our transaction.

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { Address, toNano } from '@ton/core';

const contractAddress = new Address(0, stateInit.hash()); // 获取stateInit的哈希来获取我们的智能合约在工作链ID为0的地址
console.log(`合约地址: ${contractAddress.toString()}`); // 输出合约地址到控制台

const internalMessageBody = beginCell().
    storeUint(0, 32).
    storeStringTail('Deploying...').
    endCell();

const internalMessage = beginCell().
    storeUint(0x10, 6). // 无弹回
    storeAddress(contractAddress).
    storeCoins(toNano('0.01')).
    storeUint(0, 1 + 4 + 4 + 64 + 32).
    storeBit(1). // 我们有State Init
    storeBit(1). // 我们将State Init作为引用存储
    storeRef(stateInit). // 将State Init作为引用存储
    storeBit(1). // 我们将消息体作为引用存储
    storeRef(internalMessageBody). // 将消息体Init作为引用存储
    endCell();
```


<TabItem value="go" label="Golang">

```go
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




:::info
Note that above, the bits have been specified and that the stateInit and internalMessageBody have been saved as references. 请注意，上述中已指定位，并且stateInit和internalMessageBody已作为引用保存。由于链接是分开存储的，我们可以写4（0b100）+ 2（0b10）+ 1（0b1）->（4 + 2 + 1, 1 + 4 + 4 + 64 + 32 + 1 + 1 + 1）即（0b111, 1 + 4 + 4 + 64 + 32 + 1 + 1 + 1），然后保存两个引用。
:::

接下来，我们将为我们的钱包准备一条消息并发送它：

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { TonClient } from '@ton/ton';
import { sign } from '@ton/crypto';

const client = new TonClient({
    endpoint: 'https://toncenter.com/api/v2/jsonRPC',
    apiKey: 'put your api key' // 您可以从Telegram中的@tonapibot bot获取api key
});

const walletMnemonicArray = 'put your mnemonic'.split(' ');
const walletKeyPair = await mnemonicToWalletKey(walletMnemonicArray); // 从助记词提取私钥和公钥
const walletAddress = Address.parse('用来部署的你的钱包地址');
const getMethodResult = await client.runMethod(walletAddress, 'seqno'); // 从你的钱包合约运行"seqno" GET方法
const seqno = getMethodResult.stack.readNumber(); // 从回应中获取seqno

// 我们钱包的交易
const toSign = beginCell().
    storeUint(698983191, 32). // 子钱包id
    storeUint(Math.floor(Date.now() / 1e3) + 60, 32). // 交易过期时间, +60 = 1 分钟
    storeUint(seqno, 32). // 存储seqno
    // 不要忘记如果我们使用钱包V4，我们需要添加storeUint(0, 8). 
    storeUint(3, 8).
    storeRef(internalMessage);

const signature = sign(toSign.endCell().hash(), walletKeyPair.secretKey); // 获取我们发往钱包智能合约的消息hash并签名以获取签名
const body = beginCell().
    storeBuffer(signature). // 存储签名
    storeBuilder(toSign). // 存储我们的消息
    endCell();

const external = beginCell().
    storeUint(0b10, 2). // 表示这是一个传入的外部交易
    storeUint(0, 2). // src -> addr_none
    storeAddress(walletAddress).
    storeCoins(0). // 导入费
    storeBit(0). // 我们没有State Init
    storeBit(1). // 我们将消息体作为引用存储
    storeRef(body). // 将消息体作为引用存储
    endCell();

console.log(external.toBoc().toString('base64'));
client.sendFile(external.toBoc());
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




This concludes our work with ordinary wallets. 这就结束了我们和普通钱包的工作。在这个阶段，您应该对如何与钱包智能合约互动，发送交易，以及能够使用各种库类型有一个深入的了解。

## 🔥 高负载钱包

In some situations, sending a large number of transactions per message may be necessary. 在某些情况下，可能需要一次发送大量的交易。如前所述，普通钱包支持一次发送最多4笔交易，这是通过在单个cell中存储[最多4个引用](/develop/data-formats/cell-boc#cell)来支持的。高负载钱包则允许一次发送255笔交易。这个限制的存在是因为区块链的配置设置中对外部消息（动作）的最大数量设定为255。 High-load wallets only allow 255 transactions to be sent at once. This restriction exists because the maximum number of outgoing messages (actions) in the blockchain’s config settings is set to 255.

交易所可能是使用高负载钱包的最佳示例。像币安这样的大型交易所有着极大的用户基础，这意味着在短时间内会处理大量的交易提款请求。高负载钱包有助于处理这些提款请求。 Established exchanges like Binance and others have extremely large user bases, this means that a large number of transaction withdrawals are processed in short time periods. High-load wallets help address these withdrawal requests.

### 高负载钱包 FunC 代码

首先，让我们查看[高负载钱包智能合约的代码结构](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/highload-wallet-v2-code.fc)：

```func
() recv_external(slice in_msg) impure {
  var signature = in_msg~load_bits(512); ;; 从消息体中获取签名
  var cs = in_msg;
  var (subwallet_id, query_id) = (cs~load_uint(32), cs~load_uint(64)); ;; 从消息体中获取其余值
  var bound = (now() << 32); ;; 位左移操作
  throw_if(35, query_id < bound); ;; 如果交易已过期则抛出错误
  var ds = get_data().begin_parse();
  var (stored_subwallet, last_cleaned, public_key, old_queries) = (ds~load_uint(32), ds~load_uint(64), ds~load_uint(256), ds~load_dict()); ;; 从存储中读取值
  ds.end_parse(); ;; 确保 ds 中没有任何东西
  (_, var found?) = old_queries.udict_get?(64, query_id); ;; 检查是否已经存在此类请求
  throw_if(32, found?); ;; 如果是则抛出错误
  throw_unless(34, subwallet_id == stored_subwallet);
  throw_unless(35, check_signature(slice_hash(in_msg), signature, public_key));
  var dict = cs~load_dict(); ;; 获取包含消息的字典
  cs.end_parse(); ;; 确保 cs 中没有任何东西
  accept_message();
```

> 💡 有用的链接:
>
> [位运算](/develop/func/stdlib/#dict_get)
>
> [load_dict()](/develop/func/stdlib/#load_dict)
>
> [udict_get?()](/develop/func/stdlib/#dict_get)

You notice some differences from ordinary wallets. 您会发现与普通钱包有些不同。现在让我们更详细地看看高负载钱包在TON上的工作原理（除了子钱包，因为我们之前已经讨论过了）。

### 使用查询 ID 代替 Seqno

As we previously discussed, ordinary wallet seqno increase by `1` after each transaction. While using a wallet sequence we had to wait until this value was updated, then retrieve it using the GET method and send a new transaction.
This process takes a significant amount of time which high-load wallets are not designed for (as discussed above, they are meant to send a large number of transactions very quickly). Therefore, high-load wallets on TON make use of the `query_id`.

如果相同的交易请求已经存在，合约将不会接受它，因为它已经被处理过了：

```func
var (stored_subwallet, last_cleaned, public_key, old_queries) = (ds~load_uint(32), ds~load_uint(64), ds~load_uint(256), ds~load_dict()); ;; 从存储中读取值
ds.end_parse(); ;; 确保 ds 中没有任何东西
(_, var found?) = old_queries.udict_get?(64, query_id); ;; 检查是否已经存在此类请求
throw_if(32, found?); ;; 如果是则抛出错误
```

通过这种方式，我们**被保护免受重复交易的影响**，这是普通钱包中 seqno 的作用。

### 发送交易

合约接受外部消息后，将开始循环，在循环中取出存储在字典中的 `slices`。这些切片存储了交易模式和交易本身。发送新交易一直进行，直到字典为空。 These slices store transaction modes and the transactions themselves. Sending new transactions takes place until the dictionary is empty.

```func
int i = -1; ;; 我们写 -1 是因为它将是所有字典键中的最小值
do {
  (i, var cs, var f) = dict.idict_get_next?(16, i); ;; 获取键及其对应的最小键值，这个键值大于 i
  if (f) { ;; 检查是否找到了任何值
    var mode = cs~load_uint(8); ;; 加载交易模式
    send_raw_message(cs~load_ref(), mode); ;; 加载交易本身并发送
  }
} until (~ f); ;; 如果找到任何值则继续
```

> 💡 有用的链接：
>
> [idict_get_next()](/develop/func/stdlib/#dict_get_next)

Note that if a value is found, `f` is always equal to -1 (true). The `~ -1` operation (bitwise not) will always return a value of 0, meaning that the loop should be continued. At the same time, when a dictionary is filled with transactions, it is necessary to start calculating those **with a value greater than -1** (e.g., 0) and continue increasing the value by 1 with each transaction. This structure allows transactions to be sent in the correct sequential order.

### 移除过期查询

通常情况下，[TON上的智能合约需要为自己的存储付费](develop/smart-contracts/fees#storage-fee)。这意味着智能合约可以存储的数据量是有限的，以防止高网络交易费用。为了让系统更高效，超过 64 秒的交易将从存储中移除。按照以下方式进行： This means that the amount of data smart contracts can store is limited to prevent high network transaction fees. To allow the system to be more efficient, transactions that are more than 64 seconds old are removed from the storage. 通过以下方式实现：

```func
bound -= (64 << 32);   ;; 清除记录，这些记录超过 64 秒前已过期
old_queries~udict_set_builder(64, query_id, begin_cell()); ;; 将当前查询添加到字典中
var queries = old_queries; ;; 将字典复制到另一个变量中
do {
  var (old_queries', i, _, f) = old_queries.udict_delete_get_min(64);
  f~touch();
  if (f) { ;; 检查是否找到了任何值
    f = (i < bound); ;; 检查是否超过 64 秒后过期
  }
  if (f) { 
    old_queries = old_queries'; ;; 如果是，则在我们的字典中保存更改
    last_cleaned = i; ;; 保存最后移除的查询
  }
} until (~ f);
```

> 💡 有用的链接:
>
> [udict_delete_get_min()](/develop/func/stdlib/#dict_delete_get_min)

Note that it is necessary to interact with the `f` variable several times. 请注意，必须多次与 `f` 变量进行交互。由于 [TVM 是一个堆栈机器](learn/tvm-instructions/tvm-overview#tvm-is-a-stack-machine)，在每次与 `f` 变量交互时，必须弹出所有值以获得所需的变量。`f~touch()` 操作将 f 变量放在堆栈顶部，以优化代码执行。 The `f~touch()` operation places the f  variable at the top of the stack to optimize code execution.

### Bitwise Operations

This section may seem a bit complicated for those who have not previously worked with bitwise operations. 如果您之前没有使用过位运算，那么这个部分可能会显得有些复杂。在智能合约代码中可以看到以下代码行：

```func
var bound = (now() << 32); ;; 位左移操作
```

As a result 32 bits are added to the number on the right side. This means that **existing values are moved 32 bits to the left**. For example, let’s consider the number 3 and translate it into a binary form with a result of 11. Applying the `3 << 2` operation, 11 is moved 2 bit places. This means that two bits are added to the right of the string. In the end, we have 1100, which is 12.

The first thing to understand about this process is to remember that the `now()` function returns a result of uint32, meaning that the resulting value will be 32 bits. 关于这个过程要理解的第一件事是记住 `now()` 函数返回 uint32 的结果，意味着结果值将是 32 位。通过向左移动 32 位，为另一个 uint32 打开了空间，结果是正确的 query_id。这样，**时间戳和 query_id 可以在一个变量中组合**以进行优化。 This way, the **timestamp and query_id can be combined** within one variable for optimization.

接下来，让我们考虑以下代码行：

```func
bound -= (64 << 32); ;; 清除超过 64 秒之前过期的记录
```

Above we performed an operation to shift the number 64 by 32 bits to **subtract 64 seconds** from our timestamp. This way we'll be able to compare past query_ids and see if they are less than the received value. If so, they expired more than 64 seconds ago:

```func
if (f) { ;; 检查是否找到了任何值
  f = (i < bound); ;; 检查是否超过 64 秒后过期
}
```

To understand this better, let’s use the number `1625918400` as an example of a timestamp. Its binary representation (with the left-handed addition of zeros for 32 bits) is 01100000111010011000101111000000. By performing a 32 bit bitwise left shift, the result is 32 zeros at the end of the binary representation of our number.

After this is completed, **it is possible to add any query_id (uint32)**. 在上面，我们执行了一个操作，将数字 64 向左移动 32 位，以**减去 64 秒**的时间戳。这样我们就可以比较过去的 query_ids，看看它们是否小于接收到的值。如果是这样，它们就超过了 64 秒： This fact can be verified by performing the following calculations `((1625918400 << 32) - (64 << 32)) >> 32`. This way we can compare the necessary portions of our number (the timestamp) and at the same time the query_id does not interfere.

### 存储更新

所有操作完成后，剩下的唯一任务就是将新的值保存在存储中：

```func
  set_data(begin_cell()
    .store_uint(stored_subwallet, 32)
    .store_uint(last_cleaned, 64)
    .store_uint(public_key, 256)
    .store_dict(old_queries)
    .end_cell());
}
```

### GET 方法

在我们深入了解钱包部署和交易创建之前，我们必须考虑的最后一件事是高负载钱包的 GET 方法：

|                                         方法                                        |                                                                                                                           说明                                                                                                                           |
| :-------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|        int processed?(int query_id)       | Notifies the user if a particular request has been processed. 响应必须是 `-1`，意味着结果是真的。如果需要的话，也可以发送切片和cell。创建切片或cell并将其传递替代 BigInt 就足够了，指定相应的类型。 通知用户特定请求是否已处理。这意味着如果请求已经处理，则返回 `-1`；如果尚未处理，则返回 `0`。此外，如果答案未知，因为请求较旧，且不再存储在合约中，此方法可能返回 `1`。 |
| int get_public_key() |                                                                               Rerive a public key. We have considered this method before.                                                                              |

让我们仔细看看 `int processed?(int query_id)` 方法，以帮助我们了解为什么我们需要使用 last_cleaned：

```func
int processed?(int query_id) method_id {
  var ds = get_data().begin_parse();
  var (_, last_cleaned, _, old_queries) = (ds~load_uint(32), ds~load_uint(64), ds~load_uint(256), ds~load_dict());
  ds.end_parse();
  (_, var found) = old_queries.udict_get?(64, query_id);
  return found ? true : - (query_id <= last_cleaned);
}
```

`last_cleaned` 从合约的存储和旧查询字典中检索。如果找到了查询，它应返回 true；如果没有，则表达式 `- (query_id <= last_cleaned)`。last_cleaned 包含最后一个被删除的、**时间戳最高**的请求，因为我们开始时从最小时间戳删除请求。 请注意，如果找到一个值，`f` 永远等于 -1（真）。`~ -1` 操作（位非）将始终返回 0 的值，意味着应该继续循环。与此同时，当字典填充了交易时，需要开始计算那些**大于 -1** 的值（例如，0），并且每次交易都将值递增 1。这个结构允许以正确的顺序发送交易。 The last_cleaned contains the last removed request **with the highest timestamp**, as we started with the minimum timestamp when deleting the requests.

这意味着，如果传递给方法的 query_id 小于 last_cleaned 值，就无法确定它是否曾在合约中。因此 `query_id <= last_cleaned` 返回 -1，而表达式前面的减号将答案改为 1。如果 query_id 大于 last_cleaned 方法，则表示它尚未被处理。 完成后，**可以添加任何 query_id (uint32)**。然后减去 `64 << 32` 的结果是 64 秒前有相同 query_id 的时间戳。可以通过执行以下计算来验证这一点 `((1625918400 << 32) - (64 << 32)) >> 32`。这样我们可以比较我们数字的必要部分（时间戳），同时 query_id 不会干扰。 If query_id is larger than last_cleaned method, then it has not yet been processed.

### 部署高负载钱包

为了部署高负载钱包，必须提前生成一个助记词密钥，用户将使用此密钥。可以使用在本教程之前部分中使用的相同密钥。 It is possible to use the same key that was used in previous sections of this tutorial.

要开始部署高负载钱包的过程，必须将[智能合约的代码](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/highload-wallet-v2-code.fc)复制到 stdlib.fc 和 wallet_v3 所在的同一目录中，并记得在代码开头添加`#include "stdlib.fc";`。接下来，我们将像在[第三节](/develop/smart-contracts/tutorials/wallet#compiling-wallet-code)中所做的那样，编译高负载钱包代码： 在本节中，我们将介绍如何从头开始创建钱包（钱包v3）。您将学习如何为钱包智能合约编译代码，生成助记词短语，获得钱包地址，并使用外部交易和State Init部署钱包。

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { compileFunc } from '@ton-community/func-js';
import fs from 'fs'
import { Cell } from '@ton/core';

const result = await compileFunc({
    targets: ['highload_wallet.fc'], // 你项目的目标
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

// 现在我们有了编译后代码的 base64 编码 BOC 在 result.codeBoc 中
console.log('代码 BOC: ' + result.codeBoc);
console.log('\n哈希值: ' + codeCell.hash().toString('base64')); // 获取cell的哈希值并转换为 base64 编码字符串

```




在终端中的输出将如下所示：

```text
Code BOC: te6ccgEBCQEA5QABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQHq8oMI1xgg0x/TP/gjqh9TILnyY+1E0NMf0z/T//QE0VNggED0Dm+hMfJgUXO68qIH+QFUEIf5EPKjAvQE0fgAf44WIYAQ9HhvpSCYAtMH1DAB+wCRMuIBs+ZbgyWhyEA0gED0Q4rmMQHIyx8Tyz/L//QAye1UCAAE0DACASAGBwAXvZznaiaGmvmOuF/8AEG+X5dqJoaY+Y6Z/p/5j6AmipEEAgegc30JjJLb/JXdHxQANCCAQPSWb6VsEiCUMFMDud4gkzM2AZJsIeKz

Hash: lJTRzI7fEvBWcaGpugmSEJbrUIEeGSTsZcPGKfu4CBI=
```

在上述结果的基础上，我们可以使用base64编码的输出，在其他库和语言中检索包含我们钱包代码的cell，具体操作如下：

<Tabs groupId="code-examples">
<TabItem value="go" label="Golang">

```go
import (
  "encoding/base64"
  "github.com/xssnick/tonutils-go/tvm/cell"
  "log"
)

base64BOC := "te6ccgEBCQEA5QABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQHq8oMI1xgg0x/TP/gjqh9TILnyY+1E0NMf0z/T//QE0VNggED0Dm+hMfJgUXO68qIH+QFUEIf5EPKjAvQE0fgAf44WIYAQ9HhvpSCYAtMH1DAB+wCRMuIBs+ZbgyWhyEA0gED0Q4rmMQHIyx8Tyz/L//QAye1UCAAE0DACASAGBwAXvZznaiaGmvmOuF/8AEG+X5dqJoaY+Y6Z/p/5j6AmipEEAgegc30JjJLb/JXdHxQANCCAQPSWb6VsEiCUMFMDud4gkzM2AZJsIeKz" // 将编译器输出的base64编码保存到变量中
codeCellBytes, _ := base64.StdEncoding.DecodeString(base64BOC) // 解码base64以获取字节数组
codeCell, err := cell.FromBOC(codeCellBytes) // 从字节数组中获取包含代码的cell
if err != nil { // 检查是否有任何错误
  panic(err) 
}

log.Println("Hash:", base64.StdEncoding.EncodeToString(codeCell.Hash())) // 获取我们cell的哈希值，因为它的类型是[]byte，所以编码为base64并输出到终端
```




现在我们需要检索由其初始数据组成的cell，构建一个State Init，并计算一个高负载钱包地址。经过研究智能合约代码后，我们发现subwallet_id、last_cleaned、public_key和old_queries是顺序存储在存储中的： 钱包智能合约中的交易重放保护与交易 seqno（序列号）直接相关，它跟踪哪些交易以什么顺序发送。不能重复发送钱包中的单个交易非常重要，因为这会完全破坏系统的完整性。如果进一步检查智能合约代码，通常会处理 `seqno` 如下：

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { Address, beginCell } from '@ton/core';
import { mnemonicToWalletKey } from '@ton/crypto';

const highloadMnemonicArray = 'put your mnemonic that you have generated and saved before'.split(' ');
const highloadKeyPair = await mnemonicToWalletKey(highloadMnemonicArray); // 从助记词中提取私钥和公钥

const dataCell = beginCell().
    storeUint(698983191, 32). // 子钱包ID
    storeUint(0, 64). // 上次清理时间
    storeBuffer(highloadKeyPair.publicKey). // 公钥
    storeBit(0). // 表示字典为空
    endCell();

const stateInit = beginCell().
    storeBit(0). // 无split_depth
    storeBit(0). // 无special
    storeBit(1). // 我们有代码
    storeRef(codeCell).
    storeBit(1). // 我们有数据
    storeRef(dataCell).
    storeBit(0). // 无库
    endCell();

const contractAddress = new Address(0, stateInit.hash()); // 获取stateInit的哈希值以获得我们智能合约在工作链ID为0的地址
console.log(`Contract address: ${contractAddress.toString()}`); // 输出合约地址到控制台
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


 

以上我们详细描述的步骤与[通过钱包部署合约](/develop/smart-contracts/tutorials/wallet#contract-deployment-via-wallet)部分中的步骤一致。为了更好地分析完整功能的代码，请访问教程开始处提到的库，其中存储了所有源代码。 To better analyze the fully functional code, please visit the repository indicated at the beginning of the tutorial where all sources are stored.

### 发送高负载钱包交易

当前此选项被禁用（意味着我们存储 1），因为 Instant Hypercube Routing 尚未完全实现。此外，当网络上有大量 [Shardchains](/learn/overviews/ton-blockchain#many-accountchains-shards) 时，这将是必要的。有关禁用 IHR 的更多信息，请阅读[tblkch.pdf](https://ton.org/tblkch.pdf)（第 2 章）。 现在，让我们编程高负载钱包同时发送多条消息。例如，让我们每条消息发送12笔交易，这样gas费用就很小。

:::info 高负载余额
要完成交易，合约的余额必须至少为0.5 TON。
:::

每条消息携带其自己的含代码的评论，目的地址将是我们部署的钱包：

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { Address, beginCell, Cell, toNano } from '@ton/core';

let internalMessages:Cell[] = [];
const walletAddress = Address.parse('put your wallet address from which you deployed high-load wallet');

for (let i = 0; i < 12; i++) {
    const internalMessageBody = beginCell().
        storeUint(0, 32).
        storeStringTail(`Hello, TON! #${i}`).
        endCell();

    const internalMessage = beginCell().
        storeUint(0x18, 6). // 弹回
        storeAddress(walletAddress).
        storeCoins(toNano('0.01')).
        storeUint(0, 1 + 4 + 4 + 64 + 32).
        storeBit(0). // 我们没有State Init
        storeBit(1). // 我们将消息体存储为引用
        storeRef(internalMessageBody). // 将消息体Init存储为引用
        endCell();

    internalMessages.push(internalMessage);
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




After completing the above process, the result is an array of internal messages. 完成上述过程后，结果是一系列内部消息。接下来，需要创建一个消息存储的字典来准备并签名消息体。如下所示： This is completed as follows:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { Dictionary } from '@ton/core';
import { mnemonicToWalletKey, sign } from '@ton/crypto';
import * as crypto from 'crypto';

const dictionary = Dictionary.empty<number, Cell>(); // 创建一个键为数字值为cell的空字典
for (let i = 0; i < internalMessages.length; i++) {
    const internalMessage = internalMessages[i]; // 从数组中获取我们的消息
    dictionary.set(i, internalMessage); // 在字典中保存该消息
}

const queryID = crypto.randomBytes(4).readUint32BE(); // 创建一个随机的uint32数字，4字节 = 32位
const now = Math.floor(Date.now() / 1000); // 获取当前时间戳
const timeout = 120; // 消息失效的超时时间，120秒 = 2分钟
const finalQueryID = (BigInt(now + timeout) << 32n) + BigInt(queryID); // 获取我们最终的query_id
console.log(finalQueryID); // 打印query_id。使用这个query_id我们可以调用GET方法来检查我们的请求是否已被处理

const toSign = beginCell().
    storeUint(698983191, 32). // subwallet_id
    storeUint(finalQueryID, 64).
    // 在这里我们创建自己的方法来保存
    // 交易mode和对交易的引用
    storeDict(dictionary, Dictionary.Keys.Int(16), {
        serialize: (src, buidler) => {
            buidler.storeUint(3, 8); // 保存交易mode，mode = 3
            buidler.storeRef(src); // 以引用形式保存交易
        },
        // 实际上我们不会使用这个，但这个方法
        // 将帮助读取我们保存的字典
        parse: (src) => {
            let cell = beginCell().
                storeUint(src.loadUint(8), 8).
                storeRef(src.loadRef()).
                endCell();
            return cell;
        }
    }
);

const highloadMnemonicArray = 'put your high-load wallet mnemonic'.split(' ');
const highloadKeyPair = await mnemonicToWalletKey(highloadMnemonicArray); // 从助记词中提取私钥和公钥
const highloadWalletAddress = Address.parse('put your high-load wallet address');

const signature = sign(toSign.endCell().hash(), highloadKeyPair.secretKey); // 获取我们向智能合约钱包发送的消息哈希并签名以获取签名
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




:::note 重要
Note that while using JavaScript and TypeScript that our messages were saved into an array without using a send mode. This occurs because during using @ton/ton library, it is expected that developer will implement process of serialization and deserialization by own hands. Therefore, a method is passed that first saves the transaction mode after it saves the transaction itself. 请注意，在使用JavaScript和TypeScript时，我们的消息被保存在数组中而没有使用发送模式。这是因为，在使用@ton/ton库时，预期开发者将自行实现序列化和反序列化的过程。因此，会传递一个首先保存交易模式然后保存交易本身的方法。如果我们使用`Dictionary.Values.Cell()`规范作为值方法，它会将整个消息作为cell引用保存，而不是单独保存模式。
:::

接下来我们将创建一个外部消息并使用以下代码发送到区块链：

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { TonClient } from '@ton/ton';

const body = beginCell().
    storeBuffer(signature). // 保存签名
    storeBuilder(toSign). // 保存我们的消息
    endCell();

const externalMessage = beginCell().
    storeUint(0b10, 2). // 表明这是一个传入的外部交易
    storeUint(0, 2). // src -> addr_none
    storeAddress(highloadWalletAddress).
    storeCoins(0). // 导入费用
    storeBit(0). // 我们没有State Init
    storeBit(1). // 我们以引用形式存储消息体
    storeRef(body). // 以引用形式存储消息体
    endCell();

// 我们在这里不需要键，因为我们将以每秒1个请求的速度发送
const client = new TonClient({
    endpoint: 'https://toncenter.com/api/v2/jsonRPC',
    // apiKey: 'put your api key' // 你可以从Telegram中的@tonapibot bot获得一个api密钥
});

client.sendFile(externalMessage.toBoc());
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




After this process is completed it is possible to look up our wallet and verify that 12 outgoing transactions were sent on our wallet. Is it also possible to call the `processed?` GET method using the query_id we initially used in the console. If this request has been processed correctly it provides a result of `-1` (true).

## 🏁 结论

这个教程让我们更好地理解了TON区块链上不同钱包类型的运作方式。它还让我们学会了如何创建外部和内部消息，而不使用预定义的库方法。 It also allowed us to learn how to create external and internal messages without using predefined library methods.

这有助于我们独立于使用库，并以更深入的方式理解TON区块链的结构。我们还学习了如何使用高负载钱包，并分析了许多与不同数据类型和各种操作相关的细节。 We also learned how to use high-load wallets and analyzed many details to do with different data types and various operations.

## 🧩 下一步

Reading the documentation provided above is a complex undertaking and it’s difficult to understand the entirety of the TON platform. However, it is a good exercise for those passionate about building on the TON. 阅读上述文档是一项复杂的任务，人们难以完全理解TON平台的全部内容。然而，这对于那些热衷于在TON上建设的人来说是一个很好的练习。另一个建议是开始学习如何在TON上编写智能合约，可以参考以下资源：[FunC概览](https://docs.ton.org/develop/func/overview)，[最佳实践](https://docs.ton.org/develop/smart-contracts/guidelines)，[智能合约示例](https://docs.ton.org/develop/smart-contracts/examples)，[FunC开发手册](https://docs.ton.org/develop/func/cookbook)

此外，建议读者更详细地熟悉以下文档：[ton.pdf](https://docs.ton.org/ton.pdf) 和 [tblkch.pdf](https://ton.org/tblkch.pdf) 文档。

## 📬 关于作者

如果您有任何问题、评论或建议，请通过 [Telegram](https://t.me/aspite) (@aSpite 或 @SpiteMoriarty) 或 [GitHub](https://github.com/aSpite) 联系本文档部分的作者。

## 📖 参阅

- 钱包的源代码：[V3](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet3-code.fc)，[V4](https://github.com/ton-blockchain/wallet-contract/blob/main/func/wallet-v4-code.fc)，[高负载](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/highload-wallet-v2-code.fc)

- 有用的概念文件（可能包含过时信息）：[ton.pdf](https://docs.ton.org/ton.pdf)，[tblkch.pdf](https://ton.org/tblkch.pdf)，[tvm.pdf](https://ton.org/tvm.pdf)

代码的主要来源：

- [@ton/ton (JS/TS)](https://github.com/ton-org/ton)
- [@ton/core (JS/TS)](https://github.com/ton-org/ton-core)
- [@ton/crypto (JS/TS)](https://github.com/ton-org/ton-crypto)
- [tonutils-go (GO)](https://github.com/xssnick/tonutils-go).

官方文档：

- [内部消息](/develop/smart-contracts/guidelines/internal-messages)

- [外部消息](/develop/smart-contracts/guidelines/external-messages)

- [钱包合约类型](/participate/wallets/contracts#wallet-v4)

- [TL-B](/develop/data-formats/tl-b-language)

- [区块链网络](https://docs.ton.org/learn/overviews/ton-blockchain)

外部参考：

- [Ton Deep](https://github.com/xssnick/ton-deep-doc)

- [Block.tlb](https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb)

- [TON中的标准](https://github.com/ton-blockchain/TEPs)
