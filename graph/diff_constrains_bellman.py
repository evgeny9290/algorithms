from bellman_ford import *
import pandas as pd
from Graph_package.graph import Graph
from collections import defaultdict

if __name__ == '__main__':
    df = pd.read_csv("data/diff_constraints.csv", header=None).T
    g = Graph(kind='list', directed=True)
    nums = list(df[0])
    constrains_graph = defaultdict(dict)

    for i in range(0, len(nums), 3):
        constrains_graph[nums[i+1]][nums[i]] = -1 * nums[i + 2]
    constrains_graph['s'] = {i: 0 for i in constrains_graph.keys()}

    for src, neighbors in constrains_graph.items():
        for dst, w in neighbors.items():
            g.add_edge(src, dst, w)

    #               i    i+1   i+2     i+1   i      -1*i+2
    #xi, xj, bk --> xi - xj >= bk <==> xj - xi <= - bk

    #without default dict
    # constrains_graph2 = {}
    # for i in range(0, len(nums), 3):
    #     if nums[i+1] not in constrains_graph2:
    #         constrains_graph2[nums[i+1]] = {nums[i]: -1 * nums[i + 2]}
    #     else:
    #         constrains_graph2[nums[i+1]][nums[i]] = -1 * nums[i + 2]
    #
    # constrains_graph2['s'] = {i: 0 for i in constrains_graph2.keys()}
    # print(constrains_graph2)
    # for src, neighbors in constrains_graph2.items():
    #     for dst, w in neighbors.items():
    #         g.add_edge(src, dst, w)

    # print(constrains_graph2)
    print(g)
    print(bellman_ford(g, 's'))

