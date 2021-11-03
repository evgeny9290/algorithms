from .matrix_graph import AdjMatrixGraph
from .list_graph import AdjListGraph


class Graph:
    def __init__(self, graph=None, graph_with_weight_vertex=None, kind='list', mat_size=10, directed=False):
        super().__init__()
        if kind == 'matrix':
            self.kind = AdjMatrixGraph(max_size=mat_size, directed=directed)
        elif kind == 'list':
            self.kind = AdjListGraph(directed=directed)
        # if graph is not None:
        #     self.__construct_graph_weighless(graph)
        if graph_with_weight_vertex is not None and graph is not None:
            self.__construct_graph_weighted_vertex(graph_with_weight_vertex, graph)
        elif graph is not None and graph_with_weight_vertex is None:
            self.__construct_graph_weighless(graph)

    def __str__(self):
        return self.kind.__str__()

    def get_vertices_keys(self):
        return self.kind.get_vertices_keys()

    def get_vertex_by_name(self, name):
        return self.kind.vertexes[name]

    def get_distance(self, src, dst):
        return self.kind.graph[src][dst]

    def get_edges(self):
        return self.kind.get_edges()

    def __getitem__(self, item):
        return self.get_neighbors(item)
        # return self.kind.graph[item]

    def add_vertex(self, key, weight=0):
        self.kind.add_vertex(key, weight)

    def add_edge(self, v, u, w=1):
        self.kind.add_edge(v, u, w)

    def get_neighbors(self, key):
        return self.kind.get_neighbors(key)

    def get_vertices_list(self):
        return self.kind.get_vertices_list()

    def remove_vertex(self, v):
        self.kind.remove_vertex(v)

    def remove_edge(self, v, u):
        self.kind.remove_edge(v, u)

    def vertex_deg(self, key):
        return self.kind.vertex_deg(key)

    def has_cycle(self):
        if self.kind.directed:
            return self.__dfs_detect_cycle_directed()
        return self.__dfs_detect_cycle_undirected()

    def __dfs_detect_cycle_directed(self):
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
            for u in self.get_neighbors(v):
                if u.key not in visited:
                    visited[u.key] = 1
                    if dfs_helper(u.key):
                        return True
                elif visited[u.key] == 1:
                    # gray node, found cycle
                    return True

            visited[v] = 2
            return False

        for vertex in self.get_vertices_list():
            visited[vertex.key] = 1
            if dfs_helper(vertex.key):
                return True
        return False

    def __dfs_detect_cycle_undirected(self):
        """ dfs returns if cycle exists in undirected graph

        Args:
            g: Graph
            start: start node
        Returns:
            True - cycle exist
            False - cycle doesnt exist
        """
        visited = [self.get_vertices_list()[0].key]

        def dfs_helper(v, parent):
            nonlocal visited
            for u in self.get_neighbors(v):
                if u.key not in visited:
                    visited.append(u.key)
                    if dfs_helper(u.key, v):
                        return True
                elif u.key != parent:
                    return True

            return False

        return dfs_helper(self.get_vertices_list()[0].key, None)

    def __construct_graph_weighless(self, graph):
        for k in graph.keys():
            self.add_vertex(k)
        for src, neighbors in graph.items():
            for dst, w in neighbors.items():
                self.add_edge(src, dst, w)

    def __construct_graph_weighted_vertex(self, graph_with_weight_vertex, graph):
        for k, data in graph_with_weight_vertex.items():
            self.add_vertex(k, data)
        for src, neighbors in graph.items():
            for dst, w in neighbors.items():
                self.add_edge(src, dst, w)


if __name__ == '__main__':
    g = Graph(directed=True)
    g.add_vertex('s')
    g.add_vertex('e')
    g.add_vertex('i')
    g.add_vertex('y')

    g.add_edge('s', 'i', w=5)
    g.add_edge('s', 'y')
    g.add_edge('y', 'e')
    g.add_edge('e', 'i')

    print(g)
