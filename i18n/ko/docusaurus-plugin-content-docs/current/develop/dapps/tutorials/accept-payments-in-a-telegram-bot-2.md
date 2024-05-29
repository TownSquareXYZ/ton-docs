---
description: 이 글에서는 TON에서 결제를 수락하는 간단한 텔레그램 봇을 만들어 보겠습니다.
---

# 자체 잔액이 있는 봇

이 글에서는 TON에서 결제를 수락하는 간단한 텔레그램 봇을 만들어 보겠습니다.

## 🦄 어떻게 생겼나요?

봇은 다음과 같이 표시됩니다:

![이미지](/img/tutorials/bot1.png)

### 소스 코드

소스는 GitHub에서 사용할 수 있습니다:

- https://github.com/Gusarich/ton-bot-example

## 📖 학습 내용

방법을 배우게 됩니다:

- Aiogram을 사용하여 Python3에서 텔레그램 봇 만들기
- SQLITE 데이터베이스 작업
- 공개 TON API로 작업

## ✍️ 시작하기 위해 필요한 사항

아직 설치하지 않았다면 [Python](https://www.python.org/)을 설치하세요.

또한 이러한 PyPi 라이브러리가 필요합니다:

- aiogram
- 요청

터미널에서 명령 한 번으로 설치할 수 있습니다.

```bash
pip install aiogram==2.21 requests
```

## 🚀 시작해보자!

네 개의 파일이 들어 있는 봇용 디렉터리를 만듭니다:

- 텔레그램 봇을 실행하는 `bot.py` 프로그램
- config.py\`-config 파일
- sqlite3 데이터베이스와 상호 작용하는 `db.py` 모듈
- `ton.py`- TON에서 결제를 처리하는 모듈

디렉토리는 다음과 같이 표시되어야 합니다:

```
my_bot
├── bot.py
├── config.py
├── db.py
└── ton.py
```

이제 코드 작성을 시작해 보겠습니다!

## 구성

가장 작은 파일인 `config.py`부터 시작하겠습니다. 여기에 몇 가지 매개변수만 설정하면 됩니다.

**config.py**

```python
BOT_TOKEN = 'YOUR BOT TOKEN'
DEPOSIT_ADDRESS = 'YOUR DEPOSIT ADDRESS'
API_KEY = 'YOUR API KEY'
RUN_IN_MAINNET = True  # Switch True/False to change mainnet to testnet

if RUN_IN_MAINNET:
    API_BASE_URL = 'https://toncenter.com'
else:
    API_BASE_URL = 'https://testnet.toncenter.com'
```

여기에서 처음 세 줄의 값을 입력해야 합니다:

- 봇 생성](https://t.me/BotFather) 후 받을 수 있는 텔레그램 봇 토큰이 바로 `BOT_TOKEN`입니다.
- '입금 주소'는 모든 결제를 받을 프로젝트의 지갑 주소입니다. 새 TON 지갑을 생성하고 주소를 복사하면 됩니다.
- 'API_KEY'는 [이 봇](https://t.me/tonapibot)에서 얻을 수 있는 TON 센터의 API 키입니다.

봇을 테스트넷에서 실행할지 메인넷(4번째 라인)에서 실행할지 선택할 수도 있습니다.

이제 구성 파일은 여기까지이니 계속 진행하겠습니다!

## 데이터베이스

이제 봇의 데이터베이스와 함께 작동할 `db.py` 파일을 편집해 보겠습니다.

sqlite3 라이브러리를 가져옵니다.

```python
import sqlite3
```

데이터베이스 연결과 커서를 초기화합니다(`db.sqlite` 대신 파일 이름을 선택할 수 있습니다).

```python
con = sqlite3.connect('db.sqlite')
cur = con.cursor()
```

사용자에 대한 정보(이 경우 잔액)를 저장하려면 사용자 ID와 잔액 행이 있는 'Users'라는 테이블을 만듭니다.

```python
cur.execute('''CREATE TABLE IF NOT EXISTS Users (
                uid INTEGER,
                balance INTEGER
            )''')
con.commit()
```

이제 데이터베이스와 함께 작동할 몇 가지 함수를 선언해야 합니다.

add_user\` 함수는 데이터베이스에 새 사용자를 삽입하는 데 사용됩니다.

```python
def add_user(uid):
    # new user always has balance = 0
    cur.execute(f'INSERT INTO Users VALUES ({uid}, 0)')
    con.commit()
```

check_user\` 함수는 데이터베이스에 사용자가 존재하는지 여부를 확인하는 데 사용됩니다.

```python
def check_user(uid):
    cur.execute(f'SELECT * FROM Users WHERE uid = {uid}')
    user = cur.fetchone()
    if user:
        return True
    return False
```

add_balance\` 함수를 사용하여 사용자의 잔액을 늘릴 수 있습니다.

```python
def add_balance(uid, amount):
    cur.execute(f'UPDATE Users SET balance = balance + {amount} WHERE uid = {uid}')
    con.commit()
```

get_balance\` 함수는 사용자의 잔액을 검색하는 데 사용됩니다.

```python
def get_balance(uid):
    cur.execute(f'SELECT balance FROM Users WHERE uid = {uid}')
    balance = cur.fetchone()[0]
    return balance
```

여기까지 `db.py` 파일에 대한 설명입니다!

이제 봇의 다른 구성 요소에서 이 네 가지 함수를 사용하여 데이터베이스로 작업할 수 있습니다.

## TON 센터 API

톤 파이\` 파일에서 모든 신규 입금을 처리하고, 사용자 잔액을 늘리고, 사용자에게 알리는 함수를 선언할 것입니다.

### getTransactions 메서드

TON 센터 API를 사용하겠습니다. 관련 문서는 여기에서 확인할 수 있습니다:
https://toncenter.com/api/v2/

특정 계정의 최근 거래에 대한 정보를 가져오려면 [getTransactions](https://toncenter.com/api/v2/#/accounts/get_transactions_getTransactions_get) 메서드가 필요합니다.

이 메서드가 입력 매개변수로 받는 항목과 반환하는 내용을 살펴보겠습니다.

필수 입력 필드인 '주소'는 하나뿐이지만, 대가로 받을 트랜잭션 수를 지정하기 위해 '제한' 필드도 필요합니다.

이제 [톤 센터 웹사이트](https://toncenter.com/api/v2/#/accounts/get_transactions_getTransactions_get)에서 기존 지갑 주소로 이 방법을 실행하여 출력 결과를 확인해 보겠습니다.

```json
{
  "ok": true,
  "result": [
    {
      ...
    },
    {
      ...
    }
  ]
}
```

따라서 모든 것이 정상일 때 `ok` 필드는 `true`로 설정되고 `limit` 최신 트랜잭션 목록이 포함된 배열 `result`가 있습니다. 이제 하나의 트랜잭션을 살펴봅시다:

```json
{
    "@type": "raw.transaction",
    "utime": 1666648337,
    "data": "...",
    "transaction_id": {
        "@type": "internal.transactionId",
        "lt": "32294193000003",
        "hash": "ez3LKZq4KCNNLRU/G4YbUweM74D9xg/tWK0NyfuNcxA="
    },
    "fee": "105608",
    "storage_fee": "5608",
    "other_fee": "100000",
    "in_msg": {
        "@type": "raw.message",
        "source": "EQBIhPuWmjT7fP-VomuTWseE8JNWv2q7QYfsVQ1IZwnMk8wL",
        "destination": "EQBKgXCNLPexWhs2L79kiARR1phGH1LwXxRbNsCFF9doc2lN",
        "value": "100000000",
        "fwd_fee": "666672",
        "ihr_fee": "0",
        "created_lt": "32294193000002",
        "body_hash": "tDJM2A4YFee5edKRfQWLML5XIJtb5FLq0jFvDXpv0xI=",
        "msg_data": {
            "@type": "msg.dataText",
            "text": "SGVsbG8sIHdvcmxkIQ=="
        },
        "message": "Hello, world!"
    },
    "out_msgs": []
}
```

정확한 트랜잭션을 식별하는 데 도움이 되는 정보가 '트랜잭션_id' 필드에 저장되어 있음을 알 수 있습니다. 어떤 트랜잭션이 먼저 발생했고 어떤 트랜잭션이 나중에 발생했는지 파악하려면 이 필드에서 `lt` 필드가 필요합니다.

코인 전송에 대한 정보는 `in_msg` 필드에 있습니다. 이 필드에서 `value`와 `message`가 필요합니다.

이제 결제 처리기를 만들 준비가 되었습니다.

### 코드에서 API 요청 보내기

필요한 라이브러리와 이전 파일 두 개를 가져오는 것부터 시작하겠습니다: config.py`와 `db.py\`를 가져옵니다.

```python
import requests
import asyncio

# Aiogram
from aiogram import Bot
from aiogram.types import ParseMode

# We also need config and database here
import config
import db
```

결제 처리를 구현하는 방법에 대해 생각해 보겠습니다.

몇 초마다 API를 호출하여 지갑 주소에 새로운 거래가 있는지 확인할 수 있습니다.

이를 위해서는 마지막으로 처리된 트랜잭션이 무엇인지 알아야 합니다. 가장 간단한 방법은 해당 트랜잭션에 대한 정보를 파일에 저장하고 새 트랜잭션을 처리할 때마다 업데이트하는 것입니다.

트랜잭션에 대한 어떤 정보를 파일에 저장할까요? 사실, 우리는 'lt' 값, 즉 논리적 시간만 저장하면 됩니다.
이 값으로 어떤 트랜잭션을 처리해야 하는지 파악할 수 있습니다.

따라서 새로운 비동기 함수를 정의해야 하며, 이를 'start'라고 부르겠습니다. 이 함수가 비동기여야 하는 이유는 무엇일까요? 텔레그램 봇용 아이오그램 라이브러리도 비동기식이며, 나중에 비동기 함수로 작업하기가 더 쉬워질 것이기 때문입니다.

이것이 바로 '시작' 함수의 모습입니다:

```python
async def start():
    try:
        # Try to load last_lt from file
        with open('last_lt.txt', 'r') as f:
            last_lt = int(f.read())
    except FileNotFoundError:
        # If file not found, set last_lt to 0
        last_lt = 0

    # We need the Bot instance here to send deposit notifications to users
    bot = Bot(token=config.BOT_TOKEN)

    while True:
        # Here we will call API every few seconds and fetch new transactions.
        ...
```

이제 while 루프의 본문을 작성해 보겠습니다. 여기서 몇 초마다 TON Center API를 호출해야 합니다.

```python
while True:
    # 2 Seconds delay between checks
    await asyncio.sleep(2)

    # API call to TON Center that returns last 100 transactions of our wallet
    resp = requests.get(f'{config.API_BASE_URL}/api/v2/getTransactions?'
                        f'address={config.DEPOSIT_ADDRESS}&limit=100&'
                        f'archival=true&api_key={config.API_KEY}').json()

    # If call was not successful, try again
    if not resp['ok']:
        continue
    
    ...
```

요청.get`으로 호출한 후에는 API의 응답을 포함하는 변수 `resp`가 있습니다. 'resp'는 객체이고 `resp['result']\`는 주소에 대한 최근 100개의 트랜잭션이 포함된 목록입니다.

이제 이러한 트랜잭션을 반복하여 새로운 트랜잭션을 찾아보겠습니다.

```python
while True:
    ...

    # Iterating over transactions
    for tx in resp['result']:
        # LT is Logical Time and Hash is hash of our transaction
        lt, hash = int(tx['transaction_id']['lt']), tx['transaction_id']['hash']

        # If this transaction's logical time is lower than our last_lt,
        # we already processed it, so skip it

        if lt <= last_lt:
            continue
        
        # at this moment, `tx` is some new transaction that we haven't processed yet
        ...
```

새 거래는 어떻게 처리하나요? 처리해야 합니다:

- 어떤 사용자가 보냈는지 파악
- 해당 사용자의 잔액 늘리기
- 사용자에게 입금에 대해 알림

이 모든 작업을 수행하는 코드는 다음과 같습니다:

```python
while True:
    ...

    for tx in resp['result']:
        ...
        # at this moment, `tx` is some new transaction that we haven't processed yet

        value = int(tx['in_msg']['value'])
        if value > 0:
            uid = tx['in_msg']['message']

            if not uid.isdigit():
                continue

            uid = int(uid)

            if not db.check_user(uid):
                continue

            db.add_balance(uid, value)

            await bot.send_message(uid, 'Deposit confirmed!\n'
                                    f'*+{value / 1e9:.2f} TON*',
                                    parse_mode=ParseMode.MARKDOWN)
```

이 기능을 살펴보고 그 기능을 이해해 보겠습니다.

코인 전송에 대한 모든 정보는 `tx['in_msg']`에 있습니다. 여기서 'value'와 'message' 필드만 있으면 됩니다.

우선 값이 0보다 큰지 확인하고 0보다 큰 경우에만 계속 진행합니다.

그런 다음 전송에 댓글( `tx['in_msg']['message']`)이 있고 봇의 사용자 ID가 있을 것으로 예상하여 유효한 번호인지, 해당 UID가 데이터베이스에 존재하는지 확인합니다.

이렇게 간단한 확인을 마치면 입금 금액이 포함된 변수 'value'와 입금한 사용자의 ID가 포함된 변수 'uid'가 생깁니다. 따라서 해당 사용자의 계좌에 자금을 추가하고 알림 메시지를 보내기만 하면 됩니다.

또한 값은 기본적으로 나노톤 단위이므로 10억으로 나누어야 합니다.
`{value / 1e9:.2f}`
여기서 값을 `1e9`(10억)로 나누고 소수점 뒤에 두 자리만 남겨 사용자에게 알기 쉬운 형식으로 표시합니다.

잘됐네요! 이제 프로그램은 새로운 거래를 처리하고 사용자에게 입금에 대해 알릴 수 있습니다. 하지만 이전에 사용했던 `lt`를 저장하는 것을 잊지 말아야 합니다. 새로운 트랜잭션이 처리되었으므로 마지막 `lt`를 업데이트해야 합니다.

간단합니다:

```python
while True:
    ...
    for tx in resp['result']:
        ...
        # we have processed this tx

        # lt variable here contains LT of the last processed transaction
        last_lt = lt
        with open('last_lt.txt', 'w') as f:
            f.write(str(last_lt))
```

여기까지가 `ton.py` 파일의 전부입니다!
이제 봇의 3/4이 완성되었으므로 봇 자체에 몇 개의 버튼이 있는 사용자 인터페이스만 만들면 됩니다.

## 텔레그램 봇

### 초기화

bot.py\` 파일을 열고 필요한 모든 모듈을 가져옵니다.

```python
# Logging module
import logging

# Aiogram imports
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ParseMode, ReplyKeyboardMarkup, KeyboardButton, \
                          InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# Local modules to work with the Database and TON Network
import config
import ton
import db
```

나중에 디버깅을 위해 어떤 일이 발생하는지 확인할 수 있도록 프로그램에 로깅을 설정해 보겠습니다.

```python
logging.basicConfig(level=logging.INFO)
```

이제 봇 객체와 해당 디스패처를 Aiogram으로 초기화해야 합니다.

```python
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)
```

여기서는 튜토리얼의 시작 부분에서 만든 설정의 `BOT_TOKEN`을 사용합니다.

봇을 초기화했지만 아직 비어 있습니다. 사용자와의 상호작용을 위해 몇 가지 기능을 추가해야 합니다.

### 메시지 핸들러

#### /start 명령

시작`및`/help`명령 핸들러부터 시작하겠습니다. 이 함수는 사용자가 봇을 처음 실행하거나, 다시 시작하거나,`/help\` 명령을 사용할 때 호출됩니다.

```python
@dp.message_handler(commands=['start', 'help'])
async def welcome_handler(message: types.Message):
    uid = message.from_user.id  # Not neccessary, just to make code shorter

    # If user doesn't exist in database, insert it
    if not db.check_user(uid):
        db.add_user(uid)

    # Keyboard with two main buttons: Deposit and Balance
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(KeyboardButton('Deposit'))
    keyboard.row(KeyboardButton('Balance'))

    # Send welcome text and include the keyboard
    await message.answer('Hi!\nI am example bot '
                         'made for [this article](/develop/dapps/payment-processing/accept-payments-in-a-telegram-bot-2).\n'
                         'My goal is to show how simple it is to receive '
                         'payments in Toncoin with Python.\n\n'
                         'Use keyboard to test my functionality.',
                         reply_markup=keyboard,
                         parse_mode=ParseMode.MARKDOWN)
```

환영 메시지는 무엇이든 원하는 대로 입력할 수 있습니다. 키보드 버튼은 모든 텍스트가 될 수 있지만 이 예제에서는 봇에 가장 명확한 방식으로 '입금'과 '잔액'이라는 레이블이 지정되어 있습니다.

#### 잔액 버튼

이제 사용자는 봇을 시작하고 두 개의 버튼이 있는 키보드를 볼 수 있습니다. 하지만 이 중 하나를 호출한 후에는 사용자가 아무런 응답도 받지 못하는데, 이는 저희가 해당 기능을 만들지 않았기 때문입니다.

이제 잔액을 요청하는 기능을 추가해 보겠습니다.

```python
@dp.message_handler(commands='balance')
@dp.message_handler(Text(equals='balance', ignore_case=True))
async def balance_handler(message: types.Message):
    uid = message.from_user.id

    # Get user balance from database
    # Also don't forget that 1 TON = 1e9 (billion) Nanoton
    user_balance = db.get_balance(uid) / 1e9

    # Format balance and send to user
    await message.answer(f'Your balance: *{user_balance:.2f} TON*',
                         parse_mode=ParseMode.MARKDOWN)
```

매우 간단합니다. 데이터베이스에서 잔액을 가져와서 사용자에게 메시지를 보내기만 하면 됩니다.

#### 입금 버튼

두 번째 '입금' 버튼은 어떻게 되나요? 그 기능은 다음과 같습니다:

```python
@dp.message_handler(commands='deposit')
@dp.message_handler(Text(equals='deposit', ignore_case=True))
async def deposit_handler(message: types.Message):
    uid = message.from_user.id

    # Keyboard with deposit URL
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Deposit',
                                  url=f'ton://transfer/{config.DEPOSIT_ADDRESS}&text={uid}')
    keyboard.add(button)

    # Send text that explains how to make a deposit into bot to user
    await message.answer('It is very easy to top up your balance here.\n'
                         'Simply send any amount of TON to this address:\n\n'
                         f'`{config.DEPOSIT_ADDRESS}`\n\n'
                         f'And include the following comment: `{uid}`\n\n'
                         'You can also deposit by clicking the button below.',
                         reply_markup=keyboard,
                         parse_mode=ParseMode.MARKDOWN)
```

여기서 하는 일도 쉽게 이해할 수 있습니다.

톤 파이\` 파일에서 UID로 댓글을 달아 어떤 사용자가 입금했는지 확인했던 것을 기억하시나요? 이제 여기 봇에서 사용자에게 UID가 포함된 댓글로 트랜잭션을 보내도록 요청해야 합니다.

### 봇 시작

이제 `bot.py`에서 해야 할 일은 봇 자체를 실행하고 `ton.py`에서 `start` 함수를 실행하는 것뿐입니다.

```python
if __name__ == '__main__':
    # Create Aiogram executor for our bot
    ex = executor.Executor(dp)

    # Launch the deposit waiter with our executor
    ex.loop.create_task(ton.start())

    # Launch the bot
    ex.start_polling()
```

이제 봇에 필요한 모든 코드를 작성했습니다. 모든 작업을 올바르게 완료했다면 터미널에서 `python my-bot/bot.py` 명령으로 실행했을 때 작동해야 합니다.

봇이 제대로 작동하지 않는다면 [이 리포지토리의] 코드(https://github.com/Gusarich/ton-bot-example)와 코드를 비교해 보세요.

## 참조

- 톤-풋스텝8](https://github.com/ton-society/ton-footsteps/issues/8)의 일환으로 톤을 위해 제작되었습니다.
- 구사리치([텔레그램 @Gusarich](https://t.me/Gusarich), [깃허브의 구사리치](https://github.com/Gusarich))
