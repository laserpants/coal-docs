# `Result`

Utilities for working with the built-in `Result` type, which represents the
outcome of a computation that may fail — a success value wrapped in `Ok`, or
an error value wrapped in `Err`.

---

### `is_ok`

Return `true` if the given value is constructed with `Ok`, and `false`
otherwise.

```coal
is_ok : Result<e, a> -> bool
```

---

### `is_err`

Return `true` if the given value is constructed with `Err`, and `false`
otherwise.

```coal
is_err : Result<e, a> -> bool
```

---

### `ok_with_default`

Extract a value of type `a` from a `Result<e, a>` by providing a default
value for the case when the input is `Err`.

```coal
ok_with_default : a -> Result<e, a> -> a
```

---

### `err_with_default`

Extract an error of type `e` from a `Result<e, a>` by providing a default
value for the case when the input is `Ok`.

```coal
err_with_default : e -> Result<e, a> -> e
```
