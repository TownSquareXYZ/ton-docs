# TON 上的订阅服务

由于 TON 区块链中的交易快速，网络费用低廉，您可以通过智能合约在链上处理定期支付。

例如，用户可以订阅数字内容（或其他任何东西）并被收取每月 1 TON 的费用。

:::tip
This content is specific for wallets of version v4. Older wallets don't have this functionality; it is eligible to change in future versions as well.
:::

:::warning
Subscription contract requires authorization exactly once, on installation; then it can withdraw TON as it pleases. Do your own research before attaching unknown subscriptions.

目前的标准方法：

## Example flow

- Users use a v4 wallet. It allows additional smart contracts, known as plugins, to extend its functionality.

  After ensuring their functionality, the user can approve the addresses of trusted smart contracts (plugins) for his wallet. Following that, the trusted smart contracts can withdraw Toncoin from the wallet. This is similar to "Infinite Approval" in some other blockchains.

- An intermediate subscription smart contract is used between each user and service as a wallet plugin.

  This smart contract guarantees that a specified amount of Toncoin will be debited from a user's wallet no more than once within a specified period.

- The service's backend initiates payments on a regular basis by sending an external message to subscription smart contracts.

- Either user or service can decide they no longer need a subscription and terminate it.

## Smart contract examples

- [Wallet v4 smart contract source code](https://github.com/ton-blockchain/wallet-contract/blob/main/func/wallet-v4-code.fc)
- [Subscription smart contract source code](https://github.com/ton-blockchain/wallet-contract/blob/main/func/simple-subscription-plugin.fc)

## Implementation

A good example of implementation is decentralized subscriptions for Toncoin to private channels in Telegram by the [@donate](https://t.me/donate) bot and the [Tonkeeper wallet](https://tonkeeper.com).
