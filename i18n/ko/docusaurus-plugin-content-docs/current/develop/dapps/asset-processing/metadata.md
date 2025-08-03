# 메타데이터 파싱

NFT, NFT 컬렉션, Jetton에 대한 메타데이터 표준은 TON Enhancement Proposal 64 [TEP-64](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md)에 설명되어 있습니다.

TON에서 엔티티는 세 가지 유형의 메타데이터를 가질 수 있습니다: 온체인, 세미체인, 오프체인.

- **온체인 메타데이터:** 블록체인 내에 저장되며 이름, 속성, 이미지 등을 포함합니다.
- **오프체인 메타데이터:** 체인 외부에 호스팅된 메타데이터 파일에 대한 링크를 사용하여 저장됩니다.
- **세미체인 메타데이터:** 온체인과 오프체인의 하이브리드 형태로, 블록체인에 이름이나 속성 등의 작은 필드를 저장하면서, 이미지는 오프체인에 저장하고 링크만 보관하는 방식입니다.

## Snake 데이터 인코딩

Snake 인코딩 형식은 일부 데이터를 표준화된 셀에 저장하고, 나머지 부분은 자식 셀에 저장하는 재귀적 방식을 사용합니다. Snake 인코딩 형식은 `0x00` 바이트로 시작해야 합니다. TL-B 스키마:

```
tail#_ {bn:#} b:(bits bn) = SnakeData ~0;
cons#_ {bn:#} {n:#} b:(bits bn) next:^(SnakeData ~n) = SnakeData ~(n + 1);
```

데이터가 단일 셀에 저장할 수 있는 최대 크기를 초과할 경우 추가 데이터를 셀에 저장하기 위해 Snake 형식을 사용합니다. 이 방식은 데이터의 일부를 루트 셀에, 나머지 부분을 첫 번째 자식 셀에 저장하며, 모든 데이터를 저장할 때까지 재귀적으로 반복됩니다.

아래는 TypeScript로 작성된 Snake 형식 인코딩 및 디코딩의 예시입니다:

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

Snake 형식 사용 시, 루트 셀에서 `0x00` 바이트 접두어가 항상 필요한 것은 아닙니다(예: 오프체인 NFT 콘텐츠). 또한, 셀을 파싱하기 쉽게 하기 위해 바이트로 채워집니다. Snake 셀은 부모 셀에 참조가 이미 작성된 후, 다음 자식 셀에 대한 참조를 추가하는 문제를 피하기 위해 역순으로 생성됩니다.

## Chunked 인코딩

Chunked 인코딩 형식은 chunk_index에서 chunk로의 사전 자료 구조를 사용하여 데이터를 저장합니다. Chunked 인코딩은 `0x01` 바이트로 시작해야 합니다. TL-B 스키마:

```
chunked_data#_ data:(HashMapE 32 ^(SnakeData ~0)) = ChunkedData;
```

아래는 TypeScript로 작성된 Chunked 인코딩 및 디코딩의 예시입니다:

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

## NFT 메타데이터 속성

| 속성            | 유형        | 요구 사항 | 설명                                                                               |
| ------------- | --------- | ----- | -------------------------------------------------------------------------------- |
| `uri`         | ASCII 문자열 | 선택 사항 | "세미체인 콘텐츠 레이아웃"에서 사용되는 메타데이터가 포함된 JSON 문서로의 URI를 가리킵니다.          |
| `name`        | UTF8 문자열  | 선택 사항 | 자산을 식별합니다.                                                       |
| `description` | UTF8 문자열  | 선택 사항 | 자산에 대해 설명합니다.                                                    |
| `image`       | ASCII 문자열 | 선택 사항 | MIME 타입 이미지를 가진 리소스에 대한 URI를 가리킵니다.                              |
| `image_data`  | 바이너리\*    | 선택 사항 | 온체인 레이아웃에서는 이미지의 바이너리 표현 또는 오프체인 레이아웃에서는 base64로 인코딩된 데이터를 가집니다. |

## Jetton 메타데이터 속성

1. `uri` - 선택 사항. "세미체인 콘텐츠 레이아웃"에서 사용됩니다. ASCII 문자열로, 메타데이터가 포함된 JSON 문서로의 URI를 가리킵니다.
2. `name` - 선택 사항. UTF8 문자열. 자산을 식별합니다.
3. `description` - 선택 사항. UTF8 문자열. 자산에 대해 설명합니다.
4. `image` - 선택 사항. ASCII 문자열. MIME 타입 이미지를 가진 리소스에 대한 URI를 가리킵니다.
5. `image_data` - 선택 사항. 온체인 레이아웃에서는 이미지의 바이너리 표현 또는 오프체인 레이아웃에서는 base64로 인코딩된 데이터를 가집니다.
6. `symbol` - 선택 사항. UTF8 문자열. 토큰의 심볼, 예: "XMPL". "You received 99 XMPL" 형식으로 사용됩니다.
7. `decimals` - 선택 사항. 기본값은 9입니다. 0에서 255까지의 숫자를 가진 UTF8로 인코딩된 문자열. 예: 8은 토큰 금액을 100000000으로 나누어 사용자 표현으로 변환해야 한다는 것을 의미합니다.
8. `amount_style` - 선택 사항. 외부 애플리케이션이 Jetton 수를 표시할 형식을 이해하는 데 필요합니다.

- "n" - Jetton 수 (기본값). 사용자가 소수점 이하 자릿수 0인 100개의 토큰을 보유하고 있으면 100개의 토큰이 있는 것으로 표시됩니다.
- "n-of-total" - 발행된 Jetton의 총 수 중에서 Jetton 수. 예: totalSupply Jetton = 1000이고 사용자가 Jetton 지갑에 100개를 보유하고 있으면 사용자의 지갑에 100/1000으로 표시됩니다.
- "%" - 발행된 Jetton의 총 수 중 Jetton의 백분율. 예: totalSupply Jetton = 1000이고 사용자가 100개를 보유하고 있으면 지갑에 10%로 표시됩니다.

9. `render_type` - 선택 사항. Jetton이 속한 그룹과 표시 방법을 이해하는 데 외부 애플리케이션이 필요로 합니다.

- "currency" - 통화로 표시 (기본값).
- "game" - 게임용으로 표시. NFT로 표시되어야 하지만, `amount_style`을 고려하여 Jetton의 수를 표시합니다.

| 속성             | 유형        | 요구 사항 | 설명                                                                                                                                                                                                                          |
| -------------- | --------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `uri`          | ASCII 문자열 | 선택 사항 | "세미체인 콘텐츠 레이아웃"에서 사용되는 메타데이터가 포함된 JSON 문서로의 URI를 가리킵니다.                                                                                                                                                     |
| `name`         | UTF8 문자열  | 선택 사항 | 자산을 식별합니다.                                                                                                                                                                                                  |
| `description`  | UTF8 문자열  | 선택 사항 | 자산에 대해 설명합니다.                                                                                                                                                                                               |
| `image`        | ASCII 문자열 | 선택 사항 | MIME 타입 이미지를 가진 리소스에 대한 URI를 가리킵니다.                                                                                                                                                                         |
| `image_data`   | 바이너리\*    | 선택 사항 | 온체인 레이아웃에서는 이미지의 바이너리 표현 또는 오프체인 레이아웃에서는 base64로 인코딩된 데이터를 가집니다.                                                                                                                                            |
| `symbol`       | UTF8 문자열  | 선택 사항 | 토큰의 심볼, 예: "XMPL"로 "You received 99 XMPL" 형식으로 사용됩니다.                                                                                                                                       |
| `decimals`     | UTF8 문자열  | 선택 사항 | 토큰이 사용하는 소수점 자릿수. 지정되지 않은 경우 기본값은 9입니다. 0~255 사이의 숫자를 가진 UTF8로 인코딩된 문자열입니다. 예: 8은 토큰 금액을 100000000으로 나누어 사용자 표현으로 변환해야 합니다. |
| `amount_style` |           | 선택 사항 | 외부 애플리케이션이 Jetton 수를 표시할 형식을 이해하는 데 필요합니다. *n*, *n-of-total*, *%* 값으로 정의됩니다.                                                                                                                |
| `render_type`  |           | 선택 사항 | Jetton이 속한 그룹과 표시 방법을 이해하는 데 외부 애플리케이션이 필요로 합니다. "currency" - 통화로 표시 (기본값). "game" - 게임용으로 표시되며 NFT로 표시되지만, `amount_style` 값을 고려하여 Jetton의 수를 표시합니다.     |

> `amount_style` 매개변수:

- *n* - Jetton 수 (기본값). 사용자가 소수점 이하 자릿수 0인 100개의 토큰을 보유하고 있으면 100개의 토큰이 있는 것으로 표시됩니다.
- *n-of-total* - 발행된 Jetton의 총 수 중에서 Jetton 수. 예를 들어, totalSupply Jetton이 1000이고 사용자가 Jetton 지갑에 100개를 보유하고 있으면 사용자의 지갑에 100/1000 또는 사용자 토큰과 발행된 총 토큰의 비율을 보여주는 다른 방식으로 표시됩니다.
- *%* - 발행된 Jetton의 총 수 중 Jetton의 백분율. 예를 들어, totalSupply Jetton이 1000이고 사용자가 100개의 Jetton을 보유하고 있으면, 지갑에 사용자 잔액의 10%로 표시됩니다 (100 ÷ 1000 = 0.1 또는 10%).

> `render_type` 매개변수:

- *currency* - 통화로 표시 (기본값).
- *game* - 게임용으로 표시되며, NFT로 표시되지만 Jetton의 수를 표시하고 `amount_style` 값을 고려합니다.

## 메타데이터 파싱

메타데이터를 파싱하려면 블록체인에서 먼저 NFT 데이터를 가져와야 합니다. 이 과정을 더 잘 이해하려면 TON 자산 처리 문서 섹션의 [NFT 데이터 가져오기](/develop/dapps/asset-processing/nfts#getting-nft-data)를 참조하세요.

온체인 NFT 데이터를 가져온 후에는 이를 파싱해야 합니다. 이 과정은 NFT의 내부 작동을 구성하는 첫 번째 바이트를 읽어 NFT 콘텐츠 유형을 결정하는 것으로 시작합니다.

### 오프체인

메타데이터 바이트 문자열이 `0x01`로 시작하면 오프체인 NFT 콘텐츠 유형을 나타냅니다. NFT 콘텐츠의 나머지 부분은 ASCII 문자열로 Snake 인코딩 형식을 사용하여 디코딩됩니다. 올바른 NFT URL이 확인되고 NFT 식별 데이터가 검색되면 프로세스가 완료됩니다. 아래는 오프체인 NFT 콘텐츠 메타데이터 파싱을 사용하는 URL의 예입니다:
`https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/95/meta.json`

URL 내용 (위에서 가져옴):

```json
{
   "name": "TON Smart Challenge #2 Winners Trophy",
   "description": "TON Smart Challenge #2 Winners Trophy 1 place out of 181",
   "image": "https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/images/943e994f91227c3fdbccbc6d8635bfaab256fbb4",
   "content_url": "https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/content/84f7f698b337de3bfd1bc4a8118cdfd8226bbadf",
   "attributes": []
}
```

### 온체인 및 세미체인

메타데이터 바이트 문자열이 `0x00`으로 시작하면 NFT가 온체인 또는 세미체인 형식을 사용하는 것을 나타냅니다.

NFT의 메타데이터는 속성 이름의 SHA256 해시가 키이고, 데이터가 Snake 또는 Chunked 형식으로 저장된 값인 사전에서 저장됩니다.

어떤 유형의 NFT가 사용되는지 확인하려면 개발자가 `uri`, `name`, `image`, `description`, `image_data`와 같은 알려진 NFT 속성을 읽어야 합니다. 메타데이터에 `uri` 필드가 있으면 세미체인 레이아웃을 나타냅니다. 이러한 경우, uri 필드에 지정된 오프체인 콘텐츠를 다운로드하여 사전 값과 병합해야 합니다.

온체인 NFT 예시: [EQBq5z4N_GeJyBdvNh4tPjMpSkA08p8vWyiAX6LNbr3aLjI0](https://getgems.io/collection/EQAVGhk_3rUA3ypZAZ1SkVGZIaDt7UdvwA4jsSGRKRo-MRDN/EQBq5z4N_GeJyBdvNh4tPjMpSkA08p8vWyiAX6LNbr3aLjI0)

세미체인 NFT 예시: [EQB2NJFK0H5OxJTgyQbej0fy5zuicZAXk2vFZEDrqbQ_n5YW](https://getgems.io/nft/EQB2NJFK0H5OxJTgyQbej0fy5zuicZAXk2vFZEDrqbQ_n5YW)

온체인 Jetton 마스터 예시: [EQA4pCk0yK-JCwFD4Nl5ZE4pmlg4DkK-1Ou4HAUQ6RObZNMi](https://tonscan.org/jetton/EQA4pCk0yK-JCwFD4Nl5ZE4pmlg4DkK-1Ou4HAUQ6RObZNMi)

온체인 NFT 파서 예시: [stackblitz/ton-onchain-nft-parser](https://stackblitz.com/edit/ton-onchain-nft-parser?file=src%2Fmain.ts)

## 중요한 NFT 메타데이터 참고 사항

1. NFT 메타데이터의 경우, `name`, `description`, `image`(또는 `image_data`) 필드는 NFT를 표시하는 데 필수적입니다.
2. Jetton 메타데이터의 경우, `name`, `symbol`, `decimals` 및 `image`(또는 `image_data`)가 기본 필드입니다.
3. 누구나 `name`, `description`, `image`를 사용하여 NFT 또는 Jetton을 생성할 수 있습니다. 혼동과 잠재적인 사기를 방지하려면 사용자는 항상 자신의 앱의 다른 부분과 명확히 구분되도록 NFT를 표시해야 합니다. 악의적인 NFT와 Jetton은 잘못된 정보와 함께 사용자의 지갑에 전송될 수 있습니다.
4. 일부 항목에는 NFT 또는 Jetton과 관련된 비디오 콘텐츠를 링크하는 `video` 필드가 있을 수 있습니다.

## 참조

- [TON Enhancement Proposal 64 (TEP-64)](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md)

## 참고 사항

- [TON NFT 처리](/develop/dapps/asset-processing/nfts)
- [TON Jetton 처리](/develop/dapps/asset-processing/jettons)
- [Jetton 처음 발행하기](/develop/dapps/tutorials/jetton-minter)
