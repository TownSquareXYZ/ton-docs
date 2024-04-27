# DHT

DHT代表分布式哈希表，本质上是一个分布式的键值数据库，其中网络的每个成员都可以存储某些内容，例如，关于自己的信息。

TON中的DHT实现与IPFS中使用的[Kademlia](https://codethechange.stanford.edu/guides/guide_kademlia.html)的实现本质上类似。任何网络成员都可以运行一个DHT节点，生成密钥并存储数据。为此，他需要生成一个随机ID并通知其他节点自己的存在。

为了确定在哪个节点上存储数据，使用了一种确定节点与密钥之间“距离”的算法。算法很简单：我们取节点的ID和密钥的ID，执行XOR操作。值越小，节点越近。任务是尽可能接近密钥的节点上存储密钥，以便其他网络参与者可以使用同样的算法，找到可以给出此密钥数据的节点。

## 通过密钥查找值

让我们看一个查找密钥的示例，[连接到任何DHT节点并通过ADNL UDP建立连接](/develop/network/adnl-udp#packet-structure-and-communication)。

例如，我们想找到托管foundation.ton站点的节点的地址和公钥。假设我们已经通过执行DNS合约的Get方法获得了该站点的ADNL地址。ADNL地址的十六进制表示为`516618cf6cbe9004f6883e742c9a2e3ca53ed02e3e36f4cef62a98ee1e449174`。现在我们的目标是找到拥有此地址的节点的ip、端口和公钥。

为此，我们需要获取DHT密钥的ID，首先我们将填充DHT密钥模式：

```tlb
dht.key id:int256 name:bytes idx:int = dht.Key
```

`name`是密钥类型，对于ADNL地址使用“address”，例如，要搜索分片链节点 - 使用“nodes”。但密钥类型可以是任何字节数组，取决于您正在查找的值。

填写此模式，我们得到：

```
8fde67f6                                                           -- TL ID dht.key
516618cf6cbe9004f6883e742c9a2e3ca53ed02e3e36f4cef62a98ee1e449174   -- 我们搜索的ADNL地址
07 61646472657373                                                  -- 密钥类型，word “address”作为TL字节数组
00000000                                                           -- 索引0因为只有1个密钥
```

接下来 - 从上面序列化的字节获取DHT密钥ID的sha256哈希。它将是`b30af0538916421b46df4ce580bf3a29316831e0c3323a7f156df0236c5b2f75`

现在我们可以开始搜索。为此，我们需要执行一个具有[模式](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L197)的查询：

```tlb
dht.findValue key:int256 k:int = dht.ValueResult
```

`key`是我们DHT密钥的id，`k`是搜索的“宽度”，它越小，搜索越精确，但可查询的潜在节点越少。TON节点的最大k为10，通常使用6。

我们填充这个结构，序列化并发送请求，使用`adnl.message.query`模式。[您可以在另一篇文章中阅读更多关于此的内容](/develop/network/adnl-udp#packet-structure-and-communication)。

作为回应，我们可以得到：

- `dht.valueNotFound` - 如果未找到值。
- `dht.valueFound` - 如果此节点上找到了值。

##### dht.valueNotFound

如果我们得到`dht.valueNotFound`，响应将包含我们请求的节点所知并且尽可能接近我们请求的密钥的节点列表。在这种情况下，我们需要连接并将收到的节点添加到我们已知的列表中。
之后，从我们已知的所有节点列表中选择最接近、可访问且尚未请求的节点，并对其进行相同的请求。如此反复，直到我们尝试了我们选择的范围内的所有节点或直到我们不再收到新节点为止。

让我们更详细地分析响应字段，使用的模式：

```tlb
adnl.address.udp ip:int port:int = adnl.Address;
adnl.addressList addrs:(vector adnl.Address) version:int reinit_date:int priority:int expire_at:int = adnl.AddressList;

dht.node id:PublicKey addr_list:adnl.addressList version:int signature:bytes = dht.Node;
dht.nodes nodes:(vector dht.node) = dht.Nodes;

dht.valueNotFound nodes:dht.nodes = dht.ValueResult;
```

`dht.nodes -> nodes` - DHT节点列表（数组）。

每个节点都有一个`id`，即其公钥，通常是[pub.ed25519](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L47)，用作通过ADNL连接到节点的服务器密钥。此外，每个节点都有一个地址列表`addr_list:adnl.addressList`，版本和签名。

我们需要检查每个节点的签名，为此我们读取`signature`的值并将该字段置零（我们使其成为空字节数组）。之后 - 我们序列化TL结构`dht.node`并检查空签名。之后 - 我们使用`id`字段中的公钥检查清空之前的`signature`字段。[[实现示例]](https://github.com/xssnick/tonutils-go/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/dht/client.go#L91)

从列表`addrs:(vector adnl.Address)`中，我们取地址并尝试建立ADNL UDP连接，作为服务器密钥我们使用`id`，即公钥。

为了找出与该节点的“距离” - 我们需要从`id`字段的密钥中取出[key id](/develop/network/adnl-tcp#getting-key-id)并通过节点密钥id和所需密钥的XOR操作检查距离。如果距离足够小，我们可以对此节点发出相同的请求。依此类推，直到我们找到值或没有更多新节点。

##### dht.valueFound

响应将包含值本身，完整的密钥信息，以及可选的签名（取决于值类型）。

让我们更详细地分析响应字段，使用的模式：

```tlb
adnl.address.udp ip:int port:int = adnl.Address;
adnl.addressList addrs:(vector adnl.Address) version:int reinit_date:int priority:int expire_at:int = adnl.AddressList;

dht.key id:int256 name:bytes idx:int = dht.Key;

dht.updateRule.signature = dht.UpdateRule;
dht.updateRule.anybody = dht.UpdateRule;
dht.updateRule.overlayNodes = dht.UpdateRule;

dht.keyDescription key:dht.key id:PublicKey update_rule:dht.UpdateRule signature:bytes = dht.KeyDescription;

dht.value key:dht.keyDescription value:bytes ttl:int signature:bytes = dht.Value; 

dht.valueFound value:dht.Value = dht.ValueResult;
```

首先，让我们分析`key:dht.keyDescription`，它是密钥的完整描述，密钥本身以及谁以及如何可以更新值的信息。

- `key:dht.key` - 密钥必须与我们用于搜索的密钥ID的密钥相匹配。
- `id:PublicKey` - 记录所有者
- `update_rule:dht.UpdateRule` - record update rule.
- - `dht.updateRule.signature` - only the owner of the private key can update the record, the `signature` of both the key and the value must be valid
- - `dht.updateRule.anybody` - everyone can update the record, `signature` is empty and not checked
- - `dht.updateRule.overlayNodes` - nodes from the same overlay can update the key, used to find nodes of the same overlay and add yourself

###### dht.updateRule.signature

After reading the description of the key, we act depending on the `updateRule`, for the ADNL address lookup case the type is always `dht.updateRule.signature`.
We check the key signature in the same way as last time, make the signature an empty byte array, serialize and check. After - we repeat the same for the value, i.e. for the entire `dht.value` object (while returning the key signature to its place).

[[Implementation example]](https://github.com/xssnick/tonutils-go/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/dht/client.go#L331)

###### dht.updateRule.overlayNodes

[[实现示例]](https://github.com/xssnick/tonutils-go/blob/46dbf5f820af066ab10c5639a508b4295e5aa0fb/adnl/dht/client.go#L331)

```tlb
overlay.node id:PublicKey overlay:int256 version:int signature:bytes = overlay.Node;
overlay.nodes nodes:(vector overlay.node) = overlay.Nodes;
```

用于包含有关网络中工作链和其分片的其他节点信息的键，值始终具有`overlay.nodes`的TL结构。
该值字段必须为空。

```tlb
overlay.node id:PublicKey overlay:int256 version:int signature:bytes = overlay.Node;
overlay.nodes nodes:(vector overlay.node) = overlay.Nodes;
```

为了检查有效性，我们必须检查所有`nodes`，对每个节点检查`signature`，对TL结构进行序列化：

As a result, we get a valid list of nodes that are able to give us information about the workchain shard we need.

###### dht.updateRule.anybody

因此，我们得到了能够给我们提供所需工作链分片信息的节点的有效列表。

#### dht.updateRule.anybody

没有签名，任何人都可以更新。

After the connection is established, we can request the pages of the site using the RLDP protocol. The task from the DHT side at this stage is completed.

### Search for nodes that store the state of the blockchain

建立连接后，我们可以使用RLDP协议请求站点的页面。从DHT方面来看，此阶段的任务已完成。

In order to get data, for example, of the masterchain and its shards, we need to fill in the TL structure:

```
tonNode.shardPublicOverlayId workchain:int shard:long zero_state_file_hash:int256 = tonNode.ShardPublicOverlayId;
```

为了获取例如主链及其分片的数据，我们需要填充TL结构：

```json
tonNode.shardPublicOverlayId workchain:int shard:long zero_state_file_hash:int256 = tonNode.ShardPublicOverlayId;
```

其中`workchain`在主链的情况下将等于-1，它的分片将等于-922337203685477580（0xFFFFFFFFFFFFFFFF），而`zero_state_file_hash`是链的零状态的哈希（file_hash），像其他数据一样，可以从全局网络配置中获取，在`"validator"`字段中

We need to use the resulting key ID as `name` to fill in the `pub.overlay name:bytes = PublicKey` structure, wrapping it in TL bytes array. Next, we serialize it, and we get the key ID now from it.

在我们填充了`tonNode.shardPublicOverlayId`后，我们序列化它并通过哈希获取密钥ID（像往常一样）。

我们需要使用结果密钥ID作为`name`来填充`pub.overlay name:bytes = PublicKey`结构，将其包裹在TL字节数组中。接下来，我们序列化它，并从中获取现在的密钥ID。

结果id将是用于`dht.findValue`的密钥，而`name`字段的值将是 word “nodes”。我们重复上一节的过程，一切与上次相同，但`updateRule`将是[dht.updateRule.overlayNodes](#dhtupdateruleoverlaynodes)。

## References

结果是，我们将得到节点的地址，如果需要，我们可以使用[overlay.getRandomPeers](https://github.com/ton-blockchain/ton/blob/ad736c6bc3c06ad54dc6e40d62acbaf5dae41584/tl/generate/scheme/ton_api.tl#L237)方法找到此链的其他节点的地址。我们还可以从这些节点接收有关区块的所有信息。
