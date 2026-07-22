# Core modules

This documentation is automatically generated from docblocks in the standard library source code.

## `Char`

### `digit_to_int32`

Convert a numeric character ('0'-'9') into its corresponding `int32` value.
If the input character is a valid decimal digit, the function returns
`Some(n)`, where `n` is the integer value of that digit. For example,
`'3'` produces `Some(3)`.
If the character is not a digit, the function returns `None`.

---

### `ord`

Return the Unicode code point of a character.
Convert the given character into its numeric Unicode scalar value
and return it as an `int32`. This is the inverse of `chr`.

---

### `chr`

Construct a character from a Unicode code point.
Convert the given numeric Unicode scalar value into the corresponding
character. This is the inverse of `ord`.

---

### `is_digit`

Check if character is a digit (0-9)

---

### `is_whitespace`

Check if character is whitespace

---

### `is_alpha`

Check if character is a letter (a-z, A-Z)

---

## `Coal.Applicative`

### `map2`

No documentation available.

---

## `Coal.Combinators`

### `identity`

The identity function.
Returns the value unchanged.

```coal
identity : a -> a
```

---

### `always`

When applied to one argument, return a function that always returns this 
value.

```coal
always : a -> b -> a
```

---

### `fst`

Extract the first element of a pair.

```coal
fst : (a, b) -> a
```

---

### `snd`

Extract the second element of a pair.

```coal
snd : (a, b) -> b
```

---

### `apply_fst`

Apply a function to the first element of a pair.

```coal
apply_fst : (a -> b) -> (a, c) -> (b, c)
```

---

### `apply_snd`

Apply a function to the second element of a pair.

```coal
apply_snd : (b -> c) -> (a, b) -> (a, c)
```

---

### `swap`

Swap the components of a pair.

```coal
swap : (a, b) -> (b, a)
```

---

### `fst3`

Extract the first element of a triple.

```coal
fst3 : (a, b, c) -> a
```

---

### `snd3`

Extract the second element of a triple.

```coal
snd3 : (a, b, c) -> b
```

---

### `thd3`

Extract the third element of a triple.

```coal
thd3 : (a, b, c) -> c
```

---

### `curry`

Convert a function that takes a pair into one that takes two arguments.

```coal
curry : ((a, b) -> c) -> a -> b -> c
```

---

### `uncurry`

Convert a function of two arguments into one that takes a pair.

```coal
uncurry : (a -> b -> c) -> (a, b) -> c
```

---

### `flip`

Reverse the order of the arguments to a two-argument function.

```coal
flip : (a -> b -> c) -> b -> a -> c
```

---

### `iterate`

Apply the function `f` to the value `x`, `n` times.

```coal
iterate : nat -> (a -> a) -> a -> a
```

---

## `Coal.Functor`

### `void`

No documentation available.

---

## `Coal.Monad`

### `then_do`

No documentation available.

---

### `and_then`

No documentation available.

---

### `and_eval`

No documentation available.

---

## `Coal.Monoid`

*No documented definitions.*

## `Codata.Machine`

### `observe`

No documentation available.

---

### `receive`

No documentation available.

---

### `machine`

No documentation available.

---

### `map_machine`

No documentation available.

---

### `map2_machine`

No documentation available.

---

### `map3_machine`

No documentation available.

---

### `map4_machine`

No documentation available.

---

### `contramap_input`

No documentation available.

---

### `compose`

No documentation available.

---

### `duplicate`

No documentation available.

---

### `zip`

No documentation available.

---

### `zip2`

No documentation available.

---

### `zip3`

No documentation available.

---

### `zip4`

No documentation available.

---

### `cons`

No documentation available.

---

### `process`

No documentation available.

---

### `cofix`

No documentation available.

---

### `run_while`

No documentation available.

---

## `Codata.Stream`

### `Stream`

No documentation available.

---

### `repeat`

No documentation available.

---

### `enum_from`

No documentation available.

---

### `nats`

No documentation available.

---

### `tail`

No documentation available.

---

### `head`

No documentation available.

---

### `map_stream`

No documentation available.

---

### `map2_stream`

No documentation available.

---

### `map3_stream`

No documentation available.

---

### `map4_stream`

No documentation available.

---

### `merge_with`

No documentation available.

---

### `merge`

No documentation available.

---

### `scan`

No documentation available.

---

## `IO`

### `println_string`

No documentation available.

---

### `print_string`

No documentation available.

---

### `println_int32`

No documentation available.

---

### `print_int32`

No documentation available.

---

### `println_int64`

No documentation available.

---

### `print_int64`

No documentation available.

---

### `println_bignum`

No documentation available.

---

### `print_bignum`

No documentation available.

---

### `println_bool`

No documentation available.

---

### `print_bool`

No documentation available.

---

### `println_char`

No documentation available.

---

### `print_char`

No documentation available.

---

### `println_float`

No documentation available.

---

### `print_float`

No documentation available.

---

### `println_double`

No documentation available.

---

### `print_double`

No documentation available.

---

### `println_nat`

No documentation available.

---

### `print_nat`

No documentation available.

---

### `__eval_io`

No documentation available.

---

### `__return_io`

No documentation available.

---

### `return`

No documentation available.

---

### `FileIOResult`

No documentation available.

---

### `FileIOError`

No documentation available.

---

### `read_file`

No documentation available.

---

### `write_file`

No documentation available.

---

### `readln`

No documentation available.

---

### `random`

No documentation available.

---

## `List`

### `head`

Return the first element of the list wrapped in `Some`, or `None` if the
list is empty.

---

### `tail`

Return the list without its first element, or `None` if the list is empty.

---

### `uncons`

Return a pair (head, tail) wrapped in `Some`, or `None` if the list is 
empty.

---

### `length`

Return the length of the list as a natural number.

---

### `reduce`

Right-associative fold.
Apply the function to each element and an accumulator, starting from the
end of the list.

---

### `reduce_left`

Left-associative fold.

---

### `singleton`

Return a list containing exactly one element.

---

### `is_empty`

Return `true` if the list is empty, or `false` otherwise.

---

### `is_nonempty`

Return `true` if the list contains any elements, or `false` otherwise.

---

### `is_singleton`

Return `true` if the list contains precisely one element, or `false` 
otherwise.

---

### `concat`

Flatten a list of lists into a single list.

---

### `take`

Return the first `n` elements of the list.
If the list is shorter than `n`, return the whole list.

---

### `drop`

Remove the first `n` elements from the list.
If the list is shorter than `n`, return an empty list.

---

### `slice`

Extract a range of elements from the list.
slice(m, n, xs) = xs |. drop(m) |. take(n - m)

---

### `element_at`

Return the element at index `n`, or `None` if out of bounds.

---

### `map`

Transform each element of a list using the given function.

---

### `concat_map`

Apply a function to every element of a list, where that function must 
return a list, and then concatenate the resulting lists into a single, 
flattened list.

---

### `filter`

Keep only the elements for which the predicate returns `true`.

---

### `reverse`

Return a new list with the elements in reverse order.

---

### `unzip`

Convert a list of pairs into a pair of lists, in the natural way.
E.g., unzip([(1, "one"), (2, "two")]) returns:
([1, 2], ["one", "two"])

---

### `zip`

Convert two lists into a list of pairs, in the natural way.
E.g., zip([1, 2], ["one", "two"]) returns:
[(1, "one"), (2, "two")]

---

### `any`

Return `true` if and only if any element of the list satisfies the given 
predicate.

---

### `all`

Return `true` if and only if all element of the list satisfy the given 
predicate.

---

### `all_true`

Return the conjunction of a list of bools.

---

### `any_true`

Return the disjunction of a list of bools.

---

### `find`

Return the first element of the list that satisfies the given predicate, 
or `None`, if there is no such element.

---

### `is_prefix_of`

Return a boolean indicating whether the first list is a prefix of the 
second.

---

### `range`

Return the list [start, start + 1, ..., start + count - 1].

---

## `Nat`

### `pack`

Convert an `int32` value into a natural number.
Interpret the given integer as a natural number and return the
corresponding `nat` value. If the input is negative, the function
will return `Zero`.

---

### `unpack`

Convert a natural number into an `int32` value.
Return the integer representation of the given value as an `int32`.

---

## `Number`

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

---

### `int32_to_double`

Convert a 32-bit integer to a double.

---

### `int64_to_float`

Convert a 64-bit integer to a float.

---

### `int64_to_double`

Convert a 64-bit integer to a double.

---

### `float_to_int32`

Convert a float to a 32-bit integer.

---

### `double_to_int32`

Convert a double to a 32-bit integer.

---

### `float_to_int64`

Convert a float to a 64-bit integer.

---

### `double_to_int64`

Convert a double to a 64-bit integer.

---

### `parse_bignum`

Parse a decimal string into a bignum.
Returns `None` if parsing fails, otherwise `Some(bignum)`.

---

### `bignum_to_float`

Convert a bignum to a float.

---

### `bignum_to_double`

Convert a bignum to a double.

---

### `max`

Return the greater of two comparable values.

---

### `maximum`

Compute the maximum element of a list.
Returns `None` for an empty list.

---

### `is_even`

Test whether a number is even.

---

### `is_odd`

Test whether a number is odd.

---

## `Option`

### `with_default`

Extract a value of type `a` from an `Option<a>` by providing a default 
value for the case when the input is `None`.

---

### `is_some`

Return `true` if the given value is constructed with `Some`, and `false` 
otherwise.

---

### `is_none`

Return `true` if the given value is `None`, and `false` otherwise.

---

### `option`

From a default value of type `b`, a function of type `a -> b`, and an 
`Option<a>` value, apply the function to the value inside the `Some` 
constructor and return the result, or if the value is `None`, return
the default value.

---

### `cat_options`

Collect all values contained in `Some` constructors from a list of
`Option<a>` values, discarding occurrences of `None`.

---

### `list_to_option`

Convert a list to an `Option<a>` by returning `Some` applied to the first
element of the list, or `None` if the list is empty.

---

### `option_to_list`

Convert an `Option<a>` value to a list by returning a singleton list
containing the value if it is `Some`, or the empty list if it is `None`.

---

## `String`

### `char_to_string`

Convert a character to a one-character string.

---

### `bool_to_string`

Convert a boolean to a string, i.e., either "true" or "false".

---

### `int32_to_string`

Convert an int32 value to its string representation.

---

### `float_to_string`

Convert a floating-point value to its string representation.

---

### `double_to_string`

Convert a double-precision value to its string representation.

---

### `to_list`

Convert a string into a list of its characters.

---

### `from_list`

Build a string from a list of characters.

---

### `length`

Return the number of characters in the string.

---

### `is_empty`

Determine whether the string is empty.

---

### `head`

Return the first character of the string, or `None` if empty.

---

### `tail`

Return the string without its first character.

---

### `cons`

Prepend a character to the front of a string.

---

### `uncons`

Return the head and tail of a string, as a pair.

---

### `reverse`

Reverse the characters in the string.

---

### `remove_whitespace`

Remove all whitespace characters from the string.

---

### `intercalate`

Insert a separator between the strings in a list and concatenate them.

---

### `concat`

Take a list of strings and concatenate them into a single string.

---

### `is_prefix_of`

Return a boolean indicating whether the first string is a prefix of the 
second.

---

### `drop`

Remove the first `n` characters from the string.
If the string is shorter than `n`, return an empty string.

---
