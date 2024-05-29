# IDE 지원

### 하이라이트

intellij-ton](https://github.com/andreypfau/intellij-ton) 플러그인은 Fift 및 FunC 프로그래밍 언어와 타이핑된 언어 바이너리(TL-B) 형식을 지원합니다.

또한 올바른 TL-B 구문 사양은 [TlbParser.bnf](https://github.com/andreypfau/intellij-ton/blob/main/src/main/grammars/TlbParser.bnf) 파일에 설명되어 있습니다.

### TL-B 파서

TL-B 구문 분석기는 기본 [TL-B 유형](/개발/데이터-형식/tl-b-types)의 직렬화를 수행하는 데 도움을 줍니다. 각각은 TL-B 유형을 객체로 구현하고 직렬화된 바이너리 데이터를 반환합니다.

| 언어     | SDK                                                                                                                    | 소셜                                                                          |
| ------ | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Kotlin | [ton-kotlin](https://github.com/andreypfau/ton-kotlin/tree/main/ton-kotlin-tlb) (+ `.tlb` 파일 구문 분석) | https://t.me/tonkotlin                      |
| 이동     | [토누틸](https://github.com/xssnick/tonutils-go/tree/master/tlb)                                                          | https://t.me/tonutils                       |
| 이동     | [통고](https://github.com/tonkeeper/tongo/tree/master/tlb) (+ `.tlb` 파일 파싱)                           | https://t.me/tongo_lib |
| 타입스크립트 | [tlb-parser](https://github.com/ton-community/tlb-parser)                                                              | -                                                                           |
