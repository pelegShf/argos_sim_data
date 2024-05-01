import pandas as pd
import networkx as nx
import multiprocessing as mp
from consts import *
from utils import build_graph, data_cleaning




def count_components(G, df):
    count = 0
    for component in nx.connected_components(G):
        if not df.loc[df[ROBOT_ID_COL].isin(component),IS_FAULTY_COL].any():
            count += 1
    return count

def worker(graph_df_tuple):
    graph, df_subset = graph_df_tuple
    return count_components(graph, df_subset)

def get_union(df, num_rows_per_timestep, G=None):
    # Clean the data once before building the graphs
    df = data_cleaning(df)

    if G is None:
        G = []
        for i in range(0, len(df), num_rows_per_timestep):
            df_subset = df[i:i+num_rows_per_timestep]
            G.append((build_graph(df_subset), df_subset))

    # Create a multiprocessing Pool
    with mp.Pool(mp.cpu_count()) as pool:
        # Use the pool.map function to parallelize the computation
        unions = pool.map(worker, G)

    return unions