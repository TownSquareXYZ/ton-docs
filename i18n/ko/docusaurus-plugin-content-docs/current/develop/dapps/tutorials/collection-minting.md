# 단계별 NFT 컬렉션 채굴

## 👋 소개

대체 불가능한 토큰, 즉 NFT는 디지털 아트와 수집품 세계에서 가장 뜨거운 주제 중 하나가 되었습니다. NFT는 블록체인 기술을 사용해 소유권과 진위 여부를 확인하는 고유한 디지털 자산입니다. 이는 크리에이터와 수집가가 디지털 아트, 음악, 동영상 및 기타 형태의 디지털 콘텐츠로 수익을 창출하고 거래할 수 있는 새로운 가능성을 열어주었습니다. 최근
몇 년 동안 NFT 시장은 폭발적으로 성장하여 수백만 달러에 달하는 매출을 기록한 사례도 있습니다. 이 글에서는 TON에서 NFT 컬렉션을 단계별로 구축해 보겠습니다.

\*\*이 튜토리얼이 끝날 때까지 만들게 될 아름다운 오리 컬렉션은 다음과 같습니다.

![](/img/tutorials/nft/collection.png)

## 🦄 학습 내용

1. TON에서 NFT 컬렉션을 발행합니다.
2. TON의 NFT가 어떻게 작동하는지 이해하게 될 것입니다.
3. NFT를 판매합니다.
4. 핀타 클라우드](https://pinata.cloud)에 메타데이터를 업로드합니다.

## 💡 전제 조건

2톤 이상의 테스트넷 지갑이 이미 있어야 합니다. 테스트넷 코인은 [@testgiver_ton_bot](https://t.me/testgiver_ton_bot)에서 받을 수 있습니다.

:::info 톤키퍼 지갑의 테스트넷 버전은 어떻게 열 수 있나요?\
톤키퍼에서 테스트넷 네트워크를 열려면 설정으로 이동하여 하단에 있는 톤키퍼 로고를 5번 클릭한 후 메인넷 대신 테스트넷을 선택합니다.
:::

Pinata를 IPFS 스토리지 시스템으로 사용할 것이므로 [pinata.cloud](https://pinata.cloud)에서 계정을 만들고 api_key 및 api_secreat를 받아야 합니다. 공식 Pinata [문서 튜토리얼](https://docs.pinata.cloud/pinata-api/authentication)에서 도움을 받을 수 있습니다. 이 API 토큰을 받으시면 여기서 기다리고 있을게요!!!

## 💎 TON의 NFT란 무엇인가요?

튜토리얼의 주요 부분을 시작하기 전에 실제로 NFT가 TON에서 일반적으로 어떻게 작동하는지 이해해야합니다. 그리고 예기치 않게도 업계의 일반적인 블록체인과 비교하여 TON에서 NFT 구현의 특성이 무엇인지 이해하기 위해 NFT가 ETH에서 어떻게 작동하는지에 대한 설명부터 시작하겠습니다.

### 이더리움에서 NFT 구현

이더리움에서 NFT를 구현하는 것은 매우 간단합니다. 간단한 해시맵을 저장하는 컬렉션의 메인 컨트랙트가 하나 있고, 이 컬렉션의 NFT 데이터를 저장하는 컨트랙트가 하나 있습니다. 이 컬렉션과 관련된 모든 요청(사용자가 NFT를 전송하거나 판매하고자 하는 경우 등)은 이 컬렉션의 컨트랙트 1개로만 전송됩니다.

![](/img/tutorials/nft/eth-collection.png)

### TON에서 이러한 구현으로 발생할 수 있는 문제

TON의 맥락에서 이러한 구현의 문제점은 TON의 [NFT 스탠드아트](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md)에 완벽하게 설명되어 있습니다:

- 예측할 수 없는 가스 소비. TON에서 사전 연산을 위한 가스 소비량은 정확한 키 세트에 따라 달라집니다. 또한 TON은 비동기식 블록체인입니다. 즉, 스마트 컨트랙트에 메시지를 보내면 메시지 이전에 다른 사용자의 메시지가 얼마나 많은 스마트 컨트랙트에 도달할지 알 수 없습니다. 따라서 메시지가 스마트 콘트랙트에 도달하는 순간 사전의 크기가 어떻게 될지 알 수 없습니다. 이는 단순한 지갑-> NFT 스마트 컨트랙트 상호작용에서는 괜찮지만, 지갑-> NFT 스마트 컨트랙트-> 경매-> NFT 스마트 컨트랙트와 같은 스마트 컨트랙트 체인에서는 허용되지 않습니다. 가스 소비량을 예측할 수 없는 경우, NFT 스마트 컨트랙트에서 소유자가 변경되었지만 경매 작업에 필요한 톤코인이 충분하지 않은 상황이 발생할 수 있습니다. 사전 없이 스마트 컨트랙트를 사용하면 가스 소비량을 결정적으로 예측할 수 있습니다.

- 확장되지 않음(병목 현상이 발생함). TON의 확장은 샤딩, 즉 부하가 걸렸을 때 네트워크를 샤드체인으로 자동 분할하는 개념을 기반으로 합니다. 인기있는 NFT의 단일 대형 스마트 콘트랙트는 이 개념과 모순됩니다. 이 경우 많은 트랜잭션이 하나의 스마트 콘트랙트를 참조하게 됩니다. TON 아키텍처는 샤드화된 스마트 콘트랙트를 제공하지만(백서 참조), 현재로서는 구현되지 않았습니다.

\*확장성이 떨어지고 TON과 같은 비동기식 블록체인에는 적합하지 않은 TL;DR ETH 솔루션입니다.

### TON NFT 구현

TON에는 메타데이터와 소유자의 주소를 저장하는 컬렉션의 스마트 컨트랙트인 마스터 컨트랙트가 하나 있으며, 가장 중요한 것은 새로운 NFT 아이템을 생성("민트")하고 싶다면 이 컬렉션 컨트랙트에 메시지를 보내기만 하면 된다는 점입니다. 그리고 이 컬렉션 컨트랙트는 우리가 제공한 데이터와 함께 새로운 NFT 아이템의 컨트랙트를 배포합니다.

![](/img/tutorials/nft/ton-collection.png)

:::info
이 주제에 대해 더 자세히 알아보려면 [TON에서의 NFT 처리](/develop/dapps/asset-processing/nfts) 문서를 확인하거나 [NFT 표준](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md) 문서를 읽어보시기 바랍니다.
:::

## ⚙ 개발 환경 설정

빈 프로젝트를 만드는 것부터 시작하겠습니다:

1. 새 폴더 만들기
   `mkdir MintyTON`
2. 이 폴더 열기
   `cd MintyTON`
3. 프로젝트 `yarn init -y`를 초기화합니다.
4. 타입스크립트 설치

```
yarn add typescript @types/node -D
```

5. 이 구성을 tsconfig.json에 복사합니다.

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

6. 패키지.json에 앱 빌드 및 시작 스크립트 추가하기

```json
"scripts": {
    "start": "tsc --skipLibCheck && node dist/app.js"
  },
```

7. 필수 라이브러리 설치

```
yarn add @pinata/sdk dotenv ton ton-core ton-crypto
```

8. .env\` 파일을 만들고 이 템플릿을 기반으로 자체 데이터를 추가합니다.

```
PINATA_API_KEY=your_api_key
PINATA_API_SECRET=your_secret_api_key
MNEMONIC=word1 word2 word3 word4
TONCENTER_API_KEY=aslfjaskdfjasasfas
```

톤센터 API 키는 [@tonapibot](https://t.me/tonapibot)에서 받을 수 있으며 메인넷 또는 테스트넷을 선택할 수 있습니다. MNEMONIC\` 변수에 컬렉션 소유자 지갑 시드 문구 24단어를 저장합니다.

훌륭합니다! 이제 프로젝트의 코드 작성을 시작할 준비가 되었습니다.

### 쓰기 도우미 함수

먼저 `src/utils.ts`에 니모닉으로 지갑을 열고 지갑의 publicKey/secretKey를 반환하는 함수를 만들어 보겠습니다.

24개의 단어(시드 구문)를 기반으로 한 쌍의 키를 얻습니다:

```ts
import { KeyPair, mnemonicToPrivateKey } from "ton-crypto";
import {
  beginCell,
  Cell,
  OpenedContract,
  TonClient,
  WalletContractV4,
} from "ton";

export type OpenedWallet = {
  contract: OpenedContract<WalletContractV4>;
  keyPair: KeyPair;
};

export async function openWallet(mnemonic: string[], testnet: boolean) {
  const keyPair = await mnemonicToPrivateKey(mnemonic);
}
```

톤센터와 상호 작용할 클래스 인스턴스를 생성합니다:

```ts
const toncenterBaseEndpoint: string = testnet
  ? "https://testnet.toncenter.com"
  : "https://toncenter.com";

const client = new TonClient({
  endpoint: `${toncenterBaseEndpoint}/api/v2/jsonRPC`,
  apiKey: process.env.TONCENTER_API_KEY,
});
```

그리고 마지막으로 지갑을 엽니다:

```ts
const wallet = WalletContractV4.create({
    workchain: 0,
    publicKey: keyPair.publicKey,
  });

const contract = client.open(wallet);
return { contract, keyPair };
```

이제 프로젝트의 메인 엔트리포인트인 `app.ts`를 생성하겠습니다.
여기서는 방금 만든 함수 `openWallet`을 사용하고 메인 함수 `init`을 호출합니다.
여기까지입니다.

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

마지막으로 `seqno`가 증가할 때까지 기다리는 함수를 만드는 `delay.ts` 파일을 만들어 보겠습니다.

```ts
import { OpenedWallet } from "utils";

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

:::info seqno란 무엇인가요?
간단히 말해서, Seqno는 지갑으로 전송된 발신 트랜잭션의 카운터일 뿐입니다.
리플레이 공격을 방지하는 데 사용됩니다. 트랜잭션이 지갑 스마트 콘트랙트로 전송되면, 지갑은 트랜잭션의 seqno 필드를 저장소 내부의 필드와 비교합니다. 일치하면 트랜잭션이 승인되고 저장된 seqno가 1씩 증가합니다. 일치하지 않으면 트랜잭션이 삭제됩니다. 그렇기 때문에 모든 발신 트랜잭션 후에 잠시 기다려야 합니다.
:::

## 🖼 메타데이터 준비

메타데이터 - NFT 또는 컬렉션을 설명하는 간단한 정보입니다. 예를 들어 이름, 설명 등이 있습니다.

먼저, `/data/images`에 `0.png`, `1.png`, ...라는 이름의 NFT 이미지를 저장하고, 아이템 사진의 경우 `logo.png`, 컬렉션 아바타의 경우 `logo.png`로 저장해야 합니다. 오리 이미지가 포함된 [다운로드 팩](/img/tutorials/nft/ducks.zip)을 쉽게 다운로드하거나 해당 폴더에 이미지를 넣을 수 있습니다. 또한 모든 메타데이터 파일은 `/data/metadata/` 폴더에 저장합니다.

### NFT 사양

TON의 대부분의 제품은 이러한 메타데이터 사양을 지원하여 NFT 수집에 대한 정보를 저장합니다:

| 이름     | 설명                                                                                              |
| ------ | ----------------------------------------------------------------------------------------------- |
| 이름     | 컬렉션 이름                                                                                          |
| 설명     | 컬렉션 설명                                                                                          |
| 이미지    | 아바타로 표시될 이미지로 연결되는 링크를 클릭합니다. 지원되는 링크 형식 https, ipfs, TON 스토리지. |
| 커버 이미지 | 이미지에 링크하면 컬렉션의 표지 이미지로 표시됩니다.                                                   |
| 소셜 링크  | 프로젝트의 소셜 미디어 프로필에 대한 링크 목록입니다. 링크는 10개 이하로 사용하세요.               |

![이미지](/img/tutorials/nft/collection-metadata.png)

이 정보를 바탕으로 컬렉션의 메타데이터를 설명하는 자체 메타데이터 파일 `collection.json`을 만들어 보겠습니다!

```json
{
  "name": "Ducks on TON",
  "description": "This collection is created for showing an example of minting NFT collection on TON. You can support creator by buying one of this NFT.",
  "social_links": ["https://t.me/DucksOnTON"]
}
```

"이미지" 매개 변수를 작성하지 않았으니 조금만 기다리시면 그 이유를 알게 될 것입니다!

컬렉션 메타데이터 파일을 생성한 후에는 NFT의 메타데이터를 생성해야 합니다.

NFT 아이템 메타데이터 사양:

| 이름                                | 설명                                                                                                                          |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| 이름                                | NFT 이름. 권장 길이: 15~30자 이내                                                    |
| 설명                                | NFT 설명. 권장 길이: 최대 500자                                                                      |
| 이미지                               | NFT 이미지에 링크합니다.                                                                                             |
| 속성                                | NFT 속성. 특성 유형(특성 이름)과 값(속성에 대한 간단한 설명)이 지정된 특성 목록입니다. |
| lottie                            | 로티 애니메이션이 포함된 json 파일에 링크합니다.  지정하면 이 링크의 로티 애니메이션이 NFT가 있는 페이지에서 재생됩니다.                    |
| content_url  | 추가 콘텐츠로 연결되는 링크입니다.                                                                                         |
| content_type | content_url 링크를 통해 추가된 콘텐츠 유형입니다. 예를 들어 동영상/mp4 파일입니다.                 |

![이미지](/img/tutorials/nft/item-metadata.png)

```json
{
  "name": "Duck #00",
  "description": "What about a round of golf?",
  "attributes": [{ "trait_type": "Awesomeness", "value": "Super cool" }]
}
```

그런 다음 메타데이터가 포함된 NFT 항목의 파일을 원하는 만큼 만들 수 있습니다.

### 메타데이터 업로드

이제 메타데이터 파일을 IPFS에 업로드하는 코드를 작성해 보겠습니다. 메타데이터.ts\` 파일을 만들고 필요한 모든 임포트를 추가합니다:

```ts
import pinataSDK from "@pinata/sdk";
import { readdirSync } from "fs";
import { writeFile, readFile } from "fs/promises";
import path from "path";
```

그런 다음 실제로 폴더의 모든 파일을 IPFS로 업로드하는 함수를 만들어야 합니다:

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

훌륭합니다! 다시 당면한 질문으로 돌아가서 메타데이터 파일의 '이미지' 필드를 비워둔 이유는 무엇일까요? 컬렉션에 1000개의 NFT를 만들고 싶고, 이에 따라 각 항목을 수동으로 살펴보고 사진 링크를 수동으로 삽입해야 하는 상황을 상상해 보겠습니다.
이것은 정말 불편하고 잘못된 일이므로 이 작업을 자동으로 수행하는 함수를 작성해 봅시다!

```ts
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

먼저 지정된 폴더에 있는 모든 파일을 읽습니다:

```ts
const files = readdirSync(metadataFolderPath);
```

각 파일을 반복하여 콘텐츠를 가져옵니다.

```ts
const filePath = path.join(metadataFolderPath, filename)
const file = await readFile(filePath);

const metadata = JSON.parse(file.toString());
```

그런 다음 폴더의 마지막 파일이 아닌 경우 이미지 필드에 `ipfs://{IpfsHash}/{index}.jpg` 값을 할당하고, 그렇지 않으면 `ipfs://{imagesIpfsHash}/logo.jpg`를 할당하여 실제로 새 데이터로 파일을 다시 작성합니다.

메타데이터.ts의 전체 코드:

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

좋아요, app.ts 파일에서 이 메서드를 호출해 보겠습니다.
함수의 임포트를 추가합니다:

```ts
import { updateMetadataFiles, uploadFolderToIPFS } from "./metadata";
```

메타데이터/이미지 폴더에 경로와 함께 변수를 저장하고 함수를 호출하여 메타데이터를 업로드합니다.

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

그 후 'yarn start'를 실행하면 배포된 메타데이터에 대한 링크를 확인할 수 있습니다!

### 오프체인 콘텐츠 인코딩

스마트 컨트랙트에 저장된 메타데이터 파일에 어떻게 연결되나요? 이 질문은 [토큰 데이터 표준](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md)에서 충분히 답변할 수 있습니다.
어떤 경우에는 단순히 원하는 플래그를 제공하고 링크를 ASCII 문자로 제공하는 것만으로는 충분하지 않을 수 있으므로 스네이크 형식을 사용하여 링크를 여러 부분으로 분할해야 하는 옵션을 고려해 보겠습니다.

먼저 버퍼를 청크로 변환하는 함수를 생성합니다:

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

마지막으로 이 함수를 사용하여 오프체인 콘텐츠를 셀로 인코딩하는 함수를 만들어야 합니다:

```ts
export function encodeOffChainContent(content: string) {
  let data = Buffer.from(content);
  const offChainPrefix = Buffer.from([0x01]);
  data = Buffer.concat([offChainPrefix, data]);
  return makeSnakeCell(data);
}
```

## 🚢 NFT 컬렉션 배포

메타데이터가 준비되고 이미 IPFS에 업로드되면 컬렉션 배포부터 시작하면 됩니다!

컬렉션과 관련된 모든 로직을 `/contracts/NftCollection.ts` 파일에 저장하는 파일을 생성합니다. 항상 그렇듯이 임포트로 시작합니다:

```ts
import {
  Address,
  Cell,
  internal,
  beginCell,
  contractAddress,
  StateInit,
  SendMode,
} from "ton-core";
import { encodeOffChainContent, OpenedWallet } from "../utils";
```

그리고 수집에 필요한 초기화 데이터를 설명하는 유형을 선언합니다:

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

| 이름          | 설명                                                                           |
| ----------- | ---------------------------------------------------------------------------- |
| 소유자 주소      | 컬렉션의 소유자로 설정할 주소입니다. 소유자만 새 NFT를 발행할 수 있습니다. |
| 로열티퍼센트      | 각 판매 금액의 백분율로 지정된 주소로 전송됩니다.                                 |
| 로열티주소       | 이 NFT 컬렉션의 판매로 로열티를 받을 지갑 주소                                                 |
| 다음 항목 인덱스   | 다음 NFT 항목이 가져야 하는 인덱스입니다.                                    |
| 컬렉션 콘텐츠 URL | 컬렉션 메타데이터에 대한 URL                                                            |
| 공통 콘텐츠 URL  | NFT 아이템 메타데이터의 기본 URL                                                        |

먼저 컬렉션의 코드가 포함된 셀을 반환하는 비공개 메서드를 작성해 보겠습니다.

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

이 코드에서는 컬렉션 스마트 컨트랙트의 base64 표현에서 셀을 읽었습니다.

이제 컬렉션의 초기 데이터가 있는 셀만 남았습니다.
기본적으로 컬렉션데이터의 데이터를 올바른 방식으로 저장하기만 하면 됩니다. 먼저 빈 셀을 만들고 거기에 컬렉션 소유자 주소와 다음에 발행할 아이템의 인덱스를 저장해야 합니다.

```ts
private createDataCell(): Cell {
  const data = this.collectionData;
  const dataCell = beginCell();

  dataCell.storeAddress(data.ownerAddress);
  dataCell.storeUint(data.nextItemIndex, 64);
```

그 다음에는 컬렉션의 콘텐츠를 저장할 빈 셀을 만들고, 그 뒤에 컬렉션의 인코딩된 콘텐츠가 있는 셀을 참조하는 store 참조를 만듭니다. 그리고 그 바로 뒤에 메인 데이터 셀의 contentCell을 참조합니다.

```ts
const contentCell = beginCell();

const collectionContent = encodeOffChainContent(data.collectionContentUrl);

const commonContent = beginCell();
commonContent.storeBuffer(Buffer.from(data.commonContentUrl));

contentCell.storeRef(collectionContent);
contentCell.storeRef(commonContent.asCell());
dataCell.storeRef(contentCell);
```

그런 다음 컬렉션에 생성될 NFT 아이템의 코드 셀을 생성하고 이 셀에 대한 참조를 데이터셀에 저장합니다.

```ts
const NftItemCodeCell = Cell.fromBase64(
  "te6cckECDQEAAdAAART/APSkE/S88sgLAQIBYgMCAAmhH5/gBQICzgcEAgEgBgUAHQDyMs/WM8WAc8WzMntVIAA7O1E0NM/+kAg10nCAJp/AfpA1DAQJBAj4DBwWW1tgAgEgCQgAET6RDBwuvLhTYALXDIhxwCSXwPg0NMDAXGwkl8D4PpA+kAx+gAxcdch+gAx+gAw8AIEs44UMGwiNFIyxwXy4ZUB+kDUMBAj8APgBtMf0z+CEF/MPRRSMLqOhzIQN14yQBPgMDQ0NTWCEC/LJqISuuMCXwSED/LwgCwoAcnCCEIt3FzUFyMv/UATPFhAkgEBwgBDIywVQB88WUAX6AhXLahLLH8s/Im6zlFjPFwGRMuIByQH7AAH2UTXHBfLhkfpAIfAB+kDSADH6AIIK+vCAG6EhlFMVoKHeItcLAcMAIJIGoZE24iDC//LhkiGOPoIQBRONkchQCc8WUAvPFnEkSRRURqBwgBDIywVQB88WUAX6AhXLahLLH8s/Im6zlFjPFwGRMuIByQH7ABBHlBAqN1viDACCAo41JvABghDVMnbbEDdEAG1xcIAQyMsFUAfPFlAF+gIVy2oSyx/LPyJus5RYzxcBkTLiAckB+wCTMDI04lUC8ANqhGIu"
);
dataCell.storeRef(NftItemCodeCell);
```

스마트 컨트랙트에 저장된 로열티 매개변수는 로열티팩터, 로열티베이스, 로열티주소입니다. 로열티 퍼센트는 '(로열티팩터/로열티베이스) \* 100%'라는 공식으로 계산할 수 있습니다. 따라서 로열티 퍼센트를 알고 있다면 로열티 팩터를 구하는 것은 문제가 되지 않습니다.

```ts
const royaltyBase = 1000;
const royaltyFactor = Math.floor(data.royaltyPercent * royaltyBase);
```

계산 후에는 로열티 데이터를 별도의 셀에 저장하고 데이터셀에 이 셀에 대한 참조를 제공해야 합니다.

```ts
const royaltyCell = beginCell();
royaltyCell.storeUint(royaltyFactor, 16);
royaltyCell.storeUint(royaltyBase, 16);
royaltyCell.storeAddress(data.royaltyAddress);
dataCell.storeRef(royaltyCell);

return dataCell.endCell();
}
```

이제 실제로 컬렉션의 StateInit을 반환하는 getter를 작성해 보겠습니다:

```ts
public get stateInit(): StateInit {
  const code = this.createCodeCell();
  const data = this.createDataCell();

  return { code, data };
}
```

그리고 게터는 컬렉션의 주소를 계산합니다(TON의 스마트 컨트랙트 주소는 StateInit의 해시일 뿐입니다).

```ts
public get address(): Address {
    return contractAddress(0, this.stateInit);
  }
```

이제 스마트 컨트랙트를 블록체인에 배포하는 메서드 작성만 남았습니다!

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

우리의 경우 새로운 스마트 컨트랙트를 배포하는 것은 지갑에서 수집 주소(StateInit이 있으면 계산할 수 있는 주소)로 메시지를 보내는 것뿐이며, StateInit이 있습니다!

소유자가 새로운 NFT를 발행하면 컬렉션은 소유자의 메시지를 수락하고 생성된 NFT 스마트 컨트랙트에 새로운 메시지를 전송하므로(수수료 지불 필요), 발행된 NFT의 수에 따라 컬렉션의 잔액을 보충하는 메서드를 작성해 보겠습니다:

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

이제 `app.ts`에 몇 줄을 추가하여 새 컬렉션을 배포해 보겠습니다:

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

컬렉션이 준비되면 NFT 발행을 시작할 수 있습니다! 우리는 `src/contracts/NftItem.ts`에 코드를 저장할 것입니다.

예기치 않게, 이제 `NftCollection.ts`로 돌아가야 합니다. 그리고 이 유형을 파일 맨 위에 있는 `collectionData` 근처에 추가합니다.

```ts
export type mintParams = {
  queryId: number | null,
  itemOwnerAddress: Address,
  itemIndex: number,
  amount: bigint,
  commonContentUrl: string
}
```

| 이름         | 설명                                                                                        |
| ---------- | ----------------------------------------------------------------------------------------- |
| 항목 소유자 주소  | 항목의 소유자로 설정할 주소                                                                           |
| 항목 인덱스     | NFT 항목 인덱스                                                                                |
| 금액         | 배포와 함께 NFT로 전송되는 TON의 양은 다음과 같습니다.                                        |
| 공통 콘텐츠 URL | 항목 URL에 대한 전체 링크는 컬렉션의 "commonContentUl" + 이 commonContentUl로 표시할 수 있습니다. |

그리고 NFT 아이템의 배포를 위한 본문을 구성하는 메서드를 NftCollection 클래스에서 생성합니다. 먼저 비트를 저장하여 스마트 컨트랙트 컬렉션에 새로운 NFT를 생성할 것임을 알립니다. 그런 다음 이 NFT 아이템의 쿼리아이디와 인덱스를 저장합니다.

```ts
public createMintBody(params: mintParams): Cell {
    const body = beginCell();
    body.storeUint(1, 32);
    body.storeUint(params.queryId || 0, 64);
    body.storeUint(params.itemIndex, 64);
    body.storeCoins(params.amount);
  }
```

나중에 이 NFT의 빈 셀과 스토어 소유자 주소를 생성합니다:

```ts
    const nftItemContent = beginCell();
    nftItemContent.storeAddress(params.itemOwnerAddress);
```

그리고 이 셀에 저장된 참조(NFT 아이템 콘텐츠 포함)는 이 아이템의 메타데이터를 참조합니다:

```ts
const uriContent = beginCell();
uriContent.storeBuffer(Buffer.from(params.commonContentUrl));
nftItemContent.storeRef(uriContent.endCell());
```

저장소는 본문 셀의 항목 콘텐츠가 있는 셀을 참조합니다:

```ts
body.storeRef(nftItemContent.endCell());
return body.endCell();
```

좋아요! 이제 `NftItem.ts`로 돌아올 수 있습니다. 이제 NFT 본문과 함께 수집 컨트랙트에 메시지를 보내기만 하면 됩니다.

```ts
import { internal, SendMode } from "ton-core";
import { OpenedWallet } from "utils";
import { NftCollection, mintParams } from "./NftCollection";

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

마지막에는 인덱스로 NFT의 주소를 가져오는 짧은 메서드를 작성하겠습니다.

컬렉션의 get 메서드를 호출하는 데 도움이 되는 클라이언트 변수 생성부터 시작하세요.

```ts
static async getAddressByIndex(
  collectionAddress: Address,
  itemIndex: number
): Promise<Address> {
  const client = new TonClient({
    endpoint: "https://testnet.toncenter.com/api/v2/jsonRPC",
    apiKey: process.env.TONCENTER_API_KEY,
  });
}
```

그런 다음 컬렉션의 get-method를 호출하여 해당 인덱스가 있는 이 컬렉션의 NFT 주소를 반환합니다.

```ts
const response = await client.runMethod(
  collectionAddress,
  "get_nft_address_by_index",
  [{ type: "int", value: BigInt(itemIndex) }]
);
```

... 그리고 이 주소를 파싱하세요!

```ts
return response.stack.readAddress();
```

이제 `app.ts`에 몇 가지 코드를 추가하여 각 NFT의 발행 프로세스를 자동화해 보겠습니다. 먼저 메타데이터가 있는 폴더의 모든 파일을 읽습니다:

```ts
const files = await readdir(metadataFolderPath);
files.pop();
let index = 0;
```

두 번째로 컬렉션의 잔액을 충전하세요:

```ts
seqno = await collection.topUpBalance(wallet, files.length);
await waitSeqno(seqno, wallet);
console.log(`Balance top-upped`);
```

마지막으로 메타데이터가 있는 각 파일을 살펴보고 `NftItem` 인스턴스를 생성한 후 배포 메서드를 호출합니다. 그 후 seqno가 증가할 때까지 잠시 기다려야 합니다:

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

NFT를 판매하려면 두 개의 스마트 컨트랙트가 필요합니다.

- 신규 매출 창출 논리만 담당하는 마켓플레이스
- 판매 계약 - 판매 구매/취소 로직을 담당합니다.

### 마켓플레이스 배포

계약/NftMarketplace.ts\`에 새 파일을 생성합니다. 평소와 같이 이 마켓플레이스 소유자의 주소를 받는 기본 클래스를 생성하고, 이 스마트 컨트랙트 및 초기 데이터의 코드(NFT-Marketplace 스마트 컨트랙트 기본 버전(https://github.com/ton-blockchain/token-contract/blob/main/nft/nft-marketplace.fc)를 사용하겠습니다)로 셀을 생성합니다.

```ts
import {
  Address,
  beginCell,
  Cell,
  contractAddress,
  internal,
  SendMode,
  StateInit,
} from "ton-core";
import { OpenedWallet } from "utils";

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

그리고 StateInit을 기반으로 스마트 컨트랙트의 주소를 계산하는 메서드를 만들어 보겠습니다:

```ts
public get address(): Address {
    return contractAddress(0, this.stateInit);
  }
```

그 후에는 실제로 마켓플레이스를 배포할 수 있는 방법을 만들어야 합니다:

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

보시다시피, 이 코드는 다른 스마트 컨트랙트 배포와 다르지 않습니다(새 컬렉션 배포의 nft-item 스마트 컨트랙트). 유일한 점은 처음에 마켓플레이스를 0.05톤이 아닌 0.5톤씩 보충한다는 것입니다. 그 이유는 무엇일까요?  새로운 스마트 판매 콘트랙트가 배포되면 마켓플레이스는 요청을 수락하고 처리한 후 새 콘트랙트에 메시지를 전송합니다(예, NFT 컬렉션의 상황과 유사합니다). 그렇기 때문에 수수료를 지불하기 위해 약간의 추가 톤이 필요합니다.

마지막으로 `app.ts` 파일에 몇 줄의 코드를 추가하여 마켓플레이스를 배포해 보겠습니다:

```ts
console.log("Start deploy of new marketplace  ");
const marketplace = new NftMarketplace(wallet.contract.address);
seqno = await marketplace.deploy(wallet);
await waitSeqno(seqno, wallet);
console.log("Successfully deployed new marketplace");
```

### 판매 계약 배포

훌륭합니다! 지금 바로 NFT 판매의 스마트 컨트랙트를 배포할 수 있습니다. 어떻게 작동할까요? 새로운 컨트랙트를 배포한 후, NFT를 판매 컨트랙트로 "이전"해야 합니다(즉, 아이템 데이터에서 NFT의 소유자를 판매 컨트랙트로 변경하기만 하면 됩니다). 이 튜토리얼에서는 [nft-fixprice-sale-v2](https://github.com/getgems-io/nft-contracts/blob/main/packages/contracts/sources/nft-fixprice-sale-v2.fc) 판매 스마트 컨트랙트를 사용하겠습니다.

먼저 판매 스마트 컨트랙트의 데이터를 설명하는 새로운 유형을 선언해 보겠습니다:

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
} from "ton-core";
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

이제 스마트 컨트랙트의 초기화 데이터 셀을 생성할 클래스와 기본 메서드를 만들어 보겠습니다.

수수료 정보가 담긴 셀을 만드는 것부터 시작하겠습니다. 마켓플레이스 수수료를 받을 스토어 주소와 수수료로 마켓플레이스에 보낼 TON의 양을 입력해야 합니다. 판매에 따른 로열티를 받을 스토어 주소와 로열티 금액을 저장합니다.

```ts
export class NftSale {
  private data: GetGemsSaleData;

  constructor(data: GetGemsSaleData) {
    this.data = data;
  }

  private createDataCell(): Cell {
    const saleData = this.data;

    const feesCell = beginCell();

    feesCell.storeAddress(saleData.marketplaceFeeAddress);
    feesCell.storeCoins(saleData.marketplaceFee);
    feesCell.storeAddress(saleData.royaltyAddress);
    feesCell.storeCoins(saleData.royaltyAmount);
  }
}
```

그런 다음 빈 셀을 생성하고 판매 데이터의 정보를 올바른 순서로 저장한 다음 그 바로 뒤에 수수료 정보가 있는 셀을 참조하면 됩니다:

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
```

그리고 항상 그렇듯이 stateInit, 초기화 코드 셀 및 스마트 컨트랙트의 주소를 가져오는 메서드를 추가합니다.

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

판매 계약을 배포하기 위해 마켓플레이스에 보낼 메시지를 작성하고 실제로 이 메시지를 보내는 일만 남아 있습니다.

먼저, 새 판매 계약의 StateInit을 저장할 셀을 생성합니다.

```ts
public async deploy(wallet: OpenedWallet): Promise<number> {
    const stateInit = beginCell()
      .store(storeStateInit(this.stateInit))
      .endCell();
}
```

메시지 본문이 포함된 셀을 생성합니다. 먼저 연산 코드를 1로 설정해야 합니다(마켓플레이스에 새 판매 스마트 컨트랙트를 배포할 것임을 나타내기 위해). 그런 다음 새로운 판매 스마트 컨트랙트로 전송할 코인을 저장해야 합니다. 마지막으로 새 스마트 컨트랙트의 stateInit에 대한 참조 2와 이 새 스마트 컨트랙트로 전송될 본문을 저장해야 합니다.

```ts
const payload = beginCell();
payload.storeUint(1, 32);
payload.storeCoins(toNano("0.05"));
payload.storeRef(stateInit);
payload.storeRef(new Cell());
```

마지막으로 메시지를 보내겠습니다:

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
```

판매 스마트 컨트랙트가 배포되면 남은 것은 NFT 아이템의 소유자를 이 판매 주소로 변경하는 것뿐입니다.

### 항목 전송

아이템을 전송한다는 것은 무엇을 의미하나요? 소유자의 지갑에서 스마트 컨트랙트로 아이템의 새 소유자가 누구인지에 대한 정보를 담은 메시지를 전송하기만 하면 됩니다.

NftItem.ts\`로 이동하여 해당 메시지의 본문을 생성하는 새로운 정적 메서드를 NftItem 클래스에서 생성합니다:

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

  }
```

새 소유자의 작업 코드, 쿼리 ID, 주소 외에도 성공적인 전송 확인과 함께 응답을 보낼 주소와 수신 메시지 코인의 나머지 부분도 저장해야 합니다. 새 소유자에게 전달될 TON의 양과 문자 페이로드를 받을지 여부.

```ts
msgBody.storeAddress(params.responseTo || null);
msgBody.storeBit(false); // no custom payload
msgBody.storeCoins(params.forwardAmount || 0);
msgBody.storeBit(0); // no forward_payload 

return msgBody.endCell();
```

그리고 NFT를 전송하는 전송 함수를 생성합니다.

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

좋아요, 이제 거의 다 끝났습니다. 다시 `app.ts`로 돌아가서 판매할 NFT의 주소를 가져와 보겠습니다:

```ts
const nftToSaleAddress = await NftItem.getAddressByIndex(collection.address, 0);
```

판매에 대한 정보를 저장할 변수를 생성합니다:

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

이렇게 하면 판매 계약이 배포 시 코인을 수락하게 되므로 nftOwnerAddress를 null로 설정했습니다.

세일을 배포합니다:

```ts
const nftSaleContract = new NftSale(saleData);
seqno = await nftSaleContract.deploy(wallet);
await waitSeqno(seqno, wallet);
```

... 그리고 전송하세요!

```ts
await NftItem.transfer(wallet, nftToSaleAddress, nftSaleContract.address);
```

이제 프로젝트를 시작하고 그 과정을 즐길 수 있습니다!

```
yarn start
```

https://testnet.getgems.io/collection/\<YOUR_COLLECTION_ADDRESS_HERE> 으로 이동하여 이 완벽한 오리를 보세요!

## 결론

오늘 여러분은 TON에 대해 많은 새로운 것을 배웠고 테스트넷에서 자신만의 아름다운 NFT 컬렉션을 만들었습니다! 여전히 궁금한 점이 있거나 오류를 발견했다면 언제든지 작성자에게 편지를 보내주세요 - [@coalus](https://t.me/coalus).

## 참조

- [겟젬스 NFT 컨트랙트](https://github.com/getgems-io/nft-contracts)
- [NFT 스탠다드](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md)

## 저자 소개

- 텔레그램](https://t.me/coalus) 또는 [깃허브](https://github.com/coalus)에서 Coalus를 만나보세요.
