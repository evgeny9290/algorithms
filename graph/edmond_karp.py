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


def find_augmented_path(graph, source='s', target='t'):
    path = []

    def dfs_helper(v):
        nonlocal path
        if v == target:
            return True

        for edge in graph[v].values():
            if edge not in path and edge.remaining_cap() > 0:
                path.append(edge)
                if dfs_helper(edge.dst()):
                    return True
                path.pop()

        return False

    dfs_helper(source)
    return path


def edmond_karp(graph, source='s', target='t'):
    path = find_augmented_path(graph)
    max_flow = 0
    while path:
        bottle_neck = math.inf
        for edge in path:
            bottle_neck = min(bottle_neck, edge.remaining_cap())

        max_flow += bottle_neck

        for edge in path:
            edge.augment(bottle_neck)

        path = find_augmented_path(graph)

    return max_flow


if __name__ == '__main__':
    test_graph = {
        's': {1: 7, 2: 6},
        1: {2: 4},
        2: {3: 3, 4: 6},
        3: {1: 1, 5: 4},
        4: {3: 3, 5: 2, 't': 3},
        5: {'t': 5}
    }

    # n = 1e7
    # test_graph = {
    #     's': {1: 7, 2: 6},
    #     1: {'t': 1, 2: 4},
    #     2: {'t': 6}
    # }

    g = FlowGraph(graph=test_graph)
    # print(g)

    # print(one_go_ford_fulkerson(g))
    # print(find_augmented_path(g))
    print(edmond_karp(g))
    # print(g)


# import math

from graph_package.flow_graph import FlowGraph

# def find_augmented_path(graph, source='s', target='t'):
#     path = []
#
#     def dfs_helper(v):
#         nonlocal path
#         if v == target:
#             return True
#
#         for edge in graph[v].values():
#             if edge not in path and edge.remaining_capacity() > 0:
#                 path.append(edge)
#                 if dfs_helper(edge.get_dst()):
#                     return True
#                 path.pop()
#
#         return False
#
#     dfs_helper(source)
#     return path

# def ford_fulkerson(graph, source='s', target='t'):
#     max_flow = 0
#     while True:
#         path = find_augmented_path(graph)
#         if not path:
#             break
#
#         bottle_neck = min(path, key=lambda e: e.remaining_capacity()).remaining_capacity()
#         max_flow += bottle_neck
#         for edge in path:
#             edge.augment(bottle_neck)
#
#     return max_flow
#
# # def ford_fulkerson(g, source='s', target='t'):
# #
# #     def dfs(src, bottle_neck):
# #         nonlocal visited
# #
# #         if src == target:
# #             return bottle_neck
# #
# #         for edge in g[src].values():
# #             if edge.get_dst() not in visited and edge.remaining_capacity() > 0:
# #                 visited.append(edge.get_dst())
# #                 bottle_neck = min(bottle_neck, edge.remaining_capacity())
# #                 returned_bottle_neck = dfs(edge.get_dst(), bottle_neck)
# #
# #                 # we have found the target
# #                 if returned_bottle_neck < math.inf:
# #                     edge.augment(returned_bottle_neck)
# #                     return returned_bottle_neck
# #
# #
# #         return math.inf
# #
# #     while True:
# #         visited = []
# #         if dfs(source, math.inf) == math.inf:
# #             break
# #
# #     return sum([edge.get_flow() for edge in g['s'].values()])
#
# if __name__ == '__main__':
#     # test_graph = {
#     #     's': {1: 7, 2: 6},
#     #     1: {2: 4},
#     #     2: {3: 3, 4: 6},
#     #     3: {1: 1, 5: 4},
#     #     4: {3: 3, 5: 2, 't': 3},
#     #     5: {'t': 5}
#     # }
#
#     test_graph = {
#         's': {1: 7, 2: 6},
#         1: {2: 4, 't': 1},
#         2: {'t': 6}
#     }
#     print(test_graph)
#     g = FlowGraph(graph=test_graph)
#     # print(g)
#     #
#     print(ford_fulkerson(g))
#     print(g.result())

##################################################

# def ford_fulkerson(graph, source='s', target='t'):
#     max_flow = 0
#     while True:
#         path = find_augmented_path(graph)
#         if not path:
#             break
#
#         bottle_neck = min(path, key=lambda e: e.remaining_cap()).remaining_cap()
#         max_flow += bottle_neck
#         for edge in path:
#             edge.augment(bottle_neck)
#
#     return max_flow

# def augmenting_path_bfs(g, src='s', target='t'):
#     visited = []
#     q = []
#     parent = {src: None}
#
#     def bfs_helper(g, src='s', target='t'):
#         q.append(src)
#         while q:
#             s = q.pop(0)
#             for edge in g[s].values():
#                 if edge.dst() not in visited and edge.remaining_cap() > 0:
#                     visited.append(edge.dst())
#                     parent[edge.dst()] = s
#                     q.append(edge.dst())
#                 if edge.dst() == target:
#                     return parent
#
#     parents = bfs_helper(g, src, target)
#     return recunstruct_path(g, parents, target)