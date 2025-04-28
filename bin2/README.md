# bin2

This is a version of the binaries I started working on after realising that the 'wrapper' approach was not going to be good enough. I have kept the folders separately both because [bin](../bin) contains some logging infrastructure that `bin2` does not and because having the folders separately has allowed me to efficiently dif outputs for single- and all-versions without things getting too messy. Optimally, this would ultimately be a single `bin` folder, of course.

## Programs

+ [create_tables](#create_tables): Init of `testsuite.db` (in case things get messed up badly)

+ [show_schemas](#show_schemas): Show schemas in provided database (try it with `testsuite.db`)

+ [update_module](#update_module): Updates `MODULE` table based on paths in `sources`

+ [update_node](#update_node): Updates `NODE` table

Note that there are eponymous `.py` files that do the heavy lifting. The shell scripts take care of the `module load`ing and `module purge`ing around that.

### `create_tables`

```
Usage: create_tables <database_name>
```

### `show_schemas`

```
Usage: show_schemas <database_name>
```

### `update_module`

```
Usage: update_module <source_path>
```

### `update_node`

```
Usage: update_node
```

## *What all do we want to test?*

+ `testapp`

  - One job per version per software

  - One job per software (all versions)

+ testsuite

  - Options or separate scripts for testing different

    + module paths

    + partitions

  - One job per software (all versions)

  - One job per node (all software all versions)

+ (Optional)

  - Convert `verify_output` from perl to python

  - GPU software tests

## *How can we make the output from these tests more readable and accessible?*

On the front end, connecting the cluster and Tableau seems the way to go, e.g. `csv` format.

### Proposed tables and columns

To avoid data duplication, we can have multiple tables.

+ `MODULE` (primary key `MODULE`,`VERSION`)

  - `MODULE` (string)

  - `VERSION` (string)

  - `GPU_ENABLED` (boolean) — Is this version of the module GPU enabled?

+ `NODE` (primary key PARTITION,NODE)

  - `PARTITION` (string)

  - `NODE` (string)

  - `HAS_GPU` (boolean) — Does this node have a GPU available?

+ `TEST` (primary key `TEST_DATE`,`MODULE`,`VERSION`,`PARTITION`,`NODE`,`GPU_USED`)

  - `TEST_DATE` (timestamp)

  - `MODULE` (string)

  - `VERSION` (string)

  - `PARTITION` (string)

  - `NODE` (string)

  - `GPU_USED` (boolean) — Was a GPU used for this test?

  - `PASS` (boolean)

  - `CAUSE` (string) — Why did the test fail?

    + Categorisation of failures encountered so far

    + `None` by default

    + `OTHER` for a decent number of failing tests

    + regex for some reoccurring key phrases

    + unsure how helpful because user may have to see log anyway

### Potentially useful srun options

+ `--partition=partition`

+ `--nodes=N`

+ `--cpus-per-task=ncpus`

+ `--cpus-per-gpu=n`

### Questions

+ *Should one be periodically testing for all nodes? How does the status of a node affect whether it should be tested?*

+ *How does one know if a `MODULE` is `GPU_ENABLED`? Is this a strictly manual task?*

+ *The TEST table is updated whenever tests are run. How large a window of data to maintain?*
