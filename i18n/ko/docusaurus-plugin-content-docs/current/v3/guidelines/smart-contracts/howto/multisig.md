---
description: 튜토리얼이 끝나면, 당신은 TON 블록체인에 다중서명 컨트랙트를 배포하게 될 것입니다.
---

# Fift로 간단한 멀티시그 컨트랙트 만들기

:::caution 고급 수준
이 정보는 **매우 로우레벨**입니다. 초보자가 이해하기 어려울 수 있으며 [fift](/v3/documentation/smart-contracts/fift/overview)를 이해하고자 하는 고급 사용자를 위해 설계되었습니다. 일상적인 작업에서는 fift 사용이 필요하지 않습니다.
:::

## 💡 개요

이 튜토리얼은 멀티시그 컨트랙트를 배포하는 방법을 배우는 데 도움이 됩니다.
(n, k)-멀티시그 컨트랙트는 n개의 개인 키 보유자가 있는 다중 서명 지갑으로, 요청(별칭 주문, 쿼리)이 보유자의 최소 k개 서명을 수집한 경우 메시지 전송 요청을 수락합니다.

원본 멀티시그 컨트랙트 코드와 akifoq의 업데이트 기반:

- [원본 TON 블록체인 multisig-code.fc](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/multisig-code.fc)
- 멀티시그 작업을 위한 fift 라이브러리가 있는 [akifoq/multisig](https://github.com/akifoq/multisig)

:::tip 초보자 팁
멀티시그를 처음 접하는 사람을 위한 영상: [멀티시그 기술이란? (비디오)](https://www.youtube.com/watch?v=yeLqe_gg2u0)
:::

## 📖 배우게 될 내용

- 간단한 멀티시그 지갑을 만들고 커스터마이즈하는 방법
- lite-client를 사용하여 멀티시그 지갑을 배포하는 방법
- 요청에 서명하고 블록체인에 메시지로 보내는 방법

## ⚙ 환경 설정

여정을 시작하기 전에 환경을 확인하고 준비하세요.

- [설치](/v3/documentation/archive/precompiled-binaries) 섹션에서 `func`, `fift`, `lite-client` 바이너리와 `fiftlib` 설치
- [저장소](https://github.com/akifoq/multisig) 클론하고 CLI에서 디렉토리 열기

```bash
git clone https://github.com/akifoq/multisig.git
cd ~/multisig
```

## 🚀 시작합시다!

1. 코드를 fift로 컴파일
2. 멀티시그 소유자 키 준비
3. 컨트랙트 배포
4. 블록체인에서 배포된 멀티시그 지갑과 상호작용

### 컨트랙트 컴파일

다음으로 컨트랙트를 Fift로 컴파일:

```cpp
func -o multisig-code.fif -SPA stdlib.fc multisig-code.fc
```

### 멀티시그 소유자 키 준비

#### 참가자 키 생성

키를 생성하려면 다음을 실행:

```cpp
fift -s new-key.fif $KEY_NAME$
```

- 여기서 `KEY_NAME`은 개인 키가 작성될 파일의 이름입니다.

예시:

```cpp
fift -s new-key.fif multisig_key
```

개인 키가 들어있는 `multisig_key.pk` 파일을 받게 됩니다.

#### 공개 키 수집

스크립트는 다음 형식의 공개 키도 출력합니다:

```
Public key = Pub5XqPLwPgP8rtryoUDg2sadfuGjkT4DLRaVeIr08lb8CB5HW
```

"Public key = " 이후의 모든 것을 저장해야 합니다!

`keys.txt` 파일에 저장하겠습니다. 한 줄에 하나의 공개 키, 이는 중요합니다.

### 컨트랙트 배포

#### lite-client를 통한 배포

모든 키를 생성한 후, 공개 키를 `keys.txt` 텍스트 파일에 수집해야 합니다.

예시:

```bash
PubExXl3MdwPVuffxRXkhKN1avcGYrm6QgJfsqdf4dUc0an7/IA
PubH821csswh8R1uO9rLYyP1laCpYWxhNkx+epOkqwdWXgzY4
```

그 다음 실행:

```cpp
fift -s new-multisig.fif 0 $WALLET_ID$ wallet $KEYS_COUNT$ ./keys.txt
```

- `$WALLET_ID$` - 현재 키에 할당된 지갑 번호. 동일한 키로 새 지갑마다 고유한 `$WALLET_ID$`를 사용하는 것이 좋습니다.
- `$KEYS_COUNT$` - 확인에 필요한 키 수, 보통 공개 키 수와 같음

:::info wallet_id 설명
같은 키(Alice 키, Bob 키)로 여러 지갑을 만들 수 있습니다. Alice와 Bob이 이미 보물을 가지고 있다면 어떻게 할까요? 이것이 `$WALLET_ID$`가 여기서 중요한 이유입니다.
:::

스크립트는 다음과 같은 내용을 출력합니다:

```bash
new wallet address = 0:4bbb2660097db5c72dd5e9086115010f0f8c8501e0b8fef1fe318d9de5d0e501

(Saving address to file wallet.addr)

Non-bounceable address (for init): 0QBLuyZgCX21xy3V6QhhFQEPD4yFAeC4_vH-MY2d5dDlAbel

Bounceable address (for later access): kQBLuyZgCX21xy3V6QhhFQEPD4yFAeC4_vH-MY2d5dDlAepg

(Saved wallet creating query to file wallet-create.boc)
```

:::info
"public key must be 48 characters long" 오류가 발생하면 `keys.txt`의 줄 바꿈이 unix 타입 - LF인지 확인하세요. 예를 들어 Sublime 텍스트 에디터를 통해 줄 바꿈을 변경할 수 있습니다.
:::

:::tip
Bounceable 주소를 보관하는 것이 좋습니다 - 이것이 지갑의 주소입니다.
:::

#### 컨트랙트 활성화

우리의 새로 생성된 _보물_에 일정량의 TON을 보내야 합니다. 예를 들어 0.5 TON. [@testgiver_ton_bot](https://t.me/testgiver_ton_bot)을 통해 테스트넷 코인을 보낼 수 있습니다.

그 다음 lite-client를 실행:

```bash
lite-client -C global.config.json
```

:::info `global.config.json`은 어디서 얻나요?
[메인넷](https://ton.org/global-config.json) 또는 [테스트넷](https://ton.org/testnet-global.config.json)에서 최신 config 파일 `global.config.json`을 얻을 수 있습니다.
:::

lite-client를 시작한 후, lite-client 콘솔에서 `time` 명령을 실행하여 연결이 성공했는지 확인하는 것이 좋습니다:

```bash
time
```

좋습니다, lite-client가 작동합니다!

그 다음 지갑을 배포해야 합니다. 명령 실행:

```
sendfile ./wallet-create.boc
```

그 후 1분 이내에 지갑이 작동할 준비가 됩니다.

### 멀티시그 지갑과 상호작용

#### 요청 생성

먼저 메시지 요청을 생성해야 합니다:

```cpp
fift -s create-msg.fif $ADDRESS$ $AMOUNT$ $MESSAGE$
```

- `$ADDRESS$` - 코인을 보낼 주소
- `$AMOUNT$` - 코인의 수
- `$MESSAGE$` - 컴파일된 메시지의 파일 이름

예시:

```cpp
fift -s create-msg.fif EQApAj3rEnJJSxEjEHVKrH3QZgto_MQMOmk8l72azaXlY1zB 0.1 message
```

:::tip
트랜잭션에 코멘트를 추가하려면 `-C comment` 속성을 사용하세요. 더 많은 정보를 얻으려면 *create-msg.fif* 파일을 매개변수 없이 실행하세요.
:::

#### 지갑 선택

다음으로 코인을 보낼 지갑을 선택해야 합니다:

```
fift -s create-order.fif $WALLET_ID$ $MESSAGE$ -t $AWAIT_TIME$
```

여기서

- `$WALLET_ID$` — 이 멀티시그 컨트랙트가 지원하는 지갑의 ID입니다.
- `$AWAIT_TIME$` — 스마트 컨트랙트가 요청에 대해 멀티시그 지갑 소유자의 서명을 기다릴 시간(초)입니다.
- `$MESSAGE$` — 이전 단계에서 생성된 메시지 boc-파일의 이름입니다.

:::info
요청 서명 전에 `$AWAIT_TIME$`과 같은 시간이 지나면 요청이 만료됩니다. 보통 $AWAIT_TIME$은 몇 시간(7200초)입니다
:::

예시:

```
fift -s create-order.fif 0 message -t 7200
```

준비된 파일은 `order.boc`에 저장됩니다

:::info
`order.boc`는 키 보유자들과 공유되어야 하며, 그들이 서명해야 합니다.
:::

#### 내 부분 서명

서명하려면 다음을 수행해야 합니다:

```bash
fift -s add-signature.fif $KEY$ $KEY_INDEX$
```

- `$KEY$` - 서명에 사용할 개인 키가 들어있는 파일의 이름(확장자 제외)
- `$KEY_INDEX$` - `keys.txt`에서 주어진 키의 인덱스(0부터 시작)

예를 들어, 우리의 `multisig_key.pk` 파일의 경우:

```
fift -s add-signature.fif multisig_key 0
```

#### 메시지 생성

모든 사람이 주문에 서명한 후, 지갑에 대한 메시지로 전환하고 다음 명령으로 다시 서명해야 합니다:

```
fift -s create-external-message.fif wallet $KEY$ $KEY_INDEX$
```

이 경우 지갑 소유자의 서명 하나만으로 충분합니다. 아이디어는 유효하지 않은 서명으로 컨트랙트를 공격할 수 없다는 것입니다.

예시:

```
fift -s create-external-message.fif wallet multisig_key 0
```

#### TON 블록체인에 서명 보내기

그 후 light client를 다시 시작해야 합니다:

```bash
lite-client -C global.config.json
```

마지막으로 우리의 서명을 보내고 싶습니다! 실행:

```bash
sendfile wallet-query.boc
```

다른 모든 사람이 요청에 서명했다면 완료될 것입니다!

해냈습니다, 하하! 🚀🚀🚀

## 다음은 무엇인가요?

- akifoq의 [TON의 멀티시그 지갑에 대해 더 읽기](https://github.com/akifoq/multisig)
