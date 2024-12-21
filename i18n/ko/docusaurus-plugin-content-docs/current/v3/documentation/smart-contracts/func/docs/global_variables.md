# 전역 변수

FunC 프로그램은 본질적으로 함수 선언/정의와 전역 변수 선언의 목록입니다. 이 섹션에서는 두 번째 주제를 다룹니다.

전역 변수는 `global` 키워드 뒤에 변수 타입과 변수 이름을 붙여 선언할 수 있습니다. 예를 들어,

```func
global ((int, int) -> int) op;

int check_assoc(int a, int b, int c) {
  return op(op(a, b), c) == op(a, op(b, c));
}

int main() {
  op = _+_;
  return check_assoc(2, 3, 9);
}
```

이는 전역 함수형 변수 `op`에 덧셈 연산자 `_+_`를 쓰고 세 개의 샘플 정수 2, 3, 9에 대해 덧셈의 결합법칙을 확인하는 간단한 프로그램입니다.

내부적으로, 전역 변수들은 TVM의 c7 제어 레지스터에 저장됩니다.

전역 변수의 타입은 생략될 수 있습니다. 이 경우, 변수의 사용으로부터 타입이 추론될 것입니다. 예를 들어, 위 프로그램을 다음과 같이 다시 작성할 수 있습니다:

```func
global op;

int check_assoc(int a, int b, int c) {
  return op(op(a, b), c) == op(a, op(b, c));
}

int main() {
  op = _+_;
  return check_assoc(2, 3, 9);
}
```

동일한 `global` 키워드 뒤에 여러 변수를 선언하는 것이 가능합니다. 다음 코드들은 동등합니다:

```func
global int A;
global cell B;
global C;
```

```func
global int A, cell B, C;
```

이미 선언된 전역 변수와 동일한 이름으로 지역 변수를 선언하는 것은 허용되지 않습니다. 예를 들어, 이 코드는 컴파일되지 않을 것입니다:

```func
global cell C;

int main() {
  int C = 3;
  return C;
}
```

다음 코드는 올바르다는 점에 주목하세요:

```func
global int C;

int main() {
  int C = 3;
  return C;
}
```

하지만 여기서 `int C = 3;`은 `C = 3;`과 동등합니다. 즉, 이는 지역 변수 `C`의 선언이 아니라 전역 변수 `C`에 대한 할당입니다 (이 효과에 대한 설명은 [statements](/v3/documentation/smart-contracts/func/docs/statements#variable-declaration)에서 찾을 수 있습니다).
