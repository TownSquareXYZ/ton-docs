# TVM против EVM

Ethereum Virtual Machine (EVM) и TON Virtual Machine (TVM) - это две стековые виртуальные машины, разработанные для запуска кода смарт-контрактов. Хотя у них есть общие черты, между ними есть заметные различия.

## Представление данных

### Ethereum Virtual Machine (EVM)

1. Основные единицы данных

- EVM работает в основном с 256-битными целыми числами, что отражает ее дизайн вокруг криптографических функций Ethereum (например, хеширование Keccak-256 и операции с эллиптическими кривыми).
- Типы данных ограничены в основном целыми числами, байтами и иногда массивами этих типов, но все они должны соответствовать 256-битным правилам обработки.

2. Хранилище состояний

- Все состояние блокчейна Ethereum представляет собой отображение 256-битных адресов в 256-битных значениях. Это отображение поддерживается в структуре данных, известной как Merkle Patricia Trie (MPT).
- MPT позволяет Ethereum эффективно доказывать согласованность и целостность состояния блокчейна с помощью криптографической проверки, что жизненно важно для децентрализованной системы, такой как Ethereum.

3. Ограничения структуры данных

- Упрощение до ограничений в 256 бит означает, что EVM изначально не предназначена для обработки сложных или пользовательских структур данных напрямую.
- Разработчикам часто требуется внедрять дополнительную логику в смарт-контракты для моделирования более сложных структур данных, что может привести к увеличению затрат на газ и сложности.

### TON Virtual Machine (TVM)

1. Архитектура на основе ячеек

- TVM использует уникальную модель "bag of cells" для представления данных. Каждая ячейка может содержать до 128 байтов данных и может иметь до 4 ссылок на другие ячейки.
- Эта структура позволяет TVM изначально поддерживать произвольные алгебраические типы данных и более сложные конструкции, такие как деревья или направленные ациклические графы (DAG) непосредственно в своей модели хранения.

2. Гибкость и эффективность

- Модель ячеек обеспечивает значительную гибкость, позволяя TVM обрабатывать широкий спектр структур данных более естественно и эффективно, чем EVM.
- Например, возможность создания связанных структур с помощью ссылок на ячейки позволяет создавать динамические и потенциально бесконечные структуры данных, которые имеют решающее значение для определенных типов приложений, таких как децентрализованные социальные сети или сложные децентрализованные финансовые протоколы (DeFi).

3. Сложная обработка данных

- Возможность управлять сложными типами данных, изначально заложенная в архитектуре VM, снижает необходимость в обходных решениях в смарт-контрактах, что потенциально снижает стоимость выполнения и увеличивает скорость выполнения.
- Конструкция TVM особенно выгодна для приложений, требующих сложного управления состоянием или взаимосвязанных структур данных, предоставляя разработчикам надежную основу для создания сложных и масштабируемых децентрализованных приложений.

## Стековая машина

### Ethereum Virtual Machine (EVM)

- EVM работает как традиционная стековая машина, где она использует стек "последним пришел — первым вышел" (LIFO) для управления вычислениями.
- Он обрабатывает операции, помещая и выталкивая 256-битные целые числа, которые являются стандартным размером для всех элементов в стеке.

### TON Virtual Machine (TVM)

- TVM также функционирует как стековая машина, но с ключевым отличием: она поддерживает как 257-битные целые числа, так и ссылки на ячейки.
- Это позволяет TVM помещать и выводить эти два различных типа данных в стек/из стека, обеспечивая повышенную гибкость в прямой управлении данными.

### Пример операций со стеком

Предположим, мы хотим сложить два числа (2 и 2) в EVM. Процесс будет включать помещение чисел в стек и последующий вызов инструкции `ADD`. Результат (4) останется наверху стека.

Мы можем выполнить эту операцию таким же образом в TVM. Но давайте рассмотрим другой пример с более сложными структурами данных, такими как хэш-карты и ссылки на ячейки. Предположим, у нас есть хэш-карта, которая хранит пары ключ-значение, где ключи являются целыми числами, а значения — либо целыми числами, либо ссылками на ячейки. Допустим, наша хэш-карта содержит следующие записи:

```js
{
    1: 10
    2: cell_a (which contains 10)
}
```

Мы хотим сложить значения, связанные с ключами 1 и 2, и сохранить результат с ключом 3. Давайте рассмотрим операции со стеком:

1. Поместить ключ 1 в стек: `stack` = (1)
2. Вызвать `DICTGET` для ключа 1 (извлечь значение, связанное с ключом наверху стека): Извлечь значение 10. `stack` = (10)
3. Поместить ключ 2 в стек: `stack` = (10, 2)
4. Вызвать `DICTGET` для ключа 2: Извлечь ссылку на Cell_A. `stack` = (10, Cell_A)
5. Загрузить значение из Cell_A: Выполняется инструкция по загрузке значения из ссылки на ячейку. `stack` = (10, 10)
6. Вызвать инструкцию `ADD`: При выполнении инструкции `ADD` TVM извлечет два верхних элемента из стека, сложит их и поместит результат обратно в стек. В этом случае верхние два элемента — 10 и 10. После сложения стек будет содержать результат: `stack` = (20)
7. Поместить ключ 3 в стек: `stack` = (20, 3)
8. Вызвать `DICTSET`: Сохраняет 20 с ключом 3. Обновленная хэш-карта:

```js
{
    1: 10,
    2: cell_a,
    3: 20
}
```

Чтобы сделать то же самое в EVM, нам нужно определить сопоставление, которое хранит пары ключ-значение, и функцию, в которой мы работаем напрямую с 256-битными целыми числами, хранящимися в сопоставлении. Важно отметить, что EVM поддерживает сложные структуры данных, используя Solidity, но эти структуры построены поверх более простой модели данных EVM, которая принципиально отличается от более выразительной модели данных TVM

## Арифметические операции

### Ethereum Virtual Machine (EVM)

- Ethereum Virtual Machine (EVM) обрабатывает арифметику с использованием 256-битных целых чисел. Это означает, что операции, такие как сложение, вычитание, умножение и деление, адаптированы под этот размер данных.

### TON Virtual Machine (TVM)

- TON Virtual Machine (TVM) поддерживает более широкий спектр арифметических операций, включая 64-битные, 128-битные и 256-битные целые числа, как беззнаковые, так и знаковые, а также операции по модулю. TVM дополнительно расширяет свои арифметические возможности с помощью таких операций, как умножение-затем-сдвиг и сдвиг-затем-деление, которые особенно полезны для реализации арифметики с фиксированной точкой. Это разнообразие позволяет разработчикам выбирать наиболее эффективные арифметические операции на основе конкретных требований их смарт-контрактов, предлагая потенциальные оптимизации на основе размера и типа данных.

## Проверки переполнения

### Ethereum Virtual Machine (EVM)

- В EVM проверки переполнения не выполняются самой виртуальной машиной. С введением Solidity 0.8.0 автоматические проверки переполнения и потери значимости были интегрированы в язык для повышения безопасности. Эти проверки помогают предотвратить распространенные уязвимости, связанные с арифметическими операциями, но требуют более новых версий Solidity, поскольку более ранние версии требуют ручной реализации этих мер безопасности.

### TON Virtual Machine (TVM)

- Напротив, TVM автоматически выполняет проверки переполнения для всех арифметических операций, функция, встроенная непосредственно в виртуальную машину. Такой выбор дизайна упрощает разработку смарт-контрактов, изначально снижая риск ошибок и повышая общую надежность и безопасность кода.

## Криптография и хэш-функции

### Ethereum Virtual Machine (EVM)

- EVM поддерживает специфичную для Ethereum схему криптографии, такую ​​как эллиптическая кривая secp256k1 и хэш-функцию keccak256. Кроме того, EVM не имеет встроенной поддержки доказательств Меркла, которые являются криптографическими доказательствами, используемыми для проверки принадлежности элемента к множеству.

### TON Virtual Machine (TVM)

- TVM предлагает поддержку 256-битной криптографии на эллиптических кривых (ECC) для предопределенных кривых, таких как Curve25519. Он также поддерживает пары Вейля на некоторых эллиптических кривых, которые полезны для быстрой реализации zk-SNARK (доказательства с нулевым разглашением). Также поддерживаются популярные хэш-функции, такие как sha256, что обеспечивает больше возможностей для криптографических операций. Кроме того, TVM может работать с доказательствами Меркла, предоставляя дополнительные криптографические функции, которые могут быть полезны для определенных случаев использования, таких как проверка включения транзакции в блок.

## Высокоуровневые языки

### Ethereum Virtual Machine (EVM)

- EVM в первую очередь использует Solidity в качестве своего высокоуровневого языка, который является объектно-ориентированным статически типизированным языком, похожим на JavaScript и C++. Также существуют другие языки для написания смарт-контрактов Ethereum, такие как Vyper, Yul и т. д.

### TON Virtual Machine (TVM)

- TVM использует FunC в качестве высокоуровневого языка, предназначенного для написания смарт-контрактов TON. Это процедурный язык со статическими типами и поддержкой алгебраических типов данных. FunC компилируется в Fift, который, в свою очередь, компилируется в байт-код TVM.

## Заключение

Подводя итог, можно сказать, что хотя и EVM, и TVM являются стековыми машинами, предназначенными для выполнения смарт-контрактов, TVM предлагает большую гибкость, поддержку более широкого спектра типов и структур данных, встроенные проверки переполнения, расширенные криптографические функции.

Поддержка TVM смарт-контрактов с поддержкой шардинга и его уникальный подход к представлению данных делают его более подходящим для определенных вариантов использования и масштабируемых сетей блокчейнов.