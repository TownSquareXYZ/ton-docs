# 本机令牌：Toncoin

TON Blockchain 原生的加密货币是**Toncoin**。

交易费、气体付款(即智能合同电文处理费)和持久性储存付款都在Toncoin收取。

Tonco币用于使存款成为区块链验证器。

支付Tonco币的过程在[相应章节](/develop/dapps/asset-processing)中描述。

您可以在 [website](https://ton.org/coin)上找到购买或兑换Tonco币的地点。

## 额外货币

TON Blockchain 最多支持2^32内置货币。

额外货币余额可以存储在每个区块链帐户上，然后本地转到其他帐户(从一个智能合同到另一个的内部消息)。 除了Tonco币金额外，您可以指定额外货币金额的哈希图。

TLB: `extra_currencies$_ dict:(HashmapE 32 (VarUInteger 32)) = ExtraCurrencyCollection;` - hashmap of currency ID and amount.

然而，额外货币只能储存和转移(如Toncoin)并且没有自己的任意代码或功能。

请注意，如果创建了大量额外货币，帐户将会“精彩”，因为它们需要存储它们。

因此，额外货币最好用于众所周知的分散货币（例如： 包装的比特币或以太币，创建这种额外的货币应该是非常昂贵的。

[Jettons](/develop/dapps/违抗/tokens#jettons) 适合其他任务。

目前，TON Blockchain没有创建额外货币。 TON Blockchain 通过帐户和消息完全支持额外的货币，但创建这些货币的矿工系统合同尚未创建。
