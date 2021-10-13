from .graph_interface import GraphInterface, Vertex, Edge


class AdjListGraph(GraphInterface):
    def __init__(self, directed=False) -> None:
        super().__init__()
        self.directed = directed
        self.graph = {}
        self.vertexes = {}

    def __str__(self) -> str:
        return super().__str__() \
               + "\n".join([str(src) + ' -> ' + str(neighbors) for src, neighbors in self.graph.items()])

    def get_vertices_keys(self):
        return list(self.graph.keys())

    def get_edges(self):
        edges = []
        visited = []
        for v, neighbors in self.graph.items():
            visited.append(v)
            for u, weight in neighbors.items():
                # [from, to, weight]
                if u not in visited and not self.directed:
                    continue
                edges.append(Edge(v, u, weight))
        return edges

    def add_vertex(self, key, weight=0):
        """
        this function will add Vertex to the graph
        :param key: vertex name
        :return: None
        """
        if key in self.vertexes:
            raise Exception("already exist")
        # creating the vertex
        self.vertexes[key] = Vertex(key, 0, weight)
        self.graph[key] = {}

    def add_edge(self, v, u, w=1):
        """
        this function will add edge to the graph.
        in case of missing Vertexes, they will be inserted automatically.
        :param v:
        :param u:
        :param w:
        :return: None
        """
        # adding the vertexes if not exist
        if v not in self.vertexes:
            self.add_vertex(v)
        if u not in self.vertexes:
            self.add_vertex(u)
        # assigning the weight of the edge
        self.graph[v][u] = w
        if not self.directed:
            self.graph[u][v] = w

    def get_neighbors(self, key):
        """
        this function will get all the neighbors names.
        :param key:
        :return: list of neighbors names
        """
        if key not in self.vertexes:
            raise Exception("Not exist")

        # returning all the outgoing

        # incoming_neighbors = [self.vertexes[key] for src, neighbors in self.adj_list.items() if key in neighbors]
        # incoming_neighbors = []

        # return all the incoming neighbors
        # outgoing_neighbors = list(self.adj_list[key].keys())
        outgoing_neighbors = [self.vertexes[neighbor] for neighbor in self.graph[key].keys()]
        # if self.directed:
        #     return outgoing_neighbors

        return list(set(outgoing_neighbors))

    def remove_vertex(self, v):
        """
        will remove the vertex (if exists)
        :param v:
        :return: None
        """
        if v in self.vertexes:
            # removing the vertex from the dictionaries
            del self.vertexes[v]
            # removing the outgoing edges
            del self.graph[v]
            # removing the incoming edges
            for src, neighbors in self.graph.items():
                if v in neighbors:
                    del neighbors[v]

    def remove_edge(self, src, dst):
        """
        will remove the edge
        :param src: from vertex
        :param dst: to vertex
        :return: None
        """
        if src in self.graph and dst in self.graph[src]:
            del self.graph[src][dst]
            if not self.directed:
                del self.graph[dst][src]

    def get_vertices_list(self):
        return list(self.vertexes.values())

    def vertex_deg(self, key):
        """
        will return the number of in/out-degree in case of directed graphs
        will return the number of degree in case of undirected graph.
        :param key:
        :return: degree for undirected , [in_degree, out_degree] for directed
        """
        degree = len(self.graph[key])
        if self.directed:
            in_degree = sum([sum([1 for dst, _ in neighbors.items() if dst is key])
                             for _, neighbors in self.graph.items()])
            out_degree = degree
            return [in_degree, out_degree]
        else:
            return degree

    def all_paths(self, v1, v2, path=[]):
        path = path + [v1]
        if v1 not in self.graph:
            return []

        if v1 == v2:
            return [path]

        paths = []

        for node in self.graph[v1]:
            if node not in path:
                sub_paths = self.all_paths(node, v2, path)
                paths.extend(sub_paths)

        return paths

    def shortest_path(self, v1, v2):
        return sorted(self.all_paths(v1, v2), key=len)[0]

    def longest_path(self, v1, v2):
        return sorted(self.all_paths(v1, v2), key=len)[-1]


if __name__ == '__main__':
    peterson_graph = {
        0: {4: 1, 5: 1, 1: 1},
        1: {0: 1, 6: 1, 2: 1},
        2: {1: 1, 7: 1, 3: 1},
        3: {2: 1, 8: 1, 4: 1},
        4: {3: 1, 9: 1, 0: 1},
        5: {0: 1, 7: 1, 8: 1},
        6: {1: 1, 9: 1, 8: 1},
        7: {2: 1, 5: 1, 9: 1},
        8: {3: 1, 6: 1, 5: 1},
        9: {4: 1, 7: 1, 6: 1}
    }

    g = AdjListGraph(directed=False)
    for src, neighbors in peterson_graph.items():
        for dst, _ in neighbors.items():
            g.add_edge(src, dst)
    print(g)

    print("The paths from '0' to '2':")
    x = g.all_paths(0, 2)
    for s in x:
        print(sorted(s), end=' ')
        print(list(set(s)), end=' ')
        print(sorted(s) == list(set(s)))
        print()
    print("The shortest path: ", g.shortest_path(0, 2))
    print("The longest path: ", g.longest_path(0, 2))

    # print(g.get_vertices_list())
    # g.add_vertex('s')
    # g.add_vertex('e')
    # g.add_vertex('i')
    # g.add_vertex('y')
    #
    # g.add_edge('s', 'i', w=5)
    # g.add_edge('s', 'y')
    # g.add_edge('y', 'e')
    # g.add_edge('e', 'i')
    # g.add_edge('i', 's')
    # g.add_edge('i', 'e')
    # g.add_edge('i', 'y')

    # g.remove_vertex('i')
    # g.remove_edge('s', 'i')
    # g.remove_edge('y', 'e')
    # print(g)
    # print(g.get_neighbors('e'))
    # print(g.degree('i'))  # print(g.get_neighbors('i'))
    # g.degree()
    # g.remove_edge()
