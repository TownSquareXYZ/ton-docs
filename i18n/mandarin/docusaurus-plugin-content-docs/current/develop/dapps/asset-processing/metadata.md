# TON Metadata Parsing

元数据标准涵盖NFT、NFT 收藏和Jetton，TON Enhancing Proposal 64 [TEP-64](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md)

关于TON，各实体可以有三种类型的元数据：链上、半链和外部链。

- **在链中的元数据：** 存储在区块链中，包括名称、属性和图像。
- **离链元数据：** 使用链接存储到链外托管的元数据文件。
- **半链元数据：** 两者之间的混合，允许区块链上的名称或属性等小字段存储。 当托管图像超链并只存储到它的链接。

## 吸附数据编码

Snake编码格式允许部分数据存储在标准化单元格， 其余部分存放在儿童牢房里(以递归方式)。 Snake编码格式必须使用0x00字节预设。 TL-B scheme:

```
text#_ {bn:#} b:(bits bn) = SnakeData ~0;
cons_ {bn:#} {n:#} b:(bits bn) 接下来：^(SnakeData ~n) = SnakeData ~(n + 1)；
```

当数据超过可存储在单个单元格中的最大尺寸时，吸附格式用于在单元格中存储额外数据。 这是通过将部分数据存储在根单元格中，其余部分存储在第一个儿童单元格中来实现的。 并继续递归地这样做，直到所有数据都已储存完毕。

下面是在 TypeScript 中的 Snake 格式编码和解码示例：

```typescript
export function makeSnakeCell(data: Buffer): Cell {
  const chunks = bufferToChunks(data, 127)

  if (chunks.length === 0) {
    return beginCell().endCell()
  }

  if (chunks.length === 1) {
    return beginCell().storeBuffer(chunks[0]).endCell()
  }

  let curCell = beginCell()

  for (let i = chunks.length - 1; i >= 0; i--) {
    const chunk = chunks[i]

    curCell.storeBuffer(chunk)

    if (i - 1 >= 0) {
      const nextCell = beginCell()
      nextCell.storeRef(curCell)
      curCell = nextCell
    }
  }

  return curCell.endCell()
}

export function flattenSnakeCell(cell: Cell): Buffer {
  let c: Cell | null = cell;

  const bitResult = new BitBuilder();
  while (c) {
    const cs = c.beginParse();
    if (cs.remainingBits === 0) {
      break;
    }

    const data = cs.loadBits(cs.remainingBits);
    bitResult.writeBits(data);
    c = c.refs && c.refs[0];
  }

  const endBits = bitResult.build();
  const reader = new BitReader(endBits);

  return reader.loadBuffer(reader.remaining / 8);
}
```

应该注意到，使用 snake 格式时，根单元格并不总是需要 `0x00` 字节前缀。 与链外NFT内容的情况相同。 此外，为了简化解析，单元格用字节而不是位填充。 为了避免在已经写入父单元之后(在下一个子单元中)添加提及的内容， 吸附单元格是按反向顺序构建的。

## 区块编码

区块编码格式用于使用字典数据结构存储数据，从区块索引到区块。 区块编码必须使用 '0x01' 字节前缀。 TL-B scheme:

```
chunked_data#_data:(HashMapE 32 ^(SnakeData ~0)) = ChunkedData;
```

下面是使用TypeScript解码区块数据的示例：

```typescript
interface ChunkDictValue {
  content: Buffer;
}
export const ChunkDictValueSerializer = {
  serialize(src: ChunkDictValue, builder: Builder) {},
  parse(src: Slice): ChunkDictValue {
    const snake = flattenSnakeCell(src.loadRef());
    return { content: snake };
  },
};

export function ParseChunkDict(cell: Slice): Buffer {
  const dict = cell.loadDict(
    Dictionary.Keys.Uint(32),
    ChunkDictValueSerializer
  );

  let buf = Buffer.alloc(0);
  for (const [_, v] of dict) {
    buf = Buffer.concat([buf, v.content]);
  }
  return buf;
}
```

## NFT 元数据属性

| 属性           | 类型        | 要求  | 描述                            |
| ------------ | --------- | --- | ----------------------------- |
| `uri`        | ASCII 字符串 | 可选的 | a URI指向JSON文档，元数据被“半链内容布局”使用。 |
| `name`       | UTF8 字符串  | 可选的 | 识别资产                          |
| `描述`         | UTF8 字符串  | 可选的 | 描述资产                          |
| `image`      | ASCII 字符串 | 可选的 | 一个 URI 指向一个带有mime 类型图像的资源     |
| `image_data` | 二进制\*     | 可选的 | 要么是二进制图像的链式布局或底层64的非链式布局。     |

## Jeton 元数据属性

1. `uri` - 可选的。 用于"半链内容布局"。 ASCII 字符串。 一个 URI 指向带元数据的 JSON 文档。
2. `name` - 可选的。 UTF8 字符串。 确认资产。
3. `description` - 可选的。 UTF8 字符串。 描述资产。
4. `image` - 可选的。 ASCII 字符串。 一个 URI 指向一个 mime 类型图像的资源。
5. `image_data` - 可选的。 要么是上链布局图像的二进制表现，要么是离链布局的基础64。
6. `symbol` - 可选的。 UTF8 字符串。 令牌的符号 - 例如"XMPL"。 用于表单“你收到了99 XMPL”。
7. `十进制` - 可选的。 如果未指定，则默认使用9。 UTF8 编码字符串的数字从 0 到 255。 代币使用的小数点数 - 例如8, 意味着将代币金额除以 100000000，以获得其用户代表性。
8. `amount_style` - 可选的。 需要外部应用程序来了解显示珠宝数量的格式。

- "n" - jettons 的数量 (默认值)。 如果用户有 100 个代币与小数位0，则显示该用户有 100 个代币。
- “无总数”——发放的珠宝总数中的珠宝数量。 例如，供应总量=1000。 用户在jetton钱包里有 100 jetton。 例如，必须在用户的钱包中显示1000个中的100个或任何其他文字或图形的方式来显示一般的特定情况。
- “%”——珠宝在发行珠宝总数中所占百分比。 例如，供应总量=1000。 用户在jetton钱包里有 100 jetton。 例如，它应该显示在用户的钱包中占10%。

9. `render_type` - 可选的。 需要外部应用程序来了解珠宝属于哪个组以及如何显示它。

- "货币" - 以货币显示(默认值)。
- "游戏" - 显示游戏。 它应该以NFT形式显示, 但同时显示考虑到 'amount_style' 的jettons 的数量

| 属性             | 类型        | 要求  | 描述                                                                                                                                |
| -------------- | --------- | --- | --------------------------------------------------------------------------------------------------------------------------------- |
| `uri`          | ASCII 字符串 | 可选的 | a URI指向JSON文档，元数据被“半链内容布局”使用。                                                                                                     |
| `name`         | UTF8 字符串  | 可选的 | 识别资产                                                                                                                              |
| `描述`           | UTF8 字符串  | 可选的 | 描述资产                                                                                                                              |
| `image`        | ASCII 字符串 | 可选的 | 一个 URI 指向一个带有mime 类型图像的资源                                                                                                         |
| `image_data`   | 二进制\*     | 可选的 | 要么是二进制图像的链式布局或底层64的非链式布局。                                                                                                         |
| `符号`           | UTF8 字符串  | 可选的 | 代币符号 - 例如"XMPL" 并使用表单"你收到了99 XMPL"                                                                                                |
| `小数`           | UTF8 字符串  | 可选的 | 代币使用的小数点数。 如果未指定，则默认使用9。 UTF8 编码字符串的数字介于 0 到 255 之间。 - 例如，8, 是指令牌金额必须除以100000000，才能获得用户表示权。                                       |
| `amount_style` |           | 可选的 | 外部应用程序需要了解显示珠宝数量的格式。 定义为 _n_, _n-of-total_, _%_.                                                                  |
| `render_type`  |           | 可选的 | 需要外部应用程序来了解珠宝属于哪个组以及如何显示它。  "货币" - 显示为货币(默认值)。 游戏" - 用于作为NFT显示的游戏的显示器，但也显示珠宝数量，并考虑数量_风格值。 |

> `amount_style` 参数：

- _n_ - jettons (默认值) 如果用户有 100 个代币，小数为0，那么它会显示用户有 100 个代币。
- - 发放珠宝总数中的珠宝数量。 例如，如果犹太人的总供应量是1000，用户在他们的钱包里拥有100头饰， 它必须在用户的钱包中显示1000或其他文本或图形的方式，以显示用户令牌与可用代币总量的比率。
- _%_——喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷气式喷 例如，如果犹太人的总供应量为1000，如果用户拥有100首饰， 百分比应该显示为用户钱包余额的10% (100 mix 1000 = 0)。 或10%。

> `render_type`参数:

- _cury_ - 显示为货币 (默认值)。
- _game_ - 用于作为NFT显示的游戏的显示器，但同时也显示了珠宝数量，并考虑了“amount_style value”。

## Parsing Metadata

要解析元数据，首先必须从 blockchain 获取NFT 数据。 为了更好地理解这个过程，请阅读我们的TON资产处理文档部分的[获取NFT数据](/develop/dapps/asset-processing/nfts#geting-nft-data) 部分。

在检索到上链NFT数据后，必须解析。 执行这一进程； NFT 内容类型必须通过读取构成NFT 内部工作的第一字节来确定。

### 离链中

如果元数据字节字符串以 `0x01` 开头，它表示一个超链的 NFT 内容类型。 NFT 内容的剩余部分将使用 Snake 编码格式解码为 ASCII 字符串。 在正确的 NFT URL实现后，检索NFT 识别数据后，过程已完成。 下面是一个使用超链NFT内容元数据解析的 URL 示例：
`https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/95/meta.json`

网址内容(直接来自上面)：

```json
{
   "name": "TON Smart Challenge #2 Winners Trophy",
   "description": "TON Smart Challenge #2 Winners Trophy 1 place out of 181",
   "image": "https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/images/943e994f91227c3fdbccbc6d8635bfaab256fbb4",
   "content_url": "https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/content/84f7f698b337de3bfd1bc4a8118cdfd8226bbadf",
   "attributes": []
}
```

### 链条和半链条

如果元数据字节字符串以 `0x00`开头，它表示NFT 要么使用在链或半链格式。

我们的 NFT 元数据存储在字典中，键值是 SHA256 哈希属性名称，而值是存储在 Snake 或区块格式中的数据。

要确定正在使用哪种类型的 NFT ，开发者必须读取已知的 NFT 属性，如`uri`， `name`, `image`, `description`, and `image_data`. 如果元数据中存在`uri`字段，则表示一个半链布局。 在这种情况下，应该下载uri 字段中指定的链外内容并将其与字典值合并。

链上NFT: [EQBq5z4N_GeJyBdvNh4tPjMpSkA08p8vWyiAX6LNbr3aLjI0](https://getgems.io/collection/EQAVGhk_3rUA3ypZAZ1SkVGZIaDt7UdvwA4jsGRKRo-MRDN/EQBq5z4N_GeJyBdvNh4tPjMpSkA08p8vWyiAX6LNbr3aLjI0)

半链NFT：  [EQB2NJFK0H5OxJTgyQbej0fy5zuicZAXk2vFZEDrqbQ_n5YW](https://getgems.io/nft/EQB2NJFK0H5OxJTgyQbej0fy5zuicZAXk2vFZEDrqbQ_n5YW)

Jeton Master的例子： [EQA4pCk0yK-JCwFD4Nl5ZE4pmlg4DkK-1Ou4HAUQ6RObZNMi](https://tonscan.org/jetton/EQA4pCk0yK-JCwFD4Nl5ZE4pmlg4DkK-1Ou4HAUQ6RObZNMi)

链上的 NFT 解析器示例：[stackblitz/ton-onchain-nft-parser](https://stackblitz.com/edit/ton-onchain-nft-parser?file=src%2Fmain.s)

## 重要的 NFT 元数据注释

1. 对于NFT元数据来说，显示NFT需要“name”、“description”和“image`(或`image_data\`)”字段。
2. 对于杰顿元数据来说，`name`, `symbol`, `decimals` 和 `image`(or `image_data`) 是主要的。
3. 必须认识到，任何人都可以使用任何`name`、`description`或`image`创建一个 NFT 或 Jetton。  为了避免混乱和可能发生的丑闻， 用户应始终以明确区分其应用的其他部分的方式显示其NFT。 恶意的 NFT 和 Jettons 可以通过误导或虚假信息发送到用户的钱包。
4. 有些项目可能有一个“视频”字段，它连接到与 NFT 或 Jetton 相关的视频内容。

## 参考

- [TON Improvement Proposal 64 (TEP-64)](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md)

## 另见：

- [TON NFT 正在处理](/develop/dapps/asset-processing/nfs)
- [TON Jeton processing](/develop/dapps/asset-processing/jettons)
- [Mint your first Jetton](/develop/dapps/tutorials/jetton-minter)
