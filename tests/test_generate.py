# coding: utf-8
from context import spar
from spar import generate


def test_random_dag():
    print(generate.random_dag(10))


def test_random_job():
    print(generate.random_job())
