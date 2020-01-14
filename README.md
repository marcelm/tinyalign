[![Travis](https://travis-ci.org/marcelm/tinyalign.svg?branch=master)](https://travis-ci.org/marcelm/tinyalign)

# tinyalign

A small Python module providing edit distance (aka Levenshtein distance, that
is, counting insertions, deletions and substitutions) and Hamming distance
computation.

Its main purpose is to speed up computation of edit distance by
allowing to specify a maximum number of differences `maxdiff` (banding). If
that parameter is provided, the returned edit distance is anly accurate up to
`maxdiff`. That is, if the actual edit distance is higher than `maxdiff`, a
value larger than `maxdiff` is returned, but not necessarily the actual edit
distance.

For computing regular edit distances, you should prefer
[https://github.com/fujimotos/polyleven](polyleven) as it is faster. When
`maxdiff` is small enough (what that means depends on your data), this
module is faster.

```
>>> from tinyalign import edit_distance, hamming_distance
>>> edit_distance("banana", "ananas")
2
>>> hamming_distance("hello", "yello")
1
>>> edit_distance("hello", "world", maxdiff=2)
3
```
