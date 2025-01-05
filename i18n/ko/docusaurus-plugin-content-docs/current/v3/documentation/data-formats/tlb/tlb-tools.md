# TL-B 도구

## TL-B 파서

TL-B 파서는 기본 [TL-B 타입](/v3/documentation/data-formats/tlb/tl-b-types)의 직렬화를 수행하는 데 도움을 줍니다. 각각은
TL-B 타입을 객체로 구현하고 직렬화된 이진 데이터를 반환합니다.

| 언어         | SDK                                                                                                         | 소셜                                                                          |
| ---------- | ----------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Kotlin     | [ton-kotlin](https://github.com/ton-community/ton-kotlin/tree/main/tlb) (+ `.tlb` 파일 파싱) | https://t.me/tonkotlin                      |
| Go         | [tonutils](https://github.com/xssnick/tonutils-go/tree/master/tlb)                                          | https://t.me/tonutils                       |
| Go         | [tongo](https://github.com/tonkeeper/tongo/tree/master/tlb) (+ `.tlb` 파일 파싱)             | https://t.me/tongo_lib |
| TypeScript | [tlb-parser](https://github.com/ton-community/tlb-parser)                                                   | -                                                                           |
| Python     | [ton-kotlin](https://github.com/disintar/tonpy) (+ `.tlb` 파일 파싱)                         | https://t.me/dtontech                       |

## TL-B 생성기

[tlb-codegen](https://github.com/ton-community/tlb-codegen) 패키지를 사용하면 제공된 TLB 스키마에 따라 구조를 직렬화하고 역직렬화하는 Typescript 코드를 생성할 수 있습니다.

[tonpy](https://github.com/disintar/tonpy) 패키지를 사용하면 제공된 TLB 스키마에 따라 구조를 직렬화하고 역직렬화하는 Python 코드를 생성할 수 있습니다.
