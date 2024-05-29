# 다섯 가지 심층 분석

하이레벨 스택 기반 언어인 Fift는 셀 및 기타 TVM 프리미티브의 로컬 조작에 사용되며, 주로 TVM 어셈블리 코드를 컨트랙트 코드 백오브셀로 변환하는 데 사용됩니다.

:::caution
이 섹션에서는 **매우** 낮은 수준에서 TON 관련 기능과의 상호작용에 대해 설명합니다.
스택 언어의 기본에 대한 진지한 이해가 필요합니다.
:::

## 간단한 산술

Fift 인터프리터를 계산기로 사용하여 [역 폴란드어 표기법](https://en.wikipedia.org/wiki/Reverse_Polish_notation)으로 식을 작성할 수 있습니다.

```
6 17 17 * * 289 + .
2023 ok
```

## 표준 출력

```
27 emit ."[30;1mgrey text" 27 emit ."[37m"
grey text ok
```

emit`은 스택 상단에서 숫자를 가져와 지정된 코드의 유니코드 문자를 stdout에 출력합니다.
"..."`는 상수 문자열을 인쇄합니다.

## 함수 정의(다섯 단어)

단어를 정의하는 주된 방법은 해당 효과를 중괄호로 묶은 다음 `:`와 단어 이름을 쓰는 것입니다.

```
{ minmax drop } : min
{ minmax nip } : max
```

> Fift.fif

하지만 `:`뿐만 아니라 여러 가지 *정의 단어*가 있습니다. 정의어 중 일부는 **활성**(중괄호 안에서 작동), 일부는 **접두사**(뒤에 공백 문자가 올 필요가 없음)로 정의된다는 점에서 차이가 있습니다:

```
{ bl word 1 2 ' (create) } "::" 1 (create)
{ bl word 0 2 ' (create) } :: :
{ bl word 2 2 ' (create) } :: :_
{ bl word 3 2 ' (create) } :: ::_
{ bl word 0 (create) } : create
```

> Fift.fif

## 조건부 실행

코드 블록(중괄호로 구분된 블록)은 조건부 또는 무조건 실행할 수 있습니다.

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

루프 워드 `times`는 두 개의 인자(`cont`와 `n`이라고 부르겠습니다)를 받아 `cont` `n` 번 실행합니다.
여기서 `list-delete-first`는 `safe-cdr`(리스프 스타일 목록에서 헤드를 삭제하는 명령)의 연속을 받아 `c` 아래에 배치한 다음 `c` times는 스택에 있는 목록에서 헤드를 제거합니다.

'동안'과 '때까지'라는 단어도 있습니다.

## 댓글

```
{ 0 word drop 0 'nop } :: //
{ char " word 1 { swap { abort } if drop } } ::_ abort"
{ { bl word dup "" $= abort"comment extends after end of file" "*/" $= } until 0 'nop } :: /*
```

> Fift.fif

주석은 `Fift.fif`에 정의되어 있습니다. 한 줄 코멘트는 `//`로 시작하여 줄 끝으로 이어지고, 여러 줄 코멘트는 `/*`로 시작하여 `*/`로 끝납니다.

왜 그렇게 작동하는지 이해해 봅시다.\
파이브 프로그램은 본질적으로 단어의 시퀀스이며, 각 단어는 어떤 방식으로 스택을 변환하거나 새로운 단어를 정의합니다. 위에 표시된 코드인 `Fift.fif`의 첫 줄은 새로운 단어 `//`의 선언입니다.
주석은 새로운 단어를 정의할 때도 작동해야 하므로 중첩된 환경에서도 작동해야 합니다. 그렇기 때문에 `::`를 사용하여 **활성** 단어로 정의합니다. 생성 중인 단어의 동작은 중괄호 안에 나열됩니다:

1. 0\`: 스택에 0을 밀어 넣습니다.
2. word`: 이 명령은 스택의 맨 위에 해당하는 문자에 도달할 때까지 문자를 읽고 읽은 데이터를 문자열로 밀어넣습니다. 여기서 `word\`는 선행 공백을 건너뛰고 현재 입력 줄의 끝까지 읽습니다.
3. drop\`: 최상위 요소(댓글 데이터)가 스택에서 삭제됩니다.
4. 0`: 단어가 `::\`로 정의되었기 때문에 사용되는 결과의 수인 0이 다시 스택에 푸시됩니다.
5. 'nop'은 호출 시 실행 토큰을 아무것도 하지 않습니다. 이는 `{ nop }`와 거의 동일합니다.

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

> Asm.fif(줄 순서 반전)

Defop`은 옵코드를 넣을 공간이 충분한지 확인하고(`@havebitrefs`), 공간이 충분하지 않으면 다른 빌더(`@|`; 암시적 점프라고도 함)에 계속 쓰도록 합니다. 따라서 일반적으로 `x{A988} s,`를 옵코드로 작성하지 않는 이유는 이 옵코드를 넣을 공간이 부족하여 컴파일에 실패할 수 있으므로 대신 `x{A988} @addop\`을 작성해야 합니다.

Fift를 사용하여 계약에 대용량 셀 백을 포함할 수 있습니다:

```
<b 8 4 u, 8 4 u, "fift/blob.boc" file>B B>boc ref, b> <s @Defop LDBLOB
```

이 명령은 프로그램에 포함될 때 `x{88}`(`PUSHREF`)와 제공된 백 오브 셀에 대한 참조를 쓰는 연산 코드를 정의합니다. 따라서 `LDBLOB` 명령이 실행되면 셀을 TVM 스택으로 푸시합니다.

## 특별 기능

- Ed25519 암호화
  - newkeypair - 개인-공개 키 쌍 생성
  - priv>pub - 비공개에서 공개 키를 생성합니다.
  - ed25519_sign[_uint] - 주어진 데이터와 개인 키로 서명을 생성합니다.
  - ed25519_chksign - Ed25519 서명을 확인합니다.
- TVM과의 상호 작용
  - runvmcode 및 유사 - 스택에서 가져온 코드 슬라이스로 TVM을 호출합니다.
- BOC를 파일에 쓰기:
  `boc>B ".../contract.boc" B>파일`

## 학습 계속하기

- 니콜라이 두로프의 [파이브: 간략한 소개](https://docs.ton.org/fiftbase.pdf)
