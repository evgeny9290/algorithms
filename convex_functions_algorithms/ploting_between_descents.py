from gradient_descent_back_tracking import *
from newton_descent_back_tracking import *
import matplotlib.pyplot as plt

if __name__ == '__main__':
    f = lambda x: x[0]**4 + x[1]**2
    x0 = [1, 1]

    epsilons = np.linspace(1e-3, 1e-4, 30)
    GD_times = []
    N_times = []
    i = 1
    for e in epsilons:
        print(i)
        _, time_GD = gradient_descent(x0, f, e, line_search=GD_backtrack, max_iters=1000, print_steps=False)
        _, time_N = newton_gradient_descent(x0, f, e, line_search=newton_backtrack, max_iters=1000)
        GD_times.append(time_GD)
        N_times.append(time_N)
        i += 1

    # print(GD_times)
    # print(N_times)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(GD_times)
    ax.plot(N_times)
    plt.show()