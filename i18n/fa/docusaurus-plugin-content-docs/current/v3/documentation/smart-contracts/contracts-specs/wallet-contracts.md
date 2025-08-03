import Feedback from '@site/src/components/Feedback';

import ConceptImage from '@site/src/components/conceptImage';
import ThemedImage from '@theme/ThemedImage';

# Wallet contracts

You may have heard about different versions of wallets on TON Blockchain. But what do these versions actually mean, and how do they differ?

در این مقاله، ما نسخه‌ها و تغییرات مختلف کیف پول‌های TON را بررسی خواهیم کرد.

:::info
Before we start, there are some terms and concepts that you should be familiar with to fully understand the article:

- [مدیریت پیام](/v3/documentation/smart-contracts/message-management/messages-and-transactions)، زیرا این عملکرد اصلی کیف‌پول‌ها است.
- [FunC language](/v3/documentation/smart-contracts/func/overview), because we will heavily rely on implementations made using it.
  :::

## مفهوم مشترک

برای رهایی از تنش، ابتدا باید بفهمیم که کیف‌پول‌ها یک واحد خاص در اکوسیستم TON نیستند. آنها هنوز هم فقط قراردادهای هوشمندی هستند که از کد و داده‌ها تشکیل شده‌اند و از این منظر با هر عامل دیگری (یعنی قرارداد هوشمند) در TON برابر هستند.

Like your own custom smart contract, or any other one, wallets can receive external and internal messages, send internal messages and logs, and provide `get methods`.
So the question is: what functionality do they provide and how it differs between versions?

می‌توانید هر نسخه کیف‌پول را به عنوان یک پیاده‌سازی قرارداد هوشمند با ارائه یک رابط بیرونی استاندارد در نظر بگیرید که به مشتریان بیرونی مختلف اجازه می‌دهد تا به همان شکل با کیف‌پول‌ها تعامل داشته باشند. می‌توانید این پیاده‌سازی‌ها را در زبان‌های FunC و Fift در مخزن اصلی TON پیدا کنید:

- [ton/crypto/smartcont/](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/)

## کیف پول‌های پایه

### کیف پول V1

این ساده‌ترین است. فقط به شما اجازه می‌دهد که چهار تراکنش به‌طور هم‌زمان ارسال کنید و هیچ‌چیز، به‌جز امضای شما و seqno، را بررسی نمی‌کند.

کد منبع کیف پول:

- [ton/crypto/smartcont/wallet-code.fif](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-wallet.fif)

این نسخه حتی در برنامه‌های معمولی استفاده نمی‌شود زیرا برخی مسائل اساسی دارد:

- هیچ راه آسانی برای بازیابی seqno و کلید عمومی از قرارداد وجود ندارد.
- کنترل `valid_until` وجود ندارد، بنابراین نمی‌توانید مطمئن باشید که تراکنش خیلی دیر تایید نمی‌شود.

The first issue was fixed in `V1R2` and `V1R3`. The `R` stands for **revision**. Usually, revisions are just small updates that only add get methods; you can find all of those in the changes history of `new-wallet.fif`. Hereinafter, we will consider only the latest revisions.

با این حال، از آنجایی که هر نسخه بعدی عملکرد نسخه قبلی را به ارث می‌برد، ما باید همچنان به آن وفادار بمانیم زیرا این به ما در نسخه‌های آینده کمک خواهد کرد.

#### طرح چیدمان حافظه پایدار

- <b>seqno</b>: شماره ترتیبی ۳۲ بیتی.
- <b>public-key</b>: کلید عمومی ۲۵۶ بیتی.

#### طرح چیدمان بدنه پیام خارجی

1. داده:
  - <b>امضا</b>: امضای ed25519 با طول ۵۱۲ بیت.
  - <b>msg-seqno</b>: شماره ترتیبی ۳۲ بیتی.
  - <b>(0-4)mode</b>: حداکثر تا چهار عدد صحیح ۸ بیتی برای تعریف حالت ارسال برای هر پیام.
2. تا ۴ ارجاع به سلولی که حاوی پیام‌ها باشد.

همان‌طور که می‌بینید، عملکرد اصلی کیف‌پول این است که یک روش امن برای ارتباط با بلاکچین ton از دنیای خارج فراهم کند. مکانیزم `seqno` از حملات بازپخش جلوگیری می‌کند و `Ed25519 signature` دسترسی مجاز به عملکرد کیف‌پول را فراهم می‌کند. ما به جزئیات هر کدام از این مکانیزم‌ها نخواهیم پرداخت، چرا که آن‌ها به‌صورت جامع در صفحه مستندات [پیام خارجی](/v3/documentation/smart-contracts/message-management/external-messages) توصیف شده‌اند و میان قراردادهای هوشمند که پیام‌های خارجی دریافت می‌کنند، بسیار رایج هستند. داده‌های بار شامل تا ۴ ارجاع به سلول‌ها و تعداد حالت‌های متناظر است که به طور مستقیم به متد [send_raw_message(cell msg, int mode)](/v3/documentation/smart-contracts/func/docs/stdlib#send_raw_message) انتقال داده خواهد شد.

:::caution
به خاطر داشته باشید که کیف‌پول هیچ گونه تأییدی برای پیام‌های داخلی که از طریق آن ارسال می‌کنید ارائه نمی‌دهد. مسئولیت سریال‌سازی داده‌ها بر اساس [طرح پیام داخلی](http://localhost:3000/v3/documentation/smart-contracts/message-management/sending-messages#message-layout) به عهده برنامه‌نویس (یعنی، مشتری خارجی) است.
:::

#### کدهای خروج

| کد خروج | توضیحات                                                  |
| ------- | -------------------------------------------------------- |
| 0x21    | بررسی `seqno` شکست خورده، محافظت در برابر پاسخ تضمین شده |
| 0x22    | بررسی `Ed25519 signature` شکست خورده                     |
| 0x0     | کد خروج اجرای موفقیت آمیز استاندارد.     |

:::info
توجه کنید که [TVM](/v3/documentation/tvm/tvm-overview) [کدهای خروج استاندارد](/v3/documentation/tvm/tvm-exit-codes) دارد (یکی از آنها `0x0` است)، بنابراین اگر مثلاً از [Gas](https://docs.ton.org/develop/smart-contracts/fees) تمام شوید، می‌توانید یکی از آنها را دریافت کنید، به عنوان مثال، کد `0xD` را خواهید گرفت.
:::

#### روش‌های Get

1. int seqno() شماره ترتیبی ذخیره شده فعلی را برمی گرداند.
2. int get_public_key کلید عمومی فعلی ذخیره شده را برمی گرداند.

### کیف پول V2

کد منبع کیف پول:

- [ton/crypto/smartcont/wallet-code.fc](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet-code.fc)

این نسخه پارامتر `valid_until` را معرفی می‌کند، که برای تعیین محدودیت زمانی برای تراکنش استفاده می‌شود اگر نمی‌خواهید که تراکنش خیلی دیر تایید شود. این نسخه همچنین متد گت برای کلید عمومی ندارد، که در `V2R2` اضافه شد.

همه تفاوت‌ها نسبت به نسخه قبلی نتیجه افزودن قابلیت `valid_until` است. یک کد خروج جدید اضافه شده است: `0x23`، که شکست بررسی valid_until را نشان می‌دهد. علاوه بر این، یک فیلد زمان یونیکس جدید به طرح بدنه پیام خارجی اضافه شده است که محدودیت زمانی تراکنش را تعیین می‌کند. همه متدهای get همانطور باقی می‌مانند.

#### طرح چیدمان بدنه پیام خارجی

1. داده:
  - <b>امضا</b>: امضای ed25519 با طول ۵۱۲ بیت.
  - <b>msg-seqno</b>: شماره ترتیبی ۳۲ بیتی.
  - <b>valid-until</b>: عدد صحیح ۳۲ بیتی زمان یونیکس.
  - <b>(0-4)mode</b>: حداکثر چهار عدد صحیح ۸-بیتی برای تعیین حالت ارسال هر پیام.
2. حداکثر ۴ ارجاع به cells حاوی پیام‌ها.

### کیف پول V3

این نسخه پارامتر `subwallet_id` را معرفی می‌کند که به شما اجازه می‌دهد چندین کیف پول با استفاده از همان کلید عمومی ایجاد کنید (بنابراین شما می‌توانید فقط یک عبارت بذر و چندین کیف پول داشته باشید). مانند قبل، `V3R2` فقط روش get برای کلید عمومی را اضافه می‌کند.

کد منبع کیف پول:

- [کیف پول v3](-code.fc](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/wallet3-code.fc)

در اصل، `subwallet_id` فقط یک عدد است که در زمان اجرای قرارداد به وضعیت آن اضافه می‌شود. از آنجایی که آدرس قرارداد در TON یک هش از وضعیت و کد آن است، آدرس کیف پول با `subwallet_id` متفاوت تغییر خواهد کرد. این نسخه در حال حاضر به طور گسترده استفاده می‌شود. بیشتر موارد استفاده را پوشش می‌دهد و همچنان پاک، ساده و به طور عمده مشابه نسخه‌های قبلی باقی می‌ماند. تمام متدهای get یکسان می‌مانند.

#### چیدمان حافظه پایدار

- <b>seqno</b>: عدد ترتیبی ۳۲-بیتی.
- <b>subwallet</b>: شناسه subwallet ۳۲-بیتی.
- <b>کلید عمومی</b>: کلید عمومی ۲۵۶-بیتی.

#### طرح پیام خارجی

1. Data:
  - <b>امضا</b>: امضای ۵۱۲-بیتی ed25519.
  - <b>شناسه-subballet</b>: شناسه subwallet ۳۲-بیتی.
  - <b>msg-seqno</b>: عدد ترتیبی ۳۲-بیتی.
  - <b>valid-until</b>: عدد صحیح زمان UNIX ۳۲-بیتی.
  - <b>(0-4)mode</b>: حداکثر چهار عدد صحیح ۸-بیتی برای تعیین حالت ارسال هر پیام.
2. حداکثر ۴ ارجاع به cells حاوی پیام‌ها.

#### کدهای خروج

| کد خروج | توضیحات                                                                 |
| ------- | ----------------------------------------------------------------------- |
| 0x23    | بررسی `valid_until` شکست خورد؛ تلاش برای تأیید تراکنش خیلی دیر انجام شد |
| 0x23    | بررسی `Ed25519 signature` شکست خورد                                     |
| 0x21    | بررسی `seqno` شکست خورد؛ محافظت پاسخ فعال شد                            |
| 0x22    | `subwallet-id` با ذخیره‌شده تطابق ندارند                                |
| 0x0     | کد خروج استاندارد برای اجرای موفق.                      |

### کیف پول V4

این نسخه تمام قابلیت‌های نسخه‌های قبلی را حفظ می‌کند ولی همچنین چیزی بسیار قدرتمند به نام: `پلاگین‌ها` معرفی می‌کند.

کد منبع کیف پول:

- [ton-blockchain/wallet-contract](https://github.com/ton-blockchain/wallet-contract)

این ویژگی به توسعه‌دهندگان اجازه می‌دهد تا منطق پیچیده‌ای را پیاده‌سازی کنند که با کیف پول کاربر هماهنگ کار کند. به عنوان مثال، یک DApp ممکن است از کاربر بخواهد که هر روز مقدار کوچکی سکه پرداخت کند تا از برخی ویژگی‌ها استفاده کند. در این صورت، کاربر باید با امضای تراکنش، پلاگین را بر روی کیف پول خود نصب کند. سپس پلاگین به طور روزانه وقتی که توسط پیام خارجی درخواست شود سکه‌ها را به آدرس مقصد ارسال می‌کند.

#### پلاگین‌ها

پلاگین‌ها اساساً سایر قرارداد های هوشمند در TON هستند که توسعه‌دهندگان می‌توانند به خواست خود پیاده‌سازی کنند. نسبت به کیف پول، آنها به سادگی آدرس های قرارداد هوشمند ذخیره‌شده در [دیکشنری](/v3/documentation/smart-contracts/func/docs/dictionaries) در حافظه پایدار کیف پول هستند. این پلاگین‌ها مجاز به درخواست بودجه و حذف خود از "لیست مجاز" با ارسال پیام‌های داخلی به کیف پول هستند.

#### چیدمان حافظه ماندگار

- <b>seqno</b>: عدد ترتیبی ۳۲-بیتی.
- <b>شناسه-subballet</b>: شناسه subwallet ۳۲-بیتی.
- <b>کلید عمومی</b>: کلید عمومی ۲۵۶-بیتی.
- <b>پلاگین‌ها</b>: دیکشنری شامل پلاگین‌ها (ممکن است خالی باشد)

#### دریافت پیام‌های داخلی

تمام نسخه‌های قبلی کیف پول‌ها پیاده‌سازی ساده‌ای برای دریافت پیام‌های داخلی داشتند. آنها به سادگی وجوه ورودی از هر فرستنده‌ای را پذیرفته و متن پیام داخلی را نادیده می‌گرفتند، اگر حاضر بود، یا به عبارت دیگر، آنها یک متد recv_internal خالی داشتند. اما همان‌طور که قبلاً ذکر شد، نسخه چهارم کیف پول دو عملیات اضافی موجود را معرفی می‌کند. بیایید به چیدمان متن پیام داخلی نگاهی بیندازیم:

- <b>op-code?</b>: کد عملیات ۳۲-بیتی. این یک فیلد اختیاری است؛ هر پیام حاوی کمتر از ۳۲ بیت در متن پیام، کد عملیاتی نادرست یا آدرس فرستنده که به عنوان پلاگین ثبت نشده باشد، به عنوان انتقال ساده در نظر گرفته می‌شود، مشابه نسخه‌های قبلی کیف پول.
- <b>query-id</b>: عدد صحیح ۶۴-بیتی. این فیلد هیچ تأثیری بر رفتار قرارداد هوشمند ندارد؛ برای پیگیری زنجیره‌های پیام بین قراردادها استفاده می‌شود.

1. op-code = 0x706c7567, کد عملیات درخواست بودجه.
  - <b>toncoins</b>: مقدار VARUINT16 از toncoins درخواست‌شده.
  - <b>extra_currencies</b>: دیکشنری حاوی مقدار پول‌های اضافی درخواست‌شده (ممکن است خالی باشد).
2. op-code = 0x64737472, درخواست حذف فرستنده پلاگین از "لیست مجاز".

#### چیدمان بدنه پیام خارجی

- <b>امضا</b>: امضای ۵۱۲-بیتی ed25519.
- <b>شناسه-subballet</b>: شناسه subwallet ۳۲-بیتی.
- <b>تا-معتبر</b>: عدد صحیح زمان Unix ۳۲-بیتی.
- <b>msg-seqno</b>: عدد ترتیبی ۳۲-بیتی.
- <b>op-code</b>: کد عملیات ۳۲-بیتی.

1. op-code = 0x0, ارسال ساده.
  - <b>(0-4)mode</b>: حداکثر چهار عدد صحیح ۸-بیتی برای تعیین حالت ارسال هر پیام.
  - <b>(0-4)پیام‌ها</b>: حداکثر چهار مرجع به cells حاوی پیام‌ها.
2. op-code = 0x1, استقرار و نصب پلاگین.
  - <b>workchain</b>: عدد صحیح ۸-بیتی.
  - <b>موجودی</b>: مقدار VARUINT16 تونکوین از موجودی اولیه.
  - <b>state-init</b>: مرجع Cell شامل وضعیت اولیه افزونه.
  - <b>بدنه</b>: مرجع Cell شامل بدنه.
3. op-code = 0x2/0x3, نصب افزونه / حذف افزونه.
  - <b>wc_n_address</b>: ۸-بیت طولانی workchain_id + ۲۵۶-بیت طولانی آدرس افزونه.
  - <b>موجودی</b>: مقدار VARUINT16 تونکوین از موجودی اولیه.
  - <b>query-id</b>: عدد صحیح ۶۴ بیتی.

همانطور که می‌بینید، نسخه چهارم هنوز از طریق کد عملیاتی `0x0` عملکرد استانداردی ارائه می‌دهد، مشابه نسخه‌های قبلی. عمل‌های `0x2` و `0x3` اجازه دستکاری در فرهنگ‌نامه افزونه‌ها را می‌دهند. توجه داشته باشید که در حالت `0x2`، شما باید خودتان افزونه را با آن آدرس پیاده‌سازی کنید. برعکس، کد عملیاتی `0x1` همچنین فرایند پیاده‌سازی را با استفاده از فیلد state_init مدیریت می‌کند.

:::tip
If `state_init` doesn't make much sense from its name, take a look at the following references:

- [addresses-in-ton-blockchain](/v3/documentation/smart-contracts/addresses#workchain-id-and-account-id)
- [send-a-deploy-message](/v3/documentation/smart-contracts/func/cookbook#how-to-send-a-deploy-message-with-stateinit-only-with-stateinit-and-body)
- [internal-message-layout](/v3/documentation/smart-contracts/message-management/sending-messages#message-layout)
  :::

#### کدهای خروج

| کد خروج | توضیحات                                                                                                                  |
| ------- | ------------------------------------------------------------------------------------------------------------------------ |
| 0x24    | بررسی `valid_until` ناموفق بود، تلاش برای تایید تراکنش بسیار دیر انجام شد                                                |
| 0x23    | بررسی `Ed25519 signature` ناموفق بود                                                                                     |
| 0x21    | بررسی `seqno` ناموفق بود، محافظت از پاسخ فعال شد                                                                         |
| 0x22    | `subwallet-id` با دستگاه ذخیره شده مطابقت ندارد                                                                          |
| 0x27    | دستکاری در فرهنگ‌نامه افزونه‌ها ناموفق بود (کدهای عملیاتی 0x1-0x3 recv_external) |
| 0x50    | بودجه کافی برای درخواست بودجه موجود نیست                                                                                 |
| 0x0     | کد خروج اجرای موفق استاندارد.                                                                            |

#### دریافت روش‌ها

1. int seqno() - شماره فعلی ذخیره‌شده seqno را بازمی‌گرداند.
2. int get_public_key() - کلید عمومی ذخیره‌شده فعلی را بازمی‌گرداند.
3. int get_subwallet_id() - شناسه فعلی زیرکیف را بازمی‌گرداند.
4. int is_plugin_installed(int wc, int addr_hash) بررسی می‌کند که آیا افزونه با شناسه workchain و هش آدرس تعریف‌شده نصب شده است یا خیر.
5. tuple get_plugin_list() فهرست افزونه‌ها را بازمی‌گرداند.

### کیف پول V5

It is the most modern wallet version at the moment, developed by the Tonkeeper team, aimed at replacing V4 and allowing arbitrary extensions. <br></br>
<ThemedImage
alt=""
sources={{
light: '/img/docs/wallet-contracts/wallet-contract-V5.png?raw=true',
dark: '/img/docs/wallet-contracts/wallet-contract-V5_dark.png?raw=true',
}}
/> <br></br><br></br><br></br>
The V5 wallet standard offers many benefits that improve the experience for both users and merchants. V5 supports gas-free transactions, account delegation and recovery, subscription payments using tokens and Toncoin, and low-cost multi-transfers. In addition to retaining the previous functionality (V4), the new contract allows you to send up to 255 messages at a time.

کد منبع کیف پول:

- [ton-blockchain/wallet-contract-v5](https://github.com/ton-blockchain/wallet-contract-v5)

طرح TL-B:

- [ton-blockchain/wallet-contract-v5/types.tlb](https://github.com/ton-blockchain/wallet-contract-v5/blob/main/types.tlb)

:::caution
برخلاف مشخصات نسخه‌های قبلی کیف پول، به دلیل پیچیدگی نسبی پیاده‌سازی رابط این نسخه از کیف پول، ما بر طرح [TL-B](/v3/documentation/data-formats/tlb/tl-b-language) تکیه خواهیم کرد. ما توضیحاتی برای هر یک از آن‌ها ارائه خواهیم داد. با این حال، درک پایه‌ای همچنان نیاز است، در ترکیب با کد منبع کیف پول، باید کافی باشد.
:::

#### طرح حافظه پایدار

```
contract_state$_
    is_signature_allowed:(## 1)
    seqno:#
    wallet_id:(## 32)
    public_key:(## 256)
    extensions_dict:(HashmapE 256 int1) = ContractState;
```

همانطور که می‌بینید، `ContractState` نسبت به نسخه‌های قبلی تغییرات عمده‌ای نداشته است. تفاوت اصلی نشانگر <b>۱</b>-بیتی جدید `is_signature_allowed` است که از طریق امضا و کلید عمومی ذخیره‌شده دسترسی را محدود یا مجاز می‌کند. اهمیت این تغییر را در موضوعات بعدی توضیح خواهیم داد.

#### فرایند تأیید هویت

```
signed_request$_             // 32 (opcode from outer)
  wallet_id:    #            // 32
  valid_until:  #            // 32
  msg_seqno:    #            // 32
  inner:        InnerRequest //
  signature:    bits512      // 512
= SignedRequest;             // Total: 688 .. 976 + ^Cell

internal_signed#73696e74 signed:SignedRequest = InternalMsgBody;

internal_extension#6578746e
    query_id:(## 64)
    inner:InnerRequest = InternalMsgBody;

external_signed#7369676e signed:SignedRequest = ExternalMsgBody;
```

قبل از اینکه به بار واقعی پیام‌های خود برسیم — `InnerRequest` — بیایید ابتدا ببینیم که نسخه ۵ در فرایند احراز هویت چگونه با نسخه‌های قبلی تفاوت دارد. ترکیب‌کننده `InternalMsgBody` دو روش دسترسی به عملیات کیف پول از طریق پیام‌های داخلی را توضیح می‌دهد. روش اول همان است که از نسخه ۴ با آن آشنا هستیم: احراز هویت به عنوان یک افزونه ثبت‌شده قبلی که آدرس آن در `extensions_dict` ذخیره می‌شود. روش دوم احراز هویت از طریق کلید عمومی ذخیره‌شده و امضا است، شبیه به درخواست‌های خارجی.

در ابتدا، این ممکن است به نظر ویژگی غیرضروری برسد، اما در واقع امکان پردازش درخواست‌ها را از طریق خدمات خارجی (قراردادهای هوشمند) که بخشی از زیرساخت گسترش کیف پول شما نیستند فراهم می‌کند— ویژگی کلیدی V5. تراکنش‌های بدون گاز به این عملکرد تکیه دارند.

توجه داشته باشید که دریافت ساده وجوه همچنان یک گزینه است. عملاً، هر پیام داخلی دریافت‌شده که از فرآیند احراز هویت عبور نمی‌کند به عنوان انتقال محسوب می‌شود.

#### اقدامات

اولین چیزی که باید به آن توجه کنیم `InnerRequest` است که قبلاً در فرآیند احراز هویت دیده‌ایم. برخلاف نسخه قبلی، هر دو پیام خارجی و داخلی به همان ویژگی‌ها دسترسی دارند، به جز تغییر وضعیت امضا (یعنی نشانگر `is_signature_allowed`).

```
out_list_empty$_ = OutList 0;
out_list$_ {n:#}
    prev:^(OutList n)
    action:OutAction = OutList (n + 1);

action_send_msg#0ec3c86d mode:(## 8) out_msg:^(MessageRelaxed Any) = OutAction;

// Extended actions in V5:
action_list_basic$_ {n:#} actions:^(OutList n) = ActionList n 0;
action_list_extended$_ {m:#} {n:#} action:ExtendedAction prev:^(ActionList n m) = ActionList n (m+1);

action_add_ext#02 addr:MsgAddressInt = ExtendedAction;
action_delete_ext#03 addr:MsgAddressInt = ExtendedAction;
action_set_signature_auth_allowed#04 allowed:(## 1) = ExtendedAction;

actions$_ out_actions:(Maybe OutList) has_other_actions:(## 1) {m:#} {n:#} other_actions:(ActionList n m) = InnerRequest;
```

ما می‌توانیم `InnerRequest` را به عنوان دو لیست از اقدامات در نظر بگیریم: اول، `OutList`، یک زنجیره اختیاری از ارجاعات سلولی است که هر کدام شامل یک درخواست ارسال پیام با راهنمایی حالت پیام است. دوم، `ActionList`، با یک نشانگر یک‌بیته `has_other_actions` هدایت می‌شود که حضور اقدامات گسترش یافته را نشان می‌دهد، از اولین سلول شروع شده و به عنوان زنجیره‌ای از ارجاعات سلولی ادامه می‌یابد. ما با اولین دو عمل گسترشی آشنا هستیم: `action_add_ext` و `action_delete_ext`، دنبال شده توسط آدرس داخلی که می‌خواهیم از فرهنگ‌نامه گسترش‌دهی حذف یا اضافه کنیم. سوم، `action_set_signature_auth_allowed`، احراز هویت را از طریق کلید عمومی محدود یا مجاز می‌کند، و تنها راه تعامل با کیف پول از طریق گسترش‌ها باقی می‌ماند. این عملکرد در مواردی که کلید خصوصی گم شده یا به خطر افتاده باشد می‌تواند بسیار مهم باشد.

:::info
توجه داشته باشید که حداکثر تعداد اقدامات ۲۵۵ است؛ این نتیجه پیاده‌سازی از طریق رجیستر TVM [c5](/v3/documentation/tvm/tvm-overview#result-of-tvm-execution) است. از لحاظ فنی، شما می‌توانید با `OutAction` و `ExtendedAction` خالی درخواست کنید، اما در این صورت مشابه به دریافت ساده وجوه خواهد بود.
:::

#### کدهای خروجی

| کد خروجی | توضیحات                                                                                                                        |
| -------- | ------------------------------------------------------------------------------------------------------------------------------ |
| 0x84     | تلاش برای تأیید هویت از طریق امضا در حالی‌که غیرفعال است                                                                       |
| 0x85     | `seqno` بررسی ناموفق بود، محافظت از پاسخ رخ داد                                                                                |
| 0x86     | `wallet-id` با ذخیره شده‌ی خود مطابق نیست                                                                                      |
| 0x87     | بررسی `Ed25519 signature` ناموفق بود                                                                                           |
| 0x88     | بررسی `valid-until` ناموفق بود                                                                                                 |
| 0x89     | الزام کنید که `send_mode` دارای بیت +2 (نادیده گرفتن خطاها) تنظیم شده برای پیام خارجی باشد. |
| 0x8A     | پیشوند `external-signed` با دریافتی مطابقت ندارد                                                                               |
| 0x8B     | عملیات افزودن افزونه موفقیت‌آمیز نبود                                                                                          |
| 0x8C     | عملیات حذف افزونه موفقیت‌آمیز نبود                                                                                             |
| 0x8D     | پیشوند پیام توسعه یافته پشتیبانی نمی‌شود                                                                                       |
| 0x8E     | تلاش برای غیرفعال کردن احراز هویت از طریق امضا در حالی‌که فرهنگ لغت افزونه خالی است                                            |
| 0x8F     | تلاش برای تنظیم امضا به حالتی که قبلاً تنظیم شده است                                                                           |
| 0x90     | تلاش برای حذف آخرین افزونه در زمانی‌که امضا غیرفعال است                                                                        |
| 0x91     | افزونه دارای زنجیره کاری نادرست است                                                                                            |
| 0x92     | تلاش برای تغییر حالت امضا از طریق پیام خارجی                                                                                   |
| 0x93     | `c5` نامعتبر، تأیید `action_send_msg` ناموفق بود                                                                               |
| 0x0      | کد خروجی استاندارد برای اجرای موفقیت‌آمیز.                                                                     |

:::danger
توجه داشته باشید که کدهای خروجی کیف پول `0x8E`، `0x90` و `0x92` برای جلوگیری از از دست دادن دسترسی به عملکرد کیف پول طراحی شده‌اند. با این حال، باید به یاد داشته باشید که کیف پول بررسی نمی‌کند که آیا آدرس‌های افزونه ذخیره شده واقعاً در تون وجود دارند یا نه. شما هم‌چنین می‌توانید کیف پولی با داده‌های اولیه که شامل یک لغت‌نامه افزونه خالی و حالت امضای محدود است، استقرار دهید. در این صورت، تا زمانی که اولین افزونه خود را اضافه نکرده‌اید، می‌توانید از طریق کلید عمومی به کیف پول دسترسی داشته باشید. بنابراین با این سناریوها با احتیاط برخورد کنید.
:::

#### دریافت روش‌ها

1. int is_signature_allowed() مقدار نشانگر ذخیره‌شده `is_signature_allowed` را برمی‌گرداند.
2. int seqno() مقدار seqno فعلی ذخیره‌شده را برمی‌گرداند.
3. int get_subwallet_id() شناسه زیرکیف پول فعلی را برمی‌گرداند.
4. int get_public_key() کلید عمومی ذخیره‌شده فعلی را برمی‌گرداند.
5. cell get_extensions() لغت‌نامه افزونه‌ها را برمی‌گرداند.

#### Preparing for gasless transactions

As was said, before v5, the wallet smart contract allowed the processing of internal messages signed by the owner. This also allows you to make gasless transactions, e.g., payment of network fees when transferring USDt in USDt itself. The common scheme looks like this:

![image](/img/gasless.jpg)

:::tip
در نهایت، خدماتی (مانند [باتری Tonkeeper](https://blog.ton.org/tonkeeper-releases-huge-update#tonkeeper-battery)) وجود خواهد داشت که این قابلیت را ارائه می‌دهند: آنها هزینه‌های تراکنش را به نمایندگی از کاربر در تون‌ها پرداخت می‌کنند، اما هزینه‌ای را به صورت توکن‌ها دریافت می‌کنند.
:::

#### جریان

1. هنگام ارسال USDt، کاربر یک پیام را امضا می‌کند که حاوی دو انتقال خروجی USDt است:
  1. انتقال USDt به آدرس گیرنده.
  2. انتقال مقدار کمی USDt به نفع سرویس.
2. این پیام امضا شده به صورت خارج از زنجیره از طریق HTTPS به بک‌اند سرویس ارسال می‌شود. بک‌اند سرویس آن را به بلاکچین TON ارسال می‌کند و هزینه‌های شبکه را با Toncoins پرداخت می‌کند.

نسخه بتا API بک‌اند بدون گاز در [tonapi.io/api-v2](https://tonapi.io/api-v2) در دسترس است. اگر در حال توسعه هر گونه اپلیکیشن کیف پول هستید و نظری درباره این روش‌ها دارید، لطفاً آن را در گفتگوی [@tonapitech](https://t.me/tonapitech) به اشتراک بگذارید.

کد منبع کیف پول:

- [ton-blockchain/wallet-contract-v5](https://github.com/ton-blockchain/wallet-contract-v5)

## کیف پول‌های ویژه

گاهی اوقات کارکرد کیف پول‌های پایه کافی نیست. به همین دلیل چندین نوع کیف پول خاص وجود دارد: `high-load`، `lockup` و `restricted`.

بگذارید نگاهی به آن‌ها بیندازیم.

### Highload wallets

هنگام کار با تعداد زیادی پیام در مدت زمان کوتاه، نیاز به یک کیف پول خاص به نام کیف پول با بار سنگین وجود دارد. برای اطلاعات بیشتر [مقاله](/v3/documentation/smart-contracts/contracts-specs/highload-wallet) را بخوانید.

### کیف پول قفل شده

اگر شما، به دلایلی، نیاز دارید که سکه‌ها را برای مدتی در کیف پول قفل کنید و قبل از گذشت آن زمان نتوانید آن‌ها را برداشت کنید، به کیف پول قفل شده نگاه کنید.

این امکان به شما می‌دهد که زمان عدم امکان برداشت از کیف پول را تنظیم کنید. همچنین می‌توانید با تنظیم دوره‌های باز کردن، امکان خرج کردن برخی سکه‌ها را در این دوره‌ها فراهم کنید.

برای مثال: شما می‌توانید یک کیف پول ایجاد کنید که ۱ میلیون سکه را با زمان تخصیص کل ۱۰ سال نگه دارد. دوره کلایف را به یک سال تنظیم کنید، به طوری که سرمایه‌ها در سال اول پس از ایجاد کیف پول قفل باشند. سپس، می‌توانید دوره باز کردن را به یک ماه تنظیم کنید، بنابراین `1'000'000 TON / 120 ماه = ~8333 TON` هر ماه باز خواهند شد.

کد منبع کیف پول:

- [ton-blockchain/lockup-wallet-contract](https://github.com/ton-blockchain/lockup-wallet-contract)

### کیف پول محدود

وظیفه این کیف پول این است که مانند یک کیف پول معمولی عمل کند، اما انتقال‌ها را به یک آدرس مقصد از پیش تعریف‌شده محدود کند. شما می‌توانید مقصد را هنگام ایجاد این کیف پول تنظیم کنید و سپس تنها می‌توانید از آن به آن آدرس وجوه را منتقل کنید. اما توجه داشته باشید که همچنان می‌توانید وجوه را به قراردادهای اعتبارسنجی منتقل کنید بنابراین می‌توانید با این کیف پول یک اعتبارسنج ایجاد کنید.

کد منبع کیف پول:

- [EmelyanenkoK/nomination-contract/restricted-wallet](https://github.com/EmelyanenkoK/nomination-contract/tree/master/restricted-wallet)

## نتیجه‌گیری

همان‌طور که می‌بینید، نسخه‌های مختلف زیادی از کیف‌پول‌ها در TON وجود دارد. اما در بیشتر موارد، شما فقط به `V3R2` یا `V4R2` نیاز دارید. شما همچنین می‌توانید از یکی از کیف‌پول‌های ویژه استفاده کنید اگر می‌خواهید عملکردهای اضافی مانند باز کردن دوره‌ای وجوه داشته باشید.

## See also

- [کار با قراردادهای هوشمند کیف پول](/v3/guidelines/smart-contracts/howto/wallet)
- [منابع کیف‌پول‌های پایه](https://github.com/ton-blockchain/ton/tree/master/crypto/smartcont)
- [توضیحات فنی بیشتری از نسخه‌ها](https://github.com/toncenter/tonweb/blob/master/src/contract/wallet/WalletSources.md)
- [منابع و توصیف دقیق کیف‌پول V4](https://github.com/ton-blockchain/wallet-contract)
- [منابع و توصیف دقیق کیف‌پول قفل‌شده](https://github.com/ton-blockchain/lockup-wallet-contract)
- [منابع کیف‌پول‌های محدود](https://github.com/EmelyanenkoK/nomination-contract/tree/master/restricted-wallet)
- [تراکنش‌های بدون گاز در تون](https://medium.com/@buidlingmachine/gasless-transactions-on-ton-75469259eff2)

<Feedback />

