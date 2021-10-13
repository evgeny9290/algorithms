from bellman_ford import *
import math
from Graph_package.graph import Graph
from copy import deepcopy


def mat_init(graph):
    dist = deepcopy(graph.kind.graph)

    # distance mat init
    for i in range(len(graph.kind.graph[0])):
        for j in range(len(graph.kind.graph[0])):
            if i == j:
                dist[i][j] = 0
            if dist[i][j] is None:
                dist[i][j] = math.inf

    # parent mat init
    parent = deepcopy(graph.kind.graph)
    vertices = graph.get_vertices_keys()
    for i in range(len(dist[0])):
        for j in range(len(dist[0])):
            if i == j or dist[i][j] == math.inf:
                parent[i][j] = None
            else:
                parent[i][j] = vertices[i]

    return dist, parent


def floyd_warshell(graph):
    prev_mat, parent_mat = mat_init(graph)
    n = len(prev_mat[0])
    for k in range(n):
        for i in range(n):
            for j in range(n):
                new_weight = prev_mat[i][k] + prev_mat[k][j]
                if new_weight < prev_mat[i][j]:
                    prev_mat[i][j] = new_weight
                    parent_mat[i][j] = parent_mat[k][j]

    return prev_mat, parent_mat


if __name__ == '__main__':

    test_graph = {
        's': {'w': -1},
        'x': {'s': 1, 'z': 2},
        't': {'x': 2, 'y': -8},
        'y': {'x': 5, 't': 10},
        'w': {'x': 7},
        'z': {'w': 3, 's': -4}
    }

    g = Graph(kind='matrix', directed=True, mat_size=len(test_graph.keys()))
    for ver in test_graph.keys():
        g.add_vertex(ver)
    for src, neighbors in test_graph.items():
        for dst, w in neighbors.items():
            g.add_edge(src, dst, w)
    test_graph = {
        's': {'w': -1},
        'x': {'s': 1, 'z': 2},
        't': {'x': 2, 'y': -8},
        'y': {'x': 5, 't': 10},
        'w': {'x': 7},
        'z': {'w': 3, 's': -4}
    }

    # g = Graph(graph=test_graph, kind='list', directed=True, mat_size=len(test_graph.keys()))
    # graph_nodes = ['s', 'x', 't', 'y', 'w', 'z']
    # print(g)
    mat,parent = floyd_warshell(g)
    for p in parent:
        print(p)

    print()

    for x in mat:
        print(x)

    # for start_ver in g.get_vertices_list():
    #     print(bellman_ford(g, start_ver.key))
