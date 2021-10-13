from sched_package.task import Task
from single_machine_unweighted_sched import single_machine_unweighted
from multiple_machine_unweighted import multiple_machine_unweighted


def are_compatible_easy_ver(tasks):
    res = single_machine_unweighted(tasks)
    return len(tasks) == len(res)


def are_compatible_hard_ver(tasks):
    start_times = [(t.start, True) for t in tasks]
    final_times = [(t.end, False) for t in tasks]
    merged_list = sorted(start_times + final_times, key=lambda x: x[0])
    for i in range(1, len(merged_list)):
        if merged_list[i-1][1] == merged_list[i][1]:
            return False
    return True


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

    for machine_tasks in multiple_machine_unweighted(tasks):
        print(f'compatible tasks? -> {are_compatible_hard_ver(machine_tasks)}')
        for task in machine_tasks:
            print(task)
        print()