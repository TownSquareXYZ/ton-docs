import Feedback from '@site/src/components/Feedback';

# Tolk 的历史

当 Tolk 发布新版本时，我们将在此提及。

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

## v0.6

1. Syntax `tensorVar.0` and `tupleVar.0` (both for reading and writing)
2. Allow `cell`, `slice`, etc. to be valid identifiers (not keywords)

## Tolk 是如何诞生的

1. Under the hood: refactor compiler internals; AST-level semantic analysis kernel
2. Under the hood: rewrite the type system from Hindley-Milner to static typing
3. Clear and readable error messages on type mismatch
4. Generic functions `fun f<T>(...)` and instantiations like `f<int>(...)`
5. The `bool` type; type casting via `value as T`

## v0.6

几个月来，我一直在私下开发 Tolk。我进行了大量的修改。
这不仅仅是语法的问题。例如，Tolk 拥有 FunC 完全没有的内部 AST 表示法。

## Tolk 是如何诞生的

In June 2024, I created a pull request [FunC v0.5.0](https://github.com/ton-blockchain/ton/pull/1026).
Besides this PR, I've written a roadmap for what can be enhanced in FunC, syntactically and semantically.

Instead of merging v0.5.0 and continuing to develop FunC, we decided to **fork** it.
To leave FunC untouched as it is. As it always was. And to develop a new language driven by a fresh and new name.

For several months, I have worked on Tolk privately. I have implemented a giant list of changes.
And it's not only about the syntax. For instance, Tolk has an internal AST representation that is completely missed in FunC.

On TON Gateway, from 1 to 2 November in Dubai, I gave a speech presenting Tolk to the public, and we released it the same day.
The video is available [on YouTube](https://www.youtube.com/watch?v=Frq-HUYGdbI).

这是第一个拉取请求：["Tolk Language: next-generation FunC"](https://github.com/ton-blockchain/ton/pull/1345)。

Tolk 语言的第一个版本是 v0.6，它是 FunC v0.5 的一个隐喻，错过了出现的机会。

## 名字 "Tolk "的含义

**Tolk** is a wonderful word.

In English, it's consonant with *talk*. Because, generally, what do we need a language for? We need it *to talk* to computers.

In all Slavic languages, the root *tolk* and the phrase *"to have tolk"* means "to make sense"; "to have deep internals".

But actually, **TOLK** is an abbreviation.\
You know, that TON is **The Open Network**.\
By analogy, TOLK is **The Open Language K**.

What is K, will you ask? Probably, "kot" — the nick of Nikolay Durov? Or Kolya? Kitten? Kernel? Kit? Knowledge?\
The right answer — none of this. This letter does not mean anything. It's open.\
*The Open Letter K*

<Feedback />

