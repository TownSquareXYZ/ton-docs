# TON API на основе HTTP

:::tip

Существует несколько способов подключения к блокчейну:

1. **RPC-провайдер данных или другой API**: в большинстве случаев вы должны *полагаться* на его стабильность и безопасность.
2. ADNL-соединение: вы подключаетесь к [liteserver](/v3/guidelines/nodes/running-nodes/liteserver-node). Они могут быть недоступны, но при определенном уровне проверки (реализованном в библиотеке) не могут лгать.
3. Двоичный файл Tonlib: вы также подключаетесь к liteserver, поэтому все преимущества и недостатки остаются, но ваше приложение также содержит библиотеку с динамической загрузкой, скомпилированную вне.
4. Только для Offchain. Такие SDK позволяют создавать и сериализовать ячейки, которые затем можно отправить в API.

:::

## Плюсы и минусы

- ✅ Привычный и подходит для быстрого старта, это идеально для всех новичков, которые хотят поиграть с TON.

- ✅ Веб-ориентированный. Отлично подходит для загрузки данных из умных контрактов TON через веб и также позволяет отправлять сообщения.

- ❌ Упрощенный. Нет возможности получать информацию, где требуется индексированный API TON.

- ❌ HTTP-посредник.  Вы не можете полностью доверять ответам сервера,  если он не расширяет данные блокчейна с использованием [Merkle proofs](/v3/documentation/data-formats/tlb/proofs) для подтверждения их подлинности.

## Мониторинг

- [status.toncenter](https://status.toncenter.com/) - показывает все полные узлы сети и валидаторы, активные за последние часы, а также различные статистические данные.
- [Tonstat.us](https://tonstat.us/) - предоставляет приборную панель на основе Grafana, отображающую статус всех API, связанных с TON, с обновлением данных каждые 5 минут.

## Узлы RPC

- [QuickNode](https://www.quicknode.com/chains/ton?utm_source=ton-docs) - Ведущий поставщик узлов для блокчейна, предлагающий самый быстрый доступ с помощью интеллектуальной DNS-маршрутизации для оптимизации глобального охвата и масштабируемости с балансировкой нагрузки.
- [Chainstack](https://chainstack.com/build-better-with-ton/) - узлы RPC и индексатор в нескольких регионах с географическим распределением и балансировкой нагрузки.
- [Tatum](https://docs.tatum.io/reference/rpc-ton) - доступ к RPC узлам TON и мощным инструментам разработчика в одной простой для использования платформе.
- [GetBlock Nodes](https://getblock.io/nodes/ton/) - подключитесь и протестируйте свои dApps с использованием узлов GetBlock
- [TON Access](https://www.orbs.com/ton-access/) - HTTP API для The Open Network (TON).
- [Toncenter](https://toncenter.com/api/v2/) - хостинг проект сообщества для быстрого старта с помощью API. (Получите API ключ[@tonapibot](https://t.me/tonapibot))
- [ton-node-docker](https://github.com/fmira21/ton-node-docker) - Docker Full Node и Toncenter API.
- [toncenter/ton-http-api](https://github.com/toncenter/ton-http-api) - запустите свой собственный узел RPC.
- [nownodes.io](https://nownodes.io/nodes) - Полный узел NOWNodes and проводники блоков Blockbook через API.
- [Chainbase](https://chainbase.com/chainNetwork/TON) - API узлов и инфраструктура данных для The Open Network.

## Индексатор

### Toncenter TON Index

Индексаторы позволяют получать списки jetton кошельков, NFT, транзакций по определенным фильтрам, а не только извлекать конкретные данные.

- TON Index может быть использован: для тестов и разработки - бесплатно, [premium](https://t.me/tonapibot) для производства - [toncenter.com/api/v3/](https://toncenter.com/api/v3/).
- Запустите свой собственный TON Index с помощью [Worker](https://github.com/toncenter/ton-index-worker/tree/36134e7376986c5517ee65e6a1ddd54b1c76cdba) и [TON Index API wrapper](https://github.com/toncenter/ton-indexer).

### Anton

Написанный на языке Go, Anton - это блокчейн-индексатор The Open Network с открытым исходным кодом, доступный по лицензии Apache License 2.0. Anton разработан, чтобы предоставить разработчикам масштабируемое, гибкое решение для доступа и анализа данных блокчейна. Наша цель - помочь разработчикам и пользователям понять, как используется блокчейн, и сделать так, чтобы разработчики могли добавлять в наш проводник свои собственные контракты с настраиваемыми схемами сообщений.

- [Проект GitHub](https://github.com/tonindexer/anton) - для запуска собственного индексатора
- [Документация по API Swagger](https://github.com/tonindexer/anton), [Примеры запросов к API](https://github.com/tonindexer/anton/blob/main/docs/API.md) - чтобы использовать, изучите документацию и примеры
- [Apache Superset](https://github.com/tonindexer/anton) - используйте для просмотра данных

### GraphQL Nodes

Узлы GraphQL также выступают в роли индексаторов.

- [dton.io](https://dton.io/graphql) помимо предоставления данных о контрактах, дополненных проанализированными флагами "is jetton", "is NFT", позволяет эмулировать транзакции и получать трассировки выполнения.

## Другие API

- [TonAPI](https://docs.tonconsole.com/tonapi) - API, разработанный для предоставления пользователям удобного опыта работы, не заботясь о низкоуровневых деталях умных контрактов.