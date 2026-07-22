# `Nat`

### `pack`

Convert an `int32` value into a natural number.
Interpret the given integer as a natural number and return the
corresponding `nat` value. If the input is negative, the function
will return `Zero`.

```coal
pack : int32 -> nat
```

---

### `unpack`

Convert a natural number into an `int32` value.
Return the integer representation of the given value as an `int32`.

```coal
unpack : nat -> int32
```

---
