---
description: 이 튜토리얼에서는 지갑, 트랜잭션, 스마트 컨트랙트를 완벽하게 사용하는 방법을 알려드립니다.
---

'@theme/Tabs'에서 Tabs 가져오기;
'@theme/TabItem'에서 TabItem 가져오기;

# 월렛 스마트 컨트랙트 작업

## 👋 소개

스마트 컨트랙트 개발을 시작하기 전에 TON에서 지갑과 트랜잭션이 어떻게 작동하는지 알아두는 것은 필수입니다. 이러한 지식은 개발자가 특정 개발 작업을 구현하기 위해 지갑, 트랜잭션, 스마트 콘트랙트 간의 상호 작용을 이해하는 데 도움이 됩니다.

이 섹션에서는 개발 워크플로우를 이해하기 위해 미리 구성된 함수를 사용하지 않고 작업을 만드는 방법을 배웁니다. 이 튜토리얼의 분석에 필요한 모든 참조 자료는 참조 장에 있습니다.

## 💡 전제 조건

이 튜토리얼은 자바스크립트, 타입스크립트, 골랑에 대한 기본 지식이 필요합니다. 또한, 최소 3톤(거래소 계정, 비위탁 지갑 또는 텔레그램 봇 지갑을 사용하여 보관할 수 있음)을 보유하고 있어야 합니다. 이 튜토리얼을 이해하려면 [셀](/학습/개요/셀), [TON의 주소](/학습/개요/주소), [블록체인의 블록체인](/학습/개요/톤블록체인)에 대한 기본적인 이해가 필요합니다.

:::info 메인넷 개발은 필수\
TON 테스트넷으로 작업하면 종종 배포 오류, 트랜잭션 추적의 어려움, 불안정한 네트워크 기능 등이 발생합니다. 따라서 대부분의 개발을 TON 메인넷에서 완료하면 이러한 문제를 피할 수 있으며, 트랜잭션 수를 줄여 수수료를 최소화하는 데 도움이 될 수 있습니다.
:::

## 소스 코드

이 튜토리얼에 사용된 모든 코드 예제는 다음 [GitHub 리포지토리](https://github.com/aSpite/wallet-tutorial)에서 찾을 수 있습니다.

## ✍️ 시작하기 위해 필요한 것

- NodeJS가 설치되어 있는지 확인합니다.
- 특정 톤 라이브러리가 필요하며 다음이 포함됩니다: 톤/톤 13.5.1+, 톤/코어 0.49.2+ 및 @톤/크립토 3.2.0+.

**옵션**: JS 대신 GO를 사용하려면 [tonutils-go](https://github.com/xssnick/tonutils-go) 라이브러리와 GoLand IDE를 설치하여 TON에서 개발을 진행해야 합니다. 이 라이브러리는 이 튜토리얼에서 GO 버전에 사용됩니다.

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```bash
npm i --save @ton/ton @ton/core @ton/crypto
```

</TabItem>
<TabItem value="go" label="Golang">

```bash
go get github.com/xssnick/tonutils-go
go get github.com/xssnick/tonutils-go/adnl
go get github.com/xssnick/tonutils-go/address
```

</TabItem>
</Tabs>

## ⚙ 환경 설정

TypeScript 프로젝트를 만들려면 다음 단계를 순서대로 수행해야 합니다:

1. 빈 폴더를 만듭니다(이름은 WalletsTutorial으로 지정합니다).
2. CLI를 사용하여 프로젝트 폴더를 엽니다.
3. 다음 명령을 사용하여 프로젝트를 설정합니다:

```bash
npm init -y
npm install typescript @types/node ts-node nodemon --save-dev
npx tsc --init --rootDir src --outDir build \ --esModuleInterop --target es2020 --resolveJsonModule --lib es6 \ --module commonjs --allowJs true --noImplicitAny false --allowSyntheticDefaultImports true --strict false
```

:::info
다음 프로세스를 수행하기 위해 `ts-node`는 사전 컴파일 없이 타입스크립트 코드를 직접 실행하는 데 사용됩니다. nodemon\`은 디렉토리의 파일 변경이 감지되면 노드 애플리케이션을 자동으로 재시작하는 데 사용됩니다.
:::

```json
  "files": [
    "\",
    "\"
  ]
```

5. 그런 다음 프로젝트 루트에 다음 내용으로 `nodemon.json` 설정을 생성합니다:

```json
{
  "watch": ["src"],
  "ext": ".ts,.js",
  "ignore": [],
  "exec": "npx ts-node ./src/index.ts"
}
```

6. 프로젝트를 생성할 때 추가되는 "test" 대신 이 스크립트를 `package.json`에 추가합니다:

```json
"start:dev": "npx nodemon"
```

7. 프로젝트 루트에 `src` 폴더를 만들고 이 폴더에 `index.ts` 파일을 만듭니다.
8. 다음으로 다음 코드를 추가해야 합니다:

```ts
async function main() {
  console.log("Hello, TON!");
}

main().finally(() => console.log("Exiting..."));
```

9. 터미널을 사용하여 코드를 실행합니다:

```bash
npm run start:dev
```

10. 마지막으로 콘솔 출력이 나타납니다.

![](/img/docs/how-to-wallet/wallet_1.png)

:::tip 블루프린트
TON 커뮤니티는 모든 개발 프로세스(배포, 컨트랙트 작성, 테스트)를 자동화하는 훌륭한 도구인 [블루프린트](https://github.com/ton-org/blueprint)를 만들었습니다. 그러나 저희는 이러한 강력한 도구가 필요하지 않으므로 위의 지침을 따르는 것이 좋습니다.
:::

\*\*선택 사항: \*\* Golang을 사용할 때는 다음 지침을 따르세요:

1. GoLand IDE를 설치합니다.
2. 다음 내용을 사용하여 프로젝트 폴더와 `go.mod` 파일을 생성합니다(현재 사용 중인 Go 버전이 오래된 경우 이 과정을 수행하기 위해 **버전**을 변경해야 할 수 있습니다):

```
module main

go 1.20
```

3. 터미널에 다음 명령을 입력합니다:

```bash
go get github.com/xssnick/tonutils-go
```

4. 프로젝트의 루트에 다음 내용으로 `main.go` 파일을 만듭니다:

```go
package main

import (
	"log"
)

func main() {
	log.Println("Hello, TON!")
}
```

5. go.mod`에서 모듈의 이름을 `메인\`으로 변경합니다.
6. 터미널에 출력이 표시될 때까지 위의 코드를 실행합니다.

:::info
GoLand는 무료가 아니므로 다른 IDE를 사용할 수도 있지만, 이 방법을 선호합니다.
:::

:::warning 중요

또한 특정 코드 섹션에 필요한 가져오기만 각각의 새 섹션에 지정되며 새 가져오기를 추가하고 이전 가져오기와 결합해야 합니다(\
::):

## 🚀 시작하자!

이 튜토리얼에서는 TON 블록체인에서 가장 많이 사용되는 지갑(버전 3과 4)을 알아보고 해당 지갑의 스마트 컨트랙트 작동 방식에 대해 알아볼 것입니다. 이를 통해 개발자는 TON 플랫폼의 다양한 트랜잭션 유형을 더 잘 이해하여 트랜잭션을 생성하고, 블록체인에 전송하고, 지갑을 배포하고, 결국에는 부하가 높은 지갑으로 작업할 수 있게 될 것입니다.

저희의 주요 임무는 @ton/ton, @ton/core, @ton/crypto(외부 메시지, 내부 메시지, 서명 등)에 대한 다양한 객체와 함수를 사용하여 트랜잭션을 구축하여 더 큰 규모의 트랜잭션이 어떻게 보이는지 이해하는 것입니다. 이 과정을 수행하기 위해 두 가지 주요 지갑 버전(v3 및 v4)을 사용하게 되는데, 거래소, 비수탁 지갑 및 대부분의 사용자가 이 특정 버전만 사용한다는 사실을 고려한 것입니다.

:::note
There may be occasions in this tutorial when there is no explanation for particular details. In these cases, more details will be provided in later stages of this tutorial.

**중요:** 이 튜토리얼에서는 지갑 개발 과정을 더 잘 이해하기 위해 [지갑 v3 코드](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet3-code.fc)를 사용합니다. v3 버전에는 r1과 r2라는 두 가지 하위 버전이 있다는 점에 유의해야 합니다. 현재 두 번째 버전만 사용 중이므로 이 문서에서 v3를 언급할 때는 v3r2를 의미합니다.
:::

## 💎 TON 블록체인 지갑

TON 블록체인에서 작동하고 실행되는 모든 지갑은 실제로 스마트 컨트랙트이며, 마찬가지로 TON에서 작동하는 모든 것이 스마트 컨트랙트입니다. 대부분의 블록체인과 마찬가지로 네트워크에 스마트 컨트랙트를 배포하고 다양한 용도에 맞게 커스터마이징할 수 있습니다. 이 기능 덕분에 **완전한 지갑 커스터마이징이 가능합니다**.
온톤 지갑의 스마트 컨트랙트는 플랫폼이 다른 스마트 컨트랙트 유형과 통신하는 데 도움이 됩니다. 그러나 지갑 통신이 어떻게 이루어지는지 고려하는 것이 중요합니다.

### 월렛 커뮤니케이션

일반적으로 톤 블록체인에는 '내부'와 '외부'의 두 가지 트랜잭션 유형이 있습니다. 외부 트랜잭션은 외부에서 블록체인으로 메시지를 보낼 수 있는 기능으로, 이러한 트랜잭션을 수락하는 스마트 컨트랙트와 통신할 수 있습니다. 이 과정을 담당하는 함수는 다음과 같습니다:

```func
() recv_external(slice in_msg) impure {
    ;; some code
}
```

지갑에 대해 자세히 알아보기 전에 지갑이 외부 트랜잭션을 어떻게 수락하는지 살펴보겠습니다. TON에서 모든 지갑은 소유자의 `공개키`, `세그노`, `서브월렛_id`를 보유합니다. 외부 트랜잭션을 수신하면 지갑은 `get_data()` 메서드를 사용하여 지갑의 스토리지 부분에서 데이터를 검색합니다. 그런 다음 몇 가지 확인 절차를 수행하여 트랜잭션을 수락할지 여부를 결정합니다. 이 과정은 다음과 같이 진행됩니다:

```func
() recv_external(slice in_msg) impure {
  var signature = in_msg~load_bits(512); ;; get signature from the message body
  var cs = in_msg;
  var (subwallet_id, valid_until, msg_seqno) = (cs~load_uint(32), cs~load_uint(32), cs~load_uint(32));  ;; get rest values from the message body
  throw_if(35, valid_until <= now()); ;; check the relevance of the transaction
  var ds = get_data().begin_parse(); ;; get data from storage and convert it into a slice to be able to read values
  var (stored_seqno, stored_subwallet, public_key) = (ds~load_uint(32), ds~load_uint(32), ds~load_uint(256)); ;; read values from storage
  ds.end_parse(); ;; make sure we do not have anything in ds variable
  throw_unless(33, msg_seqno == stored_seqno);
  throw_unless(34, subwallet_id == stored_subwallet);
  throw_unless(35, check_signature(slice_hash(in_msg), signature, public_key));
  accept_message();
```

> 💡 유용한 링크:
>
> ["load_bits()" in docs](/develop/func/stdlib/#load_bits)
>
> ["get_data()" in docs](/develop/func/stdlib/#load_bits)
>
> ["begin_parse()" in docs](/develop/func/stdlib/#load_bits)
>
> ["end_parse()" in docs](/develop/func/stdlib/#end_parse)
>
> ["load_int()" in docs](/develop/func/stdlib/#load_int)
>
> ["load_uint()" in docs](/develop/func/stdlib/#load_int)
>
> ["check_signature()" in docs](/develop/func/stdlib/#check_signature)
>
> ["slice_hash()" in docs](/develop/func/stdlib/#slice_hash)
>
> ["accept_message()"(/개발/스마트-계약/가이드라인/수락)](/개발/스마트-계약/가이드라인/수락)

이제 자세히 살펴보겠습니다.

### 리플레이 보호 - Seqno

지갑 스마트 컨트랙트의 트랜잭션 리플레이 보호는 어떤 트랜잭션이 어떤 순서로 전송되었는지 추적하는 트랜잭션 시퀀스 번호와 직접적으로 관련이 있습니다. 하나의 트랜잭션이 지갑에서 반복되지 않도록 하는 것은 매우 중요한데, 이는 시스템의 무결성을 완전히 무너뜨리기 때문입니다. 지갑 내 스마트 컨트랙트 코드를 자세히 살펴보면, 일반적으로 `seqno`는 다음과 같이 처리됩니다:

```func
throw_unless(33, msg_seqno == stored_seqno);
```

위 코드 줄은 트랜잭션에 들어온 `seqno`를 스마트 컨트랙트에 저장된 `seqno`와 비교하여 확인합니다. 일치하지 않으면 컨트랙트는 `33 종료 코드`와 함께 오류를 반환합니다. 따라서 발신자가 유효하지 않은 seqno를 전달했다는 것은 트랜잭션 시퀀스에서 실수를 했다는 의미이며, 컨트랙트는 이러한 경우를 대비해 보호합니다.

:::note
또한 외부 메시지는 누구나 보낼 수 있다는 점도 고려해야 합니다. 즉, 누군가에게 1톤을 보내면 다른 사람이 이 메시지를 반복할 수 있다는 뜻입니다. 그러나 seqno가 증가하면 이전 외부 메시지는 무효가 되어 아무도 반복할 수 없으므로 자금을 도용할 가능성을 방지할 수 있습니다.
:::

### 서명

앞서 언급했듯이 지갑 스마트 콘트랙트는 외부 트랜잭션을 허용합니다. 그러나 이러한 거래는 외부 세계에서 이루어지며 해당 데이터를 100% 신뢰할 수 없습니다. 따라서 각 지갑은 소유자의 공개 키를 저장합니다. 스마트 콘트랙트는 소유자가 개인 키로 서명한 외부 트랜잭션을 받을 때 공개 키를 사용해 거래 서명의 적법성을 확인합니다. 이를 통해 트랜잭션이 실제로 계약 소유자가 보낸 것인지 확인합니다.

이 프로세스를 수행하려면 먼저 지갑이 수신 메시지에서 서명을 받아야 하며, 지갑은 스토리지에서 공개 키를 로드하고 다음 프로세스를 사용하여 서명의 유효성을 검사합니다:

```func
var signature = in_msg~load_bits(512);
var ds = get_data().begin_parse();
var (stored_seqno, stored_subwallet, public_key) = (ds~load_uint(32), ds~load_uint(32), ds~load_uint(256));
throw_unless(35, check_signature(slice_hash(in_msg), signature, public_key));
```

그리고 모든 확인 프로세스가 올바르게 완료되면 스마트 컨트랙트는 메시지를 수락하고 처리합니다:

```func
accept_message();
```

:::info accept_message()
트랜잭션이 외부에서 발생하기 때문에 트랜잭션 수수료를 지불하는 데 필요한 톤코인은 포함되어 있지 않습니다. accept_message() 함수를 사용하여 TON을 전송할 때 가스 크레딧(작성 시점의 값은 10,000 가스 단위)이 적용되어 가스가 가스 크레딧 값을 초과하지 않으면 필요한 계산을 무료로 수행할 수 있습니다. accept_message() 함수가 사용된 후, 사용된 모든 가스(톤 단위)는 스마트 컨트랙트 잔액에서 인출됩니다. 이 프로세스에 대한 자세한 내용은 [여기](/개발/스마트 컨트랙트/가이드라인/수락)에서 확인할 수 있습니다.
:::

### 거래 만료

외부 트랜잭션의 유효성을 확인하는 데 사용되는 또 다른 단계는 `valid_until` 필드입니다. 변수 이름에서 알 수 있듯이, 이것은 트랜잭션이 유효하기 전 UNIX에서의 시간입니다. 이 확인 프로세스가 실패하면 컨트랙트는 트랜잭션 처리를 완료하고 35 종료 코드를 반환합니다:

```func
var (subwallet_id, valid_until, msg_seqno) = (cs~load_uint(32), cs~load_uint(32), cs~load_uint(32));
throw_if(35, valid_until <= now());
```

이 알고리즘은 트랜잭션이 더 이상 유효하지 않지만 알 수 없는 이유로 블록체인에 전송되었을 때 발생할 수 있는 다양한 오류의 가능성을 방지하기 위해 작동합니다.

### 월렛 v3와 월렛 v4의 차이점

월렛 v3와 월렛 v4의 유일한 차이점은 월렛 v4는 설치 및 삭제가 가능한 '플러그인'을 사용한다는 것입니다. 이러한 플러그인은 지갑 스마트 컨트랙트에서 특정 시간에 특정 수의 TON을 요청할 수 있는 특수 스마트 컨트랙트입니다.

지갑 스마트 컨트랙트는 소유자가 참여할 필요 없이 필요한 만큼의 TON을 전송합니다. 이는 플러그인이 생성되는 **구독 모델**과 유사합니다. 자세한 내용은 이 튜토리얼의 범위를 벗어나므로 여기서는 다루지 않겠습니다.

### 지갑이 스마트 컨트랙트와의 커뮤니케이션을 촉진하는 방법

앞서 설명한 것처럼 지갑 스마트 콘트랙트는 외부 트랜잭션을 수락하고, 유효성을 검사한 후 모든 검사를 통과하면 트랜잭션을 승인합니다. 그런 다음 컨트랙트는 외부 메시지 본문에서 메시지를 검색하는 루프를 시작한 다음 내부 메시지를 생성하여 다음과 같이 블록체인으로 전송합니다:

```func
cs~touch();
while (cs.slice_refs()) {
    var mode = cs~load_uint(8); ;; load transaction mode
    send_raw_message(cs~load_ref(), mode); ;; get each new internal message as a cell with the help of load_ref() and send it
}
```

:::tip 터치()
TON에서 모든 스마트 컨트랙트는 스택 기반 TON 가상머신(TVM)에서 실행됩니다. ~ 터치()는 스택 위에 변수 `cs`를 배치하여 코드 실행을 최적화하여 가스를 적게 소모합니다.
:::

하나의 셀에 **최대 4개의 참조**를 저장할 수 있으므로, 외부 메시지당 최대 4개의 내부 메시지를 보낼 수 있습니다.

> 💡 유용한 링크:
>
> ["slice_refs()" in docs](/develop/func/stdlib/#slice_refs)
>
> ["send_raw_message() 및 트랜잭션 모드" 문서](/develop/func/stdlib/#send_raw_message)
>
> ["load_ref()" in docs](/develop/func/stdlib/#load_ref)

## 📬 외부 및 내부 거래

이 섹션에서는 '내부' 및 '외부' 트랜잭션에 대해 자세히 알아보고, 트랜잭션을 생성하고 네트워크에 전송하여 미리 준비된 함수 사용을 최소화하겠습니다.

이 프로세스를 수행하려면 기성품 지갑을 사용하여 작업을 더 쉽게 수행해야 합니다. 이를 위해

1. 지갑 앱](/참여/지갑/앱)을 설치합니다(예: 글쓴이가 사용하는 톤키퍼).
2. 지갑 앱을 v3r2 주소 버전으로 전환하기
3. 지갑에 1톤 입금하기
4. 다른 주소로 트랜잭션을 전송합니다(동일한 지갑으로 본인에게 전송할 수 있음).

이렇게 하면 톤키퍼 지갑 앱이 지갑 컨트랙트를 배포하고 다음 단계에 사용할 수 있습니다.

:::note
이 글을 작성하는 시점에 TON의 대부분의 지갑 앱은 기본적으로 지갑 v4 버전을 사용합니다. 이 튜토리얼에서는 플러그인이 필요하지 않으며 지갑 v3에서 제공하는 기능을 활용하겠습니다. 톤키퍼를 사용하는 동안 사용자가 원하는 지갑 버전을 선택할 수 있습니다. 따라서 지갑 버전 3(지갑 v3)을 배포하는 것이 좋습니다.
:::

### TL-B

앞서 언급했듯이, 톤 블록체인의 모든 것은 셀로 구성된 스마트 컨트랙트입니다. 데이터를 제대로 직렬화 및 역직렬화하려면 표준이 필요합니다. 직렬화 및 역직렬화 프로세스를 수행하기 위해 'TL-B'는 셀 내부에서 서로 다른 시퀀스로 서로 다른 데이터 유형을 서로 다른 방식으로 설명할 수 있는 범용 도구로 만들어졌습니다.

이 섹션에서는 [block.tlb](https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb)를 살펴봅니다. 이 파일은 다양한 셀을 조립하는 방법을 설명하기 때문에 향후 개발 과정에서 매우 유용할 것입니다. 특히 저희의 경우 내부 및 외부 트랜잭션의 복잡성에 대해 자세히 설명합니다.

:::info
이 가이드에서는 기본적인 정보를 제공합니다. 자세한 내용은 TL-B [문서](/개발/데이터-포맷/tl-b-language)를 참조하여 TL-B에 대해 자세히 알아보세요.
:::

### 공통메시지정보

처음에 각 메시지는 먼저 `CommonMsgInfo`([TL-B](https://github.com/ton-blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L123-L130)) 또는 `CommonMsgInfoRelaxed`([TL-B](https://github.com/ton-blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L132-L137))를 저장해야 합니다. 이를 통해 트랜잭션 유형, 트랜잭션 시간, 수신자 주소, 기술 플래그 및 수수료와 관련된 기술적 세부 정보를 정의할 수 있습니다.

block.tlb`파일을 읽으면`int_msg_info$0`, `ext_in_msg_info$10`, `ext_out_msg_info$11`의 세 가지 유형의 CommonMsgInfo를 확인할 수 있습니다. 여기서는 `ext_out_msg_info\` TL-B 구조의 특수성에 대해 자세히 설명하지 않겠습니다. 즉, 스마트 콘트랙트가 외부 로그로 사용하기 위해 전송할 수 있는 외부 트랜잭션 유형입니다. 이 형식의 예시를 보시려면 [Elector](\(https://tonscan.org/address/Ef8zMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM0vF\)) 컨트랙트를 자세히 살펴보시기 바랍니다.

[TL-B](https://github.com/ton-blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L127-L128)를 보면, **확장_in_msg_info 타입과 함께 사용할 때 CommonMsgInfo만 사용 가능하다는 것을 알 수 있습니다**. 이는 트랜잭션 처리 중에 `src`, `created_lt`, `created_at` 등과 같은 트랜잭션 타입 필드가 검증자에 의해 재작성되기 때문입니다. 이 경우 트랜잭션이 전송될 때 발신자를 알 수 없고 검증 중에 유효성 검사기에 의해 작성되기 때문에 `src` 트랜잭션 유형이 가장 중요합니다. 이렇게 하면 `src` 필드의 주소가 정확하고 조작할 수 없게 됩니다.

그러나 `CommonMsgInfo` 구조체는 `MsgAddress` 사양만 지원하지만 일반적으로 발신자의 주소를 알 수 없는 경우 `addr_none`(0비트 `00` 2개)을 써야 합니다. 이 경우 `addr_none` 주소를 지원하는 `CommonMsgInfoRelaxed` 구조체가 사용됩니다. 수신 외부 메시지에 사용되는 `ext_in_msg_info`의 경우, 이러한 메시지 유형은 발신자를 사용하지 않고 항상 [MsgAddressExt](https://hub.com/ton/ton.blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L100) 구조체(`addr_none$00`은 0비트 2개)를 사용하므로 데이터를 덮어쓸 필요가 없으므로 `CommonMsgInfo` 구조체가 사용됩니다.

:::note
'$' 기호 뒤의 숫자는 특정 구조의 시작 부분에 저장해야 하는 비트로, 읽기(역직렬화) 중에 이러한 구조를 추가로 식별하기 위해 필요합니다.
:::

### 내부 거래 생성

내부 트랜잭션은 컨트랙트 간에 메시지를 전송하는 데 사용됩니다. NFT](https://github.com/ton-blockchain/token-contract/blob/f2253cb0f0e1ae0974d7dc0cef3a62cb6e19f806/nft/nft-item.fc#L51-L56), [제톤](https://github.com/ton-blockchain/token-contract/blob/f2253cb0f0e1ae0974d7dc0cef3a62cb6e19f806/ft/jetton-wallet.fc#L139-L144) 등 컨트랙트 작성을 고려하는 메시지를 보내는 다양한 컨트랙트 유형을 분석할 때, 다음과 같은 코드가 자주 사용됩니다:

```func
var msg = begin_cell()
  .store_uint(0x18, 6) ;; or 0x10 for non-bounce
  .store_slice(to_address)
  .store_coins(amount)
  .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; default message headers (see sending messages page)
  ;; store something as a body
```

먼저 다음과 같은 방식으로 배열된 16진수인 `0x18`과 `0x10`(x - 16진수)을 고려해 보겠습니다(6비트를 할당한다는 가정 하에): 011000`과 `010000\`입니다. 즉, 위의 코드를 다음과 같이 덮어쓸 수 있습니다:

```func
var msg = begin_cell()
  .store_uint(0, 1) ;; this bit indicates that we send an internal message according to int_msg_info$0  
  .store_uint(1, 1) ;; IHR Disabled
  .store_uint(1, 1) ;; or .store_uint(0, 1) for 0x10 | bounce
  .store_uint(0, 1) ;; bounced
  .store_uint(0, 2) ;; src -> two zero bits for addr_none
  .store_slice(to_address)
  .store_coins(amount)
  .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; default message headers (see sending messages page)
  ;; store something as a body
```

이제 각 옵션을 자세히 살펴보겠습니다:

|    옵션   |                                                                                                                                                                                                  설명                                                                                                                                                                                                  |
| :-----: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| IHR 장애인 |                                  현재 이 옵션은 인스턴트 하이퍼큐브 라우팅이 완전히 구현되지 않았기 때문에 비활성화되어 있습니다(즉, 1을 저장합니다). 또한 많은 수의 [샤드체인](/학습/개요/톤블록체인#많은-계정체인-샤드)이 네트워크에 연결되어 있을 때 이 옵션이 필요합니다. IHR 비활성화 옵션에 대한 자세한 내용은 [tblkch.pdf](https://ton.org/tblkch.pdf)(2장)에서 확인할 수 있습니다.                                 |
|  Bounce | 트랜잭션을 전송하는 동안 스마트 컨트랙트 처리 중에 다양한 오류가 발생할 수 있습니다. TON을 잃지 않으려면 반송 옵션을 1(true)로 설정해야 합니다. 이 경우 트랜잭션 처리 중 컨트랙트 오류가 발생하면 트랜잭션은 발신자에게 반환되며, 수수료를 제외한 동일한 금액의 TON을 받게 됩니다. 반송 불가 메시지에 대한 자세한 내용은 [여기](/개발/스마트컨트랙트/가이드라인/반송 불가 메시지)에서 확인할 수 있습니다. |
| Bounced |                                                                                                                                   반송된 트랜잭션은 스마트 컨트랙트로 트랜잭션을 처리하는 동안 오류가 발생하여 발신자에게 반환되는 트랜잭션입니다. 이 옵션은 수신된 트랜잭션이 반송되었는지 여부를 알려줍니다.                                                                                                                                   |
|   Src   |                                                                                                                                                      Src는 발신자 주소입니다. 이 경우 두 개의 0비트가 기록되어 `addr_none` 주소를 나타냅니다.                                                                                                                                                      |

다음 두 줄의 코드입니다:

```func
...
.store_slice(to_address)
.store_coins(amount)
...
```

- 수신자와 전송할 TON의 개수를 지정합니다.

마지막으로 나머지 코드 줄을 살펴봅시다:

```func
...
  .store_uint(0, 1) ;; Extra currency
  .store_uint(0, 4) ;; IHR fee
  .store_uint(0, 4) ;; Forwarding fee
  .store_uint(0, 64) ;; Logical time of creation
  .store_uint(0, 32) ;; UNIX time of creation
  .store_uint(0, 1) ;; State Init
  .store_uint(0, 1) ;; Message body
  ;; store something as a body
```

|     옵션     |                                                                                                                              설명                                                                                                                             |
| :--------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|    추가 통화   |                                                                                                       이는 기존 제톤의 기본 구현이며 현재 사용되지 않습니다.                                                                                                       |
|   IHR 수수료  |                  앞서 언급했듯이 IHR은 현재 사용되지 않으므로 이 수수료는 항상 0입니다. 이에 대한 자세한 내용은 [tblkch.pdf](https://ton.org/tblkch.pdf)(3.1.8)에서 확인할 수 있습니다.                  |
|   포워딩 수수료  |                                                                            전달 메시지 수수료. 이에 대한 자세한 내용은 [수수료 문서](/개발/방법/수수료-저수준#거래-단계)에서 확인할 수 있습니다.                                                                           |
|  논리적 생성 시간 |                                                                                                        올바른 트랜잭션 대기열을 만드는 데 사용된 시간입니다.                                                                                                       |
| UNIX 창조의 서 |                                                                                                           트랜잭션이 UNIX에서 생성된 시간입니다.                                                                                                           |
|   상태 초기화   | 스마트 컨트랙트 배포를 위한 코드 및 소스 데이터입니다. 비트가 `0`으로 설정되어 있으면 State Init이 없음을 의미합니다. 그러나 `1`로 설정되어 있다면 State Init이 같은 셀에 저장되어 있는지(0), 아니면 참조로 기록되어 있는지(1)를 나타내는 다른 비트를 기록해야 합니다. |
|   메시지 본문   |            이 부분은 메시지 본문이 저장되는 방식을 정의합니다. 때때로 메시지 본문이 너무 커서 메시지 자체에 들어갈 수 없는 경우가 있습니다. 이 경우, 본문이 참조로 사용됨을 나타내기 위해 비트가 `1`로 설정된 **참조**로 저장해야 합니다. 비트가 `0`이면 본문이 메시지와 같은 셀에 있는 것입니다.           |

위에 설명된 값(src 포함)은 State Init 및 Message Body 비트를 제외하고 유효성 검사기에 의해 재작성됩니다.

:::note
숫자 값이 지정한 것보다 적은 비트 내에 맞는 경우 누락된 0이 값의 왼쪽에 추가됩니다. 예를 들어 0x18은 5비트 이내 -> `11000`에 맞습니다. 그러나 6비트를 지정했기 때문에 최종 결과는 `011000`이 됩니다.
:::

다음으로, 다른 지갑 v3으로 톤코인을 전송하는 트랜잭션 준비를 시작하겠습니다.
먼저 사용자가 "\*\*안녕, 톤!"이라는 텍스트로 0.5톤을 자신에게 보내고 싶다고 가정하고, 이 문서 섹션을 참조하여 배우겠습니다([댓글로 메시지 보내는 방법](/develop/func/cookbook#how-to-simple-message)).

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { beginCell } from '@ton/core';

let internalMessageBody = beginCell()
  .storeUint(0, 32) // write 32 zero bits to indicate that a text comment will follow
  .storeStringTail("Hello, TON!") // write our text comment
  .endCell();
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
	"github.com/xssnick/tonutils-go/tvm/cell"
)

internalMessageBody := cell.BeginCell().
  MustStoreUInt(0, 32). // write 32 zero bits to indicate that a text comment will follow
  MustStoreStringSnake("Hello, TON!"). // write our text comment
  EndCell()
```

</TabItem>
</Tabs>

위에서 메시지 본문이 저장되는 `InternalMessageBody`를 만들었습니다. 하나의 셀(1023비트)에 맞지 않는 텍스트를 저장할 때는 [다음 문서](/개발/스마트-계약/지침/내부-메시지)에 따라 **데이터를 여러 셀로 분할**해야 한다는 점에 유의하세요. 하지만 이 경우 상위 라이브러리에서 요구사항에 따라 셀을 생성하므로 이 단계에서는 걱정할 필요가 없습니다.

다음으로, 앞서 학습한 정보에 따라 다음과 같이 `InternalMessage`를 생성합니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { toNano, Address } from '@ton/ton';

const walletAddress = Address.parse('put your wallet address');

let internalMessage = beginCell()
  .storeUint(0, 1) // indicate that it is an internal message -> int_msg_info$0
  .storeBit(1) // IHR Disabled
  .storeBit(1) // bounce
  .storeBit(0) // bounced
  .storeUint(0, 2) // src -> addr_none
  .storeAddress(walletAddress)
  .storeCoins(toNano("0.2")) // amount
  .storeBit(0) // Extra currency
  .storeCoins(0) // IHR Fee
  .storeCoins(0) // Forwarding Fee
  .storeUint(0, 64) // Logical time of creation
  .storeUint(0, 32) // UNIX time of creation
  .storeBit(0) // No State Init
  .storeBit(1) // We store Message Body as a reference
  .storeRef(internalMessageBody) // Store Message Body as a reference
  .endCell();
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/tlb"
)

walletAddress := address.MustParseAddr("put your address")

internalMessage := cell.BeginCell().
  MustStoreUInt(0, 1). // indicate that it is an internal message -> int_msg_info$0
  MustStoreBoolBit(true). // IHR Disabled
  MustStoreBoolBit(true). // bounce
  MustStoreBoolBit(false). // bounced
  MustStoreUInt(0, 2). // src -> addr_none
  MustStoreAddr(walletAddress).
  MustStoreCoins(tlb.MustFromTON("0.2").NanoTON().Uint64()).   // amount
  MustStoreBoolBit(false). // Extra currency
  MustStoreCoins(0). // IHR Fee
  MustStoreCoins(0). // Forwarding Fee
  MustStoreUInt(0, 64). // Logical time of creation
  MustStoreUInt(0, 32). // UNIX time of creation
  MustStoreBoolBit(false). // No State Init
  MustStoreBoolBit(true). // We store Message Body as a reference
  MustStoreRef(internalMessageBody). // Store Message Body as a reference
  EndCell()
```

</TabItem>
</Tabs>

### 메시지 만들기

지갑 스마트 컨트랙트의 `seqno`(시퀀스 번호)를 검색해야 합니다. 이를 위해 '클라이언트'가 생성되며, 이 클라이언트는 지갑의 "seqno" 가져오기 메서드 실행 요청을 전송하는 데 사용됩니다. 또한 다음 단계를 통해 트랜잭션에 서명하기 위해 시드 문구(지갑을 만들 때 저장한 [여기](#--외부 및 내부 트랜잭션))를 추가해야 합니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { TonClient } from '@ton/ton';
import { mnemonicToWalletKey } from '@ton/crypto';

const client = new TonClient({
  endpoint: "https://toncenter.com/api/v2/jsonRPC",
  apiKey: "put your api key" // you can get an api key from @tonapibot bot in Telegram
});

const mnemonic = 'put your mnemonic'; // word1 word2 word3
let getMethodResult = await client.runMethod(walletAddress, "seqno"); // run "seqno" GET method from your wallet contract
let seqno = getMethodResult.stack.readNumber(); // get seqno from response

const mnemonicArray = mnemonic.split(' '); // get array from string
const keyPair = await mnemonicToWalletKey(mnemonicArray); // get Secret and Public keys from mnemonic 
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "context"
  "crypto/ed25519"
  "crypto/hmac"
  "crypto/sha512"
  "github.com/xssnick/tonutils-go/liteclient"
  "github.com/xssnick/tonutils-go/ton"
  "golang.org/x/crypto/pbkdf2"
  "log"
  "strings"
)

mnemonic := strings.Split("put your mnemonic", " ") // get our mnemonic as array

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection) // create client

block, err := client.CurrentMasterchainInfo(context.Background()) // get current block, we will need it in requests to LiteServer
if err != nil {
  log.Fatalln("CurrentMasterchainInfo err:", err.Error())
  return
}

getMethodResult, err := client.RunGetMethod(context.Background(), block, walletAddress, "seqno") // run "seqno" GET method from your wallet contract
if err != nil {
  log.Fatalln("RunGetMethod err:", err.Error())
  return
}
seqno := getMethodResult.MustInt(0) // get seqno from response

// The next three lines will extract the private key using the mnemonic phrase. We will not go into cryptographic details. With the tonutils-go library, this is all implemented, but we’re doing it again to get a full understanding.
mac := hmac.New(sha512.New, []byte(strings.Join(mnemonic, " ")))
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // In TON libraries "TON default seed" is used as salt when getting keys

privateKey := ed25519.NewKeyFromSeed(k)
```

</TabItem>
</Tabs>

따라서 `seqno`, `키`, `내부 메시지`를 전송해야 합니다. 이제 지갑에 대한 [메시지](/개발/스마트컨트랙트/메시지)를 생성하고 튜토리얼의 시작 부분에서 사용한 순서대로 이 메시지에 데이터를 저장해야 합니다. 이는 다음과 같이 수행됩니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { sign } from '@ton/crypto';

let toSign = beginCell()
  .storeUint(698983191, 32) // subwallet_id | We consider this further
  .storeUint(Math.floor(Date.now() / 1e3) + 60, 32) // Transaction expiration time, +60 = 1 minute
  .storeUint(seqno, 32) // store seqno
  .storeUint(3, 8) // store mode of our internal transaction
  .storeRef(internalMessage); // store our internalMessage as a reference

let signature = sign(toSign.endCell().hash(), keyPair.secretKey); // get the hash of our message to wallet smart contract and sign it to get signature

let body = beginCell()
  .storeBuffer(signature) // store signature
  .storeBuilder(toSign) // store our message
  .endCell();
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "time"
)

toSign := cell.BeginCell().
  MustStoreUInt(698983191, 32). // subwallet_id | We consider this further
  MustStoreUInt(uint64(time.Now().UTC().Unix()+60), 32). // Transaction expiration time, +60 = 1 minute
  MustStoreUInt(seqno.Uint64(), 32). // store seqno
  MustStoreUInt(uint64(3), 8). // store mode of our internal transaction
  MustStoreRef(internalMessage) // store our internalMessage as a reference

signature := ed25519.Sign(privateKey, toSign.EndCell().Hash()) // get the hash of our message to wallet smart contract and sign it to get signature

body := cell.BeginCell().
  MustStoreSlice(signature, 512). // store signature
  MustStoreBuilder(toSign). // store our message
  EndCell()
```

</TabItem>
</Tabs>

여기서는 `toSign`의 정의에 '.endCell()\`이 사용되지 않았습니다. 사실 이 경우에는 **toSign 콘텐츠를 메시지 본문으로 직접 전송해야 합니다**. 셀을 작성해야 한다면 참조로 저장해야 합니다.

:::tip 월렛 V4
월렛 V3의 경우 아래에서 배운 기본 인증 프로세스 외에도 월렛 V4 스마트 컨트랙트(단순 번역인지 플러그인과 관련된 트랜잭션인지 판단하기 위해 옵코드 추출)(https://github.com/ton-blockchain/wallet-contract/blob/4111fd9e3313ec17d99ca9b5b1656445b5b49d8f/func/wallet-v4-code.fc#L94-L100)가 필요합니다. 이 버전과 일치하려면 seqno(시퀀스 번호) 작성 후 트랜잭션 모드를 지정하기 전에 `storeUint(0, 8).`(JS/TS), `MustStoreUInt(0, 8).`(Golang) 함수를 추가해야 합니다.
:::

### 외부 거래 생성

외부에서 블록체인으로 내부 메시지를 전달하려면, 외부 트랜잭션 내에서 메시지를 전송해야 합니다. 앞서 살펴본 것처럼, 컨트랙트에 외부 메시지를 보내는 것이 목표이므로 `ext_in_msg_info$10` 구조만 사용해야 합니다. 이제 지갑으로 전송할 외부 메시지를 생성해 보겠습니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
let externalMessage = beginCell()
  .storeUint(0b10, 2) // 0b10 -> 10 in binary
  .storeUint(0, 2) // src -> addr_none
  .storeAddress(walletAddress) // Destination address
  .storeCoins(0) // Import Fee
  .storeBit(0) // No State Init
  .storeBit(1) // We store Message Body as a reference
  .storeRef(body) // Store Message Body as a reference
  .endCell();
```

</TabItem>
<TabItem value="go" label="Golang">

```go
externalMessage := cell.BeginCell().
  MustStoreUInt(0b10, 2). // 0b10 -> 10 in binary
  MustStoreUInt(0, 2). // src -> addr_none
  MustStoreAddr(walletAddress). // Destination address
  MustStoreCoins(0). // Import Fee
  MustStoreBoolBit(false). // No State Init
  MustStoreBoolBit(true). // We store Message Body as a reference
  MustStoreRef(body). // Store Message Body as a reference
  EndCell()
```

</TabItem>
</Tabs>

|   옵션   |                                                                                                                                 설명                                                                                                                                 |
| :----: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|   Src  | 발신자 주소입니다. 수신 외부 메시지에는 발신자가 있을 수 없으므로 항상 2개의 0비트(addr_none [TL-B](https://github.com/ton-blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L100)가 있습니다.) |
| 수입 수수료 |                                                                                                         외부에서 들어오는 메시지를 가져오기 위해 지불하는 수수료입니다.                                                                                                        |
| 상태 초기화 |                                                       내부 메시지와 달리, 외부 메시지 내의 상태 초기화는 **외부 세계에서 컨트랙트를 배포하기 위해** 필요합니다. 내부 메시지와 함께 사용되는 상태 초기화는 한 컨트랙트가 다른 컨트랙트를 배포할 수 있도록 합니다.                                                       |
| 메시지 본문 |                                                                                                             처리를 위해 계약에 전송해야 하는 메시지입니다.                                                                                                             |

:::tip 0b10
0b10(b - 바이너리)은 바이너리 레코드를 나타냅니다. 이 과정에서 두 비트가 저장됩니다: 1`과 `0`입니다. 따라서 `ext_in_msg_info$10\`이라고 지정합니다.
:::

이제 컨트랙트로 전송할 준비가 완료된 메시지가 완성되었습니다. 이를 위해서는 먼저 `BOC`([Bag of Cells](/develop/data-formats/cell-boc#bag-of-cells))로 직렬화 한 다음 다음 코드를 사용하여 전송해야 합니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
console.log(externalMessage.toBoc().toString("base64"))

client.sendFile(externalMessage.toBoc());
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "encoding/base64"
  "github.com/xssnick/tonutils-go/tl"
)

log.Println(base64.StdEncoding.EncodeToString(externalMessage.ToBOCWithFlags(false)))

var resp tl.Serializable
err = client.Client().QueryLiteserver(context.Background(), ton.SendMessage{Body: externalMessage.ToBOCWithFlags(false)}, &resp)

if err != nil {
  log.Fatalln(err.Error())
  return
}
```

</TabItem>
</Tabs>

> 💡 유용한 링크:
>
> [백 오브 셀에 대해 자세히 알아보기](/개발/데이터 형식/cell-boc#bag-of-cells)

그 결과 콘솔에서 BOC의 출력과 지갑으로 전송된 트랜잭션을 확인할 수 있었습니다. base64로 인코딩된 문자열을 복사하면 [수동으로 트랜잭션을 전송하고 톤센터를 사용하여 해시를 검색할 수 있습니다](https://toncenter.com/api/v2/#/send/send_boc_return_hash_sendBocReturnHash_post).

## 👛 지갑 배포

이제 지갑을 배포하는 데 도움이 될 메시지 생성의 기본을 배웠습니다. 이전에는 지갑 앱을 통해 지갑을 배포했지만, 이 경우에는 수동으로 지갑을 배포해야 합니다.

이 섹션에서는 지갑(지갑 v3)을 처음부터 만드는 방법을 살펴보겠습니다. 지갑 스마트 컨트랙트의 코드를 컴파일하고, 니모닉 문구를 생성하고, 지갑 주소를 받고, 외부 트랜잭션과 상태 초기화를 사용하여 지갑을 배포하는 방법을 배우게 됩니다.

### 니모닉 생성

지갑을 올바르게 생성하기 위해 가장 먼저 필요한 것은 '개인' 키와 '공개' 키를 검색하는 것입니다. 이 작업을 수행하려면 니모닉 시드 구문을 생성한 다음 암호화 라이브러리를 사용하여 개인 키와 공개 키를 추출해야 합니다.

이 작업은 다음과 같이 수행됩니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { mnemonicToWalletKey, mnemonicNew } from '@ton/crypto';

// const mnemonicArray = 'put your mnemonic'.split(' ') // get our mnemonic as array
const mnemonicArray = await mnemonicNew(24); // 24 is the number of words in a seed phrase
const keyPair = await mnemonicToWalletKey(mnemonicArray); // extract private and public keys from mnemonic
console.log(mnemonicArray) // if we want, we can print our mnemonic
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
	"crypto/ed25519"
	"crypto/hmac"
	"crypto/sha512"
	"log"
	"github.com/xssnick/tonutils-go/ton/wallet"
	"golang.org/x/crypto/pbkdf2"
	"strings"
)

// mnemonic := strings.Split("put your mnemonic", " ") // get our mnemonic as array
mnemonic := wallet.NewSeed() // get new mnemonic

// The following three lines will extract the private key using the mnemonic phrase. We will not go into cryptographic details. It has all been implemented in the tonutils-go library, but it immediately returns the finished object of the wallet with the address and ready methods. So we’ll have to write the lines to get the key separately. Goland IDE will automatically import all required libraries (crypto, pbkdf2 and others).
mac := hmac.New(sha512.New, []byte(strings.Join(mnemonic, " "))) 
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // In TON libraries "TON default seed" is used as salt when getting keys
// 32 is a key len 

privateKey := ed25519.NewKeyFromSeed(k) // get private key
publicKey := privateKey.Public().(ed25519.PublicKey) // get public key from private key
log.Println(publicKey) // print publicKey so that at this stage the compiler does not complain that we do not use our variable
log.Println(mnemonic) // if we want, we can print our mnemonic
```

</TabItem>
</Tabs>

트랜잭션에 서명하려면 개인 키가 필요하며, 공개 키는 지갑의 스마트 컨트랙트에 저장됩니다.

:::danger 중요
지갑 코드를 실행할 때마다 동일한 키 쌍을 사용하려면 생성된 니모닉 시드 문구를 콘솔에 출력한 다음 저장하고 사용해야 합니다(이전 섹션에서 설명한 대로).
:::

### 하위 지갑 ID

스마트 컨트랙트 지갑의 가장 주목할 만한 장점 중 하나는 단 하나의 개인 키로 **방대한 수의 지갑**을 생성할 수 있다는 점입니다. 이는 TON 블록체인의 스마트 컨트랙트 주소가 'stateInit'을 포함한 여러 요소를 사용하여 계산되기 때문입니다. stateInit에는 블록체인의 스마트 컨트랙트 저장소에 저장되는 `코드`와 `초기 데이터`가 포함되어 있습니다.

stateInit 내에서 한 비트만 변경하면 다른 주소가 생성될 수 있습니다. 이것이 바로 `subwallet_id`가 처음에 생성된 이유입니다. 서브월렛_id\`는 컨트랙트 저장소에 저장되며, 하나의 개인 키로 여러 개의 다른 지갑(서브월렛 ID가 다른)을 생성하는 데 사용할 수 있습니다. 이 기능은 다양한 지갑 유형을 거래소와 같은 중앙화된 서비스와 통합할 때 매우 유용할 수 있습니다.

TON 블록체인의 소스 코드에서 가져온 아래 [코드 줄](https://github.com/ton-blockchain/ton/blob/4b940f8bad9c2d3bf44f196f6995963c7cee9cc3/tonlib/tonlib/TonlibClient.cpp#L2420)에 따르면 기본 subwallet_id 값은 `698983191`입니다:

```cpp
res.wallet_id = td::as<td::uint32>(res.config.zero_state_id.root_hash.as_slice().data());
```

구성 파일](https://ton.org/global-config.json)에서 제네시스 블록 정보(zero_state)를 검색할 수 있습니다. 이에 대한 복잡하고 자세한 내용을 이해할 필요는 없지만 `subwallet_id`의 기본값은 `698983191`이라는 점을 기억하는 것이 중요합니다.

각 지갑 컨트랙트는 다른 ID로 지갑에 요청이 전송되는 경우를 방지하기 위해 외부 트랜잭션에 대해 subwallet_id 필드를 확인합니다:

```func
var (subwallet_id, valid_until, msg_seqno) = (cs~load_uint(32), cs~load_uint(32), cs~load_uint(32));
var (stored_seqno, stored_subwallet, public_key) = (ds~load_uint(32), ds~load_uint(32), ds~load_uint(256));
throw_unless(34, subwallet_id == stored_subwallet);
```

컨트랙트의 초기 데이터에 위의 값을 추가해야 하므로 변수를 다음과 같이 저장해야 합니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
const subWallet = 698983191;
```

</TabItem>
<TabItem value="go" label="Golang">

```go
var subWallet uint64 = 698983191
```

</TabItem>
</Tabs>

### 지갑 코드 컴파일하기

이제 개인 키와 공개 키, 서브월렛 아이디가 명확하게 정의되었으므로 지갑 코드를 컴파일해야 합니다. 이를 위해 공식 저장소의 [지갑 v3 코드](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet3-code.fc)를 사용하겠습니다.

지갑 코드를 컴파일하려면 [@ton-community/func-js](https://github.com/ton-community/func-js) 라이브러리를 사용해야 합니다.
이 라이브러리를 사용하면 FunC 코드를 컴파일하고 코드가 포함된 셀을 검색할 수 있습니다. 시작하려면 다음과 같이 라이브러리를 설치하고 `package.json`에 저장(--save)해야 합니다:

```bash
npm i --save @ton-community/func-js
```

코드 컴파일을 위한 라이브러리는 자바스크립트 기반이므로 코드 컴파일에는 자바스크립트만 사용할 것입니다.
하지만 컴파일이 완료된 후 셀의 **base64 출력**만 있으면 이 컴파일된 코드를 Go 등의 언어에서 사용할 수 있습니다.

먼저 두 개의 파일을 만들어야 합니다: wallet_v3.fc`와 `stdlib.fc`입니다. 컴파일러는 stdlib.fc 라이브러리와 함께 작동합니다. 라이브러리에는 `asm` 명령어에 해당하는 모든 필수 및 기본 함수가 만들어져 있습니다. stdlib.fc 파일은 [여기](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/stdlib.fc)에서 다운로드할 수 있습니다. 지갑_v3.fc` 파일에 위의 코드를 복사해야 합니다.

이제 우리가 만들고 있는 프로젝트의 구조는 다음과 같습니다:

```
.
├── src/
│   ├── main.ts
│   ├── wallet_v3.fc
│   └── stdlib.fc
├── nodemon.json
├── package-lock.json
├── package.json
└── tsconfig.json
```

:::info
IDE 플러그인이 `stdlib.fc` 파일에 있는 `() set_seed(int) impure asm "SETRAND";`와 충돌하는 것은 괜찮습니다.
:::

'wallet_v3.fc' 파일의 시작 부분에 다음 줄을 추가하여 아래에서 stdlib의 함수가 사용됨을 표시해야 합니다:

```func
#include "stdlib.fc";
```

이제 스마트 컨트랙트를 컴파일하고 `npm run start:dev`를 사용하여 실행하는 코드를 작성해 보겠습니다:

```js
import { compileFunc } from '@ton-community/func-js';
import fs from 'fs'; // we use fs for reading content of files
import { Cell } from '@ton/core';

const result = await compileFunc({
targets: ['wallet_v3.fc'], // targets of your project
sources: {
    "stdlib.fc": fs.readFileSync('./src/stdlib.fc', { encoding: 'utf-8' }),
    "wallet_v3.fc": fs.readFileSync('./src/wallet_v3.fc', { encoding: 'utf-8' }),
}
});

if (result.status === 'error') {
console.error(result.message)
return;
}

const codeCell = Cell.fromBoc(Buffer.from(result.codeBoc, "base64"))[0]; // get buffer from base64 encoded BOC and get cell from this buffer

// now we have base64 encoded BOC with compiled code in result.codeBoc
console.log('Code BOC: ' + result.codeBoc);
console.log('\nHash: ' + codeCell.hash().toString('base64')); // get the hash of cell and convert in to base64 encoded string. We will need it further
```

결과는 터미널에 다음과 같은 출력으로 표시됩니다:

```text
Code BOC: te6ccgEBCAEAhgABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQCW8oMI1xgg0x/TH9MfAvgju/Jj7UTQ0x/TH9P/0VEyuvKhUUS68qIE+QFUEFX5EPKj+ACTINdKltMH1AL7AOgwAaTIyx/LH8v/ye1UAATQMAIBSAYHABe7Oc7UTQ0z8x1wv/gAEbjJftRNDXCx+A==

Hash: idlku00WfSC36ujyK2JVT92sMBEpCNRUXOGO4sJVBPA=
```

이 작업이 완료되면 다른 라이브러리 및 언어를 사용하여 지갑 코드와 동일한 셀(base64로 인코딩된 출력물 사용)을 검색할 수 있습니다:

<Tabs groupId="code-examples">
<TabItem value="go" label="Golang">

```go
import (
  "encoding/base64"
  "github.com/xssnick/tonutils-go/tvm/cell"
)

base64BOC := "te6ccgEBCAEAhgABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQCW8oMI1xgg0x/TH9MfAvgju/Jj7UTQ0x/TH9P/0VEyuvKhUUS68qIE+QFUEFX5EPKj+ACTINdKltMH1AL7AOgwAaTIyx/LH8v/ye1UAATQMAIBSAYHABe7Oc7UTQ0z8x1wv/gAEbjJftRNDXCx+A==" // save our base64 encoded output from compiler to variable
codeCellBytes, _ := base64.StdEncoding.DecodeString(base64BOC) // decode base64 in order to get byte array
codeCell, err := cell.FromBOC(codeCellBytes) // get cell with code from byte array
if err != nil { // check if there are any error
  panic(err) 
}

log.Println("Hash:", base64.StdEncoding.EncodeToString(codeCell.Hash())) // get the hash of our cell, encode it to base64 because it has []byte type and output to the terminal
```

</TabItem>
</Tabs>

결과는 터미널에 다음과 같은 출력으로 표시됩니다:

```text
idlku00WfSC36ujyK2JVT92sMBEpCNRUXOGO4sJVBPA=
```

위의 프로세스가 완료되면 해시가 일치하므로 셀 내에서 올바른 코드가 사용되고 있음을 확인할 수 있습니다.

### 배포를 위한 상태 초기화 만들기

트랜잭션을 구축하기 전에 스테이트 이니트가 무엇인지 이해하는 것이 중요합니다. 먼저 [TL-B 체계](https://github.com/ton-blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L141-L143)를 살펴봅시다:

|             옵션             |                                                                                                                                                                              설명                                                                                                                                                                             |
| :------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
| 분할_뎁스 |                     이 옵션은 여러 [샤드체인](/학습/개요/톤블록체인#많은-계정체인-샤드)에 분할하여 위치시킬 수 있는 고부하 스마트 컨트랙트를 위한 것입니다.  자세한 작동 방식은 [tblkch.pdf](https://ton.org/tblkch.pdf)(4.1.6)에서 확인할 수 있습니다.  지갑 스마트 컨트랙트 내에서만 사용되므로 `0` 비트만 저장됩니다.                     |
|             특별             | 틱톡에 사용됩니다. 이러한 스마트 컨트랙트는 각 블록에 대해 자동으로 호출되며 일반 스마트 컨트랙트에는 필요하지 않습니다. 이에 대한 정보는 [이 섹션](/개발/데이터-포맷/트랜잭션-레이아웃#틱톡) 또는 [tblkch.pdf](https://ton.org/tblkch.pdf)(4.1.6)에서 확인할 수 있습니다. 이 사양에서는 이러한 함수가 필요하지 않으므로 `0` 비트만 저장됩니다. |
|             코드             |                                                                                                                                                     1\` 비트는 스마트 컨트랙트 코드가 참조로 존재함을 의미합니다.                                                                                                                                                    |
|             데이터            |                                                                                                                                                    '1' 비트는 스마트 컨트랙트 데이터가 참조로 존재함을 의미합니다.                                                                                                                                                    |
|            라이브러리           |     마스터체인](/학습/개요/톤블록체인#마스터체인-블록체인-블록체인)에서 작동하며 다른 스마트 컨트랙트에서 사용할 수 있는 라이브러리입니다. 지갑에는 사용되지 않으므로 비트는 `0`으로 설정됩니다. 이에 대한 정보는 [tblkch.pdf](https://ton.org/tblkch.pdf)(1.8.4)에서 확인할 수 있습니다.    |

다음으로 배포 직후 컨트랙트의 저장소에 존재할 '초기 데이터'를 준비하겠습니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { beginCell } from '@ton/core';

const dataCell = beginCell()
  .storeUint(0, 32) // Seqno
  .storeUint(698983191, 32) // Subwallet ID
  .storeBuffer(keyPair.publicKey) // Public Key
  .endCell();
```

</TabItem>
<TabItem value="go" label="Golang">

```go
dataCell := cell.BeginCell().
  MustStoreUInt(0, 32). // Seqno
  MustStoreUInt(698983191, 32). // Subwallet ID
  MustStoreSlice(publicKey, 256). // Public Key
  EndCell()
```

</TabItem>
</Tabs>

이 단계에서는 컨트랙트 '코드'와 '초기 데이터'가 모두 존재합니다. 이 데이터로 **지갑 주소**를 생성할 수 있습니다. 지갑 주소는 코드와 초기 데이터가 포함된 상태 초기화에 따라 달라집니다.

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { Address } from '@ton/core';

const stateInit = beginCell()
  .storeBit(0) // No split_depth
  .storeBit(0) // No special
  .storeBit(1) // We have code
  .storeRef(codeCell)
  .storeBit(1) // We have data
  .storeRef(dataCell)
  .storeBit(0) // No library
  .endCell();

const contractAddress = new Address(0, stateInit.hash()); // get the hash of stateInit to get the address of our smart contract in workchain with ID 0
console.log(`Contract address: ${contractAddress.toString()}`); // Output contract address to console
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "github.com/xssnick/tonutils-go/address"
)

stateInit := cell.BeginCell().
  MustStoreBoolBit(false). // No split_depth
  MustStoreBoolBit(false). // No special
  MustStoreBoolBit(true). // We have code
  MustStoreRef(codeCell).
  MustStoreBoolBit(true). // We have data
  MustStoreRef(dataCell).
  MustStoreBoolBit(false). // No library
  EndCell()

contractAddress := address.NewAddress(0, 0, stateInit.Hash()) // get the hash of stateInit to get the address of our smart contract in workchain with ID 0
log.Println("Contract address:", contractAddress.String()) // Output contract address to console
```

</TabItem>
</Tabs>

이제 상태 초기화를 사용해 트랜잭션을 생성하고 블록체인으로 전송할 수 있습니다. 이 과정을 수행하려면 **최소 0.1톤**의 지갑 잔액이 필요합니다(잔액은 더 적을 수 있지만, 이 금액이면 충분합니다). 이를 위해서는 튜토리얼의 앞부분에서 언급한 코드를 실행하고 올바른 지갑 주소를 얻은 다음 이 주소로 0.1톤을 보내야 합니다.

이전 섹션\*\*에서 구축한 트랜잭션과 유사한 트랜잭션을 구축하는 것부터 시작하겠습니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { sign } from '@ton/crypto';
import { toNano } from '@ton/core';

const internalMessageBody = beginCell()
  .storeUint(0, 32)
  .storeStringTail("Hello, TON!")
  .endCell();

const internalMessage = beginCell()
  .storeUint(0x10, 6) // no bounce
  .storeAddress(Address.parse("put your first wallet address from were you sent 0.1 TON"))
  .storeCoins(toNano("0.03"))
  .storeUint(1, 1 + 4 + 4 + 64 + 32 + 1 + 1) // We store 1 that means we have body as a reference
  .storeRef(internalMessageBody)
  .endCell();

// transaction for our wallet
const toSign = beginCell()
  .storeUint(subWallet, 32)
  .storeUint(Math.floor(Date.now() / 1e3) + 60, 32)
  .storeUint(0, 32) // We put seqno = 0, because after deploying wallet will store 0 as seqno
  .storeUint(3, 8)
  .storeRef(internalMessage);

const signature = sign(toSign.endCell().hash(), keyPair.secretKey);
const body = beginCell()
  .storeBuffer(signature)
  .storeBuilder(toSign)
  .endCell();
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "github.com/xssnick/tonutils-go/tlb"
  "time"
)

internalMessageBody := cell.BeginCell().
  MustStoreUInt(0, 32).
  MustStoreStringSnake("Hello, TON!").
  EndCell()

internalMessage := cell.BeginCell().
  MustStoreUInt(0x10, 6). // no bounce
  MustStoreAddr(address.MustParseAddr("put your first wallet address from were you sent 0.1 TON")).
  MustStoreBigCoins(tlb.MustFromTON("0.03").NanoTON()).
  MustStoreUInt(1, 1 + 4 + 4 + 64 + 32 + 1 + 1). // We store 1 that means we have body as a reference
  MustStoreRef(internalMessageBody).
  EndCell()

// transaction for our wallet
toSign := cell.BeginCell().
  MustStoreUInt(subWallet, 32).
  MustStoreUInt(uint64(time.Now().UTC().Unix()+60), 32).
  MustStoreUInt(0, 32). // We put seqno = 0, because after deploying wallet will store 0 as seqno
  MustStoreUInt(3, 8).
  MustStoreRef(internalMessage)

signature := ed25519.Sign(privateKey, toSign.EndCell().Hash())
body := cell.BeginCell().
  MustStoreSlice(signature, 512).
  MustStoreBuilder(toSign).
	EndCell()
```

</TabItem>
</Tabs>

이 작업이 완료되면 올바른 상태 초기화 및 메시지 본문이 생성됩니다.

### 외부 거래 보내기

가장 큰 차이점은 올바른 컨트랙트 배포를 수행하기 위해 State Init이 저장되기 때문에 외부 메시지가 있다는 것입니다. 컨트랙트에는 아직 자체 코드가 없으므로 내부 메시지를 처리할 수 없습니다. 따라서 다음으로 코드와 초기 데이터를 **성공적으로 배포된 후** "Hello, TON!" 코멘트와 함께 전송하여 메시지를 처리할 수 있도록 합니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
const externalMessage = beginCell()
  .storeUint(0b10, 2) // indicate that it is an incoming external transaction
  .storeUint(0, 2) // src -> addr_none
  .storeAddress(contractAddress)
  .storeCoins(0) // Import fee
  .storeBit(1) // We have State Init
  .storeBit(1) // We store State Init as a reference
  .storeRef(stateInit) // Store State Init as a reference
  .storeBit(1) // We store Message Body as a reference
  .storeRef(body) // Store Message Body as a reference
  .endCell();
```

</TabItem>
<TabItem value="go" label="Golang">

```go
externalMessage := cell.BeginCell().
  MustStoreUInt(0b10, 2). // indicate that it is an incoming external transaction
  MustStoreUInt(0, 2). // src -> addr_none
  MustStoreAddr(contractAddress).
  MustStoreCoins(0). // Import fee
  MustStoreBoolBit(true). // We have State Init
  MustStoreBoolBit(true).  // We store State Init as a reference
  MustStoreRef(stateInit). // Store State Init as a reference
  MustStoreBoolBit(true). // We store Message Body as a reference
  MustStoreRef(body). // Store Message Body as a reference
  EndCell()
```

</TabItem>
</Tabs>

마지막으로 트랜잭션을 블록체인으로 전송하여 지갑을 배포하고 사용할 수 있습니다.

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { TonClient } from '@ton/ton';

const client = new TonClient({
  endpoint: "https://toncenter.com/api/v2/jsonRPC",
  apiKey: "put your api key" // you can get an api key from @tonapibot bot in Telegram
});

client.sendFile(externalMessage.toBoc());
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "context"
  "github.com/xssnick/tonutils-go/liteclient"
  "github.com/xssnick/tonutils-go/tl"
  "github.com/xssnick/tonutils-go/ton"
)

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection)

var resp tl.Serializable
err = client.Client().QueryLiteserver(context.Background(), ton.SendMessage{Body: externalMessage.ToBOCWithFlags(false)}, &resp)
if err != nil {
  log.Fatalln(err.Error())
  return
}
```

</TabItem>
</Tabs>

모드 `3`을 사용하여 내부 메시지를 보냈습니다. 동일한 지갑의 배포를 반복해야 하는 경우 **스마트 컨트랙트를 파기**할 수 있습니다. 이를 위해서는 128(스마트 컨트랙트 전체 잔액 가져가기) + 32(스마트 컨트랙트 파기)를 더하여 `160`으로 모드를 올바르게 설정하면 남은 TON 잔액을 가져와 지갑을 다시 배포할 수 있습니다.

새 트랜잭션이 발생할 때마다 **seqno**를 하나씩 늘려야 한다는 점에 유의하세요.

:::info
우리가 사용한 계약 코드는 [확인됨](https://tonscan.org/tx/BL9T1i5DjX1JRLUn4z9JOgOWRKWQ80pSNevis26hGvc=)이며, [여기](https://tonscan.org/address/EQDBjzo_iQCZh3bZSxFnK9ue4hLTOKgsCNKfC8LOUM4SlSCX#source)에서 예시를 볼 수 있습니다.
:::

## 💸 월렛 스마트 컨트랙트로 작업하기

이 튜토리얼의 전반부를 마친 후에는 지갑 스마트 컨트랙트와 그 개발 및 사용 방식에 대해 훨씬 더 익숙해졌습니다. 미리 구성된 라이브러리 함수에 의존하지 않고 스마트 컨트랙트를 배포 및 소멸하고 메시지를 전송하는 방법을 배웠습니다. 다음 섹션에서는 위에서 배운 내용을 더 많이 적용하기 위해 좀 더 복잡한 메시지를 구축하고 전송하는 데 집중하겠습니다.

### 여러 개의 메시지를 동시에 보내기

이미 알고 계시겠지만, [하나의 셀은 최대 1023비트의 데이터와 최대 4개의 참조를 다른 셀에 저장할 수 있습니다](/개발/데이터-포맷/셀-boc#셀). 이 튜토리얼의 첫 번째 섹션에서는 내부 메시지를 '전체' 루프를 통해 링크로 전달하고 전송하는 방법을 자세히 설명했습니다. 즉, 외부\*\* 메시지 안에 내부 메시지를 최대 4개까지 \*\*저장할 수 있습니다. 이렇게 하면 4개의 트랜잭션을 동시에 전송할 수 있습니다.

이를 위해서는 4개의 서로 다른 내부 메시지를 만들어야 합니다. 이 작업은 수동으로 또는 '루프'를 통해 수행할 수 있습니다. TON 금액 배열, 댓글 배열, 메시지 배열의 세 가지 배열을 정의해야 합니다. 메시지의 경우 내부 메시지라는 또 하나의 배열을 준비해야 합니다.

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { Cell } from '@ton/core';

const internalMessagesAmount = ["0.01", "0.02", "0.03", "0.04"];
const internalMessagesComment = [
  "Hello, TON! #1",
  "Hello, TON! #2",
  "", // Let's leave the third transaction without comment
  "Hello, TON! #4" 
]
const destinationAddresses = [
  "Put any address that belongs to you",
  "Put any address that belongs to you",
  "Put any address that belongs to you",
  "Put any address that belongs to you"
] // All 4 addresses can be the same

let internalMessages:Cell[] = []; // array for our internal messages
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "github.com/xssnick/tonutils-go/tvm/cell"
)

internalMessagesAmount := [4]string{"0.01", "0.02", "0.03", "0.04"}
internalMessagesComment := [4]string{
  "Hello, TON! #1",
  "Hello, TON! #2",
  "", // Let's leave the third transaction without comment
  "Hello, TON! #4",
}
destinationAddresses := [4]string{
  "Put any address that belongs to you",
  "Put any address that belongs to you",
  "Put any address that belongs to you",
  "Put any address that belongs to you",
} // All 4 addresses can be the same

var internalMessages [len(internalMessagesAmount)]*cell.Cell // array for our internal messages
```

</TabItem>
</Tabs>

모든 메시지에 대한 [전송 모드](/개발/스마트-계약/메시지#메시지-모드)는 '모드 3'으로 설정되어 있습니다.  그러나 다른 모드가 필요한 경우 다른 목적을 달성하기 위해 배열을 만들 수 있습니다.

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { Address, beginCell, toNano } from '@ton/core';

for (let index = 0; index < internalMessagesAmount.length; index++) {
  const amount = internalMessagesAmount[index];
  
  let internalMessage = beginCell()
      .storeUint(0x18, 6) // bounce
      .storeAddress(Address.parse(destinationAddresses[index]))
      .storeCoins(toNano(amount))
      .storeUint(0, 1 + 4 + 4 + 64 + 32 + 1);
      
  /*
      At this stage, it is not clear if we will have a message body. 
      So put a bit only for stateInit, and if we have a comment, in means 
      we have a body message. In that case, set the bit to 1 and store the 
      body as a reference.
  */

  if(internalMessagesComment[index] != "") {
    internalMessage.storeBit(1) // we store Message Body as a reference

    let internalMessageBody = beginCell()
      .storeUint(0, 32)
      .storeStringTail(internalMessagesComment[index])
      .endCell();

    internalMessage.storeRef(internalMessageBody);
  } 
  else 
    /*
        Since we do not have a message body, we indicate that 
        the message body is in this message, but do not write it, 
        which means it is absent. In that case, just set the bit to 0.
    */
    internalMessage.storeBit(0);
  
  internalMessages.push(internalMessage.endCell());
}
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/tlb"
)

for i := 0; i < len(internalMessagesAmount); i++ {
  amount := internalMessagesAmount[i]

  internalMessage := cell.BeginCell().
    MustStoreUInt(0x18, 6). // bounce
    MustStoreAddr(address.MustParseAddr(destinationAddresses[i])).
    MustStoreBigCoins(tlb.MustFromTON(amount).NanoTON()).
    MustStoreUInt(0, 1+4+4+64+32+1)

  /*
      At this stage, it is not clear if we will have a message body. 
      So put a bit only for stateInit, and if we have a comment, in means 
      we have a body message. In that case, set the bit to 1 and store the 
      body as a reference.
  */

  if internalMessagesComment[i] != "" {
    internalMessage.MustStoreBoolBit(true) // we store Message Body as a reference

    internalMessageBody := cell.BeginCell().
      MustStoreUInt(0, 32).
      MustStoreStringSnake(internalMessagesComment[i]).
      EndCell()

    internalMessage.MustStoreRef(internalMessageBody)
  } else {
    /*
        Since we do not have a message body, we indicate that
        the message body is in this message, but do not write it,
        which means it is absent. In that case, just set the bit to 0.
    */
    internalMessage.MustStoreBoolBit(false)
  }
  internalMessages[i] = internalMessage.EndCell()
}
```

</TabItem>
</Tabs>

이제 [2장](/개발/스마트 컨트랙트/자습서/지갑#-지갑 배포하기)에서 배운 지식을 활용하여 4개의 트랜잭션을 동시에 전송할 수 있는 지갑을 만들어 보겠습니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { TonClient } from '@ton/ton';
import { mnemonicToWalletKey } from '@ton/crypto';

const walletAddress = Address.parse('put your wallet address');
const client = new TonClient({
  endpoint: "https://toncenter.com/api/v2/jsonRPC",
  apiKey: "put your api key" // you can get an api key from @tonapibot bot in Telegram
});

const mnemonic = 'put your mnemonic'; // word1 word2 word3
let getMethodResult = await client.runMethod(walletAddress, "seqno"); // run "seqno" GET method from your wallet contract
let seqno = getMethodResult.stack.readNumber(); // get seqno from response

const mnemonicArray = mnemonic.split(' '); // get array from string
const keyPair = await mnemonicToWalletKey(mnemonicArray); // get Secret and Public keys from mnemonic 

let toSign = beginCell()
  .storeUint(698983191, 32) // subwallet_id
  .storeUint(Math.floor(Date.now() / 1e3) + 60, 32) // Transaction expiration time, +60 = 1 minute
  .storeUint(seqno, 32); // store seqno
  // Do not forget that if we use Wallet V4, we need to add .storeUint(0, 8) 
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
	"context"
	"crypto/ed25519"
	"crypto/hmac"
	"crypto/sha512"
	"github.com/xssnick/tonutils-go/liteclient"
	"github.com/xssnick/tonutils-go/ton"
	"golang.org/x/crypto/pbkdf2"
	"log"
	"strings"
	"time"
)

walletAddress := address.MustParseAddr("put your wallet address")

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection)

mnemonic := strings.Split("put your mnemonic", " ") // word1 word2 word3
// The following three lines will extract the private key using the mnemonic phrase.
// We will not go into cryptographic details. In the library tonutils-go, it is all implemented,
// but it immediately returns the finished object of the wallet with the address and ready-made methods.
// So we’ll have to write the lines to get the key separately. Goland IDE will automatically import
// all required libraries (crypto, pbkdf2 and others).
mac := hmac.New(sha512.New, []byte(strings.Join(mnemonic, " ")))
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // In TON libraries "TON default seed" is used as salt when getting keys
// 32 is a key len
privateKey := ed25519.NewKeyFromSeed(k)              // get private key

block, err := client.CurrentMasterchainInfo(context.Background()) // get current block, we will need it in requests to LiteServer
if err != nil {
  log.Fatalln("CurrentMasterchainInfo err:", err.Error())
  return
}

getMethodResult, err := client.RunGetMethod(context.Background(), block, walletAddress, "seqno") // run "seqno" GET method from your wallet contract
if err != nil {
  log.Fatalln("RunGetMethod err:", err.Error())
  return
}
seqno := getMethodResult.MustInt(0) // get seqno from response

toSign := cell.BeginCell().
  MustStoreUInt(698983191, 32). // subwallet_id | We consider this further
  MustStoreUInt(uint64(time.Now().UTC().Unix()+60), 32). // transaction expiration time, +60 = 1 minute
  MustStoreUInt(seqno.Uint64(), 32) // store seqno
  // Do not forget that if we use Wallet V4, we need to add MustStoreUInt(0, 8). 
```

</TabItem>
</Tabs>

다음으로 앞서 루프에서 작성한 메시지를 추가합니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
for (let index = 0; index < internalMessages.length; index++) {
  const internalMessage = internalMessages[index];
  toSign.storeUint(3, 8) // store mode of our internal transaction
  toSign.storeRef(internalMessage) // store our internalMessage as a reference
}
```

</TabItem>
<TabItem value="go" label="Golang">

```go
for i := 0; i < len(internalMessages); i++ {
		internalMessage := internalMessages[i]
		toSign.MustStoreUInt(3, 8) // store mode of our internal transaction
		toSign.MustStoreRef(internalMessage) // store our internalMessage as a reference
}
```

</TabItem>
</Tabs>

위의 과정이 완료되었으므로 이제 메시지를 **서명**하고, (이 튜토리얼의 이전 섹션에서 설명한 대로) 외부 메시지를 작성하여 블록체인에 **전송**해 보겠습니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { sign } from '@ton/crypto';

let signature = sign(toSign.endCell().hash(), keyPair.secretKey); // get the hash of our message to wallet smart contract and sign it to get signature

let body = beginCell()
    .storeBuffer(signature) // store signature
    .storeBuilder(toSign) // store our message
    .endCell();

let externalMessage = beginCell()
    .storeUint(0b10, 2) // ext_in_msg_info$10
    .storeUint(0, 2) // src -> addr_none
    .storeAddress(walletAddress) // Destination address
    .storeCoins(0) // Import Fee
    .storeBit(0) // No State Init
    .storeBit(1) // We store Message Body as a reference
    .storeRef(body) // Store Message Body as a reference
    .endCell();

client.sendFile(externalMessage.toBoc());
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "github.com/xssnick/tonutils-go/tl"
)

signature := ed25519.Sign(privateKey, toSign.EndCell().Hash()) // get the hash of our message to wallet smart contract and sign it to get signature

body := cell.BeginCell().
  MustStoreSlice(signature, 512). // store signature
  MustStoreBuilder(toSign). // store our message
  EndCell()

externalMessage := cell.BeginCell().
  MustStoreUInt(0b10, 2). // ext_in_msg_info$10
  MustStoreUInt(0, 2). // src -> addr_none
  MustStoreAddr(walletAddress). // Destination address
  MustStoreCoins(0). // Import Fee
  MustStoreBoolBit(false). // No State Init
  MustStoreBoolBit(true). // We store Message Body as a reference
  MustStoreRef(body). // Store Message Body as a reference
  EndCell()

var resp tl.Serializable
err = client.Client().QueryLiteserver(context.Background(), ton.SendMessage{Body: externalMessage.ToBOCWithFlags(false)}, &resp)

if err != nil {
  log.Fatalln(err.Error())
  return
}
```

</TabItem>
</Tabs>

:::info 연결 오류
라이트 서버 연결(Golang)과 관련된 오류가 발생하면 트랜잭션을 전송할 수 있을 때까지 코드를 실행해야 합니다. 이는 톤툴즈-고 라이브러리가 코드에 지정된 전역 구성을 통해 여러 개의 다른 라이트 서버를 사용하기 때문입니다. 그러나 모든 라이트 서버가 연결을 수락할 수 있는 것은 아닙니다.
:::

이 프로세스가 완료되면 TON 블록체인 탐색기를 사용하여 지갑이 이전에 지정한 주소로 4개의 트랜잭션을 전송했는지 확인할 수 있습니다.

### NFT 전송

일반 트랜잭션 외에도 사용자들은 종종 NFT를 서로에게 전송하기도 합니다. 안타깝게도 모든 라이브러리에 이러한 유형의 스마트 컨트랙트에 사용할 수 있는 메서드가 포함되어 있는 것은 아닙니다. 따라서 NFT 전송을 위한 트랜잭션을 구축할 수 있는 코드를 만들어야 합니다. 먼저 TON NFT [표준](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md)에 대해 더 자세히 알아봅시다.

특히 [NFT 전송](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md#1-transfer)을 위한 TL-B에 대한 자세한 이해가 필요합니다.

- 쿼리 ID\`: 쿼리 ID는 트랜잭션 처리 측면에서 아무런 가치가 없습니다. NFT 컨트랙트는 이를 검증하지 않고 읽기만 합니다. 이 값은 서비스가 식별 목적으로 각 트랜잭션에 특정 쿼리 ID를 할당하고자 할 때 유용할 수 있습니다. 따라서 0으로 설정하겠습니다.

- 응답_대상\`: 소유권 변경 트랜잭션을 처리한 후 추가 TON이 발생합니다. 지정한 경우 이 주소로 전송되며, 그렇지 않으면 NFT 잔고에 남아 있습니다.

- 커스텀 페이로드\`: custom_payload는 특정 작업을 수행하는 데 필요하며 일반 NFT에는 사용되지 않습니다.

- forward_amount\`: forward_amount가 0이 아닌 경우, 지정된 TON 금액이 새 소유자에게 전송됩니다. 이렇게 하면 새 소유자는 무언가를 받았다는 알림을 받게 됩니다.

- 포워드_페이로드\`: forward_payload는 forward_amount와 함께 새 소유자에게 전송할 수 있는 추가 데이터입니다. 예를 들어, 앞서 튜토리얼에서 설명한 것처럼 forward_payload를 사용하면 [NFT 전송 중 코멘트를 추가](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md#forward_payload-format)할 수 있습니다. 그러나 forward_payload는 TON의 NFT 표준에 따라 작성되었지만, 블록체인 탐색기는 다양한 세부 정보 표시를 완벽하게 지원하지 않습니다. 제톤을 표시할 때도 동일한 문제가 존재합니다.

이제 트랜잭션 자체를 구축해 보겠습니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { Address, beginCell, toNano } from '@ton/core';

const destinationAddress = Address.parse("put your wallet where you want to send NFT");
const walletAddress = Address.parse("put your wallet which is the owner of NFT")
const nftAddress = Address.parse("put your nft address");

// We can add a comment, but it will not be displayed in the explorers, 
// as it is not supported by them at the time of writing the tutorial.
const forwardPayload = beginCell()
  .storeUint(0, 32)
  .storeStringTail("Hello, TON!")
  .endCell();

const transferNftBody = beginCell()
  .storeUint(0x5fcc3d14, 32) // Opcode for NFT transfer
  .storeUint(0, 64) // query_id
  .storeAddress(destinationAddress) // new_owner
  .storeAddress(walletAddress) // response_destination for excesses
  .storeBit(0) // we do not have custom_payload
  .storeCoins(toNano("0.01")) // forward_amount
  .storeBit(1) // we store forward_payload as a reference
  .storeRef(forwardPayload) // store forward_payload as a .reference
  .endCell();

const internalMessage = beginCell().
  storeUint(0x18, 6). // bounce
  storeAddress(nftAddress).
  storeCoins(toNano("0.05")).
  storeUint(1, 1 + 4 + 4 + 64 + 32 + 1 + 1). // We store 1 that means we have body as a reference
  storeRef(transferNftBody).
  endCell();
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/tlb"
  "github.com/xssnick/tonutils-go/tvm/cell"
)

destinationAddress := address.MustParseAddr("put your wallet where you want to send NFT")
walletAddress := address.MustParseAddr("put your wallet which is the owner of NFT")
nftAddress := address.MustParseAddr("put your nft address")

// We can add a comment, but it will not be displayed in the explorers,
// as it is not supported by them at the time of writing the tutorial.
forwardPayload := cell.BeginCell().
  MustStoreUInt(0, 32).
  MustStoreStringSnake("Hello, TON!").
  EndCell()

transferNftBody := cell.BeginCell().
  MustStoreUInt(0x5fcc3d14, 32). // Opcode for NFT transfer
  MustStoreUInt(0, 64). // query_id
  MustStoreAddr(destinationAddress). // new_owner
  MustStoreAddr(walletAddress). // response_destination for excesses
  MustStoreBoolBit(false). // we do not have custom_payload
  MustStoreBigCoins(tlb.MustFromTON("0.01").NanoTON()). // forward_amount
  MustStoreBoolBit(true). // we store forward_payload as a reference
  MustStoreRef(forwardPayload). // store forward_payload as a reference
  EndCell()

internalMessage := cell.BeginCell().
  MustStoreUInt(0x18, 6). // bounce
  MustStoreAddr(nftAddress).
  MustStoreBigCoins(tlb.MustFromTON("0.05").NanoTON()).
  MustStoreUInt(1, 1 + 4 + 4 + 64 + 32 + 1 + 1). // We store 1 that means we have body as a reference
  MustStoreRef(transferNftBody).
  EndCell()
```

</TabItem>
</Tabs>

NFT 전송 옵코드는 [동일한 표준](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md#tl-b-schema)에서 가져온 것입니다.
이제 이 튜토리얼의 이전 섹션에서 설명한 대로 트랜잭션을 완료해 보겠습니다. 트랜잭션을 완료하는 데 필요한 올바른 코드는 [GitHub 리포지토리](/개발/스마트컨트랙트/자습서/월렛#소스 코드)에서 찾을 수 있습니다.

제톤을 사용하여 동일한 절차를 완료할 수 있습니다. 이 절차를 수행하려면 제톤 전송에 대한 TL-B [표준](https://github.com/ton-blockchain/TEPs/blob/master/text/0074-jettons-standard.md)을 참조하세요. 특히 이 시점까지는 NFT와 제톤 전송 간에 약간의 차이가 존재합니다.

### 월렛 v3 및 월렛 v4 가져오기 메서드

스마트 콘트랙트는 종종 [GET 메서드](/개발/스마트 콘트랙트/가이드라인/get-methods)를 사용하지만, 블록체인 내부에서 실행되는 것이 아니라 클라이언트 측에서 실행됩니다. GET 메서드는 다양한 용도로 사용되며 스마트 콘트랙트에 다양한 데이터 유형에 대한 접근성을 제공합니다. 예를 들어, NFT 스마트 컨트랙트의 [get_nft_data()] 메서드(https://github.com/ton-blockchain/token-contract/blob/991bdb4925653c51b0b53ab212c53143f71f5476/nft/nft-item.fc#L142-L145)를 사용하면 특정 콘텐츠, 소유자, NFT 수집 정보를 검색할 수 있습니다.

아래에서는 [V3](https://github.com/ton-blockchain/ton/blob/e37583e5e6e8cd0aebf5142ef7d8db282f10692b/crypto/smartcont/wallet3-code.fc#L31-L41) 및 [V4](https://github.com/ton-blockchain/wallet-contract/blob/4111fd9e3313ec17d99ca9b5b1656445b5b49d8f/func/wallet-v4-code.fc#L164-L198)에서 사용되는 GET 메서드의 기본 사항에 대해 자세히 알아보겠습니다. 두 지갑 버전에 모두 동일한 메서드부터 시작하겠습니다:

|                                         방법                                        |                                                                                                                           설명                                                                                                                           |
| :-------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|                           int seqno()                          |                                                                  이 메서드는 현재 seqno를 수신하고 올바른 값으로 트랜잭션을 전송하는 데 필요합니다. 이 튜토리얼의 이전 섹션에서는 이 메서드를 자주 호출했습니다.                                                                  |
| int get_public_key() | 이 메서드는 공개키를 다시 가져오는 데 사용됩니다. get_public_key()는 광범위하게 사용되지는 않으며, 여러 서비스에서 사용할 수 있습니다. 예를 들어, 일부 API 서비스에서는 동일한 공개 키를 가진 여러 지갑을 검색할 수 있습니다. |

이제 V4 지갑에서만 사용하는 방법으로 이동해 보겠습니다:

|                                                                방법                                                                |                                                                        설명                                                                        |
| :------------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------: |
|                        int get_subwallet_id()                       |                튜토리얼 앞부분에서 이를 고려했습니다. 이 메서드를 사용하면 subwallet_id를 다시 가져올 수 있습니다.               |
| int is_plugin_installed(int wc, int addr_hash) | 플러그인이 설치되었는지 알려주세요. 이 메서드를 호출하려면 [workchain](/학습/오버뷰/톤블록체인#워크체인-블록체인-with-your-own-rules)과 플러그인 주소 해시를 전달해야 합니다. |
|                         튜플 get_plugin_list()                        |                                                    이 메서드는 설치된 플러그인의 주소를 반환합니다.                                                   |

get_public_key`와 `is_plugin_installed\` 메서드를 고려해 보겠습니다. 이 두 메서드는 처음에는 256비트 데이터에서 공개 키를 가져와야 하고, 그 후에는 슬라이스와 다양한 유형의 데이터를 GET 메서드에 전달하는 방법을 배워야 하기 때문에 선택했습니다. 이는 이러한 메서드를 올바르게 사용하는 방법을 배우는 데 매우 유용합니다.

먼저 요청을 보낼 수 있는 클라이언트가 필요합니다. 따라서 특정 지갑 주소([EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF](https://tonscan.org/address/EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF))를 예로 들어보겠습니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { TonClient } from '@ton/ton';
import { Address } from '@ton/core';

const client = new TonClient({
    endpoint: "https://toncenter.com/api/v2/jsonRPC",
    apiKey: "put your api key" // you can get an api key from @tonapibot bot in Telegram
});

const walletAddress = Address.parse("EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF"); // my wallet address as an example
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "context"
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/liteclient"
  "github.com/xssnick/tonutils-go/ton"
  "log"
)

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection)

block, err := client.CurrentMasterchainInfo(context.Background()) // get current block, we will need it in requests to LiteServer
if err != nil {
  log.Fatalln("CurrentMasterchainInfo err:", err.Error())
  return
}

walletAddress := address.MustParseAddr("EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF") // my wallet address as an example
```

</TabItem>
</Tabs>

이제 GET 메서드 지갑을 호출해야 합니다.

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
// I always call runMethodWithError instead of runMethod to be able to check the exit_code of the called method. 
let getResult = await client.runMethodWithError(walletAddress, "get_public_key"); // run get_public_key GET Method
const publicKeyUInt = getResult.stack.readBigNumber(); // read answer that contains uint256
const publicKey = publicKeyUInt.toString(16); // get hex string from bigint (uint256)
console.log(publicKey)
```

</TabItem>
<TabItem value="go" label="Golang">

```go
getResult, err := client.RunGetMethod(context.Background(), block, walletAddress, "get_public_key") // run get_public_key GET Method
if err != nil {
	log.Fatalln("RunGetMethod err:", err.Error())
	return
}

// We have a response as an array with values and should specify the index when reading it
// In the case of get_public_key, we have only one returned value that is stored at 0 index
publicKeyUInt := getResult.MustInt(0) // read answer that contains uint256
publicKey := publicKeyUInt.Text(16)   // get hex string from bigint (uint256)
log.Println(publicKey)
```

</TabItem>
</Tabs>

호출이 성공적으로 완료되면 최종 결과는 매우 큰 256비트 숫자가 되며, 이를 16진수로 변환해야 합니다. 위에서 제공한 지갑 주소의 결과 16진수 문자열은 다음과 같습니다: `430db39b13cf3cb76bfa818b6b13417b82be2c6c389170fbe06795c71996b1f8`.
다음으로, [TonAPI](https://tonapi.io/swagger-ui) (/v1/wallet/findByPubkey 메서드)를 활용하여 얻은 16진수를 시스템에 입력하면 답변 내 배열의 첫 번째 요소가 내 지갑을 식별한다는 것을 즉시 알 수 있습니다.

그런 다음 `is_plugin_installed` 메서드로 전환합니다. 예를 들어, 앞서 사용한 지갑([EQAM7M--HGyfxlErAIUODrxBA3yj5roBeYiTuy6BHgJ3Sx8k](https://tonscan.org/address/EQAM7M--HGyfxlErAIUODrxBA3yj5roBeYiTuy6BHgJ3Sx8k))과 플러그인([EQBTKTis-SWYdupy99ozeOvnEBu8LRrQP_N9qwOTSAy3sQSZ](https://tonscan.org/address/EQBTKTis-SWYdupy99ozeOvnEBu8LRrQP_N9qwOTSAy3sQSZ)) 지갑을 다시 사용해보도록 하죠:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
const oldWalletAddress = Address.parse("EQAM7M--HGyfxlErAIUODrxBA3yj5roBeYiTuy6BHgJ3Sx8k"); // my old wallet address
const subscriptionAddress = Address.parseFriendly("EQBTKTis-SWYdupy99ozeOvnEBu8LRrQP_N9qwOTSAy3sQSZ"); // subscription plugin address which is already installed on the wallet
```

</TabItem>
<TabItem value="go" label="Golang">

```go
oldWalletAddress := address.MustParseAddr("EQAM7M--HGyfxlErAIUODrxBA3yj5roBeYiTuy6BHgJ3Sx8k")
subscriptionAddress := address.MustParseAddr("EQBTKTis-SWYdupy99ozeOvnEBu8LRrQP_N9qwOTSAy3sQSZ") // subscription plugin address which is already installed on the wallet
```

</TabItem>
</Tabs>

이제 플러그인의 해시 주소를 검색하여 주소를 숫자로 변환하고 GET 메서드로 전송할 수 있도록 해야 합니다.

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
const hash = BigInt(`0x${subscriptionAddress.address.hash.toString("hex")}`) ;

getResult = await client.runMethodWithError(oldWalletAddress, "is_plugin_installed", 
[
    {type: "int", value: BigInt("0")}, // pass workchain as int
    {type: "int", value: hash} // pass plugin address hash as int
]);
console.log(getResult.stack.readNumber()); // -1
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "math/big"
)

hash := big.NewInt(0).SetBytes(subscriptionAddress.Data())
// runGetMethod will automatically identify types of passed values
getResult, err = client.RunGetMethod(context.Background(), block, oldWalletAddress,
  "is_plugin_installed",
  0,    // pass workchain
  hash) // pass plugin address
if err != nil {
  log.Fatalln("RunGetMethod err:", err.Error())
  return
}

log.Println(getResult.MustInt(0)) // -1
```

</TabItem>
</Tabs>

응답은 결과가 참임을 의미하는 `-1`이어야 합니다. 필요한 경우 슬라이스와 셀을 전송할 수도 있습니다. 빅인트를 사용하는 대신 슬라이스나 셀을 생성하고 적절한 유형을 지정하여 전송하면 충분합니다.

### 월렛을 통한 계약 배포

3장에서는 지갑을 배포했습니다. 이를 위해 처음에는 TON을 전송한 다음 지갑에서 트랜잭션을 전송하여 스마트 컨트랙트를 배포했습니다. 그러나 이 프로세스는 외부 트랜잭션에는 광범위하게 사용되지 않으며 주로 지갑에만 주로 사용됩니다. 컨트랙트를 개발하는 동안 배포 프로세스는 내부 메시지를 전송하여 초기화됩니다.

이를 위해 [세 번째 챕터]에서 사용한 V3R2 지갑 스마트 컨트랙트를 사용합니다(/개발/스마트 컨트랙트/자습서/월렛#컴파일-우리-월렛-코드).
이 경우, 동일한 개인 키를 사용할 때 다른 주소를 검색하는 데 필요한 `subwallet_id`를 `3` 또는 다른 숫자로 설정합니다(변경 가능):

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { beginCell, Cell } from '@ton/core';
import { mnemonicToWalletKey } from '@ton/crypto';

const mnemonicArray = 'put your mnemonic'.split(" ");
const keyPair = await mnemonicToWalletKey(mnemonicArray); // extract private and public keys from mnemonic

const codeCell = Cell.fromBase64('te6ccgEBCAEAhgABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQCW8oMI1xgg0x/TH9MfAvgju/Jj7UTQ0x/TH9P/0VEyuvKhUUS68qIE+QFUEFX5EPKj+ACTINdKltMH1AL7AOgwAaTIyx/LH8v/ye1UAATQMAIBSAYHABe7Oc7UTQ0z8x1wv/gAEbjJftRNDXCx+A==');
const dataCell = beginCell()
    .storeUint(0, 32) // Seqno
    .storeUint(3, 32) // Subwallet ID
    .storeBuffer(keyPair.publicKey) // Public Key
    .endCell();

const stateInit = beginCell()
    .storeBit(0) // No split_depth
    .storeBit(0) // No special
    .storeBit(1) // We have code
    .storeRef(codeCell)
    .storeBit(1) // We have data
    .storeRef(dataCell)
    .storeBit(0) // No library
    .endCell();
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "crypto/ed25519"
  "crypto/hmac"
  "crypto/sha512"
  "encoding/base64"
  "github.com/xssnick/tonutils-go/tvm/cell"
  "golang.org/x/crypto/pbkdf2"
  "strings"
)

mnemonicArray := strings.Split("put your mnemonic", " ")
// The following three lines will extract the private key using the mnemonic phrase.
// We will not go into cryptographic details. In the library tonutils-go, it is all implemented,
// but it immediately returns the finished object of the wallet with the address and ready-made methods.
// So we’ll have to write the lines to get the key separately. Goland IDE will automatically import
// all required libraries (crypto, pbkdf2 and others).
mac := hmac.New(sha512.New, []byte(strings.Join(mnemonicArray, " ")))
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // In TON libraries "TON default seed" is used as salt when getting keys
// 32 is a key len
privateKey := ed25519.NewKeyFromSeed(k)              // get private key
publicKey := privateKey.Public().(ed25519.PublicKey) // get public key from private key

BOCBytes, _ := base64.StdEncoding.DecodeString("te6ccgEBCAEAhgABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQCW8oMI1xgg0x/TH9MfAvgju/Jj7UTQ0x/TH9P/0VEyuvKhUUS68qIE+QFUEFX5EPKj+ACTINdKltMH1AL7AOgwAaTIyx/LH8v/ye1UAATQMAIBSAYHABe7Oc7UTQ0z8x1wv/gAEbjJftRNDXCx+A==")
codeCell, _ := cell.FromBOC(BOCBytes)
dataCell := cell.BeginCell().
  MustStoreUInt(0, 32).           // Seqno
  MustStoreUInt(3, 32).           // Subwallet ID
  MustStoreSlice(publicKey, 256). // Public Key
  EndCell()

stateInit := cell.BeginCell().
  MustStoreBoolBit(false). // No split_depth
  MustStoreBoolBit(false). // No special
  MustStoreBoolBit(true).  // We have code
  MustStoreRef(codeCell).
  MustStoreBoolBit(true). // We have data
  MustStoreRef(dataCell).
  MustStoreBoolBit(false). // No library
  EndCell()
```

</TabItem>
</Tabs>

다음으로 컨트랙트에서 주소를 검색하고 InternalMessage를 빌드하겠습니다. 또한 트랜잭션에 "배포 중..." 코멘트를 추가합니다.

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { Address, toNano } from '@ton/core';

const contractAddress = new Address(0, stateInit.hash()); // get the hash of stateInit to get the address of our smart contract in workchain with ID 0
console.log(`Contract address: ${contractAddress.toString()}`); // Output contract address to console

const internalMessageBody = beginCell()
    .storeUint(0, 32)
    .storeStringTail('Deploying...')
    .endCell();

const internalMessage = beginCell()
    .storeUint(0x10, 6) // no bounce
    .storeAddress(contractAddress)
    .storeCoins(toNano('0.01'))
    .storeUint(0, 1 + 4 + 4 + 64 + 32)
    .storeBit(1) // We have State Init
    .storeBit(1) // We store State Init as a reference
    .storeRef(stateInit) // Store State Init as a reference
    .storeBit(1) // We store Message Body as a reference
    .storeRef(internalMessageBody) // Store Message Body Init as a reference
    .endCell();
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/tlb"
  "log"
)

contractAddress := address.NewAddress(0, 0, stateInit.Hash()) // get the hash of stateInit to get the address of our smart contract in workchain with ID 0
log.Println("Contract address:", contractAddress.String())   // Output contract address to console

internalMessageBody := cell.BeginCell().
  MustStoreUInt(0, 32).
  MustStoreStringSnake("Deploying...").
  EndCell()

internalMessage := cell.BeginCell().
  MustStoreUInt(0x10, 6). // no bounce
  MustStoreAddr(contractAddress).
  MustStoreBigCoins(tlb.MustFromTON("0.01").NanoTON()).
  MustStoreUInt(0, 1+4+4+64+32).
  MustStoreBoolBit(true).            // We have State Init
  MustStoreBoolBit(true).            // We store State Init as a reference
  MustStoreRef(stateInit).           // Store State Init as a reference
  MustStoreBoolBit(true).            // We store Message Body as a reference
  MustStoreRef(internalMessageBody). // Store Message Body Init as a reference
  EndCell()
```

</TabItem>
</Tabs>

:::info
위에서 비트가 지정되었고 stateInit과 internalMessageBody가 참조로 저장되었다는 점에 유의하세요. 링크가 별도로 저장되므로 4 (0b100) + 2 (0b10) + 1 (0b1) -> (4 + 2 + 1, 1 + 4 + 4 + 64 + 32 + 1 + 1 + 1), 즉 (0b111, 1 + 4 + 4 + 64 + 32 + 1 + 1 + 1)을 작성한 다음 두 참조를 저장할 수 있습니다.
:::

다음으로 지갑에 보낼 메시지를 준비하여 전송합니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { TonClient } from '@ton/ton';
import { sign } from '@ton/crypto';

const client = new TonClient({
    endpoint: 'https://toncenter.com/api/v2/jsonRPC',
    apiKey: 'put your api key' // you can get an api key from @tonapibot bot in Telegram
});

const walletMnemonicArray = 'put your mnemonic'.split(' ');
const walletKeyPair = await mnemonicToWalletKey(walletMnemonicArray); // extract private and public keys from mnemonic
const walletAddress = Address.parse('put your wallet address with which you will deploy');
const getMethodResult = await client.runMethod(walletAddress, 'seqno'); // run "seqno" GET method from your wallet contract
const seqno = getMethodResult.stack.readNumber(); // get seqno from response

// transaction for our wallet
const toSign = beginCell()
    .storeUint(698983191, 32) // subwallet_id
    .storeUint(Math.floor(Date.now() / 1e3) + 60, 32) // Transaction expiration time, +60 = 1 minute
    .storeUint(seqno, 32) // store seqno
    // Do not forget that if we use Wallet V4, we need to add .storeUint(0, 8) 
    .storeUint(3, 8)
    .storeRef(internalMessage);

const signature = sign(toSign.endCell().hash(), walletKeyPair.secretKey); // get the hash of our message to wallet smart contract and sign it to get signature
const body = beginCell()
    .storeBuffer(signature) // store signature
    .storeBuilder(toSign) // store our message
    .endCell();

const external = beginCell()
    .storeUint(0b10, 2) // indicate that it is an incoming external transaction
    .storeUint(0, 2) // src -> addr_none
    .storeAddress(walletAddress)
    .storeCoins(0) // Import fee
    .storeBit(0) // We do not have State Init
    .storeBit(1) // We store Message Body as a reference
    .storeRef(body) // Store Message Body as a reference
    .endCell();

console.log(external.toBoc().toString('base64'));
client.sendFile(external.toBoc());
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "context"
  "github.com/xssnick/tonutils-go/liteclient"
  "github.com/xssnick/tonutils-go/tl"
  "github.com/xssnick/tonutils-go/ton"
  "time"
)

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection)

block, err := client.CurrentMasterchainInfo(context.Background()) // get current block, we will need it in requests to LiteServer
if err != nil {
  log.Fatalln("CurrentMasterchainInfo err:", err.Error())
  return
}

walletMnemonicArray := strings.Split("put your mnemonic", " ")
mac = hmac.New(sha512.New, []byte(strings.Join(walletMnemonicArray, " ")))
hash = mac.Sum(nil)
k = pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // In TON libraries "TON default seed" is used as salt when getting keys
// 32 is a key len
walletPrivateKey := ed25519.NewKeyFromSeed(k) // get private key
walletAddress := address.MustParseAddr("put your wallet address with which you will deploy")

getMethodResult, err := client.RunGetMethod(context.Background(), block, walletAddress, "seqno") // run "seqno" GET method from your wallet contract
if err != nil {
  log.Fatalln("RunGetMethod err:", err.Error())
  return
}
seqno := getMethodResult.MustInt(0) // get seqno from response

toSign := cell.BeginCell().
  MustStoreUInt(698983191, 32).                          // subwallet_id | We consider this further
  MustStoreUInt(uint64(time.Now().UTC().Unix()+60), 32). // transaction expiration time, +60 = 1 minute
  MustStoreUInt(seqno.Uint64(), 32).                     // store seqno
  // Do not forget that if we use Wallet V4, we need to add MustStoreUInt(0, 8).
  MustStoreUInt(3, 8).          // store mode of our internal transaction
  MustStoreRef(internalMessage) // store our internalMessage as a reference

signature := ed25519.Sign(walletPrivateKey, toSign.EndCell().Hash()) // get the hash of our message to wallet smart contract and sign it to get signature

body := cell.BeginCell().
  MustStoreSlice(signature, 512). // store signature
  MustStoreBuilder(toSign).       // store our message
  EndCell()

externalMessage := cell.BeginCell().
  MustStoreUInt(0b10, 2).       // ext_in_msg_info$10
  MustStoreUInt(0, 2).          // src -> addr_none
  MustStoreAddr(walletAddress). // Destination address
  MustStoreCoins(0).            // Import Fee
  MustStoreBoolBit(false).      // No State Init
  MustStoreBoolBit(true).       // We store Message Body as a reference
  MustStoreRef(body).           // Store Message Body as a reference
  EndCell()

var resp tl.Serializable
err = client.Client().QueryLiteserver(context.Background(), ton.SendMessage{Body: externalMessage.ToBOCWithFlags(false)}, &resp)

if err != nil {
  log.Fatalln(err.Error())
  return
}
```

</TabItem>
</Tabs>

이것으로 일반 지갑에 대한 작업을 마칩니다. 이 단계에서는 지갑 스마트 컨트랙트와 상호작용하고 트랜잭션을 전송하는 방법을 잘 이해하고 다양한 라이브러리 유형을 사용할 수 있어야 합니다.

## 🔥 고용량 지갑

경우에 따라 메시지당 많은 수의 트랜잭션을 전송해야 할 수도 있습니다. 앞서 언급했듯이 일반 지갑은 하나의 셀에 [최대 4개의 참조](/개발/데이터-포맷/셀-boc#셀)를 저장하여 한 번에 최대 4개의 트랜잭션 전송을 지원합니다. 부하가 높은 지갑은 한 번에 255개의 트랜잭션만 전송할 수 있습니다. 이러한 제한은 블록체인의 구성 설정에서 발신 메시지(작업)의 최대 개수가 255개로 설정되어 있기 때문에 존재합니다.

거래소는 고부하 지갑이 대규모로 사용되는 가장 좋은 예일 것입니다. 바이낸스와 같은 기존 거래소는 사용자 기반이 매우 크기 때문에 단기간에 많은 수의 거래 출금이 처리됩니다. 고부하 지갑은 이러한 출금 요청을 처리하는 데 도움이 됩니다.

### 고부하 지갑 FunC 코드

먼저, [고부하 지갑 스마트 컨트랙트의 코드 구조](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/highload-wallet-v2-code.fc)를 살펴보겠습니다:

```func
() recv_external(slice in_msg) impure {
  var signature = in_msg~load_bits(512); ;; get signature from the message body
  var cs = in_msg;
  var (subwallet_id, query_id) = (cs~load_uint(32), cs~load_uint(64)); ;; get rest values from the message body
  var bound = (now() << 32); ;; bitwise left shift operation
  throw_if(35, query_id < bound); ;; throw an error if transaction has expired
  var ds = get_data().begin_parse();
  var (stored_subwallet, last_cleaned, public_key, old_queries) = (ds~load_uint(32), ds~load_uint(64), ds~load_uint(256), ds~load_dict()); ;; read values from storage
  ds.end_parse(); ;; make sure we do not have anything in ds
  (_, var found?) = old_queries.udict_get?(64, query_id); ;; check if we have already had such a request
  throw_if(32, found?); ;; if yes throw an error
  throw_unless(34, subwallet_id == stored_subwallet);
  throw_unless(35, check_signature(slice_hash(in_msg), signature, public_key));
  var dict = cs~load_dict(); ;; get dictionary with messages
  cs.end_parse(); ;; make sure we do not have anything in cs
  accept_message();
```

> 💡 유용한 링크:
>
> ["문서에서 비트 연산"](/develop/func/stdlib/#dict_get)
>
> ["load_dict()" in docs](/develop/func/stdlib/#load_dict)
>
> ["udict_get?()" in docs](/develop/func/stdlib/#dict_get)

일반 지갑과 몇 가지 차이점이 있습니다. 이제 TON에서 고용량 지갑이 작동하는 방식에 대해 자세히 살펴보겠습니다(서브 지갑은 앞서 살펴본 것처럼 제외).

### 시퀀스 번호 대신 쿼리 ID 사용

앞서 설명한 것처럼 일반 지갑 시퀀스는 트랜잭션이 발생할 때마다 '1'씩 증가합니다. 지갑 시퀀스를 사용하는 동안 이 값이 업데이트될 때까지 기다렸다가 GET 메서드를 사용해 값을 가져와 새 트랜잭션을 전송해야 했습니다.
이 과정에는 상당한 시간이 소요되는데, 이는 고용량 지갑이 설계되지 않은 것입니다(위에서 설명한 것처럼 고용량 지갑은 대량의 트랜잭션을 매우 빠르게 전송하기 위한 것입니다). 따라서 TON의 고부하 지갑은 `query_id`를 사용합니다.

동일한 거래 요청이 이미 존재하는 경우, 이미 처리되었으므로 계약이 수락하지 않습니다:

```func
var (stored_subwallet, last_cleaned, public_key, old_queries) = (ds~load_uint(32), ds~load_uint(64), ds~load_uint(256), ds~load_dict()); ;; read values from storage
ds.end_parse(); ;; make sure we do not have anything in ds
(_, var found?) = old_queries.udict_get?(64, query_id); ;; check if we have already had such a request
throw_if(32, found?); ;; if yes throw an error
```

이렇게 하면 일반 지갑에서 섹노의 역할이었던 반복 거래\*\*로부터 보호받을 수 있습니다.

### 거래 보내기

컨트랙트가 외부 메시지를 수락하면 루프가 시작되고, 이 루프는 사전에 저장된 '슬라이스'를 가져옵니다. 이 슬라이스는 트랜잭션 모드와 트랜잭션 자체를 저장합니다. 새로운 트랜잭션 전송은 사전이 비워질 때까지 진행됩니다.

```func
int i = -1; ;; we write -1 because it will be the smallest value among all dictionary keys
do {
  (i, var cs, var f) = dict.idict_get_next?(16, i); ;; get the key and its corresponding value with the smallest key, which is greater than i
  if (f) { ;; check if any value was found
    var mode = cs~load_uint(8); ;; load transaction mode
    send_raw_message(cs~load_ref(), mode); ;; load transaction itself and send it
  }
} until (~ f); ;; if any value was found continue
```

> 💡 유용한 링크:
>
> ["idict_get_next()" in docs](/develop/func/stdlib/#dict_get_next)

값이 발견되면 `f`는 항상 -1(참)과 같다는 점에 유의하세요. 비트 단위로 `~ -1` 연산은 항상 0의 값을 반환하며, 이는 루프를 계속해야 함을 의미합니다. 동시에 사전이 트랜잭션으로 가득 차면 -1\*\*보다 큰 값(예: 0)으로 \*\*계산을 시작하고 각 트랜잭션마다 값을 1씩 계속 늘려야 합니다. 이러한 구조를 통해 트랜잭션이 올바른 순서로 전송될 수 있습니다.

### 만료된 쿼리 제거하기

일반적으로 [톤의 스마트 컨트랙트는 자체 스토리지 비용을 지불합니다](/개발/방법/수수료-저수준#스토리지-수수료). 즉, 높은 네트워크 트랜잭션 수수료를 방지하기 위해 스마트 콘트랙트가 저장할 수 있는 데이터의 양이 제한됩니다. 시스템의 효율성을 높이기 위해 64초 이상 지난 트랜잭션은 스토리지에서 제거됩니다. 이는 다음과 같이 진행됩니다:

```func
bound -= (64 << 32);   ;; clean up records that have expired more than 64 seconds ago
old_queries~udict_set_builder(64, query_id, begin_cell()); ;; add current query to dictionary
var queries = old_queries; ;; copy dictionary to another variable
do {
  var (old_queries', i, _, f) = old_queries.udict_delete_get_min(64);
  f~touch();
  if (f) { ;; check if any value was found
    f = (i < bound); ;; check if more than 64 seconds have elapsed after expiration
  }
  if (f) { 
    old_queries = old_queries'; ;; if yes save changes in our dictionary
    last_cleaned = i; ;; save last removed query
  }
} until (~ f);
```

> 💡 유용한 링크:
>
> ["udict_delete_get_min()" in docs](/develop/func/stdlib/#dict_delete_get_min)

f`변수와 여러 번 상호작용해야 한다는 점에 유의하세요. TVM은 스택 머신이므로](/learn/tvm-instruction/tvm-overview#tvm-is-a-stack-machine),`f` 변수와 상호작용할 때마다 원하는 변수를 얻기 위해 모든 값을 팝해야 합니다. f~touch()` 연산은 코드 실행을 최적화하기 위해 f 변수를 스택의 맨 위에 배치합니다.

### 비트 단위 연산

이 섹션은 비트 연산에 익숙하지 않은 분들에게는 다소 복잡해 보일 수 있습니다. 스마트 컨트랙트 코드에서 다음 코드 줄을 볼 수 있습니다:

```func
var bound = (now() << 32); ;; bitwise left shift operation
```

결과적으로 오른쪽의 숫자에 32비트가 추가됩니다. 즉, **기존 값이 왼쪽으로 32비트 이동**한다는 뜻입니다. 예를 들어 숫자 3을 2진수 형태로 변환하면 결과는 11이 됩니다. '3 << 2' 연산을 적용하면 11은 2비트 이동합니다. 즉, 문자열의 오른쪽에 2비트가 추가됩니다. 결국 1100은 12가 됩니다.

이 프로세스에 대해 가장 먼저 이해해야 할 것은 `now()` 함수는 결과값이 32비트라는 의미의 uint32 결과를 반환한다는 점을 기억하는 것입니다. 32비트를 왼쪽으로 이동하면 다른 uint32를 위한 공간이 확보되어 올바른 query_id가 생성됩니다. 이렇게 하면 **타임스탬프와 쿼리 아이디를 하나의 변수 내에서 결합**하여 최적화할 수 있습니다.

다음으로 다음 코드 줄을 고려해 보겠습니다:

```func
bound -= (64 << 32); ;; clean up the records that have expired more than 64 seconds ago
```

위에서는 숫자 64를 32비트씩 이동하여 타임스탬프에서 **64초**를 빼는 연산을 수행했습니다. 이렇게 하면 과거의 쿼리 ID를 비교하여 수신된 값보다 작은지 확인할 수 있습니다. 그렇다면 64초 이상 전에 만료된 것입니다:

```func
if (f) { ;; check if any value has been found
  f = (i < bound); ;; check if more than 64 seconds have elapsed after expiration
}
```

이를 더 잘 이해하기 위해 `1625918400`이라는 숫자를 타임스탬프의 예로 들어보겠습니다. 이 숫자의 이진 표현(32비트에 0을 왼쪽으로 더한 것)은 01100000111010011000101111000000 입니다. 32비트 왼쪽 시프트를 수행하면 숫자의 이진 표현 끝에 0이 32개가 됩니다.

이 작업이 완료되면 \*\*어떤 쿼리 아이디(uint32)\*\*도 추가할 수 있습니다. 그런 다음 `64 << 32`를 빼면 64초 전에 동일한 query_id를 가졌던 타임스탬프가 생성됩니다. 이 사실은 다음 계산 `((1625918400 << 32) - (64 << 32)) >> 32`를 수행하여 확인할 수 있습니다. 이렇게 하면 번호의 필요한 부분(타임스탬프)을 비교하는 동시에 쿼리_id가 간섭하지 않습니다.

### 스토리지 업데이트

모든 작업이 완료되면 남은 작업은 저장소에 새 값을 저장하는 것뿐입니다:

```func
  set_data(begin_cell()
    .store_uint(stored_subwallet, 32)
    .store_uint(last_cleaned, 64)
    .store_uint(public_key, 256)
    .store_dict(old_queries)
    .end_cell());
}
```

### GET 메서드

지갑 배포와 트랜잭션 생성에 대해 알아보기 전에 마지막으로 고려해야 할 것은 부하가 높은 지갑 GET 메서드입니다:

|                                         방법                                        |                                                                                                 설명                                                                                                 |
| :-------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|        int processed?(int QUERY_ID)       | 특정 요청이 처리되었는지 여부를 사용자에게 알립니다. 즉, 요청이 처리된 경우 `-1`을 반환하고 처리되지 않은 경우 `0`을 반환합니다. 또한 요청이 오래되어 더 이상 컨트랙트에 저장되지 않아 응답을 알 수 없는 경우 이 메서드는 `1`을 반환할 수 있습니다. |
| int get_public_key() |                                                               공개 키를 다시 생성합니다. 이전에도 이 방법을 고려한 적이 있습니다.                                                              |

마지막_클린을 사용해야 하는 이유를 이해하기 위해 `int processed?(int query_id)` 메서드를 자세히 살펴봅시다:

```func
int processed?(int query_id) method_id {
  var ds = get_data().begin_parse();
  var (_, last_cleaned, _, old_queries) = (ds~load_uint(32), ds~load_uint(64), ds~load_uint(256), ds~load_dict());
  ds.end_parse();
  (_, var found) = old_queries.udict_get?(64, query_id);
  return found ? true : - (query_id <= last_cleaned);
}
```

last_cleaned`는 컨트랙트 저장소와 이전 쿼리 사전에서 검색됩니다. 쿼리가 발견되면 참을 반환하고, 발견되지 않으면 `- (query_id <= last_cleaned)\` 표현식을 반환합니다. 요청을 삭제할 때 최소 타임스탬프로 시작하기 때문에 last_cleaned에는 **가장 높은 타임스탬프를 가진** 마지막으로 삭제된 요청이 포함됩니다.

즉, 메서드에 전달된 query_id가 마지막 last_cleaned 값보다 작으면 컨트랙트에 있었는지 여부를 확인할 수 없습니다. 따라서 `query_id <= last_cleaned`는 -1을 반환하고, 이 표현식 앞에 마이너스가 있으면 답이 1로 변경됩니다. query_id가 last_cleaned 메서드보다 크면 아직 처리되지 않은 것입니다.

### 고부하 지갑 배포

부하가 높은 지갑을 배포하려면 사용자가 사용할 니모닉 키를 미리 생성해야 합니다. 이 튜토리얼의 이전 섹션에서 사용한 것과 동일한 키를 사용할 수 있습니다.

고부하 지갑을 배포하는 데 필요한 프로세스를 시작하려면 [스마트 컨트랙트 코드](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/highload-wallet-v2-code.fc)를 stdlib.fc와 wallet_v3가 있는 동일한 디렉토리에 복사하고 코드 시작 부분에 `#include "stdlib.fc";`를 추가하는 것을 잊지 말아야 합니다. 다음으로 [섹션 3]에서 했던 것처럼 고부하 지갑 코드를 컴파일합니다(/개발/스마트 컨트랙트/튜토리얼/월렛#컴파일-월렛-코드):

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { compileFunc } from '@ton-community/func-js';
import fs from 'fs'
import { Cell } from '@ton/core';

const result = await compileFunc({
    targets: ['highload_wallet.fc'], // targets of your project
    sources: {
        'stdlib.fc': fs.readFileSync('./src/stdlib.fc', { encoding: 'utf-8' }),
        'highload_wallet.fc': fs.readFileSync('./src/highload_wallet.fc', { encoding: 'utf-8' }),
    }
});

if (result.status === 'error') {
console.error(result.message)
return;
}

const codeCell = Cell.fromBoc(Buffer.from(result.codeBoc, 'base64'))[0];

// now we have base64 encoded BOC with compiled code in result.codeBoc
console.log('Code BOC: ' + result.codeBoc);
console.log('\nHash: ' + codeCell.hash().toString('base64')); // get the hash of cell and convert in to base64 encoded string

```

</TabItem>
</Tabs>

결과는 터미널에 다음과 같은 출력으로 표시됩니다:

```text
Code BOC: te6ccgEBCQEA5QABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQHq8oMI1xgg0x/TP/gjqh9TILnyY+1E0NMf0z/T//QE0VNggED0Dm+hMfJgUXO68qIH+QFUEIf5EPKjAvQE0fgAf44WIYAQ9HhvpSCYAtMH1DAB+wCRMuIBs+ZbgyWhyEA0gED0Q4rmMQHIyx8Tyz/L//QAye1UCAAE0DACASAGBwAXvZznaiaGmvmOuF/8AEG+X5dqJoaY+Y6Z/p/5j6AmipEEAgegc30JjJLb/JXdHxQANCCAQPSWb6VsEiCUMFMDud4gkzM2AZJsIeKz

Hash: lJTRzI7fEvBWcaGpugmSEJbrUIEeGSTsZcPGKfu4CBI=
```

위의 결과를 사용하면 다음과 같이 다른 라이브러리 및 언어에서 지갑 코드가 포함된 셀을 검색하기 위해 base64로 인코딩된 출력을 사용할 수 있습니다:

<Tabs groupId="code-examples">
<TabItem value="go" label="Golang">

```go
import (
  "encoding/base64"
  "github.com/xssnick/tonutils-go/tvm/cell"
  "log"
)

base64BOC := "te6ccgEBCQEA5QABFP8A9KQT9LzyyAsBAgEgAgMCAUgEBQHq8oMI1xgg0x/TP/gjqh9TILnyY+1E0NMf0z/T//QE0VNggED0Dm+hMfJgUXO68qIH+QFUEIf5EPKjAvQE0fgAf44WIYAQ9HhvpSCYAtMH1DAB+wCRMuIBs+ZbgyWhyEA0gED0Q4rmMQHIyx8Tyz/L//QAye1UCAAE0DACASAGBwAXvZznaiaGmvmOuF/8AEG+X5dqJoaY+Y6Z/p/5j6AmipEEAgegc30JjJLb/JXdHxQANCCAQPSWb6VsEiCUMFMDud4gkzM2AZJsIeKz" // save our base64 encoded output from compiler to variable
codeCellBytes, _ := base64.StdEncoding.DecodeString(base64BOC) // decode base64 in order to get byte array
codeCell, err := cell.FromBOC(codeCellBytes) // get cell with code from byte array
if err != nil { // check if there is any error
  panic(err) 
}

log.Println("Hash:", base64.StdEncoding.EncodeToString(codeCell.Hash())) // get the hash of our cell, encode it to base64 because it has []byte type and output to the terminal
```

</TabItem>
</Tabs>

이제 초기 데이터로 구성된 셀을 검색하고, 상태 초기화를 빌드하고, 부하가 높은 지갑 주소를 계산해야 합니다. 스마트 컨트랙트 코드를 살펴본 결과, 하위 지갑 아이디, 마지막 청소, 공개 키, 오래된 쿼리가 스토리지에 순차적으로 저장된다는 것을 알 수 있었습니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { Address, beginCell } from '@ton/core';
import { mnemonicToWalletKey } from '@ton/crypto';

const highloadMnemonicArray = 'put your mnemonic that you have generated and saved before'.split(' ');
const highloadKeyPair = await mnemonicToWalletKey(highloadMnemonicArray); // extract private and public keys from mnemonic

const dataCell = beginCell()
    .storeUint(698983191, 32) // Subwallet ID
    .storeUint(0, 64) // Last cleaned
    .storeBuffer(highloadKeyPair.publicKey) // Public Key
    .storeBit(0) // indicate that the dictionary is empty
    .endCell();

const stateInit = beginCell()
    .storeBit(0) // No split_depth
    .storeBit(0) // No special
    .storeBit(1) // We have code
    .storeRef(codeCell)
    .storeBit(1) // We have data
    .storeRef(dataCell)
    .storeBit(0) // No library
    .endCell();

const contractAddress = new Address(0, stateInit.hash()); // get the hash of stateInit to get the address of our smart contract in workchain with ID 0
console.log(`Contract address: ${contractAddress.toString()}`); // Output contract address to console
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "crypto/ed25519"
  "crypto/hmac"
  "crypto/sha512"
  "github.com/xssnick/tonutils-go/address"
  "golang.org/x/crypto/pbkdf2"
  "strings"
)

highloadMnemonicArray := strings.Split("put your mnemonic that you have generated and saved before", " ") // word1 word2 word3
mac := hmac.New(sha512.New, []byte(strings.Join(highloadMnemonicArray, " ")))
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // In TON libraries "TON default seed" is used as salt when getting keys
// 32 is a key len
highloadPrivateKey := ed25519.NewKeyFromSeed(k)                      // get private key
highloadPublicKey := highloadPrivateKey.Public().(ed25519.PublicKey) // get public key from private key

dataCell := cell.BeginCell().
  MustStoreUInt(698983191, 32).           // Subwallet ID
  MustStoreUInt(0, 64).                   // Last cleaned
  MustStoreSlice(highloadPublicKey, 256). // Public Key
  MustStoreBoolBit(false).                // indicate that the dictionary is empty
  EndCell()

stateInit := cell.BeginCell().
  MustStoreBoolBit(false). // No split_depth
  MustStoreBoolBit(false). // No special
  MustStoreBoolBit(true).  // We have code
  MustStoreRef(codeCell).
  MustStoreBoolBit(true). // We have data
  MustStoreRef(dataCell).
  MustStoreBoolBit(false). // No library
  EndCell()

contractAddress := address.NewAddress(0, 0, stateInit.Hash()) // get the hash of stateInit to get the address of our smart contract in workchain with ID 0
log.Println("Contract address:", contractAddress.String())    // Output contract address to console
```

</TabItem>
</Tabs> 

:::caution
위에서 설명한 모든 내용은 컨트랙트 [지갑을 통한 배포](/개발/스마트-컨트랙트/자습서/지갑#컨트랙트-배포-바이-월렛) 섹션과 동일한 단계를 따릅니다. 더 잘 이해하려면 전체 [GitHub 소스 코드](\(https://github.com/aSpite/wallet-tutorial\))를 읽어보시기 바랍니다.
:::

### 고부하 지갑 거래 보내기

이제 여러 개의 메시지를 동시에 보내도록 고부하 지갑을 프로그래밍해 보겠습니다. 예를 들어 가스 요금이 적게 들도록 메시지당 12개의 트랜잭션을 전송한다고 가정해 보겠습니다.

:::info 높은 부하 균형
거래를 완료하려면 계약 잔액이 0.5톤 이상이어야 합니다.
:::

각 메시지에는 코드가 포함된 고유한 코멘트가 포함되며, 대상 주소는 배포한 지갑이 됩니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { Address, beginCell, Cell, toNano } from '@ton/core';

let internalMessages:Cell[] = [];
const walletAddress = Address.parse('put your wallet address from which you deployed high-load wallet');

for (let i = 0; i < 12; i++) {
    const internalMessageBody = beginCell()
        .storeUint(0, 32)
        .storeStringTail(`Hello, TON! #${i}`)
        .endCell();

    const internalMessage = beginCell()
        .storeUint(0x18, 6) // bounce
        .storeAddress(walletAddress)
        .storeCoins(toNano('0.01'))
        .storeUint(0, 1 + 4 + 4 + 64 + 32)
        .storeBit(0) // We do not have State Init
        .storeBit(1) // We store Message Body as a reference
        .storeRef(internalMessageBody) // Store Message Body Init as a reference
        .endCell();

    internalMessages.push(internalMessage);
}
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "fmt"
  "github.com/xssnick/tonutils-go/address"
  "github.com/xssnick/tonutils-go/tlb"
  "github.com/xssnick/tonutils-go/tvm/cell"
)

var internalMessages []*cell.Cell
wallletAddress := address.MustParseAddr("put your wallet address from which you deployed high-load wallet")

for i := 0; i < 12; i++ {
  comment := fmt.Sprintf("Hello, TON! #%d", i)
  internalMessageBody := cell.BeginCell().
    MustStoreUInt(0, 32).
    MustStoreBinarySnake([]byte(comment)).
    EndCell()

  internalMessage := cell.BeginCell().
    MustStoreUInt(0x18, 6). // bounce
    MustStoreAddr(wallletAddress).
    MustStoreBigCoins(tlb.MustFromTON("0.001").NanoTON()).
    MustStoreUInt(0, 1+4+4+64+32).
    MustStoreBoolBit(false). // We do not have State Init
    MustStoreBoolBit(true). // We store Message Body as a reference
    MustStoreRef(internalMessageBody). // Store Message Body Init as a reference
    EndCell()

  messageData := cell.BeginCell().
    MustStoreUInt(3, 8). // transaction mode
    MustStoreRef(internalMessage).
    EndCell()

	internalMessages = append(internalMessages, messageData)
}
```

</TabItem>
</Tabs>

위의 과정을 완료하면 내부 메시지 배열이 생성됩니다. 다음으로 메시지 저장용 사전을 만들고 메시지 본문을 준비하고 서명해야 합니다. 다음과 같이 완료됩니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { Dictionary } from '@ton/core';
import { mnemonicToWalletKey, sign } from '@ton/crypto';
import * as crypto from 'crypto';

const dictionary = Dictionary.empty<number, Cell>(); // create an empty dictionary with the key as a number and the value as a cell
for (let i = 0; i < internalMessages.length; i++) {
    const internalMessage = internalMessages[i]; // get our message from an array
    dictionary.set(i, internalMessage); // save the message in the dictionary
}

const queryID = crypto.randomBytes(4).readUint32BE(); // create a random uint32 number, 4 bytes = 32 bits
const now = Math.floor(Date.now() / 1000); // get current timestamp
const timeout = 120; // timeout for message expiration, 120 seconds = 2 minutes
const finalQueryID = (BigInt(now + timeout) << 32n) + BigInt(queryID); // get our final query_id
console.log(finalQueryID); // print query_id. With this query_id we can call GET method to check if our request has been processed

const toSign = beginCell()
    .storeUint(698983191, 32) // subwallet_id
    .storeUint(finalQueryID, 64)
    // Here we create our own method that will save the 
    // transaction mode and a reference to the transaction
    .storeDict(dictionary, Dictionary.Keys.Int(16), {
        serialize: (src, buidler) => {
            buidler.storeUint(3, 8); // save transaction mode, mode = 3
            buidler.storeRef(src); // save transaction as reference
        },
        // We won't actually use this, but this method 
        // will help to read our dictionary that we saved
        parse: (src) => {
            let cell = beginCell()
                .storeUint(src.loadUint(8), 8)
                .storeRef(src.loadRef())
                .endCell();
            return cell;
        }
    }
);

const highloadMnemonicArray = 'put your high-load wallet mnemonic'.split(' ');
const highloadKeyPair = await mnemonicToWalletKey(highloadMnemonicArray); // extract private and public keys from mnemonic
const highloadWalletAddress = Address.parse('put your high-load wallet address');

const signature = sign(toSign.endCell().hash(), highloadKeyPair.secretKey); // get the hash of our message to wallet smart contract and sign it to get signature
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "crypto/ed25519"
  "crypto/hmac"
  "crypto/sha512"
  "golang.org/x/crypto/pbkdf2"
  "log"
  "math/big"
  "math/rand"
  "strings"
  "time"
)

dictionary := cell.NewDict(16) // create an empty dictionary with the key as a number and the value as a cell
for i := 0; i < len(internalMessages); i++ {
  internalMessage := internalMessages[i]                             // get our message from an array
  err := dictionary.SetIntKey(big.NewInt(int64(i)), internalMessage) // save the message in the dictionary
  if err != nil {
    return
  }
}

queryID := rand.Uint32()
timeout := 120                                                               // timeout for message expiration, 120 seconds = 2 minutes
now := time.Now().Add(time.Duration(timeout)*time.Second).UTC().Unix() << 32 // get current timestamp + timeout
finalQueryID := uint64(now) + uint64(queryID)                                // get our final query_id
log.Println(finalQueryID)                                                    // print query_id. With this query_id we can call GET method to check if our request has been processed

toSign := cell.BeginCell().
  MustStoreUInt(698983191, 32). // subwallet_id
  MustStoreUInt(finalQueryID, 64).
  MustStoreDict(dictionary)

highloadMnemonicArray := strings.Split("put your high-load wallet mnemonic", " ") // word1 word2 word3
mac := hmac.New(sha512.New, []byte(strings.Join(highloadMnemonicArray, " ")))
hash := mac.Sum(nil)
k := pbkdf2.Key(hash, []byte("TON default seed"), 100000, 32, sha512.New) // In TON libraries "TON default seed" is used as salt when getting keys
// 32 is a key len
highloadPrivateKey := ed25519.NewKeyFromSeed(k) // get private key
highloadWalletAddress := address.MustParseAddr("put your high-load wallet address")

signature := ed25519.Sign(highloadPrivateKey, toSign.EndCell().Hash())
```

</TabItem>
</Tabs>

:::note 중요
자바스크립트와 타입스크립트를 사용하는 동안 전송 모드를 사용하지 않고 메시지를 배열로 저장했습니다. 이는 @ton/ton 라이브러리를 사용하는 동안 개발자가 직접 직렬화 및 역직렬화 프로세스를 구현할 것으로 예상되기 때문에 발생합니다. 따라서 트랜잭션 자체를 저장한 후 트랜잭션 모드를 먼저 저장하는 메서드를 전달합니다. 값 메서드에 `Dictionary.Values.Cell()` 사양을 활용하면 모드를 별도로 저장하지 않고 전체 메시지를 셀 참조로 저장합니다.
:::

다음으로 다음 코드를 사용하여 외부 메시지를 생성하고 블록체인으로 전송합니다:

<Tabs groupId="code-examples">
<TabItem value="js" label="JavaScript">

```js
import { TonClient } from '@ton/ton';

const body = beginCell()
    .storeBuffer(signature) // store signature
    .storeBuilder(toSign) // store our message
    .endCell();

const externalMessage = beginCell()
    .storeUint(0b10, 2) // indicate that it is an incoming external transaction
    .storeUint(0, 2) // src -> addr_none
    .storeAddress(highloadWalletAddress)
    .storeCoins(0) // Import fee
    .storeBit(0) // We do not have State Init
    .storeBit(1) // We store Message Body as a reference
    .storeRef(body) // Store Message Body as a reference
    .endCell();

// We do not need a key here as we will be sending 1 request per second
const client = new TonClient({
    endpoint: 'https://toncenter.com/api/v2/jsonRPC',
    // apiKey: 'put your api key' // you can get an api key from @tonapibot bot in Telegram
});

client.sendFile(externalMessage.toBoc());
```

</TabItem>
<TabItem value="go" label="Golang">

```go
import (
  "context"
  "github.com/xssnick/tonutils-go/liteclient"
  "github.com/xssnick/tonutils-go/tl"
  "github.com/xssnick/tonutils-go/ton"
)

body := cell.BeginCell().
  MustStoreSlice(signature, 512). // store signature
  MustStoreBuilder(toSign). // store our message
  EndCell()

externalMessage := cell.BeginCell().
  MustStoreUInt(0b10, 2). // ext_in_msg_info$10
  MustStoreUInt(0, 2). // src -> addr_none
  MustStoreAddr(highloadWalletAddress). // Destination address
  MustStoreCoins(0). // Import Fee
  MustStoreBoolBit(false). // No State Init
  MustStoreBoolBit(true). // We store Message Body as a reference
  MustStoreRef(body). // Store Message Body as a reference
  EndCell()

connection := liteclient.NewConnectionPool()
configUrl := "https://ton-blockchain.github.io/global.config.json"
err := connection.AddConnectionsFromConfigUrl(context.Background(), configUrl)
if err != nil {
  panic(err)
}
client := ton.NewAPIClient(connection)

var resp tl.Serializable
err = client.Client().QueryLiteserver(context.Background(), ton.SendMessage{Body: externalMessage.ToBOCWithFlags(false)}, &resp)

if err != nil {
  log.Fatalln(err.Error())
  return
}
```

</TabItem>
</Tabs>

이 프로세스가 완료되면 지갑을 조회하여 지갑에서 12개의 발신 트랜잭션이 전송된 것을 확인할 수 있습니다. 콘솔에서 처음에 사용한 쿼리 아이디를 사용해 `processed?` GET 메서드를 호출할 수도 있습니다. 이 요청이 올바르게 처리되었다면 `-1`(참)의 결과를 반환합니다.

## 🏁 결론

이 튜토리얼을 통해 TON 블록체인에서 다양한 지갑 유형이 어떻게 작동하는지에 대해 더 잘 이해할 수 있었습니다. 또한 미리 정의된 라이브러리 메서드를 사용하지 않고도 외부 및 내부 메시지를 생성하는 방법을 배울 수 있었습니다.

이를 통해 라이브러리 사용으로부터 독립하고 TON 블록체인의 구조를 보다 심도 있게 이해할 수 있었습니다. 또한 고용량 지갑을 사용하는 방법을 배우고 다양한 데이터 유형과 다양한 작업과 관련된 많은 세부 사항을 분석했습니다.

## 🧩 다음 단계

위에 제공된 문서를 읽는 것은 복잡한 작업이며 TON 플랫폼 전체를 이해하기는 어렵습니다. 하지만 TON을 기반으로 구축하는 데 열정을 가진 분들에게는 좋은 연습이 될 것입니다. 또 다른 제안은 다음 리소스를 참조하여 TON에서 스마트 컨트랙트를 작성하는 방법을 배우기 시작하는 것입니다: [FunC 개요](https://docs.ton.org/develop/func/overview), [모범 사례](https://docs.ton.org/develop/smart-contracts/guidelines), [스마트 컨트랙트 예시](https://docs.ton.org/develop/smart-contracts/examples), [FunC 쿡북](https://docs.ton.org/develop/func/cookbook)

또한 다음 문서를 자세히 숙지하는 것이 좋습니다: [ton.pdf](https://docs.ton.org/ton.pdf) 및 [tblkch.pdf](https://ton.org/tblkch.pdf) 문서.

## 📬 저자 소개

질문, 의견, 제안이 있으시면 [텔레그램](https://t.me/aspite)(@aSpite 또는 @SpiteMoriarty) 또는 [깃허브](https://github.com/aSpite)에서 이 문서 섹션의 작성자에게 연락해 주세요.

## 📖 참고 항목

- 지갑의 소스 코드: [V3](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet3-code.fc), [V4](https://github.com/ton-blockchain/wallet-contract/blob/main/func/wallet-v4-code.fc), [고부하](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/highload-wallet-v2-code.fc)

- 유용한 개념 문서(오래된 정보가 포함될 수 있음): [ton.pdf](https://docs.ton.org/ton.pdf), [tblkch.pdf](https://ton.org/tblkch.pdf), [tvm.pdf](https://ton.org/tvm.pdf)

주요 코드 소스:

- [@톤/톤(JS/TS)](https://github.com/ton-org/ton)
- [@ton/core (JS/TS)](https://github.com/ton-org/ton-core)
- [@ton/crypto (JS/TS)](https://github.com/ton-org/ton-crypto)
- [tonutils-go (GO)](https://github.com/xssnick/tonutils-go).

공식 문서:

- [내부 메시지](/개발/스마트-계약/가이드라인/내부 메시지)

- [외부 메시지](/개발/스마트-계약/가이드라인/외부 메시지)

- [지갑 계약 유형](/참여하기/지갑/계약#지갑-v4)

- [TL-B](/개발/데이터-포맷/tl-b-language)

- [블록체인의 블록체인](https://docs.ton.org/learn/overviews/ton-blockchain)

외부 참조:

- [톤 딥](https://github.com/xssnick/ton-deep-doc)

- [Block.tlb](https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb)

- [톤 단위 표준](https://github.com/ton-blockchain/TEPs)
