# UFF Utils 

UFF Utils is a command-line tool for inspecting and manipulating UFF files (e.g., take subsets, move, rotate, scale). For example, if you want to take a subset of every 1000th node and scale a file from m to mm, and inspect the resulting file, you can do: 

```powershell 
uffutils subset in.uff subset.uff --step 1000
uffutils scale subset.uff scaled.uff --length 1000
uffutils inspect scaled.uff
```

For more functionality, see the description of each command below. 

## Installing

A good way to run UFF utils is through [`uv`](https://docs.astral.sh/uv/getting-started/installation/). Once you have installed `uv`, you can run `uffutils` like so: 

```powershell 
uvx uffutils --help
```

## The `inspect` command 

The `inspect` command allows you to view the contents of a UFF file. Example usage: 

```sh 
uffutils inspect my_file.uff  # Print nice overview 
uffutils inspect my_file.uff --nodes # Print full list of nodes
```

## The `subset` command

Allows you to create file with a subset of nodes, which is particularly useful if you want to downsize a UFF file. Usage: 


```sh
uffutils subset in.uff out.uff --ids "1,2,3"  # Only takes nodes 1, 2 and 3
uffutils subset in.uff out.uff --step 1000  # Takes every 1000th node, starting at 1 
uffutils subset in.uff out.uff --max 100 # Takes the first 100 nodes 
```

Operations can be combined. The following operation yields a file with nodes 10 and 30. 

```sh
uffutils subset in.uff out.uff `
    --selection "10,20,30,40,50"
    --step 2
    --max 2
```

## The `scale` command  

You can scale length: 

```sh
uffutils scale in.uff out.uff --length 1000 
```

## The `move` command 

You can translate the data: 

```sh 
uffutils move in.uff out.uff --xyz 10.0 20.0 30.0 
```

## The `rotate` command

You can rotate the data: 

```sh 
uffutils rotate in.uff out.uff --xyz 90 90 90 --origin 0 0 0
```

## Combining operations in a single command 

You can pipe commands, like so: 

```sh
uffutils subset in.uff --step 100 | `
    uffutils scale --length 1000 | `
    uffutils move - out.uff --xyz 10 20 30 `
```
