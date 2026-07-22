# `Number`

Numeric utilities and conversions.

---

### `_INT32_MAX`

Maximum value representable by a 32-bit signed integer.

---

### `_INT64_MAX`

Maximum value representable by a 64-bit signed integer.

---

### `_INT32_MIN`

Minimum value representable by a 32-bit signed integer.

---

### `_INT64_MIN`

Minimum value representable by a 64-bit signed integer.

---

### `int32_to_float`

Convert a 32-bit integer to a float.

```coal
int32_to_float : int32 -> float
```

---

### `int32_to_double`

Convert a 32-bit integer to a double.

```coal
int32_to_double : int32 -> double
```

---

### `int64_to_float`

Convert a 64-bit integer to a float.

```coal
int64_to_float : int64 -> float
```

---

### `int64_to_double`

Convert a 64-bit integer to a double.

```coal
int64_to_double : int64 -> double
```

---

### `float_to_int32`

Convert a float to a 32-bit integer.

```coal
float_to_int32 : float -> int32
```

---

### `double_to_int32`

Convert a double to a 32-bit integer.

```coal
double_to_int32 : double -> int32
```

---

### `float_to_int64`

Convert a float to a 64-bit integer.

```coal
float_to_int64 : float -> int64
```

---

### `double_to_int64`

Convert a double to a 64-bit integer.

```coal
double_to_int64 : double -> int64
```

---

### `parse_bignum`

Parse a decimal string into a bignum.

Returns `None` if parsing fails, otherwise `Some(bignum)`.

```coal
parse_bignum : string -> Option<bignum>
```

---

### `bignum_to_float`

Convert a bignum to a float.

```coal
bignum_to_float : bignum -> float
```

---

### `bignum_to_double`

Convert a bignum to a double.

```coal
bignum_to_double : bignum -> double
```

---

### `max`

Return the greater of two comparable values.

```coal
max : a -> a -> a with (Ordered<a>)
```

---

### `maximum`

Compute the maximum element of a list.

Returns `None` for an empty list.

```coal
maximum : List<a> -> Option<a> with (Ordered<a>)
```

---

### `is_even`

Test whether a number is even.

```coal
is_even : a -> bool with (Modulo<a>)
```

---

### `is_odd`

Test whether a number is odd.

```coal
is_odd : a -> bool with (Modulo<a>)
```
