# `Nat`

Functions for converting between `nat` values and the ordinary integer
representation of the natural numbers.

The built-in `nat` type is defined as:

```
type nat
  = Zero
  | Succ(nat)
```

Note that it is not necessary to use `pack` explicitly when working with
numeric literals. For example, you can write:

```
let
  x : nat = 5
  in
```

and the compiler will perform the conversion automatically. This works
because numeric literals are overloaded.

---

### `pack`

Convert an `int64` value into a natural number.

Interpret the given integer as a natural number and return the
corresponding `nat` value. If the input is negative, the function
will return `Zero`.

```coal
pack : int64 -> nat
```

---

### `unpack`

Convert a natural number into an `int64` value.

Return the integer representation of the given value as an `int64`.

```coal
unpack : nat -> int64
```

---

### `Natural`

<span class="badge badge-primary">trait</span>

Trait that comprises types that can be converted to `nat`, via:

- `to_nat : n -> nat`

---

### `pred`

Return the predecessor of a natural number.

Returns `Zero` for `Zero` (saturation), otherwise strips one `Succ`
constructor.

```coal
pred : nat -> nat
```

---

### `sub`

Saturating subtraction of natural numbers.

Returns `Zero` when `n` is greater than `m` (the result would be
negative), following the convention of `pack`, which likewise maps 
negative integers to `Zero`.

```coal
sub : nat -> nat -> nat
```

---

### `checked_sub`

Checked subtraction of natural numbers.

Returns `None` when `n` is greater than `m` (there is no natural number 
result), otherwise `Some` of the difference.

```coal
checked_sub : nat -> nat -> Option<nat>
```

---

### `div_mod`

Division with remainder in a single pass.

Returns `None` when the divisor is `Zero`, otherwise `Some` of the
`(quotient, remainder)` pair. Satisfies the law: `Some((q, r))`
implies `n = d * q + r` with `r < d`.

```coal
div_mod : nat -> nat -> Option<(nat, nat)>
```

---

### `checked_div`

Checked division of natural numbers.

Returns `None` when the divisor is `Zero`, otherwise `Some` of the
quotient.

```coal
checked_div : nat -> nat -> Option<nat>
```

---

### `checked_mod`

Checked remainder of natural numbers.

Returns `None` when the divisor is `Zero`, otherwise `Some` of the
remainder.

```coal
checked_mod : nat -> nat -> Option<nat>
```
