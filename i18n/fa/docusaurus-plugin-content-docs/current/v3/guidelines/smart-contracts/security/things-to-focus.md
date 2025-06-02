import Feedback from '@site/src/components/Feedback';

# Things to focus on while working with TON Blockchain

در این مقاله، ما عناصر مهم برای توسعه‌دهندگانی که می‌خواهند برنامه‌های TON ایجاد کنند را بازبینی و بررسی خواهیم کرد.

## لیست بررسی

### ۱. تداخل نام‌ها

متغیرها و توابع Func می‌توانند تقریباً هر کاراکتر قانونی را شامل شوند. به‌عبارت دیگر، `var++`، `~bits`، `foo-bar+baz` شامل کاماها نام‌های معتبر برای متغیرها و توابع هستند.

هنگام نوشتن و بازرسی کد Func باید از Linter استفاده شود.

- [پلاگین‌های IDE](/v3/documentation/smart-contracts/getting-started/ide-plugins/)

### ۲. بررسی مقادیر پرتاب

هر بار که اجرای TVM به طور عادی متوقف می‌شود، با کدهای خروجی "۰" یا "۱" متوقف می‌شود. اگرچه این به طور خودکار انجام می‌شود، اجرای TVM می‌تواند به طور مستقیم به روشی غیرمنتظره متوقف شود اگر کدهای خروجی "۰" و "۱" به طور مستقیم توسط دستورات "throw(0)" یا "throw(1)" داده شود.

- [نحوهٔ handle کردن خطاها](/v3/documentation/smart-contracts/func/docs/builtins#throwing-exceptions)
- [کدهای خروج TVM](/v3/documentation/tvm/tvm-exit-codes)

### ۳. Func یک زبان به شدت نوع‌مند است با ساختارهای داده‌ای که دقیقاً آنچه باید ذخیره کنند را نگهداری می‌کند

دنبال‌کردن دقیق اینکه کد چه کاری انجام می‌دهد و چه چیزی ممکن است برگرداند بسیار مهم است. به یاد داشته باشید که کامپایلر فقط به کد اهمیت می‌دهد و فقط در حالت اولیه آن. پس از برخی عملیات، مقادیر ذخیره‌شده بعضی متغیرها ممکن است تغییر کنند.

خواندن مقادیر غیرمنتظره متغیرها و فراخوانی روش‌ها بر روی نوع‌های داده‌ای که نباید داشته باشند (یا مقادیر بازگشتی آن‌ها به‌درستی ذخیره نشوند) خطاها هستند و به‌عنوان "خطاهای اخطار" یا "اعلان‌ها" محسوب نمی‌شوند بلکه به کد منزجر می‌انجامند. به یاد داشته باشید که ممکن است نگهداری یک مقدار غیرمنتظره اشکالی نداشته باشد، اما خواندن آن ممکن است مشکلاتی ایجاد کند، مثلاً کد خطای ۵ (عدد صحیح خارج از محدوده موردانتظار) ممکن است برای یک متغیر صحیح تولید شود.

### ۴. پیام‌ها دارای حالت‌ها هستند

بررسی حالت پیام، به خصوص تعامل آن با پیام‌های ارسال شده قبلی و هزینه‌ها، ضروری است. یک خطای ممکن عدم حسابداری برای هزینه‌های storage است، که در این صورت قرارداد ممکن است TON خود را تمام کند و به شکست‌های ناخواسته در هنگام ارسال پیام‌های خروجی منجر شود. شما می‌توانید حالت‌های پیام را [اینجا](/v3/documentation/smart-contracts/message-management/sending-messages#message-modes) ببینید.

### 5. Replay protection {#replay-protection}

There are two custom solutions for wallets (smart contracts that store user funds): `seqno-based` (using a counter to prevent processing the same message twice) and `high-load` (storing processed identifiers and their expiration times).

- [کیف‌پول‌های مبتنی بر Seqno](/v3/guidelines/dapps/asset-processing/payments-processing/#seqno-based-wallets)
- [کیف‌پول‌های پر بار](/v3/guidelines/dapps/asset-processing/payments-processing/#high-load-wallets)

For `seqno`, refer to [this section](/v3/documentation/smart-contracts/message-management/sending-messages#mode3) for details on possible replay scenarios.

### 6. TON fully implements the actor model

این به معنای این است که کد قرارداد قابلیت تغییر دارد. می‌توان آن را به صورت دائمی با استفاده از دستور TVM [`SETCODE`](/v3/documentation/smart-contracts/func/docs/stdlib#set_code) تغییر داد، یا در زمان اجرا، ثبت نام کد TVM را تا پایان execution به یک مقدار جدید cell تنظیم کرد.

### 7. TON Blockchain has several transaction phases: computational phase, actions phase, and a bounce phase among them

فاز محاسبه کد قراردادهای هوشمند را اجرا می‌کند و تنها پس از آن اقدامات انجام می‌شود (ارسال پیام‌ها، تغییر کد، تغییر کتابخانه‌ها و غیره). بنابراین، برخلاف بلاک‌چین‌های مبتنی بر اتریوم، اگر انتظار داشتید پیام ارسالی موفق نشود، کد خروج فاز محاسبه را مشاهده نخواهید کرد، زیرا این عمل در فاز محاسبه انجام نشده بود، بلکه بعدها در فاز اجرا انجام شده بود.

- [تراکنش‌ها و فازها](/v3/documentation/tvm/tvm-overview#transactions-and-phases)

### 8. TON contracts are autonomous

قراردادها در بلاکچین می‌توانند در شاردهای جداگانه قرار گیرند که توسط مجموعه‌ای دیگر از اعتبارسنج‌ها پردازش می‌شوند، به این معنی که توسعه‌دهنده نمی‌تواند بر اساس تقاضا داده‌ها را از قراردادهای دیگر دریافت کند. بنابراین، هر گونه ارتباط به صورت غیرهمزمان است و با ارسال پیام‌ها انجام می‌شود.

- [ارسال پیام‌ها از smart-contract](/v3/documentation/smart-contracts/message-management/sending-messages)
- [ارسال پیام‌ها از DApp](/v3/guidelines/ton-connect/guidelines/sending-messages)

### 9. Unlike other blockchains, TON does not contain revert messages, only exit codes

قبل از شروع برنامه‌نویسی قرارداد هوشمند TON خود، بهتر است به دقت نقشه خروج کدهای جریان کد را بررسی کرده (و مستندات آن را تهیه کنید).

### 10. Func functions that have method_id identifiers have method IDs

آنها می‌توانند یا به طور واضح "method_id(5)" تنظیم شوند، یا به طور ضمنی توسط کامپایلر func تنظیم شوند. در این صورت، می‌توان آنها را میان اعلامیه‌های روش‌ها در فایل فیتف مونتاژ یافت. دو مورد از آنها پیش‌تعریف‌شده هستند: یکی برای دریافت پیام‌ها درون بلاکچین "(0)", که معمولاً به نام "recv_internal" شناخته می‌شود، و یکی برای دریافت پیام‌ها از خارج "(-1)", "recv_external".

### 11. TON crypto address may not have any coins or code

آدرس‌های قراردادهای هوشمند در بلاکچین TON قطعی هستند و می‌توان آنها را پیش محاسبه کرد. حساب‌های Ton، که با آدرس‌ها مرتبط هستند، حتی ممکن است هیچ کدی نداشته باشند که به معنی این است که آنها غیرمقداردهی اولیه (اگر به کار گرفته نشوند) و یا منجمد شده‌اند در حالی که هیچ ذخیره‌سازی یا کوین‌های TON را ندارند اگر پیامی با نشانگر‌های خاص ارسال شده باشد.

### 12. TON addresses may have three representations

آدرس‌های TON ممکن است سه نمایش داشته باشند.
نمایش کامل می‌تواند به صورت "خام" (`workchain:address`) یا "کاربر پسند" باشد. آخرین مورد همان چیزی است که کاربران بیشتر در بازارند. آن شامل یک byte برچسب، که نشان می‌دهد آیا آدرس `bounceable` است یا `non-bounceable`، و یک byte شناسه زنجیره کار است. این اطلاعات باید یادداشت شود.

- [Raw and user-friendly addresses](/v3/documentation/smart-contracts/addresses#raw-and-user-friendly-addresses)

### 13. Keep track of the flaws in code execution

بر خلاف Solidity که شما مسئول تعیین نمایش روش‌ها هستید، در صورت Func، نمایش‌ها به صورت پیچیده‌تری محدود می‌شوند یا از طریق نمایش خطاها یا با جملات اگر محدوده می‌شود.

### 14. Keep an eye on gas before sending bounced messages

در صورتی که قرارداد هوشمند پیام‌های بازگشتی را با مقداری که توسط کاربر فراهم شده است ارسال کند، اطمینان حاصل کنید که هزینه‌های مربوط به گاز از مقدار بازگشتی کسر شوند تا خالی نشوند.

### 15. Monitor the callbacks and their failures

بلاکچین TON غیرهمزمان است. این بدان معناست که پیام‌ها نباید به طور متوالی برسند. به‌عنوان مثال، وقتی که اطلاعیه شکست عملیاتی می‌رسد، باید به درستی پردازش شود.

### 16. Check if the bounced flag was sent receiving internal messages

ممکن است پیام‌های بازگشتی (اطلاعیه‌های خطا) که باید پردازش شوند، دریافت کنید.

- [Handling of standard response messages](/v3/documentation/smart-contracts/message-management/internal-messages#handling-of-standard-response-messages)

## منابع

- [Original article](https://0xguard.com/things_to_focus_on_while_working_with_ton_blockchain) - *0xguard*

<Feedback />

