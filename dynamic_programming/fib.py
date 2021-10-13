from collections import defaultdict

def fib(n):
    memo = defaultdict(int)

    def fib_helper(n):
        if n in memo:
            return memo[n]
        if n == 0:
            return 0
        if n == 1:
            return 1
        val = fib_helper(n-1) + fib_helper(n-2)
        memo[n] = val
        return val

    fib_helper(n)
    return memo[n]

for i in range(50):
    print(f'{i} ->{fib(i)}')