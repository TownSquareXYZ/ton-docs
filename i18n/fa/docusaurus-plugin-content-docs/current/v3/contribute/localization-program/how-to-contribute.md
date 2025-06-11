import Feedback from '@site/src/components/Feedback';

# How to contribute

This page explains how to participate in the localization program for TON documentation.

## پیش‌نیازها

Localization contribution is open to everyone. Here are a few steps you need to take before you start contributing:

1. Log in to your [Crowdin](https://crowdin.com) account or sign up.
2. زبانی که می‌خواهید در آن مشارکت کنید را انتخاب کنید.
3. Familiarize yourself with the [How to use crowdin](/v3/contribute/localization-program/how-to-contribute/) guide and the [Translation style guide](/v3/contribute/localization-program/translation-style-guide/) for tips and best practices.
4. Use machine translations to aid your work, but do not rely solely on them.
5. Preview all translation results on the website after proofreading.

:::info
Before contributing, read the guidelines below to ensure standardization and quality, speeding up the review process.
:::

## Side-by-side mode

All tasks are performed in **side-by-side** mode in the Crowdin Editor. To enable this, click a file you want to work on. At the top right of the page, click the **Editor view** button and select **side-by-side** mode for a clearer editor view.\
![side-by-side mode](/img/localizationProgramGuideline/side-by-side.png)

## نقش‌ها

در اینجا **نقش‌هایی** که می‌توانید در سیستم بپذیرید آورده شده است:

- **هماهنگ‌کننده زبان** - مدیریت ویژگی‌های پروژه در زبان‌های اختصاص داده شده.
- **Developer** – Uploads files, edits translatable text, connects integrations and uses the API.
- **تصحیح‌کننده** – ترجمه و تأیید رشته‌ها.
- **مترجم** (داخلی یا جامعه) – ترجمه رشته‌ها و رأی دادن به ترجمه‌های اضافه شده توسط دیگران.

The localization project is hosted on [Crowdin](https://crowdin.com/project/ton-docs).

### Language coordinator guidelines

- Translate and approve strings
- Pre-translate project content
- Manage project members and join requests
  ![manage-members](/img/localizationProgramGuideline/manage-members.png)
- Generate project reports
  ![generate-reports](/img/localizationProgramGuideline/generate-reports.png)
- Create tasks
  ![create-tasks](/img/localizationProgramGuideline/create-tasks.png)

### Developer guidelines

- **Update footer configuration for your language:**
  1. Fork our [repository](https://github.com/TownSquareXYZ/ton-docs/tree/i18n_feat).
  2. فایل [**`src/theme/Footer/config.ts`**](https://github.com/TownSquareXYZ/ton-docs/blob/main/src/theme/Footer/config.ts) را پیدا کنید.
  3. مقدار متغیر **`FOOTER_COLUMN_LINKS_EN`** را در **`FOOTER_COLUMN_LINKS_[YOUR_LANG]`** کپی کنید.
  4. مقادیر کلیدهای **`headerLangKey`** و **`langKey`** را به زبان خود ترجمه کنید، همانطور که ما برای زبان ماندارین در **`FOOTER_COLUMN_LINKS_CN`** انجام دادیم.
  5. یک ویژگی جدید به **`FOOTER_LINKS_TRANSLATIONS`** اضافه کنید:
    - **کلید** را به عنوان [**کد زبان ISO**](https://www.andiamo.co.uk/resources/iso-language-codes/) خود (**دو حرف**، **حروف کوچک**) تنظیم کنید.
    - **The value** should be the new variable you created for your language.
  6. دستور **`yarn start:local [YOUR_IOS_LANG_CODE]`** را اجرا کنید تا فوتر جدید را به زبان خود پیش‌نمایش کنید.
    (مثلاً، **`yarn start:local ru`** برای پیش‌نمایش فوتر **روسی**)
  7. اگر همه چیز خوب به نظر می‌رسد، یک درخواست کششی به شاخه **`i18n_feat`** ایجاد کنید.
- **آپلود فایل‌ها**
- **ویرایش متون قابل ترجمه**
- **اتصال یکپارچه‌سازی‌ها** (مثلاً افزودن یکپارچه‌سازی GitHub)
  ![نصب یکپارچه‌سازی GitHub](/img/localizationProgramGuideline/howItWorked/install-github-integration.png)
- **استفاده از [Crowdin API](https://developer.crowdin.com/api/v2/)**

### Proofreader guidelines

به عنوان **تصحیح‌کننده**، شما بر روی فایل‌هایی با یک **نوار پیشرفت آبی** کار خواهید کرد.
![مرحله تصحیح 1](/img/localizationProgramGuideline/proofread-step1.png)
روی یک فایل کلیک کنید تا وارد رابط ویرایش شوید.

#### Contribution flow

1. اطمینان حاصل کنید که در [**حالت side-by-side**](#side-by-side-mode) هستید. فیلتر ترجمه‌های **Not Approved** را فعال کنید تا رشته‌هایی که نیاز به تصحیح دارند را ببینید.
  ![فیلتر تصحیح](/img/localizationProgramGuideline/proofread-filter.png)

2. به این قوانین پایبند باشید:
  - رشته‌هایی را انتخاب کنید که دارای **آیکون مکعب آبی** هستند. هر ترجمه را بررسی کنید:
    - اگر **درست** بود، دکمه ☑️ را کلیک کنید.
    - اگر **اشتباه** بود، به خط بعدی بروید.

![تصحیح تایید شده](/img/localizationProgramGuideline/proofread-approved.png)

:::info
You can also review the approved lines:

1. با **Approved** فیلتر کنید.

2. اگر خط تأیید شده ای مشکلی داشت، دکمه ☑️ را کلیک کنید تا به وضعیت نیازمند تصحیح برگردد.
  :::

3. To move to the following file, click the file name at the top, select the new file from the pop-up window, and continue proofreading.
  ![to next](/img/localizationProgramGuideline/redirect-to-next.png)

#### Previewing your work

The preview website displays all approved content within one hour. Check [**our repo**](https://github.com/TownSquareXYZ/ton-docs/pulls) for the **preview** link in the newest PR.
![preview link](/img/localizationProgramGuideline/preview-link.png)

### Translator guidelines

As a translator, you aim to ensure that translations are faithful and expressive, keeping them as close to the original meaning and as understandable as possible. Your mission is to make the blue progress bar reach 100%.

#### Translation flow

برای یک فرآیند ترجمه موفق، این مراحل را دنبال کنید:

1. فایل‌هایی را انتخاب کنید که هنوز به ۱۰۰٪ ترجمه نرسیده‌اند.
  ![انتخاب مترجم](/img/localizationProgramGuideline/translator-select.png)

2. اطمینان حاصل کنید که در [**حالت side-by-side**](#side-by-side-mode) هستید. با رشته‌های **Untranslated** فیلتر کنید.
  ![فیلتر مترجم](/img/localizationProgramGuideline/translator-filter.png)

3. فضای کاری شما دارای چهار بخش است:
  - **بالا سمت چپ:** ترجمه خود را بر اساس رشته منبع وارد کنید.
  - **پایین سمت چپ:** پیش‌نمایش فایل ترجمه شده. فرمت اصلی را حفظ کنید.
  - **پایین سمت راست:** ترجمه‌های پیشنهاد شده از Crowdin. برای استفاده کلیک کنید، اما دقت آن را بررسی کنید، به ویژه برای پیوندها.

4. ترجمه خود را با کلیک بر روی دکمه **Save** در بالا ذخیره کنید.
  ![translator save](/img/localizationProgramGuideline/translator-save.png)

5. برای انتقال به فایل بعدی، بر روی نام فایل در بالا کلیک کنید و فایل جدید را از پنجره پاپ‌آپ انتخاب کنید.
  ![to next](/img/localizationProgramGuideline/redirect-to-next.png)

## How to add support for a new language

If you are a community manager, follow these steps:

1. یک شاخه جدید به نام `[lang]_localization` (مثلاً، `ko_localization` برای کره‌ای) در [TownSquareXYZ/ton-docs](https://github.com/TownSquareXYZ/ton-docs) اضافه کنید.
2. **با مالک Vercel این ریپو تماس بگیرید** تا زبان جدید را به منو اضافه کند.
3. یک درخواست کششی به شاخه dev ارسال کنید. **با dev ادغام نکنید**؛ این صرفاً برای اهداف پیش‌نمایش است.

Once you complete these steps, you can see the preview of your language in the PR request.
![ko preview](/img/localizationProgramGuideline/ko_preview.png)

هنگامی که زبان شما برای مستندات TON آماده شد، یک issue ایجاد کنید و ما زبان شما را در محیط تولید قرار خواهیم داد.

<Feedback />

