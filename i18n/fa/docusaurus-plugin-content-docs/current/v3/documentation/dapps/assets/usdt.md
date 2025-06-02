import Feedback from '@site/src/components/Feedback';

import Button from '@site/src/components/button'

# USDT processing

## تتر

[Apr 18, 2023](https://t.me/toncoin/824), the public launch of native USD₮ token issued by the company <a href="https://tether.to/en/" target="_blank">Tether</a>.

In TON Blockchain USD₮ supported as a [Jetton asset](/v3/guidelines/dapps/asset-processing/jettons).

:::info
برای ادغام توکن USD₮ تتر در بلاکچین TON از آدرس قرارداد زیر استفاده کنید:
[EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs](https://tonviewer.com/EQCxE6mUtQJKFnGfaROTKOt1lZbDiiX1kCixRv7Nw2Id_sDs?section=jetton)
:::

<Button href="https://github.com/ton-community/assets-sdk" colorType="primary" sizeType={'sm'}>Assets SDK</Button>
<Button href="/v3/guidelines/dapps/asset-processing/jettons" colorType={'secondary'} sizeType={'sm'}>Jetton processing</Button>
<Button href="https://github.com/ton-community/tma-usdt-payments-demo?tab=readme-ov-file#tma-usdt-payments-demo" colorType={'secondary'} sizeType={'sm'}>TMA USDT payments demo</Button>

## مزایای USD₮ در TON

### ادغام بی‌نقص تلگرام

[USD₮ در TON](https://ton.org/borderless) به‌صورت بی‌نقص در تلگرام ادغام خواهد شد و تجربه‌ای کاربرپسند ارائه می‌دهد که TON را به عنوان مناسب‌ترین بلاکچین برای تراکنش‌های USDt معرفی می‌کند. این ادغام باعث ساده‌سازی DeFi برای کاربران تلگرام خواهد شد و قابلیت دسترسی و درک آن را افزایش می‌دهد.

### هزینه‌های پایین‌تر تراکنش‌ها

Fees for Ethereum USD₮ transfers are calculated dynamically depending on network load. This is why transactions can become expensive.

```cpp
transaction_fee = gas_used * gas_price
```

- `gas_used` is the amount of gas used during transaction execution.
- `gas_price` is the cost of one unit of gas in Gwei, calculated dynamically.

On the other hand average fee for sending any amount of USD₮ in TON Blockchain is about 0.0145 TON nowadays. Even if the price of TON increases 100 times, transactions will [remain ultra-cheap](/v3/documentation/smart-contracts/transaction-fees/fees#average-transaction-cost). The core TON development team has optimized Tether’s smart contract to make it three times cheaper than any other Jetton.

### سریع‌تر و مقیاس‌پذیر

توان عملیاتی بالا و زمان‌های تایید سریع در TON امکان پردازش تراکنش‌های USD₮ را سریع‌تر از گذشته فراهم می‌کند.

## Advanced details

:::caution مهم

توصیه‌های [مهم](/v3/guidelines/dapps/asset-processing/jettons) را ببینید.
:::

## See also

- [Payments processing](/v3/guidelines/dapps/asset-processing/payments-processing)

<Feedback />

