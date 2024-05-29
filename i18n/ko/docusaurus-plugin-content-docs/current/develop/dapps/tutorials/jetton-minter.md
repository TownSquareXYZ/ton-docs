# 첫 번째 제톤 만들기

환영합니다, 개발자님! 이곳에 오게 되어 반갑습니다. 👋

이번 아티클에서는 TON에서 첫 번째 대체 가능한 토큰(제톤)을 생성하는 방법을 알려드리겠습니다.

제톤을 발행하기 위해 [TON Minter](https://minter.ton.org/) 브라우저 서비스를 사용할 것입니다.

## 📖 학습 내용

이 글에서는 방법을 알아보세요:

- 브라우저를 사용하여 Jetton 배포
- 토큰 커스터마이징
- 토큰 관리 및 사용
- 토큰 매개변수 편집

## 📌 시작하기 전에 준비하기

1. 먼저 [Tonhub](https://ton.app/wallets/tonhub-wallet) / [Tonkeeper](https://ton.app/wallets/tonkeeper) 지갑 또는 [Chrome 확장 프로그램](https://ton.app/wallets/chrome-plugin) 또는 기타 서비스에서 지원되는 지갑이 있어야 합니다.
2. 블록체인 수수료를 충당하려면 잔액에 0.25톤코인 + 자금이 있어야 합니다.

:::tip 시작 팁
~이 튜토리얼에서는 0.5톤이면 충분합니다.
:::

## 🚀 시작해보자!

웹 브라우저를 사용하여 [톤민터](https://minter.ton.org/) 서비스를 엽니다.

![이미지](/img/tutorials/jetton/jetton-main-page.png)

### 브라우저를 사용하여 Jetton 배포

#### 지갑 연결

'지갑 연결' 버튼을 클릭하여 [Tonhub](https://ton.app/wallets/tonhub-wallet) 지갑 또는 [크롬 확장 프로그램](https://ton.app/wallets/chrome-plugin) 또는 아래 지갑 중 다른 지갑을 연결합니다.

#### ![이미지](/img/tutorials/jetton/jetton-connect-wallet.png)

모바일 지갑(예: 톤허브)에서 **QR코드**를 스캔하거나(https://ton.app/wallets/tonhub-wallet), [크롬 확장 프로그램]을 통해 지갑에 **로그인**합니다(https://ton.app/wallets/chrome-plugin).

#### 관련 정보로 빈칸을 채우세요.

1. 이름(보통 1~3단어).
2. 기호(보통 대문자 3~5자)를 입력합니다.
3. 금액(예: 1,000,000).
4. 토큰에 대한 설명(선택 사항).

#### 토큰 로고 URL(선택 사항)

![이미지](/img/tutorials/jetton/jetton-token-logo.png)

매력적인 제톤 토큰을 갖고 싶다면 어딘가에 호스팅된 아름다운 로고가 필요합니다.  예를 들어

- https://bitcoincash-example.github.io/website/logo.png

:::info
You can easily find out  about url placement of the logo in the [repository](https://github.com/ton-blockchain/minter-contract#jetton-metadata-field-best-practices) in paragraph "Where is this metadata stored".

- 온체인.
- 오프체인 IPFS.
- 오프체인 웹사이트.
  :::

#### 로고 URL은 어떻게 만드나요?

1. 투명한 배경을 가진 토큰 로고의 **256x256** PNG 이미지를 준비합니다.
2. 로고에 대한 링크를 얻으세요. 좋은 해결책은 [깃허브 페이지](https://pages.github.com/)입니다. 사용해 봅시다.
3. '웹사이트'라는 이름으로 [새 공개 리포지토리 만들기](https://docs.github.com/en/get-started/quickstart/create-a-repo)를 클릭합니다.
4. 준비된 이미지를 git에 업로드하고 `GitHub 페이지`를 활성화합니다.
   1. [리포지토리에 깃허브 페이지 추가](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).
   2. [이미지 업로드 및 링크 받기](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).
5. 자체 도메인이 있는 경우 `github.io` 대신 `.org`를 사용하는 것이 좋습니다.

## 💸 제톤 보내기

화면 오른쪽에서 [Tonkeeper](https://tonkeeper.com/) 또는 [Tonhub](https://ton.app/wallets/tonhub-wallet)와 같은 다중 통화 지갑으로 토큰을 **송금**할 수 있습니다.

![이미지](/img/tutorials/jetton/jetton-send-tokens.png)

:::info
You always also **burn** your Jettons to reduce their amount.

![이미지](/img/tutorials/jetton/jetton-burn-tokens.png)
:::

### 📱 톤키퍼를 사용하여 휴대폰에서 토큰 보내기

전제 조건:

1. 토큰을 보내려면 잔액에 토큰이 이미 있어야 합니다.
2. 거래 수수료를 지불하려면 최소 0.1톤코인이 있어야 합니다.

#### 단계별 가이드

그런 다음 **토큰**으로 이동하여 **금액**을 설정하고 **수신자 주소**를 입력합니다.

![이미지](/img/tutorials/jetton/jetton-send-tutorial.png)

## 📚 사이트에서 토큰 사용

사이트 상단의 **검색 필드**에 토큰 주소를 입력하여 소유자의 관리 권한을 사용할 수 있습니다.

:::info
The address can be found on the right side if you are already in the owner panel, or you can find the token address when receiving an airdrop.

![이미지](/img/tutorials/jetton/jetton-wallet-address.png)
:::

## ✏️ 제톤(토큰) 사용자 지정

FunC](/develop/func/overview) 언어를 사용하면 토큰의 동작을 원하는 대로 변경할 수 있습니다.

변경하려면 여기에서 시작하세요:

- https://github.com/ton-blockchain/minter-contract

### 개발자를 위한 단계별 가이드

1. 톤스타터-계약](https://github.com/ton-defi-org/tonstarter-contracts) 리포지토리의 모든 "종속성 및 요구 사항"이 있는지 확인하세요.
2. 민터-계약 저장소](https://github.com/ton-blockchain/minter-contract)를 복제하고 프로젝트 이름을 변경합니다.
3. 설치하려면 루트에서 터미널을 열고 실행해야 합니다:

```bash npm2yarn
npm install
```

4. 루트 터미널에서 원본 스마트 컨트랙트 파일을 같은 방식으로 편집합니다. 모든 컨트랙트 파일은 `contracts/*.fc`에 있습니다.

5. 다음을 사용하여 프로젝트를 빌드합니다:

```bash npm2yarn
npm run build
```

빌드 결과에는 필요한 파일을 만드는 과정과 스마트 컨트랙트 검색에 대한 설명이 나와 있습니다.

:::정보
콘솔을 읽어보세요, 많은 팁이 있습니다!
:::

6. 다음을 사용하여 변경 사항을 테스트할 수 있습니다:

```bash npm2yarn
npm run test
```

7. JettonParams 객체를 변경하여 `build/jetton-minter.deploy.ts`에서 토큰의 **이름** 및 기타 메타데이터를 편집합니다.

```js
// This is example data - Modify these params for your own jetton!
// - Data is stored on-chain (except for the image data itself)
// - Owner should usually be the deploying wallet's address.
  
const jettonParams = {
 owner: Address.parse("EQD4gS-Nj2Gjr2FYtg-s3fXUvjzKbzHGZ5_1Xe_V0-GCp0p2"),
 name: "MyJetton",
 symbol: "JET1",
 image: "https://www.linkpicture.com/q/download_183.png", // Image url
 description: "My jetton",
};
```

8. 토큰을 배포하려면 다음 명령을 사용합니다:

```bash npm2yarn
npm run deploy
```

프로젝트를 실행한 결과입니다:

````
```js
> @ton-defi.org/jetton-deployer-contracts@0.0.2 deploy
> ts-node ./build/_deploy.ts

=================================================================
Deploy script running, let's find some contracts to deploy..

* We are working with 'mainnet'

* Config file '.env' found and will be used for deployment!
 - Wallet address used to deploy from is: YOUR-ADDRESS
 - Wallet balance is YOUR-BALANCE TON, which will be used for gas

* Found root contract 'build/jetton-minter.deploy.ts - let's deploy it':
 - Based on your init code+data, your new contract address is: YOUR-ADDRESS
 - Let's deploy the contract on-chain..
 - Deploy transaction sent successfully
 - Block explorer link: https://tonwhales.com/explorer/address/YOUR-ADDRESS
 - Waiting up to 20 seconds to check if the contract was actually deployed..
 - SUCCESS! Contract deployed successfully to address: YOUR-ADDRESS
 - New contract balance is now YOUR-BALANCE TON, make sure it has enough to pay rent
 - Running a post deployment test:
{
  name: 'MyJetton',
  description: 'My jetton',
  image: 'https://www.linkpicture.com/q/download_183.png',
  symbol: 'JET1'
}
```
````

## 다음 단계는 무엇인가요?

더 자세히 알아보고 싶으시다면 Tal Kol의 이 글을 읽어보세요:

- [스마트 컨트랙트를 샤딩하는 방법과 이유 - 톤 제톤의 해부학 연구](https://blog.ton.org/how-to-shard-your-ton-smart-contract-and-why-studying-the-anatomy-of-tons-jettons)

## 참조

- 프로젝트: https://github.com/ton-blockchain/minter-contract
- Slava ([텔레그램 @delovoyslava](https://t.me/delovoyslava), [깃허브의 delovoyhomie](https://github.com/delovoyhomie)) 님이 작성했습니다.
