import Feedback from '@site/src/components/Feedback';

# Staking with nominator pools

## مرور کلی

با قراردادهای هوشمند TON، می‌توانید هر مکانیک استیکینگ و واریز دلخواهتان را پیاده‌سازی کنید.

However, there is native staking in TON Blockchain - you can lend Toncoin to validators for staking and share the reward for validation.

کسی که به validator قرض می‌دهد به نام **nominator** شناخته می‌شود.

A smart contract, called a [**nominator pool**](/v3/documentation/smart-contracts/contracts-specs/nominator-pool), provides the ability for one or more nominators to lend Toncoin in a validator stake, and ensures that the validator can use that Toncoin only for validation. This smart contract guarantees the distribution of the reward.

If you are familiar with cryptocurrencies, you must have heard about **validators** and **nominators**. Now, the time has come to find out what they are — the two major actors ruling the blockchain.

## Validator

A validator is a network node that helps keep the blockchain running by verifying (or validating) suggested blocks and recording them on the blockchain.

To become a validator, you must meet two requirements: have a high-performance server and obtain at least 300,000 Toncoins, in order to make a stake. At the time of writing, there are up to 400 validators per round on TON.

## Nominator

:::info
New version of [nominator pool](/v3/documentation/smart-contracts/contracts-specs/nominator-pool/) available, read more in the [Single nominator pool](/v3/documentation/smart-contracts/contracts-specs/single-nominator-pool/) and [Vesting contract](/v3/documentation/smart-contracts/contracts-specs/vesting-contract/) pages.
:::

مشخص است که هر کسی نمی‌تواند 100,000 Toncoin در موجودی خود داشته باشد - اینجاست که Nominator وارد عمل می‌شود. به‌طور ساده، nominatr یک کاربر است که TON خود را به Validators قرض می‌دهد. هر بار که Validator با اعتبارسنجی بلاک‌ها پاداش کسب می‌کند، پاداش بین شرکت‌کنندگان توزیع می‌شود.

TON Whales pool allows a minimum deposit of 50 TON. TON Foundation open nominator pool allows users to stake Toncoin in a fully decentralized way, starting with **10,000 TON**.

*از [پست انجمن TON](https://t.me/toncoin/۵۴۳).*

همیشه باید **۱۰ TON** در موجودی استخر باشد - این کمترین موجودی برای هزینه ذخیره‌سازی شبکه است.

## هزینه در ماه

Since validation round lasts ~18 hours, takes about 5 TON per validation round and 1 nominator pool takes part in even and odd validation rounds it will take **~105 TON per month** to operate the pool.

## روش مشارکت?

- [لیست استخرهای nominator TON](https://tonvalidators.org/)

## کد منبع

- [Nominator pool smart contract source code](https://github.com/ton-blockchain/nominator-pool)

:::info
نظریه nominator در [سفیدنامه TON](https://docs.ton.org/ton.pdf) در فصل‌های ۲.۶.۳ و ۲.۶.۲۵ توضیح داده شده است.
:::

## See also

- [Running validator node](/v3/guidelines/nodes/running-nodes/validator-node)
- [Nominator pool](/v3/documentation/smart-contracts/contracts-specs/nominator-pool/)
- [Single nominator pool](/v3/documentation/smart-contracts/contracts-specs/single-nominator-pool/)
  <Feedback />

