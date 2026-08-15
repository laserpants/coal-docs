# Packages

## coal-containers

Repository: [codeberg.org/laserpants/coal-containers](https://codeberg.org/laserpants/coal-containers)

A collection of functional data structures for the Coal programming language, providing efficient implementations of common container types.

- **Map** — An AVL tree-based associative map with automatic balancing
- **Set** — A set implementation built on top of Map
- **Tree** — General-purpose tree structure (rose tree) with arbitrary children
- **NonEmpty.List** — Type-safe non-empty list with guaranteed head element

#### Installation

```bash
coal add https://git@codeberg.org/laserpants/coal-containers.git
```

---

## coal-monads

Repository: [codeberg.org/laserpants/coal-monads](https://codeberg.org/laserpants/coal-monads)

A collection of common monad implementations for the Coal programming language.

- **Reader** &ndash; For shared environment access
- **State** &ndash; For stateful computations
- **Writer** &ndash; For computations that produce a log alongside a result

#### Installation

```bash
coal add https://git@codeberg.org/laserpants/coal-monads.git
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

```bash
coal add https://git@codeberg.org/laserpants/coal-json.git
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

#### Installation

```bash
coal add https://git@codeberg.org/laserpants/coal-micro-test.git
```

---

## coal-pretty

Repository: [codeberg.org/laserpants/coal-pretty](https://codeberg.org/laserpants/coal-pretty)

A pretty-printing library for the Coal programming language, providing a `Pretty` trait with instances for common built-in and composite types.

#### Installation

```bash
coal add https://git@codeberg.org/laserpants/coal-pretty.git
```

---

## coal-parsers

Repository: [codeberg.org/laserpants/coal-parsers](https://codeberg.org/laserpants/coal-parsers)

A parser combinator library  with modular, composable parsers for text processing, language implementation, and data format parsing.

#### Installation

```bash
coal add https://git@codeberg.org/laserpants/coal-parsers.git
```

---

## coal-event-source

Repository: [codeberg.org/laserpants/coal-event-source](https://codeberg.org/laserpants/coal-event-source)

An event source library providing composable, blocking event sources with file descriptor and timer-based I/O multiplexing via `select()`.

#### Installation

```bash
coal add https://git@codeberg.org/laserpants/coal-event-source.git
```
