import Feedback from '@site/src/components/Feedback';

# Smart contract addresses

在 TON 区块链上，每个行为者（包括钱包和智能合约）都有一个地址。这些地址对于接收和发送信息和交易至关重要。智能合约地址有两种主要格式：**原始地址**和**用户友好地址**。

## Address components

TON 上的每个地址都由两个主要部分组成：

- **工作链 ID(Workchain ID)**：带符号的 32 位整数，表示合约属于哪个工作链（例如，"-1 "表示主链，"0 "表示基础链）。
- **账户 ID(Account ID)**：合约的唯一标识符，主链和底层链的长度一般为 256 位。

## Address states

TON 上的每个地址都可以处于以下状态之一：

- **Nonexist**：地址没有数据（所有地址的初始状态）。
- **Uninit**：地址有余额，但没有智能合约代码。
- **Active**：该地址已启用智能合约代码和余额。
- **Frozen**：由于存储费用超过余额，地址被锁定。

## Address formats

A TON address uniquely identifies a contract in the blockchain, indicating its workchain and original state hash. [Two standard formats](/v3/documentation/smart-contracts/addresses#raw-and-user-friendly-addresses) are used: **raw** (workchain and HEX-encoded hash separated by the ":" character) and **user-friendly** (base64-encoded with certain flags).

```
User-friendly: EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
Raw: 0:ca6e321c7cce9ecedf0a8ca2492ec8592494aa5fb5ce0387dff96ef6af982a3e
```

## User-friendly address

A **user-friendly address** designed for blockchain users with features:

1. **Flags**: Indicates if the address is bounceable for contracts or non-bounceable for wallets.
2. **Checksum**: A 2-byte error-checking mechanism CRC16 that helps detect errors before sending.
3. \*\* Encoding\*\*：使用 base64 或 base64url 将原始地址转换为可读的简洁形式。

Example: `EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF` (base64)

用户友好型地址可防止出错，并允许在交易失败的情况下退回资金，从而使交易更加安全。

### User-friendly address flags

Two flags are defined: **bounceable**/**non-bounceable** and **testnet**/**any-net**. The first letter of the address reflects address type because it stands for the first 6 bits in address encoding, and flags are located in these 6 bits according to [TEP-2](https://github.com/ton-blockchain/TEPs/blob/master/text/0002-address.md#smart-contract-addresses):

|                   Address beginning                  |        Binary form        | Bounceable | Testnet-only |
| :--------------------------------------------------: | :-----------------------: | :--------: | :----------: |
| E... | 000100.01 |     yes    |      no      |
| U... | 010100.01 |     no     |      no      |
| k... | 100100.01 |     yes    |      yes     |
| 0... | 110100.01 |     no     |      yes     |

:::tip
The Testnet-only flag doesn't have representation in the blockchain at all. The non-bounceable flag makes a difference only when used as the destination address for a transfer: in this case, it [disallows bounce](/v3/documentation/smart-contracts/message-management/non-bounceable-messages) for a message sent; the address in blockchain, again, does not contain this flag.
:::

```
default bounceable: EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPrHF
urlSafe: EQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff+W72r5gqPrHF
non-bounceable: UQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPuwA
Testnet: kQDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPgpP
non-bounceable, Testnet: 0QDKbjIcfM6ezt8KjKJJLshZJJSqX7XOA4ff-W72r5gqPleK
```

## Raw address

**原始地址**只包含基本要素：

- **工作链 ID**（例如，"-1 "表示主链）
- **账户 ID**：256 位唯一标识符

示例：\
`-1:fcb91a3a3816d0f7b8c2c76108b8a9bc5a6b7a55bd79f8ab101c52db29232260`.

然而，原始地址有两个主要问题：

1. 它们缺乏内置的错误检查功能，这意味着复制错误可能导致资金损失。
2. They don't support additional features like bounceable/non-bounceable flags.

## Converting between address formats

Convert raw, user-friendly addresses using [ton.org/address](https://ton.org/address/).

For more details, refer to the refhandling guide in the [Smart contracts addresses documentation](/v3/documentation/smart-contracts/addresses/) section.

## See also

- [Explorers in TON](/v3/concepts/dive-into-ton/ton-ecosystem/explorers-in-ton/)
- [Smart contracts addresses documentation](/v3/documentation/smart-contracts/addresses/)

<Feedback />

