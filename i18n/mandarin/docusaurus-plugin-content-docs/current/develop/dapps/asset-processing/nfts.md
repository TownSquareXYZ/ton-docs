# TON NFT 处理

## 概述

In this section of our documentation we’ll provide readers with a better understanding of NFTs. This will teach the reader how to interact with NFTs, and how to accept NFTs via transactions sent on TON Blockchain.

The information provided below assumes the reader has already taken a deep dive into our previous.
[section detailing Toncoin payment processing](/develop/dapps/asset-processing), while also assuming that they possess a basic understanding of how to interact with wallet smart contracts programmatically.

## 理解 NFT 的基础

在 TON 区块链上运行的 NFT 由 [TEP-62](https://github.com/ton-blockchain/TEPs/blob/master/text/0062-nft-standard.md) 和 [TEP-64](https://github.com/ton-blockchain/TEPs/blob/master/text/0064-token-data-standard.md) 标准表示。

The Open Network (TON) Blockchain is designed with high performance in mind and includes a feature that makes use of automatic sharding based on contract addresses on TON (which are used to help provision specific NFT designs). In order to achieve optimal performance, individual NFTs must make use of their own smart contract. This enables the creation of NFT collections of any size (whether large or small in number), while also reducing development costs and performance issues. However, this approach also introduces new considerations for the development of NFT collections.

Because each NFT makes use of its own smart contract, it is not possible to obtain information about each individualized NFT within an NFT collection using a single contract. To retrieve information on an entire collection as a whole, as well as each individual NFT within a collection, it is necessary to query both the collection contract and each individual NFT contract individually. For the same reason, to track NFT transfers, it is necessary to track all transactions for each individualized NFT within a specific collection.

### NFT 集合

NFT 集合是一个用于索引和存储 NFT 内容的合约，并应包含以下接口：

#### 获取方法 `get_collection_data`

```
(int next_item_index, cell collection_content, slice owner_address) get_collection_data()
```

获取关于集合的一般信息，表示如下：

1. `next_item_index` - if the collection is ordered, this classification indicates the total number of NFTs in the collection, as well as the next index used for minting. For unordered collections, the `next_item_index` value is -1, meaning the collection uses unique mechanisms to keep track of NFTs (e.g., the hash of TON DNS domains).
2. `collection_content` - 一个以 TEP-64 兼容格式表示集合内容的 cell。
3. `owner_address` - 包含集合所有者地址的 slice（此值也可以为空）。

#### 获取方法 `get_nft_address_by_index`

```
(slice nft_address) get_nft_address_by_index(int index)
```

This method can be used to verify the authenticity of an NFT and confirm whether it truly belongs to a specific collection. It also enables users to retrieve the address of an NFT by providing its index in the collection. The method should return a slice containing the address of the NFT that corresponds to the provided index.

#### 获取方法 `get_nft_content`

```
(cell full_content) get_nft_content(int index, cell individual_content)
```

Since the collection serves as a common data storage for NFTs, this method is necessary to complete the NFT content. To use this method, first, it’s necessary to obtain the NFT’s `individual_content` by calling the corresponding `get_nft_data()` method. After obtaining the `individual_content`, it’s possible to call the `get_nft_content()` method with the NFT index and the `individual_content` cell. The method should return a TEP-64 cell containing the full content of the NFT.

### NFT 项

基本 NFT 应实现：

#### 获取方法 `get_nft_data()`

```
(int init?, int index, slice collection_address, slice owner_address, cell individual_content) get_nft_data()
```

#### 内联消息处理器 `transfer`

```
transfer#5fcc3d14 query_id:uint64 new_owner:MsgAddress response_destination:MsgAddress custom_payload:(Maybe ^Cell) forward_amount:(VarUInteger 16) forward_payload:(Either Cell ^Cell) = InternalMsgBody
```

让我们看一下您需要在消息中填充的每个参数：

1. `OP` - `0x5fcc3d14` - 由 TEP-62 标准在转移消息中定义的常量。
2. `queryId` - `uint64` - 用于跟踪消息的 uint64 数字。
3. `newOwnerAddress` - `MsgAddress` - 用于将 NFT 转移至的合约地址。
4. `responseAddress` - `MsgAddress` - the address used to transfer excess funds to. Typically, an extra amount of TON (e.g., 1 TON) is sent to the NFT contract to ensure it has enough funds to pay transaction fees and create a new transfer if needed. All unused funds within the transaction are sent to the `responseAddress`.
5. `forwardAmount` - `Coins` - the amount of TON used in conjunction with the forward message (usually set to 0.01 TON). Since TON uses an asynchronous architecture, the new owner of the NFT will not be notified immediately upon successfully receiving the transaction. To notify the new owner, an internal message is sent from the NFT smart contract to the `newOwnerAddress` with a value denoted using the `forwardAmount`. The forward message will begin with the `ownership_assigned` OP (`0x05138d91`), followed by the previous owner's address and the `forwardPayload` (if present).
6. `forwardPayload` - `Slice | Cell` - 作为 `ownership_assigned` 通知消息的一部分发送。

如上所述，这个消息是与 NFT 交互的主要方式，用于在收到上述消息的通知后改变所有权。

For example, this message type above is often used to send a NFT Item Smart Contract from a Wallet Smart Contract. When an NFT Smart Contract receives this message and executes it, the NFT Contract's storage (inner contract data) is updated along with the Owner's ID. In this way, the NFT Item(contract) changes owners correctly. This process details a standard NFT Transfer

In this case, the forward amount should be set to an appropriate value(0.01 TON for a regular wallet or more if you want to execute a contract by transferring an NFT), to ensure that the new owner receives a notification regarding the ownership transfer. This is important because the new owner won’t be notified that they have received the NFT without this notification.

## 检索 NFT 数据

大多数 SDK 使用现成的处理器来检索 NFT 数据，包括：[tonweb(js)](https://github.com/toncenter/tonweb/blob/b550969d960235314974008d2c04d3d4e5d1f546/src/contract/token/nft/NftItem.js#L38)、[tonutils-go](https://github.com/xssnick/tonutils-go/blob/fb9b3fa7fcd734eee73e1a73ab0b76d2fb69bf04/ton/nft/item.go#L132)、[pytonlib](https://github.com/toncenter/pytonlib/blob/d96276ec8a46546638cb939dea23612876a62881/pytonlib/client.py#L771)等。

To receive NFT data it is necessary to make use of the `get_nft_data()` retrieval mechanism. For example, we must verify the following NFT item address `EQB43-VCmf17O7YMd51fAvOjcMkCw46N_3JMCoegH_ZDo40e`(also known as [foundation.ton](https://tonscan.org/address/EQB43-VCmf17O7YMd51fAvOjcMkCw46N_3JMCoegH_ZDo40e) domain).

首先需要按照如下方式使用 toncenter.com API 执行 get 方法。:

```
curl -X 'POST' \
  'https://toncenter.com/api/v2/runGetMethod' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "address": "EQB43-VCmf17O7YMd51fAvOjcMkCw46N_3JMCoегH_ZDo40e",
  "method": "get_nft_data",
  "stack": []
}'
```

响应通常类似于如下内容：

```json
{
  "ok": true,
  "result": {
    "@type": "smc.runResult",
    "gas_used": 1581,
    "stack": [
      // init
      [ "num", "-0x1" ],
      // index
      [ "num", "0x9c7d56cc115e7cf6c25e126bea77cbc3cb15d55106f2e397562591059963faa3" ],
      // collection_address
      [ "cell", { "bytes": "te6cckEBAQEAJAAAQ4AW7psr1kCofjDYDWbjVxFa4J78SsJhlfLDEm0U+hltmfDtDcL7" } ],
      // owner_address
      [ "cell", { "bytes": "te6cckEBAQEAJAAAQ4ATtS415xpeB1e+YRq/IsbVL8tFYPTNhzrjr5dcdgZdu5BlgvLe" } ],
      // content
      [ "cell", { "bytes": "te6cckEBCQEA7AABAwDAAQIBIAIDAUO/5NEvz/d9f/ZWh+aYYobkmY5/xar2cp73sULgTwvzeuvABAIBbgUGAER0c3/qevIyXwpbaQiTnJ1y+S20wMpSzKjOLEi7Jwi/GIVBAUG/I1EBQhz26hlqnwXCrTM5k2Qg5o03P1s9x0U4CBUQ7G4HAUG/LrgQbAsQe0P2KTvsDm8еA3Wr0ofDEIPQlYa5wXdpD/oIAEmf04AQe/qqXMblNo5fl5kYi9eYzSLgSrFtHY6k/DdIB0HmNQAQAEatAVFmGM9svpAE9og+dCyaLjylPtAuPjb0zvYqmO4eRJF0AIDBvlU=" } ]
    ],
    "exit_code": 0,
    "@extra": "1679535187.3836682:8:0.06118075068995321"
  }
}
```

返回参数：

- `init` - `boolean` - -1 表示 NFT 已初始化并可使用
- `index` - `uint256` - index of the NFT in the collection. Can be sequential or derived in some other way. For example, this can denote an NFT doman hash used with TON DNS contracts, while collections should only have only one unique NFT within a given index.
- `collection_address` - `Cell` - 包含 NFT 集合地址的 cell（可以为空）。
- `owner_address` - `Cell` - 包含当前所有者 NFT 地址的 cell（可以为空）。
- `content` - `Cell` - 包含 NFT 项内容的 cell（如果需要解析，需要参考 TEP-64 标准）。

## 检索集合内的所有 NFT

The process for retrieving all NFTs within a collection differs depending on whether the collection is ordered or not. Let’s outline both processes below.

### 有序集合

Retrieving all NFTs in an ordered collection is relatively straightforward since the number of NFTs needed for retrieval is already known and their addresses can easily be easily obtained. To complete this process, the following steps should be followed in order:

1. 使用 TonCenter API 调用集合合约中的 `get_collection_data` 方法，并从响应中检索 `next_item_index` 值。
2. 使用 `get_nft_address_by_index` 方法，传入索引值 `i`（最初设置为 0），以检索集合中第一个 NFT 的地址。
3. Retrieve the NFT Item data using the address obtained in the previous step. Next, verify that the initial NFT Collection smart contract coincides with the NFT Collection smart contract reported by the NFT item itself (to ensure the Collection didn't appropriate another user’s NFT smart contract).
4. 使用来自上一步的 `i` 和 `individual_content` 调用 `get_nft_content` 方法。
5. `i` 增加 1 并重复步骤 2-5，直到 `i` 等于 `next_item_index`。
6. 此时，您将拥有来自集合及其各个项目所需的信息。

### 无序集合

Retrieving the list of NFTs in an unordered collection is more difficult because there is no inherent way to obtain the addresses of the NFTs that belong to the collection. Therefore, it is necessary to parse all transactions in the collection contract and check all outgoing messages to identify the ones that correspond to NFTs belonging to the collection.

To do so, the NFT data must be retrieved, and the `get_nft_address_by_index` method is called in the collection with the ID returned by the NFT. If the NFT contract address and the address returned by the `get_nft_address_by_index` method match, it indicates that the NFT belongs to the current collection. However, parsing all messages to the collection can be a lengthy process and may require archive nodes.

## 在 TON 之外的 NFT 处理

### 发送 NFT

To transfer NFT ownership it is necessary to send an internal message from the NFT owner’s wallet to the NFT contract by creating a cell that contains a transfer message. This can be accomplished using libraries (such as [tonweb(js)](https://github.com/toncenter/tonweb/blob/b550969d960235314974008d2c04d3d4e5d1f546/src/contract/token/nft/NftItem.js#L65), [ton(js)](https://github.com/getgems-io/nft-contracts/blob/debcd8516b91320fa9b23bff6636002d639e3f26/packages/contracts/nft-item/NftItem.data.ts#L102), [tonutils-go(go)](https://github.com/xssnick/tonutils-go/blob/fb9b3fa7fcd734eee73e1a73ab0b76d2fb69bf04/ton/nft/item.go#L132)) for the specific language.

一旦创建了转移消息，就必须从所有者的钱包合约地址发送到 NFT 项合约地址，并附带足够的 TON 以支付关联的交易费用。

To transfer an NFT from another user to yourself, it is necessary to use TON Connect 2.0 or a simple QR code that contains a ton:// link. For example:
`ton://transfer/{nft_address}?amount={message_value}&bin={base_64_url(transfer_message)}`

### 接收 NFTs

The process of tracking NFTs sent to a certain smart contract address (i.e. a user's wallet) is similar to the mechanism used to track payments. This is completed by listening to all new transactions in your wallet and parsing them.

The next steps may vary depending on the specific use case. Let’s examine several different scenarios below.

#### 等待已知 NFT 地址转移的服务:

- 验证从 NFT 项目智能合约地址发送的新交易。
- 读取消息体的前 32 位作为使用 `uint` 类型，并验证它是否等于 `op::ownership_assigned()`(`0x05138d91`)
- 从消息体中读取接下来的 64 位作为 `query_id`。
- 将消息体中的地址读作 `prev_owner_address`。
- 现在可以管理您的新 NFT 了。

#### 监听所有类型的 NFT 转移的服务:

- 检查所有新交易，忽略那些消息体长度小于 363 位（OP - 32，QueryID - 64，地址 - 267）的交易。
- 重复上面列表中详细介绍的步骤。
- If the process is working correctly, it is necessary to verify the authenticity of the NFT by parsing it and the collection it belongs to. Next, it is necessary to ensure that the NFT belongs to the specified collection. More information detailing this process can be found in the `Getting all collection NFTs` section. This process can be simplified by using a whitelist of NFTs or collections.
- 现在可以管理您的新 NFT 了。

#### 将 NFT 转移绑定到内部交易:

When a transaction of this type is received, it's necessary to repeat the steps from the previous list. Once this process is completed, it is possible to retrieve the `RANDOM_ID`  parameter by reading a uint32 from the message body after reading the `prev_owner_address` value.

#### 未发送通知信息的 NFT 发送:

All of the strategies outlined above rely on the services correctly creating a forward message with the NFT transfer. If they don't do this, we won't know that they transferred the NFT to us. However, there are a few workarounds:

All of the strategies outlined above rely on the service correctly creating a forward message within the NFT transfer. If this process is not carried out, it won’t be clear whether the NFT was transferred to the correct party. However, there are a several workarounds that are possible in this scenario:

- 如果预计 NFT 数量较少，可以定期解析它们并验证所有者是否已更改为相应的合约类型。
- If a large number of NFTs is expected, it is possible to parse all new blocks and verify if there were any calls sent to the NFT destination using the `op::transfer` method. If a transaction like this is initiated, it is possible to verify the NFT owner and receive the transfer.
- If it's not possible to parse new blocks within the transfer, it is possible for users to trigger NFT ownership verification processes themselves. This way, it is possible to trigger the NFT ownership verification process after transferring an NFT without a notification.

## 从智能合约与 NFTs 交互

既然我们已经涵盖了发送和接收 NFTs 的基础，现在让我们探讨如何使用 [NFT Sale](https://github.com/ton-blockchain/token-contract/blob/1ad314a98d20b41241d5329e1786fc894ad811de/nft/nft-sale.fc) 合约示例从智能合约接收和转移 NFTs。

### 发送 NFTs

在这个例子中，NFT 转移信息位于 [第 67 行](https://www.google.com/url?q=https://github.com/ton-blockchain/token-contract/blob/1ad314a98d20b41241d5329e1786fc894ad811de/nft/nft-sale.fc%23L67\&sa=D\&source=docs\&ust=1685436161341866\&usg=AOvVaw1yuoIzcbEuvqMS4xQMqfXE):

```
var nft_msg = begin_cell()
  .store_uint(0x18, 6)
  .store_slice(nft_address)
  .store_coins(0)
  .store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1) ;; 默认消息头（见发送消息页面）
  .store_uint(op::transfer(), 32)
  .store_uint(query_id, 64)
  .store_slice(sender_address) ;; new_owner_address
  .store_slice(sender_address) ;; response_address
  .store_int(0, 1) ;; 空的自定义有效载荷
  .store_coins(0) ;; 向 new_owner_address 转发金额
  .store_int(0, 1); ;; 空的转发有效载荷


send_raw_message(nft_msg.end_cell(), 128 + 32);
```

让我们仔细检查每行代码：

- `store_uint(0x18, 6)` - 存储消息标志。
- `store_slice(nft_address)` - 存储消息目标（NFT 地址）。
- `store_coins(0)` -  the amount of TON to send with the message is set to 0 because the `128` [message mode](/develop/smart-contracts/messages#message-modes) is used to send the message with its remaining balance. To send an amount other than the user’s entire balance, the number must be changed. Note that it should be large enough to pay for gas fees as well as any forwarding amount.
- `store_uint(0, 1 + 4 + 4 + 64 + 32 + 1 + 1)` - 剩余构成消息头的部分被留空。
- `store_uint(op::transfer(), 32)` - this is the start of the msg_body. Here we start by using the transfer OP code so the receiver understands its transfer ownership message.
- `store_uint(query_id, 64)` - 存储查询 ID。
- `store_slice(sender_address) ;; new_owner_address` - 第一个存储的地址是用于转移 NFTs 和发送通知的地址。
- `store_slice(sender_address) ;; response_address` - 第二个存储的地址是响应地址。
- `store_int(0, 1)` - 自定义有效载荷标志设置为 0，表示不需要自定义有效载荷。
- `store_coins(0)` - amount of TON to be forwarded with the message. In this example it’s set to 0, however, it is recommended to set this value to a higher amount (such as at least 0.01 TON) in order to create a forward message and notify the new owner that they have received the NFT. The amount should be sufficient to cover any associated fees and costs.
- `.store_int(0, 1)` - custom payload flag. It's necessary to set up to `1` if your service should pass payload as a ref.

### 接收 NFTs

Once we've sent the NFT, it is critical to determine when it has been received by the new owner. A good example of how to do this can be found in the same NFT sale smart contract:

```
slice cs = in_msg_full.begin_parse();
int flags = cs~load_uint(4);

if (flags & 1) {  ;; 忽略所有弹回消息
    return ();
}
slice sender_address = cs~load_msg_addr();
throw_unless(500, equal_slices(sender_address, nft_address));
int op = in_msg_body~load_uint(32);
throw_unless(501, op == op::ownership_assigned());
int query_id = in_msg_body~load_uint(64);
slice prev_owner_address = in_msg_body~load_msg_addr();
```

让我们再次检查每行代码：

- `slice cs = in_msg_full.begin_parse();` - 用于解析传入消息。
- `int flags = cs~load_uint(4);` - 用于从消息的前 4 位加载标志。
- `if (flags & 1) { return (); } ;; ignore all bounced messages` - used to verify that the message has not bounced. It’s important to carry out this process for all your incoming messages if there is no reason to do otherwise. Bounced messages are messages that encountered errors while trying to receive a transaction and were returned to the sender.
- `slice sender_address = cs~load_msg_addr();` - next the message sender is loaded. In this case specifically by using an NFT address.
- `throw_unless(500, equal_slices(sender_address, nft_address));` - used to verify that the sender is indeed an NFT that should have been transferred via a contract. It's quite difficult to parse NFT data from smart contracts, so in most cases the NFT address is predefined at contract creation.
- `int op = in_msg_body~load_uint(32);` - 加载消息 OP 代码。
- `throw_unless(501, op == op::ownership_assigned());` - 确保接收的 OP 代码与所有权分配的常量值匹配。
- `slice prev_owner_address = in_msg_body~load_msg_addr();` - previous owner address that is extracted from the incoming message body and loaded into the `prev_owner_address` slice variable. This can be useful if the previous owner chooses to cancel the contract and have the NFT returned to them.

现在我们已经成功地解析并验证了通知消息，我们可以继续我们的业务逻辑，这用于启动销售智能合约（它旨在处理 NFT 物品业务销售过程，例如 NFT 拍卖，如 getgems.io）
