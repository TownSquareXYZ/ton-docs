import Feedback from '@site/src/components/Feedback';

import Button from '@ite/src/components/button'

# USDT processing

## Tether

[Apr 18, 2023](https://t.me/toncoin/824), the public launch of native USD₮ token issued by the company <a href="https://tether.to/en/" target="_blank">Tether</a>.

In TON Blockchain USD₮ supported as a [Jetton asset](/v3/guidelines/dapps/asset-processing/jettons).

:::info
Tether の USD₮ トークンを TON ブロックチェーンに統合するには、コントラクトアドレスを使用します：
[EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs](https://tonviewer.com/EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs?section=jetton)
:::

<Button href="https://github.com/ton-community/assets-sdk" colorType="primary" sizeType={'sm'}>Assets SDK</Button>
<Button href="/v3/guidelines/dapps/asset-processing/jettons" colorType={'secondary'} sizeType={'sm'}>Jetton processing</Button>
<Button href="https://github.com/ton-community/tma-usdt-payments-demo?tab=readme-ov-file#tma-usdt-payments-demo" colorType={'secondary'} sizeType={'sm'}>TMA USDT payments demo</Button>

## TON上の USD₮ の利点

### シームレスなTelegramとの統合

[TON上のUSD₮](https://ton.org/borderless)はTelegramにシームレスに統合され、TONをUSDt取引に最も便利なブロックチェーンとして位置づけ、独自のユーザーフレンドリーな体験を提供します。この統合は、TelegramユーザーにとってDeFiを簡素化し、よりアクセスしやすく理解しやすくします。

### 取引手数料の低減

イーサリアムUSD₮送金で消費される手数料は、ネットワーク負荷に応じて動的に計算されます。そのため、取引には多くのコストがかかります。

```cpp
transaction_fee = gas_used * gas_price
```

- `gas_used` は、トランザクション実行中にガスが使用された量です。
- `gas_price` は、Gweiのガス1ユニットの価格です。

一方、TONブロックチェーンで USD₮ を送金する際の平均手数料は、現在約0.0145TONです。TONの価格が100倍になったとしても、取引は[超格安のまま](/develop/smart-contracts/fees#average-transaction-cost) です。TONのコア開発チームは、Tetherのスマートコントラクトを最適化し、他のどのJettonよりも3倍安くしました。

### より高速でスケーラブル

TONの高いスループットと迅速な確認時間により、USD₮ 取引はこれまで以上に迅速に処理されます。

## Advanced details

:::caution 重要

[重要推奨事項](/v3/guidelines/dapps/asset-processing/jettons)をご確認ください。
:::

## See also

- [Payments processing](/v3/guidelines/dapps/asset-processing/payments-processing)

<Feedback />

