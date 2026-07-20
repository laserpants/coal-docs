# Coal

<img alt="Coal" src="assets/mine.jpg" />

<a href="https://codeberg.org/laserpants/coal"><img src="https://badgen.net/codeberg/stars/laserpants/coal" /></a>

This is the official documentation for the Coal programming language. 

## About

Coal is a declarative, statically typed, purely functional programming language with simple and intuitive syntax. It provides:

- algebraic data types and pattern matching, 
- extensible records, 
- structural recursion, 
- codata, and
- traits (type classes)

among other features. Coal’s type system, like Haskell’s and ML’s, supports type inference and parametric polymorphism, drawing on the [System-F](https://en.wikipedia.org/wiki/System_F) lambda calculus. The Coal compiler is implemented in Haskell and targets [LLVM](https://llvm.org/) for code generation. 

As a [total](https://en.wikipedia.org/wiki/Total_functional_programming) language, Coal takes a different approach to recursion, following the motto that "[recursion is the `goto` of functional programming](https://www.semanticscholar.org/paper/Functional-Programming-with-Bananas%2C-Lenses%2C-and-Meijer-Fokkinga/5db3c6793c07285bf0f5e95fe5a25f53e7488051)." To guarantee that programs are provably terminating, recursion is only available in a restricted form, known as *structural recursion*. 

```coal
fun sum(numbers : List<int32>) : int32 =
  fold(numbers) {
    | [] => 0
    | x :: @tot => x + tot
  }
```

The language finds inspiration in ideas from the field of Mathematics of Program Construction, where streams and other infinite data types are described as [coalgebras](https://coal-lang.org/data-and-codata/) — hence the name *Coal*. 

This project is licensed under the terms of the MIT license. The source code is hosted at [codeberg.org/laserpants/coal](https://codeberg.org/laserpants/coal).
