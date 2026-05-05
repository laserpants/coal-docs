# CLI reference

The Coal CLI is the primary tool for compiling Coal programs and managing Coal projects. It provides commands for:

- **Compiling** individual Coal source files into executables
- **Building** projects defined by `coal.json` manifests
- **Managing dependencies** from Git repositories
- **Cleaning** build artifacts

The CLI is invoked using the `coal` command, followed by a subcommand and options.

## Quick start

Here's a minimal example to compile and run a Coal program:

```bash
# Create a simple Coal program
cat > Main.coal << 'EOF'
module Main {
  import IO(println_string)
  fun main() = println_string("Hello, Coal!")
}
EOF

# Compile the program
coal compile -I. Main.coal -o hello

# Run the executable
./hello
```

For project-based development with dependencies:

```bash
# Create a project manifest
cat > coal.json << 'EOF'
{
  "name": "my-project",
  "version": "0.1.0",
  "modules": ["Main"]
}
EOF

# Install dependencies (if any)
coal install

# Build the project
coal build
```

## Commands

### coal compile

Compiles Coal source files into an executable binary.

#### Usage

```bash
coal compile [OPTIONS] FILES...
```

#### Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--output FILE` | `-o` | Required | Output executable file name/path |
| `--path FILE` | `-I` | Multiple | Source directory path (can be specified multiple times) |
| `--extra-c FILE` | | Multiple | Extra C source file to link (can be specified multiple times) |
| `--generate-debug-artifacts` | | Flag | Generate build info and Graphviz DOT files |
| `--debug-llvm-ir` | | Flag | Output intermediate LLVM IR |
| `--silent` | `-s` | Flag | Suppress terminal output |
| `--no-cache` | | Flag | Disable caching |

#### Behavior

- Compiles the specified input files into a native executable
- Automatically includes `src` directory in source paths (in addition to any paths specified with `-I`)
- Links with the Coal runtime C code automatically
- Generates LLVM IR and compiles to native code
- Extra C files (specified with `--extra-c`) are compiled and linked into the final executable

#### Examples

**Basic compilation:**

```bash
coal compile -I. Main.coal -o myprogram
```

**Compile with multiple source paths:**

```bash
coal compile -I./src -I./lib Main.coal -o myprogram
```

**Compile with debug artifacts:**

```bash
coal compile -I. Main.coal -o dist --generate-debug-artifacts --debug-llvm-ir
```

This generates additional debugging files including:

- [Graphviz](https://graphviz.org/) DOT files for visualizing the compilation process
- Build information files
- LLVM IR output

**Compile with extra C files:**

```bash
coal compile -I. Main.coal --extra-c helpers.c --extra-c utils.c -o myapp
```

**Silent compilation without cache:**

```bash
coal compile -s --no-cache -I. Main.coal -o dist
```

### coal build

Builds a Coal project using configuration from a `coal.json` manifest file.

#### Usage

```bash
coal build
```

#### Options

None. All configuration is read from `coal.json` in the current directory.

#### Behavior

1. Reads project configuration from `coal.json` in the current directory
2. Requires `coal.lock.json` to be present (run `coal install` first if missing)
3. Loads all dependency manifests from `.coal/packages/`
4. Combines local source paths with dependency source paths
5. Compiles all modules listed in the manifest
6. Outputs an executable using the project name and version from the manifest

#### Error handling

The command will fail if:

- `coal.json` is missing or invalid
- `coal.lock.json` is missing (run `coal install` first)
- Any dependency manifests are missing from `.coal/packages/`
- Module names in the manifest are invalid

#### Example

```bash
# After setting up coal.json and running coal install
coal build
```

See [Creating a new project](#creating-a-new-project) for a complete workflow example.

### coal install

Installs packages specified in `coal.json` and generates/updates `coal.lock.json`.

#### Usage

```bash
coal install
```

#### Options

None. Dependencies are read from `coal.json` in the current directory.

#### Behavior

1. Reads dependencies from `coal.json`
2. For each dependency:
   - Lists available Git tags/versions from the remote repository
   - Selects the version matching the constraint (or latest if constraint is `*`)
   - Clones the repository to `.coal/packages/<name>/<commit-hash>/`
   - Checks out the specific commit corresponding to the selected version
   - Recursively installs transitive dependencies
3. Generates or updates `coal.lock.json` with exact versions and commit hashes
4. Uses depth-first traversal with cycle detection

#### Package storage

Packages are stored at: `.coal/packages/<package-name>/<commit-hash>/`

For example:
```
.coal/packages/hello-world/05c8b6e2c7b1ad49db83a9d035e131163482606c/
```

#### Version resolution

- Uses semantic versioning (SemVer) for version constraints
- Supports wildcard constraint `*` (picks latest version)
- Supports specific version constraints (e.g., `"1.2.3"`, `"^1.0.0"`, `"~2.1.0"`)
- Tags in Git repositories must follow SemVer format (e.g., `v1.0.0`, `v2.3.1`)

#### Error handling

The command will fail if:

- `coal.json` is missing or invalid
- No version matches the constraint
- Git operations fail (clone, ls-remote, checkout)

#### Example

```bash
coal install
```

See [Adding dependencies](#adding-dependencies) for a complete workflow example.

### coal clean

Removes the `.build` directory containing build artifacts.

#### Usage

```bash
coal clean
```

#### Options

None.

#### Behavior

- Recursively deletes the `.build/` directory
- Silently succeeds if the directory doesn't exist
- Does **not** remove the dependency cache (`.coal/packages/`)

To remove dependencies, manually delete the `.coal/` directory:

```bash
rm -rf .coal
```

#### Example

```bash
coal clean
```

### coal --version

Displays the Coal compiler version.

#### Usage

```bash
coal --version
coal -V
```

#### Output

The version is derived from Git tags. Examples:

- `v0.1.0` (release version)
- `v0.1.0-3-g1234abc` (3 commits after v0.1.0)
- `v1.2.3-dirty` (uncommitted changes)

#### Example

```bash
$ coal --version
v0.1.0-5-g9a8b7c6
```

## Configuration files

### coal.json

The project manifest file defines package metadata, modules, dependencies, and build configuration.

#### Schema

```json
{
  "name": "<package-name>",
  "version": "<semver-version>",
  "modules": ["<module-path>", ...],
  "source_dirs": ["<path>", ...],
  "dependencies": {
    "<package-name>": {
      "version": "<version-constraint>",
      "git": "<git-repo-url>"
    }
  }
}
```

#### Field descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | `String` | Yes | Package name (used as identifier in dependency resolution) |
| `version` | `String` | No | Package version in SemVer format (e.g., `"0.1.0"`, `"1.2.3"`) |
| `modules` | `Array[String]` | Yes | List of module paths to compile |
| `source_dirs` | `Array[String]` | No | Source directories to search (defaults to `["src"]`) |
| `dependencies` | `Object` | No | Map of package dependencies |

#### Module paths

Module paths use Coal's module naming conventions:

- Simple modules: `"Main"`, `"Utils"`
- Nested modules: `"Foo.Bar"`, `"Data.Types.User"`

These are converted to file paths by the module system:

- `"Main"` → `Main.coal`
- `"Foo.Bar"` → `Foo/Bar.coal`
- `"Data.Types.User"` → `Data/Types/User.coal`

#### Source directories

- Paths are relative to the manifest file location
- Default is `["src"]` if not specified
- The `"src"` directory is always included automatically by `coal build`

#### Dependency format

Each dependency entry has the following structure:

```json
{
  "version": "<version-constraint>",
  "git": "<git-repo-url>"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | String | No | SemVer constraint. If omitted or `"*"`, picks latest version |
| `git` | String | Yes | Git repository URL (supports SSH, HTTPS, etc.) |

#### Version constraint examples

- `"*"` — Any version (picks latest)
- `"1.2.3"` — Exact version 1.2.3
- `"^1.2.0"` — Compatible with 1.2.0 (SemVer caret range)
- `"~1.2.3"` — Approximately 1.2.3 (SemVer tilde range)

#### Examples

**Minimal manifest:**

```json
{
  "name": "my-app",
  "version": "0.1.0",
  "modules": ["Main"]
}
```

**With dependencies:**

```json
{
  "name": "my-package",
  "version": "0.1.0",
  "modules": ["Main"],
  "source_dirs": ["./src"],
  "dependencies": {
    "hello-world": {
      "version": "*",
      "git": "ssh://git@codeberg.org/laserpants/coal-hello-world.git"
    }
  }
}
```

**Multiple modules and source directories:**

```json
{
  "name": "complex-project",
  "version": "1.2.3",
  "modules": [
    "Main",
    "Utils.Helpers",
    "Data.Types"
  ],
  "source_dirs": [
    "./src",
    "./lib"
  ],
  "dependencies": {
    "core-lib": {
      "version": "^2.0.0",
      "git": "https://github.com/example/coal-core.git"
    },
    "utils": {
      "version": "~1.5.0",
      "git": "ssh://git@codeberg.org/example/coal-utils.git"
    }
  }
}
```

### coal.lock.json

The lock file records exact versions and commit hashes of all installed dependencies, ensuring reproducible builds.

#### Schema

```json
{
  "packages": {
    "<package-name>": {
      "version": "<semver-version>",
      "source": "<git-repo-url>",
      "commit": "<git-commit-hash>"
    }
  }
}
```

#### Field descriptions

| Field | Type | Description |
|-------|------|-------------|
| `packages` | Object | Map of package name to lock specification |

**Lock specification (per package):**

| Field | Type | Description |
|-------|------|-------------|
| `version` | String | Exact SemVer version installed |
| `source` | String | Git repository URL |
| `commit` | String | Full Git commit SHA-1 hash |

#### Example

```json
{
  "packages": {
    "hello-world": {
      "commit": "05c8b6e2c7b1ad49db83a9d035e131163482606c",
      "source": "ssh://git@codeberg.org/laserpants/coal-hello-world.git",
      "version": "0.1.0"
    },
    "core-lib": {
      "commit": "a1b2c3d4e5f6789012345678901234567890abcd",
      "source": "https://github.com/example/coal-core.git",
      "version": "2.1.4"
    }
  }
}
```

#### Behavior

**Generation:**

- Created/updated by `coal install` command
- Includes all direct and transitive dependencies
- Pins exact commit hashes for reproducibility

**Usage:**

- Required by `coal build` command
- Ensures deterministic builds across different environments
- Should be committed to version control

**Updating:**

- Re-run `coal install` to update dependencies
- The lock file is completely regenerated (not incrementally updated)

## Dependency management

### Git-based dependencies

Coal uses Git repositories as the primary source for dependencies. This enables decentralized package distribution without requiring a central package registry.

#### Supported Git URLs

Coal supports any Git URL format recognized by your system's Git client:

- **SSH:** `ssh://git@codeberg.org/user/repo.git`
- **HTTPS:** `https://github.com/user/repo.git`
- **Git protocol:** `git://example.com/repo.git`

#### Version gagging requirements

For a Git repository to work as a Coal dependency, it must:

1. Tag releases using SemVer-formatted tags
2. Use the format: `v<major>.<minor>.<patch>`

Examples of valid tags:

- `v1.0.0`
- `v0.1.0`
- `v2.3.1`

The CLI uses `git ls-remote --tags` to list available versions from the remote repository.

### Version constraints

Coal supports semantic versioning (SemVer) constraints for specifying dependency versions.

#### Constraint formats

| Constraint | Meaning | Example Match |
|------------|---------|---------------|
| `"*"` | Any version (latest) | `1.0.0`, `2.5.3`, `10.0.0` |
| `"1.2.3"` | Exact version | `1.2.3` only |
| `"^1.2.0"` | Compatible with 1.2.0 (caret) | `1.2.0`, `1.2.1`, `1.9.9` (not `2.0.0`) |
| `"~1.2.3"` | Approximately 1.2.3 (tilde) | `1.2.3`, `1.2.4` (not `1.3.0`) |

#### Wildcard (`*`)

The wildcard constraint selects the latest available version:

```json
{
  "dependencies": {
    "some-package": {
      "version": "*",
      "git": "https://github.com/example/some-package.git"
    }
  }
}
```

#### Caret (`^`)

The caret constraint allows changes that do not modify the left-most non-zero digit:

- `^1.2.3` matches `>=1.2.3` and `<2.0.0`
- `^0.2.3` matches `>=0.2.3` and `<0.3.0`
- `^0.0.3` matches `>=0.0.3` and `<0.0.4`

#### Tilde (`~`)

The tilde constraint allows patch-level changes:

- `~1.2.3` matches `>=1.2.3` and `<1.3.0`
- `~1.2` matches `>=1.2.0` and `<1.3.0`

### Resolution algorithm

When you run `coal install`, the CLI performs dependency resolution using the following algorithm:

1. **Parse Constraints:** Read version constraints from `coal.json`
2. **Fetch Versions:** For each dependency, list available tags from the Git remote using `git ls-remote --tags`
3. **Select Version:** Pick the highest version satisfying the constraint
4. **Clone & Checkout:** Clone the repository and checkout the commit for the selected tag
5. **Recursive Install:** Parse the dependency's `coal.json` and repeat the process for transitive dependencies
6. **Cycle Detection:** Track visited (package, commit) pairs to avoid infinite loops
7. **Generate Lock:** Write all installed packages to `coal.lock.json`

#### Transitive dependencies

If package A depends on package B, and package B depends on package C, all three packages are installed and recorded in the lock file.

#### Conflict resolution

Currently, Coal uses a simple depth-first approach. If multiple versions of the same package are required by different dependencies, the first version encountered is used. Future versions may implement more sophisticated conflict resolution.

### Package storage

Installed packages are stored in the `.coal/packages/` directory with the following structure:

```
.coal/
└── packages/
    └── <package-name>/
        └── <commit-hash>/
            ├── coal.json
            ├── src/
            │   └── (source files)
            └── (other package files)
```

#### Example

For a package named `hello-world` at commit `05c8b6e2...`:

```
.coal/packages/hello-world/05c8b6e2c7b1ad49db83a9d035e131163482606c/
├── coal.json
├── src/
│   └── Main.coal
└── README.md
```

#### Source path resolution

When building with dependencies, the compiler searches for modules in:

1. Local source paths from your project's `coal.json` `source_dirs` field
2. Dependency source paths: `<package-base>/<source-dir>` for each dependency
3. Standard library paths (built-in)

The `src` directory is always included by default.

## Workflows and tutorials

### Creating a new project

This tutorial walks through creating a new Coal project from scratch.

#### Step 1: Create project directory

```bash
mkdir my-project
cd my-project
```

#### Step 2: Create coal.json

Create a manifest file with your project metadata:

```bash
cat > coal.json << 'EOF'
{
  "name": "my-project",
  "version": "0.1.0",
  "modules": ["Main"]
}
EOF
```

#### Step 3: Create source directory and Main module

```bash
mkdir -p src
cat > src/Main.coal << 'EOF'
module Main {
  import IO(println_string)
  
  fun main() = println_string("Hello, Coal!")
}
EOF
```

#### Step 4: Install dependencies

Even if you have no dependencies, run `coal install` to generate the lock file:

```bash
coal install
```

This creates an empty `coal.lock.json`:

```json
{
  "packages": {}
}
```

#### Step 5: Build

```bash
coal build
```

This compiles your project and generates an executable (the name depends on your project name and version).

#### Step 6: Run

```bash
./my-project-0.1.0  # Or whatever executable name was generated
```

Output:
```
Hello, Coal!
```

### Adding dependencies

This tutorial shows how to add and use a Git-based dependency.

#### Step 1: Update coal.json

Add a dependency to your `coal.json`:

```json
{
  "name": "my-project",
  "version": "0.1.0",
  "modules": ["Main"],
  "dependencies": {
    "hello-world": {
      "version": "*",
      "git": "ssh://git@codeberg.org/laserpants/coal-hello-world.git"
    }
  }
}
```

#### Step 2: Install the dependency

```bash
coal install
```

This will:

1. Clone the `hello-world` repository
2. Select the latest version
3. Store it in `.coal/packages/hello-world/<commit>/`
4. Update `coal.lock.json` with the exact version and commit

#### Step 3: Use the dependency

Update your `src/Main.coal` to import from the dependency:

```coal
module Main {
  import HelloWorld(greet)
  
  fun main() = greet()
}
```

(Note: The actual modules and functions available depend on the dependency's implementation.)

#### Step 4: Rebuild

```bash
coal build
```

The compiler will now include modules from the `hello-world` dependency.

### Multi-module projects

This tutorial demonstrates organizing a project with multiple modules across multiple source directories.

#### Project structure

```
my-project/
├── coal.json
├── src/
│   ├── Main.coal
│   └── Utils/
│       └── Helpers.coal
└── lib/
    └── Data/
        └── Types.coal
```

#### coal.json

```json
{
  "name": "my-project",
  "version": "0.1.0",
  "modules": [
    "Main",
    "Utils.Helpers",
    "Data.Types"
  ],
  "source_dirs": [
    "./src",
    "./lib"
  ]
}
```

#### src/Main.coal

```coal
module Main {
  import IO(println_string)
  import Utils.Helpers(format_message)
  import Data.Types(User)
  
  fun main() = println_string(format_message("Hello!"))
}
```

#### src/Utils/Helpers.coal

```coal
module Utils.Helpers {
  fun format_message(msg: String): String = 
    "[INFO] " ++ msg
}
```

#### lib/Data/Types.coal

```coal
module Data.Types {
  data User = User { name: String, age: Nat }
}
```

#### Building

```bash
coal install
coal build
```

The compiler will:

1. Search for `Main.coal` in `./src` (finds `src/Main.coal`)
2. Search for `Utils/Helpers.coal` in `./src` (finds `src/Utils/Helpers.coal`)
3. Search for `Data/Types.coal` in `./src`, then `./lib` (finds `lib/Data/Types.coal`)

## Troubleshooting

### Common errors

> #### "Project manifest (coal.json) file is missing"

**Problem:** The current directory doesn't contain a `coal.json` file.

**Solution:** Create a `coal.json` manifest file. See [Creating a new project](#creating-a-new-project).

```bash
cat > coal.json << 'EOF'
{
  "name": "my-project",
  "version": "0.1.0",
  "modules": ["Main"]
}
EOF
```

> #### "No project lock-file found. Try running `coal install`."

**Problem:** Running `coal build` without a `coal.lock.json` file.

**Solution:** Run `coal install` first to generate the lock file:

```bash
coal install
coal build
```

> #### "Project manifest (coal.json) file format is invalid"

**Problem:** The `coal.json` file contains invalid JSON or is missing required fields.

**Solution:** Verify your JSON syntax and ensure all required fields are present:

- `name` (required)
- `modules` (required, must be an array)

Use a JSON validator or linter to check your file.

> #### "No install candidate found for package '<name>'"

**Problem:** No version in the Git repository matches your version constraint.

**Possible causes:**

1. The repository has no tags
2. Tags don't follow the `v<major>.<minor>.<patch>` format
3. No tagged version satisfies your constraint

**Solution:**

1. Check that the repository has valid SemVer tags: `git ls-remote --tags <repo-url>`
2. Try using a wildcard constraint: `"version": "*"`
3. Verify the repository URL is correct

> #### "The package '<name>' is missing a manifest file"

**Problem:** A dependency doesn't have a `coal.json` file.

**Solution:** Ensure the dependency repository contains a valid `coal.json` at its root. This is required for all Coal packages.

> #### "'<module>' is not a valid module name"

**Problem:** A module name in the `modules` array doesn't follow Coal's naming conventions.

**Solution:** Module names must:

- Start with an uppercase letter
- Use dots (`.`) to separate nested modules
- Contain only alphanumeric characters and dots

Valid examples: `"Main"`, `"Utils.Helpers"`, `"Data.Types.User"`

### Debug options

#### Generating debug artifacts

Use the `--generate-debug-artifacts` flag with `coal compile` to generate additional debugging information:

```bash
coal compile -I. Main.coal -o dist --generate-debug-artifacts
```

This generates:

- Graphviz DOT files for visualizing the compilation pipeline
- Build information files with detailed compilation metadata

These files are stored in the `.debug/` directory.

#### Viewing LLVM IR

Use the `--debug-llvm-ir` flag to output the intermediate LLVM IR:

```bash
coal compile -I. Main.coal -o dist --debug-llvm-ir
```

This outputs the LLVM intermediate representation before final compilation, useful for:

- Understanding code generation
- Debugging optimization issues
- Analyzing performance

#### Silent mode

Use `--silent` or `-s` to suppress compiler output:

```bash
coal compile -s -I. Main.coal -o dist
```

Useful for build scripts and automation where you only want to see errors.

#### Disabling cache

Use `--no-cache` to disable the compilation cache:

```bash
coal compile --no-cache -I. Main.coal -o dist
```

Forces a complete recompilation, useful when:

- Debugging cache-related issues
- Ensuring a clean build
- External files have changed but aren't detected
