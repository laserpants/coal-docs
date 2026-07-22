# `Coal.Functor`

A functor abstracts the idea of mapping a function over a container-like structure.

---

### `Functor`

<span class="badge badge-primary">trait</span>

Trait that supports mapping a function over a value in a structured 
context via the `map` operation.

- `map : (a -> b) -> f<a> -> f<b> with (Functor<f>)`

---

### `void`

`void` discards the value inside a functor, replacing it with the 
unit value.

```coal
void : f<a> -> f<unit> with (Functor<f>)
```
