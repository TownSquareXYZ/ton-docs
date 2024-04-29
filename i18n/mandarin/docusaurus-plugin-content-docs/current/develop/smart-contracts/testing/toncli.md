# 使用toncli

:::tip 初学者提示
如果您之前没有使用过toncli，请尝试[快速入门指南](https://github.com/disintar/toncli/blob/master/docs/quick_start_guide.md)。
:::

## 使用toncli进行测试

`toncli`使用FunC来测试智能合约。此外，最新版本支持Docker，用于快速环境设置。

本教程将帮助您测试智能合约的功能，以确保项目正常工作。

描述使用toncli进行测试的最佳教程是：

- [FunC测试如何工作？](https://github.com/disintar/toncli/blob/master/docs/advanced/func_tests_new.md)
- [如何用toncli调试交易？](https://github.com/disintar/toncli/blob/master/docs/advanced/transaction_debug.md)

## 在toncli下的FunC测试结构

为了测试我们的智能合约，我们需要编写2个函数。其中一个接受值，包含期望的结果，并在被测试的函数不正确工作时给出错误。

### 让我们创建一个包含测试的文件

在`tests`文件夹中创建名为`example.func`的文件，在其中编写我们的测试。

### 数据函数

通常，测试函数不接受参数，但必须返回它们。

- **函数选择器** - 测试合约中被调用函数的id；
- **元组** - （栈）我们将传递给执行测试的函数的值；
- **c4 cell** - 控制寄存器c4中的"永久数据"；
- **c7元组** - 控制寄存器c7中的"临时数据"；
- \*\* gas 限制整数\*\* -  gas 限制（要理解 gas 的概念，我建议您首先阅读以太坊中的相关内容）；

:::info 关于 gas

您可以详细阅读[这里](https://ton-blockchain.github.io/docs/#/smart-contracts/fees)。完整细节在[附录A](https://ton-blockchain.github.io/docs/tvm.pdf)。

关于寄存器c4和c7的更多信息[这里](https://ton-blockchain.github.io/docs/tvm.pdf)在1.3.1
:::

## 让我们开始为我们的智能合约编写测试

### 介绍

在新测试中，测试是通过两个函数进行的，这些函数允许调用智能合约方法：

- `invoke_method`，假设不会抛出异常
- `invoke_method_expect_fail`，假设会抛出异常

这些是测试函数内的函数，可以返回任意数量的值，所有这些值都将在运行测试时显示在报告中。

:::info 重要！
值得注意的是，每个测试函数名称必须以`_test`开头。
:::

### 创建测试函数

让我们称我们的测试函数为`__test_example()`，它将返回消耗的 gas 量，因此它是`int`。

```js
int __test_example() {

}
```

### 更新寄存器c4

由于我们将进行大量测试，需要频繁更新`c4`寄存器，因此我们将创建一个辅助函数，它将将`c4`写为零

```js
() set_default_initial_data() impure {
  set_data(begin_cell().store_uint(0, 64).end_cell());
}
```

- `begin_cell()` - 将为未来的 cell创建一个构造器
- `store_uint()` - 写入总量的值
- `end_cell()`- 创建cell
- `set_data()` - 将cell写入寄存器c4

`impure`是一个关键词，表示该函数更改了智能合约数据。

我们得

到一个将在测试函数主体中使用的函数

```js
int __test_example() {
	set_default_initial_data();

}
```

### Test Methods

It is worth noting that in the new version of the tests, we have the ability to call several smart contract methods in the testing function.

值得注意的是，在新版本的测试中，我们有能力在测试函数中调用几个智能合约方法。

在我们的测试中，我们将调用`recv_internal()`方法和Get方法，所以我们将通过消息增加c4中的值，并立即检查该值是否已更改为发送的值。

```js
int __test_example() {
	set_default_initial_data();
	cell message = begin_cell().store_uint(10, 32).end_cell();
}
```

After this step, we are going to use the `invoke_method` method.

此后，我们将使用`invoke_method`方法。

- method name
- arguments to test as a `tuple`

Two values ​​are returned: the gas used and the values ​​returned by the method (as a tuple).

:::info It's worth noting
Two values ​​are returned: the gas used and the values ​​returned by the method (as a tuple).
:::

In the first call, the arguments will be `recv_internal` and a tuple with a message transformed into a slice using `begin_parse()`

```js
var (int gas_used1, _) = invoke_method(recv_internal, [message.begin_parse()]);
```

For the record, let's store the amount of gas used in int `gas_used1`.

为了记录，让我们将使用的 gas 量存储在`int gas_used1`中。

```js
var (int gas_used2, stack) = invoke_method(get_total, []);
```

For the report, we also store the amount of gas used in `int gas_used2`, plus the values ​​that the method returns, to check later that everything worked correctly.

为了报告，我们还将使用的 gas 量存储在`int gas_used2`中，以及方法返回的值，以便稍后检查一切是否正确。

```js
int __test_example() {
	set_default_initial_data();

	cell message = begin_cell().store_uint(10, 32).end_cell();
	var (int gas_used1, _) = invoke_method(recv_internal, [message.begin_parse()]);
	var (int gas_used2, stack) = invoke_method(get_total, []);

}
```

Now, finally, the most important step. We have to check if our smart contract is working properly.

现在，最后，最重要的步骤。我们必须检查我们的智能合约是否正常工作。

```js
[int total] = stack; 
throw_if(101, total != 10); 
```

**Explanations:**

- Passing a tuple
- In the first argument, the number of the error (101), which we will receive if the smart contract does not work correctly
- In the second argument is the correct answer

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

This is the whole test, very convenient.
