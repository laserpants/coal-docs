# `Option`

### `with_default`

Extract a value of type `a` from an `Option<a>` by providing a default 
value for the case when the input is `None`.

```coal
with_default : a -> Option<a> -> a
```

---

### `is_some`

Return `true` if the given value is constructed with `Some`, and `false` 
otherwise.

```coal
is_some : Option<a> -> bool
```

---

### `is_none`

Return `true` if the given value is `None`, and `false` otherwise.

```coal
is_none : Option<a> -> bool
```

---

### `option`

From a default value of type `b`, a function of type `a -> b`, and an 
`Option<a>` value, apply the function to the value inside the `Some` 
constructor and return the result, or if the value is `None`, return
the default value.

```coal
option : b -> (a -> b) -> Option<a> -> b
```

---

### `cat_options`

Collect all values contained in `Some` constructors from a list of
`Option<a>` values, discarding occurrences of `None`.

```coal
cat_options : List<Option<a>> -> List<a>
```

---

### `list_to_option`

Convert a list to an `Option<a>` by returning `Some` applied to the first
element of the list, or `None` if the list is empty.

```coal
list_to_option : List<a> -> Option<a>
```

---

### `option_to_list`

Convert an `Option<a>` value to a list by returning a singleton list
containing the value if it is `Some`, or the empty list if it is `None`.

```coal
option_to_list : Option<a> -> List<a>
```

---
