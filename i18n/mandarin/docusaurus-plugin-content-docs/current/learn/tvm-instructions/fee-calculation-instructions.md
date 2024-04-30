# TVM Upgrade 2024.04

## Introduction of new instructions for cheap fee calculation

:::tip
This upgrade is active in mainnet since March 16 (see https://t.me/tonstatus/101). Preview of this update for blueprint is available in `@ton/sandbox@0.16.0-tvmbeta.3`, `@ton-community/func-js@0.6.3-tvmbeta.3` and `@ton-community/func-js-bin@0.4.5-tvmbeta.3` packages.
:::

This update is activated by Config8 `version` >= 6.

## c7

**c7** tuple extended from 14 to 16 elements:

* **14**: tuple that contains some config parameters as cell slices. If the parameter is absent from the config, the value is null.
  * **0**: `StoragePrices` from `ConfigParam 18`. Not the whole dict, but only the one StoragePrices entry that corresponds to the current time.
  * **1**: `ConfigParam 19` (global id).
  * **2**: `ConfigParam 20` (mc gas prices).
  * **3**: `ConfigParam 21` (gas prices).
  * **4**: `ConfigParam 24` (mc fwd fees).
  * **5**: `ConfigParam 25` (fwd fees).
  * **6**: `ConfigParam 43` (size limits).
* **15**: "[due payment](https://github.com/ton-blockchain/ton/blob/8a9ff339927b22b72819c5125428b70c406da631/crypto/block/block.tlb#L237)" - current debt for storage fee (nanotons). Asm opcode: `DUEPAYMENT`.
* **16**: "precompiled gas usage" - gas usage for the current contract if it is precompiled (see ConfigParam 45), null otherwise. Asm opcode: `GETPRECOMPILEDGAS`.

The idea behind this extension of c7 by unpacked config parameters is the following: this data will be retrieved from global configuration by transaction executor, so it is already presented in memory of executor. However (before extension) smart-contract need to get all of these parameters one-by-one from configuration dictionary which is expensive and potentially unpredictable by gas (since cost depends on number of parameters).

Due payment is needed so contract can properly assess storage fees: when message sent in default (bouncable) mode to smart-contract, storage fees are deducted (or added to due_payment field that contains storage fee related debt) prior message value is added to balance. Thus, if contract after processing message send gas excesses back with mode=64, that means that if contract balance hit 0, on next transactions storage fees start accruing in due_payment (and not deducted from incoming messages). That way debt will silently accumulate until account freezes. `DUEPAYMENT` allows developer explicitly account/withhold comission for storage and thus prevent any issues.

## New opcodes

### Opcodes to work with new c7 values

26 gas for each, except for `SENDMSG` (because of cell operations).

| xxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxx<br/>Stack | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description                                                                                                                          |
| :------------------------------------- | :------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `UNPACKEDCONFIGTUPLE`                  | *`- c`*             | Retrieves tuple of configs slices from c7                                                                                                                                      |
| `DUEPAYMENT`                           | *`- i`*             | Retrieves value of due payment from c7                                                                                                                                         |
| `GLOBALID`                             | *`- i`*             | Now retrieves  `ConfigParam 19` from from c7, ton form config dict.                                                                                            |
| `SENDMSG`                              | *`msg mode - i`*    | Now retrieves `ConfigParam 24/25` (message prices) and `ConfigParam 43` (`max_msg_cells`) from c7, not from config dict. |

### Opcodes to process config parameters

The introduction of tuple of configurations slices in the TON transaction executor has made it more cost-effective to parse fee parameters. However, as new config parameters constructors may be introduced in the future, smart contracts may need to be updated to interpret these new parameters. To address this issue, special opcodes for fee calculation have been introduced. These opcodes read parameters from c7 and calculate fees in the same manner as the executor. With the introduction of new parameters constructors, these opcodes will be updated to accommodate the changes. This allows smart contracts to rely on these instructions for fee calculation without needing to interpret all types of constructors.

26 gas for each.

| xxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxx<br/>Stack                  | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| :------------------------------------- | :----------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `GETGASFEE`                            | *`gas_used is_mc - price`*           | Calculates computation cost in nanotons for transaction that consumes *`gas_used`* gas.                                                                                                                                                                                                                                                                                                                                                                                                       |
| `GETSTORAGEFEE`                        | *`cells bits seconds is_mc - price`* | Calculates storage fees in nanotons for contract based on current storage prices. `cells` and `bits` are the size of the [`AccountState`](https://github.com/ton-blockchain/ton/blob/8a9ff339927b22b72819c5125428b70c406da631/crypto/block/block.tlb#L247) (with deduplication, including root cell).                                                                                                                                                      |
| `GETFORWARDFEE`                        | *`cells bits is_mc - price`*         | Calculates forward fees in nanotons for outgoing message. *`is_mc`* is true if the source or the destination is in masterchain, false if both are in basechain. Note, cells and bits in Message should be counted with account for deduplication and *root-is-not-counted* rules.                                                                                                                                                                             |
| `GETPRECOMPILEDGAS`                    | *`- null`*                           | reserved, currently returns `null`. Will return cost of contract execution in gas units if this contract is *precompiled*                                                                                                                                                                                                                                                                                                                                                                     |
| `GETORIGINALFWDFEE`                    | *`fwd_fee is_mc - orig_fwd_fee`*     | calculate `fwd_fee * 2^16 / first_frac`. Can be used to get the original `fwd_fee` of the message (as replacement for hardcoded values like [this](https://github.com/ton-blockchain/token-contract/blob/21e7844fa6dbed34e0f4c70eb5f0824409640a30/ft/jetton-wallet.fc#L224C17-L224C46)) from `fwd_fee` parsed from incoming message. *`is_mc`* is true if the source or the destination is in masterchain, false if both are in basechain. |
| `GETGASFEESIMPLE`                      | *`gas_used is_mc - price`*           | Calculates additional computation cost in nanotons for transaction that consumes additional *`gas_used`*. In other words, same as `GETGASFEE`, but without flat price (just `(gas_used * price) / 2^16`).                                                                                                                                                                                                                                                  |
| `GETFORWARDFEESIMPLE`                  | *`cells bits is_mc - price`*         | Calculates additional forward cost in nanotons for message that contains additional *`cells`* and *`bits`*. In other words, same as `GETFORWARDFEE`, but without lump price (just `(bits*bit_price + cells*cell_price) / 2^16`).                                                                                                                                                                                                                           |

`gas_used`, `cells`, `bits`, `time_delta` are integers in range `0..2^63-1`.

### Cell level operations

Operations for working with Merkle proofs, where cells can have non-zero level and multiple hashes.
26 gas for each.

| xxxxxxxxxxxxxxxxxxxxxx<br/>Fift syntax | xxxxxxxxx<br/>Stack   | xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx<br/>Description |
| :------------------------------------- | :-------------------- | :---------------------------------------------------- |
| `CLEVEL`                               | *`cell - level`*      | Returns level of the cell                             |
| `CLEVELMASK`                           | *`cell - level_mask`* | Returns level mask of the cell                        |
| `i CHASHI`                             | *`cell - hash`*       | Returns `i`th hash of the cell                        |
| `i CDEPTHI`                            | *`cell - depth`*      | Returns `i`th depth of the cell                       |
| `CHASHIX`                              | *`cell i - depth`*    | Returns `i`th hash of the cell                        |
| `CDEPTHIX`                             | *`cell i - depth`*    | Returns `i`th depth of the cell                       |

`i` is in range `0..3`.
