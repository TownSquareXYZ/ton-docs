# 함수

FunC 프로그램은 본질적으로 함수 선언/정의와 전역 변수 선언의 목록입니다. 이 섹션에서는 첫 번째 주제를 다룹니다.

모든 함수 선언이나 정의는 공통된 패턴으로 시작하며, 다음 세 가지 중 하나가 이어집니다:

- 단일 `;` - 함수가 선언되었지만 아직 정의되지 않았음을 의미합니다. 같은 파일의 뒷부분이나 FunC 컴파일러에 현재 파일보다 먼저 전달된 다른 파일에서 정의될 수 있습니다. 예를 들어,
  ```func
  int add(int x, int y);
  ```
  는 `(int, int) -> int` 타입의 `add`라는 이름의 함수에 대한 간단한 선언입니다.

- 어셈블러 함수 본문 정의 - FunC 프로그램에서 나중에 사용하기 위해 저수준 TVM 프리미티브로 함수를 정의하는 방법입니다. 예를 들어,
  ```func
  int add(int x, int y) asm "ADD";
  ```
  는 TVM 오프코드 `ADD`로 변환될 `(int, int) -> int` 타입의 동일한 `add` 함수에 대한 어셈블러 정의입니다.

- 일반적인 블록 문 함수 본문 정의 - 함수를 정의하는 일반적인 방법입니다. 예를 들어,
  ```func
  int add(int x, int y) {
    return x + y;
  }
  ```
  는 `add` 함수의 일반적인 정의입니다.

## 함수 선언

앞서 언급했듯이, 모든 함수 선언이나 정의는 공통된 패턴으로 시작합니다. 다음이 그 패턴입니다:

```func
[<forall declarator>] <return_type> <function_name>(<comma_separated_function_args>) <specifiers>
```

여기서 `[ ... ]`는 선택적 항목에 해당합니다.

### 함수 이름

함수 이름은 모든 [식별자](/v3/documentation/smart-contracts/func/docs/literals_identifiers#identifiers)가 될 수 있으며, `.` 또는 `~` 기호로 시작할 수도 있습니다. 이러한 기호의 의미는 statements 섹션에서 [설명](/v3/documentation/smart-contracts/func/docs/statements#methods-calls)됩니다.

예를 들어, `udict_add_builder?`, `dict_set`, `~dict_set`은 모두 유효하고 서로 다른 함수 이름입니다. (이들은 [stdlib.fc](/v3/documentation/smart-contracts/func/docs/stdlib)에 정의되어 있습니다.)

#### 특별한 함수 이름

FunC(실제로는 Fift 어셈블러)는 미리 정의된 [id](/v3/documentation/smart-contracts/func/docs/functions#method_id)를 가진 여러 예약된 함수 이름을 가지고 있습니다.

- `main`과 `recv_internal`은 id = 0
- `recv_external`은 id = -1
- `run_ticktock`은 id = -2

모든 프로그램은 반드시 id가 0인 함수, 즉 `main` 또는 `recv_internal` 함수를 가져야 합니다.
`run_ticktock`은 특별한 스마트 컨트랙트의 틱톡 트랜잭션에서 호출됩니다.

#### 내부 수신

`recv_internal`은 스마트 컨트랙트가 인바운드 내부 메시지를 수신할 때 호출됩니다.
[TVM이 초기화](/v3/documentation/tvm/tvm-overview#initialization-of-tvm)될 때 스택에 몇 가지 변수가 있으며, `recv_internal`에 인수를 설정함으로써 스마트 컨트랙트 코드가 이들 중 일부를 인식하게 합니다. 코드가 알지 못하는 인수들은 스택의 맨 밑에서 전혀 건드리지 않은 채로 있게 됩니다.

따라서 다음의 `recv_internal` 선언들은 모두 올바르지만, 변수가 적은 것들이 약간의 가스를 덜 소비합니다(사용되지 않는 각 인수는 추가적인 `DROP` 명령어를 추가합니다)

```func

() recv_internal(int balance, int msg_value, cell in_msg_cell, slice in_msg) {}
() recv_internal(int msg_value, cell in_msg_cell, slice in_msg) {}
() recv_internal(cell in_msg_cell, slice in_msg) {}
() recv_internal(slice in_msg) {}
```

#### 외부 수신

`recv_external`은 인바운드 외부 메시지를 위한 것입니다.

### 반환 타입

반환 타입은 [타입](/v3/documentation/smart-contracts/func/docs/types) 섹션에서 설명된 모든 원자적 또는 복합 타입이 될 수 있습니다. 예를 들어,

```func
int foo();
(int, int) foo'();
[int, int] foo''();
(int -> int) foo'''();
() foo''''();
```

는 모두 유효한 함수 선언입니다.

타입 추론도 허용됩니다. 예를 들어,

```func
_ pyth(int m, int n) {
  return (m * m - n * n, 2 * m * n, m * m + n * n);
}
```

는 피타고라스 삼중항을 계산하는 `(int, int) -> (int, int, int)` 타입의 `pyth` 함수의 유효한 정의입니다.

### 함수 인수

함수 인수는 쉼표로 구분됩니다. 인수의 유효한 선언은 다음과 같습니다:

- 일반 선언: 타입 + 이름. 예를 들어, `() foo(int x);` 함수 선언에서 `int x`는 `int` 타입과 `x`라는 이름을 가진 인수의 선언입니다.
- 사용되지 않는 인수 선언: 타입만. 예를 들어,
  ```func
  int first(int x, int) {
    return x;
  }
  ```
  는 `(int, int) -> int` 타입의 유효한 함수 정의입니다
- 추론된 타입의 인수 선언: 이름만.
  예를 들어,
  ```func
  int inc(x) {
    return x + 1;
  }
  ```
  는 `int -> int` 타입의 유효한 함수 정의입니다. `x`의 `int` 타입은 타입 체커에 의해 추론됩니다.

함수가 여러 인수를 가진 함수처럼 보일 수 있지만, 실제로는 하나의 [텐서 타입](/v3/documentation/smart-contracts/func/docs/types#tensor-types) 인수를 가진 함수라는 점에 주의하세요. 차이점을 이해하려면 [함수 적용](/v3/documentation/smart-contracts/func/docs/statements#function-application)을 참조하세요. 그럼에도 불구하고, 인수 텐서의 구성 요소들은 관례적으로 함수 인수라고 불립니다.

### 함수 호출

#### 수정하지 않는 메서드

:::info
수정하지 않는 함수는 `.`를 사용한 짧은 함수 호출 형식을 지원합니다
:::

```func
example(a);
a.example();
```

함수가 적어도 하나의 인수를 가지고 있다면, 수정하지 않는 메서드로 호출될 수 있습니다. 예를 들어, `store_uint`는 `(builder, int, int) -> builder` 타입을 가집니다(두 번째 인수는 저장할 값이고, 세 번째는 비트 길이입니다). `begin_cell`은 새로운 빌더를 생성하는 함수입니다. 다음 코드들은 동등합니다:

```func
builder b = begin_cell();
b = store_uint(b, 239, 8);
```

```func
builder b = begin_cell();
b = b.store_uint(239, 8);
```

따라서 함수의 첫 번째 인수는 `.`로 구분되어 함수 이름 앞에 위치할 수 있습니다. 코드는 더 간단하게 만들 수 있습니다:

```func
builder b = begin_cell().store_uint(239, 8);
```

메서드의 다중 호출도 가능합니다:

```func
builder b = begin_cell().store_uint(239, 8)
                        .store_int(-1, 16)
                        .store_uint(0xff, 10);
```

#### 수정하는 함수

:::info
수정하는 함수는 `~`와 `.` 연산자를 사용한 짧은 형식을 지원합니다.
:::

함수의 첫 번째 인수가 타입 `A`를 가지고 함수의 반환 값이 `(A, B)` 형태를 가질 때(`B`는 임의의 타입), 그 함수는 수정하는 메서드로 호출될 수 있습니다.

수정하는 함수 호출은 일부 인수를 받고 일부 값을 반환할 수 있지만, 첫 번째 인수를 수정합니다. 즉, 반환된 값의 첫 번째 구성 요소를 첫 번째 인수의 변수에 할당합니다.

```func
a~example();
a = example(a);
```

예를 들어, `cs`가 셀 슬라이스이고 `load_uint`가 `(slice, int) -> (slice, int)` 타입을 가진다고 가정해봅시다: 이는 셀 슬라이스와 로드할 비트 수를 받아서 슬라이스의 나머지와 로드된 값을 반환합니다. 다음 코드들은 동등합니다:

```func
(cs, int x) = load_uint(cs, 8);
```

```func
(cs, int x) = cs.load_uint(8);
```

```func
int x = cs~load_uint(8);
```

어떤 경우에는 값을 반환하지 않고 첫 번째 인수만 수정하는 함수를 수정하는 메서드로 사용하고 싶을 수 있습니다. 이는 다음과 같이 unit 타입을 사용하여 수행할 수 있습니다: 정수를 증가시키는 `int -> int` 타입의 `inc` 함수를 정의하고 이를 수정하는 메서드로 사용하고 싶다고 가정해봅시다. 그렇다면 `inc`를 `int -> (int, ())` 타입의 함수로 정의해야 합니다:

```func
(int, ()) inc(int x) {
  return (x + 1, ());
}
```

이렇게 정의하면 수정하는 메서드로 사용할 수 있습니다. 다음은 `x`를 증가시킬 것입니다.

```func
x~inc();
```

#### 함수 이름의 `.`와 `~`

`inc`를 수정하지 않는 메서드로도 사용하고 싶다고 가정해봅시다. 다음과 같이 작성할 수 있습니다:

```func
(int y, _) = inc(x);
```

하지만 수정하는 메서드로서의 `inc` 정의를 오버라이드하는 것이 가능합니다.

```func
int inc(int x) {
  return x + 1;
}
(int, ()) ~inc(int x) {
  return (x + 1, ());
}
```

그리고 다음과 같이 호출할 수 있습니다:

```func
x~inc();
int y = inc(x);
int z = x.inc();
```

첫 번째 호출은 x를 수정할 것이고; 두 번째와 세 번째는 수정하지 않을 것입니다.

요약하면, `foo`라는 이름의 함수가 수정하지 않는 메서드나 수정하는 메서드로 호출될 때(즉, `.foo` 또는 `~foo` 구문으로), FunC 컴파일러는 그러한 정의가 있다면 `.foo` 또는 `~foo`의 정의를 사용하고, 없다면 `foo`의 정의를 사용합니다.

### 지정자

세 가지 유형의 지정자가 있습니다: `impure`, `inline`/`inline_ref`, 그리고 `method_id`. 함수 선언에 이들 중 하나, 여러 개, 또는 아무것도 넣을 수 있지만 현재는 올바른 순서로 제시되어야 합니다. 예를 들어, `impure`를 `inline` 뒤에 넣는 것은 허용되지 않습니다.

#### Impure 지정자

`impure` 지정자는 함수가 무시할 수 없는 부작용을 가질 수 있음을 의미합니다. 예를 들어, 함수가 컨트랙트 저장소를 수정하거나, 메시지를 보내거나, 일부 데이터가 유효하지 않을 때 예외를 던지고 그 함수가 이 데이터를 검증하기 위한 것이라면 `impure` 지정자를 넣어야 합니다.

`impure`가 지정되지 않았고 함수 호출의 결과가 사용되지 않는다면, FunC 컴파일러는 이 함수 호출을 삭제할 수 있고 또 삭제할 것입니다.

예를 들어, [stdlib.fc](/v3/documentation/smart-contracts/func/docs/stdlib)에서

```func
int random() impure asm "RANDU256";
```

가 정의되어 있습니다. `RANDU256`이 난수 생성기의 내부 상태를 변경하기 때문에 `impure`가 사용됩니다.

#### Inline 지정자

함수가 `inline` 지정자를 가지면, 그 코드는 실제로 함수가 호출되는 모든 곳에서 대체됩니다. 당연하게도, 인라인된 함수에 대한 재귀 호출은 불가능합니다.

예를 들어,

```func
(int) add(int a, int b) inline {
    return a + b;
}
```

`add` 함수는 `inline` 지정자로 표시되어 있습니다. 컴파일러는 `add` 호출을 실제 코드 `a + b`로 대체하여 함수 호출 오버헤드를 피하려고 할 것입니다.

인라인을 사용할 수 있는 또 다른 예시는 [ICO-Minter.fc](https://github.com/ton-blockchain/token-contract/blob/f2253cb0f0e1ae0974d7dc0cef3a62cb6e19f806/ft/jetton-minter-ICO.fc#L16)에서 가져온 것입니다:

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

`inline_ref` 지정자를 가진 함수의 코드는 별도의 셀에 넣어지며, 함수가 호출될 때마다 TVM에 의해 `CALLREF` 명령이 실행됩니다. 따라서 `inline`과 비슷하지만, 셀은 중복 없이 여러 곳에서 재사용될 수 있기 때문에, 함수가 정확히 한 번만 호출되는 경우가 아니라면 거의 항상 코드 크기 면에서 `inline` 대신 `inline_ref` 지정자를 사용하는 것이 더 효율적입니다. TVM 셀에는 순환 참조가 없기 때문에 `inline_ref`된 함수의 재귀 호출은 여전히 불가능합니다.

#### method_id

TVM 프로그램의 모든 함수는 호출될 수 있는 내부 정수 id를 가집니다. 일반 함수는 보통 1부터 시작하는 연속적인 정수로 번호가 매겨지지만, 컨트랙트의 get-메서드는 이름의 crc16 해시로 번호가 매겨집니다. `method_id(<some_number>)` 지정자는 함수의 id를 지정된 값으로 설정할 수 있게 하며, `method_id`는 기본값 `(crc16(<function_name>) & 0xffff) | 0x10000`을 사용합니다. 함수가 `method_id` 지정자를 가지면, 라이트-클라이언트나 ton-explorer에서 get-메서드로 이름을 통해 호출될 수 있습니다.

예를 들어,

```func
(int, int) get_n_k() method_id {
  (_, int n, int k, _, _, _, _) = unpack_state();
  return (n, k);
}
```

는 멀티시그 컨트랙트의 get-메서드입니다.

### forall을 사용한 다형성

모든 함수 선언이나 정의 앞에는 `forall` 타입 변수 선언자가 올 수 있습니다. 구문은 다음과 같습니다:

```func
forall <comma_separated_type_variables_names> ->
```

여기서 타입 변수 이름은 아무 [식별자](/v3/documentation/smart-contracts/func/docs/literals_identifiers#identifiers)가 될 수 있습니다. 보통 대문자로 이름을 짓습니다.

예를 들어,

```func
forall X, Y -> [Y, X] pair_swap([X, Y] pair) {
  [X p1, Y p2] = pair;
  return [p2, p1];
}
```

는 정확히 길이가 2인 튜플을 받아서, 구성 요소의 값이 어떤 (단일 스택 항목) 타입이든 상관없이 서로 교환하는 함수입니다.

`pair_swap([2, 3])`은 `[3, 2]`를 생성하고 `pair_swap([1, [2, 3, 4]])`는 `[[2, 3, 4], 1]`을 생성할 것입니다.

이 예시에서 `X`와 `Y`는 [타입 변수](/v3/documentation/smart-contracts/func/docs/types#polymorphism-with-type-variables)입니다. 함수가 호출될 때, 타입 변수는 실제 타입으로 대체되고 함수의 코드가 실행됩니다. 함수가 다형성을 가지지만, 실제 어셈블러 코드는 모든 타입 대체에 대해 동일하다는 점에 주목하세요. 이는 본질적으로 스택 조작 프리미티브의 다형성을 통해 달성됩니다. 현재 다른 형태의 다형성(타입 클래스를 사용한 애드혹 다형성과 같은)은 지원되지 않습니다.

또한, `X`와 `Y`의 타입 너비가 1이어야 한다는 점에 주의해야 합니다; 즉, `X`나 `Y`의 값은 단일 스택 항목을 차지해야 합니다. 따라서 실제로는 `[(int, int), int]` 타입의 튜플에 대해 `pair_swap` 함수를 호출할 수 없습니다. 왜냐하면 `(int, int)` 타입은 너비가 2이기 때문입니다. 즉, 2개의 스택 항목을 차지합니다.

## 어셈블러 함수 본문 정의

앞서 언급했듯이, 함수는 어셈블러 코드로 정의될 수 있습니다. 구문은 `asm` 키워드 뒤에 하나 또는 여러 개의 어셈블러 명령어가 문자열로 표현되는 것입니다.
예를 들어, 다음과 같이 정의할 수 있습니다:

```func
int inc_then_negate(int x) asm "INC" "NEGATE";
```

– 정수를 증가시키고 이를 부정(음수로 변환)하는 함수입니다. 이 함수에 대한 호출은 두 개의 어셈블리 명령어 `INC`와 `NEGATE`로 변환됩니다. 이 함수를 정의하는 또 다른 방법은 다음과 같습니다:

```func
int inc_then_negate'(int x) asm "INC NEGATE";
```

`INC NEGATE`는 FunC에 의해 하나의 어셈블러 명령어로 간주되지만, Fift 어셈블러가 이것이 2개의 별개의 명령어라는 것을 알기 때문에 괜찮습니다.

:::info
어셈블러 명령어 목록은 여기에서 찾을 수 있습니다: [TVM instructions](/v3/documentation/tvm/instructions).
:::

### 스택 항목 재배치

어떤 경우에는 어셈블러 명령어가 요구하는 것과 다른 순서로 인수를 전달하거나, 명령어가 반환하는 것과 다른 스택 항목 순서로 결과를 받고 싶을 수 있습니다. 해당하는 스택 프리미티브를 추가하여 수동으로 스택을 재배치할 수 있지만, FunC가 자동으로 이를 수행할 수 있습니다.

:::info
수동 재배치의 경우, 인수는 재배치된 순서로 계산될 것입니다. 이 동작을 재정의하려면 `#pragma compute-asm-ltr`를 사용하세요: [compute-asm-ltr](/v3/documentation/smart-contracts/func/docs/compiler_directives#pragma-compute-asm-ltr)
:::

예를 들어, STUXQ 어셈블러 명령어가 정수, 빌더, 정수를 받은 다음 빌더와 함께 연산의 성공 또는 실패를 나타내는 정수 플래그를 반환한다고 가정해봅시다.
다음과 같이 함수를 정의할 수 있습니다:

```func
(builder, int) store_uint_quite(int x, builder b, int len) asm "STUXQ";
```

하지만 인수를 재배치하고 싶다고 가정해봅시다. 그러면 다음과 같이 정의할 수 있습니다:

```func
(builder, int) store_uint_quite(builder b, int x, int len) asm(x b len) "STUXQ";
```

따라서 `asm` 키워드 뒤에 필요한 인수 순서를 지정할 수 있습니다.

또한, 다음과 같이 반환 값을 재배치할 수 있습니다:

```func
(int, builder) store_uint_quite(int x, builder b, int len) asm( -> 1 0) "STUXQ";
```

숫자는 반환된 값의 인덱스에 해당합니다(0은 반환된 값들 중 가장 깊은 스택 항목).

이러한 기법들을 결합하는 것도 가능합니다.

```func
(int, builder) store_uint_quite(builder b, int x, int len) asm(x b len -> 1 0) "STUXQ";
```

### 여러 줄 asm

여러 줄의 어셈블러 명령어나 심지어 Fift-코드 스니펫도 `"""`로 시작하고 끝나는 여러 줄 문자열을 통해 정의할 수 있습니다.

```func
slice hello_world() asm """
  "Hello"
  " "
  "World"
  $+ $+ $>s
  PUSHSLICE
""";
```
