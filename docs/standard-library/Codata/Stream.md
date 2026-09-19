# `Codata.Stream`

Potentially infinite sequences of values, represented as
`Machine<unit, a>`, i.e., machines whose input is the `unit` value.

Elements are produced on demand: `head` returns the current element, and
`tail` advances the stream to the next one.

---

### `Stream`

<span class="badge badge-primary">type</span>

A stream is a machine whose input is the unit value, so that elements
can be produced on demand.

```coal
Stream<a> = Machine<unit, a>
```

---

### `repeat`

Return a stream that repeats the given element indefinitely.

```coal
repeat : a -> Stream<a>
```

---

### `enum_from`

Return the stream of consecutive integers starting at `n`.

```coal
enum_from : int32 -> Stream<int32>
```

---

### `nats`

The stream of all natural numbers, starting at zero.

Equivalently, `enum_from(0)`.

```coal
nats : Stream<int32>
```

---

### `tail`

Return the stream without its first element.

```coal
tail : Stream<a> -> Stream<a>
```

---

### `head`

Return the first element of the stream.

```coal
head : Stream<a> -> a
```

---

### `cons`

Return a stream whose first element is `state`, followed by the
elements of the given stream.

```coal
cons : a -> Stream<a> -> Stream<a>
```

---

### `map_stream`

Transform each element of a stream using the given function.

```coal
map_stream : (a -> b) -> Stream<a> -> Stream<b>
```

---

### `map2_stream`

Combine two streams elementwise using the given function.

```coal
map2_stream : (a -> b -> c) -> Stream<a> -> Stream<b> -> Stream<c>
```

---

### `map3_stream`

Combine three streams elementwise using the given function.

```coal
map3_stream : (a -> b -> c -> d) -> Stream<a> -> Stream<b> -> Stream<c> -> Stream<d>
```

---

### `map4_stream`

Combine four streams elementwise using the given function.

```coal
map4_stream : (a -> b -> c -> d -> e) -> Stream<a> -> Stream<b> -> Stream<c> -> Stream<d> -> Stream<e>
```

---

### `merge_with`

Interleave two streams, applying `fa` to the elements of the first
stream and `fb` to the elements of the second.

The elements are drawn alternately from `s1` and `s2`, beginning with
`s1`.

```coal
merge_with : (a -> c) -> (b -> c) -> Stream<a> -> Stream<b> -> Stream<c>
```

---

### `merge`

Interleave two streams, alternating between their elements.

Equivalent to `merge_with(identity, identity, s1, s2)`.

```coal
merge : Stream<a> -> Stream<a> -> Stream<a>
```

---

### `scan`

Fold over a stream, returning a stream of successive accumulator
values.

The first element of the result is the initial value `seed`; each
subsequent element is obtained by applying `transition` to the next
element of the stream and the previous accumulator.

```coal
scan : (i -> o -> o) -> o -> Stream<i> -> Stream<o>
```
