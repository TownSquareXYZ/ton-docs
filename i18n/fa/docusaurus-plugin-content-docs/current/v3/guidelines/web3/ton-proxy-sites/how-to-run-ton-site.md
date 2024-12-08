# چگونه سایت‌های TON را اجرا کنیم

## 👋 معرفی

[سایت‌های TON](https://blog.ton.org/ton-sites) تقریباً مانند سایت‌های معمولی کار می‌کنند به جز نصب آن‌ها. برای راه‌اندازی آن‌ها چند اقدام اضافی لازم است. در این آموزش، من به شما نشان می‌دهم چگونه این کار را انجام دهید.

## 🖥 اجرای سایت TON

[Tonutils Reverse Proxy](https://github.com/tonutils/reverse-proxy) را نصب کنید تا TON Proxy را برای سایت خود استفاده کنید.

### نصب بر روی هر نوع لینوکس

##### دانلود

```bash
wget https://github.com/ton-utils/reverse-proxy/releases/latest/download/tonutils-reverse-proxy-linux-amd64
chmod +x tonutils-reverse-proxy-linux-amd64
```

##### اجرا کردن

با پیکربندی دامنه اجرا کنید و مراحل زیر را دنبال کنید:

```
./tonutils-reverse-proxy-linux-amd64 --domain your-domain.ton 
```

کد QR را از ترمینال خود با استفاده از Tonkeeper، Tonhub یا هر کیف‌پول دیگری اسکن کنید و تراکنش را انجام دهید. دامنه شما به سایت شما پیوند داده می‌شود.

###### اجرا بدون دامنه

به صورت جایگزین، اگر دامنه .ton یا .t.me ندارید، می‌توانید با دامنه .adnl به صورت ساده اجرا کنید:

```
./tonutils-reverse-proxy-linux-amd64
```

##### استفاده

اکنون هر کسی می‌تواند با استفاده از آدرس یا دامنه ADNL به سایت TON شما دسترسی داشته باشد.

اگر می‌خواهید برخی از تنظیمات مانند proxy pass URL را تغییر دهید، فایل `config.json` را باز کرده، ویرایش کنید و پراکسی را مجدداً راه‌اندازی کنید. proxy pass URL پیش‌فرض `http://127.0.0.1:80/` است

پراکسی سرور هد‌رهایی اضافه می‌کند:
`X-Adnl-Ip` - آی‌پی کلاینت، و `X-Adnl-Id` - شناسه ADNL کلاینت

### نصب بر روی هر سیستم عامل دیگر

سورس کد را بیلد کنید و آن را همانند مرحله ۲ برای لینوکس اجرا کنید. برای بیلد، محیط Go لازم است.

```bash
git clone https://github.com/tonutils/reverse-proxy.git
cd reverse-proxy
make build
```

برای بیلد برای دیگر سیستم‌عامل‌ها، `make all` را اجرا کنید

## 👀 مراحل بیشتر

### 🔍 بررسی قابلیت دسترسی به سایت

پس از انجام تمام مراحل روش انتخابی شما، باید TON Proxy راه‌اندازی شده باشد. اگر همه چیز موفقیت‌آمیز بود، سایت شما در آدرس ADNL دریافتی در مرحله مربوطه در دسترس خواهد بود.

شما می‌توانید با باز کردن این آدرس با دامنه `.adnl`، قابلیت دسترسی به سایت را بررسی کنید. همچنین به یاد داشته باشید که برای باز کردن سایت باید یک TON Proxy در مرورگر شما در حال اجرا باشد، به عنوان مثال از طریق یک افزونه [MyTonWallet](https://mytonwallet.io/).

## 📌 منابع

- [TON Sites، TON WWW و TON Proxy](https://blog.ton.org/ton-sites)
- [Tonutils Reverse Proxy](https://github.com/tonutils/reverse-proxy)
- نویسندگان: [Andrew Burnosov](https://github.com/AndreyBurnosov) (TG: [@AndrewBurnosov](https://t.me/AndreyBurnosov)), [Daniil Sedov](https://gusarich.com) (TG: [@sedov](https://t.me/sedov)), [George Imedashvili](https://github.com/drforse)

## همچنین ببینید

- [اجرای پیاده‌سازی C++](/v3/guidelines/web3/ton-proxy-sites/running-your-own-ton-proxy)
