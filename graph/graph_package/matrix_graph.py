from .graph_interface import GraphInterface, Vertex, Edge


class AdjMatrixGraph(GraphInterface):
    def __init__(self, max_size=100, directed=False):
        super().__init__()
        self.max_size = max_size
        self.num_vertexes = 0
        self.vertexes = {}
        self.graph = [[None] * self.max_size for _ in range(self.max_size)]
        self.idx_to_key = {}
        self.directed = directed

    def __str__(self):
        s = super().__str__() + '\n'.join([str(row) for row in self.graph])
        return s

    def get_vertices_keys(self):
        return list(self.vertexes.keys())

    def get_edges(self):
        edges = []
        for i in range(self.max_size):
            start = i if not self.directed else 0 # upper diagonal for undirected, else all matrix
            for j in range(start, self.max_size):
                if self.graph[i][j] is not None:
                    # [from, to, weight]
                    edges.append(Edge(self.idx_to_key[i], self.idx_to_key[j], self.graph[i][j]))
        return edges

    def add_vertex(self, key, weight=0):
        if self.num_vertexes > self.max_size:
            raise TypeError('key should be from 0 up to size')
        if key in self.vertexes:
            raise Exception(f'vertex with key {key} already exist')
        self.vertexes[key] = Vertex(key, self.num_vertexes, weight)
        self.idx_to_key[self.num_vertexes] = key
        self.num_vertexes += 1

    def add_edge(self, v, u, w=1):
        if v not in self.vertexes:
            self.add_vertex(v)
        if u not in self.vertexes:
            self.add_vertex(u)
        self.graph[self.vertexes[v].idx][self.vertexes[u].idx] = w
        if not self.directed:
            self.graph[self.vertexes[u].idx][self.vertexes[v].idx] = w

    def get_neighbors(self, v):
        if v not in self.vertexes:
            raise Exception(f'vertex v {v} doesnt exist')
        out_neighbors = [self.vertexes[self.idx_to_key[i]] for i, w in enumerate(self.graph[self.vertexes[v].idx]) if w is not None]
        in_edges_col = [self.graph[i][self.vertexes[v].idx] for i in range(self.max_size)]
        in_neighbors = [self.vertexes[self.idx_to_key[i]] for i, w in enumerate(in_edges_col) if w is not None]
        if self.directed:
            return out_neighbors

        return list(set(in_neighbors + out_neighbors))

    def remove_edge(self, v, u):
        if 0 <= v < self.max_size and 0 <= u < self.max_size:
            self.graph[self.vertexes[v].idx][self.vertexes[u].idx] = None
            if not self.directed:
                self.graph[self.vertexes[u].idx][self.vertexes[v].idx] = None

    def remove_vertex(self, v):
        """
        removing row and col representing the vertex v
        and removing the vertex v from the dictionaries
        """
        if v in self.vertexes:
            self.graph[self.vertexes[v].idx] = [None] * self.max_size
            for _ in self.graph:
                self.graph[self.vertexes[v].idx] = None
            del self.vertexes[v]
            del self.idx_to_key[self.vertexes[v].idx]

    def get_vertices_list(self):
        return list(self.vertexes.values())

    def vertex_deg(self, v):
        """
        if directed graph returns [in_deg,out_deg] of v
        if undirected returns degree of v
        """
        deg = sum([1 for edge in self.graph[self.vertexes[v].idx] if edge is not None])
        if self.directed:
            inc_edges = [self.graph[i][self.vertexes[v].idx] for i in range(self.max_size)]
            in_deg = sum([1 for w in inc_edges if w is not None])
            out_deg = deg
            return [in_deg, out_deg]
        else:
            return deg


if __name__ == '__main__':
    g = AdjMatrixGraph(max_size=6, directed=False)
    g.add_edge('s', 'i', w=5)
    g.add_edge('s', 'y')
    g.add_edge('y', 'e')
    g.add_edge('e', 'i')
    # g.add_edge('v0', 'v1', 5)
    # g.add_edge('v1', 'v2', 4)
    # g.add_edge('v2', 'v3', 9)
    # g.add_edge('v3', 'v4', 7)
    # g.add_edge('v4', 'v0', 1)
    # g.add_edge('v0', 'v5', 2)
    # g.add_edge('v5', 'v4', 8)
    # g.add_edge('v3', 'v5', 3)
    # g.add_edge('v5', 'v2', 1)
    # g.add_vertex('v6')  # extra vertex with no connections

    print(g)
    print(g.vertex_deg('i'))
    print(g.get_neighbors('i'))
