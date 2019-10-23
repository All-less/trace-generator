# coding: utf-8
import math
import time
import pickle
from pathlib import Path
from collections import defaultdict

import numpy as np


DATA_DIR = Path(__file__).resolve().parents[0] / 'data'
DIST_CACHE = {}
SAMPLE_CACHE = defaultdict(list)


def draw(dist_name, num=1, path=[], output_integer=True):
    """Draw random samples from a given distribution."""
    if dist_name not in DIST_CACHE:
        with (DATA_DIR / dist_name).open('rb') as f:
            DIST_CACHE[dist_name] = pickle.load(f)

    dist = DIST_CACHE[dist_name]
    for p in path:
        dist = dist[p]

    # As the drawing process is time-consuming, we generate a large batch
    # in advance and return the results from cached values.
    cache_name = dist_name + ''.join(map(str, path))
    cache = SAMPLE_CACHE[cache_name]
    while len(cache) < num:
        cache += list(dist.rvs(size=10240))

    samples = cache[:num]
    if output_integer:
        samples = [ *map(math.ceil, samples) ]

    SAMPLE_CACHE[cache_name] = cache[num:]

    return samples
