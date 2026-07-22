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
