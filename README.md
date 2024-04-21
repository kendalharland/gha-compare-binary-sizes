# Compare binary sizes workflow

These workflows display a pull request's impact on the size of one or more binary files.

## Overview

This project exports two callable workflows that must be used together. 
`compute-binary-sizes` runs against a project's `main` branch and caches information about a binary's on-disk and in-memory segment sizes. `compare-binary-sizes` runs against pull requests for the `main` branch and compares the binary's new segment sizes with the cached values.

## Usage

For a basic setup, trigger the `compute-binary-sizes` workflow on [push events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#push) to the main branch and the `compare-binary-sizes` workflow on [pull_request events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#pull_request) to the main branch. You may use any other branch as long as both workflows are triggered.

### Prerequisites

Create a workflow .yml file in your repository's `.github/workflows` directory. An [example workflow](#example-workflow) is available below. For more information about creating workflows, see the GitHub Help Documentation.

### Platform support

- [x] Windows
- [ ] Linux
- [ ] MacOS

### Binary file support

- [x] PE/COFF (.exe, .dll)
- [x] ELF
- [x] Mach-O
- [x] WebAssembly

## Example workflow

Below is an example workflow that calls `compute-binary-sizes`:

```
name: Example call compute

on:
  push:
    branches:
      - 'main'

jobs:
  build_app:
    runs-on: windows-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Build app
        run: make all 

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: binaries
          path: build/app/app.exe

  compute_binary_sizes:
    name: Compute binary sizes
    needs: [build_app]
    uses: kendalharland/gha-compare-binary-sizes/.github/workflows/compute-binary-sizes.yml
    with:
      artifact: binaries
```

And here is a corresponding workflow to call `compare-binary-sizes`:

```
name: Example call comapre

on:
  pull_request:
  
jobs:
  build_app:
    runs-on: windows-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Build main
        run: make all

      - name: Upload artifacts for comparison
        uses: actions/upload-artifact@v4
        with:
          name: binaries
          path: build/app/app.exe

  compare_binary_sizes:
    name: Compare binary sizes
    needs: [build_app]
    uses: kendalharland/gha-compare-binary-sizes/.github/workflows/compare-binary-sizes.yml
    with:
      artifact: binaries
```

## Contributing

Pull requests are welcome! Please see [CONTRIBUTING.md] before getting started.

## License

The scripts and documentation in this project are released under the MIT License

### To Answer:
- Can you reuse this workflow if your project does not build on windows?
- How do I contribute to it?
- What happens if there's no size data from the base ref?
- How do I use this as a presubmit check to cap binary growth?
- Can I use environment variables and/or `~` ?

### How to:
- How these workflows share data.
- How to use these workflows on branches other than 'main'

### Limitations
- Cache size and retention
- File format support

### TODO:
- Documentation about how this works at a high level.
- Name the bloaty cache after the base branch and commit.
- Write python program to diff bloaty output.
- Store bloaty output in a directory that won't conflict with user files.
- Support for rendering a table and commenting on PRs.
