# `Runtime`

---

### `event_loop`

Co-recursive event loop.

Calls `step_fn` repeatedly with the current state. Continues as long
as `step_fn` returns `Some(next_state)`. Stops and returns the current
state when `step_fn` returns `None`.

---

### `event_loop_io`

Co-recursive event loop with IO effects.

Calls `step_fn` repeatedly with the current state, where `step_fn`
returns an `IO` action producing `Option<next_state>`. Continues as
long as the action yields `Some(next_state)`. Stops and returns the
current state (wrapped in `IO`) when it yields `None`.

---

### `blocking_poll`

Blocking poll loop.

Calls `try_fn(state)`. If it returns `Some(result)`, returns `result`.
Otherwise calls `block_fn(state)` to wait for data, then retries
`try_fn` with the same state.
