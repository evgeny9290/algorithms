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


def dijkstra(graph, start):
    dist_dict = init_source_distance(graph.get_vertices_keys(), start)
    res = {start: Node(start, 0)}

    while dist_dict:
        closest = min(dist_dict, key=lambda x: dist_dict[x].distance)
        res[closest] = (dist_dict[closest].distance, dist_dict[closest].parent)
        for neighbor in graph[closest]:
            if neighbor.key in dist_dict:
                relax(v=dist_dict[closest], u=dist_dict[neighbor.key],
                      weight=graph.kind.graph[closest][neighbor.key])

        del dist_dict[closest]

    return res


def reconstruct_path(parent_dict, target):
    path = []
    cur = target
    while cur:
        path.append(cur)
        cur = parent_dict[cur][1]

    path.reverse()
    return path


if __name__ == '__main__':

    test_graph = {'s': {'t': 3, 'y': 5},
                  't': {'y': 2, 'x': 6},
                  'x': {'z': 11},
                  'z': {'x': 7, 's': 3},
                  'y': {'t': 1, 'x': 4, 'z': 6}
                  }

    g = Graph(kind='list', directed=True)
    for src, neighbors in test_graph.items():
        for dst, w in neighbors.items():
            g.add_edge(src, dst, w)

    print(g)
    res = dijkstra(g, 's')
    print(res)
    print(reconstruct_path(res, 'z'))