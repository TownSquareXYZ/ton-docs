# TON付款

TON 付款是小额支付渠道的平台。

它允许即时支付，无需将所有交易提交到区块链，支付相关的交易费 (e)。 .等候五秒钟，直到包含有关交易的
方块得到确认。

由于这种即时支付的总费用如此之低，它们可以用于游戏、API和脱链应用中的微额支付。 [见例子](/develop/dapps/违抗/ton-payments#examps)。

- [TON付款](https://blog.ton.org/ton-pays)

## 支付频道

### 智能合同

- [ton-blockchain/pay-channels](https://github.com/ton-blockchain/pay-channels)

### SDK

要使用付款通道，您不需要深入了解加密技术。

您可以使用准备的 SDK：

- [toncenter/tonweb](https://github.com/toncenter/tonweb) JavaScript SDK
- [toncenter/pay-channels-example](https://github.com/toncenter/payment-channels-example)-如何使用带有tonweb的付款频道。

### 示例：

查找在[Hack-a-TON #1](https://ton.org/hack-a-ton-1) 中使用付款渠道的例子：

- [grejwood/Hack-a-TON](https://github.com/Grejwood/Hack-a-TON)-OnlyTONs付款项目([website](https://main.d3puvu1kvbh8ti.amplifyapp.com/), [video](https://www.youtube.com/watch?v=38JpX1vRNTk))
- [nns2009/Hack-a-TON-1_Tonario](https://github.com/nns2009/Hack-a-TON-1_Tonario)-仅支付项目([website](https://onlygrams.io/), [video](https://www.youtube.com/watch?v=gm5-FPWn1XM))
- [sevezing/hack-a-ton](https://github.com/sevezing/hack-a-ton)-Pay-per Request API 使用于TON ([video](https://www.youtube.com/watch?v=7lAnbyJdpOA\&feature=youtu.be))
- [illright/diamonds](https://github.com/illright/diamonds)__pay-per Minute learning platform ([website](https://diamonds-ton.vercel.app/), [video](https://www.youtube.com/watch?v=g9wmdOjAv1s))

## 另见：

- [付款处理](/develop/dapps/asset-processing)
- [TON 连接](/develop/dapps/ton-connect)
