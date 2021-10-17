from .flow_edge import FlowEdge
from .graph import Graph


class FlowGraph(Graph):
    def __init__(self, graph=None, source='s', target='t'):
        super().__init__(graph=graph, directed=True)
        self.source = source
        self.target = target

    def __getitem__(self, item):
        return self.kind.graph[item]

    def residual_graph(self):
        return "\n".join([str(src) + ' -> ' + str({s: neighbor.remaining_cap()
                                                   for s, neighbor in neighbors.items()})
                                                   for src, neighbors in self.kind.graph.items()])

    def __str__(self):
        return "\n".join([str(src) + ' -> ' + str({s: f'{neighbor.get_flow()}/{neighbor.get_cap()}'
                                                   for s, neighbor in neighbors.items() if not neighbor.is_replica()})
                                                   for src, neighbors in self.kind.graph.items()])

    def result(self):
        return "Flow Network Graph\n" + "\n".join(
            [str(src) + ' -> ' + str({s: f'{neighbor.get_flow()}/{neighbor.get_cap()}'
                                      for s, neighbor in neighbors.items()
                                      if not neighbor.is_replica() and neighbor.get_flow()})
             for src, neighbors in self.kind.graph.items()]) + '\n'

    def flow(self):
        return sum([edge.get_flow() for edge in self.kind.graph[self.source].values()])

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
        if v not in self.kind.vertexes:
            self.add_vertex(v)
        if u not in self.kind.vertexes:
            self.add_vertex(u)
        # create two edges for residual graph
        self.kind.graph[v][u] = FlowEdge(v, u, w)
        self.kind.graph[u][v] = FlowEdge(u, v, cap=0)

        # each edge is a residual of the other
        self.kind.graph[v][u].residual = self.kind.graph[u][v]
        self.kind.graph[u][v].residual = self.kind.graph[v][u]

    def get_edges(self):
        edges = []
        for key in self.kind.graph.values():
            for edge in key.values():
                edges.append(edge)
        return edges
