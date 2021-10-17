from graph_package.graph import Graph
import numpy as np
import heapq


def chosen_edge(min_heap, visited):
    edge = heapq.heappop(min_heap)
    while edge[1][1] in visited:
        try:
            edge = heapq.heappop(min_heap)
        except IndexError:
            return False
    return edge


def prim_connected_graph(graph, start, visited):
    min_heap = [(graph.kind.adj_list[start][dst.key], (start, dst.key)) for dst in graph[start]]
    visited.append(start)
    taken_edges = []
    heapq.heapify(min_heap)

    new_edge = chosen_edge(min_heap, visited)
    while new_edge:
        new_vertex = new_edge[1][1]

        taken_edges.append(new_edge)
        visited.append(new_vertex)

        for dst in graph[new_vertex]:
            heapq.heappush(min_heap, (graph.kind.adj_list[new_vertex][dst.key], (new_vertex, dst.key)))

        new_edge = chosen_edge(min_heap, visited)

    return taken_edges


def prim(graph):
    visited = []
    bst_trees = []
    for vertex in graph.get_vertices_list():
        if vertex.key not in visited:
            bst_trees.append(prim_connected_graph(graph, vertex.key, visited))

    return bst_trees


if __name__ == '__main__':
    test_graph = {'a': {'b': 4, 'h': 8},
                  'b': {'a': 4, 'h': 11, 'c': 8},
                  'c': {'b': 8, 'i': 2, 'f': 4, 'd': 7},
                  'd': {'c': 7, 'f': 14, 'e': 9},
                  'e': {'d': 9, 'f': 10},
                  'f': {'e': 10, 'd': 14, 'c': 4, 'g': 2},
                  'g': {'f': 2, 'i': 6, 'h': 1},
                  'h': {'i': 7, 'g': 1, 'b': 11, 'a': 8},
                  'i': {'c': 2, 'g': 6, 'h': 7},
                  }
    g = Graph()
    for src, neighbors in test_graph.items():
        for dst, w in neighbors.items():
            g.add_edge(src, dst, w)

    # print(g,end='\n\n')
    print(prim(g))
    # print(g.get_edges())