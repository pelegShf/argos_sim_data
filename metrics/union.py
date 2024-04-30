import pandas as pd

from utils import build_graph, data_cleaning


def dfs(id, graph, visited, component):
    visited.add(id)
    component.add(id)
    for neighbor in graph[id]:
        if neighbor not in visited:
            dfs(neighbor, graph, visited, component)

def count_components(graph, df):
    visited = set()
    count = 0
    for id in graph:
        if id not in visited:
            component = set()
            dfs(id, graph, visited, component)
            if not df.loc[df['RobotID'].isin(component), 'IsFaulty'].all():
                count += 1
    return count



def get_union(df,G=None):
    if G is None:
        G = df.groupby('TimeStep').apply(build_graph)
    #graph = build_graph(df)
    unions = G.apply(lambda x: count_components(x, df))
    unions = data_cleaning(unions)

    return unions