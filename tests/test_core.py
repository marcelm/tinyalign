from tinyalign import edit_distance, hamming_distance

import random
import pytest


STRING_PAIRS = [
    ('', ''),
    ('', 'A'),
    ('A', 'A'),
    ('AB', ''),
    ('AB', 'ABC'),
    ('TGAATCCC', 'CCTGAATC'),
    ('ANANAS', 'BANANA'),
    ('SISSI', 'MISSISSIPPI'),
    ('GGAATCCC', 'TGAGGGATAAATATTTAGAATTTAGTAGTAGTGTT'),
    ('TCTGTTCCCTCCCTGTCTCA', 'TTTTAGGAAATACGCC'),
    ('TGAGACACGCAACATGGGAAAGGCAAGGCACACAGGGGATAGG', 'AATTTATTTTATTGTGATTTTTTGGAGGTTTGGAAGCCACTAAGCTATACTGAGACACGCAACAGGGGAAAGGCAAGGCACA'),
    ('TCCATCTCATCCCTGCGTGTCCCATCTGTTCCCTCCCTGTCTCA', 'TTTTAGGAAATACGCCTGGTGGGGTTTGGAGTATAGTGAAAGATAGGTGAGTTGGTCGGGTG'),
    ('A', 'TCTGCTCCTGGCCCATGATCGTATAACTTTCAAATTT'),
    ('GCGCGGACT', 'TAAATCCTGG'),
    ]


def py_edit_distance(s, t):
    """
    Pure-Python edit distance
    """
    m = len(s)
    n = len(t)

    costs = list(range(m + 1))
    for j in range(1, n + 1):
        prev = costs[0]
        costs[0] += 1
        for i in range(1, m + 1):
            c = min(
                prev + int(s[i-1] != t[j-1]),
                costs[i] + 1,
                costs[i-1] + 1,
            )
            prev = costs[i]
            costs[i] = c

    return costs[-1]


def random_string():
    return ''.join(random.choice('AC') for _ in range(random.randint(0, 20)))


RANDOM_STRING_PAIRS = [(random_string(), random_string()) for _ in range(10000)]


def test_edit_distance():
    assert edit_distance('', '') == 0
    assert edit_distance('', 'A') == 1
    assert edit_distance('A', 'B') == 1
    assert edit_distance('A', 'A') == 0
    assert edit_distance('A', 'AB') == 1
    assert edit_distance('BA', 'AB') == 2
    for s, t in STRING_PAIRS + RANDOM_STRING_PAIRS:
        assert edit_distance(s, '') == len(s)
        assert edit_distance('', s) == len(s)
        assert edit_distance(s, t) == edit_distance(t, s)
        assert edit_distance(s, t) == py_edit_distance(s, t)


def assert_banded(s, t, maxdiff):
    banded_dist = edit_distance(s, t, maxdiff=maxdiff)
    true_dist = edit_distance(s, t)
    if true_dist > maxdiff:
        assert banded_dist > maxdiff
    else:
        assert banded_dist == true_dist


def test_edit_distance_banded():
    for maxdiff in range(5):
        assert_banded('ABC', '', maxdiff)
        for s, t in STRING_PAIRS:
            assert_banded(s, '', maxdiff)
            assert_banded('', s, maxdiff)
            assert_banded(s, t, maxdiff)
            assert_banded(t, s, maxdiff)


def test_hamming_distance():
    assert hamming_distance('', '') == 0
    assert hamming_distance('A', 'A') == 0
    assert hamming_distance('HELLO', 'HELLO') == 0
    assert hamming_distance('ABC', 'DEF') == 3
    assert hamming_distance('ABCXDEF', 'ABCYDEF') == 1


def test_hamming_distance_incorrect_length():
    with pytest.raises(IndexError):
        hamming_distance('A', 'BC')
