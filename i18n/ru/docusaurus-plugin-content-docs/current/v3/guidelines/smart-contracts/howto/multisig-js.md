---
description: В конце этого руководства вы развернете мультиподписной кошелек и отправите несколько транзакций с помощью библиотеки ton
---

# Взаимодействие с мультиподписными кошельками с помощью TypeScript

## Введение

Если вы не знаете, что такое мультиподписной кошелек в ​​TON, вы можете ознакомиться с этим [здесь](/v3/guidelines/smart-contracts/howto/multisig)

Выполнив эти шаги, вы узнаете, как:

- Создать и развернуть мультиподписной кошелек
- Создать, подписать и отправить транзакции с помощью этого кошелька

Мы создадим проект TypeScript и используем библиотеку [ton](https://www.npmjs.com/package/ton), поэтому вам нужно сначала установить ее. Мы также будем использовать [ton-access](https://www.orbs.com/ton-access/):

```bash
yarn add typescript @types/node ton ton-crypto ton-core buffer @orbs-network/ton-access
yarn tsc --init -t es2022
```

Полный код этого руководства доступен здесь:

- https://github.com/Gusarich/multisig-ts-example

## Создание и развертывание мультиподписного кошелька

Давайте создадим исходный файл, например `main.ts`. Откройте его в своем любимом редакторе кода и следуйте этому руководству!

Сначала нам нужно импортировать все важные данные

```js
import { Address, beginCell, MessageRelaxed, toNano, TonClient, WalletContractV4, MultisigWallet, MultisigOrder, MultisigOrderBuilder } from "ton";
import { KeyPair, mnemonicToPrivateKey } from 'ton-crypto';
import { getHttpEndpoint } from "@orbs-network/ton-access";
```

Создайте экземпляр `TonClient`:

```js
const endpoint = await getHttpEndpoint();
const client = new TonClient({ endpoint });
```

Затем нам понадобятся пары ключей для работы:

```js
let keyPairs: KeyPair[] = [];

let mnemonics[] = [
    ['orbit', 'feature', ...], //this should be the seed phrase of 24 words
    ['sing', 'pattern',  ...],
    ['piece', 'deputy', ...],
    ['toss', 'shadow',  ...],
    ['guard', 'nurse',   ...]
];

for (let i = 0; i < mnemonics.length; i++) keyPairs[i] = await mnemonicToPrivateKey(mnemonics[i]);
```

Существует два способа создать объект `MultisigWallet`:

- Импортируйте существующий из адреса

```js
let addr: Address = Address.parse('EQADBXugwmn4YvWsQizHdWGgfCTN_s3qFP0Ae0pzkU-jwzoE');
let mw: MultisigWallet = await MultisigWallet.fromAddress(addr, { client });
```

- Создайте новый

```js
let mw: MultisigWallet = new MultisigWallet([keyPairs[0].publicKey, keyPairs[1].publicKey], 0, 0, 1, { client });
```

Также есть два способа его развертывания

- С помощью внутреннего сообщения

```js
let wallet: WalletContractV4 = WalletContractV4.create({ workchain: 0, publicKey: keyPairs[4].publicKey });
//wallet should be active and have some balance
await mw.deployInternal(wallet.sender(client.provider(wallet.address, null), keyPairs[4].secretKey), toNano('0.05'));
```

- С помощью внешнего сообщения

```js
await mw.deployExternal();
```

## Создание, подпись и отправка заявки

Нам нужен объект `MultisigOrderBuilder` для создания новой заявки.

```js
let order1: MultisigOrderBuilder = new MultisigOrderBuilder(0);
```

Затем мы можем добавить в нее несколько сообщений.

```js
let msg: MessageRelaxed = {
    body: beginCell().storeUint(0, 32).storeBuffer(Buffer.from('Hello, world!')).endCell(),
    info: {
        bounce: true,
        bounced: false,
        createdAt: 0,
        createdLt: 0n,
        dest: Address.parse('EQArzP5prfRJtDM5WrMNWyr9yUTAi0c9o6PfR4hkWy9UQXHx'),
        forwardFee: 0n,
        ihrDisabled: true,
        ihrFee: 0n,
        type: "internal",
        value: { coins: toNano('0.01') }
    }
};

order1.addMessage(msg, 3);
```

После того, как вы закончите с добавлением сообщений, преобразуйте `MultisigOrderBuilder` в `MultisigOrder`, вызвав метод `build()`.

```js
let order1b: MultisigOrder = order1.build();
order1b.sign(0, keyPairs[0].secretKey);
```

Теперь давайте создадим еще одну заявку, добавим в нее сообщение, подпишем ее другим набором ключей и объединим подписи этих заявок.

```js
let order2: MultisigOrderBuilder = new MultisigOrderBuilder(0);
order2.addMessage(msg, 3);
let order2b = order2.build();
order2b.sign(1, keyPairs[1].secretKey);

order1b.unionSignatures(order2b); //Now order1b have also have all signatures from order2b
```

И, наконец, отправим подписанную заявку:

```js
await mw.sendOrder(order1b, keyPairs[0].secretKey);
```

Теперь соберите проект

```bash
yarn tsc
```

И запустите скомпилированный файл

```bash
node main.js
```

Если он не выдает никаких ошибок, вы все сделали правильно! Теперь проверьте, прошла ли ваша транзакция успешно с помощью любого обозревателя или кошелька.

## Другие методы и свойства

Вы можете легко очистить сообщения из объектов `MultisigOrderBuilder`:

```js
order2.clearMessages();
```

Вы также можете очистить подписи из объектов `MultisigOrder`:

```js
order2b.clearSignatures();
```

И, конечно, вы можете получить публичные свойства из объектов `MultisigWallet`, `MultisigOrderBuilder` и `MultisigOrder`

- MultisigWallet:
  - `owners` - `словарь <number, Buffer>` подписей *ownerId => signature*
  - `workchain` - воркчейн, где развернут кошелек
  - `walletId` - идентификатор кошелька
  - `k` - количество подписей, необходимых для подтверждения транзакции
  - `address` - адрес кошелька
  - `provider` - экземпляр `ContractProvider`.

- MultisigOrderBuilder
  - `messages` - массив `MessageWithMode`, который будет добавлен к заявке
  - `queryId` - глобальное время, до которого заявка действительна

- MultisigOrder
  - `payload` - `Cell` с платой за payload
  - `signatures` - `словарь <number, Buffer>` подписей *ownerId => signature*

## Ссылки

- [Руководство по низкоуровневой мультиподписи](/v3/guidelines/smart-contracts/howto/multisig)
- [Документация ton.js](https://ton-community.github.io/ton/)
- [Источники контрактов Multisig](https://github.com/ton-blockchain/multisig-contract)