# Расчет комиссии

Когда ваш контракт начинает обработку входящего сообщения, вы должны проверить количество TON, прикрепленных к сообщению, чтобы убедиться, что их достаточно для покрытия [всех типов комиссий](/v3/documentation/smart-contracts/transaction-fees/fees#elements-of-transaction-fee). Для этого вам нужно рассчитать (или предсказать) комиссию для текущей транзакции.

В этом документе описывается, как рассчитать комиссию в контрактах FunC с помощью новых опкодов TVM.

:::info Больше информации об опкодах
Полный список опкодов TVM, включая упомянутые ниже, вы можете найти на странице [Инструкция TVM] (/v3/documentation/tvm/instructions).
:::

## Комиссия за хранение

### Обзор

В общем, "плата за хранение" — это сумма, которую вы платите за хранение смарт-контракта в блокчейне. Вы платите за каждую секунду, в течение которой смарт-контракт хранится в блокчейне.

Используйте опкод `GETSTORAGEFEE` со следующими параметрами:

| Параметр                   | Описание                                                           |
| :------------------------- | :----------------------------------------------------------------- |
| cells                      | Количество ячеек контракта                                         |
| bits                       | Количество битов контракта                                         |
| is_mc | Истина, если источник или пункт назначения находится в мастерчейне |

:::info Для расчета комиссии за хранение и пересылку учитываются только уникальные хеш-ячейки, то есть 3 идентичные хеш-ячейки считаются как одна.

В частности, данные дедуплицируются: если несколько эквивалентных подъячеек упоминаются в разных ветвях, их содержимое хранится только один раз.

[Подробнее о дедупликации](/v3/documentation/data-formats/tlb/library-cells).
:::

### Поток вычислений

Каждый контракт имеет свой баланс. Вы можете рассчитать, сколько TON требуется вашему контракту, чтобы оставаться действительным в течение указанного времени `seconds`, используя функцию:

```func
int get_storage_fee(int workchain, int seconds, int bits, int cells) asm(cells bits seconds workchain) "GETSTORAGEFEE";
```

Затем вы можете вписать это значение в контракт и рассчитать текущую плату за хранение, используя его:

```func
;; functions from func stdlib (not presented on mainnet)
() raw_reserve(int amount, int mode) impure asm "RAWRESERVE";
int get_storage_fee(int workchain, int seconds, int bits, int cells) asm(cells bits seconds workchain) "GETSTORAGEFEE";
int my_storage_due() asm "DUEPAYMENT";

;; constants from stdlib
;;; Creates an output action which would reserve exactly x nanograms (if y = 0).
const int RESERVE_REGULAR = 0;
;;; Creates an output action which would reserve at most x nanograms (if y = 2).
;;; Bit +2 in y means that the external action does not fail if the specified amount cannot be reserved; instead, all remaining balance is reserved.
const int RESERVE_AT_MOST = 2;
;;; in the case of action fail - bounce transaction. No effect if RESERVE_AT_MOST (+2) is used. TVM UPGRADE 2023-07. v3/documentation/tvm/changelog/tvm-upgrade-2023-07#sending-messages
const int RESERVE_BOUNCE_ON_ACTION_FAIL = 16;

() calculate_and_reserve_at_most_storage_fee(int balance, int msg_value, int workchain, int seconds, int bits, int cells) inline {
    int on_balance_before_msg = my_ton_balance - msg_value;
    int min_storage_fee = get_storage_fee(workchain, seconds, bits, cells); ;; can be hardcoded IF CODE OF THE CONTRACT WILL NOT BE UPDATED
    raw_reserve(max(on_balance_before_msg, min_storage_fee + my_storage_due()), RESERVE_AT_MOST);
}
```

Если `storage_fee` введен жестко, **не забудьте обновить его** в процессе обновления контракта. Не все контракты поддерживают обновление, поэтому это необязательное требование.

## Комиссия за вычисления

### Обзор

В большинстве случаев используйте опкод `GETGASFEE` со следующими параметрами:

| Параметр   | Описание                                                           |
| :--------- | :----------------------------------------------------------------- |
| `gas_used` | Закодированное количество газа, рассчитанное в тестах              |
| `is_mc`    | Истина, если источник или пункт назначения находится в мастерчейне |

### Поток вычислений

```func
int get_compute_fee(int workchain, int gas_used) asm(gas_used workchain) "GETGASFEE";
```

Но как получить `gas_used`? Через тесты!

Чтобы вычислить `gas_used`, следует написать тест для вашего контракта, который:

1. Делает перевод.
2. Проверяет успешность и получает информацию о переводе.
3. Проверяет фактическое количество газа, использованное этим переводом для вычисления.

Поток вычислений контракта может зависеть от входных данных. Вам следует запускать контракт таким образом, чтобы использовалось как можно больше газа. Убедитесь, что вы используете самый затратный способ вычисления для контракта

```ts
// Just Init code
const deployerJettonWallet = await userWallet(deployer.address);
let initialJettonBalance = await deployerJettonWallet.getJettonBalance();
const notDeployerJettonWallet = await userWallet(notDeployer.address);
let initialJettonBalance2 = await notDeployerJettonWallet.getJettonBalance();
let sentAmount = toNano('0.5');
let forwardAmount = toNano('0.05');
let forwardPayload = beginCell().storeUint(0x1234567890abcdefn, 128).endCell();
// Make sure payload is different, so cell load is charged for each individual payload.
let customPayload = beginCell().storeUint(0xfedcba0987654321n, 128).endCell();

// Let's use this case for fees calculation
// Put the forward payload into custom payload, to make sure maximum possible gas is used during computation
const sendResult = await deployerJettonWallet.sendTransfer(deployer.getSender(), toNano('0.17'), // tons
    sentAmount, notDeployer.address,
    deployer.address, customPayload, forwardAmount, forwardPayload);
expect(sendResult.transactions).toHaveTransaction({ //excesses
    from: notDeployerJettonWallet.address,
    to: deployer.address,
});
/*
transfer_notification#7362d09c query_id:uint64 amount:(VarUInteger 16)
                              sender:MsgAddress forward_payload:(Either Cell ^Cell)
                              = InternalMsgBody;
*/
expect(sendResult.transactions).toHaveTransaction({ // notification
    from: notDeployerJettonWallet.address,
    to: notDeployer.address,
    value: forwardAmount,
    body: beginCell().storeUint(Op.transfer_notification, 32).storeUint(0, 64) // default queryId
        .storeCoins(sentAmount)
        .storeAddress(deployer.address)
        .storeUint(1, 1)
        .storeRef(forwardPayload)
        .endCell()
});
const transferTx = findTransactionRequired(sendResult.transactions, {
    on: deployerJettonWallet.address,
    from: deployer.address,
    op: Op.transfer,
    success: true
});

let computedGeneric: (transaction: Transaction) => TransactionComputeVm;
computedGeneric = (transaction) => {
  if(transaction.description.type !== "generic")
    throw("Expected generic transactionaction");
  if(transaction.description.computePhase.type !== "vm")
    throw("Compute phase expected")
  return transaction.description.computePhase;
}

let printTxGasStats: (name: string, trans: Transaction) => bigint;
printTxGasStats = (name, transaction) => {
    const txComputed = computedGeneric(transaction);
    console.log(`${name} used ${txComputed.gasUsed} gas`);
    console.log(`${name} gas cost: ${txComputed.gasFees}`);
    return txComputed.gasFees;
}

send_gas_fee = printTxGasStats("Jetton transfer", transferTx);
```

## Комиссия за пересылку

### Обзор

Комиссия за пересылку взимается за исходящие сообщения.

В общем случае существует три варианта обработки комиссии за пересылку:

1. Структура сообщения детерминирована, и вы можете предсказать размер комиссии.
2. Структура сообщения во многом зависит от структуры входящего сообщения.
3. Вы вообще не можете предсказать структуру исходящего сообщения.

### Поток вычислений

Если структура сообщения детерминирована, используйте опкод `GETFORWARDFEE` со следующими параметрами:

| Параметр                   | Описание                                                           |
| :------------------------- | :----------------------------------------------------------------- |
| cells                      | Количество ячеек                                                   |
| bits                       | Количество битов                                                   |
| is_mc | Истина, если источник или пункт назначения находится в мастерчейне |

:::info Для расчета комиссии за хранение и пересылку учитываются только уникальные хеш-ячейки, то есть 3 идентичные хеш-ячейки считаются как одна.

В частности, данные дедуплицируются: если несколько эквивалентных подъячеек упоминаются в разных ветвях, их содержимое хранится только один раз.

[Подробнее о дедупликации](/v3/documentation/data-formats/tlb/library-cells).
:::

Однако иногда исходящее сообщение существенно зависит от входящей структуры, и в этом случае dы не можете полностью предсказать размер комиссии. Попробуйте использовать опкод `GETORIGINALFWDFEE` со следующими параметрами:

| Параметр                     | Описание                                                           |
| :--------------------------- | :----------------------------------------------------------------- |
| fwd_fee | Извлечено из входящего сообщени                                    |
| is_mc   | Истина, если источник или пункт назначения находится в мастерчейне |

:::caution Будьте осторожны с опкодом `SENDMSG`.

Он расходует **непредсказуемое количество** газа.

Не используйте его без необходимости.
:::

Если `GETORIGINALFWDFEE` не удается использовать, есть еще один вариант. Используйте опкод `SENDMSG` со следующими параметрами:

| Параметр | Описание         |
| :------- | :--------------- |
| cells    | Количество ячеек |
| mode     | Режим сообщений  |

Режимы влияют на расчет комиссии следующим образом:

- `+1024` не создают действие, а только оценивают комиссию. Другие режимы отправят сообщение на этапе выполнения действия.
- `+128` подставляет значение всего баланса контракта до начала фазы вычислений (немного неточно, так как расходы на газ, которые невозможно оценить до завершения вычислений, не учитываются).
- `+64` подставляет весь баланс входящего сообщения в качестве исходящего значения (немного неточно, расходы на газ, которые невозможно оценить до завершения вычислений, не учитываются).
- Другие режимы можно найти [на странице режимов сообщений] (/v3/documentation/smart-contracts/message-management/sending-messages#message-modes).

Он создает действие вывода и возвращает комиссию за создание сообщения. Однако он использует непредсказуемое количество газа, которое нельзя рассчитать с помощью формул, так как же его рассчитать? Используйте `GASCONSUMED`:

```func
int send_message(cell msg, int mode) impure asm "SENDMSG";
int gas_consumed() asm "GASCONSUMED";
;; ... some code ...

() calculate_forward_fee(cell msg, int mode) inline {
  int gas_before = gas_consumed();
  int forward_fee = send_message(msg, mode);
  int gas_usage = gas_consumed() - gas_before;
  
  ;; forward fee -- fee value
  ;; gas_usage -- amount of gas, used to send msg
}
```

## См. также

- [Контракт Stablecoin с расчетом комиссии](https://github.com/ton-blockchain/stablecoin-contract)
