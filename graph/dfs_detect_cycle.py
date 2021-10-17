from graph_package.graph import Graph
import numpy as np


def dfs_detect_cycle_undirected(g, start):
    """ dfs returns if cycle exists in undirected graph

    Args:
        g: Graph
        start: start node
    Returns:
        True - cycle exist
        False - cycle doesnt exist
    """
    visited = [start]

    def dfs_helper(v, parent):
        nonlocal visited
        for u in g[v]:
            if u not in visited:
                visited.append(u)
                if dfs_helper(u, v):
                    return True
            elif u != parent:
                return True

        return False

    return dfs_helper(start, None)


def dfs_detect_cycle_directed(g):
    """ dfs returns if cycle exists in directed graph

    Args:
        g: Graph
    Returns:
        True - cycle exist
        False - cycle doesnt exist
    """
    visited = {}

    def dfs_helper(v):
        nonlocal visited
        for u in g[v]:
            if u not in visited:
                visited[u] = 1
                if dfs_helper(u):
                    return True
            elif visited[u] == 1:
                # gray node, found cycle
                return True

        visited[v] = 2
        return False

    for vertex in g.get_vertices_list():
        visited[vertex] = 1
        if dfs_helper(vertex):
            return True
    return False

    # return dfs_helper(start, None)


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

    test_graph_2 = {0: {1: 1},
                    1: {},
                    2: {1: 1, 3: 1},
                    3: {4: 1},
                    4: {0: 1, 2: 1}
                    }

    g_with_cycle = Graph(directed=False)
    g_with_cycle_2 = Graph(directed=True)

    for vertex in test_graph.keys():
        g_with_cycle.add_vertex(vertex)
    for src, neighbors in test_graph.items():
        for dst, _ in neighbors.items():
            g_with_cycle.add_edge(src, dst)

    for vertex in test_graph_2.keys():
        g_with_cycle_2.add_vertex(vertex)
    for src, neighbors in test_graph_2.items():
        for dst, _ in neighbors.items():
            g_with_cycle_2.add_edge(src, dst)

    print(g_with_cycle_2)
    print(g_with_cycle.has_cycle())
    print(g_with_cycle_2.has_cycle())

