---
description: در این مقاله، ما یک ربات تلگرام ساده برای قبول پرداخت‌ها در TON ایجاد خواهیم کرد.
---

import Feedback from '@site/src/components/Feedback';

# ربات با موجودی خود

در این مقاله، ما یک ربات تلگرام ساده برای قبول پرداخت‌ها در TON ایجاد خواهیم کرد.

## 🦄 ظاهر آن چگونه است

ربات به این صورت خواهد بود:

![image](/img/tutorials/bot1.png)

### کد منبع

The sources are available on GitHub:

- https://github.com/Gusarich/ton-bot-example

## 📖 آنچه یاد خواهید گرفت

شما یاد خواهید گرفت چگونه:

- Create a Telegram bot in Python3 using Aiogram,
- Work with SQLITE databases,
- Work with public TON API.

## ✍️ آنچه برای شروع نیاز دارید

Install [Python](https://www.python.org/) if you haven't already.

Install the required PyPi libraries:

- aiogram,
- requests.

آن‌ها را می‌توانید با یک فرمان در ترمینال نصب کنید.

```bash
pip install aiogram==2.21 requests
```

## 🚀 بیایید شروع کنیم!

یک پوشه برای ربات خود بسازید که چهار فایل در آن قرار دارد:

- `bot.py`— Program to run the Telegram bot,
- `config.py`— Configuration file,
- `db.py`— Module for interacting with the SQLite database,
- `ton.py`— Module for handling payments in TON.

پوشه باید به این صورت باشد:

```
my_bot
├── bot.py
├── config.py
├── db.py
└── ton.py
```

Now, let’s start coding!

## پیکربندی

We'll begin with `config.py` since it's the smallest file. We just need to set a few parameters in it.

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

در اینجا شما باید مقادیر را در سه خط اول پر کنید:

- `BOT_TOKEN`- Your Telegram bot token [creating a bot](https://t.me/BotFather).
- `DEPOSIT_ADDRESS` - Your project's wallet address for receiving payments. You can create a new TON Wallet and copy its address.
- `API_KEY` - Your API key from TON Center which you can get in [this bot](https://t.me/tonapibot).

You can also choose whether your bot will run on the Testnet or the Mainnet (4th line).

Once these values are set, we can move forward!

## پایگاه‌داده

Now let's edit the `db.py` file to store user balances.

کتابخانه sqlite3 را وارد کنید.

```python
import sqlite3
```

ارتباط با پایگاه‌داده و کرسر را مقداردهی اولیه کنید (شما می‌توانید هر نام فایل دیگری به جای `db.sqlite` برگزینید).

```python
con = sqlite3.connect('db.sqlite')
cur = con.cursor()
```

Create a table called **Users** with `uid` and `balance` columns to store information about users and their balances.

```python
cur.execute('''CREATE TABLE IF NOT EXISTS Users (
                uid INTEGER,
                balance INTEGER
            )''')
con.commit()
```

Define helper functions to interact with the database:

تابع `add_user` برای درج کاربران جدید در پایگاه‌داده استفاده خواهد شد.

```python
def add_user(uid):
    # new user always has balance = 0
    cur.execute(f'INSERT INTO Users VALUES ({uid}, 0)')
    con.commit()
```

تابع `check_user` برای بررسی اینکه آیا کاربر در پایگاه‌داده وجود دارد یا خیر استفاده خواهد شد.

```python
def check_user(uid):
    cur.execute(f'SELECT * FROM Users WHERE uid = {uid}')
    user = cur.fetchone()
    if user:
        return True
    return False
```

تابع `add_balance` برای افزایش موجودی کاربر استفاده خواهد شد.

```python
def add_balance(uid, amount):
    cur.execute(f'UPDATE Users SET balance = balance + {amount} WHERE uid = {uid}')
    con.commit()
```

تابع `get_balance` برای بازیابی موجودی کاربر استفاده خواهد شد.

```python
def get_balance(uid):
    cur.execute(f'SELECT balance FROM Users WHERE uid = {uid}')
    balance = cur.fetchone()[0]
    return balance
```

و این تمام فایل `db.py` است!

Once this file is set up, we can use these functions in other parts of the bot.

## API مرکز ton

در فایل `ton.py` تابعی را اعلام خواهیم کرد که همه واریزهای جدید را پردازش کند، موجودی کاربران را افزایش دهد و به کاربران اطلاع‌رسانی کند.

### متد getTransactions

We'll use the TON Center API. Their documentation is available here:
https://toncenter.com/api/v2/

We need the [getTransactions](https://toncenter.com/api/v2/#/accounts/get_transactions_getTransactions_get) method to retrieve information about the latest transactions of a given account.
Let's review the input parameters this method requires and what it returns.

The only mandatory input field is `address`, but we also need the `limit` field to specify how many transactions we want to retrieve.

Let's test this method on the [TON Center website](https://toncenter.com/api/v2/#/accounts/get_transactions_getTransactions_get) website using any existing wallet address to see what the output looks like.

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

خب، بنابراین، فیلد `ok` وقتی همه‌چیز خوب است به `true` تنظیم شده است، و ما یک مجموعه `result` با لیست آخرین تراکنش‌های `limit` داریم. اکنون بیایید به یک تراکنش منفرد نگاه کنیم:

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

We can see that the key details for identifying a specific transaction are stored in the `transaction_id` field. We need the `lt` field from this to determine the chronological order of transactions.

Now, we're ready to create a payment handler.

### ارسال درخواست‌های API از کد

Let's start by importing the required libraries along with the `config.py` and `db.py` files.

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

Let's explore how payment processing can be implemented.

We can call the API every few seconds to check if new transactions have been received in our wallet.

To do this, we need to track the last processed transaction. The simplest approach is to save this transaction’s details in a file and update it every time a new transaction is processed.

What information should we store? We only need the `lt` (logical time) value, which will allow us to determine which transactions need to be processed.

Next, we define an asynchronous function called `start`. Why async? Because the Aiogram library for Telegram bots is asynchronous, making it easier to work with async functions.

تابع `start` ما باید به این شکل باشد:

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

Within the `while` loop, we need to call the TON Center API every few seconds.

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

After making a `requests.get` call, the response is stored in the `resp` variable. The resp object contains a result list with the 100 most recent transactions for our address.

Now, we iterate through these transactions and identify the new ones.

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

How to process a new transaction? We need to:

- Identify which user sent the transaction,
- Update that user's balance,
- Notify the user about their deposit.

Below is the code that handles this:

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

Let's analyze what it does:

All the information about the coin transfer is in `tx['in_msg']`. We just need the `value` and `message` fields.

First, we check if value is greater than zero—if not, we ignore the transaction.

Next, we verify that the ( `tx['in_msg']['message']` ) field contains a valid user ID from our bot and that the UID exists in our database.

After these checks, we extract the deposit amount `value` and the user ID `uid`. Then, we add the funds to the user’s account and send them a notification.
Also note that value is in nanotons by default, so we need to divide it by 1 billion. We do that in line with notification:
`{value / 1e9:.2f}`
Here we divide the value by `1e9` (1 billion) and leave only two digits after the decimal point to show it to the user in a friendly format.

Once a transaction is processed, we must update the stored `lt` value to reflect the most recent transaction.

این ساده است:

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

و این همه برای فایل `ton.py` است!
ربات ما اکنون ۳/۴ تکمیل شده است؛ ما فقط نیاز داریم که یک رابط کاربری با چند دکمه در خود ربات ایجاد کنیم.

## ربات تلگرام

### راه‌اندازی

Open the `bot.py` file and import all necessary modules.

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

بیایید لاگ‌گیری را به برنامه‌مان اضافه کنیم تا بتوانیم برای دیباگینگ ببینیم که چه اتفاقاتی رخ داده است.

```python
logging.basicConfig(level=logging.INFO)
```

Next, we initialize the bot and dispatcher using Aiogram:

```python
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)
```

Here we use the `BOT_TOKEN` from our config file.

At this point, our bot is initialized but still lacks functionality. We now need to define interaction handlers.

### مدیرهای پیام

#### دستور /start

Let's begin with the `/start` and `/help` commands handlers. This function will be triggered when the user launches the bot for the first time, restarts it, or uses the  `/help` command.

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

The welcome message can be customized to anything you prefer. The keyboard buttons can also be labeled as needed, but in this example, we use the most straightforward labels for our bot: `Deposit` and `Balance`.

#### دکمه تعادل

Once the user starts the bot, they will see a keyboard with two buttons. However, pressing these buttons won't yield any response yet, as we haven't created functions for them.

Let's add a function to check the user's balance.

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

The implementation is simple: we retrieve the balance from the database and send a message displaying it to the user.

#### دکمه واریز

Let's implement the **Deposit** button. Here’s how it works:

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

This step is crucial because, in `ton.py` we identify which user made a deposit by extracting their UID from the transaction comment. Now, within the bot, we must guide the user to include their UID in the transaction comment.

### شروع ربات

The final step in `bot.py` is to launch the bot and also start the `start` function from `ton.py`.

```python
if __name__ == '__main__':
    # Create Aiogram executor for our bot
    ex = executor.Executor(dp)

    # Launch the deposit waiter with our executor
    ex.loop.create_task(ton.start())

    # Launch the bot
    ex.start_polling()
```

At this point, we have written all the necessary code for our bot. If everything is set up correctly, the bot should work when you run the following command in the terminal: `python my-bot/bot.py`.

If the bot does not function as expected, compare your code with the code [from this repository](https://github.com/Gusarich/ton-bot-example) to ensure there are no discrepancies.

## منابع

- ساخته شده برای TON به عنوان بخشی از [ton-footsteps/8](https://github.com/ton-society/ton-footsteps/issues/8)
- [Telegram @Gusarich](https://t.me/Gusarich), [Gusarich on GitHub](https://github.com/Gusarich) - *Gusarich*

<Feedback />

