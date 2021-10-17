from graph_package.graph import Graph
from topological_sort import topological_sort, dfs
import math


def init_source_distance(nodes, start):
    distances = {key: (math.inf, None) for key in nodes}
    distances[start] = (0, None)
    return distances


def relax(dist, v, u, v_dist, u_dist, weight):
    if u_dist > v_dist + weight:
        dist[u] = (v_dist + weight, v)


def dag_shortest_path(graph, start):
    dists = topological_sort(graph)
    dist_dict = init_source_distance(dists, start)
    for node in dist_dict:
        for neighbor in graph[node]:
            relax(dist=dist_dict, v=node, u=neighbor.key,
                  v_dist=dist_dict[node][0],
                  u_dist=dist_dict[neighbor.key][0],
                  weight=graph.kind.graph[node][neighbor.key])

    return dist_dict


def reconstruct_path(parent_dict, target):
    path = []
    cur = target
    while cur:
        path.append(cur)
        cur = parent_dict[cur][1]

    path.reverse()
    return path


if __name__ == '__main__':

    test_graph = {'r': {'s': 5, 't': 3},
                  's': {'x': 6, 't': 2},
                  't': {'x': 7, 'y': 4, 'z': 2},
                  'x': {'z': 1, 'y': -1},
                  'y': {'z': -2},
                  'z': {}
                  }

    g = Graph(kind='list', directed=True)
    for src, neighbors in test_graph.items():
        for dst, w in neighbors.items():
            g.add_edge(src, dst, w)
    # print(g)
    dict_path = dag_shortest_path(g, 's')
    print(dict_path)
    print(reconstruct_path(dict_path, 'y'))
