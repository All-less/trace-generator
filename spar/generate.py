# coding: utf-8
from math import ceil
from random import sample
from functools import reduce
from collections import defaultdict

from .utils import draw


def random_interval():
    return draw('job_interval_dist.pkl')[0]


def random_levels(num_nodes):
    cpl = min(draw('cpl_dist.pkl', output_integer=True, path=[ min(num_nodes, 35), ])[0], num_nodes)
    levels = draw('level_dist.pkl', num=num_nodes - cpl, output_integer=True, path=[ min(cpl, 20), ])
    return levels + [ *range(1, cpl + 1) ]


def random_dag(num_nodes):
    if num_nodes == 1:
        return { 0: [] }

    # randomly select a critical path length and assign nodes along it
    nodes = defaultdict(list)
    for n, l in enumerate(sorted(random_levels(num_nodes))):
        nodes[l].append(n)

    # randomly generate edges
    parents = { n:[] for n in range(num_nodes) }
    for l in range(1, len(nodes)):
        for n in nodes[l]:
            for c in set(sample(nodes[l + 1], ceil(len(nodes[l + 1]) / len(nodes[l]) * 3 / 4))):
                parents[c].append(n)

    return parents


def random_job():
    task_num = draw('task_num_dist.pkl', num=1, output_integer=True)[0]
    job_dag = random_dag(task_num)  # { <task_1>: [ <parent_1, parent_2>, ... ], ... }

    # generate task_name, duration, plan_cpu, plan_mem, inst_num for each task
    task_info = [ *zip(
        [ f'T{k}' + reduce(str.__add__, [ f'_{p}' for p in v ], '') for k, v in job_dag.items() ],
        draw('task_duration_dist.pkl', num=len(job_dag)),
        draw('task_cpu_dist.pkl', num=len(job_dag)),
        draw('task_mem_dist.pkl', num=len(job_dag)),
        draw('instance_num_dist.pkl', num=len(job_dag), output_integer=True)
    ) ]

    # generate task_name, inst_name, duration, cpu_avg, mem_avg for each instance
    instance_info = reduce(list.__add__, [ [ *zip(
            [ task_name for _ in range(inst_num) ],
            [ f'inst_{i}' for i in range(inst_num) ],
            draw('instance_duration_dist.pkl', num=inst_num),
            draw('instance_cpu_dist.pkl', num=inst_num),
            draw('instance_mem_dist.pkl', num=inst_num)
        ) ] for task_name, _, _, _, inst_num in task_info
    ])

    return {
        'tasks': [ ','.join(map(str, info)) for info in task_info ],
        'instances': [ ','.join(map(str, info)) for info in instance_info ]
    }
