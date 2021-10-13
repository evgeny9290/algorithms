from Graph_package.graph import Graph
import numpy as np


def is_bipartite(graph, start):
    visited = {}

    def dfs_help(v, curr_color):
        if v in visited:
            if visited[v] != curr_color:
                return False
            else:
                return True
        else:
            visited[v] = curr_color

        for u in graph[v]:
            if not dfs_help(u.key, not curr_color):
                return False
        return True

    for vertex in graph.get_vertices_list():
        if vertex.key not in visited:
            if not dfs_help(vertex.key, True):
                return False

    left = [key for key in visited.keys() if visited[key] is False]
    right = [key for key in visited.keys() if visited[key] is True]
    return [left, right]


if __name__ == '__main__':
    bipartite_graph = {'s': {'w': 1, 'x': 1},
                       'w': {'s': 1, 'v': 1},
                       'x': {'s': 1, 'v': 1},
                       'v': {'w': 1, 'x': 1},
                       }

    g2 = Graph(directed=True)

    for vertex in bipartite_graph.keys():
        g2.add_vertex(vertex)
    for src, neighbors in bipartite_graph.items():
        for dst, _ in neighbors.items():
            g2.add_edge(src, dst)

    print(is_bipartite(g2, 's'))
    print(g2)
    # print(g2.get_edges())
