# `Coal.Monad`

Monads extend applicative functors with sequential composition, allowing
effectful computations to be chained where each step depends on the result
of the previous one.

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

### `and_always`

`and_always` is `then_do` with its arguments flipped: the second action is
evaluated first, and the first is returned.

```coal
and_always : m<b> -> m<a> -> m<a> with (Monad<m>)
```

---

### `and_return`

`and_return` is `and_always` composed with `pure`: it runs the given monadic
action, discarding its result, and returns the given pure value.

```coal
and_return : a -> m<b> -> m<a> with (Monad<m>)
```

---

### `join`

`join` flattens a nested monadic value by one level, transforming
`m<m<a>>` into `m<a>`. It is equivalent to `bind` with the identity
function.

```coal
join : m<m<a>> -> m<a> with (Monad<m>)
```

---

### `only_when`

`only_when` conditionally executes an applicative action: it returns the given
action when the predicate is `true`, and an action that produces `()` (and
so has no effect) otherwise.

```coal
only_when : bool -> f<unit> -> f<unit> with (Applicative<f>)
```

---

### `unless`

`unless` is the negation of `only_when`: it runs the given applicative
action only when the predicate is `false`, and does nothing otherwise.

```coal
unless : bool -> f<unit> -> f<unit> with (Applicative<f>)
```
