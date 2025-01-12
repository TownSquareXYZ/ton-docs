# Сминтите свой первый Jetton

Добро пожаловать,  разработчик! Очень приятно видеть Вас здесь. 👋

В этой статье мы расскажем Вам о создании Вашего первого взаимозаменяемого токена (Jetton) на TON.

Для минта жетонов мы будем использовать браузерный сервис [TON Minter](https://minter.ton.org/) / [TON Minter testnet](https://minter.ton.org/?testnet=true).

## 📖 Чему Вы научитесь

В этой статье Вы узнаете, как:

- развернуть жетон с помощью браузера
- настроить свой токен
- управлять и использовать Ваш токен
- отредактировать параметры токена

## 📌 Подготовьтесь перед началом работы

1. Для начала Вам необходимо иметь кошелек [Tonhub](https://ton.app/wallets/tonhub-wallet) / [Tonkeeper](https://ton.app/wallets/tonkeeper) или любой другой, поддерживаемый на сервисе.
2. На Вашем балансе должно быть более 0,25 Toncoin и дополнительные средства для покрытия комиссии за блокчейн.

:::tip Совет на старте
~0,5 TON должно быть достаточно для этого урока.
:::

## 🚀 Давайте начнем!

С помощью веб-браузера откройте сервис [TON Minter](https://minter.ton.org/) / [TON Minter testnet](https://minter.ton.org/?testnet=true).

![image](/img/tutorials/jetton/jetton-main-page.png)

### Разверните жетон с помощью браузера

#### Подключите кошелек

Нажмите кнопку `Подключить кошелек`, чтобы подключить Ваш кошелек [Tonhub](https://ton.app/wallets/tonhub-wallet) или другой кошелек из представленных ниже.

#### ![image](/img/tutorials/jetton/jetton-connect-wallet.png)

**Просканируйте QR-код** в [Мобильном кошельке (Tonhub, например)](https://ton.app/wallets/tonhub-wallet)

#### Заполните пустые места соответствующей информацией

1. Название (обычно 1-3 слова).
2. Символ (обычно 3-5 заглавных символов).
3. Сумма (например, 1,000,000).
4. Описание токена (необязательно).

#### URL-адрес логотипа токена (необязательно)

![image](/img/tutorials/jetton/jetton-token-logo.png)

Если Вы хотите иметь привлекательный токен Jetton, Вам нужно где-то разместить красивый логотип. Например:

- https://bitcoincash-example.github.io/website/logo.png

:::info
You can easily find out  about url placement of the logo in the [repository](https://github.com/ton-blockchain/minter-contract#jetton-metadata-field-best-practices) in paragraph "Where is this metadata stored".

- On-chain.
- Off-chain IPFS.
- Off-chain веб-сайт.
  :::

#### Как создать URL-адрес своего логотипа?

1. Подготовьте **256x256** PNG-изображение логотипа токена с прозрачным фоном.
2. Получите ссылку на свой логотип. Хорошим решением является [GitHub Pages](https://pages.github.com/). Давайте воспользуемся им.
3. [Создайте новый публичный репозиторий](https://docs.github.com/en/get-started/quickstart/create-a-repo) с именем `website`.
4. Загрузите подготовленное изображение в git и включите `GitHub Pages`.
   1. [Добавьте страницы GitHub в свой репозиторий](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site).
   2. [Загрузите свое изображение и получите ссылку](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).
5. Если у Вас есть собственный домен, то лучше использовать `.org` вместо `github.io`.

## 💸 Отправить жетоны

В правой части экрана Вы можете **отправить токены** на мультивалютные кошельки, такие как [Tonkeeper](https://tonkeeper.com/) или [Tonhub](https://ton.app/wallets/tonhub-wallet).

![image](/img/tutorials/jetton/jetton-send-tokens.png)

:::info
You always also **burn** your Jettons to reduce their amount.

![image](/img/tutorials/jetton/jetton-burn-tokens.png)
:::

### 📱 Отправляйте токены с телефона с помощью Tonkeeper

Пререквизиты:

1. Чтобы отправить их, у Вас на балансе уже должны быть токены.
2. Для оплаты транзакционных сборов должно быть не менее 0,1 Тонкоина.

#### Пошаговое руководство

Затем перейдите к **Вашему токену**, установите **сумму** для отправки и введите **адрес получателя**.

![image](/img/tutorials/jetton/jetton-send-tutorial.png)

## 📚 Использование токена на сайте

Вы можете получить доступ к **полю поиска** в верхней части сайта, введя адрес токена, чтобы управлять им как владелец.

:::info
The address can be found on the right side if you are already in the owner panel, or you can find the token address when receiving an airdrop.

![image](/img/tutorials/jetton/jetton-wallet-address.png)
:::

## ✏️ Настройка жетона (токена)

С помощью языка [FunC](/v3/documentation/smart-contracts/func/overview) Вы можете изменить поведение токена в свою пользу.

Чтобы внести изменения, начните отсюда:

- https://github.com/ton-blockchain/minter-contract

### Пошаговое руководство для разработчиков

1. Убедитесь, что у Вас есть все "Зависимости и требования" из репозитория [tonstarter-contracts](https://github.com/ton-defi-org/tonstarter-contracts).
2. Клонируйте репозиторий [minter-contract repository](https://github.com/ton-blockchain/minter-contract) и переименуйте проект.
3. Для установки Вам необходимо открыть терминал с правами root и запустить его:

```bash npm2yarn
npm install
```

4. Отредактируйте оригинальные файлы смарт-контрактов таким же образом в корневом терминале. Все файлы контрактов находятся в папке `contracts/*.fc`.

5. Создайте проект с помощью:

```bash npm2yarn
npm run build
```

Результат сборки будет описывать процесс создания необходимых файлов, а также поиск смарт-контрактов.

:::info
Просмотрите консоль, там много советов!
:::

6. Вы можете протестировать свои изменения, используя:

```bash npm2yarn
npm run test
```

7. Отредактируйте **имя** и другие метаданные токена в файле `build/jetton-minter.deploy.ts`, изменив объект JettonParams.

```js
// This is example data - Modify these params for your own jetton!
// - Data is stored on-chain (except for the image data itself)
// - Owner should usually be the deploying wallet's address.
  
const jettonParams = {
 owner: Address.parse("EQD4gS-Nj2Gjr2FYtg-s3fXUvjzKbzHGZ5_1Xe_V0-GCp0p2"),
 name: "MyJetton",
 symbol: "JET1",
 image: "https://www.linkpicture.com/q/download_183.png", // Image url
 description: "My jetton",
};
```

8. Чтобы развернуть токен, выполните следующую команду:

```bash npm2yarn
npm run deploy
```

Результат выполнения Вашего проекта:

````
```js
> @ton-defi.org/jetton-deployer-contracts@0.0.2 deploy
> ts-node ./build/_deploy.ts

=================================================================
Deploy script running, let's find some contracts to deploy..

* We are working with 'mainnet'

* Config file '.env' found and will be used for deployment!
 - Wallet address used to deploy from is: YOUR-ADDRESS
 - Wallet balance is YOUR-BALANCE TON, which will be used for gas

* Found root contract 'build/jetton-minter.deploy.ts - let's deploy it':
 - Based on your init code+data, your new contract address is: YOUR-ADDRESS
 - Let's deploy the contract on-chain..
 - Deploy transaction sent successfully
 - Block explorer link: https://tonwhales.com/explorer/address/YOUR-ADDRESS
 - Waiting up to 20 seconds to check if the contract was actually deployed..
 - SUCCESS! Contract deployed successfully to address: YOUR-ADDRESS
 - New contract balance is now YOUR-BALANCE TON, make sure it has enough to pay rent
 - Running a post deployment test:
{
  name: 'MyJetton',
  description: 'My jetton',
  image: 'https://www.linkpicture.com/q/download_183.png',
  symbol: 'JET1'
}
```
````

## Что дальше?

Если Вы хотите углубиться, прочтите эту статью Tal Kol:

- [Как и почему нужно чередовать смарт-контракты — изучаем анатомию TON Jettons](https://blog.ton.org/how-to-shard-your-ton-smart-contract-and-why-studying-the-anatomy-of-tons-jettons)

## Ссылки

- Проект: https://github.com/ton-blockchain/minter-contract
- Slava ([Telegram @delovoyslava](https://t.me/delovoyslava), [delovoyhomie на GitHub](https://github.com/delovoyhomie))
- [Обработка жетонов](/v3/guidelines/dapps/asset-processing/jettons)
