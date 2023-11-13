# nix-flake-to-graphviz

A simple tool to create dot files to represent the dependency graph of a given Nix flake.

## How to run it

``` sh
nix run https://github.com/rydnr/nix-flake-to-graphviz/[version]?dir=nix
```

### Usage

``` sh
nix run https://github.com/rydnr/nix-flake-to-graphviz/[version]?dir=nix [-h|--help] [-f|--flake-folder folder] [-o|--output-file file]
```
- `-h|--help`: Prints the usage.
- `-f|--flake-folder`: The folder with the Nix flake to analyze.
- `-o|--output-file`: The output file.

#### Create an image

``` sh
dot -Tpng [generated-file] > [image-file].png
```


