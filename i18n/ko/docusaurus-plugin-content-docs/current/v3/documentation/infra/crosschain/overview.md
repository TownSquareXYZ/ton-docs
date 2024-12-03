# 크로스체인 브릿지

TON 블록체인에서 운영되는 탈중앙화 크로스체인 브릿지를 통해 TON 블록체인과 다른 블록체인 간의 자산 이동이 가능합니다.

## Toncoin 브릿지

Toncoin 브릿지는 TON 블록체인과 이더리움 블록체인 사이, 그리고 TON 블록체인과 BNB 스마트 체인 사이에서 Toncoin을 전송할 수 있게 해줍니다.

브릿지는 [탈중앙화 오라클](/v3/documentation/infra/crosschain/bridge-addresses)이 관리합니다.

### 사용 방법

브릿지 프론트엔드는 https://ton.org/bridge 에서 호스팅됩니다.

:::info
[브릿지 프론트엔드 소스 코드](https://github.com/ton-blockchain/bridge)
:::

### TON-이더리움 스마트 컨트랙트 소스 코드

- [FunC (TON 측)](https://github.com/ton-blockchain/bridge-func)
- [Solidity (이더리움 측)](https://github.com/ton-blockchain/bridge-solidity/tree/eth_mainnet)

### TON-BNB 스마트 체인 스마트 컨트랙트 소스 코드

- [FunC (TON 측)](https://github.com/ton-blockchain/bridge-func/tree/bsc)
- [Solidity (BSC 측)](https://github.com/ton-blockchain/bridge-solidity/tree/bsc_mainnet)

### 블록체인 설정

해당 설정을 검사하여 실제 브릿지 스마트 컨트랙트 주소와 오라클 주소를 얻을 수 있습니다:

TON-Ethereum: [#71](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L738)

TON-BSC: [#72](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L739)

TON-Polygon: [#73](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L740)

### 문서

- [브릿지 작동 방식](https://github.com/ton-blockchain/TIPs/issues/24)

### 크로스체인 로드맵

- https://t.me/tonblockchain/146
