import math
import numpy as np
from copy import deepcopy
from functools import wraps
import matplotlib.pyplot as plt


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


class TSPath:
    def __init__(self, mat, start_node):
        self.start_node = start_node
        self.path = self.__random_path(mat)
        self.weight = self.__path_weight(mat)

    def create_mutation(self, mat, swap_ratio=0.1):
        num_swaps = math.ceil(len(self.path) * swap_ratio)
        cpy = deepcopy(self)
        for _ in range(num_swaps):
            to_swap = np.random.choice(cpy.path[1:], 2, replace=False)
            cpy.__swap(to_swap)
        # calc new weight path
        cpy.weight = cpy.__path_weight(mat)
        return cpy

    def __random_path(self, mat):
        rand_permutation = np.random.permutation(mat.shape[0])
        start_location = np.where(rand_permutation == self.start_node)[0][0]
        rand_permutation[0], rand_permutation[start_location] = rand_permutation[start_location], rand_permutation[0]
        return rand_permutation

    def __path_weight(self, mat):
        res = 0
        for i in range(len(self.path)):
            if i == len(self.path) - 1:
                res += mat[self.path[i], self.path[0]]
            else:
                res += mat[self.path[i], self.path[i + 1]]
        return res

    def __str__(self):
        path_res = f'weight is {self.weight}: '
        for i in self.path:
            path_res += f'{i} -> '
        path_res += f'{self.path[0]}'
        return path_res

    def __swap(self, indexes):
        self.path[indexes[0]], self.path[indexes[1]] = self.path[indexes[1]], self.path[indexes[0]]


class TspGeneticSolver:
    def __init__(self, mat, start_location=0,
                 population_size=50, growth_rate=0.5,
                 num_children=2, generations=100, swap_ratio=0.1):

        self.mat = mat
        self.start_location = start_location
        self.population_size = population_size
        self.growth_rate = growth_rate
        self.num_children = num_children
        self.generations = generations
        self.swap_ratio = swap_ratio
        self.population = []
        self.solution = None
        self.results_weights = []

    @my_timer
    def solve(self):
        self.__generate_population()
        while self.generations > 0 and len(self.population) > 1:
            self.population = self.__create_new_generation()
            self.population = self.__select_best()
            self.results_weights.append(self.__best_solution().weight)
            self.generations -= 1

        self.solution = self.__best_solution()
        return self.solution, self.results_weights

    def __generate_population(self):
        for _ in range(self.population_size):
            self.population.append(TSPath(self.mat, self.start_location))

    def __select_best(self):
        elite_size = math.ceil((len(self.population) // self.num_children) * self.growth_rate)
        sorted_by_weight = sorted(self.population, key=lambda path: path.weight)
        return sorted_by_weight[:elite_size]

    def __create_new_generation(self):
        new_population = []
        for individual in self.population:
            for child in range(self.num_children):
                new_population.append(individual.create_mutation(self.mat, self.swap_ratio))
        self.population = new_population
        return self.population

    def __best_solution(self):
        return min(self.population, key=lambda path: path.weight)


if __name__ == '__main__':
    graph = np.random.randint(10, 100, size=(80, 80), dtype=int)
    for i in range(graph.shape[0]):
       graph[i, i] = 0

    random_path = TSPath(mat=graph, start_node=0)

    tsp_solver = TspGeneticSolver(mat=graph, start_location=0,
                                  population_size=200, growth_rate=1,
                                  num_children=32, generations=150, swap_ratio=0.001)

    res_final, res_weights = tsp_solver.solve()
    print(f'some random nigga: {random_path}')
    print(f'best nigga: {res_final}')

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(res_weights, color='blue', lw=2)
    plt.show()