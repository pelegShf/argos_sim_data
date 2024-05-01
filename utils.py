import os
import pandas as pd
import numpy as np
import networkx as nx

from visualization.main import plot_series
from consts import *


def read_csv(file_path):
    return pd.read_csv(file_path)

def data_cleaning(df):
    df = df.drop(df.index[0])
    return df



def build_graph(df):
    G = nx.Graph()
    for _, row in df.iterrows():
        robot_id = row[ROBOT_ID_COL]
        neighbors = set(row[NEIGHBORS_COL].split())
        
        # Add node with DataFrame row as attributes
        G.add_node(robot_id, **row[[X_COL, Y_COL, HEADING_COL, IS_FAULTY_COL]].to_dict())
        for neighbor in neighbors:
            G.add_edge(robot_id, neighbor)
    return G