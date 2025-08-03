import Feedback from '@site/src/components/Feedback';

# Tolk vs FunC：简而言之

Tolk is much more similar to TypeScript and Kotlin than C and Lisp.
But it still gives you complete control over the TVM assembler since it has a FunC kernel inside.

1. Functions are declared via `fun`, get methods via `get`, variables via `var`, immutable variables via `val`, putting types on the right; parameter types are mandatory; return type can be omitted (auto inferred), as well as for locals; specifiers `inline` and others are `@` attributes

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

2. No `impure`, it's by default, the Tolk compiler won't drop user function calls
3. 不是 `recv_internal` 和 `recv_external`，而是 `onInternalMessage` 和 `onExternalMessage` 。
4. `2+2` 是 4，不是标识符；标识符是字母数字；使用命名 `const OP_INCREASE` 而不是 `const op::increase`
5. 支持逻辑运算符 AND `&&`、OR `||`、NOT `!`
6. 语法改进
    - `;; comment` → `// comment`
    - `{- comment -}` → `/* comment */`
    - `#include` → `import`，严格规定 "用什么导入什么"
    - `~ found` → `!found`（显然只适用于真/假）（"true "为-1，就像在 FunC 中一样）
    - `v = null()` → `v = null`
    - `null?(v)` → `v == null`，`builder_null?` 等也是如此
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
    - `"..."c` → `stringCrc32("...")` (and other postfixes also)
7. 即使函数在下面声明，也可以被调用；不需要正向声明；编译器首先进行解析，然后进行符号解析；现在有了源代码的 AST 表示法
8. stdlib函数重命名为 ~~verbose~~ 清晰的名称，驼峰字体；现在是嵌入式的，而不是从GitHub下载的；它被分成几个文件；常用函数始终可用，更具体的可用 `import "@stdlib/tvm-dicts"`，IDE会建议您使用；这里是[一个映射](/v3/documentation/smart-contracts/tolk/tolk-vs-func/stdlib)
9. No `~` tilda methods; `cs.loadInt(32)` modifies a slice and returns an integer; `b.storeInt(x, 32)` modifies a builder; `b = b.storeInt()` also works since it is not only modifies but returns; chained methods work identically to JS, they return `self`; everything works exactly as expected, similar to JS; no runtime overhead, exactly same Fift instructions; custom methods are created with ease; tilda `~` does not exist in Tolk at all; [more details here](/v3/documentation/smart-contracts/tolk/tolk-vs-func/mutability)
10. Clear and readable error messages on type mismatch
11. `bool` type support
12. Indexed access `tensorVar.0` and `tupleVar.0` support
13. Nullable types `T?`, null safety, smart casts, operator `!`
14. Union types and pattern matching (for types and for expressions, switch-like behavior)
15. Type aliases are supported
16. Structures are supported
17. Generics are supported
18. Methods (as extension functions) are supported
19. Trailing comma is supported
20. Semicolon after the last statement in a block is optional
21. Fift output contains original .tolk lines as comments

#### 周边工具

- JetBrains 插件已存在
- VS 代码扩展 [已存在](https://github.com/ton-blockchain/tolk-vscode)
- blueprint 的 WASM 封装器 [已存在](https://github.com/ton-blockchain/tolk-js)
- 甚至还有从 FunC 到 Tolk 的转换器 [已存在](https://github.com/ton-blockchain/convert-func-to-tolk)

## See also

- [Tolk vs FunC：详细](/v3/documentation/smart-contracts/tolk/tolk-vs-func/in-detail)

<Feedback />

