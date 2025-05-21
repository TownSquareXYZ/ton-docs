# CRC32

## 개요

CRC(Cyclic Redundancy Check)는 디지털 데이터의 무결성을 검증하는 데 일반적으로 사용되는 방법입니다. 전송이나 저장 중 디지털 데이터에서 오류가 발생했는지 확인하는 오류 감지 알고리즘입니다. CRC는 전송되거나 저장되는 데이터의 짧은 체크섬이나 해시를 생성하여 데이터에 추가합니다. 데이터를 받거나 검색할 때 CRC를 재계산하여 원래 체크섬과 비교합니다. 두 체크섬이 일치하면 데이터가 손상되지 않은 것으로 간주됩니다. 일치하지 않으면 오류가 발생했음을 나타내며 데이터를 다시 전송하거나 검색해야 합니다.

TL-B 스키마에는 CRC32 IEEE 버전이 사용됩니다. [NFT 작업 코드](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md#tl-b-schema) 예제를 보면 다양한 메시지에 대한 TL-B 계산을 더 명확하게 이해할 수 있습니다.

## 도구

### 온라인 계산기

- [온라인 계산기 예제](https://emn178.github.io/online-tools/crc32.html)
- [Tonwhales 인트로스펙션 ID 생성기](https://tonwhales.com/tools/introspection-id)

### VS Code 확장

- [crc32-opcode-helper](https://marketplace.visualstudio.com/items?itemName=Gusarich.crc32-opcode-helper)

### Python

```python
import zlib
print(zlib.crc32(b'<TL-B>') & 0x7FFFFFFF)
```

### Go

```python
func main() {

	var schema = "some"

	schema = strings.ReplaceAll(schema, "(", "")
	schema = strings.ReplaceAll(schema, ")", "")
	data := []byte(schema)
	var crc = crc32.Checksum(data, crc32.MakeTable(crc32.IEEE))

	var b_data = make([]byte, 4)
	binary.BigEndian.PutUint32(b_data, crc)
	var res = hex.EncodeToString(b_data)
	fmt.Println(res)
}
```

### TypeScript

```typescript
import * as crc32 from 'crc-32';

function calculateRequestOpcode_1(str: string): string {
    return (BigInt(crc32.str(str)) & BigInt(0x7fffffff)).toString(16);
}

function calculateResponseOpcode_2(str: string): string {
    const a = BigInt(crc32.str(str));
    const b = BigInt(0x80000000);
    return ((a | b) < 0 ? (a | b) + BigInt('4294967296') : a | b).toString(16);
}
```

