# 톤클리 사용

:::tip 시작 팁
톤클리를 사용해 본 적이 없다면 [빠른 시작 가이드](https://github.com/disintar/toncli/blob/master/docs/quick_start_guide.md)를 참조하세요.
:::

## 톤클리를 사용한 테스트

톤클리\`는 FunC를 사용해 스마트 컨트랙트를 테스트합니다. 또한 최신 버전은 빠른 환경 설정을 위해 도커를 지원합니다.

이 튜토리얼은 스마트 컨트랙트의 기능을 테스트하여 프로젝트가 올바르게 작동하는지 확인하는 데 도움이 됩니다.

톤클리를 사용한 테스트를 설명하는 가장 좋은 튜토리얼은 다음과 같습니다:

- [FunC 테스트는 어떻게 진행되나요?(https://github.com/disintar/toncli/blob/master/docs/advanced/func_tests_new.md)
- [톤클리로 트랜잭션을 디버깅하는 방법](https://github.com/disintar/toncli/blob/master/docs/advanced/transaction_debug.md)

## 톤클리의 FunC 테스트 구조

스마트 컨트랙트를 테스트하려면 두 가지 함수를 작성해야 합니다. 그 중 하나는 값을 받고 원하는 결과를 포함하며 테스트 중인 함수가 올바르게 작동하지 않으면 오류를 반환합니다.

### 테스트가 포함된 파일을 만들어 보겠습니다.

tests`폴더에 테스트를 작성할 파일`example.func\`를 만듭니다.

### 데이터 함수

일반적으로 테스트 함수는 인수를 허용하지 않지만 반드시 인수를 반환해야 합니다.

- **함수 선택자** - 테스트된 컨트랙트에서 호출된 함수의 ID입니다;
- **튜플** - 테스트를 수행하는 함수에 전달할 (스택) 값입니다;
- **C4 셀** - 제어 레지스터 C4의 "영구 데이터";
- **C7 튜플** - 제어 레지스터 C7의 "임시 데이터";
- **가스 제한 정수** - 가스 제한(가스 개념을 이해하려면 먼저 이더리움에서 가스 제한에 대해 읽어보시기 바랍니다);

:::info 가스 정보

자세한 내용은 [여기](https://ton-blockchain.github.io/docs/#/smart-contracts/fees)에서 확인할 수 있습니다. 자세한 내용은 [부록 A](https://ton-blockchain.github.io/docs/tvm.pdf)에서 확인할 수 있습니다.

1.3.1의 레지스터 c4 및 c7에 대한 자세한 내용은 [여기](https://ton-blockchain.github.io/docs/tvm.pdf)
:::

## 스마트 컨트랙트에 대한 테스트 작성을 시작해 보겠습니다.

### 소개

새로운 테스트에서는 스마트 컨트랙트 메서드를 호출할 수 있는 두 가지 함수를 통해 테스트가 진행됩니다:

- 예외가 발생하지 않는다고 가정하는 `invoke_method`를 호출합니다.
- 예외가 발생한다고 가정하는 `invoke_method_expect_fail`을 호출합니다.

테스트 함수 내부에 있는 함수로, 원하는 수의 값을 반환할 수 있으며 테스트가 실행될 때 보고서에서 모두 표시됩니다.

:::info 중요!
각 테스트 함수 이름은 `_test`로 시작해야 한다는 점에 유의할 필요가 있습니다.
:::

### 테스트 함수 만들기

테스트 함수 `__test_example()`을 호출하면 소비된 가스의 양을 반환하므로 `int`가 됩니다.

```js
int __test_example() {

}
```

### 등록 업데이트 C4

많은 수의 테스트로 인해 `c4` 레지스터를 자주 업데이트해야 하므로 `c4`를 0으로 쓰는 도우미 함수를 만들겠습니다.

```js
() set_default_initial_data() impure {
  set_data(begin_cell().store_uint(0, 64).end_cell());
}
```

- `begin_cell()` - 향후 셀에 대한 빌더를 생성합니다.
- `store_uint()` - 합계 값을 씁니다.
- end_cell()\`- 셀 생성
- `set_data()` - 셀을 기록하여 c4를 등록합니다.

'impure'는 함수가 스마트 컨트랙트 데이터를 변경한다는 것을 나타내는 키워드입니다.

테스트 함수 본문에서 사용할 함수가 있습니다.

**결과:**

```js
int __test_example() {
	set_default_initial_data();

}
```

### 테스트 방법

새 버전의 테스트에서는 테스트 기능에서 여러 스마트 컨트랙트 메서드를 호출할 수 있다는 점에 주목할 필요가 있습니다.

테스트에서는 `recv_internal()` 메서드와 Get 메서드를 호출하여 메시지로 c4의 값을 증가시키고 전송된 값으로 변경되었는지 즉시 확인합니다.

recv_internal()\` 메서드를 호출하려면 메시지가 있는 셀을 만들어야 합니다.

```js
int __test_example() {
	set_default_initial_data();
	cell message = begin_cell().store_uint(10, 32).end_cell();
}
```

이 단계가 끝나면 `invoke_method` 메서드를 사용하겠습니다.

이 메서드에는 두 개의 인수가 필요합니다:

- 메서드 이름
- 인수를 '튜플'로 테스트합니다.

사용된 가스와 메서드가 반환한 값(튜플)의 두 가지 값이 반환됩니다.

:::info 주목할 만한 점은 다음과 같습니다.
사용된 가스와 메서드가 반환한 값(튜플)의 두 가지 값이 반환됩니다.
:::

첫 번째 호출에서 인수는 `recv_internal`과 `begin_parse()`를 사용하여 슬라이스로 변환된 메시지가 있는 튜플이 됩니다.

```js
var (int gas_used1, _) = invoke_method(recv_internal, [message.begin_parse()]);
```

참고로, 사용된 가스의 양을 int `gas_used1`에 저장해 보겠습니다.

두 번째 호출에서 인수는 Get 메서드 `get_total()`과 빈 튜플이 됩니다.

```js
var (int gas_used2, stack) = invoke_method(get_total, []);
```

보고서의 경우, 나중에 모든 것이 올바르게 작동했는지 확인하기 위해 `int gas_used2`에 사용된 가스 양과 메서드가 반환하는 값도 저장합니다.

이해합니다:

```js
int __test_example() {
	set_default_initial_data();

	cell message = begin_cell().store_uint(10, 32).end_cell();
	var (int gas_used1, _) = invoke_method(recv_internal, [message.begin_parse()]);
	var (int gas_used2, stack) = invoke_method(get_total, []);

}
```

이제 마지막으로 가장 중요한 단계입니다. 스마트 컨트랙트가 제대로 작동하는지 확인해야 합니다.

즉, **정확한 결과**를 반환하면 `성공` 또는 `실패`와 함께 사용된 가스를 반환합니다.

```js
[int total] = stack; 
throw_if(101, total != 10); 
```

**설명:**

- 튜플 전달
- 첫 번째 인수는 스마트 컨트랙트가 올바르게 작동하지 않을 경우 받게 될 오류의 수(101)입니다.
- 두 번째 인수는 정답입니다.

```js
int __test_example() {
	set_data(begin_cell().store_uint(0, 64).end_cell());
	cell message = begin_cell().store_uint(10, 32).end_cell();
	var (int gas_used1, _) = invoke_method(recv_internal, [message.begin_parse()]);
	var (int gas_used2, stack) = invoke_method(get_total, []);
	[int total] = stack;
	throw_if(101, total != 10);
	return gas_used1 + gas_used2;
}
```

이것은 전체 테스트이며 매우 편리합니다.
