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


def reconstruct_lcs(cache, s1):
    lcs = ""
    i, j = len(cache)-1, len(cache[0])-1
    while cache[i][j] != 0:
        if cache[i-1][j] != cache[i][j] and cache[i][j-1] != cache[i][j]:
            lcs += s1[j-1]
            i, j = i - 1, j - 1
        elif cache[i-1][j] == cache[i][j]:
            i = i - 1
        elif cache[i][j-1] == cache[i][j]:
            j = j - 1

    return lcs[::-1]


def LCS(s1, s2):
    """DP of the longest common subsequence """
    cache = [[0 for _ in range(len(s1)+1)] for _ in range(len(s2)+1)]
    for i in range(len(s2)):
        for j in range(len(s1)):
            if s1[j] == s2[i]:
                cache[i+1][j+1] = cache[i][j] + 1
            else:
                cache[i+1][j+1] = max(cache[i][j+1], cache[i+1][j])

    return reconstruct_lcs(cache, s1)


@cache_dec
def lcs(X, Y):
    """DP of the longest common subsequence """
    if len(X) == 0 or len(Y) == 0:
        return 0
    elif X[-1] == Y[-1]:
        return 1 + lcs(X[:-1], Y[:-1])
    else:
        return max(lcs(X, Y[:-1]), lcs(X[:-1], Y))

# Driver program to test the above function
X = "AgfggAB"
Y = "GXasdfgdAYB"

print("Length of LCS is ", LCS(X, Y))