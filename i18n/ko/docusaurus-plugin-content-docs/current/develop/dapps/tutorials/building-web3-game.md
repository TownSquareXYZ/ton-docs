# 게임용 TON 블록체인

## 튜토리얼의 내용

이 튜토리얼에서는 게임에 TON 블록체인을 추가하는 방법을 살펴보겠습니다. 이 예제에서는 Phaser로 작성된 Flappy Bird 클론을 사용하여 단계별로 GameFi 기능을 추가하겠습니다. 튜토리얼에서는 가독성을 높이기 위해 짧은 코드 조각과 의사 코드를 사용할 것입니다. 또한 이해를 돕기 위해 실제 코드 블록에 대한 링크를 제공할 것입니다. 전체 구현은 [데모 리포지토리](https://github.com/ton-community/flappy-bird)에서 확인할 수 있습니다.

![게임파이 기능이 없는 플래피 버드 게임](/img/tutorials/gamefi-flappy/no-gamefi-yet.png)

다음 사항을 구현할 예정입니다:

- 업적. SBT](https://docs.ton.org/learn/glossary#sbt)로 사용자에게 보상을 제공하세요. 업적 시스템은 사용자 참여도를 높일 수 있는 훌륭한 도구입니다.
- 게임 화폐. TON 블록체인에서는 나만의 토큰(제톤)을 쉽게 출시할 수 있습니다. 토큰은 게임 내 경제를 만드는 데 사용할 수 있습니다. 사용자는 게임 코인을 획득하여 나중에 사용할 수 있습니다.
- 게임 상점. 게임 내 화폐 또는 TON 코인을 사용하여 게임 내 아이템을 구매할 수 있는 기능을 제공할 예정입니다.

## 준비 사항

### GameFi SDK 설치

먼저 게임 환경을 설정합니다. 이를 위해서는 `assets-sdk`를 설치해야 합니다. 이 패키지는 개발자가 블록체인을 게임에 통합하는 데 필요한 모든 것을 준비하도록 설계되었습니다. 이 라이브러리는 CLI 또는 Node.js 스크립트에서 사용할 수 있습니다. 이 튜토리얼에서는 CLI 접근 방식을 고수합니다.

```sh
npm install -g @ton-community/assets-sdk@beta
```

### 마스터 지갑 만들기

다음으로 마스터 지갑을 만들어야 합니다. 마스터 지갑은 제튼, 컬렉션, NFT, SBT를 발행하고 지불을 받는 데 사용할 지갑입니다.

```sh
assets-cli setup-env
```

몇 가지 질문을 받게 됩니다:

| 필드         | 힌트                                                                                                                                                                     |
| :--------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 네트워크       | 테스트 게임인 만큼 '테스트넷'을 선택합니다.                                                                                                                              |
| 유형         | 마스터 지갑으로 사용하기에 가장 성능이 좋은 'high-load-v2' 유형의 지갑을 선택합니다.                                                                                                 |
| 스토리지       | 저장소는 `NFT`/`SB`T 파일을 저장하는 데 사용됩니다. Amazon S3`(중앙 집중식) 또는 `Pinata`(탈중앙화).  이 튜토리얼에서는 분산형 스토리지가 Web3 게임을 더 잘 설명할 수 있으므로 `피나타\`를 사용하겠습니다. |
| IPFS 게이트웨이 | 에셋 메타데이터를 로드할 서비스: `pinata`, `ipfs.io` 또는 기타 서비스 URL을 입력합니다.                                                                           |

스크립트는 생성된 지갑 상태를 확인하기 위해 열 수 있는 링크를 출력합니다.

![존재하지 않는 상태의 새 지갑](/img/tutorials/gamefi-flappy/wallet-nonexist-status.png)

보시다시피 지갑은 아직 실제로 생성되지 않았습니다. 지갑이 실제로 생성되려면 지갑에 자금을 입금해야 합니다. 실제 시나리오에서는 지갑 주소를 사용하여 원하는 방식으로 지갑을 입금할 수 있습니다. 저희의 경우 [테스트 제공자 TON 봇](https://t.me/testgiver_ton_bot)을 사용하겠습니다. 테스트 TON 코인 5개를 받으려면 봇을 열어주세요.

잠시 후 지갑에 5 TON이 표시되고 상태가 `유닛`이 되었습니다. 지갑이 준비되었습니다. 첫 번째 사용 후 상태가 '활성'으로 변경됩니다.

![충전 후 지갑 상태](/img/tutorials/gamefi-flappy/wallet-nonexist-status.png)

### 게임 내 화폐 발행

게임 내 화폐를 생성하여 사용자에게 보상할 예정입니다:

```sh
assets-cli deploy-jetton
```

몇 가지 질문을 받게 됩니다:

| 필드  | 힌트                                                                                                                                                                                                                           |
| :-- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 이름  | 토큰 이름(예: `플래피 제튼`).                                                                                                                                                       |
| 설명  | 토큰 설명, 예를 들어: Flappy Bird 세계관의 생동감 넘치는 디지털 토큰입니다.                                                                                                                                            |
| 이미지 | 준비된 [제톤 로고](https://raw.githubusercontent.com/ton-community/flappy-bird/ca4b6335879312a9b94f0e89384b04cea91246b1/scripts/tokens/flap/image.png)를 다운로드하고 파일 경로를 지정합니다. 물론 어떤 이미지든 사용할 수 있습니다. |
| 기호  | '플랩'을 입력하거나 사용하려는 약어를 입력합니다.                                                                                                                                                                                 |
| 소수점 | 점 뒤에 0이 몇 개 있는지 입력합니다. 이 경우에는 '0'으로 설정합니다.                                                                                                                                                   |

스크립트는 생성된 제톤 상태를 확인하기 위해 열 수 있는 링크를 출력합니다. 상태는 '활성'입니다. 지갑 상태는 `유닛`에서 `활성`으로 변경됩니다.

![게임 내 화폐/제트톤](/img/tutorials/gamefi-flappy/jetton-active-status.png)

### SBT용 컬렉션 만들기

예를 들어, 데모 게임에서는 첫 번째와 다섯 번째 게임에 대해 사용자에게 보상을 제공합니다. 따라서 사용자가 첫 번째와 다섯 번째 플레이 등 관련 조건을 달성하면 두 개의 컬렉션을 발행하여 그 안에 SBT를 넣을 것입니다:

```sh
assets-cli deploy-nft-collection
```

| 필드  | 첫 번째 게임                                                                                                                                               | 다섯 번째 게임                                                                                                                                              |
| :-- | :---------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| 유형  | `sbt`                                                                                                                                                 | `sbt`                                                                                                                                                 |
| 이름  | Flappy 첫 비행                                                                                                                                           | 플래피 하이 파이버                                                                                                                                            |
| 설명  | 플리피 버드 게임에서의 첫 여정을 기념하세요!                                                                                                                             | 플랩피 하이파이버 NFT로 꾸준한 플레이를 축하하세요!                                                                                                                        |
| 이미지 | 여기에서 [이미지](https://raw.githubusercontent.com/ton-community/flappy-bird/article-v1/scripts/tokens/first-time/image.png)를 다운로드할 수 있습니다. | 여기에서 [이미지](https://raw.githubusercontent.com/ton-community/flappy-bird/article-v1/scripts/tokens/five-times/image.png)를 다운로드할 수 있습니다. |

우리는 완전히 준비되었습니다. 이제 로직 구현으로 넘어가 보겠습니다.

## 지갑 연결

모든 것은 사용자가 지갑을 연결하는 것에서 시작됩니다. 이제 지갑 연결 연동을 추가해 보겠습니다. 클라이언트 측에서 블록체인을 사용하려면 Phaser용 GameFi SDK를 설치해야 합니다:

```sh
npm install --save @ton/phaser-sdk@beta
```

이제 GameFi SDK를 설정하고 인스턴스를 생성해 보겠습니다:

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

> 초기화 옵션에 대해 자세히 알아보려면 [라이브러리 문서](https://github.com/ton-org/game-engines-sdk)를 참조하세요.

> 톤커넥트-매니페스트.json\`이 무엇인지 알아보려면 톤커넥트 [매니페스트 설명](https://docs.ton.org/develop/dapps/ton-connect/manifest)을 확인하시기 바랍니다.

이제 지갑 연결 버튼을 만들 준비가 되었습니다. 페이저에서 연결 버튼이 포함될 UI 장면을 만들어 보겠습니다:

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

> 연결 버튼](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/client/src/connect-wallet-ui.ts#L82)과 [UI 장면](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/client/src/connect-wallet-ui.ts#L45)을 만드는 방법을 읽어보세요.

사용자가 지갑을 연결하거나 연결 해제하는 시점을 확인하려면 다음 코드를 사용하겠습니다:

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

> 더 복잡한 시나리오에 대해 알아보려면 [지갑 연결 흐름](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/client/src/index.ts#L16)의 전체 구현을 확인하시기 바랍니다.

게임 UI 관리](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/client/src/index.ts#L50)가 어떻게 구현되는지 읽어보세요.

이제 사용자 지갑이 연결되었으니 앞으로 나아갈 수 있습니다.

![지갑 연결 버튼](/img/tutorials/gamefi-flappy/wallet-connect-button.png)
![지갑 연결 확인](/img/tutorials/gamefi-flappy/wallet-connect-confirmation.png)
![지갑 연결됨](/img/tutorials/gamefi-flappy/wallet-connected.png)

## 업적 및 보상 구현

업적과 보상 시스템을 구현하려면 사용자 시도당 요청할 엔드포인트를 준비해야 합니다.

### `/played` 엔드포인트

다음을 수행해야 하는 엔드포인트 `/played`를 만들어야 합니다:

- 는 앱 실행 시 사용자 지갑 주소와 텔레그램 초기 데이터가 포함된 본문을 미니앱으로 전달받습니다. 초기 데이터를 파싱하여 인증 데이터를 추출하고, 사용자가 요청을 대신해서만 전송하는지 확인해야 합니다.
- 엔드포인트는 사용자가 플레이한 게임 수를 계산하고 저장해야 합니다.
- 엔드포인트는 사용자의 첫 번째 또는 다섯 번째 게임인지 확인하고, 그렇다면 사용자에게 관련 SBT를 보상해야 합니다.
- 엔드포인트는 각 게임에 대해 사용자에게 플랩 1개를 보상해야 합니다.

> 재생된 엔드포인트](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/server/src/index.ts#L197) 코드를 읽습니다.

### 요청 `/played` 엔드포인트

새가 파이프에 부딪히거나 떨어질 때마다 클라이언트 코드는 올바른 몸체를 전달하는 `/played` 엔드포인트를 호출해야 합니다:

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

> 제출 플레이어 함수](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/client/src/game-scene.ts#L10) 코드를 읽습니다.

첫 번째 게임을 플레이하고 플랩 토큰과 SBT를 보상으로 받도록 하겠습니다. 플레이 버튼을 클릭하고 파이프를 한두 개 통과한 다음 튜브에 부딪히세요. 좋아요, 모든 것이 작동합니다!

![토큰 및 SBT로 보상받기](/img/tutorials/gamefi-flappy/sbt-rewarded.png)

4번 더 플레이하여 두 번째 SBT를 획득한 다음 지갑인 TON 스페이스를 엽니다. 여기 수집품이 있습니다:

![월렛에서 SBT로 달성한 업적](/img/tutorials/gamefi-flappy/sbts-in-wallet.png)

## 게임 상점 구현

게임 내 상점을 만들려면 두 가지 구성 요소가 필요합니다. 첫 번째는 사용자 구매에 대한 정보를 제공하는 엔드포인트입니다. 두 번째는 사용자 트랜잭션을 감시하고 소유자에게 게임 속성을 할당하는 글로벌 루프입니다.

### 구매\` 엔드포인트

엔드포인트는 다음을 수행합니다:

- 텔레그램 미니앱 초기 데이터로 '인증'받기 매개변수를 받습니다.
- 엔드포인트는 사용자가 구매한 아이템을 가져와 아이템 목록으로 응답합니다.

> 구매](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/server/src/index.ts#L303) 엔드포인트 코드를 읽습니다.

### 구매 루프

사용자가 언제 결제하는지 알기 위해서는 마스터 지갑 트랜잭션을 살펴봐야 합니다. 모든 트랜잭션에는 `userId`:`itemId` 메시지가 포함되어야 합니다. 마지막으로 처리된 트랜잭션을 기억하고, 새로운 트랜잭션만 가져오고, `userId`와 `itemId`를 사용해 구매한 자산을 사용자에게 할당하고, 마지막 트랜잭션 해시를 다시 작성합니다. 이것은 무한 루프에서 작동합니다.

> 구매 루프](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/server/src/index.ts#L110) 코드를 읽습니다.

### 상점의 클라이언트 측

클라이언트 측에는 쇼핑 버튼이 있습니다.

![상점 입력 버튼](/img/tutorials/gamefi-flappy/shop-enter-button.png)

사용자가 버튼을 클릭하면 상점 장면이 열립니다. 상점 장면에는 사용자가 구매할 수 있는 품목 목록이 포함되어 있습니다. 각 품목에는 가격과 구매 버튼이 있습니다. 사용자가 구매 버튼을 클릭하면 구매가 이루어집니다.

상점을 열면 구매한 아이템이 10초마다 로드되고 업데이트됩니다:

```typescript
// inside of fetchPurchases function
await fetch('http://localhost:3000/purchases?auth=' + encodeURIComponent((window as any).Telegram.WebApp.initData))
// watch for purchases
setTimeout(() => { fetchPurchases() }, 10000)
```

> 쇼샵 함수](https://github.com/ton-community/flappy-bird/blob/article-v1/workspaces/client/src/ui.ts#L191) 코드를 읽습니다.

이제 구매 자체를 구현해야 합니다. 이를 위해 먼저 GameFi SDK 인스턴스를 생성한 다음 `buyWithJetton` 메서드를 사용하겠습니다:

```typescript
gameFi.buyWithJetton({
    amount: BigInt(price),
    forwardAmount: BigInt(1),
    forwardPayload: (window as any).Telegram.WebApp.initDataUnsafe.user.id + ':' + itemId
});
```

![게임 소품 구매](/img/tutorials/gamefi-flappy/purchase-item.png)

![속성 사용 준비 완료](/img/tutorials/gamefi-flappy/purchase-done.png)

TON 코인으로 결제할 수도 있습니다:

```typescript
import { toNano } from '@ton/phaser-sdk'

gameFi.buyWithTon({
    amount: toNano(0.5),
    comment: (window as any).Telegram.WebApp.initDataUnsafe.user.id + ':' + 1
});
```

## 후기

이번 튜토리얼은 여기까지입니다! 기본적인 GameFi 기능에 대해 살펴보았지만, SDK는 플레이어 간 전송, NFT와 컬렉션을 작동시키는 유틸리티 등 더 많은 기능을 제공합니다. 앞으로 더 많은 기능을 제공할 예정입니다.

GameFi에서 사용할 수 있는 모든 기능에 대해 자세히 알아보려면 [ton-org/game-engines-sdk](https://github.com/ton-org/game-engines-sdk) 및 [@ton-community/assets-sdk](https://github.com/ton-community/assets-sdk) 문서를 참조하세요.

토론](https://github.com/ton-org/game-engines-sdk/discussions)에서 여러분의 의견을 알려주세요!

전체 구현은 [flappy-bird](https://github.com/ton-community/flappy-bird) 리포지토리에서 확인할 수 있습니다.
