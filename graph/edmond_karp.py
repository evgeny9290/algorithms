from Graph_package.flow_graph import FlowGraph
import math


def recunstruct_path(g, parents, target):
    path = []
    while True:
        edge = g[parents[target]][target]
        path.append(edge)
        target = parents[target]
        if parents[target] is None:
            return path[::-1]


def augmenting_path_bfs(g, src='s', target='t'):
    visited = []
    q = []
    parent = {src: None}

    def bfs_helper(g, src='s', target='t'):
        q.append(src)
        while q:
            s = q.pop(0)
            for edge in g[s].values():
                if edge.dst() not in visited and edge.remaining_cap() > 0:
                    visited.append(edge.dst())
                    parent[edge.dst()] = s
                    q.append(edge.dst())
                if edge.dst() == target:
                    return parent

    parents = bfs_helper(g, src, target)
    return recunstruct_path(g, parents, target)


def edmond_karp(graph, source='s', target='t'):
    path = augmenting_path_bfs(graph)
    max_flow = 0
    while path:
        bottle_neck = math.inf
        for edge in path:
            bottle_neck = min(bottle_neck, edge.remaining_cap())

        max_flow += bottle_neck

        for edge in path:
            edge.augment(bottle_neck)

        path = augmenting_path_bfs(graph)

    return max_flow


if __name__ == '__main__':
    # test_graph = {
    #     's': {1: 7, 2: 6},
    #     1: {2: 4},
    #     2: {3: 3, 4: 6},
    #     3: {1: 1, 5: 4},
    #     4: {3: 3, 5: 2, 't': 3},
    #     5: {'t': 5}
    # }

    # n = 1e7
    test_graph = {
        's': {1: 7, 2: 6},
        1: {'t': 1, 2: 4},
        2: {'t': 6}
    }

    g = FlowGraph(graph=test_graph)
    # print(g)

    # print(one_go_ford_fulkerson(g))
    # print(find_augmented_path(g))
    print(edmond_karp(g))
    # print(g)