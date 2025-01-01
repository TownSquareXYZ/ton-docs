# ارائه‌دهندگان POW

:::warning منسوخ شده
این اطلاعات ممکن است کهنه و دیگر معتبر نباشد. می‌توانید از آن چشم‌پوشی کنید.
:::

هدف این متن توصیف چگونگی تعامل با قراردادهای هوشمند ارائه‌دهنده Proof-of-Work برای دریافت Toncoin است. ما فرض می‌کنیم با لایت کلاینت TON Blockchain آشنا هستید همانطور که در بخش `Getting Started` توضیح داده شده است و با رویه مورد نیاز برای کامپایل لایت کلاینت و نرم‌افزارهای دیگر نیز آشنا هستید. برای به دست آوردن مقدار بیشتری Toncoin که برای اجرای یک اعتبارسنج نیاز است، ما همچنین آشنایی با صفحات `Full Node` و `Validator` را فرض می‌کنیم. شما همچنین به یک سرور اختصاصی قدرتمند برای اجرا کردن یک Full Node نیاز خواهید داشت تا مقدار بیشتری Toncoin به دست آید. به‌دست‌آوردن مقادیر کوچک‌تر Toncoin نیازی به سرور اختصاصی ندارد و ممکن است در عرض چند دقیقه بر روی یک کامپیوتر خانگی انجام شود.

> توجه داشته باشید که در حال حاضر برای هر نوع استخراج به دلیل تعداد زیاد استخراج‌کنندگان، منابع زیادی لازم است.

## ۱. قراردادهای هوشمند ارائه‌دهنده Proof-of-Work

برای جلوگیری از جمع‌آوری تمام Toncoin توسط تعداد کمی از افراد مخرب، نوع خاصی از قراردادهای هوشمند "ارائه‌دهنده Proof-of-Work" در زنجیره اصلی شبکه مستقر شده است. آدرس‌های این قراردادهای هوشمند به شرح زیر است:

ارائه‌دهندگان کوچک (هر چند دقیقه ۱۰ تا ۱۰۰ Toncoin می‌دهند):

- kf-kkdY_B7p-77TLn2hUhM6QidWrrsl8FYWCIvBMpZKprBtN
- kf8SYc83pm5JkGt0p3TQRkuiM58O9Cr3waUtR9OoFq716lN-
- kf-FV4QTxLl-7Ct3E6MqOtMt-RGXMxi27g4I645lw6MTWraV
- kf_NSzfDJI1A3rOM0GQm7xsoUXHTgmdhN5-OrGD8uwL2JMvQ
- kf8gf1PQy4u2kURl-Gz4LbS29eaN4sVdrVQkPO-JL80VhOe6
- kf8kO6K6Qh6YM4ddjRYYlvVAK7IgyW8Zet-4ZvNrVsmQ4EOF
- kf-P_TOdwcCh0AXHhBpICDMxStxHenWdLCDLNH5QcNpwMHJ8
- kf91o4NNTryJ-Cw3sDGt9OTiafmETdVFUMvylQdFPoOxIsLm
- kf9iWhwk9GwAXjtwKG-vN7rmXT3hLIT23RBY6KhVaynRrIK7
- kf8JfFUEJhhpRW80_jqD7zzQteH6EBHOzxiOhygRhBdt4z2N

ارائه‌دهندگان بزرگ (حداقل یک بار در روز ۱۰٬۰۰۰ Toncoin می‌دهند):

- kf8guqdIbY6kpMykR8WFeVGbZcP2iuBagXfnQuq0rGrxgE04
- kf9CxReRyaGj0vpSH0gRZkOAitm_yDHvgiMGtmvG-ZTirrMC
- kf-WXA4CX4lqyVlN4qItlQSWPFIy00NvO2BAydgC4CTeIUme
- kf8yF4oXfIj7BZgkqXM6VsmDEgCqWVSKECO1pC0LXWl399Vx
- kf9nNY69S3_heBBSUtpHRhIzjjqY0ChugeqbWcQGtGj-gQxO
- kf_wUXx-l1Ehw0kfQRgFtWKO07B6WhSqcUQZNyh4Jmj8R4zL
- kf_6keW5RniwNQYeq3DNWGcohKOwI85p-V2MsPk4v23tyO3I
- kf_NSPpF4ZQ7mrPylwk-8XQQ1qFD5evLnx5_oZVNywzOjSfh
- kf-uNWj4JmTJefr7IfjBSYQhFbd3JqtQ6cxuNIsJqDQ8SiEA
- kf8mO4l6ZB_eaMn1OqjLRrrkiBcSt7kYTvJC_dzJLdpEDKxn

> توجه داشته باشید که در حال حاضر همه ارائه‌دهندگان بزرگ خالی هستند.

ده قرارداد هوشمند اول به کاربرانی که مایل به دریافت مقدار کمی از Toncoin هستند، امکان می‌دهد که بدون صرف قدرت محاسباتی زیاد (معمولاً چند دقیقه کار بر روی یک کامپیوتر خانگی کافی است) برخی را دریافت کنند. قراردادهای هوشمند باقی‌مانده برای به دست آوردن مقادیر بیشتری از Toncoin هستند که برای اجرای یک اعتبارسنج در شبکه نیاز است؛ معمولاً یک روز کار بر روی یک سرور اختصاصی قدرتمند برای اجرای یک اعتبارسنج کافی است تا مقدار لازم به دست آید.

> توجه داشته باشید که در حال حاضر به دلیل تعداد زیادی از استخراج‌کنندگان، منابع زیادی برای استخراج ارائه‌دهندگان کوچک لازم است.

شما باید یکی از این قراردادهای هوشمند "ارائه‌دهنده Proof-of-work" را به صورت تصادفی انتخاب کنید (با توجه به هدفتان از یکی از این دو فهرست) و با روشی مشابه استخراج، Toncoin را از این قرارداد هوشمند به دست آورید. در اصل، شما باید یک پیام خارجی شامل اثبات کار و آدرس کیف پول خود را به این قرارداد هوشمند "ارائه‌دهنده Proof-of-work" ارائه دهید و سپس مقدار مورد نیاز برای شما ارسال خواهد شد.

## ۲. فرآیند استخراج

برای ایجاد یک پیام خارجی که شامل "اثبات کار" باشد، شما باید یک ابزار استخراج ویژه‌ای که از سورس TON در مخزن GitHub کامپایل شده است را اجرا کنید. این ابزار در فایل `./crypto/pow-miner` نسبت به دایرکتوری ساخت قرار دارد و می‌توان آن را با وارد کردن `make pow-miner` در دایرکتوری ساخت کامپایل کرد.

با این حال، قبل از اجرای `pow-miner`، باید مقادیر واقعی پارامترهای `seed` و `complexity` قرارداد هوشمند انتخاب شده "proof-of-work giver" را بدانید. این کار با فراخوانی متد `get_pow_params` از این قرارداد هوشمند انجام می‌شود. برای مثال، اگر از قرارداد هوشمند ارائه‌دهنده استفاده می‌کنید، `kf-kkdY_B7p-77TLn2hUhM6QidWrrsl8FYWCIvBMpZKprBtN` می‌توانید به سادگی تایپ کنید:

```
> runmethod kf-kkdY_B7p-77TLn2hUhM6QidWrrsl8FYWCIvBMpZKprBtN get_pow_params
```

در کنسول لایت کلاینت و خروجی مانند زیر دریافت کنید:

```...
    arguments:  [ 101616 ] 
    result:  [ 229760179690128740373110445116482216837 53919893334301279589334030174039261347274288845081144962207220498432 100000000000 256 ] 
    remote result (not to be trusted):  [ 229760179690128740373110445116482216837 53919893334301279589334030174039261347274288845081144962207220498432 100000000000 256 ]
```

دو عدد بزرگ اول در خط "result:" به ترتیب `seed` و `complexity` این قرارداد هوشمند است. در این مثال، seed برابر است با `229760179690128740373110445116482216837` و پیچیدگی برابر است با `53919893334301279589334030174039261347274288845081144962207220498432`.

سپس، ابزار `pow-miner` را به صورت زیر فراخوانی کنید:

```
$ crypto/pow-miner -vv -w<num-threads> -t<timeout-in-sec> <your-wallet-address> <seed> <complexity> <iterations> <pow-giver-address> <boc-filename>
```

اینجا:

- `<num-threads>` تعداد هسته‌های CPU است که می‌خواهید برای ماینینگ استفاده کنید.
- `<timeout-in-sec>` حداکثر تعداد ثانیه‌هایی است که ماینر قبل از اعلام شکست اجرا خواهد کرد.
- `<your-wallet-address>` آدرس کیف پول شما است (ممکن است هنوز مقداردهی اولیه نشده باشد). این آدرس یا در مسترچین است یا در ورکچین (توجه داشته باشید که برای کنترل یک اعتبارسنج به کیف پول مسترچین نیاز دارید).
- `<seed>` و `<complexity>` آخرین مقادیر به‌دست‌آمده با اجرای متد `get-pow-params` هستند.
- `<pow-giver-address>` آدرس قرارداد هوشمند ارائه‌دهنده proof-of-work انتخابی است.
- `<boc-filename>` نام فایل خروجی است که در صورت موفقیت، پیام خارجی با اثبات کار در آن ذخیره خواهد شد.

برای مثال، اگر آدرس کیف پول شما `kQBWkNKqzCAwA9vjMwRmg7aY75Rf8lByPA9zKXoqGkHi8SM7` باشد، ممکن است این مراحل را اجرا کنید:

```
$ crypto/pow-miner -vv -w7 -t100 kQBWkNKqzCAwA9vjMwRmg7aY75Rf8lByPA9zKXoqGkHi8SM7 229760179690128740373110445116482216837 53919893334301279589334030174039261347274288845081144962207220498432 100000000000 kf-kkdY_B7p-77TLn2hUhM6QidWrrsl8FYWCIvBMpZKprBtN mined.boc
```

برنامه برای مدتی اجرا خواهد شد (حداکثر ۱۰۰ ثانیه در این مورد) و یا به صورت موفقیت‌آمیز خاتمه خواهد یافت (با کد خروج صفر) و اثبات کار مورد نیاز را در فایل `mined.boc` ذخیره خواهد کرد یا با کد خروج غیرصفر خاتمه خواهد یافت اگر اثبات کاری پیدا نشود.

در صورت شکست، چیزی شبیه به این خواهید دید:

```
   [ expected required hashes for success: 2147483648 ]
   [ hashes computed: 1192230912 ]
```

و برنامه با کد خروج غیرصفر خاتمه خواهد یافت. سپس باید دوباره `seed` و `complexity` را به‌دست آورید (زیرا ممکن است در این میان با پردازش درخواست‌های ماینرهای موفق‌تر تغییر کرده باشند) و `pow-miner` را با پارامترهای جدید دوباره اجرا کنید و فرآیند را مجدداً تکرار کنید تا موفق شوید.

در صورت موفقیت، چیزی شبیه به این را خواهید دید:

```
   [ expected required hashes for success: 2147483648 ]
   4D696E65005EFE49705690D2AACC203003DBE333046683B698EF945FF250723C0F73297A2A1A41E2F1A1F533B3BC4F5664D6C743C1C5C74BB3342F3A7314364B3D0DA698E6C80C1EA4ACDA33755876665780BAE9BE8A4D6385A1F533B3BC4F5664D6C743C1C5C74BB3342F3A7314364B3D0DA698E6C80C1EA4
   Saving 176 bytes of serialized external message into file `mined.boc`
   [ hashes computed: 1122036095 ]
```

سپس می‌توانید از لاینت کلاینت برای ارسال پیام خارجی از فایل `mined.boc` به قرارداد هوشمند proof-of-work giver استفاده کنید (و باید این کار را هر چه زودتر انجام دهید):

```
> sendfile mined.boc
... external message status is 1
```

می‌توانید چند ثانیه صبر کنید و وضعیت کیف پول خود را بررسی کنید:

:::info
لطفاً توجه داشته باشید که در اینجا و همچنین در آینده، کد، توضیحات و/یا مستندات ممکن است حاوی پارامترها، متدها و تعاریفی مانند «gram»، «nanogram» و غیره باشند. این میراث کد اصلی TON است که توسط تلگرام توسعه یافته است. ارز دیجیتال گرام هرگز صادر نشده است. ارز TON و تست‌نت TON تون‌کوین است.
:::

```
> last
> getaccount kQBWkNKqzCAwA9vjMwRmg7aY75Rf8lByPA9zKXoqGkHi8SM7
...
account state is (account
  addr:(addr_std
    anycast:nothing workchain_id:0 address:x5690D2AACC203003DBE333046683B698EF945FF250723C0F73297A2A1A41E2F1)
  storage_stat:(storage_info
    used:(storage_used
      cells:(var_uint len:1 value:1)
      bits:(var_uint len:1 value:111)
      public_cells:(var_uint len:0 value:0)) last_paid:1593722498
    due_payment:nothing)
  storage:(account_storage last_trans_lt:7720869000002
    balance:(currencies
      grams:(nanograms
        amount:(var_uint len:5 value:100000000000))
      other:(extra_currencies
        dict:hme_empty))
    state:account_uninit))
x{C005690D2AACC203003DBE333046683B698EF945FF250723C0F73297A2A1A41E2F12025BC2F7F2341000001C169E9DCD0945D21DBA0004_}
last transaction lt = 7720869000001 hash = 83C15CDED025970FEF7521206E82D2396B462AADB962C7E1F4283D88A0FAB7D4
account balance is 100000000000ng
```

اگر قبل از شما هیچ‌کس یک اثبات کار معتبر با این `seed` و `complexity` نفرستاده باشد، proof-of-work giver اثبات کار شما را قبول خواهد کرد و این امر در موجودی کیف پول شما منعکس خواهد شد (ممکن است بعد از ارسال پیام خارجی ۱۰ یا ۲۰ ثانیه بگذرد تا این اتفاق بیفتد؛ حتماً چندین بار تلاش کنید و قبل از بررسی موجودی کیف پول خود، هربار `last` را تایپ کنید تا وضعیت لاینت کلاینت را تازه‌سازی کنید). در صورت موفقیت، خواهید دید که موجودی افزایش یافته است (و حتی اگر کیف پولتان قبلاً وجود نداشت، به صورت یک وضعیت غیرفعال ایجاد شده است). در صورت شکست، باید `seed` و `complexity` جدید را دریافت کرده و فرآیند استخراج را از ابتدا تکرار کنید.

اگر خوش شانس بوده‌اید و موجودی کیف پول شما افزایش یافته است، اگر کیف پول شما قبلا مقداردهی اولیه نشده باشد ممکن است بخواهید کیف پول را مقداردهی اولیه کنید (اطلاعات بیشتر در مورد ایجاد کیف پول را می‌توانید در `مرحله‌به‌مرحله` پیدا کنید):

```
> sendfile new-wallet-query.boc
... external message status is 1
> last
> getaccount kQBWkNKqzCAwA9vjMwRmg7aY75Rf8lByPA9zKXoqGkHi8SM7
...
account state is (account
  addr:(addr_std
    anycast:nothing workchain_id:0 address:x5690D2AACC203003DBE333046683B698EF945FF250723C0F73297A2A1A41E2F1)
  storage_stat:(storage_info
    used:(storage_used
      cells:(var_uint len:1 value:3)
      bits:(var_uint len:2 value:1147)
      public_cells:(var_uint len:0 value:0)) last_paid:1593722691
    due_payment:nothing)
  storage:(account_storage last_trans_lt:7720945000002
    balance:(currencies
      grams:(nanograms
        amount:(var_uint len:5 value:99995640998))
      other:(extra_currencies
        dict:hme_empty))
    state:(account_active
      (
        split_depth:nothing
        special:nothing
        code:(just
          value:(raw@^Cell 
            x{}
             x{FF0020DD2082014C97BA218201339CBAB19C71B0ED44D0D31FD70BFFE304E0A4F260810200D71820D70B1FED44D0D31FD3FFD15112BAF2A122F901541044F910F2A2F80001D31F3120D74A96D307D402FB00DED1A4C8CB1FCBFFC9ED54}
            ))
        data:(just
          value:(raw@^Cell 
            x{}
             x{00000001CE6A50A6E9467C32671667F8C00C5086FC8D62E5645652BED7A80DF634487715}
            ))
        library:hme_empty))))
x{C005690D2AACC203003DBE333046683B698EF945FF250723C0F73297A2A1A41E2F1206811EC2F7F23A1800001C16B0BC790945D20D1929934_}
 x{FF0020DD2082014C97BA218201339CBAB19C71B0ED44D0D31FD70BFFE304E0A4F260810200D71820D70B1FED44D0D31FD3FFD15112BAF2A122F901541044F910F2A2F80001D31F3120D74A96D307D402FB00DED1A4C8CB1FCBFFC9ED54}
 x{00000001CE6A50A6E9467C32671667F8C00C5086FC8D62E5645652BED7A80DF634487715}
last transaction lt = 7720945000001 hash = 73353151859661AB0202EA5D92FF409747F201D10F1E52BD0CBB93E1201676BF
account balance is 99995640998ng
```

اکنون شما مالک خوشحال ۱۰۰ تون‌کوین هستید. تبریک می‌گویم!

## ۳. خودکارسازی فرآیند استخراج در صورت شکست

اگر برای مدت طولانی نتوانید تون‌کوین به‌دست آورید، ممکن است به‌دلیل این باشد که کاربران دیگر زیادی به صورت همزمان از همان قرارداد هوشمند ارائه‌دهنده proof-of-work استخراج می‌کنند. شاید باید یک قرارداد هوشمند ارائه‌دهنده proof-of-work دیگر از یکی از لیست‌های داده شده انتخاب کنید. به صورت جایگزین، می‌توانید یک اسکریپت ساده بنویسید که به‌طور خودکار `pow-miner` را با پارامترهای صحیح تا زمان موفقیت (تشخیص با بررسی کد خروج `pow-miner`) اجرا کند و با پارامتر `-c 'sendfile mined.boc'` به لایت کلاینت فراخوانی کند تا پیام خارجی بلافاصله پس از یافتن ارسال شود.
