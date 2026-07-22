# `Coal.Monad`

Monads extend applicative functors with sequential composition, allowing effectful computations to be chained where each step depends on the result of the previous one.

---

### `Monad`

<span class="badge badge-primary">trait</span>

Trait that extends `Applicative` with `bind` (also known as flat-map), 
enabling sequential composition of effectful computations.

- `bind : m<a> -> (a -> m<b>) -> m<b>`

---

### `then_do`

`then_do` sequences two monadic actions, discarding the result of the
first and returning the second.

```coal
then_do : m<a> -> m<b> -> m<b> with (Monad<m>)
```

---

### `and_then`

`and_then` is `bind` with its arguments flipped: the continuation comes
first, making it read like "and then do this with the result".

```coal
and_then : (a -> m<b>) -> m<a> -> m<b> with (Monad<m>)
```

---

### `and_eval`

`and_eval` is `then_do` with its arguments flipped: the second action is
evaluated first, and the first is returned.

```coal
and_eval : m<b> -> m<a> -> m<a> with (Monad<m>)
```
