import Feedback from '@site/src/components/Feedback';

# 工作原理

![工作原理](/img/localizationProgramGuideline/localization-program.png)

The TownSquare Labs Localization Program comprises several key components. This chapter provides an overview of localization, helping you understand how it works and how to use it effectively.

在这个系统中，我们整合了多个应用程序，使其作为一个统一的整体无缝运行：

- **GitHub**：托管文档，同步上游版本库中的文档，并将翻译同步到特定分支。
- **Crowdin**：管理翻译流程，包括翻译、校对和设置语言首选项。
- **人工智能系统**：利用先进的人工智能协助翻译员，确保工作流程顺畅。
- **Customized Glossary**: This glossary guides translators and ensures AI generates accurate translations based on the project’s context. Users can also upload their glossaries as needed.

:::info
This guide won't cover the entire process but will highlight the key components that make the TownSquare Labs Localization Program unique. You can explore the program further on your own.
:::

## GitHub synchronization for documentation and translations

Our repository utilizes several branches to manage documentation and translations. Below is a detailed explanation of the purpose and function of each special branch:

### Branches overview

- **`dev`**\
  `dev` 分支运行 GitHub Actions 来处理同步任务，你可以在 [**`.github/workflows`**](https://github.com/TownSquareXYZ/ton-docs/tree/dev/.github/workflows) 目录中找到工作流配置。

  - **`sync-fork.yml`**：此工作流程从上游版本库同步文档。每天 00:00 运行。
  - **`sync-translations.yml`**: This workflow synchronizes updated translations to the respective language branches for preview purposes on the corresponding websites.

- **`main`**\
  This branch stays in sync with the upstream repository through GitHub Actions, which runs on the `dev` branch. It also updates specific codes we intend to propose to the original repository.

- **`l10n_main`**\
  This branch includes all changes from the `main` branch and translations from Crowdin. All modifications in this branch are periodically committed to the upstream repository using a new sub-branch named `l10n_main_[some data]`.

- **`l10n_feat` or `l10n_feat_[specific functions]`**\
  This branch will include changes to code or documentation related to the translation system. Once you finalize all content, the changes in this branch will be merged into `l10_main`.

- **`[lang]_preview`**\
  这些分支被指定用于特定语言的预览，例如 `ko_preview` 用于韩语`ja_preview` 用于日语。它们允许我们在不同语言中预览网站。

`dev`分支运行 GitHub Actions 来处理同步任务。你可以在 [**`.github/workflows`**](https://github.com/TownSquareXYZ/ton-docs/tree/dev/.github/workflows) 目录中找到工作流配置：

## How to set up a new crowdin project

1. 登录您的 [**Crowdin 帐户**](https://accounts.crowdin.com/login)。

2. 点击菜单中的 `Create new project`。
  ![创建新项目](/img/localizationProgramGuideline/howItWorked/create-new-project.png)

3. 设置项目名称和目标语言。您可以稍后在设置中更改语言。
  ![创建项目设置](/img/localizationProgramGuideline/howItWorked/create-project-setting.png)

4. 转到刚刚创建的项目，选择`Integrations`，点击 `Add Integration` 按钮，搜索 `GitHub`，然后安装。
  ![install-github-integration](/img/localizationProgramGuideline/howItWorked/install-github-integration.png)

5. 在 Crowdin 上配置 GitHub 集成之前，请先指定要上传到 Crowdin 的文件，以免上传不必要的文件：

  1. 在**你的 GitHub 仓库**的根目录下创建一个**crowdin.yml**文件，输入以下基本配置：

  ```yml
  project_id: <Your project id>
  preserve_hierarchy: 1
  files:
    - source: <Path of your original files>
      translation: <Path of your translated files>
  ```

  2. 获取正确的配置值：
    - **project_id**：在您的 Crowdin 项目中，转到 `Tools` 选项卡，选择 API，并在其中找到**project_id**。
      ![select-api-tool](/img/localizationProgramGuideline/howItWorked/select-api-tool.png)
      ![projectId](/img/localizationProgramGuideline/howItWorked/projectId.png)
    - **preserve_hierarchy**：是否在 Crowdin 服务器上保持 GitHub 中的目录结构。
    - **source** and **translation**：指定要上传到 Crowdin 的源文件路径(source)和翻译文件(translation)的输出路径。

      For an example, refer to the [**config file**](https://github.com/TownSquareXYZ/ton-docs/blob/localization/crowdin.yml).\
      Find more in the [**Crowdin configuration documentation**](https://developer.crowdin.com/configuration-file/).

6. 配置 Crowdin 以连接到你的 GitHub 仓库：
  1. 单击 `Add Repository` 并选择 `Source and translation files mode`。
    ![选择集成模式](/img/localizationProgramGuideline/howItWorked/select-integration-mode.png)
  2. 连接 GitHub 账户并搜索要翻译的 repo。
    ![search-repo](/img/localizationProgramGuideline/howItWorked/search-repo.png)
  3. Select the branch on the left to generate a new branch where Crowdin will post the translations.
    ![setting-branch](/img/localizationProgramGuideline/howItWorked/setting-branch.png)
  4. Choose the frequency for updating translations to your GitHub branch, then click save to enable the integration.
    ![frequency-save](/img/localizationProgramGuideline/howItWorked/frequency-save.png)

Find more details in the [**GitHub integration documentation**](https://support.crowdin.com/github-integration/).

7. 此外，你可以点击 "立即同步 "按钮，在需要时同步版本库和翻译。

## 术语表

### What is a glossary?

Sometimes, AI translators can't recognize untranslatable and specific terms. For instance, we don't want "Rust" translated when referring to the programming language. To prevent such mistakes, we use a glossary to guide translations.

A **glossary** allows you to create, store, and manage project-specific terminology in one place, ensuring that terms are translated correctly and consistently.

You can reference our [**ton-i18n-glossary**](https://github.com/TownSquareXYZ/ton-i18n-glossary).
![ton-i18n-glossary](/img/localizationProgramGuideline/howItWorked/ton-i18n-glossary.png)

### How to set up a glossary for a new language?

详情请参考 [**GitHub 集成文档**](https://support.crowdin.com/github-integration/)。

In DeepL, upload your glossary, which will be used automatically during AI translation.

我们创建了[**词汇表程序**](https://github.com/TownSquareXYZ/ton-i18n-glossary)，可自动上传更新内容。

在术语表中添加术语：

1. 如果词汇表中已有英文术语，请找到要翻译的语言的相应行和列，输入译文并上传。
2. 要上传新的词汇表，请克隆项目并运行：

```bash
npm i
```

```bash
npm run generate -- <glossary name you want>
```

通过**术语表**，您可以在一个地方创建、存储和管理项目特定术语，确保术语翻译的正确性和一致性。

## How to take advantage of AI translation copilot?

大多数翻译平台都支持词汇表。在 Crowdin 中，设置词汇表后，每个术语都会在编辑器中显示为下划线词。将鼠标悬停在术语上，即可查看其翻译、语篇和定义（如果已在词汇表中提供）。
![github-glossary](/img/localizationProgramGuideline/howItWorked/github-glossary.png)
![crowdin-glossary](/img/localizationProgramGuideline/howItWorked/crowdin-glossary.png)

- **增强一致性**：人工智能翻译以最新信息为基础，提供最准确和最新的翻译。
- **速度与效率**：人工智能翻译瞬时完成，可实时处理大量内容。
- **Robust Scalability**: AI systems continuously learn and improve, enhancing translation quality over time.

We use DeepL for AI translation in our Crowdin project:

1. 在 Crowdin 菜单中选择 `Machine Translation` ，然后点击 DeepL 那一行上的`edit`。
  ![select-deepl](/img/localizationProgramGuideline/howItWorked/select-deepl.png)
2. 启用 DeepL 支持并输入 DeepL Translator API 密钥。
  > [如何获取 DeepL Translator API 密钥](https://www.deepl.com/pro-api?cta=header-pro-api)

![config-crowdin-deepl](/img/localizationProgramGuideline/howItWorked/config-crowdin-deepl.png)

3. 我们的 DeepL 设置使用定制的词汇表。有关上传词汇表的详细信息，请查阅 [**ton-i18n-glossary**](https://github.com/TownSquareXYZ/ton-i18n-glossary) 。

4. 在 repo 中，单击 Pre-translation（预翻译）并选择 via Machine Translation（通过机器翻译）。
  ![预翻译](/img/localizationProgramGuideline/howItWorked/pre-translation.png)

5. Choose DeepL as the Translation Engine, select the target languages, and select the translated files.
  ![pre-translate-config](/img/localizationProgramGuideline/howItWorked/pre-translate-config.png)

That's it! Now, you can take a break and wait for the pre-translation to complete.

<Feedback />

