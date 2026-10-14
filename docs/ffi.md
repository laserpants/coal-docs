# C function interface

## Rationale

Some applications need to interact with native libraries or system APIs accessible through C. Examples include database drivers, networking libraries, and low-level I/O bindings.
In Coal, this is achieved through the C (foreign) function interface.

!!! info 

    A *Foreign Function Interface* (FFI) allows a program written in one programming language to call routines or use services written in another one.

The syntax to specify a C function call is:

```
#{<c_function_name : t>}(<arg_0>, <arg_1>, ..., <arg_n>)(<continuation>)
```

This expression has three subcomponents:

1. The first part is the C function to call. Note that, unlike other expressions in Coal, the type annotation is mandatory here.

    ```
    #{c_function_name : t}
    ```

2. The second part is a list of arguments to pass to the C function.

    ```
    (<arg_0>, <arg_1>, ..., <arg_n>)
    ```

3. The last component is the *continuation*. After the C function returns, the generated code passes its result to this expression. 

    ```
    (<continuation>)
    ```

### Matching the C signature

A C function call is not an ordinary Coal expression. It is a low-level construct 
that bridges Coal's type system and runtime representation with the C function's ABI. 
The compiler checks the type annotation against the Coal arguments and continuation, but it
cannot verify that the annotation matches the actual C function signature. 
The type declaration’s arity must match the number of arguments, and its argument 
and result types determine the C function signature.
The programmer is responsible for ensuring that the declaration in Coal agrees with the C implementation.

## Type conversions at the C boundary

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

**C function return values.** The C function returns the C value corresponding
to the annotated result type, and the generated code boxes primitive results
where necessary before passing them to the continuation. The declared C return
type must be:

| Coal result type | C return type |
| ---------------- | ------------- |
| `bool`           | `bool` (`_Bool`) |
| `char`           | `uint32_t` (Unicode code point) |
| `int32`          | `int32_t` |
| `int64`          | `int64_t` |
| `float`          | `float` (unboxed) |
| `double`         | `double` (unboxed) |
| `integer`        | `rt_bignum_t *` (never `mpz_t *`) |
| `string`         | `rt_string_t *` (never `char *`) |
| `unit`           | `void *` (usually `NULL`) |

For primitives the value is returned raw and boxed by the generated code.
Returning a boxed `float`/`double` (an `rt_value_t` heap pointer) is wrong: the
generator declares the function with its raw floating-point return type and
reads the result straight out of the machine register, so the callee must return
the unboxed value. For `integer` and `string`, by contrast, the returned pointer
*is* the boxed representation (the box is the identity), so the function returns
the `rt_bignum_t *` / `rt_string_t *` produced by the runtime (for example
`rt_bignum_new(...)`, `rt_string_new(...)`), not a GMP `mpz_t *` and not a bare
`char *`.

**Ownership and mutation.** Coal values are managed by the runtime's garbage
collector. Do not `free` a value passed to C, and do not build a value to return
with `malloc`: return an object created by the runtime (for example
`rt_string_new`, `rt_bignum_new`). Treat arguments as borrowed for the duration
of the call. The pointers returned by `rt_string_data` and `rt_bignum_value`
point into the runtime object, so they are valid only while that object is
alive; do not retain one past the call unless you keep a reference to the
object. Coal values are immutable, so do not modify the bytes of a string or the
contents of a bignum through those pointers.

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
    /* int32 arguments are untagged immediates: the pointer's numeric value is
       the integer itself, so it is recovered with an intptr_t cast. */
    int32_t x = (int32_t)(intptr_t) a;
    int32_t y = (int32_t)(intptr_t) b;
    return x + y;
}
```

`intptr_t`, defined in `<stdint.h>`, is an integer type that can represent a 
converted pointer value on implementations that provide it. Here, the cast 
recovers the integer encoded in the untagged immediate. This relies on Coal's 
runtime representation and is not a general way to convert arbitrary pointers 
into integers.

When compiling your program, pass each C file as an `--extra-c` command line argument. For example:

```
coal Main.coal --extra-c my_c_lib.c -o dist
```

For project-based builds, specify the `c_sources` field in your project's `coal.json` configuration:


```json
    "c_sources": [
        "my_c_lib.c"
    ]
```

