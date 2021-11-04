from graph_package.graph import Graph
import math


class Node:
    def __init__(self, key, distance, parent=None):
        self.parent = parent
        self.key = key
        self.distance = distance


def init_source_distance(nodes, start):
    distances = {key: Node(key, math.inf) for key in nodes}
    distances[start].distance = 0
    return distances


def relax(v, u, weight):
    if u.distance > v.distance + weight:
        u.distance = v.distance + weight
        u.parent = v.key


def bellman_ford(graph, start):
    dist_dict = init_source_distance(graph.get_vertices_keys(), start)
    edges = graph.get_edges()
    vertexes = len(graph.get_vertices_list())
    for _ in range(vertexes):
        for edge in edges:
            relax(v=dist_dict[edge.src], u=dist_dict[edge.dst], weight=edge.weight)

    # if negative cycle detected, distance is updated to -inf
    for edge in edges:
        if dist_dict[edge.dst].distance > dist_dict[edge.src].distance + edge.weight:
            # dist_dict[edge.dst].distance = -math.inf
            # dist_dict[edge.dst].parent = dist_dict[edge.src].key
            return False

    return {node.key: (node.distance, node.parent) for node in dist_dict.values()}


def reconstruct_path(parent_dict, target):
    path = []
    cur = target
    while cur:
        path.append(cur)
        if parent_dict[cur][0] == -math.inf:
            return 'negative cycle, infinite path'
        cur = parent_dict[cur][1]

    path.reverse()
    return path


if __name__ == '__main__':
    test_graph = {'s': {'t': 3, 'y': 5},
                  't': {'y': 2, 'x': 6},
                  'x': {'z': 11},
                  'z': {'x': 7, 's': 3},
                  'y': {'t': -1, 'x': 4, 'z': 6}
                  }

    g = Graph(kind='list', directed=True)
    for src, neighbors in test_graph.items():
        for dst, w in neighbors.items():
            g.add_edge(src, dst, w)

    print(g)
    path = bellman_ford(g, 's')
    print(path)
    print(reconstruct_path(path, 't'))
