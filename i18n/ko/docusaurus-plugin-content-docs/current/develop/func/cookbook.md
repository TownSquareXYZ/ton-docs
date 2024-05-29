# FunC 요리책

펀씨 쿡북을 만든 핵심 이유는 펀씨 개발자들의 모든 경험을 한곳에 모아 미래의 개발자들이 활용할 수 있도록 하기 위해서입니다!

펀씨 문서](/develop/func/types)에 비해 이 문서는 모든 펀씨 개발자가 스마트 컨트랙트를 개발하는 동안 해결해야 하는 일상적인 작업에 더 초점을 맞추고 있습니다.

## 기본 사항

### if 문을 작성하는 방법

어떤 이벤트가 관련성이 있는지 확인하고 싶다고 가정해 보겠습니다. 이를 위해 플래그 변수를 사용합니다. FunC에서 `true`는 `-1`이고 `false`는 `0`이라는 것을 기억하세요.

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
> 0`값은`거짓`이므로 다른 값은 `참`이 되므로 연산자 `==\`가 필요하지 않습니다.

> 💡 유용한 링크
>
> [문서에서 "If 문"](/개발/펀크/스테이트먼트#if-스테이트먼트)

### 반복 루프를 작성하는 방법

예를 들어 지수화를 예로 들 수 있습니다.

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
> [문서의 "반복 루프"](/개발/펀크/문장#반복-루프)

### 동안 루프를 작성하는 방법

동안은 특정 작업을 얼마나 자주 수행해야 할지 모를 때 유용합니다. 예를 들어 다른 셀에 대한 참조를 최대 4개까지 저장하는 것으로 알려진 '셀'을 예로 들어보겠습니다.

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
> [문서의 "동안 루프"](/개발/펀크/스테이트먼트#동안-루프)
>
> [문서의 '셀'](/학습/개요/셀)
>
> ["slice_refs_empty?()" in docs](/develop/func/stdlib#slice_refs_empty)
>
> ["store_ref()" in docs](/develop/func/stdlib#store_ref)
>
> ["begin_cell()" in docs](/develop/func/stdlib#begin_cell)
>
> ["end_cell()" in docs](/develop/func/stdlib#end_cell)
>
> ["begin_parse()" in docs](/develop/func/stdlib#begin_parse)

### do until 루프를 작성하는 방법

사이클을 한 번 이상 실행해야 할 때는 `할 때까지`를 사용합니다.

```func
int flag = 0;

do {
    ;; do something even flag is false (0) 
} until (flag == -1); ;; -1 is true
```

> 💡 유용한 링크
>
> ["문서에서 루프까지"](/개발/펀크/스테이트먼트#유틸-루프)

### 슬라이스가 비어 있는지 확인하는 방법

슬라이스`로 작업하기 전에 올바르게 처리할 데이터가 있는지 확인해야 합니다. 이를 위해 `slice_empty?()`를 사용할 수 있지만, 적어도 하나의 `bit`데이터 또는 하나의`ref`가 있는 경우 `-1`(`true\`)을 반환한다는 점을 고려해야 합니다.

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
> ["slice_empty?()" in docs](/develop/func/stdlib#slice_empty)
>
> ["store_slice()" in docs](/develop/func/stdlib#store_slice)
>
> ["store_ref()" in docs](/develop/func/stdlib#store_ref)
>
> ["begin_cell()" in docs](/develop/func/stdlib#begin_cell)
>
> ["end_cell()" in docs](/develop/func/stdlib#end_cell)
>
> ["begin_parse()" in docs](/develop/func/stdlib#begin_parse)

### 슬라이스가 비어 있는지 확인하는 방법(비트는 없지만 참조가 있을 수 있음)

만약 `비트`만 확인해야 하고 `슬라이스`에 `ref`가 있는지 여부는 중요하지 않다면 `slice_data_empty?()`를 사용해야 합니다.

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
> ["slice_data_empty?()" in docs](/develop/func/stdlib#slice_data_empty)
>
> ["store_slice()" in docs](/develop/func/stdlib#store_slice)
>
> ["store_ref()" in docs](/develop/func/stdlib#store_ref)
>
> ["begin_cell()" in docs](/develop/func/stdlib#begin_cell)
>
> ["end_cell()" in docs](/develop/func/stdlib#end_cell)
>
> ["begin_parse()" in docs](/develop/func/stdlib#begin_parse)

### 슬라이스가 비어 있는지 확인하는 방법(참조가 없지만 비트가 있을 수 있음)

참조`에만 관심이 있는 경우 `slice_refs_empty?()\`를 사용하여 참조의 존재 여부를 확인해야 합니다.

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
> ["slice_refs_empty?()" in docs](/develop/func/stdlib#slice_refs_empty)
>
> ["store_slice()" in docs](/develop/func/stdlib#store_slice)
>
> ["store_ref()" in docs](/develop/func/stdlib#store_ref)
>
> ["begin_cell()" in docs](/develop/func/stdlib#begin_cell)
>
> ["end_cell()" in docs](/develop/func/stdlib#end_cell)
>
> ["begin_parse()" in docs](/develop/func/stdlib#begin_parse)

### 셀이 비어 있는지 확인하는 방법

셀`에 데이터가 있는지 확인하려면 먼저 `슬라이스`로 변환해야 합니다. 만약 `비트`만 있다면 `slice_data_empty?()`를, `ref`만 있다면 `slice_refs_empty?()`를 사용해야 합니다. 비트`인지 `ref`인지에 관계없이 모든 데이터의 존재 여부를 확인하려면 `slice_empty?()`를 사용해야 합니다.

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
> ["slice_empty?()" in docs](/develop/func/stdlib#slice_empty)
>
> ["begin_cell()" in docs](/develop/func/stdlib#begin_cell)
>
> ["store_uint()" in docs](/develop/func/stdlib#store_uint)
>
> ["end_cell()" in docs](/develop/func/stdlib#end_cell)
>
> ["begin_parse()" in docs](/develop/func/stdlib#begin_parse)

### 딕셔너리가 비어 있는지 확인하는 방법

딕셔너리에 날짜가 있는지 확인하는 `dict_empty?()` 메서드가 있습니다. 이 메서드는 일반적으로 `null` 셀은 빈 딕셔너리이므로 `cell_null?()`과 동일합니다.

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
> ["dict_empty?()" in docs](/develop/func/stdlib#dict_empty)
>
> ["new_dict()" in docs](/develop/func/stdlib/#new_dict) 빈 딕셔너리를 생성합니다.
>
> 문서의 ["dict_set()"](/develop/func/stdlib/#dict_set)은 함수를 사용하여 딕션의 일부 요소를 추가하므로 비어 있지 않습니다.

### 튜플이 비어 있는지 확인하는 방법

튜플`로 작업할 때는 항상 내부에 추출할 값이 있는지 확인하는 것이 중요합니다. 빈 '튜플'에서 값을 추출하려고 하면 오류가 발생합니다: "유효한 크기의 튜플이 아닙니다"라는 오류와 함께 `종료 코드 7\`이 표시됩니다.

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
> tlen 어셈블리 함수를 선언합니다. 자세한 내용은 [여기](/개발/펀크/함수#어셈블러-함수-본문-정의)에서 확인할 수 있으며 [모든 어셈블러 명령어 목록](/학습/tvm-지침/지침)을 참조하세요.

> 💡 유용한 링크
>
> ["empty_tuple?()" in docs](/develop/func/stdlib#empty_tuple)
>
> ["tpush()" in docs](/develop/func/stdlib/#tpush)
>
> [문서의 "종료 코드"](/학습/tvm-지침/tvm-exit-codes)

### 리스프 스타일 목록이 비어 있는지 확인하는 방법

```func
tuple numbers = null();
numbers = cons(100, numbers);

if (numbers.null?()) {
    ;; list-style list is empty
} else {
    ;; list-style list is not empty
}
```

단점](/develop/func/stdlib/#cons) 함수를 사용하여 목록 스타일 목록에 100번을 추가하고 있으므로 비어 있지 않습니다.

### 컨트랙트가 비어 있는 상태를 확인하는 방법

트랜잭션 수를 저장하는 '카운터'가 있다고 가정해 봅시다. 이 변수는 스마트 컨트랙트 상태의 첫 번째 트랜잭션에서는 상태가 비어 있기 때문에 사용할 수 없으므로 이러한 경우를 처리할 필요가 있습니다. 상태가 비어 있으면 '카운터'라는 변수를 생성하고 저장합니다.

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
> 셀이 비어 있는지 확인하려면 [셀이 비어 있는지](/develop/func/cookbook#how-to-determine-if-cell-is-empty)를 확인하여 컨트랙트 상태가 비어 있는지 확인할 수 있습니다.

> 💡 유용한 링크
>
> ["get_data()" in docs](/develop/func/stdlib#get_data)
>
> ["begin_parse()" in docs](/develop/func/stdlib/#begin_parse)
>
> ["slice_empty?()" in docs](/develop/func/stdlib/#slice_empty)
>
> ["set_data?()" in docs](/develop/func/stdlib#set_data)

### 내부 메시지 셀을 만드는 방법

컨트랙트가 내부 메시지를 보내려면 먼저 기술 플래그, 수신자 주소, 나머지 데이터를 지정하여 셀로 올바르게 생성해야 합니다.

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
> 이 예제에서는 리터럴 `a`를 사용하여 주소를 가져옵니다. 문자열 리터럴에 대한 자세한 내용은 [문서](/개발/펀크/리터럴_식별자#string-literals)에서 확인할 수 있습니다.

> 💡 참고
>
> 자세한 내용은 [문서](/개발/스마트계약/메시지)에서 확인할 수 있습니다. 또한 이 링크를 통해 [레이아웃](/개발/스마트계약/메시지#메시지-레이아웃)으로 이동할 수도 있습니다.

> 💡 유용한 링크
>
> ["begin_cell()" in docs](/develop/func/stdlib#begin_cell)
>
> ["store_uint()" in docs](/develop/func/stdlib#store_uint)
>
> ["store_slice()" in docs](/develop/func/stdlib#store_slice)
>
> ["store_coins()" in docs](/develop/func/stdlib#store_coins)
>
> ["end_cell()" in docs](/develop/func/stdlib/#end_cell)
>
> ["send_raw_message()" in docs](/develop/func/stdlib/#send_raw_message)

### 내부 메시지 셀에 참조로 본문을 포함하는 방법

플래그 및 기타 기술 데이터 뒤에 오는 메시지 본문에는 `int`, `슬라이스`, `셀`을 보낼 수 있습니다. 후자의 경우 `store_ref()` 앞에 비트를 `1`로 설정하여 `셀`이 계속 진행됨을 표시해야 합니다.

공간이 충분하다고 확신하는 경우 헤더와 동일한 '셀' 안에 메시지 본문을 보낼 수도 있습니다. 이 경우 비트를 `0`으로 설정해야 합니다.

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
> 이 예제에서는 리터럴 `a`를 사용하여 주소를 가져옵니다. 문자열 리터럴에 대한 자세한 내용은 [문서](/개발/펀크/리터럴_식별자#string-literals)에서 확인할 수 있습니다.

> 💡 참고
>
> 이 예에서는 모드 3을 사용하여 들어오는 톤을 가져와서 계약 잔액에서 수수료를 지불하고 오류를 무시한 채 지정된 양(금액)을 정확히 전송했습니다. 받은 모든 톤에서 수수료를 뺀 금액을 반환하려면 모드 64가 필요하며, 모드 128은 전체 잔액을 전송합니다.

> 💡 참고
>
> 메시지 작성](/develop/func/cookbook#how-to-build-an-internal-message-cell)을 하고 있지만 메시지 본문은 별도로 추가하고 있습니다.

> 💡 유용한 링크
>
> ["begin_cell()" in docs](/develop/func/stdlib#begin_cell)
>
> ["store_uint()" in docs](/develop/func/stdlib#store_uint)
>
> ["store_slice()" in docs](/develop/func/stdlib#store_slice)
>
> ["store_coins()" in docs](/develop/func/stdlib#store_coins)
>
> ["end_cell()" in docs](/develop/func/stdlib/#end_cell)
>
> ["send_raw_message()" in docs](/develop/func/stdlib/#send_raw_message)

### 내부 메시지 셀에 슬라이스로 본문을 포함하는 방법

메시지를 보낼 때 본문 메시지는 `셀` 또는 `슬라이스`로 보낼 수 있습니다. 이 예에서는 `슬라이스` 안에 메시지 본문을 보냅니다.

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
> 이 예제에서는 리터럴 `a`를 사용하여 주소를 가져옵니다. 문자열 리터럴에 대한 자세한 내용은 [문서](/개발/펀크/리터럴_식별자#string-literals)에서 확인할 수 있습니다.

> 💡 참고
>
> 이 예에서는 모드 3을 사용하여 들어오는 톤을 가져와서 계약 잔액에서 수수료를 지불하고 오류를 무시한 채 지정된 양(금액)을 정확히 전송했습니다. 받은 모든 톤에서 수수료를 뺀 금액을 반환하려면 모드 64가 필요하며, 모드 128은 전체 잔액을 전송합니다.

> 💡 참고
>
> 우리는 [메시지 구축](/develop/func/cookbook#how-to-build-an-internal-message-cell)을 하고 있지만 메시지를 슬라이스로 추가하고 있습니다.

### 튜플을 반복하는 방법(양방향)

FunC에서 배열이나 스택으로 작업하려면 튜플이 필요합니다. 그리고 우선 값을 반복하여 작업할 수 있어야 합니다.

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
> tlen\` 어셈블리 함수를 선언합니다. 자세한 내용은 [여기](/개발/펀크/함수#어셈블러-함수-본문-정의)에서 확인할 수 있으며, [모든 어셈블러 명령어 목록](/학습/tvm-지침/지침)을 참조하세요.
>
> 또한 `to_tuple` 함수를 선언합니다. 이 함수는 모든 입력의 데이터 유형을 튜플로 변경하므로 사용할 때 주의해야 합니다.

### 아스\` 키워드를 사용하여 자체 함수를 작성하는 방법

어떤 기능을 사용할 때는 실제로 `stdlib.fc`에 미리 준비된 메서드를 사용합니다. 하지만 실제로는 더 많은 기회를 사용할 수 있으며 직접 작성하는 방법을 배워야 합니다.

예를 들어, 'tpush'라는 메서드는 'tuple'에 요소를 추가하지만 'tpop'이 없는 메서드입니다. 이 경우에는 이렇게 해야 합니다:

```func
;; ~ means it is modifying method
forall X -> (tuple, X) ~tpop (tuple t) asm "TPOP"; 
```

반복을 위한 '튜플'의 길이를 알고 싶다면 `TLEN` asm 명령어를 사용하여 새 함수를 작성해야 합니다:

```func
int tuple_length (tuple t) asm "TLEN";
```

stdlib.fc에서 이미 알려진 함수의 몇 가지 예입니다:

```func
slice begin_parse(cell c) asm "CTOS";
builder begin_cell() asm "NEWC";
cell end_cell(builder b) asm "ENDC";
```

> 💡 유용한 링크:
>
> [문서의 "수정 방법"](/개발/펀크/스테이트먼트#수정 방법)
>
> [문서에서 "stdlib"](/개발/펀크/stdlib)
>
> [문서의 'TVM 지침'](/학습/tvm-지침/지침)

### n 중첩 튜플 반복하기

중첩된 튜플을 반복하고 싶을 때가 있습니다. 다음 예제는 `[[2,6],[1,[3,[3,5]], 3]` 형식의 튜플에 있는 모든 항목을 머리부터 반복하여 출력합니다.

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
> [문서의 "전역 변수"](/개발/펀크/글로벌_변수)
>
> [문서에서 "~덤프"](/개발/펀크/빌트인#덤프-변수)
>
> [문서의 'TVM 지침'](/학습/tvm-지침/지침)

### 튜플을 사용한 기본 연산

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

### X 유형 해결

다음 예제는 어떤 값이 튜플에 포함되어 있는데 튜플에 값 X(셀, 슬라이스, int, 튜플, int)가 포함되어 있는지 확인하는 예제입니다. 값을 확인하고 그에 따라 형변환해야 합니다.

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
> [문서의 'TVM 지침'](/학습/tvm-지침/지침)

### 현재 시간을 얻는 방법

```func
int current_time = now();
  
if (current_time > 1672080143) {
    ;; do some stuff 
}
```

### 난수 생성 방법

:::caution 초안

자세한 내용은 [난수 생성](https://docs.ton.org/develop/smart-contracts/guidelines/random-number-generation)을 확인하세요.
:::

```func
randomize_lt(); ;; do this once

int a = rand(10);
int b = rand(1000000);
int c = random();
```

### 모듈식 연산

예를 들어 모든 256개의 숫자에 대해 `(xp + zp)*(xp-zp)`라는 연산을 실행한다고 가정해 보겠습니다. 이러한 연산은 대부분 암호화에 사용되므로 다음 예제에서는 모듈로 연산자를 몬토고메리 곡선에 사용합니다.
xp+zp는 유효한 변수 이름(공백 없이)이라는 점에 유의하세요.

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
> [문서의 "muldivmod"](/학습/tvm-지침/지침#52-division)

### 오류를 던지는 방법

```func
int number = 198;

throw_if(35, number > 50); ;; the error will be triggered only if the number is greater than 50

throw_unless(39, number == 198); ;; the error will be triggered only if the number is NOT EQUAL to 198

throw(36); ;; the error will be triggered anyway
```

[표준 tvm 예외 코드](/learn/tvm-instructions/tvm-exit-codes.md)

### 튜플 반전

튜플은 데이터를 스택으로 저장하기 때문에 때로는 반대쪽에서 데이터를 읽기 위해 튜플을 역방향으로 바꿔야 할 때가 있습니다.

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
> ["tpush()" in docs](/develop/func/stdlib/#tpush)

### 목록에서 특정 색인이 있는 항목을 삭제하는 방법

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

### 슬라이스가 동일한지 확인

동등성을 판단하는 방법에는 두 가지가 있습니다. 하나는 슬라이스 해시를 기반으로 하는 것이고, 다른 하나는 SDEQ asm 명령어를 사용하는 것입니다.

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

- ["slice_hash()" in docs](/develop/func/stdlib/#slice_hash)
- [문서의 "SDEQ"](/학습/tvm-지침/지침#62-다른 비교)

### 셀이 동일한지 확인

해시를 기반으로 셀의 동일성을 쉽게 확인할 수 있습니다.

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
> ["cell_hash()" in docs](/develop/func/stdlib/#cell_hash)

### 튜플이 동일한지 확인

좀 더 고급 예는 각 튜플 값을 반복하고 비교하는 것입니다. X이므로 해당 유형을 확인하고 해당 유형으로 형변환해야 하며, 튜플인 경우 재귀적으로 반복해야 합니다.

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
> ["cell_hash()" in docs](/develop/func/stdlib/#cell_hash)
>
> [문서의 'TVM 지침'](/학습/tvm-지침/지침)

### 내부 주소 생성

컨트랙트가 새 컨트랙트를 배포해야 할 때 내부 주소를 생성해야 하는데 주소를 모릅니다. 새 컨트랙트의 코드와 데이터인 `state_init`이 이미 있다고 가정해봅시다.

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
> 이 예에서는 `workchain()`을 사용하여 워크체인의 ID를 가져옵니다. 워크체인 ID에 대한 자세한 내용은 [문서](/학습/개요/주소#워크체인-id)에서 확인할 수 있습니다.

> 💡 유용한 링크
>
> ["cell_hash()" in docs](/develop/func/stdlib/#cell_hash)

### 외부 주소 생성

블록](https://github.com/ton-blockchain/ton/blob/24dc184a2ea67f9c47042b4104bbb4d82289fac1/crypto/block/block.tlb#L101C1-L101C12)의 TL-B 체계를 사용하여 이 형식의 주소를 생성하는 방법을 이해합니다.

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

주소가 차지하는 비트 수를 결정해야 하므로, 숫자를 저장하는 데 필요한 최소 비트 수를 반환하는 연산자 `UBITSIZE`를 사용하여 [asm 함수 선언](#how-to-write-own-functions-using-asm-keyword)을 해야 합니다.

> 💡 유용한 링크
>
> [문서의 'TVM 지침'](/학습/tvm-지침/지침#53-교대-논리적-연산)

### 로컬 저장소에 사전을 저장하고 로드하는 방법

사전을 로드하는 로직

```func
slice local_storage = get_data().begin_parse();
cell dictionary_cell = new_dict();
if (~ slice_empty?(local_storage)) {
    dictionary_cell = local_storage~load_dict();
}
```

사전을 저장하는 로직은 다음 예시와 같습니다:

```func
set_data(begin_cell().store_dict(dictionary_cell).end_cell());
```

> 💡 유용한 링크
>
> ["get_data()" in docs](/develop/func/stdlib/#get_data)
>
> ["new_dict()" in docs](/develop/func/stdlib/#new_dict)
>
> ["slice_empty?()" in docs](/develop/func/stdlib/#slice_empty)
>
> ["load_dict()" in docs](/develop/func/stdlib/#load_dict)
>
> [문서에서 "~"](/개발/펀크/스테이트먼트#유니타리 연산자)

### 간단한 메시지 보내기

댓글과 함께 톤을 전송하는 일반적인 방법은 사실 간단한 메시지입니다. 메시지 본문이 '댓글'임을 지정하려면 메시지 텍스트 앞의 '32비트'를 0으로 설정해야 합니다.

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
> [[문서의 '메시지 레이아웃'](/개발/스마트계약/메시지)

### 수신 계정으로 메시지를 보내는 방법

아래 계약 예시는 사용자와 주 계약 간에 어떤 작업을 수행해야 하는 경우, 즉 대리 계약이 필요한 경우에 유용합니다.

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
> [[문서의 '메시지 레이아웃'](/개발/스마트계약/메시지)
>
> ["load_msg_addr()" in docs](/develop/func/stdlib/#load_msg_addr)

### 전체 잔액으로 메시지를 보내는 방법

스마트 콘트랙트의 전체 잔액을 전송해야 하는 경우, 이 경우 '모드 128'을 사용해야 합니다. 이러한 경우의 예로는 결제를 수락하고 메인 컨트랙트로 전달하는 프록시 컨트랙트를 들 수 있습니다.

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
> [[문서의 '메시지 레이아웃'](/개발/스마트계약/메시지)
>
> ["메시지 모드" 문서](/develop/func/stdlib/#send_raw_message)

### 긴 텍스트 댓글이 포함된 메시지를 보내는 방법

아시다시피, 하나의 '셀'(<1023비트)에는 127자만 들어갈 수 있습니다. 더 많은 문자가 필요한 경우 스네이크 셀을 구성해야 합니다.

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
> [문서의 '내부 메시지'](/개발/스마트계약/가이드라인/내부 메시지)

### 슬라이스에서 데이터 비트만 가져오는 방법(참조 없이)

'슬라이스' 안에 있는 '참조'에 관심이 없다면 별도의 날짜를 가져와서 작업할 수 있습니다.

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
> [문서에서 "슬라이스 프리미티브"](/개발/펀크/stdlib/#슬라이스 프리미티브)
>
> ["preload_bits()" in docs](/develop/func/stdlib/#preload_bits)
>
> ["slice_bits()" in docs](/develop/func/stdlib/#slice_bits)

### 나만의 수정 방법을 정의하는 방법

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
> ["문서에서 메서드 수정하기"](/개발/펀크/스테이트먼트#메서드 수정하기)

### 숫자를 n의 거듭제곱으로 올리는 방법

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

### 사전을 반복하는 방법

딕셔너리는 많은 데이터로 작업할 때 매우 유용합니다. 내장 메서드 `dict_get_min?`과 `dict_get_max?`를 사용하여 각각 최소 및 최대 키 값을 얻을 수 있습니다. 또한 `dict_get_next?`를 사용하여 사전을 반복할 수 있습니다.

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
> [문서의 "딕셔너리 프리미티브"](/개발/펀크/스탠다드 라이브러리/#딕셔너리-프리미티브)
>
> ["dict_get_max?()" in docs](/develop/func/stdlib/#dict_get_max)
>
> ["dict_get_min?()" in docs](/develop/func/stdlib/#dict_get_min)
>
> ["dict_get_next?()" in docs](/develop/func/stdlib/#dict_get_next)
>
> ["dict_set()" in docs](/develop/func/stdlib/#dict_set)

### 사전에서 값을 삭제하는 방법

```func
cell names = new_dict();
names~udict_set(256, 27, "Alice");
names~udict_set(256, 25, "Bob");

names~udict_delete?(256, 27);

(slice val, int key) = names.udict_get?(256, 27);
~dump(val); ;; null() -> means that key was not found in a dictionary
```

### 셀 트리를 재귀적으로 반복하는 방법

아시다시피, 하나의 '셀'은 최대 '1023비트'의 데이터와 최대 '4개의 참조'를 저장할 수 있습니다. 이 한계를 극복하기 위해 셀 트리를 사용할 수 있지만, 이를 위해서는 적절한 데이터 처리를 위해 반복할 수 있어야 합니다.

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
> [문서의 "Lisp 스타일 목록"](/개발/펀크/스탠다드 라이브러리/#lisp-style-lists)
>
> ["null()" in docs](/develop/func/stdlib/#null)
>
> ["slice_refs()" in docs](/develop/func/stdlib/#slice_refs)

### 리스프 스타일 목록을 반복하는 방법

데이터 유형 튜플은 최대 255개의 값을 담을 수 있습니다. 이것으로 충분하지 않다면 리스프 스타일의 목록을 사용해야 합니다. 튜플 안에 튜플을 넣어 제한을 우회할 수 있습니다.

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
> [문서의 "Lisp 스타일 목록"](/개발/펀크/스탠다드 라이브러리/#lisp-style-lists)
>
> ["null()" in docs](/develop/func/stdlib/#null)

### 배포 메시지를 보내는 방법(stateInit만 사용, stateInit과 본문 포함)

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

### stateInit 셀을 빌드하는 방법

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

### 컨트랙트 주소를 계산하는 방법(stateInit 사용)

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

아래는 카운터를 증가시키고 스마트 컨트랙트 로직을 업데이트하는 기능이 있는 간단한 `СounterV1` 스마트 컨트랙트입니다.

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

스마트 컨트랙트를 작동한 후, 미터기 감소 기능이 누락되었다는 것을 알게 됩니다. 스마트 컨트랙트 'CounterV1'의 코드를 복사하고 '증가' 기능 옆에 새로운 '감소' 기능을 추가해야 합니다. 이제 코드가 다음과 같이 보입니다:

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

스마트 컨트랙트 `CounterV2`가 준비되면, 이를 오프체인에서 `셀`로 컴파일하고 `CounterV1` 스마트 컨트랙트로 업그레이드 메시지를 보내야 합니다.

```javascript
await contractV1.sendUpgrade(provider.sender(), {
    code: await compile('ContractV2'),
    value: toNano('0.05'),
});
```

> 💡 유용한 링크
>
> [기존 주소에 코드를 다시 배포할 수 있나요, 아니면 새 컨트랙트로 배포해야 하나요?(/develop/howto/faq#is-it-possible-to-re-deploy-code-to-an-existing-address-or-does-it-have-to-be-deployed-as-새-계약으로)](/개발/방법/질문)
>
> ["set_code()" in docs](/develop/func/stdlib#set_code)
