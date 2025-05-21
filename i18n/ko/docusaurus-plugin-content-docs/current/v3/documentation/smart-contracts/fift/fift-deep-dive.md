# Fift 심층 탐구

Fift는 고수준 스택 기반 언어로, TVM 어셈블리 코드를 컨트랙트 코드 bag-of-cells로 변환하는 등 셀과 기타 TVM 기본요소를 로컬에서 조작하는 데 사용됩니다.

:::caution
이 섹션은 **매우** 낮은 수준에서 TON 관련 기능과 상호작용하는 것을 설명합니다.
스택 언어의 기본에 대한 깊은 이해가 필요합니다.
:::

## 간단한 산술

[역 폴란드 표기법](https://en.wikipedia.org/wiki/Reverse_Polish_notation)으로 표현식을 작성하여 Fift 인터프리터를 계산기로 사용할 수 있습니다.

```
6 17 17 * * 289 + .
2023 ok
```

## 표준 출력

```
27 emit ."[30;1mgrey text" 27 emit ."[37m"
grey text ok
```

`emit`은 스택 최상위에서 숫자를 가져와 지정된 코드의 유니코드 문자를 stdout에 출력합니다.
`."..."`는 상수 문자열을 출력합니다.

## 함수 정의(Fift 단어)

단어를 정의하는 주된 방법은 그 효과를 중괄호로 감싸고 `:`와 단어 이름을 쓰는 것입니다.

```
{ minmax drop } : min
{ minmax nip } : max
```

> Fift.fif

하지만 `:`뿐만 아니라 여러 *정의 단어*가 있습니다. 이들 중 일부로 정의된 단어는 **활성**(중괄호 안에서 작동)이고 일부는 **접두사**(뒤에 공백 문자가 필요 없음)라는 점에서 차이가 있습니다:

```
{ bl word 1 2 ' (create) } "::" 1 (create)
{ bl word 0 2 ' (create) } :: :
{ bl word 2 2 ' (create) } :: :_
{ bl word 3 2 ' (create) } :: ::_
{ bl word 0 (create) } : create
```

> Fift.fif

## 조건부 실행

코드 블록(중괄호로 구분된 것)은 조건부 또는 무조건적으로 실행될 수 있습니다.

```
{ { ."true " } { ."false " } cond } : ?.   4 5 = ?.  4 5 < ?.
false true  ok
{ ."hello " } execute ."world"
hello world ok
```

## 루프

```
// ( l c -- l')  deletes first c elements from list l
{ ' safe-cdr swap times } : list-delete-first
```

> GetOpt.fif

루프 단어 `times`는 두 인수(`cont`와 `n`이라고 부르자)를 받아 `cont`를 `n`번 실행합니다.
여기서 `list-delete-first`는 `safe-cdr`의 연속(Lisp 스타일 리스트에서 헤드를 삭제하는 명령)을 가져와 `c` 아래에 놓고 스택에 있는 리스트에서 헤드를 `c`번 제거합니다.

`while`과 `until` 단어도 있습니다.

## 주석

```
{ 0 word drop 0 'nop } :: //
{ char " word 1 { swap { abort } if drop } } ::_ abort"
{ { bl word dup "" $= abort"comment extends after end of file" "*/" $= } until 0 'nop } :: /*
```

> Fift.fif

주석은 `Fift.fif`에 정의되어 있습니다. 한 줄 주석은 `//`로 시작하여 줄 끝까지 계속되고, 여러 줄 주석은 `/*`로 시작하여 `*/`로 끝납니다.

왜 이것들이 작동하는지 이해해봅시다.\
Fift 프로그램은 본질적으로 단어들의 시퀀스이며, 각 단어는 어떤 방식으로 스택을 변환하거나 새로운 단어를 정의합니다. `Fift.fif`의 첫 번째 줄(위에 표시된 코드)은 새로운 단어 `//`의 선언입니다.
주석은 새로운 단어를 정의할 때도 작동해야 하므로 중첩된 환경에서 작동해야 합니다. 그래서 `::` 수단을 통해 **활성** 단어로 정의됩니다. 생성되는 단어의 동작은 중괄호에 나열됩니다:

1. `0`: 스택에 0이 푸시됩니다
2. `word`: 이 명령은 스택 최상위와 동일한 문자가 나올 때까지 문자를 읽고 읽은 데이터를 문자열로 푸시합니다. 0은 특별한 경우입니다: 여기서 `word`는 선행 공백을 건너뛰고 현재 입력 줄 끝까지 읽습니다.
3. `drop`: 최상위 요소(주석 데이터)가 스택에서 제거됩니다.
4. `0`: 0이 다시 스택에 푸시됩니다 - `::`로 정의되었기 때문에 사용되는 결과의 수입니다.
5. `'nop`은 호출될 때 아무것도 하지 않는 실행 토큰을 푸시합니다. `{ nop }`와 거의 동일합니다.

## TVM 어셈블리 코드 정의에 Fift 사용

```
x{00} @Defop NOP
{ 1 ' @addop does create } : @Defop
{ tuck sbitrefs @ensurebitrefs swap s, } : @addop
{ @havebitrefs ' @| ifnot } : @ensurebitrefs
{ 2 pick brembitrefs 1- 2x<= } : @havebitrefs
{ rot >= -rot <= and } : 2x<=
...
```

> Asm.fif (줄 순서 역순)

`@Defop`는 옵코드를 위한 공간이 충분한지 확인하고(`@havebitrefs`), 충분하지 않으면 다른 빌더(`@|`; 암시적 점프라고도 함)에 쓰기를 계속합니다. 그래서 일반적으로 `x{A988} s,`를 옵코드로 쓰고 싶지 않습니다: 이 옵코드를 배치할 공간이 부족할 수 있어서 컴파일이 실패할 수 있습니다; 대신 `x{A988} @addop`를 써야 합니다.

큰 bag-of-cells를 컨트랙트에 포함시키기 위해 Fift를 사용할 수 있습니다:

```
<b 8 4 u, 8 4 u, "fift/blob.boc" file>B B>boc ref, b> <s @Defop LDBLOB
```

이 명령은 프로그램에 포함될 때 `x{88}`(`PUSHREF`)과 제공된 bag-of-cells에 대한 참조를 쓰는 옵코드를 정의합니다. 따라서 `LDBLOB` 명령이 실행되면 셀을 TVM 스택에 푸시합니다.

## 특별 기능

- Ed25519 암호화
 - newkeypair - 개인-공개 키 쌍 생성
 - priv>pub   - 개인 키에서 공개 키 생성
 - ed25519_sign[_uint] - 데이터와 개인 키가 주어지면 서명 생성
 - ed25519_chksign     - Ed25519 서명 확인
- TVM과의 상호작용
 - runvmcode와 유사 - 스택에서 가져온 코드 슬라이스로 TVM 호출
- BOC를 파일에 쓰기:
 `boc>B ".../contract.boc" B>file`

## 더 알아보기

- Nikolai Durov의 [Fift: A Brief Introduction](https://docs.ton.org/fiftbase.pdf)
