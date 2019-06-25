from alignlib import edit_distance, hamming_distance

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


random.seed(10)

def random_string():
    return ''.join(random.choice('AC') for _ in range(random.randint(0, 10)))

STRING_PAIRS.extend((random_string(), random_string()) for _ in range(10000))


def test_edit_distance():
    assert edit_distance('', '') == 0
    assert edit_distance('', 'A') == 1
    assert edit_distance('A', 'B') == 1
    assert edit_distance('A', 'A') == 0
    assert edit_distance('A', 'AB') == 1
    assert edit_distance('BA', 'AB') == 2
    for s, t in STRING_PAIRS:
        assert edit_distance(s, '') == len(s)
        assert edit_distance('', s) == len(s)
        assert edit_distance(s, t) == edit_distance(t, s)


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


def test_hamming_distance_incorrect_length():
    with pytest.raises(IndexError):
        hamming_distance('A', 'BC')
