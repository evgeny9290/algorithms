import random
from collections import defaultdict
import numpy as np


class Task:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def __str__(self):
        return f'{self.name}: {self.duration}'


def sorted_load_balacings(tasks, num_of_machines):
    """scheduling tasks for each machine to minimize max time to perform all given tasks
        will result with at most (1.5 * optimal sched)

    Params:
        tasks = list of tasks
        num_of_machines = number of machines to distribute the tasks on to

    Returns:
        list of machines with the allocated schedule and the max time needed to perform all tasks

    """
    tasks = sorted(tasks, key=lambda t: t.duration, reverse=True)
    machine_times = [0] * num_of_machines
    machine_tasks = defaultdict(list)

    for task in tasks:
        min_idx = np.argmin(machine_times)
        machine_tasks[min_idx].append(task)
        machine_times[min_idx] += task.duration

    return machine_tasks, max(machine_times)


if __name__ == '__main__':
    tasks = [Task('a1', 1), Task('a2', 1), Task('a3', 1), Task('a4', 2), Task('a5', 2),
             Task('a6', 3), Task('a7', 4), Task('a8', 4), Task('a9', 5)]
    random.shuffle(tasks)
    sched, max_time = sorted_load_balacings(tasks, num_of_machines=4)
    print(f'maximum time needed: {max_time}')
    for machine_name, tasks in sched.items():
        print(f'machine {machine_name} ->', end=' ')
        for task in tasks:
            print(f'{task}\t', end='')
        print()