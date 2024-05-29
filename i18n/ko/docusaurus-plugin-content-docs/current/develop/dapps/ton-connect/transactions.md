# 메시지 보내기

톤 커넥트 2.0은 디앱에서 사용자를 인증하는 것 이상의 강력한 옵션을 제공합니다: 연결된 지갑을 통해 발신 메시지를 보낼 수 있습니다!

이해하실 겁니다:

- 디앱에서 블록체인으로 메시지를 보내는 방법
- 하나의 트랜잭션으로 여러 개의 메시지를 보내는 방법
- 톤 커넥트를 사용하여 컨트랙트를 배포하는 방법

## 놀이터 페이지

자바스크립트용 로우레벨 [TON Connect SDK](https://github.com/ton-connect/sdk/tree/main/packages/sdk)를 사용하겠습니다. 지갑이 이미 연결된 페이지의 브라우저 콘솔에서 실험해 보겠습니다. 다음은 샘플 페이지입니다:

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

브라우저 콘솔에 복사하여 붙여넣고 실행하세요.

## 여러 개의 메시지 보내기

### 1. 작업 이해

한 번의 트랜잭션으로 두 개의 별도 메시지를 보내는데, 하나는 0.2톤을 담고 있는 본인 주소로, 다른 하나는 0.1톤을 담고 있는 다른 지갑 주소로 보내드립니다.

참고로 한 번의 트랜잭션으로 전송할 수 있는 메시지 수에는 제한이 있습니다:

- 표준 ([v3](/참여/지갑/계약#지갑-v3)/[v4](/참여/지갑/계약#지갑-v4)) 지갑: 발신 메시지 4개;
- 고부하 지갑: 255개의 발신 메시지(블록체인의 한계에 근접).

### 2. 메시지 보내기

다음 코드를 실행합니다:

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

이 명령은 아무것도 반환하지 않는 함수를 반환하므로 콘솔에 `null` 또는 `정의되지 않음`이 출력되지 않는 것을 알 수 있습니다. 즉, `connector.sendTransaction`이 즉시 종료되지 않습니다.

지갑 애플리케이션을 열면 그 이유를 알 수 있습니다. 전송할 코인과 코인이 어디로 갈지 보여주는 요청이 있습니다. 수락해 주세요.

### 3. 결과 얻기

함수가 종료되고 블록체인의 출력이 인쇄됩니다:

```json
{
  boc: "te6cckEBAwEA4QAC44gBZUPZ6qi8Dtmm1cot1P175lXUARlUVwlfMM19lkERK1oCUB3RqDxAFnPpeo191X/jiimn9Bwnq3zwcU/MMjHRNN5sC5tyymBV3SJ1rjyyscAjrDDFAIV/iE+WBySEPP9wCU1NGLsfcvVgAAACSAAYHAECAGhCAFlQ9nqqLwO2abVyi3U/XvmVdQBGVRXCV8wzX2WQRErWoAmJaAAAAAAAAAAAAAAAAAAAAGZCAFlQ9nqqLwO2abVyi3U/XvmVdQBGVRXCV8wzX2WQRErWnMS0AAAAAAAAAAAAAAAAAAADkk4U"
}
```

BOC는 [백 오브 셀](/학습/개요/셀)로, 데이터가 TON에 어떻게 저장되는지를 나타내는 방식입니다. 이제 이를 해독할 수 있습니다.

원하는 도구에서 이 BOC를 디코딩하면 다음과 같은 셀 트리가 표시됩니다:

```bash
x{88016543D9EAA8BC0ED9A6D5CA2DD4FD7BE655D401195457095F30CD7D9641112B5A02501DD1A83C401673E97A8D7DD57FE38A29A7F41C27AB7CF0714FCC3231D134DE6C0B9B72CA6055DD2275AE3CB2B1C023AC30C500857F884F960724843CFF70094D4D18BB1F72F5600000024800181C_}
 x{42005950F67AAA2F03B669B5728B753F5EF9957500465515C257CC335F6590444AD6A00989680000000000000000000000000000}
 x{42005950F67AAA2F03B669B5728B753F5EF9957500465515C257CC335F6590444AD69CC4B40000000000000000000000000000}
```

이것은 직렬화된 외부 메시지이며, 두 개의 참조는 발신 메시지 표현입니다.

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

전송된 트랜잭션의 BOC를 반환하는 목적은 트랜잭션을 추적하기 위한 것입니다.

## 복잡한 트랜잭션 보내기

### 셀의 직렬화

계속 진행하기 전에 보낼 메시지의 형식에 대해 이야기해 보겠습니다.

- **페이로드**(문자열 base64, 선택 사항): Base64로 인코딩된 원시 1셀 BoC.
  - 전송 시 텍스트 코멘트를 저장하는 데 사용합니다.
- **stateInit**(문자열 base64, 선택 사항): Base64로 인코딩된 원시 1셀 BoC.
  - 스마트 컨트랙트를 배포하는 데 사용할 것입니다.

메시지를 작성하고 나면 이를 BOC로 직렬화할 수 있습니다.

```js
TonWeb.utils.bytesToBase64(await payloadCell.toBoc())
```

### 댓글로 전송하기

톤센터/톤웹](https://github.com/toncenter/tonweb) JS SDK 또는 선호하는 도구를 사용하여 셀을 BOC로 직렬화할 수 있습니다.

전송 시 텍스트 댓글은 옵트인 코드 0(0비트 32개) + UTF-8 바이트의 댓글로 인코딩됩니다. 다음은 이를 셀 백으로 변환하는 방법의 예시입니다.

```js
let a = new TonWeb.boc.Cell();
a.bits.writeUint(0, 32);
a.bits.writeString("TON Connect 2 tutorial!");
let payload = TonWeb.utils.bytesToBase64(await a.toBoc());

console.log(payload);
// te6ccsEBAQEAHQAAADYAAAAAVE9OIENvbm5lY3QgMiB0dXRvcmlhbCFdy+mw
```

### 스마트 컨트랙트 배포

그리고 [스마트 컨트랙트 예시](/개발/스마트-계약/#스마트-계약-예시) 중 하나로 언급된 매우 간단한 [챗봇 도제](https://github.com/LaDoger/doge.fc)의 인스턴스를 배포하겠습니다. 우선, 코드를 로드하고 고유한 데이터를 데이터에 저장하여 다른 사람이 배포하지 않은 고유한 인스턴스를 받습니다. 그런 다음 코드와 데이터를 stateInit에 결합합니다.

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

이제 트랜잭션을 전송할 시간입니다!

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
전송 NFT 및 제톤을 위한 [메시지 준비하기](/개발/앱/톤 연결/메시지 작성기) 페이지에서 더 많은 예시를 확인하세요.
:::

확인 후 [tonscan.org](https://tonscan.org/tx/pCA8LzWlCRTBc33E2y-MYC7rhUiXkhODIobrZVVGORg=)에서 거래가 완료된 것을 확인할 수 있습니다.

## 사용자가 트랜잭션 요청을 거부하면 어떻게 되나요?

요청 거부를 처리하는 것은 매우 쉽지만 프로젝트를 개발할 때는 어떤 일이 일어날지 미리 알아두는 것이 좋습니다.

사용자가 지갑 애플리케이션의 팝업에서 '취소'를 클릭하면 '오류'라는 예외가 발생합니다: [TON_CONNECT_SDK_ERROR] 지갑이 요청을 거부했습니다\`. 이 오류는 연결 취소와 달리 최종 오류로 간주할 수 있으며, 이 오류가 발생하면 다음 요청이 전송될 때까지 요청된 트랜잭션은 확실히 발생하지 않습니다.

## 참고 항목

- [메시지 준비하기](/개발/앱/톤커넥트/메시지 작성기)
