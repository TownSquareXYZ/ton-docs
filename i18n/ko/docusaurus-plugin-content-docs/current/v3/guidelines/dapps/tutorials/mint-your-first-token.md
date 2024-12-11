# 첫 번째 Jetton 발행하기

개발자님 환영합니다! 👋

이 글에서는 TON 블록체인에서 첫 번째 대체 가능한 토큰(Jetton)을 만드는 방법을 알려드리겠습니다.

Jetton을 발행하기 위해 [TON Minter](https://minter.ton.org/) / [TON Minter testnet](https://minter.ton.org/?testnet=true) 브라우저 서비스를 사용할 것입니다.

## 📖 학습 내용

이 글에서 다음 내용을 배우게 됩니다:

- 브라우저를 사용하여 Jetton 배포하기
- 토큰 커스터마이징하기
- 토큰 관리 및 사용하기
- 토큰 파라미터 수정하기

## 📌 시작 전 준비사항

1. 먼저 [Tonhub](https://ton.app/wallets/tonhub-wallet) / [Tonkeeper](https://ton.app/wallets/tonkeeper) 지갑 또는 서비스에서 지원하는 다른 지갑이 필요합니다.
2. 블록체인 수수료를 커버하기 위해 0.25 Toncoin 이상의 잔액이 필요합니다.

:::tip 초보자 팁
이 튜토리얼을 위해서는 약 0.5 TON이면 충분합니다.
:::

## 🚀 시작하기!

웹 브라우저에서 [TON Minter](https://minter.ton.org/) / [TON Minter testnet](https://minter.ton.org/?testnet=true) 서비스를 엽니다.

![image](/img/tutorials/jetton/jetton-main-page.png)

### 브라우저로 Jetton 배포하기

#### 지갑 연결하기

`Connect Wallet` 버튼을 클릭하여 [Tonhub](https://ton.app/wallets/tonhub-wallet) 지갑이나 다른 지원 지갑을 연결하세요.

#### ![image](/img/tutorials/jetton/jetton-connect-wallet.png)

**QR 코드를 스캔하세요** ([Tonhub와 같은 모바일 지갑](https://ton.app/wallets/tonhub-wallet)에서)

#### 관련 정보 입력하기

1. 이름 (보통 1-3단어)
2. 심볼 (보통 3-5자의 대문자)
3. 수량 (예: 1,000,000)
4. 토큰 설명 (선택사항)

#### 토큰 로고 URL (선택사항)

![image](/img/tutorials/jetton/jetton-token-logo.png)

매력적인 Jetton 토큰을 만들고 싶다면, 아름다운 로고를 어딘가에 호스팅해야 합니다. 예시:

- https://bitcoincash-example.github.io/website/logo.png

:::info
You can easily find out  about url placement of the logo in the [repository](https://github.com/ton-blockchain/minter-contract#jetton-metadata-field-best-practices) in paragraph "Where is this metadata stored".

- 온체인
- 오프체인 IPFS
- 오프체인 웹사이트
  :::

#### 로고 URL을 만드는 방법

1. 투명한 배경의 **256x256** PNG 이미지로 토큰 로고를 준비하세요.
2. 로고 링크를 받으세요. [GitHub Pages](https://pages.github.com/)가 좋은 해결책입니다. 이것을 사용해보겠습니다.
3. `website`라는 이름으로 [새로운 공개 저장소를 만드세요](https://docs.github.com/en/get-started/quickstart/create-a-repo).
4. 준비된 이미지를 git에 업로드하고 `GitHub Pages`를 활성화하세요.
   1. [저장소에 GitHub Pages 추가하기](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)
   2. [이미지를 업로드하고 링크 받기](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository)
5. 자체 도메인이 있다면 `github.io` 대신 `.org`를 사용하는 것이 좋습니다.

## 💸 Jetton 전송하기

화면 오른쪽에서 [Tonkeeper](https://tonkeeper.com/) 또는 [Tonhub](https://ton.app/wallets/tonhub-wallet)와 같은 멀티통화 지갑으로 **토큰을 전송**할 수 있습니다.

화면 오른쪽에서 [Tonkeeper](https://tonkeeper.com/) 또는 [Tonhub](https://ton.app/wallets/tonhub-wallet)과 같은 멀티 통화 지갑으로 **토큰 전송**이 가능합니다.

:::info
You always also **burn** your Jettons to reduce their amount.

![image](/img/tutorials/jetton/jetton-burn-tokens.png)
:::

### 📱 Tonkeeper로 휴대폰에서 토큰 전송하기

전제조건:

1. 전송할 토큰이 이미 잔액에 있어야 합니다.
2. 거래 수수료를 지불하기 위해 최소 0.1 Toncoin이 있어야 합니다.

#### 단계별 가이드

**토큰**으로 이동하여 전송할 **수량**을 설정하고 **수신자 주소**를 입력하세요.

토큰 페이지로 이동하여 **전송할 양**과 **수신자 주소**를 입력하세요.

## 📚 사이트에서 토큰 사용하기

사이트 상단의 **검색 필드**에 토큰 주소를 입력하여 소유자로서 관리할 수 있습니다.

:::info
The address can be found on the right side if you are already in the owner panel, or you can find the token address when receiving an airdrop.

사이트 상단 검색창에서 토큰 주소를 입력하면 소유자로서 관리할 수 있습니다.

## ✏️ Jetton(토큰) 커스터마이징

[FunC](/v3/documentation/smart-contracts/func/overview) 언어를 사용하여 토큰의 동작을 원하는 대로 변경할 수 있습니다.

변경하려면 여기서 시작하세요:

- https://github.com/ton-blockchain/minter-contract

### 개발자를 위한 단계별 가이드

1. [tonstarter-contracts](https://github.com/ton-defi-org/tonstarter-contracts) 저장소의 모든 "의존성 및 요구사항"이 있는지 확인하세요.
2. [minter-contract 저장소](https://github.com/ton-blockchain/minter-contract)를 클론하고 프로젝트 이름을 바꾸세요.
3. 설치하려면 루트에서 터미널을 열고 실행하세요:

```bash npm2yarn
npm install
```

4. 루트 터미널에서 원본 스마트 컨트랙트 파일을 같은 방식으로 편집하세요. 모든 컨트랙트 파일은 `contracts/*.fc`에 있습니다.

5. 다음을 사용하여 프로젝트를 빌드하세요:

```bash npm2yarn
npm run build
```

빌드 결과는 필요한 파일 생성 과정과 스마트 컨트랙트 검색을 설명합니다.

:::정보
콘솔에는 많은 팁이 있습니다!
:::

6. 다음을 사용하여 변경 사항을 테스트할 수 있습니다:

```bash npm2yarn
npm run test
```

7. `build/jetton-minter.deploy.ts`에서 JettonParams 객체를 변경하여 토큰의 **이름**과 다른 메타데이터를 편집하세요.

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

8. 토큰을 배포하려면 다음 명령을 사용하세요:

```bash npm2yarn
npm run deploy
```

프로젝트 실행 결과:

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

## 다음 단계

더 깊이 알아보고 싶다면, Tal Kol의 이 글을 읽어보세요:

- [How and why to shard your smart contract—studying the anatomy of TON Jettons](https://blog.ton.org/how-to-shard-your-ton-smart-contract-and-why-studying-the-anatomy-of-tons-jettons)

## 참고자료

- 프로젝트: https://github.com/ton-blockchain/minter-contract
- 작성자: Slava ([텔레그램 @delovoyslava](https://t.me/delovoyslava), [GitHub delovoyhomie](https://github.com/delovoyhomie))
- [Jetton 처리](/v3/guidelines/dapps/asset-processing/jettons)
