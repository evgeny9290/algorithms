from Graph_package.graph import Graph
import numpy as np
import pandas as pd


if __name__ == '__main__':
    galaxy_graph = Graph()
    df = pd.read_csv("Data/delivery_map.csv")
    vertices = list(df['Unnamed: 0'])

    for v in vertices:
        for idx, weight in enumerate(list(df[v])):
            if weight != 0:
                galaxy_graph.add_edge(v, vertices[idx])

    def bfs(graph, start):
        queue = [start]
        visited = [start]
        paths = []

        def bfs_helper(max_depth=3):
            path = []
            depth = 0
            while queue:
                v = queue.pop(0)
                path.append(v)
                if len(path) <= max_depth:
                    paths.append(path.copy())
                    if len(path) == max_depth:
                        path.pop()
                depth += 1
                for neighbor in graph[v].keys():
                    if neighbor not in visited and depth < max_depth:
                        visited.append(neighbor)
                        queue.append(neighbor)

        bfs_helper()
        return paths

    res = bfs(galaxy_graph, 'polaris')
    print(res)

    destinations = ['acturus', 'sol', 'pollux', 'vega']
    valid_paths = []
    for path in res:
        if path[-1] in destinations:
            valid_paths.append(path)

    print(valid_paths)
