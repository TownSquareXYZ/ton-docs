# TVM 升级 2023.07

:::tip
此升级于 2023 年 12 月在主网上启动，详细信息请参考 [run](https://t.me/tonblockchain/223)。
:::

# c7

**c7** 是存储有关合约执行所需的本地 context 信息的寄存器
（如时间、lt、网络配置等）。

**c7** 元组从 10 扩展到 14 个元素：

- **10**: 存储智能合约本身的 `cell`。
- **11**: `[integer, maybe_dict]`：传入消息的 TON 值，额外代币。
- **12**: `integer`，存储阶段收取的费用。
- **13**: `tuple` 包含有关先前区块的信息。

**10** 当前智能合约的代码仅以可执行继续的形式在 TVM 级别呈现，无法转换为cell。这段代码通常用于授权相同类型的 neighbor 合约，例如 Jetton 钱包授权 Jetton 钱包。目前我们需要显式地代码cell存储在存储器中，这使得存储和 init_wrapper 变得更加麻烦。
使用 **10** 作为代码对于 tvm 的 Everscale 更新兼容。

**11** 当前，传入消息的值在 TVM 初始化后以堆栈形式呈现，因此如果在执行过程中需要，
则需要将其存储到全局变量或通过本地变量传递（在 funC 级别看起来像所有函数中的额外 `msg_value` 参数）。通过将其放在 **11** 元素中，我们将重复合约余额的行为：它既出现在堆栈中，也出现在 c7 中。

**12** 目前计算存储费用的唯一方法是在先前的交易中存储余额，以某种方式计算 prev 交易中的 gas 用量，然后与当前余额减去消息值进行比较。与此同时，经常希望考虑存储费用。

**13** 目前没有办法检索先前区块的数据。TON 的一个关键特性是每个结构都是 Merkle 证明友好的cell（树），此外，TVM 也是cell和 Merkle 证明友好的。通过在 TVM context中包含区块信息，将能够实现许多不信任的情景：合约 A 可以检查合约 B 上的交易（无需 B 的合作），可以恢复中断的消息链（当恢复合约获取并检查某些事务发生但被还原的证明时），还需要了解主链区块哈希以在链上进行某些验证 fisherman 函数功能。

区块 id 的表示如下：

```
[ wc:Integer shard:Integer seqno:Integer root_hash:Integer file_hash:Integer ] = BlockId;
[ last_mc_blocks:[BlockId0, BlockId1, ..., BlockId15]
  prev_key_block:BlockId ] : PrevBlocksInfo
```

包括主链的最后 16 个区块的 id（如果主链 seqno 小于 16，则为少于 16 个），以及最后的关键区块。包含有关分片区块的数据可能会导致一些数据可用性问题（由于合并/拆分事件），这并非必需（因为可以使用主链区块来证明任何事件/数据），因此我们决定不包含。

# 新的操作码

在选择新操作码的 gas 成本时的经验法则是它不应少于正常成本（从操作码长度计算）且不应超过每个 gas 单位 20 ns。

## 用于处理新 c7 值的操作码

每个操作码消耗 26 gas，除了 `PREVMCBLOCKS` 和 `PREVKEYBLOCK`（34 gas）。

| xxxxxxxxxxxxxxxxxxxxxx<br/>Fift 语法 | xxxxxxxxx<br/>堆栈 | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>描述                                |
| :--------------------------------- | :--------------- | :-------------------------------------------------------------------------- |
| `MYCODE`                           | _`- c`_          | 从 c7 检索智能合约的代码                                                              |
| `INCOMINGVALUE`                    | _`- t`_          | 从 c7 检索传入消息的值                                                               |
| `STORAGEFEES`                      | _`- i`_          | 从 c7 检索存储阶段费用的值                                                             |
| `PREVBLOCKSINFOTUPLE`              | _`- t`_          | 从 c7 中检索 PrevBlocksInfo: `[last_mc_blocks, prev_key_block]` |
| `PREVMCBLOCKS`                     | _`- t`_          | 仅检索 `last_mc_blocks`                                                        |
| `PREVKEYBLOCK`                     | _`- t`_          | 仅检索 `prev_key_block`                                                        |
| `GLOBALID`                         | _`- i`_          | 从网络配置的第 19 项检索 `global_id`                                                  |

## Gas

| xxxxxxxxxxxxxx<br/>Fift 语法 | xxxxxxxx<br/>堆栈 | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>描述 |
| :------------------------- | :-------------- | :-------------------------------------------- |
| `GASCONSUMED`              | _`- g_c`_       | 返回到目前为止 VM 消耗的 gas（包括此指令）。<br/>_26 gas_       |

## 算术

添加了 [除法操作码](https://docs.ton.org/learn/tvm-instructions/instructions#52-division)（`A9mscdf`）的新变体：
`d=0` 从堆栈中获取一个额外的整数，并将其添加到除法/右移之前的中间值。这些操作返回商和余数（与 `d=3` 类似）。

还提供了静默变体（例如 `QMULADDDIVMOD` 或 `QUIET MULADDDIVMOD`）。

如果返回值

不适应 257 位整数或除数为零，非静默操作会引发整数溢出异常。静默操作返回 `NaN` 而不是不适应的值（如果除数为零则返回两个 `NaN`）。

| xxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Stack |
| :------------------------------------- | :------------------------------------------------------- |
| `MULADDDIVMOD`                         | _`x y w z - q=floor((xy+w)/z) r=(xy+w)-zq`_              |
| `MULADDDIVMODR`                        | _`x y w z - q=round((xy+w)/z) r=(xy+w)-zq`_              |
| `MULADDDIVMODC`                        | _`x y w z - q=ceil((xy+w)/z) r=(xy+w)-zq`_               |
| `ADDDIVMOD`                            | _`x w z - q=floor((x+w)/z) r=(x+w)-zq`_                  |
| `ADDDIVMODR`                           | _`x w z - q=round((x+w)/z) r=(x+w)-zq`_                  |
| `ADDDIVMODC`                           | _`x w y - q=ceil((x+w)/z) r=(x+w)-zq`_                   |
| `ADDRSHIFTMOD`                         | _`x w z - q=floor((x+w)/2^z) r=(x+w)-q*2^z`_             |
| `ADDRSHIFTMODR`                        | _`x w z - q=round((x+w)/2^z) r=(x+w)-q*2^z`_             |
| `ADDRSHIFTMODC`                        | _`x w z - q=ceil((x+w)/2^z) r=(x+w)-q*2^z`_              |
| `z ADDRSHIFT#MOD`                      | _`x w - q=floor((x+w)/2^z) r=(x+w)-q*2^z`_               |
| `z ADDRSHIFTR#MOD`                     | _`x w - q=round((x+w)/2^z) r=(x+w)-q*2^z`_               |
| `z ADDRSHIFTC#MOD`                     | _`x w - q=ceil((x+w)/2^z) r=(x+w)-q*2^z`_                |
| `MULADDRSHIFTMOD`                      | _`x y w z - q=floor((xy+w)/2^z) r=(xy+w)-q*2^z`_         |
| `MULADDRSHIFTRMOD`                     | _`x y w z - q=round((xy+w)/2^z) r=(xy+w)-q*2^z`_         |
| `MULADDRSHIFTCMOD`                     | _`x y w z - q=ceil((xy+w)/2^z) r=(xy+w)-q*2^z`_          |
| `z MULADDRSHIFT#MOD`                   | _`x y w - q=floor((xy+w)/2^z) r=(xy+w)-q*2^z`_           |
| `z MULADDRSHIFTR#MOD`                  | _`x y w - q=round((xy+w)/2^z) r=(xy+w)-q*2^z`_           |
| `z MULADDRSHIFTC#MOD`                  | _`x y w - q=ceil((xy+w)/2^z) r=(xy+w)-q*2^z`_            |
| `LSHIFTADDDIVMOD`                      | _`x w z y - q=floor((x*2^y+w)/z) r=(x*2^y+w)-zq`_        |
| `LSHIFTADDDIVMODR`                     | _`x w z y - q=round((x*2^y+w)/z) r=(x*2^y+w)-zq`_        |
| `LSHIFTADDDIVMODC`                     | _`x w z y - q=ceil((x*2^y+w)/z) r=(x*2^y+w)-zq`_         |
| `y LSHIFT#ADDDIVMOD`                   | _`x w z - q=floor((x*2^y+w)/z) r=(x*2^y+w)-zq`_          |
| `y LSHIFT#ADDDIVMODR`                  | _`x w z - q=round((x*2^y+w)/z) r=(x*2^y+w)-zq`_          |
| `y LSHIFT#ADDDIVMODC`                  | _`x w z - q=ceil((x*2^y+w)/z) r=(x*2^y+w)-zq`_           |

## Stack operations

Currently arguments of all stack operations are bounded by 256.
That means that if stack become deeper than 256 it becomes difficult to manage deep stack elements.
In most cases there are no safety reasons for that limit, i.e. arguments are not limited to prevent too expensive operations.
For some mass stack operations, such as `ROLLREV` (where computation time lineary depends on argument value) gas cost also lineary depends on argument value.

- Arguments of `PICK`, `ROLL`, `ROLLREV`, `BLKSWX`, `REVX`, `DROPX`, `XCHGX`, `CHKDEPTH`, `ONLYTOPX`, `ONLYX` are now unlimited.
- `ROLL`, `ROLLREV`, `REVX`, `ONLYTOPX` consume more gas when arguments are big: additional gas cost is `max(arg-255,0)` (for argument less than 256 the gas consumption is constant and corresponds to the current behavior)
- For `BLKSWX`, additional cost is `max(arg1+arg2-255,0)` (this does not correspond to the current behavior, since currently both `arg1` and `arg2` are limited to 255).

## Hashes

Currently only two hash operations are available in TVM: calculation of representation hash of cell/slice, and sha256 of data, but only up to 127 bytes (only that much data fits into one cell).

目前 TVM 中只有两个哈希操作：计算cell/切片的 representation hash ，以及对数据进行 sha256，但只支持最多 127 字节（只有这么多数据适应一个cell）。

| xxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description                                                                   |
| :---------------------------------- | :------------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| `HASHEXT_(HASH)`                    | _`s_1 ... s_n n - h`_            | Calculates and returns hash of the concatenation of slices (or builders) `s_1...s_n`. |
| `HASHEXTR_(HASH)`                   | _`s_n ... s_1 n - h`_            | Same thing, but arguments are given in reverse order.                                                    |
| `HASHEXTA_(HASH)`                   | _`b s_1 ... s_n n - b'`_         | Appends the resulting hash to a builder `b` instead of pushing it to the stack.                          |
| `HASHEXTAR_(HASH)`                  | _`b s_n ... s_1 n - b'`_         | Arguments are given in reverse order, appends hash to builder.                                           |

Only the bits from root cells of `s_i` are used.

仅使用 `s_i` 的根cell的位。

每个块 `s_i` 可能包含非整数数量的字节。但所有块的位的和应该是 8 的倍数。注意 TON 使用最高位优先顺序，因此当连接两个具有非整数字节的切片时，第一个切片的位变为最高位。

gas 消耗取决于哈希字节数和所选算法。每个块额外消耗 1 gas 单位。

如果未启用 `[A]`，则哈希的结果将作为无符号整数返回，如果适应 256 位，否则返回整数的元组。

- `SHA256` - openssl implementation, 1/33 gas per byte, hash is 256 bits.
- `SHA512` - openssl implementation, 1/16 gas per byte, hash is 512 bits.
- `BLAKE2B` - openssl implementation, 1/19 gas per byte, hash is 512 bits.
- `KECCAK256` - [ethereum compatible implementation](http://keccak.noekeon.org/), 1/11 gas per byte, hash is 256 bits.
- `KECCAK512` - [ethereum compatible implementation](http://keccak.noekeon.org/), 1/6 gas per byte, hash is 512 bits.

Gas usage is rounded down.

## Crypto

Currently the only cryptographic algorithm available is `CHKSIGN`: check the Ed25519-signature of a hash `h` for a public key `k`.

- For compatibility with prev generation blockchains such as Bitcoin and Ethereum we also need checking `secp256k1` signatures.
- For modern cryptographic algorithms the bare minimum is curve addition and multiplication.
- For compatibility with Ethereum 2.0 PoS and some other modern cryptography we need BLS-signature scheme on bls12-381 curve.
- For some secure hardware secp256r1 == P256 == prime256v1 is needed.

### secp256k1

Bitcoin/ethereum signatures. Uses [libsecp256k1 implementation](https://github.com/bitcoin-core/secp256k1).

| xxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack      | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description                                                                                                                                                                                                                                                                                                                                   |
| :---------------------------- | :------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ECRECOVER`                   | _`hash v r s - 0 or h x1 x2 -1`_ | Recovers public key from signature, identical to Bitcoin/Ethereum operations.<br/>Takes 32-byte hash as uint256 `hash`; 65-byte signature as uint8 `v` and uint256 `r`, `s`.<br/>Returns `0` on failure, public key and `-1` on success.<br/>65-byte public key is returned as uint8 `h`, uint256 `x1`, `x2`.<br/>_1526 gas_ |

### secp256r1

Uses OpenSSL implementation. Interface is similar to `CHKSIGNS`/`CHKSIGNU`. Compatible with Apple Secure Enclave.

| xxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| :---------------------------- | :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `P256_CHKSIGNS`               | _`d sig k - ?`_             | Checks seck256r1-signature `sig` of data portion of slice `d` and public key `k`. Returns -1 on success, 0 on failure.<br/>Public key is a 33-byte slice (encoded according to Sec. 2.3.4 point 2 of [SECG SEC 1](https://www.secg.org/sec1-v2.pdf)).<br/>Signature `sig` is a 64-byte slice (two 256-bit unsigned integers `r` and `s`).<br/>_3526 gas_ |
| `P256_CHKSIGNU`               | _`h sig k - ?`_             | Same thing, but the signed data is 32-byte encoding of 256-bit unsigned integer `h`.<br/>_3526 gas_                                                                                                                                                                                                                                                                                                                                                                                            |

### Ristretto

Extended docs are [here](https://ristretto.group/). In short, Curve25519 was developed with performance in mind, however it exhibits symmetry due to which group elements have multiple representations. Simpler protocols such as Schnorr signatures or Diffie-Hellman apply tricks at the protocol level to mitigate some issues, but break key derivation and key blinding schemes. And those tricks do not scale to more complex protocols such as Bulletproofs. Ristretto is an arithmetic abstraction over Curve25519 such that each group element corresponds to a unique point, which is the requirement for most cryptographic protocols. Ristretto is essentially a compression/decompression protocol for Curve25519 that offers the required arithmetic abstraction. As a result, crypto protocols are easy to write correctly, while benefiting from the high performance of Curve25519.

Ristretto operations allow calculating curve operations on Curve25519 (the reverse is not true), thus we can consider that we add both Ristretto and Curve25519 curve operation in one step.

更详细的文档在[这里](https://ristretto.group/)。简而言之，Curve25519 是为了性能而开发的，但由于对称性而表现出多重表示的问题，使得群元素具有多个表示。简单的协议，如Schnorr签名或Diffie-Hellman，在协议级别应用一些技巧以减轻一些问题，但破坏了密钥推导和密钥遮蔽方案。而这些技巧在更复杂的协议，如Bulletproofs上无法扩展。Ristretto是对Curve25519的算术抽象，使得每个群元素对应于唯一的点，这是大多数密码协议的要求。Ristretto实质上是Curve25519的压缩/解压缩协议，提供所需的算术抽象。因此，可以认为我们在一步中添加了Ristretto和Curve25519曲线操作。

[libsodium 实现](https://github.com/jedisct1/libsodium/)。

| xxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description                                                                                          |
| :---------------------------- | :-------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RIST255_FROMHASH`            | _`h1 h2 - x`_               | Deterministically generates a valid point `x` from a 512-bit hash (given as two 256-bit integers).<br/>_626 gas_ |
| `RIST255_VALIDATE`            | _`x -`_                     | Checks that integer `x` is a valid representation of some curve point. Throws `range_chk` on error.<br/>_226 gas_   |
| `RIST255_ADD`                 | _`x y - x+y`_               | Addition of two points on a curve.<br/>_626 gas_                                                                                    |
| `RIST255_SUB`                 | _`x y - x-y`_               | Subtraction of two points on curve.<br/>_626 gas_                                                                                   |
| `RIST255_MUL`                 | _`x n - x*n`_               | Multiplies point `x` by a scalar `n`.<br/>Any `n` is valid, including negative.<br/>_2026 gas_                      |
| `RIST255_MULBASE`             | _`n - g*n`_                 | Multiplies the generator point `g` by a scalar `n`.<br/>Any `n` is valid, including negative.<br/>_776 gas_         |
| `RIST255_PUSHL`               | _`- l`_                     | Pushes integer `l=2^252+27742317777372353535851937790883648493`, which is the order of the group.<br/>_26 gas_                      |
| `RIST255_QVALIDATE`           | _`x - 0 or -1`_             | Quiet version of `RIST255_VALIDATE`.<br/>_234 gas_                                                                                  |
| `RIST255_QADD`                | _`x y - 0 or x+y -1`_       | Quiet version of `RIST255_ADD`. <br/>_634 gas_                                                                                      |
| `RIST255_QSUB`                | _`x y - 0 or x-y -1`_       | Quiet version of `RIST255_SUB`.<br/>_634 gas_                                                                                       |
| `RIST255_QMUL`                | _`x n - 0 or x*n -1`_       | Quiet version of `RIST255_MUL`.<br/>_2034 gas_                                                                                      |
| `RIST255_QMULBASE`            | _`n - 0 or g*n -1`_         | Quiet version of `RIST255_MULBASE`.<br/>_784 gas_                                                                                   |

### BLS12-381

Operations on a pairing friendly BLS12-381 curve. [BLST](https://github.com/supranational/blst) implementation is used. Also, ops for BLS signature scheme which is based on this curve.

在配对友好的 BLS12-381 曲线上进行操作。使用[BLST](https://github.com/supranational/blst)实现。此外，还有基于该曲线的 BLS 签名方案的操作。

- G1-points and public keys: 48-byte slice.
- G2-points and signatures: 96-byte slice.
- Elements of field FP: 48-byte slice.
- Elements of field FP2: 96-byte slice.
- Messages: slice. Number of bits should be divisible by 8.

When input value is a point or a field element, the slice may have more than 48/96 bytes. In this case only the first 48/96 bytes are taken. If the slice has less bytes (or if message size is not divisible by 8), cell underflow exception is thrown.

#### High-level operations

These are high-level operations for verifying BLS signatures.

| xxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack                | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description                                                                                                                                                                 |
| :---------------------------- | :----------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `BLS_VERIFY`                  | _`pk msg sgn - bool`_                      | Checks BLS signature, return true on success, false otherwise.<br/>_61034 gas_                                                                                                                             |
| `BLS_AGGREGATE`               | _`sig_1 ... sig_n n - sig`_                | Aggregates signatures. `n>0`. Throw exception if `n=0` or if some `sig_i` is not a valid signature.<br/>_`gas=n*4350-2616`_                                                |
| `BLS_FASTAGGREGATEVERIFY`-    | _`pk_1 ... pk_n n msg sig - bool`_         | Checks aggregated BLS signature for keys `pk_1...pk_n` and message `msg`. Return true on success, false otherwise. Return false if `n=0`.<br/>_`gas=58034+n*3000`_         |
| `BLS_AGGREGATEVERIFY`         | _`pk_1 msg_1 ... pk_n msg_n n sgn - bool`_ | Checks aggregated BLS signature for key-message pairs `pk_1 msg_1...pk_n msg_n`. Return true on success, false otherwise. Return false if `n=0`.<br/>_`gas=38534+n*22500`_ |

`VERIFY` instructions don't throw exception on invalid signatures and public keys (except for cell underflow exceptions), they return false instead.

#### Low-level operations

These are arithmetic operations on group elements.

| xxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack                     | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description                                                                                                                                                                                                                      |
| :---------------------------- | :---------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `BLS_G1_ADD`                  | _`x y - x+y`_                                   | Addition on G1.<br/>_3934 gas_                                                                                                                                                                                                                                  |
| `BLS_G1_SUB`                  | _`x y - x-y`_                                   | Subtraction on G1.<br/>_3934 gas_                                                                                                                                                                                                                               |
| `BLS_G1_NEG`                  | _`x - -x`_                                      | Negation on G1.<br/>_784 gas_                                                                                                                                                                                                                                   |
| `BLS_G1_MUL`                  | _`x s - x*s`_                                   | Multiplies G1 point `x` by scalar `s`.<br/>Any `s` is valid, including negative.<br/>_5234 gas_                                                                                                                                                 |
| `BLS_G1_MULTIEXP`             | _`x_1 s_1 ... x_n s_n n - x_1*s_1+...+x_n*s_n`_ | Calculates `x_1*s_1+...+x_n*s_n` for G1 points `x_i` and scalars `s_i`. Returns zero point if `n=0`.<br/>Any `s_i` is valid, including negative.<br/>_`gas=11409+n*630+n/floor(max(log2(n),4))*8820`_                           |
| `BLS_G1_ZERO`                 | _`- zero`_                                      | Pushes zero point in G1.<br/>_34 gas_                                                                                                                                                                                                                           |
| `BLS_MAP_TO_G1`               | _`f - x`_                                       | Converts FP element `f` to a G1 point.<br/>_2384 gas_                                                                                                                                                                                                           |
| `BLS_G1_INGROUP`              | _`x - bool`_                                    | Checks that slice `x` represents a valid element of G1.<br/>_2984 gas_                                                                                                                                                                                          |
| `BLS_G1_ISZERO`               | _`x - bool`_                                    | Checks that G1 point `x` is equal to zero.<br/>_34 gas_                                                                                                                                                                                                         |
| `BLS_G2_ADD`                  | _`x y - x+y`_                                   | Addition on G2.<br/>_6134 gas_                                                                                                                                                                                                                                  |
| `BLS_G2_SUB`                  | _`x y - x-y`_                                   | Subtraction on G2.<br/>_6134 gas_                                                                                                                                                                                                                               |
| `BLS_G2_NEG`                  | _`x - -x`_                                      | Negation on G2.<br/>_1584 gas_                                                                                                                                                                                                                                  |
| `BLS_G2_MUL`                  | _`x s - x*s`_                                   | Multiplies G2 point `x` by scalar `s`.<br/>Any `s` is valid, including negative.<br/>_10584 gas_                                                                                                                                                |
| `BLS_G2_MULTIEXP`             | _`x_1 s_1 ... x_n s_n n - x_1*s_1+...+x_n*s_n`_ | Calculates `x_1*s_1+...+x_n*s_n` for G2 points `x_i` and scalars `s_i`. Returns zero point if `n=0`.<br/>Any `s_i` is valid, including negative.<br/>_`gas=30422+n*1280+n/floor(max(log2(n),4))*22840`_                         |
| `BLS_G2_ZERO`                 | _`- zero`_                                      | Pushes zero point in G2.<br/>_34 gas_                                                                                                                                                                                                                           |
| `BLS_MAP_TO_G2`               | _`f - x`_                                       | Converts FP2 element `f` to a G2 point.<br/>_7984 gas_                                                                                                                                                                                                          |
| `BLS_G2_INGROUP`              | _`x - bool`_                                    | Checks that slice `x` represents a valid element of G2.<br/>_4284 gas_                                                                                                                                                                                          |
| `BLS_G2_ISZERO`               | _`x - bool`_                                    | Checks that G2 point `x` is equal to zero.<br/>_34 gas_                                                                                                                                                                                                         |
| `BLS_PAIRING`                 | _`x_1 y_1 ... x_n y_n n - bool`_                | Given G1 points `x_i` and G2 points `y_i`, calculates and multiply pairings of `x_i,y_i`. Returns true if the result is the multiplicative identity in FP12, false otherwise. Returns false if `n=0`.<br/>_`gas=20034+n*11800`_ |
| `BLS_PUSHR`                   | _`- r`_                                         | Pushes the order of G1 and G2 (approx. `2^255`).<br/>_34 gas_                                                                                                                                                                |

`INGROUP`, `ISZERO` don't throw exception on invalid points (except for cell underflow exceptions), they return false instead.

`INGROUP`，`ISZERO`在无效的点上（除了cell下溢异常）不会引发异常，而是返回false。

## RUNVM

Currently there is no way for code in TVM to call external untrusted code "in sandbox". In other words, external code always can irreversibly update code, data of contract, or set actions (such as sending all money).
`RUNVM` instruction allows to spawn an independent VM instance, run desired code and get needed data (stack, registers, gas consumption etc) without risks of polluting caller's state. Running arbitrary code in a safe way may be useful for [v4-style plugins](/participate/wallets/contracts#wallet-v4), Tact's `init` style subcontract calculation etc.

| xxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxxxxxxxxxx<br/>Stack                                                                              | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description                                                                                                                                                                           |
| :---------------------------- | :------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `flags RUNVM`                 | _`x_1 ... x_n n code [r] [c4] [c7] [g_l] [g_m] - x'_1 ... x'_m exitcode [data'] [c4'] [c5] [g_c]`_       | Runs child VM with code `code` and stack `x_1...x_n`. Returns the resulting stack `x'_1...x'_m` and exitcode.<br/>Other arguments and return values are enabled by flags, see below. |
| `RUNVMX`                      | _`x_1 ... x_n n code [r] [c4] [c7] [g_l] [g_m] flags - x'_1 ... x'_m exitcode [data'] [c4'] [c5] [g_c]`_ | Same thing, but pops flags from stack.                                                                                                                                                                               |

Flags are similar to `runvmx` in fift:

- `+1`: set c3 to code
- `+2`: push an implicit 0 before running the code
- `+4`: take `c4` from stack (persistent data), return its final value
- `+8`: take gas limit `g_l` from stack, return consumed gas `g_c`
- `+16`: take `c7` from stack (smart-contract context)
- `+32`: return final value of `c5` (actions)
- `+64`: pop hard gas limit (enabled by ACCEPT) `g_m` from stack
- `+128`: "isolated gas consumption". Child VM will have a separate set of visited cells and a separate chksgn counter.
- `+256`: pop integer `r`, return exactly `r` values from the top of the stack (only if `exitcode=0 or 1`; if not enough then `exitcode=stk_und`)

Gas cost:

- 66 gas
- 1 gas for every stack element given to the child VM (first 32 are free)
- 1 gas for every stack element returned from the child VM (first 32 are free)

## Sending messages

Currently it is difficult to calculate cost of sending message in contract (which leads to some approximations like in [jettons](https://github.com/ton-blockchain/token-contract/blob/main/ft/jetton-wallet.fc#L94)) and impossible to bounce request back if action phase is incorrect. It is also impossible to accurately subtract from incoming message sum of "constant fee for contract logic" and "gas expenses".

- `SENDMSG` takes a cell and mode as input. Creates an output action and returns a fee for creating a message. Mode has the same effect as in the case of SENDRAWMSG. Additionally `+1024` means - do not create an action, only estimate fee. Other modes affect the fee calculation as follows: `+64` substitutes the entire balance of the incoming message as an outcoming value (slightly inaccurate, gas expenses that cannot be estimated before the computation is completed are not taken into account), `+128` substitutes the value of the entire balance of the contract before the start of the computation phase (slightly inaccurate, since gas expenses that cannot be estimated before the completion of the computation phase are not taken into account).
- `SENDRAWMSG`, `RAWRESERVE`, `SETLIBCODE`, `CHANGELIB` - `+16` flag is added, that means in the case of action fail - bounce transaction. No effect if `+2` is used.
