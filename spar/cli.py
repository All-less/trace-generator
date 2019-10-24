# coding: utf-8
import random
from math import ceil, floor
from pathlib import Path

import click

from .io import iter_job, write_job
from .progress import Bar
from .generate import random_interval, random_job
from .transform import Transformer


@click.command()
@click.option('--trace-dir', type=click.Path(exists=True), default=(Path(__file__).parents[0] / 'data' / 'samples'),
              help='The location of Alibaba trace.')
@click.option('--output-dir', type=click.Path(exists=True), prompt=True,
              help='The directory for generated trace.')
@click.option('--load-factor', type=float, default=1,
              help='A factor adjusting the average load (i.e., # jobs/hour) of the output trace.')
@click.option('--duration', type=click.FloatRange(0, None), default=1,
              help='The duration (in hours) of the trace.')
@click.option('--heter-factor', type=float, default=1,
              help='A factor adjusting the heterogeneity (defined as the ratio: value/average) of the output trace.')
@click.option('--machine-conf', type=(int, int), default=(96, 100),
              help='An integer pair indicating the (CPU, memory) of each server. Default: (96, 100) as in Alibaba cluster.')
def main(trace_dir, output_dir, load_factor, heter_factor, machine_conf, duration):
    '''
    \b
    By default, we output an hour-long trace from the original Alibaba trace. But you
    could provide several parameters and we would transform the trace as follows.
    1. Up- or down-sample trace according to load-factor. For up-sampling,
    we replace the dependencies with synthesized ones.
    2. Adjust resource heterogeneity according to heter-factor.
    3. Rescale resource request and usage according to machine-conf.

    Examples:

    \b
    Generate an hour-long trace.
    $ spar --output-dir <output_path>

    \b
    Generate an hour-long trace with 2x jobs.
    $ spar --output-dir <output_path> --load-factor 2

    \b
    Generate a half-hour-long trace.
    $ spar --output-dir <output_path> --duration 0.5

    \b
    Generate an hour-long trace with the resource request and usage deviating from the average 1.5x the original.
    $ spar --output-dir <output_path> --heter-factor 1.5

    \b
    Generate an hour-long trace for clusters with 24 cores and 50 unit of memory.
    $ spar --output-dir <output_path> --machine-conf (24, 50)
    '''
    with (Path(trace_dir) / 'sample_tasks.csv').open() as sample_task, \
         (Path(trace_dir) / 'sample_instances.csv').open() as sample_instance, \
         (Path(output_dir) / 'batch_task.csv').open('w') as output_task, \
         (Path(output_dir) / 'batch_instace.csv').open('w') as output_instace:

        transformer = Transformer(heter_factor, machine_conf)
        output_job = lambda a, j: write_job(a, transformer.transform(j),
                                            output_task, output_instace)
        last = 0  # the arrival time of the last generated job

        total_jobs = 16749 * duration * load_factor  # total number of jobs to be generated
        step_size = int(30 * random.random() + 20)  # enlarge interval of updating progress bar to reduce overhead
        with Bar(label='Generating jobs ', expected_size=total_jobs, every=step_size) as bar:
            for i, (arrive_at, job) in enumerate(iter_job(sample_task, sample_instance)):

                # d: duration, l: load_factor
                dl = duration * load_factor
                if dl == 1:
                    # the number of jobs will not change
                    output_job(arrive_at / load_factor, job)

                elif dl > 1:
                    # insert expected dl-1 synthesized jobs
                    to_insert = ceil(dl) if floor(dl) + random.random() < dl else floor(dl)
                    for _ in range(to_insert):
                        last += random_interval() / load_factor
                        output_job(last, random_job())
                    output_job(arrive_at * duration, job)

                # when d*l < 1, retain the job with probability of d*l
                elif random.random() < dl:
                    output_job(arrive_at * duration, job)

                last = arrive_at * duration
                bar.show(int(i * dl))


if __name__ == '__main__':
    main()
