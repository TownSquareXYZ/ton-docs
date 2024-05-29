---
description: 이 가이드의 마지막 부분에서는 멀티서명 지갑을 배포하고 톤 라이브러리를 사용하여 몇 가지 트랜잭션을 전송합니다.
---

# TypeScript를 사용하여 다중 서명 지갑과 상호작용하기

## 소개

TON에서 다중서명 지갑이 무엇인지 모르신다면 [여기](/개발/스마트 컨트랙트/자습서/멀티서그)에서 확인하실 수 있습니다.

이 단계를 따라 방법을 배워보세요:

- 다중서명 지갑 생성 및 배포
- 해당 지갑으로 트랜잭션 생성, 서명, 전송하기

타입스크립트 프로젝트를 생성하고 [ton](https://www.npmjs.com/package/ton) 라이브러리를 사용할 예정이므로 먼저 설치해야 합니다. 톤 액세스](https://www.orbs.com/ton-access/)도 사용할 것입니다:

```bash
yarn add typescript @types/node ton ton-crypto ton-core buffer @orbs-network/ton-access
yarn tsc --init -t es2022
```

이 가이드의 전체 코드는 여기에서 확인할 수 있습니다:

- https://github.com/Gusarich/multisig-ts-example

## 다중서명 지갑 생성 및 배포

예를 들어 `main.ts`라는 소스 파일을 만들어 보겠습니다. 즐겨 사용하는 코드 편집기에서 파일을 열고 이 가이드를 따르세요!

먼저 모든 중요한 항목을 가져와야 합니다.

```js
import { Address, beginCell, MessageRelaxed, toNano, TonClient, WalletContractV4, MultisigWallet, MultisigOrder, MultisigOrderBuilder } from "ton";
import { KeyPair, mnemonicToPrivateKey } from 'ton-crypto';
import { getHttpEndpoint } from "@orbs-network/ton-access";
```

톤클라이언트\` 인스턴스를 생성합니다:

```js
const endpoint = await getHttpEndpoint();
const client = new TonClient({ endpoint });
```

작업할 키쌍이 필요합니다:

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

멀티시그월렛\` 개체를 생성하는 방법은 두 가지가 있습니다:

- 주소에서 기존 주소 가져오기

```js
let addr: Address = Address.parse('EQADBXugwmn4YvWsQizHdWGgfCTN_s3qFP0Ae0pzkU-jwzoE');
let mw: MultisigWallet = await MultisigWallet.fromAddress(addr, { client });
```

- 새로 만들기

```js
let mw: MultisigWallet = new MultisigWallet([keyPairs[0].publicKey, keyPairs[1].publicKey], 0, 0, 1, { client });
```

배포하는 방법도 두 가지가 있습니다.

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

## 주문 생성, 서명 및 전송

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

이제 다른 주문을 만들고, 메시지를 추가하고, 다른 키 세트로 서명하고, 이 주문의 서명을 합쳐 보겠습니다.

```js
let order2: MultisigOrderBuilder = new MultisigOrderBuilder(0);
order2.addMessage(msg, 3);
let order2b = order2.build();
order2b.sign(1, keyPairs[1].secretKey);

order1b.unionSignatures(order2b); //Now order1b have also have all signatures from order2b
```

마지막으로 서명된 주문서를 전송합니다:

```js
await mw.sendOrder(order1b, keyPairs[0].secretKey);
```

이제 프로젝트를 빌드하세요.

```bash
yarn tsc
```

그리고 컴파일된 파일을 실행합니다.

```bash
node main.js
```

오류가 발생하지 않는다면 모든 것이 정상입니다! 이제 탐색기나 지갑에서 트랜잭션이 성공했는지 확인해보세요.

## 기타 메서드 및 속성

멀티 시그 주문 빌더\` 개체에서 메시지를 쉽게 지울 수 있습니다:

```js
order2.clearMessages();
```

또한 `멀티서명주문` 개체에서 서명을 지울 수도 있습니다:

```js
order2b.clearSignatures();
```

물론 `멀티시그월렛`, `멀티시그오더빌더`, `멀티시그오더` 객체에서 공개 속성을 가져올 수 있습니다.

- 멀티시그월렛:
  - 소유자`-`사전\<number, Buffer>\` 서명의 소유자 *소유자 ID => 서명*
  - '워크체인' - 지갑이 배포되는 워크체인
  - `walletId` - 지갑 아이디
  - `k` - 거래 확인에 필요한 서명 수
  - `주소` - 지갑 주소
  - 제공자`-`계약 제공자\` 인스턴스

- 멀티시그오더 빌더
  - `메시지` - 주문에 추가할 `메시지위드모드`의 배열입니다.
  - `querryId` - 주문이 유효할 때까지의 골발 시간

- 다중 서명 주문
  - 페이로드`- 주문 페이로드가 있는`셀\`
  - 서명`-`사전\<number, Buffer>\` 서명의 *ownerId => 서명*

## 참조

- [로우레벨 멀티서명 가이드](/개발/스마트 컨트랙트/튜토리얼/멀티서명)
- [ton.js 문서](https://ton-community.github.io/ton/)
- [멀티서명 컨트랙트 소스](https://github.com/ton-blockchain/multisig-contract)
