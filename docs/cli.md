# CLI reference

The Coal CLI is the primary tool for compiling Coal programs and managing Coal projects. It provides commands for:

- **Compiling** individual Coal source files into executables
- **Building** projects defined by `coal.json` manifests
- **Initializing** new projects with `coal init`
- **Adding and managing dependencies** from Git repositories (`coal add`, `coal install`, `coal update`)
- **Cleaning** build artifacts

The CLI is invoked using the `coal` command, followed by a subcommand and options. All commands exit with a non-zero status on failure.

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
# Create a new project
mkdir my-project
cd my-project
coal init

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
| `--sanitize` | | Flag | Enable AddressSanitizer for debugging |
| `--entry-point MODULE.FUNCTION` | | Optional | Entry point module and function (e.g., `Main.main`) |

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


**Compile with custom entry point:**

```bash
coal compile -I. Main.coal -o myprogram --entry-point Main.main
```

### coal init

Initializes a new Coal project with a `coal.json` manifest and a basic `Main.coal` module.

#### Usage

```bash
coal init [--name NAME] [--force]
```

#### Options

| Option | Type | Description |
|--------|------|-------------|
| `--name NAME` | Optional | Project name (defaults to the current directory name) |
| `--force` | Flag | Overwrite existing `coal.json` file if it exists |

#### Behavior

1. Checks if `coal.json` already exists in the current directory
2. If it exists and `--force` is not provided, the command fails with an error
3. Creates a `src/` directory if it doesn't exist
4. Creates `src/Main.coal` with a basic "Hello, world!" template
5. Creates `coal.json` with the project configuration:
   - `name`: The project name (from `--name` or current directory)
   - `modules`: `["Main"]`
   - `source_dirs`: `["src"]`
   - `entry_point`: `"Main.main"`

#### Example

```bash
# Initialize a new project with the current directory name
mkdir my-project
cd my-project
coal init

# Or with a custom name
coal init --name my-project
```

This creates:

```
my-project/
├── coal.json
└── src/
    └── Main.coal
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
2. Uses `coal.lock.json` if present; projects without dependencies do not require a lock file
3. Loads all dependency manifests from `.coal/packages/`
4. Combines local source paths with dependency source paths
5. Compiles all modules listed in the manifest
6. Outputs an executable using the `executable_name` field if set, otherwise the project name and version from the manifest

#### Error handling

The command will fail if:

- `coal.json` is missing or invalid
- `coal.lock.json` is missing and the project has dependencies (run `coal install`)
- Any dependency manifests are missing from `.coal/packages/`
- Module names in the manifest are invalid

#### Example

```bash
# After setting up coal.json and running coal install
coal build
```

See [Creating a new project](#creating-a-new-project) for a complete workflow example.

### coal add

Adds a dependency to `coal.json` and installs it in one step.

```bash
coal add [OPTIONS] GIT_URL
```

#### Options

| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `GIT_URL` | | Required | Git repository URL (positional argument) |
| `--version CONSTRAINT` | | Optional | SemVer constraint for the dependency (defaults to `*`) |
| `--name NAME` | | Optional | Package name for the dependency (defaults to the name from the package's `coal.json`) |

#### Behavior

1. Reads the current `coal.json` from the working directory
2. If `--name` is not provided, clones the repository and derives the package name from its `coal.json` manifest
3. If `--version` is not provided, defaults to the wildcard constraint `*` (latest version)
4. Adds or updates the dependency in `coal.json` with the specified Git URL, version constraint, and package name
5. Automatically runs `coal install` to clone the dependency and generate/update `coal.lock.json`

#### Examples

**Add a dependency with default name and version:**

```bash
coal add https://git@codeberg.org/laserpants/coal-hello-world.git
```

This clones the repository temporarily to read its `coal.json` and derive the package name, adds it to `coal.json` with the `*` version constraint, and runs `coal install`.

**Add a dependency with a specific version constraint:**

```bash
coal add --version "^1.0.0" https://github.com/example/coal-core.git
```

**Add a dependency with a custom name:**

```bash
coal add --name my-utils ssh://git@example.com/utils-repo.git
```

**Add a dependency with both name and version:**

```bash
coal add --name core-lib --version "~2.1.0" https://github.com/example/coal-core.git
```

#### Error handling

The command will fail if:

- `coal.json` is missing or invalid
- The Git repository cannot be cloned (when deriving the package name)
- The cloned repository has no `coal.json` (when `--name` is not provided)
- Any step in `coal install` fails (e.g., no matching version found)

### coal update

Re-resolves dependencies and updates `coal.lock.json`. With no arguments, updates all dependencies; with one or more package names, updates only those packages plus their transitive dependencies (everything else stays pinned).

#### Usage

```bash
coal update [PACKAGE...]
```

#### Options

| Option | Type | Description |
|--------|------|-------------|
| `PACKAGE` | Optional (repeatable) | Package name(s) to update. With no arguments, all dependencies are re-resolved. |

#### Behavior

1. Reads the project lock file (`coal.lock.json`) if present; if absent, behaves like `coal install` (resolve everything fresh).
2. For named packages (if any): re-fetches available versions from the Git remote and picks the newest version satisfying **all** constraints on that package across the entire dependency graph (the project manifest plus every installed package's manifest).
3. For packages not named: keeps the locked version and commit, **provided** each entry still satisfies its constraint. If an entry no longer satisfies a constraint (e.g. because the manifest was tightened), the command fails with a stale-lock error.
4. Resolves transitive dependencies of any package that was re-resolved, recursively, so a named update may pull in new transitive dependencies or drop outdated ones.
5. Rewrites `coal.lock.json` only when something changed; otherwise reports that the lock file is up to date.
6. Prints a summary to **stdout** of what changed: each bumped package as `<name> <old-version> → <new-version>`, each new package as `+ <name> <version>`, each removed package as `- <name> <version>`. If nothing changed, prints `No changes.`.

#### Examples

**Update all dependencies:**

```bash
coal update
```

**Update a single package (and its transitive dependencies):**

```bash
coal update coal-micro-test
```

**Update multiple packages:**

```bash
coal update coal-json coal-micro-test
```

#### Error handling

The command will fail if:

- `coal.json` is missing or invalid.
- A named package is not part of the dependency graph (including the project's direct dependencies). The error lists the unknown name(s) and the known package names.
- A named update would move a package to a version that violates any pinned constraint elsewhere (for example, bumping `coal-micro-test` while another dependency pins exactly `0.9.0`). The error reports the conflict with attribution and suggests a full `coal update` or an edit to one of the conflicting declarations.
- A locked commit is no longer available in its Git repository (e.g. the tag was force-pushed or rewritten). The error suggests running `coal update`.
- Any other install-step failure (no version satisfying the constraint, Git clone failure, missing `coal.json` in a dependency).

#### Notes

- `coal update` is the intended way to refresh stale lockfiles. `coal install` does **not** re-resolve packages whose locked entries are still valid.
- The summary output goes to stdout (so it can be captured in scripts); progress lines during installation go to stderr.
- One package name maps to exactly one version in a given build. Conflicting requirements across manifests are reported as errors rather than silently choosing one.

#### Behavior

1. Reads the project lock file (`coal.lock.json`) if present; if absent, resolves everything fresh.
2. Reads dependencies from `coal.json` (direct dependencies).
3. For each dependency in the dependency graph (direct and transitive, in the order they are discovered):
   - **If a locked entry exists** for that package with the **same repository URL** and the locked version **satisfies the constraint** declared for it (including a missing/omitted constraint, which is treated as unconstrained), the install reuses that entry: the package is taken at the locked version and commit, cloning `.coal/packages/<name>/<commit>/` only if it is missing locally.
   - **If no locked entry exists, the repository URL differs, or the locked version no longer satisfies the constraint**, the install fetches the available versions from the Git remote with `git ls-remote --tags`, picks the newest version that satisfies the constraint, and resolves that package together with its transitive dependencies (recursively).
4. Validates the final resolved set: every package name maps to exactly one version, and every constraint on that name must be satisfied. If two manifests require incompatible versions, the install fails with a conflict report (see [Version constraints](#version-constraints) and the troubleshooting entries below).
5. Rewrites `coal.lock.json` only when the resolved set actually changed; otherwise reports `coal.lock.json is up to date`.
6. Prunes lock entries for packages that are no longer reachable from the current dependency graph (their `.coal/packages/<name>/<commit>/` checkouts are left on disk and are removed manually if desired).
7. Uses depth-first traversal with cycle detection (a visited package-commit pair is skipped).

#### Package storage

Packages are stored in: `.coal/packages/<package-name>/<commit-hash>/`

For example:
```
.coal/packages/hello-world/05c8b6e2c7b1ad49db83a9d035e131163482606c/
```

#### Version resolution

- Uses semantic versioning (SemVer) for version constraints.
- **Supported constraint syntax (parsed by the underlying SemVer library):** `*`; exact versions such as `"1.2.3"`; comparisons (`>=`, `>`, `<=`, `<`); space-separated conjunctions (AND); and `||` disjunctions (OR). Caret (`^`) and tilde (`~`) constraints are **not** supported.
- Wildcard `*` picks the newest available version.
- A missing or omitted `version` field is treated as unconstrained (`*`).
- Tags in Git repositories must follow SemVer format (e.g. `v1.0.0`, `v2.3.1`). `git ls-remote --tags` is called once per dependency that needs fresh resolution; with a warm, consistent lock file, `coal install` can run with no network access.

#### Error handling

The command will fail if:

- `coal.json` is missing or invalid.
- `.coal/` exists but is not a directory (stale build artifact).
- No version matches a constraint (`No install candidate found for package '<name>'`).
- Two manifests require incompatible versions of the same package (conflict report).
- The manifest was changed incompatibly with an existing lock file (run `coal update`).
- A locked commit is no longer available in its Git repository (run `coal update`).
- Git operations fail (clone, ls-remote, checkout).
- Any transitive dependency is missing its `coal.json`.

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

To remove all dependencies in a project, manually delete the `.coal/` directory:

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
  "entry_point": "Module.function",
  "executable_name": "<executable-name>",
  "build_config": {
    "generate_debug_artifacts": false,
    "debug_llvm_ir": false,
    "silent": false,
    "show_timing": false,
    "no_cache": false,
    "sanitize": false
  },
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
| `entry_point` | `String` | No | Entry point module and function (e.g., `"Main.main"`) |
| `executable_name` | `String` | No | Output executable name/path (overrides the default `<name>-<version>` naming; corresponds to `-o`/`--output` in `coal compile`) |
| `c_sources` | `Array[String]` | No | Extra C source files to compile and link |
| `build_config` | `Object` | No | Compiler build flags (all fields default to `false`) |
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

#### Build configuration

The `build_config` section controls compiler behavior when using `coal build`. All fields are optional and default to `false`, so you only need to specify the flags you want to enable.

```json
{
  "build_config": {
    "generate_debug_artifacts": true,
    "debug_llvm_ir": true,
    "silent": false,
    "show_timing": true,
    "no_cache": false,
    "sanitize": false
  }
}
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `generate_debug_artifacts` | `Boolean` | `false` | Generate build info and Graphviz DOT files (corresponds to `--generate-debug-artifacts` in `coal compile`) |
| `debug_llvm_ir` | `Boolean` | `false` | Output intermediate LLVM IR (corresponds to `--debug-llvm-ir` in `coal compile`) |
| `silent` | `Boolean` | `false` | Suppress terminal output (corresponds to `--silent`/`-s` in `coal compile`) |
| `show_timing` | `Boolean` | `false` | Show elapsed time for each compiler phase (corresponds to `--show-timing` in `coal compile`) |
| `no_cache` | `Boolean` | `false` | Disable caching (corresponds to `--no-cache` in `coal compile`) |
| `sanitize` | `Boolean` | `false` | Enable AddressSanitizer for debugging (corresponds to `--sanitize` in `coal compile`) |

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
| `version` | String | No | SemVer constraint. If omitted or `"*"`, picks latest version. Supported syntax: `*`; exact versions; `>=`, `>`, `<=`, `<`; space-separated AND; `||` OR. Caret (`^`) and tilde (`~`) are **not** supported. |
| `git` | String | Yes | Git repository URL (supports SSH, HTTPS, etc.) |

#### Version constraint examples

- `"*"` — Any version (picks latest)
- `"1.2.3"` — Exact version 1.2.3
- `">=1.2.0"` — At least 1.2.0
- `">=1.2.0 <2.0.0"` — At least 1.2.0 and below 2.0.0 (AND)
- `">=1.0.0 || >=2.0.0"` — At least 1.0.0 or at least 2.0.0 (OR)

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
      "git": "https://git@codeberg.org/laserpants/coal-hello-world.git"
    }
  }
}
```

**With custom entry point:**

```json
{
  "name": "my-app",
  "version": "0.1.0",
  "modules": ["Main", "Utils.Helpers"],
  "entry_point": "Main.main"
}
```

**With custom executable name:**

```json
{
  "name": "my-app",
  "version": "0.1.0",
  "modules": ["Main"],
  "executable_name": "bin/my-app"
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
      "version": ">=2.0.0",
      "git": "https://github.com/example/coal-core.git"
    },
    "utils": {
      "version": ">=1.5.0",
      "git": "https://git@codeberg.org/example/coal-utils.git"
    }
  }
}
```

**With build configuration:**

```json
{
  "name": "my-app",
  "version": "0.1.0",
  "modules": ["Main"],
  "entry_point": "Main.main",
  "build_config": {
    "generate_debug_artifacts": true,
    "show_timing": true
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
      "source": "https://git@codeberg.org/laserpants/coal-hello-world.git",
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

- Use `coal install` to reuse locked entries that still satisfy their constraints, resolving only what is missing or stale. The lock file is rewritten only when something changed.
- Use `coal update` to re-resolve dependencies: with no arguments, update everything to the newest versions that satisfy all constraints; with one or more package names, update only those packages (and their transitive dependencies) while keeping every other package pinned.
- Both commands validate the final resolved set: if two manifests require incompatible versions of the same package, the command fails with a conflict report.

## Dependency management

### Git-based dependencies

Coal uses Git repositories as the primary source for dependencies. This enables decentralized package distribution without requiring a central package registry.

#### Supported Git URLs

Coal supports any Git URL format recognized by your system's Git client:

- **SSH:** `ssh://git@codeberg.org/user/repo.git`
- **HTTPS:** `https://github.com/user/repo.git`
- **Git protocol:** `git://example.com/repo.git`

!!! warning "Important!"

    Do not use SSH URLs (e.g., `ssh://git@github.com/user/repo.git`) for
    public packages: `coal install` will fail unless you have SSH access
    to the repository (GitHub, Codeberg, etc.) where the package source is
    hosted. SSH is therefore only suitable for private repositories. For
    public packages, use an HTTPS URL instead (e.g.,
    `https://github.com/user/repo.git`).


#### Version tagging requirements

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
| `">=1.2.0"` | At least 1.2.0 | `1.2.0`, `1.2.1`, `2.0.0` |
| `">=1.2.0 <2.0.0"` | At least 1.2.0 and below 2.0.0 (AND) | `1.2.0`, `1.9.9` (not `2.0.0`) |
| `">=1.0.0 || >=2.0.0"` | At least 1.0.0 or at least 2.0.0 (OR) | `1.0.0`, `2.0.0`, `3.0.0` |

Supported syntax: `*`; exact versions; comparisons (`>=`, `>`, `<=`, `<`); space-separated conjunctions (AND); `||` disjunctions (OR). Caret (`^`) and tilde (`~`) constraints are **not** supported.

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

### Resolution algorithm

When you run `coal install`, the CLI performs dependency resolution using the following algorithm:

1. **Load lock file:** Read the existing `coal.lock.json` if present.
2. **Parse constraints:** Read version constraints from `coal.json` (direct dependencies).
3. **Resolve each dependency:**
   - **Lock reuse:** If a locked entry exists for the package with the **same repository URL** and the locked version **satisfies the constraint** declared for it, use the locked version and commit. Clone the package to `.coal/packages/<name>/<commit>/` only if the checkout is missing locally. (A missing/omitted `version` field is treated as unconstrained.)
   - **Fresh resolution:** If no locked entry exists, the repository URL differs, or the locked version no longer satisfies the constraint, fetch available versions from the Git remote with `git ls-remote --tags`, pick the newest version satisfying the constraint, and resolve that package together with its transitive dependencies.
   - **Conflict check:** After resolution, every package name maps to exactly one version, and every constraint on that name must be satisfied. If two manifests require incompatible versions, fail with a conflict report attributed to each requirement.
4. **Recursive install:** For packages resolved fresh, parse their `coal.json` and repeat the resolution process for their transitive dependencies.
5. **Cycle detection:** Track visited (package, commit) pairs to avoid infinite loops.
6. **Rewrite lock:** Write `coal.lock.json` only when the resolved set actually changed. Remove lock entries for packages that are no longer reachable from the dependency graph.
7. **Validate:** After resolution, check that every requirement across all manifests is satisfied. Fail with attribution if any conflict remains.

#### Transitive dependencies

If package A depends on package B, and package B depends on package C, all three packages are installed and recorded in the lock file.

#### Conflict resolution

Coal uses a lock-first approach. When you run `coal install`:

- Packages with valid locked entries (same URL, version satisfies constraint) are reused without any network access.
- Packages without valid locked entries are resolved fresh to the newest version satisfying the constraint.
- After resolution, the installer validates that every constraint across all manifests (the project manifest plus every installed package manifest) is satisfied. If conflicts remain — for example, your project requires `coal-micro-test@>=0.10.0` but another dependency requires `coal-micro-test@0.9.0` exactly — the install fails with a conflict report listing each requirement and its source.

For updating dependencies, use `coal update` instead of re-running `coal install`. See [`coal update`](#coal-update) for details.

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

#### Step 2: Initialize the project

Use `coal init` to create the project structure:

```bash
coal init
```

This creates:

- `src/` directory
- `src/Main.coal` with a basic "Hello, world!" template
- `coal.json` with the project configuration

Alternatively, you can manually create the files for more control:

```bash
cat > coal.json << 'EOF'
{
  "name": "my-project",
  "version": "0.1.0",
  "modules": ["Main"]
}
EOF

mkdir -p src
cat > src/Main.coal << 'EOF'
module Main {
  import IO(println_string)
  
  fun main() = println_string("Hello, Coal!")
}
EOF
```



#### Step 3: Install dependencies

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


#### Step 4: Build

```bash
coal build
```

This compiles your project and generates an executable (the name depends on your project name and version).

#### Step 5: Run

```bash
./my-project-0.1.0  # Or whatever executable name was generated
```

Output:
```
Hello, Coal!
```

### Adding dependencies

This tutorial shows how to add and use a Git-based dependency.

You can use `coal add` as a shortcut to add a dependency and install it in one step:

```bash
coal add https://git@codeberg.org/laserpants/coal-hello-world.git
```

This automatically updates `coal.json` and runs `coal install`. If you need more control (e.g., specifying a custom name or version constraint), you can use the `--name` and `--version` options:

```bash
coal add --name hello-world --version ">=0.1.0" https://git@codeberg.org/laserpants/coal-hello-world.git
```

Note: caret (`^`) and tilde (`~`) version constraints are **not** supported. If you pass an unsupported constraint to `coal add --version`, it silently falls back to the wildcard `*`. For supported constraint syntax, see [Version constraints](#version-constraints).

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
      "git": "https://git@codeberg.org/laserpants/coal-hello-world.git"
    }
  }
}
```

#### Step 2: Install the dependency

```bash
coal install
```

This will:

1. Resolve the `hello-world` dependency: since no locked entry exists, the installer fetches available versions from the Git remote with `git ls-remote --tags`, picks the newest version satisfying the constraint, and resolves its transitive dependencies.
2. Store the package in `.coal/packages/hello-world/<commit>/`.
3. Update `coal.lock.json` with the exact version and commit.

For a subsequent run with a warm cache and an unchanged lock file, the same packages are reused straight from the lock (cloned only if the checkout is missing locally) without any network tag scan — and the installer reports `coal.lock.json is up to date` instead of rewriting the lock.

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

---

> #### "No project lock-file found. Try running `coal install`."

**Problem:** Running `coal build` without a `coal.lock.json` file.

**Solution:** Run `coal install` first to generate the lock file:

```bash
coal install
coal build
```

---

> #### "Project manifest (coal.json) file format is invalid"

**Problem:** The `coal.json` file contains invalid JSON or is missing required fields.

**Solution:** Verify your JSON syntax and ensure all required fields are present:

- `name` (required)
- `modules` (required, must be an array)

Use a JSON validator or linter to check your file.

---

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

---

> #### "The package '<name>' is missing a manifest file"

**Problem:** A dependency doesn't have a `coal.json` file.

**Solution:** Ensure the dependency repository contains a valid `coal.json` at its root. This is required for all Coal packages.

---

> #### "'<module>' is not a valid module name"

**Problem:** A module name in the `modules` array doesn't follow Coal's naming conventions.

**Solution:** Module names must:

- Start with an uppercase letter
- Use dots (`.`) to separate nested modules
- Contain only alphanumeric characters and dots

Valid examples: `"Main"`, `"Utils.Helpers"`, `"Data.Types.User"`



---

> #### "The lockfile is out of date for package '<name>'"

**Problem:** The `coal.json` manifest was changed incompatibly with an existing `coal.lock.json` — for example, a dependency constraint was tightened and no longer matches the locked version.

**Solution:** Run `coal update` to re-resolve the dependencies and rewrite the lock file:

```bash
coal update
```

---

> #### "Version conflict for package '<name>'"

**Problem:** Two manifests in the dependency graph require incompatible versions of the same package. The error reports each requirement with its source and the version that was selected.

**Solution:** Relax one of the conflicting declarations (for example, use `">=0.9.0"` instead of an exact version pin like `"0.9.0"`), or use `coal update` to re-resolve. If a specific package must pin an exact version, consider releasing a new version of the conflicting dependency with a compatible requirement.

---

> #### "Unknown update target '<name>'"

**Problem:** `coal update <name>` was run with a package name that is not part of the dependency graph (neither a direct dependency nor a transitive dependency).

**Solution:** Check the package names. The error lists the unknown name(s) and the known package names in the lock file.

---

> #### "The locked commit for package '<name>' is no longer available"

**Problem:** The commit hash recorded in `coal.lock.json` for a package is no longer reachable in its Git repository — typically because the tag was force-pushed or the repository was rewritten.

**Solution:** Run `coal update` to pick a current version for that package.

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
