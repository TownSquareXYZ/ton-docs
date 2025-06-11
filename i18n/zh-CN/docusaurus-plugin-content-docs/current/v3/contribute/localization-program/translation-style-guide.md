import Feedback from '@site/src/components/Feedback';

# 翻译风格指南

This translation style guide contains essential guidelines, instructions, and tips for translators, helping us localize the website.

This document serves as a general guide and is not specific to any language.

## 理解信息的精髓

当翻译 TON 文档内容时，避免直译。

The translations must capture the essence of the message. This approach means rephrasing specific phrases or using descriptive translations instead of translating the content word for word.

Different languages have different grammar rules, conventions, and word order. When translating, please be mindful of structuring sentences in the target languages, and avoid word-for-word translation of the English source, as this can lead to poor sentence structure and readability.

Instead of translating the source text word for word, you should read the entire sentence and adapt it to fit the conventions of the target language.

## 正式与非正式

我们使用正式的称呼形式，这对所有访客来说始终是礼貌和适当的。

Using the formal address allows us to avoid sounding unofficial or offensive and works regardless of the reader’s age and gender.

Most Indo-European and Afro-Asiatic languages use gender-specific second-person personal pronouns, distinguishing between males and females. When addressing the user or using possessive pronouns, we can avoid assuming the reader’s gender, as the formal address is generally applicable and consistent, regardless of how they identify.

## Straightforward vocabulary and meaning

我们的目标是让尽可能多的人能够理解网站上的内容。

In most cases, contributors can achieve this result by using short and simple words that are easily understandable. If multiple possible translations exist for a word in your language with the same meaning, the best option is often the shortest word reflecting the meaning.

## 书写系统

All of the content should be translated using the correct writing system for your language and should not include any words written using Latin characters.

翻译内容时，应确保翻译内容一致且不包含任何拉丁字符。

**Do not translate proper names defined by glossary**

## 翻译页面元数据

Some pages contain metadata, such as 'title', 'lang', 'description', 'sidebar', etc.

When uploading new pages to Crowdin, we hide content that translators should never translate. This feature makes visible to translators in Crowdin only the text that should be translated.

Please be especially careful when translating strings where the source text is 'en'. This represents the language page, which is available and should be translated to the [ISO language code for your language](https://www.andiamo.co.uk/resources/iso-language-codes/). These strings should always be translated using Latin characters, not the writing script, native to the target language.

使用最广泛的语言的语言代码示例：

- 英文 - en
- 简体中文 - zh-CN
- 俄语 - ru
- 韩语 - ko
- 波兰语 - pl
- 乌克兰语 - uk

## 外部文章标题

Some strings contain titles of external articles. Most of our developer documentation pages contain links to external articles for further reading. The strings containing article titles need to be translated, regardless of the article's language, to ensure a more consistent user experience for visitors viewing the page in their language.

## Crowdin 警告

Crowdin has a built-in feature that warns translators when they are about to make a mistake. Crowdin will automatically alert you before saving your translation if you forget to include a tag from the source, translate elements that should not be translated, add several consecutive spaces, forget end punctuation, etc. If you see a warning like this, please double-check the suggested translation.

:::warning
Never ignore these warnings, as they usually mean something is wrong or the translation lacks a key part of the source text.
:::

## Short vs. complete forms and abbreviations

The website uses many abbreviations, such as apps, DApps, NFT, DAO, DeFi, etc. These abbreviations are standard in English, and most visitors are familiar with them.

Since they usually don’t have established translations in other languages, the best approach to these and similar terms is to provide a descriptive translation of the entire form and add the English abbreviation in brackets.

Do not translate these abbreviations since most people are unfamiliar with them, and the localized versions would not make much sense to most visitors.

Example of how to translate DApps:

- Decentralized applications (DApps) → Translated in complete form (English abbreviation in brackets)

## 没有既定翻译的术语

Some terms might not have established translations in other languages but are widely known by their original English names. Such terms include newer concepts, like proof-of-work, proof-of-stake, Beacon Chain, staking, etc.

While translating these terms can sound unnatural, since the English version is a basis for other languages, it is highly recommended that they be translated.

Feel free to get creative, use descriptive translations, or translate them literally.

Most terms should be translated instead of leaving some in English, as this new terminology will become more widespread as more people start using TON and related technologies. To onboard more people to TON, we must provide understandable terminology in as many languages as possible, even if we need to create it ourselves.

## 按钮与行动号召

Do not translate the website's contents, such as buttons.

You may identify button text by viewing the context screenshots connected with most strings or by checking the context in the editor, which includes the phrase ‘’button’’.

Button translations should be as short as possible to prevent formatting mismatches. Additionally, button translations, i.e., presenting a command or request, should be imperative.

## 翻译包容性

TON docs visitors come from all over the world and from different backgrounds. Therefore, the language on the website should be neutral, welcoming to everyone, and not exclusive.

Gender neutrality is an essential aspect of this. Use the formal address form and avoid gender-specific words in the translations.

Another form of inclusivity is trying to translate for a global audience, not specific to any country, race, or region.

最后，语言应该适合所有大众和年龄段的读者。

## 特定语言的翻译

When translating, it is crucial to follow the grammar rules, conventions, and formatting used in your language instead of copying from the source. The source text follows English grammar rules and conventions, which do not apply to many other languages.

You should be aware of the rules for your language and translate accordingly. If you need help, contact us; we will help you with resources on translating elements for your language.

一些需要特别注意的例子：

### 标点、格式

#### 大写

- 不同语言的大小写存在巨大差异。
- 在英语中，通常将标题和名称、月份和日期、语言名称、假期等中的所有单词大写。 在许多其他语言中，这在语法上是不正确的，因为它们具有不同的大小写规则。
- Some languages also have rules about capitalizing personal pronouns, nouns, and adjectives that you shouldn't capitalize in English.

#### 间距

- 正字法规则定义了每种语言的空格使用。 因为到处都使用空格，所以这些规则是最独特的，而空格是最容易误译的元素。
- 英语和其他语言之间的一些常见间距差异：
  - Space before units of measure and currencies. Example: USD, EUR, kB, MB
  - Space before degree signs. Example: °C, ℉
  - Space before some punctuation marks, especially the ellipsis. Example: Then… in summary
  - Space before and after slashes. Example: if / else

#### 列表

- Every language has a diverse and complex set of rules for writing lists. These can be significantly different from English.
- In some languages, the first word of each new line needs to be capitalized, while in others, new lines should start with lowercase letters. Many languages also have different rules about capitalization in lists, depending on the length of each line.
- The same applies to the punctuation of line items. The end punctuation in lists can be a period (.), comma (,), or semicolon (;), depending on the language.

#### 引号

- 语言使用许多不同的引号。 简单地从源中复制英文引号通常是不正确的。
- 一些最常见的引号类型包括：
  - “示例文本”
  - ‘示例文本’
  - »示例文本«
  - “示例文本”
  - ‘示例文本’
  - «示例文本»

#### 连字符和破折号

- In English, a hyphen `-` is used to join words or different parts of a word, while a dash `—` indicates a range or a pause.
  - Example: TON — is ... proof-of-stake.
- Many languages have different rules for using hyphens and dashes that should be observed.

### Formats

#### Numbers

- The main difference in writing numbers in different languages is the separator for decimals and thousands. For thousands, this can be a period, comma, or space. Similarly, some languages use a decimal point, while others use a decimal comma.
  - Example:
    - English – **1,000.50**
    - Spanish – **1.000,50**
    - French – **1 000,50**
- The percent sign is another critical consideration when translating numbers. Write numbers in the typical format for the corresponding language.
  - Example: **100%**, **100 %**, or **%100**.
- Finally, negative numbers can be displayed differently, depending on the language
  - Example: -100, 100-, (100) or [100].

#### 日期

- When translating dates, there are several considerations and differences based on the language. These include the date format, separator, capitalization, and leading zeros. There are also differences between full-length and numerical dates.
  - 不同日期格式的一些示例：
    - 英语（英国）(dd/mm/yyyy) – 1st January, 2022
    - 英语（美国）(mm/dd/yyyy) – January 1st, 2022
    - 中文 (yyyy-mm-dd) – 2022 年 1 月 1 日
    - 法语 (dd/mm/yyyy) – 1er janvier 2022
    - 意大利语 (dd/mm/yyyy) – 1º gennaio 2022
    - 德语 (yyyy/mm/dd) – 1. Januar 2022

#### 货币

- Translating currencies can be challenging due to the different formats, conventions, and conversions. As a general rule, please keep currencies the same as the source. You can add your local currency and conversion in brackets for the reader's benefit.
- 用不同语言书写货币的主要区别包括符号位置、小数逗号与小数点、间距以及缩写与符号。
  - 符号放置：美元 100或 100 美元
  - 小数逗号和。小数点：100,50$ 或 100.50$
  - 间距：100美元或 100 美元
  - 缩写和符号：100$ 或 100 USD

#### 计量单位

- As a general rule, please keep the units of measure as per the source. You can include the conversion in brackets if your country uses a different system.
- Aside from the localization of units of measure, it is also important to note the differences in how languages approach these units. The main difference is the spacing between the number and unit, which can differ based on the language. Examples of this include 100kB vs. 100 kB or 50ºF vs. 50 ºF.

## 结论

翻译时尽量不要着急。 放轻松，玩得开心！

Thank you for helping us localize the website and make it accessible to a wider audience. The TON community is global, and we are happy you are a part of it!

<Feedback />

