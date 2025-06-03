import Feedback from '@site/src/components/Feedback';

# Tolk의 역사

새로운 버전의 Tolk가 출시되면 여기에 기록될 것입니다.

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

1. 내부적으로: 컴파일러 내부 리팩토링; AST 레벨 시맨틱 분석 커널
2. 내부적으로: Hindley-Milner에서 정적 타이핑으로 타입 시스템 재작성
3. 타입 불일치에 대한 명확하고 읽기 쉬운 오류 메시지
4. 제네릭 함수 `fun f<T>(...)` 및 `f<int>(...)`와 같은 인스턴스화
5. `bool` 타입; `value as T`를 통한 타입 캐스팅

## v0.6

첫 번째 공개 릴리스입니다. 다음은 그 기원에 대한 몇 가지 참고사항입니다:

## Tolk는 어떻게 탄생했나

In June 2024, I created a pull request [FunC v0.5.0](https://github.com/ton-blockchain/ton/pull/1026).
Besides this PR, I've written a roadmap for what can be enhanced in FunC, syntactically and semantically.

Instead of merging v0.5.0 and continuing to develop FunC, we decided to **fork** it.
To leave FunC untouched as it is. As it always was. And to develop a new language driven by a fresh and new name.

For several months, I have worked on Tolk privately. I have implemented a giant list of changes.
And it's not only about the syntax. For instance, Tolk has an internal AST representation that is completely missed in FunC.

On TON Gateway, from 1 to 2 November in Dubai, I gave a speech presenting Tolk to the public, and we released it the same day.
The video is available [on YouTube](https://www.youtube.com/watch?v=Frq-HUYGdbI).

여기 최초의 풀 리퀘스트가 있습니다: ["Tolk Language: next-generation FunC"](https://github.com/ton-blockchain/ton/pull/1345).

Tolk 언어의 첫 번째 버전은 v0.6으로, 일어날 기회를 놓친 FunC v0.5에 대한 은유입니다.

## "Tolk"라는 이름의 의미

**Tolk** is a wonderful word.

영어에서는 *talk*와 발음이 비슷합니다. 일반적으로, 우리가 언어를 필요로 하는 이유가 무엇일까요? 우리는 컴퓨터와 *대화하기* 위해 필요로 합니다.

In all Slavic languages, the root *tolk* and the phrase *"to have tolk"* means "to make sense"; "to have deep internals".

하지만 실제로, **TOLK**는 약어입니다.\
여러분은 TON이 **The Open Network**라는 것을 알고 있습니다.\
이와 유사하게, TOLK는 **The Open Language K**입니다.

K가 무엇이냐고요? 아마도 Nikolay Durov의 닉네임인 "kot"? 아니면 Kolya? Kitten? Kernel? Kit? Knowledge?\
정답은 - 이 중 어느 것도 아닙니다. 이 문자는 아무 의미가 없습니다. 그것은 열려있습니다.\
*The Open Letter K*

<Feedback />

