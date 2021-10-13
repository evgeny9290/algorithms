from sched_package.task import Task
import pickle
from functools import wraps


def cache_dec(f):
    cache = {}
    @wraps(f)
    def wrapper(*args, **kwargs):
        # using pickle to hash any objects that are not hashable
        t = (pickle.dumps(args), pickle.dumps(kwargs))
        if t not in cache:
            cache[t] = f(*args, **kwargs)
        return cache[t]
    return wrapper


def prev_available_task(final_times):
    p = [0] * (len(final_times) + 1)
    for cur_task in final_times:
        for avaliable_task in final_times:
            if cur_task.start < avaliable_task.end:
                p[cur_task.name] = avaliable_task.name - 1
                break
    return p


def single_machine_weighted(tasks):
    final_times = sorted(tasks.values(), key=lambda t: t.end)
    p = prev_available_task(final_times)

    @cache_dec
    def single_machine_helper(n):
        if n == 0:
            return 0
        return max(final_times[n-1].weight + single_machine_helper(p[n]), single_machine_helper(n-1))

    return single_machine_helper(len(final_times))


if __name__ == '__main__':
    tasks = {
        1: Task(1, 1, 4, 2),
        2: Task(2, 2, 6, 4),
        3: Task(3, 5, 7, 4),
        4: Task(4, 3, 10, 7),
        5: Task(5, 8, 11, 2),
        6: Task(6, 9, 12, 1)
    }

    print(single_machine_weighted(tasks))