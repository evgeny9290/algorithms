import numpy as np


def bucket_sort(arr):
    buckets = {}
    for x in arr:
        if x in buckets.keys():
            buckets[x] += 1
        else:
            buckets[x] = 1

    res = []
    buckets = {key: buckets[key] for key in sorted(buckets)}

    for k,v in buckets.items():
        for i in range(v):
            res.append(k)

    return res


def max_product_of_two(arr):
    if len(arr) < 2:
        print('array too small')
        return
    if len(arr) == 2:
        return [arr[0] * arr[1], [arr[0], arr[1]]]
    pos_m1, pos_m2 = arr[0], arr[0]
    neg_m1, neg_m2 = arr[0], arr[0]
    for i in range(1, len(arr)):
        if arr[i] > pos_m1:
            pos_m2 = pos_m1
            pos_m1 = arr[i]
        elif arr[i] > pos_m2:
            pos_m2 = arr[i]

        if arr[i] < 0 and abs(arr[i]) > abs(neg_m1):
            neg_m2 = neg_m1
            neg_m1 = arr[i]
        elif arr[i] < 0 and abs(arr[i]) > abs(neg_m2):
            neg_m2 = arr[i]

    if pos_m1 * pos_m2 > neg_m1 * neg_m2:
        return [pos_m1 * pos_m2, [pos_m1, pos_m2]]
    else:
        return [neg_m1 * neg_m2, [neg_m1, neg_m2]]


if __name__ == "__main__":
    nums = [4, 3, 15, 0]
    arr = np.random.choice(nums, 100)
    res = bucket_sort(arr)
    #print(res)
    for i in range(10):
        test_arr = np.random.randint(-100, 100, size=10)
        print(test_arr)
        print(max_product_of_two(test_arr))