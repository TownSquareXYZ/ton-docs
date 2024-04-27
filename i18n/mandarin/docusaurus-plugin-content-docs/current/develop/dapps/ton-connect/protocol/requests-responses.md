# 请求和回应

应用向钱包发送请求。 钱包向应用程序发送响应和事件。

```tsx
输入 AppMessage = ConnectRequest | AppRequest;

类型 WalletMessage = WalletResponse | WalletEvent;
```

### 应用清单

应用程序需要有它的清单才能将元信息传递到钱包中。 清单是一个 JSON 文件，名称为“tonconnect-manifest.json”，格式如下：

```json
Mr.
  "url": "<app-url>", // 必填
  "name": "<app-name>", // 需要
  "iconUrl": "<app-icon-url>", // 需要
  "termsOfUseUrl": "<terms-of-use-url>", // 可选
  "privacyPolicyUrl": "<privacy-policy-url>" // 可选
}
```

最佳做法是将清单放在您的应用根目录中，例如`https://myapp.com/tonconnect-manifest.json`。 它允许钱包更好地处理您的应用并改进连接到您的应用的 UX 。
请确保该清单通过 URL 提供给GET。

#### 字段描述

- `url` -- 应用程序 URL。 将用作DApp标识符。 将用于打开 DAppafter 点击钱包中的图标。 建议通过 url 不要关闭 slash ，例如'https://mydapp.com' 而不是 'https://mydapp.com/'。
- "name" -- 应用程序名称。 可能是简单的，将不会被用作标识符。
- `iconUrl` -- URL到应用程序图标。 必须是PNG, ICO, ... 格式。 不支持 SVG 图标。 完美地将URL传递到 180x180px PNG 图标。
- `terms sOfUseUrl` -- (可选) URL。 普通应用可选，但是放在守护者推荐应用列表中的应用所需。
- `privacyPolicyUrl` -- (可选) url 到隐私政策文档。 普通应用可选，但是放在守护者推荐应用列表中的应用所需。

### 正在启动连接

应用请求消息是 **InitialRequest**。

```tsx
type ConnectRequest = {
  manifestUrl: string;
  items: ConnectItem[], // data items to share with the app
}

// In the future we may add other personal items.
// Or, instead of the wallet address we may ask for per-service ID.
type ConnectItem = TonAddressItem | TonProofItem | ...;

type TonAddressItem = {
  name: "ton_addr";
}
type TonProofItem = {
  name: "ton_proof";
  payload: string; // arbitrary payload, e.g. nonce + expiration timestamp.
}
```

连接请求描述：

- `manifesturl`: 链接到应用的tonconnect-manifest.json
- `items`: 要与应用共享的数据项。

如果用户批准请求，钱包响应**ConnectEvent**消息。

```tsx
type ConnectEvent = ConnectEventSuccess | ConnectEventError;

type ConnectEventSuccess = {
  event: "connect";
  id: number; // increasing event counter
  payload: {
      items: ConnectItemReply[];
      device: DeviceInfo;   
  }
}
type ConnectEventError = {
  event: "connect_error",
  id: number; // increasing event counter
  payload: {
      code: number;
      message: string;
  }
}

type DeviceInfo = {
  platform: "iphone" | "ipad" | "android" | "windows" | "mac" | "linux";
  appName:      string; // e.g. "Tonkeeper"  
  appVersion:  string; // e.g. "2.3.367"
  maxProtocolVersion: number;
  features: Feature[]; // list of supported features and methods in RPC
                                // Currently there is only one feature -- 'SendTransaction'; 
}

type Feature = { name: 'SendTransaction', maxMessages: number } | // `maxMessages` is maximum number of messages in one `SendTransaction` that the wallet supports
        { name: 'SignData' };

type ConnectItemReply = TonAddressItemReply | TonProofItemReply ...;

// Untrusted data returned by the wallet. 
// If you need a guarantee that the user owns this address and public key, you need to additionally request a ton_proof.
type TonAddressItemReply = {
  name: "ton_addr";
  address: string; // TON address raw (`0:<hex>`)
  network: NETWORK; // network global_id
  publicKey: string; // HEX string without 0x
  walletStateInit: string; // Base64 (not url safe) encoded stateinit cell for the wallet contract
}

type TonProofItemReply = TonProofItemReplySuccess | TonProofItemReplyError;

type TonProofItemReplySuccess = {
  name: "ton_proof";
  proof: {
    timestamp: string; // 64-bit unix epoch time of the signing operation (seconds)
    domain: {
      lengthBytes: number; // AppDomain Length
      value: string;  // app domain name (as url part, without encoding) 
    };
    signature: string; // base64-encoded signature
    payload: string; // payload from the request
  }
}

type TonProofItemReplyError = {
  name: "ton_addr";
  error: {
      code: ConnectItemErrorCode;
      message?: string;
  }
}

enum NETWORK {
  MAINNET = '-239',
  TESTNET = '-3'
}
```

**Connect 事件错误代码：**

| 代码  | 描述       |
| --- | -------- |
| 0   | 未知错误     |
| 1   | 错误请求     |
| 2   | 找不到应用清单  |
| 3   | 应用清单内容错误 |
| 100 | 未知应用     |
| 300 | 用户拒绝连接   |

**连接项目错误代码：**

| 代码  | 描述     |
| --- | ------ |
| 0   | 未知错误   |
| 400 | 不支持此方法 |

如果钱包不支持请求的`ConnectItem` (例如"ton_proof")，它必须发送与请求的项目对应的 ConnectItemReply 的回复。
使用以下结构：

```ts
输入 ConnectItemReplyError = Power
  name: "<requested-connect-item-name>";
  错误: Power
      code: 400;
      message?: string;
  }
}
```

### 地址验证签名 (`ton_proof`)

如果需要`TonProofItem`，钱包证明了所选账户钥匙的所有权。 签名的消息绑定到：

- 唯一的前缀，将消息从链条中分离出来。 (`ton-connect`)
- 钱包地址。
- 应用域
- 签名时间戳
- 应用程序的自定义有效载荷(服务器可以放开它的开启，cookie id，过期时间)。

```
message = utf8_encode("ton-proof-item-v2") ++ 
          Address ++
          AppDomain ++
          Timestamp ++  
          Payload 
signature = Ed25519Signe (privkey, sha256(0xffff ++ utf8_encode("ton-connect") +sha256(message))
```

式中：

- `Address`是作为序列编码的钱包地址：
  - “工作链”：32位符号整数大院；
  - `hash`: 256位无符号整数大枚举;
- `AppDomain` 是长度++ EncoedDomainname
  - `Length` 是 utf-8 编码应用域名长度的32位值（字节）
  - `EncodeedDomainName` id `Length`-byte utf-8 编码的应用域名
- `Timestamp` 64 bit unix eoch 时间
- `Payload`是一个可变长的二进制字符串。

注意：有效载荷是变量长度不信任的数据。 为了避免使用不必要的长度前缀，我们只是把它放在信息中。

签名必须由公钥验证：

1. 首先，尝试通过 `get_public_key` 获取智能合同上的 `Address` 获取公钥。

2. 如果智能合约尚未部署，或者获取方法丢失，您需要：

   1. 解析 `TonAddressItemReply.walletStateInit` 并从stateInit获取公钥。 您可以比较`walletStateInit.code`和标准钱包合同代码，并根据找到的钱包版本解析数据。

   2. 检查`TonAddsItemReply.publicKey`等于获取的公钥

   3. 检查`TonAddressItemReply.walletStateInit.hash()`等于`TonAddressItemReply.address`。 `.hash()`是指BoC hash。

## 留言

- 从应用程序到钱包的所有消息都是操作的请求。
- 从钱包到应用程序的消息可以是对应用程序请求的响应，也可以是用户在钱包一侧动作触发的事件。

**可用操作：**

- 发送交易
- signData
- 断开连接

**可用事件：**

- 连接
- 连接错误
- 断开连接

### 结构

**所有应用请求都有以下结构(如json-rpc 2.0)**

```tsx
接口AppRequest v.
	method: string;
	params: string[];
	id: string;
}
```

位置

- `method`: 操作名称 ('sendTransaction', 'signMessage', ...)
- `params`: 操作特定参数的数组
- `id`：能够匹配请求和响应的更多标识符

**钱包消息是响应或事件。**

响应是一个格式为 json-rpc 2.0 响应的对象。 响应 'id' 必须匹配请求的 id。

钱包不接受没有超过该会话最后处理的请求ID的任何请求。

```tsx
type WalletResponse = WalletResponseSuccess | WalletResponseError;

interface WalletResponseSuccess {
    result: string;
    id: string;
}

interface WalletResponseError {
    error: { code: number; message: string; data?: unknown };
    id: string;
}
```

事件是一个属性`event`的对象，它等于事件名称、`id`正在增加事件计数器(**非**) 。 d`因为没有事件请求，以及`payload\` 包含事件额外数据。

```tsx
interface WalletEvent {
    event: WalletEventName;
    id: number; // increasing event counter
    payload: <event-payload>; // specific payload for each event
}

type WalletEventName = 'connect' | 'connect_error' | 'disconnect';
```

钱包在生成新事件时必须增加 id。 (下一个事件必须有 `id` > 前一个事件`id`)

DApp不接受任何ID不会超过该会话最后处理的事件ID的事件。

### 方法

#### 签名并发送交易

应用发送 **SendTransactionRequest**：

```tsx
interface SendTransactionRequest {
	method: 'sendTransaction';
	params: [<transaction-payload>];
	id: string;
}
```

<transaction-payload>为JSON的地方，具有以下属性：

- `valid_until` (整数, 可选)：unix 时间戳。 此时交易将是无效的。
- `network` (NetWORK, optional): DApp打算发送交易的网络 (主页或测试网)。 如果未设置，交易将被发送到钱包中当前设置的网络， 但这并不安全，DApp应始终努力建立网络。 如果设置了 `network` 参数，但钱包有不同的网络集合。 钱包应该显示警报，不要再发送此交易。
- `from` (字符串在`<wc>:<hex>`格式，可选) - DApp打算从其中发送交易的发件人地址。 如果未设置，钱包允许用户在交易批准时选择发送者地址。 如果设置了 `from` 参数，钱包应该不允许用户选择发件人的地址； 如果无法从指定地址发送，钱包应显示警报，不要再发送此交易。
- `messages` (消息线)：1-4 条从钱包合同发送的消息到其他帐户。 所有消息都是按顺序发送的，但是**钱包不能保证消息将以同样的顺序发送和执行**。

消息结构：

- `address` (字符串)：消息目标
- `amount` (十进制字符串)：要发送的纳米材料数量。
- `payload` (string base64, optional)：原始的一个单元格 BoC 编码在 Base64 。
- `stateInit` (string base64, optional): raw one-cell BoC encoded in Base64

#### 常见案件

1. 没有有效载荷，没有stateIn: 没有消息的简单传输。
2. 有效载荷前置32个零位, 没有stateIn: 简单传输文本消息。
3. 没有有效载荷，也没有预先设定32个零位；State Init存在：部署合同。

<details>
<summary>示例</summary>

```json5
{
  "valid_until": 1658253458,
  "network": "-239", // enum NETWORK { MAINNET = '-239', TESTNET = '-3'}
  "from": "0:348bcf827469c5fc38541c77fdd91d4e347eac200f6f2d9fd62dc08885f0415f",
  "messages": [
    {
      "address": "0:412410771DA82CBA306A55FA9E0D43C9D245E38133CB58F1457DFB8D5CD8892F",
      "amount": "20000000",
      "stateInit": "base64bocblahblahblah==" //deploy contract
    },{
      "address": "0:E69F10CC84877ABF539F83F879291E5CA169451BA7BCE91A37A5CED3AB8080D3",
      "amount": "60000000",
      "payload": "base64bocblahblahblah==" //transfer nft to new deployed account 0:412410771DA82CBA306A55FA9E0D43C9D245E38133CB58F1457DFB8D5CD8892F
    }
  ]
}
```

</details>

钱包回复 **SendTransactionResponse** :

```tsx
输入 SendTransactionResponse = SendTransactionResponseSuccess | SendTransactionResponseError; 

接口 SendTransactionResponsePoint
    result: <boc>;
    id: string;
	
}

接口 SendTransactionResponseErrorer Paper
   error: Power code: number; 消息：字符串}；
   id：字符串；
}
```

**错误代码：**

| 代码  | 描述      |
| --- | ------- |
| 0   | 未知错误    |
| 1   | 错误请求    |
| 100 | 未知应用    |
| 300 | 用户拒绝了交易 |
| 400 | 方法不支持   |

#### 标志数据(实验性)

> 警告：这是一种实验性方法，其签名可能会在将来改变

应用程序发送 **SignDataRequest**：

```tsx
接口 SignDataRequest
	方法: 'signData';
	参数: [<sign-data-payload>];
	id: string;
}
```

<sign-data-payload>为JSON的地方，具有以下属性：

- `schema_crc` (整数)：表示payload 单元格的布局，它反过来定义域分隔。
- `cell` (字符串，Base64 编码的单元)：包含根据TL-B定义的任意数据。
- `publicKey` (HEX string without 0x, optional): DApp打算签署数据的密钥对的公钥。 如果未设置，钱包不受密钥对签名的限制。 如果设置了 `publicKey` 参数，钱包SHOULD 可以通过对应此公钥的密钥签名； 如果无法使用指定的密钥对签名，钱包应显示警报，不要再登陆此数据。

签名将按以下方式计算：
`ed25519(schema_crc) ++ uint64be(timestamp) ++ cell_hash(X), privkey)`

[详情](https://github.com/oleganza/TEPs/blob/datasig/text/0000-data-signatures.md)

钱包应该按照schema_crc 解码单元格，并向用户显示相应的数据。
如果钱包未知schema_crc ，钱包应向用户显示危险通知/UI。

钱包响应**SignDataResponse**：

```tsx
type SignDataResponse = SignDataResponseSuccess | SignDataResponseError; 

interface SignDataResponseSuccess {
    result: {
      signature: string; // base64 encoded signature 
      timestamp: string; // UNIX timestamp in seconds (UTC) at the moment on creating the signature.
    };
    id: string;
}

interface SignDataResponseError {
   error: { code: number; message: string };
   id: string;
}
```

**错误代码：**

| 代码  | 描述      |
| --- | ------- |
| 0   | 未知错误    |
| 1   | 错误请求    |
| 100 | 未知应用    |
| 300 | 用户拒绝了请求 |
| 400 | 方法不支持   |

#### 断开操作

当用户在 dApp中断开钱包时，DApp应该通知钱包以帮助钱包保存资源并删除不必要的会话。
允许钱包更新其接口到断开状态。

```tsx
接口断开连接Request
	方法：'断开连接'；
	参数：[]；
	id：字符串；
}
```

钱包响应**断开连接**：

```ts
type DisconnectResponse = DisconnectResponseSuccess | DisconnectResponseError; 

interface DisconnectResponseSuccess {
    id: string;
    result: { };
}

interface DisconnectResponseError {
   error: { code: number; message: string };
   id: string;
}
```

当断开连接由 dApp 初始化时，钱包**shouldn't** 会释放一个“断开连接”事件。

**错误代码：**

| 代码  | 描述    |
| --- | ----- |
| 0   | 未知错误  |
| 1   | 错误请求  |
| 100 | 未知应用  |
| 400 | 方法不支持 |

### 钱包事件

<ins>断开</ins>

当用户删除钱包中的应用程序时触发事件。 应用程序必须对事件作出反应并删除已保存的会话。 如果用户在应用侧断开钱包连接，则事件不会触发，会话信息仍在本地存储

```tsx
interface DisconnectEvent {
	type: "disconnect",
	id: number; // increasing event counter
	payload: { }
}
```

<ins>连接</ins>

```tsx
type ConnectEventSuccess = {
    event: "connect",
    id: number; // increasing event counter
    payload: {
        items: ConnectItemReply[];
        device: DeviceInfo;
    }
}
type ConnectEventError = {
    event: "connect_error",
    id: number; // increasing event counter
    payload: {
        code: number;
        message: string;
    }
}
```
