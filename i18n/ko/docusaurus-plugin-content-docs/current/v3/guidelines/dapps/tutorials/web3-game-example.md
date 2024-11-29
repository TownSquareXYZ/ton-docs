# TON 블록체인을 활용한 게임 개발

## 튜토리얼 내용

이 튜토리얼에서는 게임에 TON 블록체인을 추가하는 방법을 알아보겠습니다. 예제로, Phaser로 작성된 Flappy Bird 클론을 사용하고 단계별로 GameFi 기능을 추가할 것입니다. 이해하기 쉽도록 튜토리얼에서는 짧은 코드 조각과 의사코드를 사용할 것입니다. 또한 더 잘 이해할 수 있도록 실제 코드 블록에 대한 링크도 제공합니다. 전체 구현은 [데모 저장소](https://github.com/ton-community/flappy-bird)에서 확인할 수 있습니다.

![GameFi 기능이 없는 Flappy Bird 게임](/img/tutorials/gamefi-flappy/no-gamefi-yet.png)

다음 기능들을 구현할 예정입니다:

- 업적. 사용자에게 [SBT](/v3/concepts/glossary#sbt)로 보상합시다. 업적 시스템은 사용자 참여를 높이는 훌륭한 도구입니다.
- 게임 화폐. TON 블록체인에서는 자체 토큰(jetton)을 쉽게 발행할 수 있습니다. 토큰은 게임 내 경제를 만드는 데 사용될 수 있습니다. 사용자는 게임 코인을 획득하여 나중에 사용할 수 있습니다.
- 게임 상점. 사용자가 게임 내 화폐나 TON 코인을 사용하여 게임 내 아이템을 구매할 수 있게 할 것입니다.

## 준비사항

### GameFi SDK 설치

먼저, 게임 환경을 설정하겠습니다. 이를 위해 `assets-sdk`를 설치해야 합니다. 이 패키지는 개발자가 블록체인을 게임에 통합하는 데 필요한 모든 것을 준비하도록 설계되었습니다. 이 라이브러리는 CLI나 Node.js 스크립트에서 사용할 수 있습니다. 이 튜토리얼에서는 CLI 방식을 사용하겠습니다.

```sh
npm install -g @ton-community/assets-sdk@beta
```

### 마스터 지갑 생성

다음으로, 마스터 지갑을 생성해야 합니다. 마스터 지갑은 jetton, 컬렉션, NFT, SBT를 발행하고 결제를 받는 데 사용할 지갑입니다.

```sh
assets-cli setup-env
```

몇 가지 질문을 받게 됩니다:

| 필드           | 힌트                                                                                                                                                                                                                                          |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Network      | 테스트 게임이므로 `testnet`을 선택하세요.                                                                                                                                                                                                 |
| Type         | 마스터 지갑으로 사용하기에 가장 좋고 성능이 좋은 옵션이므로 `highload-v2` 타입을 선택하세요.                                                                                                                                                                  |
| Storage      | `NFT`/`SBT` 파일을 저장하는 데 사용될 스토리지입니다. `Amazon S3`(중앙화) 또는 `Pinata`(탈중앙화) 중에서 선택할 수 있습니다. Web3 게임에 더 적합한 탈중앙화 스토리지를 사용하기 위해 이 튜토리얼에서는 `Pinata`를 사용하겠습니다. |
| IPFS gateway | 자산 메타데이터를 로드할 서비스: `pinata`, `ipfs.io` 또는 다른 서비스 URL을 입력하세요.                                                                                                                                                |

스크립트는 생성된 지갑 상태를 볼 수 있는 링크를 출력합니다.

![Nonexist 상태의 새 지갑](/img/tutorials/gamefi-flappy/wallet-nonexist-status.png)

보시다시피 지갑은 아직 실제로 생성되지 않았습니다. 지갑이 실제로 생성되려면 약간의 자금을 입금해야 합니다. 실제 시나리오에서는 지갑 주소를 사용하여 원하는 방식으로 입금할 수 있습니다. 우리의 경우 [Testgiver TON Bot](https://t.me/testgiver_ton_bot)을 사용할 것입니다. 5개의 테스트 TON 코인을 받기 위해 봇을 열어주세요.

잠시 후 지갑에 5 TON이 표시되고 상태가 `Uninit`으로 변경됩니다. 지갑이 준비되었습니다. 첫 사용 후에는 상태가 `Active`로 변경됩니다.

![충전 후 지갑 상태](/img/tutorials/gamefi-flappy/wallet-nonexist-status.png)

### 게임 내 화폐 발행

사용자에게 보상할 게임 내 화폐를 만들어보겠습니다:

```sh
assets-cli deploy-jetton
```

몇 가지 질문을 받게 됩니다:

| 필드          | 힌트                                                                                                                                                                                                                                |
| :---------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name        | 토큰 이름, 예: `Flappy Jetton`                                                                                                                                                                                         |
| Description | 토큰 설명, 예: A vibrant digital token from the Flappy Bird universe.                                                                                                                                  |
| Image       | 준비된 [jetton 로고](https://raw.githubusercontent.com/ton-community/flappy-bird/ca4b6335879312a9b94f0e89384b04cea91246b1/scripts/tokens/flap/image.png)를 다운로드하고 파일 경로를 지정하세요. 물론 다른 이미지를 사용할 수도 있습니다. |
| Symbol      | `FLAP` 또는 사용하고 싶은 약어를 입력하세요.                                                                                                                                                                                      |
| Decimals    | 화폐의 소수점 이하 자릿수입니다. 우리의 경우 `0`으로 하겠습니다.                                                                                                                                                            |

스크립트는 생성된 jetton 상태를 볼 수 있는 링크를 출력합니다. 상태는 `Active`가 될 것입니다. 지갑 상태도 `Uninit`에서 `Active`로 변경됩니다.

![게임 내 화폐 / jetton](/img/tutorials/gamefi-flappy/jetton-active-status.png)

### SBT를 위한 컬렉션 생성

예시로, 데모 게임에서는 첫 번째와 다섯 번째 게임에 대해 사용자에게 보상을 할 것입니다. 따라서 사용자가 관련 조건(첫 번째와 다섯 번째 게임 플레이)을 달성했을 때 SBT를 넣을 두 개의 컬렉션을 발행할 것입니다:

```sh
assets-cli deploy-nft-collection
```

| 필드          | 첫 번째 게임                                                                                                                         | 다섯 번째 게임                                                                                                                        |
| :---------- | :------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------ |
| Type        | `sbt`                                                                                                                           | `sbt`                                                                                                                           |
| Name        | Flappy First Flight                                                                                                             | Flappy High Fiver                                                                                                               |
| Description | 당신의 첫 Flappy Bird 게임 여정을 기념합니다!                                                                                                 | 다섯 번째 플레이를 기념하는 Flappy High Fiver NFT입니다!                                                                                       |
| Image       | [이미지](https://raw.githubusercontent.com/ton-community/flappy-bird/article-v1/scripts/tokens/first-time/image.png)를 다운로드할 수 있습니다 | [이미지](https://raw.githubusercontent.com/ton-community/flappy-bird/article-v1/scripts/tokens/five-times/image.png)를 다운로드할 수 있습니다 |

모든 준비가 되었습니다. 이제 로직 구현으로 넘어가겠습니다.

## 지갑 연결하기

모든 것은 사용자가 자신의 지갑을 연결하는 것에서 시작됩니다. 지갑 연결 통합을 추가해보겠습니다. 클라이언트 측에서 블록체인 작업을 하기 위해 Phaser용 GameFi SDK를 설치해야 합니다:

```sh
npm install --save @ton/phaser-sdk@beta
```

이제 GameFi SDK를 설정하고 인스턴스를 생성해보겠습니다:

```typescript
import { GameFi } from '@ton/phaser-sdk'

const gameFi = await GameFi.create({
    network: 'testnet'
    connector: {
        // if tonconnect-manifest.json is placed in the root you can skip this option
        manifestUrl: '/assets/tonconnect-manifest.json',
        actionsConfiguration: {
            // address of your Telegram Mini App to return to after the wallet is connected
            // url you provided to BothFather during the app creation process
            // to read more please read https://github.com/ton-community/flappy-bird#telegram-bot--telegram-web-app
            twaReturnUrl: URL_YOU_ASSIGNED_TO_YOUR_APP
        },
        contentResolver: {
            // some NFT marketplaces don't support CORS, so we need to use a proxy
            // you are able to use any format of the URL, %URL% will be replaced with the actual URL
            urlProxy: `${YOUR_BACKEND_URL}/${PROXY_URL}?url=%URL%`
        },
        // where in-game purchases come to
        merchant: {
            // in-game jetton purchases (FLAP)
            // use address you got running `assets-cli deploy-jetton`
            jettonAddress: FLAP_ADDRESS,
            // in-game TON purchases
            // use master wallet address you got running `assets-cli setup-env`
            tonAddress: MASTER_WALLET_ADDRESS
        }
    },

})
```

> 초기화 옵션에 대해 자세히 알아보려면 [라이브러리 문서](https://github.com/ton-org/game-engines-sdk)를 읽어보세요.

> `tonconnect-manifest.json`이 무엇인지 알아보려면 ton-connect [매니페스트 설명](/v3/guidelines/ton-connect/guidelines/creating-manifest)을 확인하세요.

이제 지갑 연결 버튼을 만들 준비가 되었습니다. Phaser에서 연결 버튼이 포함될 UI 씬을 만들어보겠습니다:

```typescript
class UiScene extends Phaser.Scene {
    // receive gameFi instance via constructor
    private gameFi: GameFi;

    create() {
        this.button = this.gameFi.createConnectButton({
            scene: this,
            // you can calculate the position for the button in your UI scene
            x: 0,
            y: 0,
            button: {
                onError: (error) => {
                    console.error(error)
                }
                // other options, read the docs
            }
        })
    }
}
```

> [connect 버튼](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/client/src/connect-wallet-ui.ts#L82)과 [UI 씬](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/client/src/connect-wallet-ui.ts#L45)을 만드는 방법을 읽어보세요.

사용자가 지갑을 연결하거나 연결 해제할 때를 감시하기 위해 다음 코드를 사용해보겠습니다:

```typescript
function onWalletChange(wallet: Wallet | null) {
    if (wallet) {
        // wallet is ready to use
    } else {
        // wallet is disconnected
    }
}
const unsubscribe = gameFi.onWalletChange(onWalletChange)
```

> 더 복잡한 시나리오에 대해서는 [지갑 연결 흐름](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/client/src/index.ts#L16)의 전체 구현을 확인하세요.

[게임 UI 관리](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/client/src/index.ts#L50)가 어떻게 구현될 수 있는지 읽어보세요.

이제 사용자의 지갑이 연결되었고 계속 진행할 수 있습니다.

![지갑 연결 버튼](/img/tutorials/gamefi-flappy/wallet-connect-button.png)
![지갑 연결 확인](/img/tutorials/gamefi-flappy/wallet-connect-confirmation.png)
![지갑이 연결됨](/img/tutorials/gamefi-flappy/wallet-connected.png)

## 업적 & 보상 구현하기

업적과 보상 시스템을 구현하기 위해 사용자가 시도할 때마다 요청될 엔드포인트를 준비해야 합니다.

### `/played` 엔드포인트

`/played` 엔드포인트를 만들어야 하며 다음을 수행해야 합니다:

- 사용자 지갑 주소와 앱 실행 중 미니 앱에 전달된 텔레그램 초기 데이터가 포함된 본문을 받습니다. 초기 데이터는 인증 데이터를 추출하고 사용자가 자신을 대신해서만 요청을 보내는지 확인하기 위해 파싱되어야 합니다.
- 엔드포인트는 사용자가 플레이한 게임의 수를 계산하고 저장해야 합니다.
- 엔드포인트는 사용자의 첫 번째 또는 다섯 번째 게임인지 확인하고 그렇다면 관련 SBT로 보상해야 합니다.
- 엔드포인트는 각 게임마다 1 FLAP으로 사용자에게 보상해야 합니다.

> [/played 엔드포인트](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/server/src/index.ts#L197) 코드를 읽어보세요.

### `/played` 엔드포인트 요청하기

새가 파이프에 부딪히거나 떨어질 때마다 클라이언트 코드는 올바른 본문을 포함하여 `/played` 엔드포인트를 호출해야 합니다:

```typescript
async function submitPlayed(endpoint: string, walletAddress: string) {
    return await (await fetch(endpoint + '/played', {
        body: JSON.stringify({
            tg_data: (window as any).Telegram.WebApp.initData,
            wallet: walletAddress
        }),
        headers: {
            'content-type': 'application/json'
        },
        method: 'POST'
    })).json()
}

const playedInfo = await submitPlayed('http://localhost:3001', wallet.account.address);
```

> [submitPlayer 함수](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/client/src/game-scene.ts#L10) 코드를 읽어보세요.

첫 번째로 플레이하고 FLAP 토큰과 SBT로 보상받을 수 있는지 확인해보겠습니다. Play 버튼을 클릭하고, 한두 개의 파이프를 통과한 다음 관에 부딪혀보세요. 좋습니다, 모든 것이 작동합니다!

![토큰과 SBT로 보상받음](/img/tutorials/gamefi-flappy/sbt-rewarded.png)

두 번째 SBT를 받기 위해 4번 더 플레이한 다음, 지갑, TON Space를 열어보세요. 여기 당신의 수집품이 있습니다:

![지갑의 업적으로서의 SBT](/img/tutorials/gamefi-flappy/sbts-in-wallet.png)

## 게임 상점 구현하기

게임 내 상점을 갖기 위해서는 두 가지 구성 요소가 필요합니다. 첫 번째는 사용자의 구매 정보를 제공하는 엔드포인트입니다. 두 번째는 사용자 트랜잭션을 감시하고 게임 속성을 소유자에게 할당하는 전역 루프입니다.

### `/purchases` 엔드포인트

이 엔드포인트는 다음을 수행합니다:

- 텔레그램 미니 앱 초기 데이터가 있는 `auth` get 파라미터를 받습니다.
- 엔드포인트는 사용자가 구매한 아이템을 가져와 아이템 목록으로 응답합니다.

> [/purchases](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/server/src/index.ts#L303) 엔드포인트 코드를 읽어보세요.

### 구매 루프

사용자가 결제를 할 때를 알기 위해 마스터 지갑 트랜잭션을 감시해야 합니다. 각 트랜잭션에는 `userId`:`itemId` 메시지가 포함되어야 합니다. 마지막으로 처리된 트랜잭션을 기억하고, 새로운 것들만 가져오고, `userId`와 `itemId`를 사용하여 구매한 속성을 사용자에게 할당하고, 마지막 트랜잭션 해시를 다시 쓸 것입니다. 이는 무한 루프로 작동할 것입니다.

> [구매 루프](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/server/src/index.ts#L110) 코드를 읽어보세요.

### 상점의 클라이언트 사이드

클라이언트 측에는 Shop 버튼이 있습니다.

![상점 입장 버튼](/img/tutorials/gamefi-flappy/shop-enter-button.png)

사용자가 버튼을 클릭하면 상점 씬이 열립니다. 상점 씬에는 사용자가 구매할 수 있는 아이템 목록이 포함되어 있습니다. 각 아이템에는 가격과 Buy 버튼이 있습니다. 사용자가 Buy 버튼을 클릭하면 구매가 이루어집니다.

상점을 열면 구매한 아이템을 로드하고 10초마다 업데이트하는 것이 트리거됩니다:

```typescript
// inside of fetchPurchases function
await fetch('http://localhost:3000/purchases?auth=' + encodeURIComponent((window as any).Telegram.WebApp.initData))
// watch for purchases
setTimeout(() => { fetchPurchases() }, 10000)
```

> [showShop 함수](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/client/src/ui.ts#L191) 코드를 읽어보세요.

이제 구매 자체를 구현해야 합니다. 이를 위해 먼저 GameFi SDK 인스턴스를 만들고 `buyWithJetton` 메소드를 사용할 것입니다:

```typescript
gameFi.buyWithJetton({
    amount: BigInt(price),
    forwardAmount: BigInt(1),
    forwardPayload: (window as any).Telegram.WebApp.initDataUnsafe.user.id + ':' + itemId
});
```

![구매할 게임 속성](/img/tutorials/gamefi-flappy/purchase-item.png)
![구매 확인](/img/tutorials/gamefi-flappy/purchase-confirmation.png)
![속성 사용 준비 완료](/img/tutorials/gamefi-flappy/purchase-done.png)

TON 코인으로도 결제할 수 있습니다:

```typescript
import { toNano } from '@ton/phaser-sdk'

gameFi.buyWithTon({
    amount: toNano(0.5),
    comment: (window as any).Telegram.WebApp.initDataUnsafe.user.id + ':' + 1
});
```

## 마무리

이것으로 이 튜토리얼은 끝났습니다! 기본적인 GameFi 기능들을 살펴보았지만, SDK는 플레이어 간의 전송, NFT와 컬렉션 작업을 위한 유틸리티 등 더 많은 기능을 제공합니다. 앞으로 더 많은 기능을 제공할 예정입니다.

사용할 수 있는 모든 GameFi 기능에 대해 알아보려면 [ton-org/game-engines-sdk](https://github.com/ton-org/game-engines-sdk)와 [@ton-community/assets-sdk](https://github.com/ton-community/assets-sdk)의 문서를 읽어보세요.

[Discussions](https://github.com/ton-org/game-engines-sdk/discussions)에서 여러분의 생각을 들려주세요!

전체 구현은 [flappy-bird](https://github.com/ton-community/flappy-bird) 저장소에서 확인할 수 있습니다.
