# Ячейки как хранилище данных

Все в TON хранится в ячейках. Ячейка — это структура данных, содержащая:

- до **1023 бит** данных (не байтов!)
- до **4 ссылок** на другие ячейки

Биты и ссылки не смешиваются (они хранятся отдельно). Циклические ссылки запрещены: для любой ячейки ни одна из ее дочерних ячеек не может иметь эту исходную ячейку в качестве ссылки.

Таким образом, все ячейки составляют направленный ациклический граф (DAG). Вот хорошая картинка для иллюстрации:

![Направленный ациклический граф](/img/docs/dag.png)

## Типы ячеек

В настоящее время существует 5 типов ячеек: *обычные* и 4 *экзотических*. Экзотические типы следующие:

- Ячейка с обрезанной ветвью
- Ячейка библиотечной ссылки
- Ячейка с доказательством Меркла
- Ячейка обновления Меркла

:::tip
Подробнее об экзотических ячейках см: [**TVM Whitepaper, раздел 3**](https://ton.org/tvm.pdf).
:::

## Варианты ячеек

Ячейка — это непрозрачный объект, оптимизированный для компактного хранения.

В частности, он дедуплицирует данные: если есть несколько эквивалентных подъячеек, на которые есть ссылки в разных ветвях, их содержимое сохраняется только один раз. Однако непрозрачность означает, что ячейку нельзя изменять или читать напрямую. Таким образом, существует 2 дополнительных разновидности ячеек:

- *Builder* для частично построенных ячеек, для которых можно определить быстрые операции для добавления битовых строк, целых чисел, других ячеек и ссылок на другие ячейки.
- *Slice* для "разрезанных" ячеек, представляющих собой либо остаток частично разобранной ячейки, либо значение (подъячейку), находящееся внутри такой ячейки и извлеченное из нее с помощью инструкции по разбору.

Еще одна особая разновидность ячеек используется в TVM:

- *Continuation* для ячеек, содержащих opcode (инструкции) для виртуальной машины TON, см. [обзор TVM](/v3/documentation/tvm/tvm-overview).

## Сериализация данных в ячейки

Любой объект в TON (сообщение, очередь сообщений, блок, состояние всего блокчейна, код контракта и данные) сериализуется в ячейку.

Процесс сериализации описывается схемой TL-B: формальное описание того, как этот объект может быть сериализован в *Builder* или как проанализировать объект заданного типа из *Slice*. TL-B для ячеек — это то же самое, что TL или ProtoBuf для байтовых потоков.

Если вы хотите узнать больше подробностей о (де)сериализации ячеек, вы можете прочитать статью [Cell & Bag of Cells](/v3/documentation/data-formats/tlb/cell-boc).

## См. также

- [Язык TL-B](/v3/documentation/data-formats/tlb/tl-b-language)