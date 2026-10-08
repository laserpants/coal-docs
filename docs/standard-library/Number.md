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

### `int32_to_int64`

Convert a 32-bit integer to a 64-bit integer.

The value is sign-extended.

```coal
int32_to_int64 : int32 -> int64
```

---

### `int64_to_int32`

Convert a 64-bit integer to a 32-bit integer.

The value is truncated; the result is implementation-defined if
the value does not fit in 32 bits.

```coal
int64_to_int32 : int64 -> int32
```

---

### `parse_int32`

Parse a decimal string into a 32-bit integer.

Returns `None` if parsing fails (invalid format or overflow), 
otherwise `Some(int32)`.

```coal
parse_int32 : string -> Option<int32>
```

---

### `parse_int64`

Parse a decimal string into a 64-bit integer.

Returns `None` if parsing fails (invalid format or overflow), 
otherwise `Some(int64)`.

```coal
parse_int64 : string -> Option<int64>
```

---

### `parse_float`

Parse a decimal string into a float.

Returns `None` if parsing fails (invalid format), 
otherwise `Some(float)`.

```coal
parse_float : string -> Option<float>
```

---

### `parse_double`

Parse a decimal string into a double.

Returns `None` if parsing fails (invalid format), 
otherwise `Some(double)`.

```coal
parse_double : string -> Option<double>
```

---

### `parse_integer`

Parse a decimal string into an arbitrary-precision integer.

Returns `None` if parsing fails, otherwise `Some(integer)`.

```coal
parse_integer : string -> Option<integer>
```

---

### `integer_to_float`

Convert an integer to a float.

```coal
integer_to_float : integer -> float
```

---

### `integer_to_double`

Convert an integer to a double.

```coal
integer_to_double : integer -> double
```

---

### `integer_to_string`

Convert an integer to its string representation.

```coal
integer_to_string : integer -> string
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
