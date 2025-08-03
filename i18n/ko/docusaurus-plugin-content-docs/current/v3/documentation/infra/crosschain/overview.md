import Feedback from '@site/src/components/Feedback';

# 크로스체인 브릿지

Decentralized cross-chain bridges function on TON Blockchain, allowing asset transfers between this blockchain and the others.

## Toncoin bridge

The Toncoin bridge enables transfers of Toncoin between TON and Ethereum Blockchain and between TON and the BSC (BNB Smart Chain).

This bridge is managed by [decentralized oracles](/v3/documentation/infra/crosschain/bridge-addresses).

### How to use it

The bridge frontend is hosted [here](https://ton.org/bridge).

:::info
[브릿지 프론트엔드 소스 코드](https://github.com/ton-blockchain/bridge)
:::

### Smart contract source codes

#### TON-Ethereum

- [FunC (TON 측)](https://github.com/ton-blockchain/bridge-func)
- [Solidity (이더리움 측)](https://github.com/ton-blockchain/bridge-solidity/tree/eth_mainnet)

#### TON-BSC (BNB Smart Chain)

- [FunC (TON 측)](https://github.com/ton-blockchain/bridge-func/tree/bsc)
- [Solidity (BSC 측)](https://github.com/ton-blockchain/bridge-solidity/tree/bsc_mainnet)

### Blockchain configurations

You can find the current bridge smart contract addresses and oracle addresses by checking the corresponding configuration:

- TON-Ethereum: [#71](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L738)
- TON-BSC: [#72](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L739)
- TON-Polygon: [#73](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L740)

### 문서

- [브릿지 작동 방식](https://github.com/ton-blockchain/TIPs/issues/24)

### 크로스체인 로드맵

- [@The Open Network](https://t.me/tonblockchain/146)

<Feedback />

