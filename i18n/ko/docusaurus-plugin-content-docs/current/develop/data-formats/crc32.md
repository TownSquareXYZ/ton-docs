# CRC32

## 개요

CRC는 디지털 데이터의 무결성을 검증하는 데 일반적으로 사용되는 방법인 순환 중복 검사(Cyclic Redundancy Check)의 약자입니다. 전송 또는 저장 중 디지털 데이터에 오류가 발생했는지 확인하는 데 사용되는 오류 감지 알고리즘입니다. CRC는 전송 또는 저장 중인 데이터의 짧은 체크섬 또는 해시를 생성하여 데이터에 추가합니다. 데이터가 수신되거나 검색되면 CRC가 다시 계산되어 원래의 체크섬과 비교됩니다. 두 체크섬이 일치하면 데이터가 손상되지 않은 것으로 간주합니다. 일치하지 않으면 오류가 발생했음을 나타내며 데이터를 다시 보내거나 검색해야 합니다.

TL-B 방식에 사용되는 CRC32 IEEE 버전입니다. 이 [NFT 연산 코드](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md#tl-b-schema) 예시를 보면 다양한 메시지에 대한 TL-B 계산을 보다 명확하게 이해할 수 있습니다.

## 도구

### 온라인 계산기

- [온라인 계산기 예시](https://emn178.github.io/online-tools/crc32.html)
- [톤웨일즈 인트로스펙션 ID 생성기](https://tonwhales.com/tools/introspection-id)

### VS 코드 확장

- [crc32-opcode-helper](https://marketplace.visualstudio.com/items?itemName=Gusarich.crc32-opcode-helper)

### Python

```python
import zlib
print(zlib.crc32(b'<TL-B>') & 0x7FFFFFFF)
```

### 이동

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

### 타입스크립트

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
