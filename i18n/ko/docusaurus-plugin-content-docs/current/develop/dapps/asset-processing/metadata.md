# 메타데이터 구문 분석

NFT, NFT 컬렉션, 제톤을 다루는 메타데이터 표준은 TON 개선 제안 64[TEP-64](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md)에 설명되어 있습니다.

TON에서 엔티티는 온체인, 세미체인, 오프체인의 세 가지 유형의 메타데이터를 가질 수 있습니다.

- \*\*온체인 메타데이터: 이름, 속성, 이미지 등 블록체인 내부에 저장되는 메타데이터입니다.
- \*\*오프체인 메타데이터: \*\*체인 외부에서 호스팅되는 메타데이터 파일에 대한 링크를 사용하여 저장됩니다.
- \*\*세미체인 메타데이터: 이름이나 속성과 같은 작은 필드를 블록체인에 저장하는 동시에 이미지를 오프체인에 호스팅하고 링크만 저장할 수 있는 이 두 가지의 하이브리드입니다.

## 스네이크 데이터 인코딩

스네이크 인코딩 포맷을 사용하면 데이터의 일부는 표준화된 셀에 저장하고 나머지 부분은 하위 셀에 재귀적인 방식으로 저장할 수 있습니다. Snake 인코딩 형식은 0x00 바이트를 사용하여 접두사를 붙여야 합니다. TL-B 스키마를 사용해야 합니다:

```
tail#_ {bn:#} b:(bits bn) = SnakeData ~0;
cons#_ {bn:#} {n:#} b:(bits bn) next:^(SnakeData ~n) = SnakeData ~(n + 1);
```

스네이크 형식은 데이터가 단일 셀에 저장할 수 있는 최대 크기를 초과할 때 셀에 추가 데이터를 저장하는 데 사용됩니다. 이는 데이터의 일부를 루트 셀에 저장하고 나머지 부분을 첫 번째 자식 셀에 저장한 후 모든 데이터가 저장될 때까지 재귀적으로 계속 저장하는 방식으로 이루어집니다.

아래는 타입스크립트에서 스네이크 포맷 인코딩 및 디코딩의 예시입니다:

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

오프체인 NFT 콘텐츠의 경우처럼 스네이크 형식을 사용할 때 루트 셀에 '0x00' 바이트 접두사가 항상 필요한 것은 아니라는 점에 유의하시기 바랍니다. 또한 구문 분석을 간소화하기 위해 셀은 비트가 아닌 바이트로 채워집니다. 부모 셀에 이미 기록된 참조에 다음 자식 셀에 참조를 추가하는 문제를 방지하기 위해 스네이크 셀은 역순으로 구성됩니다.

## 청크 인코딩

청크 인코딩 형식은 청크_인덱스에서 청크까지와 같이 사전 데이터 구조를 사용하여 데이터를 저장하는 데 사용됩니다. 청크 인코딩은 `0x01` 바이트 앞에 접두사를 사용해야 합니다. TL-B 체계:

```
chunked_data#_ data:(HashMapE 32 ^(SnakeData ~0)) = ChunkedData;
```

아래는 타입스크립트를 사용한 청크 데이터 디코딩의 예시입니다:

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

| 속성        | 유형        | 요구 사항 | 설명                                                                      |
| --------- | --------- | ----- | ----------------------------------------------------------------------- |
| `우리`      | ASCII 문자열 | 선택 사항 | "세미체인 콘텐츠 레이아웃"에서 사용하는 메타데이터가 포함된 JSON 문서를 가리키는 URI입니다. |
| 이름\`      | UTF8 문자열  | 선택 사항 | 자산을 식별합니다.                                              |
| `설명`      | UTF8 문자열  | 선택 사항 | 에셋을 설명합니다.                                              |
| `이미지`     | ASCII 문자열 | 선택 사항 | 마임 유형 이미지가 있는 리소스를 가리키는 URI                                             |
| `이미지_데이터` | 바이너리\*    | 선택 사항 | 온체인 레이아웃의 경우 이미지의 바이너리 표현 또는 오프체인 레이아웃의 경우 base64입니다.   |

## Jetton 메타데이터 속성

1. `uri` - 선택 사항입니다. "세미 체인 콘텐츠 레이아웃"에서 사용됩니다. ASCII 문자열. 메타데이터가 있는 JSON 문서를 가리키는 URI입니다.
2. 이름\` - 선택 사항입니다. UTF8 문자열. 에셋을 식별합니다.
3. 설명\` - 선택 사항입니다. UTF8 문자열. 에셋을 설명합니다.
4. `이미지` - 선택 사항입니다. ASCII 문자열. 마임 유형 이미지가 있는 리소스를 가리키는 URI입니다.
5. 이미지_데이터\` - 선택 사항. 온체인 레이아웃의 경우 이미지의 이진 표현, 오프체인 레이아웃의 경우 base64입니다.
6. 기호\` - 선택 사항입니다. UTF8 문자열. 토큰의 기호 - 예: "XMPL". "99 XMPL을 받았습니다"와 같은 형식으로 사용됩니다.
7. '소수점' - 선택 사항입니다. 지정하지 않으면 기본적으로 9가 사용됩니다. 0에서 255 사이의 숫자로 UTF8 인코딩된 문자열입니다. 토큰이 사용하는 소수점 수(예: 8)는 토큰 금액을 100000000 으로 나누어 사용자 표현을 구하는 것을 의미합니다.
8. `amount_style` - 선택 사항입니다. 외부 애플리케이션에서 제톤 수를 표시하는 형식을 이해하기 위해 필요합니다.

- "n" - 제톤 수(기본값). 사용자에게 소수점이 0인 토큰이 100개 있는 경우 사용자가 100개의 토큰을 가지고 있다고 표시합니다.
- "총 n" - 발행된 총 제톤 수 중 제톤의 수입니다. 예를 들어, 총공급 제톤 = 1000입니다. 사용자가 제톤 지갑에 100개의 제톤을 가지고 있습니다. 예를 들어 사용자의 지갑에 1000의 100으로 표시하거나 기타 텍스트 또는 그래픽 방식으로 표시하여 일반과 특정의 차이를 보여줘야 합니다.
- "%" - 발행된 총 제톤 수에서 제톤의 백분율입니다. 예를 들어 총공급 제톤 = 1000입니다. 사용자가 제톤 지갑에 100개의 제톤을 가지고 있습니다. 예를 들어 사용자의 지갑에는 10%로 표시되어야 합니다.

9. '렌더_유형' - 선택 사항입니다. 외부 애플리케이션에서 제톤이 속한 그룹과 표시 방법을 이해하기 위해 필요합니다.

- "통화" - 통화로 표시합니다(기본값).
- "game" - 게임용 표시. NFT로 표시되어야 하지만 동시에 `amount_style`을 고려하여 제톤 수를 표시해야 합니다.

| 속성        | 유형        | 요구 사항 | 설명                                                                                                                                                                                                                                 |
| --------- | --------- | ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `우리`      | ASCII 문자열 | 선택 사항 | "세미체인 콘텐츠 레이아웃"에서 사용하는 메타데이터가 포함된 JSON 문서를 가리키는 URI입니다.                                                                                                                                                            |
| 이름\`      | UTF8 문자열  | 선택 사항 | 자산을 식별합니다.                                                                                                                                                                                                         |
| `설명`      | UTF8 문자열  | 선택 사항 | 에셋을 설명합니다.                                                                                                                                                                                                         |
| `이미지`     | ASCII 문자열 | 선택 사항 | 마임 유형 이미지가 있는 리소스를 가리키는 URI                                                                                                                                                                                                        |
| `이미지_데이터` | 바이너리\*    | 선택 사항 | 온체인 레이아웃의 경우 이미지의 바이너리 표현 또는 오프체인 레이아웃의 경우 base64입니다.                                                                                                                                                              |
| `심볼`      | UTF8 문자열  | 선택 사항 | 토큰의 기호(예: "XMPL")를 입력하고 "99 XMPL을 받았습니다"라는 형식을 사용합니다.                                                                                                                           |
| `소수`      | UTF8 문자열  | 선택 사항 | 토큰이 사용하는 소수점 수입니다. 지정하지 않으면 기본적으로 9가 사용됩니다. 0에서 255 사이의 숫자로 UTF8로 인코딩된 문자열입니다. - 예를 들어 8은 토큰 금액을 100000000 으로 나누어 사용자 표현을 얻어야 함을 의미합니다.                            |
| `금액_스타일`  |           | 선택 사항 | 외부 애플리케이션에서 제톤 수를 표시하는 형식을 이해하기 위해 필요합니다. n_, *n-of-total*, _%_로 정의합니다.                                                             |
| 렌더링 유형\`  |           | 선택 사항 | 외부 애플리케이션에서 제톤이 속한 그룹과 표시 방법을 이해하기 위해 필요합니다.  "currency" - 통화로 표시(기본값)."game" - NFT로 표시되는 게임에 사용되는 표시이지만 제톤 수를 표시하고 amount_style 값도 고려합니다. |

> 금액_스타일\` 매개변수:

- n_ - 제톤 수(기본값). 사용자에게 소수점이 0인 토큰이 100개이면 사용자에게 100개의 토큰이 있음을 표시합니다.
- *n-of-total* - 발행된 총 제톤 수 중 제톤의 수입니다. 예를 들어, 총 공급량이 1000이고 사용자가 지갑에 100개의 제톤을 가지고 있다면, 사용자의 지갑에 1000의 100 또는 다른 텍스트 또는 그래픽 방식으로 표시하여 총 토큰 수량에 대한 사용자 토큰의 비율을 보여줘야 합니다.
- *%* - 발행된 총 제톤 수에서 제톤의 백분율입니다. 예를 들어, 총 제톤 공급량이 1000인 경우 사용자가 100개의 제톤을 보유하고 있다면 백분율은 사용자 지갑 잔액의 10%(100 ÷ 1000 = 0.1 또는 10%)로 표시되어야 합니다.

> 렌더링 유형\` 매개변수:

- *currency* - 통화로 표시됩니다(기본값).
- *game* - NFT로 표시되는 게임에 사용되는 표시이지만 제톤 수를 표시하고 '금액_스타일 값'도 고려합니다.

## 메타데이터 구문 분석

메타데이터를 파싱하려면 먼저 블록체인에서 NFT 데이터를 가져와야 합니다. 이 과정을 더 잘 이해하려면 TON 자산 처리 문서 섹션의 [NFT 데이터 가져오기](/develop/dapps/asset-processing/nfts#getting-nft-data) 섹션을 읽어보시기 바랍니다.

온체인 NFT 데이터를 검색한 후에는 이를 구문 분석해야 합니다. 이 과정을 수행하려면 NFT의 내부를 구성하는 첫 바이트를 읽어 NFT 콘텐츠 유형을 결정해야 합니다.

### 오프체인

메타데이터 바이트 문자열이 `0x01`로 시작하면 오프체인 NFT 콘텐츠 유형을 의미합니다. NFT 콘텐츠의 나머지 부분은 스네이크 인코딩 형식을 사용해 ASCII 문자열로 디코딩됩니다. 올바른 NFT URL이 구현되고 NFT 식별 데이터가 검색되면 프로세스가 완료됩니다. 다음은 오프체인 NFT 콘텐츠 메타데이터 파싱을 사용하는 URL의 예시입니다:
`https://s.getgems.io/nft/b/c/62fba50217c3fe3cbaad9e7f/95/meta.json`

URL 콘텐츠(바로 위에서부터):

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

메타데이터 바이트 문자열이 '0x00'으로 시작하면 NFT가 온체인 또는 세미체인 형식을 사용한다는 뜻입니다.

NFT의 메타데이터는 딕셔너리에 저장되며, 키는 속성 이름의 SHA256 해시이고 값은 스네이크 또는 청크 형식으로 저장된 데이터입니다.

어떤 유형의 NFT가 사용되고 있는지 확인하려면 개발자가 `uri`, `name`, `image`, `description`, `image_data`와 같은 알려진 NFT 속성을 읽어야 합니다. 메타데이터 내에 `uri` 필드가 있는 경우 세미 체인 레이아웃을 나타냅니다. 이러한 경우, uri 필드에 지정된 오프체인 콘텐츠를 다운로드하여 사전 값과 병합해야 합니다.

온체인 NFT의 예: [EQBq5z4N_GeJyBdvNh4tPjMpSkA08p8vWyiAX6LNbr3aLjI0](https://getgems.io/collection/EQAVGhk_3rUA3ypZAZ1SkVGZIaDt7UdvwA4jsSGRKRo-MRDN/EQBq5z4N_GeJyBdvNh4tPjMpSkA08p8vWyiAX6LNbr3aLjI0)

세미체인 NFT의 예: [EQB2NJFK0H5OxJTgyQbej0fy5zuicZAXk2vFZEDrqbQ_n5YW](https://getgems.io/nft/EQB2NJFK0H5OxJTgyQbej0fy5zuicZAXk2vFZEDrqbQ_n5YW)

온체인 제톤 마스터의 예시입니다: [EQA4pCk0yK-JCwFD4Nl5ZE4pmlg4DkK-1Ou4HAUQ6RObZNMi](https://tonscan.org/jetton/EQA4pCk0yK-JCwFD4Nl5ZE4pmlg4DkK-1Ou4HAUQ6RObZNMi)

온체인 NFT 파서의 예시입니다: [스택블리츠/톤온체인-nft-파서](https://stackblitz.com/edit/ton-onchain-nft-parser?file=src%2Fmain.ts)

## 중요한 NFT 메타데이터 참고 사항

1. NFT 메타데이터의 경우, NFT를 표시하려면 `이름`, `설명`, `이미지`(또는 `이미지_데이터`) 필드가 필요합니다.
2. 제톤 메타데이터의 경우 `이름`, `심볼`, `숫자` 및 `이미지`(또는 `이미지_데이터`)가 기본입니다.
3. 누구나 '이름', '설명', '이미지'를 사용해 NFT 또는 제톤을 만들 수 있다는 점을 알아두는 것이 중요합니다.  혼란과 잠재적인 사기를 방지하기 위해 사용자는 항상 앱의 다른 부분과 명확하게 구분할 수 있는 방식으로 NFT를 표시해야 합니다. 악의적인 NFT와 제톤은 오해의 소지가 있거나 잘못된 정보와 함께 사용자의 지갑으로 전송될 수 있습니다.
4. 일부 항목에는 NFT 또는 제트턴과 관련된 동영상 콘텐츠로 연결되는 '동영상' 필드가 있을 수 있습니다.

## 참조

- [TON 개선 제안 64(TEP-64)](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md)

## 참고 항목

- [TON NFT 처리](/개발/앱/자산 처리/nfts)
- [TON 제톤 처리](/개발/앱/자산 처리/제톤)
- [첫 제톤 채굴하기](/개발/앱/튜토리얼/제톤 채굴기)
