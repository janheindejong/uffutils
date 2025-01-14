# UFF Utils 

This library contains a set of pipeline tools for manipulating UFF files. It contains the following: 

* `uffutils move {input_file} -x 1 -y 1 -z 1`
* `uffutils rotate {input_file} -x 1 -y 1 -z 1`
* `uffutils scale {input_file} --length 1000`
* `uffutils subset {input_file} --nodes "1,2,3,4"`
* `uffutils nodes {input_file} --step 100`

This will allow us to chain things, like so: 

```sh
uffutils read my_file.uff | 
uffutils subset --nodes $(uffutils read my_file.uff | uffutils nodes --step 100) | 
uffutils scale --length 1000 | 
uffutils write my_output_file.uff
```

Note: I might make the "reading" implicit, in case a path is passed instead of a json string. This would turn the previous command into: 

```sh
uffutils my_file.uff subset --nodes $(uffutils nodes my_file.uff --step 100) | 
uffutils scale --length 1000 | 
uffutils write my_output_file.uff
```
