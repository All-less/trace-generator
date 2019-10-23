# coding: utf-8
from context import spar
from spar import progress


def test_bar():
    print('\n')
    for _ in progress.bar(range(10000)):
        pass
