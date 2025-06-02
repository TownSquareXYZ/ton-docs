import Feedback from '@site/src/components/Feedback';

# 如何参与贡献

This page explains how to participate in the localization program for TON documentation.

## 预备流程

Localization contribution is open to everyone. Here are a few steps you need to take before you start contributing:

1. Log in to your [Crowdin](https://crowdin.com) account or sign up.
2. 选择您要贡献的语言。
3. Familiarize yourself with the [How to use crowdin](/v3/contribute/localization-program/how-to-contribute/) guide and the [Translation style guide](/v3/contribute/localization-program/translation-style-guide/) for tips and best practices.
4. Use machine translations to aid your work, but do not rely solely on them.
5. Preview all translation results on the website after proofreading.

:::info
Before contributing, read the guidelines below to ensure standardization and quality, speeding up the review process.
:::

## Side-by-side mode

All tasks are performed in **side-by-side** mode in the Crowdin Editor. To enable this, click a file you want to work on. At the top right of the page, click the **Editor view** button and select **side-by-side** mode for a clearer editor view.\
![side-by-side mode](/img/localizationProgramGuideline/side-by-side.png)

## 角色

以下是您在系统中可以担任的**角色**：

- **语言协调员(Language Coordinator)** - 管理指定语言的项目功能。
- **Developer** – Uploads files, edits translatable text, connects integrations and uses the API.
- **校对员(Proofreader)** - 翻译和批准字符串。
- **翻译员(Translator)** - 翻译字符串并对他人添加的翻译进行投票。

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
  2. 来到以下文件 [**`src/theme/Footer/config.ts`**](https://github.com/TownSquareXYZ/ton-docs/blob/main/src/theme/Footer/config.s).
  3. 将变量\*\*`FOOTER_COLUMN_LINKS_EN`\*\* 的值复制到\*\*`FOOTER_COLUMN_LINKS_[YOUR_LANG]`\*\*。
  4. 就如我们在 \*\*`FOTER_COLUMN_LINKS_CN`\*\*中对Mandarin 所做的那样，您也可以将 **`headerLangKey`** 和 **`langKey`** 的键值翻译成您的语言，
  5. 向\*\*`FOOTER_LINKS_TRANSLATIONS`\*\*添加一个新属性：
    - 将 **the key** 设置为您的 [**国际标准组的语言代码**](https://www.andiamo.co.uk/resources/iso-language-codes/) (注意使用**两个英语字母**, **小写**，eg：zh)。
    - **The value** should be the new variable you created for your language.
  6. 您可以运行命令 **`yarn start:local [YOUR_IOS_LANG_CODE]`** 来预览您的语言的新页脚。\
    (例如\*\*`yarn start:local zh`\*\* 用于预览**汉语** 页脚)
  7. 如果一切看起来都没问题，请在 **`i18n_feat`** 分支上创建一个拉取请求。
- **编辑可翻译文本**
- **连接集成**（例如，添加 GitHub 集成）
  ![install-github-integration](/img/localizationProgramGuideline/howItWorked/install-github-integration.png)
- **使用 [Crowdin API](https://developer.crowdin.com/api/v2/)**
- **使用 [Crowdin API](https://developer.crowdin.com/api/v2/)**

### Proofreader guidelines

作为**校对员**，您将处理带有**蓝色进度条**的文件。
![proofread step1](/img/localizationProgramGuideline/proofread-step1.png)
点击文件进入编辑界面。

#### Contribution flow

1. 确保您处于 [**side-by-side 模式**](#side-by-side-mode)。启用**Not Approved**过滤，查看需要校对的字符串。
  ![校对过滤器](/img/localizationProgramGuideline/proofread-filter.png)

2. 请遵守这些规则：
  - 选择带有**蓝色立方体图标**的字符串。检查每个翻译：
    - 如果**正确**，请单击 ☑️ 按钮。
    - 如果**不正确**，请移至下一行。

![校对通过](/img/localizationProgramGuideline/proofread-approved.png)

:::info
You can also review the approved lines:

1. 使用**Approved**过滤选项。

2. 如果已批准的翻译有问题，请单击 ☑️ 按钮将其还原为需要校对的状态。
  :::

3. To move to the following file, click the file name at the top, select the new file from the pop-up window, and continue proofreading.
  ![to next](/img/localizationProgramGuideline/redirect-to-next.png)

#### Previewing your work

The preview website displays all approved content within one hour. Check [**our repo**](https://github.com/TownSquareXYZ/ton-docs/pulls) for the **preview** link in the newest PR.
![preview link](/img/localizationProgramGuideline/preview-link.png)

### Translator guidelines

As a translator, you aim to ensure that translations are faithful and expressive, keeping them as close to the original meaning and as understandable as possible. Your mission is to make the blue progress bar reach 100%.

#### Translation flow

请按照以下步骤成功完成翻译过程：

1. 选择尚未达到 100% 翻译的文件。
  ![翻译选择](/img/localizationProgramGuideline/translator-select.png)

2. 确保您处于 [**side-by-side 模式**](#side-by-side-mode)。通过**Untranslated**字符串进行过滤。
  ![翻译过滤器](/img/localizationProgramGuideline/translator-filter.png)

3. 您的工作区有四个部分：
  - **左上：** 根据源字符串输入您的翻译。
  - **左下：** 预览翻译文件。保持原始格式。
  - **右下：** Crowdin 建议的翻译。点击使用，但请核实准确性，尤其是链接。

4. 点击顶部的**Save**按钮保存翻译。
  ![translator save](/img/localizationProgramGuideline/translator-save.png)

5. 要移动到下一个文件，请单击顶部的文件名，然后从弹出窗口中选择新文件。
  ![转到下一个](/img/localizationProgramGuideline/redirect-to-next.png)

## How to add support for a new language

If you are a community manager, follow these steps:

1. 在 [TownSquareXYZ/ton-docs](https://github.com/TownSquareXYZ/ton-docs) 上添加一个名为 `[lang]_localization`（例如，韩语为 `ko_localization`）的新分支。
2. **请联系此仓库的 Vercel 所有者**，将新语言添加到菜单中。
3. 向开发分支创建 PR 请求。**请勿合并到开发分支**；这仅供预览之用。

Once you complete these steps, you can see the preview of your language in the PR request.
![ko preview](/img/localizationProgramGuideline/ko_preview.png)

当您的语言准备好在 TON 文档中展示时，请创建一个issue，我们会将您的语言设置到生产环境中。

<Feedback />

