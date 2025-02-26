import Button from '@site/src/components/button'
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# مروری بر پردازش دارایی‌ها

اینجا می‌توانید **یک مرور کوتاه** درباره [نحوه عملکرد انتقال‌های TON](/v3/documentation/dapps/assets/overview#overview-on-messages-and-transactions) بیابید، چه [انواع دارایی](/v3/documentation/dapps/assets/overview#digital-asset-types-on-ton) را می‌توانید در TON پیدا کنید (و در مورد چه چیزی در [بخش بعدی](/v3/documentation/dapps/assets/overview#read-next) خواهید خواند) و چطور با استفاده از زبان برنامه‌نویسی خود با TON [تعامل کنید](/v3/documentation/dapps/assets/overview#interaction-with-ton-blockchain)، توصیه می‌شود تمامی اطلاعاتی که در زیر آمده است را قبل از رفتن به صفحات بعدی درک کنید.

## مروری بر پیام‌ها و تراکنش‌ها

به کارگیری یک رویکرد کاملاً غیرهمزمان، بلاکچین TON شامل چندین مفهوم است که برای بلاکچین‌های سنتی غیرمعمول هستند. به‌ویژه، هر تعامل از هر بازیگر با بلاکچین شامل یک نمودار از [پیام‌های](/v3/documentation/smart-contracts/message-management/messages-and-transactions) منتقل شده به‌صورت غیرهمزمان بین قراردادهای هوشمند و/یا دنیای خارجی است. هر تراکنش شامل یک پیام ورودی و حداکثر ۲۵۵ پیام خروجی است.

۳ نوع پیام وجود دارد که به طور کامل [در اینجا](/v3/documentation/smart-contracts/message-management/sending-messages#types-of-messages) توصیف شده‌اند. به طور خلاصه:

- [پیام خارجی](/v3/documentation/smart-contracts/message-management/external-messages):
  - `external in message` (که گاهی به سادگی `external message` نیز خوانده می‌شود) پیامی است که از *خارج* از بلاکچین به یک قرارداد هوشمند *درون* بلاکچین ارسال می‌شود.
  - `external out message` (که معمولاً به `logs message` معروف است) از یک *نهاد بلاکچین* به *دنیای بیرونی* ارسال می‌شود.
- [پیام داخلی](/v3/documentation/smart-contracts/message-management/internal-messages) از یک *نهاد بلاکچین* به *نهاد دیگر* ارسال می‌شود و می‌تواند مقداری دارایی دیجیتال و بخشی دلخواه از داده‌ها را به همراه داشته باشد.

مسیر معمول هر تعامل با ارسال یک پیام خارجی به یک قرارداد هوشمند `wallet` شروع می‌شود، که فرستنده پیام را با استفاده از رمزنگاری کلید عمومی احراز هویت می‌کند، مسئولیت پرداخت هزینه را بر عهده می‌گیرد و پیام‌های داخلی بلاکچین را ارسال می‌کند. این صف پیام‌ها یک نمودار جهت‌دار غیرمدور، یا یک درخت را تشکیل می‌دهند.

برای مثال:

![](/img/docs/asset-processing/alicemsgDAG.svg)

- `Alice` برای ارسال یک `external message` به کیف پول خود از [Tonkeeper](https://tonkeeper.com/) استفاده می‌کند.
- `external message` ورودی قرارداد `wallet A v4` است با مبدا خالی (یک پیام از هیچ جا، مانند [Tonkeeper](https://tonkeeper.com/)).
- `outgoing message`، پیام خروجی برای قرارداد `wallet A v4` و پیام ورودی برای قرارداد `wallet B v4` با مبدا `wallet A v4` و مقصد `wallet B v4` است.

در نتیجه، ۲ تراکنش با مجموعه‌ای از پیام‌های ورودی و خروجی وجود دارد.

هر عمل که در آن، قرارداد پیام را به عنوان ورودی می‌گیرد (توسط آن تحریک می‌شود)، آن را پردازش نموده و پیام‌های خروجی تولید کند یا نکند، به عنوان `transaction` شناخته می‌شود. درباره تراکنش‌ها [اینجا](/v3/documentation/smart-contracts/message-management/messages-and-transactions#what-is-a-transaction) بیشتر بخوانید.

این `transactions` می‌توانند دوره **طولانی مدتی** را پوشش دهند. از نظر فنی، تراکنش‌ها با صف‌های پیام به بلوک‌هایی که توسط تاییدکنندگان پردازش می‌شوند تجمیع می‌شوند. ماهیت ناهمزمان بلاکچین TON **اجازه پیش‌بینی هش و زمان منطقی (lt) یک تراکنش** را در مرحله ارسال پیام نمی‌دهد.

`transaction` پذیرفته شده در بلوک نهایی است و قابل تغییر نیست.

:::info تاییدیه تراکنش
تراکنش‌های TON پس از تنها یک تأیید غیرقابل بازگشت هستند. برای بهترین تجربه کاربری، پیشنهاد می‌شود پس از اتمام تراکنش‌ها بر روی بلاکچین TON منتظر بلوک‌های اضافی نمانید. برای اطلاعات بیشتر به [Catchain.pdf](https://docs.ton.org/catchain.pdf#page=3) مراجعه کنید.
:::

قراردادهای هوشمند برای تراکنش‌ها چند نوع [هزینه](/v3/documentation/smart-contracts/transaction-fees/fees) می‌پردازند (معمولاً از موجودی پیام دریافتی، طرز کار بستگی به [حالت پیام](/v3/documentation/smart-contracts/message-management/sending-messages#message-modes) دارد). میزان هزینه‌ها بستگی به پیکربندی‌های زنجیره‌کار دارد با حداکثر هزینه‌ها در `masterchain` و هزینه‌های بسیار کمتر در `basechain`.

## انواع دارایی‌های دیجیتال در TON

TON دارای سه نوع دارایی دیجیتال است.

- Toncoin، توکن اصلی شبکه است. این توکن برای تمام عملیات پایه‌ای در بلاکچین استفاده می‌شود، مانند پرداخت هزینه‌های گس یا استیکینگ برای تأیید.
- دارایی‌های قراردادی، مانند توکن‌ها و NFTها، که مشابه استانداردهای ERC-20/ERC-721 هستند و توسط قراردادهای دلخواه مدیریت می‌شوند و بنابراین ممکن است به قوانین سفارشی برای پردازش نیاز داشته باشند. شما می‌توانید اطلاعات بیشتری درباره پردازش آنها در مقالات [پردازش NFTها](/v3/guidelines/dapps/asset-processing/nft-processing/nfts) و [پردازش Jettonها](/v3/guidelines/dapps/asset-processing/jettons) پیدا کنید.
- توکن بومی، که یک نوع خاص از دارایی است که می‌تواند به هر پیامی در شبکه پیوست شود. اما این دارایی‌ها در حال حاضر استفاده نمی‌شوند زیرا قابلیت صدور توکن‌های جدید بومی غیر فعال است.

## تعامل با بلاکچین TON

عملیات پایه در بلاکچین TON می‌توانند از طریق TonLib انجام شوند. این یک کتابخانه مشترک است که می‌تواند همراه با یک نود TON کامپایل شده و API ها را برای تعامل با بلاکچین از طریق به اصطلاح سرورهای لایت (سرورها برای کلاینت‌های لایت) آشکار می‌کند. TonLib از رویکرد بدون اعتماد پیروی می‌کند با بررسی مدارک برای همه داده‌های ورودی؛ بنابراین، نیازی به تامین‌کننده داده‌های معتبر نیست. روش‌های موجود در TonLib [در الگو TL](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L234) لیست شده‌اند. آنها می‌توانند به عنوان یک کتابخانه مشترک از طریق [پوشش‌دهنده‌ها](/v3/guidelines/dapps/asset-processing/payments-processing/#sdks) استفاده شوند.

## ادامه مطلب

پس از خواندن این مقاله، می‌توانید بررسی کنید:

1. [پردازش پرداخت‌ها](/v3/guidelines/dapps/asset-processing/payments-processing) برای آشنایی با نحوه کار با `تونکوین‌ها`
2. [پردازش Jettonها](/v3/guidelines/dapps/asset-processing/jettons) برای آشنایی با نحوه کار با `Jetton` (گاهی اوقات به آنها `tokens` گفته می‌شود)
3. [پردازش NFTها](/v3/guidelines/dapps/asset-processing/nft-processing/nfts) برای آشنایی با نحوه کار با `NFT` (که نوع خاصی از `jetton` است)
