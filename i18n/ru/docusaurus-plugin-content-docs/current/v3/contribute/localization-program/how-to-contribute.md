# Как внести свой вклад

В нашем стремлении сделать **TON самым успешным блокчейном**, обеспечение того, чтобы документация TON была понятна людям во всем мире, имеет решающее значение. Локализация имеет ключевое значение, и мы **рады**, что вы присоединились к нам в этом начинании.

## Предварительные условия

Программа локализации **TownSquare Labs** открыта для всех! Вот несколько шагов, которые вам необходимо выполнить, прежде чем вы начнете вносить свой вклад:

1. Войдите в свою учетную запись [**Crowdin**](https://crowdin.com) или зарегистрируйтесь.
2. Выберите язык, на котором вы хотите внести свой вклад.
3. Ознакомьтесь с руководством [**Как использовать Crowdin**](/v3/contribute/localization-program/how-to-contribute) и руководством по [**Стилю перевода**](/v3/contribute/localization-program/translation-style-guide) для получения советов и рекомендаций.
4. Используйте машинные переводы для помощи в своей работе, но не полагайтесь исключительно на них.
5. Все результаты перевода можно предварительно просмотреть на веб-сайте через час после исправлений.

## Роли

Вот **роли**, которые вы можете взять на себя в системе:

- **Language Coordinator** - Управляет функциями проекта в рамках назначенных языков.
- **Developer** - Загружает файлы, редактирует переводимый текст, подключает интеграции и использует API.
- **Proofreader** - Переводит и утверждает строки.
- **Translator** (собственный или сообщества) - переводит строки и голосует за переводы,.

Наш проект локализации размещен на [Crowdin](https://crowdin.com/project/ton-docs).

:::info
Before you start contributing, **read the guidelines below** to ensure standardization and quality, making the review process much faster.

## Режим "Бок о бок"

Все задачи выполняются в режиме **бок о бок** в редакторе Crowdin. Чтобы включить его, щелкните файл, над которым вы хотите работать. В правом верхнем углу страницы щелкните кнопку **Вид редактора** и выберите режим **бок о бок"** для более удобного просмотра в редакторе.
![Режим "бок о бок"](/img/localizationProgramGuideline/side-by-side.png)
:::

### Language Coordinator

- **Переводите и утверждайте строки**
- **Предварительно переводите содержимое проекта**
- **Управляйте участниками проекта и запросами на присоединение**
  ![manage-members](/img/localizationProgramGuideline/manage-members.png)
- **Создавайте отчеты по проекту**
  ![generate-reports](/img/localizationProgramGuideline/generate-reports.png)
- **Создавайте задачи**
  ![create-tasks](/img/localizationProgramGuideline/create-tasks.png)

### Developer

- **Обновление конфигурации нижнего колонтитула для вашего языка:**
  1. Создайте ответвление нашего [**репозитория**](https://github.com/TownSquareXYZ/ton-docs/tree/i18n_feat).
  2. Перейдите к файлу [**`src/theme/Footer/config.ts`**] (https://github.com/TownSquareXYZ/ton-docs/blob/main/src/theme/Footer/config.ts).
  3. Скопируйте значение переменной **`FOOTER_COLUMN_LINKS_EN`** в **`FOOTER_COLUMN_LINKS_[YOUR_LANG]`**.
  4. Переведите значения ключей **`headerLangKey`** и **`langKey`** на ваш язык, как мы это сделали для мандаринского в **`FOOTER_COLUMN_LINKS_CN`**.
  5. Добавьте новое свойство в **`FOOTER_LINKS_TRANSLATIONS`**:
     - Установите **ключ** как ваш [**код языка ISO**](https://www.andiamo.co.uk/resources/iso-language-codes/) (**две буквы**, **нижний регистр**).
     - **Значение** должно быть новой переменной, которую вы только что создали для вашего языка.
  6. Выполните команду **`yarn start:local [YOUR_IOS_LANG_CODE]`**, чтобы просмотреть новый нижний колонтитул на вашем языке.\
     (например, **`yarn start:local ru`** для предварительного просмотра на **русском** языке)
  7. Если все выглядит хорошо, создайте pull request в ветку **`i18n_feat`**.
- **Загрузите файлы**
- **Отредактируйте переводимый текст**
- **Подключите интеграции** (например, добавьте интеграцию с GitHub)
  ![install-github-integration](/img/localizationProgramGuideline/howItWorked/install-github-integration.png)
- **Используйте [Crowdin API](https://developer.crowdin.com/api/v2/)**

### Proofreader

Как **Proofreader**, вы будете работать с файлами с **синим индикатором выполнения**.
![proofread step1](/img/localizationProgramGuideline/proofread-step1.png)
Щелкните на файле, чтобы войти в интерфейс редактирования.

#### Давайте начнем вносить свой вклад

1. Убедитесь, что вы работаете в [**режиме бок о бок**](#side-by-side-mode). Отфильтруйте **неутвержденные** переводы, чтобы увидеть строки, требующие проверки..
   ![proofread](/img/localizationProgramGuideline/proofread-filter.png)

2. Соблюдайте следующие правила:
   - Выберите строки с **синим прямоугольным значком**. Проверьте каждый перевод:
     - Если **правильный**, нажмите кнопку ☑️.
     - Если **неправильный**, перейдите к следующей строке.

![proofread approved](/img/localizationProgramGuideline/proofread-approved.png)

:::info
You can also review approved lines:

1. Фильтр по **утвержденным**.

2. Если в утвержденной строке есть проблемы, нажмите кнопку ☑️, чтобы вернуть ее к требующей проверки.
   :::

3. Чтобы перейти к следующему файлу, щелкните имя файла вверху, выберите новый файл во всплывающем окне и продолжите проверку.
   ![to next](/img/localizationProgramGuideline/redirect-to-next.png)

#### Предварительный просмотр вашей работы

Все одобренные материалы будут размещены на веб-сайте предварительного просмотра в течение одного часа. Ознакомьтесь с [**нашим репозиторием**](https://github.com/TownSquareXYZ/ton-docs/pulls) на наличие ссылки предварительного просмотра в последнем PR.
![preview link](/img/localizationProgramGuideline/preview-link.png)

### Translator

Ваша цель как **Translator** — обеспечить точность и выразительность переводов, максимально приблизив их к исходному значению и сделав максимально понятными. Ваша миссия — довести **синюю полосу выполнения** до 100%.

#### Давайте начнем перевод

Для успешного процесса перевода выполните следующие шаги:

1. Выберите файлы, которые не достигли 100% перевода.
   ![translator select](/img/localizationProgramGuideline/translator-select.png)

2. Убедитесь, что вы находитесь в [**режиме бок о бок**](#side-by-side-mode). Фильтр по **непереведенным** строкам.
   ![translator filter](/img/localizationProgramGuideline/translator-filter.png)

3. Ваше рабочее пространство состоит из четырех частей:
   - **Сверху слева:** введите свой перевод на основе исходной строки.
   - **Снизу слева:** предварительный просмотр переведенного файла. Сохраните исходный формат.
   - **Снизу справа:** предлагаемые переводы от Crowdin. Нажмите, чтобы использовать, но проверьте точность, особенно со ссылками.

4. Сохраните свой перевод, нажав кнопку **Сохранить** вверху.
   ![translator save](/img/localizationProgramGuideline/translator-save.png)

5. Чтобы перейти к следующему файлу, щелкните имя файла вверху и выберите новый файл во всплывающем окне.
   ![to next](/img/localizationProgramGuideline/redirect-to-next.png)

## Как добавить поддержку нового языка

В настоящее время в Crowdin есть все нужные языки. Если вы являетесь менеджером сообщества, выполните следующие действия:

1. Добавьте новую ветку с именем `[lang]_localization` (например, `ko_localization` для корейского языка) в [TownSquareXYZ/ton-docs](https://github.com/TownSquareXYZ/ton-docs).
2. **Свяжитесь с владельцем этого репозитория Vercel**, чтобы добавить новый язык в меню.
3. Создайте PR-запрос в ветку dev. **Не объединяйте с dev**; это нужно только для целей предварительного просмотра.

После завершения этих действий вы сможете увидеть предварительный просмотр своего языка в запросе на PR.
![ko preview](/img/localizationProgramGuideline/ko_preview.png)

Когда ваш язык будет готов для документации TON, создайте issue, и мы добавим ваш язык в производственную среду.