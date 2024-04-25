# 语句

本节简要讨论构成普通函数体代码的 FunC 语句。

## 表达式语句

The most common type of a statement is the expression statement. It's an expression followed by `;`. Expression's description would be quite complicated, so only a sketch is presented here. As a rule all sub-expressions are computed left to right with one exception of [asm stack rearrangement](functions#rearranging-stack-entries) which may define order manually.

### 变量声明

不可能声明一个局部变量而不定义其初始值。

以下是一些变量声明的示例：

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

变量可以在同一作用域内“重新声明”。例如，以下是正确的代码： For example, this is a correct code:

```func
int x = 2;
int y = x + 1;
int x = 3;
```

事实上，`int x` 的第二次出现不是声明，而只是编译时确认 `x` 的类型为 `int`。因此第三行实际上等同于简单的赋值 `x = 3;`。 像这样定义时，它可以用作修改方法。以下将递增 `x`。

在嵌套作用域中，变量可以像在 C 语言中一样真正重新声明。例如，考虑以下代码： For example, consider the code:

```func
int x = 0;
int i = 0;
while (i < 10) {
  (int, int) x = (i, i + 1);
  ;; 这里 x 是类型为 (int, int) 的变量
  i += 1;
}
;; 这里 x 是类型为 int 的（不同）变量
```

但如在全局变量[章节](/develop/func/global_variables.md)中提到的，不允许重新声明全局变量。

请注意，变量声明**是**表达式语句，因此像 `int x = 2` 这样的结构实际上是完整的表达式。例如，以下是正确的代码： For example, this is a correct code:

```func
int y = (int x = 3) + 1;
```

它声明了两个变量 `x` 和 `y`，分别等于 `3` 和 `4`。

#### 下划线

Underscore `_` is used when a value is not needed. For example, suppose a function `foo` has type `int -> (int, int, int)`. We can get the first returned value and ignore the second and third like this:

```func
(int fst, _, _) = foo(42);
```

### 函数应用

A call of a function looks like as such in a conventional language. 函数调用看起来像在常规语言中那样。函数调用的参数在函数名之后列出，用逗号分隔。

```func
;; 假设 foo 的类型为 (int, int, int) -> int
int x = foo(1, 2, 3);
```

但请注意，`foo` 实际上是**一个**参数类型为 `(int, int, int)` 的函数。为了看到区别，假设 `bar` 是类型为 `int -> (int, int, int)` 的函数。与常规语言不同，你可以这样组合函数： 下划线 `_` 用于表示不需要的值。例如，假设函数 `foo` 的类型为 `int -> (int, int, int)`。我们可以获取第一个返回值并忽略第二个和第三个，如下所示： Unlike in conventional languages, you can compose the functions like that:

```func
int x = foo(bar(42));
```

而不是类似但更长的形式：

```func
(int a, int b, int c) = bar(42);
int x =

 foo(a, b, c);
```

也可以进行 Haskell 类型的调用，但不总是可行（稍后修复）：

```func
;; 假设 foo 的类型为 int -> int -> int -> int
;; 即它是柯里化的
(int a, int b, int c) = (1, 2, 3);
int x = foo a b c; ;; ok
;; int y = foo 1 2 3; 不会编译
int y = foo (1) (2) (3); ;; ok
```

### Lambda 表达式

暂不支持 Lambda 表达式。

### 方法调用

#### 非修改方法

If a function has at least one argument, it can be called as a non-modifying method. For example, `store_uint` has type `(builder, int, int) -> builder` (the second argument is the value to store, and the third is the bit length). `begin_cell` is a function that creates a new builder. The following codes are equivalent:

```func
builder b = begin_cell();
b = store_uint(b, 239, 8);
```

```func
builder b = begin_cell();
b = b.store_uint(239, 8);
```

因此，函数的第一个参数可以在函数名前传递给它，如果用 `.` 分隔。代码可以进一步简化： The code can be further simplified:

```func
builder b = begin_cell().store_uint(239, 8);
```

也可以进行多次方法调用：

```func
builder b = begin_cell().store_uint(239, 8)
                        .store_int(-1, 16)
                        .store_uint(0xff, 10);
```

#### 修改方法

如果函数的第一个参数的类型为 `A`，并且函数的返回值的形状为 `(A, B)`，其中 `B` 是某种任意类型，那么该函数可以作为修改方法调用。修改方法调用可以接受一些参数并返回一些值，但它们会修改其第一个参数，即将返回值的第一个组件赋值给第一个参数的变量。例如，假设 `cs` 是一个cell切片，`load_uint` 的类型为 `(slice, int) -> (slice, int)`：它接受一个cell切片和要加载的位数，并返回切片的剩余部分和加载的值。以下代码是等价的： Modifying method calls may take some arguments and return some values, but they modify their first argument, that is, assign the first component of the returned value to the variable from the first argument. For example, suppose `cs` is a cell slice and `load_uint` has type `(slice, int) -> (slice, int)`: it takes a cell slice and number of bits to load and returns the remainder of the slice and the loaded value. The following codes are equivalent:

```func
(cs, int x) = load_uint(cs, 8);
```

```func
(cs, int x) = cs.load_uint(8);
```

```func
int x = cs~load_uint(8);
```

In some cases we want to use a function as a modifying method that doesn't return any value and only modifies the first argument. 在某些情况下，我们希望将不返回任何值且只修改第一个参数的函数用作修改方法。可以使用cell类型如下操作：假设我们想定义类型为 `int -> int` 的函数 `inc`，它用于递增整数，并将其用作修改方法。然后我们应该将 `inc` 定义为类型为 `int -> (int, ())` 的函数： Then we should define `inc` as a function of type `int -> (int, ())`:

```func
(int, ()) inc(int x) {
  return (x + 1, ());
}
```

When defined like that, it can be used as a modifying method. The following will increment `x`.

```func
x~inc();
```

#### 函数名中的 `.` 和 `~`

假设我们也想将 `inc` 用作非修改方法。我们可以写类似以下内容： We can write something like that:

```func
(int y, _) = inc(x);
```

但可以覆盖 `inc` 作为修改方法的定义。

```func
int inc(int x) {
  return x + 1;
}
(int, ()) ~inc(int x) {
  return (x + 1, ());
}
```

然后这样调用它：

```func
x~inc();
int y = inc(x);
int z = x.inc();
```

第一次调用将修改 x；第二次和第三次调用不会。

总结一下，当以非修改或修改方法（即使用 `.foo` 或 `~foo` 语法）调用名为 `foo` 的函数时，如果存在 `.foo` 或 `~foo` 的定义，FunC 编译器将分别使用 `.foo` 或 `~foo` 的定义，如果没有，则使用 `foo` 的定义。

### Operators

Note that currently all of the unary and binary operators are integer operators. 请注意，目前所有的一元和二元运算符都是整数运算符。逻辑运算符表示为位整数运算符（参见[没有布尔类型](/develop/func/types#absence-of-boolean-type)）。

#### Unary operators

有两个一元运算符：

- `~` 是按位非（优先级 75）
- `-` 是整数取反（优先级 20）

它们应该与参数分开：

- `- x` 是可以的。
- `-x` 不可以（它是单个标识符）

#### 二元运算符

优先级为 30（左结合性）：

- `*` 是整数乘法
- `/` 是整数除法（向下取整）
- `~/` 是整数除法（四舍五入）
- `^/` 是整数除法（向上取整）
- `%` 是整数取模运算（向下取整）
- `~%` 是整数取模运算（四舍五入）
- `^%` 是整数取模运算（向上取整）
- `/%` 返回商和余数
- `&` 是按位与

优先级为 20（左结合性）：

- `+` 是整数加法
- `-` 是整数减法
- `|` 是按位或
- `^` is bitwise XOR

优先级为 17（左结合性）：

- `<<` 是按位左移
- `>>` 是按位右移
- `~>>` 是按位右移（四舍五入）
- `^>>` 是按位右移（向上取整）

优先级为 15（左结合性）：

- `==` 是整数等值检查
- `!=` 是整数不等检查
- `<` 是整数比较
- `<=` 是整数比较
- `>` 是整数比较
- `>=` 是整数比较
- `<=>` 是整数比较（返回 -1、0 或 1）

它们也应该与参数分开：

- `x + y` 是可以的
- `x+y` 不可以（它是单个标识符）

#### 条件运算符

它具有通常的语法。

```func
<condition> ? <consequence> : <alternative>
```

具有通常的语法。示例：

```func
x > 0 ? x * fac(x - 1) : 1;
```

优先级为 13。

#### Assignments

优先级 10。

简单赋值 `=` 以及二元运算的对应项：`+=`、`-=`、`*=`、`/=`、`~/=`、`^/=`、`%=`、`~%=`、`^%=`、`<<=`、`>>=`、`~>>=`、`^>>=`、`&=`、`|=`、`^=`。

## 循环

FunC 支持 `repeat`、`while` 和 `do { ... } until` 循环。不支持 `for` 循环。 The `for` loop is not supported.

### Repeat 循环

语法是 `repeat` 关键字后跟一个类型为 `int` 的表达式。指定次数重复代码。示例： Repeats the code for the specified number of times. 示例：

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

如果次数小于 `-2^31` 或大于 `2^31 - 1`，将抛出范围检查异常。

### While 循环

最常见的语句类型是表达式语句。它是一个表达式后跟 `;`。表达式的描述相当复杂，因此这里只提供一个概述。通常所有子表达式都是从左到右计算的，唯一的例外是[汇编堆栈重排](functions#rearranging-stack-entries)，它可能手动定义顺序。 赋值

```func
int x = 2;
while (x < 100) {
  x = x * x;
}
;; x = 256
```

请注意，条件 `x < 100` 的真值是类型为 `int` 的（参见[没有布尔类型](/develop/func/types#absence-of-boolean-type)）。

### Until 循环

具有以下语法：

```func
int x = 0;
do {
  x += 3;
} until (x % 17 == 0);
;; x = 51
```

## If 语句

示例：

```func
;; 通常的 if
if (flag) {
  do_something();
}
```

```func
;; 等同于 if (~ flag)
ifnot (flag) {
  do_something();
}
```

```func
;; 通常的 if-else
if (flag) {
  do_something();
}
else {
  do_alternative();
}
```

```func
;; 一些特定功能
if (flag1) {
  do_something1();
} else {
  do_alternative4();
}
```

The curly brackets are necessary. That code wouldn't be compiled:

```func
if (flag1)
  do_something();
```

## Try-Catch 语句

_自 func v0.4.0 起可用_

Executes the code in `try` block. 执行 `try` 块中的代码。如果失败，完全回滚在 `try` 块中所做的更改，并执行 `catch` 块；`catch` 接收两个参数：任何类型的异常参数（`x`）和错误代码（`n`，整数）。

与许多其他语言不同，在 FunC 的 try-catch 语句中，try 块中所做的更改，特别是局部和全局变量的修改，所有寄存器的更改（即 `c4` 存储寄存器、`c5` 操作/消息寄存器、`c7` 上下文寄存器等）**被丢弃**，如果 try 块中有错误，因此所有合约存储更新和消息发送将被撤销。需要注意的是，一些 TVM 状态参数，如 _codepage_ 和gas计数器不会回滚。这意味着，尤其是，try 块中花费的所有gas将被计入，以及改变gas限制的操作（`accept_message` 和 `set_gas_limit`）的效果将被保留。 It is important to note that some TVM state parameters such as _codepage_ and gas counters will not be rolled back. This means, in particular, that all gas spent in the try block will be taken into account, and the effects of OPs that change the gas limit (`accept_message` and `set_gas_limit`) will be preserved.

请注意，异常参数可以是任何类型（可能在不同异常情况下不同），因此 funC 无法在编译时预测它。这意味着开发者需要通过将异常参数转换为某种类型来“帮助”编译器（请参见下面的示例 2）： 花括号是必需的。以下代码将无法编译：

例如：

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
;; x = 0（而非 1）
```

## 区块语句

Block statements are also allowed. They open a new nested scope:

```func
int x = 1;
builder b = begin_cell();
{
  builder x = begin_cell().store_uint(0, 8);
  b = x;
}
x += 1;
```
