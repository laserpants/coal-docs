# C function interface

## Rationale

Some applications need to interact with native libraries or system APIs accessible through C. Examples include database drivers, networking libraries, and low-level I/O.
In Coal, this is achieved through the C (foreign) function interface.

!!! info 

    A *foreign function interface* (FFI) allows a program written in one programming language to call routines or use services written in another one.

The syntax to specify a C function call is:

```
#{<c_function_name : t>}(<arg_0>, <arg_1>, ..., <arg_n>)(<continuation>)
```

This expression consists of three components:

1. The first part is the C function to call. Note that the type annotation is mandatory.

    ```
    #{c_function_name : t}
    ```

2. The second part is a list of arguments to pass to the C function.

    ```
    (<arg_0>, <arg_1>, ..., <arg_n>)
    ```

3. The last component is the *continuation*. After the C function returns, Coal passes its result to this expression. 

    ```
    (<continuation>)
    ```

An important point is that the compiler cannot check the type annotation against the C
function's real signature. The annotation is checked against the argument and continuation
types, but the programmer is responsible for keeping it in sync with the C code.

### Type conversions at the C boundary

The conversions are **not symmetric**, and the annotation `t` in `#{name : t}`
must be the full function type. It determines the ABI. The code generator uses the
runtime's uniform boxed representation, `rt_value_t` (a `void *`).

**Arguments are boxed.** Each argument is boxed into one `rt_value_t`, and the
C function is declared as taking one `void *` per argument. A function
annotated `int32 -> double` therefore has the C prototype

```c
double f(void *arg0);
```

Inside the C function the value is recovered by unboxing it:

| Coal argument type | Boxed representation passed as `void *` | Recover in C |
| ------------------ | --------------------------------------- | ------------ |
| `bool`             | untagged immediate (`0` / `1`)          | `rt_bool_unbox(a)` -> `bool` |
| `char`             | untagged immediate (Unicode code point) | `rt_char_unbox(a)` -> `uint32_t` |
| `int32`            | untagged immediate                      | `rt_int32_unbox(a)` -> `int32_t` |
| `int64`            | untagged immediate                      | `rt_int64_unbox(a)` -> `int64_t` |
| `float`            | heap pointer to an `rt_float_t`         | `rt_float_unbox(a)` -> `float` |
| `double`           | heap pointer to an `rt_double_t`        | `rt_double_unbox(a)` -> `double` |
| `integer`          | heap pointer to an `rt_bignum_t`        | `rt_bignum_value(rt_bignum_unbox(a))` -> `mpz_ptr` |
| `string`           | heap pointer to an `rt_string_t`        | `rt_string_data(rt_string_unbox(a))` -> `char *` (UTF-8, NUL-terminated) |
| `unit`             | `NULL`                                  | ignore |

"Untagged immediate" means the pointer's numeric value *is* the value:
`rt_int32_box`, `rt_int64_box`, `rt_bool_box`, and `rt_char_box` are plain
integer-to-pointer casts that allocate nothing, so an `int32` argument can also
be recovered as `(int32_t)(intptr_t)a`. `float` and `double` are different: they
are heap-boxed, so the argument really is a pointer. Values of other types
(records, functions, data constructors) are passed as opaque pointers to their
runtime representation.

**Results are returned unboxed.** The C function returns the *raw* C value
and the code generator boxes it itself before passing it to the continuation.
The declared C return type must be:

| Coal result type | C return type |
| ---------------- | ------------- |
| `bool`           | `bool` (`_Bool`) |
| `char`           | `uint32_t` / `int32_t` (Unicode code point) |
| `int32`          | `int32_t` |
| `int64`          | `int64_t` |
| `float`          | `float` (unboxed) |
| `double`         | `double` (unboxed) |
| `integer`        | `rt_bignum_t *` (never `mpz_t *`) |
| `string`         | `rt_string_t *` (never `char *`) |
| `unit`           | `void *` (usually `NULL`) |

Returning a boxed `float`/`double` (an `rt_value_t` heap pointer) is wrong: the
generator declares the function with its raw floating-point return type and
reads the result straight out of the machine register, so the callee must return
the unboxed value. For `integer` and `string` the boxed representation *is* the
object pointer, so the function returns the `rt_bignum_t *` / `rt_string_t *`
produced by the runtime (for example `rt_bignum_new(...)`, `rt_string_new(...)`),
not a GMP `mpz_t *` and not a bare `char *`.

The continuation is applied to the boxed result through the runtime's uniform
application, and the code generator unboxes it to the continuation's result
type, which is also the type of the whole `#{...}(...)(...)` expression.

For example, this Coal call

```coal
#{my_add : int32 -> int32 -> int32}(x, y)(fn(r) => r)
```

matches

```c
#include <stdint.h>

int32_t my_add(void *a, void *b)
{
    int32_t x = (int32_t)(intptr_t) a;
    int32_t y = (int32_t)(intptr_t) b;
    return x + y;
}
```

When compiling your program, pass each C file as an `--extra-c` command line argument. For example:

```
coal Main.coal --extra-c my_c_lib.c -o dist
```

For project-based builds, specify the `c_sources` field in your project's `coal.json` configuration.


```json
    "c_sources": [
        "runtime.c"
    ]
```

