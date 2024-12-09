# NFT 컬렉션 만들기 단계별 가이드

## 👋 소개

대체불가능 토큰(NFT)은 디지털 아트와 수집품 세계에서 가장 뜨거운 주제 중 하나가 되었습니다. NFT는 블록체인 기술을 사용하여 소유권과 진위성을 검증하는 고유한 디지털 자산입니다. NFT는 창작자와 수집가들이 디지털 아트, 음악, 비디오 및 기타 디지털 콘텐츠를 수익화하고 거래할 수 있는 새로운 가능성을 열었습니다. 최근 몇 년간 NFT 시장이 급성장하여 일부 유명 작품은 수백만 달러에 거래되고 있습니다. 이 글에서는 TON에서 단계별로 NFT 컬렉션을 만들어보겠습니다.

**이 튜토리얼이 끝나면 만들게 될 아름다운 오리 컬렉션입니다:**

![](/img/tutorials/nft/collection.png)

## 🦄 배울 내용

1. TON에서 NFT 컬렉션을 발행합니다.
2. TON의 NFT 작동 방식을 이해합니다.
3. NFT를 판매합니다.
4. 메타데이터를 [pinata.cloud](https://pinata.cloud)에 업로드합니다.

## 💡 전제 조건

최소 2 TON이 있는 테스트넷 지갑이 필요합니다. [@testgiver_ton_bot](https://t.me/testgiver_ton_bot)에서 테스트넷 코인을 받을 수 있습니다.

:::info Tonkeeper 지갑의 테스트넷 버전을 여는 방법?\
Tonkeeper의 테스트넷을 열려면 설정으로 가서 하단의 Tonkeeper 로고를 5번 클릭하세요. 그런 다음 "mainnet" 대신 "testnet"을 선택하세요.
:::

IPFS 스토리지 시스템으로 Pinata를 사용할 것이므로 [pinata.cloud](https://pinata.cloud)에 계정을 만들고 api_key와 api_secret을 받아야 합니다. 공식 Pinata [문서 튜토리얼](https://docs.pinata.cloud/account-management/api-keys)이 도움이 될 수 있습니다. API 토큰을 받았다면, 여기서 계속하시죠!

## 💎 TON의 NFT란 무엇인가요?

튜토리얼의 메인 파트를 시작하기 전에 TON의 NFT가 일반적으로 어떻게 작동하는지 이해해야 합니다. 의외로 TON의 NFT 구현이 업계의 다른 블록체인과 비교하여 어떻게 독특한지 이해하기 위해 Ethereum(ETH)의 NFT 작동 방식부터 설명하겠습니다.

### ETH의 NFT 구현

ETH의 NFT 구현은 매우 단순합니다 - 컬렉션의 메인 컨트랙트 하나가 있고, 이 컨트랙트는 해당 컬렉션의 NFT 데이터를 저장하는 간단한 해시맵을 가지고 있습니다. 이 컬렉션과 관련된 모든 요청(사용자가 NFT를 전송하거나 판매하려는 경우 등)은 특별히 이 단일 컬렉션 컨트랙트로 보내집니다.

![](/img/tutorials/nft/eth-collection.png)

### TON에서 이러한 구현의 발생 가능한 문제점

TON의 [NFT 표준](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md)은 이러한 구현의 문제점을 완벽하게 설명합니다:

- 예측할 수 없는 가스 소비. TON에서는 딕셔너리 작업의 가스 소비가 정확한 키 집합에 따라 달라집니다. 또한 TON은 비동기 블록체인입니다. 이는 스마트 컨트랙트에 메시지를 보내면 다른 사용자의 메시지가 얼마나 많이 당신의 메시지보다 먼저 스마트 컨트랙트에 도달할지 모른다는 의미입니다. 따라서 당신의 메시지가 스마트 컨트랙트에 도달할 때 딕셔너리의 크기가 어떨지 알 수 없습니다. 이는 단순한 지갑 -> NFT 스마트 컨트랙트 상호작용에서는 괜찮지만, 지갑 -> NFT 스마트 컨트랙트 -> 경매 -> NFT 스마트 컨트랙트와 같은 스마트 컨트랙트 체인에서는 받아들일 수 없습니다. 가스 소비를 예측할 수 없다면, NFT 스마트 컨트랙트에서 소유자가 변경되었지만 경매 작업을 위한 Toncoin이 충분하지 않은 상황이 발생할 수 있습니다. 딕셔너리가 없는 스마트 컨트랙트를 사용하면 가스 소비를 결정적으로 만들 수 있습니다.

- 확장이 안 됨(병목현상이 됨). TON의 확장성은 샤딩 개념을 기반으로 합니다. 즉, 부하 시 네트워크가 자동으로 샤드체인으로 분할됩니다. 인기 있는 NFT의 단일 대형 스마트 컨트랙트는 이 개념과 모순됩니다. 이 경우 많은 트랜잭션이 하나의 단일 스마트 컨트랙트를 참조하게 됩니다. TON 아키텍처는 샤드된 스마트 컨트랙트(화이트페이퍼 참조)를 제공하지만, 현재는 구현되어 있지 않습니다.

*TL;DR ETH 솔루션은 확장성이 없고 TON과 같은 비동기 블록체인에는 적합하지 않습니다.*

### TON NFT 구현

TON에서는 마스터 컨트랙트 하나가 있습니다 - 우리 컬렉션의 스마트 컨트랙트로, 메타데이터와 소유자 주소를 저장하고 가장 중요한 점은 새로운 NFT 아이템을 만들고("mint") 싶을 때 이 컬렉션 컨트랙트에 메시지를 보내기만 하면 된다는 것입니다. 이 컬렉션 컨트랙트는 우리가 제공하는 데이터를 사용하여 새로운 NFT 아이템 컨트랙트를 배포할 것입니다.

![](/img/tutorials/nft/ton-collection.png)

:::info
이 주제에 대해 더 자세히 알고 싶다면 [TON의 NFT 처리](/v3/guidelines/dapps/asset-processing/nft-processing/nfts) 글을 확인하거나 [NFT 표준](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md)을 읽어보세요.
:::

## ⚙ 개발 환경 설정

빈 프로젝트를 만드는 것부터 시작해보겠습니다:

1. 새 폴더 만들기

```bash
mkdir MintyTON
```

2. 폴더 열기

```bash
cd MintyTON
```

3. 프로젝트 초기화

```bash
yarn init -y
```

4. typescript 설치

```bash
yarn add typescript @types/node -D
```

5. TypeScript 프로젝트 초기화

```bash
tsc --init
```

6. 이 설정을 tsconfig.json에 복사

```json
{
    "compilerOptions": {
      "module": "commonjs",
      "target": "es6",
      "lib": ["ES2022"],
      "moduleResolution": "node",
      "sourceMap": true,
      "outDir": "dist",
      "baseUrl": "src",
      "emitDecoratorMetadata": true,
      "experimentalDecorators": true,
      "strict": true,
      "esModuleInterop": true,
      "strictPropertyInitialization": false
    },
    "include": ["src/**/*"]
}
```

7. `package.json`에 앱을 빌드하고 시작하는 스크립트 추가

```json
"scripts": {
    "start": "tsc --skipLibCheck && node dist/app.js"
  },
```

8. 필요한 라이브러리 설치

```bash
yarn add @pinata/sdk dotenv @ton/ton @ton/crypto @ton/core buffer
```

9. `.env` 파일을 만들고 이 템플릿을 기반으로 자신의 데이터 추가

```
PINATA_API_KEY=your_api_key
PINATA_API_SECRET=your_secret_api_key
MNEMONIC=word1 word2 word3 word4
TONCENTER_API_KEY=aslfjaskdfjasasfas
```

[@tonapibot](https://t.me/tonapibot)에서 toncenter api 키를 받을 수 있으며 메인넷이나 테스트넷을 선택할 수 있습니다. `MNEMONIC` 변수에는 컬렉션 소유자 지갑의 24단어 시드 구문을 저장합니다.

좋습니다! 이제 프로젝트의 코드를 작성할 준비가 되었습니다.

### 헬퍼 함수 작성

먼저 `src/utils.ts`에 `openWallet` 함수를 만들어 니모닉으로 지갑을 열고 publicKey/secretKey를 반환하도록 하겠습니다.

24단어(시드 구문)를 기반으로 키 쌍을 얻습니다:

```ts
import { KeyPair, mnemonicToPrivateKey } from "@ton/crypto";
import { beginCell, Cell, OpenedContract} from "@ton/core";
import { TonClient, WalletContractV4 } from "@ton/ton";

export type OpenedWallet = {
  contract: OpenedContract<WalletContractV4>;
  keyPair: KeyPair;
};

export async function openWallet(mnemonic: string[], testnet: boolean) {
  const keyPair = await mnemonicToPrivateKey(mnemonic);
```

toncenter와 상호작용하기 위한 클래스 인스턴스를 만듭니다:

```ts
  const toncenterBaseEndpoint: string = testnet
    ? "https://testnet.toncenter.com"
    : "https://toncenter.com";

  const client = new TonClient({
    endpoint: `${toncenterBaseEndpoint}/api/v2/jsonRPC`,
    apiKey: process.env.TONCENTER_API_KEY,
  });
```

마지막으로 지갑을 엽니다:

```ts
  const wallet = WalletContractV4.create({
      workchain: 0,
      publicKey: keyPair.publicKey,
    });

  const contract = client.open(wallet);
  return { contract, keyPair };
}
```

좋습니다. 그 다음 프로젝트의 메인 엔트리포인트인 `src/app.ts`를 만듭니다.
여기서는 방금 만든 `openWallet` 함수를 사용하고 메인 함수 `init`을 호출합니다.
지금은 이 정도면 충분합니다.

```ts
import * as dotenv from "dotenv";

import { openWallet } from "./utils";
import { readdir } from "fs/promises";

dotenv.config();

async function init() {
  const wallet = await openWallet(process.env.MNEMONIC!.split(" "), true);  
}

void init();
```

마지막으로 `src` 디렉토리에 `delay.ts` 파일을 만들어 `seqno`가 증가할 때까지 기다리는 함수를 만듭니다.

```ts
import { OpenedWallet } from "./utils";

export async function waitSeqno(seqno: number, wallet: OpenedWallet) {
  for (let attempt = 0; attempt < 10; attempt++) {
    await sleep(2000);
    const seqnoAfter = await wallet.contract.getSeqno();
    if (seqnoAfter == seqno + 1) break;
  }
}

export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
```

:::info seqno가 무엇인가요?
간단히 말해서, seqno는 지갑이 보낸 나가는 트랜잭션의 카운터입니다.
seqno는 재생 공격을 방지하는 데 사용됩니다. 트랜잭션이 지갑 스마트 컨트랙트로 전송되면, 트랜잭션의 seqno 필드와 저장소 내부의 seqno를 비교합니다. 일치하면 수락되고 저장된 seqno가 1 증가합니다. 일치하지 않으면 트랜잭션이 폐기됩니다. 이것이 모든 나가는 트랜잭션 후에 잠시 기다려야 하는 이유입니다.
:::

## 🖼 메타데이터 준비

메타데이터는 우리의 NFT나 컬렉션을 설명하는 간단한 정보입니다. 예를 들어 이름, 설명 등입니다.

먼저 우리 NFT의 이미지를 `/data/images`에 `0.png`, `1.png`, ... 형식으로 아이템 사진을, 그리고 컬렉션의 아바타로 `logo.png`를 저장해야 합니다. [오리 이미지 팩](/img/tutorials/nft/ducks.zip)을 쉽게 다운로드하거나 자신의 이미지를 해당 폴더에 넣을 수 있습니다. 또한 모든 메타데이터 파일을 `/data/metadata/` 폴더에 저장할 것입니다.

### NFT 명세

TON의 대부분 제품은 NFT 컬렉션에 대한 정보를 저장하기 위해 다음과 같은 메타데이터 명세를 지원합니다:

| 이름                                | 설명                                                                                    |
| --------------------------------- | ------------------------------------------------------------------------------------- |
| name                              | 컬렉션 이름                                                                                |
| description                       | 컬렉션 설명                                                                                |
| image                             | 아바타로 표시될 이미지 링크. 지원되는 링크 형식: https, ipfs, TON Storage |
| cover_image  | 컬렉션의 커버 이미지로 표시될 이미지 링크                                                               |
| social_links | 프로젝트의 소셜 미디어 프로필 링크 목록. 최대 10개 링크                                     |

![image](/img/tutorials/nft/collection-metadata.png)

이 정보를 바탕으로 우리 컬렉션의 메타데이터를 설명하는 `collection.json` 파일을 만들어봅시다!

```json
{
  "name": "Ducks on TON",
  "description": "This collection is created for showing an example of minting NFT collection on TON. You can support creator by buying one of this NFT.",
  "social_links": ["https://t.me/DucksOnTON"]
}
```

"image" 파라미터를 쓰지 않았다는 점에 주목하세요. 곧 이유를 알게 될 것입니다!

컬렉션 메타데이터 파일을 만든 후에는 NFT의 메타데이터를 만들어야 합니다.

NFT 아이템 메타데이터 명세:

| 이름                                | 설명                                                                                                                                    |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| name                              | NFT 이름. 권장 길이: 15-30자 이내                                                                              |
| description                       | NFT 설명. 권장 길이: 500자 이내                                                                                |
| image                             | NFT 이미지 링크                                                                                                                            |
| attributes                        | NFT 속성. trait_type(속성 이름)과 value(속성에 대한 간단한 설명)가 지정된 속성 목록 |
| lottie                            | Lottie 애니메이션이 있는 json 파일 링크. 지정된 경우 NFT 페이지에서 이 링크의 Lottie 애니메이션이 재생됩니다.                              |
| content_url  | 추가 콘텐츠 링크                                                                                                                             |
| content_type | content_url 링크를 통해 추가된 콘텐츠의 타입. 예: video/mp4 파일                                  |

![image](/img/tutorials/nft/item-metadata.png)

```json
{
  "name": "Duck #00",
  "description": "What about a round of golf?",
  "attributes": [{ "trait_type": "Awesomeness", "value": "Super cool" }]
}
```

이제 원하는 만큼 메타데이터가 있는 NFT 아이템 파일을 만들 수 있습니다.

### 메타데이터 업로드

이제 메타데이터 파일을 IPFS에 업로드하는 코드를 작성해보겠습니다. `src` 디렉토리에 `metadata.ts` 파일을 만들고 필요한 임포트를 모두 추가합니다:

```ts
import pinataSDK from "@pinata/sdk";
import { readdirSync } from "fs";
import { writeFile, readFile } from "fs/promises";
import path from "path";
```

그 다음, 우리 폴더의 모든 파일을 IPFS에 업로드하는 함수를 만듭니다:

```ts
export async function uploadFolderToIPFS(folderPath: string): Promise<string> {
  const pinata = new pinataSDK({
    pinataApiKey: process.env.PINATA_API_KEY,
    pinataSecretApiKey: process.env.PINATA_API_SECRET,
  });

  const response = await pinata.pinFromFS(folderPath);
  return response.IpfsHash;
}
```

훌륭합니다! 다시 질문으로 돌아가보겠습니다: 왜 메타데이터 파일에서 "image" 필드를 비워뒀을까요? 컬렉션에 1000개의 NFT를 만들고 싶은 상황을 상상해보세요. 각 아이템을 수동으로 하나씩 확인하고 사진 링크를 직접 삽입해야 합니다.
이는 매우 불편하고 잘못된 방법입니다. 따라서 이를 자동으로 수행하는 함수를 작성해보겠습니다!

```ts
export async function updateMetadataFiles(metadataFolderPath: string, imagesIpfsHash: string): Promise<void> {
  const files = readdirSync(metadataFolderPath);

  await Promise.all(files.map(async (filename, index) => {
    const filePath = path.join(metadataFolderPath, filename)
    const file = await readFile(filePath);
    
    const metadata = JSON.parse(file.toString());
    metadata.image =
      index != files.length - 1
        ? `ipfs://${imagesIpfsHash}/${index}.jpg`
        : `ipfs://${imagesIpfsHash}/logo.jpg`;
    
    await writeFile(filePath, JSON.stringify(metadata));
  }));
}
```

먼저 지정된 폴더의 모든 파일을 읽습니다:

```ts
const files = readdirSync(metadataFolderPath);
```

각 파일을 반복하면서 내용을 가져옵니다

```ts
const filePath = path.join(metadataFolderPath, filename)
const file = await readFile(filePath);

const metadata = JSON.parse(file.toString());
```

그 다음, 폴더의 마지막 파일이 아니라면 이미지 필드에 `ipfs://{IpfsHash}/{index}.jpg` 값을 할당하고, 그렇지 않다면 `ipfs://{imagesIpfsHash}/logo.jpg`를 할당하고 실제로 새 데이터로 파일을 다시 작성합니다.

metadata.ts의 전체 코드:

```ts
import pinataSDK from "@pinata/sdk";
import { readdirSync } from "fs";
import { writeFile, readFile } from "fs/promises";
import path from "path";

export async function uploadFolderToIPFS(folderPath: string): Promise<string> {
  const pinata = new pinataSDK({
    pinataApiKey: process.env.PINATA_API_KEY,
    pinataSecretApiKey: process.env.PINATA_API_SECRET,
  });

  const response = await pinata.pinFromFS(folderPath);
  return response.IpfsHash;
}

export async function updateMetadataFiles(metadataFolderPath: string, imagesIpfsHash: string): Promise<void> {
  const files = readdirSync(metadataFolderPath);

  files.forEach(async (filename, index) => {
    const filePath = path.join(metadataFolderPath, filename)
    const file = await readFile(filePath);
    
    const metadata = JSON.parse(file.toString());
    metadata.image =
      index != files.length - 1
        ? `ipfs://${imagesIpfsHash}/${index}.jpg`
        : `ipfs://${imagesIpfsHash}/logo.jpg`;
    
    await writeFile(filePath, JSON.stringify(metadata));
  });
}
```

좋습니다. app.ts 파일에서 이 메소드들을 호출해보겠습니다.
우리 함수의 임포트를 추가합니다:

```ts
import { updateMetadataFiles, uploadFolderToIPFS } from "./src/metadata";
```

메타데이터/이미지 폴더 경로의 변수를 저장하고 메타데이터를 업로드하는 함수를 호출합니다.

```ts
async function init() {
  const metadataFolderPath = "./data/metadata/";
  const imagesFolderPath = "./data/images/";

  const wallet = await openWallet(process.env.MNEMONIC!.split(" "), true);

  console.log("Started uploading images to IPFS...");
  const imagesIpfsHash = await uploadFolderToIPFS(imagesFolderPath);
  console.log(
    `Successfully uploaded the pictures to ipfs: https://gateway.pinata.cloud/ipfs/${imagesIpfsHash}`
  );

  console.log("Started uploading metadata files to IPFS...");
  await updateMetadataFiles(metadataFolderPath, imagesIpfsHash);
  const metadataIpfsHash = await uploadFolderToIPFS(metadataFolderPath);
  console.log(
    `Successfully uploaded the metadata to ipfs: https://gateway.pinata.cloud/ipfs/${metadataIpfsHash}`
  );
}
```

이제 `yarn start`를 실행하면 배포된 메타데이터의 링크를 볼 수 있습니다!

### 오프체인 콘텐츠 인코딩

우리 메타데이터 파일의 링크가 스마트 컨트랙트에 어떻게 저장될까요? 이 질문에 대한 답은 [Token Data Standard](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md)에서 찾을 수 있습니다.
어떤 경우에는 단순히 원하는 플래그를 제공하고 링크를 ASCII 문자로 제공하는 것만으로는 충분하지 않을 수 있습니다. 이것이 스네이크 포맷을 사용하여 링크를 여러 부분으로 나누어야 하는 옵션을 고려해야 하는 이유입니다.

먼저 `./src/utils.ts`에서 버퍼를 청크로 변환하는 함수를 만듭니다:

```ts
function bufferToChunks(buff: Buffer, chunkSize: number) {
  const chunks: Buffer[] = [];
  while (buff.byteLength > 0) {
    chunks.push(buff.subarray(0, chunkSize));
    buff = buff.subarray(chunkSize);
  }
  return chunks;
}
```

그리고 모든 청크를 하나의 스네이크 셀로 묶는 함수를 만듭니다:

```ts
function makeSnakeCell(data: Buffer): Cell {
  const chunks = bufferToChunks(data, 127);

  if (chunks.length === 0) {
    return beginCell().endCell();
  }

  if (chunks.length === 1) {
    return beginCell().storeBuffer(chunks[0]).endCell();
  }

  let curCell = beginCell();

  for (let i = chunks.length - 1; i >= 0; i--) {
    const chunk = chunks[i];

    curCell.storeBuffer(chunk);

    if (i - 1 >= 0) {
      const nextCell = beginCell();
      nextCell.storeRef(curCell);
      curCell = nextCell;
    }
  }

  return curCell.endCell();
}
```

마지막으로, 이 함수들을 사용하여 오프체인 콘텐츠를 셀로 인코딩하는 함수를 만들어야 합니다:

```ts
export function encodeOffChainContent(content: string) {
  let data = Buffer.from(content);
  const offChainPrefix = Buffer.from([0x01]);
  data = Buffer.concat([offChainPrefix, data]);
  return makeSnakeCell(data);
}
```

## 🚢 NFT 컬렉션 배포

메타데이터가 준비되고 IPFS에 업로드되었으므로 컬렉션 배포를 시작할 수 있습니다!

`/contracts/NftCollection.ts` 파일에 우리 컬렉션과 관련된 모든 로직을 저장할 것입니다. 늘 그렇듯이 임포트부터 시작합니다:

```ts
import {
  Address,
  Cell,
  internal,
  beginCell,
  contractAddress,
  StateInit,
  SendMode,
} from "@ton/core";
import { encodeOffChainContent, OpenedWallet } from "../utils";
```

그리고 우리 컬렉션에 필요한 초기 데이터를 설명하는 타입을 선언합니다:

```ts
export type collectionData = {
  ownerAddress: Address;
  royaltyPercent: number;
  royaltyAddress: Address;
  nextItemIndex: number;
  collectionContentUrl: string;
  commonContentUrl: string;
}
```

| 이름                   | 설명                                                             |
| -------------------- | -------------------------------------------------------------- |
| ownerAddress         | 우리 컬렉션의 소유자로 설정될 주소. 소유자만이 새로운 NFT를 발행할 수 있습니다 |
| royaltyPercent       | 각 판매 금액의 몇 퍼센트가 지정된 주소로 갈지                                     |
| royaltyAddress       | 이 NFT 컬렉션의 판매에서 로열티를 받을 지갑 주소                                  |
| nextItemIndex        | 다음 NFT 아이템이 가져야 할 인덱스                                          |
| collectionContentUrl | 컬렉션 메타데이터의 URL                                                 |
| commonContentUrl     | NFT 아이템 메타데이터의 기본 url                                          |

먼저 우리 컬렉션의 코드가 있는 셀을 반환하는 private 메소드를 작성해보겠습니다.

```ts
export class NftCollection {
  private collectionData: collectionData;

  constructor(collectionData: collectionData) {
    this.collectionData = collectionData;
  }

  private createCodeCell(): Cell {
    const NftCollectionCodeBoc =
      "te6cckECFAEAAh8AART/APSkE/S88sgLAQIBYgkCAgEgBAMAJbyC32omh9IGmf6mpqGC3oahgsQCASAIBQIBIAcGAC209H2omh9IGmf6mpqGAovgngCOAD4AsAAvtdr9qJofSBpn+pqahg2IOhph+mH/SAYQAEO4tdMe1E0PpA0z/U1NQwECRfBNDUMdQw0HHIywcBzxbMyYAgLNDwoCASAMCwA9Ra8ARwIfAFd4AYyMsFWM8WUAT6AhPLaxLMzMlx+wCAIBIA4NABs+QB0yMsCEsoHy//J0IAAtAHIyz/4KM8WyXAgyMsBE/QA9ADLAMmAE59EGOASK3wAOhpgYC42Eit8H0gGADpj+mf9qJofSBpn+pqahhBCDSenKgpQF1HFBuvgoDoQQhUZYBWuEAIZGWCqALnixJ9AQpltQnlj+WfgOeLZMAgfYBwGyi544L5cMiS4ADxgRLgAXGBEuAB8YEYGYHgAkExIREAA8jhXU1DAQNEEwyFAFzxYTyz/MzMzJ7VTgXwSED/LwACwyNAH6QDBBRMhQBc8WE8s/zMzMye1UAKY1cAPUMI43gED0lm+lII4pBqQggQD6vpPywY/egQGTIaBTJbvy9AL6ANQwIlRLMPAGI7qTAqQC3gSSbCHis+YwMlBEQxPIUAXPFhPLP8zMzMntVABgNQLTP1MTu/LhklMTugH6ANQwKBA0WfAGjhIBpENDyFAFzxYTyz/MzMzJ7VSSXwXiN0CayQ==";
    return Cell.fromBase64(NftCollectionCodeBoc);
  }
}
```

이 코드에서는 컬렉션 스마트 컨트랙트의 base64 표현에서 Cell을 읽기만 합니다.

좋습니다. 이제 우리 컬렉션의 초기 데이터가 있는 셀만 남았습니다.
기본적으로 collectionData의 데이터를 올바른 방식으로 저장하기만 하면 됩니다. 먼저 빈 셀을 만들고 거기에 컬렉션 소유자 주소와 발행될 다음 아이템의 인덱스를 저장해야 합니다. 다음 private 메소드를 작성해보겠습니다:

```ts
private createDataCell(): Cell {
  const data = this.collectionData;
  const dataCell = beginCell();

  dataCell.storeAddress(data.ownerAddress);
  dataCell.storeUint(data.nextItemIndex, 64);
```

그 다음, 우리 컬렉션의 콘텐츠를 저장할 빈 셀을 만들고, 우리 컬렉션의 인코딩된 콘텐츠에 대한 참조를 저장합니다. 그리고 바로 그 후에 contentCell에 대한 참조를 우리의 메인 데이터 셀에 저장합니다.

```ts
const contentCell = beginCell();

const collectionContent = encodeOffChainContent(data.collectionContentUrl);

const commonContent = beginCell();
commonContent.storeBuffer(Buffer.from(data.commonContentUrl));

contentCell.storeRef(collectionContent);
contentCell.storeRef(commonContent.asCell());
dataCell.storeRef(contentCell);
```

그 다음 우리 컬렉션에서 생성될 NFT 아이템의 코드 셀을 만들고 이 셀에 대한 참조를 dataCell에 저장합니다.

```ts
const NftItemCodeCell = Cell.fromBase64(
  "te6cckECDQEAAdAAART/APSkE/S88sgLAQIBYgMCAAmhH5/gBQICzgcEAgEgBgUAHQDyMs/WM8WAc8WzMntVIAA7O1E0NM/+kAg10nCAJp/AfpA1DAQJBAj4DBwWW1tgAgEgCQgAET6RDBwuvLhTYALXDIhxwCSXwPg0NMDAXGwkl8D4PpA+kAx+gAxcdch+gAx+gAw8AIEs44UMGwiNFIyxwXy4ZUB+kDUMBAj8APgBtMf0z+CEF/MPRRSMLqOhzIQN14yQBPgMDQ0NTWCEC/LJqISuuMCXwSED/LwgCwoAcnCCEIt3FzUFyMv/UATPFhAkgEBwgBDIywVQB88WUAX6AhXLahLLH8s/Im6zlFjPFwGRMuIByQH7AAH2UTXHBfLhkfpAIfAB+kDSADH6AIIK+vCAG6EhlFMVoKHeItcLAcMAIJIGoZE24iDC//LhkiGOPoIQBRONkchQCc8WUAvPFnEkSRRURqBwgBDIywVQB88WUAX6AhXLahLLH8s/Im6zlFjPFwGRMuIByQH7ABBHlBAqN1viDACCAo41JvABghDVMnbbEDdEAG1xcIAQyMsFUAfPFlAF+gIVy2oSyx/LPyJus5RYzxcBkTLiAckB+wCTMDI04lUC8ANqhGIu"
);
dataCell.storeRef(NftItemCodeCell);
```

로열티 파라미터는 스마트 컨트랙트에 royaltyFactor, royaltyBase, royaltyAddress로 저장됩니다. 로열티의 백분율은 `(royaltyFactor / royaltyBase) * 100%` 공식으로 계산할 수 있습니다. 따라서 royaltyPercent를 알고 있다면 royaltyFactor를 구하는 것은 문제가 되지 않습니다.

```ts
const royaltyBase = 1000;
const royaltyFactor = Math.floor(data.royaltyPercent * royaltyBase);
```

계산 후에는 로열티 데이터를 별도의 셀에 저장하고 이 셀에 대한 참조를 dataCell에 제공해야 합니다.

```ts
const royaltyCell = beginCell();
royaltyCell.storeUint(royaltyFactor, 16);
royaltyCell.storeUint(royaltyBase, 16);
royaltyCell.storeAddress(data.royaltyAddress);
dataCell.storeRef(royaltyCell);

return dataCell.endCell();
}
```

이제 우리 컬렉션의 StateInit을 반환하는 getter를 실제로 작성해보겠습니다:

```ts
public get stateInit(): StateInit {
  const code = this.createCodeCell();
  const data = this.createDataCell();

  return { code, data };
}
```

그리고 우리 컬렉션의 주소를 계산하는 getter를 작성합니다(TON의 스마트 컨트랙트 주소는 단순히 그것의 StateInit의 해시입니다).

```ts
public get address(): Address {
    return contractAddress(0, this.stateInit);
  }
```

이제 블록체인에 스마트 컨트랙트를 배포하는 메소드만 작성하면 됩니다!

```ts
public async deploy(wallet: OpenedWallet) {
    const seqno = await wallet.contract.getSeqno();
    await wallet.contract.sendTransfer({
      seqno,
      secretKey: wallet.keyPair.secretKey,
      messages: [
        internal({
          value: "0.05",
          to: this.address,
          init: this.stateInit,
        }),
      ],
      sendMode: SendMode.PAY_GAS_SEPARATELY + SendMode.IGNORE_ERRORS,
    });
    return seqno;
  }
```

우리의 경우 새로운 스마트 컨트랙트의 배포는 StateInit이 있는 컬렉션 주소(StateInit이 있으면 계산할 수 있음)로 우리 지갑에서 메시지를 보내는 것뿐입니다!

소유자가 새로운 NFT를 발행할 때, 컬렉션은 소유자의 메시지를 받고 생성된 NFT 스마트 컨트랙트로 새로운 메시지를 보냅니다(이는 수수료를 지불해야 함). 따라서 발행할 nft 수에 기반하여 컬렉션의 잔액을 충전하는 메소드를 작성해보겠습니다:

```ts
public async topUpBalance(
    wallet: OpenedWallet,
    nftAmount: number
  ): Promise<number> {
    const feeAmount = 0.026 // approximate value of fees for 1 transaction in our case 
    const seqno = await wallet.contract.getSeqno();
    const amount = nftAmount * feeAmount;

    await wallet.contract.sendTransfer({
      seqno,
      secretKey: wallet.keyPair.secretKey,
      messages: [
        internal({
          value: amount.toString(),
          to: this.address.toString({ bounceable: false }),
          body: new Cell(),
        }),
      ],
      sendMode: SendMode.PAY_GAS_SEPARATELY + SendMode.IGNORE_ERRORS,
    });

    return seqno;
  }
```

완벽합니다. 이제 `app.ts`에 몇 가지를 추가해보겠습니다:

```ts
import { waitSeqno } from "./delay";
import { NftCollection } from "./contracts/NftCollection";
```

그리고 새로운 컬렉션을 배포하기 위해 `init()` 함수 끝에 몇 줄을 추가합니다:

```ts
console.log("Start deploy of nft collection...");
const collectionData = {
  ownerAddress: wallet.contract.address,
  royaltyPercent: 0.05, // 0.05 = 5%
  royaltyAddress: wallet.contract.address,
  nextItemIndex: 0,
  collectionContentUrl: `ipfs://${metadataIpfsHash}/collection.json`,
  commonContentUrl: `ipfs://${metadataIpfsHash}/`,
};
const collection = new NftCollection(collectionData);
let seqno = await collection.deploy(wallet);
console.log(`Collection deployed: ${collection.address}`);
await waitSeqno(seqno, wallet);
```

## 🚢 NFT 아이템 배포

우리 컬렉션이 준비되었으니, NFT 발행을 시작할 수 있습니다! 코드는 `src/contracts/NftItem.ts`에 저장할 것입니다.

의외로, 이제 `NftCollection.ts`로 돌아가야 합니다. 그리고 파일 상단의 `collectionData` 옆에 이 타입을 추가합니다.

```ts
export type mintParams = {
  queryId: number | null,
  itemOwnerAddress: Address,
  itemIndex: number,
  amount: bigint,
  commonContentUrl: string
}
```

| 이름               | 설명                                                                       |
| ---------------- | ------------------------------------------------------------------------ |
| itemOwnerAddress | 아이템의 소유자로 설정될 주소                                                         |
| itemIndex        | NFT 아이템의 인덱스                                                             |
| amount           | NFT와 함께 배포될 TON의 양                                                       |
| commonContentUrl | 아이템 URL의 전체 링크는 컬렉션의 "commonContentUrl" + 이 commonContentUrl로 표시될 수 있습니다 |

그리고 NftCollection 클래스에 우리의 NFT 아이템 배포를 위한 본문을 구성하는 메소드를 만듭니다. 먼저 새로운 NFT를 만들고 싶다는 것을 컬렉션 스마트 컨트랙트에 알리는 비트를 저장합니다. 그 다음 queryId와 이 NFT 아이템의 인덱스를 저장합니다.

```ts
public createMintBody(params: mintParams): Cell {
    const body = beginCell();
    body.storeUint(1, 32);
    body.storeUint(params.queryId || 0, 64);
    body.storeUint(params.itemIndex, 64);
    body.storeCoins(params.amount);
```

나중에 빈 셀을 만들고 이 NFT의 소유자 주소를 저장합니다:

```ts
    const nftItemContent = beginCell();
    nftItemContent.storeAddress(params.itemOwnerAddress);
```

그리고 이 아이템의 메타데이터에 대한 참조를 이 셀(NFT 아이템 콘텐츠가 있는)에 저장합니다:

```ts
    const uriContent = beginCell();
    uriContent.storeBuffer(Buffer.from(params.commonContentUrl));
    nftItemContent.storeRef(uriContent.endCell());
```

우리 본문 셀에 아이템 콘텐츠가 있는 셀에 대한 참조를 저장합니다:

```ts
    body.storeRef(nftItemContent.endCell());
    return body.endCell();
}
```

훌륭합니다! 이제 `NftItem.ts`로 돌아갈 수 있습니다. 해야 할 일은 우리 NFT의 본문으로 우리 컬렉션 컨트랙트에 메시지를 보내는 것뿐입니다.

```ts
import { internal, SendMode, Address, beginCell, Cell, toNano } from "@ton/core";
import { OpenedWallet } from "utils";
import { NftCollection, mintParams } from "./NftCollection";
import { TonClient } from "@ton/ton";

export class NftItem {
  private collection: NftCollection;

  constructor(collection: NftCollection) {
    this.collection = collection;
  }

  public async deploy(
    wallet: OpenedWallet,
    params: mintParams
  ): Promise<number> {
    const seqno = await wallet.contract.getSeqno();
    await wallet.contract.sendTransfer({
      seqno,
      secretKey: wallet.keyPair.secretKey,
      messages: [
        internal({
          value: "0.05",
          to: this.collection.address,
          body: this.collection.createMintBody(params),
        }),
      ],
      sendMode: SendMode.IGNORE_ERRORS + SendMode.PAY_GAS_SEPARATELY,
    });
    return seqno;
  }
}
```

마지막으로, NFT의 인덱스로 주소를 얻는 간단한 메소드를 작성하겠습니다.

컬렉션의 get-메소드를 호출하는데 도움이 될 client 변수를 만드는 것부터 시작합니다:

```ts
static async getAddressByIndex(
  collectionAddress: Address,
  itemIndex: number
): Promise<Address> {
  const client = new TonClient({
    endpoint: "https://testnet.toncenter.com/api/v2/jsonRPC",
    apiKey: process.env.TONCENTER_API_KEY,
  });
```

그런 다음 해당 인덱스를 가진 이 컬렉션의 NFT 주소를 반환하는 컬렉션의 get-메소드를 호출합니다:

```ts
  const response = await client.runMethod(
    collectionAddress,
    "get_nft_address_by_index",
    [{ type: "int", value: BigInt(itemIndex) }]
  );
```

...그리고 이 주소를 파싱합니다!

```ts
    return response.stack.readAddress();
}
```

이제 각 NFT의 발행 프로세스를 자동화하기 위해 `app.ts`에 코드를 추가해보겠습니다:

```ts
  import { NftItem } from "./contracts/NftItem";
  import { toNano } from '@ton/core';
```

먼저 우리 메타데이터가 있는 폴더의 모든 파일을 읽습니다:

```ts
const files = await readdir(metadataFolderPath);
files.pop();
let index = 0;
```

두 번째로 우리 컬렉션의 잔액을 충전합니다:

```ts
seqno = await collection.topUpBalance(wallet, files.length);
await waitSeqno(seqno, wallet);
console.log(`Balance top-upped`);
```

마지막으로, 메타데이터가 있는 각 파일을 확인하고, `NftItem` 인스턴스를 만들고 deploy 메소드를 호출합니다. 그 후에는 seqno가 증가할 때까지 잠시 기다려야 합니다:

```ts
for (const file of files) {
    console.log(`Start deploy of ${index + 1} NFT`);
    const mintParams = {
      queryId: 0,
      itemOwnerAddress: wallet.contract.address,
      itemIndex: index,
      amount: toNano("0.05"),
      commonContentUrl: file,
    };

    const nftItem = new NftItem(collection);
    seqno = await nftItem.deploy(wallet, mintParams);
    console.log(`Successfully deployed ${index + 1} NFT`);
    await waitSeqno(seqno, wallet);
    index++;
  }
```

## 🏷 NFT 판매하기

NFT를 판매하기 위해서는 두 개의 스마트 컨트랙트가 필요합니다.

- 새로운 판매를 생성하는 로직만 담당하는 마켓플레이스
- 판매 구매/취소 로직을 담당하는 판매 컨트랙트

### 마켓플레이스 배포

`/contracts/NftMarketplace.ts`에 새 파일을 만듭니다. 평소처럼 이 마켓플레이스의 소유자 주소를 받는 기본 클래스를 만들고 이 스마트 컨트랙트의 코드([NFT-Marketplace 스마트 컨트랙트의 기본 버전](https://github.com/ton-blockchain/token-contract/blob/main/nft/nft-marketplace.fc))가 있는 셀과 초기 데이터를 만듭니다.

```ts
import {
  Address,
  beginCell,
  Cell,
  contractAddress,
  internal,
  SendMode,
  StateInit,
} from "@ton/core";
import { OpenedWallet } from "../utils";

export class NftMarketplace {
  public ownerAddress: Address;

  constructor(ownerAddress: Address) {
    this.ownerAddress = ownerAddress;
  }


  public get stateInit(): StateInit {
    const code = this.createCodeCell();
    const data = this.createDataCell();

    return { code, data };
  }

  private createDataCell(): Cell {
    const dataCell = beginCell();

    dataCell.storeAddress(this.ownerAddress);

    return dataCell.endCell();
  }

  private createCodeCell(): Cell {
    const NftMarketplaceCodeBoc = "te6cckEBBAEAbQABFP8A9KQT9LzyyAsBAgEgAgMAqtIyIccAkVvg0NMDAXGwkVvg+kDtRND6QDASxwXy4ZEB0x8BwAGOK/oAMAHU1DAh+QBwyMoHy//J0Hd0gBjIywXLAljPFlAE+gITy2vMzMlx+wCRW+IABPIwjvfM5w==";
    return Cell.fromBase64(NftMarketplaceCodeBoc)
  }
}
```

그리고 StateInit을 기반으로 우리 스마트 컨트랙트의 주소를 계산하는 메소드를 만듭니다:

```ts
public get address(): Address {
    return contractAddress(0, this.stateInit);
  }
```

그 다음 실제로 우리 마켓플레이스를 배포하는 메소드를 만듭니다:

```ts
public async deploy(wallet: OpenedWallet): Promise<number> {
    const seqno = await wallet.contract.getSeqno();
    await wallet.contract.sendTransfer({
      seqno,
      secretKey: wallet.keyPair.secretKey,
      messages: [
        internal({
          value: "0.5",
          to: this.address,
          init: this.stateInit,
        }),
      ],
      sendMode: SendMode.IGNORE_ERRORS + SendMode.PAY_GAS_SEPARATELY,
    });
    return seqno;
  }
```

보시다시피, 이 코드는 다른 스마트 컨트랙트(nft-item 스마트 컨트랙트, 새로운 컬렉션의 배포)의 배포와 다르지 않습니다. 단 한 가지 다른 점은 우리가 마켓플레이스를 초기에 0.05 TON이 아닌 0.5 TON으로 충전한다는 것입니다. 이유는 무엇일까요? 새로운 판매 스마트 컨트랙트가 배포될 때, 마켓플레이스는 요청을 받고, 처리하고, 새로운 컨트랙트로 메시지를 보냅니다(예, NFT 컬렉션과 비슷한 상황입니다). 이것이 수수료를 지불하기 위해 약간의 추가 톤이 필요한 이유입니다.

마지막으로, 우리 마켓플레이스를 배포하기 위해 `app.ts` 파일에 몇 줄의 코드를 추가해봅시다:

```ts
import { NftMarketplace } from "./contracts/NftMarketplace";
```

그리고:

```ts
console.log("Start deploy of new marketplace  ");
const marketplace = new NftMarketplace(wallet.contract.address);
seqno = await marketplace.deploy(wallet);
await waitSeqno(seqno, wallet);
console.log("Successfully deployed new marketplace");
```

### 판매 컨트랙트 배포

좋습니다! 이제 우리의 NFT 판매 스마트 컨트랙트를 배포할 수 있습니다. 어떻게 작동할까요? 새 컨트랙트를 배포하고 그 후에 우리의 nft를 판매 컨트랙트로 "이전"해야 합니다(다시 말해, 아이템 데이터에서 우리 NFT의 소유자를 판매 컨트랙트로 변경하기만 하면 됩니다). 이 튜토리얼에서는 [nft-fixprice-sale-v2](https://github.com/getgems-io/nft-contracts/blob/main/packages/contracts/sources/nft-fixprice-sale-v2.fc) 판매 스마트 컨트랙트를 사용할 것입니다.

`/contracts/NftSale.ts`에 새 파일을 만듭니다. 먼저 우리의 판매 스마트 컨트랙트의 데이터를 설명하는 새로운 타입을 선언합니다:

```ts
import {
  Address,
  beginCell,
  Cell,
  contractAddress,
  internal,
  SendMode,
  StateInit,
  storeStateInit,
  toNano,
} from "@ton/core";
import { OpenedWallet } from "utils";

export type GetGemsSaleData = {
  isComplete: boolean;
  createdAt: number;
  marketplaceAddress: Address;
  nftAddress: Address;
  nftOwnerAddress: Address | null;
  fullPrice: bigint;
  marketplaceFeeAddress: Address;
  marketplaceFee: bigint;
  royaltyAddress: Address;
  royaltyAmount: bigint;
};
```

이제 클래스를 만들고 우리 스마트 컨트랙트의 초기 데이터 셀을 만드는 기본 메소드를 만들어보겠습니다.

```ts
export class NftSale {
  private data: GetGemsSaleData;

  constructor(data: GetGemsSaleData) {
    this.data = data;
  }
}
```

수수료 정보가 있는 셀을 만드는 것부터 시작하겠습니다. 마켓플레이스의 수수료로 받을 주소와 수수료로 보낼 TON의 양을 저장해야 합니다. 판매의 로열티를 받을 주소와 로열티 금액을 저장합니다.

```ts
private createDataCell(): Cell {
  const saleData = this.data;

  const feesCell = beginCell();

  feesCell.storeAddress(saleData.marketplaceFeeAddress);
  feesCell.storeCoins(saleData.marketplaceFee);
  feesCell.storeAddress(saleData.royaltyAddress);
  feesCell.storeCoins(saleData.royaltyAmount);
```

그 다음 빈 셀을 만들고 saleData의 정보를 올바른 순서로 저장한 다음 수수료 정보가 있는 셀에 대한 참조를 저장합니다:

```ts
  const dataCell = beginCell();

  dataCell.storeUint(saleData.isComplete ? 1 : 0, 1);
  dataCell.storeUint(saleData.createdAt, 32);
  dataCell.storeAddress(saleData.marketplaceAddress);
  dataCell.storeAddress(saleData.nftAddress);
  dataCell.storeAddress(saleData.nftOwnerAddress);
  dataCell.storeCoins(saleData.fullPrice);
  dataCell.storeRef(feesCell.endCell());

  return dataCell.endCell();
}
```

그리고 늘 그렇듯이 stateInit을 가져오고, 코드 셀을 초기화하고 우리 스마트 컨트랙트의 주소를 가져오는 메소드를 추가합니다.

```ts
public get address(): Address {
  return contractAddress(0, this.stateInit);
}

public get stateInit(): StateInit {
  const code = this.createCodeCell();
  const data = this.createDataCell();

  return { code, data };
}

private createCodeCell(): Cell {
  const NftFixPriceSaleV2CodeBoc =
    "te6cckECDAEAAikAART/APSkE/S88sgLAQIBIAMCAATyMAIBSAUEAFGgOFnaiaGmAaY/9IH0gfSB9AGoYaH0gfQB9IH0AGEEIIySsKAVgAKrAQICzQgGAfdmCEDuaygBSYKBSML7y4cIk0PpA+gD6QPoAMFOSoSGhUIehFqBSkHCAEMjLBVADzxYB+gLLaslx+wAlwgAl10nCArCOF1BFcIAQyMsFUAPPFgH6AstqyXH7ABAjkjQ04lpwgBDIywVQA88WAfoCy2rJcfsAcCCCEF/MPRSBwCCIYAYyMsFKs8WIfoCy2rLHxPLPyPPFlADzxbKACH6AsoAyYMG+wBxVVAGyMsAFcsfUAPPFgHPFgHPFgH6AszJ7VQC99AOhpgYC42EkvgnB9IBh2omhpgGmP/SB9IH0gfQBqGBNgAPloyhFrpOEBWccgGRwcKaDjgskvhHAoomOC+XD6AmmPwQgCicbIiV15cPrpn5j9IBggKwNkZYAK5Y+oAeeLAOeLAOeLAP0BZmT2qnAbE+OAcYED6Y/pn5gQwLCQFKwAGSXwvgIcACnzEQSRA4R2AQJRAkECPwBeA6wAPjAl8JhA/y8AoAyoIQO5rKABi+8uHJU0bHBVFSxwUVsfLhynAgghBfzD0UIYAQyMsFKM8WIfoCy2rLHxnLPyfPFifPFhjKACf6AhfKAMmAQPsAcQZQREUVBsjLABXLH1ADzxYBzxYBzxYB+gLMye1UABY3EDhHZRRDMHDwBTThaBI=";

  return Cell.fromBase64(NftFixPriceSaleV2CodeBoc);
}
```

이제 우리의 마켓플레이스에 판매 컨트랙트를 배포하기 위해 보낼 메시지를 구성하고 실제로 이 메시지를 보내야 합니다.

먼저 우리의 새로운 판매 컨트랙트의 StateInit을 저장할 셀을 만듭니다:

```ts
public async deploy(wallet: OpenedWallet): Promise<number> {
    const stateInit = beginCell()
      .store(storeStateInit(this.stateInit))
      .endCell();
```

우리 메시지의 본문을 위한 셀을 만듭니다. 먼저 op-code를 1로 설정해야 합니다(마켓플레이스에 새로운 판매 스마트 컨트랙트를 배포하고 싶다는 것을 알리기 위해). 그 다음 우리의 새로운 판매 스마트 컨트랙트로 보낼 코인을 저장합니다. 마지막으로 새로운 스마트 컨트랙트의 stateInit과 이 새로운 스마트 컨트랙트로 보낼 본문에 대한 2개의 참조를 저장해야 합니다.

```ts
  const payload = beginCell();
  payload.storeUint(1, 32);
  payload.storeCoins(toNano("0.05"));
  payload.storeRef(stateInit);
  payload.storeRef(new Cell());
```

그리고 마지막으로 우리의 메시지를 보냅니다:

```ts
  const seqno = await wallet.contract.getSeqno();
  await wallet.contract.sendTransfer({
    seqno,
    secretKey: wallet.keyPair.secretKey,
    messages: [
      internal({
        value: "0.05",
        to: this.data.marketplaceAddress,
        body: payload.endCell(),
      }),
    ],
    sendMode: SendMode.IGNORE_ERRORS + SendMode.PAY_GAS_SEPARATELY,
  });
  return seqno;
}
```

완벽합니다. 판매 스마트 컨트랙트가 배포되면 우리 NFT 아이템의 소유자를 이 판매의 주소로 변경하기만 하면 됩니다.

### 아이템 이전

아이템을 이전한다는 것은 무엇을 의미할까요? 단순히 누가 아이템의 새로운 소유자인지에 대한 정보와 함께 소유자의 지갑에서 스마트 컨트랙트로 메시지를 보내는 것입니다.

`NftItem.ts`로 가서 NftItem 클래스에 이러한 메시지의 본문을 만드는 새로운 static 메소드를 만듭니다:

빈 셀을 만들고 데이터를 채우기만 하면 됩니다.

```ts
static createTransferBody(params: {
    newOwner: Address;
    responseTo?: Address;
    forwardAmount?: bigint;
  }): Cell {
    const msgBody = beginCell();
    msgBody.storeUint(0x5fcc3d14, 32); // op-code 
    msgBody.storeUint(0, 64); // query-id
    msgBody.storeAddress(params.newOwner);
```

op-code, query-id, 새 소유자의 주소 외에도, 성공적인 전송 확인에 대한 응답을 보낼 주소와 들어오는 메시지 코인의 나머지 부분도 저장해야 합니다. 새 소유자에게 갈 TON의 양과 텍스트 페이로드를 받을지 여부를 저장합니다.

```ts
  msgBody.storeAddress(params.responseTo || null);
  msgBody.storeBit(false); // no custom payload
  msgBody.storeCoins(params.forwardAmount || 0);
  msgBody.storeBit(0); // no forward_payload 

  return msgBody.endCell();
}
```

그리고 NFT를 이전하기 위한 이전 함수를 만듭니다.

```ts
static async transfer(
    wallet: OpenedWallet,
    nftAddress: Address,
    newOwner: Address
  ): Promise<number> {
    const seqno = await wallet.contract.getSeqno();

    await wallet.contract.sendTransfer({
      seqno,
      secretKey: wallet.keyPair.secretKey,
      messages: [
        internal({
          value: "0.05",
          to: nftAddress,
          body: this.createTransferBody({
            newOwner,
            responseTo: wallet.contract.address,
            forwardAmount: toNano("0.02"),
          }),
        }),
      ],
      sendMode: SendMode.IGNORE_ERRORS + SendMode.PAY_GAS_SEPARATELY,
    });
    return seqno;
  }
```

좋습니다, 이제 거의 끝에 가까워졌습니다. `app.ts`로 돌아가서 판매하고 싶은 nft의 주소를 가져옵시다:

```ts
const nftToSaleAddress = await NftItem.getAddressByIndex(collection.address, 0);
```

우리 판매에 대한 정보를 저장할 변수를 만듭니다.

`app.ts`의 시작 부분에 추가:

```ts
import { GetGemsSaleData, NftSale } from "./contracts/NftSale";
```

그리고:

```ts
const saleData: GetGemsSaleData = {
  isComplete: false,
  createdAt: Math.ceil(Date.now() / 1000),
  marketplaceAddress: marketplace.address,
  nftAddress: nftToSaleAddress,
  nftOwnerAddress: null,
  fullPrice: toNano("10"),
  marketplaceFeeAddress: wallet.contract.address,
  marketplaceFee: toNano("1"),
  royaltyAddress: wallet.contract.address,
  royaltyAmount: toNano("0.5"),
};
```

참고로, `nftOwnerAddress`를 null로 설정했습니다. 이렇게 하면 우리의 판매 컨트랙트는 배포 시 우리의 코인을 받기만 할 것입니다.

우리의 판매를 배포합니다:

```ts
const nftSaleContract = new NftSale(saleData);
seqno = await nftSaleContract.deploy(wallet);
await waitSeqno(seqno, wallet);
```

...그리고 이전합니다!

```ts
await NftItem.transfer(wallet, nftToSaleAddress, nftSaleContract.address);
```

이제 프로젝트를 실행하고 과정을 즐길 수 있습니다!

```
yarn start
```

https://testnet.getgems.io/collection/{YOUR_COLLECTION_ADDRESS_HERE}로 가서 이 멋진 오리들을 보세요!

## 결론

오늘 TON에 대한 많은 새로운 것을 배웠고 심지어 테스트넷에서 자신만의 아름다운 NFT 컬렉션도 만들었습니다! 여전히 질문이 있거나 오류를 발견했다면 작성자에게 자유롭게 문의하세요 - [@coalus](https://t.me/coalus)

## 참고자료

- [GetGems NFT-contracts](https://github.com/getgems-io/nft-contracts)
- [NFT 표준](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md)

## 작성자 소개

- Coalus: [텔레그램](https://t.me/coalus) 또는 [GitHub](https://github.com/coalus)

## 참고

- [NFT 사용 사례](/v3/documentation/dapps/defi/nft)
