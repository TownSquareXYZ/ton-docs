# انواع API

**APIهای بلاکچین با دسترسی بالا عنصر اصلی توسعه امن، راحت و سریع برنامه‌های کاربردی مفید بر روی TON هستند.**

- [TON HTTP API](/v3/guidelines/dapps/apis-sdks/ton-http-apis) — API که اجازه کار با *اطلاعات ایندکس شده بلاک‌چین* را می‌دهد.
- [TON ADNL API](/v3/guidelines/dapps/apis-sdks/ton-adnl-apis) — یک API امن برای ارتباط با TON، بر اساس پروتکل ADNL.

## APIهای Toncenter

- [TON Index](https://toncenter.com/api/v3/) - TON Index داده‌ها را از یک Full Node به پایگاه‌داده PostgreSQL جمع‌آوری می‌کند و API مناسبی را برای یک بلاک‌چین ایندکس شده فراهم می‌کند.
- [toncenter/v2](https://toncenter.com/) - این API دسترسی HTTP به بلاک‌چین TON را فراهم می‌کند، اطلاعات حساب‌ها و Wallet‌ها را دریافت می‌کند، بلوک‌ها و تراکنش‌ها را جستجو می‌کند، پیام‌ها را به بلاک‌چین ارسال می‌کند، متدهای get قراردادهای هوشمند را فراخوانی می‌کند و بیشتر.

## APIهای شخص ثالث

- [tonapi.io](https://docs.tonconsole.com/tonapi) - API سریع ایندکس شده که داده‌های پایه‌ی مربوط به حساب‌ها، تراکنش‌ها، بلاک‌ها و داده‌های خاص نرم‌افزار مربوط به NFT، حراج‌ها، Jettonها، TON DNS و اشتراک‌ها را فراهم می‌کند. همچنین داده‌های توضیح‌دار مربوط به زنجیره‌های تراکنش را ارائه می‌دهد.
- [TONX API](https://docs.tonxapi.com/) - یک API است که به‌طور خاص برای توسعه بی‌درنگ DApp طراحی شده است، دسترسی آسان به مجموعه‌ای گوناگون از ابزارها و داده‌ها را ممکن می‌سازد.
- [dton.io](https://dton.io/graphql/) - GraphQL API که می‌تواند داده‌هایی در مورد حساب‌ها، تراکنش‌ها و بلوک‌ها، و همچنین داده‌های خاص نرم‌افزار در مورد NFT، حراج‌ها، Jettonها و TON DNS ارائه دهد.
- [ton-api-v4](https://mainnet-v4.tonhubapi.com) - یک لایت API دیگر که بر سرعت تمرکز دارد از طریق کشینگ تهاجمی در CDN.
- [docs.nftscan.com](https://docs.nftscan.com/reference/ton/model/asset-model) - APIهای NFT برای بلاک‌چین TON.
- [everspace.center](https://everspace.center/toncoin) - API ساده RPC برای دسترسی به بلاک‌چین TON.

## APIهای اضافی

### APIهای نرخ Toncoin

- https://docs.tonconsole.com/tonapi/rest-api/rates
- https://coinmarketcap.com/api/documentation/v1/
- https://apiguide.coingecko.com/getting-started

### APIهای تبدیل آدرس

:::info
ترجیح داده می‌شود آدرس را از طریق الگوریتم محلی تبدیل کنید، برای مطالعه بیشتر به بخش [Addresses](/v3/documentation/smart-contracts/addresses) مستندات مراجعه کنید.
:::

#### از شکل دوستانه به شکل خام

/api/v2/unpackAddress

Curl

```curl
curl -X 'GET' \
'https://toncenter.com/api/v2/unpackAddress?address=EQApAj3rEnJJSxEjEHVKrH3QZgto_MQMOmk8l72azaXlY1zB' \
-H 'accept: application/json'
```

متن پاسخ

```curl
{
"ok": true,
"result": "0:29023deb1272494b112310754aac7dd0660b68fcc40c3a693c97bd9acda5e563"
}
```

#### از شکل دوستانه به شکل خام

/api/v2/packAddress

Curl

```curl
curl -X 'GET' \
'https://toncenter.com/api/v2/packAddress?address=0%3A29023deb1272494b112310754aac7dd0660b68fcc40c3a693c97bd9acda5e563' \
-H 'accept: application/json'
```

متن پاسخ

```json
{
  "ok": true,
  "result": "EQApAj3rEnJJSxEjEHVKrH3QZgto/MQMOmk8l72azaXlY1zB"
}
```

## همچنین ببینید

- [TON HTTP API](/v3/guidelines/dapps/apis-sdks/ton-http-apis)
- [فهرست SDKها](/v3/guidelines/dapps/apis-sdks/sdk)
- [کتاب آشپزی TON](/v3/guidelines/dapps/cookbook)
