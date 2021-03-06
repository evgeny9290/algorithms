import heapq
from board_state import *
from functools import wraps


def my_timer(orig_fun):
    import time
    @wraps(orig_fun) #will prevent the stacking problem to occure
    def wrapper(*args, **kwargs):
        start = time.time()
        result = orig_fun(*args, **kwargs)
        time_took = time.time() - start
        print(f'{orig_fun.__name__} Run in {time_took} sec')
        return result
    return wrapper


def reconstruct_path(src):
    result = [src]
    while src.parent is not None:
        result.append(src.parent)
        src = src.parent
    return result[::-1]


@my_timer
def a_star(start, target, eps=1):
    start.g = 0
    open_list = [start]
    heapq.heapify(open_list)
    closed_list = []
    while open_list:
        src = heapq.heappop(open_list)
        if src == target:
            return reconstruct_path(src)
        for dst in src.neighbors():
            dst_current_cost = src.g + 1
            if dst_current_cost < dst.g:
                dst.g = dst_current_cost
                dst.f = dst.g + eps * dst.h
                dst.parent = src
                if dst in closed_list:
                    closed_list.remove(dst)
                    heapq.heappush(open_list, dst)
                else:
                    heapq.heappush(open_list, dst)

        closed_list.append(src)

    return None


if __name__ == '__main__':
    t = np.array([
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5]
    ])
    s = np.array([
        [2, 8, 3],
        [1, 6, 4],
        [7, 0, 5]
    ])

    start = BoardState(mat=s, target=t, heuristic='manhattan')
    end = BoardState(mat=t, heuristic='manhattan')
    result = a_star(start, end, eps=1)
    for i, x in enumerate(result):
        print(f'step: {i+1}\n {x}', end='\n\n')