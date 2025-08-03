# Mostki międzyłańcuchowe

Zdecentralizowane mosty międzyłańcuchowe działają na TON Blockchain, umożliwiając przesyłanie aktywów z TON Blockchain do innych łańcuchów bloków i odwrotnie.

## Most Toncoin

Most Toncoin umożliwia przesyłanie Toncoinów między TON Blockchain a blockchainem Ethereum, a także między TON Blockchain a BNB Smart Chain.

Most jest zarządzany przez [zdecentralizowane wyrocznie] (/participate/crosschain/bridge-addresses).

### Jak go używać?

Frontend Bridge jest hostowany na stronie https://ton.org/bridge.

:::info
[Kod źródłowy interfejsu Bridge](https://github.com/ton-blockchain/bridge)
:::

### Kody źródłowe inteligentnych kontraktów TON-Ethereum

- [FunC (strona TON)](https://github.com/ton-blockchain/bridge-func)
- [Solidity (strona Ethereum)](https://github.com/ton-blockchain/bridge-solidity/tree/eth_mainnet)

### Kody źródłowe inteligentnych kontraktów TON-BNB Smart Chain

- [FunC (strona TON)](https://github.com/ton-blockchain/bridge-func/tree/bsc)
- [Solidity (strona BSC)](https://github.com/ton-blockchain/bridge-solidity/tree/bsc_mainnet)

### Konfiguracje blockchain

Rzeczywiste adresy inteligentnych kontraktów bridge i adresy oracle można uzyskać, sprawdzając odpowiednią konfigurację:

TON-Ethereum: [#71](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L738).

TON-BSC: [#72](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L739).

TON-Polygon: [#73](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L740).

### Dokumentacja

- [Jak działa most](https://github.com/ton-blockchain/TIPs/issues/24)

### Międzyłańcuchowa mapa drogowa

- https://t.me/tonblockchain/146

## Most Tonana

### Jak wziąć udział?

:::caution projekt\
To jest artykuł koncepcyjny. Wciąż szukamy kogoś doświadczonego, kto mógłby go napisać.
:::

Front-end znajdą Państwo tutaj: https://tonana.org/

Kod źródłowy znajduje się tutaj: https://github.com/tonanadao
