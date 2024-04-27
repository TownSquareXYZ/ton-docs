# 钱包准则

## 网络

### 没有很多网络。

目前，只有两个网络――主网和试验网。
在可预见的将来，预计不会出现新的主要网络TON式网络。 请注意当前的Mainnet有一个内置的替代网络――工作链机制。

### 向普通用户隐藏测试网。

测试网仅供开发者使用。 普通用户不应查看 Testnet。
这意味着切换到 Testnet 不应轻松可用，用户SHOULD 不会被提示将钱包切换到 Testnet ，即使DAppis 在 Testnet。
用户切换到 Testnet，不了解这个动作，不能切换回Mainnet。

由于这些原因，dapps不需要在运行时切换网络。 更可取的做法是 DAppon 不同域名的不同实例。 om, Testnet.dapp.com。
出于同样的原因，Ton Connect 协议中没有`NetworkChanged`或`ChainChanged`事件。

### 如果数据库在 Testnet 和 Mainnet，请勿发送任何信息。

当DApp试图在 Testnet中发送交易和钱包在 Mainnet中发送交易时，必须防止资金流失。

Dapps应在 `SendTransaction` 请求中明确显示 `network` 字段。

如果设置了 `network` 参数，但钱包有不同的网络集合。 钱包应该显示警报，不要再发送此交易。

在这种情况下，钱包不能切换到另一个网络。

## 多账户

可以为一个密钥对创建多个网络帐户。 在你的钱包中实现这个功能——用户会发现它是有用的。

### 总的来说没有当前的“活动”账户

目前，TON Connect 并不是建立在钱包中有一个选定账户的模式上的。 当用户切换到另一个帐户时，`AccountChanged`事件将被发送到舞台。

我们认为钱包是一个实际钱包，可以包含许多“银行卡”(帐户)。

在大多数情况下，发件人地址对编程并不重要， 在这些情况下，用户可以在批准交易时选择适当的账户，交易将从选定的账户中发送。

在某些情况下，DApp必须从一个特定地址发送交易。 在这种情况下，它在`SendTransaction`请求中明确指定`from`字段。 如果设置了 `from` 参数，钱包应该不允许用户选择发件人的地址； 如果无法从指定地址发送，钱包应显示警报，不要再发送此交易。

### 登录流程

当DApp连接钱包时，用户在钱包中选择他们想要登录到数据库的账户之一。

无论用户在钱包中使用什么帐户，DApp都与他在连接上收到的帐户合作。

就像您使用您的电子邮件帐户登录网络服务一样——如果您随后更改电子邮件服务中的电子邮件帐户的话。 网站服务继续使用他在登录时得到的服务。

为此原因，协议没有提供 `AccountChanged` 事件。

要切换帐户，用户需要断开连接 (注销) 并在 DAppUI 中再次连接 (登录)。

我们推荐钱包提供了与指定的DApp断开会话的能力，因为DApp可能有不完整的UI。

## 另见：

- [TON Connect Overview](/dapps/ton-connect/overview.)
- [Protocol specifications](/dapps/ton-connect/protocol/)
- [Connect a Wallet](/dapps/ton-connect/wallet)
