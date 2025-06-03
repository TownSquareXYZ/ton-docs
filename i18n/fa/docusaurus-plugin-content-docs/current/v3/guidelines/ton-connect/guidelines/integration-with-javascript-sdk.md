import Feedback from '@site/src/components/Feedback';

# راهنمای یکپارچه‌سازی با JavaScript SDK

:::danger
The page is outdated and will be deleted soon. Learn actual JS flow from [the guideline for web](/v3/guidelines/ton-connect/frameworks/web).
:::

In this tutorial, we’ll create a sample web app that supports TON Connect 2.0 authentication. It will allow for signature verification to eliminate the possibility of fraudulent identity impersonation without the need for agreement establishment between parties.

## پیوندهای مستندات

1. [مستندات @tonconnect/sdk](https://www.npmjs.com/package/@tonconnect/sdk)
2. [پروتکل تبادل پیام برنامه کیف پول](https://github.com/ton-connect/docs/blob/main/requests-responses.md)
3. [پیاده‌سازی tonkeeper در سمت کیف پول](https://github.com/tonkeeper/wallet/tree/main/packages/mobile/src/tonconnect)

## پیش‌نیازها

In order for connectivity to be fluent between apps and wallets, the web app must make use of manifest that is accessible via wallet applications. The prerequisite to accomplish this is typically a host for static files. For example, if a developer wants to make use of GitHub pages, or deploy their website using TON Sites hosted on their computer. This would mean their web app site is publicly accessible.

## دریافت لیست کیف‌های پشتیبانی شده

To increase the overall adoption of TON Blockchain, it is necessary that TON Connect 2.0 is able to facilitate a vast number of application and wallet connectivity integrations. Of late and of significant importance, the ongoing development of TON Connect 2.0 has allowed for the connection of the Tonkeeper, TonHub, MyTonWallet and other wallets with various TON Ecosystem Apps. It is our mission to eventually allow for the exchange of data between applications and all wallet types built on TON via the TON Connect protocol. For now, this is achieved by enabling TON Connect to load an extensive list of available wallets currently operating within the TON Ecosystem.

در حال حاضر، نمونه برنامه وب ما توانایی‌های زیر را دارد:

1. بارگذاری TON Connect SDK (کتابخانه‌ای که برای ساده‌سازی یکپارچه‌سازی طراحی شده است)،
2. ایجاد یک اتصال‌دهنده (در حال حاضر بدون مانیفست برنامه)،
3. بارگذاری یک فهرست از کیف‌های پشتیبانی شده (از [wallets.json در GitHub](https://raw.githubusercontent.com/ton-connect/wallets-list/main/wallets.json)).

به منظور یادگیری، بیایید به صفحه HTML که توسط کد زیر توصیف شده است نگاهی بیندازیم:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <script src="https://unpkg.com/@tonconnect/sdk@latest/dist/tonconnect-sdk.min.js" defer></script>  <!-- (1) -->
  </head>
  <body>
    <script>
      window.onload = async () => {
        const connector = new TonConnectSDK.TonConnect();  // (2)
        const walletsList = await connector.getWallets();  // (3)
        
        console.log(walletsList);
      }
    </script>
  </body>
</html>
```

If you load this page in a browser and check the console, you may see something like this:

```bash
> Array [ {…}, {…} ]

0: Object { name: "Tonkeeper", imageUrl: "https://tonkeeper.com/assets/tonconnect-icon.png", aboutUrl: "https://tonkeeper.com", … }
  aboutUrl: "https://tonkeeper.com"
  bridgeUrl: "https://bridge.tonapi.io/bridge"
  deepLink: undefined
  embedded: false
  imageUrl: "https://tonkeeper.com/assets/tonconnect-icon.png"
  injected: false
  jsBridgeKey: "tonkeeper"
  name: "Tonkeeper"
  tondns: "tonkeeper.ton"
  universalLink: "https://app.tonkeeper.com/ton-connect"
```

بر اساس مشخصات TON Connect ۲٫۰، اطلاعات برنامه کیف پول همیشه از قالب زیر استفاده می‌کند:

```js
{
    name: string;
    imageUrl: string;
    tondns?: string;
    aboutUrl: string;
    universalLink?: string;
    deepLink?: string;
    bridgeUrl?: string;
    jsBridgeKey?: string;
    injected?: boolean; // true if this wallet is injected to the webpage
    embedded?: boolean; // true if the DAppis opened inside this wallet's browser
}
```

## نمایش دکمه برای برنامه‌های مختلف کیف پول

دکمه‌ها ممکن است بر اساس طراحی برنامه وب شما متفاوت باشند.
صفحه فعلی نتیجه زیر را ایجاد می‌کند:

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <script src="https://unpkg.com/@tonconnect/sdk@latest/dist/tonconnect-sdk.min.js" defer></script>

    // highlight-start
    <style>
      body {
        width: 1000px;
        margin: 0 auto;
        font-family: Roboto, sans-serif;
      }
      .section {
        padding: 20px; margin: 20px;
        border: 2px #AEFF6A solid; border-radius: 8px;
      }
      #tonconnect-buttons>button {
        display: block;
        padding: 8px; margin-bottom: 8px;
        font-size: 18px; font-family: inherit;
      }
      .featured {
        font-weight: 800;
      }
    </style>
    // highlight-end
  </head>
  <body>
    // highlight-start
    <div class="section" id="tonconnect-buttons">
    </div>
    // highlight-end
    
    <script>
      const $ = document.querySelector.bind(document);
      
      window.onload = async () => {
        const connector = new TonConnectSDK.TonConnect();
        const walletsList = await connector.getWallets();

        // highlight-start
        let buttonsContainer = $('#tonconnect-buttons');
        
        for (let wallet of walletsList) {
          let connectButton = document.createElement('button');
          connectButton.innerText = 'Connect with ' + wallet.name;
          
          if (wallet.embedded) {
            // `embedded` means we are browsing the app from wallet application
            // we need to mark this sign-in option somehow
            connectButton.classList.add('featured');
          }
          
          if (!wallet.bridgeUrl && !wallet.injected && !wallet.embedded) {
            // no `bridgeUrl` means this wallet app is injecting JS code
            // no `injected` and no `embedded` -> app is inaccessible on this page
            connectButton.disabled = true;
          }
          
          buttonsContainer.appendChild(connectButton);
        }
	// highlight-end
      };
    </script>
  </body>
</html>
```

لطفاً به نکات زیر توجه کنید:

1. اگر صفحه وب از طریق برنامه کیف پول نمایش داده شود، گزینه `embedded` را به `true` تنظیم می‌کند. این به معنای آن است که باید این گزینه ورود را که بیشتر استفاده می‌شود، مورد توجه قرار داد.
2. اگر یک کیف خاص تنها با استفاده از JavaScript ساخته شده باشد (آن دارای `bridgeUrl` نمی‌باشد) و آن خاصیت `injected` را تنظیم نکرده باشد (یا `embedded`، برای امنیت)، در این صورت واضح است که دسترسی به آن وجود ندارد و دکمه باید غیرفعال شود.

## اتصال بدون مانیفست برنامه

در صورتی که اتصال بدون مانیفست برنامه صورت گیرد، اسکریپت باید به صورت زیر تغییر کند:

```js
      const $ = document.querySelector.bind(document);
      
      window.onload = async () => {
        const connector = new TonConnectSDK.TonConnect();
        const walletsList = await connector.getWallets();
        
        const unsubscribe = connector.onStatusChange(
          walletInfo => {
            console.log('Connection status:', walletInfo);
          }
        );
        
        let buttonsContainer = $('#tonconnect-buttons');

        for (let wallet of walletsList) {
          let connectButton = document.createElement('button');
          connectButton.innerText = 'Connect with ' + wallet.name;
          
          if (wallet.embedded) {
            // `embedded` means we are browsing the app from wallet application
            // we need to mark this sign-in option somehow
            connectButton.classList.add('featured');
          }
          
          // highlight-start
          if (wallet.embedded || wallet.injected) {
            connectButton.onclick = () => {
              connectButton.disabled = true;
              connector.connect({jsBridgeKey: wallet.jsBridgeKey});
            };
          } else if (wallet.bridgeUrl) {
            connectButton.onclick = () => {
              connectButton.disabled = true;
              console.log('Connection link:', connector.connect({
                universalLink: wallet.universalLink,
                bridgeUrl: wallet.bridgeUrl
              }));
            };
          } else {
            // wallet app does not provide any auth method
            connectButton.disabled = true;
          }
	  // highlight-end
          
          buttonsContainer.appendChild(connectButton);
        }
      };
```

اکنون که فرآیند فوق انجام شده است، تغییرات وضعیت ثبت می‌شوند (تا ببینیم آیا TON Connect کار می‌کند یا نه). نمایش مدال‌ها با کدهای QR برای اتصال خارج از محدوده این راهنما است. برای اهداف آزمایشی می‌توان از یک افزونه مرورگر استفاده کرد یا با هر وسیله‌ای که لازم است (برای مثال، با استفاده از تلگرام) لینک درخواست اتصال را به تلفن کاربر ارسال کرد.
توجه: هنوز یک مانیفست برنامه ایجاد نکرده‌ایم. در این زمان، بهترین روش این است که نتیجه نهایی را در صورتی که این الزامات برآورده نشود، تحلیل کنیم.

### ورود با Tonkeeper

برای ورود به Tonkeeper، پیوند زیر برای احراز هویت ایجاد می‌شود (زیر برای مراجعه):

```
https://app.tonkeeper.com/ton-connect?v=2&id=3c12f5311be7e305094ffbf5c9b830e53a4579b40485137f29b0ca0c893c4f31&r=%7B%22manifestUrl%22%3A%22null%2Ftonconnect-manifest.json%22%2C%22items%22%3A%5B%7B%22name%22%3A%22ton_addr%22%7D%5D%7D
```

هنگامی که رمزگشایی شود، پارامتر `r` قالب JSON زیر را تولید می‌کند:

```js
{"manifestUrl":"null/tonconnect-manifest.json","items":[{"name":"ton_addr"}]}
```

با کلیک بر روی لینک تلفن همراه، Tonkeeper به طور خودکار باز و سپس بسته می‌شود و درخواست را رد می‌کند. علاوه بر این، خطای زیر در کنسول صفحه برنامه وب ظاهر می‌شود:
`خطا: [TON_CONNECT_SDK_ERROR] نمی‌توان null/tonconnect-manifest.json را گرفت`.

This indicates that the application manifest must be available for download.

## اتصال با استفاده از مانیفست برنامه

از این نقطه به بعد، لازم است فایل‌های کاربر (عمدتاً tonconnect-manifest.json) در جایی میزبانی شوند. در این مثال، ما از مانیفست یک برنامه وب دیگر استفاده خواهیم کرد. با این حال، این برای محیط‌های تولیدی توصیه نمی‌شود، اما برای اهداف آزمایشی مجاز است.

کد نمونه زیر:

```js
      window.onload = async () => {
        const connector = new TonConnectSDK.TonConnect();
        
        const walletsList = await connector.getWallets();
        
        const unsubscribe = connector.onStatusChange(
          walletInfo => {
            console.log('Connection status:', walletInfo);
          }
        );
```

باید با این نسخه جایگزین شود:

```js
      window.onload = async () => {
        const connector = new TonConnectSDK.TonConnect({manifestUrl: 'https://ratingers.pythonanywhere.com/ratelance/tonconnect-manifest.json'});
        // highlight-next-line
        window.connector = connector;  // for experimenting in browser console
        
        const walletsList = await connector.getWallets();
        
        const unsubscribe = connector.onStatusChange(
          walletInfo => {
            console.log('Connection status:', walletInfo);
          }
        );
	// highlight-next-line
        connector.restoreConnection();
```

در نسخه جدیدتر بالا، ذخیره متغیر `connector` در `window` اضافه شده است تا در کنسول مرورگر قابل دسترسی باشد. علاوه بر این، `restoreConnection` اضافه شده است تا کاربر به ورود به حساب در هر صفحه از برنامه وب نیاز نداشته باشد.

### ورود با Tonkeeper

اگر درخواست خود را از کیف پول رد کنیم، نتیجه‌ای که در کنسول ظاهر می‌شود `Error: [TON_CONNECT_SDK_ERROR] Wallet declined the request` خواهد بود.

بنابراین، اگر پیوند ذخیره شده باشد، کاربر می‌تواند همان درخواست ورود را بپذیرد. این بدان معناست که برنامه وب باید بتواند رد اعتبارسنجی را به عنوان نهایی در نظر نگیرد تا به درستی کار کند.

پس از آن، درخواست ورود پذیرفته شده و بلافاصله در کنسول مرورگر به صورت زیر منعکس می‌شود:

```bash
22:40:13.887 Connection status:
Object { device: {…}, provider: "http", account: {…} }
  account: Object { address: "0:b2a1ec...", chain: "-239", walletStateInit: "te6cckECFgEAAwQAAgE0ARUBFP8A9..." }
  device: Object {platform: "android", appName: "Tonkeeper", appVersion: "2.8.0.261", …}
  provider: "http"
```

نتایج فوق، موارد زیر را در نظر گرفته‌اند:

1. **حساب**: اطلاعات: شامل آدرس (ورک‌چین+هش)، شبکه (مین‌نت/تست‌نت)، و حالت اولیه کیف پول که برای استخراج کلید عمومی استفاده می‌شود.
2. **دستگاه**: اطلاعات: شامل نام و نسخه برنامه کیف پول (نام باید با چیزی که در ابتدا درخواست شد مساوی باشد، اما می‌توان آن را برای اطمینان از اصالت بررسی کرد)، و نام پلتفرم و لیست ویژگی‌های پشتیبانی شده.
3. **ارائه‌دهنده**: شامل http -- که اجازه می‌دهد تا تمام درخواست‌ها و پاسخ‌ها بین کیف پول و برنامه‌های وب از طریق پل اجرا شوند.

## خروج از سیستم و درخواست TonProof

اکنون وارد مینی اپ خود شده‌ایم، اما... چگونه بک‌اند می‌داند که طرف صحیح است؟ برای تأیید این موضوع باید درخواست اثبات مالکیت کیف پول را بدهیم.

این تنها با استفاده از احراز هویت قابل انجام است، بنابراین باید خارج شویم. بنابراین، کد زیر را در کنسول اجرا می‌کنیم:

```js
connector.disconnect();
```

وقتی فرآیند قطع ارتباط کامل شد، `وضعیت اتصال: null` نمایش داده می‌شود.

قبل از افزودن TonProof، کد را طوری تغییر دهیم که نشان دهد پیاده‌سازی فعلی امنیتی نیست:

```js
let connHandler = connector.statusChangeSubscriptions[0];
connHandler({
  device: {
    appName: "Uber Singlesig Cold Wallet App",
    appVersion: "4.0.1",
    features: [],
    maxProtocolVersion: 3,
    platform: "ios"
  },
  account: {
    /* TON Foundation address */
    address: '0:83dfd552e63729b472fcbcc8c45ebcc6691702558b68ec7527e1ba403a0f31a8',
    chain: '-239',
    walletStateInit: 'te6ccsEBAwEAoAAFcSoCATQBAgDe/wAg3SCCAUyXuiGCATOcurGfcbDtRNDTH9MfMdcL/+ME4KTyYIMI1xgg0x/TH9Mf+CMTu/Jj7UTQ0x/TH9P/0VEyuvKhUUS68qIE+QFUEFX5EPKj+ACTINdKltMH1AL7AOjRAaTIyx/LH8v/ye1UAFAAAAAAKamjF3LJ7WtipuLroUqTuQRi56Nnd3vrijj7FbnzOETSLOL/HqR30Q=='
  },
  provider: 'http'
});
```

خطوط کد حاصل در کنسول تقریباً با خطوطی که هنگام شروع اتصال در اول نمایش داده شدند، یکسان هستند. بنابراین، اگر بک‌اند احراز هویت کاربر را به درستی همانطور که انتظار می‌رفت انجام ندهد، راهی برای آزمایش اینکه آیا به درستی کار می‌کند، نیاز است. برای دستیابی به این، می‌توان به عنوان بنیاد TON در داخل کنسول عمل کرد تا بتوان قانونی بودن بالانس‌های توکن و پارامترهای مالکیت توکن را آزمایش کرد. طبعاً، کد ارائه شده هیچ متغیری را در کانکتور تغییر نمی‌دهد، اما کاربر می‌تواند برنامه را به دلخواه خود استفاده کند مگر اینکه کانکتور با بستن محافظت شود. حتی اگر چنین باشد، استخراج آن با استفاده از دیباگر و نقاط شکست کدنویسی دشوار نیست.

اکنون که احراز هویت کاربر تأیید شده است، بیایید به نوشتن کد بپردازیم.

## اتصال با استفاده از TonProof

طبق مستندات SDK TON Connect، آرگومان دوم به متد `connect()` اشاره دارد که حاوی یک payload است که توسط کیف پول پیچیده و امضا می‌شود. بنابراین، نتیجه کد اتصال جدید است:

```js
          if (wallet.embedded || wallet.injected) {
            connectButton.onclick = () => {
              connectButton.disabled = true;
              connector.connect({jsBridgeKey: wallet.jsBridgeKey},
                                {tonProof: 'doc-example-<BACKEND_AUTH_ID>'});
            };
          } else if (wallet.bridgeUrl) {
            connectButton.onclick = () => {
              connectButton.disabled = true;
              console.log('Connection link:', connector.connect({
                universalLink: wallet.universalLink,
                bridgeUrl: wallet.bridgeUrl
              }, {tonProof: 'doc-example-<BACKEND_AUTH_ID>'}));
            };
```

لینک اتصال:

```
https://app.tonkeeper.com/ton-connect?v=2&id=4b0a7e2af3b455e0f0bafe14dcdc93f1e9e73196ae2afaca4d9ba77e94484a44&r=%7B%22manifestUrl%22%3A%22https%3A%2F%2Fratingers.pythonanywhere.com%2Fratelance%2Ftonconnect-manifest.json%22%2C%22items%22%3A%5B%7B%22name%22%3A%22ton_addr%22%7D%2C%7B%22name%22%3A%22ton_proof%22%2C%22payload%22%3A%22doc-example-%3CBACKEND_AUTH_ID%3E%22%7D%5D%7D
```

پارامتر `r` بسط داده و ساده شده:

```js
{
  "manifestUrl":
    "https://ratingers.pythonanywhere.com/ratelance/tonconnect-manifest.json",
  "items": [
    {"name": "ton_addr"},
    {"name": "ton_proof", "payload": "doc-example-<BACKEND_AUTH_ID>"}
  ]
}
```

سپس لینک آدرس URL به دستگاه موبایل ارسال می‌شود و با استفاده از Tonkeeper باز می‌شود.

پس از تکمیل این فرآیند، اطلاعات زیر که مختص به کیف پول است دریافت می‌شود:

```js
{
  "device": {
    "platform": "android",
    "appName": "Tonkeeper",
    "appVersion": "2.8.0.261",
    "maxProtocolVersion": 2,
    "features": [
      "SendTransaction"
    ]
  },
  "provider": "http",
  "account": {
    "address": "0:b2a1ecf5545e076cd36ae516ea7ebdf32aea008caa2b84af9866becb208895ad",
    "chain": "-239",
    "walletStateInit": "te6cckECFgEAAwQAAgE0ARUBFP8A9KQT9LzyyAsCAgEgAxACAUgEBwLm0AHQ0wMhcbCSXwTgItdJwSCSXwTgAtMfIYIQcGx1Z70ighBkc3RyvbCSXwXgA/pAMCD6RAHIygfL/8nQ7UTQgQFA1yH0BDBcgQEI9ApvoTGzkl8H4AXTP8glghBwbHVnupI4MOMNA4IQZHN0crqSXwbjDQUGAHgB+gD0BDD4J28iMFAKoSG+8uBQghBwbHVngx6xcIAYUATLBSbPFlj6Ahn0AMtpF8sfUmDLPyDJgED7AAYAilAEgQEI9Fkw7UTQgQFA1yDIAc8W9ADJ7VQBcrCOI4IQZHN0coMesXCAGFAFywVQA88WI/oCE8tqyx/LP8mAQPsAkl8D4gIBIAgPAgEgCQ4CAVgKCwA9sp37UTQgQFA1yH0BDACyMoHy//J0AGBAQj0Cm+hMYAIBIAwNABmtznaiaEAga5Drhf/AABmvHfaiaEAQa5DrhY/AABG4yX7UTQ1wsfgAWb0kK29qJoQICga5D6AhhHDUCAhHpJN9KZEM5pA+n/mDeBKAG3gQFImHFZ8xhAT48oMI1xgg0x/TH9MfAvgju/Jk7UTQ0x/TH9P/9ATRUUO68qFRUbryogX5AVQQZPkQ8qP4ACSkyMsfUkDLH1Iwy/9SEPQAye1U+A8B0wchwACfbFGTINdKltMH1AL7AOgw4CHAAeMAIcAC4wABwAORMOMNA6TIyx8Syx/L/xESExQAbtIH+gDU1CL5AAXIygcVy//J0Hd0gBjIywXLAiLPFlAF+gIUy2sSzMzJc/sAyEAUgQEI9FHypwIAcIEBCNcY+gDTP8hUIEeBAQj0UfKnghBub3RlcHSAGMjLBcsCUAbPFlAE+gIUy2oSyx/LP8lz+wACAGyBAQjXGPoA0z8wUiSBAQj0WfKnghBkc3RycHSAGMjLBcsCUAXPFlAD+gITy2rLHxLLP8lz+wAACvQAye1UAFEAAAAAKamjFyM60x2mt5eboNyOTE+5RGOe9Ee2rK1Qcb+0ZuiP9vb7QJRlz/c="
  },
  "connectItems": {
    "tonProof": {
      "name": "ton_proof",
      "proof": {
        "timestamp": 1674392728,
        "domain": {
          "lengthBytes": 28,
          "value": "ratingers.pythonanywhere.com"
        },
        "signature": "trCkHit07NZUayjGLxJa6FoPnaGHkqPy2JyNjlUbxzcc3aGvsExCmHXi6XJGuoCu6M2RMXiLzIftEm6PAoy1BQ==",
        "payload": "doc-example-<BACKEND_AUTH_ID>"
      }
    }
  }
}
```

بیایید امضای دریافت شده را تأیید کنیم. برای انجام این کار، تأیید امضا از پایتون استفاده می‌کند زیرا می‌تواند به راحتی با بک‌اند تعامل کند. کتابخانه‌های موردنیاز برای انجام این فرایند `pytoniq` و `pynacl` هستند.

بعد، لازم است که کلید عمومی کیف پول را بازیابی کنیم. برای انجام این کار، از `tonapi.io` یا خدمات مشابه استفاده نمی‌شود زیرا به نتیجه نهایی نمی‌توان به طور قابل اعتماد اعتماد کرد. در عوض، این کار با تجزیه `walletStateInit` انجام می‌شود.

همچنین بسیار مهم است که اطمینان حاصل شود که `address` و `walletStateInit` مطابقت دارند، وگرنه payload می‌تواند با کلید کیف پول خود در فیلد `stateInit` امضا شود و کیف پول دیگری در فیلد `address` ارائه شود.

`StateInit` از دو نوع مرجع تشکیل شده است: یکی برای کد و یکی برای داده‌ها. در این زمینه، هدف بازیابی کلید عمومی است بنابراین مرجع دوم (مرجع داده) بارگذاری می‌شود. سپس ۸ بایت رد می‌شود (۴ بایت برای فیلد `seqno` و ۴ برای `subwallet_id` در همه قراردادهای کیف پول مدرن) و ۳۲ بایت بعدی (۲۵۶ بیت) بارگذاری می‌شود -- کلید عمومی.

```python
import nacl.signing
import pytoniq

import hashlib
import base64

received_state_init = 'te6cckECFgEAAwQAAgE0ARUBFP8A9KQT9LzyyAsCAgEgAxACAUgEBwLm0AHQ0wMhcbCSXwTgItdJwSCSXwTgAtMfIYIQcGx1Z70ighBkc3RyvbCSXwXgA/pAMCD6RAHIygfL/8nQ7UTQgQFA1yH0BDBcgQEI9ApvoTGzkl8H4AXTP8glghBwbHVnupI4MOMNA4IQZHN0crqSXwbjDQUGAHgB+gD0BDD4J28iMFAKoSG+8uBQghBwbHVngx6xcIAYUATLBSbPFlj6Ahn0AMtpF8sfUmDLPyDJgED7AAYAilAEgQEI9Fkw7UTQgQFA1yDIAc8W9ADJ7VQBcrCOI4IQZHN0coMesXCAGFAFywVQA88WI/oCE8tqyx/LP8mAQPsAkl8D4gIBIAgPAgEgCQ4CAVgKCwA9sp37UTQgQFA1yH0BDACyMoHy//J0AGBAQj0Cm+hMYAIBIAwNABmtznaiaEAga5Drhf/AABmvHfaiaEAQa5DrhY/AABG4yX7UTQ1wsfgAWb0kK29qJoQICga5D6AhhHDUCAhHpJN9KZEM5pA+n/mDeBKAG3gQFImHFZ8xhAT48oMI1xgg0x/TH9MfAvgju/Jk7UTQ0x/TH9P/9ATRUUO68qFRUbryogX5AVQQZPkQ8qP4ACSkyMsfUkDLH1Iwy/9SEPQAye1U+A8B0wchwACfbFGTINdKltMH1AL7AOgw4CHAAeMAIcAC4wABwAORMOMNA6TIyx8Syx/L/xESExQAbtIH+gDU1CL5AAXIygcVy//J0Hd0gBjIywXLAiLPFlAF+gIUy2sSzMzJc/sAyEAUgQEI9FHypwIAcIEBCNcY+gDTP8hUIEeBAQj0UfKnghBub3RlcHSAGMjLBcsCUAbPFlAE+gIUy2oSyx/LP8lz+wACAGyBAQjXGPoA0z8wUiSBAQj0WfKnghBkc3RycHSAGMjLBcsCUAXPFlAD+gITy2rLHxLLP8lz+wAACvQAye1UAFEAAAAAKamjFyM60x2mt5eboNyOTE+5RGOe9Ee2rK1Qcb+0ZuiP9vb7QJRlz/c='
received_address = '0:b2a1ecf5545e076cd36ae516ea7ebdf32aea008caa2b84af9866becb208895ad'

state_init = pytoniq.Cell.one_from_boc(base64.b64decode(received_state_init))

address_hash_part = state_init.hash.hex()
assert received_address.endswith(address_hash_part)

public_key = state_init.refs[1].bits.tobytes()[8:][:32]

# bytearray(b'#:\xd3\x1d\xa6\xb7\x97\x9b\xa0\xdc\x8eLO\xb9Dc\x9e\xf4G\xb6\xac\xadPq\xbf\xb4f\xe8\x8f\xf6\xf6\xfb')

verify_key = nacl.signing.VerifyKey(bytes(public_key))
```

پس از اجرای کد توالی بالا، با مستندات صحیح مشورت می‌شود تا بررسی شود که کدام پارامترها با استفاده از کلید کیف پول تایید و امضا شده‌اند:

> ```
> message = utf8_encode("ton-proof-item-v2/") ++  
>           Address ++  
>           AppDomain ++  
>           Timestamp ++  
>           Payload
>
> signature = Ed25519Sign(
>   privkey,
>   sha256(0xffff ++ utf8_encode("ton-connect") ++ sha256(message))
> )
> ```

> از این رو:
>
> - `Address` بیانگر آدرس کیف پول به صورت کدگذاری‌شده به عنوان یک دنباله است:
>   - `workchain`: ۳۲ بیتی دارای علامت به صورت big endian؛
>   - `hash`: ۲۵۶ بیتی بدون علامت به صورت big endian؛
> - `AppDomain` طول ++ EncodedDomainName است
>   - `Length` از یک مقدار ۳۲ بیتی استفاده می‌کند که طول نام دامنه اپلیکیشن utf-8 کدگذاری شده را به بایت نشان می‌دهد
>   - `EncodedDomainName` شناسه `Length`-بایت utf-8 نام دامنه اپلیکیشن کدگذاری شده‌ است
> - `Timestamp` نشانه ۶۴ بیتی زمان دوره یونیکس عملیات امضا است
> - `Payload` بیانگر یک رشته باینری با طول متغیر است
> - `utf8_encode` یک رشته بایت ساده بدون پیشوند طول تولید می‌کند.

بیایید این را در پایتون بازپیاده‌سازی کنیم. اندازه‌اندی برخی از اعداد صحیح بالا مشخص نشده است، بنابراین باید چندین مثال در نظر گرفته شود. لطفاً به پیاده‌سازی tonkeeper زیر مراجعه کنید که مثال‌های مرتبط را شرح می‌دهد: : [ConnectReplyBuilder.ts](https://github.com/tonkeeper/wallet/blob/77992c08c663dceb63ca6a8e918a2150c75cca3a/src/tonconnect/ConnectReplyBuilder.ts#L42).

```python
received_timestamp = 1674392728
signature = 'trCkHit07NZUayjGLxJa6FoPnaGHkqPy2JyNjlUbxzcc3aGvsExCmHXi6XJGuoCu6M2RMXiLzIftEm6PAoy1BQ=='

message = (b'ton-proof-item-v2/'
         + 0 .to_bytes(4, 'big') + si.bytes_hash()
         + 28 .to_bytes(4, 'little') + b'ratingers.pythonanywhere.com'
         + received_timestamp.to_bytes(8, 'little')
         + b'doc-example-<BACKEND_AUTH_ID>')
# b'ton-proof-item-v2/\x00\x00\x00\x00\xb2\xa1\xec\xf5T^\x07l\xd3j\xe5\x16\xea~\xbd\xf3*\xea\x00\x8c\xaa+\x84\xaf\x98f\xbe\xcb \x88\x95\xad\x1c\x00\x00\x00ratingers.pythonanywhere.com\x984\xcdc\x00\x00\x00\x00doc-example-<BACKEND_AUTH_ID>'

signed = b'\xFF\xFF' + b'ton-connect' + hashlib.sha256(message).digest()
# b'\xff\xffton-connectK\x90\r\xae\xf6\xb0 \xaa\xa9\xbd\xd1\xaa\x96\x8b\x1fp\xa9e\xff\xdf\x81\x02\x98\xb0)E\t\xf6\xc0\xdc\xfdx'

verify_key.verify(hashlib.sha256(signed).digest(), base64.b64decode(signature))
# b'\x0eT\xd6\xb5\xd5\xe8HvH\x0b\x10\xdc\x8d\xfc\xd3#n\x93\xa8\xe9\xb9\x00\xaaH%\xb5O\xac:\xbd\xcaM'
```

پس از پیاده‌سازی پارامترهای فوق، اگر یک مهاجم تلاش کند که به‌جای کاربر جا زده شود و امضای معتبری ارائه ندهد، خطای زیر نمایش داده می‌شود:

```bash
nacl.exceptions.BadSignatureError: Signature was forged or corrupt.
```

## See also

- [Preparing Messages](/v3/guidelines/ton-connect/guidelines/preparing-messages)
- [Sending Messages](/v3/guidelines/ton-connect/guidelines/sending-messages)

## مراحل بعدی

هنگام نوشتن یک dApp، باید موارد زیر نیز در نظر گرفته شود:

- پس از تکمیل اتصال موفق (چه اتصال بازیابی شده یا جدید باشد)، باید به جای چندین دکمه `Connect`، دکمه `Disconnect` نمایش داده شود
- پس از قطع ارتباط یک کاربر، نیاز به بازسازی دکمه‌های `Disconnect` است
- کد کیف پول باید بررسی شود، زیرا
  - نسخه‌های جدیدتر کیف پول ممکن است کلیدهای عمومی را در مکان متفاوتی قرار دهند و مشکلاتی ایجاد کنند
  - کاربر فعلی ممکن است به جای کیف پول با استفاده از نوع دیگری از قرارداد وارد شود. خوشبختانه، این شامل کلید عمومی در مکان مورد انتظار خواهد بود

موفق باشید و از نوشتن dApps لذت ببرید!

<Feedback />

