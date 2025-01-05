# FunC의 역사

# 초기 버전

초기 버전은 Telegram에 의해 만들어졌으며 2020년 5월 이후 활발한 개발이 중단되었습니다. 2020년 5월의 버전을 "초기"라고 부릅니다.

# 버전 0.1.0

[05.2022 업데이트](https://github.com/ton-blockchain/ton/releases/tag/v2022.05)에서 출시되었습니다.

이 버전에서 추가된 기능:

- [상수](/v3/documentation/smart-contracts/func/docs/literals_identifiers#constants)
- [확장된 문자열 리터럴](/v3/documentation/smart-contracts/func/docs/literals_identifiers#string-literals)
- [Semver 프라그마](/v3/documentation/smart-contracts/func/docs/compiler_directives#pragma-version)
- [Include 기능](/v3/documentation/smart-contracts/func/docs/compiler_directives#pragma-version)

수정사항:

- Asm.fif에서 드물게 발생하던 버그들이 수정되었습니다.

# 버전 0.2.0

[08.2022 업데이트](https://github.com/ton-blockchain/ton/releases/tag/v2022.08)에서 출시되었습니다.

이 버전에서 추가된 기능:

- 불균형 if/else 분기문 (일부 분기는 반환하고 일부는 반환하지 않는 경우)

수정사항:

- [FunC가 while(false) 루프를 잘못 처리하는 문제 #377](https://github.com/ton-blockchain/ton/issues/377)
- [FunC가 ifelse 분기문에 대한 코드를 잘못 생성하는 문제 #374](https://github.com/ton-blockchain/ton/issues/374)
- [FunC가 인라인 함수에서 조건의 반환을 잘못 처리하는 문제 #370](https://github.com/ton-blockchain/ton/issues/370)
- [Asm.fif: 큰 함수 본문의 분할이 인라인과 잘못 간섭하는 문제 #375](https://github.com/ton-blockchain/ton/issues/375)

# 버전 0.3.0

[10.2022 업데이트](https://github.com/ton-blockchain/ton/releases/tag/v2022.10)에서 출시되었습니다.

이 버전에서 추가된 기능:

- [여러 줄의 어셈블리](/v3/documentation/smart-contracts/func/docs/functions#multiline-asms)
- 상수와 어셈블리에 대한 동일한 정의의 중복이 허용됨
- 상수에 대한 비트 연산이 허용됨

# 버전 0.4.0

[01.2023 업데이트](https://github.com/ton-blockchain/ton/releases/tag/v2023.01)에서 출시되었습니다.

이 버전에서 추가된 기능:

- [try/catch 문](/v3/documentation/smart-contracts/func/docs/statements#try-catch-statements)
- [throw_arg 함수](/v3/documentation/smart-contracts/func/docs/builtins#throwing-exceptions)
- 전역 변수의 제자리 수정과 대량 할당이 허용됨: `a`가 전역일 때 `a~inc()`와 `(a, b) = (3, 5)`

수정사항:

- 동일한 표현식에서 사용된 후 지역 변수의 모호한 수정을 금지: `var x = (ds, ds~load_uint(32), ds~load_unit(64));`는 금지되었지만 `var x = (ds~load_uint(32), ds~load_unit(64), ds);`는 허용됨
- 빈 인라인 함수 허용
- 드문 `while` 최적화 버그 수정
