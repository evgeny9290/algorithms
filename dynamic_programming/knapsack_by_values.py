import numpy as np


def recunstruct_path(table, elements_w, sack_size):
    i = table.shape[0]-1
    result = []
    for j in range(table.shape[1]-1, 0, -1):
        if sack_size > 0 and table[i, j] <= sack_size:
            while table[i-1, j] == table[i, j]:
                i -= 1
            result.append(i-1)
            sack_size -= elements_w[i]
            i -= 1
    return result


def knapsack(elements_W, elements_V, sack_size):
    max_val = max(elements_V)
    n = len(elements_V)
    cache = np.zeros(shape=(len(elements_W)+1, n*max_val+1), dtype=int)
    cache[0, :] = max_val * 10
    elements_V.insert(0, None)
    elements_W.insert(0, None)

    for i in range(1, n + 1):
        for p in range(1, n*max_val + 1):
            if elements_V[i] > p:
                cache[i, p] = cache[i-1, p]
            else:
                cache[i, p] = min(cache[i-1, p], elements_W[i] + cache[i-1, p-elements_V[i]])

    return cache, recunstruct_path(cache, elements_w, sack_size)


if __name__ == '__main__':
    elements_w = [2, 1, 4, 3, 1]
    elements_v = [3, 3, 4, 4, 3]
    sack_size = 5

    table, result = knapsack(elements_W=elements_w, elements_V=elements_v, sack_size=sack_size)
    print(table)
    print(result)
