import Button from '@site/src/components/button'
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# پردازش پرداخت‌ها

این صفحه **نحوه پردازش** (ارسال و پذیرش) `digital assets` در بلاکچین TON را توضیح می‌دهد. این عمدتاً نحوه کار با `تونکوین‌ها` را توصیف می‌کند، اما **بخش تئوری** حتی اگر بخواهید فقط با `Jettonها` کار کنید، **مهم** است.

:::tip
پیشنهاد می‌شود قبل از مطالعه این آموزش با [بررسی اجمالی پردازش دارایی](/v3/documentation/dapps/assets/overview) آشنا شوید.
:::

## قرارداد هوشمند کیف پول

قراردادهای هوشمند کیف پول در شبکه TON به بازیگران خارجی اجازه می‌دهد با نهادهای بلاکچین تعامل داشته باشند.

- مالک را تأیید می‌کند: درخواست‌هایی که سعی در پردازش یا پرداخت هزینه‌ها به نمایندگی از غیر مالکان دارند را رد می‌کند.
- محافظت در برابر اجرای مجدد: از اجرای مکرر همان درخواست جلوگیری می‌کند، مانند ارسال دارایی به قرارداد هوشمند دیگر.
- تعاملات دلخواه با قراردادهای هوشمند دیگر را آغاز می‌کند.

راه‌حل استاندارد برای اولین چالش، رمزنگاری با کلید عمومی است: `wallet` کلید عمومی را ذخیره می‌کند و بررسی می‌کند که آیا پیام ورودی دارای درخواست، توسط کلید خصوصی مربوطه که فقط صاحب آن می‌داند، امضا شده است.

راه‌حل چالش سوم نیز رایج است؛ به‌طور کلی، درخواست شامل یک پیام داخلی کاملاً شکل‌گرفته است که توسط `wallet` به شبکه ارسال می‌شود. با این حال، برای محافظت در برابر اجرای مجدد، رویکردهای مختلفی وجود دارد.

### کیف پول‌های مبتنی بر Seqno

کیف‌پول‌های مبتنی بر Seqno از ساده‌ترین روش برای ترتیب‌بندی پیام‌ها استفاده می‌کنند. هر پیام دارای یک عدد صحیح ویژه `seqno` است که باید با شمارنده ذخیره‌شده در قرارداد هوشمند `wallet` همخوانی داشته باشد. `wallet` شمارنده خود را در هر درخواست به‌روزرسانی می‌کند و بدین ترتیب اطمینان حاصل می‌شود که یک درخواست دوبار پردازش نمی‌شود. چند نسخه `wallet` وجود دارد که در روش‌های عمومی متفاوت هستند: توانایی محدود کردن درخواست‌ها براساس زمان انقضا و قابلیت داشتن چندین کیف‌پول با همان کلید عمومی. با این حال، الزام ذاتی این روش ارسال درخواست‌ها به طور یکی‌یکی است، زیرا هر شکافی در دنباله `seqno` منجر به عدم توانایی در پردازش همه درخواست‌های بعدی می‌شود.

### کیف پول‌های با بار بالا

این نوع `wallet` از رویکردی بر اساس ذخیره شناسه درخواست‌های پردازش‌شده و غیرمنقضی در ذخیره‌سازی قرارداد هوشمند پیروی می‌کند. در این روش، هر درخواست بررسی می‌شود تا در صورت مطابقت آن با درخواست‌هايی که قبلاً پردازش شده‌اند، حذف شود. به دلیل انقضاء، قرارداد نمی‌تواند تمامی درخواست‌ها را برای همیشه ذخیره کند، اما آنهایی که به دلیل محدودیت زمان انقضاء قابل پردازش نیستند، حذف می‌شوند. درخواست‌ها به این `wallet` می‌توانند بدون تداخل به صورت موازی ارسال شوند، اما این روش نیاز به نظارت پیشرفته‌تری برای پردازش درخواست‌ها دارد.

### استقرار کیف پول

برای استقرار یک کیف‌پول از طریق TonLib، باید:

1. یک جفت کلید خصوصی/عمومی را از طریق [createNewKey](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L244) یا توابع پوشش آن (مثال در [tonlib-go](https://github.com/mercuryoio/tonlib-go/tree/master/v2#create-new-private-key)) ایجاد کنید. توجه داشته باشید که کلید خصوصی به صورت محلی تولید می‌شود و دستگاه میزبان را ترک نمی‌کند.
2. ساختار [InitialAccountWallet](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L62) مورد نظر را مطابق با یکی از `wallet`های فعال تشکیل دهید. در حال حاضر `wallet.v3`، `wallet.v4`، `wallet.highload.v1`، `wallet.highload.v2` قابل استفاده هستند.
3. آدرس یک قرارداد هوشمند جدید `wallet` را از طریق متد [getAccountAddress](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L283) محاسبه کنید. توصیه می‌کنیم از ویرایش پیش‌فرض `0` استفاده کنید و همچنین کیف پول‌ها را در زنجیره اصلی `workchain=0`، برای کاهش هزینه‌های پردازش و ذخیره‌سازی، استقرار دهید.
4. مقداری تونکوین به آدرس محاسبه‌شده ارسال کنید. توجه داشته باشید که باید آن‌ها را در حالت `non-bounce` ارسال کنید، چرا که این آدرس هنوز هیچ کدی ندارد و نمی‌تواند پیام‌های ورودی را پردازش کند. پرچم `non-bounce` نشان می‌دهد که حتی اگر پردازش شکست بخورد، پول نباید با پیام بازگشت داده شود. توصیه نمی‌کنیم که از پرچم `non-bounce` برای تراکنش‌های دیگر، به‌ویژه هنگام حمل مبالغ بزرگ، استفاده کنید، چون مکانیزم بازگشت در برابر اشتباهات تا حدودی محافظت می‌کند.
5. [اقدام](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L154) مورد نظر را شکل دهید، بعنوان مثال برای فقط استقرار از `actionNoop` استفاده کنید. سپس از [createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L292) و [sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L300) برای شروع تعامل با بلاکچین استفاده کنید.
6. قرارداد را چند ثانیه بعد با متد [getAccountState](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L288) بررسی کنید.

:::tip
مطالعه بیشتر در [آموزش کیف پول](/v3/guidelines/smart-contracts/howto/wallet#-deploying-a-wallet)
:::

### اعتبار آدرس کیف پول را بررسی کنید

بیشتر SDK ها شما را مجبور به تأیید آدرس می کنند (بیشتر آنها در طول فرآیند ایجاد کیف پول یا آماده‌سازی تراکنش آن را تأیید می کنند)، بنابراین معمولاً نیازی به مراحل پیچیده اضافی از جانب شما ندارد.

<Tabs groupId="address-examples">

  <TabItem value="Tonweb" label="JS (Tonweb)">

```js
  const TonWeb = require("tonweb")
  TonWeb.utils.Address.isValid('...')
```

  </TabItem>
  <TabItem value="GO" label="tonutils-go">

```python
package main

import (
  "fmt"
  "github.com/xssnick/tonutils-go/address"
)

if _, err := address.ParseAddr("EQCD39VS5j...HUn4bpAOg8xqB2N"); err != nil {
  return errors.New("invalid address")
}
```

  </TabItem>
  <TabItem value="Java" label="Ton4j">

```javascript
try {
  Address.of("...");
  } catch (e) {
  // not valid address
}
```

  </TabItem>
  <TabItem value="Kotlin" label="ton-kotlin">

```javascript
  try {
    AddrStd("...")
  } catch(e: IllegalArgumentException) {
      // not valid address
  }
```

  </TabItem>
</Tabs>

:::tip
توضیحات کامل آدرس در صفحه [آدرس‌های قرارداد هوشمند](/v3/documentation/smart-contracts/addresses).
:::

## کار با انتقالات

### تراکنش‌های یک قرارداد را بررسی کنید

تراکنش‌های قرارداد با استفاده از [getTransactions](https://toncenter.com/api/v2/#/accounts/get_transactions_getTransactions_get) قابل دسترسی هستند. این روش به شما امکان می‌دهد ۱۰ تراکنش از `last_transaction_id` و قبلتر دریافت کنید. برای پردازش تمام تراکنش‌های ورودی، مراحل زیر باید دنبال شوند:

1. آخرین `last_transaction_id` را می‌توان با استفاده از [getAddressInformation](https://toncenter.com/api/v2/#/accounts/get_address_information_getAddressInformation_get) به دست آورد
2. فهرست ۱۰ تراکنش باید از طریق متد `getTransactions` بارگذاری شود.
3. تراکنش‌ها را با مبدا غیر خالی در پیام ورودی پردازش کنید و مقصد برابر با آدرس حساب باشد.
4. ۱۰ تراکنش بعدی باید بارگذاری شوند و مراحل ۲،۳،۴،۵ تکرار شوند تا زمانیکه شما همه تراکنش‌های ورودی را پردازش کنید.

### بازیابی تراکنش‌های ورودی/خروجی

در طول پردازش تراکنش، می‌توان جریان پیام‌ها را ردیابی کرد. از آنجا که جریان پیام یک DAG است، کافی است با استفاده از متد [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get) تراکنش جاری را دریافت کنید و تراکنش ورودی را با استفاده از `out_msg` از [tryLocateResultTx](https://testnet.toncenter.com/api/v2/#/transactions/get_try_locate_result_tx_tryLocateResultTx_get) یا تراکنش‌های خروجی را با `in_msg` از [tryLocateSourceTx](https://testnet.toncenter.com/api/v2/#/transactions/get_try_locate_source_tx_tryLocateSourceTx_get) بیابید.

<Tabs groupId="example-outgoing-transaction">
<TabItem value="JS" label="JS">

```ts
import { TonClient, Transaction } from '@ton/ton';
import { getHttpEndpoint } from '@orbs-network/ton-access';
import { CommonMessageInfoInternal } from '@ton/core';

async function findIncomingTransaction(client: TonClient, transaction: Transaction): Promise<Transaction | null> {
  const inMessage = transaction.inMessage?.info;
  if (inMessage?.type !== 'internal') return null;
  return client.tryLocateSourceTx(inMessage.src, inMessage.dest, inMessage.createdLt.toString());
}

async function findOutgoingTransactions(client: TonClient, transaction: Transaction): Promise<Transaction[]> {
  const outMessagesInfos = transaction.outMessages.values()
    .map(message => message.info)
    .filter((info): info is CommonMessageInfoInternal => info.type === 'internal');
  
  return Promise.all(
    outMessagesInfos.map((info) => client.tryLocateResultTx(info.src, info.dest, info.createdLt.toString())),
  );
}

async function traverseIncomingTransactions(client: TonClient, transaction: Transaction): Promise<void> {
  const inTx = await findIncomingTransaction(client, transaction);
  // now you can traverse this transaction graph backwards
  if (!inTx) return;
  await traverseIncomingTransactions(client, inTx);
}

async function traverseOutgoingTransactions(client: TonClient, transaction: Transaction): Promise<void> {
  const outTxs = await findOutgoingTransactions(client, transaction);
  // do smth with out txs
  for (const out of outTxs) {
    await traverseOutgoingTransactions(client, out);
  }
}

async function main() {
  const endpoint = await getHttpEndpoint({ network: 'testnet' });
  const client = new TonClient({
    endpoint,
    apiKey: '[API-KEY]',
  });
  
  const transaction: Transaction = ...; // Obtain first transaction to start traversing
  await traverseIncomingTransactions(client, transaction);
  await traverseOutgoingTransactions(client, transaction);
}

main();
```

</TabItem>
</Tabs>

### ارسال پرداخت‌ها

:::tip
یادگیری از نمونه پایه‌ای پردازش پرداخت‌ها از [TMA USDT Payments demo](https://github.com/ton-community/tma-usdt-payments-demo)
:::

1. سرویس باید یک `wallet` ایجاد کند و آن را تأمین مالی کند تا از تخریب قرارداد به دلیل هزینه‌های ذخیره‌سازی جلوگیری شود. توجه داشته باشید که هزینه‌های ذخیره‌سازی عموماً کمتر از ۱ تونکوین در سال است.
2. سرویس باید از کاربر `destination_address` و `comment` اختیاری را بگیرد. توجه داشته باشید که در حال حاضر، پیشنهاد می‌کنیم یا پرداخت‌های خروجی ناتمام با همان مفدار (`destination_address`, `value`, `comment`) را ممنوع کنید یا برنامه‌ریزی مناسب برای این پرداخت‌ها انجام دهید؛ در این صورت، پرداخت بعدی فقط پس از تأیید پرداخت قبلی آغاز می‌شود.
3. [msg.dataText](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L103) را با `comment` به عنوان متن تشکیل دهید.
4. [msg.message](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L113) را که شامل `destination_address`، `public_key` خالی، `amount` و `msg.dataText` می‌باشد، تشکیل دهید.
5. [Action](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L154) را که شامل یک سری پیام‌های خروجی است، تشکیل دهید.
6. برای ارسال پرداخت‌های خروجی از کوئری‌های [createQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L292) و [sendQuery](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L300) استفاده کنید.
7. سرویس باید به طور منظم متد [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get) را برای قرارداد `wallet` اجرا کند. تطبیق تراکنش‌های تأیید شده با پرداخت‌های خروجی بر اساس (`destination_address`, `value`, `comment`) اجازه می‌دهد پرداخت‌ها به عنوان کامل شده علامت‌گذاری شوند؛ هش تراکنش و lt (زمان منطقی) مربوطه را شناسایی و به کاربر نشان دهید.
8. درخواست‌های به `v3` کیف پول‌های `high-load` به طور پیش‌فرض دارای زمان انقضای ۶۰ ثانیه هستند. پس از این زمان، درخواست‌های پردازش نشده می‌توانند به طور امن به شبکه مجدداً ارسال شوند (به مراحل ۳ تا ۶ مراجعه کنید).

:::caution
اگر `value` پیوست شده بسیار کوچک باشد، تراکنش ممکن است با خطای `cskip_no_gas` متوقف شود. در این صورت، تونکوین‌ها با موفقیت منتقل خواهند شد اما هیچ منطقی در طرف دیگر اجرا نمی‌شود (حتی TVM راه‌اندازی نمی‌شود). درباره محدودیت‌های گس می‌توانید بیشتر [اینجا](/v3/documentation/network/configs/blockchain-configs#param-20-and-21) بخوانید.
:::

### دریافت شناسه تراکنش

ممکن است نامشخص باشد که برای دریافت اطلاعات بیشتر در مورد تراکنش، کاربر باید بلاکچین را از طریق تابع [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get) اسکن کند.
کسب شناسه تراکنش بلافاصله پس از ارسال پیام غیرممکن است، زیرا تراکنش ابتدا باید توسط شبکه بلاکچین تأیید شود.
برای درک فرآیند مورد نیاز، [ارسال پرداخت‌ها](/v3/guidelines/dapps/asset-processing/payments-processing/#send-payments) را با دقت مطالعه کنید، به ویژه بند ۷.

## رویکرد مبتنی بر فاکتور

برای پذیرش پرداخت‌ها بر اساس نظرات پیوست، سرویس باید

1. قرارداد `wallet` را مستقر کند.
2. یک `invoice` منحصر به فرد برای هر کاربر تولید کند. ارائه رشته‌ای uuid32 کافی است.
3. باید به کاربران دستور داده شود که تونکوین را به قرارداد `wallet` سرویس با پیوست `invoice` به عنوان نظر بفرستند.
4. سرویس باید به طور منظم متد [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get) را برای قرارداد `wallet` اجرا کند.
5. برای تراکنش‌های جدید، پیام ورودی باید استخراج شود، `comment` با پایگاه داده تطبیق داده شود و **مقدار پیام ورودی** به حساب کاربر واریز شود.

برای محاسبه **مقدار پیام ورودی** که پیام به قرارداد می‌آورد، لازم است که تراکنش تجزیه شود. این امر زمانی اتفاق می‌افتد که پیام به قرارداد برخورد کند. تراکنش را می‌توان با استفاده از [getTransactions](https://github.com/ton-blockchain/ton/blob/master/tl/generate/scheme/tonlib_api.tl#L268) بدست آورد. برای یک تراکنش کیف پول ورودی، داده صحیح شامل یک پیام ورودی و صفر پیام خروجی است. در غیر این صورت، یا یک پیام خارجی به کیف پول ارسال می‌شود که در آن صورت مالک تونکوین مصرف می‌کند، یا کیف پول مستقر نمی‌شود و تراکنش ورودی بازگشت داده می‌شود.

به طور کلی، مبلغی که یک پیام به قرارداد می‌برد را می‌توان به صورت مقدار پیام ورودی منهای مجموع مقادیر پیام‌های خروجی منهای کارمزد محاسبه کرد: `value_{in_msg} - SUM(value_{out_msg}) - fee`. به طور تکنیکی، نمایش تراکنش شامل سه فیلد متفاوت با `fee` در نام آنهاست: `fee`، `storage_fee` و `other_fee`، یعنی کارمزد کل، بخشی از کارمزد مرتبط با هزینه‌های ذخیره سازی و بخشی از کارمزد مرتبط با پردازش تراکنش. فقط باید از اولین استفاده شود.

### صورتحساب‌ها با TON Connect

بهترین گزینه برای DAppsهایی که نیاز به امضای چندین پرداخت/تراکنش در یک سشن دارند یا به حفظ اتصال به کیف پول برای مدت زمانی نیاز دارند.

- ✅ یک کانال ارتباطی دائمی با کیف پول وجود دارد، اطلاعات مربوط به آدرس کاربر

- ✅ کاربران فقط نیاز به اسکن یک بار کد QR دارند

- ✅ این امکان دارد که بدانیم آیا کاربر تراکنش را در کیف پول تایید کرده است، تراکنش را از طریق BOC برگشتی پیگیری کنید

- ✅ SDK‌های آماده و کیت‌های رابط کاربری برای پلتفرم‌های مختلف موجود هستند

- ❌ اگر فقط نیاز به ارسال یک پرداخت دارید، کاربر باید دو اقدام انجام دهد: اتصال کیف پول و تایید تراکنش

- ❌ پیاده‌سازی پیچیده‌تر از لینک ton:// است

<Button href="/v3/guidelines/ton-connect/overview/"
colorType="primary" sizeType={'lg'}>

بیشتر بدانید

</Button>

### صورتحساب‌ها با لینک ton://

:::warning
لینک Ton منسوخ شده است، از استفاده از این پرهیز کنید
:::

اگر به یک پیاده‌سازی ساده برای یک جریان ساده کاربری نیاز دارید، استفاده از لینک ton:// مناسب است.
بهترین گزینه برای پرداخت‌های یکباره و صورتحساب‌ها است.

```bash
ton://transfer/<destination-address>?
    [nft=<nft-address>&]
    [fee-amount=<nanocoins>&]
    [forward-amount=<nanocoins>] 
```

- ✅ پیاده‌سازی آسان

- ✅ نیازی به اتصال کیف پول ندارد

- ❌ کاربران برای هر پرداخت نیاز به اسکن یک کد QR جدید دارند

- ❌ امکان پیگیری این که کاربر تراکنش را امضا کرده یا نه وجود ندارد

- ❌ هیچ اطلاعاتی در مورد آدرس کاربر وجود ندارد

- ❌ در پلتفرم‌هایی که چنین لینک‌هایی قابل کلیک نیستند (مثلاً پیام‌های از ربات‌ها برای کلاینت‌های دسکتاپ تلگرام)، نیاز به راه‌حل‌های جایگزین می‌باشد

[اینجا بیشتر درباره لینک‌های ton بیاموزید](https://github.com/tonkeeper/wallet-api#payment-urls)

## کاوشگرها

کاوشگر بلاکچین https://tonscan.org است.

برای تولید یک لینک تراکنش در کاوشگر، سرویس نیاز دارد تا lt (زمان منطقی)، هش تراکنش و آدرس حساب را به دست آورد ( آدرس حسابی که از طریق متد [getTransactions](https://toncenter.com/api/v2/#/transactions/get_transactions_getTransactions_get) برای آن  lt و txhash دریافت شده است). سپس https://tonscan.org و https://explorer.toncoin.org/ می‌توانند صفحه برای آن tx را به فرمت زیر نشان دهند:

`https://tonviewer.com/transaction/{txhash as base64url}`

`https://tonscan.org/tx/{lt as int}:{txhash as base64url}:{account address}`

`https://explorer.toncoin.org/transaction?account={account address}&lt={lt as int}&hash={txhash as base64url}`

توجه داشته باشید که tonviewer و tonscan به جای هش تراکنش برای لینک در اکسپلورر، از هش پیام خارجی پشتیبانی می‌کنند.
این می‌تواند زمانی مفید باشد که می‌خواهید پیام خارجی تولید کرده و فوراً لینک تولید کنید.
اطلاعات بیشتر درباره تراکنش‌ها و هش پیام‌ها در [اینجا](/v3/guidelines/dapps/cookbook#how-to-find-transaction-or-message-hash) بخوانید.

## بهترین تمرین‌ها

### ایجاد کیف پول

<Tabs groupId="example-create_wallet">
<TabItem value="JS" label="JS">

- **toncenter:**
  - [ایجاد کیف پول + دریافت آدرس کیف پول](https://github.com/toncenter/examples/blob/main/common.js)

- **ton-community/ton:**
  - [ایجاد کیف پول + دریافت موجودی](https://github.com/ton-community/ton#usage)

</TabItem>

<TabItem value="Go" label="Go">

- **xssnick/tonutils-go:**
  - [ایجاد کیف پول + دریافت موجودی](https://github.com/xssnick/tonutils-go?tab=readme-ov-file#wallet)

</TabItem>

<TabItem value="Python" label="Python">

- **psylopunk/pythonlib:**
  - [ایجاد کیف پول + دریافت آدرس کیف پول](https://github.com/psylopunk/pytonlib/blob/main/examples/generate_wallet.py)
- **yungwine/pytoniq:**

```py
import asyncio

from pytoniq.contract.wallets.wallet import WalletV4R2
from pytoniq.liteclient.balancer import LiteBalancer


async def main():
    provider = LiteBalancer.from_mainnet_config(2)
    await provider.start_up()

    mnemonics, wallet = await WalletV4R2.create(provider)
    print(f"{wallet.address=} and {mnemonics=}")

    await provider.close_all()


if __name__ == "__main__":
    asyncio.run(main())
```

</TabItem>

</Tabs>

### ایجاد کیف پول برای شاردهای مختلف

هنگامی که بار زیادی وجود دارد، بلاکچین TON ممکن است به [شاردها](/v3/documentation/smart-contracts/shards/shards-intro) تقسیم شود. یک تشبیه ساده برای شارد در دنیای Web3 می‌تواند یک بخش شبکه باشد.

درست همانطور که ما زیرساخت‌های سرویس را در دنیای Web2 توزیع می‌کنیم تا به کاربر نهایی نزدیک‌تر باشیم، در TON، ما می‌توانیم قراردادها را در همان شاردی که کیف پول کاربر یا هر قراردادی که با آن تعامل دارد، قرار دهیم.

برای مثال، یک DApp که از کاربران برای سرویس آیردراپ آینده‌ هزینه می‌گیرد، ممکن است کیف پول‌های جداگانه‌ای برای هر شارد آماده کند تا تجربه کاربری در روزهای اوج بارگذاری بهبود یابد. برای رسیدن به بالاترین سرعت پردازش، باید یک کیف پول جمع‌آوری‌کننده برای هر شارد مستقر کنید.

پیشوند شارد `SHARD_INDEX` یک قرارداد با اولین ۴ بیت از هش آدرس آن تعریف می‌شود.
برای مستقر کردن کیف پول در شارد خاص، می‌توانید از منطق مبتنی بر قطعه کد زیر استفاده کنید:

```javascript

import { NetworkProvider, sleep } from '@ton/blueprint';
import { Address, toNano } from "@ton/core";
import {mnemonicNew, mnemonicToPrivateKey} from '@ton/crypto';
import { WalletContractV3R2 } from '@ton/ton';

export async function run(provider?: NetworkProvider) {
  if(!process.env.SHARD_INDEX) {
    throw new Error("Shard index is not specified");
  }

    const shardIdx = Number(process.env.SHARD_INDEX);
    let testWallet: WalletContractV3R2;
    let mnemonic:  string[];
    do {
        mnemonic   = await mnemonicNew(24);
        const keyPair = await mnemonicToPrivateKey(mnemonic);
        testWallet = WalletContractV3R2.create({workchain: 0, publicKey: keyPair.publicKey});
    } while(testWallet.address.hash[0] >> 4 !== shardIdx);

    console.log("Mnemonic for shard found:", mnemonic);
    console.log("Wallet address:",testWallet.address.toRawString());
}

if(require.main === module) {
run();
}

```

در مورد قرارداد کیف پول، ممکن است از `subwalletId` به جای mnemonic استفاده شود، اما `subwalletId` توسط [اپلیکیشن‌های کیف پول](https://ton.org/wallets) پشتیبانی نمی‌شود.

پس از تکمیل استقرار، می‌توانید با الگوریتم زیر پردازش را ادامه دهید:

1. کاربر به صفحه DApp می‌رود و درخواست اقدام می‌کند.
2. DApp نزدیک‌ترین کیف پول به کاربر را انتخاب می‌کند (با مقایسه پیشوند ۴ بیتی)
3. DApp به کاربر payloadی ارائه می‌دهد که هزینه او را به کیف پول انتخاب شده می‌فرستد.

به این ترتیب شما خواهید توانست بهترین تجربه کاربری ممکن را بدون توجه به بار کنونی شبکه ارائه دهید.

### سپرده‌های تونکوین‌ (دریافت تونکوین‌ها)

<Tabs groupId="example-toncoin_deposit">
<TabItem value="JS" label="JS">

- **toncenter:**
  - [پردازش سپرده تونکوین‌ها](https://github.com/toncenter/examples/blob/main/deposits.js)
  - [پردازش سپرده‌های تونکوین‌ها در چندین کیف پول](https://github.com/toncenter/examples/blob/main/deposits-multi-wallets.js)

</TabItem>

<TabItem value="Go" label="Go">

- **xssnick/tonutils-go:**

<details>
<summary>بررسی سپرده‌ها</summary>

```go
package main 

import (
	"context"
	"encoding/base64"
	"log"

	"github.com/xssnick/tonutils-go/address"
	"github.com/xssnick/tonutils-go/liteclient"
	"github.com/xssnick/tonutils-go/ton"
)

const (
	num = 10
)

func main() {
	client := liteclient.NewConnectionPool()
	err := client.AddConnectionsFromConfigUrl(context.Background(), "https://ton.org/global.config.json")
	if err != nil {
		panic(err)
	}

	api := ton.NewAPIClient(client, ton.ProofCheckPolicyFast).WithRetry()

	accountAddr := address.MustParseAddr("0QA__NJI1SLHyIaG7lQ6OFpAe9kp85fwPr66YwZwFc0p5wIu")

	// we need fresh block info to run get methods
	b, err := api.CurrentMasterchainInfo(context.Background())
	if err != nil {
		log.Fatal(err)
	}

	// we use WaitForBlock to make sure block is ready,
	// it is optional but escapes us from liteserver block not ready errors
	res, err := api.WaitForBlock(b.SeqNo).GetAccount(context.Background(), b, accountAddr)
	if err != nil {
		log.Fatal(err)
	}

	lastTransactionId := res.LastTxHash
	lastTransactionLT := res.LastTxLT

	headSeen := false

	for {
		trxs, err := api.ListTransactions(context.Background(), accountAddr, num, lastTransactionLT, lastTransactionId)
		if err != nil {
			log.Fatal(err)
		}

		for i, tx := range trxs {
			// should include only first time lastTransactionLT
			if !headSeen {
				headSeen = true
			} else if i == 0 {
				continue
			}

			if tx.IO.In == nil || tx.IO.In.Msg.SenderAddr().IsAddrNone() {
				// external message should be omitted
				continue
			}

      if tx.IO.Out != nil {
				// no outgoing messages - this is incoming Toncoins
				continue
			}

			// process trx
			log.Printf("found in transaction hash %s", base64.StdEncoding.EncodeToString(tx.Hash))
		}

		if len(trxs) == 0 || (headSeen && len(trxs) == 1) {
			break
		}

		lastTransactionId = trxs[0].Hash
		lastTransactionLT = trxs[0].LT
	}
}
```

</details>
</TabItem>

<TabItem value="Python" label="Python">

- **yungwine/pytoniq:**

<summary>بررسی سپرده‌ها</summary>

```python
import asyncio

from pytoniq_core import Transaction

from pytoniq import LiteClient, Address

MY_ADDRESS = Address("kf8zMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzMzM_BP")


async def main():
    client = LiteClient.from_mainnet_config(ls_i=0, trust_level=2)

    await client.connect()

    last_block = await client.get_trusted_last_mc_block()

    _account, shard_account = await client.raw_get_account_state(MY_ADDRESS, last_block)
    assert shard_account

    last_trans_lt, last_trans_hash = (
        shard_account.last_trans_lt,
        shard_account.last_trans_hash,
    )

    while True:
        print(f"Waiting for{last_block=}")

        transactions = await client.get_transactions(
            MY_ADDRESS, 1024, last_trans_lt, last_trans_hash
        )
        toncoin_deposits = [tx for tx in transactions if filter_toncoin_deposit(tx)]
        print(f"Got {len(transactions)=} with {len(toncoin_deposits)=}")

        for deposit_tx in toncoin_deposits:
            # Process toncoin deposit transaction
            print(deposit_tx.cell.hash.hex())

        last_trans_lt = transactions[0].lt
        last_trans_hash = transactions[0].cell.hash


def filter_toncoin_deposit(tx: Transaction):
    if tx.out_msgs:
        return False

    if tx.in_msg:
        return False

    return True


if __name__ == "__main__":
    asyncio.run(main())
```

</TabItem>
</Tabs>

### برداشت تونکوین‌ (ارسال تونکوین‌ها)

<Tabs groupId="example-toncoin_withdrawals">
<TabItem value="JS" label="JS">

- **toncenter:**
  - [برداشت تونکوین‌ها از یک کیف پول به صورت دسته‌ای](https://github.com/toncenter/examples/blob/main/withdrawals-highload-batch.js)
  - [برداشت تونکوین‌ها از یک کیف پول](https://github.com/toncenter/examples/blob/main/withdrawals-highload.js)

- **ton-community/ton:**
  - [برداشت تونکوین‌ها از یک کیف پول](https://github.com/ton-community/ton#usage)

</TabItem>

<TabItem value="Go" label="Go">

- **xssnick/tonutils-go:**
  - [برداشت تونکوین‌ها از یک کیف پول](https://github.com/xssnick/tonutils-go?tab=readme-ov-file#wallet)

</TabItem>

<TabItem value="Python" label="Python">

- **yungwine/pytoniq:**

```python
import asyncio

from pytoniq_core import Address
from pytoniq.contract.wallets.wallet import WalletV4R2
from pytoniq.liteclient.balancer import LiteBalancer


MY_MNEMONICS = "one two tree ..."
DESTINATION_WALLET = Address("Destination wallet address")


async def main():
    provider = LiteBalancer.from_mainnet_config()
    await provider.start_up()

    wallet = await WalletV4R2.from_mnemonic(provider, MY_MNEMONICS)

    await wallet.transfer(DESTINATION_WALLET, 5)
    
    await provider.close_all()


if __name__ == "__main__":
    asyncio.run(main())
```

</TabItem>

</Tabs>

### دریافت تراکنش‌های قرارداد

<Tabs groupId="example-get_transactions">
<TabItem value="JS" label="JS">

- **ton-community/ton:**
  - [کلاینت با متد getTransaction](https://github.com/ton-community/ton/blob/master/src/client/TonClient.ts)

</TabItem>

<TabItem value="Go" label="Go">

- **xssnick/tonutils-go:**
  - [دریافت تراکنش‌ها](https://github.com/xssnick/tonutils-go?tab=readme-ov-file#account-info-and-transactions)

</TabItem>

<TabItem value="Python" label="Python">

- **yungwine/pytoniq:**
  - [دریافت تراکنش‌ها](https://github.com/yungwine/pytoniq/blob/master/examples/transactions.py)

</TabItem>

</Tabs>

## SDKها

لیست کامل SDKها برای زبان‌های برنامه‌نویسی مختلف (JS، Python، Golang و غیره) [اینجا](/v3/guidelines/dapps/apis-sdks/sdk) در دسترس است.
