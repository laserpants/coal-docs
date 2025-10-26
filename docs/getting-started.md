# Getting started

## Installation and setup

The compiler has been tested on Linux and Mac OS.

!!! warning "Important notice"

    The Coal compiler is still a work in progress. 
    There are many important features missing. See the [roadmap](https://codeberg.org/laserpants/coal#roadmap) to keep track of current progress. Also consider [contributing](https://codeberg.org/laserpants/noll/src/branch/develop#how-to-contribute) to the project.

### Prerequisites

#### Haskell/GHC

A recent version of [GHC](https://www.haskell.org/ghc/) is needed. It is **recommended** to install Haskell, GHC and Stack using the [GHCup](https://www.haskell.org/ghcup/) tool.

#### LLVM

An [LLVM](https://llvm.org/) toolchain that provides `llc` (the LLVM static compiler) is also required.

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

**Note:** If you use Homebrew to install LLVM, you may need to add the binaries to your `PATH` manually. 

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
cd coal && stack install
```

Restart or refresh your shell, using e.g., `exec $SHELL -l`. To verify that the executable is installed, run:

```
coal --help
```

### Hello, world!

```
module Main {

  fun main() = trace_string("Hello, world!")

}
```

Save this program as "Main.coal". Compile the program with the command:

```
coal Main.coal -o dist
```
