import Feedback from '@site/src/components/Feedback';

# Transaction fees

每个TON用户都应该记住，*手续费取决于许多因素*。

## Gas

所有费用都以Gas计算。这是TON中用作费用的特殊货币。

所有费用都以一定数量的gas来指定和固定，但gas价格本身并不固定。今天的gas价格为：

当前的基础链设置如下：1 单位 gas 耗费 400  nanotons  。

```cpp
1 gas = 26214400 / 2^16 nanotons = 0.000 000 4 TON
```

主链的当前设置如下：1 单位 gas 耗费 10000  nanotons  。

```cpp
1 gas = 655360000 / 2^16 nanotons = 0.000 01 TON
```

### 平均交易成本

> **TLDR：** 今天，每笔交易的成本约为 **~0.005  TON**

像TON的许多其他参数一样，gas费用是可配置的，可以通过主网上的特殊投票来更改。

:::info
当前 gas 量分别写入主链和基链的网络配置 [param 20](https://tonviewer.com/config#20) 和 [param 21](https://tonviewer.com/config#21)。
:::

### Gas 的成本会更高吗？

与 TON 的许多其他参数一样， gas 费也是可配置的，可以通过主网的特别投票进行更改。

Changing any parameter requires approval from 66% of the validators' votes.

#### gas 价格会更贵吗？

> *这是否意味着有一天gas价格可能会上涨1000倍甚至更多？*

TON上的费用难以提前计算，因为它们的数量取决于交易运行时间、账户状态、消息内容和大小、区块链网络设置以及无法在交易发送之前计算的其他许多变量。阅读关于[计算费用](/develop/howto/fees-low-level#computation-fees)的低层级文章概述。

这就是为什么即使NFT市场通常会额外收取大约1 TON的TON，并在稍后返还(*`1 - transaction_fee`*)。

### 如何计算费用？

TON 的费用很难提前计算，因为其金额取决于交易运行时间、账户状态、信息内容和大小、区块链网络设置以及其他一些变量，在交易发送之前无法计算。

That is why NFT marketplaces typically require an extra amount of TON (~1 TON) and refund the remaining amount (1 - transaction_fee) after the transaction.

:::info
Each contract should check incoming messages for the amount of TON attached to ensure it is enough to cover the fees.

查看[低级收费概述](/v3/documentation/smart-contracts/transaction-fees/fees-low-level)，了解更多佣金计算公式；查看[收费计算](/v3/guidelines/smart-contracts/fee-calculation)，了解如何使用新的 TVM 操作码计算 FunC 合约中的收费。
:::

不过，让我们进一步了解一下 TON 的收费功能。

## Basic fees formula

TON验证者从智能合约收取存储费用。

```cpp
transaction_fee = storage_fees
                + in_fwd_fees // also named import_fee
                + computation_fees
                + action_fees
                + out_fwd_fees
```

```jsx live
// Welcome to LIVE editor!
// feel free to change any variables
// Check https://retracer.ton.org/?tx=b5e14a9c4a4e982fda42d6079c3f84fa48e76497a8f3fca872f9a3737f1f6262

function FeeCalculator() {
  // https://tonviewer.com/config#25
  const lump_price = 400000;
  const bit_price = 26214400;
  const cell_price = 2621440000;
  const ihr_price_factor = 98304;
  const first_frac = 21845;
  const nano = 10 ** -9;
  const bit16 = 2 ** 16;

  const ihr_disabled = 0; // First of all define is ihr gonna be counted

  let fwd_fee =
    lump_price + Math.ceil((bit_price * 0 + cell_price * 0) / bit16);

  if (ihr_disabled) {
    var ihr_fee = 0;
  } else {
    var ihr_fee = Math.ceil((fwd_fee * ihr_price_factor) / bit16);
  }

  let total_fwd_fees = fwd_fee + ihr_fee;
  let gas_fees = 0.0011976; // Gas fees out of scope here
  let storage_fees = 0.000000003; // And storage fees as well
  let total_action_fees = +((fwd_fee * first_frac) / bit16).toFixed(9);
  let import_fee =
    lump_price + Math.ceil((bit_price * 528 + cell_price * 1) / bit16);
  let total_fee =
    gas_fees + storage_fees + total_action_fees * nano + import_fee * nano;

  return (
    <div>
      <p> Total fee: {+total_fee.toFixed(9)} TON</p>
      <p> Action fee: {+(total_action_fees * nano).toFixed(9)} TON </p>
      <p> Fwd fee: {+(total_fwd_fees * nano).toFixed(9)} TON </p>
      <p> Import fee: {+(import_fee * nano).toFixed(9)} TON </p>
      <p> IHR fee: {+(ihr_fee * nano).toFixed(9)} TON </p>
    </div>
  );
}
```

## Elements of transaction fee

- `storage_fees` is the amount you pay for storing a smart contract in the blockchain. In fact, you pay for every second the smart contract is stored on the blockchain.
  - *Example*: your TON wallet is also a smart contract, and it pays a storage fee every time you receive or send a transaction. Read more about [how storage fees are calculated](/v3/documentation/smart-contracts/transaction-fees/fees-low-level#storage-fee).
- `in_fwd_fees` is a charge for importing messages only from outside the blockchain, e.g. `external` messages. Every time you make a transaction, it must be delivered to the validators who will process it. For ordinary messages from contract to contract this fee is not applicable. Read [the TON Blockchain paper](https://docs.ton.org/tblkch.pdf) to learn more about inbound messages.
  - *Example*: each transaction you make with your wallet app (like Tonkeeper) requires first to be distributed among validation nodes.
- `computation_fees` is the amount you pay for executing code in the virtual machine. The larger the code, the more fees must be paid.
  - *Example*: each time you send a transaction with your wallet (which is a smart contract), you execute the code of your wallet contract and pay for it.
- `action_fees` is a charge for sending outgoing messages made by a smart contract, updating the smart contract code, updating the libraries, etc.
- `out_fwd_fees` stands for a charge for sending messages outside the TON Blockchain to interact with off-chain services (e.g., logs) and external blockchains.

## FAQ

Here are the most frequently asked questions by visitors of TON:

### Fees for sending TON?

The average fee for sending any amount of TON is 0.0055 TON.

### Fees for sending Jettons?

The average fee for sending any amount of a custom Jettons is 0.037 TON.

### Cost of minting NFTs?

The average fee for minting one NFT is 0.08 TON.

### Cost of saving data in TON?

Saving 1 MB of data for one year on TON will cost 6.01 TON. Note that you usually don't need to store large amounts of data on-chain. Consider using [TON Storage](/v3/guidelines/web3/ton-storage/storage-daemon) if you need decentralized storage.

### Is it possible to send a gasless transaction?

In TON, gasless transactions are possible using [wallet v5](/v3/documentation/smart-contracts/contracts-specs/wallet-contracts#preparing-for-gasless-transactions) a relayer that pays the gas fee for transaction.

### How to calculate fees?

There is an article about [fee calculation](/v3/guidelines/smart-contracts/fee-calculation) in TON Blockchain.

## References

- Based on the [@thedailyton article](https://telegra.ph/Commissions-on-TON-07-22) - *[menschee](https://github.com/menschee)*

## See also

- [Low-level fees overview](/v3/documentation/smart-contracts/transaction-fees/fees-low-level)—read about the formulas for calculating commissions.
- [Smart contract function to calculate forward fees in FunC](https://github.com/ton-blockchain/token-contract/blob/main/misc/forward-fee-calc.fc)

<Feedback />

