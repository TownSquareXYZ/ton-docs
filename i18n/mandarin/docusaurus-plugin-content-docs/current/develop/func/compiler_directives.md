# Compiler directives

These are keywords that start with `#` and instruct the compiler to do some actions, checks, or change parameters.

Those directives can be used only at the outermost level (not inside any function definition).

## #include

The `#include` directive allows to include another FunC source code file that will be parsed in place of include.

Syntax is `#include "filename.fc";`. Files are automatically checked for re-inclusion, and attempts to include
a file more than once will be ignored by default, with a warning if the verbosity level is no lower than 2.

If an error happens during the parsing of an included file, additionally, a stack of inclusions is printed with the locations
of each included file in the chain.

## #pragma

The `#pragma` directive is used to provide additional information to the compiler beyond what the language itself conveys.

### #pragma version

Version pragma is used to enforce a specific version of FunC compiler when compiling the file.

The version is specified in a semver format, that is, *a.b.c*, where *a* is the major version, *b* is the minor, and *c* is the patch.

There are several comparison operators available to a developer:

* *a.b.c* or *=a.b.c*—requires exactly the *a.b.c* version of the compiler
* *>a.b.c*—requires the compiler version to be higher than *a.b.c*,
  * *>=a.b.c*—requires the compiler version to be higher or equal to *a.b.c*
* *\<a.b.c*—requires the compiler version to be lower than *a.b.c*,
  * *<=a.b.c*—requires the compiler version to be lower or equal to *a.b.c*
* *^a.b.c*—requires the major compiler version to be equal to the 'a' part and the minor to be no lower than the 'b' part,
  * *^a.b*—requires the major compiler version to be equal to *a* part and minor be no lower than *b* part
  * *^a*—requires the major compiler version to be no lower than *a* part

For other comparison operators (*=*, *>*, *>=*, *<*, *<=*) short format assumes zeros in omitted parts, that is:

* *>a.b* is the same as *>a.b.0* (and therefore does NOT match thd *a.b.0* version)
* *<=a* is the same as *<=a.0.0* (and therefore does NOT match the *a.0.1* version)
* *^a.b.0* is **NOT** the same as *^a.b*

For example, *^a.1.2* matches *a.1.3* but not *a.2.3* or *a.1.0*, however, *^a.1* matches them all.

This directive may be used multiple times; the compiler version must satisfy all provided conditions.

### #pragma not-version

The syntax of this pragma is the same as the version pragma but it fails if the condition is satisfied.

It can be used for blacklisting a specific version known to have problems, for example.

### #pragma allow-post-modification

*funC v0.4.1*

By default it is prohibited to use variable prior to its modification in the same expression. In other words, expression `(x, y) = (ds, ds~load_uint(8))` won't compile, while `(x, y) = (ds~load_uint(8), ds)` is valid.

This rule can be overwritten, by `#pragma allow-post-modification`, which allow to modify variable after usage in mass assignments and function invocation; as usual sub-expressions will be computed left to right: `(x, y) = (ds, ds~load_bits(8))` will result in `x` containing initial `ds`; `f(ds, ds~load_bits(8))` first argument of `f` will contain initial `ds`, and second - 8 bits of `ds`.

`#pragma allow-post-modification` works only for code after the pragma.

### #pragma compute-asm-ltr

*funC v0.4.1*

Asm declarations can overwrite order of arguments, for instance in the following expression

```func
idict_set_ref(ds~load_dict(), ds~load_uint(8), ds~load_uint(256), ds~load_ref())
```

order of parsing will be: `load_ref()`, `load_uint(256)`, `load_dict()` and `load_uint(8)` due to following asm declaration (note `asm(value index dict key_len)`):

```func
cell idict_set_ref(cell dict, int key_len, int index, cell value) asm(value index dict key_len) "DICTISETREF";
```

This behavior can be changed to strict left-to-right order of computation via `#pragma compute-asm-ltr`

As a result in

```func
#pragma compute-asm-ltr
...
idict_set_ref(ds~load_dict(), ds~load_uint(8), ds~load_uint(256), ds~load_ref());
```

order of parsing will be `load_dict()`, `load_uint(8)`, `load_uint(256)`, `load_ref()` and all asm permutation will happen after computation.

`#pragma compute-asm-ltr` works only for code after the pragma.
