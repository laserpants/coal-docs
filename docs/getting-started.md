# Getting started

## Installation and setup

The compiler currently supports Linux and Mac OS. Windows support is not yet available.

### Prerequisites

#### Haskell/GHC

A recent version of [GHC](https://www.haskell.org/ghc/) is needed. It is **recommended** to install Haskell, GHC and Stack using the [GHCup](https://www.haskell.org/ghcup/) tool.

#### LLVM

An [LLVM](https://llvm.org/) toolchain that provides `llvm-as` and `llc` (the LLVM static compiler) is also required.

##### Linux

- Debian/Ubuntu (or derivatives):

  ```
  sudo apt update
  sudo apt install llvm clang     
  ```

- Fedora, RHEL, or CentOS:

  ```
  sudo dnf install llvm clang
  ```

- Arch Linux:

  ```
  sudo pacman -S llvm
  ```

##### Mac OS

See [Getting Started with the LLVM System](https://llvm.org/docs/GettingStarted.html), or install using Homebrew:

```
brew install llvm
```

!!! note 

    If you use Homebrew to install LLVM, you may need to add the binaries to your `PATH` manually. 

#### Additional dependencies

- GCC (probably not needed on Mac)
- [Boehm–Demers–Weiser garbage collector](https://github.com/ivmai/bdwgc)
- [The GNU Multiple Precision Arithmetic Library](https://gmplib.org/)

##### Linux

- Debian/Ubuntu (or derivatives):

  ```
  sudo apt update
  sudo apt install libgc-dev libgmp-dev build-essential
  ```

- Fedora, RHEL, or CentOS:

  ```
  sudo dnf install gc-devel gmp-devel gcc make
  ```

- Arch Linux:

  ```
  sudo pacman -S gc gmp base-devel
  ```

##### Mac OS

```
brew install bdw-gc gmp
```

## Building the compiler

Clone the repository:

```
git clone ssh://git@codeberg.org/laserpants/coal.git
```

```
cd coal && chmod +x project && ./project install
```

Restart or refresh your shell, using e.g., `exec $SHELL -l`. To verify that the executable is installed, run:

```
coal --version
```

### Hello, world!

```coal
module Main {

  import IO(println_string)

  fun main() =
    println_string("Hello, world!")

}
```

Save this program as "Main.coal". Compile the program with the command:

```
coal compile -I. Main.coal -o dist
```

## Docker-based workflow

This section explains how to use Docker to compile and run Coal programs without needing to install Haskell, LLVM, or other dependencies locally.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed and running on your machine
- A terminal with Docker access

### Available Docker images

Coal provides two official Docker images:

---

#### `ghcr.io/laserpants/coal:latest`

The **recommended image for most users**. This image includes the complete Coal compiler toolchain with the `coal` binary pre-installed and ready to use. It's based on `coal-dev` and includes:

- The Coal compiler (`coal` CLI command)
- All runtime dependencies (LLVM, GHC, Stack, GMP, Boehm GC)
- Ubuntu 24.04 base system

Use this image if you want to **compile and run Coal programs** without building the compiler yourself.

---

#### `ghcr.io/laserpants/coal-dev:latest`

The **development image for contributors**. This image includes only the build toolchain needed to compile Coal from source:

- Haskell toolchain (GHC 9.4.8, Stack)
- LLVM / Clang
- GCC / build-essential
- GMP and Boehm GC development libraries
- Node.js 22 LTS
- Ubuntu 24.04 base system

Use this image if you want to **contribute to the Coal project** or experiment with the compiler source code. You'll need to build the compiler yourself using the `coal-install` script from inside the container.

### Quick start

#### Using the pre-built compiler image

The fastest way to compile Coal programs is using the `coal:latest` image:

Navigate to your Coal project directory and run:

```bash
docker run --rm \
  -v "$PWD:/src" \
  -w /src \
  ghcr.io/laserpants/coal:latest \
  compile -I. Main.coal -o dist
```

#### Interactive use

For an interactive development workflow:

```bash
docker run --rm \
  -it \
  -v "$PWD:/src" \
  -w /src \
  --entrypoint bash \
  ghcr.io/laserpants/coal:latest
```

#### Command explanation

| Flag | Purpose |
|------|---------|
| `--rm` | Automatically remove the container when you exit |
| `-it` | Run interactively with a TTY (gives you a shell prompt) |
| `-v "$PWD:/src"` | Mount your current directory to `/src` in the container |
| `-w /src` | Set the working directory inside the container |
| `--entrypoint bash` | Start a bash shell (instead of the default `coal` command) |

!!! warning "Important!"

    The `-v "$pwd:/src"` flag makes your local files accessible inside the container. any changes you make inside `/src` are immediately reflected in your local directory.

Once inside the container, the `coal` command is ready to use:

```bash
# Compile your program
coal compile -I. Main.coal -o dist

# Run it
./dist

# Show the help text
coal --help
```

## Editor support

### Visual Studio Code

The [Coal VS Code extension](https://codeberg.org/laserpants/vscode-coal) provides TextMate-based syntax highlighting, code snippets and a basic language configuration for files with the `.coal` extension.

#### Features

- **Syntax highlighting** for all Coal language constructs, including keywords, pattern matching with guards (`when`, `otherwise`) and as-patterns, do-notation with bind syntax (`<-`), lambda expressions (`fn`), FFI calls, record literals and extensions, type annotations and arrows, all operators, documentation comments, and built-in types and constructors.
- **Code snippets** for common patterns such as function, module, import, type, trait and instance definitions, pattern matching, lambda expressions, let expressions, fold expressions and do-notation blocks.
- **Language configuration** for auto-closing pairs, comment toggling, code folding and indentation rules.

#### Installation

The extension is distributed as source and must be packaged into a `.vsix` file before it can be installed. This requires Node.js and npm.

Clone the repository and build the extension:

```
git clone https://codeberg.org/laserpants/vscode-coal.git
cd vscode-coal
npm install --no-audit --no-fund
npm run package
```

This produces a file such as `coal-0.2.0.vsix`. Install it into VS Code using the `code` CLI:

```
code --install-extension ./coal-0.2.0.vsix --force
code --list-extensions | grep -i coal
```

Alternatively, you can install the `.vsix` file from the Extensions view in VS Code via **"Install from VSIX..."** (the `...` menu).

!!! note

    Packaging uses [`vsce`](https://github.com/microsoft/vscode-vsce), which is provided in the project devDependencies and installed by `npm install`. If Node.js is not available in your environment, you can install a local Node LTS with [`nvm`](https://github.com/nvm-sh/nvm).

