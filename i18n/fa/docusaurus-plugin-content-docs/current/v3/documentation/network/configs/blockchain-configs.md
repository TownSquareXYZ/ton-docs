import Feedback from '@site/src/components/Feedback';

# Config parameters

:::info
You can view live values by using [Tonviewer](https://tonviewer.com/config).
:::

## Introduction

This page provides a description of the configuration parameters used in the TON Blockchain.

TON features a complex configuration consisting of many technical parameters, some of which are utilized by the blockchain itself, while others serve the ecosystem. However, only a limited number of individuals fully understand the significance of these parameters. This article aims to offer users a straightforward explanation of each parameter and its purpose.

## Prerequisites

This material should be read alongside the parameter list.

You can view the parameter values in the [current configuration](https://explorer.toncoin.org/config), and the method of writing them into [cells](/v3/concepts/dive-into-ton/ton-blockchain/cells-as-data-storage) is outlined in the [block.tlb](https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb) file in [TL-B](/v3/documentation/data-formats/tlb/tl-b-language) format.

:::info
The binary encoding found at the end of the TON Blockchain parameter represents a serialized binary format of its configuration. This allows for efficient storage and transmission of the configuration data. The specific details of the serialization process vary depending on the encoding scheme utilized by the TON Blockchain.
:::

All parameters are in place, and you won't get lost. For your convenience, please use the right sidebar for quick navigation.

## پارامتر ۰

این پارامتر آدرس یک قرارداد هوشمند ویژه است که پیکربندی بلاکچین را ذخیره می‌کند. پیکربندی در قرارداد ذخیره می‌شود تا بارگذاری و تغییر آن در طول رأی‌گیری اعتبارسنج‌ها ساده شود.

:::info
In the configuration parameter, only the hash portion of the address is recorded, as the contract always resides in the [MasterChain](/v3/concepts/dive-into-ton/ton-blockchain/blockchain-of-blockchains#masterchain-blockchain-of-blockchains) (WorkChain -1). Therefore, the full address of the contract will be written as `-1:<value of the configuration parameter>`.
:::

## پارامتر ۱

This parameter is the address of the [elector smart contract](/v3/documentation/smart-contracts/contracts-specs/governance#elector), responsible for appointing validators, distributing rewards, and voting on changes to blockchain parameters.

## پارامتر ۲

This parameter represents the address of the system, on behalf of which new Toncoins are minted and sent as rewards for validating the blockchain.

:::info
If the parameter 2 is missing, the parameter 0 is used instead (newly minted Toncoins come from the configuration smart contract).
:::

## پارامتر ۳

این پارامتر آدرس جمع‌آوری‌کننده هزینه تراکنش است.

:::info
If the this parameter is missing (for the time being), transaction fees are directed to the elector smart contract (parameter 1).
:::

## پارامتر ۴

این پارامتر آدرس قرارداد روت DNS شبکه TON است.

:::info
More detailed information, please see the [TON DNS & Domains](/v3/guidelines/web3/ton-dns/dns) documentation and in a more detailed original description [here](https://github.com/ton-blockchain/TEPs/blob/master/text/0081-dns-standard.md).

This contract is not responsible for selling **.ton** domains.
:::

## پارامتر ۶

این پارامتر مسئول هزینه‌های ساخت رشته‌های جدید است.

:::info
Currently, the minting of additional currency is not implemented and does not function. The implementation and launch of the minter are planned for the future.

You can learn more about the issues and prospects in the [relevant documentation](/v3/documentation/infra/minter-flow).
:::

## پارامتر ۷

This parameter stores the volume of each additional currency in circulation. The data is organized as a dictionary (also referred to as a **hashmap**, although this name may be a typo during the TON Blockchain's development). The structure uses the format `extracurrency_id -> amount`, where the amount is represented as a `VarUint 32`, which is an integer ranging from `0` to `2^248`.

## پارامتر ۸

این پارامتر نشان‌دهنده نسخه شبکه و قابلیت‌های اضافی است که توسط اعتبارسنج‌ها پشتیبانی می‌شود.

:::info
Validators are nodes in the TON Blockchain network that are responsible for creating new blocks and verifying transactions.
:::

- `version`: این فیلد نسخه را مشخص می‌کند.

- `قابلیت‌ها`: این فیلد مجموعه‌ای از نشانه‌ها است که برای نشان دادن وجود یا عدم وجود قابلیت‌ها یا ویژگی‌های خاصی استفاده می‌شود.

Thus, when updating the network, validators will vote to change parameter 8. This way, the TON Blockchain network can be updated without downtime.

## پارامتر ۹

این پارامتر شامل یک لیست (درخت باینری) از پارامترهای اجباری است. این اطمینان حاصل می‌کند که پارامترهای خاصی از پیکربندی همواره وجود دارند و تا زمانی که پارامتر ۹ تغییر نکند، نمی‌توان آنها را با پیشنهاد تغییر پیکربندی حذف کرد.

## پارامتر ۱۰

This parameter represents a list (binary tree) of critical TON parameters whose change significantly affects the network, so more voting rounds are held.

## پارامتر ۱۱

این پارامتر مشخص می‌کند که تحت چه شرایطی پیشنهادهای تغییر پیکربندی TON پذیرفته می‌شوند.

- `min_tot_rounds`: The minimum number of rounds before a proposal can be applied

- `max_tot_rounds`: The maximum number of rounds, upon reaching which the proposal will automatically be rejected

- `min_wins`: The required number of wins (3/4 of validators by the sum of the pledge must vote in favor)

- `max_losses`: The maximum number of losses, upon reaching which the proposal will automatically be rejected

- `min_store_sec` و `max_store_sec` بازه زمانی ممکن را تعیین می‌کنند که در طی آن پیشنهاد ذخیره می‌شود

- `bit_price` و `cell_price` قیمت ذخیره‌سازی یک بیت یا یک Cell از پیشنهاد را نشان می‌دهند

## پارامتر ۱۲

This parameter represents the configuration of a WorkChain in the TON Blockchain. WorkChains are designed as independent blockchains that can operate in parallel, allowing TON to scale and process a large number of transactions and smart contracts.

### WorkChain configuration parameters

- `enabled_since`: A UNIX timestamp of the moment this WorkChain was enabled.

- `actual_min_split`: The minimum depth of the split (sharding) of this WorkChain, supported by validators.

- `min_split`: The minimum depth of the split of this WorkChain, set by the configuration.

- `max_split`: The maximum depth of the split of this WorkChain.

- `basic`: A boolean flag (1 for true, 0 for false) indicating whether this WorkChain is basic (handles TON coins, smart contracts based on the TON Virtual Machine).

- `active`: A boolean flag indicating whether this WorkChain is active at the moment.

- `accept_msgs`: A boolean flag indicating whether this WorkChain is accepting messages at the moment.

- `flags`: Additional flags for the WorkChain (reserved, currently always 0).

- `zerostate_root_hash` and `zerostate_file_hash`: Hashes of the first block of the WorkChain.

- `version`: Version of the WorkChain.

- `format`: The format of the WorkChain, which includes `vm_version` and `vm_mode` - the virtual machine used there.

## پارام ۱۳

This parameter defines the cost of filing complaints about incorrect operation of validators in the [elector smart contract](/v3/documentation/smart-contracts/contracts-specs/governance#elector).

## پارام ۱۴

This parameter indicates the reward for creating a block in the TON Blockchain. Nanograms represent nanoToncoins. Therefore, the reward for block creation in the MasterChain is 1.7 Toncoins, while in the basic WorkChain, it is 1.0 Toncoins. In the event of a WorkChain split, the block reward is also divided: if there are two ShardChains within the WorkChain, then the reward for each shard block will be 0.5 Toncoins.

## پارام ۱۵

این پارامتر مدت زمان مراحل مختلف انتخابات و کار اعتبارسنج‌ها در بلاکچین TON را نشان می‌دهد.

For each validation period, there is an `election_id` equal to the UNIX-format time at the start of the validation.

You can get the current `election_id` (if elections are ongoing) or the past one by invoking the elector smart contract's respective get-methods `active_election_id` and `past_election_ids`.

### WorkChain configuration parameters

- `validators_elected_for`: The number of seconds the elected set of validators perform their role (one round).

- `elections_start_before`: The seconds before the end of the current round the election process for the next period will start.

- `elections_end_before`: The seconds before the end of the current round, the validators for the next round will be chosen.

- `stake_held_for`: The period for which a validator's stake is held (for handling complaints) after the round expires.

:::info
هر مقدار در آرگومان‌ها توسط نوع داده `uint32` تعیین می‌شود.
:::

### مثال‌ها

In the TON Blockchain, validation periods are typically divided into **even** and **odd** rounds that alternate. Voting for the next round occurs during the previous one, so a validator must allocate their funds into two separate pools to participate in both rounds.

#### Mainnet

مقادیر فعلی:

```python
constants = {
    'validators_elected_for': 65536,  # 18.2 hours
    'elections_start_before': 32768,  # 9.1 hours
    'elections_end_before': 8192,     # 2.2 hours
    'stake_held_for': 32768           # 9.1 hours
}
```

طرح:

![image](/img/docs/blockchain-configs/config15-mainnet.png)

#### چگونه دوره‌ها را محاسبه کنیم?

فرض کنید `election_id = validation_start = 1600032768`. سپس:

```python
election_start = election_id - constants['elections_start_before'] = 1600032768 - 32768 = 1600000000
election_end = delay_start = election_id - constants['elections_end_before'] = 1600032768 - 8192 = 1600024576
hold_start = validation_end = election_id + constants['validators_elected_for'] = 1600032768 + 65536 = 1600098304
hold_end = hold_start + constants['stake_held_for'] = 1600098304 + 32768 = 1600131072
```

Therefore, at this time, the length of one round of one parity is `1600131072 - 1600000000 = 131072 seconds = 36.40888... hours`

#### Testnet

مقادیر فعلی:

```python
constants = {
    'validators_elected_for': 7200,  # 2 hours
    'elections_start_before': 2400,  # 40 minutes
    'elections_end_before': 180,     # 3 minutes
    'stake_held_for': 900            # 15 minutes
}
```

Scheme:

![image](/img/docs/blockchain-configs/config15-testnet.png)

#### چگونه دوره‌ها را محاسبه کنیم?

فرض کنید `election_id = validation_start = 160002400`. سپس:

```python
election_start = election_id - constants['elections_start_before'] = 160002400 - 2400 = 1600000000
election_end = delay_start = election_id - constants['elections_end_before'] = 160002400 - 180 = 160002220
hold_start = validation_end = election_id + constants['validators_elected_for'] = 160002400 + 7200 = 160009600
hold_end = hold_start + constants['stake_held_for'] = 160009600 + 900 = 160010500
```

Therefore, at this time, the length of one round of one parity is `160010500 - 1600000000 = 10500 seconds = 175 minutes = 2.91666... hours`

## پارام ۱۶

This parameter represents the limits on the number of validators in the TON Blockchain. It is directly used by the elector smart contract.

### Configuration parameters for the number of validators for elections

- `max_validators`: این پارامتر حداکثر تعداد اعتبارسنج‌هایی که می‌توانند در عملیات شبکه در هر زمان معین شرکت کنند را نشان می‌دهد.

- `max_main_validators`: این پارامتر حداکثر تعداد اعتبارسنج‌های masterchain را نشان می‌دهد.

- `min_validators`: این پارامتر حداقل تعداد اعتبارسنج‌هایی که باید عملیات شبکه را پشتیبانی کنند را نشان می‌دهد.

#### Notes

- The maximum number of validators is greater than or equal to the maximum number of MasterChain validators.

- The maximum number of MasterChain validators must be greater than or equal to the minimum number of validators.

- حداقل تعداد اعتبارسنج‌ها نباید کمتر از ۱ باشد.

## پارام ۱۷

این پارامتر نشان‌دهنده پیکربندی پارامترهای سهام در بلاکچین TON است. در بسیاری از سیستم‌های بلاکچین، به‌ویژه آن‌هایی که از الگوریتم اجماع Proof-of-Stake یا Delegated Proof-of-Stake استفاده می‌کنند، صاحبان ارز رمزنگاری متعلق به شبکه می‌توانند توکن‌های خود را "سهام" کنند تا به اعتبارسنج‌ها تبدیل شوند و پاداش دریافت کنند.

### Configuration parameters

- `min_stake`: This parameter represents the minimum amount of Toncoins that an interested party needs to stake to participate in the validation process.

- `max_stake`: This parameter represents the maximum amount of Toncoins that an interested party can stake.

- `min_total_stake`: This parameter represents the minimum total amount of Toncoins that the chosen set of validators must hold.

- `max_stake_factor`: این پارامتر یک ضریب ضرب است که نشان می‌دهد چقدر می‌تواند بیشترین سهام مؤثر (پیش‌نیاز) از حداقل سهامی که توسط هر اعتبارسنج دیگر ارسال شده است افزایش یابد.

:::info
هر مقدار در آرگومان‌ها توسط نوع داده `uint32` تعیین می‌شود.
:::

## پارام ۱۸

این پارامتر نمایانگر پیکربندی برای تعیین قیمت‌های ذخیره‌سازی داده در بلاکچین TON است. این به عنوان یک معیار برای جلوگیری از اسپم و تشویق به نگهداری شبکه عمل می‌کند.

### Dictionary of storage fee parameters

- `utime_since`: این پارامتر زمان سنج اولیه یونیکس را که از آن قیمت‌های مشخص شده اعمال می‌شوند، فراهم می‌کند.

- `bit_price_ps` and `cell_price_ps`: These parameters represent the storage prices for one bit or one cell of information in the main WorkChains of the TON Blockchain for 65536 seconds

- `mc_bit_price_ps` and `mc_cell_price_ps`: These parameters represent the prices for computational resources specifically in the TON MasterChain for 65536 seconds

:::info
`utime_since` accepts values in the `uint32` data type.

باقی‌مانده مقادیر در نوع داده `uint64` را می‌پذیرند.
:::

## پارامتر ۲۰ و ۲۱

این پارامترها هزینه محاسبات را در شبکه TON تعریف می‌کنند. پیچیدگی هر محاسبه در واحدهای گاز تخمین زده می‌شود.

- `flat_gas_limit` و `flat_gas_price`: مقدار شروع مشخصی از گاز با قیمتی برابر `flat_gas_price` فراهم می‌شود (برای جبران هزینه‌های راه اندازی ماشین مجازی TON).

- `gas_price`: این پارامتر قیمت گاز در شبکه، به عنوان نانوتون‌ها برای ۶۵۵۳۶ واحد گاز، را منعکس می‌کند.

- `gas_limit`: این پارامتر حداکثر مقدار گازی که برای هر تراکنش قابل مصرف است را نشان می‌دهد.

- `special_gas_limit`: این پارامتر محدودیت مقدار گاز قابل مصرف برای هر تراکنش یک قرارداد ویژه (سیستمی) را نشان می‌دهد.

- `gas_credit`: This parameter represents a credit in gas units provided to transactions to check an external message.

- `block_gas_limit`: این پارامتر حداکثر مقدار گاز قابل مصرف در یک بلوک واحد را نشان می‌دهد.

- `freeze_due_limit` and `delete_due_limit`: Limits of accumulated storage fees (in nanoToncoin) at which a contract is frozen and deleted, respectively.

:::info
You can find more about `gas_credit` and other parameters in the section of external messages [here](/v3/documentation/smart-contracts/transaction-fees/accept-message-effects#external-messages).
:::

## پارامتر ۲۲ و ۲۳

این پارامترها محدودیت‌های بلوک را تنظیم می‌کنند که با رسیدن به آن، بلوک نهایی می‌شود و فراخوان پیام‌های باقیمانده (در صورت وجود) به بلوک بعدی منتقل می‌شود.

### Configuration parameters

- `bytes`: این بخش محدودیت‌های اندازه بلوک بر حسب بایت را تنظیم می‌کند.

- `underload`: زیر بار حالتی است که شارد متوجه می‌شود که باری وجود ندارد و تمایل به ادغام دارد، اگر یک شارد مجاور تمایل داشته باشد.

- `soft_limit`: حد نرم - وقتی این محدودیت برسد، پردازش پیام‌های داخلی متوقف می‌شود.

- `hard_limit`: حد سخت - این حداکثر اندازه مطلق است.

- `gas`: This section sets the limits on the amount of gas that a block can consume. Gas, in the context of blockchain, is an indicator of computational work. The limits on underload, soft and hard limits, work the same as for size in bytes.

- `lt_delta`: This section sets the limits on the difference in logical time between the first and last transaction. Logical time is a concept used in the TON Blockchain for ordering events. The limits on underload, soft and hard limits, work the same as for size in bytes and gas.

:::info
If a shard has insufficient load and there is an intention to merge with a neighboring shard, the `soft_limit` indicates a threshold. When this threshold is exceeded, internal messages will stop being processed, while external messages will still be handled. External messages will continue to be processed until the total reaches a limit that is equal to half the sum of the `soft_limit` and `hard_limit`, or `(soft_limit + hard_limit) / 2`.
:::

## پارامتر ۲۴ و ۲۵

Parameter 24 represents the configuration for the cost of sending messages in the MasterChain of the TON Blockchain.

پارامتر ۲۵ پیکربندی هزینه ارسال پیام‌ها در همه موارد دیگر را نشان می‌دهد.

### Configuration parameters defining the costs of forwarding

- `lump_price`: این پارامتر به معنای قیمت پایه برای انتقال یک پیام است، صرف نظر از اندازه یا پیچیدگی آن.

- `bit_price`: این پارامتر هزینه هر بیت از انتقال پیام را نشان می‌دهد.

- `cell_price`: این پارامتر هزینه ارسال پیام به ازای هر Cell را منعکس می‌کند. Cell واحد اساسی ذخیره‌سازی داده‌ها در بلاکچین TON است.

- `ihr_price_factor`: This is a factor used to calculate the cost of immediate hypercube routing (IHR).

:::info
IHR is a method of message delivery in the TON Blockchain network, where messages are sent directly to the recipient's ShardChain.
:::

- `first_frac`: این پارامتر کسر باقیمانده‌ای را تعریف می‌کند که برای اولین انتقال در طول مسیر پیام استفاده خواهد شد.

- `next_frac`: این پارامتر کسر باقی‌مانده‌ای را تعریف می‌کند که برای انتقال‌های بعدی در طول مسیر پیام استفاده خواهد شد.

## پارامتر ۲۸

This parameter provides the configuration for the `Catchain` protocol in the TON Blockchain. `Catchain` is the lowest-level consensus protocol used in the TON to achieve agreement among validators.

### Configuration parameters

- `flags`: یک فیلد عمومی که می‌تواند برای تنظیم انواع پارامترهای دودویی استفاده شود. در این مورد، برابر ۰ است که به معنای تنظیم نشدن نشانگر خاصی می‌باشد.

- `shuffle_mc_validators`: مقدار Boolean که نشان می‌دهد آیا باید تأییدکنندگان مسترچین را شافل کرد یا نه. اگر این پارامتر به ۱ تنظیم شده باشد، تأییدکنندگان شافل می‌شوند؛ وگرنه، نخواهند شد.

- `mc_catchain_lifetime`: The lifetime of MasterChain's `Catchain` groups in seconds.

- `shard_catchain_lifetime`: The lifetime of ShardChain's `Catchain` groups in seconds.

- `shard_validators_lifetime`: The lifetime of a ShardChain's validators group in seconds.

- `shard_validators_num`: The number of validators in each ShardChain validation group.

## پارامتر ۲۹

This parameter provides the configuration for the consensus protocol above `Catchain` ([Param 28](#param-28)) in the TON Blockchain. The consensus protocol is a crucial component of a blockchain network, and it ensures that all nodes agree on the state of the distributed ledger.

### Configuration parameters

- `flags`: یک فیلد عمومی که می‌تواند برای تنظیم پارامترهای مختلف باینری استفاده شود. در این مورد، مقدار آن ۰ است که به معنی تنظیم نشدن نشانگر‌های خاص است.

- `new_catchain_ids`: A Boolean value indicating whether to generate new `Catchain` identifiers. If this parameter is set to 1, new identifiers will be generated. In this case, it is assigned the value of 1, which means that new identifiers will be generated.

- `round_candidates`: تعداد نامزدهایی که در هر دور از پروتکل اجماع بررسی می‌شوند. اینجا به ۳ تنظیم شده است.

- `next_candidate_delay_ms`: تأخیر به میلی‌ثانیه قبل از انتقال حق تولید یک بلوک سفارشی به اعتبارسنج بعدی. در اینجا، به ۲۰۰۰ میلی‌ثانیه (۲ ثانیه) تنظیم شده است.

- `consensus_timeout_ms`: زمان‌بندی برای اجماع بلوک به میلی‌ثانیه. در اینجا، به ۱۶۰۰۰ میلی‌ثانیه (۱۶ ثانیه) تنظیم شده است.

- `fast_attempts`: تعداد تلاش‌های "سریع" برای رسیدن به اجماع. در اینجا، به ۳ تنظیم شده است.

- `attempt_duration`: مدت زمان هر تلاش برای توافق. در اینجا به ۸ تنظیم شده است.

- `catchain_max_deps`: حداکثر تعداد وابستگی‌های یک بلوک Catchain. در اینجا به ۴ تنظیم شده است.

- `max_block_bytes`: حداکثر حجم یک بلوک به بایت. در اینجا به 2097152 بایت (۲ MB) تنظیم شده است.

- `max_collated_bytes`: حداکثر حجم اثبات‌های درستی‌سازی بلوک سریال شده به بایت. در اینجا به 2097152 بایت (۲ MB) تنظیم شده است.

- `proto_version`: نسخه پروتکل. در اینجا به ۲ تنظیم شده است.

- `catchain_max_blocks_coeff`: The coefficient limiting the rate of block generation in `Catchain`, [description](https://github.com/ton-blockchain/ton/blob/master/doc/catchain-dos.md). Here, it is set to 10000.

## پارامتر ۳۱

This parameter represents the configuration of smart contract addresses from which no fees are charged for either gas or storage and where **tick-tok** transactions can be created. The list usually includes governance contracts. The parameter is presented as a binary tree structure — a tree (HashMap 256), where the keys are a 256-bit representation of the address. Only addresses in the MasterChain can be present in this list.

## پارامتر ۳۲، ۳۴ و ۳۶

لیست اعتبارسنج‌ها از دور قبلی (۳۲)، فعلی (۳۴)، و بعدی (۳۶). پارامتر ۳۶ از پایان انتخابات تا شروع دور تنظیم شده است.

### Configuration parameters

- `cur_validators`: این لیست فعلی اعتبارسنج‌ها است. اعتبارسنج‌ها معمولاً مسئول اعتبارسنجی تراکنش‌ها در یک شبکه بلاکچین هستند.

- `utime_since` و `utime_until`: این پارامترها دوره زمانی که این اعتبارسنج‌ها فعال هستند را ارائه می‌دهند.

- `total` and `main`: These parameters provide the total number of validators and the number of validators validating the MasterChain in the network.

- `total_weight`: این وزن اعتبارسنج‌ها را جمع می‌کند.

- `list`: A list of validators in the tree format `id->validator-data`: `validator_addr`, `public_key`, `weight`, `adnl_addr`: These parameters provide details about each validator - their 256 addresses in the MasterChain, public key, weight, ADNL address (the address used at the network level of the TON).

## پارامتر ۴۰

This parameter defines the structure of the configuration for punishment for improper behavior (non-validation). In the absence of the parameter, the default fine size is 101 Toncoins.

### Configuration parameters

`MisbehaviourPunishmentConfig`: This data structure defines how improper behavior in the system is punished.

شامل چندین فیلد است:

- `default_flat_fine`: این بخش از جریمه به اندازه سهام وابسته نیست.

- `default_proportional_fine`: این بخش از جریمه با اندازه سهام اعتبارسنج متناسب است.

- `severity_flat_mult`: این ضریبی است که برای مقدار `default_flat_fine` برای تخلفات جدی توسط اعتبارسنج اعمال می‌شود.

- `severity_proportional_mult`: این ضریبی است که برای مقدار `default_proportional_fine` برای تخلفات جدی توسط اعتبارسنج اعمال می‌شود.

- `unpunishable_interval`: این پارامتر نمایانگر دوره‌ای است که در آن مجرمان مجازات نمی‌شوند تا مشکلات موقت شبکه یا سایر ناهنجاری‌ها را از بین ببرد.

- `long_interval`, `long_flat_mult`, `long_proportional_mult`: این پارامترها دوره "بلند" و ضریب‌ها برای جریمه‌های ثابت و متناسب برای رفتار نامناسب را تعریف می‌کنند.

- `medium_interval`, `medium_flat_mult`, `medium_proportional_mult`: به همین ترتیب، آنها یک دوره زمانی "متوسط" و ضرایب جریمه ثابت و نسبی برای رفتار نامناسب را تعریف می‌کنند.

## پارامتر ۴۳

This parameter relates to the size limits and other features of accounts and messages.

### Configuration parameters

- `max_msg_bits`: Maximum message size in bits.

- `max_msg_cells`: Maximum number of cells (a form of storage unit) a message can occupy.

- `max_library_cells`: Maximum number of cells that can be used for library cells.

- `max_vm_data_depth`: Maximum cell depth in messages and account state.

- `max_ext_msg_size`: Maximum external message size in bits.

- `max_ext_msg_depth`: Maximum external message depth. This could refer to the depth of the data structure within the message.

- `max_acc_state_cells`: Maximum number of cells that an account state can occupy.

- `max_acc_state_bits`: Maximum account state size in bits.

اگر غایب باشد، پارامترهای پیش‌فرض برداشت می‌شوند:

- `max_size` = 65535

- `max_depth` = ۵۱۲

- `max_msg_bits` = ۱ \<\< ۲۱

- `max_msg_cells` = ۱ \<\< ۱۳

- `max_library_cells` = 1000

- `max_vm_data_depth` = ۵۱۲

- `max_acc_state_cells` = ۱ \<\< ۱۶

- `max_acc_state_bits` = (۱ \<\< ۱۶) \* ۱۰۲۳

:::info
می‌توانید جزئیات بیشتر درباره پارامترهای استاندارد را در [اینجا](https://github.com/ton-blockchain/ton/blob/fc9542f5e223140fcca833c189f77b1a5ae2e184/crypto/block/mc-config.h#L379) در کد منبع مشاهده کنید.
:::

## پارامتر ۴۴

این پارامتر فهرست آدرس‌های مسدود شده را تعریف می‌کند که نمی‌توانند تا `suspended_until` راه‌اندازی شوند. این تنها برای حساب‌های هنوز آغاز نشده اعمال می‌شود. این یک اقدام برای تثبیت اقتصاد توکن (محدود کردن ماینرهای اولیه) است. اگر تنظیم نشده باشد - هیچ محدودیتی وجود ندارد. هر آدرس به عنوان یک گره پایانی در این درخت نشان داده می‌شود و ساختار درخت مانند امکان بررسی مؤثر وجود یا عدم وجود یک آدرس در فهرست را می‌دهد.

:::info
The stabilization of the tokenomics is further described in the [official report](https://t.me/tonblockchain/178) of the **@tonblockchain** Telegram channel.
:::

## پارامتر ۴۵

The list of precompiled contracts is stored in the MasterChain config:

```
precompiled_smc#b0 gas_usage:uint64 = PrecompiledSmc;
precompiled_contracts_config#c0 list:(HashmapE 256 PrecompiledSmc) = PrecompiledContractsConfig;
_ PrecompiledContractsConfig = ConfigParam 45;
```

More details about precompiled contracts are on [this page](/v3/documentation/smart-contracts/contracts-specs/precompiled-contracts).

## پارامتر ۷۱ - ۷۳

This parameter pertains to bridges for wrapping Toncoins in other networks:

- ETH-TON **(71)**

- BSC-TON **(72)**

- Polygon-TON **(73)**

### Configuration parameters

- `bridge_address`: This is the bridge contract address that accepts TON to issue wrapped Toncoins in other networks.

- `oracle_multisig_address`: این آدرس کیف پول مدیریت پل است. کیف پول چند امضایی نوعی کیف پول دیجیتال است که برای تأیید یک تراکنش به امضاهای چندین طرف نیاز دارد. اغلب برای افزایش امنیت استفاده می‌شود. اوراکل‌ها به عنوان طرف‌ها عمل می‌کنند.

- `oracles`: List of oracles in the form of a tree `id->address`

- `external_chain_address`: این آدرس قرارداد پل در بلاک‌چین خارجی مربوطه است.

## پارامتر ۷۹، ۸۱ و ۸۲

This parameter relates to bridges for wrapping tokens from other networks into tokens on the TON network:

- ETH-TON **(79)**

- BSC-TON **(81)**

- Polygon-TON **(82)**

### Configuration parameters

- `bridge_address` و `oracles_address`: این‌ها آدرس‌های بلاکچین پل و قرارداد مدیریت پل (oracles multisig) به ترتیب هستند.

- `oracles`: List of oracles in the form of a tree `id->address`

- `state_flags`: نشانگر وضعیت. این پارامتر مسئول فعال‌سازی/غیرفعال‌سازی عملکردهای مجزای پل است.

- `prices`: این پارامتر شامل فهرست یا دیکشنری قیمت‌ها برای عملیات‌ها یا هزینه‌های مختلف مرتبط با پل، مانند `bridge_burn_fee`، `bridge_mint_fee`، `wallet_min_tons_for_storage`، `wallet_gas_consumption`، `minter_min_tons_for_storage`، `discover_gas_consumption` است.

- `external_chain_address`: آدرس قرارداد پل در یک بلاکچین دیگر.

## Negative parameters

:::info
The distinction between negative and positive parameters lies in the necessity for validators to verify them; negative parameters typically lack a specific assigned role.
:::

## Next steps

After thoroughly reviewing this article, it is highly recommended that you dedicate time for a more in-depth study of the following documents:

- The original descriptions are present, but they may be limited, in the documents:
    - [The Open Network Whitepaper](https://ton.org/whitepaper.pdf)
    - [Telegram Open Network Blockchain](/tblkch.pdf)

- Source code:
    - [mc-config.h](https://github.com/ton-blockchain/ton/blob/fc9542f5e223140fcca833c189f77b1a5ae2e184/crypto/block/mc-config.h)
    - [block.tlb](https://github.com/ton-blockchain/ton/blob/master/crypto/block/block.tlb)
    - [BlockMasterConfig Type](https://docs.evercloud.dev/reference/graphql-api/field_descriptions#blockmasterconfig-type)

## See also

On these pages, you can find active network configurations of the TON Blockchain:

- [Mainnet configuration](https://ton.org/global-config.json)
- [Testnet configuration](https://ton.org/testnet-global.config.json)
- [Russian version](https://github.com/delovoyhomie/description-config-for-TON-Blockchain/blob/main/Russian-version.md)

<Feedback />

