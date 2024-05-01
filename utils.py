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

    # Add nodes with attributes
    for row in df.itertuples():
        robot_id = getattr(row, ROBOT_ID_COL)
        neighbors = set(getattr(row, NEIGHBORS_COL).split())
        attributes = {X_COL: getattr(row, X_COL), Y_COL: getattr(row, Y_COL), 
                      HEADING_COL: getattr(row, HEADING_COL), IS_FAULTY_COL: getattr(row, IS_FAULTY_COL)}
        G.add_node(robot_id, **attributes)

    # Add edges
    edges = [(row[ROBOT_ID_COL], neighbor) for _, row in df.iterrows() for neighbor in set(row[NEIGHBORS_COL].split())]
    G.add_edges_from(edges)

    return G