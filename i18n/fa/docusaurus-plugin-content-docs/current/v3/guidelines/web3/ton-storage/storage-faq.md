# راهنمای پرسش‌های متداول TON Storage

## چگونه یک دامنه TON را به یک مجموعه از فایل‌های TON Storage اختصاص دهیم

1. [بارگذاری](/v3/guidelines/web3/ton-storage/storage-daemon#creating-a-bag-of-files) کیف فایل‌ها به شبکه و دریافت شناسه کیف

2. مرورگر Google Chrome را روی کامپیوتر خود باز کنید.

3. [افزونه TON](https://chrome.google.com/webstore/detail/ton-wallet/nphplpgoakhhjchkkhmiggakijnkhfnd) را برای Google Chrome نصب کنید.
   همچنین می‌توانید از [MyTonWallet](https://chrome.google.com/webstore/detail/mytonwallet/fldfpgipfncgndfolcbkdeeknbbbnhcc) استفاده کنید.

4. افزونه را باز کنید، "Import wallet" را کلیک کنید و با استفاده از عبارت بازیابی، کیف پول که مالک دامنه است را وارد کنید.

5. حالا دامنه خود را در https://dns.ton.org باز کنید و "Edit" را کلیک کنید.

6. شناسه کیف خود را به فیلد "Storage" کپی کنید و "Save" را کلیک کنید.

## چگونه یک سایت استاتیک TON را در TON Storage میزبانی کنیم

1. [ایجاد کنید](/v3/guidelines/web3/ton-storage/storage-daemon#creating-a-bag-of-files) کیف از پوشه با فایل‌های وب‌سایت، به شبکه بارگذاری کنید و شناسه کیف را دریافت کنید. پوشه باید شامل فایل `index.html` باشد.

2. مرورگر Google Chrome را روی کامپیوتر خود باز کنید.

3. [افزونه TON](https://chrome.google.com/webstore/detail/ton-wallet/nphplpgoakhhjchkkhmiggakijnkhfnd) را برای Google Chrome نصب کنید.
   همچنین می‌توانید از [MyTonWallet](https://chrome.google.com/webstore/detail/mytonwallet/fldfpgipfncgndfolcbkdeeknbbbnhcc) استفاده کنید.

4. افزونه را باز کنید، "Import wallet" را کلیک کنید و با استفاده از عبارت بازیابی، کیف پول که مالک دامنه است را وارد کنید.

5. حالا دامنه خود را در https://dns.ton.org باز کنید و "Edit" را کلیک کنید.

6. شناسه کیف خود را به فیلد "Site" کپی کنید، چک‌باکس "Host in TON Storage" را انتخاب کنید و "Save" را کلیک کنید.

## چگونه محتوای TON NFT را به TON Storage انتقال دهیم

اگر از [قرارداد هوشمند استاندارد NFT](https://github.com/ton-blockchain/token-contract/blob/main/nft/nft-collection-editable.fc) برای کلکسیون خود استفاده کرده‌اید، باید یک [پیام](https://github.com/ton-blockchain/token-contract/blob/2d411595a4f25fba43997a2e140a203c140c728a/nft/nft-collection-editable.fc#L132) از کیف پول مالک کلکسیون با پیش‌شوند URL جدید به قرارداد هوشمند کلکسیون ارسال کنید.

به عنوان مثال، اگر پیشوند URL قبلاً `https://mysite/my_collection/` بود، پیشوند جدید `tonstorage://my_bag_id/` خواهد بود.

## چگونه یک دامنه TON را به یک کیف‌فایل TON Storage اختصاص دهیم (سطح پایین)

شما باید مقدار زیر را به رکورد sha256("storage") دامنه TON خود اختصاص دهید:

```
dns_storage_address#7473 bag_id:uint256 = DNSRecord;
```

## چگونه یک سایت استاتیک TON را در TON Storage میزبانی کنیم (سطح پایین)

یگ کیف از پوشه فایل‌های وب‌سایت [ایجاد کنید](/v3/guidelines/web3/ton-storage/storage-daemon#creating-a-bag-of-files)، در شبکه بارگذاری کنید و شناسه کیف را دریافت کنید. پوشه باید شامل فایل `index.html` باشد.

شما باید مقدار زیر را به رکورد sha256("site") دامنه TON خود اختصاص دهید:

```
dns_storage_address#7473 bag_id:uint256 = DNSRecord;
```

