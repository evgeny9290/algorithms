from Graph_package.flow_graph import FlowGraph
from flow_ford_fulkerson import *
import pandas as pd
from collections import defaultdict

if __name__ == '__main__':
    df = pd.read_csv('data/girls_boys.csv', header=None).T
    input_graph = defaultdict(dict)

    for i in range(df.shape[0]):
        for j in range(df.shape[1]):
            if df[i][j] == 1:
                input_graph[f'boy {i}'][f'girl {j}'] = 1

    for i in range(df.shape[0]):
        input_graph['s'][f'boy {i}'] = 1
        input_graph[f'girl {i}']['t'] = 1

    graph = FlowGraph(graph=input_graph)
    # print(graph)
    print(ford_fulkerson(graph))
    # print(graph)
    print(graph.result())
    print(graph.flow())
