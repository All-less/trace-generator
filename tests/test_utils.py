# coding: utf-8
from context import spar
from spar import utils


def test_draw():
    print(utils.draw('task_num_dist.pkl', num=5, output_integer=True))
