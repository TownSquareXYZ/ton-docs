# 内容订阅

由于TON区块链中的交易很快，网络费用很低， 您可以通过智能合约处理在链上的重复付款。

例如，用户可以订阅数字内容（或任何其他内容），并每月收取1TON的费用。

:::tip
此内容是版本v4的钱包的特定内容。 旧钱包没有此功能；它也可以在未来版本中更改。
:::

:::warning
Subscription contract requires authorization exactly once, on installation; then it can withdraw TON as it pleases. Do your own research before attaching unknown subscriptions.

另一方面，用户在没有知识的情况下无法安装订阅。
:::

## 示例流程

- 用户使用 v4 钱包。 它允许额外的智能合约，称为插件，扩展它的功能。

  在确保其功能后，用户可以批准他钱包的可信智能合同(插件)的地址。 在此之后，可信的智能合约可以从钱包中提取Tonco币。 这类似于其他区块链中的“无限审核”。

- 作为钱包插件，每个用户和服务之间使用中间订阅智能合同。

  这个智能合约保证在一个指定的时期内从用户的钱包中借出一定数量的Tonco币。

- 服务的后端通过向订阅智能合约发送外部信息启动付款。

- 用户或服务可以决定他们不再需要订阅并终止订阅。

## 智能合同示例

- [Wallet v4 智能合同源代码](https://github.com/ton-blockchain/wallet-contract/blob/main/func/wallet-v4-code.fc)
- [订阅智能合同源代码](https://github.com/ton-blockchain/wallet-contract/blob/main/func/simple-subscription-plugin.fc)

## 二． 执行情况

一个很好的实现例子是通过 [@donate](https://t.me/donate) 机器人和 [Tonkeeper wallet](https://tonkeeper.com) 将Tonco币的订阅分散到私人频道。
