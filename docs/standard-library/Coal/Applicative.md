# `Coal.Applicative`

Applicative generalizes function application to effectful or structured contexts.

---

### `Applicative`

<span class="badge badge-primary">trait</span>

Applicative generalizes function application to effectful or structured contexts.

An Applicative functor must support:

- `pure`, which lifts a value into the context, and
- `ap`, which applies a context-wrapped function to a context-wrapped value.

---

### `map2`

`map2` lifts a binary function into an applicative context, applying it to two 
wrapped values.

```coal
map2 : (p -> q -> r) -> f<p> -> f<q> -> f<r> with (Applicative<f>, Functor<f>)
```
