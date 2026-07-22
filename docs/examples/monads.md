# Monads

These examples reimplement Haskell’s Reader, Writer, and State monads.

### Reader

```coal
module Main {

  import namespace IO
  import Coal.Monad(Monad, and_then)
  import Coal.Functor(Functor)
  import Coal.Applicative(Applicative)

  type Reader<r, a> = Reader(r -> a)

  fun run_reader(reader, env) =
    match(reader) {
      | Reader(f) => f(env)
    }

  fun ask() = 
    Reader(fn(env) => env)

  instance Functor<Reader<r>> {
    fun map(f, Reader(g)) =
      Reader(fn(r) => f(g(r)))
  }

  instance Applicative<Reader<r>> {
    fun pure(r) = 
      Reader(fn(_) => r)

    fun ap(Reader(f), Reader(g)) =
      Reader(fn(r) =>
        let func = f(r) in
        let a    = g(r) in
        func(a)
      )
  }

  instance Monad<Reader<r>> {
    fun bind(Reader(f) : Reader<r, a>, next : a -> Reader<r, b>) : Reader<r, b> = 
      Reader(fn(env) =>
        let a = 
          f(env) 
        in
        match(next(a)) {
          | Reader(g) => g(env)
        }
      )
  }

  fun local(transform, Reader(f)) = 
    Reader(fn(env) => f(transform(env)))

  // Example use:

  fun test_reader(val : int32) : Reader<int32, int32> =
    ask()
      |. and_then(fn(r) => pure(val + r))

  fun main() =
    IO.println_int32(run_reader(test_reader(5), 5))

}
```

### Writer

```coal
module Main {

  import namespace IO
  import namespace List
  import Coal.Monad(Monad, and_then, and_eval)
  import Coal.Functor(Functor)
  import Coal.Applicative(Applicative)
  import Coal.Monoid(Monoid)
  import IO(return)

  type Writer<w, a> = Writer(a, w)

  fun run_writer(writer) =
    match(writer) {
      | Writer(a, w) => (a, w)
    }

  instance Functor<Writer<w>> {
    fun map(f, Writer(a, w)) =
      Writer(f(a), w)
  }

  instance Applicative<Writer<w>> {
    fun pure(w) = 
      Writer(w, id)

    fun ap(Writer(f, w1), Writer(a, w2)) =
      Writer(f(a), w1 <> w2)
  }

  instance Monad<Writer<w>> {
    fun bind(writer, k) : Writer<w, b> =
      match(writer) {
        | Writer(a, w1) =>
            match(k(a)) {
              | Writer(b, w2) => 
                  Writer(b, w1 <> w2)
            }
      }
  }

  fun tell(w) : Writer<w, unit> =
    Writer((), w)

  fun listen(m) : Writer<w,(a, w)> =
    match(m) {
      | Writer(a, w) => Writer((a, w), w)
    }

  // Example use:

  fun test_writer() : Writer<List<string>, int32> =
    tell(["one"])
      |. and_eval(tell(["two"]))
      |. and_eval(tell(["three"]))
      |. and_eval(pure(100))

  fun print_msgs(msgs : List<string>) =
    fold(msgs) {
      | [] => 
          return()
      | m :: @next =>
          IO.println_string(m) |. and_eval(next)
    }

  fun main() =
    match(run_writer(test_writer())) {
      | ((_, w)) => print_msgs(w)
    }

}
```

### State

```coal
module Main {

  import namespace IO
  import Coal.Functor(Functor)
  import Coal.Monad(Monad, and_then)
  import Coal.Applicative(Applicative)
  import Coal.Combinators(fst)

  type State<s, a> = State(s -> (a, s))

  fun run_state(State(f), s) = 
    f(s)

  fun eval_state(st, s0) =
    fst(run_state(st, s0))

  instance Functor<State<s>> {
    fun map(f, State(g)) =
      State(fn(s) =>
        let (a, s1) = g(s) 
        in
        (f(a), s1)
      )
  }

  instance Applicative<State<s>> {
    fun pure(x) =
      State(fn(s) => (x, s))

    fun ap(State(sf), State(sa)) =
      State(fn(s0) =>
        let (f, s1) = sf(s0) in
        let (a, s2) = sa(s1) in
        (f(a), s2)
      )
  }

  instance Monad<State<s>> {
    fun bind(m, k) =
      State(fn(s0) =>
        let (a, s1) = run_state(m, s0) 
        in
        run_state(k(a), s1)
      )
  }

  fun get() = 
    State(fn(s) => (s, s))

  fun put(s) = 
    State(fn(_) => ((), s))

  fun modify(f) = 
    State(fn(s) => ((), f(s)))

  // Example use:

  fun authenticate
    | "password123" => put(true)
    | _             => put(false)

   fun msg(success : bool) =
     if (success) then "Logged in" else "Authentication failed"

  fun state_example(pw : string) =
    get()
      |. and_then(fn(logged_in) => 
           if (logged_in) 
             then pure("Already logged in")
             else 
               authenticate(pw) 
                 |. and_then(get) 
                 |. and_then(pure << msg)
      )

  fun main() =
    IO.println_string(eval_state(state_example("abc123"), false))

}
```
