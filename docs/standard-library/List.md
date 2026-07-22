# `List`

### `head`

Return the first element of the list wrapped in `Some`, or `None` if the
list is empty.

```coal
head : List<a> -> Option<a>
```

---

### `tail`

Return the list without its first element, or `None` if the list is empty.

```coal
tail : List<a> -> Option<List<a>>
```

---

### `uncons`

Return a pair (head, tail) wrapped in `Some`, or `None` if the list is 
empty.

```coal
uncons : List<a> -> Option<(a, List<a>)>
```

---

### `length`

Return the length of the list as a natural number.

```coal
length : List<a> -> nat
```

---

### `reduce`

Right-associative fold.
Apply the function to each element and an accumulator, starting from the
end of the list.

```coal
reduce : (a -> b -> b) -> b -> List<a> -> b
```

---

### `reduce_left`

Left-associative fold.

```coal
reduce_left : (b -> a -> b) -> b -> List<a> -> b
```

---

### `singleton`

Return a list containing exactly one element.

```coal
singleton : a -> List<a>
```

---

### `is_empty`

Return `true` if the list is empty, or `false` otherwise.

```coal
is_empty : List<a> -> bool
```

---

### `is_nonempty`

Return `true` if the list contains any elements, or `false` otherwise.

```coal
is_nonempty : List<a> -> bool
```

---

### `is_singleton`

Return `true` if the list contains precisely one element, or `false` 
otherwise.

```coal
is_singleton : List<a> -> bool
```

---

### `concat`

Flatten a list of lists into a single list.

```coal
concat : List<List<a>> -> List<a>
```

---

### `take`

Return the first `n` elements of the list.
If the list is shorter than `n`, return the whole list.

```coal
take : nat -> List<a> -> List<a>
```

---

### `drop`

Remove the first `n` elements from the list.
If the list is shorter than `n`, return an empty list.

```coal
drop : nat -> List<a> -> List<a>
```

---

### `slice`

Extract a range of elements from the list.
slice(m, n, xs) = xs |. drop(m) |. take(n - m)

```coal
slice : nat -> nat -> List<a> -> List<a>
```

---

### `element_at`

Return the element at index `n`, or `None` if out of bounds.

```coal
element_at : nat -> List<a> -> Option<a>
```

---

### `map`

Transform each element of a list using the given function.

```coal
map : (a -> b) -> List<a> -> List<b>
```

---

### `concat_map`

Apply a function to every element of a list, where that function must 
return a list, and then concatenate the resulting lists into a single, 
flattened list.

```coal
concat_map : (a -> List<b>) -> List<a> -> List<b>
```

---

### `filter`

Keep only the elements for which the predicate returns `true`.

```coal
filter : (a -> bool) -> List<a> -> List<a>
```

---

### `reverse`

Return a new list with the elements in reverse order.

```coal
reverse : List<a> -> List<a>
```

---

### `unzip`

Convert a list of pairs into a pair of lists, in the natural way.
E.g., unzip([(1, "one"), (2, "two")]) returns:
([1, 2], ["one", "two"])

```coal
unzip : List<(a, b)> -> (List<a>, List<b>)
```

---

### `zip`

Convert two lists into a list of pairs, in the natural way.
E.g., zip([1, 2], ["one", "two"]) returns:
[(1, "one"), (2, "two")]

```coal
zip : List<a> -> List<b> -> List<(a, b)>
```

---

### `any`

Return `true` if and only if any element of the list satisfies the given 
predicate.

```coal
any : (a -> bool) -> List<a> -> bool
```

---

### `all`

Return `true` if and only if all element of the list satisfy the given 
predicate.

```coal
all : (a -> bool) -> List<a> -> bool
```

---

### `all_true`

Return the conjunction of a list of bools.

```coal
all_true : List<bool> -> bool
```

---

### `any_true`

Return the disjunction of a list of bools.

```coal
any_true : List<bool> -> bool
```

---

### `find`

Return the first element of the list that satisfies the given predicate, 
or `None`, if there is no such element.

```coal
find : (a -> bool) -> List<a> -> Option<a>
```

---

### `is_prefix_of`

Return a boolean indicating whether the first list is a prefix of the 
second.

```coal
is_prefix_of : List<a> -> List<a> -> bool
```

---

### `range`

Return the list [start, start + 1, ..., start + count - 1].

```coal
range : n -> nat -> List<n>
```

---
