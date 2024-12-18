# Обзор

Цель этого статьи - помочь вам выбрать правильные инструменты для разработки приложений в экосистеме TON.

## Разработка TMA

- Используйте [Mini Apps SDKs](/v3/guidelines/dapps/tma/overview#mini-apps-sdks) для разработки [Мини приложений Telegram](/v3/guidelines/dapps/tma/overview).
- Выберите [SDK, базирующийся на JS/TS](/v3/guidelines/dapps/apis-sdks/sdk#typescript--javascript) для взаимодействия с блокчейном TON.

## Разработка DApps

- Используйте Tolk, FunC или Tact [языки программирования](/v3/documentation/smart-contracts/overview#programming-languages), если требуется разработка умных контрактов на блокчейне TON для вашего [DApp](/v3/guidelines/dapps/overview).
- Чтобы взаимодействовать с блокчейном TON и обрабатывать его данные, выберите один из перечисленных [SDK](/v3/guidelines/dapps/apis-sdks/sdk). Одними из самых популярных языков для этого назначения:
  - [JS/TS](/v3/guidelines/dapps/apis-sdks/sdk#typescript--javascript)
  - [Go](/v3/guidelines/dapps/apis-sdks/sdk#go)
  - [Python](/v3/guidelines/dapps/apis-sdks/sdk#python)
- Чтобы интегрировать аутентификацию пользователей с их кошельками TON (включая логику обработки платежей) в ваш DApp, используйте [TON Connect](/v3/guidelines/ton-connect/overview).

## Анализатор статистики TON

Вам может понадобиться быстрое взаимодействие с блокчейном TON или сбор и анализ его данных. Для этих целей может быть полезно запустить свой собственный [Ton Node] (/v3/documentation/infra/nodes/node-types).

- [Liteserver узел](/v3/guidelines/nodes/running-nodes/liteserver-node) - только для взаимодействия с блокчейном.
- [Архивный узел](/v3/guidelines/nodes/running-nodes/archive-node) - сбор расширенных исторических данных блокчейна.

Используйте SDK с встроенной поддержкой [ADNL](/v3/documentation/network/protocols/adnl/adnl-tcp):

- [Go](https://github.com/xssnick/tonutils-go)
- [Python](https://github.com/yungwine/pytoniq)

## См. также

- [SDK](/v3/guidelines/dapps/apis-sdks/sdk)
- [Руководства по разработке TMA](/v3/guidelines/dapps/tma/tutorials/step-by-step-guide)
- [Руководства по TON Connect](/v3/guidelines/ton-connect/guidelines/how-ton-connect-works)
- [Обработка платежей](/v3/guidelines/dapps/asset-processing/payments-processing)
