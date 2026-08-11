# `Runtime`

---

### `event_loop`

Co-recursive event loop.

Calls `step_fn` repeatedly with the current state. Continues as long
as `step_fn` returns `Some(next_state)`. Stops and returns the current
state when `step_fn` returns `None`.

---

### `blocking_poll`

Blocking poll loop.

Calls `try_fn(state)`. If it returns `Some(result)`, returns `result`.
Otherwise calls `block_fn(state)` to wait for data, then retries
`try_fn` with the same state.
