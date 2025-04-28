# `testsuite` for Tufts HPC
Testsuite is a collection of tests that are used to validate a cluster before and after a maintenance. It produces a simple `PASS/FAIL` output for each test which 
is easier to interpret. Ideally all the tests in testsuite should `PASS` but sometimes tests may `FAIL` due to license issues or other changes. At a minimum, the
`testsuite` results after a maintenance should be no worse than the one before.

## Structure

```
.
├── bin/                      # Original binaries
│   ├── testapp               # Single module default version
│   ├── testapp_forall        # Single module all versions (non-optimized)
│   ├── testsuite             # All modules default version
│   └── testsuite_forall      # All modules all versions (non-optimized)
├── bin2/                     # Binaries during restructuring
│   ├── create_tables         # Init of testsuite.db (in case things get messed up badly)
│   ├── show_schemas          # Show schemas in provided database (try it with testsuite.db!)
│   ├── sources               # Locations from which to update NODE table
│   ├── testapp               # Single module all versions (optimized)
│   ├── testsuite             # All modules all versions (optimized)
│   ├── testsuite.db          # Stores MODULE and NODE tables
│   ├── update_module         # Updates MODULE table
│   └── update_node           # Updates NODE table
├── profiles/                 # Specification of groups of modules for testing
│   ├── Archive/              # Profiles irrelevant to Tufts cluster
│   ├── split.py              # Generates individual profiles from 'all' profile
│   └── ...                   # Individual profiles
├── testapps/                 # Specifications of tests for all modules
│   ├── Archive/              # Tests irrelevant to Tufts cluster and halfway-there tests
│   └── ...                   # Individual module tests
└── README.md                 # This file
```

## Acknowledgement
`testsuite` and `testapp` are modified from `testsuite` and `testpbs` developed by Rose Center for Advanced Computing ([RCAC](https://www.rcac.purdue.edu/)) at Purdue University. Many thanks to RCAC for developing such useful tools and sharing with us.
