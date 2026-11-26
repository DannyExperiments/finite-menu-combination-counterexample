#!/usr/bin/env python3
"""Check exact rational instances of the pairwise conflict and finite misses."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import floor

CENTER = Q(1, 2)
NEGATIVE = (Q(-1), Q(-1))
FIXED_MENU = ((Q(-17, 32), Q(15, 32)), NEGATIVE)


def probability(n):
    return CENTER + Q(1, 4 * n)


def expectation(gamble, p):
    a, b = gamble
    return (1 - p) * a + p * b


def lexicographic(gamble):
    a, b = gamble
    return (expectation(gamble, CENTER), b - a) > (0, 0)


def negative(gamble):
    return tuple(-u for u in gamble)


def conflicting_gamble(n):
    c = (CENTER + probability(n)) / 2
    return (c, c - 1)


def stabilization_index(gamble):
    a, b = gamble
    e = abs(expectation(gamble, CENTER))
    return 1 if e == 0 else floor(abs(b - a) / (4 * e)) + 1


def check_conflicts():
    assert not lexicographic(NEGATIVE)
    for n in range(1, 10001):
        p = probability(n)
        f = conflicting_gamble(n)
        assert CENTER < p < 1
        assert expectation(f, CENTER) == Q(1, 8 * n)
        assert expectation(f, p) == -Q(1, 8 * n)
        assert lexicographic(f) and not lexicographic(negative(f))
        assert expectation(negative(f), p) == Q(1, 8 * n)
        assert tuple(a + b for a, b in zip(f, negative(f))) == (0, 0)
    print("10,000 exact opposite-gamble certificates and negative singleton verified")


def check_stabilization():
    sample = tuple(product(range(-3, 4), repeat=2))
    for f in sample:
        n = stabilization_index(f)
        assert (expectation(f, probability(n)) > 0) == lexicographic(f)
        assert (expectation(f, probability(n + 1)) > 0) == lexicographic(f)
    rejected = [f for f in sample if not lexicographic(f)]
    count = 0
    for k in range(1, 4):
        for menu in combinations(rejected, k):
            n = max(map(stabilization_index, menu))
            assert all(expectation(f, probability(n)) <= 0 for f in menu)
            assert all(expectation(f, probability(n + 1)) <= 0 for f in menu)
            count += 1
    print(f"{count:,} finite-menu exclusions checked at common stabilization indices")


def check_worked_menu():
    assert not any(map(lexicographic, FIXED_MENU))
    for n in range(1, 25):
        assert any(expectation(f, probability(n)) > 0 for f in FIXED_MENU) == (n < 8)
    assert expectation(FIXED_MENU[0], probability(8)) == 0
    print("Explorer menu misses L and hits D_n exactly for 1 <= n < 8")


if __name__ == "__main__":
    check_conflicts()
    check_stabilization()
    check_worked_menu()
