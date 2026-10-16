# C function interface

## Rationale

Programs may need to interact with native libraries or system APIs accessible via code written in C. 
Examples include database drivers, networking libraries, and low-level I/O bindings. 
A *Foreign Function Interface* (FFI) allows a program written in one programming language to call functions written in another. 
In Coal, this is achieved through the C function interface.

Note that a C function call is not an ordinary Coal expression. It is a low-level construct that bridges the language's own type system and runtime representation with the C function's ABI. 

!!! warning "Important!"

    This language feature is primarily intended for library authors. When exposing a C function to Coal, the programmer is responsible for ensuring that each declaration agrees with the corresponding C function. Application code should generally use existing Coal libraries rather than declare C functions directly.

The syntax to specify a C function call is:

```
#{<c_function_name : t>}(<arg_0>, <arg_1>, ..., <arg_n>)(<continuation>)
```

This expression has three parts:

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

### C function type

The type declaration's arity must match the number of arguments, and its argument and result types **determine** the C function signature. 
The compiler checks the type annotation against the Coal arguments and continuation, but it cannot verify that the annotation matches the actual C function signature. 

## Type conversions at the C boundary

The type annotation `t` in `#{name : t}` must be the full function type. It determines the ABI: how arguments are passed and how the result is returned.

Coal uses a uniform boxed representation, `rt_value_t` (`void *`), for values passed to C. However, **arguments and return values are handled differently**.

### Arguments

Each argument is passed as a single `void *`. The C function must recover the value using the appropriate runtime function.

For example, a function annotated `int32 -> double` has the C prototype:

```c
double f(void *arg0);
```

The argument representations and corresponding unboxing functions are listed below.

| Coal type | Representation | Recover in C |
|---|---|---|
| `bool` | Untagged immediate (`0` / `1`) | `rt_bool_unbox(a)` → `bool` |
| `char` | Untagged immediate (Unicode code point) | `rt_char_unbox(a)` → `uint32_t` |
| `int32` | Untagged immediate | `rt_int32_unbox(a)` → `int32_t` |
| `int64` | Untagged immediate | `rt_int64_unbox(a)` → `int64_t` |
| `float` | Heap pointer to `rt_float_t` | `rt_float_unbox(a)` → `float` |
| `double` | Heap pointer to `rt_double_t` | `rt_double_unbox(a)` → `double` |
| `integer` | Heap pointer to `rt_bignum_t` | `rt_bignum_value(rt_bignum_unbox(a))` → `mpz_ptr` |
| `string` | Heap pointer to `rt_string_t` | `rt_string_data(rt_string_unbox(a))` → `char *` |
| `unit` | `NULL` | Ignore |

An *untagged immediate* encodes the value directly in the pointer's numeric value. The runtime's `rt_int32_box`, `rt_int64_box`, `rt_bool_box`, and `rt_char_box` functions use integer-to-pointer casts without allocating memory. For example, an `int32` argument can be recovered with `(int32_t)(intptr_t)a`.

By contrast, `float` and `double` are heap-allocated boxes, so their arguments are actual pointers to runtime objects. Values of other types, such as records, functions, and data constructors, are passed as opaque pointers to their runtime representations.

### Return values

The C function returns a value corresponding to the annotated result type. The generated code boxes primitive results where necessary before passing them to the continuation.

| Coal result type | C return type |
|---|---|
| `bool` | `_Bool` |
| `char` | `uint32_t` (Unicode code point) |
| `int32` | `int32_t` |
| `int64` | `int64_t` |
| `float` | `float` |
| `double` | `double` |
| `integer` | `rt_bignum_t *` |
| `string` | `rt_string_t *` |
| `unit` | `void *` (usually `NULL`) |

Primitive values must be returned unboxed. In particular, a C function returning `float` or `double` must return the actual floating-point value, not a pointer to a boxed value.

For `integer` and `string`, the returned pointer is already the representation expected by Coal. Return an `rt_bignum_t *` or `rt_string_t *` created by the runtime, for example with `rt_bignum_new(...)` or `rt_string_new(...)`. Do not return an `mpz_t *` or a bare `char *` in their place.

The continuation is applied to the result after it has been converted to the representation expected by Coal. The continuation's result type is also the type of the entire `#{...}(...)(...)` expression.

### Ownership and mutation

Coal values are managed by the runtime's garbage collector. Follow these rules when working with them in C:

- **Do not free Coal values.** Do not call `free` on a value passed to C.
- **Use runtime allocation functions.** Return Coal objects created by the runtime, such as `rt_string_new` and `rt_bignum_new`, rather than manually allocating their representations with `malloc`.
- **Treat arguments as borrowed.** Do not retain pointers to runtime objects or their internal data beyond the lifetime guaranteed by the runtime. 
- **Do not mutate Coal values.** Coal values are immutable. Do not modify string bytes or bignum contents through pointers returned by `rt_string_data` or `rt_bignum_value`.

The pointers returned by `rt_string_data` and `rt_bignum_value` refer to data held by runtime objects. Their validity depends on the lifetime of those objects.

## Example

This Coal expression calls a C function that adds two integers:

```coal
#{my_add : int32 -> int32 -> int32}(x, y)(fn(r) => r)
```

The corresponding C function is:

```c
#include <stdint.h>

int32_t my_add(void *a, void *b)
{
    int32_t x = (int32_t)(intptr_t) a;
    int32_t y = (int32_t)(intptr_t) b;
    return x + y;
}
```

The `int32` arguments are untagged immediates, so their integer values are recovered using `intptr_t` casts. Defined in `<stdint.h>`, `intptr_t` is an optional integer type capable of representing converted pointer values. This technique relies on Coal's runtime representation; it is not a general way to convert arbitrary pointers into integers.

The compiler cannot verify that the annotation matches the actual C function signature. The programmer is responsible for ensuring that they agree.

## Compiling C code

Pass each C source file to the compiler using `--extra-c`. For example:

```sh
coal Main.coal --extra-c my_c_lib.c -o dist
```

For project-based builds, specify the C source files in the `c_sources` field of `coal.json`:

```json
{
    "c_sources": [
        "my_c_lib.c"
    ]
}
```
