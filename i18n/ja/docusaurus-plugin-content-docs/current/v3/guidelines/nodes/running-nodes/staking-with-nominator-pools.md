import Feedback from '@site/src/components/Feedback';

# Staking with nominator pools

## 概要

TON スマートコントラクトを使用すると、任意のステーキングと預金メカニズムを実装できます。

However, there is native staking in TON Blockchain - you can lend Toncoin to validators for staking and share the reward for validation.

バリデータに貸し出すのは **nominator** と呼ばれます。

A smart contract, called a [**nominator pool**](/v3/documentation/smart-contracts/contracts-specs/nominator-pool), provides the ability for one or more nominators to lend Toncoin in a validator stake, and ensures that the validator can use that Toncoin only for validation. This smart contract guarantees the distribution of the reward.

If you are familiar with cryptocurrencies, you must have heard about **validators** and **nominators**. Now, the time has come to find out what they are — the two major actors ruling the blockchain.

## Validator

A validator is a network node that helps keep the blockchain running by verifying (or validating) suggested blocks and recording them on the blockchain.

To become a validator, you must meet two requirements: have a high-performance server and obtain at least 300,000 Toncoins, in order to make a stake. At the time of writing, there are up to 400 validators per round on TON.

## Nominator

:::info
New version of [nominator pool](/v3/documentation/smart-contracts/contracts-specs/nominator-pool/) available, read more in the [Single nominator pool](/v3/documentation/smart-contracts/contracts-specs/single-nominator-pool/) and [Vesting contract](/v3/documentation/smart-contracts/contracts-specs/vesting-contract/) pages.
:::

誰もが自分の残高に10万のToncoinを持つ余裕がないことは明らかです - ここにノミネーターが登場する場所です。 簡単に言えば、推薦者はバリデータにTON を貸し出すユーザーです。 バリデータがブロックを検証することで報酬を獲得するたびに、参加者間で分配されます。

TON Whales pool allows a minimum deposit of 50 TON. TON Foundation open nominator pool allows users to stake Toncoin in a fully decentralized way, starting with **10,000 TON**.

*From format@@0(https://t.me/toncoin/543).*

プール残高には**10 TON**が必要です。これはネットワークストレージ料金の最小残高です。

## Cost per month

Since validation round lasts ~18 hours, takes about 5 TON per validation round and 1 nominator pool takes part in even and odd validation rounds it will take **~105 TON per month** to operate the pool.

## 参加方法は？

- format@@0(https://tonvalidators.org/)

## ソース コード

- [Nominator pool smart contract source code](https://github.com/ton-blockchain/nominator-pool)

:::info
推薦者の理論は、format@@0(https://docs.ton.org/ton.pdf)2.6.3, 2.6.25章で説明されています。
:::

## See also

- [Running validator node](/v3/guidelines/nodes/running-nodes/validator-node)
- [Nominator pool](/v3/documentation/smart-contracts/contracts-specs/nominator-pool/)
- [Single nominator pool](/v3/documentation/smart-contracts/contracts-specs/single-nominator-pool/)
  <Feedback />

