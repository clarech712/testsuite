# bin2

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
