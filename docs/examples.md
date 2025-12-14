# Examples

## Quicksort

#### Tree.coal

```
module Tree {

  type Tree<a>
    = Node(a, Tree<a>, Tree<a>)
    | Leaf

  fun flatten(tree) = 
    fold(tree) {
      | Node(y, @lhs, @rhs) =>
          lhs ++ y :: rhs
      | Leaf =>
          []
    }

}
```

#### Qsort.coal

```
module Qsort(sort) {

  import Tree(type Tree, flatten)
  import Coal.Combinators(always)
  import Number(_INT32_MAX)

  fun binary_search_tree(list : List<int32>) : Tree<int32> =
    fold(list, { min = 0, max = _INT32_MAX }) {
      | (p :: @g) =>
          fn(range) =>
            if (p > range.min && p <= range.max)
              then 
                Node
                  ( p 
                  , g({ min = range.min, max = p })
                  , g({ min = p, max = range.max })
                  )
              else
                g(range)
      | [] =>
          always(Leaf)
    }

  let sort = flatten << binary_search_tree

}
```

#### Main.coal

```
module Main {

  import Qsort(sort)
  import Coal.Monad(trait Monad, and_eval)
  import IO(return)

  import namespace IO

  fun print_all(ints : List<int32>) : IO<unit> =
    fold(ints) {
      | [] => 
          return()
      | m :: @next =>
          IO.println_int32(m) |. and_eval(next)
    }

  fun main() = 
    let xs = [105, 103, 234, 109, 107, 55, 102, 999, 101, 8, 106, 104]
    in
    print_all(sort(xs))

}
```

## Basic I/O

This program demonstrates how to combine parsing and monadic pipelining to build a small interactive console application.
Using `IO` operations composed through monadic combinators, the program asks the user for their name and then runs a simple number-guessing game

```
module Main {

  import Char(digit_to_int32)
  import Coal.Functor(trait Functor(map))
  import Coal.Monad(trait Monad, and_then)
  import IO(readln, println_string, random, return)
  import List(is_empty)
  import Number(double_to_int32)
  import String(to_list, remove_whitespace, int32_to_string)

  fun digits_to_unsigned(chars) : Option<int32> =
    if (is_empty(chars)) 
      then
        None
      else
        fold(chars, Some(0)) {
          | ch :: @go =>
              fn(t) =>
                match(digit_to_int32(ch)) {
                  | Some(n) =>
                      go(map(fn(s) => n + 10 * s, t))
                  | None =>
                      None
                }
          | [] =>
              fn(t) => t
        }

  fun parse_int32(str : string) : Option<int32> =
    digits_to_unsigned(to_list(remove_whitespace(str)))

  fun random_int32() : IO<int32> =
    random()
      |. and_then(fn(n) => return(double_to_int32(n * 10)))

  fun main() = 
    println_string("Enter your name")
      |. and_then(readln)
      |. and_then(fn(s) => println_string("Hello, " <> s <> "!"))
      |. and_then(random_int32)
      |. and_then(fn(rand) => 
           println_string("Guess what number I am thinking of")
             |. and_then(readln)
             |. and_then(fn(s) => 
                  match(parse_int32(s)) {
                    | Some(n) =>
                        if (n == rand) 
                          then println_string("You guessed right!")
                          else println_string("Sorry, the number I was thinking of was " <> int32_to_string(rand) <> ".")
                    | None =>
                        println_string("Not a number")
                  }
                )
         )

}
```

### Do-notation

Using `do`-notation, we can refactor `main` in the above program, so that it
instead becomes:

```
  fun main() = do {
    println_string("Enter your name");
    name <- readln();
    println_string("Hello, " <> name <> "!");

    rand <- random_int32();
    println_string("Guess what number I am thinking of");
    guess <- readln();

    println_string(
      match(parse_int32(guess)) {
        | Some(n) =>
            if (n == rand) 
              then "You guessed right!"
              else "Sorry, the number I was thinking of was " <> int32_to_string(rand) <> "."
        | None =>
            "Not a number"
      });
  }
```

<!--
## JSON

TODO
-->

## Monads

These examples reimplement Haskell’s Reader, Writer, and State monads.

### Reader

```
module Main {

  import namespace IO
  import Coal.Monad(trait Monad, and_then)
  import Coal.Functor(trait Functor)
  import Coal.Applicative(trait Applicative)

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
    fun bind(reader : Reader<r, a>, next : a -> Reader<r, b>) : Reader<r, b> = 
      match(reader) {
        | Reader(f) =>
            Reader(fn(env) =>
              let a = 
                f(env) 
              in
              match(next(a)) {
                | Reader(g) => g(env)
              }
            )
      }
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

```
module Main {

  import namespace IO
  import namespace List
  import Coal.Monad(trait Monad, and_then, and_eval)
  import Coal.Functor(trait Functor)
  import Coal.Applicative(trait Applicative)
  import Coal.Monoid(trait Monoid)
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

```
module Main {

  import namespace IO
  import Coal.Functor(trait Functor)
  import Coal.Monad(trait Monad, and_then)
  import Coal.Applicative(trait Applicative)
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
    | "password123" = put(true)
    | _             = put(false)

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
