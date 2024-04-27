# 会话协议

会话协议定义客户端标识符，并为应用程序和钱包提供端到端加密。 这意味着HTTP桥完全不受信任，无法读取用户在应用程序和钱包之间传输的数据。 JS bridge不使用此协议，因为钱包和应用程序都在同一设备上运行。

## 定 义

### Client Keypair

用于NaCl “crypto_box”协议的X25519密钥配对。

```
a <-随机23 字节
A <-X25519Pubkey(s)
```

或

```
(a,A) <- nacl.box.keyPair()
```

### 客户端ID

[客户端密钥](#client-keypair) (32 bytes) 的公钥部分。

### 会议

会话由两对客户端ID来定义。 应用程序和钱包都创建了他们自己的[客户端IDs](#客户端-id)。

### 创建客户密钥对

```
(a,A) <- nacl.box.keyPair()
```

### 加密

来自应用程序的所有请求(初始请求除外)以及来自钱包的所有响应都是加密的。

给消息**m**、收件人[客户端ID](#客户端-id) **X** 和发送人的私钥**y** 的二进制编码：

```
nonce <- 随机(24字节)
ct <- nacl.box(m, nonce, X, y)
M <- nonce ++ ct
```

也就是说，最后消息**M** 的前24字节设置为随机失调。

### 解密文件

要解密消息**M**，收件人使用其私钥 **x** 和发送人的公钥 **Y** (aka [client ID](#client-id)):

```
nonce <-M[0..24]
ct <-M[24..]
m <-nacl.box.open(ct, nonce, Y, )
```

纯文本**m** 已被恢复并解析 [请求/响应](/develop/dapps/ton-connect/protocol/requests-responses#requests-and-responses)。
