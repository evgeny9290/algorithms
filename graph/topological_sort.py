from Graph_package.graph import Graph
import numpy as np


def dfs(g, start, visited=None):
    if visited is None:
        visited = []

    stack = []
    visited.append(start)

    def dfs_helper(v):
        nonlocal visited, stack

        for u in g[v]:
            if u.key not in visited:
                visited.append(u.key)
                dfs_helper(u.key)

        stack.append(v)

    dfs_helper(start)

    return stack


def topological_sort(graph):
    if not graph.has_cycle():
        visited = []
        stack = []
        vertices = graph.get_vertices_list()
        for v in vertices:
            if v.key not in visited:
                stack.extend(dfs(graph, v.key, visited))  # stack.copy instead of visited
                visited = stack.copy()

        return stack[::-1]
    return 'no such sort exist'


if __name__ == "__main__":
    topological_sort_test_graph = {'shirt': {'tie': 1,'belt': 1},
                                   'tie': {'jacket': 1},
                                   'jacket': {},
                                   'belt': {'jacket': 1},
                                   'pants': {'belt': 1, 'shoes': 1},
                                   'undershorts': {'pants': 1, 'shoes': 1},
                                   'shoes': {},
                                   'socks': {'shoes': 1},
                                   'watch': {}
                                   }

    g = Graph(kind='matrix', directed=True)

    for vertex in topological_sort_test_graph.keys():
        g.add_vertex(vertex)
    for src, neighbors in topological_sort_test_graph.items():
        for dst, _ in neighbors.items():
            g.add_edge(src, dst)

    print(topological_sort(g))