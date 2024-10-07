# Перехресні ланцюгові мости

Децентралізовані крос-ланцюгові мости працюють на TON Blockchain, дозволяючи переносити активи з TON Blockchain в інші блокчейни і навпаки.

## Toncoin Bridge

Міст Toncoin дозволяє переказувати Toncoin між блокчейном TON і блокчейном Ethereum, а також між блокчейном TON і смарт-ланцюжком BNB.

Мостом керують [децентралізовані оракули](/учасники/кросчейн/адреси мосту).

### Як ним користуватися?

Фронтенд мосту розміщений на https://ton.org/bridge.

:::info
[Вихідний код інтерфейсу мосту](https://github.com/ton-blockchain/bridge)
:::

### Вихідні коди смарт-контрактів TON-Ethereum

- [FunC (сторона TON)](https://github.com/ton-blockchain/bridge-func)
- [Solidity (сторона Ethereum)] (https://github.com/ton-blockchain/bridge-solidity/tree/eth_mainnet)

### Вихідні коди смарт-контрактів TON-BNB Smart Chain

- [FunC (сторона TON)](https://github.com/ton-blockchain/bridge-func/tree/bsc)
- [Солідність (сторона BSC)] (https://github.com/ton-blockchain/bridge-solidity/tree/bsc_mainnet)

### Налаштування блокчейну

Ви можете отримати фактичні адреси мостових смарт-контрактів та адреси оракулів, переглянувши відповідний конфіг:

TON-Ethereum: [#71](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L738).

TON-BSC: [#72](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L739).

ТОН-Полігон: [#73](https://github.com/ton-blockchain/ton/blob/35d17249e6b54d67a5781ebf26e4ee98e56c1e50/crypto/block/block.tlb#L740).

### Документація

- [Як працює міст] (https://github.com/ton-blockchain/TIPs/issues/24)

### Дорожня карта перехресного ланцюга

- https://t.me/tonblockchain/146

## Міст Тонана

### Як взяти участь?

:::caution проект\
Це концептуальна стаття. Ми все ще шукаємо когось досвідченого для її написання.
:::

Ви можете знайти фронтенд тут: https://tonana.org/

Вихідний код знаходиться тут: https://github.com/tonanadao
