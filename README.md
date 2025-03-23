# Results

## Bloom Filter

* Password '**password123**' - not unique.
* Password '**newpassword**' - unique.
* Password '**admin123**' - not unique.
* Password '**guest**' - unique.

## HyperLogLog filter

| Results of comparison:  | Exact count         | HyperLogLog        |
|-------------------------|:-------------------:|:------------------:|
| Unique elements         | 28                  | 28.096141520458556 |
| Execution time (s)      | 0.0000016000        | 0.0001889000       |
