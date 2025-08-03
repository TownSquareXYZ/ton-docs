import Feedback from '@site/src/components/Feedback';

# 料金履歴

Tolkの新しいバージョンがリリースされると、それらはここで紹介されます。

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

## v0.8

1. Syntax `tensorVar.0` and `tupleVar.0` (both for reading and writing)
2. Allow `cell`, `slice`, etc. to be valid identifiers (not keywords)

## v0.7

1. 内部: コンパイラの内部をリファクタリングします。 ASTレベルのセマンティック分析カーネル
2. 内部: 型システムを Hindley-Milner から静的型付けに書き直します。
3. 型の不一致に関する明確で読みやすいエラー メッセージ
4. ジェネリック関数 `fun f<T>(...)` および `f<int>(...)` のようなインスタンス化
5. `bool` 型。 `value as T` による型キャスト

## v0.6

初公開。その由来については次のようなメモがあります。

## どのようにTolkが生まれたか？

In June 2024, I created a pull request [FunC v0.5.0](https://github.com/ton-blockchain/ton/pull/1026).
Besides this PR, I've written a roadmap for what can be enhanced in FunC, syntactically and semantically.

Instead of merging v0.5.0 and continuing to develop FunC, we decided to **fork** it.
To leave FunC untouched as it is. As it always was. And to develop a new language driven by a fresh and new name.

For several months, I have worked on Tolk privately. I have implemented a giant list of changes.
And it's not only about the syntax. For instance, Tolk has an internal AST representation that is completely missed in FunC.

On TON Gateway, from 1 to 2 November in Dubai, I gave a speech presenting Tolk to the public, and we released it the same day.
The video is available [on YouTube](https://www.youtube.com/watch?v=Frq-HUYGdbI).

ここに最初のプルリクエストがあります: [Tolk Language: 次世代FunC"](https://github.com/ton-blockchain/ton/pull/1345)

Tolk Languageの最初のバージョンはv0.6で、発生する機会を逃したFunC v0.5のメタファーである。

## 名前の意味 "Tolk"

**Tolk** is a wonderful word.

英語では*talk*の子音です。なぜなら、一般的に、言語は何のために必要なのでしょうか?コンピューターと「通信」するにはそれが必要です。

In all Slavic languages, the root *tolk* and the phrase *"to have tolk"* means "to make sense"; "to have deep internals".

しかし、実際には **TOLK** は略語です。\
ご存知のとおり、TON は **The Open Network** です。\
類推すると、TOLK は **The Open Language K** です。

Kとは何か、聞いてみませんか？おそらく、「kot」はニコライ・ドゥロフのニックネームでしょうか？それともKolya？Kitty？Kernel？Kit？Knowledge？\
どれも正しい答えではありません。この文字列には何の意味もありません。\
*The Open Letter K*

<Feedback />

