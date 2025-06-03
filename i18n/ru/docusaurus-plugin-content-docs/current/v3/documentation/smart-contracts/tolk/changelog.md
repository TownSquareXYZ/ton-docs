import Feedback from '@site/src/components/Feedback';

# История Tolk

Когда будут выпущены новые версии Tolk, они будут упомянуты здесь.

## v0.12

1. Structures `struct A { ... }`
2. Generics `struct<T>` and `type<T>`
3. Methods `fun Point.getX(self)`
4. Rename stdlib functions to short methods

## v0.11

1. Type aliases `type NewName = <existing type>`
2. Union types `T1 | T2 | ...`
3. Pattern matching for types
4. Operators `is` and `!is`
5. Pattern matching for expressions
6. Semicolon for the last statement in a block can be omitted

## v0.10

1. Fixed-width integers: `int32`, `uint64`, etc. [Details](https://github.com/ton-blockchain/ton/pull/1559)
2. Type `coins` and function `ton("0.05")`
3. `bytesN` and `bitsN` types (backed by slices at TVM level)
4. Replace `"..."c` postfixes with `stringCrc32("...")` functions
5. Support `0b...` number literals along with `0x...`
6. Trailing comma support

## v0.9

1. Nullable types `int?`, `cell?`, etc.; null safety
2. Standard library (asm definitions) updated to reflect nullability
3. Smart casts, like in TypeScript in Kotlin
4. Operator `!` (non-null assertion)
5. Code after `throw` is treated as unreachable
6. The `never` type

## v0.7

1. Под капотом: рефакторинг внутренних компонентов компилятора; ядро ​​семантического анализа на уровне AST
2. Под капотом: переписываем систему типов с Хиндли-Милнера на статическую типизацию

## v0.7

1. Под капотом: рефакторинг внутренних компонентов компилятора; ядро ​​семантического анализа на уровне AST
2. Под капотом: переписываем систему типов с Хиндли-Милнера на статическую типизацию
3. Понятные и читаемые сообщения об ошибках при несоответствии типов
4. Универсальные функции `fun f<T>(...)` и их экземпляры, такие как `f<int>(...)`
5. Тип `bool`; приведение типа через `value as T`

## v0.6

Первый публичный релиз. Вот некоторые заметки о его происхождении:

## Как появился Tolk

In June 2024, I created a pull request [FunC v0.5.0](https://github.com/ton-blockchain/ton/pull/1026).
Besides this PR, I've written a roadmap for what can be enhanced in FunC, syntactically and semantically.

Instead of merging v0.5.0 and continuing to develop FunC, we decided to **fork** it.
To leave FunC untouched as it is. As it always was. And to develop a new language driven by a fresh and new name.

For several months, I have worked on Tolk privately. I have implemented a giant list of changes.
And it's not only about the syntax. For instance, Tolk has an internal AST representation that is completely missed in FunC.

On TON Gateway, from 1 to 2 November in Dubai, I gave a speech presenting Tolk to the public, and we released it the same day.
The video is available [on YouTube](https://www.youtube.com/watch?v=Frq-HUYGdbI).

Первая версия языка Tolk — v0.6, метафора FunC v0.5, которая упустила шанс появиться.

Первая версия языка Tolk — v0.6, метафора FunC v0.5, которая упустила шанс появиться.

## Значение названия "Tolk"

**Tolk** is a wonderful word.

Во всех славянских языках корень *толк* и фраза *иметь толк* означают "иметь смысл", "иметь глубокие внутренние чувства".

In all Slavic languages, the root *tolk* and the phrase *"to have tolk"* means "to make sense"; "to have deep internals".

Что такое К, спросите вы? Наверное, "кот" — ник Николая Дурова? Или Коля? Котенок? Ядро (Kernel)? Кит? Знание (Knowledge)?
Правильный ответ — ничего из этого. Эта буква ничего не значит. Она открытая.
*The Open Letter K*

Что такое К, спросите вы? Наверное, "кот" — ник Николая Дурова? Или Коля? Котенок? Ядро (Kernel)? Кит? Знание (Knowledge)?
Правильный ответ — ничего из этого. Эта буква ничего не значит. Она открытая.
*The Open Letter K*

<Feedback />

