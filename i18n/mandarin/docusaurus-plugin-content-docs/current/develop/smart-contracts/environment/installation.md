import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import Button from '@site/src/components/button'

# 预编译二进制文件

:::caution 重要
您不再需要手动安装Blueprint SDK的二进制文件。
:::

Blueprint SDK已提供所有开发和测试所需的二进制文件。

\<Button href="/develop/smart-contracts/sdk/javascript"
colorType="primary" sizeType={'sm'}>
迁移到Blueprint SDK </Button>

## 预编译二进制文件

如果您不使用Blueprint SDK进行智能合约开发，您可以使用适用于您的操作系统和工具选择的预编译二进制文件。

### 先决条件

对于在本地开发TON智能合约 _无需Javascript_，您需要在您的设备上准备`func`、`fift`和`lite client`的二进制文件。

您可以从下表中下载并设置它们，或阅读TON Society的这篇文章：

- [设置TON开发环境](https://blog.ton.org/setting-up-a-ton-development-environment)

### 1. 下载

从下表中下载二进制文件。请确保选择适合您操作系统的正确版本，并安装任何附加依赖项：

| 操作系统                               | TON二进制文件                                                                                  | fift                                                                                   | func                                                                                   | lite-client                                                                                   | 附加依赖项                                                                                                   |
| ---------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| MacOS x86-64                       | [下载](https://github.com/ton-blockchain/ton/releases/latest/download/ton-mac-x86-64.zip)   | [下载](https://github.com/ton-blockchain/ton/releases/latest/download/fift-mac-x86-64)   | [下载](https://github.com/ton-blockchain/ton/releases/latest/download/func-mac-x86-64)   | [下载](https://github.com/ton-blockchain/ton/releases/latest/download/lite-client-mac-x86-64)   |                                                                                                         |
| MacOS arm64                        | [下载](https://github.com/ton-blockchain/ton/releases/latest/download/ton-mac-arm64.zip)    |                                                                                        |                                                                                        |                                                                                               | `brew install openssl ninja libmicrohttpd pkg-config`                                                   |
| Windows x86-64                     | [下载](https://github.com/ton-blockchain/ton/releases/latest/download/ton-win-x86-64.zip)   | [下载](https://github.com/ton-blockchain/ton/releases/latest/download/fift.exe)          | [下载](https://github.com/ton-blockchain/ton/releases/latest/download/func.exe)          | [下载](https://github.com/ton-blockchain/ton/releases/latest/download/lite-client.exe)          | 安装 [OpenSSL 1.1.1](/ton-binaries/windows/Win64OpenSSL_Light-1_1_1q.msi) |
| Linux  x86_64 | [下载](https://github.com/ton-blockchain/ton/releases/latest/download/ton-linux-x86_64.zip) | [下载](https://github.com/ton-blockchain/ton/releases/latest/download/fift-linux-x86_64) | [下载](https://github.com/ton-blockchain/ton/releases/latest/download/func-linux-x86_64) | [下载](https://github.com/ton-blockchain/ton/releases/latest/download/lite-client-linux-x86_64) |                                                                                                         |
| Linux  arm64                       | [下载](https://github.com/ton-blockchain/ton/releases/latest/download/ton-linux-arm64.zip)  |                                                                                        |                                                                                        |                                                                                               | `sudo apt install libatomic1 libssl-dev`                                                                |

### 2. 设置您的二进制文件

export const Highlight = ({children, color}) => (
\<span
style={{
backgroundColor: color,
borderRadius: '2px',
color: '#fff',
padding: '0.2rem',
}}>
{children} </span>
);

<Tabs groupId="operating-systems">
  <TabItem value="win" label="Windows">

1. 下载后，您需要`创建`一个新文件夹。例如：**`C:/Users/%USERNAME%/ton/bin`**，并将安装的文件移动到那里。

2. 要打开Windows环境变量，请按键盘上的<Highlight color="#1877F2">Win + R</Highlight>按钮，键入`sysdm.cpl`，然后按Enter键。

3. 在“_高级_”选项卡上

4. In the _"User variables"_ section, select the "_Path_" variable and click <Highlight color="#1877F2">"Edit"</Highlight> (this is usually required).

5. To add a new value `(path)` to the system variable in the next window, click the  button <Highlight color="#1877F2">"New"</Highlight>.
   In the new field, you need to specify the path to the folder where the previously installed files are stored:

```
C:\Users\%USERNAME%\ton\bin\
```

6. 在_“用户变量”_部分，选择“_Path_”变量，然后点击<Highlight color="#1877F2">“编辑”</Highlight>（通常需要）。

```bash
C:\Users\%USERNAME%\ton\bin\
```

7. 要检查是否一切安装正确，请在终端运行（_cmd.exe_）：

   1. Download [fiftlib.zip](/ton-binaries/windows/fiftlib.zip)
   2. Open the zip in some directory on your machine (like **`C:/Users/%USERNAME%/ton/lib/fiftlib`**)
   3. Create a new (click button <Highlight color="#1877F2">"New"</Highlight>) environment variable `FIFTPATH` in "_User variables_" section.
   4. In the "_Variable value_" field, specify the path to the files: **`/%USERNAME%/ton/lib/fiftlib`** and click <Highlight color="#1877F2">OK</Highlight>. Done.

:::caution important
Instead of the `%USERNAME%` keyword, you must insert your own `username`.\
:::</TabItem>
<TabItem value="mac" label="Linux / MacOS">1. After downloading, make sure the downloaded binaries are executable by changing their permissions.```bash
chmod +x func
chmod +x fift
chmod +x lite-client
```2. It's also useful to add these binaries to your path (or copy them to `/usr/local/bin`) so you can access them from anywhere.```bash
cp ./func /usr/local/bin/func
cp ./fift /usr/local/bin/fift
cp ./lite-client /usr/local/bin/lite-client
```3. To check that everything was installed correctly, run in terminal.```bash
fift -V && func -V && lite-client -V
```4. If you plan to `use fift`, also download [fiftlib.zip](/ton-binaries/windows/fiftlib.zip), open the zip in some directory on your device (like `/usr/local/lib/fiftlib`), and set the environment variable `FIFTPATH` to point to this directory.```
unzip fiftlib.zip
mkdir -p /usr/local/lib/fiftlib
cp fiftlib/* /usr/local/lib/fiftlib
```:::info Hey, you're almost finished :)
Remember to set the [environment variable](https://stackoverflow.com/questions/14637979/how-to-permanently-set-path-on-linux-unix) `FIFTPATH` to point to this directory.
:::


<TabItem value="mac" label="Linux / MacOS">

1. After downloading, make sure the downloaded binaries are executable by changing their permissions.

```bash
chmod +x func
chmod +x fift
chmod +x lite-client
```

2. 下载后，请确保通过更改权限使下载的二进制文件可执行。

```bash
chmod +x func
chmod +x fift
chmod +x lite-client
```

3. 将这些二进制文件添加到您的路径中（或复制到`/usr/local/bin`），以便您可以在任何地方访问它们也是很有用的。

```bash
cp ./func /usr/local/bin/func
cp ./fift /usr/local/bin/fift
cp ./lite-client /usr/local/bin/lite-client
```

4. 要检查是否一切安装正确，请在终端运行。

```
fift -V && func -V && lite-client -V
```

:::info Hey, you're almost finished :)
Remember to set the [environment variable](https://stackoverflow.com/questions/14637979/how-to-permanently-set-path-on-linux-unix) `FIFTPATH` to point to this directory.
:::

  


## Build from source

If you don't want to rely on pre-compiled binaries and prefer to compile the binaries yourself, you can follow the [official instructions](/develop/howto/compile).

The ready-to-use gist instructions are provided below:

### Linux (Ubuntu / Debian)

```bash
sudo apt update
sudo apt install git make cmake g++ libssl-dev zlib1g-dev wget
cd ~ && git clone https://github.com/ton-blockchain/ton.git
cd ~/ton && git submodule update --init
mkdir ~/ton/build && cd ~/ton/build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j 4
```

## Linux（Ubuntu / Debian）

The core team provides automatic builds for several operating systems as [GitHub Actions](https://github.com/ton-blockchain/ton/releases/latest).

Click on the link above, choose the workflow on the left relevant to your operating system, click on a recent green passing build, and download `ton-binaries` under "Artifacts".
