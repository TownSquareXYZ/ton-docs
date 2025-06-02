import Feedback from '@site/src/components/Feedback';

# How it works

![چگونه کار می کند](/img/localizationProgramGuideline/localization-program.png)

The TownSquare Labs Localization Program comprises several key components. This chapter provides an overview of localization, helping you understand how it works and how to use it effectively.

در این سیستم، ما چندین برنامه کاربردی را ادغام می‌کنیم تا به‌صورت یکپارچه به عنوان یک برنامه واحد کار کنند:

- **GitHub**: مستندات را میزبانی کرده، اسناد را از مخزن بالادستی یکپارچه شده و ترجمه‌ها را به شاخه‌‍‌های خاص همگام‌سازی می‌کند.
- **Crowdin**: فرآیندهای ترجمه را مدیریت می‌کند، از جمله ترجمه، بازبینی و تنظیم ترجیحات زبانی.
- **سیستم‌های هوش مصنوعی**: از هوش مصنوعی پیشرفته برای کمک به مترجمان استفاده می‌کند و اطمینان حاصل می‌کند که جریان کار به‌طور روان انجام شود.
- **Customized Glossary**: This glossary guides translators and ensures AI generates accurate translations based on the project’s context. Users can also upload their glossaries as needed.

:::info
This guide won't cover the entire process but will highlight the key components that make the TownSquare Labs Localization Program unique. You can explore the program further on your own.
:::

## GitHub synchronization for documentation and translations

Our repository utilizes several branches to manage documentation and translations. Below is a detailed explanation of the purpose and function of each special branch:

### Branches overview

- **`dev`**\
  شاخه `dev` عملیات‌های GitHub Actions را اجرا می‌کند تا وظایف همگام‌سازی را مدیریت کند. می‌توانید تنظیمات گردش کار را در مسیر [**`.github/workflows`**](https://github.com/TownSquareXYZ/ton-docs/tree/dev/.github/workflows) پیدا کنید:

  - **`sync-fork.yml`**: این گردش کار مستندات را از مخزن بالادستی همگام‌سازی می‌کند و روزانه در ساعت 00:00 اجرا می‌شود.
  - **`sync-translations.yml`**: This workflow synchronizes updated translations to the respective language branches for preview purposes on the corresponding websites.

- **`main`**\
  This branch stays in sync with the upstream repository through GitHub Actions, which runs on the `dev` branch. It also updates specific codes we intend to propose to the original repository.

- **`l10n_main`**\
  This branch includes all changes from the `main` branch and translations from Crowdin. All modifications in this branch are periodically committed to the upstream repository using a new sub-branch named `l10n_main_[some data]`.

- **`l10n_feat` or `l10n_feat_[specific functions]`**\
  This branch will include changes to code or documentation related to the translation system. Once you finalize all content, the changes in this branch will be merged into `l10_main`.

- **`[lang]_preview`**\
  این شاخه‌ها برای پیش‌نمایش به زبان‌های خاص تعیین‌شده‌اند، مانند `ko_preview` برای کره‌ای و `ja_preview` برای ژاپنی. این‌ها به ما امکان می‌دهند تا وب‌سایت را در زبان‌های مختلف پیش‌نمایش کنیم.

با مدیریت این شاخه‌ها و استفاده از GitHub Actions ما به‌صورت مؤثر همگام‌سازی مستندات و به‌روزرسانی‌های ترجمه‌ای خود را مدیریت می‌کنیم، بنابراین محتوای چندزبانی ما همیشه به‌روز است.

## How to set up a new crowdin project

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

      For an example, refer to the [**config file**](https://github.com/TownSquareXYZ/ton-docs/blob/localization/crowdin.yml).\
      Find more in the [**Crowdin configuration documentation**](https://developer.crowdin.com/configuration-file/).

6. Crowdin را برای اتصال به مخزن GitHub خود پیکربندی کنید:
  1. روی `Add Repository` کلیک کنید و `Source and translation files mode` را انتخاب کنید.
    ![select-integration-mode](/img/localizationProgramGuideline/howItWorked/select-integration-mode.png)
  2. حساب GitHub خود را متصل کرده و مخزنی که می‌خواهید ترجمه کنید را جستجو کنید.
    ![search-repo](/img/localizationProgramGuideline/howItWorked/search-repo.png)
  3. Select the branch on the left to generate a new branch where Crowdin will post the translations.
    ![setting-branch](/img/localizationProgramGuideline/howItWorked/setting-branch.png)
  4. Choose the frequency for updating translations to your GitHub branch, then click save to enable the integration.
    ![frequency-save](/img/localizationProgramGuideline/howItWorked/frequency-save.png)

Find more details in the [**GitHub integration documentation**](https://support.crowdin.com/github-integration/).

7. در نهایت، می‌توانید با کلیک بر روی دکمه `Sync Now` در هر زمان که نیاز بود مخزن و ترجمه‌ها را همگام‌سازی کنید.

## واژه‌نامه

### What is a glossary?

Sometimes, AI translators can't recognize untranslatable and specific terms. For instance, we don't want "Rust" translated when referring to the programming language. To prevent such mistakes, we use a glossary to guide translations.

A **glossary** allows you to create, store, and manage project-specific terminology in one place, ensuring that terms are translated correctly and consistently.

You can reference our [**ton-i18n-glossary**](https://github.com/TownSquareXYZ/ton-i18n-glossary).
![ton-i18n-glossary](/img/localizationProgramGuideline/howItWorked/ton-i18n-glossary.png)

### How to set up a glossary for a new language?

بیشتر پلتفرم‌های ترجمه از واژه‌نامه‌ها پشتیبانی می‌کنند. در Crowdin، پس از راه‌اندازی واژه‌نامه، هر واژه به صورت یک کلمه زیر خط‌دار در ویرایشگر نمایش داده می‌شود. با نگه داشتن نشانگر روی واژه، ترجمه، بخش گفتاری و تعریف آن (در صورت موجود بودن) را مشاهده کنید.
![github-glossary](/img/localizationProgramGuideline/howItWorked/github-glossary.png)
![crowdin-glossary](/img/localizationProgramGuideline/howItWorked/crowdin-glossary.png)

In DeepL, upload your glossary, which will be used automatically during AI translation.

ما [**برنامه‌ای برای واژه‌نامه**](https://github.com/TownSquareXYZ/ton-i18n-glossary) ایجاد کرده‌ایم که به‌صورت خودکار به‌روزرسانی‌ها را آپلود می‌کند.

برای افزودن یک اصطلاح به واژه‌نامه:

1. اگر اصطلاح انگلیسی قبلاً در واژه‌نامه موجود است، خط و ستون مربوط به زبان مدنظر خود برای ترجمه را پیدا کنید، ترجمه را وارد کرده و آپلود کنید.
2. برای آپلود یک واژه‌نامه جدید، پروژه را کلون کرده و اجرا کنید:

```bash
npm i
```

```bash
npm run generate -- <glossary name you want>
```

مرحله ۱ را برای افزودن واژه جدید تکرار کنید.

## How to take advantage of AI translation copilot?

کوپایلوت ترجمه هوشمند به شکستن موانع زبانی با چندین مزیت کمک می‌کند:

- **افزایش همسانی**: ترجمه‌های هوش مصنوعی بر اساس اطلاعات به‌روز هستند و دقیق‌ترین و جدیدترین ترجمه‌ها را ارائه می‌دهند.
- **سرعت و کارایی**: ترجمه با هوش مصنوعی به‌صورت فوری انجام می‌شود و می‌تواند حجم بالایی از محتوا را به‌صورت بلادرنگ پردازش کند.
- **Robust Scalability**: AI systems continuously learn and improve, enhancing translation quality over time.

We use DeepL for AI translation in our Crowdin project:

1. در منوی Crowdin، Machine Translation را انتخاب کرده و در خط DeepL روی ویرایش کلیک کنید.
  ![select-deepl](/img/localizationProgramGuideline/howItWorked/select-deepl.png)
2. پشتیبانی DeepL را فعال کنید و کلید API مترجم DeepL را وارد کنید.
  > [چگونه کلید API مترجم DeepL را دریافت کنیم](https://www.deepl.com/pro-api?cta=header-pro-api)

![config-crowdin-deepl](/img/localizationProgramGuideline/howItWorked/config-crowdin-deepl.png)

3. تنظیمات DeepL ما از یک واژه‌نامه سفارشی استفاده می‌کند. برای جزئیات در مورد آپلود واژه‌نامه، [**ton-i18n-glossary**](https://github.com/TownSquareXYZ/ton-i18n-glossary) را بررسی کنید.

4. در مخزن، روی Pre-translation کلیک کرده و از طریق Machine Translation انتخاب کنید.
  ![pre-translation](/img/localizationProgramGuideline/howItWorked/pre-translation.png)

5. Choose DeepL as the Translation Engine, select the target languages, and select the translated files.
  ![pre-translate-config](/img/localizationProgramGuideline/howItWorked/pre-translate-config.png)

That's it! Now, you can take a break and wait for the pre-translation to complete.

<Feedback />

