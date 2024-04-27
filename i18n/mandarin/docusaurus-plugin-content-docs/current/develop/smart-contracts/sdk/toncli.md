# 使用toncli

_toncli—The Open Network跨平台智能合约命令行界面。_

易于部署和与TON智能合约交互。

`toncli`使用FunC来测试智能合约。此外，最新版本支持Docker，用于快速环境设置。

- [GitHub库](https://github.com/disintar/toncli)

## 快速开始 📌

以下是使用toncli库制作的教程：

- [快速开始指南](https://github.com/disintar/toncli/blob/master/docs/quick_start_guide.md) — 部署示例智能合约到TON的简单步骤。
- [TON Learn: FunC旅程概览。第1部分](https://blog.ton.org/func-journey)
- [TON Learn: FunC旅程概览。第2部分](https://blog.ton.org/func-journey-2)
- [TON Learn: FunC旅程概览。第3部分](https://blog.ton.org/func-journey-3)
- [TON Learn: 10个从零到英雄的课程](https://github.com/romanovichim/TonFunClessons_Eng) ([俄语版本](https://github.com/romanovichim/TonFunClessons_ru))

## 安装 💾

### 让我们创建一个包含测试的文件

- Docker镜像预构建可在[此处](https://hub.docker.com/r/trinketer22/func_docker/)找到
- 带有说明的Docker文件可在[此处](https://github.com/Trinketer22/func_docker)找到

### 数据函数

1. 下载必要的特殊预构建（使用最新构建）

- **函数选择器** - 测试合约中被调用函数的id；
- **元组** - （栈）我们将传递给执行测试的函数的值；

:::info 关于 gas
要下载必要的文件，您必须登录您的账户
:::

2. 安装[Python3.9](https://www.python.org/downloads/)或更高版本

3. 在终端运行`pip install toncli`或`pip3 install toncli`

:::tip 可能的错误
如果您看到`WARNING: The script toncli is installed in '/Python/3.9/bin' which is not on PATH`，则将bin的完整路径添加到PATH环境变量中
:::

4. 运行`toncli`并传递第一步中的`func/fift/lite-client`的绝对路径

### 介绍

1. 从[此处](https://github.com/SpyCheese/ton/actions/workflows/win-2019-compile.yml?query=branch%3Atoncli-local)下载必要的特殊预构建（使用最新构建）

:::info 下载特殊预构建提示
要下载必要的文件，您必须登录您的账户
:::

2. 安装[Python3.9](https://www.python.org/downloads/)或更高版本

:::info 重要！
值得注意的是，每个测试函数名称必须以`_test`开头。
:::

3. 以管理员身份打开终端并通过安装`toncli`来`pip install toncli`

4. 解压下载的存档并将[libcrypto-1_1-x64.dll](https://disk.yandex.ru/d/BJk7WPwr_JT0fw)添加到解压文件中

5. 为Windows用户打开文件夹：

让我们称我们的测试函数为`__test_example()`，它将返回消耗的 gas 量，因此它是`int`。

- 右键单击，打开终端

**Windows 10**:

- 在资源管理器中复制路径，然后在终端运行`cd 全路径`

## 创建项目 ✏️

这些是在TON中部署示例智能合约的简单步骤。
您可以在[此处](https://github.com

### Step-by-step guide

1. Open the terminal as an administrator and go to your project folder

2. To create a project, run `toncli start YOUR-PROJECT-NAME`

3. Go to the project folder `cd YOUR-PROJECT-NAME`

:::info Result

- build
- func
- fift
- test
  :::

4. build

## 测试方法

值得注意的是，在新版本的测试中，我们有能力在测试函数中调用几个智能合约方法。

```bash
toncli start nft_colletion/jetton_minter/nft_item/jetton_wallet
```

要调用`recv_internal()`方法，我们需要创建一个带有消息的cell。

## To test smart contracts using toncli, go to [testing](/develop/smart-contracts/testing/toncli)

## 要使用toncli测试智能合约，请前往[测试](/develop/smart-contracts/testing/toncli)

这个方法接受两个参数：

1. 方法名称
2. 作为`tuple`的测试参数
3. [Multiple contracts](https://github.com/disintar/toncli/blob/master/docs/advanced/multiple_contracts.md)
4. [Send boc with fift](https://github.com/disintar/toncli/blob/master/docs/advanced/send_boc_with_fift.md)
5. [Project structure](https://github.com/disintar/toncli/blob/master/docs/advanced/project_structure.md)
6. [Interesting features](https://github.com/disintar/toncli/blob/master/docs/advanced/intresting_features.md)
7. [Send internal fift messages](https://github.com/disintar/toncli/blob/master/docs/advanced/send_fift_internal.md)
8. [How does the FunC test work?](https://github.com/disintar/toncli/blob/master/docs/advanced/func_tests_new.md)
9. [How to debug transactions with toncli?](https://github.com/disintar/toncli/blob/master/docs/advanced/transaction_debug.md)
10. [Dockerfile for FunC testing GitHub repository](https://github.com/Trinketer22/func_docker)
