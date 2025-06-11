import Feedback from '@site/src/components/Feedback';

# クロスチェーンブリッジ

Decentralized cross-chain bridges function on TON Blockchain, allowing asset transfers between this blockchain and the others.

## Toncoin bridge

The Toncoin bridge enables transfers of Toncoin between TON and Ethereum Blockchain and between TON and the BSC (BNB Smart Chain).

This bridge is managed by [decentralized oracles](/v3/documentation/infra/crosschain/bridge-addresses).

### How to use it

The bridge frontend is hosted [here](https://ton.org/bridge).

:::info
[ブリッジ・フロントエンドのソースコード](https://github.com/ton-blockchain/bridge)
:::

### Smart contract source codes

#### TON-Ethereum

- [Func（TON側）](https://github.com/ton-blockchain/bridge-func)
- [ソリディティ（イーサリアム側）](https://github.com/ton-blockchain/bridge-solidity/tree/eth_mainnet)

#### TON-BSC (BNB Smart Chain)

- [Func（TON側）](https://github.com/ton-blockchain/bridge-func/tree/bsc)
- [ソリディティ（BSC側）](https://github.com/ton-blockchain/bridge-solidity/tree/bsc_mainnet)

### Blockchain configurations

You can find the current bridge smart contract addresses and oracle addresses by checking the corresponding configuration:

- TON-Ethereum: [#71](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L738)
- TON-BSC: [#72](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L739)
- TON-Polygon: [#73](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L740)

### ドキュメンテーション

- [橋の仕組み](https://github.com/ton-blockchain/TIPs/issues/24)

### クロスチェーンのロードマップ

- [@The Open Network](https://t.me/tonblockchain/146)

<Feedback />

