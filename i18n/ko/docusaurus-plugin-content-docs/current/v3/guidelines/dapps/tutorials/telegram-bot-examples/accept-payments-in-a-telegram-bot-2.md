---
description: 이 글에서는 TON 결제를 수락할 수 있는 간단한 Telegram 봇을 만드는 방법을 소개합니다.
---

# 자체 잔액을 가진 봇

이 글에서는 TON으로 결제를 받는 간단한 텔레그램 봇을 만들어보겠습니다.

## 🦄 어떻게 보이나요

봇은 다음과 같이 보일 것입니다:

![image](/img/tutorials/bot1.png)

### 소스 코드

소스는 GitHub에서 확인할 수 있습니다:

- https://github.com/Gusarich/ton-bot-example

## 📖 배울 내용

다음 내용을 배우게 됩니다:

- Python3에서 Aiogram을 사용하여 텔레그램 봇 만들기
- SQLITE 데이터베이스 다루기
- 공개 TON API 사용하기

## ✍️ 시작하기 전 준비사항

아직 설치하지 않았다면 [Python](https://www.python.org/)을 설치하세요.

또한 다음 PyPi 라이브러리들이 필요합니다:

- aiogram
- requests

터미널에서 다음 명령어로 한 번에 설치할 수 있습니다.

```bash
pip install aiogram==2.21 requests
```

## 🚀 시작하기!

봇을 위한 디렉토리를 만들고 다음 네 개의 파일을 생성합니다:

- `bot.py` - 텔레그램 봇을 실행하는 프로그램
- `config.py` - 설정 파일
- `db.py` - sqlite3 데이터베이스와 상호작용하는 모듈
- `ton.py` - TON에서 결제를 처리하는 모듈

디렉토리는 다음과 같이 보여야 합니다:

```
my_bot
├── bot.py
├── config.py
├── db.py
└── ton.py
```

이제 코드를 작성해봅시다!

## 설정

가장 작은 파일인 `config.py`부터 시작하겠습니다. 몇 가지 파라미터만 설정하면 됩니다.

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

처음 세 줄의 값을 채워넣어야 합니다:

- `BOT_TOKEN`은 [봇 생성](https://t.me/BotFather) 후 받을 수 있는 텔레그램 봇 토큰입니다.
- `DEPOSIT_ADDRESS`는 모든 결제를 받을 프로젝트의 지갑 주소입니다. 새로운 TON Wallet을 만들고 주소를 복사하면 됩니다.
- `API_KEY`는 [이 봇](https://t.me/tonapibot)에서 받을 수 있는 TON Center의 API 키입니다.

봇을 테스트넷이나 메인넷에서 실행할지도 선택할 수 있습니다(4번째 줄).

설정 파일은 이게 전부이니 다음으로 넘어갑시다!

## 데이터베이스

이제 봇의 데이터베이스를 다룰 `db.py` 파일을 수정해봅시다.

sqlite3 라이브러리를 임포트합니다.

```python
import sqlite3
```

데이터베이스 연결과 커서를 초기화합니다(`db.sqlite` 대신 원하는 파일명을 선택할 수 있습니다).

```python
con = sqlite3.connect('db.sqlite')
cur = con.cursor()
```

사용자 정보(이 경우 잔액)를 저장하기 위해 사용자 ID와 잔액 열이 있는 "Users" 테이블을 만듭니다.

```python
cur.execute('''CREATE TABLE IF NOT EXISTS Users (
                uid INTEGER,
                balance INTEGER
            )''')
con.commit()
```

이제 데이터베이스 작업을 위한 몇 가지 함수를 선언해야 합니다.

`add_user` 함수는 새로운 사용자를 데이터베이스에 추가하는 데 사용됩니다.

```python
def add_user(uid):
    # new user always has balance = 0
    cur.execute(f'INSERT INTO Users VALUES ({uid}, 0)')
    con.commit()
```

`check_user` 함수는 사용자가 데이터베이스에 있는지 확인하는 데 사용됩니다.

```python
def check_user(uid):
    cur.execute(f'SELECT * FROM Users WHERE uid = {uid}')
    user = cur.fetchone()
    if user:
        return True
    return False
```

`add_balance` 함수는 사용자의 잔액을 증가시키는 데 사용됩니다.

```python
def add_balance(uid, amount):
    cur.execute(f'UPDATE Users SET balance = balance + {amount} WHERE uid = {uid}')
    con.commit()
```

`get_balance` 함수는 사용자의 잔액을 조회하는 데 사용됩니다.

```python
def get_balance(uid):
    cur.execute(f'SELECT balance FROM Users WHERE uid = {uid}')
    balance = cur.fetchone()[0]
    return balance
```

이게 `db.py` 파일의 전부입니다!

이제 봇의 다른 구성 요소에서 이 네 가지 함수를 사용하여 데이터베이스를 다룰 수 있습니다.

## TON Center API

`ton.py` 파일에서는 모든 새로운 입금을 처리하고, 사용자 잔액을 증가시키고, 사용자에게 알림을 보내는 함수를 선언할 것입니다.

### getTransactions 메소드

TON Center API를 사용할 것입니다. 문서는 여기서 확인할 수 있습니다:
https://toncenter.com/api/v2/

주어진 계정의 최근 거래 정보를 얻기 위해 [getTransactions](https://toncenter.com/api/v2/#/accounts/get_transactions_getTransactions_get) 메소드가 필요합니다.

이 메소드가 어떤 입력 파라미터를 받고 무엇을 반환하는지 살펴봅시다.

`address` 필드만 필수이지만, 반환받을 거래 수를 지정하기 위해 `limit` 필드도 필요합니다.

이제 [TON Center 웹사이트](https://toncenter.com/api/v2/#/accounts/get_transactions_getTransactions_get)에서 이 메소드를 실존하는 지갑 주소로 실행해보고 출력에서 무엇을 얻어야 하는지 이해해봅시다.

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

모든 것이 정상이면 `ok` 필드가 `true`로 설정되고, `limit` 개수만큼의 최근 거래 목록이 있는 `result` 배열이 있습니다. 이제 단일 거래를 살펴봅시다:

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

정확한 거래를 식별하는 데 도움이 되는 정보는 `transaction_id` 필드에 저장되어 있습니다. 어떤 거래가 더 일찍 발생했고 어떤 거래가 더 늦게 발생했는지 이해하기 위해 `lt` 필드가 필요합니다.

코인 전송에 대한 정보는 `in_msg` 필드에 있습니다. 여기서 `value`와 `message`가 필요합니다.

이제 결제 핸들러를 만들 준비가 되었습니다.

### 코드에서 API 요청 보내기

먼저 필요한 라이브러리와 이전에 만든 두 파일인 `config.py`와 `db.py`를 임포트합니다.

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

결제 처리를 어떻게 구현할 수 있을지 생각해봅시다.

몇 초마다 API를 호출하여 우리 지갑 주소로 새로운 거래가 있는지 확인할 수 있습니다.

이를 위해서는 마지막으로 처리된 거래가 무엇인지 알아야 합니다. 가장 간단한 방법은 해당 거래에 대한 정보를 파일에 저장하고 새로운 거래를 처리할 때마다 업데이트하는 것입니다.

파일에 어떤 거래 정보를 저장할까요? 사실 논리적 시간인 `lt` 값만 저장하면 됩니다.
이 값으로 어떤 거래를 처리해야 하는지 이해할 수 있습니다.

따라서 새로운 비동기 함수를 정의해야 합니다. `start`라고 부르겠습니다. 이 함수가 비동기여야 하는 이유는 무엇일까요? 텔레그램 봇을 위한 Aiogram 라이브러리도 비동기이기 때문에, 나중에 비동기 함수와 작업하기가 더 쉬울 것이기 때문입니다.

우리의 `start` 함수는 다음과 같이 보일 것입니다:

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

이제 while 루프의 본문을 작성해봅시다. 여기서 매 몇 초마다 TON Center API를 호출해야 합니다.

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

`requests.get`으로 호출한 후, API의 응답을 포함하는 `resp` 변수가 있습니다. `resp`는 객체이고 `resp['result']`는 우리 주소의 마지막 100개 거래가 있는 리스트입니다.

이제 이러한 거래들을 반복하면서 새로운 것들을 찾아봅시다.

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

새로운 거래를 어떻게 처리할까요? 다음을 수행해야 합니다:

- 누가 보냈는지 이해하기
- 해당 사용자의 잔액을 증가시키기
- 사용자에게 입금 알림 보내기

다음은 이 모든 것을 수행하는 코드입니다:

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

이것이 무엇을 하는지 이해해봅시다.

코인 전송에 대한 모든 정보는 `tx['in_msg']`에 있습니다. 여기서는 'value'와 'message' 필드만 필요합니다.

먼저 값이 0보다 큰지 확인하고 그런 경우에만 계속합니다.

그런 다음 이체에 우리 봇의 사용자 ID가 포함된 코멘트(`tx['in_msg']['message']`)가 있기를 기대하므로, 유효한 숫자인지와 그 UID가 데이터베이스에 존재하는지 확인합니다.

이러한 간단한 확인 후에, 입금 금액이 있는 `value` 변수와 이 입금을 한 사용자의 ID가 있는 `uid` 변수가 있습니다. 따라서 해당 계정에 자금을 추가하고 알림 메시지를 보낼 수 있습니다.

또한 기본적으로 value는 나노톤 단위라는 점에 유의하세요. 따라서 10억으로 나눠야 합니다. 알림 줄에서 이렇게 합니다:
`{value / 1e9:.2f}`
여기서 값을 `1e9`(10억)로 나누고 소수점 이하 두 자리만 남겨 사용자에게 친숙한 형식으로 보여줍니다.

훌륭합니다! 이제 프로그램이 새로운 거래를 처리하고 사용자에게 입금을 알릴 수 있습니다. 하지만 이전에 사용했던 `lt`를 저장하는 것을 잊지 말아야 합니다. 새로운 거래가 처리되었으므로 마지막 `lt`를 업데이트해야 합니다.

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

이것으로 `ton.py` 파일이 완성되었습니다!
봇의 3/4이 완성되었고, 이제 봇 자체에 몇 개의 버튼이 있는 사용자 인터페이스만 만들면 됩니다.

## 텔레그램 봇

### 초기화

`bot.py` 파일을 열고 필요한 모든 모듈을 임포트합니다.

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

나중에 디버깅을 위해 무슨 일이 일어나는지 볼 수 있도록 프로그램에 로깅을 설정합시다.

```python
logging.basicConfig(level=logging.INFO)
```

이제 Aiogram으로 봇 객체와 디스패처를 초기화해야 합니다.

```python
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)
```

여기서 튜토리얼 시작 부분에서 만든 config의 `BOT_TOKEN`을 사용합니다.

봇을 초기화했지만 아직 비어 있습니다. 사용자와의 상호작용을 위한 함수를 추가해야 합니다.

### 메시지 핸들러

#### /start 명령

`/start`와 `/help` 명령 핸들러부터 시작해봅시다. 이 함수는 사용자가 처음으로 봇을 시작하거나, 재시작하거나, `/help` 명령을 사용할 때 호출됩니다.

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
                         'made for [this article](docs.ton.org/v3/guidelines/dapps/tutorials/telegram-bot-examples/accept-payments-in-a-telegram-bot-2).\n'
                         'My goal is to show how simple it is to receive '
                         'payments in Toncoin with Python.\n\n'
                         'Use keyboard to test my functionality.',
                         reply_markup=keyboard,
                         parse_mode=ParseMode.MARKDOWN)
```

환영 메시지는 원하는 대로 할 수 있습니다. 키보드 버튼도 아무 텍스트나 가능하지만, 이 예제에서는 봇의 기능을 가장 명확하게 보여주는 방식으로 라벨을 붙였습니다: `입금`과 `잔액`.

#### 잔액 버튼

이제 사용자는 봇을 시작하고 두 개의 버튼이 있는 키보드를 볼 수 있습니다. 하지만 이들 중 하나를 호출한 후에는 아무 응답도 받지 못할 것입니다. 아직 그들을 위한 함수를 만들지 않았기 때문입니다.

그래서 잔액을 요청하는 함수를 추가해봅시다.

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

그리고 두 번째 `입금` 버튼은 어떨까요? 여기 그것을 위한 함수가 있습니다:

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

여기서 하는 일도 이해하기 쉽습니다.

`ton.py` 파일에서 UID로 코멘트를 달아 어떤 사용자가 입금했는지 확인했던 것을 기억하시나요? 이제 여기 봇에서는 사용자에게 자신의 UID가 포함된 코멘트와 함께 거래를 보내달라고 요청해야 합니다.

### 봇 시작

이제 `bot.py`에서 해야 할 일은 봇 자체를 실행하고 `ton.py`의 `start` 함수도 실행하는 것뿐입니다.

```python
if __name__ == '__main__':
    # Create Aiogram executor for our bot
    ex = executor.Executor(dp)

    # Launch the deposit waiter with our executor
    ex.loop.create_task(ton.start())

    # Launch the bot
    ex.start_polling()
```

이 시점에서 봇에 필요한 모든 코드를 작성했습니다. 모든 것을 올바르게 했다면 터미널에서 `python my-bot/bot.py` 명령으로 실행했을 때 작동해야 합니다.

봇이 제대로 작동하지 않는다면, [이 저장소](https://github.com/Gusarich/ton-bot-example)의 코드와 비교해보세요.

## 참고자료

- [ton-footsteps/8](https://github.com/ton-society/ton-footsteps/issues/8)의 일부로 TON을 위해 만들어짐
- 작성자: Gusarich ([텔레그램 @Gusarich](https://t.me/Gusarich), [GitHub Gusarich](https://github.com/Gusarich))
