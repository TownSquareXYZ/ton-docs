# Highload Wallet

При работе с большим количеством сообщений за короткий период времени необходим специальный кошелек под названием Highload Wallet. Highload Wallet V2 долгое время был основным кошельком на TON, но с ним нужно было быть очень осторожным. В противном случае можно было [заблокировать все средства](https://t.me/tonstatus/88).

[С появлением Highload Wallet V3](https://github.com/ton-blockchain/Highload-wallet-contract-v3) эта проблема была решена на уровне архитектуры контракта и потребляет меньше газа. В этой главе будут рассмотрены основы Highload Wallet V3 и важные нюансы, которые следует помнить.

## Highload Wallet v3

Этот кошелек создан для тех, кому необходимо отправлять транзакции с очень высокой скоростью. Например, для криптобирж.

- [Исходный код](https://github.com/ton-blockchain/Highload-wallet-contract-v3)

Любое внешнее сообщение (запрос на перевод) для Highload v3 содержит:

- подпись (512 бит) в ячейке верхнего уровня - другие параметры находятся в ссылке этой ячейки
- ID субкошелька (32 бита)
- сообщение для отправки в качестве ссылки (сериализованное внутреннее сообщение, которое будет отправлено)
- режим отправки сообщения (8 бит)
- составной идентификатор запроса - 13 бит "сдвига" и 10 бит "номера бита", однако 10 бит номера бита могут доходить только до 1022, а не до 1023, а также последний такой используемый query ID (8388605) зарезервирован для экстренных случаев и не должен использоваться
- дата создания или временная метка сообщения
- время ожидания

Время ожидания сохраняется в Highload в качестве параметра и проверяется на время ожидания во всех запросах - таким образом, время ожидания для всех запросов одинаково. Сообщение не должно быть старше времени ожидания на момент поступления в кошелек Highload, или в коде требуется, чтобы `created_at > now() - timeout`. Query ID хранятся в целях защиты от повторного воспроизведения в течение как минимум времени ожидания и, возможно, до 2 \* время ожидания, однако не следует ожидать, что они будут храниться дольше, чем истечение этого времени. Идентификатор суб-кошелька сверяется с идентификатором, сохраненным в кошельке. Хэш внутренней ссылки проверяется вместе с подписью на соответствие открытому ключу кошелька.

Highload v3 может отправлять только 1 сообщение из любого заданного внешнего сообщения, однако он может отправлять это сообщение себе с помощью специального op code, что позволяет устанавливать любую ячейку действия для этого вызова внутреннего сообщения, что фактически позволяет отправлять до 254 сообщений на 1 внешнее сообщение (возможно, больше, если другое сообщение снова отправляется в кошелек Highload среди этих 254).

Highload v3 всегда будет сохранять query ID (защита от повторного воспроизведения) после прохождения всех проверок, однако сообщение может быть не отправлено из-за некоторых условий, включая, но не ограничиваясь ими:

- **содержащее состояние init** (такие сообщения, если требуется, могут быть отправлены с использованием специального op code для установки ячейки действия после внутреннего сообщения из кошелька Highload на себя)
- недостаточный баланс
- недопустимая структура сообщения (которая включает внешние исходящие сообщения - только внутренние сообщения могут быть отправлены напрямую из внешнего сообщения)

Highload v3 никогда не будет выполнять несколько внешних сообщений, содержащих один и тот же `query_id` **и** `created_at` - к тому времени, когда он забудет любой заданный `query_id`, условие `created_at` предотвратит выполнение такого сообщения. Это фактически делает `query_id` **и** `created_at` вместе "первичным ключом" запроса на перевод для Highload v3.

При итерации (увеличении) query ID дешевле (с точки зрения TON, потраченного на сборы) сначала перебрать номер бита, а затем сдвиг, как при увеличении обычного числа. После того, как вы достигли последнего query ID (помните об аварийном query ID- см. выше), вы можете сбросить query ID на 0, но если период ожидания Highload еще не прошел, то словарь защиты от повторного воспроизведения будет заполнен, и вам придется ждать, пока пройдет период ожидания.

## Highload wallet v2

:::danger
Устаревший контракт, рекомендуется использовать Highload wallet v3.
:::

Этот кошелек создан для тех, кому нужно отправлять сотни транзакций за короткий промежуток времени. Например, криптобиржи.

Он позволяет отправлять до `254` транзакций за один вызов смарт-контракта. Он также использует немного другой подход для решения проблемы атак повторного воспроизведения вместо seqno, поэтому вы можете вызывать этот кошелек несколько раз одновременно, чтобы отправлять даже тысячи транзакций в секунду.

:::caution Ограничения
Обратите внимание, что при работе с Highload wallet необходимо проверить и принять во внимание следующие ограничения.
:::

1. **Ограничение размера хранилища.** В настоящее время размер хранилища контракта должен быть меньше 65535 ячеек. Если размер
   old_queries превысит этот предел, будет выдано исключение в ActionPhase, и транзакция завершится ошибкой.
   Неудачная транзакция может быть воспроизведена.
2. **Лимит газа.** В настоящее время лимит газа составляет 1 000 000 единиц газа, что означает, что существует ограничение на то, сколько старых запросов может быть очищено за одну транзакцию. Если количество истекших запросов будет больше, контракт зависнет.

Это означает, что не рекомендуется устанавливать слишком большую дату истечения срока:
количество запросов в течение периода истечения срока не должно превышать 1000.

Кроме того, количество истекших запросов, очищенных за одну транзакцию, должно быть меньше 100.

## Как это сделать

Вы также можете прочитать статью [Руководство по Highload Wallet](/v3/guidelines/smart-contracts/howto/wallet#-high-load-wallet-v3).

Исходный код кошелька:

- [ton/crypto/smartcont/Highload-wallet-v2-code.fc](https://github.com/ton-blockchain/ton/blob/master/crypto/smartcont/new-highload-wallet-v2.fif)