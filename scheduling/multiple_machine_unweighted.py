from sched_package.task import Task
from single_machine_unweighted_sched import single_machine_unweighted


def multiple_machine_unweighted(tasks):
    res = []
    while tasks:
        machine_tasks = single_machine_unweighted(tasks)
        res.append(machine_tasks)
        for task in machine_tasks:
            del tasks[task.name]

    return res


if __name__ == '__main__':
    tasks = {
        'd': Task('d', 5, 10),
        'b': Task('b', 3, 9),
        'f': Task('f', 11, 14),
        'g': Task('g', 13, 18),
        'a': Task('a', 1, 5),
        'e': Task('e', 7, 12),
        'j': Task('j', 17, 22),
        'h': Task('h', 15, 21),
        'i': Task('i', 16, 20),
        'c': Task('c', 4, 6),
        'k': Task('k', 19, 23)
    }

    for x in multiple_machine_unweighted(tasks.copy()):
        print(x, end='\n\n')
