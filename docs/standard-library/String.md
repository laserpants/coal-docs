# `String`

Functions for working with the built-in `string` type.

---

### `char_to_string`

Convert a character to a one-character string.

```coal
char_to_string : char -> string
```

---

### `bool_to_string`

Convert a boolean to a string, i.e., either "true" or "false".

```coal
bool_to_string : bool -> string
```

---

### `int32_to_string`

Convert an int32 value to its string representation.

```coal
int32_to_string : int32 -> string
```

---

### `float_to_string`

Convert a floating-point value to its string representation.

```coal
float_to_string : float -> string
```

---

### `double_to_string`

Convert a double-precision value to its string representation.

```coal
double_to_string : double -> string
```

---

### `to_list`

Convert a string into a list of its characters.

```coal
to_list : string -> List<char>
```

---

### `from_list`

Build a string from a list of characters.

```coal
from_list : List<char> -> string
```

---

### `length`

Return the number of characters in the string.

```coal
length : string -> nat
```

---

### `is_empty`

Determine whether the string is empty.

```coal
is_empty : string -> bool
```

---

### `head`

Return the first character of the string, or `None` if empty.

```coal
head : string -> Option<char>
```

---

### `tail`

Return the string without its first character.

```coal
tail : string -> string
```

---

### `cons`

Prepend a character to the front of a string.

```coal
cons : char -> string -> string
```

---

### `uncons`

Return the head and tail of a string, as a pair.

```coal
uncons : string -> (Option<char>, string)
```

---

### `reverse`

Reverse the characters in the string.

```coal
reverse : string -> string
```

---

### `remove_whitespace`

Remove all whitespace characters from the string.

```coal
remove_whitespace : string -> string
```

---

### `intercalate`

Insert a separator between the strings in a list and concatenate them.

```coal
intercalate : string -> List<string> -> string
```

---

### `concat`

Take a list of strings and concatenate them into a single string.

```coal
concat : List<string> -> string
```

---

### `is_prefix_of`

Return a boolean indicating whether the first string is a prefix of the 
second.

```coal
is_prefix_of : string -> string -> bool
```

---

### `drop`

Remove the first `n` characters from the string.

If the string is shorter than `n`, return an empty string.

```coal
drop : nat -> string -> string
```
