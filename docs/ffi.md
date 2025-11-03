# C function interface

When developing applications or libraries that perform network access, disk I/O, or other tasks that interact with low-level system APIs, it is often necessary to interface with code written in C.
This can be achieved in Coal through the C function interface:

```
  #{<c_function_name : t>}(<arg_0>, <arg_1>, ..., <arg_n>)(<continuation>)
```

This expression consists of three components. The first 

```
#{c_function_name : t}
```

Function calls of this type are not inherently type-safe.
The programmer is responsible for 
attention is needed to make sure that 

The second part is a list of arguments to pass to the C function:

```
(<arg_0>, <arg_1>, ..., <arg_n>)
```

The compiler understands and automatically performs the following type conversions:

| Coal primitive     | C type                  | Remarks                  |
| ------------------ | ----------------------- | ------------------------ |
| `bool`             | `bool`                  |                          |
| `char`             | `int32_t`               | A unicode code point     |
| `float`            | `float`                 |                          |
| `double`           | `double`                |                          |
| `int32`            | `int32_t`               |                          |
| `int64`            | `int64_t`               |                          |
| `bignum`           | `mpz_t*`                |                          |
| `string`           | `char*`                 | UTF-8 encoded            |

(<continuation>)

The last 




When compiling your program, pass each C file as an `--extra-c` command line argument. For example:

```
coal Main.coal --extra-c my_c_lib.c -o dist
```


