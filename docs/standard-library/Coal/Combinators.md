# `Coal.Combinators`

Combinators and tuple operations for functional programming.

---

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
