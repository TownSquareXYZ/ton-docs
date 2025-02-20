# Get-методы

:::note
Прежде чем продолжить, рекомендуется ознакомиться с основами [языка программирования FunC](/v3/documentation/smart-contracts/func/overview) на блокчейне TON. Это поможет лучше понять представленную ниже информацию.
:::

## Введение

Get-методы - это специальные функции в смарт-контрактах, предназначенные для получения определённых данных. Их выполнение происходит вне блокчейна и не требует комиссии.

Эти функции очень часто используются во многих смарт-контрактах. Например, стандартный [контракт Кошелька](/v3/documentation/smart-contracts/contracts-specs/wallet-contracts) содержит несколько get-методов: `seqno()`, `get_subwallet_id()` и `get_public_key()`. Они применяются в кошельках, SDK и API для получения данных о кошельках.

## Шаблоны проектирования для get-методов

### Основные шаблоны проектирования get-методов

1. **Получение отдельных данных.** Базовый шаблон заключается в создании методов, которые извлекают отдельные данные из состояния контракта. Такие методы не имеют параметров и возвращают одно значение.

   Например:

   ```func
   int get_balance() method_id {
       return get_data().begin_parse().preload_uint(64);
   }
   ```

2. **Получение агрегированных данных.** Ещё один распространённый шаблон - методы, которые извлекают сразу несколько значений из состояния контракта за один вызов. Это удобно, если данные часто используются вместе. Такие методы часто используются в контрактах [Jetton](#jettons) и [NFT](#nfts).

   Например:

   ```func
   (int, slice, slice, cell) get_wallet_data() method_id {
       return load_data();
   }
   ```

### Продвинутые шаблоны проектирования get-методов

1. **Извлечение вычисляемых данных**: В некоторых случаях необходимые данные не хранятся непосредственно в состоянии контракта, а вычисляются на основе состояния и входных аргументов.

   Пример:

   ```func
   slice get_wallet_address(slice owner_address) method_id {
       (int total_supply, slice admin_address, cell content, cell jetton_wallet_code) = load_data();
       return calculate_user_jetton_wallet_address(owner_address, my_address(), jetton_wallet_code);
   }
   ```

2. **Извлечение данных с учетом условий**: Иногда извлекаемые данные зависят от определённых условий, например, от текущего времени.

   Пример:

   ```func
   (int) get_ready_to_be_used() method_id {
       int ready? = now() >= 1686459600;
       return ready?;
   }
   ```

## Наиболее распространенные get-методы

### Стандартные кошельки

#### seqno()

```func
int seqno() method_id {
    return get_data().begin_parse().preload_uint(32);
}
```

Возвращает порядковый номер транзакции в определённом кошельке. Этот метод в основном используется для [защиты от повторения] (/v3/guidelines/smart-contracts/howto/wallet#replay-protection---seqno).

#### get_subwallet_id()

```func
int get_subwallet_id() method_id {
    return get_data().begin_parse().skip_bits(32).preload_uint(32);
}
```

- [Что такое Subwallet ID?] (/v3/guidelines/smart-contracts/howto/wallet#subwallet-ids)

#### get_public_key()

```func
int get_public_key() method_id {
    var cs = get_data().begin_parse().skip_bits(64);
    return cs.preload_uint(256);
}
```

Получает публичный ключ, связанный с кошельком.

### Жетоны

#### get_wallet_data()

```func
(int, slice, slice, cell) get_wallet_data() method_id {
    return load_data();
}
```

Этот метод возвращает полный набор данных, связанных с кошельком jetton:

- (int) баланс
- (slice) owner_address
- (slice) jetton_master_address
- (cell) jetton_wallet_code

#### get_jetton_data()

```func
(int, int, slice, cell, cell) get_jetton_data() method_id {
    (int total_supply, slice admin_address, cell content, cell jetton_wallet_code) = load_data();
    return (total_supply, -1, admin_address, content, jetton_wallet_code);
}
```

Возвращает данные master жетона, включая его общий объём выпуска, адрес админа, содержимое жетона и код кошелька.

#### get_wallet_address(slice owner_address)

```func
slice get_wallet_address(slice owner_address) method_id {
    (int total_supply, slice admin_address, cell content, cell jetton_wallet_code) = load_data();
    return calculate_user_jetton_wallet_address(owner_address, my_address(), jetton_wallet_code);
}
```

Принимая адрес владельца, этот метод вычисляет и возвращает адрес контракта кошелька Jetton этого владельца.

### NFTs

#### get_nft_data()

```func
(int, int, slice, slice, cell) get_nft_data() method_id {
    (int init?, int index, slice collection_address, slice owner_address, cell content) = load_data();
    return (init?, index, collection_address, owner_address, content);
}
```

Возвращает данные, связанные с невзаимозаменяемым токеном, включая информацию о том, был ли он инициализирован, индекс в коллекции, адрес коллекции, адрес владельца и индивидуальное содержимое.

#### get_collection_data()

```func
(int, cell, slice) get_collection_data() method_id {
    var (owner_address, next_item_index, content, _, _) = load_data();
    slice cs = content.begin_parse();
    return (next_item_index, cs~load_ref(), owner_address);
}
```

Возвращает данные о коллекции NFT, включая индекс следующего элемента для минта, содержимое коллекции и адрес владельца.

#### get_nft_address_by_index(int index)

```func
slice get_nft_address_by_index(int index) method_id {
    var (_, _, _, nft_item_code, _) = load_data();
    cell state_init = calculate_nft_item_state_init(index, nft_item_code);
    return calculate_nft_item_address(workchain(), state_init);
}
```

Принимая индекс, этот метод вычисляет и возвращает адрес соответствующего контракта NFT-элемента этой коллекции.

#### royalty_params()

```func
(int, int, slice) royalty_params() method_id {
    var (_, _, _, _, royalty) = load_data();
    slice rs = royalty.begin_parse();
    return (rs~load_uint(16), rs~load_uint(16), rs~load_msg_addr());
}
```

Получает параметры роялти для NFT. Эти параметры включают процент роялти, который выплачивается оригинальному создателю при продаже NFT.

#### get_nft_content(int index, cell individual_nft_content)

```func
cell get_nft_content(int index, cell individual_nft_content) method_id {
    var (_, _, content, _, _) = load_data();
    slice cs = content.begin_parse();
    cs~load_ref();
    slice common_content = cs~load_ref().begin_parse();
    return (begin_cell()
            .store_uint(1, 8) ;; offchain tag
            .store_slice(common_content)
            .store_ref(individual_nft_content)
            .end_cell());
}
```

Принимая индекс и [индивидуальное содержимое NFT](#get_nft_data), этот метод получает и возвращает объединённые общие и индивидуальные данные NFT.

## Как работать с get-методами

### Вызов get-методов на популярных обозревателях

#### Tonviewer

Вы можете вызвать get-методы в нижней части страницы во вкладке "Методы".

- https://tonviewer.com/EQAWrNGl875lXA6Fff7nIOwTIYuwiJMq0SmtJ5Txhgnz4tXI?section=method

#### Ton.cx

Вы можете вызывать get-методы во вкладке "Get-методы".

- https://ton.cx/address/EQAWrNGl875lXA6Fff7nIOwTIYuwiJMq0SmtJ5Txhgnz4tXI

### Вызов get- методов из кода

В приведенных ниже примерах мы будем использовать библиотеки и инструменты Javascript:

- [ton](https://github.com/ton-org/ton) библиотека
- [Blueprint](/v3/documentation/smart-contracts/getting-started/javascript) SDK

Допустим, существует некий контракт со следующим get-методом:

```func
(int) get_total() method_id {
    return get_data().begin_parse().preload_uint(32); ;; load and return the 32-bit number from the data
}
```

Этот метод возвращает одно число, загруженное из данных контракта.

Приведенный ниже фрагмент кода может быть использован для вызова этого get-метода на каком-либо контракте, развёрнутом по известному адресу:

```ts
import { TonClient } from '@ton/ton';
import { Address } from '@ton/core';

async function main() {
    // Create Client
    const client = new TonClient({
        endpoint: 'https://toncenter.com/api/v2/jsonRPC',
    });

    // Call get method
    const result = await client.runMethod(
        Address.parse('EQD4eA1SdQOivBbTczzElFmfiKu4SXNL4S29TReQwzzr_70k'),
        'get_total'
    );
    const total = result.stack.readNumber();
    console.log('Total:', total);
}

main();
```

Этот код приведет к выводу `Total: 123`. Число может быть другим, это просто пример.

### Тестирование get-методов

Для тестирования созданных смарт-контрактов мы можем использовать [Sandbox](https://github.com/ton-community/sandbox), который устанавливается по умолчанию в новые проекты Blueprint.

Во-первых, вам нужно добавить специальный метод в обёртку контракта, который будет выполнять get-метод и возвращать типизированный результат. Допустим, ваш контракт называется *Counter*, и вы уже реализовали метод, который обновляет сохранённое число. Откройте `wrappers/Counter.ts` и добавьте следующий метод:

```ts
async getTotal(provider: ContractProvider) {
    const result = (await provider.get('get_total', [])).stack;
    return result.readNumber();
}
```

Он выполнил get-метод и получил результирующий стек. Стек в случае с get-методами - это, по сути, то, что он вернул. В этом фрагменте кода мы считываем из него одно число. В более сложных случаях, когда возвращается сразу несколько значений, можно просто вызвать методы типа `readSomething` несколько раз, чтобы обработать весь результат выполнения из стека.

Наконец, мы можем использовать этот метод в наших тестах. Перейдите к файлу `tests/Counter.spec.ts` и добавьте новый тест:

```ts
it('should return correct number from get method', async () => {
    const caller = await blockchain.treasury('caller');
    await counter.sendNumber(caller.getSender(), toNano('0.01'), 123);
    expect(await counter.getTotal()).toEqual(123);
});
```

Проверьте это, запустив `npx blueprint test` в терминале, и если все сделано правильно, этот тест должен быть пройден!

## Вызов get-методов из других контрактов

Вопреки тому, что может показаться интуитивным, вызов get-методов из других контрактов невозможен on-chain, прежде всего, из-за природы блокчейн-технологии и необходимости консенсуса.

Во-первых, получение данных из другого шардчейна может потребовать времени. Такая задержка может легко нарушить процесс выполнения контракта, поскольку ожидается, что операции в блокчейне будут выполняться детерминированно и своевременно.

Во-вторых, достижение консенсуса среди валидаторов будет проблематичным. Для проверки корректности транзакции валидаторам пришлось бы вызывать один и тот же get-метод. Однако если состояние целевого контракта изменится между несколькими вызовами, валидаторы могут получить в итоге разные версии результата транзакции.

Наконец, смарт-контракты в TON разработаны как чистые функции: при одинаковых входных данных они всегда будут выдавать одинаковые выходные данные. Этот принцип позволяет достичь прямого консенсуса во время обработки сообщений. Получение произвольных, динамически изменяющихся данных во время выполнения нарушит это детерминированное свойство.

### Последствия для разработчиков

Эти ограничения означают, что один контракт не может напрямую получить доступ к состоянию другого контракта через свои get-методы. Невозможность включения внешних данных в режиме реального времени в детерминированный поток контракта может показаться ограничением. Однако именно эти ограничения обеспечивают целостность и надежность блокчейн-технологии.

### Решения и обходные пути

В блокчейне TON смарт-контракты взаимодейстсвуют с помощью сообщений, вместо того чтобы напрямую вызывать методы другого контракта. Целевому контракту может быть отправлено сообщение с запросом на выполнение определённого метода. Эти запросы обычно начинаются со специальных [кодов операций] (/v3/documentation/smart-contracts/message-management/internal-messages).

Контракт, предназначенный для приёма таких запросов, выполнит нужный метод и отправит результаты обратно в отдельном сообщении. Хотя это может показаться сложным, на самом деле это упрощает взаимодействие между контрактами и улучшает масштабируемость и производительность сети блокчейн.

Этот механизм передачи сообщений является неотъемлемой частью работы блокчейна TON, обеспечивая масштабируемый росту сети без необходимости сложной синхронизации между шардами.

Для эффективного взаимодействия между контрактами очень важно, чтобы они были разработаны таким образом, чтобы правильно принимать запросы и отвечать на них. Это включает в себя указание методов, которые могут быть вызваны on-chain для отправки ответов.

Давайте рассмотрим простой пример:

```func
#include "imports/stdlib.fc";

int get_total() method_id {
    return get_data().begin_parse().preload_uint(32);
}

() recv_internal(int my_balance, int msg_value, cell in_msg_full, slice in_msg_body) impure {
    if (in_msg_body.slice_bits() < 32) {
        return ();
    }

    slice cs = in_msg_full.begin_parse();
    cs~skip_bits(4);
    slice sender = cs~load_msg_addr();

    int op = in_msg_body~load_uint(32); ;; load the operation code

    if (op == 1) { ;; increase and update the number
        int number = in_msg_body~load_uint(32);
        int total = get_total();
        total += number;
        set_data(begin_cell().store_uint(total, 32).end_cell());
    }
    elseif (op == 2) { ;; query the number
        int total = get_total();
        send_raw_message(begin_cell()
            .store_uint(0x18, 6)
            .store_slice(sender)
            .store_coins(0)
            .store_uint(0, 107) ;; default message headers (see sending messages page)
            .store_uint(3, 32) ;; response operation code
            .store_uint(total, 32) ;; the requested number
        .end_cell(), 64);
    }
}
```

В этом примере контракт получает и обрабатывает внутренние сообщения, интерпретируя коды операций, выполняя определенные методы и возвращая ответы соответствующим образом:

- Oп-код `1` обозначает запрос на обновление числа в данных контракта.
- Оп-код `2` обозначает запрос на получение числа из данных контракта.
- Оп-код `3` используется в ответном сообщении, которое вызывающий смарт-контракт должен обработать, чтобы получить результат.

Для простоты мы использовали простые маленькие числа 1, 2 и 3 для кодов операций. Но для реальных проектов следует учитывать стандарт при их назначении:

- [CRC32-хеши для оп-кодов](/v3/documentation/data-formats/tlb/crc32)

## Распространенные "подводные камни" и как их избежать

1. **Неправильное использование get-методов**: Как уже упоминалось ранее, get-методы предназначены для возврата данных из состояния контракта и не должна изменять его. Попытка изменить состояние контракта внутри get-метода не приведет к желаемому результату.

2. **Игнорирование возвращаемых типов**: Каждый get-метод должен иметь четко определённый возвращаемый тип извлекаемых данных. Если метод должен возвращать определенный тип данных, убедитесь, что во всех возможных путях выполнения возвращается именно этот тип. Избегайте использования несогласованных типов возвращаемых значений, это может привести к ошибкам и трудностям при взаимодействии с контрактом.

3. **Предполагая кросс-контрактные вызовы**: Распространённое заблуждение заключается в том, что get-методы можно вызывать из других контрактов on-chain. Однако, как уже обсуждалось, это невозможно из-за природы блокчейна и необходимости консенсуса. Всегда помните, что get-методы предназначены для использования off-chain, а взаимодействие между контрактами on-chain осуществляется через внутренние сообщения.

## Заключение

Get-методы - это важный инструмент для запроса данных из смарт-контрактов в блокчейне TON. Хотя у них есть свои ограничения, понимание этих ограничений и умение их обходить - ключ к эффективному использованию get-методов в ваших смарт-контрактах.
