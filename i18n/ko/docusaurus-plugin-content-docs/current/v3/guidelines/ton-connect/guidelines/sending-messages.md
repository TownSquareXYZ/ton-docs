# 메시지 보내기

TON Connect 2.0은 dApp에서 사용자 인증 이외에도 더 강력한 옵션을 제공합니다: 연결된 지갑을 통해 발신 메시지를 보낼 수 있습니다!

다음 내용을 이해하게 됩니다:

- DApp에서 블록체인으로 메시지를 보내는 방법
- 하나의 트랜잭션에서 여러 메시지를 보내는 방법
- TON Connect를 사용하여 컨트랙트를 배포하는 방법

## 플레이그라운드 페이지

JavaScript용 저수준 [TON Connect SDK](https://github.com/ton-connect/sdk/tree/main/packages/sdk)를 사용할 것입니다. 지갑이 이미 연결된 페이지의 브라우저 콘솔에서 실험해보겠습니다. 다음은 샘플 페이지입니다:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <script src="https://unpkg.com/@tonconnect/sdk@latest/dist/tonconnect-sdk.min.js"></script>
    <script src="https://unpkg.com/tonweb@0.0.41/dist/tonweb.js"></script>
  </head>
  <body>
    <script>
      window.onload = async () => {
        window.connector = new TonConnectSDK.TonConnect({
          manifestUrl: 'https://ratingers.pythonanywhere.com/ratelance/tonconnect-manifest.json'
        });
        connector.restoreConnection();
      }
    </script>
  </body>
</html>
```

이 코드를 브라우저 콘솔에 복사-붙여넣기하여 실행해보세요.

## 여러 메시지 보내기

### 1. 작업 이해하기

하나의 트랜잭션에서 두 개의 별도 메시지를 보낼 것입니다: 하나는 0.2 TON을 담아 자신의 주소로, 다른 하나는 0.1 TON을 담아 다른 지갑 주소로 보냅니다.

참고로 하나의 트랜잭션에서 보낼 수 있는 메시지 수 제한이 있습니다:

- 표준 ([v3](/v3/documentation/smart-contracts/contracts-specs/wallet-contracts#wallet-v3)/[v4](/v3/documentation/smart-contracts/contracts-specs/wallet-contracts#wallet-v4)) 지갑: 발신 메시지 4개
- 하이로드 지갑: 발신 메시지 255개(블록체인 제한에 근접)

### 2. 메시지 보내기

다음 코드를 실행하세요:

```js
console.log(await connector.sendTransaction({
  validUntil: Math.floor(new Date() / 1000) + 360,
  messages: [
    {
      address: connector.wallet.account.address,
      amount: "200000000"
    },
    {
      address: "0:b2a1ecf5545e076cd36ae516ea7ebdf32aea008caa2b84af9866becb208895ad",
      amount: "100000000"
    }
  ]
}));
```

이 명령이 콘솔에 아무것도 출력하지 않는다는 것을 알 수 있습니다. `null` 또는 `undefined`처럼 아무것도 반환하지 않는 함수처럼 말입니다. 이는 `connector.sendTransaction`이 즉시 종료되지 않는다는 의미입니다.

지갑 애플리케이션을 열어보면 이유를 알 수 있습니다. 무엇을 보내는지와 코인이 어디로 갈지 보여주는 요청이 있습니다. 이를 승인해주세요.

### 3. 결과 받기

함수가 종료되면 블록체인의 출력이 출력됩니다:

```json
{
  boc: "te6cckEBAwEA4QAC44gBZUPZ6qi8Dtmm1cot1P175lXUARlUVwlfMM19lkERK1oCUB3RqDxAFnPpeo191X/jiimn9Bwnq3zwcU/MMjHRNN5sC5tyymBV3SJ1rjyyscAjrDDFAIV/iE+WBySEPP9wCU1NGLsfcvVgAAACSAAYHAECAGhCAFlQ9nqqLwO2abVyi3U/XvmVdQBGVRXCV8wzX2WQRErWoAmJaAAAAAAAAAAAAAAAAAAAAGZCAFlQ9nqqLwO2abVyi3U/XvmVdQBGVRXCV8wzX2WQRErWnMS0AAAAAAAAAAAAAAAAAAADkk4U"
}
```

BOC는 [Bag of Cells](/v3/concepts/dive-into-ton/ton-blockchain/cells-as-data-storage)로, TON에서 데이터가 저장되는 방식입니다. 이제 이것을 디코딩할 수 있습니다.

선택한 도구로 이 BOC를 디코딩하면 다음과 같은 셀 트리가 나옵니다:

```bash
x{88016543D9EAA8BC0ED9A6D5CA2DD4FD7BE655D401195457095F30CD7D9641112B5A02501DD1A83C401673E97A8D7DD57FE38A29A7F41C27AB7CF0714FCC3231D134DE6C0B9B72CA6055DD2275AE3CB2B1C023AC30C500857F884F960724843CFF70094D4D18BB1F72F5600000024800181C_}
 x{42005950F67AAA2F03B669B5728B753F5EF9957500465515C257CC335F6590444AD6A00989680000000000000000000000000000}
 x{42005950F67AAA2F03B669B5728B753F5EF9957500465515C257CC335F6590444AD69CC4B40000000000000000000000000000}
```

이는 직렬화된 외부 메시지이며, 두 참조는 발신 메시지 표현입니다.

```bash
x{88016543D9EAA8BC0ED9A6D5CA2DD4FD7BE655D401195457095F30CD7D964111...
  $10       ext_in_msg_info
  $00       src:MsgAddressExt (null address)
  "EQ..."a  dest:MsgAddressInt (your wallet)
  0         import_fee:Grams
  $0        (no state_init)
  $0        (body starts in this cell)
  ...
```

전송된 트랜잭션의 BOC를 반환하는 목적은 이를 추적하기 위함입니다.

## 복잡한 트랜잭션 보내기

### 셀 직렬화

진행하기 전에 보낼 메시지의 형식에 대해 이야기해보겠습니다.

- **payload** (string base64, 선택사항): Base64로 인코딩된 원시 단일 셀 BoC
 - 전송 시 텍스트 코멘트를 저장하는 데 사용할 것입니다
- **stateInit** (string base64, 선택사항): Base64로 인코딩된 원시 단일 셀 BoC
 - 스마트 컨트랙트를 배포하는 데 사용할 것입니다

메시지를 만든 후 BOC로 직렬화할 수 있습니다.

```js
TonWeb.utils.bytesToBase64(await payloadCell.toBoc())
```

### 코멘트 포함 전송

[toncenter/tonweb](https://github.com/toncenter/tonweb) JS SDK나 선호하는 도구를 사용하여 셀을 BOC로 직렬화할 수 있습니다.

전송 시 텍스트 코멘트는 opcode 0 (32개의 0비트) + 코멘트의 UTF-8 바이트로 인코딩됩니다. 다음은 이를 셀 묶음으로 변환하는 예시입니다.

```js
let a = new TonWeb.boc.Cell();
a.bits.writeUint(0, 32);
a.bits.writeString("TON Connect 2 tutorial!");
let payload = TonWeb.utils.bytesToBase64(await a.toBoc());

console.log(payload);
// te6ccsEBAQEAHQAAADYAAAAAVE9OIENvbm5lY3QgMiB0dXRvcmlhbCFdy+mw
```

### 스마트 컨트랙트 배포

[스마트 컨트랙트 예시](/v3/documentation/smart-contracts/overview#examples-of-smart-contracts)에서 언급된 매우 간단한 [챗봇 Doge](https://github.com/LaDoger/doge.fc)의 인스턴스를 배포해보겠습니다. 먼저 코드를 로드하고 데이터에 고유한 것을 저장하여 다른 사람이 배포하지 않은 우리만의 인스턴스를 받습니다. 그런 다음 코드와 데이터를 stateInit으로 결합합니다.

```js
let code = TonWeb.boc.Cell.oneFromBoc(TonWeb.utils.base64ToBytes('te6cckEBAgEARAABFP8A9KQT9LzyyAsBAGrTMAGCCGlJILmRMODQ0wMx+kAwi0ZG9nZYcCCAGMjLBVAEzxaARfoCE8tqEssfAc8WyXP7AN4uuM8='));
let data = new TonWeb.boc.Cell();
data.bits.writeUint(Math.floor(new Date()), 64);

let state_init = new TonWeb.boc.Cell();
state_init.bits.writeUint(6, 5);
state_init.refs.push(code);
state_init.refs.push(data);

let state_init_boc = TonWeb.utils.bytesToBase64(await state_init.toBoc());
console.log(state_init_boc);
//  te6ccsEBBAEAUwAABRJJAgE0AQMBFP8A9KQT9LzyyAsCAGrTMAGCCGlJILmRMODQ0wMx+kAwi0ZG9nZYcCCAGMjLBVAEzxaARfoCE8tqEssfAc8WyXP7AAAQAAABhltsPJ+MirEd

let doge_address = '0:' + TonWeb.utils.bytesToHex(await state_init.hash());
console.log(doge_address);
//  0:1c7c35ed634e8fa796e02bbbe8a2605df0e2ab59d7ccb24ca42b1d5205c735ca
```

이제 트랜잭션을 보낼 시간입니다!

```js
console.log(await connector.sendTransaction({
  validUntil: Math.floor(new Date() / 1000) + 360,
  messages: [
    {
      address: "0:1c7c35ed634e8fa796e02bbbe8a2605df0e2ab59d7ccb24ca42b1d5205c735ca",
      amount: "69000000",
      payload: "te6ccsEBAQEAHQAAADYAAAAAVE9OIENvbm5lY3QgMiB0dXRvcmlhbCFdy+mw",
      stateInit: "te6ccsEBBAEAUwAABRJJAgE0AQMBFP8A9KQT9LzyyAsCAGrTMAGCCGlJILmRMODQ0wMx+kAwi0ZG9nZYcCCAGMjLBVAEzxaARfoCE8tqEssfAc8WyXP7AAAQAAABhltsPJ+MirEd"
    }
  ]
}));
```

:::info
NFT와 Jetton 전송을 위한 더 많은 예시는 [메시지 준비하기](/v3/guidelines/ton-connect/guidelines/preparing-messages) 페이지에서 확인하세요.
:::

확인 후에는 [tonscan.org](https://tonscan.org/tx/pCA8LzWlCRTBc33E2y-MYC7rhUiXkhODIobrZVVGORg=)에서 트랜잭션이 완료된 것을 볼 수 있습니다.

## 사용자가 트랜잭션 요청을 거부하면 어떻게 되나요?

요청 거부를 처리하는 것은 매우 쉽지만, 프로젝트를 개발할 때는 미리 어떤 일이 일어날지 아는 것이 좋습니다.

사용자가 지갑 애플리케이션의 팝업에서 "취소"를 클릭하면 예외가 발생합니다: `Error: [TON_CONNECT_SDK_ERROR] Wallet declined the request`. 이 에러는 최종적인 것으로 간주될 수 있습니다(연결 취소와는 달리) - 이 에러가 발생했다면 다음 요청이 전송될 때까지 요청된 트랜잭션은 확실히 일어나지 않을 것입니다.

## 참고 자료

- [메시지 준비하기](/v3/guidelines/ton-connect/guidelines/preparing-messages)
