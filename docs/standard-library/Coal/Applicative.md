# `Coal.Applicative`

Applicative generalizes function application to effectful or structured contexts.

---

### `Applicative`

<span class="badge badge-primary">trait</span>

Applicative generalizes function application to effectful or structured contexts.

An Applicative functor must support:

- `pure : a -> f<a>`, which lifts a value into the context, and
- `ap : f<a -> b> -> f<a> -> f<b>`, which applies a context-wrapped function to a context-wrapped value.

---

### `map2`

`map2` lifts a binary function into an applicative context, applying it to two 
wrapped values.

```coal
map2 : (p -> q -> r) -> f<p> -> f<q> -> f<r> with (Applicative<f>, Functor<f>)
```

---

### `traverse_list`

`traverse_list` applies an applicative-producing function to every element
of a list and combines the results into a single wrapped list.

```coal
traverse_list : (a -> f<b>) -> List<a> -> f<List<b>> with (Applicative<f>)
```
