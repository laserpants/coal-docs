# Quicksort

#### Tree.coal

```coal
module Tree(Tree, insert, from_list, flatten) {

  import List(reduce)

  type Tree<a>
    = Leaf
    | Node(a, Tree<a>, Tree<a>)

  fun insert(n : a, tree : Tree<a>) : Tree<a> with (Ordered<a>) =
    fold(tree) {
      | Leaf => 
          Node(n, Leaf, Leaf)
      | Node(v, @left as left_tree, @right as right_tree) 
          when (n < v) => 
            Node(v, left, right_tree)
          when (n > v) => 
            Node(v, left_tree, right)
          otherwise => 
            Node(v, left_tree, right_tree)
    }

  fun from_list(xs : List<a>) : Tree<a> with (Ordered<a>) =
    reduce(insert, Leaf, xs)

  fun flatten(tree : Tree<a>) : List<a> =
    fold(tree, []) {
      | Leaf => 
          fn(acc) => acc
      | Node(v, @left, @right) =>
          fn(acc) =>
            left(v :: right(acc))
    }

}
```

#### Qsort.coal

```coal
module Qsort(sort) {

  import Tree(flatten, from_list)

  let sort : List<a> -> List<a> with (Ordered<a>) =
    flatten << from_list

}
```

#### Main.coal

```coal
module Main {

  import Qsort(sort)
  import IO(return)
  import Coal.Monad(and_eval)
  
  import namespace IO

  fun print_all(ints : List<int32>) : IO<unit> =
    fold(ints) {
      | [] =>
          return()
      | m :: @next =>
          IO.println_int32(m) |. and_eval(next)
    }

  fun main() = 
    let sorted = sort([ 4, 34, 8, 99, 5, 102, 42, 7, 2, 1, 103, 3, 6 ]) 
    in 
    print_all(sorted) 

}
```

## Basic I/O

This program demonstrates how to combine parsing and monadic pipelining to build a small interactive console application.
Using `IO` operations composed through monadic combinators, the program asks the user for their name and then runs a simple number-guessing game

```coal
module Main {

  import Char(digit_to_int32)
  import Coal.Functor(Functor(map))
  import Coal.Monad(Monad, and_then)
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

```coal
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
