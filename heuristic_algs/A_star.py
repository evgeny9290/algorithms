from graph.graph_package.graph import Graph
from Vertex_Data import VertexData
import heapq


def reconstruct_path(g, src):
    result = [src.key]
    while src.weight.parent is not None:
        result.append(src.weight.parent.key)
        src = src.weight.parent
    return result[::-1]


def a_star(g, start, target, eps=1):
    if eps != 1:
        for v in g.get_vertices_list():
            v.weight.h *= eps

    g.get_vertex_by_name(start).weight.g = 0
    open_list = [g.get_vertex_by_name(start)]
    heapq.heapify(open_list)
    closed_list = []
    while open_list:
        src = heapq.heappop(open_list)
        if src.key == target:
            return reconstruct_path(g, src)
        for dst in g[src.key]:
            dst_current_cost = src.weight.g + g.get_distance(src.key, dst.key)
            if dst_current_cost < dst.weight.g:
                dst.weight.g = dst_current_cost
                dst.weight.f = dst.weight.g + dst.weight.h
                dst.weight.parent = src
                if dst in closed_list:
                    closed_list.remove(dst)
                    heapq.heappush(open_list, dst)
                else:
                    heapq.heappush(open_list, dst)

        closed_list.append(src)

    return None


if __name__ == '__main__':
    graph_data = {
        'ar': {'ze': 75, 'si': 140, 'ti': 118},
        'ze': {'or': 71},
        'si': {'or': 151, 'ri': 80, 'fa': 99},
        'ti': {'lu': 111},
        'lu': {'me': 70},
        'me': {'do': 75},
        'do': {'cr': 120},
        'cr': {'pi': 138, 'ri': 146},
        'ri': {'pi': 97},
        'pi': {'bu': 101},
        'bu': {'gi': 90, 'fa': 211}
    }

    heuristic_vertices = {
        'ar': VertexData(366),
        'ze': VertexData(374),
        'gi': VertexData(77),
        'si': VertexData(253),
        'ti': VertexData(329),
        'lu': VertexData(244),
        'me': VertexData(241),
        'do': VertexData(242),
        'cr': VertexData(160),
        'ri': VertexData(193),
        'pi': VertexData(10),
        'bu': VertexData(0),
        'or': VertexData(380),
        'fa': VertexData(176)
    }

    g = Graph(graph=graph_data, graph_with_weight_vertex=heuristic_vertices, kind='list', directed=False)
    result = a_star(g, 'ar', 'bu', eps=1)
    print(g.get_vertex_by_name(result[-1]).weight.g) # weight of the path (stored in the target g)
    print(result)


