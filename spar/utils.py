# coding: utf-8
import math
import time
import pickle
from pathlib import Path
from collections import defaultdict

import numpy as np
from scipy.stats import rv_histogram

DATA_DIR = Path(__file__).resolve().parents[0] / 'data' / 'distributions'
DIST_CACHE = {}
SAMPLE_CACHE = defaultdict(list)


def draw(dist_name, num=1, path=tuple(), output_integer=True, from_hist=True):
    """Draw random samples from a given distribution."""
    if dist_name not in DIST_CACHE:
        if from_hist:
            with (DATA_DIR / dist_name.replace('dist', 'hist')).open('rb') as f:
                hist = pickle.load(f)
                if isinstance(hist, dict):
                    DIST_CACHE[dist_name] = {k: rv_histogram(histogram=v, density=False) for k, v in hist.items()}
                else:
                    DIST_CACHE[dist_name] = rv_histogram(histogram=hist, density=False)
        else:
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
