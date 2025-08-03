import Feedback from '@site/src/components/Feedback';

# نتیجه‌گیری از چالش هک TON

چالش هک TON در تاریخ ۲۳ اکتبر برگزار شد.
چندین قرارداد هوشمند با نقض امنیت مصنوعی در شبکه اصلی TON مستقر شده بود. هر قرارداد یک موجودی از 3000 یا 5000 تون داشت که به شرکت‌کننده اجازه می‌داد آن را هک کرده و فوراً پاداش بگیرد.

قوانین مسابقه و کد منبع در GitHub [اینجا](https://github.com/ton-blockchain/hack-challenge-1) میزبانی شده‌اند.

## قراردادها

### 1. صندوق مشترک

:::note قانون امنیتی
همیشه توابع را برای اصلاح‌کننده [`impure`](/v3/documentation/smart-contracts/func/docs/functions#impure-specifier) بررسی کنید.
:::

اولین وظیفه بسیار ساده بود. مهاجم می‌توانست متوجه شود که تابع `authorize` `impure` نبود. نبود این اصلاح‌کننده به کامپایلر اجازه می‌دهد تا تماس‌های مربوط به این تابع را در صورتی که هیچ چیزی را بر نمی‌گرداند یا مقدار بازگشتی استفاده نمی‌شود، نادیده بگیرد.

```func
() authorize (sender) inline {
  throw_unless(187, equal_slice_bits(sender, addr1) | equal_slice_bits(sender, addr2));
}
```

### 2. بانک

:::note قانون امنیتی
همیشه به دنبال روش‌های [تغییر/غیرتغییر](/v3/documentation/smart-contracts/func/docs/statements#methods-calls) باشید.
:::

`udict_delete_get?` با `.` به‌جای `~` فراخوانده شد، بنابراین دیکشنری واقعی دست نخورده باقی ماند.

```func
(_, slice old_balance_slice, int found?) = accounts.udict_delete_get?(256, sender);
```

### 3. DAO

:::note قانون امنیتی
اگر به واقع نیاز دارید، از اعداد صحیح با علامت استفاده کنید.
:::

قدرت رأی‌گیری به عنوان یک عدد صحیح در پیام ذخیره می‌شد. بنابراین، مهاجم می‌توانست در هنگام انتقال قدرت یک مقدار منفی ارسال کند و قدرت رأی‌گیری بی‌نهایت دریافت کند.

```func
(cell,()) transfer_voting_power (cell votes, slice from, slice to, int amount) impure {
  int from_votes = get_voting_power(votes, from);
  int to_votes = get_voting_power(votes, to);

  from_votes -= amount;
  to_votes += amount;

  ;; No need to check that result from_votes is positive: set_voting_power will throw for negative votes
  ;; throw_unless(998, from_votes > 0);

  votes~set_voting_power(from, from_votes);
  votes~set_voting_power(to, to_votes);
  return (votes,());
}
```

### 4. لاتاری

:::note قانون امنیتی
همیشه قبل از انجام [`rand()`](/v3/documentation/smart-contracts/func/docs/stdlib#rand) بذر را تصادفی‌سازی کنید
:::

بذر از زمان منطقی تراکنش گرفته شده بود و یک هکر می‌تواند با نیروی محاسباتی زمان منطقی را در بلوک فعلی شکست دهد و برنده شود (زیرا lt در مرزهای یک بلوک متوالی است).

```func
int seed = cur_lt();
int seed_size = min(in_msg_body.slice_bits(), 128);

if(in_msg_body.slice_bits() > 0) {
    seed += in_msg_body~load_uint(seed_size);
}
set_seed(seed);
var balance = get_balance().pair_first();
if(balance > 5000 * 1000000000) {
    ;; forbid too large jackpot
    raw_reserve( balance - 5000 * 1000000000, 0);
}
if(rand(10000) == 7777) { ...send reward... }
```

### 5. کیف پول

:::note قانون امنیتی
به یاد داشته باشید که همه چیز در بلاک‌چین ذخیره می‌شود.
:::

کیف پول با رمز عبور محافظت می‌شد، hash آن در داده‌های قرارداد ذخیره شده بود. با این حال، بلاک‌چین همه چیز را به یاد دارد - رمز عبور در تاریخچه تراکنش‌ها بود.

### 6. خزانه

:::note قانون امنیتی
همیشه پیام‌های [bounced](/v3/documentation/smart-contracts/message-management/non-bounceable-messages) را بررسی کنید.
خطاهای ناشی از توابع [استاندارد](/v3/documentation/smart-contracts/func/docs/stdlib/) را فراموش نکنید.
شرایط خود را به حداکثر ممکن سخت‌گیرانه کنید.
:::

خزانه دارای کد زیر در مدیریت پیام پایگاه داده است:

```func
int mode = null();
if (op == op_not_winner) {
    mode = 64; ;; Refund remaining check-TONs
               ;; addr_hash corresponds to check requester
} else {
     mode = 128; ;; Award the prize
                 ;; addr_hash corresponds to the withdrawal address from the winning entry
}
```

اگر کاربر "چک" ارسال کند، خزانه یک مدیریت کننده پرش ندارد و یا پیام پراکسی به پایگاه داده نمی‌فرستد. در پایگاه داده می‌توانیم `msg_addr_none` را به عنوان یک آدرس جایزه تنظیم کنیم زیرا `load_msg_address` این را اجازه می‌دهد. ما یک چک از خزانه درخواست می‌کنیم، پایگاه داده سعی می‌کند `msg_addr_none` را با استفاده از [`parse_std_addr`](/v3/documentation/smart-contracts/func/docs/stdlib#parse_std_addr) تجزیه کند و شکست می‌خورد. پیام از پایگاه داده به خزانه پرش می‌کند و عمل `op_not_winner` نیست.

### 7. بانک بهتر

:::note قانون امنیتی
هرگز حساب را برای سرگرمی از بین نبرید.
به جای ارسال پول به خودتان، [`raw_reserve`](/v3/documentation/smart-contracts/func/docs/stdlib#raw_reserve) بسازید.
به شرایط رقابتی ممکن فکر کنید.
در مصرف گاز نقشه‌ی هش دقت کنید.
:::

در قرارداد شرایط رقابت وجود داشت: شما می‌توانستید پول واریز کنید و سپس در پیام‌های همزمان دو بار آن را برداشت کنید. هیچ تضمینی وجود ندارد که پیامی با پول ذخیره شده پردازش شود، بنابراین بانک می‌تواند پس از برداشت دوم متوقف شود. پس از آن، قرارداد می‌تواند دوباره استقرار داده شود و هر کسی می‌تواند پول مطالبه نشده را برداشت کند.

### 8. دهاشر

:::note قانون امنیتی
از اجرای کدهای شخص دیگر در قرارداد خود اجتناب کنید.
:::

```func
slice try_execute(int image, (int -> slice) dehasher) asm "<{ TRY:<{ EXECUTE DEPTH 2 THROWIFNOT }>CATCH<{ 2DROP NULL }> }>CONT"   "2 1 CALLXARGS";

slice safe_execute(int image, (int -> slice) dehasher) inline {
  cell c4 = get_data();

  slice preimage = try_execute(image, dehasher);

  ;; restore c4 if dehasher spoiled it
  set_data(c4);
  ;; clean actions if dehasher spoiled them
  set_c5(begin_cell().end_cell());

  return preimage;
}
```

هیچ راهی برای اجرای امن کدهای شخص ثالث در قرارداد وجود ندارد، زیرا استثناء [`out of gas`](/v3/documentation/tvm/tvm-exit-codes#standard-exit-codes) نمی‌تواند توسط `CATCH` مدیریت شود. مهاجم به سادگی می‌تواند هر وضعیت قرارداد را [`COMMIT`](/v3/documentation/tvm/instructions#F80F) کند و `out of gas` را افزایش دهد.

## نتیجه‌گیری

امیدواریم این مقاله برخی از قوانین غیر واضح برای توسعه‌دهندگان FunC را روشن کرده باشد.

## منابع

- [dvlkv on GitHub](https://github.com/dvlkv) - *Dan Volkov*
- [Original article](https://dev.to/dvlkv/drawing-conclusions-from-ton-hack-challenge-1aep) - *Dan Volkov*

<Feedback />

