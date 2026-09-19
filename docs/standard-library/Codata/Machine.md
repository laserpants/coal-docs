# `Codata.Machine`

Mealy machines: stateful processes that consume a sequence of inputs and
produce a sequence of outputs, one at a time.

A machine is parameterised by its input type `i` and output type `o`, and
is built from an internal state together with a transition function of
type `i -> s -> s`, which determines the next state, and a view function
of type `s -> o`, which determines the output.

The state type `s` is hidden (existentially quantified), so machines with
different internal representations share the same `Machine<i, o>` type.
`observe` returns the current output, and `receive` advances the machine
to a new state, which is itself a machine. Machines are the basis of
streams (`Stream<a> = Machine<unit, a>`), parsers and other stateful
processes.

---

### `observe`

Return the current output of a machine.

The output is computed by applying the machine's view function to its
current state. Observing a machine does not advance it.

```coal
observe : Machine<i, o> -> o
```

---

### `receive`

Feed an input into a machine and return the resulting machine.

The machine's step function is applied to the given input and its
current state, giving a machine in a new state.

```coal
receive : i -> Machine<i, o> -> Machine<i, o>
```

---

### `machine`

Construct a machine from an initial state, a transition function and a
view function.

The transition function determines the next state from an input and the
current state, and the view function determines the output from the
current state.

```coal
machine : s -> (i -> s -> s) -> (s -> o) -> Machine<i, o>
```

---

### `map_machine`

Transform the output of a machine using the given function.

The state and transition function are untouched; the function is
applied to the result of the view for each state.

```coal
map_machine : (o -> p) -> Machine<i, o> -> Machine<i, p>
```

---

### `map2_machine`

Combine the outputs of two machines using the given function.

The same input is fed to both machines.

```coal
map2_machine : (o -> p -> q) -> Machine<i, o> -> Machine<i, p> -> Machine<i, q>
```

---

### `map3_machine`

Combine the outputs of three machines using the given function.

The same input is fed to all three machines.

```coal
map3_machine : (o -> p -> q -> r) -> Machine<i, o> -> Machine<i, p> -> Machine<i, q> -> Machine<i, r>
```

---

### `map4_machine`

Combine the outputs of four machines using the given function.

The same input is fed to all four machines.

```coal
map4_machine : (o -> p -> q -> r -> s) -> Machine<i, o> -> Machine<i, p> -> Machine<i, q> -> Machine<i, r> -> Machine<i, s>
```

---

### `contramap_input`

Adapt the inputs of a machine using the given function.

Each input is transformed before it is fed to the machine; the state
and view function are untouched.

```coal
contramap_input : (j -> i) -> Machine<i, o> -> Machine<j, o>
```

---

### `compose`

Compose two machines, feeding the output of the first into the second.

When an input arrives, the first machine is stepped, its new output is
fed as input to the second, and the resulting pair of machines is
returned. The output of the composition is the output of the second
machine.

```coal
compose : Machine<a, b> -> Machine<b, c> -> Machine<a, c>
```

---

### `duplicate`

Return a machine whose output is the machine itself.

Receiving an input steps the inner machine, so that the successive
versions of the machine are observed in turn.

```coal
duplicate : Machine<i, o> -> Machine<i, Machine<i, o>>
```

---

### `zip`

Combine the outputs of two machines into a pair.

Shorthand for `zip2`.

```coal
zip : Machine<i, o1> -> Machine<i, o2> -> Machine<i, (o1, o2)>
```

---

### `zip2`

Combine the outputs of two machines into a pair.

The same input is fed to both machines.

```coal
zip2 : Machine<i, o1> -> Machine<i, o2> -> Machine<i, (o1, o2)>
```

---

### `zip3`

Combine the outputs of three machines into a triple.

The same input is fed to all three machines.

```coal
zip3 : Machine<i, o1> -> Machine<i, o2> -> Machine<i, o3> -> Machine<i, (o1, o2, o3)>
```

---

### `zip4`

Combine the outputs of four machines into a quadruple.

The same input is fed to all four machines.

```coal
zip4 : Machine<i, o1> -> Machine<i, o2> -> Machine<i, o3> -> Machine<i, o4> -> Machine<i, (o1, o2, o3, o4)>
```

---

### `process`

Construct a machine whose state is also its output.

Equivalent to `machine(seed, transition, identity)`.

```coal
process : s -> (i -> s -> s) -> Machine<i, s>
```

---

### `cofix`

Tie the recursive knot, constructing a machine from a function of the
machine itself.

The machine may use its argument to refer to itself; the unfolding is
performed on demand, so recursive definitions need not be finitely
constructed.

```coal
cofix : (Machine<i, o> -> Machine<i, o>) -> Machine<i, o>
```

---

### `run_while`

Repeatedly feed the unit input into a machine while the predicate
holds, and return the output of the resulting machine.

The predicate is checked before each step.

```coal
run_while : (unit -> bool) -> Machine<unit, a> -> a
```
