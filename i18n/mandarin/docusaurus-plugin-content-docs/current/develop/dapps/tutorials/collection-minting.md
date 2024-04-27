# 逐步创建 NFT 集合的教程

## 👋 引言

非同质化代币（NFT）已成为数字艺术和收藏品世界中最热门的话题之一。NFT是使用区块链技术验证所有权和真实性的独特数字资产。它们为创作者和收藏家提供了将数字艺术、音乐、视频和其他形式的数字内容货币化和交易的新可能性。近年来，NFT市场爆炸性增长，一些高调的销售额达到了数百万美元。在本文中，我们将逐步在TON上构建我们的NFT集合。

**这是你在本教程结束时将创建的鸭子集合的精美图片：**

![](/img/tutorials/nft/collection.png)

## 🦄 你将会学到什么

1. 你将在TON上铸造NFT集合
2. 你将理解TON上的NFT是如何工作的
3. 你将把NFT出售
4. 你将把元数据上传到[pinata.cloud](https://pinata.cloud)

## 💡 必要条件

你必须已经有一个测试网钱包，里面至少有2 TON。可以从[@testgiver_ton_bot](https://t.me/testgiver_ton_bot)获取测试网币。

:::info 如何打开我的Tonkeeper钱包的测试网版本？\
要在tonkeeper中打开测试网网络，请转到设置并点击位于底部的tonkeeper logo 5次，之后选择测试网而不是主网。
:::

我们将使用Pinata作为我们的IPFS存储系统，因此你还需要在[pinata.cloud](https://pinata.cloud)上创建一个帐户并获取api_key & api_secreat。官方Pinata [文档教程](https://docs.pinata.cloud/pinata-api/authentication)可以帮助完成这一点。只要你拿到这些api令牌，我就在这里等你！！！

## 💎 什么是 TON 上的 NFT?

在开始我们教程的主要部分之前，我们需要了解一下通常意义上TON中NFT是如何工作的。出乎意料的是，我们将从解释ETH中NFT的工作原理开始，为了理解TON中NFT实现的特殊性，与行业中常见的区块链相比。

### ETH 上的 NFT 实现

ETH中NFT的实现极其简单 - 存在1个主要的集合合约，它存储一个简单的哈希映射，该哈希映射反过来存储此集合中NFT的数据。所有与此集合相关的请求（如果任何用户想要转移NFT、将其出售等）都特别发送到此1个集合合约。

![](/img/tutorials/nft/eth-collection.png)

### 在 TON 中如此实现可能出现的问题

在TON的上下文中，此类实现的问题由[TON的NFT标准](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md)完美描述：

- 不可预测的燃料消耗。在TON中，字典操作的燃料消耗取决于确切的键集。此外，TON是一个异步区块链。这意味着，如果你向一个智能合约发送一个消息，那么你不知道有多少来自其他用户的消息会在你的消息之前到达智能合约。因此，你不知道当你的消息到达智能合约时字典的大小会是多少。这对于简单的钱包 -> NFT智能合约交互是可以的，但对于智能合约链，例如钱包 -> NFT智能合约 -> 拍卖 -> NFT智能合约，则不可接受。如果我们不能预测燃料消耗，那么可能会出现这样的情况：NFT智能合约上的所有者已经更改，但拍卖操作没有足够的Toncoin。不使用字典的智能合约可以提供确定性的燃料消耗。

- 不可扩展（成为瓶颈）。TON的扩展性基于分片的概念，即在负载下自动将网络划分为分片链。流行NFT的单个大智能合约与这一概念相矛盾。在这种情况下，许多交易将引用一个单一的智能合约。TON架构为分片的智能合约提供了设施（参见白皮书），但目前尚未实现。

_简而言之，ETH的解决方案不可扩展且不适用于像TON这样的异步区块链。_

### TON 上的 NFT 实现

在TON中，我们有1个主合约-我们集合的智能合约，它存储它的元数据和它所有者的地址，以及最重要的 - 如果我们想要创建（"铸造"）新的NFT项目 - 我们只需要向这个集合合约发送消息。而这个集合合约将为我们部署新NFT项目的合约，并提供我们提供的数据。

![](/img/tutorials/nft/ton-collection.png)

:::info
如果你想更深入地了解这个话题，可以查看[TON上的NFT处理](/develop/dapps/asset-processing/nfts)文章或阅读[NFT标准](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md)
:::

## ⚙ 设置开发环境

让我们从创建一个空项目开始：

1. 创建新文件夹
   `mkdir MintyTON`
2. 打开这个文件夹
   `cd MintyTON`
3. 初始化我们的项目 `yarn init -y`
4. 安装typescript

```
yarn add typescript @types/node -D
```

5. 将以下配置复制到tsconfig.json中

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

6. 向package.json添加脚本以构建并启动我们的应用程序

```json
"scripts": {
    "start": "tsc --skipLibCheck && node dist/app.js"
  },
```

7. 安装所需的库

```
yarn add @pinata/sdk dotenv ton ton-core ton-crypto
```

8. 创建`.env`文件并根据此模板添加你自己的数据

```
PINATA_API_KEY=your_api_key
PINATA_API_SECRET=your_secret_api_key
MNEMONIC=word1 word2 word3 word4
TONCENTER_API_KEY=aslfjaskdfjasasfas
```

你可以从[@tonapibot](https://t.me/tonapibot)获取toncenter api key并选择mainnet或testnet。在 `MNEMONIC` 变量中存储集合所有者钱包种子短语的24个单词。

太好了！现在我们准备好开始为我们的项目编写代码了。

### 编写辅助函数

首先，让我们在`src/utils.ts`中创建一个函数，该函数将通过助记词打开我们的钱包并返回它的publicKey/secretKey。

我们根据24个单词（种子短语）获取一对密钥：

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

创建一个类实例以与toncenter交互：

```ts
const toncenterBaseEndpoint: string = testnet
  ? "https://testnet.toncenter.com"
  : "https://toncenter.com";

const client = new TonClient({
  endpoint: `${toncenterBaseEndpoint}/api/v2/jsonRPC`,
  apiKey: process.env.TONCENTER_API_KEY,
});
```

最后打开我们的钱包：

```ts
const wallet = WalletContractV4.create({
    workchain: 0,
    publicKey: keyPair.publicKey,
  });

const contract = client.open(wallet);
return { contract, keyPair };
```

很好，之后我们将创建我们项目的主要入口点`app.ts`。
在这里，我们将使用刚刚创建的`openWallet`函数并调用我们的主函数`init`。
目前足够了。

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

最后，让我们创建`delay.ts`文件，在这个文件中，我们将创建一个函数来等待`seqno`增加。

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

:::info 什么是seqno?
简单来说，seqno就是由钱包发送的外部交易的计数器。
Seqno用于预防重放攻击。当交易发送到钱包智能合约时，它将交易的seqno字段与其存储中的字段进行比较。如果它们匹配，交易被接受并且存储的seqno增加一。如果它们不匹配，交易被丢弃。这就是为什么我们需要在每次发送外部交易后稍等一会儿。
:::

## 🖼 准备元数据

元数据 - 只是一些简单的信息，将描述我们的NFT或集合。例如它的名称、它的描述等。

首先，我们需要在`/data/images`中存储我们NFT的图片，命名为`0.png`、`1.png`...用于物品的照片，以及`logo.png`用于我们集合的头像。你可以轻松[下载](/img/tutorials/nft/ducks.zip)包含鸭子图片的包或将你的图片放入该文件夹。我们还将在`/data/metadata/`文件夹中存储所有的元数据文件。

### NFT 规范

TON上的大多数产品支持以下元数据规范来存储有关NFT集合的信息：

| 名称                                | 解释                                          |
| --------------------------------- | ------------------------------------------- |
| name                              | 集合名称                                        |
| description                       | 集合描述                                        |
| image                             | 将显示为头像的图片链接。支持的链接格式：https、ipfs、TON Storage。 |
| cover_image  | 将显示为集合封面图片的图片链接。                            |
| social_links | 项目社交媒体配置文件的链接列表。使用不超过10个链接。                 |

![image](/img/tutorials/nft/collection-metadata.png)

根据这些信息，让我们创建我们自己的元数据文件`collection.json`，它将描述我们集合的元数据！

```json
{
  "name": "Ducks on TON",
  "description": "This collection is created for showing an example of minting NFT collection on TON. You can support creator by buying one of this NFT.",
  "social_links": ["https://t.me/DucksOnTON"]
}
```

请注意，我们没有写"image"参数，稍后你会知道原因，请稍等！

在创建了集合的元数据文件之后，我们需要创建我们NFT的元数据。

NFT项目元数据的规范：

| 名称                                | 解释                                                                                                            |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| name                              | NFT名称。推荐长度：不超过15-30个字符                                                                                        |
| description                       | NFT描述。推荐长度：不超过500个字符                                                                                          |
| image                             | NFT图片链接。                                                                                                      |
| attributes                        | NFT属性。属性列表，其中指定了trait_type (属性名称)和value (属性的简短描述)。 |
| lottie                            | Lottie动画的json文件链接。如果指定，在NFT页面将播放来自此链接的Lottie动画。                                                               |
| content_url  | 额外内容的链接。                                                                                                      |
| content_type | 通过content_url链接添加的内容的类型。例如，视频/mp4文件。                                                     |

![image](/img/tutorials/nft/item-metadata.png)

```json
{
  "name": "Duck #00",
  "description": "What about a round of golf?",
  "attributes": [{ "trait_type": "Awesomeness", "value": "Super cool" }]
}
```

之后，你可以根据需要创建尽可能多的NFT项目及其元数据文件。

### 上传元数据

现在让我们编写一些代码，将我们的元数据文件上传到IPFS。创建 `metadata.ts` 文件并添加所需的导入：

```ts
import pinataSDK from "@pinata/sdk";
import { readdirSync } from "fs";
import { writeFile, readFile } from "fs/promises";
import path from "path";
```

之后，我们需要创建一个函数，这个函数将把我们文件夹中的所有文件实际上传到IPFS：

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

太棒了！让我们回到之前的问题：为什么我们在元数据文件中留下了“image”字段为空？想象一下你想在你的集合中创建1000个NFT，并且你必须手动遍历每个项目并手动插入图片链接。
这真的很不方便，所以让我们编写一个函数来自动完成这个操作！

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

这里我们首先读取指定文件夹中的所有文件：

```ts
const files = readdirSync(metadataFolderPath);
```

遍历每个文件并获取其内容

```ts
const filePath = path.join(metadataFolderPath, filename)
const file = await readFile(filePath);

const metadata = JSON.parse(file.toString());
```

之后，如果不是文件夹中的最后一个文件，我们将图像字段的值分配为 `ipfs://{IpfsHash}/{index}.jpg`，否则为 `ipfs://{imagesIpfsHash}/logo.jpg` 并实际用新数据重写我们的文件。

metadata.ts 的完整代码：

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

太好了，让我们在我们的 app.ts 文件中调用这些方法。
添加我们函数的导入：

```ts
import { updateMetadataFiles, uploadFolderToIPFS } from "./metadata";
```

保存元数据/图片文件夹路径变量并调用我们的函数上传元数据。

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

之后你可以运行 `yarn start` 并查看部署的元数据链接！

### 编码离线内容

我们如何将链接到智能合约中存储的元数据文件？这个问题可以通过[Token Data 标准](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md)得到完全回答。在某些情况下，仅仅提供所需的标志并以ASCII字符提供链接是不够的，这就是为什么我们考虑使用蛇形格式将我们的链接分成几个部分的选项。

首先创建一个函数，将我们的缓冲区转换成块：

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

并创建一个函数，将所有块绑定成1个蛇形cell：

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

最后，我们需要创建一个函数，使用这些函数将离线内容编码为cell：

```ts
export function encodeOffChainContent(content: string) {
  let data = Buffer.from(content);
  const offChainPrefix = Buffer.from([0x01]);
  data = Buffer.concat([offChainPrefix, data]);
  return makeSnakeCell(data);
}
```

## 🚢 部署 NFT 集合

当我们的元数据已经准备好并且已经上传到IPFS时，我们可以开始部署我们的集合了！

我们将在 `/contracts/NftCollection.ts` 文件中创建一个文件，该文件将存储与我们的集合相关的所有逻辑。我们将从导入开始：

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

并声明一个类型，它将描述我们集合所需的初始化数据：

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

| 名称                   | 解释                             |
| -------------------- | ------------------------------ |
| ownerAddress         | 将被设置为我们集合的所有者的地址。只有所有者能够铸造新NFT |
| royaltyPercent       | 每次销售金额的百分比，将转到指定地址             |
| royaltyAddress       | 将从这个NFT集合的销售中接收版税的钱包地址         |
| nextItemIndex        | 下一个NFT项目应该有的索引                 |
| collectionContentUrl | 集合元数据的URL                      |
| commonContentUrl     | NFT项目元数据的基础URL                 |

首先编写一个私有方法，用于返回带有我们集合代码的cell：

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

在这段代码中，我们只是从集合智能合约的base64表示中读取cell。

剩下的只有我们集合初始化数据的cell了。

```ts
private createDataCell(): Cell {
  const data = this.collectionData;
  const dataCell = beginCell();

  dataCell.storeAddress(data.ownerAddress);
  dataCell.storeUint(data.nextItemIndex, 64);
```

Next after that, we creating an empty cell that will store content of our collection, and after that store ref to the cell with encoded content of our collection. And right after that store ref to contentCell in our main data cell.

```ts
const contentCell = beginCell();

const collectionContent = encodeOffChainContent(data.collectionContentUrl);

const commonContent = beginCell();
commonContent.storeBuffer(Buffer.from(data.commonContentUrl));

contentCell.storeRef(collectionContent);
contentCell.storeRef(commonContent.asCell());
dataCell.storeRef(contentCell);
```

After that we just create cell of code of NFT item's, that will be created in our collection, and store ref to this cell in dataCell

```ts
const NftItemCodeCell = Cell.fromBase64(
  "te6cckECDQEAAdAAART/APSkE/S88sgLAQIBYgMCAAmhH5/gBQICzgcEAgEgBgUAHQDyMs/WM8WAc8WzMntVIAA7O1E0NM/+kAg10nCAJp/AfpA1DAQJBAj4DBwWW1tgAgEgCQgAET6RDBwuvLhTYALXDIhxwCSXwPg0NMDAXGwkl8D4PpA+kAx+gAxcdch+gAx+gAw8AIEs44UMGwiNFIyxwXy4ZUB+kDUMBAj8APgBtMf0z+CEF/MPRRSMLqOhzIQN14yQBPgMDQ0NTWCEC/LJqISuuMCXwSED/LwgCwoAcnCCEIt3FzUFyMv/UATPFhAkgEBwgBDIywVQB88WUAX6AhXLahLLH8s/Im6zlFjPFwGRMuIByQH7AAH2UTXHBfLhkfpAIfAB+kDSADH6AIIK+vCAG6EhlFMVoKHeItcLAcMAIJIGoZE24iDC//LhkiGOPoIQBRONkchQCc8WUAvPFnEkSRRURqBwgBDIywVQB88WUAX6AhXLahLLH8s/Im6zlFjPFwGRMuIByQH7ABBHlBAqN1viDACCAo41JvABghDVMnbbEDdEAG1xcIAQyMsFUAfPFlAF+gIVy2oSyx/LPyJus5RYzxcBkTLiAckB+wCTMDI04lUC8ANqhGIu"
);
dataCell.storeRef(NftItemCodeCell);
```

Royalty params stored in smart-contract by royaltyFactor, royaltyBase, royaltyAddress. Percentage of royalty can be calculated with the formula `(royaltyFactor / royaltyBase) * 100%`. So if we know royaltyPercent it's not a problem to get royaltyFactor.

```ts
const royaltyBase = 1000;
const royaltyFactor = Math.floor(data.royaltyPercent * royaltyBase);
```

After our calculations we need to store royalty data in separate cell and provide ref to this cell in dataCell.

```ts
const royaltyCell = beginCell();
royaltyCell.storeUint(royaltyFactor, 16);
royaltyCell.storeUint(royaltyBase, 16);
royaltyCell.storeAddress(data.royaltyAddress);
dataCell.storeRef(royaltyCell);

return dataCell.endCell();
}
```

Now let's actually write getter, that will return StateInit of our collection:

```ts
public get stateInit(): StateInit {
  const code = this.createCodeCell();
  const data = this.createDataCell();

  return { code, data };
}
```

And getter, that will calculate Address of our collection(address of smart-contract in TON is just hash of it's StateInit)

```ts
public get address(): Address {
    return contractAddress(0, this.stateInit);
  }
```

It remains only to write method, that will deploy the smart contract to the blockchain!

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

Deploy of new smart contract in our case - it's just sending a message from our wallet to the collection address(which one we can calculate if we have StateInit), with its StateInit!

在我们的情况下，部署新智能合约就是从我们的钱包向集合地址（如果我们有StateInit，则可以计算出此地址）发送消息！

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

Perfect, let's now add few lines to our `app.ts` to deploy new collection:

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

## 🚢 Deploy NFT Items

When our collection is ready, we can start minting our NFT! We will store code in `src/contracts/NftItem.ts`

当我们的收藏准备好后，我们可以开始铸造我们的NFT！我们将存储代码在`src/contracts/NftItem.ts`

```ts
export type mintParams = {
  queryId: number | null,
  itemOwnerAddress: Address,
  itemIndex: number,
  amount: bigint,
  commonContentUrl: string
}
```

| Name             | Explanation                                                                                            |
| ---------------- | ------------------------------------------------------------------------------------------------------ |
| itemOwnerAddress | Address that will be set as owner of item                                                              |
| itemIndex        | Index of NFT Item                                                                                      |
| amount           | Amount of TON, that will be sent to the NFT with deploy                                                |
| commonContentUrl | The full link to the Item URL can be shown as "commonContentUrl" of collection + this commonContentUrl |

And create method in NftCollection class, that will construct body for the deploy of our NFT Item. Firstly store bit, that will indicate to collection smart contract that we want to create new NFT. After that just store queryId & index of this NFT Item.

```ts
public createMintBody(params: mintParams): Cell {
    const body = beginCell();
    body.storeUint(1, 32);
    body.storeUint(params.queryId || 0, 64);
    body.storeUint(params.itemIndex, 64);
    body.storeCoins(params.amount);
  }
```

Later on create an empty cell and store owner address of this NFT:

```ts
    const nftItemContent = beginCell();
    nftItemContent.storeAddress(params.itemOwnerAddress);
```

And store ref in this cell(with NFT Item content) ref to the metadata of this item:

```ts
const uriContent = beginCell();
uriContent.storeBuffer(Buffer.from(params.commonContentUrl));
nftItemContent.storeRef(uriContent.endCell());
```

Store ref to cell with item content in our body cell:

```ts
body.storeRef(nftItemContent.endCell());
return body.endCell();
```

Great! Now we can comeback to `NftItem.ts`. All we have to do is just send message to our collection contract with body of our NFT.

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

By the end, we will write short method, that will get address of NFT by it's index.

最后，我们将编写简短方法，该方法将通过其索引获取NFT的地址。

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

Then we will call get-method of collection, that will return address of NFT in this collection with such index

```ts
const response = await client.runMethod(
  collectionAddress,
  "get_nft_address_by_index",
  [{ type: "int", value: BigInt(itemIndex) }]
);
```

... and parse this address!

```ts
return response.stack.readAddress();
```

Now let's add some code in `app.ts`, to automate the minting process of each NFT. Firstly read all of the files in folder with our metadata:

```ts
const files = await readdir(metadataFolderPath);
files.pop();
let index = 0;
```

Secondly top up balance of our collection:

```ts
seqno = await collection.topUpBalance(wallet, files.length);
await waitSeqno(seqno, wallet);
console.log(`Balance top-upped`);
```

Eventually, go through each file with metadata, create `NftItem` instance and call deploy method. After that we need to wait a bit, until the seqno increases:

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

## 🏷 Put NFT on sale

In order to put the nft for sale, we need two smart contracts.

- Marketplace, which is responsible only for logic of creating new sales
- Sale contract, which is responsible for the logic of buying/cancelling a sale

### Deploy marketplace

Create new file in `/contracts/NftMarketplace.ts`. As usual create basic class, which will accept address of owner of this marketplace and create cell with code(we will use [basic version of NFT-Marketplace smart-contract](https://github.com/ton-blockchain/token-contract/blob/main/nft/nft-marketplace.fc)) of this smart contract & initial data.

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

And let's create method, that will calculate address of our smart contract based on StateInit:

```ts
public get address(): Address {
    return contractAddress(0, this.stateInit);
  }
```

After that we need to create method, that will deploy our marketplace actually:

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

As you can see, this code does not differ from the deployment of other smart contracts (nft-item smart contract, from the deployment of a new collection). The only thing is that you can see that we initially replenish our marketplace not by 0.05 TON, but by 0.5. What is the reason for this?  When a new smart sales contract is deployed, the marketplace accepts the request, processes it, and sends a message to the new contract (yes, the situation is similar to the situation with the NFT collection). Which is why we need a little extra tone to pay fees.

如您所见，这段代码与其他智能合约的部署（nft-item智能合约，新集合的部署）并无不同。唯一的区别是您可以看到我们最初不是用0.05 TON而是用0.5 TON为我们的市场充值。这是什么原因呢？当部署新的智能销售合约时，市场接受请求，处理它，并向新合约发送消息（是的，情况类似于NFT集合）。这就是为什么我们需要额外的TON来支付费用。

```ts
console.log("Start deploy of new marketplace  ");
const marketplace = new NftMarketplace(wallet.contract.address);
seqno = await marketplace.deploy(wallet);
await waitSeqno(seqno, wallet);
console.log("Successfully deployed new marketplace");
```

### Deploy sale contract

Great! Right now we can already deploy smart contract of our NFT sale. How it will works? We need to deploy new contract, and after that "transfer" our nft to sale contract(in other words, we just need to change owner of our NFT to sale contract in item data). In this tutorial we will use [nft-fixprice-sale-v2](https://github.com/getgems-io/nft-contracts/blob/main/packages/contracts/sources/nft-fixprice-sale-v2.fc) sale smart contract.

太好了！现在我们已经可以部署我们NFT销售的智能合约了。它将如何工作？我们需要部署新合约，之后将我们的nft“转让”给销售合约（换句话说，我们只需改变我们NFT的所有者为销售合约中的数据项）。在本教程中，我们将使用[nft-fixprice-sale-v2](https://github.com/getgems-io/nft-contracts/blob/main/packages/contracts/sources/nft-fixprice-sale-v2.fc)销售智能合约。

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

And now let's create class, and basic method, that will create init data cell for our smart-contract.

现在让我们创建类，并创建一个基本方法，用于为我们的智能合约创建初始化数据cell。

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

Following that we can create an empty cell and just store in it information from saleData in correct order and right after that store ref to the cell with the fees information:

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

And as always add method's to get stateInit, init code cell and address of our smart contract.

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

It remains only to form a message that we will send to our marketplace to deploy sale contract and actually send this message

只剩下创建我们将发送到我们市场的消息以部署销售合约，并实际发送此消息

```ts
public async deploy(wallet: OpenedWallet): Promise<number> {
    const stateInit = beginCell()
      .store(storeStateInit(this.stateInit))
      .endCell();
}
```

Create cell with the body for our message. Firstly we need to set op-code to 1(to indicate marketplace, that we want to deploy new sale smart-contract). After that we need to store coins, that will be sent to our new sale smart-contract. And last of all we need to store 2 ref to stateInit of new smart-contract, and a body, that will be sent to this new smart-contract.

```ts
const payload = beginCell();
payload.storeUint(1, 32);
payload.storeCoins(toNano("0.05"));
payload.storeRef(stateInit);
payload.storeRef(new Cell());
```

And at the end let's send our message:

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

Perfect, when sale smart-contract is deployed all that's left is to change owner of our NFT Item to address of this sale.

### Transfer item

What does it mean to transfer an item? Simply send a message from the owner's wallet to the smart contract with information about who the new owner of the item is.

转移一个项目是什么意思？只需从所有者的钱包向智能合约发送消息，告知谁是该项目的新所有者即可。

转到`NftItem.ts`，并在NftItem类中创建一个新的静态方法，用于创建此类消息的主体：

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

In addition to the op-code, query-id and address of the new owner, we must also store the address where to send a response with confirmation of a successful transfer and the rest of the incoming message coins. The amount of TON that will come to the new owner and whether he will receive a text payload.

```ts
msgBody.storeAddress(params.responseTo || null);
msgBody.storeBit(false); // no custom payload
msgBody.storeCoins(params.forwardAmount || 0);
msgBody.storeBit(0); // no forward_payload 

return msgBody.endCell();
```

And create a transfer function to transfer the NFT.

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

Nice, now we can we are already very close to the end. Back to the `app.ts` and let's get address of our nft, that we want to put on sale:

```ts
const nftToSaleAddress = await NftItem.getAddressByIndex(collection.address, 0);
```

Create variable, that will store information about our sale:

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

Note, that we set nftOwnerAddress to null, because if we will do so, our sale contract would just accept our coins on deploy.

请注意，我们将nftOwnerAddress设置为null，因为如果这样做，我们的销售合约将只接受我们部署时的币值。

```ts
const nftSaleContract = new NftSale(saleData);
seqno = await nftSaleContract.deploy(wallet);
await waitSeqno(seqno, wallet);
```

... and transfer it!

```ts
await NftItem.transfer(wallet, nftToSaleAddress, nftSaleContract.address);
```

Now we can launch our project and enjoy the process!

```
yarn start
```

Go to https://testnet.getgems.io/collection/\<YOUR_COLLECTION_ADDRESS_HERE> and look to this perfect ducks!

## Conclusion

Today you have learned a lot of new things about TON and even created your own beautiful NFT collection in the testnet! If you still have any questions or have noticed an error - feel free to write to the author - [@coalus](https://t.me/coalus)

## References

- [GetGems NFT-contracts](https://github.com/getgems-io/nft-contracts)
- [NFT Standart](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md)

## About the author

- Coalus on [Telegram](https://t.me/coalus) or [GitHub](https://github.com/coalus)
