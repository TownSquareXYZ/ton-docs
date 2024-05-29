# 크로스 체인 브리지

탈중앙화 크로스체인 브리지는 TON 블록체인에서 작동하며, 이를 통해 TON 블록체인에서 다른 블록체인으로 또는 그 반대로 자산을 전송할 수 있습니다.

## 톤코인 브리지

톤코인 브릿지를 사용하면 톤 블록체인과 이더리움 블록체인 간은 물론, 톤 블록체인과 BNB 스마트 체인 간에도 톤코인을 전송할 수 있습니다.

브리지는 [탈중앙화 오라클](/참여/크로스체인/브리지 주소)에 의해 관리됩니다.

### 어떻게 사용하나요?

Bridge 프론트엔드는 https://ton.org/bridge 에서 호스팅됩니다.

:::info
[브리지 프론트엔드 소스 코드](https://github.com/ton-blockchain/bridge)
:::

### TON- 이더리움 스마트 컨트랙트 소스 코드

- [FunC(TON 측)](https://github.com/ton-blockchain/bridge-func)
- [솔리디티(이더리움 측)](https://github.com/ton-blockchain/bridge-solidity/tree/eth_mainnet)

### TON-BNB 스마트 체인 스마트 컨트랙트 소스 코드

- [FunC(TON 측)](https://github.com/ton-blockchain/bridge-func/tree/bsc)
- [견고성(BSC 측)](https://github.com/ton-blockchain/bridge-solidity/tree/bsc_mainnet)

### 블록체인 구성

해당 구성을 검사하여 실제 브리지 스마트 컨트랙트 주소와 오라클 주소를 얻을 수 있습니다:

톤-에테리움: [#71](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L738).

TON-BSC: [#72](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L739).

톤-다각형: [#73](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L740).

### 문서

- [브리지 작동 방식](https://github.com/ton-blockchain/TIPs/issues/24)

### 크로스 체인 로드맵

- https://t.me/tonblockchain/146

## 토나나 다리

### 어떻게 참여하나요?

:::caution 초안\
이 글은 콘셉트 기사입니다. 아직 글을 작성해 주실 경험자를 찾고 있습니다.
:::

프런트엔드는 여기에서 찾을 수 있습니다: https://tonana.org/

소스 코드는 여기에 있습니다: https://github.com/tonanadao
