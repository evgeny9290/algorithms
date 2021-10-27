import pylab
import numpy as np
import numdifftools as nd
import matplotlib.pyplot as plt


def backtrack(x0, f, alpha=0.9, beta=0.7):
    """backtrack the guess back such that the result is inside the convex area

    Args:
      x0: the initial values given
      f: given function
      alpha: alpha value between (0, .5)
      beta: beta value between (0, 1)
    Returns:
        t: the step size needed in order to return to the convex area
    """
    t = 1
    del_x = -nd.Gradient(f)(x0)
    while f(x0 + t*del_x) > f(x0) + alpha * t * np.dot(nd.Gradient(f)(x0), del_x):
        t *= beta
    return t


def gradient_descent(x0, f, epsilon, line_search=backtrack):
    """ works of convex functions to find the best parameters for the minimum.

    :param x0: initial guess
    :param f: function
    :param epsilon: stopping condition - the magnitude of the target gradient
    :param line_search: method to find the best step size
    :return: [variable value that gives the minimum,
              list of variables along the algorithm process]
    """
    del_x = -nd.Gradient(f)(x0)
    points_arr = [x0]
    while np.dot(del_x, del_x) > epsilon ** 2:
        del_x = -nd.Gradient(f)(x0)
        t = line_search(x0, f)
        x0 = x0 + t * del_x
        points_arr.append(x0)
    return x0, points_arr


def f_vals_from_grad_descent(f, cords_list):
    f_vals = []
    for cords in cords_list:
        f_vals.append(f(cords))
    return f_vals


def gradient_descent_plot3d(f, f_vals, X_vals):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = y = np.arange(-1.0, 1.0, 0.05)
    X, Y = np.meshgrid(x, y)
    zs = np.array([f([x, y]) for x, y in zip(np.ravel(X), np.ravel(Y))])
    Z = zs.reshape(X.shape)
    ax.plot_surface(X, Y, Z, alpha=0.2)
    ax.scatter(xs=np.array(X_vals)[:, 0], ys=np.array(X_vals)[:, 1], zs=f_vals, color='red', lw=5)
    plt.show()


def convergence_plot(f_vals):
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(f_vals, color='blue', lw=2)
    ax.set_yscale('log')
    pylab.show()


if __name__ == '__main__':
    f = lambda x: x[0]**2 + x[1]**4
    x0 = [1, 1]
    X_min, X_vals = gradient_descent(x0, f, 1e-4, line_search=backtrack)
    f_vals = f_vals_from_grad_descent(f, X_vals)

    convergence_plot(f_vals)
    gradient_descent_plot3d(f, f_vals, X_vals)
