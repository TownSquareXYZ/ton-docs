import Feedback from '@site/src/components/Feedback';

# ADNL TCP - liteserver

This is the low-level protocol that supports all interactions within the TON network. While it can operate on top of any protocol, it is most commonly used in conjunction with TCP and UDP. Typically, UDP facilitates communication between nodes, whereas TCP is employed for communication with liteservers.

In this section, we will analyze how ADNL operates over TCP and learn how to interact directly with liteservers.

In the TCP version of ADNL, network nodes utilize public keys (ed25519) as their addresses. Connections are established using a shared key obtained through the Elliptic Curve Diffie-Hellman (ECDH) procedure.

## Packet structure

除握手外，每个ADNL TCP数据包具有以下结构：

- 4 bytes of packet size in little-endian (N)
- 32字节随机数 [[?]](## "随机字节用于防止校验和攻击")
- (N - 64) 字节的有效载荷
- 32字节SHA256校验和，来自随机数和有效载荷

The entire packet, including its size, is encrypted using **AES-CTR**.

After decrypting the packet, you must verify that the checksum matches the data. To do this, simply calculate the checksum yourself and compare it to the checksum provided in the packet.

The handshake packet is an exception; it is transmitted partially unencrypted and is detailed in the next chapter.

## 建立连接

To establish a connection, we need to know the server's IP, port, and public key and generate our own private and public key, ed25519.

Public server data such as IP, port, and key can be obtained from the [global config](https://ton-blockchain.github.io/global.config.json). The IP in the config, which is numerical, can be converted to normal form using,(for example) [this tool](https://www.browserling.com/tools/dec-to-ip). The public key in the config is in base64 format.

客户端生成160个随机字节，其中一些将被双方用作AES加密的基础。

Two permanent AES-CTR ciphers are created, which the parties will use to encrypt/decrypt messages after the handshake.

- 密码A - 密钥为0 - 31字节，iv为64 - 79字节
- 密码B - 密钥为32 - 63字节，iv为80 - 95字节

The ciphers are utilized in the following order:

- 服务器使用密码A加密它发送的消息。
- Cipher A is used by the client to decrypt messages it receives.
- 客户端使用密码B加密它发送的消息。
- Cipher B is used by the server to decrypt messages it receives.

要建立连接，客户端必须发送一个包含以下内容的握手数据包：

- [32 bytes] **Server key ID** [[see details here]](#getting-key-id)
- [32字节] **我们的ed25519公钥**
- [32字节] **我们160字节的SHA256哈希**
- [160 bytes] **Our 160 bytes encrypted** [[see details here]](#handshake-packet-data-encryption)

When receiving a handshake packet, the server will do the same actions: receive an ECDH key, decrypt 160 bytes, and create 2 permanent keys. If everything works out, the server will respond with an empty ADNL packet, without payload, to decrypt which (as well as subsequent ones) we need to use one of the permanent ciphers.

从这一点开始，连接可以被视为已建立。

After we have established a connection, we can start receiving information; the TL language serializes data.

[Learn more about TL here](/v3/documentation/data-formats/tl).

## Ping and pong

最佳做法是每5秒发送一次ping数据包。这是在没有数据传输时保持连接的必要条件，否则服务器可能终止连接。

Like all the others, the ping packet is built according to the standard schema described [above](#packet-structure) and carries the request ID and ping ID as payload data.

Let's find the desired schema for the ping request [here](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L35) and calculate the schema id as `crc32_IEEE("tcp.ping random_id:long = tcp.Pong")`. When converted to little endian bytes, we get **9a2b084d**.

Therefore, our ADNL ping packet will look like this:

- 4 bytes of packet size in little-endian -> 64 + (4+8) = **76**
- 32字节随机数 -> 随机的32字节
- 4字节的ID TL模式 -> **9a2b084d**
- 8 bytes of request-id -> random uint64 number
- 32字节的SHA256校验和，来自随机数和有效载荷

我们发送我们的数据包并等待[tcp.pong](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L23)，`random_id`将与我们在ping数据包中发送的相同。

## Receiving information from a liteserver

All requests that are aimed at obtaining information from the blockchain are wrapped in [Liteserver query](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/lite_api.tl#L83) schema, which in turn is wrapped in [ADNL query](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/lite_api.tl#L22) schema.

- LiteQuery:
  `liteServer.query data:bytes = Object`, id **df068c79**
- ADNLQuery:
  `adnl.message.query query_id:int256 query:bytes = adnl.Message`, id **7af98bb4**

LiteQuery is passed inside ADNLQuery as `query:bytes`, and the final query is passed inside LiteQuery as `data:bytes`.

[Learn more about parsing encoding bytes in TL here](/v3/documentation/data-formats/tl).

### getMasterchainInfo

Since we already know how to generate TL packets for the lite API, we can request information about the current TON MasterChain block.

The MasterChain block is used in many further requests as an input parameter to indicate the state (moment) in which we need information.

We are looking for the [TL schema we require](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/lite_api.tl#L60), calculate its ID and build the packet:

- 小端模式下的4字节标签大小 -> 64 + (4+32+(1+4+(1+4+3)+3)) = **116**
- 32字节随机数 -> 随机的32字节
- 4字节的ID ADNLQuery模式 -> **7af98bb4**
- 32字节`query_id:int256` -> 随机的32字节
  - 1 字节数组大小 -> **12**
  - ID LiteQuery 模式的 4 个字节 -> **df068c79**
    - 1 字节数组大小 -> **4**
    - 4 个字节的 ID getMasterchainInfo 模式 -> **2ee6b589**
    - 3 个零字节填充（对齐至 8）
  - 3 个零字节填充（对齐至 16）
- 32 个字节的校验和 SHA256，来自 nonce 和 payload

数据包示例（十六进制）:

```
74000000                                                             -> packet size (116)
5fb13e11977cb5cff0fbf7f23f674d734cb7c4bf01322c5e6b928c5d8ea09cfd     -> nonce
  7af98bb4                                                           -> ADNLQuery
  77c1545b96fa136b8e01cc08338bec47e8a43215492dda6d4d7e286382bb00c4   -> query_id
    0c                                                               -> array size
    df068c79                                                         -> LiteQuery
      04                                                             -> array size
      2ee6b589                                                       -> getMasterchainInfo
      000000                                                         -> 3 bytes of padding
    000000                                                           -> 3 bytes of padding
ac2253594c86bd308ed631d57a63db4ab21279e9382e416128b58ee95897e164     -> sha256
```

我们预期收到的响应为[liteServer.masterchainInfo](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/lite_api.tl#L30)，包括last:[ton.blockIdExt](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/tonlib_api.tl#L51) state_root_hash:int256 和 init:[tonNode.zeroStateIdExt](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L359)。

收到的数据包与发送的数据包同样方式进行反序列化 - 具有相同算法，但方向相反，除了响应仅被[ADNLAnswer](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/lite_api.tl#L23)包裹。

解码响应后，我们得到如下形式的数据包：

```
20010000                                                                  -> packet size (288)
5558b3227092e39782bd4ff9ef74bee875ab2b0661cf17efdfcd4da4e53e78e6          -> nonce
  1684ac0f                                                                -> ADNLAnswer
  77c1545b96fa136b8e01cc08338bec47e8a43215492dda6d4d7e286382bb00c4        -> query_id (identical to request)
    b8                                                                    -> array size
    81288385                                                              -> liteServer.masterchainInfo
                                                                          last:tonNode.blockIdExt
        ffffffff                                                          -> workchain:int
        0000000000000080                                                  -> shard:long
        27405801                                                          -> seqno:int   
        e585a47bd5978f6a4fb2b56aa2082ec9deac33aaae19e78241b97522e1fb43d4  -> root_hash:int256
        876851b60521311853f59c002d46b0bd80054af4bce340787a00bd04e0123517  -> file_hash:int256
      8b4d3b38b06bb484015faf9821c3ba1c609a25b74f30e1e585b8c8e820ef0976    -> state_root_hash:int256
                                                                          init:tonNode.zeroStateIdExt 
        ffffffff                                                          -> workchain:int
        17a3a92992aabea785a7a090985a265cd31f323d849da51239737e321fb05569  -> root_hash:int256      
        5e994fcf4d425c0a6ce6a792594b7173205f740a39cd56f537defd28b48a0f6e  -> file_hash:int256
    000000                                                                -> 3 bytes of padding
520c46d1ea4daccdf27ae21750ff4982d59a30672b3ce8674195e8a23e270d21          -> sha256
```

### runSmcMethod

We already know how to get the MasterChain block, so now we can call any liteserver methods.

Let's analyze **runSmcMethod** - this is a method that calls a function from a smart contract and returns a result. Here we need to understand some new data types such as [TL-B](/v3/documentation/data-formats/tlb/tl-b-language), [Cell](/v3/documentation/data-formats/tlb/cell-boc#cell) and [BoC](/v3/documentation/data-formats/tlb/cell-boc#bag-of-cells).

要执行智能合约方法，我们需要构建并发送使用TL模式的请求：

```tlb
liteServer.runSmcMethod mode:# id:tonNode.blockIdExt account:liteServer.accountId method_id:long params:bytes = liteServer.RunMethodResult
```

并等待带有模式的响应：

```tlb
liteServer.runMethodResult mode:# id:tonNode.blockIdExt shardblk:tonNode.blockIdExt shard_proof:mode.0?bytes proof:mode.0?bytes state_proof:mode.1?bytes init_c7:mode.3?bytes lib_extras:mode.4?bytes exit_code:int result:mode.2?bytes = liteServer.RunMethodResult;
```

在请求中，我们看到以下字段：

- mode:# - uint32位掩码，指示我们希望在响应中看到的内容，例如，`result:mode.2?bytes`只有在索引为2的位设置为一时才会出现在响应中。
- id:tonNode.blockIdExt - our master block state that we got in the previous chapter.
- account:[liteServer.accountId](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/lite_api.tl#L27) - 工作链和智能合约地址数据。
- method_id:long - 8字节，其中写入了调用方法名称的crc16与XMODEM表+设置了第17位 [[计算]](https://github.com/xssnick/tonutils-go/blob/88f83bc3554ca78453dd1a42e9e9ea82554e3dd2/ton/runmethod.go#L16)
- params:bytes - [Stack](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/crypto/block/block.tlb#L783)以[BoC](/develop/data-formats/cell-boc#bag-of-cells)序列化，其中包含调用方法的参数。[[实现示例]](https://github.com/xssnick/tonutils-go/blob/88f83bc3554ca78453dd1a42e9e9ea82554e3dd2/tlb/stack.go)

例如，我们只需要`result:mode.2?bytes`，那么我们的 mode 将等于0b100，即4。在响应中，我们将获得：

- mode:# -> 发送的内容 - 4。
- id:tonNode.blockIdExt -> 我们的主区块，针对该区块执行了方法
- shardblk:tonNode.blockIdExt -> 托管合约账户的分片区块
- exit_code:int -> 4字节，是执行方法时的退出代码。如果一切顺利，则为0，如果不是，则等于异常代码。
- result:mode.2?bytes -> [Stack](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/crypto/block/block.tlb#L783)以[BoC](/develop/data-formats/cell-boc#bag-of-cells)序列化，其中包含方法返回的值。

让我们分析调用合约`EQBL2_3lMiyywU17g-or8N7v9hDmPCpttzBPE2isF2GTzpK4`的`a2`方法并获取结果：

FunC中的方法代码：

```func
(cell, cell) a2() method_id {
  cell a = begin_cell().store_uint(0xAABBCC8, 32).end_cell();
  cell b = begin_cell().store_uint(0xCCFFCC1, 32).end_cell();
  return (a, b);
}
```

填写我们的请求：

- `mode` = 4，我们只需要结果 -> `04000000`
- `id` = 执行getMasterchainInfo的结果
- `account` = 工作链 0 (4字节 `00000000`)，和int256 [从我们的合约地址获得](/develop/data-formats/tl-b#addresses)，即32字节 `4bdbfde5322cb2c14d7b83ea2bf0deeff610e63c2a6db7304f1368ac176193ce`
- `method_id` = 从`a2`[计算](https://github.com/xssnick/tonutils-go/blob/88f83bc3554ca78453dd1a42e9e9ea82554e3dd2/ton/runmethod.go#L16)得出的id -> `0a2e010000000000`
- `params:bytes` = 我们的方法不接受输入参数，因此我们需要传递一个空栈（`000000`，cell3字节 - 栈深度0）以[BoC](/develop/data-formats/cell-boc#bag-of-cells)序列化 -> `b5ee9c72010101010005000006000000` -> 序列化为字节并得到 `10b5ee9c72410101010005000006000000000000` 0x10 - 大小，在末尾的 3 字节是填充。

我们得到的响应是：

- `mode:#` -> 不感兴趣
- `id:tonNode.blockIdExt` -> 不感兴趣
- `shardblk:tonNode.blockIdExt` -> 不感兴趣
- `exit_code:int` -> 如果执行成功则为0
- `result:mode.2?bytes` -> [Stack](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/crypto/block/block.tlb#L783)包含方法返回的数据，以[BoC](/develop/data-formats/cell-boc#bag-of-cells)格式提供，我们将对其进行解包。

在`result`中我们收到`b5ee9c7201010501001b000208000002030102020203030400080ccffcc1000000080aabbcc8`，这是包含数据的[BoC](/develop/data-formats/cell-boc#bag-of-cells)。当我们反序列化它时，我们得到一个cell：

```json
32[00000203] -> {
  8[03] -> {
    0[],
    32[0AABBCC8]
  },
  32[0CCFFCC1]
}
```

If we parse it, we will get 2 values of the cell type, which our FunC method returns. The first 3 bytes of the root cell `000002` - is the depth of the stack, that is 2. This means that the method returned 2 values.

We continue parsing, the next 8 bits (1 byte) is the value type at the current stack level. For some types, it may take 2 bytes. Possible options can be seen in [schema](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/crypto/block/block.tlb#L766). In our case, we have `03`, which means:

```tlb
vm_stk_cell#03 cell:^Cell = VmStackValue;
```

Hence, the type of our value is - cell, and, according to the schema, it stores the value itself as a reference. However, if we look at the stack element storage schema:

```tlb
vm_stk_cons#_ {n:#} rest:^(VmStackList n) tos:VmStackValue = VmStackList (n + 1);
```

我们将看到第一个链接`rest:^(VmStackList n)` - 是栈中下一个值的cell，而我们的值`tos:VmStackValue`排在第二位，所以要获得我们需要的值，我们需要读取第二个链接，即`32[0CCFFCC1]` - 这是合约返回的第一个cell。

现在我们可以深入并获取栈中的第二个元素，我们通过第一个链接，现在我们有：

```json
8[03] -> {
    0[],
    32[0AABBCC8]
  }
```

我们重复相同的过程。第一个8位 = `03` - 即又是一个cell。第二个引用是值`32[0AABBCC8]`，由于我们的栈深度为2，我们完成了遍历。总体上，我们有2个值由合约返回 - `32[0CCFFCC1]`和`32[0AABBCC8]`。

请注意，它们的顺序是相反的。调用函数时也需要以相反的顺序传递参数，与我们在FunC代码中看到的顺序相反。

[Please see implementation example here](https://github.com/xssnick/tonutils-go/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/ton/runmethod.go#L24)

### getAccountState

要获取账户状态数据，如余额、代码和合约数据，我们可以使用[getAccountState](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/lite_api.tl#L68)。请求需要一个[最新的主链块](#getmasterchaininfo)和账户地址。响应中，我们将接收到TL结构[AccountState](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/lite_api.tl#L38)。

让我们分析AccountState TL模式：

```tlb
liteServer.accountState id:tonNode.blockIdExt shardblk:tonNode.blockIdExt shard_proof:bytes proof:bytes state:bytes = liteServer.AccountState;
```

- `id` - our master block, regarding which we got the data.
- `shardblk` - WorkChain shard block where our account is located, regarding which we received data.
- `shard_proof` - Merkle proof of a shard block.
- `proof` - Merkle proof of account status.
- `state` - [BoC](/develop/data-formats/cell-boc#bag-of-cells) TL-B [账户状态模式](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/crypto/block/block.tlb#L232)。

我们需要的所有数据都在state中，我们将对其进行分析。

例如，让我们获取账户`EQAhE3sLxHZpsyZ_HecMuwzvXHKLjYx4kEUehhOy2JmCcHCT`的状态，响应中的`state`将是（撰写本文时）：

```hex
b5ee9c720102350100051e000277c0021137b0bc47669b3267f1de70cbb0cef5c728b8d8c7890451e8613b2d899827026a886043179d3f6000006e233be8722201d7d239dba7d818134001020114ff00f4a413f4bcf2c80b0d021d0000000105036248628d00000000e003040201cb05060013a03128bb16000000002002012007080043d218d748bc4d4f4ff93481fd41c39945d5587b8e2aa2d8a35eaf99eee92d9ba96004020120090a0201200b0c00432c915453c736b7692b5b4c76f3a90e6aeec7a02de9876c8a5eee589c104723a18020004307776cd691fbe13e891ed6dbd15461c098b1b95c822af605be8dc331e7d45571002000433817dc8de305734b0c8a3ad05264e9765a04a39dbe03dd9973aa612a61f766d7c02000431f8c67147ceba1700d3503e54c0820f965f4f82e5210e9a3224a776c8f3fad1840200201200e0f020148101104daf220c7008e8330db3ce08308d71820f90101d307db3c22c00013a1537178f40e6fa1f29fdb3c541abaf910f2a006f40420f90101d31f5118baf2aad33f705301f00a01c20801830abcb1f26853158040f40e6fa120980ea420c20af2670edff823aa1f5340b9f2615423a3534e2a2d2b2c0202cc12130201201819020120141502016616170003d1840223f2980bc7a0737d0986d9e52ed9e013c7a21c2b2f002d00a908b5d244a824c8b5d2a5c0b5007404fc02ba1b04a0004f085ba44c78081ba44c3800740835d2b0c026b500bc02f21633c5b332781c75c8f20073c5bd0032600201201a1b02012020210115bbed96d5034705520db3c8340201481c1d0201201e1f0173b11d7420c235c6083e404074c1e08075313b50f614c81e3d039be87ca7f5c2ffd78c7e443ca82b807d01085ba4d6dc4cb83e405636cf0069006031003daeda80e800e800fa02017a0211fc8080fc80dd794ff805e47a0000e78b64c00015ae19574100d56676a1ec40020120222302014824250151b7255b678626466a4610081e81cdf431c24d845a4000331a61e62e005ae0261c0b6fee1c0b77746e102d0185b5599b6786abe06fedb1c68a2270081e8f8df4a411c4605a400031c34410021ae424bae064f613990039e2ca840090081e886052261c52261c52265c4036625ccd88302d02012026270203993828290111ac1a6d9e2f81b609402d0015adf94100cc9576a1ec1840010da936cf0557c1602d0015addc2ce0806ab33b50f6200220db3c02f265f8005043714313db3ced542d34000ad3ffd3073004a0db3c2fae5320b0f26212b102a425b3531cb9b0258100e1aa23a028bcb0f269820186a0f8010597021110023e3e308e8d11101fdb3c40d778f44310bd05e254165b5473e7561053dcdb3c54710a547abc2e2f32300020ed44d0d31fd307d307d33ff404f404d10048018e1a30d20001f2a3d307d3075003d70120f90105f90115baf2a45003e06c2170542013000c01c8cbffcb0704d6db3ced54f80f70256e5389beb198106e102d50c75f078f1b30542403504ddb3c5055a046501049103a4b0953b9db3c5054167fe2f800078325a18e2c268040f4966fa52094305303b9de208e1638393908d2000197d3073016f007059130e27f080705926c31e2b3e63006343132330060708e2903d08308d718d307f40430531678f40e6fa1f2a5d70bff544544f910f2a6ae5220b15203bd14a1236ee66c2232007e5230be8e205f03f8009322d74a9802d307d402fb0002e83270c8ca0040148040f44302f0078e1771c8cb0014cb0712cb0758cf0158cf1640138040f44301e201208e8a104510344300db3ced54925f06e234001cc8cb1fcb07cb07cb3ff400f400c9
```

[Parse this BoC](/v3/documentation/data-formats/tlb/cell-boc#bag-of-cells) and get:

<details>
  <summary>large cell</summary>

```json
473[C0021137B0BC47669B3267F1DE70CBB0CEF5C728B8D8C7890451E8613B2D899827026A886043179D3F6000006E233BE8722201D7D239DBA7D818130_] -> {
  80[FF00F4A413F4BCF2C80B] -> {
    2[0_] -> {
      4[4_] -> {
        8[CC] -> {
          2[0_] -> {
            13[D180],
            141[F2980BC7A0737D0986D9E52ED9E013C7A218] -> {
              40[D3FFD30730],
              48[01C8CBFFCB07]
            }
          },
          6[64] -> {
            178[00A908B5D244A824C8B5D2A5C0B5007404FC02BA1B048_],
            314[085BA44C78081BA44C3800740835D2B0C026B500BC02F21633C5B332781C75C8F20073C5BD00324_]
          }
        },
        2[0_] -> {
          2[0_] -> {
            84[BBED96D5034705520DB3C_] -> {
              112[C8CB1FCB07CB07CB3FF400F400C9]
            },
            4[4_] -> {
              2[0_] -> {
                241[AEDA80E800E800FA02017A0211FC8080FC80DD794FF805E47A0000E78B648_],
                81[AE19574100D56676A1EC0_]
              },
              458[B11D7420C235C6083E404074C1E08075313B50F614C81E3D039BE87CA7F5C2FFD78C7E443CA82B807D01085BA4D6DC4CB83E405636CF0069004_] -> {
                384[708E2903D08308D718D307F40430531678F40E6FA1F2A5D70BFF544544F910F2A6AE5220B15203BD14A1236EE66C2232]
              }
            }
          },
          2[0_] -> {
            2[0_] -> {
              323[B7255B678626466A4610081E81CDF431C24D845A4000331A61E62E005AE0261C0B6FEE1C0B77746E0_] -> {
                128[ED44D0D31FD307D307D33FF404F404D1]
              },
              531[B5599B6786ABE06FEDB1C68A2270081E8F8DF4A411C4605A400031C34410021AE424BAE064F613990039E2CA840090081E886052261C52261C52265C4036625CCD882_] -> {
                128[ED44D0D31FD307D307D33FF404F404D1]
              }
            },
            4[4_] -> {
              2[0_] -> {
                65[AC1A6D9E2F81B6090_] -> {
                  128[ED44D0D31FD307D307D33FF404F404D1]
                },
                81[ADF94100CC9576A1EC180_]
              },
              12[993_] -> {
                50[A936CF0557C14_] -> {
                  128[ED44D0D31FD307D307D33FF404F404D1]
                },
                82[ADDC2CE0806AB33B50F60_]
              }
            }
          }
        }
      },
      872[F220C7008E8330DB3CE08308D71820F90101D307DB3C22C00013A1537178F40E6FA1F29FDB3C541ABAF910F2A006F40420F90101D31F5118BAF2AAD33F705301F00A01C20801830ABCB1F26853158040F40E6FA120980EA420C20AF2670EDFF823AA1F5340B9F2615423A3534E] -> {
        128[DB3C02F265F8005043714313DB3CED54] -> {
          128[ED44D0D31FD307D307D33FF404F404D1],
          112[C8CB1FCB07CB07CB3FF400F400C9]
        },
        128[ED44D0D31FD307D307D33FF404F404D1],
        40[D3FFD30730],
        640[DB3C2FAE5320B0F26212B102A425B3531CB9B0258100E1AA23A028BCB0F269820186A0F8010597021110023E3E308E8D11101FDB3C40D778F44310BD05E254165B5473E7561053DCDB3C54710A547ABC] -> {
          288[018E1A30D20001F2A3D307D3075003D70120F90105F90115BAF2A45003E06C2170542013],
          48[01C8CBFFCB07],
          504[5230BE8E205F03F8009322D74A9802D307D402FB0002E83270C8CA0040148040F44302F0078E1771C8CB0014CB0712CB0758CF0158CF1640138040F44301E2],
          856[DB3CED54F80F70256E5389BEB198106E102D50C75F078F1B30542403504DDB3C5055A046501049103A4B0953B9DB3C5054167FE2F800078325A18E2C268040F4966FA52094305303B9DE208E1638393908D2000197D3073016F007059130E27F080705926C31E2B3E63006] -> {
            112[C8CB1FCB07CB07CB3FF400F400C9],
            384[708E2903D08308D718D307F40430531678F40E6FA1F2A5D70BFF544544F910F2A6AE5220B15203BD14A1236EE66C2232],
            504[5230BE8E205F03F8009322D74A9802D307D402FB0002E83270C8CA0040148040F44302F0078E1771C8CB0014CB0712CB0758CF0158CF1640138040F44301E2],
            128[8E8A104510344300DB3CED54925F06E2] -> {
              112[C8CB1FCB07CB07CB3FF400F400C9]
            }
          }
        }
      }
    }
  },
  114[0000000105036248628D00000000C_] -> {
    7[CA] -> {
      2[0_] -> {
        2[0_] -> {
          266[2C915453C736B7692B5B4C76F3A90E6AEEC7A02DE9876C8A5EEE589C104723A1800_],
          266[07776CD691FBE13E891ED6DBD15461C098B1B95C822AF605BE8DC331E7D45571000_]
        },
        2[0_] -> {
          266[3817DC8DE305734B0C8A3AD05264E9765A04A39DBE03DD9973AA612A61F766D7C00_],
          266[1F8C67147CEBA1700D3503E54C0820F965F4F82E5210E9A3224A776C8F3FAD18400_]
        }
      },
      269[D218D748BC4D4F4FF93481FD41C39945D5587B8E2AA2D8A35EAF99EEE92D9BA96000]
    },
    74[A03128BB16000000000_]
  }
}
```

</details>

现在我们需要根据TL-B结构解析cell：

```tlb
account_none$0 = Account;

account$1 addr:MsgAddressInt storage_stat:StorageInfo
          storage:AccountStorage = Account;
```

我们的结构引用了其他结构，例如：

```tlb
anycast_info$_ depth:(#<= 30) { depth >= 1 } rewrite_pfx:(bits depth) = Anycast;
addr_std$10 anycast:(Maybe Anycast) workchain_id:int8 address:bits256  = MsgAddressInt;
addr_var$11 anycast:(Maybe Anycast) addr_len:(## 9) workchain_id:int32 address:(bits addr_len) = MsgAddressInt;
   
storage_info$_ used:StorageUsed last_paid:uint32 due_payment:(Maybe Grams) = StorageInfo;
storage_used$_ cells:(VarUInteger 7) bits:(VarUInteger 7) public_cells:(VarUInteger 7) = StorageUsed;
  
account_storage$_ last_trans_lt:uint64 balance:CurrencyCollection state:AccountState = AccountStorage;

currencies$_ grams:Grams other:ExtraCurrencyCollection = CurrencyCollection;
           
var_uint$_ {n:#} len:(#< n) value:(uint (len * 8)) = VarUInteger n;
var_int$_ {n:#} len:(#< n) value:(int (len * 8)) = VarInteger n;
nanograms$_ amount:(VarUInteger 16) = Grams;  
           
account_uninit$00 = AccountState;
account_active$1 _:StateInit = AccountState;
account_frozen$01 state_hash:bits256 = AccountState;
```

As we can see, the cell contains a lot of data, but we will analyze the main cases and get a balance. You can analyze the rest in a similar way.

让我们开始解析。在根cell数据中，我们有：

```
C0021137B0BC47669B3267F1DE70CBB0CEF5C728B8D8C7890451E8613B2D899827026A886043179D3F6000006E233BE8722201D7D239DBA7D818130_
```

转换为二进制形式并获取：

```
11000000000000100001000100110111101100001011110001000111011001101001101100110010011001111111000111011110011100001100101110110000110011101111010111000111001010001011100011011000110001111000100100000100010100011110100001100001001110110010110110001001100110000010011100000010011010101000100001100000010000110001011110011101001111110110000000000000000000000110111000100011001110111110100001110010001000100000000111010111110100100011100111011011101001111101100000011000000100110
```

Let's look at our main TL-B structure, we see that we have two options for what can be there - `account_none$0` or `account$1`. We can understand which option we have by reading the prefix declared after the symbol $, in our case it is 1 bit. If there is 0, then we have `account_none`, or 1, then `account`.

我们上面的数据中的第一个bit=1，所以我们正在处理`account$1`，将使用模式：

```tlb
account$1 addr:MsgAddressInt storage_stat:StorageInfo
          storage:AccountStorage = Account;
```

Next, we have `addr:MsgAddressInt`, we see that for MsgAddressInt we also have several options:

```tlb
addr_std$10 anycast:(Maybe Anycast) workchain_id:int8 address:bits256  = MsgAddressInt;
addr_var$11 anycast:(Maybe Anycast) addr_len:(## 9) workchain_id:int32 address:(bits addr_len) = MsgAddressInt;
```

To determine which structure to work with, we follow a similar approach as last time by reading the prefix bits. This time, we read 2 bits. After processing the first bit, we have `1000000...` remaining. Reading the first 2 bits yields `10`, indicating that we are working with `addr_std$10`.

Next, we encounter `anycast:(Maybe Anycast)`. The "Maybe" indicates that we should read 1 bit; if it's 1, we read `Anycast`; if it's 0, we skip it. After processing, our remaining bits are `00000...`. We read 1 bit and find it to be 0, so we skip reading `Anycast`.

Now, we move on to `workchain_id: int8`. This is straightforward— we read 8 bits to obtain the WorkChain ID. The next 8 bits are all zeros, so the WorkChain ID is 0.

Following this, we read `address: bits256`, which consists of 256 bits for the address, similar to how we handled the `workchain_id`. Upon reading, we receive `21137B0BC47669B3267F1DE70CBB0CEF5C728B8D8C7890451E8613B2D8998270` in hexadecimal representation.

Next, we read the address `addr: MsgAddressInt` and then proceed to `storage_stat: StorageInfo` from the main structure. Its schema is:

```tlb
storage_info$_ used:StorageUsed last_paid:uint32 due_payment:(Maybe Grams) = StorageInfo;
```

First, we have `used:StorageUsed`, along with its schema:

```tlb
storage_used$_ cells:(VarUInteger 7) bits:(VarUInteger 7) public_cells:(VarUInteger 7) = StorageUsed;
```

This is the number of cells and bits used to store account data. Each field is defined as `VarUInteger 7`, which means a uint of dynamic size, but a maximum of 7 bits. You can understand how it is arranged according to the schema:

```tlb
var_uint$_ {n:#} len:(#< n) value:(uint (len * 8)) = VarUInteger n;
```

在我们的案例中，n将等于7。在len中，我们将有`(#< 7)`，这意味着可以容纳最多7的数字的位数。你可以通过将7-1=6转换为二进制形式 - `110`，我们得到3个位，所以长度len = 3个位。而value是`(uint (len * 8))`。要确定它，我们需要读取3个位的长度，得到一个数字并乘以8，这将是`value`的大小，也就是需要读取的位数以获取VarUInteger的值。

读取`cells:(VarUInteger 7)`，取我们根cell的下一个位，看接下来的16个位以理解，这是`0010011010101000`。我们读取前3个位，这是`001`，即1，我们得到大小(uint (1 \* 8))，我们得到uint 8，我们读取8个位，它将是`cells`，`00110101`，即十进制中的53。对于 `bits` 和 `public_cells`，我们做同样的操作。

我们成功读取了`used:StorageUsed`，接下来我们有`last_paid:uint32`，我们读取32个位。`due_payment:(Maybe Grams)`在这里也很简单，Maybe将是0，所以我们跳过Grams。但是，如果Maybe是1，我们可以看看Grams的`amount:(VarUInteger 16) = Grams`模式并立即理解我们已经知道如何处理这个。像上次一样，只是我们有16而不是7。

接下来我们有`storage:AccountStorage`，它的模式是：

```tlb
account_storage$_ last_trans_lt:uint64 balance:CurrencyCollection state:AccountState = AccountStorage;
```

我们读取`last_trans_lt:uint64`，这是64个位，存储最后一次账户交易的lt。最后是余额，由模式表示：

```tlb
currencies$_ grams:Grams other:ExtraCurrencyCollection = CurrencyCollection;
```

From here we will read `grams:Grams` which will be the account balance in nano-tones. `grams:Grams` is `VarUInteger 16`, to store 16 (in binary form `10000`, subtracting 1 we get `1111`), then we read the first 4 bits, and multiply the resulting value by 8, then we read the received number of bits, it is our balance.

让我们根据我们的数据分析剩余的位：

```
100000000111010111110100100011100111011011101001111101100000011000000100110
```

读取前4个位 - `1000`，这是8。8\*8=64，读取接下来的64个位 = `0000011101011111010010001110011101101110100111110110000001100000`，去掉额外的零位，我们得到`11101011111010010001110011101101110100111110110000001100000`，即等于`531223439883591776`，将 nano 转换为TON，我们得到`531223439.883591776`。

我们将在这里停止，因为我们已经分析了所有主要情况，其余的可以以与我们已分析的类似的方式获得。此外，关于解析TL-B的更多信息可以在[官方文档](/develop/data-formats/tl-b-language)中找到。

### 其他方法

After studying all the information, you can call and process responses for other liteserver methods using the same principle.

## 握手的其他技术细节

### 获取密钥ID

密钥ID是序列化TL模式的SHA256哈希。

最常用的TL模式密钥是：

```tlb
pub.ed25519 key:int256 = PublicKey -- ID c6b41348
pub.aes key:int256 = PublicKey     -- ID d4adbc2d
pub.overlay name:bytes = PublicKey -- ID cb45ba34
pub.unenc data:bytes = PublicKey   -- ID 0a451fb6
pk.aes key:int256 = PrivateKey     -- ID 3751e8a5
```

As an example, for keys of type ed25519 that are used for handshake, the key ID will be the SHA256 hash from **[0xC6, 0xB4, 0x13, 0x48]** and **public key**, (36 byte array, prefix + key).

[Please see code example](https://github.com/xssnick/tonutils-go/blob/2b5e5a0e6ceaf3f28309b0833cb45de81c580acc/liteclient/crypto.go#L16).

### 握手数据包数据加密

握手数据包以半开放形式发送，只有160字节被加密，包含有关永久密码的信息。

要加密它们，我们需要一个AES-CTR密码，我们需要160字节的SHA256哈希和[ECDH共享密钥](#使用ECDH获取共享密钥)

密码构建如下：

- key = （公钥的0 - 15字节）+（哈希的16 - 31字节）
- iv = （哈希的0 - 3字节）+（公钥的20 - 31字节）

密码组装后，我们用它加密我们的160字节。

[Please see code example](https://github.com/xssnick/tonutils-go/blob/2b5e5a0e6ceaf3f28309b0833cb45de81c580acc/liteclient/connection.go#L361).

### 使用ECDH获取共享密钥

要计算共享密钥，我们需要我们的私钥和服务器的公钥。

DH的本质是获取共享的密钥，而不暴露私人信息。我将给出一个这是如何发生的示例，以最简化的形式。假设我们需要生成我们和服务器之间的共享密钥，过程将如下：

- 我们生成secret和公共数字，如**6**和**7**
- 服务器生成secret和公共数字，如**5**和**15**
- 我们与服务器交换公共数字，发送**7**给服务器，它发送给我们**15**。
- 我们计算：**7^6 mod 15 = 4**
- 服务器计算：**7^5 mod 15 = 7**
- 我们交换收到的数字，我们给服务器**4**，它给我们**7**
- 我们计算**7^6 mod 15 = 4**
- 服务器计算：**4^5 mod 15 = 4**
- 共享密钥 = **4**

为了简洁起见，将省略ECDH本身的细节。它是通过在曲线上找到一个共同点，使用两个密钥，私钥和公钥来计算的。如果感兴趣，最好单独阅读。

[Please see code example](https://github.com/xssnick/tonutils-go/blob/2b5e5a0e6ceaf3f28309b0833cb45de81c580acc/liteclient/crypto.go#L32).

## 参考资料

Here is a [link to the original article](https://github.com/xssnick/ton-deep-doc/blob/master/ADNL-TCP-Liteserver.md) - *[Oleg Baranov](https://github.com/xssnick)*.

<Feedback />

