# `Coal.Monad.Free`

The free monad.

The free monad turns any functor `f` into a monad by describing computations
as data: a computation is built as a tree of `f`-shaped instructions, which a
separate interpreter can later give meaning to. This separates the
description of an effectful computation from its interpretation.

---

### `Free`

<span class="badge badge-primary">type</span>

The free monad over a functor `f`.

A `Free<f, a>` value is either a finished computation, `Pure(a)`, or a
single layer of `f` whose continuations are themselves `Free<f, a>`
computations, `Free(f<Free<f, a>>)`.

`Free<f>` is a `Functor`, `Applicative` and `Monad` whenever `f` is a
`Functor`.

---

### `lift_free`

Lift a single instruction into the free monad.

`lift_free(e)` is the one-step program that runs the instruction `e` and
then finishes with `pure` of its payload: `lift_free(WriteLn("hi", ()))`
is `Free(WriteLn("hi", Pure(())))`.

```coal
lift_free : f<a> -> Free<f, a> with (Functor<f>)
```

---

### `interpret`

Interpret a free program by running each instruction layer through the
handler.

`interpret(handler, instructions)` folds `instructions` bottom-up: the
handler turns one layer of instructions whose continuations have already
been interpreted into an `m`-computation, and `pure` finishes a program
that has run out of instructions.

```coal
interpret : (f<m<a>> -> m<a>) -> Free<f, a> -> m<a> with (Monad<m>)
```

---

### `map_free`

No documentation available.

---

### `ap_free`

No documentation available.

---

### `bind_free`

No documentation available.
