---
description: 튜토리얼이 끝나면 TON에서 직접 제품에 대한 결제를 수락할 수 있는 멋진 봇을 작성하게 됩니다.
---

# 만두 판매용 봇

이 글에서는 TON에서 결제를 수락하는 간단한 텔레그램 봇을 만들어 보겠습니다.

## 🦄 어떻게 생겼나요?

튜토리얼이 끝나면 TON에서 직접 제품에 대한 결제를 수락할 수 있는 멋진 봇을 작성하게 됩니다.

봇은 다음과 같이 표시됩니다:

![봇 미리보기](/img/tutorials/js-bot-preview.jpg)

## 📖 학습 내용

방법을 배우게 됩니다:

- grammY를 사용하여 NodeJS에서 텔레그램 봇 만들기
- 공개 TON 센터 API로 작업

> 왜 grammY를 사용하나요?
> grammY는 JS/TS/Deno에서 텔레그램 봇을 편안하고 빠르게 개발할 수 있는 현대적이고 젊고 높은 수준의 프레임워크이며, 이 외에도 훌륭한 [문서](https://grammy.dev)와 항상 도움을 줄 수 있는 활발한 커뮤니티가 있기 때문입니다.

## ✍️ 시작하기 위해 필요한 사항

아직 설치하지 않았다면 [NodeJS](https://nodejs.org/en/download/)를 설치하세요.

또한 이러한 라이브러리가 필요합니다:

- grammy
- 톤
- dotenv

터미널에서 명령 한 번으로 설치할 수 있습니다.

```bash npm2yarn
npm install ton dotenv grammy @grammyjs/conversations
```

## 🚀 시작해보자!

프로젝트의 구조는 다음과 같습니다:

```
src
    ├── bot
        ├── start.js
        ├── payment.js
    ├── services 
        ├── ton.js
    ├── app.js
.env
```

- 봇/시작.js`&`봇/결제.js\` - 텔레그램 봇용 핸들러가 있는 파일입니다.
- `src/ton.js` - TON과 관련된 비즈니스 로직이 포함된 파일입니다.
- `app.js` - 봇 초기화 및 실행을 위한 파일

이제 코드 작성을 시작해 보겠습니다!

## 구성

.env\`부터 시작하겠습니다. 여기에 몇 가지 매개변수를 설정하기만 하면 됩니다.

**.env**

```
BOT_TOKEN=
TONCENTER_TOKEN=
NETWORK=
OWNER_WALLET= 
```

여기에서 처음 네 줄의 값을 입력해야 합니다:

- 봇 생성](https://t.me/BotFather) 후 받을 수 있는 텔레그램 봇 토큰이 바로 `BOT_TOKEN`입니다.
- '소유자 지갑'은 모든 결제를 수락할 프로젝트의 지갑 주소입니다. 새 TON 지갑을 생성하고 주소를 복사하면 됩니다.
- 'API_KEY'는 메인넷과 테스트넷의 경우 각각 [@tonapibot](https://t.me/tonapibot)/[@tontestnetapibot](https://t.me/tontestnetapibot)에서 받을 수 있는 TON 센터의 API 키입니다.
- '네트워크'는 봇이 어떤 네트워크(테스트넷 또는 메인넷)에서 실행될지에 관한 것입니다.

설정 파일은 여기까지 했으니 이제 계속 진행하겠습니다!

## TON 센터 API

src/services/ton.py\` 파일에서 트랜잭션의 존재를 확인하고 결제를 위해 지갑 애플리케이션으로 빠르게 전환할 수 있는 링크를 생성하는 함수를 선언할 것입니다.

### 최신 지갑 거래 가져오기

우리의 임무는 특정 지갑에서 필요한 트랜잭션의 가용성을 확인하는 것입니다.

이렇게 해결하겠습니다:

1. 마지막으로 수신된 거래를 지갑으로 받게 됩니다. 왜 저희 지갑인가요? 이 경우 사용자의 지갑 주소가 무엇인지 걱정할 필요가 없고, 지갑인지 확인할 필요도 없으며, 이 지갑을 어디에 보관할 필요도 없습니다.
2. 들어오는 트랜잭션만 정렬하여 남겨두기
3. 모든 거래를 살펴보고 매번 댓글과 금액이 우리가 가지고있는 데이터와 동일한 지 확인하겠습니다.
4. 문제 해결을 축하합니다🎉

#### 최신 거래 가져오기

톤 센터 API를 사용하는 경우 [문서](https://toncenter.com/api/v2/)를 참조하여 문제를 이상적으로 해결하는 방법인 [getTransactions](https://toncenter.com/api/v2/#/accounts/get_transactions_getTransactions_get)를 찾을 수 있습니다.

결제를 수락하기 위한 지갑 주소인 매개변수 하나만으로도 트랜잭션을 받을 수 있지만, 트랜잭션 발행을 100개로 제한하기 위해 제한 매개변수도 사용할 것입니다.

EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N\` 주소로 테스트 요청을 호출해 보겠습니다(참고로 이 주소는 TON 재단 주소입니다).

```bash
curl -X 'GET' \
  'https://toncenter.com/api/v2/getTransactions?address=EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N&limit=100' \
  -H 'accept: application/json'
```

이제 ["결과"]에 트랜잭션 목록이 생겼으니 이제 트랜잭션 하나를 자세히 살펴봅시다.

```json
{
      "@type": "raw.transaction",
      "utime": 1667148685,
      "data": "*data here*",
      "transaction_id": {
        "@type": "internal.transactionId",
        "lt": "32450206000003",
        "hash": "rBHOq/T3SoqWta8IXL8THxYqTi2tOkBB8+9NK0uKWok="
      },
      "fee": "106508",
      "storage_fee": "6508",
      "other_fee": "100000",
      "in_msg": {
        "@type": "raw.message",
        "source": "EQA0i8-CdGnF_DhUHHf92R1ONH6sIA9vLZ_WLcCIhfBBXwtG",
        "destination": "EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N",
        "value": "1000000",
        "fwd_fee": "666672",
        "ihr_fee": "0",
        "created_lt": "32450206000002",
        "body_hash": "Fl+2CzHNgilBE4RKhfysLU8VL8ZxYWciCRDva2E19QQ=",
        "msg_data": {
          "@type": "msg.dataText",
          "text": "aGVsbG8g8J+Riw=="
        },
        "message": "hello 👋"
      },
      "out_msgs": []
    }
```

이 json 파일에서 유용한 몇 가지 정보를 파악할 수 있습니다:

- "out_msgs" 필드가 비어 있으므로 이것은 들어오는 트랜잭션입니다.
- 거래, 발신자, 거래 금액에 대한 댓글도 확인할 수 있습니다.

이제 트랜잭션 검사기를 만들 준비가 되었습니다.

### TON과 함께 작업하기

필요한 라이브러리 TON을 가져오는 것부터 시작하겠습니다.

```js
import { HttpApi, fromNano, toNano } from "ton";
```

사용자가 필요한 트랜잭션을 전송했는지 확인하는 방법에 대해 생각해 보겠습니다.

모든 것이 아주 간단합니다. 지갑으로 들어오는 트랜잭션만 정렬한 다음 마지막 100개의 트랜잭션을 살펴보고 댓글과 금액이 같은 트랜잭션이 발견되면 필요한 트랜잭션을 찾은 것입니다!

TON으로 편리하게 작업할 수 있도록 http 클라이언트 초기화부터 시작하겠습니다.

```js
export async function verifyTransactionExistance(toWallet, amount, comment) {
  const endpoint =
    process.env.NETWORK === "mainnet"
      ? "https://toncenter.com/api/v2/jsonRPC"
      : "https://testnet.toncenter.com/api/v2/jsonRPC";
  const httpClient = new HttpApi(
    endpoint,
    {},
    { apiKey: process.env.TONCENTER_TOKEN }
  );
```

여기서는 구성에서 선택한 네트워크에 따라 엔드포인트 URL을 생성하기만 하면 됩니다. 그런 다음 http 클라이언트를 초기화합니다.

이제 소유자의 지갑에서 마지막 100개의 트랜잭션을 가져올 수 있습니다.

```js
const transactions = await httpClient.getTransactions(toWallet, {
    limit: 100,
  });
```

로 설정하고 필터링하여 들어오는 트랜잭션만 남깁니다(트랜잭션의 out_msgs가 비어 있으면 그대로 둡니다).

```js
let incomingTransactions = transactions.filter(
    (tx) => Object.keys(tx.out_msgs).length === 0
  );
```

이제 모든 트랜잭션을 살펴보고 코멘트와 트랜잭션 값이 일치하면 참을 반환하면 됩니다.

```js
  for (let i = 0; i < incomingTransactions.length; i++) {
    let tx = incomingTransactions[i];
    // Skip the transaction if there is no comment in it
    if (!tx.in_msg.msg_data.text) {
      continue;
    }

    // Convert transaction value from nano
    let txValue = fromNano(tx.in_msg.value);
    // Get transaction comment
    let txComment = tx.in_msg.message

    if (txComment === comment && txValue === value.toString()) {
      return true;
    }
  }

  return false;
```

값은 기본적으로 나노톤 단위이므로 10억으로 나누거나 TON 라이브러리의 `fromNano` 메서드를 사용할 수 있습니다.
이상 `verifyTransactionExistance` 함수에 대한 설명이 끝났습니다!

이제 결제를 위해 지갑 애플리케이션으로 빠르게 전환할 수 있는 링크를 생성하는 기능을 만들 수 있습니다.

```js
export function generatePaymentLink(toWallet, amount, comment, app) {
  if (app === "tonhub") {
    return `https://tonhub.com/transfer/${toWallet}?amount=${toNano(
      amount
    )}&text=${comment}`;
  }
  return `https://app.tonkeeper.com/transfer/${toWallet}?amount=${toNano(
    amount
  )}&text=${comment}`;
}
```

URL에서 트랜잭션 매개변수를 대체하기만 하면 됩니다. 트랜잭션의 가치를 나노로 전송하는 것을 잊지 마세요.

## 텔레그램 봇

### 초기화

app.js\` 파일을 열고 필요한 모든 핸들러와 모듈을 가져옵니다.

```js
import dotenv from "dotenv";
import { Bot, session } from "grammy";
import { conversations, createConversation } from "@grammyjs/conversations";

import {
  startPaymentProcess,
  checkTransaction,
} from "./bot/handlers/payment.js";
import handleStart from "./bot/handlers/start.js";
```

.env 파일에서 설정한 환경 변수로 편리하게 작업할 수 있도록 dotenv 모듈을 설정해 보겠습니다.

```js
dotenv.config();
```

그런 다음 프로젝트를 실행할 함수를 만듭니다. 오류가 발생해도 봇이 멈추지 않도록 하기 위해 다음 코드를 추가합니다.

```js
async function runApp() {
  console.log("Starting app...");

  // Handler of all errors, in order to prevent the bot from stopping
  process.on("uncaughtException", function (exception) {
    console.log(exception);
  });
```

이제 봇과 필요한 플러그인을 초기화합니다.

```js
  // Initialize the bot
  const bot = new Bot(process.env.BOT_TOKEN);

  // Set the initial data of our session
  bot.use(session({ initial: () => ({ amount: 0, comment: "" }) }));
  // Install the conversation plugin
  bot.use(conversations());

  bot.use(createConversation(startPaymentProcess));
```

여기서는 튜토리얼의 시작 부분에서 만든 설정의 `BOT_TOKEN`을 사용합니다.

봇을 초기화했지만 아직 비어 있습니다. 사용자와의 상호작용을 위해 몇 가지 기능을 추가해야 합니다.

```js
  // Register all handelrs
  bot.command("start", handleStart);
  bot.callbackQuery("buy", async (ctx) => {
    await ctx.conversation.enter("startPaymentProcess");
  });
  bot.callbackQuery("check_transaction", checkTransaction);
```

명령/시작에 반응하여 핸들스타트 함수가 실행됩니다. 사용자가 callback_data가 "buy"인 버튼을 클릭하면 바로 위에 등록한 "대화"가 시작됩니다. 그리고 callback_data가 "check_transaction"인 버튼을 클릭하면 checkTransaction 함수가 실행됩니다.

이제 남은 것은 봇을 실행하고 성공적인 실행에 대한 로그를 출력하는 것뿐입니다.

```js
  // Start bot
  await bot.init();
  bot.start();
  console.info(`Bot @${bot.botInfo.username} is up and running`);
```

### 메시지 핸들러

#### /start 명령

시작\` 명령 핸들러부터 시작하겠습니다. 이 함수는 사용자가 봇을 처음 실행하고 봇을 다시 시작할 때 호출됩니다.

```js
import { InlineKeyboard } from "grammy";

export default async function handleStart(ctx) {
  const menu = new InlineKeyboard()
    .text("Buy dumplings🥟", "buy")
    .row()
    .url("Article with a detailed explanation of the bot's work", "/develop/dapps/payment-processing/accept-payments-in-a-telegram-bot-js/");

  await ctx.reply(
    `Hello stranger!
Welcome to the best Dumplings Shop in the world <tg-spoiler>and concurrently an example of accepting payments in TON</tg-spoiler>`,
    { reply_markup: menu, parse_mode: "HTML" }
  );
}
```

여기서는 먼저 문법 모듈에서 인라인 키보드를 가져옵니다. 그런 다음 핸들러에 만두 구매 제안과 이 문서에 대한 링크가 포함된 인라인 키보드를 만듭니다(여기서는 약간의 재귀가 있습니다😁).
.row()는 다음 버튼을 새 줄로 전송하는 것을 의미합니다.
그런 다음 생성 된 키보드와 함께 텍스트 (중요, 메시지에 html 마크 업을 사용하여 장식)가 포함 된 환영 메시지를 보냅니다
환영 메시지는 원하는 모든 것이 될 수 있습니다.

#### 결제 프로세스

항상 그렇듯이 필요한 가져오기로 파일을 시작하겠습니다.

```js
import { InlineKeyboard } from "grammy";

import {
  generatePaymentLink,
  verifyTransactionExistance,
} from "../../services/ton.js";
```

그 후, 특정 버튼을 눌렀을 때 실행하기 위해 app.js에 이미 등록한 startPaymentProcess 핸들러를 생성합니다.

텔레그램에서 인라인 버튼을 클릭하면 회전하는 시계가 나타나고, 이를 제거하기 위해 콜백에 응답합니다.

```js
  await ctx.answerCallbackQuery();
```

그 후 사용자에게 만두 사진을 보내고 구매하려는 만두의 수를 보내달라고 요청해야합니다. 그리고 우리는 그가이 번호를 입력하기를 기다리고 있습니다.

```js
  await ctx.replyWithPhoto(
    "https://telegra.ph/file/bad2fd69547432e16356f.jpg",
    {
      caption:
        "Send the number of portions of yummy dumplings you want buy\nP.S. Current price for 1 portion: 3 TON",
    }
  );

  // Wait until the user enters the number
  const count = await conversation.form.number();
```

이제 주문의 총 금액을 계산하고 임의의 문자열을 생성하여 거래에 댓글을 달고 만두 접미사를 추가하는 데 사용할 것입니다.

```js
  // Get the total cost: multiply the number of portions by the price of the 1 portion
  const amount = count * 3;
  // Generate random comment
  const comment = Math.random().toString(36).substring(2, 8) + "dumplings";
```

그리고 결과 데이터를 세션에 저장하여 다음 핸들러에서 이 데이터를 가져올 수 있도록 합니다.

```js
  conversation.session.amount = amount;
  conversation.session.comment = comment;
```

빠른 결제로 이동할 수 있는 링크를 생성하고 인라인 키보드를 생성합니다.

```js
const tonhubPaymentLink = generatePaymentLink(
    process.env.OWNER_WALLET,
    amount,
    comment,
    "tonhub"
  );
  const tonkeeperPaymentLink = generatePaymentLink(
    process.env.OWNER_WALLET,
    amount,
    comment,
    "tonkeeper"
  );

  const menu = new InlineKeyboard()
    .url("Click to pay in TonHub", tonhubPaymentLink)
    .row()
    .url("Click to pay in Tonkeeper", tonkeeperPaymentLink)
    .row()
    .text(`I sent ${amount} TON`, "check_transaction");
```

그리고 키보드로 메시지를 보내 사용자에게 무작위로 생성된 댓글과 함께 지갑 주소로 트랜잭션을 보내달라고 요청합니다.

```js
  await ctx.reply(
    `
Fine, all you have to do is transfer ${amount} TON to the wallet <code>${process.env.OWNER_WALLET}</code> with the comment <code>${comment}</code>.

<i>WARNING: I am currently working on ${process.env.NETWORK}</i>

P.S. You can conveniently make a transfer by clicking on the appropriate button below and confirm the transaction in the offer`,
    { reply_markup: menu, parse_mode: "HTML" }
  );
}
```

이제 트랜잭션이 있는지 확인하는 핸들러를 생성하기만 하면 됩니다.

```js
export async function checkTransaction(ctx) {
  await ctx.answerCallbackQuery({
    text: "Wait a bit, I need to check the availability of your transaction",
  });

  if (
    await verifyTransactionExistance(
      process.env.OWNER_WALLET,
      ctx.session.amount,
      ctx.session.comment
    )
  ) {
    const menu = new InlineKeyboard().text("Buy more dumplings🥟", "buy");

    await ctx.reply("Thank you so much. Enjoy your meal!", {
      reply_markup: menu,
    });

    // Reset the session data
    ctx.session.amount = 0;
    ctx.session.comment = "";
  } else {
    await ctx.reply("I didn't receive your transaction, wait a bit");
  }
}
```

여기서 우리가 하는 일은 단지 트랜잭션을 확인하고, 트랜잭션이 존재하면 사용자에게 이를 알리고 세션의 데이터를 재설정하는 것뿐입니다.

### 봇 시작

이 명령을 사용하려면 다음과 같이 하세요:

```bash npm2yarn
npm run app
```

봇이 제대로 작동하지 않는다면 [이 저장소의] 코드(https://github.com/coalus/DumplingShopBot)와 코드를 비교해 보세요. 그래도 도움이 되지 않는다면 언제든지 텔레그램으로 저에게 편지를 보내주세요. 제 텔레그램 계정은 아래에서 찾을 수 있습니다.

## 참조

- 톤-발걸음/58](https://github.com/ton-society/ton-footsteps/issues/58)의 일환으로 TON을 위해 제작되었습니다.
- Coalus ([텔레그램 @coalus](https://t.me/coalus), [깃허브의 Coalus](https://github.com/coalus) 제공)
- [봇 소스](https://github.com/coalus/DumplingShopBot)
