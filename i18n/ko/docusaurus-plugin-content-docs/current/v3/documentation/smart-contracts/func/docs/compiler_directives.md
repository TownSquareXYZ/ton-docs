# 컴파일러 지시자

`#`으로 시작하는 키워드로, 컴파일러에게 특정 작업, 검사 또는 매개변수 변경을 지시합니다.

이러한 지시자는 가장 바깥 수준(함수 정의 내부가 아닌)에서만 사용할 수 있습니다.

## #include

`#include` 지시자는 다른 FunC 소스 코드 파일을 포함시킬 수 있게 합니다.

구문은 `#include "filename.fc";`입니다. 파일은 재포함에 대해 자동으로 검사되며, 한 파일을 두 번 이상 포함하려는 시도는 기본적으로 무시되고 상세도가 2 이상인 경우 경고가 표시됩니다.

포함된 파일 파싱 중 오류가 발생하면 각 포함 파일의 위치와 함께 포함 스택이 출력됩니다.

## #pragma

`#pragma` 지시자는 언어 자체가 전달하는 것 이상의 추가 정보를 컴파일러에 제공하는 데 사용됩니다.

### #pragma version

버전 pragma는 파일 컴파일 시 특정 FunC 컴파일러 버전을 강제하는 데 사용됩니다.

버전은 semver 형식(*a.b.c*)으로 지정되며, _a_는 주 버전, _b_는 부 버전, _c_는 패치 버전입니다.

개발자가 사용할 수 있는 비교 연산자:

- *a.b.c* 또는 *=a.b.c*—정확히 *a.b.c* 버전의 컴파일러 필요
- *>a.b.c*—컴파일러 버전이 _a.b.c_보다 높아야 함
  - *>=a.b.c*—컴파일러 버전이 *a.b.c* 이상이어야 함
- *\<a.b.c*—컴파일러 버전이 _a.b.c_보다 낮아야 함
  - *\<=a.b.c*—컴파일러 버전이 *a.b.c* 이하여야 함
- *^a.b.c*—주 컴파일러 버전이 'a'와 같고 부 버전이 'b' 이상이어야 함
  - *^a.b*—주 컴파일러 버전이 _a_와 같고 부 버전이 *b* 이상이어야 함
  - *^a*—주 컴파일러 버전이 *a* 이상이어야 함

다른 비교 연산자(*=*, *>*, *>=*, *\<*, *\<=*)의 경우 생략된 부분에 0을 가정합니다:

- _>a.b_는 _>a.b.0_와 같음(따라서 *a.b.0* 버전과 일치하지 않음)
- _\<=a_는 _\<=a.0.0_와 같음(따라서 *a.0.1* 버전과 일치하지 않음)
- _^a.b.0_는 _^a.b_와 **같지 않음**

예를 들어, _^a.1.2_는 _a.1.3_과 일치하지만 *a.2.3* 또는 _a.1.0_과는 일치하지 않습니다. 하지만 _^a.1_은 모두와 일치합니다.

이 지시자는 여러 번 사용할 수 있으며, 컴파일러 버전은 제공된 모든 조건을 만족해야 합니다.

### #pragma not-version

이 pragma의 구문은 버전 pragma와 같지만 조건이 만족되면 실패합니다.

예를 들어 문제가 있는 것으로 알려진 특정 버전을 블랙리스트에 올리는 데 사용할 수 있습니다.

### #pragma allow-post-modification

*funC v0.4.1*

기본적으로 같은 표현식에서 변수를 수정하기 전에 사용하는 것은 금지되어 있습니다. 즉, `(x, y) = (ds, ds~load_uint(8))` 표현식은 컴파일되지 않지만 `(x, y) = (ds~load_uint(8), ds)`는 유효합니다.

이 규칙은 `#pragma allow-post-modification`으로 재정의할 수 있으며, 이는 대량 할당과 함수 호출에서 사용 후 변수를 수정할 수 있게 합니다. 일반적으로 하위 표현식은 왼쪽에서 오른쪽으로 계산됩니다: `(x, y) = (ds, ds~load_bits(8))`에서 `x`는 초기 `ds`를 포함하게 되고, `f(ds, ds~load_bits(8))`에서 `f`의 첫 번째 인수는 초기 `ds`를 포함하고 두 번째는 `ds`의 8비트를 포함합니다.

`#pragma allow-post-modification`은 pragma 이후의 코드에만 적용됩니다.

### #pragma compute-asm-ltr

*funC v0.4.1*

Asm 선언은 인수의 순서를 재정의할 수 있습니다. 예를 들어 다음 표현식에서:

```func
idict_set_ref(ds~load_dict(), ds~load_uint(8), ds~load_uint(256), ds~load_ref())
```

다음 asm 선언 때문에 파싱 순서는 `load_ref()`, `load_uint(256)`, `load_dict()`, `load_uint(8)`가 됩니다(`asm(value index dict key_len)` 참고):

```func
cell idict_set_ref(cell dict, int key_len, int index, cell value) asm(value index dict key_len) "DICTISETREF";
```

이 동작은 `#pragma compute-asm-ltr`를 통해 엄격한 왼쪽에서 오른쪽 계산 순서로 변경할 수 있습니다.

결과적으로:

```func
#pragma compute-asm-ltr
...
idict_set_ref(ds~load_dict(), ds~load_uint(8), ds~load_uint(256), ds~load_ref());
```

파싱 순서는 `load_dict()`, `load_uint(8)`, `load_uint(256)`, `load_ref()`가 되고 모든 asm 순열은 계산 후에 발생합니다.

`#pragma compute-asm-ltr`은 pragma 이후의 코드에만 적용됩니다.
