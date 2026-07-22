# `IO`

Functions for input/output operations. This module provides primitive I/O actions that interact with the external environment, such as printing to standard output, reading from standard input, and reading/writing files. All I/O operations are wrapped in the `IO` type to maintain purity in the language.

### `println_string`

Print a string followed by a newline.

Output the given string to standard output, appending a newline
character at the end.

```coal
println_string : string -> IO<unit>
```

---

### `print_string`

Print a string without a trailing newline.

Output the given string to standard output. No newline is appended.

```coal
print_string : string -> IO<unit>
```

---

### `println_int32`

Print a 32-bit integer followed by a newline.

Convert the given `int32` value to its decimal text representation
and output it to standard output, appending a newline.

```coal
println_int32 : int32 -> IO<unit>
```

---

### `print_int32`

Print a 32-bit integer without a trailing newline.

Convert the given `int32` value to its decimal text representation
and output it to standard output.

```coal
print_int32 : int32 -> IO<unit>
```

---

### `println_int64`

Print a 64-bit integer followed by a newline.

Convert the given `int64` value to its decimal text representation
and output it to standard output, appending a newline.

```coal
println_int64 : int64 -> IO<unit>
```

---

### `print_int64`

Print a 64-bit integer without a trailing newline.

Convert the given `int64` value to its decimal text representation
and output it to standard output.

```coal
print_int64 : int64 -> IO<unit>
```

---

### `println_bignum`

Print an arbitrary-precision integer followed by a newline.

Convert the given `bignum` value to its decimal text representation
and output it to standard output, appending a newline.

```coal
println_bignum : bignum -> IO<unit>
```

---

### `print_bignum`

Print an arbitrary-precision integer without a trailing newline.

Convert the given `bignum` value to its decimal text representation
and output it to standard output.

```coal
print_bignum : bignum -> IO<unit>
```

---

### `println_bool`

Print a boolean value followed by a newline.

Output the string representation (`true` or `false`) of the given
boolean to standard output, appending a newline.

```coal
println_bool : bool -> IO<unit>
```

---

### `print_bool`

Print a boolean value without a trailing newline.

Output the string representation (`true` or `false`) of the given
boolean to standard output.

```coal
print_bool : bool -> IO<unit>
```

---

### `println_char`

Print a character followed by a newline.

Output the given character to standard output, appending a newline.

```coal
println_char : char -> IO<unit>
```

---

### `print_char`

Print a character without a trailing newline.

Output the given character to standard output.

```coal
print_char : char -> IO<unit>
```

---

### `println_float`

Print a 32-bit floating-point number followed by a newline.

Convert the given `float` value to its decimal text representation
and output it to standard output, appending a newline.

```coal
println_float : float -> IO<unit>
```

---

### `print_float`

Print a 32-bit floating-point number without a trailing newline.

Convert the given `float` value to its decimal text representation
and output it to standard output.

```coal
print_float : float -> IO<unit>
```

---

### `println_double`

Print a 64-bit floating-point number followed by a newline.

Convert the given `double` value to its decimal text representation
and output it to standard output, appending a newline.

```coal
println_double : double -> IO<unit>
```

---

### `print_double`

Print a 64-bit floating-point number without a trailing newline.

Convert the given `double` value to its decimal text representation
and output it to standard output.

```coal
print_double : double -> IO<unit>
```

---

### `println_nat`

Print a natural number followed by a newline.

Convert the given `nat` value to its decimal text representation
(via `unpack`) and output it to standard output, appending a newline.

```coal
println_nat : nat -> IO<unit>
```

---

### `print_nat`

Print a natural number without a trailing newline.

Convert the given `nat` value to its decimal text representation
(via `unpack`) and output it to standard output.

```coal
print_nat : nat -> IO<unit>
```

---

### `__eval_io`

Evaluate an IO action and extract its result.

Internal primitive that runs the given IO action, returning the
wrapped value of type `v`. This is the eliminator for the `IO` type.

```coal
__eval_io : IO<v> -> v
```

---

### `__return_io`

Lift a pure value into the IO type.

Wrap the given value in an IO action that, when evaluated, produces
that value. This is the introduction form for the `IO` type.

```coal
__return_io : v -> IO<v>
```

---

### `FileIOResult`

Opaque type representing the result of a file I/O operation.

This type is used internally by `read_file` and `write_file` to
communicate both the status code and the result value from the
runtime back to Coal code.

---

### `FileIOError`

Errors that can occur during file I/O operations.

| Constructor    | Description                         |
|----------------|-------------------------------------|
| `FileNotFound` | The specified file does not exist   |
| `InvalidInput` | The input provided was invalid      |
| `IOError`      | A generic I/O error occurred        |
| `OutOfMemory`  | Insufficient memory for the operation |
| `UnknownError` | An unrecognised error occurred      |

---

### `read_file`

Read the contents of a file.

Open the file at the given path, read its contents into a string,
and return the result wrapped in `IO`. On success the result is
`Ok(string)`; on failure it is `Err(FileIOError)`.

```coal
read_file : string -> IO<Result<string, FileIOError>>
```

---

### `write_file`

Write data to a file.

Open the file at the given path and write the given string data
to it. Returns `None` on success, or `Some(FileIOError)` on failure.

```coal
write_file : string -> string -> IO<Option<FileIOError>>
```

---

### `readln`

Read a line of text from standard input.

Read characters from stdin until a newline is encountered, and
return the resulting string (excluding the trailing newline).

```coal
readln : unit -> IO<string>
```

---

### `random`

Generate a random floating-point number.

Return a pseudo-random `double` value uniformly distributed in the
range `[0.0, 1.0)`.

```coal
random : unit -> IO<double>
```

---

### `return`

No documentation available.

---
