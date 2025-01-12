# چگونه کار می‌کند

![چگونه کار می کند](/img/localizationProgramGuideline/localization-program.png)

برنامه بومی‌سازی **TownSquare Labs** شامل چندین مؤلفه کلیدی است. این فصل یک مرور کلی از نحوه عملکرد برنامه ارائه می‌دهد و به شما کمک می‌کند تا کارکرد آن و نحوه استفاده مؤثر از آن را درک کنید.

در این سیستم، ما چندین برنامه کاربردی را ادغام می‌کنیم تا به‌صورت یکپارچه به عنوان یک برنامه واحد کار کنند:

- **GitHub**: مستندات را میزبانی کرده، اسناد را از مخزن بالادستی یکپارچه شده و ترجمه‌ها را به شاخه‌‍‌های خاص همگام‌سازی می‌کند.
- **Crowdin**: فرآیندهای ترجمه را مدیریت می‌کند، از جمله ترجمه، بازبینی و تنظیم ترجیحات زبانی.
- **سیستم‌های هوش مصنوعی**: از هوش مصنوعی پیشرفته برای کمک به مترجمان استفاده می‌کند و اطمینان حاصل می‌کند که جریان کار به‌طور روان انجام شود.
- **واژه‌نامه سفارشی‌شده**: مترجمان را راهنمایی کرده و اطمینان حاصل می‌کند که هوش مصنوعی ترجمه‌های دقیقی بر اساس مفاد پروژه ایجاد می‌کند. کاربران می‌توانند به صورت دلخواه واژه‌نامه‌های خود را آپلود کنند.

:::info
این راهنما کل فرآیند را به تفصیل پوشش نمی‌دهد، اما بر روی مؤلفه‌های کلیدی که برنامه بومی‌سازی TownSquare Labs را منحصر به فرد می‌کند تمرکز خواهد کرد. شما می‌توانید برنامه را به‌صورت جزئی‌تر بررسی کنید.
:::

## همگام‌سازی GitHub برای مستندات و ترجمه‌ها

مخزن ما از چندین شاخه برای مدیریت مستندات و ترجمه‌ها استفاده می‌کند. در زیر توضیحات دقیق‌تری از هدف و عملکرد هر شاخه خاص ارائه شده است:

### نمای کلی شاخه‌ها

- **`dev`**\
  شاخه `dev` عملیات‌های GitHub Actions را اجرا می‌کند تا وظایف همگام‌سازی را مدیریت کند. می‌توانید تنظیمات گردش کار را در مسیر [**`.github/workflows`**](https://github.com/TownSquareXYZ/ton-docs/tree/dev/.github/workflows) پیدا کنید:

  - **`sync-fork.yml`**: این گردش کار مستندات را از مخزن بالادستی همگام‌سازی می‌کند و روزانه در ساعت 00:00 اجرا می‌شود.
  - **`sync-translations.yml`**: این گردش کار ترجمه‌های به‌روز را به شاخه‌های زبانی مرتبط همگام‌سازی می‌کند تا برای نمایش پیش‌نمایش در وب‌سایت‌های مرتبط زبانی استفاده شود.

- **`main`**\
  این شاخه از طریق GitHub Actions که در شاخه `dev` اجرا می‌شود، با مخزن بالادست همگام است. همچنین برای به‌روزرسانی برخی کدها که قصد داریم به مخزن اصلی پیشنهاد دهیم، استفاده می‌شود.

- **`l10n_main`**\
  این شاخه شامل همه تغییرات از شاخه `main` و ترجمه‌های Crowdin است. همه‌ی تغییرات در این شاخه به‌صورت دوره‌ای توسط یک زیرشاخه جدید به نام `l10n_main_[some data]` به مخزن بالادست متعهد می‌شوند.

- **`l10n_feat` یا `l10n_feat_[specific functions]`**\
  این شاخه شامل تغییرات در کد یا مستندات مربوط به سیستم ترجمه خواهد بود. پس از تکمیل همه محتوا، تغییرات در این شاخه به `l10_main` ادغام می‌شود.

- **`[lang]_preview`**\
  این شاخه‌ها برای پیش‌نمایش به زبان‌های خاص تعیین‌شده‌اند، مانند `ko_preview` برای کره‌ای و `ja_preview` برای ژاپنی. این‌ها به ما امکان می‌دهند تا وب‌سایت را در زبان‌های مختلف پیش‌نمایش کنیم.

با مدیریت این شاخه‌ها و استفاده از GitHub Actions ما به‌صورت مؤثر همگام‌سازی مستندات و به‌روزرسانی‌های ترجمه‌ای خود را مدیریت می‌کنیم، بنابراین محتوای چندزبانی ما همیشه به‌روز است.

## چگونه یک پروژه جدید Crowdin ایجاد کنیم

1. وارد [**حساب کاربری Crowdin**](https://accounts.crowdin.com/login) شوید.

2. در منو `Create new project` را کلیک کنید.
   ![Create new project](/img/localizationProgramGuideline/howItWorked/create-new-project.png)

3. نام پروژه و زبان‌های هدف را تنظیم کنید. می‌توانید بعداً زبان‌ها را در تنظیمات تغییر دهید.
   ![Create project setting](/img/localizationProgramGuideline/howItWorked/create-project-setting.png)

4. به پروژه‌ای که تازه ایجاد کرده‌اید بروید، تب Integrations را انتخاب کنید، دکمه `Add Integration` را کلیک کنید، `GitHub` را جستجو کرده و نصب کنید.
   ![install-github-integration](/img/localizationProgramGuideline/howItWorked/install-github-integration.png)

5. قبل از پیکربندی ادغام GitHub در Crowdin، مشخص کنید که کدام فایل‌ها را برای آپلود به Crowdin انتخاب کرده‌اید تا از آپلود فایل‌های غیرضروری جلوگیری کنید:

   1. یک فایل **crowdin.yml** در ریشه **مخزن GitHub خود** با این پیکربندی پایه ایجاد کنید:

   ```yml
   project_id: <Your project id>
   preserve_hierarchy: 1
   files:
     - source: <Path of your original files>
       translation: <Path of your translated files>
   ```

   2. مقادیر پیکربندی درست را دریافت کنید:
      - **project_id**: در پروژه Crowdin خود به تب Tools بروید، API را انتخاب کرده و **project_id** را پیدا کنید.
        ![select-api-tool](/img/localizationProgramGuideline/howItWorked/select-api-tool.png)
        ![projectId](/img/localizationProgramGuideline/howItWorked/projectId.png)
      - **preserve_hierarchy**: ساختار دایرکتوری GitHub را در سرور Crowdin حفظ می‌کند.
      - **source** و **translation**: مسیرهای فایل‌هایی که به Crowdin آپلود می‌شوند و مسیر خروجی فایل‌های ترجمه‌شده را مشخص کنید.

        [**فایل پیکربندی رسمی ما**](https://github.com/TownSquareXYZ/ton-docs/blob/localization/crowdin.yml) را به عنوان نمونه بررسی کنید.\
        جزئیات بیشتر را می‌توانید در [**مستندات پیکربندی Crowdin**](https://developer.crowdin.com/configuration-file/) بیابید.

6. Crowdin را برای اتصال به مخزن GitHub خود پیکربندی کنید:
   1. روی `Add Repository` کلیک کنید و `Source and translation files mode` را انتخاب کنید.
      ![select-integration-mode](/img/localizationProgramGuideline/howItWorked/select-integration-mode.png)
   2. حساب GitHub خود را متصل کرده و مخزنی که می‌خواهید ترجمه کنید را جستجو کنید.
      ![search-repo](/img/localizationProgramGuideline/howItWorked/search-repo.png)
   3. شاخه‌ی سمت چپ را انتخاب کنید که یک شاخه جدید ایجاد شود که در آن Crowdin ترجمه‌ها را ارسال می‌کند.
      ![setting-branch](/img/localizationProgramGuideline/howItWorked/setting-branch.png)
   4. تکرار به‌روزرسانی ترجمه‌ها به شاخه GitHub خود را انتخاب کنید. تنظیمات دیگر می‌توانند به‌صورت پیش‌فرض باقی بمانند و سپس ذخیره کنید تا ادغام فعال شود.
      ![frequency-save](/img/localizationProgramGuideline/howItWorked/frequency-save.png)

برای اطلاعات بیشتر به [**مستندات ادغام GitHub**](https://support.crowdin.com/github-integration/) مراجعه کنید.

7. در نهایت، می‌توانید با کلیک بر روی دکمه `Sync Now` در هر زمان که نیاز بود مخزن و ترجمه‌ها را همگام‌سازی کنید.

## واژه‌نامه

### واژه‌نامه چیست؟

گاهی اوقات، مترجم‌های هوش مصنوعی نمی‌توانند اصطلاحات خاصی که نباید ترجمه شوند را شناسایی کنند. به عنوان مثال، ما نمی‌خواهیم "Rust" را هنگامی که به زبان برنامه‌نویسی اشاره دارد، ترجمه کنیم. برای جلوگیری از چنین اشتباهاتی، از یک واژه‌نامه برای راهنمایی ترجمه‌ها استفاده می‌کنیم.

یک **واژه‌نامه** به شما اجازه می‌دهد تا اصطلاحات خاص پروژه را در یک مکان ایجاد، ذخیره و مدیریت کنید و اطمینان حاصل کنید که اصطلاحات به درستی و به طور مداوم ترجمه می‌شوند.

بعنوان مرجع به [**واژه‌نامه ton-i18n**](https://github.com/TownSquareXYZ/ton-i18n-glossary) ما نگاه کنید.
![ton-i18n-glossary](/img/localizationProgramGuideline/howItWorked/ton-i18n-glossary.png)

### چگونه برای زبان جدید یک واژه‌نامه تنظیم کنیم؟

بیشتر پلتفرم‌های ترجمه از واژه‌نامه‌ها پشتیبانی می‌کنند. در Crowdin، پس از راه‌اندازی واژه‌نامه، هر واژه به صورت یک کلمه زیر خط‌دار در ویرایشگر نمایش داده می‌شود. با نگه داشتن نشانگر روی واژه، ترجمه، بخش گفتاری و تعریف آن (در صورت موجود بودن) را مشاهده کنید.
![github-glossary](/img/localizationProgramGuideline/howItWorked/github-glossary.png)
![crowdin-glossary](/img/localizationProgramGuideline/howItWorked/crowdin-glossary.png)

در DeepL، تنها کافی است واژه‌نامه خود را آپلود کنید و این واژه‌نامه به‌صورت خودکار در طول ترجمه با هوش مصنوعی استفاده می‌شود.

ما [**برنامه‌ای برای واژه‌نامه**](https://github.com/TownSquareXYZ/ton-i18n-glossary) ایجاد کرده‌ایم که به‌صورت خودکار به‌روزرسانی‌ها را آپلود می‌کند.

برای افزودن یک اصطلاح به واژه‌نامه:

1. اگر اصطلاح انگلیسی قبلاً در واژه‌نامه موجود است، خط و ستون مربوط به زبان مدنظر خود برای ترجمه را پیدا کنید، ترجمه را وارد کرده و آپلود کنید.
2. برای آپلود یک واژه‌نامه جدید، پروژه را کلون کرده و اجرا کنید:

   - `npm i`
   - `npm run generate -- <glossary name you want>`

مرحله ۱ را برای افزودن واژه جدید تکرار کنید.

**سادگی و کارایی، نه؟**

## How to Take Advantage of AI Translation Copilot?

کوپایلوت ترجمه هوشمند به شکستن موانع زبانی با چندین مزیت کمک می‌کند:

- **افزایش همسانی**: ترجمه‌های هوش مصنوعی بر اساس اطلاعات به‌روز هستند و دقیق‌ترین و جدیدترین ترجمه‌ها را ارائه می‌دهند.
- **سرعت و کارایی**: ترجمه با هوش مصنوعی به‌صورت فوری انجام می‌شود و می‌تواند حجم بالایی از محتوا را به‌صورت بلادرنگ پردازش کند.
- **قابلیت مقیاس‌پذیری قوی**: سیستم‌های هوش مصنوعی به‌طور مداوم یاد می‌گیرند و بهبود می‌بخشند و کیفیت ترجمه در طول زمان افزایش می‌یابد. با واژه‌نامه ارائه‌شده، ترجمه‌های هوش مصنوعی می‌توانند به نیازهای خاص مخازن مختلف تطبیق داده شوند.

برای استفاده از ترجمه هوش مصنوعی در Crowdin (ما در پروژه‌مان از DeepL استفاده می‌کنیم):

1. در منوی Crowdin، Machine Translation را انتخاب کرده و در خط DeepL روی ویرایش کلیک کنید.
   ![select-deepl](/img/localizationProgramGuideline/howItWorked/select-deepl.png)
2. پشتیبانی DeepL را فعال کنید و کلید API مترجم DeepL را وارد کنید.
   > [چگونه کلید API مترجم DeepL را دریافت کنیم](https://www.deepl.com/pro-api?cta=header-pro-api)

![config-crowdin-deepl](/img/localizationProgramGuideline/howItWorked/config-crowdin-deepl.png)

3. تنظیمات DeepL ما از یک واژه‌نامه سفارشی استفاده می‌کند. برای جزئیات در مورد آپلود واژه‌نامه، [**ton-i18n-glossary**](https://github.com/TownSquareXYZ/ton-i18n-glossary) را بررسی کنید.

4. در مخزن، روی Pre-translation کلیک کرده و از طریق Machine Translation انتخاب کنید.
   ![pre-translation](/img/localizationProgramGuideline/howItWorked/pre-translation.png)

5. DeepL را به‌عنوان موتور ترجمه انتخاب کنید، زبان‌های هدف را انتخاب کنید و فایل‌هایی که می‌خواهید ترجمه کنید را انتخاب کنید.
   ![pre-translate-config](/img/localizationProgramGuideline/howItWorked/pre-translate-config.png)

تمام! حالا می‌توانید یک استراحت کنید و منتظر پایان پیش‌ترجمه بمانید.
