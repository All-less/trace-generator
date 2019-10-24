## Spår: Cluster Trace Generator

This command-line tool generates cluster trace in a more controllable manner based on [Alibaba's cluster trace](https://github.com/alibaba/clusterdata)

[![image](https://img.shields.io/pypi/l/spar.svg)](https://python.org/pypi/spar)
[![image](https://img.shields.io/pypi/pyversions/spar.svg)](https://python.org/pypi/spar)

### Installation

It is recommended to install the tool with `pip3`.

```
pip3 install spar
```


### Usage

```
Usage: spar [OPTIONS] OUTPUT_DIR

  By default, we output an hour-long trace from the original Alibaba
  trace to the OUTPUT_DIR. But you could provide several parameters
  and we would transform the trace as follows.
  1. Up- or down-sample trace according to load-factor. For up-sampling,
  we replace the dependencies with synthesized ones.
  2. Adjust resource heterogeneity according to heter-factor.
  3. Rescale resource request and usage according to machine-conf.

  Examples:

  Generate an hour-long trace.
  $ spar --output-dir <output_path>

  Generate an hour-long trace with 2x jobs.
  $ spar --output-dir <output_path> --load-factor 2

  Generate a half-hour-long trace.
  $ spar --output-dir <output_path> --duration 0.5

  Generate an hour-long trace with the resource request and usage deviating
  from the average 1.5x the original.
  $ spar --output-dir <output_path> --heter-factor 1.5

  Generate an hour-long trace for clusters with 24 cores and 50 unit of memory.
  $ spar --output-dir <output_path> --machine-conf (24, 50)

Options:
  --trace-dir PATH                The location of Alibaba trace.
  --load-factor FLOAT             A factor adjusting the average load (i.e., #
                                  jobs/hour) of the output trace.
  --duration FLOAT RANGE          The duration (in hours) of the trace.
  --heter-factor FLOAT            A factor adjusting the heterogeneity
                                  (defined as the ratio: value/average) of the
                                  output trace.
  --machine-conf <INTEGER INTEGER>...
                                  An integer pair indicating the (CPU, memory)
                                  of each server. Default: (96, 100) as in
                                  Alibaba cluster.
  --help                          Show this message and exit.
```


### Publication

For more details, please refer to the following paper.

> Tian, Huangshi, Minchen Yu, and Wei Wang. "Characterizing and Synthesizing Task Dependencies of Data-Parallel Jobs in Alibaba Cloud." In SoCC. 2019.


### Contributing

Any form of contribution is welcome! If you find a bug, create an issue; if you extend a feature, send a pull request.
