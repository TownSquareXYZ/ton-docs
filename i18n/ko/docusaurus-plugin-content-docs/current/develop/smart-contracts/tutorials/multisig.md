---
description: 튜토리얼이 끝나면 TON 블록체인에 다중 서명 컨트랙트를 배포하게 됩니다.
---

# 간단한 다중서명 컨트랙트 만드는 방법

## 💡 개요

이 튜토리얼은 다중서명 컨트랙트를 배포하는 방법을 배우는 데 도움이 됩니다.\
(n, k)-다중 서명 컨트랙트는 개인 키 보유자가 n명인 다중 서명 지갑으로, 요청(일명 주문, 쿼리)이 최소 k명의 보유자의 서명을 수집하는 경우 메시지 전송 요청을 수락한다는 점을 기억해두세요.

원본 멀티서명 컨트랙트 코드와 akifoq의 업데이트를 기반으로 합니다:

- [원본 TON 블록체인 멀티시그 코드](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/multisig-code.fc)
- 멀티서명 작업을 위한 5개의 라이브러리가 있는 [akifoq/multisig](https://github.com/akifoq/multisig).

:::tip 시작 팁
다중서명을 처음 접하는 분을 위한 도움말: [다중서명 기술이란 무엇인가요? (동영상)](https://www.youtube.com/watch?v=yeLqe_gg2u0)
:::

## 📖 학습 내용

- 간단한 다중서명 지갑을 만들고 사용자 지정하는 방법.
- 라이트 클라이언트를 사용하여 다중서명 지갑을 배포하는 방법.
- 요청에 서명하고 블록체인에 메시지로 보내는 방법.

## ⚙ 환경 설정

여행을 시작하기 전에 환경을 점검하고 준비하세요.

- 설치](/개발/스마트-계약/환경/설치) 섹션에서 `func`, `fift`, `lite-client` 바이너리 및 `fiftlib`를 설치합니다.
- 리포지토리](https://github.com/akifoq/multisig)를 복제하고 CLI에서 해당 디렉토리를 엽니다.

```cpp
https://github.com/akifoq/multisig.git
cd ~/multisig
```

## 🚀 시작해보자!

1. 코드를 5로 컴파일합니다.
2. 다중 서명 소유자 키를 준비합니다.
3. 계약을 배포합니다.
4. 블록체인에 배포된 다중서명 지갑과 상호 작용합니다.

### 계약서 컴파일

Fift와 계약을 컴파일합니다:

```cpp
func -o multisig-code.fif -SPA stdlib.fc multisig-code.fc
```

### 멀티서명 소유자 키 준비

#### 참가자 키 만들기

키를 만들려면 실행해야 합니다:

```cpp
fift -s new-key.fif $KEY_NAME$
```

- 여기서 `KEY_NAME`은 개인키가 기록될 파일의 이름입니다.

예를 들어

```cpp
fift -s new-key.fif multisig_key
```

개인 키가 포함된 파일 'multisig_key.pk'를 받게 됩니다.

#### 공개 키 수집

또한 스크립트에서 공개 키를 형식으로 발급합니다:

```
Public key = Pub5XqPLwPgP8rtryoUDg2sadfuGjkT4DLRaVeIr08lb8CB5HW
```

"공개 키 = "\` 이후의 모든 항목은 어딘가에 저장해야 합니다!

'keys.txt' 파일에 저장합니다. 한 줄당 하나의 공개키가 중요합니다.

### 계약 배포

#### 라이트 클라이언트를 통한 배포

모든 키를 생성한 후에는 공개키를 텍스트 파일 'keys.txt'에 수집해야 합니다.

예를 들어

```bash
PubExXl3MdwPVuffxRXkhKN1avcGYrm6QgJfsqdf4dUc0an7/IA
PubH821csswh8R1uO9rLYyP1laCpYWxhNkx+epOkqwdWXgzY4
```

그 후에는 실행해야 합니다:

```cpp
fift -s new-multisig.fif 0 $WALLET_ID$ wallet $KEYS_COUNT$ ./keys.txt
```

- $WALLET_ID$`- 현재 키에 할당된 지갑 번호입니다. 동일한 키를 사용하는 새 지갑마다 고유한`$WALLET_ID$\`를 사용하는 것이 좋습니다.
- $KEYS_COUNT$\` - 확인에 필요한 키 수, 일반적으로 공개 키 수와 같습니다.

:::info wallet_id 설명
동일한 키(앨리스 키, 밥 키)로 여러 개의 지갑을 만들 수 있습니다. 앨리스와 밥이 이미 보물을 가지고 있다면 어떻게 해야 하나요? 여기서 `$WALLET_ID$`가 중요한 이유입니다.
:::

스크립트는 다음과 같이 출력됩니다:

```bash
new wallet address = 0:4bbb2660097db5c72dd5e9086115010f0f8c8501e0b8fef1fe318d9de5d0e501

(Saving address to file wallet.addr)

Non-bounceable address (for init): 0QBLuyZgCX21xy3V6QhhFQEPD4yFAeC4_vH-MY2d5dDlAbel

Bounceable address (for later access): kQBLuyZgCX21xy3V6QhhFQEPD4yFAeC4_vH-MY2d5dDlAepg

(Saved wallet creating query to file wallet-create.boc)
```

:::info
"공개 키는 48자 길이여야 합니다." 오류가 발생하는 경우, `keys.txt`에 유닉스 형식의 단어 줄 바꿈(LF)이 있는지 확인하세요. 예를 들어, 단어 줄 바꿈은 Sublime 텍스트 편집기를 통해 변경할 수 있습니다.
:::

:::tip
반송 가능한 주소는 지갑의 주소이므로 보관하는 것이 좋습니다.
:::

#### 계약 활성화

새로 생성된 _보물_에 약간의 TON을 보내야 합니다. 예를 들어 0.5톤입니다.

그런 다음 라이트 클라이언트를 실행해야 합니다:

```bash
lite-client -C global.config.json
```

:::info 글로벌.config.json`은 어디서 얻나요?
메인넷](https://ton.org/global-config.json) 또는 [테스트넷](https://ton.org/testnet-global.config.json)에 대한 새로운 설정 파일 `global.config.json\`을 얻을 수 있습니다.
:::

라이트 클라이언트를 시작한 후에는 라이트 클라이언트 콘솔에서 `time` 명령을 실행하여 연결이 성공했는지 확인하는 것이 가장 좋습니다:

```bash
time
```

자, 라이트 클라이언트가 작동합니다!

지갑을 배포해야 합니다. 명령을 실행합니다:

```
sendfile ./wallet-create.boc
```

그 후 지갑은 1분 이내에 작동할 준비가 됩니다.

### 다중서명 지갑과 상호 작용

#### 요청 만들기

먼저 메시지 요청을 만들어야 합니다:

```cpp
fift -s create-msg.fif $ADDRESS$ $AMOUNT$ $MESSAGE$
```

- $ADDRESS$\` - 코인을 보낼 주소
- `$AMOUNT$` - 코인 개수
- $MESSAGE$\` - 컴파일된 메시지의 파일 이름입니다.

예를 들어

```cpp
fift -s create-msg.fif EQApAj3rEnJJSxEjEHVKrH3QZgto_MQMOmk8l72azaXlY1zB 0.1 message
```

:::tip
트랜잭션에 댓글을 추가하려면 `-C comment` 속성을 사용하세요. 자세한 정보를 얻으려면 매개 변수 없이 *create-msg.fif* 파일을 실행하세요.
:::

#### 지갑 선택

다음으로 코인을 보낼 지갑을 선택해야 합니다:

```
fift -s create-order.fif $WALLET_ID$ $MESSAGE$ -t $AWAIT_TIME$
```

Where

- $WALLET_ID$\` - 이 다중 서명 컨트랙트가 지원하는 지갑의 ID입니다.
- $AWAIT_TIME$\` - 스마트 컨트랙트가 멀티서명 지갑 소유자의 요청에 대한 서명을 기다리는 시간(초)입니다.
- $MESSAGE$\` - 이전 단계에서 생성된 메시지 boc-file의 이름입니다.

:::info
요청이 서명하기 전에 `$AWAIT_TIME$`와 같은 시간이 지나면 요청이 만료됩니다. 평소와 같이 $AWAIT_TIME$ 은 두 시간(7200초)에 해당합니다.
:::

예를 들어

```
fift -s create-order.fif 0 message -t 7200
```

준비된 파일은 `order.boc`에 저장됩니다.

:::info
주문.boc\`를 키 소유자와 공유해야 하며, 키 소유자는 여기에 서명해야 합니다.
:::

#### 서명하기

서명하려면 다음을 수행해야 합니다:

```bash
fift -s add-signature.fif $KEY$ $KEY_INDEX$
```

- $KEY$\` - 서명할 개인키가 포함된 파일의 이름(확장자 없이)입니다.
- $KEY_INDEX$`-`keys.txt\`에서 주어진 키의 인덱스(0 기반)

예를 들어, `multisig_key.pk` 파일을 예로 들어보겠습니다:

```
fift -s add-signature.fif multisig_key 0
```

#### 메시지 만들기

모든 사람이 주문에 서명한 후에는 지갑에 대한 메시지로 바꾸고 다음 명령으로 다시 서명해야 합니다:

```
fift -s create-external-message.fif wallet $KEY$ $KEY_INDEX$
```

이 경우 지갑 소유자의 서명 하나만 있으면 충분합니다. 유효하지 않은 서명이 있는 컨트랙트를 공격할 수 없다는 것이 핵심입니다.

예를 들어

```
fift -s create-external-message.fif wallet multisig_key 0
```

#### TON 블록체인에 서명 보내기

그런 다음 라이트 클라이언트를 다시 시작해야 합니다:

```bash
lite-client -C global.config.json
```

그리고 마지막으로 사인을 보내고 싶어요! 그냥 달려가세요:

```bash
sendfile wallet-query.boc
```

다른 모든 사람이 서명하면 요청이 완료됩니다!

해냈어요, 하하! 🚀🚀🚀

## 다음 단계는 무엇인가요?

- [TON의 다중서명 지갑에 대해 자세히 알아보기](https://github.com/akifoq/multisig)에서 확인하세요.
