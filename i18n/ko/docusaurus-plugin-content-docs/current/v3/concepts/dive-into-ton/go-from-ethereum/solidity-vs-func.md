# Solidity vs FunC

스마트 컨트랙트 개발에는 이더리움을 위한 Solidity, TON을 위한 FunC와 같은 미리 정의된 언어의 사용이 포함됩니다.
Solidity는 C++, Python, JavaScript의 영향을 받은 객체 지향적, 고수준, 엄격한 타입의 언어로, 이더리움 블록체인 플랫폼에서 실행되는 스마트 컨트랙트를 작성하기 위해 특별히 설계되었습니다.

FunC 또한 TON 블록체인에서 스마트 컨트랙트를 프로그래밍하는 데 사용되는 고수준 언어로, 도메인 특화된, C와 유사한, 정적 타입의 언어입니다.

아래 섹션에서는 이러한 언어들의 데이터 타입, 저장소, 함수, 흐름 제어 구조, 그리고 딕셔너리(해시맵)와 같은 측면들을 간단히 분석할 것입니다.

## 저장소 레이아웃

Solidity는 평면적 저장소 모델을 제공하는데, 이는 모든 상태 변수가 저장소라고 불리는 단일의 연속적인 메모리 블록에 저장된다는 것을 의미합니다. 저장소는 키-값 저장소로, 각 키는 저장소 슬롯 번호를 나타내는 256비트(32바이트) 정수이며, 각 값은 해당 슬롯에 저장된 256비트 워드입니다. 슬롯은 0부터 시작하여 순차적으로 번호가 매겨지며, 각 슬롯은 단일 워드를 저장할 수 있습니다. Solidity는 프로그래머가 storage 키워드를 사용하여 상태 변수를 정의함으로써 저장소 레이아웃을 지정할 수 있게 합니다. 변수가 정의되는 순서가 저장소에서의 위치를 결정합니다.

TON 블록체인에서 영구 저장소 데이터는 cell로 저장됩니다. Cell은 스택 기반 TVM에서 메모리 역할을 합니다. Cell은 slice로 변환될 수 있으며, 그런 다음 slice로부터 데이터 비트와 다른 cell에 대한 참조를 로딩하여 cell로부터 얻을 수 있습니다. 데이터 비트와 다른 cell에 대한 참조는 builder에 저장될 수 있으며, 그런 다음 builder는 새로운 cell로 최종화될 수 있습니다.

## 데이터 타입

Solidity는 다음과 같은 기본 데이터 타입을 포함합니다:

- Signed/Unsigned integers
- 불리언
- Addresses - 이더리움 지갑이나 스마트 컨트랙트 주소를 저장하는 데 사용되며, 일반적으로 20바이트입니다. 주소 타입은 "payable" 키워드를 접미사로 가질 수 있으며, 이는 지갑 주소만 저장하고 transfer와 send 암호화폐 함수를 사용하도록 제한합니다.
- Byte arrays - "bytes" 키워드로 선언되며, 키워드와 함께 선언된 최대 32까지의 미리 정의된 수의 바이트를 저장하는 데 사용되는 고정 크기 배열입니다.
- Literals - 주소, 유리수와 정수, 문자열, 유니코드, 16진수와 같은 변수에 저장될 수 있는 불변의 값들입니다.
- Enums
- Arrays (정적/동적)
- Structs
- Mappings

FunC의 경우, 주요 데이터 타입은 다음과 같습니다:

- Integers
- Cell - TON의 기본적인 불투명 데이터 구조로, 최대 1,023비트와 최대 4개의 다른 cell에 대한 참조를 포함합니다
- Slice와 Builder - cell에서 읽고 쓰기 위한 특별한 객체들
- Continuation - 실행 가능한 TVM 바이트코드를 포함하는 cell의 또 다른 형태
- Tuples - 최대 255개의 구성 요소를 가진 순서가 있는 컬렉션으로, 임의의 값 타입을 가질 수 있으며, 가능한 한 구별됩니다.
- Tensors - (int, int) a = (2, 4)와 같이 대량 할당이 가능한 순서가 있는 컬렉션입니다. 텐서 타입의 특별한 경우는 단위 타입 ()입니다. 이는 함수가 어떤 값도 반환하지 않거나 인자가 없다는 것을 나타냅니다.

현재 FunC는 사용자 정의 타입 정의를 지원하지 않습니다.

### 참고

- [구문](/v3/documentation/smart-contracts/func/docs/statements)

## 변수 선언과 사용

Solidity는 정적 타입 언어로, 이는 각 변수가 선언될 때 그 타입이 지정되어야 함을 의미합니다.

```js
uint test = 1; // Declaring an unsigned variable of integer type
bool isActive = true; // Logical variable
string name = "Alice"; // String variable
```

FunC는 더 추상적이고 함수 지향적인 언어로, 동적 타입과 함수형 프로그래밍 스타일을 지원합니다.

```func
(int x, int y) = (1, 2); // A tuple containing two integer variables
var z = x + y; // Dynamic variable declaration 
```

### 참고

- [구문](/v3/documentation/smart-contracts/func/docs/statements)

## 반복문

Solidity는 `for`, `while`, 그리고 `do { ... } while` 반복문을 지원합니다.

만약 어떤 것을 10번 하고 싶다면, 다음과 같이 할 수 있습니다:

```js
uint x = 1;

for (uint i; i < 10; i++) {
    x *= 2;
}

// x = 1024
```

FunC는 `repeat`, `while`, 그리고 `do { ... } until` 반복문을 지원합니다. for 반복문은 지원되지 않습니다. 위 예시와 같은 코드를 FunC에서 실행하고 싶다면, `repeat`를 사용할 수 있습니다.

```func
int x = 1;
repeat(10) {
  x *= 2;
}
;; x = 1024
```

### 참고

- [구문](/v3/documentation/smart-contracts/func/docs/statements)

## 함수

Solidity는 명확성과 제어를 혼합하여 함수 선언에 접근합니다. 이 프로그래밍 언어에서 각 함수는 "function" 키워드로 시작하고, 그 뒤에 함수의 이름과 매개변수가 따라옵니다. 함수의 본문은 중괄호 안에 들어가며, 작동 범위를 명확히 정의합니다. 또한, 반환 값은 "returns" 키워드를 사용하여 표시됩니다. Solidity를 특별하게 만드는 것은 함수 가시성의 분류입니다 - 함수는 `public`, `private`, `internal`, 또는 `external`로 지정될 수 있으며, 이는 컨트랙트의 다른 부분이나 외부 엔티티에 의해 접근되고 호출될 수 있는 조건을 지시합니다. 아래는 Solidity 언어에서 전역 변수 `num`을 설정하는 예시입니다:

```js
function set(uint256 _num) public returns (bool) {
    num = _num;
    return true;
}
```

FunC로 넘어가면, FunC 프로그램은 본질적으로 함수 선언/정의와 전역 변수 선언의 목록입니다. FunC 함수 선언은 일반적으로 선택적 선언자로 시작하고, 그 뒤에 반환 타입과 함수 이름이 따라옵니다. 매개변수가 다음에 나열되며, 선언은 `impure`, `inline/inline_ref`, `method_id`와 같은 지정자들의 선택으로 끝납니다. 이러한 지정자들은 함수의 가시성, 컨트랙트 저장소를 수정하는 능력, 그리고 인라이닝 동작을 조정합니다. 아래는 FunC 언어에서 저장소 변수를 영구 저장소에 cell로 저장하는 예시입니다:

```func
() save_data(int num) impure inline {
  set_data(begin_cell()
            .store_uint(num, 32)
           .end_cell()
          );
}
```

### 참고

- [함수](/v3/documentation/smart-contracts/func/docs/functions)

## 흐름 제어 구조

C나 JavaScript에서 알려진 일반적인 의미를 가진 대부분의 제어 구조가 Solidity에서 사용 가능합니다. 여기에는 `if`, `else`, `while`, `do`, `for`, `break`, `continue`, `return`이 포함됩니다.

FunC는 고전적인 `if-else` 문과 함께 `ifnot`, `repeat`, `while`, `do/until` 반복문을 지원합니다. 또한 v0.4.0부터 `try-catch` 문도 지원됩니다.

### 참고

- [구문](/v3/documentation/smart-contracts/func/docs/statements)

## 딕셔너리

딕셔너리(hashmap/mapping) 데이터 구조는 Solidity와 FunC 컨트랙트 개발에서 매우 중요합니다. 이는 개발자들이 사용자의 잔액이나 자산 소유권과 같은 특정 키와 관련된 데이터를 스마트 컨트랙트에서 효율적으로 저장하고 검색할 수 있게 해주기 때문입니다.

매핑은 Solidity에서 키-값 쌍으로 데이터를 저장하는 해시 테이블로, 키는 참조 타입을 제외한 모든 내장 데이터 타입이 될 수 있으며, 데이터 타입의 값은 어떤 타입이든 될 수 있습니다. 매핑은 Solidity와 이더리움 블록체인에서 고유한 이더리움 주소를 해당하는 값 타입에 연결하는 데 가장 일반적으로 사용됩니다. 다른 프로그래밍 언어에서 매핑은 딕셔너리와 동일합니다.

Solidity에서 매핑은 길이가 없으며, 키나 값을 설정하는 개념도 없습니다. 매핑은 저장소 참조 타입으로 작용하는 상태 변수에만 적용 가능합니다. 매핑이 초기화될 때, 모든 가능한 키를 포함하며, 바이트 표현이 모두 0인 값에 매핑됩니다.

FunC에서 매핑의 유사물은 딕셔너리 또는 TON 해시맵입니다. TON의 맥락에서 해시맵은 cell의 트리로 표현되는 데이터 구조입니다. 해시맵은 빠른 조회와 수정이 가능하도록 키를 임의의 타입의 값에 매핑합니다. TVM에서 해시맵의 추상적 표현은 Patricia 트리, 또는 압축된 이진 트라이입니다. 잠재적으로 큰 cell 트리로 작업하는 것은 여러 문제를 만들 수 있습니다. 각 업데이트 작업은 상당한 수의 cell을 만들며(만들어진 각 cell은 500 gas를 소비), 이는 이러한 작업들이 부주의하게 사용될 경우 자원이 고갈될 수 있음을 의미합니다. 가스 한도를 초과하지 않기 위해, 단일 거래에서 딕셔너리 업데이트 수를 제한하세요. 또한, `N`개의 키-값 쌍을 위한 이진 트리는 `N-1`개의 분기를 포함하며, 이는 최소 `2N-1`개의 cell을 의미합니다. 스마트 컨트랙트의 저장소는 `65536`개의 고유한 cell로 제한되므로, 딕셔너리의 최대 항목 수는 `32768`개, 또는 반복되는 cell이 있는 경우 약간 더 많을 수 있습니다.

### 참고

- [TON의 딕셔너리](/v3/documentation/smart-contracts/func/docs/dictionaries)

## 스마트 컨트랙트 통신

Solidity와 FunC는 스마트 컨트랙트와 상호작용하는 서로 다른 접근 방식을 제공합니다. 주요 차이점은 컨트랙트 간의 호출과 상호작용 메커니즘에 있습니다.

Solidity는 컨트랙트가 메서드 호출을 통해 서로 상호작용하는 객체 지향적 접근 방식을 사용합니다. 이는 전통적인 객체 지향 프로그래밍 언어의 메서드 호출과 유사합니다.

```js
// External contract interface
interface IReceiver {
    function receiveData(uint x) external;
}

contract Sender {
    function sendData(address receiverAddress, uint x) public {
        IReceiver receiver = IReceiver(receiverAddress);
        receiver.receiveData(x);  // Direct call of the contract function
    }
}
```

TON 블록체인 생태계에서 사용되는 FunC는 스마트 컨트랙트 간의 호출과 상호작용을 위해 메시지를 사용합니다. 메서드를 직접 호출하는 대신, 컨트랙트들은 서로에게 데이터와 실행할 코드를 포함할 수 있는 메시지를 보냅니다.

스마트 컨트랙트 발신자가 숫자와 함께 메시지를 보내야 하고, 스마트 컨트랙트 수신자가 그 숫자를 받아 어떤 조작을 수행해야 하는 예시를 살펴보겠습니다.

먼저, 스마트 컨트랙트 수신자는 메시지를 어떻게 받을지 설명해야 합니다.

```func
() recv_internal(int my_balance, int msg_value, cell in_msg, slice in_msg_body) impure {
    int op = in_msg_body~load_uint(32);
    
    if (op == 1) {
        int num = in_msg_body~load_uint(32);
        ;; do some manipulations
        return ();
    }

    if (op == 2) {
        ;;...
    }
}
```

우리의 목적지 컨트랙트에서 메시지를 받는 것이 어떻게 생겼는지 더 자세히 살펴보겠습니다:

1. `recv_internal()` - 이 함수는 컨트랙트가 블록체인 내에서 직접 접근될 때 실행됩니다. 예를 들어, 컨트랙트가 우리의 컨트랙트에 접근할 때입니다.
2. 함수는 컨트랙트 잔액 금액, 들어오는 메시지의 금액, 원본 메시지가 있는 cell, 그리고 받은 메시지의 본문만 저장하는 `in_msg_body` slice를 받습니다.
3. 우리의 메시지 본문은 두 개의 정수를 저장합니다. 첫 번째 숫자는 32비트 부호 없는 정수 `op`로, 수행할 `operation` 또는 호출할 스마트 컨트랙트의 `method`를 식별합니다. Solidity와 유사성을 그려볼 수 있으며 `op`를 함수 서명처럼 생각할 수 있습니다. 두 번째 숫자는 우리가 조작해야 할 숫자입니다.
4. 결과 slice에서 `op`와 '우리의 숫자'를 읽기 위해 `load_uint()`를 사용합니다.
5. 다음으로, 우리는 숫자를 조작합니다(이 예시에서는 이 기능을 생략했습니다).

다음으로, 발신자의 스마트 컨트랙트가 메시지를 올바르게 보내야 합니다. 이는 직렬화된 메시지를 인자로 기대하는 `send_raw_message`로 수행됩니다.

```func
int num = 10;
cell msg_body_cell = begin_cell().store_uint(1,32).store_uint(num,32).end_cell();

var msg = begin_cell()
            .store_uint(0x18, 6)
            .store_slice("EQBIhPuWmjT7fP-VomuTWseE8JNWv2q7QYfsVQ1IZwnMk8wL"a) ;; in the example, we just hardcode the recipient's address
            .store_coins(0)
            .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1)
            .store_ref(msg_body_cell)
        .end_cell();

send_raw_message(msg, mode);
```

우리의 스마트 컨트랙트가 수신자에게 메시지를 보내는 것이 어떻게 생겼는지 더 자세히 살펴보겠습니다:

1. 초기에 우리는 메시지를 구축해야 합니다. 전송의 전체 구조는 [여기](/v3/documentation/smart-contracts/message-management/sending-messages)에서 찾을 수 있습니다. 여기서는 어떻게 조립하는지 자세히 다루지 않을 것이며, 링크에서 그것에 대해 읽을 수 있습니다.
2. 메시지의 본문은 cell을 나타냅니다. `msg_body_cell`에서 우리는 다음을 수행합니다: `begin_cell()` - 미래 cell을 위한 `Builder`를 생성, 첫 번째 `store_uint` - 첫 번째 uint를 `Builder`에 저장(1 - 이것이 우리의 `op`), 두 번째 `store_uint` - 두 번째 uint를 `Builder`에 저장(num - 이것이 수신 컨트랙트에서 조작할 우리의 숫자), `end_cell()` - cell을 생성.
3. `recv_internal`에서 오는 본문을 메시지에 첨부하기 위해, 우리는 `store_ref`로 메시지 자체에서 수집된 cell을 참조합니다.
4. 메시지 보내기.

이 예시는 스마트 컨트랙트가 서로 어떻게 통신할 수 있는지 보여주었습니다.

### 참고

- [내부 메시지](/v3/documentation/smart-contracts/message-management/internal-messages)
- [메시지 보내기](/v3/documentation/smart-contracts/message-management/sending-messages)
- [바운스 불가능 메시지](/v3/documentation/smart-contracts/message-management/non-bounceable-messages)
