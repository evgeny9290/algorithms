from graph_package.graph import Graph

#  testing

class UnionFind:
    def __init__(self):
        self.representor_sets = {}

    def make_set(self, key):
        self.representor_sets[key] = key

    def find(self, key):
        return self.representor_sets[key]

    def union(self, x, y):
        x_r, y_r = self.find(x), self.find(y)

        for key, rep in self.representor_sets.items():
            if rep == y_r:
                self.representor_sets[key] = x_r


def kruskal(graph):
    uf = UnionFind()
    mst_trees = {}
    used_edges = []
    edges = sorted(g.get_edges(), key=lambda x: x.weight)
    for v in g.get_vertices_list():
        uf.make_set(v.key)

    for edge in edges:
        if uf.find(edge.src) != uf.find(edge.dst):
            used_edges.append(edge)
            uf.union(edge.src, edge.dst)
            # used_edges.append(edge)

    #get all mst trees if graph is disconnected
    for edge in used_edges:
        if uf.find(edge.src) in mst_trees:
            mst_trees[uf.find(edge.src)] += [(edge.src, edge.dst, edge.weight)]
        else:
            mst_trees[uf.find(edge.src)] = [(edge.src, edge.dst, edge.weight)]
    return mst_trees


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
                  'x': {'w': 10},
                  'w': {}
                  }
    g = Graph()
    for src, neighbors in test_graph.items():
        for dst, w in neighbors.items():
            g.add_edge(src, dst, w)

    print(g, end='\n\n')
    print(kruskal(g))
