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


def find_all_SCC(g):
    #first dfs
    visited = []
    stack = []
    for v in g.get_vertices_list():
        if v.key not in visited:
            stack.extend(dfs(g, v.key, visited))  # stack.copy instead of visited
            visited = stack.copy()

    #transpose
    mat = g.kind.graph
    g.kind.graph = np.array(mat).T.tolist()

    #second dfs
    scc_list = []
    visited = []
    for v in stack[::-1]:
        if v not in visited:
            ssc = dfs(g, v, visited)
            scc_list.append(ssc)
            visited.extend(ssc.copy())

    return scc_list


if __name__ == "__main__":
    test_graph = {'s': {'v': 1},
                  'v': {'w': 1},
                  'w': {'s': 1},
                  'q': {'w': 1, 's': 1, 't': 1},
                  't': {'x': 1, 'y': 1},
                  'x': {'z': 1},
                  'z': {'x': 1},
                  'y': {'q': 1},
                  'r': {'u': 1, 'y': 1},
                  'u': {'y': 1}
                  }

    g = Graph(kind='matrix', directed=True)

    for vertex in test_graph.keys():
        g.add_vertex(vertex)
    for src, neighbors in test_graph.items():
        for dst, _ in neighbors.items():
            g.add_edge(src, dst)

    print(find_all_SCC(g))
