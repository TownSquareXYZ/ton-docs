# TL

TL(Type Language)은 데이터 구조를 설명하는 언어입니다.

데이터 구조화를 위해 통신할 때 [TL 스키마](https://github.com/ton-blockchain/ton/tree/master/tl/generate/scheme)가 사용됩니다.

TL은 32비트 블록 단위로 작동합니다. 따라서 TL의 데이터 크기는 4바이트의 배수여야 합니다.
객체의 크기가 4의 배수가 아닌 경우, 배수가 될 때까지 필요한 만큼의 0바이트를 추가해야 합니다.

숫자는 항상 리틀 엔디안 순서로 인코딩됩니다.

TL에 대한 자세한 내용은 [텔레그램 문서](https://core.telegram.org/mtproto/TL)에서 확인할 수 있습니다.

## 바이트 배열 인코딩

바이트 배열을 인코딩하려면 먼저 크기를 결정해야 합니다.
254바이트 미만이면 1바이트를 크기로 사용하는 인코딩이 사용됩니다. 그 이상이면
첫 번째 바이트로 0xFE를 쓰고(큰 배열의 지표로), 그 뒤에 3바이트의 크기가 따라옵니다.

예를 들어, 배열 `[0xAA, 0xBB]`을 인코딩하면 크기가 2입니다. 1바이트
크기를 사용하고 데이터 자체를 쓰면 `[0x02, 0xAA, 0xBB]`가 됩니다. 하지만
최종 크기가 3이고 4바이트의 배수가 아니므로, 4가 되도록 1바이트의 패딩을 추가해야 합니다. 결과: `[0x02, 0xAA, 0xBB, 0x00]`.

크기가 396인 배열을 인코딩해야 하는 경우,
다음과 같이 합니다: 396 >= 254이므로 크기 인코딩에 3바이트와 1바이트의 오버사이즈 지표를 사용합니다.
결과: `[0xFE, 0x8C, 0x01, 0x00, array bytes]`, 396+4 = 400으로 4의 배수이므로 정렬이 필요 없습니다.

## 명확하지 않은 직렬화 규칙

스키마 자체 앞에 4바이트 접두사(ID)가 자주 쓰입니다. 스키마 ID는 스키마 텍스트에서 `;`와 `()` 같은 기호를 제거한 후 IEEE 테이블을 사용한 CRC32입니다. ID 접두사가 있는 스키마의 직렬화를 **boxed**라고 하며, 이를 통해 파서가 여러 옵션이 있을 때 어떤 스키마가 앞에 오는지 결정할 수 있습니다.

boxed로 직렬화할지 여부는 어떻게 결정할까요? 우리의 스키마가 다른 스키마의 일부라면 필드 타입이 어떻게 지정되었는지 봐야 합니다. 명시적으로 지정된 경우 접두사 없이 직렬화하고, 명시적이지 않은 경우(이런 타입이 많음) boxed로 직렬화해야 합니다. 예:

```tlb
pub.unenc data:bytes = PublicKey;
pub.ed25519 key:int256 = PublicKey;
pub.aes key:int256 = PublicKey;
pub.overlay name:bytes = PublicKey;
```

이러한 타입들이 있을 때, `PublicKey`가 스키마에서 `adnl.node id:PublicKey addr_list:adnl.addressList = adnl.Node`처럼 지정되면 명시적이지 않으므로 ID 접두사(boxed)로 직렬화해야 합니다. 반면 `adnl.node id:pub.ed25519 addr_list:adnl.addressList = adnl.Node`처럼 지정되었다면 명시적이므로 접두사가 필요 없습니다.

## 참고

*여기 [원본 글](https://github.com/xssnick/ton-deep-doc/blob/master/TL.md)은 [Oleg Baranov](https://github.com/xssnick)가 작성했습니다.*