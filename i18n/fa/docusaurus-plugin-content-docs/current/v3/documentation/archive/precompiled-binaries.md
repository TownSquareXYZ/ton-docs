import Feedback from '@site/src/components/Feedback';

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';
import Button from '@site/src/components/button'

# باینری‌های از پیش کامپایل شده

:::caution مهم
دیگر نیازی به نصب دستی باینری‌ها با Blueprint SDK ندارید.
:::

همه باینری‌های لازم برای توسعه و تست همراه با SDK Blueprint ارائه می‌شوند.

<Button href="/v3/documentation/smart-contracts/getting-started/javascript"
colorType="primary" sizeType={'sm'}>

به Blueprint SDK مهاجرت کنید

</Button>

## باینری‌های از پیش کامپایل شده

اگر از Blueprint SDK برای توسعه قراردادهای هوشمند استفاده نمی‌کنید، می‌توانید از باینری‌های از پیش کامپایل شده برای سیستم‌عامل و ابزار انتخابی خود استفاده کنید.

### پیش‌نیازها

برای توسعه محلی قراردادهای هوشمند TON *بدون جاوااسکریپت*، باید باینری‌های `func`, `fift`, و `lite client` را روی دستگاه خود آماده کنید.

می‌توانید آنها را از زیر دانلود و راه‌اندازی کنید یا این مقاله از جامعه TON را بخوانید:

- [راه‌اندازی محیط توسعه TON](https://blog.ton.org/setting-up-a-ton-development-environment)

### ۱. دانلود

باینری‌ها را از جدول زیر دانلود کنید. اطمینان حاصل کنید که نسخه صحیح برای سیستم‌عامل خود را انتخاب کرده و هر وابستگی اضافی را نصب کنید:

| سیستم‌عامل                        | باینری‌های TON                                                                                | fift                                                                                       | func                                                                                       | lite-client                                                                                       | وابستگی‌های اضافی                                                                                        |
| --------------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| MacOS x86-64                      | [دانلود](https://github.com/ton-blockchain/ton/releases/latest/download/ton-mac-x86-64.zip)   | [دانلود](https://github.com/ton-blockchain/ton/releases/latest/download/fift-mac-x86-64)   | [دانلود](https://github.com/ton-blockchain/ton/releases/latest/download/func-mac-x86-64)   | [دانلود](https://github.com/ton-blockchain/ton/releases/latest/download/lite-client-mac-x86-64)   |                                                                                                          |
| MacOS arm64                       | [دانلود](https://github.com/ton-blockchain/ton/releases/latest/download/ton-mac-arm64.zip)    |                                                                                            |                                                                                            |                                                                                                   | `brew install openssl ninja libmicrohttpd pkg-config`                                                    |
| Windows x86-64                    | [دانلود](https://github.com/ton-blockchain/ton/releases/latest/download/ton-win-x86-64.zip)   | [دانلود](https://github.com/ton-blockchain/ton/releases/latest/download/fift.exe)          | [دانلود](https://github.com/ton-blockchain/ton/releases/latest/download/func.exe)          | [دانلود](https://github.com/ton-blockchain/ton/releases/latest/download/lite-client.exe)          | نصب [OpenSSL 1.1.1](/ton-binaries/windows/Win64OpenSSL_Light-1_1_1q.msi) |
| Linux x86_64 | [دانلود](https://github.com/ton-blockchain/ton/releases/latest/download/ton-linux-x86_64.zip) | [دانلود](https://github.com/ton-blockchain/ton/releases/latest/download/fift-linux-x86_64) | [دانلود](https://github.com/ton-blockchain/ton/releases/latest/download/func-linux-x86_64) | [دانلود](https://github.com/ton-blockchain/ton/releases/latest/download/lite-client-linux-x86_64) |                                                                                                          |
| Linux arm64                       | [دانلود](https://github.com/ton-blockchain/ton/releases/latest/download/ton-linux-arm64.zip)  |                                                                                            |                                                                                            |                                                                                                   | `sudo apt install libatomic1 libssl-dev`                                                                 |

### ۲. باینری‌های خود را تنظیم کنید

export const Highlight = ({children, color}) => (
<span
style={{
backgroundColor: color,
borderRadius: '2px',
color: '#fff',
padding: '0.2rem',
}}>
{children} </span>
);

<Tabs groupId="operating-systems">
  <TabItem value="win" label="Windows">

1. پس از دانلود، باید یک پوشه جدید `create` کنید. به عنوان مثال: **`C:/Users/%USERNAME%/ton/bin`** و فایل‌های نصب شده را به آنجا منتقل کنید.

2. برای باز کردن متغیرهای محیطی Windows، دکمه‌های <Highlight color="#1877F2">Win + R</Highlight> روی صفحه کلید را فشار دهید، `sysdm.cpl` را تایپ کنید و Enter را بزنید.

3. در زبانه "*پیشرفته*"، دکمه <Highlight color="#1877F2">"متغیرهای محیطی..."</Highlight> را کلیک کنید.

4. در بخش *"متغیرهای کاربر"*، متغیر "*Path*" را انتخاب کرده و <Highlight color="#1877F2">"ویرایش"</Highlight> را کلیک کنید (این معمولاً لازم است).

5. برای اضافه کردن یک مقدار جدید `(مسیر)` به متغیر سیستم در پنجره بعدی، دکمه <Highlight color="#1877F2">"جدید"</Highlight> را کلیک کنید.
  در فیلد جدید، باید مسیر پوشه‌ای را که فایل‌های نصب شده در آن ذخیره شده‌اند وارد کنید:

```
C:\Users\%USERNAME%\ton\bin\
```

6. برای بررسی این که آیا همه چیز به درستی نصب شده است، در ترمینال (*cmd.exe*) اجرا کنید:

```bash
fift -V -and func -V -and lite-client -V
```

7. اگر قصد دارید از fift استفاده کنید، به متغیر محیطی `FIFTPATH` با واردات لازم نیاز دارید:

  1. [fiftlib.zip](/ton-binaries/windows/fiftlib.zip) دانلود کنید
  2. فایل زیپ را در یک دایرکتوری بر روی ماشین خود باز کنید (مثل **`C:/Users/%USERNAME%/ton/lib/fiftlib`**)
  3. یک متغیر محیطی جدید `(دکمه <Highlight color="#1877F2">"جدید"</Highlight> را کلیک کنید)` `FIFTPATH` در بخش "*متغیرهای کاربر*" ایجاد کنید.
  4. در قسمت "*مقدار متغیر*" مسیر فایل‌ها را مشخص کنید: **`/%USERNAME%/ton/lib/fiftlib`** و روی <Highlight color="#1877F2">OK</Highlight> کلیک کنید. انجام شد.

:::caution مهم
به جای کلمه کلیدی `%USERNAME%`، باید `نام‌کاربری` خودتان را وارد کنید.\
:::</TabItem>
<TabItem value="mac" label="Linux / MacOS">۱. بعد از دانلود، با تغییر مجوزها اطمینان حاصل کنید که فایل‌های دودویی دانلود شده قابل اجرا هستند.```bash
chmod +x func
chmod +x fift
chmod +x lite-client
```۲. همچنین مفید است که این فایل‌های دودویی را به مسیر خود اضافه کنید (یا آنها را به `/usr/local/bin` کپی کنید) تا از هر جایی به آنها دسترسی داشته باشید.```bash
cp ./func /usr/local/bin/func
cp ./fift /usr/local/bin/fift
cp ./lite-client /usr/local/bin/lite-client
```۳. برای بررسی اینکه همه چیز به درستی نصب شده است، در ترمینال اجرا کنید.```bash
fift -V && func -V && lite-client -V
```۴. اگر قصد `استفاده از fift` دارید، همچنین [fiftlib.zip](/ton-binaries/windows/fiftlib.zip) را دانلود کنید، در یک دایرکتوری روی دستگاه خود باز کنید (مانند `/usr/local/lib/fiftlib`)، و متغیر محیطی `FIFTPATH` را تنظیم کنید تا به این دایرکتوری اشاره کند.```
unzip fiftlib.zip
mkdir -p /usr/local/lib/fiftlib
cp fiftlib/* /usr/local/lib/fiftlib
```:::info هی، شما تقریباً تمام کرده‌اید :)
به خاطر داشته باشید که متغیر [محیطی](https://stackoverflow.com/questions/14637979/how-to-permanently-set-path-on-linux-unix) `FIFTPATH` را طوری تنظیم کنید که به این دایرکتوری اشاره کند.
:::

</TabItem>
<TabItem value="mac" label="Linux / MacOS">

1. بعد از دانلود، با تغییر مجوزها اطمینان حاصل کنید که فایل‌های دودویی دانلود شده قابل اجرا هستند.

```bash
chmod +x func
chmod +x fift
chmod +x lite-client
```

2. همچنین مفید است که این فایل‌های دودویی را به مسیر خود اضافه کنید (یا آنها را به `/usr/local/bin` کپی کنید) تا از هر جایی به آنها دسترسی داشته باشید.

```bash
cp ./func /usr/local/bin/func
cp ./fift /usr/local/bin/fift
cp ./lite-client /usr/local/bin/lite-client
```

3. برای بررسی اینکه همه چیز به درستی نصب شده است، در ترمینال اجرا کنید.

```bash
fift -V && func -V && lite-client -V
```

4. اگر قصد `استفاده از fift` دارید، همچنین [fiftlib.zip](/ton-binaries/windows/fiftlib.zip) را دانلود کنید، در یک دایرکتوری روی دستگاه خود باز کنید (مانند `/usr/local/lib/fiftlib`)، و متغیر محیطی `FIFTPATH` را تنظیم کنید تا به این دایرکتوری اشاره کند.

```
unzip fiftlib.zip
mkdir -p /usr/local/lib/fiftlib
cp fiftlib/* /usr/local/lib/fiftlib
```

:::info هی، شما تقریباً تمام کرده‌اید :)
به خاطر داشته باشید که متغیر [محیطی](https://stackoverflow.com/questions/14637979/how-to-permanently-set-path-on-linux-unix) `FIFTPATH` را طوری تنظیم کنید که به این دایرکتوری اشاره کند.
:::

  </TabItem>
</Tabs>

## ساخت از منبع

اگر نمی‌خواهید به باینری‌های پیش‌کامپایل شده وابسته باشید و ترجیح می‌دهید باینری‌ها را خودتان کامپایل کنید، می‌توانید از [دستورالعمل‌های رسمی](/v3/guidelines/smart-contracts/howto/compile/compilation-instructions) پیروی کنید.

راهنماهای آماده برای استفاده در زیر ارائه شده‌اند:

### لینوکس (اوبونتو / دبیان)

```bash
sudo apt update
sudo apt install git make cmake g++ libssl-dev zlib1g-dev wget
cd ~ && git clone https://github.com/ton-blockchain/ton.git
cd ~/ton && git submodule update --init
mkdir ~/ton/build && cd ~/ton/build && cmake .. -DCMAKE_BUILD_TYPE=Release && make -j 4
```

## سایر منابع برای باینری‌ها

تیم اصلی برای چندین سیستم‌عامل به‌صورت [GitHub Actions](https://github.com/ton-blockchain/ton/releases/latest) ساخت خودکار ارائه می‌دهد.

روی لینک بالا کلیک کنید، از سمت چپ جریان کاری مرتبط با سیستم‌عامل خود را انتخاب کنید، روی ساخت اخیر سبز کلیک کنید، و `ton-binaries` را در زیر عنوان "آثار" دانلود کنید.

<Feedback />

