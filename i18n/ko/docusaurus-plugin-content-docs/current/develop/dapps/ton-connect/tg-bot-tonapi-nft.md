# NFT 소유권 확인을 위한 텔레그램 봇

## 👋 소개

이 가이드는 대체 불가능한 토큰의 인기가 계속 치솟으면서 토큰 소유권 확인을 위한 효과적인 방법을 찾는 사람들이 늘어남에 따라 토큰 소유권 확인에 대한 지침을 제공하는 것을 목표로 합니다.

## 📝 봇을 위한 토큰 얻기

1. 텔레그램에서 [봇파더](https://t.me/BotFather)를 방문하세요.

2. 안내에 따라 새 봇을 만들 수 있습니다.

3. 봇파더가 생성되면, 고유 토큰이 제공됩니다. 이 토큰은 봇이 텔레그램 API와 통신할 수 있도록 하기 때문에 매우 중요합니다.

## 🧠 봇의 기능 설명

### 기능

텔레그램 봇은 사용자가 TON 발자취 컬렉션의 NFT 아이템을 소유하고 있는지 확인하는 흥미로운 예제 작업을 수행합니다. 핵심 구성 요소는 다음과 같습니다:

- 아이오그램 라이브러리: 텔레그램 클라이언트와의 인터페이스용.
- TON 연결: 사용자의 지갑에 연결합니다.
- Redis 데이터베이스: TON Connect와 관련된 데이터를 처리합니다.

### 🗂️ 프로젝트 구조

- 메인 파일: 봇의 기본 로직이 포함된 파일입니다.
- 헬퍼 파일:
  - 키보드: 텔레그램 봇 키보드 개체.
  - 데이터베이스 준비: TON 연결 촉진하기.

### 🛠️ 라이브러리 설치

다음 명령을 실행하여 `pip`을 통해 필요한 모든 라이브러리를 설치합니다:

```bash
pip install aiogram redis qrcode tonsdk pytonconnect requests
```

그런 다음 메인 파일로 가져옵니다:

```python
import asyncio
import requests
import qrcode
import os
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.input_file import InputFile
from tonsdk.utils import Address
from pytonconnect import TonConnect
```

### 🗄️ Redis 데이터베이스 설정

또한 Redis 데이터베이스를 설정하고 시작하려면 [여기](https://redis.io/docs/getting-started/installation/)에서 찾을 수 있는 설치 및 시작에 관한 정보를 숙지하는 것이 좋습니다.

## 🎨 봇 작성하기

### 🎹 키보드 디자인하기

우선, 필요한 모든 키보드 구성이 포함된 파일을 만들고 이름을 `keyboards.py`로 지정해 보겠습니다.

```python
# Creating custom keyboard buttons and reply markup for the Telegram bot.

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Creating a KeyboardButton for the "Check for footstep NFT" action.
CheckButton = KeyboardButton('Check for footstep NFT')

# Creating a ReplyKeyboardMarkup for the "Check" action using the CheckButton.
# The 'resize_keyboard' parameter is set to True, allowing the keyboard to be resized in the Telegram app.
Checkkb = ReplyKeyboardMarkup(resize_keyboard=True).add(CheckButton)

# Creating additional buttons for the "Tonkeeper" and "Tonhub" actions.
TonkeeperButton = KeyboardButton('Tonkeeper')
TonhubButton = KeyboardButton('Tonhub')

# Creating a ReplyKeyboardMarkup for the "Wallet" action using the TonkeeperButton and TonhubButton.
# The 'resize_keyboard' parameter is set to True to allow the keyboard to be resized in the Telegram app.
Walletkb = ReplyKeyboardMarkup(resize_keyboard=True).add(TonkeeperButton).add(TonhubButton)
```

그리고 이 파일을 `main.py`에 가져오기를 추가해 보겠습니다.

```python
import keyboards as kb
```

### 🧩 데이터베이스 준비

이제 `pytonconnect`와 인터페이스할 수 있도록 데이터베이스를 준비해야 합니다.
이를 위해 `database.py`라는 새 파일을 생성합니다.

```python
# Importing the Redis library to interact with the Redis database
import redis
# Importing the IStorage interface from pytonconnect
from pytonconnect.storage import IStorage

# Creating a connection to the Redis database running on localhost at port 6379
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Defining a class Storage that implements the IStorage interface from pytonconnect
class Storage(IStorage):
    def __init__(self, id):
        # Constructor method initializing the unique identifier for each storage instance
        self.id = id

    # Asynchronous method to set a key-value pair in Redis, with the key being appended with the unique ID
    async def set_item(self, key: str, value: str):
        r.set(key + self.id, value)

    # Asynchronous method to retrieve the value for a given key from Redis, with the key being appended with the unique ID
    # If the key does not exist, returns the default value
    async def get_item(self, key: str, default_value: str = None):
        if r.exists(key + self.id):
            return r.get(key + self.id)
        else:
            return default_value

    # Asynchronous method to remove the key-value pair for a given key from Redis, with the key being appended with the unique ID
    async def remove_item(self, key: str):
        r.delete(key + self.id)
```

또한 봇을 사용하여 메인 파일로 가져올 수도 있습니다.

```python
import database
```

### 🌟 시작 핸들러 작성

```python
# Define a command handler for the '/start' command for private chats
@dp.message_handler(commands=['start'], chat_type=types.ChatType.PRIVATE)
async def start_command(message: types.Message):
    # Send a greeting message to the user, explaining the bot's functionality
    await message.answer("Hi👋, I am an example of a bot for checking the ownership of the NFT", reply_markup=kb.Checkkb)
    # Further explain how the bot can help with NFT collection checking
    await message.answer("With my help, you can check if you have an NFT from the TON Footsteps collection")
```

### 🕵️ NFT의 존재 여부를 확인하는 기능

```python
# A message handler function to check if the user has a footstep NFT and respond accordingly.

@dp.message_handler(text='Check for footstep NFT', chat_type=types.ChatType.PRIVATE)
async def connect_wallet_tonkeeper(message: types.Message):
    # Checking if the user's wallet address is present in the database for the given Telegram ID.
    # If the address is not available, prompt the user to connect their wallet (Tonkeeper or Tonhub).
    if cur.execute(f"SELECT address FROM Users WHERE id_tg == {message.from_user.id}").fetchall()[0][0] is None:
        await message.answer(text="To check for the presence of NFT, connect your wallet (Tonkeeper or Tonhub)", reply_markup=kb.Walletkb)
    else:
        # If the user's wallet address is available, proceed to check for the presence of the footstep NFT.
        address = cur.execute(f"SELECT address FROM Users WHERE id_tg == {message.from_user.id}").fetchall()[0][0]

        # Forming the URL to query the TON API for the user's NFTs from the TON Footsteps collection.
        url = f'https://tonapi.io/v2/accounts/{address}/nfts?collection=EQCV8xVdWOV23xqOyC1wAv-D_H02f7gAjPzOlNN6Nv1ksVdL&limit=1000&offset=0&indirect_ownership=false'

        try:
            # Sending a GET request to the TON API and parsing the JSON response to extract NFT items.
            response = requests.get(url).json()['nft_items']
        except:
            # If there's an error with the API request, notify the user.
            await message.answer(text="Something went wrong...")
            return

        # Based on the response from the TON API, informing the user about the NFT presence or absence.
        if response:
            await message.answer(text="You have an NFT from the TON Footsteps collection")
        else:
            await message.answer(text="Unfortunately, you don't have NFT from the TON Footsteps collection")
```

NFT 사용자가 필요한 컬렉션을 보유하고 있는지 확인하기 위해 [TONAPI](https://tonapi.io/)를 사용합니다. 요청은 다음과 같습니다:

```bash
https://tonapi.io/v2/accounts/<ADDRESS>/nfts?collection=<NFT_COLLECTION>&limit=1000&offset=0&indirect_ownership=false
```

Where:

- '주소' - 필요한 NFT를 확인하려는 사용자의 지갑 주소입니다.
- `NFT_COLLECTION` - 필요한 NFT 컬렉션의 주소입니다.

API 요청은 지정된 컬렉션에서 사용자의 모든 NFT를 반환합니다.

### 🏡 TON Connect를 통해 사용자 주소를 가져오는 기능

```python
# Define a message handler for connection to wallets (Tonkeeper or Tonhub) in private chats
@dp.message_handler(text=['Tonkeeper', 'Tonhub'], chat_type=types.ChatType.PRIVATE)
async def connect_wallet_tonkeeper(message: types.Message):
    # Create a storage instance based on the user's ID
    storage = database.Storage(str(message.from_user.id))

    # Initialize a connection using the given manifest URL and storage
    connector = TonConnect(manifest_url='https://raw.githubusercontent.com/AndreyBurnosov/Checking_for_nft_availability/main/pytonconnect-manifest.json', storage=storage)
    # Attempt to restore the existing connection, if any
    is_connected = await connector.restore_connection()

    # If already connected, inform the user and exit the function
    if is_connected:
        await message.answer('Your wallet is already connected.')
        return

    # Define the connection options for different wallet
    connection = {'Tonkeeper': 0, 'Tonhub': 2}

    # Retrieve the available wallets
    wallets_list = connector.get_wallets()

    # Generate a connection URL for the selected wallet
    generated_url_tonkeeper = await connector.connect(wallets_list[connection[message.text]])

    # Create an inline keyboard markup with a button to open the connection URL
    urlkb = InlineKeyboardMarkup(row_width=1)
    urlButton = InlineKeyboardButton(text=f'Open {message.text}', url=generated_url_tonkeeper)
    urlkb.add(urlButton)

    # Generate a QR code for the connection URL and save it as an image
    img = qrcode.make(generated_url_tonkeeper)
    path = f'image{random.randint(0, 100000)}.png'
    img.save(path)
    photo = InputFile(path)

    # Send the QR code image to the user with the inline keyboard markup
    msg = await bot.send_photo(chat_id=message.chat.id, photo=photo, reply_markup=urlkb)
    # Remove the saved image from the local file system
    os.remove(path)

    # Check for a successful connection in a loop, with a maximum of 300 iterations (300 seconds)
    for i in range(300):
        await asyncio.sleep(1)
        if connector.connected:
            if connector.account.address:
                address = Address(connector.account.address).to_string(True, True, True)
            break

    # Delete the previously sent QR code message
    await msg.delete()

    # Confirm to the user that the wallet has been successfully connected
    await message.answer('Your wallet has been successfully connected.', reply_markup=kb.Checkkb)
```

#### 📄 TON Connect용 매니페스트 만들기

TON Connect를 올바르게 사용하려면 이 템플릿에 따라 'pytonconnect-manifest.json'이라는 파일을 만들어야 합니다:

```json
{
  "url": "<app-url>", // required
  "name": "<app-name>", // required
  "iconUrl": "<app-icon-url>", // required
  "termsOfUseUrl": "<terms-of-use-url>", // optional
  "privacyPolicyUrl": "<privacy-policy-url>" // optional
}
```

이 봇의 경우 기본 아이콘과 원하는 이름을 사용하면 충분합니다:

```json
{
  "url": "",
  "name": "Example bot",
  "iconUrl": "https://raw.githubusercontent.com/XaBbl4/pytonconnect/main/pytonconnect.png"
}
```

저장소에서 `pytonconnect` 라이브러리에 대해 자세히 알아볼 수 있습니다(https://github.com/XaBbl4/pytonconnect).

### 🚀 봇 시작하기

main.py\`의 끝에 다음 코드를 추가하면 봇을 테스트할 준비가 완료됩니다!

```python
# The main entry point of the Telegram bot application.

if __name__ == '__main__':
    # Start polling for updates from the Telegram Bot API using the executor.
    # The `dp` (Dispatcher) object handles message handling and other event processing.
    # The `skip_updates=True` parameter tells the executor to skip pending updates when starting.
    executor.start_polling(dp, skip_updates=True)
```

이제 터미널에서 이 명령을 실행하기만 하면 됩니다:

```bash
python3 main.py
```

그 후, 텔레그램에서 봇과의 대화를 열고 사용을 시도해 보세요. 이 가이드를 올바르게 따랐다면, 봇이 예상대로 작동할 것입니다!

## [🎁 최종 코드 및 리소스](https://github.com/AndreyBurnosov/Checking_for_nft_availability)

## 📌 참고 자료

- [TON API](https://tonapi.io/)
- [TON Connect2.0용 파이썬 라이브러리](https://github.com/XaBbl4/pytonconnect)
- 이 튜토리얼은 [Andrew Burnosov](https://github.com/AndreyBurnosov)가 개발했습니다(TG: [@AndrewBurnosov](https://t.me/AndreyBurnosov)).
