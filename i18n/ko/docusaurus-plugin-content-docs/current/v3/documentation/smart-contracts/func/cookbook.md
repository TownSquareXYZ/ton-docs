# FunC Cookbook

FunC Cookbook를 만든 핵심 이유는 FunC 개발자들의 모든 경험을 한 곳에 모아 미래의 개발자들이 이를 활용할 수 있도록 하기 위함입니다!

[FunC Documentation](/v3/documentation/smart-contracts/func/docs/types)과 비교했을 때, 이 문서는 FunC 개발자들이 스마트 컨트랙트 개발 중에 매일 해결하는 일상적인 작업에 더 초점을 맞추고 있습니다.

## 기초

### if 문을 작성하는 방법

이벤트가 관련이 있는지 확인하고 싶다고 가정해봅시다. 이를 위해 플래그 변수를 사용합니다. FunC에서 `true`는 `-1`이고 `false`는 `0`임을 기억하세요.

```func
int flag = 0; ;; false

if (flag) { 
    ;; do something
}
else {
    ;; reject the transaction
}
```

> 💡 참고
>
> `0`이 `false`이므로 다른 모든 값은 `true`가 되기 때문에 `==` 연산자가 필요하지 않습니다.

> 💡 유용한 링크
>
> [문서의 "If statement"](/v3/documentation/smart-contracts/func/docs/statements#if-statements)

### repeat 루프를 작성하는 방법

예시로 거듭제곱을 살펴보겠습니다.

```func
int number = 2;
int multiplier = number;
int degree = 5;

repeat(degree - 1) {

    number *= multiplier;
}
```

> 💡 유용한 링크
>
> [문서의 "Repeat loop"](/v3/documentation/smart-contracts/func/docs/statements#repeat-loop)

### while 루프를 작성하는 방법

while은 특정 작업을 얼마나 자주 수행해야 하는지 모를 때 유용합니다. 예를 들어, 최대 4개의 다른 셀에 대한 참조를 저장할 수 있다고 알려진 `cell`을 살펴보겠습니다.

```func
cell inner_cell = begin_cell() ;; create a new empty builder
        .store_uint(123, 16) ;; store uint with value 123 and length 16 bits
        .end_cell(); ;; convert builder to a cell

cell message = begin_cell()
        .store_ref(inner_cell) ;; store cell as reference
        .store_ref(inner_cell)
        .end_cell();

slice msg = message.begin_parse(); ;; convert cell to slice
while (msg.slice_refs_empty?() != -1) { ;; we should remind that -1 is true
    cell inner_cell = msg~load_ref(); ;; load cell from slice msg
    ;; do something
}
```

> 💡 유용한 링크
>
> [문서의 "While loop"](/v3/documentation/smart-contracts/func/docs/statements#while-loop)
>
> [문서의 "Cell"](/v3/concepts/dive-into-ton/ton-blockchain/cells-as-data-storage)
>
> [문서의 "slice_refs_empty?()"](/v3/documentation/smart-contracts/func/docs/stdlib#slice_refs_empty)
>
> [문서의 "store_ref()"](/v3/documentation/smart-contracts/func/docs/stdlib#store_ref)
>
> [문서의 "begin_cell()"](/v3/documentation/smart-contracts/func/docs/stdlib#begin_cell)
>
> [문서의 "end_cell()"](/v3/documentation/smart-contracts/func/docs/stdlib#end_cell)
>
> [문서의 "begin_parse()"](/v3/documentation/smart-contracts/func/docs/stdlib#begin_parse)

### do until 루프를 작성하는 방법

사이클이 최소한 한 번은 실행되어야 할 때 `do until`을 사용합니다.

```func
int flag = 0;

do {
    ;; do something even flag is false (0) 
} until (flag == -1); ;; -1 is true
```

> 💡 유용한 링크
>
> [문서의 "Until loop"](/v3/documentation/smart-contracts/func/docs/statements#until-loop)

### slice가 비어있는지 확인하는 방법

`slice`로 작업하기 전에, 올바른 처리를 위해 데이터가 있는지 확인해야 합니다. 이를 위해 `slice_empty?()`를 사용할 수 있지만, 최소 하나의 `bit` 데이터나 하나의 `ref`가 있다면 `0`(`false`)을 반환한다는 점을 고려해야 합니다.

```func
;; creating empty slice
slice empty_slice = "";
;; `slice_empty?()` returns `true`, because slice doesn't have any `bits` and `refs`
empty_slice.slice_empty?();

;; creating slice which contains bits only
slice slice_with_bits_only = "Hello, world!";
;; `slice_empty?()` returns `false`, because slice have any `bits`
slice_with_bits_only.slice_empty?();

;; creating slice which contains refs only
slice slice_with_refs_only = begin_cell()
    .store_ref(null())
    .end_cell()
    .begin_parse();
;; `slice_empty?()` returns `false`, because slice have any `refs`
slice_with_refs_only.slice_empty?();

;; creating slice which contains bits and refs
slice slice_with_bits_and_refs = begin_cell()
    .store_slice("Hello, world!")
    .store_ref(null())
    .end_cell()
    .begin_parse();
;; `slice_empty?()` returns `false`, because slice have any `bits` and `refs`
slice_with_bits_and_refs.slice_empty?();
```

> 💡 유용한 링크
>
> [문서의 "slice_empty?()"](/v3/documentation/smart-contracts/func/docs/stdlib#slice_empty)
>
> [문서의 "store_slice()"](/v3/documentation/smart-contracts/func/docs/stdlib#store_slice)
>
> [문서의 "store_ref()"](/v3/documentation/smart-contracts/func/docs/stdlib#store_ref)
>
> [문서의 "begin_cell()"](/v3/documentation/smart-contracts/func/docs/stdlib#begin_cell)
>
> [문서의 "end_cell()"](/v3/documentation/smart-contracts/func/docs/stdlib#end_cell)
>
> [문서의 "begin_parse()"](/v3/documentation/smart-contracts/func/docs/stdlib#begin_parse)

### slice가 비어있는지 확인하는 방법 (refs는 있을 수 있지만 bits는 없는 경우)

`slice`에서 `bits`만 확인하고 `refs`가 있는지는 중요하지 않다면, `slice_data_empty?()`를 사용해야 합니다.

```func
;; creating empty slice
slice empty_slice = "";
;; `slice_data_empty?()` returns `true`, because slice doesn't have any `bits`
empty_slice.slice_data_empty?();

;; creating slice which contains bits only
slice slice_with_bits_only = "Hello, world!";
;; `slice_data_empty?()` returns `false`, because slice have any `bits`
slice_with_bits_only.slice_data_empty?();

;; creating slice which contains refs only
slice slice_with_refs_only = begin_cell()
    .store_ref(null())
    .end_cell()
    .begin_parse();
;; `slice_data_empty?()` returns `true`, because slice doesn't have any `bits`
slice_with_refs_only.slice_data_empty?();

;; creating slice which contains bits and refs
slice slice_with_bits_and_refs = begin_cell()
    .store_slice("Hello, world!")
    .store_ref(null())
    .end_cell()
    .begin_parse();
;; `slice_data_empty?()` returns `false`, because slice have any `bits`
slice_with_bits_and_refs.slice_data_empty?();
```

> 💡 유용한 링크
>
> [문서의 "slice_data_empty?()"](/v3/documentation/smart-contracts/func/docs/stdlib#slice_data_empty)
>
> [문서의 "store_slice()"](/v3/documentation/smart-contracts/func/docs/stdlib#store_slice)
>
> [문서의 "store_ref()"](/v3/documentation/smart-contracts/func/docs/stdlib#store_ref)
>
> [문서의 "begin_cell()"](/v3/documentation/smart-contracts/func/docs/stdlib#begin_cell)
>
> [문서의 "end_cell()"](/v3/documentation/smart-contracts/func/docs/stdlib#end_cell)
>
> [문서의 "begin_parse()"](/v3/documentation/smart-contracts/func/docs/stdlib#begin_parse)

### slice가 비어있는지 확인하는 방법 (bits는 있을 수 있지만 refs는 없는 경우)

`refs`만 관심이 있다면, `slice_refs_empty?()`를 사용하여 존재 여부를 확인해야 합니다.

```func
;; creating empty slice
slice empty_slice = "";
;; `slice_refs_empty?()` returns `true`, because slice doesn't have any `refs`
empty_slice.slice_refs_empty?();

;; creating slice which contains bits only
slice slice_with_bits_only = "Hello, world!";
;; `slice_refs_empty?()` returns `true`, because slice doesn't have any `refs`
slice_with_bits_only.slice_refs_empty?();

;; creating slice which contains refs only
slice slice_with_refs_only = begin_cell()
    .store_ref(null())
    .end_cell()
    .begin_parse();
;; `slice_refs_empty?()` returns `false`, because slice have any `refs`
slice_with_refs_only.slice_refs_empty?();

;; creating slice which contains bits and refs
slice slice_with_bits_and_refs = begin_cell()
    .store_slice("Hello, world!")
    .store_ref(null())
    .end_cell()
    .begin_parse();
;; `slice_refs_empty?()` returns `false`, because slice have any `refs`
slice_with_bits_and_refs.slice_refs_empty?();
```

> 💡 유용한 링크
>
> [문서의 "slice_refs_empty?()"](/v3/documentation/smart-contracts/func/docs/stdlib#slice_refs_empty)
>
> [문서의 "store_slice()"](/v3/documentation/smart-contracts/func/docs/stdlib#store_slice)
>
> [문서의 "store_ref()"](/v3/documentation/smart-contracts/func/docs/stdlib#store_ref)
>
> [문서의 "begin_cell()"](/v3/documentation/smart-contracts/func/docs/stdlib#begin_cell)
>
> [문서의 "end_cell()"](/v3/documentation/smart-contracts/func/docs/stdlib#end_cell)
>
> [문서의 "begin_parse()"](/v3/documentation/smart-contracts/func/docs/stdlib#begin_parse)

### cell이 비어있는지 확인하는 방법

`cell`에 데이터가 있는지 확인하려면 먼저 `slice`로 변환해야 합니다. `bits`만 관심이 있다면 `slice_data_empty?()`, `refs`만 관심이 있다면 `slice_refs_empty?()`를 사용해야 합니다. `bit`나 `ref` 여부와 관계없이 데이터 존재 여부를 확인하려면 `slice_empty?()`를 사용해야 합니다.

```func
cell cell_with_bits_and_refs = begin_cell()
    .store_uint(1337, 16)
    .store_ref(null())
    .end_cell();

;; Change `cell` type to slice with `begin_parse()`
slice cs = cell_with_bits_and_refs.begin_parse();

;; determine if slice is empty
if (cs.slice_empty?()) {
    ;; cell is empty
}
else {
    ;; cell is not empty
}
```

> 💡 유용한 링크
>
> [문서의 "slice_empty?()"](/v3/documentation/smart-contracts/func/docs/stdlib#slice_empty)
>
> [문서의 "begin_cell()"](/v3/documentation/smart-contracts/func/docs/stdlib#begin_cell)
>
> [문서의 "store_uint()"](/v3/documentation/smart-contracts/func/docs/stdlib#store_uint)
>
> [문서의 "end_cell()"](/v3/documentation/smart-contracts/func/docs/stdlib#end_cell)
>
> [문서의 "begin_parse()"](/v3/documentation/smart-contracts/func/docs/stdlib#begin_parse)

### dict가 비어있는지 확인하는 방법

dict에 데이터가 있는지 확인하기 위한 `dict_empty?()` 메서드가 있습니다. 이 메서드는 보통 `null`-cell이 빈 딕셔너리이기 때문에 `cell_null?()`와 동일합니다.

```func
cell d = new_dict();
d~udict_set(256, 0, "hello");
d~udict_set(256, 1, "world");

if (d.dict_empty?()) { ;; Determine if dict is empty
    ;; dict is empty
}
else {
    ;; dict is not empty
}
```

> 💡 유용한 링크
>
> [문서의 "dict_empty?()"](/v3/documentation/smart-contracts/func/docs/stdlib#dict_empty)
>
> [문서의 "new_dict()"](/v3/documentation/smart-contracts/func/docs/stdlib/#new_dict) - 빈 dict 생성
>
> [문서의 "dict_set()"](/v3/documentation/smart-contracts/func/docs/stdlib/#dict_set) - dict d에 함수로 요소를 추가하여 비어있지 않게 함

### tuple이 비어있는지 확인하는 방법

`tuple`로 작업할 때는 추출할 값이 있는지 항상 알아야 합니다. 빈 `tuple`에서 값을 추출하려고 하면 "not a tuple of valid size"라는 `exit code 7` 오류가 발생합니다.

```func
;; Declare tlen function because it's not presented in stdlib
(int) tlen (tuple t) asm "TLEN";

() main () {
    tuple t = empty_tuple();
    t~tpush(13);
    t~tpush(37);

    if (t.tlen() == 0) {
        ;; tuple is empty
    }
    else {
        ;; tuple is not empty
    }
}
```

> 💡 참고
>
> tlen 어셈블리 함수를 선언하고 있습니다. 자세한 내용은 [여기](/v3/documentation/smart-contracts/func/docs/functions#assembler-function-body-definition)에서, [모든 어셈블러 명령어 목록](/v3/documentation/tvm/instructions)은 여기서 확인할 수 있습니다.

> 💡 유용한 링크
>
> [문서의 "empty_tuple?()"](/v3/documentation/smart-contracts/func/docs/stdlib#empty_tuple)
>
> [문서의 "tpush()"](/v3/documentation/smart-contracts/func/docs/stdlib/#tpush)
>
> [문서의 "Exit codes"](/v3/documentation/tvm/tvm-exit-codes)

### lisp-style 리스트가 비어있는지 확인하는 방법

```func
tuple numbers = null();
numbers = cons(100, numbers);

if (numbers.null?()) {
    ;; list-style list is empty
} else {
    ;; list-style list is not empty
}
```

[cons](/v3/documentation/smart-contracts/func/docs/stdlib/#cons) 함수를 사용하여 숫자 100을 리스트 스타일 리스트에 추가하므로 비어있지 않습니다.

### 스마트 컨트랙트의 상태가 비어있는지 확인하는 방법

거래 횟수를 저장하는 `counter`가 있다고 가정해보겠습니다. 이 변수는 상태가 비어있기 때문에 스마트 컨트랙트의 첫 번째 거래 동안에는 사용할 수 없으므로, 이러한 경우를 처리해야 합니다. 상태가 비어있다면, `counter` 변수를 생성하고 저장합니다.

```func
;; `get_data()` will return the data cell from contract state
cell contract_data = get_data();
slice cs = contract_data.begin_parse();

if (cs.slice_empty?()) {
    ;; contract data is empty, so we create counter and save it
    int counter = 1;
    ;; create cell, add counter and save in contract state
    set_data(begin_cell().store_uint(counter, 32).end_cell());
}
else {
    ;; contract data is not empty, so we get our counter, increase it and save
    ;; we should specify correct length of our counter in bits
    int counter = cs~load_uint(32) + 1;
    set_data(begin_cell().store_uint(counter, 32).end_cell());
}
```

> 💡 참고
>
> [cell이 비어있는지 확인하는 방법](/v3/documentation/smart-contracts/func/cookbook#how-to-determine-if-cell-is-empty)을 통해 컨트랙트의 상태가 비어있는지 확인할 수 있습니다.

> 💡 유용한 링크
>
> [문서의 "get_data()"](/v3/documentation/smart-contracts/func/docs/stdlib#get_data)
>
> [문서의 "begin_parse()"](/v3/documentation/smart-contracts/func/docs/stdlib/#begin_parse)
>
> [문서의 "slice_empty?()"](/v3/documentation/smart-contracts/func/docs/stdlib/#slice_empty)
>
> [문서의 "set_data?()"](/v3/documentation/smart-contracts/func/docs/stdlib#set_data)

### 내부 메시지 cell을 구성하는 방법

컨트랙트가 내부 메시지를 보내도록 하려면, 먼저 기술적인 플래그, 수신자 주소, 나머지 데이터를 지정하여 `cell`로 적절하게 생성해야 합니다.

```func
;; We use literal `a` to get valid address inside slice from string containing address 
slice addr = "EQArzP5prfRJtDM5WrMNWyr9yUTAi0c9o6PfR4hkWy9UQXHx"a;
int amount = 1000000000;
;; we use `op` for identifying operations
int op = 0;

cell msg = begin_cell()
    .store_uint(0x18, 6)
    .store_slice(addr)
    .store_coins(amount)
    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; default message headers (see sending messages page)
    .store_uint(op, 32)
.end_cell();

send_raw_message(msg, 3); ;; mode 3 - pay fees separately and ignore errors 
```

> 💡 참고
>
> 이 예시에서는 리터럴 `a`를 사용하여 주소를 가져옵니다. 문자열 리터럴에 대해 자세히 알아보려면 [문서](/v3/documentation/smart-contracts/func/docs/literals_identifiers#string-literals)를 참조하세요.

> 💡 참고
>
> 자세한 내용은 [문서](/v3/documentation/smart-contracts/message-management/sending-messages)에서 확인할 수 있습니다. 또한 이 링크로 [레이아웃](/v3/documentation/smart-contracts/message-management/sending-messages#message-layout)으로 이동할 수 있습니다.

> 💡 유용한 링크
>
> [문서의 "begin_cell()"](/v3/documentation/smart-contracts/func/docs/stdlib#begin_cell)
>
> [문서의 "store_uint()"](/v3/documentation/smart-contracts/func/docs/stdlib#store_uint)
>
> [문서의 "store_slice()"](/v3/documentation/smart-contracts/func/docs/stdlib#store_slice)
>
> [문서의 "store_coins()"](/v3/documentation/smart-contracts/func/docs/stdlib#store_coins)
>
> [문서의 "end_cell()"](/v3/documentation/smart-contracts/func/docs/stdlib/#end_cell)
>
> [문서의 "send_raw_message()"](/v3/documentation/smart-contracts/func/docs/stdlib/#send_raw_message)

### 내부 메시지 cell에 ref로 본문을 포함하는 방법

플래그와 다른 기술적 데이터 다음에 오는 메시지 본문에서 `int`, `slice`, `cell`을 보낼 수 있습니다. 후자의 경우, `cell`이 계속될 것임을 나타내기 위해 `store_ref()` 전에 비트를 `1`로 설정해야 합니다.

충분한 공간이 있다고 확신한다면 메시지 본문을 헤더와 같은 `cell` 내에 보낼 수도 있습니다. 이 경우 비트를 `0`으로 설정해야 합니다.

```func
;; We use literal `a` to get valid address inside slice from string containing address 
slice addr = "EQArzP5prfRJtDM5WrMNWyr9yUTAi0c9o6PfR4hkWy9UQXHx"a;
int amount = 1000000000;
int op = 0;
cell message_body = begin_cell() ;; Creating a cell with message
    .store_uint(op, 32)
    .store_slice("❤")
.end_cell();
    
cell msg = begin_cell()
    .store_uint(0x18, 6)
    .store_slice(addr)
    .store_coins(amount)
    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1) ;; default message headers (see sending messages page)
    .store_uint(1, 1) ;; set bit to 1 to indicate that the cell will go on
    .store_ref(message_body)
.end_cell();

send_raw_message(msg, 3); ;; mode 3 - pay fees separately and ignore errors 
```

> 💡 참고
>
> 이 예시에서는 리터럴 `a`를 사용하여 주소를 가져옵니다. 문자열 리터럴에 대해 자세히 알아보려면 [문서](/v3/documentation/smart-contracts/func/docs/literals_identifiers#string-literals)를 참조하세요.

> 💡 참고
>
> 이 예시에서는 mode 3을 사용하여 수신된 ton을 가져와서 지정된 만큼(amount) 정확히 보내면서 수수료는 컨트랙트 잔액에서 지불하고 오류를 무시합니다. Mode 64는 수수료를 제외한 모든 ton을 반환하는 데 필요하고, mode 128은 전체 잔액을 보냅니다.

> 💡 참고
>
> [메시지를 구성](/v3/documentation/smart-contracts/func/cookbook#how-to-build-an-internal-message-cell)하고 있지만 메시지 본문은 별도로 추가합니다.

> 💡 유용한 링크
>
> [문서의 "begin_cell()"](/v3/documentation/smart-contracts/func/docs/stdlib#begin_cell)
>
> [문서의 "store_uint()"](/v3/documentation/smart-contracts/func/docs/stdlib#store_uint)
>
> [문서의 "store_slice()"](/v3/documentation/smart-contracts/func/docs/stdlib#store_slice)
>
> [문서의 "store_coins()"](/v3/documentation/smart-contracts/func/docs/stdlib#store_coins)
>
> [문서의 "end_cell()"](/v3/documentation/smart-contracts/func/docs/stdlib/#end_cell)
>
> [문서의 "send_raw_message()"](/v3/documentation/smart-contracts/func/docs/stdlib/#send_raw_message)

### 내부 메시지 cell에 slice로 본문을 포함하는 방법

메시지를 보낼 때 메시지 본문을 `cell`이나 `slice`로 보낼 수 있습니다. 이 예시에서는 메시지 본문을 `slice` 내에 보냅니다.

```func
;; We use literal `a` to get valid address inside slice from string containing address 
slice addr = "EQArzP5prfRJtDM5WrMNWyr9yUTAi0c9o6PfR4hkWy9UQXHx"a;
int amount = 1000000000;
int op = 0;
slice message_body = "❤"; 

cell msg = begin_cell()
    .store_uint(0x18, 6)
    .store_slice(addr)
    .store_coins(amount)
    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; default message headers (see sending messages page)
    .store_uint(op, 32)
    .store_slice(message_body)
.end_cell();

send_raw_message(msg, 3); ;; mode 3 - pay fees separately and ignore errors 
```

> 💡 참고
>
> 이 예시에서는 리터럴 `a`를 사용하여 주소를 가져옵니다. 문자열 리터럴에 대해 자세히 알아보려면 [문서](/v3/documentation/smart-contracts/func/docs/literals_identifiers#string-literals)를 참조하세요.

> 💡 참고
>
> 이 예시에서는 mode 3을 사용하여 수신된 ton을 가져와서 지정된 만큼(amount) 정확히 보내면서 수수료는 컨트랙트 잔액에서 지불하고 오류를 무시합니다. Mode 64는 수수료를 제외한 모든 ton을 반환하는 데 필요하고, mode 128은 전체 잔액을 보냅니다.

> 💡 참고
>
> [메시지를 구성](/v3/documentation/smart-contracts/func/cookbook#how-to-build-an-internal-message-cell)하고 있지만 메시지를 slice로 추가합니다.

### tuple을 순회하는 방법 (양방향)

FunC에서 배열이나 스택으로 작업하려면 tuple이 필요합니다. 그리고 무엇보다도 값들을 순회할 수 있어야 합니다.

```func
(int) tlen (tuple t) asm "TLEN";
forall X -> (tuple) to_tuple (X x) asm "NOP";

() main () {
    tuple t = to_tuple([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
    int len = t.tlen();
    
    int i = 0;
    while (i < len) {
        int x = t.at(i);
        ;; do something with x
        i = i + 1;
    }

    i = len - 1;
    while (i >= 0) {
        int x = t.at(i);
        ;; do something with x
        i = i - 1;
    }
}
```

> 💡 참고
>
> `tlen` 어셈블리 함수를 선언하고 있습니다. 자세한 내용은 [여기](/v3/documentation/smart-contracts/func/docs/functions#assembler-function-body-definition)에서, [모든 어셈블러 명령어 목록](/v3/documentation/tvm/instructions)은 여기서 확인할 수 있습니다.
>
> 또한 `to_tuple` 함수도 선언하고 있습니다. 이는 단순히 모든 입력의 데이터 타입을 tuple로 변경하므로 사용 시 주의해야 합니다.

### `asm` 키워드를 사용하여 자체 함수 작성하는 방법

모든 기능을 사용할 때 실제로는 `stdlib.fc` 내에 미리 준비된 메서드를 사용합니다. 하지만 실제로는 더 많은 기회가 있으며, 이를 직접 작성하는 방법을 배워야 합니다.

예를 들어, `tuple`에 요소를 추가하는 `tpush` 메서드는 있지만 `tpop`은 없습니다. 이 경우 다음과 같이 해야 합니다:

```func
;; ~ means it is modifying method
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP"; 
```

반복을 위해 `tuple`의 길이를 알고 싶다면 `TLEN` asm 명령어로 새 함수를 작성해야 합니다:

```func
int tuple_length (tuple t) asm "TLEN";
```

stdlib.fc에서 이미 알고 있는 함수들의 몇 가지 예시:

```func
slice begin_parse(cell c) asm "CTOS";
builder begin_cell() asm "NEWC";
cell end_cell(builder b) asm "ENDC";
```

> 💡 유용한 링크:
>
> [문서의 "modifying method"](/v3/documentation/smart-contracts/func/docs/statements#modifying-methods)
>
> [문서의 "stdlib"](/v3/documentation/smart-contracts/func/docs/stdlib)
>
> [문서의 "TVM instructions"](/v3/documentation/tvm/instructions)

### n중 중첩 tuple 순회하기

때로는 중첩된 tuple을 순회하고 싶을 수 있습니다. 다음 예시는 `[[2,6],[1,[3,[3,5]]], 3]` 형식의 tuple에서 헤드부터 시작하여 모든 항목을 순회하고 출력합니다.

```func
int tuple_length (tuple t) asm "TLEN";
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP";
forall X -> int is_tuple (X x) asm "ISTUPLE";
forall X -> tuple cast_to_tuple (X x) asm "NOP";
forall X -> int cast_to_int (X x) asm "NOP";
forall X -> (tuple) to_tuple (X x) asm "NOP";

;; define global variable
global int max_value;

() iterate_tuple (tuple t) impure {
    repeat (t.tuple_length()) {
        var value = t~tpop();
        if (is_tuple(value)) {
            tuple tuple_value = cast_to_tuple(value);
            iterate_tuple(tuple_value);
        }
        else {
            if(value > max_value) {
                max_value = value;
            }
        }
    }
}

() main () {
    tuple t = to_tuple([[2,6], [1, [3, [3, 5]]], 3]);
    int len = t.tuple_length();
    max_value = 0; ;; reset max_value;
    iterate_tuple(t); ;; iterate tuple and find max value
    ~dump(max_value); ;; 6
}
```

> 💡 유용한 링크
>
> [문서의 "Global variables"](/v3/documentation/smart-contracts/func/docs/global_variables)
>
> [문서의 "~dump"](/v3/documentation/smart-contracts/func/docs/builtins#dump-variable)
>
> [문서의 "TVM instructions"](/v3/documentation/tvm/instructions)

### tuple에서의 기본 연산

```func
(int) tlen (tuple t) asm "TLEN";
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP";

() main () {
    ;; creating an empty tuple
    tuple names = empty_tuple(); 
    
    ;; push new items
    names~tpush("Naito Narihira");
    names~tpush("Shiraki Shinichi");
    names~tpush("Akamatsu Hachemon");
    names~tpush("Takaki Yuichi");
    
    ;; pop last item
    slice last_name = names~tpop();

    ;; get first item
    slice first_name = names.first();

    ;; get an item by index
    slice best_name = names.at(2);

    ;; getting the length of the list 
    int number_names = names.tlen();
}
```

### X 타입 해결하기

다음 예시는 tuple에 어떤 값이 포함되어 있는지 확인하지만, tuple에는 X 타입(cell, slice, int, tuple, int)의 값이 포함되어 있습니다. 값을 확인하고 적절하게 캐스트해야 합니다.

```func
forall X -> int is_null (X x) asm "ISNULL";
forall X -> int is_int (X x) asm "<{ TRY:<{ 0 PUSHINT ADD DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_cell (X x) asm "<{ TRY:<{ CTOS DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_slice (X x) asm "<{ TRY:<{ SBITS DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_tuple (X x) asm "ISTUPLE";
forall X -> int cast_to_int (X x) asm "NOP";
forall X -> cell cast_to_cell (X x) asm "NOP";
forall X -> slice cast_to_slice (X x) asm "NOP";
forall X -> tuple cast_to_tuple (X x) asm "NOP";
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP";

forall X -> () resolve_type (X value) impure {
    ;; value here is of type X, since we dont know what is the exact value - we would need to check what is the value and then cast it
    
    if (is_null(value)) {
        ;; do something with the null
    }
    elseif (is_int(value)) {
        int valueAsInt = cast_to_int(value);
        ;; do something with the int
    }
    elseif (is_slice(value)) {
        slice valueAsSlice = cast_to_slice(value);
        ;; do something with the slice
    }
    elseif (is_cell(value)) {
        cell valueAsCell = cast_to_cell(value);
        ;; do something with the cell
    }
    elseif (is_tuple(value)) {
        tuple valueAsTuple = cast_to_tuple(value);
        ;; do something with the tuple
    }
}

() main () {
    ;; creating an empty tuple
    tuple stack = empty_tuple();
    ;; let's say we have tuple and do not know the exact types of them
    stack~tpush("Some text");
    stack~tpush(4);
    ;; we use var because we do not know type of value
    var value = stack~tpop();
    resolve_type(value);
}
```

> 💡 유용한 링크
>
> [문서의 "TVM instructions"](/v3/documentation/tvm/instructions)

### 현재 시간 가져오기

```func
int current_time = now();
  
if (current_time > 1672080143) {
    ;; do some stuff 
}
```

### 난수 생성하기

:::caution draft

자세한 내용은 [난수 생성](/v3/guidelines/smart-contracts/security/random-number-generation)을 참조하세요.
:::

```func
randomize_lt(); ;; do this once

int a = rand(10);
int b = rand(1000000);
int c = random();
```

### 모듈로 연산

예를 들어 256개의 모든 숫자에 대해 `(xp + zp)*(xp-zp)` 계산을 수행한다고 가정해보겠습니다. 이러한 연산 대부분이 암호화에 사용되므로, 다음 예시에서는 몽고메리 곡선에 대한 모듈로 연산자를 사용합니다.
xp+zp는 유효한 변수 이름입니다(공백 없음).

```func
(int) modulo_operations (int xp, int zp) {  
   ;; 2^255 - 19 is a prime number for montgomery curves, meaning all operations should be done against its prime
   int prime = 57896044618658097711785492504343953926634992332820282019728792003956564819949; 

   ;; muldivmod handles the next two lines itself
   ;; int xp+zp = (xp + zp) % prime;
   ;; int xp-zp = (xp - zp + prime) % prime;
   (_, int xp+zp*xp-zp) = muldivmod(xp + zp, xp - zp, prime);
   return xp+zp*xp-zp;
}
```

> 💡 유용한 링크
>
> [문서의 "muldivmod"](/v3/documentation/tvm/instructions#A98C)

### 오류를 발생시키는 방법

```func
int number = 198;

throw_if(35, number > 50); ;; the error will be triggered only if the number is greater than 50

throw_unless(39, number == 198); ;; the error will be triggered only if the number is NOT EQUAL to 198

throw(36); ;; the error will be triggered anyway
```

[표준 tvm 예외 코드](/v3/documentation/tvm/tvm-exit-codes)

### tuple 뒤집기

tuple이 데이터를 스택으로 저장하기 때문에, 때로는 다른 쪽 끝에서 데이터를 읽기 위해 tuple을 뒤집어야 합니다.

```func
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP";
int tuple_length (tuple t) asm "TLEN";
forall X -> (tuple) to_tuple (X x) asm "NOP";

(tuple) reverse_tuple (tuple t1) {
    tuple t2 = empty_tuple();
    repeat (t1.tuple_length()) {
        var value = t1~tpop();
        t2~tpush(value);
    }
    return t2;
}

() main () {
    tuple t = to_tuple([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
    tuple reversed_t = reverse_tuple(t);
    ~dump(reversed_t); ;; [10 9 8 7 6 5 4 3 2 1]
}
```

> 💡 유용한 링크
>
> [문서의 "tpush()"](/v3/documentation/smart-contracts/func/docs/stdlib/#tpush)

### 리스트에서 특정 인덱스의 항목을 제거하는 방법

```func
int tlen (tuple t) asm "TLEN";

(tuple, ()) remove_item (tuple old_tuple, int place) {
    tuple new_tuple = empty_tuple();

    int i = 0;
    while (i < old_tuple.tlen()) {
        int el = old_tuple.at(i);
        if (i != place) {
            new_tuple~tpush(el);
        }
        i += 1;  
    }
    return (new_tuple, ());
}

() main () {
    tuple numbers = empty_tuple();

    numbers~tpush(19);
    numbers~tpush(999);
    numbers~tpush(54);

    ~dump(numbers); ;; [19 999 54]

    numbers~remove_item(1); 

    ~dump(numbers); ;; [19 54]
}
```

### slice가 동일한지 확인하는 방법

slice 해시를 기반으로 하는 방법과 SDEQ asm 명령어를 사용하는 방법, 두 가지 다른 방식으로 동일성을 확인할 수 있습니다.

```func
int are_slices_equal_1? (slice a, slice b) {
    return a.slice_hash() == b.slice_hash();
}

int are_slices_equal_2? (slice a, slice b) asm "SDEQ";

() main () {
    slice a = "Some text";
    slice b = "Some text";
    ~dump(are_slices_equal_1?(a, b)); ;; -1 = true

    a = "Text";
    ;; We use literal `a` to get valid address inside slice from string containing address
    b = "EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF"a;
    ~dump(are_slices_equal_2?(a, b)); ;; 0 = false
}
```

#### 💡 유용한 링크

- [문서의 "slice_hash()"](/v3/documentation/smart-contracts/func/docs/stdlib/#slice_hash)
- [문서의 "SDEQ"](/v3/documentation/tvm/instructions#C705)

### cell이 동일한지 확인하는 방법

cell의 해시를 기반으로 하여 쉽게 동일성을 확인할 수 있습니다.

```func
int are_cells_equal? (cell a, cell b) {
    return a.cell_hash() == b.cell_hash();
}

() main () {
    cell a = begin_cell()
            .store_uint(123, 16)
            .end_cell();

    cell b = begin_cell()
            .store_uint(123, 16)
            .end_cell();

    ~dump(are_cells_equal?(a, b)); ;; -1 = true
}
```

> 💡 유용한 링크
>
> [문서의 "cell_hash()"](/v3/documentation/smart-contracts/func/docs/stdlib/#cell_hash)

### tuple이 동일한지 확인하는 방법

더 고급스러운 예시로는 tuple의 각 값을 순회하며 비교하는 것입니다. 값들이 X 타입이므로 해당하는 타입으로 확인하고 캐스트해야 하며, tuple인 경우 재귀적으로 순회해야 합니다.

```func
int tuple_length (tuple t) asm "TLEN";
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP";
forall X -> int cast_to_int (X x) asm "NOP";
forall X -> cell cast_to_cell (X x) asm "NOP";
forall X -> slice cast_to_slice (X x) asm "NOP";
forall X -> tuple cast_to_tuple (X x) asm "NOP";
forall X -> int is_null (X x) asm "ISNULL";
forall X -> int is_int (X x) asm "<{ TRY:<{ 0 PUSHINT ADD DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_cell (X x) asm "<{ TRY:<{ CTOS DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_slice (X x) asm "<{ TRY:<{ SBITS DROP -1 PUSHINT }>CATCH<{ 2DROP 0 PUSHINT }> }>CONT 1 1 CALLXARGS";
forall X -> int is_tuple (X x) asm "ISTUPLE";
int are_slices_equal? (slice a, slice b) asm "SDEQ";

int are_cells_equal? (cell a, cell b) {
    return a.cell_hash() == b.cell_hash();
}

(int) are_tuples_equal? (tuple t1, tuple t2) {
    int equal? = -1; ;; initial value to true
    
    if (t1.tuple_length() != t2.tuple_length()) {
        ;; if tuples are differ in length they cannot be equal
        return 0;
    }

    int i = t1.tuple_length();
    
    while (i > 0 & equal?) {
        var v1 = t1~tpop();
        var v2 = t2~tpop();
        
        if (is_null(t1) & is_null(t2)) {
            ;; nulls are always equal
        }
        elseif (is_int(v1) & is_int(v2)) {
            if (cast_to_int(v1) != cast_to_int(v2)) {
                equal? = 0;
            }
        }
        elseif (is_slice(v1) & is_slice(v2)) {
            if (~ are_slices_equal?(cast_to_slice(v1), cast_to_slice(v2))) {
                equal? = 0;
            }
        }
        elseif (is_cell(v1) & is_cell(v2)) {
            if (~ are_cells_equal?(cast_to_cell(v1), cast_to_cell(v2))) {
                equal? = 0;
            }
        }
        elseif (is_tuple(v1) & is_tuple(v2)) {
            ;; recursively determine nested tuples
            if (~ are_tuples_equal?(cast_to_tuple(v1), cast_to_tuple(v2))) {
                equal? = 0;
            }
        }
        else {
            equal? = 0;
        }

        i -= 1;
    }

    return equal?;
}

() main () {
    tuple t1 = cast_to_tuple([[2, 6], [1, [3, [3, 5]]], 3]);
    tuple t2 = cast_to_tuple([[2, 6], [1, [3, [3, 5]]], 3]);

    ~dump(are_tuples_equal?(t1, t2)); ;; -1 
}
```

> 💡 유용한 링크
>
> [문서의 "cell_hash()"](/v3/documentation/smart-contracts/func/docs/stdlib/#cell_hash)
>
> [문서의 "TVM instructions"](/v3/documentation/tvm/instructions)

### 내부 주소 생성하기

새 컨트랙트를 배포해야 하지만 주소를 모를 때 내부 주소를 생성해야 합니다. 새 컨트랙트의 코드와 데이터인 `state_init`이 이미 있다고 가정하겠습니다.

해당 MsgAddressInt TLB에 대한 내부 주소를 생성합니다.

```func
(slice) generate_internal_address (int workchain_id, cell state_init) {
    ;; addr_std$10 anycast:(Maybe Anycast) workchain_id:int8 address:bits256  = MsgAddressInt;

    return begin_cell()
        .store_uint(2, 2) ;; addr_std$10
        .store_uint(0, 1) ;; anycast nothing
        .store_int(workchain_id, 8) ;; workchain_id: -1
        .store_uint(cell_hash(state_init), 256)
    .end_cell().begin_parse();
}

() main () {
    slice deploy_address = generate_internal_address(workchain(), state_init);
    ;; then we can deploy new contract
}
```

> 💡 참고
>
> 이 예시에서는 `workchain()`을 사용하여 workchain의 id를 가져옵니다. Workchain ID에 대해 자세히 알아보려면 [문서](/v3/documentation/smart-contracts/addresses#workchain-id)를 참조하세요.

> 💡 유용한 링크
>
> [문서의 "cell_hash()"](/v3/documentation/smart-contracts/func/docs/stdlib/#cell_hash)

### 외부 주소 생성하기

[block.tlb](https://github.com/ton-blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L101C1-L101C12)의 TL-B 스키마를 사용하여 이 형식으로 주소를 생성해야 하는 방법을 이해합니다.

```func
(int) ubitsize (int a) asm "UBITSIZE";

slice generate_external_address (int address) {
    ;; addr_extern$01 len:(## 9) external_address:(bits len) = MsgAddressExt;
    
    int address_length = ubitsize(address);
    
    return begin_cell()
        .store_uint(1, 2) ;; addr_extern$01
        .store_uint(address_length, 9)
        .store_uint(address, address_length)
    .end_cell().begin_parse();
}
```

주소가 차지하는 비트 수를 결정해야 하므로, 숫자를 저장하는 데 필요한 최소 비트 수를 반환하는 `UBITSIZE` 코드로 [asm 함수를 선언](#how-to-write-own-functions-using-asm-keyword)해야 합니다.

> 💡 유용한 링크
>
> [문서의 "TVM Instructions"](/v3/documentation/tvm/instructions#B603)

### 로컬 스토리지에 딕셔너리를 저장하고 로드하는 방법

딕셔너리를 로드하는 로직:

```func
slice local_storage = get_data().begin_parse();
cell dictionary_cell = new_dict();
if (~ slice_empty?(local_storage)) {
    dictionary_cell = local_storage~load_dict();
}
```

딕셔너리를 저장하는 로직은 다음 예시와 같습니다:

```func
set_data(begin_cell().store_dict(dictionary_cell).end_cell());
```

> 💡 유용한 링크
>
> [문서의 "get_data()"](/v3/documentation/smart-contracts/func/docs/stdlib/#get_data)
>
> [문서의 "new_dict()"](/v3/documentation/smart-contracts/func/docs/stdlib/#new_dict)
>
> [문서의 "slice_empty?()"](/v3/documentation/smart-contracts/func/docs/stdlib/#slice_empty)
>
> [문서의 "load_dict()"](/v3/documentation/smart-contracts/func/docs/stdlib/#load_dict)
>
> [문서의 "~"](/v3/documentation/smart-contracts/func/docs/statements#unary-operators)

### 간단한 메시지를 보내는 방법

코멘트와 함께 ton을 보내는 일반적인 방법은 실제로 간단한 메시지입니다. 메시지 본문이 `코멘트`임을 지정하려면 메시지 텍스트 앞에 `32 비트`를 0으로 설정해야 합니다.

```func
cell msg = begin_cell()
    .store_uint(0x18, 6) ;; flags
    .store_slice("EQBIhPuWmjT7fP-VomuTWseE8JNWv2q7QYfsVQ1IZwnMk8wL"a) ;; destination address
    .store_coins(100) ;; amount of nanoTons to send
    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; default message headers (see sending messages page)
    .store_uint(0, 32) ;; zero opcode - means simple transfer message with comment
    .store_slice("Hello from FunC!") ;; comment
.end_cell();
send_raw_message(msg, 3); ;; mode 3 - pay fees separately, ignore errors
```

> 💡 유용한 링크
>
> [문서의 "Message layout"](/v3/documentation/smart-contracts/message-management/sending-messages)

### 들어오는 계정으로 메시지를 보내는 방법

아래 컨트랙트 예시는 사용자와 메인 컨트랙트 사이에 작업을 수행해야 할 때, 즉 프록시 컨트랙트가 필요할 때 유용합니다.

```func
() recv_internal (slice in_msg_body) {
    {-
        This is a simple example of a proxy-contract.
        It will expect in_msg_body to contain message mode, body and destination address to be sent to.
    -}

    int mode = in_msg_body~load_uint(8); ;; first byte will contain msg mode
    slice addr = in_msg_body~load_msg_addr(); ;; then we parse the destination address
    slice body = in_msg_body; ;; everything that is left in in_msg_body will be our new message's body

    cell msg = begin_cell()
        .store_uint(0x18, 6)
        .store_slice(addr)
        .store_coins(100) ;; just for example
        .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; default message headers (see sending messages page)
        .store_slice(body)
    .end_cell();
    send_raw_message(msg, mode);
}
```

> 💡 유용한 링크
>
> [문서의 "Message layout"](/v3/documentation/smart-contracts/message-management/sending-messages)
>
> [문서의 "load_msg_addr()"](/v3/documentation/smart-contracts/func/docs/stdlib/#load_msg_addr)

### 전체 잔액을 가진 메시지를 보내는 방법

스마트 컨트랙트의 전체 잔액을 보내야 하는 경우, `mode 128`을 사용하여 보내야 합니다. 이러한 경우의 예시로는 결제를 받아서 메인 컨트랙트로 전달하는 프록시 컨트랙트가 있습니다.

```func
cell msg = begin_cell()
    .store_uint(0x18, 6) ;; flags
    .store_slice("EQBIhPuWmjT7fP-VomuTWseE8JNWv2q7QYfsVQ1IZwnMk8wL"a) ;; destination address
    .store_coins(0) ;; we don't care about this value right now
    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; default message headers (see sending messages page)
    .store_uint(0, 32) ;; zero opcode - means simple transfer message with comment
    .store_slice("Hello from FunC!") ;; comment
.end_cell();
send_raw_message(msg, 128); ;; mode = 128 is used for messages that are to carry all the remaining balance of the current smart contract
```

> 💡 유용한 링크
>
> [문서의 "Message layout"](/v3/documentation/smart-contracts/message-management/sending-messages)
>
> [문서의 "Message modes"](/v3/documentation/smart-contracts/func/docs/stdlib/#send_raw_message)

### 긴 텍스트 코멘트가 있는 메시지를 보내는 방법

단일 `cell`에는 127개의 문자(<1023 비트)만 들어갈 수 있다는 것을 알고 있습니다. 더 많이 필요한 경우 - snake cells를 구성해야 합니다.

```func
{-
    If we want to send a message with really long comment, we should split the comment to several slices.
    Each slice should have <1023 bits of data (127 chars).
    Each slice should have a reference to the next one, forming a snake-like structure.
-}

cell body = begin_cell()
    .store_uint(0, 32) ;; zero opcode - simple message with comment
    .store_slice("long long long message...")
    .store_ref(begin_cell()
        .store_slice(" you can store string of almost any length here.")
        .store_ref(begin_cell()
            .store_slice(" just don't forget about the 127 chars limit for each slice")
        .end_cell())
    .end_cell())
.end_cell();

cell msg = begin_cell()
    .store_uint(0x18, 6) ;; flags
    ;; We use literal `a` to get valid address inside slice from string containing address 
    .store_slice("EQBIhPuWmjT7fP-VomuTWseE8JNWv2q7QYfsVQ1IZwnMk8wL"a) ;; destination address
    .store_coins(100) ;; amount of nanoTons to send
    .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1) ;; default message headers (see sending messages page)
    .store_uint(1, 1) ;; we want to store body as a ref
    .store_ref(body)
.end_cell();
send_raw_message(msg, 3); ;; mode 3 - pay fees separately, ignore errors
```

> 💡 유용한 링크
>
> [문서의 "Internal messages"](/v3/documentation/smart-contracts/message-management/internal-messages)

### slice에서 refs 없이 데이터 비트만 가져오는 방법

`slice` 내의 `refs`에 관심이 없다면 날짜만 따로 가져와서 작업할 수 있습니다.

```func
slice s = begin_cell()
    .store_slice("Some data bits...")
    .store_ref(begin_cell().end_cell()) ;; some references
    .store_ref(begin_cell().end_cell()) ;; some references
.end_cell().begin_parse();

slice s_only_data = s.preload_bits(s.slice_bits());
```

> 💡 유용한 링크
>
> [문서의 "Slice primitives"](/v3/documentation/smart-contracts/func/docs/stdlib/#slice-primitives)
>
> [문서의 "preload_bits()"](/v3/documentation/smart-contracts/func/docs/stdlib/#preload_bits)
>
> [문서의 "slice_bits()"](/v3/documentation/smart-contracts/func/docs/stdlib/#slice_bits)

### 자체 수정 메서드를 정의하는 방법

수정 메서드를 사용하면 동일한 변수 내에서 데이터를 수정할 수 있습니다. 이는 다른 프로그래밍 언어의 참조와 비교할 수 있습니다.

```func
(slice, (int)) load_digit (slice s) {
    int x = s~load_uint(8); ;; load 8 bits (one char) from slice
    x -= 48; ;; char '0' has code of 48, so we substract it to get the digit as a number
    return (s, (x)); ;; return our modified slice and loaded digit
}

() main () {
    slice s = "258";
    int c1 = s~load_digit();
    int c2 = s~load_digit();
    int c3 = s~load_digit();
    ;; here s is equal to "", and c1 = 2, c2 = 5, c3 = 8
}
```

> 💡 유용한 링크
>
> [문서의 "Modifying methods"](/v3/documentation/smart-contracts/func/docs/statements#modifying-methods)

### 숫자를 n제곱하는 방법

```func
;; Unoptimized variant
int pow (int a, int n) {
    int i = 0;
    int value = a;
    while (i < n - 1) {
        a *= value;
        i += 1;
    }
    return a;
}

;; Optimized variant
(int) binpow (int n, int e) {
    if (e == 0) {
        return 1;
    }
    if (e == 1) {
        return n;
    }
    int p = binpow(n, e / 2);
    p *= p;
    if ((e % 2) == 1) {
        p *= n;
    }
    return p;
}

() main () {
    int num = binpow(2, 3);
    ~dump(num); ;; 8
}
```

### 문자열을 int로 변환하는 방법

```func
slice string_number = "26052021";
int number = 0;

while (~ string_number.slice_empty?()) {
    int char = string_number~load_uint(8);
    number = (number * 10) + (char - 48); ;; we use ASCII table
}

~dump(number);
```

### int를 문자열로 변환하는 방법

```func
int n = 261119911;
builder string = begin_cell();
tuple chars = null();
do {
    int r = n~divmod(10);
    chars = cons(r + 48, chars);
} until (n == 0);
do {
    int char = chars~list_next();
    string~store_uint(char, 8);
} until (null?(chars));

slice result = string.end_cell().begin_parse();
~dump(result);
```

### 딕셔너리를 순회하는 방법

딕셔너리는 많은 데이터를 다룰 때 매우 유용합니다. 내장 메서드 `dict_get_min?`와 `dict_get_max?`를 사용하여 최소값과 최대값 키를 각각 가져올 수 있습니다. 또한 `dict_get_next?`를 사용하여 딕셔너리를 순회할 수 있습니다.

```func
cell d = new_dict();
d~udict_set(256, 1, "value 1");
d~udict_set(256, 5, "value 2");
d~udict_set(256, 12, "value 3");

;; iterate keys from small to big
(int key, slice val, int flag) = d.udict_get_min?(256);
while (flag) {
    ;; do something with pair key->val
    
    (key, val, flag) = d.udict_get_next?(256, key);
}
```

> 💡 유용한 링크
>
> [문서의 "Dictonaries primitives"](/v3/documentation/smart-contracts/func/docs/stdlib/#dictionaries-primitives)
>
> [문서의 "dict_get_max?()"](/v3/documentation/smart-contracts/func/docs/stdlib/#dict_get_max)
>
> [문서의 "dict_get_min?()"](/v3/documentation/smart-contracts/func/docs/stdlib/#dict_get_min)
>
> [문서의 "dict_get_next?()"](/v3/documentation/smart-contracts/func/docs/stdlib/#dict_get_next)
>
> [문서의 "dict_set()"](/v3/documentation/smart-contracts/func/docs/stdlib/#dict_set)

### 딕셔너리에서 값을 삭제하는 방법

```func
cell names = new_dict();
names~udict_set(256, 27, "Alice");
names~udict_set(256, 25, "Bob");

names~udict_delete?(256, 27);

(slice val, int key) = names.udict_get?(256, 27);
~dump(val); ;; null() -> means that key was not found in a dictionary
```

### cell 트리를 재귀적으로 순회하는 방법

하나의 `cell`이 최대 `1023 비트`의 데이터와 최대 `4개의 refs`를 저장할 수 있다는 것을 알고 있습니다. 이 제한을 우회하기 위해 cell 트리를 사용할 수 있지만, 적절한 데이터 처리를 위해 이를 순회할 수 있어야 합니다.

```func
forall X -> int is_null (X x) asm "ISNULL";
forall X -> (tuple, ()) push_back (tuple tail, X head) asm "CONS";
forall X -> (tuple, (X)) pop_back (tuple t) asm "UNCONS";

() main () {
    ;; just some cell for example
    cell c = begin_cell()
        .store_uint(1, 16)
        .store_ref(begin_cell()
            .store_uint(2, 16)
        .end_cell())
        .store_ref(begin_cell()
            .store_uint(3, 16)
            .store_ref(begin_cell()
                .store_uint(4, 16)
            .end_cell())
            .store_ref(begin_cell()
                .store_uint(5, 16)
            .end_cell())
        .end_cell())
    .end_cell();

    ;; creating tuple with no data, which plays the role of stack
    tuple stack = null();
    ;; bring the main cell into the stack to process it in the loop
    stack~push_back(c);
    ;; do it until stack is not null
    while (~ stack.is_null()) {
        ;; get the cell from the stack and convert it to a slice to be able to process it
        slice s = stack~pop_back().begin_parse();

        ;; do something with s data

        ;; if the current slice has any refs, add them to stack
        repeat (s.slice_refs()) {
            stack~push_back(s~load_ref());
        }
    }
}
```

> 💡 유용한 링크
>
> [문서의 "Lisp-style lists"](/v3/documentation/smart-contracts/func/docs/stdlib/#lisp-style-lists)
>
> [문서의 "null()"](/v3/documentation/smart-contracts/func/docs/stdlib/#null)
>
> [문서의 "slice_refs()"](/v3/documentation/smart-contracts/func/docs/stdlib/#slice_refs)

### lisp-style 리스트를 순회하는 방법

tuple 데이터 타입은 최대 255개의 값을 보유할 수 있습니다. 이것으로 충분하지 않다면, lisp-style 리스트를 사용해야 합니다. tuple 안에 tuple을 넣을 수 있어서 제한을 우회할 수 있습니다.

```func
forall X -> int is_null (X x) asm "ISNULL";
forall X -> (tuple, ()) push_back (tuple tail, X head) asm "CONS";
forall X -> (tuple, (X)) pop_back (tuple t) asm "UNCONS";

() main () {
    ;; some example list
    tuple l = null();
    l~push_back(1);
    l~push_back(2);
    l~push_back(3);

    ;; iterating through elements
    ;; note that this iteration is in reversed order
    while (~ l.is_null()) {
        var x = l~pop_back();

        ;; do something with x
    }
}
```

> 💡 유용한 링크
>
> [문서의 "Lisp-style lists"](/v3/documentation/smart-contracts/func/docs/stdlib/#lisp-style-lists)
>
> [문서의 "null()"](/v3/documentation/smart-contracts/func/docs/stdlib/#null)

### 배포 메시지를 보내는 방법 (stateInit만 있는 경우, stateInit과 body가 모두 있는 경우)

```func
() deploy_with_stateinit(cell message_header, cell state_init) impure {
  var msg = begin_cell()
    .store_slice(begin_parse(msg_header))
    .store_uint(2 + 1, 2) ;; init:(Maybe (Either StateInit ^StateInit))
    .store_uint(0, 1) ;; body:(Either X ^X)
    .store_ref(state_init)
    .end_cell();

  ;; mode 64 - carry the remaining value in the new message
  send_raw_message(msg, 64); 
}

() deploy_with_stateinit_body(cell message_header, cell state_init, cell body) impure {
  var msg = begin_cell()
    .store_slice(begin_parse(msg_header))
    .store_uint(2 + 1, 2) ;; init:(Maybe (Either StateInit ^StateInit))
    .store_uint(1, 1) ;; body:(Either X ^X)
    .store_ref(state_init)
    .store_ref(body)
    .end_cell();

  ;; mode 64 - carry the remaining value in the new message
  send_raw_message(msg, 64); 
}
```

### stateInit cell을 구성하는 방법

```func
() build_stateinit(cell init_code, cell init_data) {
  var state_init = begin_cell()
    .store_uint(0, 1) ;; split_depth:(Maybe (## 5))
    .store_uint(0, 1) ;; special:(Maybe TickTock)
    .store_uint(1, 1) ;; (Maybe ^Cell)
    .store_uint(1, 1) ;; (Maybe ^Cell)
    .store_uint(0, 1) ;; (HashmapE 256 SimpleLib)
    .store_ref(init_code)
    .store_ref(init_data)
    .end_cell();
}
```

### 컨트랙트 주소를 계산하는 방법 (stateInit 사용)

```func
() calc_address(cell state_init) {
  var future_address = begin_cell() 
    .store_uint(2, 2) ;; addr_std$10
    .store_uint(0, 1) ;; anycast:(Maybe Anycast)
    .store_uint(0, 8) ;; workchain_id:int8
    .store_uint(cell_hash(state_init), 256) ;; address:bits256
    .end_cell();
}
```

### 스마트 컨트랙트 로직을 업데이트하는 방법

아래는 카운터를 증가시키고 스마트 컨트랙트 로직을 업데이트하는 기능이 있는 간단한 `CounterV1` 스마트 컨트랙트입니다.

```func
() recv_internal (slice in_msg_body) {
    int op = in_msg_body~load_uint(32);
    
    if (op == op::increase) {
        int increase_by = in_msg_body~load_uint(32);
        ctx_counter += increase_by;
        save_data();
        return ();
    }

    if (op == op::upgrade) {
        cell code = in_msg_body~load_ref();
        set_code(code);
        return ();
    }
}
```

스마트 컨트랙트를 운영한 후, 미터 감소 기능이 빠져있다는 것을 알게 됩니다. `CounterV1` 스마트 컨트랙트의 코드를 복사하고 `increase` 함수 옆에 새로운 `decrease` 함수를 추가해야 합니다. 이제 코드는 다음과 같습니다:

```func
() recv_internal (slice in_msg_body) {
    int op = in_msg_body~load_uint(32);
    
    if (op == op::increase) {
        int increase_by = in_msg_body~load_uint(32);
        ctx_counter += increase_by;
        save_data();
        return ();
    }

    if (op == op::decrease) {
        int decrease_by = in_msg_body~load_uint(32);
        ctx_counter -= increase_by;
        save_data();
        return ();
    }

    if (op == op::upgrade) {
        cell code = in_msg_body~load_ref();
        set_code(code);
        return ();
    }
}
```

`CounterV2` 스마트 컨트랙트가 준비되면, 오프체인에서 `cell`로 컴파일하고 `CounterV1` 스마트 컨트랙트에 업그레이드 메시지를 보내야 합니다.

```javascript
await contractV1.sendUpgrade(provider.sender(), {
    code: await compile('ContractV2'),
    value: toNano('0.05'),
});
```

> 💡 유용한 링크
>
> [기존 주소에 코드를 다시 배포할 수 있나요, 아니면 새 컨트랙트로 배포해야 하나요?](/v3/documentation/faq#is-it-possible-to-re-deploy-code-to-an-existing-address-or-does-it-have-to-be-deployed-as-a-new-contract)
>
> [문서의 "set_code()"](/v3/documentation/smart-contracts/func/docs/stdlib#set_code)
