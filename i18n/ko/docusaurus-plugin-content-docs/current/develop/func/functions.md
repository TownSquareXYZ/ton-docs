# 기능

FunC 프로그램은 기본적으로 함수 선언/정의와 전역 변수 선언의 목록입니다. 이 섹션에서는 첫 번째 주제를 다룹니다.

모든 함수 선언이나 정의는 공통 패턴으로 시작하며 다음 세 가지 중 하나가 진행됩니다:

- 단일 `;`는 함수가 선언되었지만 아직 정의되지 않았음을 의미합니다. 이 함수는 나중에 같은 파일이나 현재 파일보다 먼저 FunC 컴파일러에 전달되는 다른 파일에서 정의될 수 있습니다. 예를 들어
  ```func
  int add(int x, int y);
  ```
  는 `(int, int) -> int` 타입의 `add`라는 함수를 간단히 선언한 것입니다.

- 어셈블러 함수 본문 정의. 나중에 FunC 프로그램에서 사용할 수 있도록 저수준 TVM 프리미티브로 함수를 정의하는 방식입니다. 예를 들어
  ```func
  int add(int x, int y) asm "ADD";
  ```
  는 '(int, int) -> int' 타입의 동일한 함수 `add`에 대한 어셈블러 정의이며, 이는 TVM 연산자 코드 `ADD`로 변환됩니다.

- 일반 블록 문 함수 본문 정의. 함수를 정의하는 일반적인 방법입니다. 예를 들어
  ```func
  int add(int x, int y) {
    return x + y;
  }
  ```
  는 `add` 함수의 일반적인 정의입니다.

## 함수 선언

앞서 말했듯이 모든 함수 선언이나 정의는 공통 패턴으로 시작됩니다. 다음은 그 패턴입니다:

```func
[<forall declarator>] <return_type> <function_name>(<comma_separated_function_args>) <specifiers>
```

여기서 '[ ... ]\`는 선택 항목에 해당합니다.

### 함수 이름

함수 이름은 [식별자](/develop/func/literals_identifiers#identifiers)를 사용할 수 있으며, '.`또는`~\` 기호로 시작할 수도 있습니다. 이러한 기호의 의미는 문 섹션의 [설명](/develop/func/statements#methods-calls)에 나와 있습니다.

예를 들어 `udict_add_builder?`, `dict_set` 및 `~dict_set`은 유효하고 다른 함수 이름입니다. (이 함수는 [stdlib.fc](/develop/func/stdlib)에 정의되어 있습니다).

#### 특수 함수 이름

FunC(실제로는 Fift 어셈블러)에는 미리 정의된 [ids](/develop/func/functions#method_id)로 예약된 함수 이름이 여러 개 있습니다.

- 메인`및`recv_internal\`의 id는 0입니다.
- 레브_외부\`의 아이디는 -1입니다.
- run_ticktock\`의 ID는 -2입니다.

모든 프로그램에는 아이디가 0인 함수, 즉 `main` 또는 `recv_internal` 함수가 있어야 합니다.
런_틱톡\`은 특수 스마트 컨트랙트의 틱톡 트랜잭션에서 호출됩니다.

#### 내부 수신

recv_internal`은 스마트 컨트랙트가 인바운드 내부 메시지를 수신할 때 호출됩니다.
TVM이 시작될 때 스택에 몇 가지 변수가 있는데(/learn/tvm-instructions/tvm-overview#initialization-of-tvm), `recv_internal\`에 인수를 설정하면 스마트 컨트랙트 코드가 이 중 일부에 대해 인식할 수 있게 됩니다. 어떤 코드가 알지 못하는 인수는 스택의 맨 아래에 위치하여 절대 건드리지 않습니다.

따라서 다음의 `recv_internal` 선언은 각각 정확하지만 변수가 적은 선언은 가스를 약간 덜 소비합니다(사용하지 않는 인수가 있을 때마다 `DROP` 명령어가 추가됩니다).

```func

() recv_internal(int balance, int msg_value, cell in_msg_cell, slice in_msg) {}
() recv_internal(int msg_value, cell in_msg_cell, slice in_msg) {}
() recv_internal(cell in_msg_cell, slice in_msg) {}
() recv_internal(slice in_msg) {}
```

#### 외부 수신

'recv_external'은 인바운드 외부 메시지용입니다.

### 반환 유형

반환 유형은 [types](/develop/func/types.md) 섹션에 설명된 대로 원자 또는 복합 유형일 수 있습니다. 예를 들어

```func
int foo();
(int, int) foo'();
[int, int] foo''();
(int -> int) foo'''();
() foo''''();
```

는 유효한 함수 선언입니다.

유형 추론도 허용됩니다. 예를 들어

```func
_ pyth(int m, int n) {
  return (m * m - n * n, 2 * m * n, m * m + n * n);
}
```

는 피타고라스의 3배수를 계산하는 `(int, int) -> (int, int, int)` 유형의 함수 `pyth`의 유효한 정의입니다.

### 함수 인수

함수 인수는 쉼표로 구분됩니다. 인수의 유효한 선언은 다음과 같습니다:

- 일반 선언: 유형 + 이름. 예를 들어, `int x`는 함수 선언 `() foo(int x);`에서 유형 `int`와 이름 `x`의 인수를 선언한 것입니다.
- 사용하지 않은 인수 선언: 유형만 입력합니다. 예를 들어
  ```func
  int first(int x, int) {
    return x;
  }
  ```
  는 `(int, int) -> int` 타입의 유효한 함수 정의입니다.
- 추론된 타입 선언이 있는 인수: 이름만.
  예를 들어
  ```func
  int inc(x) {
    return x + 1;
  }
  ```
  는 `int -> int` 타입의 유효한 함수 정의입니다. x`의 `int\` 타입은 타입 검사기에 의해 추론됩니다.

함수는 여러 개의 인자로 구성된 함수처럼 보이지만, 실제로는 하나의 [텐서 타입](/develop/func/types#텐서 타입) 인자로 구성된 함수라는 점에 유의하세요. 차이점을 확인하려면 [함수 적용](/develop/func/statements#function-application)을 참조하세요. 그럼에도 불구하고 인자 텐서의 구성 요소는 일반적으로 함수 인자라고 불립니다.

### 함수 호출

#### 비수정 방법

:::info
비수정 함수는 `.`로 짧은 함수 호출 형식을 지원합니다.
:::

```func
example(a);
a.example();
```

함수에 인자가 하나 이상 있는 경우, 수정되지 않는 메서드로 호출할 수 있습니다. 예를 들어 `store_uint`의 타입은 `(빌더, int, int) -> 빌더`입니다(두 번째 인자는 저장할 값이고 세 번째 인자는 비트 길이입니다). begin_cell\`은 새 빌더를 생성하는 함수입니다. 다음 코드가 이에 해당합니다:

```func
builder b = begin_cell();
b = store_uint(b, 239, 8);
```

```func
builder b = begin_cell();
b = b.store_uint(239, 8);
```

따라서 함수의 첫 번째 인수는 함수 이름 앞에 `.`로 구분하여 전달할 수 있습니다. 코드를 더 단순화할 수 있습니다:

```func
builder b = begin_cell().store_uint(239, 8);
```

메서드를 여러 번 호출할 수도 있습니다:

```func
builder b = begin_cell().store_uint(239, 8)
                        .store_int(-1, 16)
                        .store_uint(0xff, 10);
```

#### 기능 수정

:::info
수정 함수는 `~` 및 '.\` 연산자를 사용한 짧은 형식을 지원합니다.
:::

함수의 첫 번째 인자가 `A` 타입이고 함수의 반환값이 `(A, B)` 형태이고 `B`가 임의의 타입인 경우, 함수를 수정 메서드로 호출할 수 있습니다.

함수 호출을 수정하면 일부 인수를 받고 일부 값을 반환할 수 있지만, 첫 번째 인수를 수정하는 즉, 반환된 값의 첫 번째 구성 요소를 첫 번째 인수에서 변수에 할당합니다.

```func
a~example();
a = example(a);
```

예를 들어 `cs`가 셀 슬라이스이고 `load_uint`의 타입이 `(슬라이스, int) -> (슬라이스, int)`라고 가정하면 셀 슬라이스와 로드할 비트 수를 취하고 나머지 슬라이스와 로드된 값을 반환하는 함수를 사용할 수 있습니다. 다음 코드가 이에 해당합니다:

```func
(cs, int x) = load_uint(cs, 8);
```

```func
(cs, int x) = cs.load_uint(8);
```

```func
int x = cs~load_uint(8);
```

어떤 경우에는 값을 반환하지 않고 첫 번째 인수만 수정하는 수정 메서드로 함수를 사용하고 싶을 때가 있습니다. 단위 타입을 사용하면 다음과 같이 할 수 있습니다: 정수를 증가시키는 `int -> int` 타입의 `inc` 함수를 정의하고 이를 수정 메서드로 사용한다고 가정해 보겠습니다. 그런 다음 `inc`를 `int -> (int, ())` 타입의 함수로 정의해야 합니다:

```func
(int, ()) inc(int x) {
  return (x + 1, ());
}
```

이렇게 정의하면 수정 메서드로 사용할 수 있습니다. 다음은 `x`를 증가시킵니다.

```func
x~inc();
```

#### 함수 이름에 `.` 및 `~` 사용

수정하지 않는 메서드로 `inc`를 사용한다고 가정해 보겠습니다. 이렇게 작성할 수 있습니다:

```func
(int y, _) = inc(x);
```

그러나 수정 메서드로서 `inc`의 정의를 재정의할 수 있습니다.

```func
int inc(int x) {
  return x + 1;
}
(int, ()) ~inc(int x) {
  return (x + 1, ());
}
```

그리고 그렇게 전화하세요:

```func
x~inc();
int y = inc(x);
int z = x.inc();
```

첫 번째 호출은 x를 수정하지만 두 번째와 세 번째 호출은 수정하지 않습니다.

요약하면, 이름이 `foo`인 함수가 비수정 또는 수정 메서드로 호출될 때(즉, `.foo` 또는 `~foo` 구문으로), FunC 컴파일러는 해당 정의가 제시되면 그에 해당하는 '.foo' 또는 `~foo`의 정의를 사용하고, 그렇지 않으면 `foo`의 정의를 사용합니다.

### 지정자

지정자에는 세 가지 유형이 있습니다: `impure`, `inline`/`inline_ref`, `method_id`. 함수 선언에 이 지정자를 하나, 여러 개 또는 전혀 넣지 않을 수 있지만 현재는 올바른 순서로 제시해야 합니다. 예를 들어, `inline` 뒤에 `impure`를 넣는 것은 허용되지 않습니다.

#### 불순한 지정자

불순한`지정자는 함수가 무시할 수 없는 부작용을 가질 수 있음을 의미합니다. 예를 들어, 함수가 컨트랙트 저장소를 수정하거나 메시지를 보내거나 일부 데이터가 유효하지 않은 경우 예외를 발생시킬 수 있고 이 데이터의 유효성을 검사하기 위한 함수라면`impure\` 지정자를 넣어야 합니다.

불순물\`이 지정되지 않고 함수 호출의 결과가 사용되지 않으면 FunC 컴파일러는 이 함수 호출을 삭제할 수 있으며 삭제합니다.

예를 들어, [stdlib.fc](/develop/func/stdlib) 함수에서 다음을 수행합니다.

```func
int random() impure asm "RANDU256";
```

가 정의됩니다. RANDU256`이 난수 생성기의 내부 상태를 변경하기 때문에 `impure\`가 사용됩니다.

#### 인라인 지정자

함수에 `인라인` 지정자가 있으면 함수가 호출되는 모든 위치에서 해당 코드가 실제로 대체됩니다. 인라인 함수에 대한 재귀 호출이 불가능하다는 것은 말할 필요도 없습니다.

예를 들어, 이 예제에서는 이렇게 '인라인'을 사용할 수 있습니다: [ICO-Minter.fc](https://github.com/ton-blockchain/token-contract/blob/f2253cb0f0e1ae0974d7dc0cef3a62cb6e19f806/ft/jetton-minter-ICO.fc#L16)

```func
() save_data(int total_supply, slice admin_address, cell content, cell jetton_wallet_code) impure inline {
  set_data(begin_cell()
            .store_coins(total_supply)
            .store_slice(admin_address)
            .store_ref(content)
            .store_ref(jetton_wallet_code)
           .end_cell()
          );
}
```

#### Inline_ref 지정자

inline_ref`지정자가 있는 함수의 코드는 별도의 셀에 넣어두고, 함수가 호출될 때마다 TVM에서`CALLREF`명령을 실행합니다. 따라서`inline`과 비슷하지만 셀을 중복하지 않고 여러 곳에서 재사용할 수 있기 때문에 함수를 정확히 한 번만 호출하는 경우가 아니라면 `inline`대신`inline_ref`지정자를 사용하는 것이 코드 크기 측면에서 더 효율적입니다. TVM 셀에는 순환 참조가 없기 때문에`inline_ref\`가 지정된 함수의 재귀 호출은 여전히 불가능합니다.

#### method_id

TVM 프로그램의 모든 함수에는 호출할 수 있는 내부 정수 ID가 있습니다. 일반 함수는 보통 1부터 시작하는 정수로 번호가 매겨지지만 컨트랙트의 get 메서드는 이름의 crc16 해시로 번호가 매겨집니다. 'method_id(\<some_number>)`지정자는 함수의 아이디를 지정된 값으로 설정할 수 있으며,`method_id`는 기본값인 '(crc16(<function_name>) & 0xffff) | 0x10000'을 사용합니다. 함수에 `method_id\` 지정자가 있는 경우, 해당 함수의 이름으로 라이트클라이언트 또는 톤 탐색기에서 get-method로 호출할 수 있습니다.

예를 들어

```func
(int, int) get_n_k() method_id {
  (_, int n, int k, _, _, _, _) = unpack_state();
  return (n, k);
}
```

는 다중 서명 컨트랙트의 가져오기 메서드입니다.

### 포올을 사용한 다형성

함수 선언이나 정의 앞에 `forall` 타입 변수 선언자가 있을 수 있습니다. 이 구문은 다음과 같습니다:

```func
forall <comma_separated_type_variables_names> ->
```

여기서 유형 변수 이름은 [식별자](/개발/펀크/리터럴_식별자#식별자)를 사용할 수 있습니다. 일반적으로 대문자로 이름을 지정합니다.

예를 들어

```func
forall X, Y -> [Y, X] pair_swap([X, Y] pair) {
  [X p1, Y p2] = pair;
  return [p2, p1];
}
```

는 길이가 정확히 2이지만 컴포넌트에서 임의의 (단일 스택 항목) 유형의 값을 가진 튜플을 가져와서 서로 교환하는 함수입니다.

pair_swap([2, 3])`은 `[3, 2]`를 생성하고 `pair_swap([1, [2, 3, 4]])`은 `[[2, 3, 4], 1]\`을 생성합니다.

이 예제에서 `X`와 `Y`는 [타입 변수](/develop/func/types#polymorphism-with-type-variables)입니다. 함수가 호출되면 타입 변수가 실제 타입으로 치환되고 함수의 코드가 실행됩니다. 함수는 다형성이지만 함수에 대한 실제 어셈블러 코드는 모든 타입 치환에 대해 동일하다는 점에 유의하세요. 이는 본질적으로 스택 조작 프리미티브의 다형성에 의해 달성됩니다. 현재 다른 형태의 다형성(예: 타입 클래스를 사용한 임시 다형성)은 지원되지 않습니다.

또한 `X`와 `Y`의 타입 폭이 1이어야 한다는 것, 즉 `X` 또는 `Y`의 값이 하나의 스택 엔트리를 차지해야 한다는 점에 주목할 필요가 있습니다. 따라서 실제로 `[(int, int), int]` 타입의 튜플에서는 `pair_swap` 함수를 호출할 수 없습니다. 왜냐하면 `(int, int)` 타입의 폭이 2이므로 스택 엔트리를 2개 차지하기 때문입니다.

## 어셈블러 함수 본문 정의

위에서 언급했듯이 함수는 어셈블러 코드로 정의할 수 있습니다. 구문은 `asm` 키워드 뒤에 하나 또는 여러 개의 어셈블러 명령어가 문자열로 표시됩니다.
예를 들어 다음과 같이 정의할 수 있습니다:

```func
int inc_then_negate(int x) asm "INC" "NEGATE";
```

- 정수를 증가시킨 다음 음수화하는 함수입니다. 이 함수에 대한 호출은 두 개의 어셈블러 명령 `INC`와 `NEGATE`로 변환됩니다. 함수를 정의하는 다른 방법은 다음과 같습니다:

```func
int inc_then_negate'(int x) asm "INC NEGATE";
```

FunC는 `INC NEGATE`를 하나의 어셈블러 명령으로 간주하지만 Fift 어셈블러는 2개의 개별 명령이라는 것을 알고 있기 때문에 괜찮습니다.

:::info
어셈블러 명령어 목록은 여기에서 확인할 수 있습니다: [TVM 지침](/학습/tvm-instructions/지침).
:::

### 스택 항목 재정렬

어셈블러 명령에 필요한 순서와 다른 순서로 어셈블러 함수에 인수를 전달하거나 명령이 반환하는 것과 다른 스택 항목 순서로 결과를 가져오고 싶은 경우가 있습니다. 수동으로 해당 스택 프리미티브를 추가하여 스택을 재정렬할 수도 있지만, FunC는 이를 자동으로 수행할 수 있습니다.

:::info
수동으로 재정렬하는 경우 인수는 재정렬된 순서대로 계산된다는 점에 유의하세요. 이 동작을 덮어쓰려면 `#pragma compute-asm-ltr`을 사용합니다: [compute-asm-ltr](컴파일러_디렉티브#pragma-compute-asm-ltr)
:::

예를 들어 어셈블러 명령 STUXQ가 정수, 빌더, 정수를 받은 다음 연산의 성공 또는 실패를 나타내는 정수 플래그와 함께 빌더를 반환한다고 가정해 보겠습니다.
함수를 정의할 수 있습니다:

```func
(builder, int) store_uint_quite(int x, builder b, int len) asm "STUXQ";
```

그러나 인수를 재정렬하고 싶다고 가정해 보겠습니다. 그러면 정의할 수 있습니다:

```func
(builder, int) store_uint_quite(builder b, int x, int len) asm(x b len) "STUXQ";
```

따라서 `asm` 키워드 뒤에 필요한 인수의 순서를 지정할 수 있습니다.

또한 다음과 같이 반환 값을 재정렬할 수도 있습니다:

```func
(int, builder) store_uint_quite(int x, builder b, int len) asm( -> 1 0) "STUXQ";
```

숫자는 반환된 값의 인덱스에 해당합니다(0은 반환된 값 중 가장 깊은 스택 항목입니다).

이 기술을 결합하는 것도 가능합니다.

```func
(int, builder) store_uint_quite(builder b, int x, int len) asm(x b len -> 1 0) "STUXQ";
```

### 멀티라인 ASMS

여러 줄의 어셈블러 명령 또는 `"""`로 시작하고 끝나는 여러 줄의 문자열을 통해 파이브 코드 스니펫을 정의할 수도 있습니다.

```func
slice hello_world() asm """
  "Hello"
  " "
  "World"
  $+ $+ $>s
  PUSHSLICE
""";
```
