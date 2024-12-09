# TON DNS و دامنه‌ها

TON DNS یک سرویس برای ترجمه نام‌های دامنه قابل خواندن برای انسان (مانند `test.ton` یا `mysite.temp.ton`) به آدرس‌های قرارداد هوشمند TON، آدرس‌های ADNL استفاده شده توسط سرویس‌های اجرایی در شبکه TON (مانند سایت‌های TON) و غیره است.

## استاندارد

[استاندارد TON DNS](https://github.com/ton-blockchain/TIPs/issues/81) قالب نام‌های دامنه، فرآیند تفسیر یک دامنه، نمایه قراردادهای هوشمند DNS و قالب رکوردهای DNS را توصیف می‌کند.

## SDK

کار با TON DNS در SDK جاوااسکریپت [TonWeb](https://github.com/toncenter/tonweb) و [TonLib](https://ton.org/#/apis/?id=_2-ton-api) پیاده‌سازی شده است.

```js
const address: Address = await tonweb.dns.getWalletAddress('test.ton');

// or 

const address: Address = await tonweb.dns.resolve('test.ton', TonWeb.dns.DNS_CATEGORY_WALLET);
```

همچنین `lite-client` و `tonlib-cli` توسط درخواست‌های DNS پشتیبانی می‌شود.

## دامنه سطح اول

در حال حاضر، تنها دامنه‌هایی که با `.ton` به پایان می‌رسند به عنوان دامنه‌های معتبر TON DNS شناسایی می‌شوند.

سورس کد قرارداد هوشمند ریشه DNS - https://github.com/ton-blockchain/dns-contract/blob/main/func/root-dns.fc.

این ممکن است در آینده تغییر کند. افزودن یک دامنه سطح اول جدید نیاز به قرارداد هوشمند ریشه جدید و رأی‌گیری عمومی برای تغییر [پیکربندی شبکه #۴](https://ton.org/#/smart-contracts/governance?id=config) دارد.

## دامنه‌های \*.ton

دامنه‌های \*.ton به صورت یک NFT پیاده‌سازی شده‌اند. از آنجا که آن‌ها استاندارد NFT را پیاده‌سازی می‌کنند، با خدمات NFT معمول (مانند بازارهای NFT) و کیف پول‌هایی که قادر به نمایش NFT هستند، سازگارند.

سورس کد دامنه‌های \*.ton - https://github.com/ton-blockchain/dns-contract.

مفسر دامنه‌ها یک نمایه کلکسیون NFT و دامنه .ton یک نمایه آیتم NFT را پیاده‌سازی می‌کنند.

فروش اولیه دامنه‌های \*.ton از طریق یک مزایده باز غیرمتمرکز در https://dns.ton.org انجام می‌شود. سورس کد - https://github.com/ton-blockchain/dns.

## زیر دامنه‌ها

مالک دامنه می‌تواند زیر دامنه‌هایی را با تنظیم آدرس قرارداد هوشمند مسئول برای تفسیر زیر دامنه‌ها در رکورد سرویس نام دامنه `sha256("dns_next_resolver")` بسازد.

این می‌تواند هر قرارداد هوشمندی باشد که استاندارد DNS را پیاده‌سازی می‌کند.
