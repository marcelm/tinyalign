# cython: language_level=3

from cpython.mem cimport PyMem_Malloc, PyMem_Free

import cython


@cython.wraparound(False)
@cython.boundscheck(False)
def edit_distance(s, t, int maxdiff=-1):
    """
    Return the edit distance between the strings s and t.
    The edit distance is the sum of the numbers of insertions, deletions,
    and mismatches that is minimally necessary to transform one string
    into the other.

    If maxdiff is not -1, then a banded alignment is performed. In that case,
    the true edit distance is returned if and only if it is maxdiff or less.
    Otherwise, a value is returned that is guaranteed to be greater than
    maxdiff, but which is not necessarily the true edit distance.
    """
    cdef:
        unsigned int m = len(s)  # index: i
        unsigned int n = len(t)  # index: j
        int e = maxdiff
        unsigned int i, j, start, stop, c, smallest
        unsigned int prev
        bint match
        bytes s_bytes, t_bytes
        char* sv
        char* tv

    # Return early if string lengths are too different
    cdef unsigned int absdiff = m - n if m > n else n - m
    if e != -1 and absdiff > e:
        return absdiff

    s_bytes = s.encode() if isinstance(s, unicode) else s
    t_bytes = t.encode() if isinstance(t, unicode) else t
    sv = s_bytes
    tv = t_bytes

    # Skip identical prefixes
    while m > 0 and n > 0 and sv[0] == tv[0]:
        sv += 1
        tv += 1
        m -= 1
        n -= 1

    # Skip identical suffixes
    while m > 0 and n > 0 and sv[m-1] == tv[n-1]:
        m -= 1
        n -= 1

    cdef unsigned int result
    cdef unsigned int* costs = <unsigned int*>PyMem_Malloc((m + 1) * sizeof(unsigned int))
    if not costs:
        raise MemoryError()

    with nogil:
        for i in range(m + 1):
            costs[i] = i
        if e == -1:
            # Regular (unbanded) global alignment
            prev = 0
            for j in range(1, n + 1):
                prev = costs[0]
                costs[0] += 1
                for i in range(1, m+1):
                    match = sv[i-1] == tv[j-1]
                    c = 1 + min(
                        prev - match,
                        costs[i],
                        costs[i-1],
                    )
                    prev = costs[i]
                    costs[i] = c
            result = costs[m]
        else:
            # Banded alignment
            smallest = 0
            for j in range(1, n + 1):
                stop = min(j + e + 1, m + 1)
                if j <= e:
                    prev = costs[0]
                    costs[0] += 1
                    smallest = costs[0]
                    start = 1
                else:
                    start = j - e
                    prev = costs[start - 1]
                    smallest = maxdiff + 1
                for i in range(start, stop):
                    match = sv[i-1] == tv[j-1]
                    c = 1 + min(
                        prev - match,
                        costs[i],
                        costs[i-1],
                    )
                    prev = costs[i]
                    costs[i] = c
                    smallest = min(smallest, c)
                if smallest > maxdiff:
                    break
            if smallest > maxdiff:
                result = smallest
            else:
                result = costs[m]
    PyMem_Free(costs)
    return result


def hamming_distance(unicode s, unicode t):
    """
    Compute hamming distance between two strings. If they do not have the
    same length, an IndexError is raised.

    Return the number of differences between the strings.
    """
    cdef Py_ssize_t m = len(s)
    cdef Py_ssize_t n = len(t)
    if m != n:
        raise IndexError("sequences must have the same length")
    cdef Py_ssize_t e = 0
    cdef Py_ssize_t i
    for i in range(m):
        if s[i] != t[i]:
            e += 1
    return e
