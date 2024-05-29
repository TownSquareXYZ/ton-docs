# FunC의 역사

# 초기 버전

초기 버전은 텔레그램에서 개발하였으며, 2020년 5월 이후 적극적인 개발은 중단되었습니다. 2020년 5월 버전을 "초기 버전"이라고 합니다.

# 버전 0.1.0

05.2022 업데이트](https://github.com/ton-blockchain/ton/releases/tag/v2022.05)에서 출시되었습니다.

이 버전에서는 추가되었습니다:

- [상수](/개발/펀크/리터럴_식별자#상수)
- [확장 문자열 리터럴](/개발/펀크/리터럴_식별자#스트링-리터럴)
- [셈버 프라그마](/개발/펀크/컴파일러_디렉티브#프라그마-버전)
- [포함](/개발/펀크/컴파일러_디렉티브#프라그마 버전)

수정되었습니다:

- Asm.fif에서 드물게 나타나는 버그를 수정했습니다.

# 버전 0.2.0

08.2022 업데이트](https://github.com/ton-blockchain/ton/releases/tag/v2022.08)에서 출시되었습니다.

이 버전에서는 추가되었습니다:

- 불균형한 경우/다른 경우 분기(일부 분기는 반환되고 일부 분기는 반환되지 않는 경우)

수정되었습니다:

- [FunC가 while(false) 루프를 잘못 처리하는 동안 #377](https://github.com/ton-blockchain/ton/issues/377)
- [ifelse 브랜치 #374에 대한 FunC 코드 생성 오류](https://github.com/ton-blockchain/ton/issues/374)
- [FunC가 인라인 함수 #370의 조건에서 잘못 반환됨](https://github.com/ton-blockchain/ton/issues/370)
- [Asm.fif: 큰 함수 본문 분할이 인라인 #375를 잘못 방해함](https://github.com/ton-blockchain/ton/issues/375)

# 버전 0.3.0

10.2022 업데이트](https://github.com/ton-blockchain/ton/releases/tag/v2022.10)에서 출시되었습니다.

이 버전에서는 추가되었습니다:

- [멀티라인 ASMS](/개발/펀크/함수#멀티라인-asms)
- 상수 및 ASMS에 대한 동일한 정의의 중복이 허용되었습니다.
- 상수에 대한 상수에 대한 비트 연산이 허용되었습니다.

# 버전 0.4.0

01.2023 업데이트](https://github.com/ton-blockchain/ton/releases/tag/v2023.01)에서 출시되었습니다.

이 버전에서는 추가되었습니다:

- [시도/캐치 문](/개발/펀크/스테이트먼트#시도-캐치-스테이트먼트)
- [throw_arg 함수](/개발/펀크/빌트인#throwing-exceptions)
- 전역 변수의 제자리 수정 및 대량 할당을 허용합니다: `a~inc()` 및 `(a, b) = (3, 5)`, 여기서 `a`는 전역 변수입니다.

수정되었습니다:

- 동일한 표현식에서 사용된 후 지역 변수를 모호하게 수정하는 것을 금지합니다: `var x = (ds, ds~load_uint(32), ds~load_unit(64));`는 허용되지만 `var x = (ds~load_uint(32), ds~load_unit(64), ds);`는 금지되지 않습니다.
- 허용된 빈 인라인 함수
- 드물게 발생하는 '동안' 최적화 버그 수정
