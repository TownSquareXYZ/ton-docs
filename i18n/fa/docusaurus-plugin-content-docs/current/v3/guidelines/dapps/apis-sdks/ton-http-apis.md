# APIهای TON مبتنی بر HTTP

:::tip

راه‌های مختلفی برای اتصال به بلاک‌چین وجود دارد:

1. **ارائه‌دهنده داده RPC یا API دیگر**: در بیشتر مواقع، باید بر ثبات و امنیت آن تکیه کنید.
2. اتصال ADNL: شما در حال اتصال به یک [لایت‌سرور](/v3/guidelines/nodes/running-nodes/liteserver-node) هستید. ممکن است در دسترس نباشد، اما با یک سطح خاص از تایید (که در کتابخانه پیاده‌سازی شده است) نمی‌تواند دروغ بگوید.
3. باینری Tonlib: شما همچنین به لایت‌سرور متصل می‌شوید، بنابراین تمامی مزایا و معایب آن اعمال می‌شود، اما برنامه شما همچنین شامل یک کتابخانه با بارگذاری پویا است که در خارج کامپایل شده است.
4. فقط آف‌چین. این‌گونه SDKها اجازه می‌دهند تا سلول‌ها را ایجاد و سریالیز کنید که می‌توانید آنها را به API ارسال کنید.

:::

## مزایا و معایب

- ✅ عادی و مناسب برای شروع سریع، این برای هر تازه‌کاری که به دنبال بازی با TON است عالی است.

- ✅ وب‌محور. برای بارگذاری داده‌ها از قراردادهای هوشمند TON از طریق وب عالی است و همچنین امکان ارسال پیام‌ها را فراهم می‌کند.

- ❌ ساده‌شده. نمی‌توان اطلاعاتی که نیاز به API ایندکس شده TON دارند را دریافت کرد.

- ❌ واسط میانی HTTP. شما نمی‌توانید به طور کامل به پاسخ‌های سرور اعتماد کنید مگر اینکه سرور داده‌های بلاک‌چین را با [اثبات‌های مرکل](/v3/documentation/data-formats/tlb/proofs) برای تأیید اصالت آن تقویت کند.

## مانیتورینگ

- [status.toncenter](https://status.toncenter.com/) - همه گره‌های شبکه کامل و اعتبارسنج‌ها را در ساعات اخیر، همراه با آمارهای مختلف نمایش می‌دهد.
- [Tonstat.us](https://tonstat.us/) - داشبوردی بر اساس Grafana ارائه می‌دهد که وضعیت همه APIهای مرتبط با TON را در زمان واقعی، با به‌روزرسانی داده‌ها هر ۵ دقیقه نمایش می‌دهد.

## گره‌های RPC

- [QuickNode](https://www.quicknode.com/chains/ton?utm_source=ton-docs) - ارائه‌دهنده پیشرو نودهای بلاکچین که با مسیریابی هوشمند DNS سریع‌ترین دسترسی را برای پوشش جهانی بهینه‌شده و مقیاس‌پذیری با توازن بار فراهم می‌کند.
- [Chainstack](https://chainstack.com/build-better-with-ton/) — نودهای RPC و ایندکسر در چندین منطقه با توزیع جغرافیایی و توازن بار.
- [Tatum](https://docs.tatum.io/reference/rpc-ton) — در یک پلتفرم ساده و آسان برای استفاده، به گره‌های TON RPC و ابزارهای پیشرفته توسعه‌دهنده دسترسی پیدا کنید.
- [گره‌های GetBlock](https://getblock.io/nodes/ton/) — با استفاده از گره‌های GetBlocks می‌توانید dAppهای خود را متصل و تست کنید
- [TON Access](https://www.orbs.com/ton-access/) - یک HTTP API برای شبکه باز (TON).
- [Toncenter](https://toncenter.com/api/v2/) — پروژه‌ای که توسط جامعه برای شروع سریع با API میزبانی می‌شود. (کلید API خود را دریافت کنید [@tonapibot](https://t.me/tonapibot))
- [ton-node-docker](https://github.com/fmira21/ton-node-docker) - نود کامل Docker و Toncenter AP.
- [toncenter/ton-http-api](https://github.com/toncenter/ton-http-api) — نود RPC خود را اجرا کنید.
- [nownodes.io](https://nownodes.io/nodes) — نودهای کامل NOWNodes و اکسپلوررهای blockbook از طریق API.
- [Chainbase](https://chainbase.com/chainNetwork/TON) — API نود و زیرساخت داده برای شبکه باز.

## ایندکسر

### ایندکسر Toncenter برای TON

ایندکسرها، نه فقط بازیابی موارد خاص، امکان لیست کردن کیف‌های Jettonها، NFTها و تراکنش‌ها بر اساس فیلترهای خاص را فراهم می‌کنند.

- می‌توان از TON Index عمومی استفاده کرد: تست‌ها و توسعه رایگان هستند، [پریمیوم](https://t.me/tonapibot) برای تولید - [toncenter.com/api/v3/](https://toncenter.com/api/v3/).
- TON Index خود را با استفاده از [ورکر](https://github.com/toncenter/ton-index-worker/tree/36134e7376986c5517ee65e6a1ddd54b1c76cdba) و [TON Index API wrapper](https://github.com/toncenter/ton-indexer) اجرا کنید.

### Anton

Anton که به زبان Go نوشته شده است، یک ایندکسر بلاکچین The Open Network با منبع باز است که تحت مجوز Apache License ۲٫۰ در دسترس است. Anton طراحی شده است تا یک راه‌حل قابل گسترش و انعطاف‌پذیر برای توسعه‌دهندگان فراهم کند تا به داده‌های بلاکچین دسترسی پیدا کنند و آنها را تحلیل کنند. هدف ما کمک به توسعه‌دهندگان و کاربران برای درک چگونگی استفاده از بلاکچین و ایجاد امکان برای توسعه‌دهندگان برای افزودن قراردادهای خود با الگوهای پیام سفارشی به اکسپلورر ما است.

- [پروژه GitHub](https://github.com/tonindexer/anton) - برای اجرای ایندکسر خود
- [مستندات Swagger API](https://github.com/tonindexer/anton), [نمونه‌های API Query](https://github.com/tonindexer/anton/blob/main/docs/API.md) - برای استفاده، مستندات و مثال‌ها را مطالعه کنید
- [Apache Superset](https://github.com/tonindexer/anton) - برای مشاهده داده‌ها استفاده کنید

### گره‌های GraphQL

گره‌های GraphQL همچنین به عنوان ایندکسر عمل می‌کنند.

- [dton.io](https://dton.io/graphql) - علاوه بر ارائه داده‌های قرارداد با پرچم‌های مجزا "is jetton" و "is NFT"، تراکنش‌ها را شبیه‌سازی کرده و ردیابی‌های اجرا را دریافت می‌کند.

## APIهای دیگر

- [TonAPI](https://docs.tonconsole.com/tonapi) - API که برای ارائه تجربه‌ای ساده شده برای کاربران طراحی شده است، بدون آنکه نگران جزئیات سطح پایین قراردادهای هوشمند باشند.
