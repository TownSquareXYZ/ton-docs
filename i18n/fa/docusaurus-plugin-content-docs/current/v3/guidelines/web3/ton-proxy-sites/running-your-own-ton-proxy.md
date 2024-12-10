# اجرای TON Proxy اختصاصی

هدف از این سند ارائه یک معرفی ملایم به TON Sites است که وب سایت‌هایی هستند که از طریق شبکه TON قابل دسترسی هستند. سایت‌های TON می‌توانند به عنوان یک نقطه ورودی راحت برای دیگر خدمات TON استفاده شوند. به‌ویژه، صفحات HTML دانلود شده از سایت‌های TON ممکن است حاوی لینک‌های به `ton://URL` باشند که نمایانگر پرداخت‌هایی هستند که کاربر می‌تواند با کلیک بر روی لینک انجام دهد، به شرطی که یک کیف پول TON بر روی دستگاه کاربر نصب شده باشد.

از دید فنی، سایت‌های TON بسیار شبیه به وب‌سایت‌های استاندارد هستند، اما از طریق [شبکه‌ی TON](/v3/concepts/dive-into-ton/ton-blockchain/ton-networking) (که یک شبکه‌ی پوششی درون اینترنت است) به جای اینترنت دسترسی پیدا می‌کنند. به طور خاص، آن‌ها یک آدرس [ADNL](/v3/documentation/network/protocols/adnl/overview) دارند (به جای یک آدرس IPv4 یا IPv6 مرسوم‌) و کوئری‌های HTTP را از طریق یک پروتکل [RLDP](/v3/documentation/network/protocols/rldp) (که یک پروتکل RPC سطح بالاتر برپایه‌ی ADNL، پروتکل اصلی شبکه‌ی TON است) به جای TCP/IP معمولی قبول می‌کنند. تمام رمزنگاری‌ها توسط ADNL انجام می‌شوند، بنابراین  اگر پراکسی ورودی به صورت محلی بر روی دستگاه کاربر میزبانی می‌شود، نیازی به استفاده از HTTPS (یعنی TLS) نیست.

برای دسترسی به سایت‌های موجود و ایجاد سایت‌های جدید TON، به دروازه‌های خاصی بین اینترنت "عادی" و شبکه TON نیاز است. به طور کلی، سایت‌های TON با کمک یک پراکسی HTTP->RLDP که به صورت محلی بر روی کامپیوتر کلاینت اجرا می‌شود، قابل دسترسی هستند و با استفاده از یک پراکسی RLDP->HTTP معکوس که بر روی یک سرور راه دور در حال اجرا است، ایجاد می‌شوند.

[اطلاعات بیشتر درباره TON Sites، TON WWW، و TON Proxy](https://blog.ton.org/ton-sites)

## اجرای یک پراکسی ورودی

برای دسترسی به سایت‌های موجود TON، باید یک RLDP-HTTP پراکسی بر روی کامپیوتر خود اجرا کنید.

1. **rldp-http-proxy** را از [TON Auto Builds](https://github.com/ton-blockchain/ton/releases/latest) دانلود کنید.

   یا می‌توانید با دنبال کردن این [دستورالعمل‌ها](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#rldp-http-proxy) خودتان **rldp-http-proxy** را کامپایل کنید.

2. [دانلود](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#download-global-config) تنظیمات جهانی TON.

3. **rldp-http-proxy** را اجرا کنید

   ```bash
   rldp-http-proxy/rldp-http-proxy -p 8080 -c 3333 -C global.config.json
   ```

در مثال بالا، `8080` پورت TCP است که در localhost برای پرسش‌های HTTP ورودی گوش داده خواهد شد و `3333` پورت UDP است که برای همه فعالیت‌های خروجی و ورودی RLDP و ADNL (یعنی برای اتصال به سایت‌های TON از طریق شبکه TON) استفاده خواهد شد. `global.config.json` نام فایل پیکربندی جهانی TON است.

اگر همه چیز را به درستی انجام داده باشید، پراکسی ورودی متوقف نخواهد شد و به کار کردن در ترمینال ادامه خواهد داد. اکنون می‌توانید از آن برای دسترسی به سایت‌های TON استفاده کنید. زمانی که دیگر نیازی به آن ندارید، می‌توانید با زدن `Ctrl+C` آن را متوقف کنید یا به سادگی پنجره ترمینال را ببندید.

پراکسی ورودی شما توسط HTTP روی `localhost` پورت `8080` در دسترس خواهد بود.

## اجرای پراکسی ورودی بر روی یک کامپیوتر راه دور

1. **rldp-http-proxy** را از [TON Auto Builds](https://github.com/ton-blockchain/ton/releases/latest) دانلود کنید.

   یا می‌توانید با دنبال کردن این [دستورالعمل‌ها](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#rldp-http-proxy) خودتان **rldp-http-proxy** را کامپایل کنید.

2. [دانلود](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#download-global-config) تنظیمات جهانی TON.

3. **generate-random-id** را از [TON Auto Builds](https://github.com/ton-blockchain/ton/releases/latest) دانلود کنید.

   یا می‌توانید با دنبال کردن این [دستورالعمل‌ها](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#generate-random-id) خودتان **generate-random-id** را کامپایل کنید.

4. یک آدرس ANDL پایدار برای پراکسی ورودی خود تولید کنید

   ```bash
   mkdir keyring

   utils/generate-random-id -m adnlid
   ```

   چیزی شبیه زیر را مشاهده خواهید کرد

   ```
   45061C1D4EC44A937D0318589E13C73D151D1CEF5D3C0E53AFBCF56A6C2FE2BD vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3
   ```

   این آدرس ADNL تازه‌تولیدشده شماست، در قالب هگزادسیمال و کاربر پسند. کلید خصوصی مربوطه در فایل `45061...2DB` در دایرکتوری فعلی ذخیره شده است. کلید را به دایرکتوری کلیدها منتقل کنید

   ```bash
   mv 45061C1* keyring/
   ```

5. **rldp-http-proxy** را اجرا کنید

   ```
   rldp-http-proxy/rldp-http-proxy -p 8080 -a <your_public_ip>:3333 -C global.config.json -A <your_adnl_address>
   ```

   در اینجا `<your_public_ip>` آدرس IPv4 عمومی شما و `<your_adnl_address>` آدرس ADNL تولید شده در مرحله قبلی است.

   مثال:

   ```
   rldp-http-proxy/rldp-http-proxy -p 8080 -a 777.777.777.777:3333 -C global.config.json -A vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3
   ```

   در مثال بالا، `8080` پورت TCP است که در localhost برای پرسش‌های HTTP ورودی گوش داده خواهد شد و `3333` پورت UDP است که برای همه فعالیت‌های خروجی و ورودی RLDP و ADNL استفاده خواهد شد (یعنی برای اتصال به سایت‌های TON از طریق شبکه TON). `global.config.json` نام فایل پیکربندی جهانی TON است.

اگر همه چیز را به درستی انجام داده‌اید، پراکسی متوقف نخواهد شد و به اجرا در ترمینال ادامه خواهد داد. اکنون می‌توانید از آن برای دسترسی به سایت‌های TON استفاده کنید. زمانی که دیگر نیازی به آن ندارید، می‌توانید با زدن `Ctrl+C` آن را متوقف کنید یا به سادگی پنجره ترمینال را ببندید. می‌توانید این را به عنوان یک خدمات یونیکس برای اجرای دائمی اجرا کنید.

پراکسی ورودی شما توسط HTTP روی `<your_public_ip>` پورت `8080` در دسترس خواهد بود.

## دسترسی به سایت‌های TON

حالا فرض کنید که یک نمونه از پراکسی RLDP-HTTP روی کامپیوتر شما در حال اجرا است و روی `localhost:8080` برای اتصالات TCP ورودی گوش می‌دهد، همان‌طور که [بالا](#running-an-entry-proxy-on-a-remote-computer) توضیح داده شد.

یک آزمون ساده که نشان می‌دهد همه چیز به درستی کار می‌کند، می‌تواند با استفاده از برنامه‌هایی مانند `curl` یا `wget` انجام شود. برای مثال،

```
curl -x 127.0.0.1:8080 http://just-for-test.ton
```

تلاش برای دانلود صفحه اصلی (TON) سایت `just-for-test.ton` با استفاده از پراکسی در `127.0.0.1:8080`. اگر پراکسی فعال و اجرا باشد، چیزی شبیه به این خواهید دید

```html

<html>
<head>
<title>TON Site</title>
</head>
<body>
<h1>TON Proxy Works!</h1>
</body>
</html>

```

شما همچنین می‌توانید از طریق آدرس‌های ADNL آنها به سایت‌های TON دسترسی پیدا کنید با استفاده از یک دامنه جعلی `<adnl-addr>.adnl`

```bash
curl -x 127.0.0.1:8080 http://utoljjye6y4ixazesjofidlkrhyiakiwrmes3m5hthlc6ie2h72gllt.adnl/
```

در حال حاضر همان صفحه وب TON را دریافت می‌کند.

به‌عنوان یک روش دیگر، می‌توانید `localhost:8080` را به عنوان یک پراکسی HTTP در مرورگر خود تنظیم کنید. به عنوان مثال، اگر از فایرفاکس استفاده می‌کنید، به [تنظیمات] -> عمومی -> تنظیمات شبکه -> تنظیمات -> پیکربندی دستی پراکسی دسترسی بروید و "127.0.0.1" را در قسمت "پراکسی HTTP" وارد کنید و "8080" را در قسمت "پورت" وارد کنید.

هنگامی که `localhost:8080` را به عنوان پراکسی HTTP در مرورگر خود تنظیم کرده‌اید، می‌توانید به سادگی URI لازم، مانند `http://just-for-test.ton` یا `http://utoljjye6y4ixazesjofidlkrhyiakiwrmes3m5hthlc6ie2h72gllt.adnl/` را در نوار ناوبری مرورگر خود وارد کنید و با سایت TON به همان روشی که با سایت‌های وب معمولی تعامل دارید، تعامل کنید.

## اجرای سایت TON

:::tip آموزش پیدا شد!
هی! نمی‌خواهید از آموزش دوستانه برای مبتدیان [چگونه سایت TON را اجرا کنیم؟](/v3/guidelines/web3/ton-proxy-sites/how-to-run-ton-site) شروع کنید
:::

بیشتر افراد فقط به دسترسی به سایت‌های موجود TON نیاز دارند و نیازی به ایجاد سایت‌های جدید ندارند. اما اگر می‌خواهید یک سایت ایجاد کنید، باید RLDP-HTTP پراکسی را بر روی سرور خود اجرا کنید، به‌همراه نرم‌افزار سرور وب معمولی مانند Apache یا Nginx.

ما فرض می‌کنیم که شما از قبل می‌دانید چگونه یک وب‌سایت عادی را راه‌اندازی کنید و یکی را بر روی سرور خود پیکربندی کرده‌اید، اتصالات HTTP ورودی را در پورت TCP `<your-server-ip>:80` قبول می‌کنید و نام دامنه‌ی موردنیاز شبکه‌ی TON (مثلاً `example.ton`) را به عنوان نام دامنه‌ی اصلی یا یک آلیاس (رکورد A) برای وب‌سایت خود در پیکربندی وب‌سرور خود تعریف کرده‌اید.

1. **rldp-http-proxy** را از [TON Auto Builds](https://github.com/ton-blockchain/ton/releases/latest) دانلود کنید.

   یا می‌توانید با این [دستورالعمل](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#rldp-http-proxy) خودتان **rldp-http-proxy** را کامپایل کنید.

2. [دانلود](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#download-global-config) تنظیمات جهانی TON.

3. **generate-random-id** را از [TON Auto Builds](https://github.com/ton-blockchain/ton/releases/latest) دانلود کنید.

   یا می‌توانید خودتان **generate-random-id** را با دنبال کردن این [دستورالعمل‌ها](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions#generate-random-id) کامپایل کنید.

4. یک آدرس دائمی ANDL برای سرور خود ایجاد کنید

   ```bash
   mkdir keyring

   utils/generate-random-id -m adnlid
   ```

   شما چیزی شبیه به این خواهید دید

   ```bash
   45061C1D4EC44A937D0318589E13C73D151D1CEF5D3C0E53AFBCF56A6C2FE2BD vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3
   ```

   این آدرس ADNL تازه‌تولیدشده شماست، در قالب هگزادسیمال و کاربر پسند. کلید خصوصی مربوطه در فایل `45061...2DB` در دایرکتوری فعلی ذخیره شده است. کلید را به دایرکتوری کلیدها منتقل کنید

   ```bash
   mv 45061C1* keyring/
   ```

5. مطمئن شوید وب‌سرور شما درخواست‌های HTTP با دامنه‌های `.ton` و `.adnl` را می‌پذیرد.

   به عنوان مثال، اگر از nginx با پیکربندی `server_name example.com;` استفاده می‌کنید، باید آن را به `server_name _;` یا `server_name example.com example.ton vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3.adnl;` تغییر دهید.

6. پراکسی را در حالت معکوس اجرا کنید

   ```bash
   rldp-http-proxy/rldp-http-proxy -a <your-server-ip>:3333 -L '*' -C global.config.json -A <your-adnl-address> -d -l <log-file>
   ```

   که در آن `<your_public_ip>` آدرس عمومی IPv4 سرور شما و `<your_adnl_address>` آدرس ADNL تولید شده در مرحله‌ی قبلی است.

اگر می‌خواهید سایت TON شما به طور دائمی اجرا شود، باید از گزینه‌های `-d` و `-l <log-file>` استفاده کنید.

مثال:

```bash
rldp-http-proxy/rldp-http-proxy -a 777.777.777.777:3333 -L '*' -C global.config.json -A vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3 -d -l tonsite.log
```

اگر همه چیز به درستی کار کند، پراکسی RLDP-HTTP درخواست‌های HTTP ورودی از شبکه‌ی TON را از طریق RLDP/ADNL که بر روی پورت UDP 3333 (البته، می‌توانید از هر پورت UDP دیگری نیز استفاده کنید) از آدرس IPv4 `<your-server-ip>` اجرا می‌شود (به ویژه اگر از فایروال استفاده می‌کنید، فراموش نکنید `rldp-http-proxy` را مجاز به دریافت و ارسال بسته‌های UDP از این پورت کنید)، می‌پذیرد و این درخواست‌های HTTP که به همه‌ی میزبان‌ها آدرس داده شدند (اگر می‌خواهید فقط به میزبان‌های خاصی فوروارد کنید، `-L '*'` را به `-L <your hostname>` تغییر دهید) به پورت TCP `80` در `127.0.0.1` (یعنی به وب‌سرور معمولی شما) فوروارد می‌کند.

شما می‌توانید سایت TON `http://<your-adnl-address>.adnl` (`http://vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3.adnl` در این مثال) را از مرورگری که بر روی یک دستگاه کلاینت اجرا می‌شود همانطور که در بخش "دسترسی به سایت‌های TON" توضیح داده شد، بازدید کنید و بررسی کنید که آیا سایت TON شما واقعاً برای عموم در دسترس است یا نه.

اگر می‌خواهید، می‌توانید یک دامنه TON DNS مانند 'example.ton' را [ثبت](/v3/guidelines/web3/ton-proxy-sites/site-and-domain-management) کنید و یک رکورد `site` برای این دامنه ایجاد کنید که به آدرس ADNL دائمی سایت TON شما اشاره دارد. سپس پراکسی‌های RLDP-HTTP که در حالت کلاینت اجرا می‌شوند، http://example.ton را به عنوان اشاره‌کننده به آدرس ADNL شما تشخیص می‌دهند و به سایت TON شما دسترسی خواهند داشت.

همچنین می‌توانید یک پراکسی معکوس بر روی یک سرور جداگانه اجرا کنید و وب‌سرور خود را به عنوان آدرس راه‌دور تنظیم کنید. در این صورت از `-R '*'@<YOUR_WEB_SERVER_HTTP_IP>:<YOUR_WEB_SERVER_HTTP_PORT>` به جای `-L '*'` استفاده کنید.

مثال:

```bash
rldp-http-proxy/rldp-http-proxy -a 777.777.777.777:3333 -R '*'@333.333.333.333:80 -C global.config.json -A vcqmha5j3ceve35ammfrhqty46rkhi455otydstv66pk2tmf7rl25f3 -d -l tonsite.log
```

در این حالت سرور وب معمولی شما باید در `http://333.333.333.333:80` قابل دسترسی باشد (این IP به بیرون منتشر نخواهد شد).

### پیشنهادات

از آنجاکه ناشناس بودن تنها در TON Proxy 2.0 در دسترس خواهد بود، اگر نمی‌خواهید آدرس IP وب‌سرور خود را فاش کنید، می‌توانید آن را به دو روش انجام دهید:

- در یک سرور جداگانه با پرچم `-R` همانطور که در بالا توضیح داده شد، یک پراکسی معکوس اجرا کنید.

- یک سرور تکراری با کپی از وب‌سایت خود ایجاد کنید و پراکسی معکوس را به صورت محلی اجرا کنید.
