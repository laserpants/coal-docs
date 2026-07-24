# Packages

## coal-containers

Repository: [codeberg.org/laserpants/coal-containers](https://codeberg.org/laserpants/coal-containers)

A collection of functional data structures for the Coal programming language, providing efficient implementations of common container types.

- **Map** — An AVL tree-based associative map with automatic balancing
- **Set** — A set implementation built on top of Map
- **Tree** — General-purpose tree structure (rose tree) with arbitrary children
- **NonEmpty.List** — Type-safe non-empty list with guaranteed head element

#### Installation

Add **coal-containers** as a dependency in your `coal.json` file:

```json
{
  "dependencies": {
    "coal-containers": {
      "version": "*",
      "git": "ssh://git@codeberg.org/laserpants/coal-containers.git"
    }
  }
}
```

---

## coal-monads

Repository: [codeberg.org/laserpants/coal-monads](https://codeberg.org/laserpants/coal-monads)

A collection of common monad implementations for the Coal programming language.

- **Reader** &ndash; For shared environment access
- **State** &ndash; For stateful computations
- **Writer** &ndash; For computations that produce a log alongside a result

#### Installation

Add this repository as a dependency in your project's `coal.json` config-file:

```json
  "dependencies": {
    "coal-monads": {
      "version": "*",
      "git": "ssh://git@codeberg.org/laserpants/coal-monads.git"
    }
  }
```

---

## coal-json

Repository: [codeberg.org/laserpants/coal-json](https://codeberg.org/laserpants/coal-json)

A JSON library for the Coal programming language, providing encoding, decoding, and pretty-printing of JSON values with composable decoder combinators and typeclass-based serialization.

- **JsonValue type** — A sum type representing all JSON primitives and compound values
- **Tokenizer/Parser** — A two-phase parser (lexer + stack machine) with proper error handling
- **Encoder** — Compact JSON encoding from `JsonValue` to string
- **Pretty-printer** — Human-readable JSON output with configurable indentation
- **Decoder combinators** — Composable decoders with combinators like `field`, `array_decoder`, `map`, and `map2`
- **Typeclass support** — `ToJson` and `FromJson` traits for automatic serialization/deserialization

#### Installation

Add **coal-json** as a dependency in your project's `coal.json` config-file:

```json
{
  "dependencies": {
    "coal-json": {
      "version": "*",
      "git": "ssh://git@codeberg.org/laserpants/coal-json.git"
    }
  }
}
```

---

## coal-micro-test

Repository: [codeberg.org/laserpants/coal-micro-test](https://codeberg.org/laserpants/coal-micro-test)

This library provides a simple and elegant way to write and run tests in Coal. It offers a functional approach to testing with assertion functions, test composition, and pretty-printed test results.

- **Simple assertions**: `assert` and `assert_eq` for common test cases
- **Composable tests**: Build complex test suites from simple test cases
- **Clear output**: Color-coded test results with pass/fail summaries
- **Functional design**: Leverages Coal's functional programming features
- **Lightweight**: Minimal dependencies and straightforward API

#### installation

Add `coal-micro-test` to your `coal.json` dependencies:

```json
{
  "name": "your-project",
  "version": "0.1.0",
  "modules": [
    "YourModule"
  ],
  "dependencies": {
    "coal-micro-test": {
      "version": "*",
      "git": "ssh://git@codeberg.org/laserpants/coal-micro-test.git"
    }
  }
}
```

---

## coal-pretty

Repository: [codeberg.org/laserpants/coal-pretty](https://codeberg.org/laserpants/coal-pretty)

A pretty-printing library for the Coal programming language, providing a `Pretty` trait with instances for common built-in and composite types.

#### installation

Add `coal-pretty` as a dependency in your project's `coal.json` config-file:

```json
{
  "dependencies": {
    "coal-pretty": {
      "version": "*",
      "git": "ssh://git@codeberg.org/laserpants/coal-pretty.git"
    }
  }
}
```

#### Usage

Import the `Pretty` trait and call `pretty` on any value with a `Pretty` instance:

```coal
import Pretty(Pretty)

let s = pretty("hello world")
// "hello world"

let n = pretty(42)
// "42"

let xs = pretty([1, 2, 3])
// "[1,2,3]"

let opt = pretty(Some(42))
// "Some(42)"
```
