from Graph_package.graph import Graph

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

if __name__ == "__main__":
    peterson_g = Graph()
    for src, neighbors in peterson_graph.items():
        for dst, _ in neighbors.items():
            peterson_g.add_edge(src, dst)

    print(peterson_g)

    """
    longest simple path using DFS
    """
    def dfs(g, start):
        visited = [start]
        max_path = []

        def dfs_helper(v):
            nonlocal max_path
            if len(max_path) < len(visited):
                max_path = visited.copy()

            for u in g[v]:
                if u.key not in visited:
                    visited.append(u.key)
                    dfs_helper(u.key)
                    visited.pop()

        dfs_helper(start)

        return max_path, len(max_path)

    print(dfs(peterson_g, 0))