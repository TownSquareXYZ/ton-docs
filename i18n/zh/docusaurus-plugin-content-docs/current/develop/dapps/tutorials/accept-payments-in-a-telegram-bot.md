---
description: 在这篇文章中，我们将引导你完成在 Telegram 机器人中接受付款的过程。
---

# 使用 TON 的商店机器人

在这篇文章中，我们将引导你完成在 Telegram 机器人中接受付款的过程。

## 📖 你将学到什么

在这篇文章中，你将学习如何：

- 使用 Python + Aiogram 创建一个 Telegram 机器人
- 使用公开的 TON API（TON Center）
- 使用 SQlite 数据库

最后：通过前面步骤的知识，在 Telegram 机器人中接受付款。

## 📚 在我们开始之前

确保你已经安装了最新版本的 Python，并且已经安装了以下包：

- aiogram
- requests
- sqlite3

## 🚀 我们开始吧！

我们将按照以下顺序操作：

1. 使用 SQlite 数据库
2. 使用公开的 TON API（TON Center）
3. 使用 Python + Aiogram 创建一个 Telegram 机器人
4. 盈利！

让我们在项目目录中创建以下四个文件：

```
telegram-bot
├── config.json
├── main.py
├── api.py
└── db.py
```

## 配置

在 `config.json` 中，我们将存储我们的机器人令牌和我们的公开 TON API 密钥。

```json
{
  "BOT_TOKEN": "你的机器人令牌",
  "MAINNET_API_TOKEN": "你的主网api令牌",
  "TESTNET_API_TOKEN": "你的测试网api令牌",
  "MAINNET_WALLET": "你的主网钱包",
  "TESTNET_WALLET": "你的测试网钱包",
  "WORK_MODE": "testnet"
}
```

在 `config.json` 中，我们决定我们将使用哪个网络：`testnet` 或 `mainnet`。

## 数据库

### 创建数据库

这个示例使用本地 Sqlite 数据库。

创建 `db.py`。

开始使用数据库，我们需要导入 sqlite3 模块和一些用于处理时间的模块。

```python
import sqlite3
import datetime
import pytz
```

- `sqlite3`—用于操作 sqlite 数据库的模块
- `datetime`—用于处理时间的模块
- `pytz`—用于处理时区的模块

接下来，我们需要创建一个数据库的连接和一个用于操作它的游标：

```python
locCon = sqlite3.connect('local.db', check_same_thread=False)
cur = locCon.cursor()
```

如果数据库不存在，将会自动创建。

现在我们可以创建表格了。我们有两个表格。 We have two of them.

#### 交易：

```sql
CREATE TABLE transactions (
    source  VARCHAR (48) NOT NULL,
    hash    VARCHAR (50) UNIQUE
                         NOT NULL,
    value   INTEGER      NOT NULL,
    comment VARCHAR (50)
);
```

- `source`—付款人的钱包地址
- `hash`—交易哈希
- `value`—交易价值
- `comment`—交易备注

#### 用户：

```sql
CREATE TABLE users (
    id         INTEGER       UNIQUE
                             NOT NULL,
    username   VARCHAR (33),
    first_name VARCHAR (300),
    wallet     VARCHAR (50)  DEFAULT none
);
```

- `id`—Telegram 用户 ID
- `username`—Telegram 用户名
- `first_name`—Telegram 用户的名字
- `wallet`—用户钱包地址

在 `users` 表中，我们存储用户 :) 他们的 Telegram ID、@username、
名字和钱包。第一次成功付款时，钱包将被添加到数据库中。 The wallet is added to the database on the first
successful payment.

The `transactions` table stores verified transactions.
To verify a transaction, we need the hash, source, value and comment.

要创建这些表格，我们需要运行以下函数：

```python
cur.execute('''CREATE TABLE IF NOT EXISTS transactions (
    source  VARCHAR (48) NOT NULL,
    hash    VARCHAR (50) UNIQUE
                        NOT NULL,
    value   INTEGER      NOT NULL,
    comment VARCHAR (50)
)''')
locCon.commit()

cur.execute('''CREATE TABLE IF NOT EXISTS users (
    id         INTEGER       UNIQUE
                            NOT NULL,
    username   VARCHAR (33),
    first_name VARCHAR (300),
    wallet     VARCHAR (50)  DEFAULT none
)''')
locCon.commit()
```

如果这些表格还没有被创建，这段代码将会创建它们。

### 使用数据库

Let's analyze the situation:
User made a transaction. How to verify it? 让我们分析一种情况：
用户进行了一笔交易。我们如何验证它？我们如何确保同一笔交易不被二次确认？

交易中有一个 body_hash，通过它我们可以轻松地了解数据库中是否存在该交易。

`transactions` 表存储已验证的交易。
要验证交易，我们需要哈希、来源、值和备注。 我们只添加我们确定的交易到数据库。`check_transaction` 函数检查数据库中是否存在找到的交易。

`add_v_transaction` 将交易添加到交易表。

```python
def add_v_transaction(source, hash, value, comment):
    cur.execute("INSERT INTO transactions (source, hash, value, comment) VALUES (?, ?, ?, ?)",
                (source, hash, value, comment))
    locCon.commit()
```

```python
def check_transaction(hash):
    cur.execute(f"SELECT hash FROM transactions WHERE hash = '{hash}'")
    result = cur.fetchone()
    if result:
        return True
    return False
```

`check_user` 检查用户是否在数据库中，并且如果不在，则添加他。

```python
def check_user(user_id, username, first_name):
    cur.execute(f"SELECT id FROM users WHERE id = '{user_id}'")
    result = cur.fetchone()

    if not result:
        cur.execute("INSERT INTO users (id, username, first_name) VALUES (?, ?, ?)",
                    (user_id, username, first_name))
        locCon.commit()
        return False
    return True
```

The user can store a wallet in the table. It is added with the first successful purchase. 用户可以在表中存储一个钱包。它是在第一次成功购买时添加的。`v_wallet` 函数检查用户是否有关联的钱包。如果有，则返回它。如果没有，则添加。 If there is, then returns it. If not, then adds.

```python
def v_wallet(user_id, wallet):
    cur.execute(f"SELECT wallet FROM users WHERE id = '{user_id}'")
    result = cur.fetchone()
    if result[0] == "none":
        cur.execute(
            f"UPDATE users SET wallet = '{wallet}' WHERE id = '{user_id}'")
        locCon.commit()
        return True
    else:
        return result[0]
```

`get_user_wallet` 简单地返回用户的钱包。

```python
def get_user_wallet(user_id):
    cur.execute(f"SELECT wallet FROM users WHERE id = '{user_id}'")
    result = cur.fetchone()
    return result[0]
```

`get_user_payments` 返回用户的支付列表。
这个函数检查用户是否有钱包。如果有，则返回支付列表。
This function checks if the user has a wallet. If he has, then it returns the payment list.

```python
def get_user_payments(user_id):
    wallet = get_user_wallet(user_id)

    if wallet == "none":
        return "You have no wallet"
    else:
        cur.execute(f"SELECT * FROM transactions WHERE source = '{wallet}'")
        result = cur.fetchall()
        tdict = {}
        tlist = []
        try:
            for transaction in result:
                tdict = {
                    "value": transaction[2],
                    "comment": transaction[3],
                }
                tlist.append(tdict)
            return tlist

        except:
            return False
```

## API

_我们有能力使用一些网络成员提供的第三方 API 与区块链进行交互。通过这些服务，开发者可以跳过运行自己的节点和自定义 API 的步骤。_ With these services, developers can skip the step of running their own node and customizing their API._

### 需要的请求

实际上，我们需要确认用户已经向我们转账了所需金额吗？

我们只需要查看我们钱包的最新进账转账，并在其中找到一笔来自正确地址、正确金额的交易（可能还有一个独特的备注）。
为了所有这一切，TON Center 有一个 `getTransactions` 方法。
For all of this, TON Center has a `getTransactions` method.

### getTransactions

By default, if we apply it, we will get the last 10 transactions. However, we can also indicate that we need more, but this will slightly increase the time of a response. And, most likely, you do not need so much.

If you want more, then each transaction has `lt` and `hash`. 如果您想要更多，那么每笔交易都有 `lt` 和 `hash`。您可以查看例如 30 条交易，如果没在其中找到正确的一笔，那么取最后一笔的 `lt` 和 `hash` 添加到请求中。

这样您就可以得到下一个 30 条交易，以此类推。

例如，测试网络中有一个钱包 `EQAVKMzqtrvNB2SkcBONOijadqFZ1gMdjmzh1Y3HB1p_zai5`，它有一些交易：

使用[查询](https://testnet.toncenter.com/api/v2/getTransactions?address=EQAVKMzqtrvNB2SkcBONOijadqFZ1gMdjmzh1Y3HB1p_zai5\&limit=2\&to_lt=0\&archival=true) 我们将得到包含两笔交易的响应（现在不需要的一些信息已经被隐藏，完整答案可以在上面的链接中看到）。

```json
{
  "ok": true,
  "result": [
    {
      "transaction_id": {
        "lt": "1944556000003",
        "hash": "swpaG6pTBXwYI2024NAisIFp59Fw3k1DRQ5fa5SuKAE="
      },
      "in_msg": {
        "source": "EQCzQJJBAQ-FrEFcvxO5sNxhV9CaOdK9CCfq2yCBnwZ4aJ9R",
        "destination": "EQAVKMzqtrvNB2SkcBONOijadqFZ1gMdjmzh1Y3HB1p_zai5",
        "value": "1000000000",
        "body_hash": "kBfGYBTkBaooeZ+NTVR0EiVGSybxQdb/ifXCRX5O7e0=",
        "message": "Sea breeze 🌊"
      },
      "out_msgs": []
    },
    {
      "transaction_id": {
        "lt": "1943166000003",
        "hash": "hxIQqn7lYD/c/fNS7W/iVsg2kx0p/kNIGF6Ld0QEIxk="
      },
      "in_msg": {
        "source": "EQCzQJJBAQ-FrEFcvxO5sNxhV9CaOdK9CCfq2yCBnwZ4aJ9R",
        "destination": "EQAVKMzqtrvNB2SkcBONOijadqFZ1gMdjmzh1Y3HB1p_zai5",
        "value": "1000000000",
        "body_hash": "7iirXn1RtliLnBUGC5umIQ6KTw1qmPk+wwJ5ibh9Pf0=",
        "message": "Spring forest 🌲"
      },
      "out_msgs": []
    }
  ]
}
```

We have received the last two transactions from this address. When adding `lt` and `hash` to the query, we will again receive two transactions. However, the second one will become the next one in a row. That is, we will get the second and third transactions for this address.

```json
{
  "ok": true,
  "result": [
    {
      "transaction_id": {
        "lt": "1943166000003",
        "hash": "hxIQqn7lYD/c/fNS7W/iVsg2kx0p/kNIGF6Ld0QEIxk="
      },
      "in_msg": {
        "source": "EQCzQJJBAQ-FrEFcvxO5sNxhV9CaOdK9CCfq2yCBnwZ4aJ9R",
        "destination": "EQAVKMzqtrvNB2SkcBONOijadqFZ1gMdjmzh1Y3HB1p_zai5",
        "value": "1000000000",
        "body_hash": "7iirXn1RtliLnBUGC5umIQ6KTw1qmPk+wwJ5ibh9Pf0=",
        "message": "Spring forest 🌲"
      },
      "out_msgs": []
    },
    {
      "transaction_id": {
        "lt": "1845458000003",
        "hash": "k5U9AwIRNGhC10hHJ3MBOPT//bxAgW5d9flFiwr1Sao="
      },
      "in_msg": {
        "source": "EQCzQJJBAQ-FrEFcvxO5sNxhV9CaOdK9CCfq2yCBnwZ4aJ9R",
        "destination": "EQAVKMzqtrvNB2SkcBONOijadqFZ1gMdjmzh1Y3HB1p_zai5",
        "value": "1000000000",
        "body_hash": "XpTXquHXP64qN6ihHe7Tokkpy88tiL+5DeqIrvrNCyo=",
        "message": "Second"
      },
      "out_msgs": []
    }
  ]
}
```

请求将看起来像[这样。](https://testnet.toncenter.com/api/v2/getTransactions?address=EQAVKMzqtrvNB2SkcBONOijadqFZ1gMdjmzh1Y3HB1p_zai5\&limit=2\&lt=1943166000003\&hash=hxIQqn7lYD%2Fc%2FfNS7W%2FiVsg2kx0p%2FkNIGF6Ld0QEIxk%3D\&to_lt=0\&archival=true)

我们还需要一个方法 `detectAddress`。

这是测试网上的 Tonkeeper 钱包地址的一个例子：`kQCzQJJBAQ-FrEFcvxO5sNxhV9CaOdK9CCfq2yCBnwZ4aCTb`。如果我们在浏览器中查找交易，代替上述地址，有：`EQCzQJJBAQ-FrEFcvxO5sNxhV9CaOdK9CCfq2yCBnwZ4aJ9R`。 If we look for the transaction in the explorer, instead of the above address, there is: `EQCzQJJBAQ-FrEFcvxO5sNxhV9CaOdK9CCfq2yCBnwZ4aJ9R`.

这个方法返回给我们“正确”的地址。

```json
{
  "ok": true,
  "result": {
    "raw_form": "0:b3409241010f85ac415cbf13b9b0dc6157d09a39d2bd0827eadb20819f067868",
    "bounceable": {
      "b64": "EQCzQJJBAQ+FrEFcvxO5sNxhV9CaOdK9CCfq2yCBnwZ4aJ9R",
      "b64url": "EQCzQJJBAQ-FrEFcvxO5sNxhV9CaOdK9CCfq2yCBnwZ4aJ9R"
    },
    "non_bounceable": {
      "b64": "UQCzQJJBAQ+FrEFcvxO5sNxhV9CaOdK9CCfq2yCBnwZ4aMKU",
      "b64url": "UQCzQJJBAQ-FrEFcvxO5sNxhV9CaOdK9CCfq2yCBnwZ4aMKU"
    }
  }
}
```

我们需要 `b64url`。

这个方法让我们能够验证用户的地址。

大部分而言，这就是我们所需要的。

### API 请求及其处理方法

Let's go back to the IDE. 让我们回到 IDE。创建文件 `api.py`。

导入所需的库。

```python
import requests
import json
# 我们导入我们的 db 模块，因为这样添加交易到数据库会很方便
import db
```

- `requests`—用来向 API 发送请求
- `json`—用来处理 json
- `db`—用来处理我们的 sqlite 数据库

让我们创建两个变量来存储请求的开头。

```python
# 这是我们请求的开始
MAINNET_API_BASE = "https://toncenter.com/api/v2/"
TESTNET_API_BASE = "https://testnet.toncenter.com/api/v2/"
```

从 config.json 文件中获取所有 API 令牌和钱包。

```python
# 弄清楚我们在哪个网络上工作
with open('config.json', 'r') as f:
    config_json = json.load(f)
    MAINNET_API_TOKEN = config_json['MAINNET_API_TOKEN']
    TESTNET_API_TOKEN = config_json['TESTNET_API_TOKEN']
    MAINNET_WALLET = config_json['MAINNET_WALLET']
    TESTNET_WALLET = config_json['TESTNET_WALLET']
    WORK_MODE = config_json['WORK_MODE']
```

根据网络，我们取所需的数据。

```python
if WORK_MODE == "mainnet":
    API_BASE = MAINNET_API_BASE
    API_TOKEN = MAINNET_API_TOKEN
    WALLET = MAINNET_WALLET
else:
    API_BASE = TESTNET_API_BASE
    API_TOKEN = TESTNET_API_TOKEN
    WALLET = TESTNET_WALLET
```

我们的第一个请求函数 `detectAddress`。

```python
def detect_address(address):
    url = f"{API_BASE}detectAddress?address={address}&api_key={API_TOKEN}"
    r = requests.get(url)
    response = json.loads(r.text)
    try:
        return response['result']['bounceable']['b64url']
    except:
        return False
```

在输入中，我们有预计的地址，输出要么是我们需要的“正确”地址，以便进行进一步的工作，要么是 False。

下一个处理器看起来可能非常复杂，但实际上并不难。首先，我们使用 `len(message.text) == 48` 检查消息是否是有效的钱包地址，因为钱包地址长 48 个字符。之后，我们使用 `api.detect_address` 函数检查地址是否有效。如你从 API 部分记得的那样，这个函数还返回 "正确" 地址，它将被存储在数据库中。 你可能会注意到请求末尾出现了 API 密钥。它是为了移除对 API 请求数量的限制。没有它，我们被限制为每秒一个请求。 Without it, we are limited to one request per second.

这里是 `getTransactions` 的下一个函数：

```python
def get_address_transactions():
    url = f"{API_BASE}getTransactions?address={WALLET}&limit=30&archival=true&api_key={API_TOKEN}"
    r = requests.get(url)
    response = json.loads(r.text)
    return response['result']
```

此函数返回最后 30 次对我们 `WALLET` 的交易。

这里可以看到 `archival=true`。这是因为我们只需要从具有完整区块链历史记录的节点获取交易。 It is needed so that we only take transactions from a node with a complete history of the blockchain.

在输出中，我们获得一个交易列表—[{0},{1},{…},{29}]。简而言之，是字典列表。 List of dictionaries in short.

最后一个函数：

```python
def find_transaction(user_wallet, value, comment):
		# 获取最后 30 次交易
    transactions = get_address_transactions()
    for transaction in transactions:
				# 选择进来的 "message" - 交易
        msg = transaction['in_msg']
        if msg['source'] == user_wallet and msg['value'] == value and msg['message'] == comment:
						# 如果所有数据匹配，我们检查这个交易
						# 我们之前没有验证过
            t = db.check_transaction(msg['body_hash'])
            if t == False:
								# 如果没有，我们在表中写入已验证
								# 并返回 True
                db.add_v_transaction(
                    msg['source'], msg['body_hash'], msg['value'], msg['message'])
                print("find transaction")
                print(
                    f"transaction from: {msg['source']} \nValue: {msg['value']} \nComment: {msg['message']}")
                return True
						# 如果这笔交易已经经过验证，我们检查剩余部分，可能会找到正确的
            else:
                pass
		# 如果最后 30 次交易不含所需的一笔，返回 False
		# 这里你可以添加代码以查看接下来的 29 个交易
		# 然而，在示例的范围内，这将是多余的。
    return False
```

输入是“正确”的钱包地址、金额和评论。如果找到预期的进账交易，输出为 True；否则为 False。 If the intended incoming transaction is found, the output is True; otherwise, it is False.

## Telegram 机器人

首先，让我们为机器人创建基础。

### 导入

在这部分，我们将导入所需的库。

来自 `aiogram`，我们需要 `Bot`、`Dispatcher`、`types` 和 `executor`。

```python
from aiogram import Bot, Dispatcher, executor, types
```

`MemoryStorage` 是用于临时存储信息的。

`FSMContext`, `State`, 和 `StatesGroup` 用于与状态机工作。

```python
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
```

`json` 用来处理 json 文件。`logging` 用来记录错误。 `logging` is needed to log errors.

```python
import json
import logging
```

`api` 和 `db` 是我们自己的文件，稍后我们将填充内容。

```python
import db
import api
```

### 配置设置

建议您将如 `BOT_TOKEN` 和接收付款的钱包等数据存储在一个名为 `config.json` 的单独文件中，以便于使用。

```json
{
  "BOT_TOKEN": "你的机器人令牌",
  "MAINNET_API_TOKEN": "你的主网api令牌",
  "TESTNET_API_TOKEN": "你的测试网api令牌",
  "MAINNET_WALLET": "你的主网钱包",
  "TESTNET_WALLET": "你的测试网钱包",
  "WORK_MODE": "testnet"
}
```

#### Bot token

`BOT_TOKEN` 是你的 Telegram 机器人令牌，来自 [@BotFather](https://t.me/BotFather)

#### 工作模式

在 `WORK_MODE` 键中，我们将定义机器人的工作模式—在测试网或主网；分别为 `testnet` 或 `mainnet`。

#### API 令牌

`*_API_TOKEN` 的 API 令牌可以在 [TON Center](https://toncenter.com/) 机器人处获取：

- 对于主网 — [@tonapibot](https://t.me/tonapibot)
- 对于测试网 — [@tontestnetapibot](https://t.me/tontestnetapibot)

#### 将配置连接到我们的机器人

接下来，我们完成机器人设置。

从 `config.json` 获取机器人工作所需的令牌：

```python
with open('config.json', 'r') as f:
    config_json = json.load(f)
    BOT_TOKEN = config_json['BOT_TOKEN']
		# 在这里放置接收付款的钱包
    MAINNET_WALLET = config_json['MAINNET_WALLET']
    TESTNET_WALLET = config_json['TESTNET_WALLET']
    WORK_MODE = config_json['WORK_MODE']

if WORK_MODE == "mainnet":
    WALLET = MAINNET_WALLET
else:
		# 默认情况下，机器人将在测试网上运行
    WALLET = TESTNET_WALLET
```

### 日志记录和机器人设置

```python
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
```

### 状态

We need States to split the bot workflow into stages. We can specialize each stage for a specific task.

```python
class DataInput (StatesGroup):
    firstState = State()
    secondState = State()
    WalletState = State()
    PayState = State()
```

详情和示例请参见 [Aiogram 文档](https://docs.aiogram.dev/en/latest/)。

### 消息处理器(Message handlers)

这是我们将编写机器人交互逻辑的部分。

我们将使用两种类型的处理器：

- `message_handler` 用于处理用户消息。
- `callback_query_handler` 用于处理来自内联键盘的回调。

如果我们想处理用户的消息，我们将使用 `message_handler` 并在函数上方放置 `@dp.message_handler` 装饰器。在这种情况下，当用户向机器人发送消息时，将调用该函数。 In this case, the function will be called when the user sends a message to the bot.

In the decorator, we can specify the conditions under which the function will be called. 在装饰器中，我们可以指定将在何种条件下调用该函数。例如，如果我们想要在用户发送文本 `/start` 的消息时调用函数，那么我们将编写以下内容：

```
@dp.message_handler(commands=['start'])
```

Handlers need to be assigned to an async function. 默认情况下，如果我们使用它，我们将获得最后 10 条交易。然而，我们也可以表示我们需要更多，但这会略微增加响应时间。而且，很有可能，你不需要那么多。 处理器需要分配给一个异步函数。在这种情况下，我们将使用 `async def` 语法。`async def` 语法用于定义将异步调用的函数。

#### /start

让我们从 `/start` 命令处理器开始。

```python
@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message):
    await message.answer(f"WORKMODE: {WORK_MODE}")
    # 检查用户是否在数据库中。如果不在，添加他
    isOld = db.check_user(
        message.from_user.id, message.from_user.username, message.from_user.first_name)
    # 如果用户已经在数据库中，我们可以不同地对待他
    if isOld == False:
        await message.answer(f"You are new here, {message.from_user.first_name}!")
        await message.answer(f"to buy air send /buy")
    else:
        await message.answer(f"Welcome once again, {message.from_user.first_name}!")
        await message.answer(f"to buy more air send /buy")
    await DataInput.firstState.set()
```

In the decorator of this handler we see `state='*'`. This means that this handler will be called regardless of the state of bot. 在此处理器的装饰器中，我们看到 `state='*'`。这意味着无论机器人的状态如何，该处理器都将被调用。如果我们希望处理器仅在机器人处于特定状态时调用，我们将编写 `state=DataInput.firstState`。在这种情况下，处理器仅在机器人处于 `firstState` 状态时被调用。 In this case, the handler will be called only when the bot is in the `firstState` state.

用户发送 `/start` 命令后，机器人将使用 `db.check_user` 函数检查用户是否在数据库中。如果不是，它将添加他。此函数还将返回布尔值，我们可以使用它以不同的方式对待用户。之后，机器人将设置状态为 `firstState`。 If not, it will add him. This function will also return the bool value and we can use it to address the user differently. After that, the bot will set the state to `firstState`.

#### /cancel

Next is the /cancel command handler. 接下来是 /cancel 命令处理器。它需要返回到 `firstState` 状态。

```python
@dp.message_handler(commands=['cancel'], state="*")
async def cmd_cancel(message: types.Message):
    await message.answer("Canceled")
    await message.answer("/start to restart")
    await DataInput.firstState.set()
```

#### /buy

And, of course, `/buy` command handler. In this example we will sell different types of air. We will use the reply keyboard to choose the type of air.

```python
# /buy 命令处理器
@dp.message_handler(commands=['buy'], state=DataInput.firstState)
async def cmd_buy(message: types.Message):
    # 带有air types的reply keyboard
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton('Just pure 🌫'))
    keyboard.add(types.KeyboardButton('Spring forest 🌲'))
    keyboard.add(types.KeyboardButton('Sea breeze 🌊'))
    keyboard.add(types.KeyboardButton('Fresh asphalt 🛣'))
    await message.answer(f"Choose your air: (or /cancel)", reply_markup=keyboard)
    await DataInput.secondState.set()
```

当然还有 `/buy` 命令处理器。在这个示例中我们将出售不同类型的空气。我们将使用reply keyboard来选择air types。 所以，当用户发送 `/buy` 命令时，机器人发送一个reply keyboard给他，上面有air type。用户选择air type后，机器人将设置状态为 `secondState`。

此处理器将仅在 `secondState` 被设置时工作，并将等待用户发送air type的消息。在这种情况下，我们需要存储用户选择的air type，因此我们将 FSMContext 作为参数传递给函数。  ...在 FSMContext 中存储air type之后，我们设置状态为 `WalletState` 并要求用户发送他的钱包地址。

FSMContext 用于在机器人的内存中存储数据。我们可以在其中存储任何数据，但这个内存不是持久的，所以如果机器人重启，数据将会丢失。但它很适合存储临时数据。 We can store any data in it but this memory is not persistent, so if the bot is restarted, the data will be lost. But it's good to store temporary data in it.

```python
# 处理air type
@dp.message_handler(state=DataInput.secondState)
async def air_type(message: types.Message, state: FSMContext):
    if message.text == "Just pure 🌫":
        await state.update_data(air_type="Just pure 🌫")
    elif message.text == "Fresh asphalt 🛣":
        await state.update_data(air_type="Fresh asphalt 🛣")
    elif message.text == "Spring forest 🌲":
        await state.update_data(air_type="Spring forest 🌲")
    elif message.text == "Sea breeze 🌊":
        await state.update_data(air_type="Sea breeze 🌊")
    else:
        await message.answer("Wrong air type")
        await DataInput.secondState.set()
        return
    await DataInput.WalletState.set()
    await message.answer(f"Send your wallet address")
```

使用...

```python
await state.update_data(air_type="Just pure 🌫")
```

...to store the air type in FSMContext. 我们从这个地址收到了最后两笔交易。当添加 `lt` 和 `hash` 到查询中时，我们将再次收到两笔交易。然而，第二笔将成为下一笔连续的交易。也就是说，我们将获得这个地址的第二笔和第三笔交易。

此处理器将仅在 `WalletState` 被设置时工作，并将等待用户发送钱包地址的消息。

The next handler seems to be very complicated but it's not. First, we check if the message is a valid wallet address using `len(message.text) == 48` because wallet address is 48 characters long. After that, we use `api.detect_address` function to check if the address is valid. As you remember from the API part, this function also returns "Correct" address which will be stored in the database.

之后，我们使用 `await state.get_data()` 从 FSMContext 获取air type并将其存储在 `user_data` 变量中。

Now we have all the data required for the payment process. We just need to generate a payment link and send it to the user. Let's use the inline keyboard.

在此示例中，将为付款创建三个按钮：

- 官方 TON Wallet
- Tonhub
- Tonkeeper

对于钱包的特殊按钮的优点是，如果用户尚未拥有钱包，则网站将提示他安装一个。

You are free to use whatever you want.

我们还需要一个用户付款后按下的按钮，这样我们就可以检查支付是否成功。

```python
@dp.message_handler(state=DataInput.WalletState)
async def user_wallet(message: types.Message, state: FSMContext):
    if len(message.text) == 48:
        res = api.detect_address(message.text)
        if res == False:
            await message.answer("Wrong wallet address")
            await DataInput.WalletState.set()
            return
        else:
            user_data = await state.get_data()
            air_type = user_data['air_type']
            # inline button "检查交易"
            keyboard2 = types.InlineKeyboardMarkup(row_width=1)
            keyboard2.add(types.InlineKeyboardButton(
                text="Check transaction", callback_data="check"))
            keyboard1 = types.InlineKeyboardMarkup(row_width=1)
            keyboard1.add(types.InlineKeyboardButton(
                text="Ton Wallet", url=f"ton://transfer/{WALLET}?amount=1000000000&text={air_type}"))
            keyboard1.add(types.InlineKeyboardButton(
                text="Tonkeeper", url=f"https://app.tonkeeper.com/transfer/{WALLET}?amount=1000000000&text={air_type}"))
            keyboard1.add(types.InlineKeyboardButton(
                text="Tonhub", url=f"https://tonhub.com/transfer/{WALLET}?amount=1000000000&text={air_type}"))
            await message.answer(f"You choose {air_type}")
            await message.answer(f"Send <code>1</code> toncoin to address \n<code>{WALLET}</code> \nwith comment \n<code>{air_type}</code> \nfrom your wallet ({message.text})", reply_markup=keyboard1)
            await message.answer(f"Click the button after payment", reply_markup=keyboard2)
            await DataInput.PayState.set()
            await state.update_data(wallet=res)
            await state.update_data(value_nano="1000000000")
    else:
        await message.answer("Wrong wallet address")
        await DataInput.WalletState.set()
```

#### /me

我们需要的最后一个消息处理器是 `/me` 命令。它显示用户的支付信息。 It shows the user's payments.

```python
# /me 命令处理器
@dp.message_handler(commands=['me'], state="*")
async def cmd_me(message: types.Message):
    await message.answer(f"Your transactions")
    # db.get_user_payments 返回用户的交易列表
    transactions = db.get_user_payments(message.from_user.id)
    if transactions == False:
        await message.answer(f"You have no transactions")
    else:
        for transaction in transactions:
            # 我们需要记住区块链中的值存储为nanotons。在区块链中，1 toncoin = 1000000000
            await message.answer(f"{int(transaction['value'])/1000000000} - {transaction['comment']}")
```

### 回调处理器(Callback handlers)

We can set callback data in buttons which will be sent to the bot when the user presses the button. 我们可以在按钮中设置回调数据，当用户按下按钮时，这些数据将被发送给机器人。在用户交易后按下的按钮中，我们设置回调数据为 "check"。因此，我们需要处理这个回调。 As a result, we need to handle this callback.

回调处理器与消息处理器非常相似，但它们有 `types.CallbackQuery` 作为参数，而不是 `message`。函数装饰器也有所不同。 Function decorator is also different.

```python
@dp.callback_query_handler(lambda call: call.data == "check", state=DataInput.PayState)
async def check_transaction(call: types.CallbackQuery, state: FSMContext):
    # 发送通知
    user_data = await state.get_data()
    source = user_data['wallet']
    value = user_data['value_nano']
    comment = user_data['air_type']
    result = api.find_transaction(source, value, comment)
    if result == False:
        await call.answer("Wait a bit, try again in 10 seconds. You can also check the status of the transaction through the explorer (tonscan.org/)", show_alert=True)
    else:
        db.v_wallet(call.from_user.id, source)
        await call.message.edit_text("Transaction is confirmed \n/start to restart")
        await state.finish()
        await DataInput.firstState.set()
```

在此处理器中，我们从 FSMContext 获取用户数据并使用 `api.find_transaction` 函数检查交易是否成功。如果成功，我们将钱包地址存储在数据库中，并向用户发送通知。此后，用户可以使用 `/me` 命令查找他的交易。 If it was, we store the wallet address in the database and send a notification to the user. After that, the user can find his transactions using `/me` command.

### main.py 的最后一部分

最后，别忘了：

```python
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
```

This part is needed to start the bot.
这部分需要启动机器人。
在 `skip_updates=True` 中，我们指定我们不想处理旧消息。但如果您想处理所有消息，可以将其设置为 `False`。 But if you want to process all messages, you can set it to `False`.

:::info

`main.py` 的所有代码可以在[这里](https://github.com/LevZed/ton-payments-in-telegram-bot/blob/main/bot/main.py)找到。

:::

## Bot in action

We finally did it! You should now have a working bot. You can test it!

运行机器人的步骤：

1. 填写 `config.json` 文件。
2. 运行 `main.py`。

All files must be in the same folder. 所有文件必须在同一个文件夹中。要启动机器人，您需要运行 `main.py` 文件。您可以在 IDE 或终端中这样做： You can do it in your IDE or in the terminal like this:

```
python main.py
```

如果您遇到任何错误，可以在终端中检查。也许您在代码中漏掉了一些东西。 你可以随意使用你想要的内容。

工作中的机器人示例[@AirDealerBot](https://t.me/AirDealerBot)

![bot](/img/tutorials/apiatb-bot.png)

## 参考资料

- 作为 [ton-footsteps/8](https://github.com/ton-society/ton-footsteps/issues/8) 的一部分
- 由 Lev 制作（[Telegram @Revuza](https://t.me/revuza), [LevZed on GitHub](https://github.com/LevZed)）
