import time
import pandas as pd
import networkx as nx
import multiprocessing as mp
from consts import *
from utils import build_graph


def count_components(G, df):
    count = 0
    if(nx.is_connected(G)):
        return 1
    for component in nx.connected_components(G):
        # Count the component only if not all of its members are faulty
         for robot_id in component:
            if not df.loc[df[ROBOT_ID_COL] == robot_id, IS_FAULTY_COL].item():
                count += 1
                break
    return count

def worker(graph_df_tuple):
    graph, df_subset = graph_df_tuple
    return count_components(graph, df_subset)

def get_union(df, num_rows_per_timestep, G=None):

    # Create a multiprocessing Pool
    # with mp.Pool(mp.cpu_count()) as pool:
    #     # Use the pool.map function to parallelize the computation
    #     unions = pool.map(worker, G)
    unions = [worker(g) for g in G]
    return unions