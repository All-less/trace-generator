# coding: utf-8
from functools import partial
from collections import defaultdict


class Transformer:

    def __init__(self, heter_factor, machine_conf):
        self._no_transform = False
        self._transformers = {
            'tasks': defaultdict(list),
            'instances': defaultdict(list),
        }
        if heter_factor == 1.0 and machine_conf == (96, 100):
            self._no_transform = True
        if heter_factor != 1.0:
            self._transformers['tasks'][1].append(lambda cpu: cpu * heter_factor if cpu > 75.414 else cpu / heter_factor)
            self._transformers['tasks'][2].append(lambda mem: mem * heter_factor if mem > 1.002 else mem / heter_factor)
            self._transformers['instances'][2].append(lambda d: d * heter_factor if d > 59.202 else d / heter_factor)
            self._transformers['instances'][3].append(lambda cpu: cpu * heter_factor if cpu > 64.291 else cpu / heter_factor)
            self._transformers['instances'][4].append(lambda mem: mem * heter_factor if mem > 1.024 else mem / heter_factor)
        if machine_conf[0] != 96:
            self._transformers['tasks'][1].append(lambda cpu: cpu / 96 * machine_conf[0])
            self._transformers['instances'][3].append(lambda cpu: cpu / 96 * machine_conf[0])
        if machine_conf[1] != 100:
            self._transformers['tasks'][2].append(lambda mem: mem / 100 * machine_conf[1])
            self._transformers['instances'][4].append(lambda mem: mem / 100 * machine_conf[1])

    def transform(self, job):
        if self._no_transform:
            return job
        job['tasks'] = [ self._apply(l.strip(), self._transformers['tasks']) for l in job['tasks'] ]
        job['instances'] = [ self._apply(l.strip(), self._transformers['instances']) for l in job['instances'] ]
        return job

    def _apply(self, line, transformers):
        parts = line.split(',')
        for pos, funcs in transformers.items():
            val = float(parts[pos])
            for f in funcs:
                val = f(val)
            parts[pos] = str(val)
        return ','.join(parts)
