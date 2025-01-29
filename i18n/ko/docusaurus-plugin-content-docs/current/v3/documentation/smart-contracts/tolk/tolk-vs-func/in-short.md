# Tolk vs FunC: 요약

Tolk는 C와 Lisp보다 TypeScript와 Kotlin에 훨씬 더 유사합니다.
하지만 내부에 FunC 커널이 있어 TVM 어셈블러를 완전히 제어할 수 있습니다.

1. 함수는 `fun`으로, get 메서드는 `get`으로, 변수는 `var`로(불변은 `val`로) 선언되며, 타입은 오른쪽에 위치; 매개변수 타입은 필수; 반환 타입은 생략 가능(자동 추론), 로컬 변수도 마찬가지; `inline` 등의 지정자는 `@` 속성

```tolk
global storedV: int;

fun parseData(cs: slice): cell {
    var flags: int = cs.loadMessageFlags();
    ...
}

@inline
fun sum(a: int, b: int) {   // auto inferred int
    val both = a + b;       // same
    return both;
}

get currentCounter(): int { ... }
```

2. `impure` 없음, 기본값이며, 컴파일러는 사용자 함수 호출을 삭제하지 않음
3. `recv_internal`과 `recv_external` 대신 `onInternalMessage`와 `onExternalMessage` 사용
4. `2+2`는 식별자가 아닌 4; 식별자는 알파벳과 숫자만 가능; `const op::increase` 대신 `const OP_INCREASE` 같은 이름 사용
5. 논리 연산자 AND `&&`, OR `||`, NOT `!` 지원
6. 구문 개선:
   - `;; comment` → `// comment`
   - `{- comment -}` → `/* comment */`
   - `#include` → `import`, "사용하는 것을 임포트하세요" 엄격 규칙과 함께
   - `~ found` → `!found` (true/false만 해당) (true는 FunC처럼 -1)
   - `v = null()` → `v = null`
   - `null?(v)` → `v == null`, `builder_null?` 등도 동일
   - `~ null?(v)` → `c != null`
   - `throw(excNo)` → `throw excNo`
   - `catch(_, _)` → `catch`
   - `catch(_, excNo)` → `catch(excNo)`
   - `throw_unless(excNo, cond)` → `assert(cond, excNo)`
   - `throw_if(excNo, cond)` → `assert(!cond, excNo)`
   - `return ()` → `return`
   - `do ... until (cond)` → `do ... while (!cond)`
   - `elseif` → `else if`
   - `ifnot (cond)` → `if (!cond)`
7. 함수는 아래에 선언되어 있어도 호출 가능; 전방 선언 불필요; 컴파일러는 먼저 구문 분석 후 심볼 해결; 소스 코드의 AST 표현 존재
8. stdlib 함수들이 ~~장황한~~ 명확한 이름과 camelCase 스타일로 변경; 이제 GitHub에서 다운로드하지 않고 내장됨; 여러 파일로 분할; 일반 함수는 항상 사용 가능, 더 특수한 함수는 `import "@stdlib/tvm-dicts"`로 사용 가능, IDE가 제안; [매핑 보기](/v3/documentation/smart-contracts/tolk/tolk-vs-func/stdlib)
9. `~` 틸다 메서드 없음; `cs.loadInt(32)`는 slice를 수정하고 정수를 반환; `b.storeInt(x, 32)`는 builder를 수정; `b = b.storeInt()`도 작동, 수정뿐만 아니라 반환도 하기 때문; 연결된 메서드는 JS와 동일하게 작동하여 `self` 반환; 모든 것이 JS와 유사하게 예상대로 정확히 작동; 런타임 오버헤드 없음, 정확히 동일한 Fift 명령어; 커스텀 메서드 쉽게 생성; 틸다 `~`는 Tolk에 전혀 존재하지 않음; [자세한 내용](/v3/documentation/smart-contracts/tolk/tolk-vs-func/mutability)
10. 타입 불일치 시 명확하고 읽기 쉬운 오류 메시지
11. `bool` 타입 지원

#### 관련 도구

- JetBrains 플러그인 존재
- VS Code 확장 [존재](https://github.com/ton-blockchain/tolk-vscode)
- blueprint용 WASM 래퍼 [존재](https://github.com/ton-blockchain/tolk-js)
- FunC에서 Tolk로의 변환기도 [존재](https://github.com/ton-blockchain/convert-func-to-tolk)

#### 다음 단계

[Tolk vs FunC: 상세](/v3/documentation/smart-contracts/tolk/tolk-vs-func/in-detail)
