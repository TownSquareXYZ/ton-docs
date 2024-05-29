---
description: 이 글에서는 텔레그램 봇에서 결제를 수락하는 과정을 안내해드리겠습니다.
---

# TON으로 결제하는 스토어 프론트 봇

이 글에서는 텔레그램 봇에서 결제를 수락하는 과정을 안내해드리겠습니다.

## 📖 학습 내용

이 글에서는 방법을 알아보세요:

- 파이썬 + 아이오그램을 사용하여 텔레그램 봇 만들기
- 공용 TON API(TON 센터)로 작업하기
- SQlite 데이터베이스 작업

마지막으로, 이전 단계의 지식으로 텔레그램 봇에서 결제를 수락하는 방법을 알려드리겠습니다.

## 📚 시작하기 전

최신 버전의 Python을 설치하고 다음 패키지를 설치했는지 확인하세요:

- aiogram
- 요청
- sqlite3

## 🚀 시작해보자!

아래 순서를 따르겠습니다:

1. SQlite 데이터베이스 작업
2. 공개 TON API(TON 센터)로 작업하기
3. 파이썬 + 아이오그램을 사용하여 텔레그램 봇 만들기
4. 이익!

프로젝트 디렉토리에 다음 네 개의 파일을 만들어 보겠습니다:

```
telegram-bot
├── config.json
├── main.py
├── api.py
└── db.py
```

## 구성

config.json\`에 봇 토큰과 공개 TON API 키를 저장합니다.

```json
{
  "BOT_TOKEN": "Your bot token",
  "MAINNET_API_TOKEN": "Your mainnet api token",
  "TESTNET_API_TOKEN": "Your testnet api token",
  "MAINNET_WALLET": "Your mainnet wallet",
  "TESTNET_WALLET": "Your testnet wallet",
  "WORK_MODE": "testnet"
}
```

config.json`에서 어떤 네트워크를 사용할지 결정합니다: 테스트넷` 또는 `메인넷` 중 하나를 선택합니다.

## 데이터베이스

### 데이터베이스 만들기

이 예제에서는 로컬 Sqlite 데이터베이스를 사용합니다.

db.py\`를 생성합니다.

데이터베이스 작업을 시작하려면 sqlite3 모듈(
)과 시간 작업을 위한 일부 모듈을 가져와야 합니다.

```python
import sqlite3
import datetime
import pytz
```

- sqlite 데이터베이스 작업을 위한 `sqlite3` 모듈
- 시간 작업을 위한 '날짜' 모듈
- 시간대 작업을 위한 '피츠' 모듈

다음으로 데이터베이스에 대한 연결과 작업할 커서를 만들어야 합니다:

```python
locCon = sqlite3.connect('local.db', check_same_thread=False)
cur = locCon.cursor()
```

데이터베이스가 존재하지 않으면 자동으로 생성됩니다.

이제 테이블을 만들 수 있습니다. 두 개의 테이블이 있습니다.

#### 거래:

```sql
CREATE TABLE transactions (
    source  VARCHAR (48) NOT NULL,
    hash    VARCHAR (50) UNIQUE
                         NOT NULL,
    value   INTEGER      NOT NULL,
    comment VARCHAR (50)
);
```

- 출처\`-결제자의 지갑 주소
- 해시\`-트랜잭션 해시
- value\`-트랜잭션 값
- 댓글\`-거래 댓글

#### 사용자:

```sql
CREATE TABLE users (
    id         INTEGER       UNIQUE
                             NOT NULL,
    username   VARCHAR (33),
    first_name VARCHAR (300),
    wallet     VARCHAR (50)  DEFAULT none
);
```

- 아이디\` - 텔레그램 사용자 아이디
- 사용자명\`-텔레그램 사용자명
- first_name\` - 텔레그램 사용자의 이름
- '지갑\`-사용자 지갑 주소

사용자\` 테이블에 사용자를 저장합니다.) 텔레그램 아이디, @사용자명,
이름, 지갑이 저장됩니다. 지갑은 첫 번째
결제 성공 시 데이터베이스에 추가됩니다.

트랜잭션\` 테이블에는 확인된 트랜잭션이 저장됩니다.
트랜잭션을 확인하려면 해시, 소스, 값 및 댓글이 필요합니다.

이러한 테이블을 만들려면 다음 함수를 실행해야 합니다:

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

이 코드는 테이블이 아직 생성되지 않은 경우 테이블을 생성합니다.

### 데이터베이스 작업

상황을 분석해 보겠습니다:
사용자가 트랜잭션을 만들었습니다. 어떻게 확인하나요? 동일한 거래가 두 번 확인되지 않도록 하려면 어떻게 해야 할까요?

데이터베이스에 트랜잭션이 있는지 여부를 쉽게 이해할 수 있는 body_hash가 트랜잭션에 있습니다.

확실하다고 판단되는 트랜잭션을 데이터베이스에 추가합니다. 'check_transaction' 함수는 찾은 트랜잭션이 데이터베이스에 있는지 여부를 확인합니다.

add_v_transaction\`은 트랜잭션 테이블에 트랜잭션을 추가합니다.

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

check_user\`는 사용자가 데이터베이스에 있는지 확인하고 없는 경우 추가합니다.

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

사용자는 테이블에 지갑을 저장할 수 있습니다. 지갑은 첫 번째 구매 성공 시 추가됩니다. v_wallet\` 함수는 사용자에게 연결된 지갑이 있는지 확인합니다. 있는 경우 반환합니다. 그렇지 않으면 추가합니다.

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

get_user_wallet\`은 단순히 사용자의 지갑을 반환합니다.

```python
def get_user_wallet(user_id):
    cur.execute(f"SELECT wallet FROM users WHERE id = '{user_id}'")
    result = cur.fetchone()
    return result[0]
```

get_user_payments\`는 사용자의 결제 목록을 반환합니다.
이 함수는 사용자가 지갑을 가지고 있는지 확인합니다. 지갑이 있으면 결제 목록을 반환합니다.

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

일부 네트워크 멤버가 제공하는 타사 API를 사용해 블록체인과 상호작용할 수 있습니다. 이러한 서비스를 통해 개발자는 자체 노드를 실행하고 API를 커스터마이징하는 단계를 생략할 수 있습니다.

### 필수 요청

실제로 사용자가 필요한 금액을 송금했는지 확인하기 위해 필요한 것은 무엇인가요?

지갑으로 들어오는 최신 이체를 살펴보고 그중에서 올바른 주소에서 올바른 금액(그리고 고유한 코멘트)의 거래를 찾기만 하면 됩니다.
이 모든 작업을 위해 TON 센터에는 `겟트랜잭션` 메서드가 있습니다.

### getTransactions

기본적으로 이를 적용하면 마지막 10개의 트랜잭션을 가져옵니다. 그러나 더 많은 트랜잭션이 필요하다고 표시할 수도 있지만 응답 시간이 약간 늘어날 수 있습니다. 그리고 대부분의 경우 그렇게 많이 필요하지 않습니다.

더 많은 트랜잭션을 원한다면 각 트랜잭션에는 `lt`와 `해시`가 있습니다. 예를 들어 30개의 트랜잭션을 살펴보고 그중에서 올바른 트랜잭션을 찾지 못한 경우 마지막 트랜잭션에서 `lt`와 `해시`를 가져와 요청에 추가할 수 있습니다.

따라서 다음 30개의 트랜잭션이 이어집니다.

예를 들어, 테스트 네트워크 `EQAVKMzqtrvNB2SkcBONOijadqFZ1gMdjmzh1Y3HB1p_zai5`에 지갑이 있으며, 일부 트랜잭션이 있습니다:

쿼리](https://testnet.toncenter.com/api/v2/getTransactions?address=EQAVKMzqtrvNB2SkcBONOijadqFZ1gMdjmzh1Y3HB1p_zai5&limit=2&to_lt=0&archival=true)를 사용하면 두 개의 트랜잭션이 포함된 응답을 얻을 수 있습니다(현재 필요하지 않은 일부 정보는 숨겨져 있으며, 위 링크에서 전체 응답을 볼 수 있습니다).

```json
{
  "ok": true,
  "result": [
    {
      "transaction_id": {
        // highlight-next-line
        "lt": "1944556000003",
        // highlight-next-line
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
        // highlight-next-line
        "lt": "1943166000003",
        // highlight-next-line
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

이 주소에서 마지막 두 개의 트랜잭션을 받았습니다. 쿼리에 `lt`와 `hash`를 추가하면 다시 두 개의 트랜잭션을 받게 됩니다. 그러나 두 번째 트랜잭션은 연속으로 다음 트랜잭션이 됩니다. 즉, 이 주소에 대한 두 번째와 세 번째 트랜잭션을 받게 됩니다.

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

요청은 [이.](https://testnet.toncenter.com/api/v2/getTransactions?address=EQAVKMzqtrvNB2SkcBONOijadqFZ1gMdjmzh1Y3HB1p_zai5\&limit=2\&lt=1943166000003\&hash=hxIQqn7lYD%2Fc%2FfNS7W%2FiVsg2kx0p%2FkNIGF6Ld0QEIxk%3D\&to_lt=0\&archival=true)와 같이 표시됩니다.

또한 `detectAddress` 메서드도 필요합니다.

다음은 테스트넷의 톤키퍼 지갑 주소의 예시입니다: `kQCzQJJBAQ-FrEFcvxO5sNxhV9CaOdK9CCfq2yCBnwZ4aCTb`. 탐색기에서 트랜잭션을 찾으면 위의 주소 대신 `EQCzQJJBAQ-FrEFcvxO5sNxhV9CaOdK9CCfq2yCBnwZ4aJ9R`이 있습니다.

이 메서드는 "올바른" 주소를 반환합니다.

```json
{
  "ok": true,
  "result": {
    "raw_form": "0:b3409241010f85ac415cbf13b9b0dc6157d09a39d2bd0827eadb20819f067868",
    "bounceable": {
      "b64": "EQCzQJJBAQ+FrEFcvxO5sNxhV9CaOdK9CCfq2yCBnwZ4aJ9R",
      // highlight-next-line
      "b64url": "EQCzQJJBAQ-FrEFcvxO5sNxhV9CaOdK9CCfq2yCBnwZ4aJ9R"
    },
    "non_bounceable": {
      "b64": "UQCzQJJBAQ+FrEFcvxO5sNxhV9CaOdK9CCfq2yCBnwZ4aMKU",
      "b64url": "UQCzQJJBAQ-FrEFcvxO5sNxhV9CaOdK9CCfq2yCBnwZ4aMKU"
    }
  }
}
```

b64url\`이 필요합니다.

이 방법을 사용하면 사용자의 주소를 확인할 수 있습니다.

대부분의 경우 이 정도면 충분합니다.

### API 요청 및 처리 방법

IDE로 돌아가 보겠습니다. 파일 `api.py`를 생성합니다.

필요한 라이브러리를 가져옵니다.

```python
import requests
import json
# We import our db module, as it will be convenient to add from here
# transactions to the database
import db
```

- '요청'- API에 요청하기
- json\`으로 작업하려면
- `db` - sqlite 데이터베이스 작업

요청의 시작을 저장하기 위한 두 개의 변수를 만들어 보겠습니다.

```python
# This is the beginning of our requests
MAINNET_API_BASE = "https://toncenter.com/api/v2/"
TESTNET_API_BASE = "https://testnet.toncenter.com/api/v2/"
```

config.json 파일에서 모든 API 토큰과 지갑을 가져옵니다.

```python
# Find out which network we are working on
with open('config.json', 'r') as f:
    config_json = json.load(f)
    MAINNET_API_TOKEN = config_json['MAINNET_API_TOKEN']
    TESTNET_API_TOKEN = config_json['TESTNET_API_TOKEN']
    MAINNET_WALLET = config_json['MAINNET_WALLET']
    TESTNET_WALLET = config_json['TESTNET_WALLET']
    WORK_MODE = config_json['WORK_MODE']
```

네트워크에 따라 필요한 데이터를 가져옵니다.

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

첫 번째 요청 함수 `detectAddress`입니다.

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

입력에는 예상 주소가 있고 출력에는 추가 작업을 수행하는 데 필요한 '올바른' 주소 또는 False가 있습니다.

요청 끝에 API 키가 표시되는 것을 볼 수 있습니다. API 요청 횟수 제한을 제거하려면 이 키가 필요합니다. 이 키가 없으면 초당 한 번의 요청으로 제한됩니다.

다음은 `getTransactions`의 다음 함수입니다:

```python
def get_address_transactions():
    url = f"{API_BASE}getTransactions?address={WALLET}&limit=30&archival=true&api_key={API_TOKEN}"
    r = requests.get(url)
    response = json.loads(r.text)
    return response['result']
```

이 함수는 마지막 30개의 트랜잭션을 `WALLET`에 반환합니다.

여기서 '아카이브=참'을 볼 수 있습니다. 이는 블록체인의 전체 기록이 있는 노드에서만 트랜잭션을 가져올 수 있도록 하기 위해 필요합니다.

출력에는 [{0},{1},{…},{29}]의 트랜잭션 목록이 표시됩니다. 간단히 말해서 사전 목록입니다.

마지막으로 마지막 기능입니다:

```python
def find_transaction(user_wallet, value, comment):
		# Get the last 30 transactions
    transactions = get_address_transactions()
    for transaction in transactions:
				# Select the incoming "message" - transaction
        msg = transaction['in_msg']
        if msg['source'] == user_wallet and msg['value'] == value and msg['message'] == comment:
						# If all the data match, we check that this transaction
						# we have not verified before
            t = db.check_transaction(msg['body_hash'])
            if t == False:
								# If not, we write in the table to the verified
								# and return True
                db.add_v_transaction(
                    msg['source'], msg['body_hash'], msg['value'], msg['message'])
                print("find transaction")
                print(
                    f"transaction from: {msg['source']} \nValue: {msg['value']} \nComment: {msg['message']}")
                return True
						# If this transaction is already verified, we check the rest, we can find the right one
            else:
                pass
		# If the last 30 transactions do not contain the required one, return False
		# Here you can add code to see the next 29 transactions
		# However, within the scope of the Example, this would be redundant.
    return False
```

입력에는 "올바른" 지갑 주소, 금액, 댓글을 입력합니다. 의도한 수신 트랜잭션이 발견되면 출력은 참이고, 그렇지 않으면 거짓입니다.

## 텔레그램 봇

먼저 봇의 기초를 만들어 보겠습니다.

### 가져오기

이 부분에서는 필요한 라이브러리를 가져오겠습니다.

아이오그램`에서 `봇`, `디스패처`, `유형`, `실행자\`가 필요합니다.

```python
from aiogram import Bot, Dispatcher, executor, types
```

임시 정보 저장을 위해 'MemoryStorage'가 필요합니다.

상태 머신으로 작업하려면 `FSMContext`, `State`, `StatesGroup`이 필요합니다.

```python
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
```

json 파일로 작업하려면 `json`이 필요합니다. 로깅\`은 오류를 기록하는 데 필요합니다.

```python
import json
import logging
```

api`와 `db\`는 나중에 채울 자체 파일입니다.

```python
import db
import api
```

### 구성 설정

편의를 위해 `BOT_TOKEN`과 같은 데이터와 결제를 받기 위한 지갑은 `config.json`이라는 별도의 파일에 저장하는 것을 권장합니다.

```json
{
  "BOT_TOKEN": "Your bot token",
  "MAINNET_API_TOKEN": "Your mainnet api token",
  "TESTNET_API_TOKEN": "Your testnet api token",
  "MAINNET_WALLET": "Your mainnet wallet",
  "TESTNET_WALLET": "Your testnet wallet",
  "WORK_MODE": "testnet"
}
```

#### 봇 토큰

봇_토큰\`은 [@봇파더](https://t.me/BotFather)의 텔레그램 봇 토큰입니다.

#### 작업 모드

작업 모드`키에서 봇의 작동 모드(테스트 또는 메인 네트워크)를 각각`테스트넷`또는`메인넷\`으로 정의합니다.

#### API 토큰

API 토큰은 [TON 센터](https://toncenter.com/) 봇에서 `*_API_TOKEN`을 획득할 수 있습니다:

- 메인넷용 - [@tonapibot](https://t.me/tonapibot)
- 테스트넷용 - [@tontestnetapibot](https://t.me/tontestnetapibot)

#### 봇에 구성 연결

다음으로 봇 설정을 완료합니다.

config.json\`에서 봇이 작동하기 위한 토큰을 가져옵니다:

```python
with open('config.json', 'r') as f:
    config_json = json.load(f)
    # highlight-next-line
    BOT_TOKEN = config_json['BOT_TOKEN']
		# put wallets here to receive payments
    MAINNET_WALLET = config_json['MAINNET_WALLET']
    TESTNET_WALLET = config_json['TESTNET_WALLET']
    WORK_MODE = config_json['WORK_MODE']

if WORK_MODE == "mainnet":
    WALLET = MAINNET_WALLET
else:
		# By default, the bot will run on the testnet
    WALLET = TESTNET_WALLET
```

### 로깅 및 봇 설정

```python
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
```

### 상태

봇 워크플로우를 여러 단계로 나누려면 스테이트가 필요합니다. 각 단계를 특정 작업에 맞게 전문화할 수 있습니다.

```python
class DataInput (StatesGroup):
    firstState = State()
    secondState = State()
    WalletState = State()
    PayState = State()
```

자세한 내용과 예시는 [아이오그램 문서](https://docs.aiogram.dev/en/latest/)를 참조하세요.

### 메시지 핸들러

봇 상호작용 로직을 작성하는 부분입니다.

두 가지 유형의 핸들러를 사용하겠습니다:

- 메시지 핸들러\`는 사용자의 메시지를 처리하는 데 사용됩니다.
- 콜백_쿼리_핸들러\`는 인라인 키보드의 콜백을 처리하는 데 사용됩니다.

사용자가 보낸 메시지를 처리하려면 함수 위에 `@dp.message_handler` 데코레이터를 배치하여 `message_handler`를 사용합니다. 이 경우 사용자가 봇에 메시지를 보낼 때 함수가 호출됩니다.

데코레이터에서 함수가 호출될 조건을 지정할 수 있습니다. 예를 들어 사용자가 `/start` 텍스트가 포함된 메시지를 보낼 때만 함수가 호출되도록 하려면 다음과 같이 작성합니다:

```
@dp.message_handler(commands=['start'])
```

핸들러를 비동기 함수에 할당해야 합니다. 이 경우 `async def` 구문을 사용합니다. 비동기적으로 호출될 함수를 정의할 때 `async def` 구문을 사용합니다.

#### /start

시작\` 명령 핸들러부터 시작하겠습니다.

```python
@dp.message_handler(commands=['start'], state='*')
async def cmd_start(message: types.Message):
    await message.answer(f"WORKMODE: {WORK_MODE}")
    # check if user is in database. if not, add him
    isOld = db.check_user(
        message.from_user.id, message.from_user.username, message.from_user.first_name)
    # if user already in database, we can address him differently
    if isOld == False:
        await message.answer(f"You are new here, {message.from_user.first_name}!")
        await message.answer(f"to buy air send /buy")
    else:
        await message.answer(f"Welcome once again, {message.from_user.first_name}!")
        await message.answer(f"to buy more air send /buy")
    await DataInput.firstState.set()
```

이 핸들러의 데코레이터에서 `state='*'`를 볼 수 있습니다. 이는 이 핸들러가 봇의 상태에 관계없이 호출된다는 것을 의미합니다. 봇이 특정 상태에 있을 때만 핸들러가 호출되도록 하려면 `state=DataInput.firstState`를 작성합니다. 이 경우 핸들러는 봇이 `firstState` 상태일 때만 호출됩니다.

사용자가 `/start` 명령을 보내면 봇은 `db.check_user` 함수를 사용하여 사용자가 데이터베이스에 있는지 확인합니다. 그렇지 않은 경우 추가합니다. 이 함수는 또한 부울 값을 반환하며 이를 사용하여 사용자를 다르게 주소 지정할 수 있습니다. 그 후 봇은 상태를 `firstState`로 설정합니다.

#### /취소

다음은 /cancel 명령 핸들러입니다. 첫 번째 상태\`로 돌아가는 데 필요합니다.

```python
@dp.message_handler(commands=['cancel'], state="*")
async def cmd_cancel(message: types.Message):
    await message.answer("Canceled")
    await message.answer("/start to restart")
    await DataInput.firstState.set()
```

#### /구매

물론 `/buy` 명령 핸들러도 있습니다. 이 예에서는 다양한 종류의 공기를 판매하겠습니다. 답장 키보드를 사용하여 공기 종류를 선택하겠습니다.

```python
# /buy command handler
@dp.message_handler(commands=['buy'], state=DataInput.firstState)
async def cmd_buy(message: types.Message):
    # reply keyboard with air types
    keyboard = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton('Just pure 🌫'))
    keyboard.add(types.KeyboardButton('Spring forest 🌲'))
    keyboard.add(types.KeyboardButton('Sea breeze 🌊'))
    keyboard.add(types.KeyboardButton('Fresh asphalt 🛣'))
    await message.answer(f"Choose your air: (or /cancel)", reply_markup=keyboard)
    await DataInput.secondState.set()
```

따라서 사용자가 `/buy` 명령을 보내면 봇은 공기 유형이 포함된 응답 키보드를 보냅니다. 사용자가 에어 타입을 선택하면 봇은 상태를 'secondState'로 설정합니다.

이 핸들러는 `secondState`가 설정된 경우에만 작동하며 공기 유형이 있는 사용자의 메시지를 기다립니다.  이 경우 사용자가 선택한 에어 타입을 저장해야 하므로 함수에 FSMContext를 인수로 전달합니다.

FSMContext는 봇의 메모리에 데이터를 저장하는 데 사용됩니다. 어떤 데이터든 저장할 수 있지만 이 메모리는 영구적이지 않으므로 봇이 다시 시작되면 데이터가 손실됩니다. 하지만 임시 데이터를 저장하는 것이 좋습니다.

```python
# handle air type
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

사용...

```python
await state.update_data(air_type="Just pure 🌫")
```

...에 공기 유형을 저장합니다. 그 후 상태를 '월렛 스테이트'로 설정하고 사용자에게 지갑 주소를 보내달라고 요청합니다.

이 핸들러는 '지갑 상태'가 설정된 경우에만 작동하며 지갑 주소가 포함된 사용자의 메시지를 기다립니다.

다음 핸들러는 매우 복잡해 보이지만 실제로는 그렇지 않습니다. 먼저 지갑 주소의 길이가 48자이므로 `len(message.text) == 48`을 사용하여 메시지가 유효한 지갑 주소인지 확인합니다. 그런 다음 `api.detect_address` 함수를 사용하여 주소가 유효한지 확인합니다. API 부분에서 기억하셨겠지만, 이 함수는 데이터베이스에 저장될 "올바른" 주소를 반환합니다.

그런 다음 `await state.get_data()`를 사용하여 FSMContext에서 공기 유형을 가져와 `user_data` 변수에 저장합니다.

이제 결제 프로세스에 필요한 모든 데이터가 준비되었습니다. 이제 결제 링크를 생성하여 사용자에게 전송하기만 하면 됩니다. 인라인 키보드를 사용하겠습니다.

이 예제에서는 결제용 버튼 3개가 생성됩니다:

- 공식 TON 월렛의 경우
- 톤허브용
- 톤키퍼용

지갑 전용 버튼의 장점은 사용자가 아직 지갑을 가지고 있지 않은 경우 사이트에서 지갑을 설치하라는 메시지를 표시한다는 것입니다.

원하는 것은 무엇이든 자유롭게 사용할 수 있습니다.

그리고 결제 성공 여부를 확인할 수 있도록 거래 후 사용자가 누를 버튼이 필요합니다.

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
            # inline button "check transaction"
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

마지막으로 필요한 메시지 핸들러는 `/me` 명령을 위한 것입니다. 사용자의 결제를 표시합니다.

```python
# /me command handler
@dp.message_handler(commands=['me'], state="*")
async def cmd_me(message: types.Message):
    await message.answer(f"Your transactions")
    # db.get_user_payments returns list of transactions for user
    transactions = db.get_user_payments(message.from_user.id)
    if transactions == False:
        await message.answer(f"You have no transactions")
    else:
        for transaction in transactions:
            # we need to remember that blockchain stores value in nanotons. 1 toncoin = 1000000000 in blockchain
            await message.answer(f"{int(transaction['value'])/1000000000} - {transaction['comment']}")
```

### 콜백 핸들러

사용자가 버튼을 누를 때 봇으로 전송되는 콜백 데이터를 버튼에 설정할 수 있습니다. 트랜잭션 후 사용자가 누르게 될 버튼에서 콜백 데이터를 "확인"으로 설정합니다. 따라서 이 콜백을 처리해야 합니다.

콜백 핸들러는 메시지 핸들러와 매우 유사하지만 `message` 대신 `types.CallbackQuery`를 인수로 사용합니다. 함수 데코레이터도 다릅니다.

```python
@dp.callback_query_handler(lambda call: call.data == "check", state=DataInput.PayState)
async def check_transaction(call: types.CallbackQuery, state: FSMContext):
    # send notification
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

이 핸들러에서는 FSMContext에서 사용자 데이터를 가져와 `api.find_transaction` 함수를 사용하여 트랜잭션이 성공했는지 확인합니다. 성공했다면 지갑 주소를 데이터베이스에 저장하고 사용자에게 알림을 보냅니다. 그 후 사용자는 `/me` 명령을 사용하여 자신의 트랜잭션을 찾을 수 있습니다.

### main.py의 마지막 부분

마지막으로 잊지 마세요:

```python
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
```

이 부분은 봇을 시작하는 데 필요합니다.
skip_updates=True`에서 이전 메시지를 처리하지 않도록 지정합니다. 그러나 모든 메시지를 처리하려면 `False\`로 설정하면 됩니다.

:::info

main.py\`의 모든 코드는 [여기](https://github.com/LevZed/ton-payments-in-telegram-bot/blob/main/bot/main.py)에서 확인할 수 있습니다.

:::

## 작동 중인 봇

드디어 해냈습니다! 이제 작동하는 봇이 생겼습니다. 테스트해 보세요!

봇을 실행하는 단계:

1. config.json\` 파일을 입력합니다.
2. main.py\`를 실행합니다.

모든 파일은 같은 폴더에 있어야 합니다. 봇을 시작하려면 `main.py` 파일을 실행해야 합니다. IDE 또는 터미널에서 다음과 같이 실행할 수 있습니다:

```
python main.py
```

오류가 있는 경우 터미널에서 확인할 수 있습니다. 코드에서 무언가를 놓쳤을 수도 있습니다.

작동 중인 봇의 예 [@AirDealerBot](https://t.me/AirDealerBot)

![봇](/img/tutorials/apiatb-bot.png)

## 참조

- 톤-풋스텝8](https://github.com/ton-society/ton-footsteps/issues/8)의 일환으로 톤을 위해 제작되었습니다.
- 레브 ([텔레그램 @Revuza](https://t.me/revuza), [깃허브의 레브제드](https://github.com/LevZed))
