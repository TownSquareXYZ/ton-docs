# 구문

이 섹션에서는 일반 함수 본문을 구성하는 FunC 구문들을 간단히 설명합니다.

## 표현식 구문

가장 일반적인 구문 유형은 표현식 구문입니다. 이는 `;`가 따라오는 표현식입니다. 표현식의 설명은 매우 복잡할 수 있으므로, 여기서는 간략한 설명만 제시합니다. 규칙적으로 모든 하위 표현식은 [asm 스택 재배치](/v3/documentation/smart-contracts/func/docs/functions#rearranging-stack-entries)의 예외를 제외하고는 왼쪽에서 오른쪽으로 계산됩니다.

### 변수 선언

초기값을 정의하지 않고 지역 변수를 선언하는 것은 불가능합니다.

다음은 변수 선언의 몇 가지 예시입니다:

```func
int x = 2;
var x = 2;
(int, int) p = (1, 2);
(int, var) p = (1, 2);
(int, int, int) (x, y, z) = (1, 2, 3);
(int x, int y, int z) = (1, 2, 3);
var (x, y, z) = (1, 2, 3);
(int x = 1, int y = 2, int z = 3);
[int, int, int] [x, y, z] = [1, 2, 3];
[int x, int y, int z] = [1, 2, 3];
var [x, y, z] = [1, 2, 3];
```

변수는 동일한 범위 내에서 "재선언"될 수 있습니다. 예를 들어, 이는 올바른 코드입니다:

```func
int x = 2;
int y = x + 1;
int x = 3;
```

사실, `int x`의 두 번째 등장은 선언이 아니라 `x`가 `int` 타입을 가진다는 컴파일 타임 보험일 뿐입니다. 따라서 세 번째 줄은 본질적으로 간단한 할당 `x = 3;`과 동등합니다.

중첩된 범위에서는 C 언어처럼 변수를 진정으로 재선언할 수 있습니다. 예를 들어, 다음 코드를 고려해보세요:

```func
int x = 0;
int i = 0;
while (i < 10) {
  (int, int) x = (i, i + 1);
  ;; here x is a variable of type (int, int)
  i += 1;
}
;; here x is a (different) variable of type int
```

하지만 전역 변수 [섹션](/v3/documentation/smart-contracts/func/docs/global_variables)에서 언급했듯이, 전역 변수는 재선언될 수 없습니다.

변수 선언은 표현식 구문**이라는** 점에 주목하세요, 따라서 실제로 `int x = 2`와 같은 구문은 완전한 표현식입니다. 예를 들어, 이는 올바른 코드입니다:

```func
int y = (int x = 3) + 1;
```

이는 각각 `3`과 `4`에 해당하는 두 변수 `x`와 `y`의 선언입니다.

#### 밑줄

밑줄 `_`은 값이 필요하지 않을 때 사용됩니다. 예를 들어, `foo` 함수가 `int -> (int, int, int)` 타입을 가진다고 가정해봅시다. 우리는 다음과 같이 첫 번째 반환 값을 얻고 두 번째와 세 번째를 무시할 수 있습니다:

```func
(int fst, _, _) = foo(42);
```

### 함수 적용

함수 호출은 일반적인 언어에서처럼 보입니다. 함수 호출의 인수들은 함수 이름 뒤에 쉼표로 구분되어 나열됩니다.

```func
;; suppose foo has type (int, int, int) -> int
int x = foo(1, 2, 3);
```

하지만 `foo`가 실제로는 `(int, int, int)` 타입의 **하나의** 인수를 가진 함수라는 점에 주목하세요. 차이점을 보려면, `bar`가 `int -> (int, int, int)` 타입의 함수라고 가정해봅시다. 일반적인 언어와는 달리, 다음과 같이 함수들을 합성할 수 있습니다:

```func
int x = foo(bar(42));
```

다음과 같은 더 긴 형태 대신:

```func
(int a, int b, int c) = bar(42);
int x = foo(a, b, c);
```

또한 Haskell 스타일의 호출도 가능하지만, 항상 가능한 것은 아닙니다(나중에 수정될 예정):

```func
;; suppose foo has type int -> int -> int -> int
;; i.e. it's carried
(int a, int b, int c) = (1, 2, 3);
int x = foo a b c; ;; ok
;; int y = foo 1 2 3; wouldn't compile
int y = foo (1) (2) (3); ;; ok
```

### 람다 표현식

람다 표현식은 아직 지원되지 않습니다.

### 메서드 호출

#### 수정하지 않는 메서드

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

#### 수정하는 메서드

함수의 첫 번째 인수가 타입 `A`를 가지고 함수의 반환 값이 `(A, B)` 형태를 가질 때(`B`는 임의의 타입), 그 함수는 수정하는 메서드로 호출될 수 있습니다. 수정하는 메서드 호출은 일부 인수를 받고 일부 값을 반환할 수 있지만, 첫 번째 인수를 수정합니다. 즉, 반환된 값의 첫 번째 구성 요소를 첫 번째 인수의 변수에 할당합니다. 예를 들어, `cs`가 셀 슬라이스이고 `load_uint`가 `(slice, int) -> (slice, int)` 타입을 가진다고 가정해봅시다: 이는 셀 슬라이스와 로드할 비트 수를 받아서 슬라이스의 나머지와 로드된 값을 반환합니다. 다음 코드들은 동등합니다:

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

### 연산자

현재 모든 단항 및 이항 연산자가 정수 연산자라는 점에 주목하세요. 논리 연산자는 비트 단위 정수 연산자로 표현됩니다 (참조: [불리언 타입의 부재](/v3/documentation/smart-contracts/func/docs/types#absence-of-boolean-type)).

#### 단항 연산자

두 가지 단항 연산자가 있습니다:

- `~`는 비트 단위 not (우선순위 75)
- `-`는 정수 부정 (우선순위 20)

이들은 인수와 분리되어야 합니다:

- `- x`는 정상입니다.
- `-x`는 정상이 아닙니다 (단일 식별자입니다)

#### 이항 연산자

우선순위 30 (왼쪽 결합):

- `*`는 정수 곱셈
- `/`는 정수 나눗셈 (내림)
- `~/`는 정수 나눗셈 (반올림)
- `^/`는 정수 나눗셈 (올림)
- `%`는 모듈로로 정수 축소 (내림)
- `~%`는 모듈로로 정수 축소 (반올림)
- `^%`는 모듈로로 정수 축소 (올림)
- `/%`는 몫과 나머지를 반환
- `&`는 비트 단위 AND

우선순위 20 (왼쪽 결합):

- `+`는 정수 덧셈
- `-`는 정수 뺄셈
- `|`는 비트 단위 OR
- `^`는 비트 단위 XOR

우선순위 17 (왼쪽 결합):

- `<<`는 비트 단위 왼쪽 시프트
- `>>`는 비트 단위 오른쪽 시프트
- `~>>`는 비트 단위 오른쪽 시프트 (반올림)
- `^>>`는 비트 단위 오른쪽 시프트 (올림)

우선순위 15 (왼쪽 결합):

- `==`는 정수 동등성 검사
- `!=`는 정수 불동등성 검사
- `<`는 정수 비교
- `<=`는 정수 비교
- `>`는 정수 비교
- `>=`는 정수 비교
- `<=>`는 정수 비교 (-1, 0 또는 1 반환)

이들도 인수와 분리되어야 합니다:

- `x + y`는 정상입니다
- `x+y`는 정상이 아닙니다 (단일 식별자입니다)

#### 조건 연산자

일반적인 구문을 가집니다.

```func
<condition> ? <consequence> : <alternative>
```

예시:

```func
x > 0 ? x * fac(x - 1) : 1;
```

우선순위는 13입니다.

#### 할당

우선순위 10.

단순 할당 `=`과 이항 연산의 대응: `+=`, `-=`, `*=`, `/=`, `~/=`, `^/=`, `%=`, `~%=`, `^%=`, `<<=`, `>>=`, `~>>=`, `^>>=`, `&=`, `|=`, `^=`.

## 반복문

FunC는 `repeat`, `while`, `do { ... } until` 반복문을 지원합니다. `for` 반복문은 지원되지 않습니다.

### Repeat 반복문

구문은 `repeat` 키워드 뒤에 `int` 타입의 표현식이 따라옵니다. 지정된 횟수만큼 코드를 반복합니다. 예시:

```func
int x = 1;
repeat(10) {
  x *= 2;
}
;; x = 1024
```

```func
int x = 1, y = 10;
repeat(y + 6) {
  x *= 2;
}
;; x = 65536
```

```func
int x = 1;
repeat(-1) {
  x *= 2;
}
;; x = 1
```

반복 횟수가 `-2^31` 미만이거나 `2^31 - 1`보다 크면 범위 검사 예외가 발생합니다.

### While 반복문

일반적인 구문을 가집니다. 예시:

```func
int x = 2;
while (x < 100) {
  x = x * x;
}
;; x = 256
```

조건 `x < 100`의 진리값이 `int` 타입이라는 점에 주목하세요 (참조: [불리언 타입의 부재](/v3/documentation/smart-contracts/func/docs/types#absence-of-boolean-type)).

### Until 반복문

다음과 같은 구문을 가집니다:

```func
int x = 0;
do {
  x += 3;
} until (x % 17 == 0);
;; x = 51
```

## If 구문

예시:

```func
;; usual if
if (flag) {
  do_something();
}
```

```func
;; equivalent to if (~ flag)
ifnot (flag) {
  do_something();
}
```

```func
;; usual if-else
if (flag) {
  do_something();
}
else {
  do_alternative();
}
```

```func
;; Some specific features
if (flag1) {
  do_something1();
} else {
  do_alternative4();
}
```

중괄호는 필수입니다. 다음 코드는 컴파일되지 않을 것입니다:

```func
if (flag1)
  do_something();
```

## Try-Catch 구문

*func v0.4.0부터 사용 가능*

`try` 블록의 코드를 실행합니다. 실패하면, `try` 블록에서 이루어진 변경사항을 완전히 롤백하고 대신 `catch` 블록을 실행합니다; `catch`는 두 개의 인수를 받습니다: 임의의 타입의 예외 매개변수(`x`)와 에러 코드(`n`, 정수).

다른 많은 언어의 try-catch 구문과 달리 FunC의 try-catch 구문에서는, try 블록에서 이루어진 변경사항, 특히 지역 및 전역 변수의 수정, 모든 레지스터의 변경사항(즉, `c4` 저장소 레지스터, `c5` 액션/메시지 레지스터, `c7` 컨텍스트 레지스터 및 기타)이 try 블록에서 오류가 발생하면 **폐기**되며 결과적으로 모든 컨트랙트 저장소 업데이트와 메시지 전송이 취소됩니다. *코드페이지* 및 가스 카운터와 같은 일부 TVM 상태 매개변수는 롤백되지 않는다는 점에 주목하는 것이 중요합니다. 이는 특히 try 블록에서 사용된 모든 가스가 계산되고 가스 제한을 변경하는 OP(`accept_message` 및 `set_gas_limit`)의 효과가 유지된다는 것을 의미합니다.

예외 매개변수는 어떤 타입이든(다른 예외의 경우 다를 수 있음) 될 수 있으므로 funC는 컴파일 시에 이를 예측할 수 없다는 점에 주목하세요. 이는 개발자가 예외 매개변수를 어떤 타입으로 캐스팅하여 컴파일러를 "도와야" 한다는 것을 의미합니다(아래의 예시 2 참조):

예시:

```func
try {
  do_something();
} catch (x, n) {
  handle_exception();
}
```

```func
forall X -> int cast_to_int(X x) asm "NOP";
...
try {
  throw_arg(-1, 100);
} catch (x, n) {
  x.cast_to_int();
  ;; x = -1, n = 100
  return x + 1;
}
```

```func
int x = 0;
try {
  x += 1;
  throw(100);
} catch (_, _) {
}
;; x = 0 (not 1)
```

## 블록 구문

블록 구문도 허용됩니다. 새로운 중첩된 범위를 엽니다:

```func
int x = 1;
builder b = begin_cell();
{
  builder x = begin_cell().store_uint(0, 8);
  b = x;
}
x += 1;
```
