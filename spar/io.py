# coding: utf-8


def write_job(arrival, job, task_file, instance_file):
    write_job.called += 1
    for line in job['tasks']:
        task_file.write(f'{arrival},j_{write_job.called},{line.strip()}\n')
    for line in job['instances']:
        instance_file.write(f'{arrival},j_{write_job.called},{line.strip()}\n')

# We assign a counter to `write_job` function and it will be
# used for generating `job_id`.
write_job.called = 0


def iter_job(task_file, instance_file):

    ARR_TIME, JOB_ID, REST = 0, 1, 2

    def extract(line):
        arrival_end = line.index(',')
        job_id_end = line.index(',', arrival_end + 1)
        return line[:arrival_end], line[arrival_end+1:job_id_end], line[job_id_end+1:]

    def read_lines(file, job_id, line_buffer):  # read all lines related to one job
        try:
            parts = extract(next(file))
            while parts[JOB_ID] == job_id:
                line_buffer.append(parts[REST])
                parts = extract(next(file))
            return parts
        except StopIteration:
            return '', '', ''

    next_task, next_instance = extract(next(task_file)), extract(next(instance_file))
    while next_task[JOB_ID] != '':
        arrive_at, task_lines, instance_lines = next_task[ARR_TIME], [ next_task[REST] ], [ next_instance[REST] ]
        next_task = read_lines(task_file, next_task[JOB_ID], task_lines)
        next_instance = read_lines(instance_file, next_task[JOB_ID], instance_lines)
        yield float(arrive_at), { 'tasks': task_lines, 'instances': instance_lines }
