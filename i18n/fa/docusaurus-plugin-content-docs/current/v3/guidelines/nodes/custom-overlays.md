# پوشش های سفارشی

گره‌های TON با تشکیل زیرشبکه‌هایی به نام *پوشش‌ها* با یکدیگر ارتباط برقرار می‌کنند. تعدادی پوشش مشترک وجود دارد که گره‌ها در آنها مشارکت می‌کنند، مانند: پوشش‌های عمومی برای هر شارد، اعتبارسنج‌ها همچنین در پوشش عمومی اعتبارسنج‌ها و پوشش‌هایی خاص برای مجموعه‌های خاص اعتبارسنج‌ها شرکت می‌کنند.

گره‌ها همچنین می‌توانند برای پیوستن به پوشش‌های سفارشی تنظیم شوند.
در حال حاضر این پوشش‌ها می‌توانند برای دو منظور استفاده شوند:

- پخش پیام‌های خارجی
- پخش کاندیدهای بلاک.

شرکت در پوشش‌های سفارشی به اجتناب از عدم قطعیت پوشش‌های عمومی و بهبود قابلیت اطمینان و کاهش تأخیر در تحویل کمک می‌کند.

هر پوشش سفارشی دارای فهرست شرکت‌کنندگان به‌صورت دقیق تعریف‌شده با مجوزهای پیش‌فرض است، به ویژه مجوز برای ارسال پیام‌های خارجی و بلاک‌ها. پیکربندی پوشش باید بر روی تمام گره‌های شرکت‌کننده یکسان باشد.

اگر چندین گره تحت کنترل شما هستند، منطقی است که آنها را به یک پوشش سفارشی متحد کنید، جایی که همه اعتبارسنج‌ها قادر به ارسال کاندیدهای بلاک و همه LS قادر به ارسال پیام‌های خارجی باشند. به این ترتیب، همگام‌سازی LS سریع‌تر خواهد بود در حالی که همزمان نرخ تحویل پیام‌های خارجی بالاتر خواهد بود (و به طور کلی تحویل قوی‌تر خواهد شد). توجه داشته باشید که پوشش اضافی ترافیک شبکه اضافی ایجاد می‌کند.

## پوشش های سفارشی پیش‌فرض

Mytonctrl از پوشش‌های سفارشی پیش‌فرض در https://ton-blockchain.github.io/fallback_custom_overlays.json استفاده می‌کند. این پوشش بیشتر مواقع استفاده نمی‌شود و برای مواقع اضطراری در صورت بروز مشکل در اتصال پوشش عمومی منظور شده است.
برای متوقف کردن شرکت در پوشش‌های سفارشی پیش‌فرض فرمان‌های زیر را اجرا کنید

```bash
MyTonCtrl> set useDefaultCustomOverlays false
MyTonCtrl> delete_custom_overlay default
```

## ایجاد پوشش سفارشی

### جمع آوری آدرس‌های adnl

برای اضافه کردن اعتبارسنج‌ها به یک پوشش سفارشی، می‌توانید از شناسه `fullnode adnl` آنها که با `validator-console -c getconfig` بدست می‌آید یا شناسه `validator adnl` که در وضعیت mytonctrl پیدا می‌شود، استفاده کنید.
برای اضافه کردن لایت‌سرورها به یک پوشش سفارشی، باید از شناسه `fullnode adnl` آنها استفاده کنید.

### ایجاد یک فایل پیکربندی

یک فایل پیکربندی در این قالب ایجاد کنید:

```json
{
    "adnl_address_hex_1": {
        "msg_sender": true,
        "msg_sender_priority": 1
    },
    "adnl_address_hex_2": {
        "msg_sender": false
    },

    "adnl_address_hex_2": {
        "block_sender": true
    },
  ...
}
```

`msg_sender_priority` تعیین کننده ترتیب گنجاندن پیام‌های خارجی در بلاک‌ها است: پیام‌ها ابتدا از منبع با اولویت بالاتر پردازش می‌شوند. پیام‌ها از پوشش عمومی و LS محلی اولویت ۰ دارند.

**توجه کنید که تمام گره‌های لیست شده در پیکربندی باید در پوشش شرکت کنند (به عبارت دیگر، آنها باید پوشش را با همین پیکربندی اضافه کنند)، وگرنه اتصال ضعیف خواهد بود و پخش ناموفق خواهد شد**

یک واژه خاص به نام `@validators` وجود دارد که می‌تواند پوشش سفارشی پویا ایجاد کند که mytonctrl به صورت خودکار هر دور همه اعتبارسنج‌های کنونی را اضافه می‌کند.

### افزودن پوشش سفارشی

از فرمان mytonctrl برای افزودن پوشش سفارشی استفاده کنید:

```bash
MyTonCtrl> add_custom_overlay <name> <path_to_config>
```

توجه کنید که نام و فایل پیکربندی **باید** در تمام اعضای پوشش یکسان باشد. با استفاده از فرمان `list_custom_overlays` mytonctrl بررسی کنید که پوشش ایجاد شده است یا نه.

### اشکال‌یابی

می‌توانید سطح گزارش‌نویسی گره را به ۴ تنظیم کنید و لاگ‌ها را با واژه "CustomOverlay" پیدا کنید.

## حذف پوشش سفارشی

برای حذف پوشش سفارشی از یک گره، از فرمان `delete_custom_overlay <name>` mytonctrl استفاده کنید. اگر پوشش پویا باشد (یعنی در پیکربندی واژه `@validators` وجود دارد) ظرف یک دقیقه حذف می‌شود، در غیر اینصورت بلافاصله حذف می‌شود. برای اطمینان از اینکه گره، پوشش سفارشی را حذف کرده است، فرمان‌های `list_custom_overlays` mytonctrl و `showcustomoverlays` validator-console را بررسی کنید.

## سطح پایین

فهرست دستورات کنسول اعتبارسنج برای کار با پوشش‌های سفارشی:

- `addcustomoverlay <path_to_config>` - افزودن پوشش سفارشی به گره محلی. توجه کنید که این پیکربندی باید در قالبی غیر از پیکربندی برای mytonctrl باشد:
  ```json
  {
    "name": "OverlayName",
    "nodes": [
      {
        "adnl_id": "adnl_address_b64_1",
        "msg_sender": true,
        "msg_sender_priority": 1
      },
      {
        "adnl_id": "adnl_address_b64_2",
        "msg_sender": false
      }, ...
    ]
  }
  ```
- `delcustomoverlay <name>` - حذف پوشش سفارشی از گره.
- `showcustomoverlays` - نمایش فهرست پوشش‌های سفارشی که گره درباره آنها می‌داند.