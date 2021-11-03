from abc import ABC, abstractmethod


class GraphInterface(ABC):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "The Matrix from this graph:\n"

    @abstractmethod
    def add_vertex(self, v):
        pass

    @abstractmethod
    def add_edge(self, v, u, w=1):
        pass

    @abstractmethod
    def get_neighbors(self, v):
        pass

    @abstractmethod
    def remove_edge(self, v, u):
        pass

    @abstractmethod
    def get_edges(self):
        pass

    @abstractmethod
    def remove_vertex(self, v):
        pass

    @abstractmethod
    def get_vertices_list(self):
        pass

    @abstractmethod
    def vertex_deg(self, v):
        pass

    @abstractmethod
    def get_vertices_keys(self):
        pass


class Vertex:
    def __init__(self, key, idx, weight):
        self.key = key
        self.idx = idx
        self.weight = weight

    def __str__(self):
        return f'name: {self.key}, value: {self.weight}'

    def __eq__(self, other):
        return self.key == other.key

    def __le__(self, other):
        return self.weight <= other.weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __ge__(self, other):
        return not self.__lt__(other)

    def __gt__(self, other):
        return not self.__le__(other)

class Edge:
    def __init__(self, src, dst, weight=1):
        self.src = src
        self.dst = dst
        self.weight = weight


