# 钱包合约类型

您可能在某处听说过TON区块链中不同版本的钱包。但这些版本实际上意味着什么，它们之间有何不同？

在本文中，我们将研究TON钱包的所有版本和修改。

## 钱包有何不同？

在我们开始之前，我们需要理解钱包究竟能有何不同。

如果我们看一下以太坊、Solana或几乎任何其他区块链，都没有不同类型或版本的钱包。但为什么TON中会存在它们呢？这是因为TON中的钱包是通过智能合约制作的。基本上，任何钱包（甚至是您的钱包）都是在TON区块链上运行的智能合约，它可以接受和发送交易到其他也是智能合约的钱包。

这些智能合约可以以不同的方式设置，并且可以具有不同的功能。这就是为什么TON中有几个版本的钱包。

## 基础钱包

### 钱包V1

这是最简单的一个。它只允许您一次发送一笔交易，除了您的签名和序列号(seqno)，它不检查任何东西。

这个版本甚至没有在常规应用中使用，因为它存在一些主要问题：

- 无法从合约中轻松检索序列号和公钥
- 没有`valid_until`检查，所以您不能确定交易不会太晚被确认。

第一个问题在`V1R2`和`V1R3`中得到修复。`R`字母代表`修订版本`。通常修订版本只是添加get方法，允许您从合约中检索序列号和公钥。
但这个版本还有第二个问题，这个问题在下一个版本中得到修复。

钱包源代码：

- [ton/crypto/smartcont/wallet-code.fc](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet-code.fc)

### 钱包V2

这个版本引入了`valid_until`参数，用于设置交易的时间限制，以防您不希望交易太晚被确认。这个版本也没有公钥的get方法，它在`V2R2`中被添加。

它在大多数情况下都可以使用，但它缺少`V3`中添加的一个酷功能。

钱包源代码：

- [ton/crypto/smartcont/new-wallet-v2.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-wallet-v2.fif)

### 钱包V3

这个版本引入了`subwallet_id`参数，允许您使用同一个公钥创建多个钱包（所以您可以只有一个种子短语和很多钱包）。和以前一样，`V3R2`只添加了公钥的get方法。

基本上，`subwallet_id`只是在部署时添加到合约状态的一个数字。由于TON中的合约地址是其状态和代码的哈希，所以不同的`subwallet_id`将会改变钱包地址。

这个版本目前是最常用的。它涵盖了大多数用例，同时保持简洁和简单。

钱包源代码：

- [ton/crypto/smartcont/wallet-v3-code.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet-v3-code.fif)

### 钱包V4

它是目前最现代的钱包版本。它仍然具有之前版本的所有功能，但还引入了一些非常强大的东西——`插件`。

这个功能允许开发者实现与用户钱包并行工作的复杂逻辑。例如，某些DApp可能需要用户每天支付少量币以使用某些功能，因此用户需要通过签署交易在其钱包上安装插件。这个插件将在每天接收外部消息时向目的地址发送币。

这是一个非常可定制的功能，是TON区块链独有的。

钱包源代码：

- [ton-blockchain/wallet-contract](https://github.com/ton-blockchain/wallet-contract)

## 特殊钱包

有时基础钱包的功能不够。这就是为什么有几种类型的专用钱包：`高负载`、`锁定`和`受限`。

让我们来看看它们。

### 高负载钱包

这种钱包适用于那些需要在短时间内发送数百笔交易的人。例如，加密货币交易所。

- [Source code](https://github.com/ton-blockchain/highload-wallet-contract-v3)

Any given external message (transfer request) to a highload v3 contains:

- **存储大小限制。** 当前，合约存储的大小应小于65535个cell。如果old_queries的大小超过此限制，将在 Action Phase 中抛出异常，交易将失败。
  失败的交易可能会重播。
- **Gas限制。** 当前，Gas限制为1'000'000 GAS单位，这意味着一次交易中可以清理过期查询的数量有限。如果过期查询的数量过多，合约将卡住。
- message to send as a ref (the serialized internal message that will be sent)
- send mode for the message (8 bits)
- composite query ID - 13 bits of "shift" and 10 bits of "bit number", however the 10 bits of bit number can only go up to 1022, not 1023, and also the last such usable query ID (8388605) is reserved for emergencies and should not be normally used
- created at, or message timestamp
- timeout

这意味着不建议设置过高的过期时间：
过期时间跨度内的查询数量不应超过1000。

此外，一次交易中清理的过期查询数量应低于100。

钱包源代码：

- [ton/crypto/smartcont/highload-wallet-v2-code.fc](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/highload-wallet-v2-code.fc)
- not enough balance
- invalid message structure (that includes external out messages - only internal messages may be sent straight from the external message)

Highload v3 will never execute multiple externals containing the same `query_id` **and** `created_at` - by the time it forgets any given `query_id`, the `created_at` condition will prevent such a message from executing. This effectively makes `query_id` **and** `created_at` together the "primary key" of a transfer request for highload v3.

如果您出于某种原因需要在一段时间内锁定钱包中的币，而在这段时间过去之前无法取出它们，请看看锁定钱包。

### Highload wallet v2

:::danger
Legacy contract, it is suggest to use High-load wallet v3.
:::

钱包源代码：

It allows you to send up to `254` transactions in one smart contract call. It also uses a slightly different approach to solve replay attacks instead of seqno, so you can call this wallet several times at once to send even thousands of transactions in a second.

:::caution Limitations
Note, when dealing with highload-wallet the following limits need to be checked and taken into account.
:::

1. **Storage size limit.** Currently, size of contract storage should be less than 65535 cells. If size of
   old_queries will grow above this limit, exception in ActionPhase will be thrown and transaction will fail.
   Failed transaction may be replayed.
2. **Gas limit.** Currently, gas limit is 1'000'000 GAS units, that means that there is a limit of how much
   old queries may be cleaned in one tx. If number of expired queries will be higher, contract will stuck.

钱包源代码：

Also, number of expired queries cleaned in one transaction should be below 100.

Wallet source code:

- [ton/crypto/smartcont/highload-wallet-v2-code.fc](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/highload-wallet-v2-code.fc)

### 参阅

If you, for some reason, need to lock coins in a wallet for some time without the possibility to withdraw them before that time passes, have a look at the lockup wallet.

It allows you to set the time until which you won't be able to withdraw anything from the wallet. You can also customize it by setting unlock periods so that you will be able to spend some coins during these set periods.

For example: you can create a wallet which will hold 1 million coins with total vesting time of 10 years. Set the cliff duration to one year, so the funds will be locked for the first year after the wallet is created. Then, you can set the unlock period to one month, so `1'000'000 TON / 120 months = ~8333 TON` will unlock every month.

Wallet source code:

- [ton-blockchain/lockup-wallet-contract](https://github.com/ton-blockchain/lockup-wallet-contract)

### Restricted wallet

This wallet's function is to act like a regular wallet, but restrict transfers to only one pre-defined destination address. You can set the destination when you create this wallet and then you'll be only able to transfer funds from it to that address. But note that you can still transfer funds to validation contracts so you can run a validator with this wallet.

Wallet source code:

- [EmelyanenkoK/nomination-contract/restricted-wallet](https://github.com/EmelyanenkoK/nomination-contract/tree/master/restricted-wallet)

## Conclusion

As you see, there are many different versions of wallets in TON. But in most cases, you only need `V3R2` or `V4R2`. You can also use one of the special wallets if you want to have some additional functionality like a periodic unlocking of funds.

## See Also

- [Sources of basic wallets](https://github.com/ton-blockchain/ton/tree/master/crypto/smartcont)
- [More technical description of versions](https://github.com/toncenter/tonweb/blob/master/src/contract/wallet/WalletSources.md)
- [Wallet V4 sources and detailed description](https://github.com/ton-blockchain/wallet-contract)
- [Lockup wallet sources and detailed description](https://github.com/ton-blockchain/lockup-wallet-contract)
- [Restricted wallet sources](https://github.com/EmelyanenkoK/nomination-contract/tree/master/restricted-wallet)
