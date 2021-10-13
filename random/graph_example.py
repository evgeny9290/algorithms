class Graph:

    def __init__(self, graph={}):
        self.__graph = graph

    def edges(self):
        return [(node, neighbor)
                for node in self.__graph
                for neighbor in self.__graph[node]]

    def nodes(self):
        return list(self.__graph.keys())

    def isolated_nodes(self):
        return [node for node in self.__graph if not self.__graph[node]]

    def add_node(self, node):
        if node not in self.__graph:
            self.__graph[node] = []

    def add_edge(self, node1, node2):
        if node1 not in self.__graph:
            self.add_node(node1)
        if node2 not in self.__graph:
            self.add_node(node2)

        self.__graph[node1].append(node2)
        self.__graph[node2].append(node1)

    # Let's begin with the method that returns all the paths
    # between two nodes.
    # The optional path parameter is set to an empty list, so that
    # we start with an empty path by default.
    def all_paths(self, node1, node2, path=[]):
        path = path + [node1]

        if node1 not in self.__graph:
            return []

        if node1 == node2:
            return [path]

        paths = []

        # Now we'll take each node adjacent to node1 and recursively
        # call the all_paths method for them to find all the paths
        # from the adjacent node to node2.
        # The adjacent nodes are the ones in the value lists in
        # the graph dictionary.
        for node in self.__graph[node1]:
            if node not in path:

                subpaths = self.all_paths(node, node2, path)
                paths.extend(subpaths)

        return paths

    # And now the other method that returns the shortest path.
    # We'll just use the method that finds all the paths and then
    # select the one with the minimum number of nodes.
    # If there are more than one path with the minimum number of nodes,
    # the first one will be returned.
    def shortest_path(self, node1, node2):
        return sorted(self.all_paths(node1, node2), key=len)[0]

    def longest_path(self,node1, node2):
        return sorted(self.all_paths(node1, node2), key=len)[-1]


peterson_graph = {0: [4, 5, 1], 1: [0, 6, 2], 2: [1, 7, 3],
                  3: [2, 8, 4], 4: [3, 9, 0], 5: [0, 7, 8],
                  6: [1, 9, 8], 7: [2, 5, 9], 8: [3, 6, 5],
                  9: [4, 7, 6]}

g = Graph(peterson_graph)

print("The paths from '0' to '2':")
x = g.all_paths(0, 2)
for s in x:
    print(sorted(s), end= ' ')
    print(list(set(s)), end=' ')
    print(sorted(s) == list(set(s)))
    print()
print("The shortest path: ", g.shortest_path(0, 2))
print("The longest path: ", g.longest_path(0, 2))
