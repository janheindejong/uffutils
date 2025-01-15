# UFF Utils 

This library contains a set of pipeline tools for manipulating UFF files. It works a bit like this: 

```sh
uffutils modify my_original_file.uff my_subset_file.uff --nodes-step 100
$nodes = $(uffutils describe my_subset_file.uff --nodes-only)
uffutils modify my_file.uff my_output.uff `
    --nodes $nodes) `
    --scale-length 1000 `
    --to-global-frame `
    --rotate 90,90,90 `
    --translate 100,100,100
```

# The `describe` command 

```sh 
uffutils describe my_file.uff  # Nice summary
uffutils describe my_file.uff --property nodes,datasets --full # List of nodes (line 1) & list of datasets (line 2)
uffutils describe my_file.uff --property nodes,datasets --summary # Summary of nodes & datasets (probably JSON)
```

# The `inspect` command 

```sh 
uffutils inspect my_file.uff  # Nice overview 
uffutils inspect my_file.uff --set 0 # Description of dataset 0
uffutils inspect my_file.uff --set 0 --node-nums --short # Short list of node numbers
```

# Alternative implementation

I considered doing something with piping, but got stuck in the fact the the PyUFF library I'm using can't handle streams. It would've looking something like this: 

```sh
uffutils subset my_original_file.uff my_subset_file.uff --step 100 
uffutils subset my_file.uff - --nodes $(uffutils describe my_subset_file.uff --nodes) | 
uffutils scale - my_output.uff --length 1000 
```
