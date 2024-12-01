---
description: 이 가이드의 마지막에는 멀티시그 지갑을 배포하고 TON 라이브러리를 사용해 몇 가지 트랜잭션을 전송하게 됩니다.
---

# TypeScript를 사용하여 멀티시그 지갑과 상호작용하기

## 소개

TON의 멀티시그 지갑에 대해 모르신다면 [여기](/v3/guidelines/smart-contracts/howto/multisig)에서 확인할 수 있습니다.

다음 단계들을 통해 배우게 될 내용:

- 멀티시그 지갑 생성 및 배포하기
- 해당 지갑으로 트랜잭션 생성, 서명, 전송하기

TypeScript 프로젝트를 만들고 [ton](https://www.npmjs.com/package/ton) 라이브러리를 사용할 것이므로 먼저 설치해야 합니다. [ton-access](https://www.orbs.com/ton-access/)도 사용할 예정입니다:

```bash
yarn add typescript @types/node ton ton-crypto ton-core buffer @orbs-network/ton-access
yarn tsc --init -t es2022
```

이 가이드의 전체 코드는 다음에서 확인할 수 있습니다:

- https://github.com/Gusarich/multisig-ts-example

## 멀티시그 지갑 생성 및 배포

소스 파일(예: `main.ts`)을 생성합시다. 선호하는 코드 에디터에서 열고 이 가이드를 따라가세요!

먼저 필요한 것들을 모두 임포트해야 합니다

```js
import { Address, beginCell, MessageRelaxed, toNano, TonClient, WalletContractV4, MultisigWallet, MultisigOrder, MultisigOrderBuilder } from "ton";
import { KeyPair, mnemonicToPrivateKey } from 'ton-crypto';
import { getHttpEndpoint } from "@orbs-network/ton-access";
```

`TonClient` 인스턴스 생성:

```js
const endpoint = await getHttpEndpoint();
const client = new TonClient({ endpoint });
```

그런 다음 작업할 keypair가 필요합니다:

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

`MultisigWallet` 객체를 생성하는 두 가지 방법이 있습니다:

- 기존 주소에서 가져오기

```js
let addr: Address = Address.parse('EQADBXugwmn4YvWsQizHdWGgfCTN_s3qFP0Ae0pzkU-jwzoE');
let mw: MultisigWallet = await MultisigWallet.fromAddress(addr, { client });
```

- 새로 생성하기

```js
let mw: MultisigWallet = new MultisigWallet([keyPairs[0].publicKey, keyPairs[1].publicKey], 0, 0, 1, { client });
```

배포하는 두 가지 방법도 있습니다

- 내부 메시지를 통해

```js
let wallet: WalletContractV4 = WalletContractV4.create({ workchain: 0, publicKey: keyPairs[4].publicKey });
//wallet should be active and have some balance
await mw.deployInternal(wallet.sender(client.provider(wallet.address, null), keyPairs[4].secretKey), toNano('0.05'));
```

- 외부 메시지를 통해

```js
await mw.deployExternal();
```

## 주문 생성, 서명, 전송

새 주문을 생성하려면 `MultisigOrderBuilder` 객체가 필요합니다.

```js
let order1: MultisigOrderBuilder = new MultisigOrderBuilder(0);
```

그런 다음 메시지를 추가할 수 있습니다.

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

메시지 추가가 끝나면 `build()` 메서드를 호출하여 `MultisigOrderBuilder`를 `MultisigOrder`로 변환합니다.

```js
let order1b: MultisigOrder = order1.build();
order1b.sign(0, keyPairs[0].secretKey);
```

이제 다른 주문을 생성하고, 메시지를 추가하고, 다른 키 세트로 서명한 다음 이러한 주문의 서명을 통합해보겠습니다.

```js
let order2: MultisigOrderBuilder = new MultisigOrderBuilder(0);
order2.addMessage(msg, 3);
let order2b = order2.build();
order2b.sign(1, keyPairs[1].secretKey);

order1b.unionSignatures(order2b); //Now order1b have also have all signatures from order2b
```

마지막으로 서명된 주문을 보냅니다:

```js
await mw.sendOrder(order1b, keyPairs[0].secretKey);
```

이제 프로젝트를 빌드합니다

```bash
yarn tsc
```

그리고 컴파일된 파일을 실행합니다

```bash
node main.js
```

오류가 발생하지 않는다면 모든 것을 올바르게 했습니다! 이제 익스플로러나 지갑으로 트랜잭션이 성공했는지 확인하세요.

## 기타 메서드와 속성

`MultisigOrderBuilder` 객체에서 메시지를 쉽게 지울 수 있습니다:

```js
order2.clearMessages();
```

`MultisigOrder` 객체에서 서명도 지울 수 있습니다:

```js
order2b.clearSignatures();
```

그리고 물론 `MultisigWallet`, `MultisigOrderBuilder`, `MultisigOrder` 객체에서 공개 속성을 가져올 수 있습니다

- MultisigWallet:
  - `owners` - 서명의 `Dictionary<number, Buffer>` *ownerId => signature*
  - `workchain` - 지갑이 배포된 workchain
  - `walletId` - 지갑 id
  - `k` - 트랜잭션 확인에 필요한 서명 수
  - `address` - 지갑 주소
  - `provider` - `ContractProvider` 인스턴스

- MultisigOrderBuilder
  - `messages` - 주문에 추가될 `MessageWithMode` 배열
  - `queryId` - 주문이 유효한 전역 시간

- MultisigOrder
  - `payload` - 주문 페이로드가 있는 `Cell`
  - `signatures` - 서명의 `Dictionary<number, Buffer>` *ownerId => signature*

## 참조

- [로우레벨 멀티시그 가이드](/v3/guidelines/smart-contracts/howto/multisig)
- [ton.js 문서](https://ton-community.github.io/ton/)
- [멀티시그 컨트랙트 소스](https://github.com/ton-blockchain/multisig-contract)
