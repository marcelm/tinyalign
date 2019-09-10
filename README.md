[![Travis](https://travis-ci.org/marcelm/tinyalign.svg?branch=master)](https://travis-ci.org/marcelm/tinyalign)

# tinyalign

A small Python module providing edit distance (aka Levenshtein distance, that is,
counting insertions, deletions and substitutions) and Hamming distance computation.

```
>>> from tinyalign import edit_distance, hamming_distance
>>> edit_distance("banana", "ananas")
2
>>> hamming_distance("hello", "yello")
1
```
