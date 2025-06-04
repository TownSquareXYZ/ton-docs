import Feedback from '@site/src/components/Feedback';

# TVM initialization

:::info
To maximize your comprehension of this page,
it is highly recommended to familiarize yourself with the [TL-B language](/v3/documentation/data-formats/tlb/cell-boc).

- [TVM retracer](https://retracer.ton.org/)
  :::

TVM is invoked during the computing phase of ordinary and other transactions.

## وضعیت اولیه

A new instance of TVM is initialized before executing a smart contract as follows:

- The original **cc**, current continuation, is initialized using the cell slice created from the `code` section of the smart contract. If the account is frozen or uninitialized, the code must be provided in the `init` field of the incoming message.

- The **cp**, current TVM codepage, is set to the default value of 0. If the smart contract needs to use another TVM codepage *x*, it must switch to it by using `SETCODEPAGE` *x* as the first instruction in its code.

- The **gas limits** values are initialized based on the results of the credit phase.

- The **library context** computation is [described below](#library-context).

- The **stack** initialization process depends on the event that triggered the transaction, and its contents are [described below](#stack).

- Control register **c0** is initialized with the extraordinary continuation `ec_quit` with parameter 0. When executed, this continuation terminates TVM with exit code 0.

- Control register **c1** is initialized with the extraordinary continuation `ec_quit` with parameter 1. When invoked, it terminates TVM with exit code 1. Both exit codes 0 and 1 are considered successful terminations of TVM.

- Control register **c2** is initialized with the extraordinary continuation `ec_quit_exc`. When invoked, it takes the top integer from the stack equal to the exception number and terminates TVM with that exit code. By default, all exceptions terminate the smart contract execution with the exception number as the exit code.

- Control register **c3** is initialized with the cell containing the smart contract code, similar to **cc** described above.

- Control register **c4** is initialized with the smart contract's persistent data from its `data` section. If the account is frozen or uninitialized, this data must be provided in the `init` field of the incoming message. Only the root of the data is loaded initially; TVM loads additional cells by their references when accessed, enabling a virtual memory mechanism.

- Control register **c5** is initialized with an empty cell. The "output action" primitives of TVM, such as `SENDMSG`, accumulate output actions (for example, outbound messages) in this register, which are performed upon successful termination of the smart contract. The TL-B scheme for its serialization is [described below](#control-register-c5).

- Control register **c7** (root of temporary data) is initialized as a tuple, and its structure is [described below](#control-register-c7).

## متن کتابخانه

A smart contract's library context/environment is a hashmap that maps 256-bit cell hashes to the corresponding cells. When an external cell reference is accessed during the smart contract's execution, the cell is looked up in the library environment, and the external cell reference is transparently replaced by the found cell.

The library environment for a smart contract invocation is computed as follows:

1. The global library environment for the current workchain is taken from the current state of the MasterChain.
2. It's augmented by the local library environment of the smart contract, stored in the `library` field of the smart contract's state. Only 256-bit keys equal to the hashes of the corresponding value cells are considered. The local environment takes precedence if a key is present in both the global and local library environments.
3. Finally, it's augmented by the `library` field of the `init` field of the incoming message. If the account is frozen or uninitialized, the `library` field of the message is used instead of the local library environment. The message library has lower precedence than local and global library environments.

The most common way to create shared libraries for TVM is to publish a reference to the library's root cell in the MasterChain.

## پشته

The TVM stack is initialized after the initial state of the TVM is set up. The contents of the stack depend on the event that triggered the transaction:

- پیام داخلی
- پیام خارجی
- Tick-tock
- آمادگی تقسیم
- نصب ادغام

The last item pushed to the stack is always the *function selector*, an *integer* that identifies the event that caused the transaction.

### Internal message

In the case of an internal message, the stack is initialized by pushing the arguments to the `main()` function of the smart contract as follows:

- The balance *b* of the smart contract is passed as an *integer* amount of nanotons after crediting the value of the inbound message.
- The balance *b*<sub>m</sub> of the inbound message *m* is passed as an *integer* amount of nanotons.
- The inbound message *m* is passed as a cell, which contains a serialized value of type *Message X*, where *X* is the message body type.
- The body *m*<sub>b</sub> of the inbound message, equal to the value of the `body` field of *m*, is passed as a cell slice.
- The function selector *s*, normally equal to 0.

After that, the smart contract's code, equal to its initial value of **c3**, is executed. It selects the correct function based on *s*, which is expected to process the remaining arguments and terminate.

### External message

یک پیام خارجی ورودی به صورت مشابه با [پیام داخلی که در بالا توضیح داده شد](#internal-message)، با تغییرات زیر پردازش می‌شود:

- The function selector *s* is set to -1.
- The balance *b*<sub>m</sub> of the inbound message is always 0.
- حد گاز فعلی اولیه *g*<sub>l</sub> همیشه ۰ است. با این حال، اعتبار گاز اولیه *g*<sub>c</sub> > ۰ است.

The smart contract must terminate with either *g*<sub>c</sub> = 0 or *g*<sub>r</sub> ≥ *g*<sub>c</sub>. If this condition isn't met, the transaction and the block containing it are considered invalid. Validators or collators proposing a block candidate must ensure that transactions processing inbound external messages are valid and exclude invalid ones.

### تیک و تاک

In the case of tick and tock transactions, the stack is initialized by pushing the arguments to the `main()` function of the smart contract as follows:

- The balance *b* of the current account is passed as an *integer* amount of nanotons.
- The 256-bit address of the current account inside the MasterChain as an unsigned *integer*.
- یک عدد صحیح برابر با ۰ برای تراکنش‌های تیک و -۱ برای تراکنش‌های تاک.
- انتخابگر تابع *s*، برابر با -۲.

### Split prepare

In the case of a split prepare transaction, the stack is initialized by pushing the arguments to the `main()` function of the smart contract as follows:

- The balance *b* of the current account is passed as an *integer* amount of nanotons.
- A *slice* containing *SplitMergeInfo*.
- آدرس ۲۵۶ بیتی حساب جاری.
- آدرس ۲۵۶ بیتی حساب همتا.
- An integer 0 ≤ *d* ≤ 63, equal to the position of the only bit in which the addresses of the current and sibling accounts differ.
- انتخابگر تابع *s*، برابر با -۳.

### Merge install

In the case of a merge install transaction, the stack is initialized by pushing the arguments to the `main()` function of the smart contract as follows:

- The balance *b* of the current account (already combined with the nanoton balance of the sibling account) is passed as an *integer* amount of nanotons.
- The balance *b'* of the sibling account, taken from the inbound message *m*, is passed as an *integer* amount of nanotons.
- A merge prepare transaction automatically generates the message *m* from the sibling account. Its `init` field contains the final state of the sibling account. The message is passed as a cell, which contains a serialized value of type *Message X*, where *X* is the message body type.
- A _StateInit _ represents the state of the sibling account.
- A *slice* containing *SplitMergeInfo*.
- آدرس ۲۵۶ بیتی حساب جاری.
- آدرس ۲۵۶ بیتی حساب همتا.
- An integer 0 ≤ *d* ≤ 63, equal to the position of the only bit in which the addresses of the current and sibling accounts differ.
- انتخابگر تابع *s*، برابر با -۴.

## رجیستر کنترل c5

The output actions of a smart contract are accumulated in the cell stored in the control register **c5**: the cell contains the last action in the list and a reference to the previous one, forming a linked list.

لیست همچنین می‌تواند به‌عنوان یک مقدار نوع *OutList n* سریال‌سازی شود، که در آن *n* طول لیست است:

```tlb
out_list_empty$_ = OutList 0;

out_list$_ {n:#}
  prev:^(OutList n)
  action:OutAction
  = OutList (n + 1);

out_list_node$_
  prev:^Cell
  action:OutAction = OutListNode;
```

The list of possible actions includes:

- `action_send_msg` — برای ارسال یک پیام خروجی
- `action_set_code` — برای تنظیم یک کد عملیاتی
- `action_reserve_currency` — برای ذخیره یک مجموعه ارز
- `action_change_library` — برای تغییر کتابخانه

همانطور که در طرح TL-B مربوطه شرح داده شده است:

```tlb
action_send_msg#0ec3c86d
  mode:(## 8) 
  out_msg:^(MessageRelaxed Any) = OutAction;
  
action_set_code#ad4de08e
  new_code:^Cell = OutAction;
  
action_reserve_currency#36e6b809
  mode:(## 8)
  currency:CurrencyCollection = OutAction;

libref_hash$0
  lib_hash:bits256 = LibRef;
libref_ref$1
  library:^Cell = LibRef;
action_change_library#26fa1dd4
  mode:(## 7) { mode <= 2 }
  libref:LibRef = OutAction;
```

## رجیستر کنترل c7

Control register **c7** contains the root of temporary data as a tuple, formed by a *SmartContractInfo* type, which includes basic blockchain context data such as time, global config, etc. The following TL-B scheme describes it:

```tlb
smc_info#076ef1ea
  actions:uint16 msgs_sent:uint16
  unixtime:uint32 block_lt:uint64 trans_lt:uint64 
  rand_seed:bits256 balance_remaining:CurrencyCollection
  myself:MsgAddressInt global_config:(Maybe Cell) = SmartContractInfo;
```

The first component of this tuple is an *integer* value, always equal to 0x076ef1ea, followed by nine named fields:

| فیلد                | نوع                                                                                 | توضیحات                                                                                                                                                                                                             |
| ------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `actions`           | uint16                                                                              | Initially set to 0, but incremented by one whenever a non-RAW output action primitive is executed                                                                                                                   |
| `msgs_sent`         | uint16                                                                              | تعداد پیام‌های ارسال شده                                                                                                                                                                                            |
| `unixtime`          | uint32                                                                              | زمان‌بند Unix به ثانیه                                                                                                                                                                                              |
| `block_lt`          | uint64                                                                              | Represents the logical time of the previous block of this account. [More about logical time](/v3/documentation/smart-contracts/message-management/messages-and-transactions#what-is-a-logical-time) |
| `trans_lt`          | uint64                                                                              | Represents the logical time of the previous transaction of this account                                                                                                                                             |
| `rand_seed`         | bits256                                                                             | به‌صورت قطعی از `rand_seed` بلوک، آدرس حساب، هش پیام ورودی که در حال پردازش است (در صورت وجود)، و زمان منطقی تراکنش `trans_lt` مقداردهی اولیه می‌شود                                             |
| `balance_remaining` | [CurrencyCollection](/v3/documentation/data-formats/tlb/msg-tlb#currencycollection) | تعادل باقی‌مانده قرارداد هوشمند                                                                                                                                                                                     |
| `myself`            | [MsgAddressInt](/v3/documentation/data-formats/tlb/msg-tlb#msgaddressint-tl-b)      | آدرس این قرارداد هوشمند                                                                                                                                                                                             |
| `global_config`     | (شاید Cell)                                                      | شامل اطلاعاتی درباره پیکربندی جهانی است                                                                                                                                                                             |

Note that in the upcoming upgrade to the TVM, the **c7** tuple was extended from 10 to 14 elements. Read more about it [here](/v3/documentation/tvm/changelog/tvm-upgrade-2023-07).

## همچنین ببینید

- Original description of TVM initialization from the whitepaper
  <Feedback />

