from graph_package.flow_graph import FlowGraph
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


def find_augmented_path_dfs(graph, source='s', target='t'):
    path = []

    def dfs_helper(v):
        nonlocal path
        if v == target:
            return path

        for edge in graph[v].values():
            if edge not in path and edge.remaining_cap() > 0:
                path.append(edge)
                if dfs_helper(edge.dst()):
                    return True
                path.pop()

        return False

    dfs_helper(source)
    return path

# def find_augmented_path(graph, source='s', target='t'):
#     path = []
#
#     def dfs_helper(v, bottle_neck):
#         nonlocal path
#         if v == target:
#             return bottle_neck
#
#         for edge in graph[v].values():
#             if edge not in path and edge.remaining_cap() > 0:
#                 # print(edge.src(), edge.dst(), edge.remaining_cap())
#                 # print(bottle_neck)
#                 bottle_neck = min(bottle_neck, edge.remaining_cap())
#                 path.append(edge)
#                 bottle_neck = dfs_helper(edge.dst(), bottle_neck)
#                 if bottle_neck < math.inf:
#                     return bottle_neck
#
#                 path.pop()
#
#         return math.inf
#
#     return path, dfs_helper(source, math.inf)

# for e in path:
#     print(e.src(),e.dst())
# path = augmenting_path_bfs(graph)
# for e in path:
#     print(e.src(), e.dst())
# path = augmenting_path_bfs(graph)
# for e in path:
#     print(e.src(), e.dst())


def ford_fulkerson(graph, source='s', target='t'):
    path = find_augmented_path_dfs(graph)
    max_flow = 0
    while path:
        bottle_neck = math.inf
        for edge in path:
            bottle_neck = min(bottle_neck, edge.remaining_cap())

        max_flow += bottle_neck

        for edge in path:
            edge.augment(bottle_neck)

        path = find_augmented_path_dfs(graph)

    return max_flow


def one_go_ford_fulkerson(g, source='s', target='t'):
    def dfs(src, bottle_neck):
        nonlocal visited

        if src == target:
            return bottle_neck

        for edge in g[src].values():
            if edge.dst() not in visited and edge.remaining_cap() > 0:
                if bottle_neck > edge.remaining_cap():
                    bottle_neck = edge.remaining_cap()

                visited.append(edge.dst())
                bottle_neck = dfs(edge.dst(), bottle_neck)

                # we have found the target
                if bottle_neck < math.inf:
                    edge.augment(bottle_neck)
                    return bottle_neck

        return math.inf

    while True:
        visited = []
        if dfs(source, math.inf) == math.inf:
            break

    return sum([edge.get_flow() for edge in g['s'].values()])


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
    print(ford_fulkerson(g))
    # print(g)
