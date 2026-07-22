# `Char`

Functions for working with the built-in `Char` type.

### `digit_to_int32`

Convert a numeric character ('0'-'9') into its corresponding `int32` value.
If the input character is a valid decimal digit, the function returns
`Some(n)`, where `n` is the integer value of that digit. For example,
`'3'` produces `Some(3)`.
If the character is not a digit, the function returns `None`.

```coal
digit_to_int32 : char -> Option<int32>
```

---

### `ord`

Return the Unicode code point of a character.
Convert the given character into its numeric Unicode scalar value
and return it as an `int32`. This is the inverse of `chr`.

```coal
ord : char -> int32
```

---

### `chr`

Construct a character from a Unicode code point.
Convert the given numeric Unicode scalar value into the corresponding
character. This is the inverse of `ord`.

```coal
chr : int32 -> char
```

---

### `is_digit`

Check if character is a digit (0-9)

```coal
is_digit : char -> bool
```

---

### `is_whitespace`

Check if character is whitespace

```coal
is_whitespace : char -> bool
```

---

### `is_alpha`

Check if character is a letter (a-z, A-Z)

```coal
is_alpha : char -> bool
```

---
