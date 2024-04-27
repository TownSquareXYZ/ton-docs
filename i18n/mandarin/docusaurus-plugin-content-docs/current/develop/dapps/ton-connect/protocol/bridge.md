# Bridge API

桥是一个传输机制，可以将信息从应用程序传送到钱包，反之亦然。

- **Bridge由钱包提供商维护**。 应用开发者不必选择或构建桥。 每个钱包的桥都在 [wallets-list](https://github.com/ton-blockchain/wallets-list) 配置中列出。
- **消息是端到端加密。** 桥无法看到应用程序或钱包的内容或长期标识符。
- **通信是对称的。** 桥并不区分应用和钱包：两者都只是客户端。
- 桥将每个收件人**客户端ID**的消息单独列队列.

桥分为两种：

- [HTTP Bridge](#http-bridge): 用于外部应用和服务。
- [JS Bridge](#js-bridge)：对于在钱包中打开的应用，或者当钱包是浏览器扩展时。

## HTTP 桥接

ID **A** 的客户端连接桥以听取收到的请求。

**客户端ID是半私有的：** 应用程序和钱包不应该与其他实体分享他们的ID，以避免他们的消息意外被删除。

**客户端可以订阅少数客户端ID** - 在这种情况下，它应该以逗号分隔开列ID。 例如：`?client_id=<A1>,<A2>,<A3>`

```tsx
请求
    GET /events?client_id=<to_hex_str(A)>

    接受：文本/事件流
```

**订阅桥第二个(任何其他)时间**

```tsx
请求
    GET /events?client_id=<to_hex_str(A)>&last_event_id=<lastEventId>

    接受：文本/事件流
```

**lastEventId** - 最后一个 SSE 事件的事件的事件Id 已经到达桥上。 在这种情况下，钱包将获取上次连接后发生的所有事件。

从客户端A发送消息到客户端B。如果ttl太高，Bridge返回错误。

```tsx
请求
    POST /message?client_id=<to_hex_str(A)>?to=<to_hex_str(B)>&ttl=300&topic=<sendTransaction|signData>

    正体： <base64_encoded_message>
```

"topic" [optional] 查询参数可以被桥用来向钱包发送推送通知。 如果给出了参数，它必须与加密的`message`中调用的 RPC 方法相对应。

桥接缓冲消息到 TTL (秒)，但收到消息后立即将其移除。

如果TTL超过桥接服务器的硬限度，它应该使用 HTTP 400。 桥应至少支持300秒的 TTL。

当桥接收到客户端`A`发出的消息`base64_encoded_message`时，它生成了一条消息`BridgeMessage`：

```js
主席:
  "from": <to_hex_str(A)>,
  "消息": <base64_encoded_message>
}
```

通过 SSE 连接发送到客户端 B

```js
resB.write(BridgeMessage)
```

### Heartbeat

为了保持连接，桥接服务器应定期向SSE频道发送一个“心谱”消息。 客户端应忽略这种消息。
因此，桥的心跳消息是一个带有`心打`字的字符串。

## 通用链接

当应用程序启动连接时，它会直接通过二维码或通用链接发送到钱包。

```bash
https:///<wallet-universal-url>?
                               v=2&
                               id=<to_hex_str(A)>&
                               r=<urlsafe(json.stringify(ConnectRequest))>&
                               ret=back
```

参数 **v** 指定了协议版本。 钱包不接受不支持的版本。

参数 **id** 指定应用程序客户端ID编码为十六进制(没有 '0x' 前缀)。

参数 **r** 指定 URL-safe json [ConnectRequest](/develop/dapps/ton-connect/protocol/requests-responses#initiating-connecess)。

参数 **ret** (可选) 指定用户签署/拒绝请求时的离线返回策略。

- 'back' (默认) 意味着返回初始化Deeplink 跳跃的应用程序(例如浏览器、本机应用...),
- “无”表示用户操作后不跳跃；
- 一个 URL：在用户完成操作后，钱包将打开此URL。 注意，如果是一个网页，您不应该通过您的应用的 URL。 这个选项应该用于本地应用围绕可能的 OSspecific 问题使用 "back" 选项。

“ret”参数应该支持空的Deeplinks — — 它可以用于在其他动作确认后指定钱包行为 (发送交易) 。 符号阵列。 ……。

```bash
https://<wallet-universal-url>?ret=back
```

链接可能嵌入二维码或直接点击。

初始请求未加密，因为(1) 尚未传送个人数据。 (2) 应用程序甚至不知道钱包的身份。

### Unified deeplink `tc`

除了自己的通用链接外，钱包还必须支持统一的深度链接。

这允许应用程序创建一个单一的 qr 代码，可以用来连接到任何钱包。

更具体地说，钱包必须支持 `tc://` deeplink以及它自己的 \`<wallet-universal-url>'。

因此，下列“连接请求”必须由钱包处理：

```bash
tc://?
       v=2&
       id=<to_hex_str(A)>&
       r=<urlsafe(json.stringify(ConnectRequest))>&
       ret=back
```

## JS 桥

嵌入式应用程序通过注入的绑定窗口使用。<wallet-js-bridge-key>.tonconnect\`。

`wallet-js-bridge-key` 可以在 [wallets list](https://github.com/ton-blockchain/wallets-list) 中指定

JS bridge 运行于与钱包和应用程序相同的设备上，所以通信不会被加密。

应用程序直接使用纯文本请求和响应，无需会话键和加密。

```tsx
interface TonConnectBridge {
    deviceInfo: DeviceInfo; // see Requests/Responses spec
    walletInfo?: WalletInfo;
    protocolVersion: number; // max supported Ton Connect version (e.g. 2)
    isWalletBrowser: boolean; // if the page is opened into wallet's browser
    connect(protocolVersion: number, message: ConnectRequest): Promise<ConnectEvent>;
    restoreConnection(): Promise<ConnectEvent>;
    send(message: AppRequest): Promise<WalletResponse>;
    listen(callback: (event: WalletEvent) => void): () => void;
}
```

就像使用 HTTP 桥。 桥的钱包侧除了 [ConnectRequest](/develop/dapps/ton-connect/protocol/requests-responses#initiating-connection)之外没有收到应用程序请求，直到会话得到用户确认。 从技术上说，这些消息从网络视图传送到桥接控制器，但却被静默忽略。

设备周围的 **自动连接()** 和 **connect()** 为建立连接的无声和非无声尝试。

### 钱包信息(可选)

表示钱包元数据。 即使钱包未在 [wallets-list.json]中列出（https://github.com/ton-blockchain/wallets-list），也可以定义使可注入钱包与 TonConnect 兼容。

钱包元数据格式：

```ts
接口WalletInfo
    name: string;
    image; <png image url>;
    tondns?: string;
    about_url: <about page url>;
}
```

详细属性描述：https://github.com/ton-blockchain/wallets-list#entry-format

如果`TonConnectBridge.walletInfo`被定义，并且钱包已经被列出在 [wallets-list.json](https://github.com/ton-blockchain/wallets-list), `TonConnectBridge.walletInfo` 属性将覆盖钱包列表中相应的钱包属性。

### connect()

启动连接请求，这类似于使用 HTTP 桥时的QR/链接。

如果此应用先前被批准为当前帐户 — — 与连接事件静默连接。 否则会向用户显示确认对话框。

您不应该在没有明确的用户动作的情况下使用 `connect` 方法(例如连接按钮点击)。 如果你想要自动尝试恢复前一个连接，你应该使用 "restoreConnection" 方法。

### resturreConnection()

尝试恢复上一次连接。

如果此应用先前被批准用于当前帐户 — — 与新的 `ConnectEvent` 和一个 `ton_addr` 数据项无声连接。

否则返回 `ConnectEventError` 错误代码 100 (未知应用)。

### Send()

发送一个 [message](/develop/dapps/ton-connect/protocol/requests-responses#messages) 到桥， 排除ConnectRequest (在使用 HTTP 桥时进入二维码，并在使用 JS 桥时连接)。
直接通过 WalletResponse 返回许诺，您不需要等待 'listen' 响应；

### listen()

从钱包注册事件侦听器。

返回退订函数。

目前，只有"断开连接" 事件可用。 稍后将会有一个开关账户事件和其他钱包事件。
