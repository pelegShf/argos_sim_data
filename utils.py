import os
import pandas as pd
import numpy as np
import networkx as nx

from visualization.main import plot_series
from consts import DEBUG_FOLDER, MATH_THRESHOLD


def read_csv(file_path):
    return pd.read_csv(file_path)

def data_cleaning(df):
    df = df.drop(df.index[0])
    return df



def build_graph(df):
    G = nx.Graph()
    for _, row in df.iterrows():
        robot_id = row['RobotID']
        neighbors = set(row['Neighbors'].split())
        for neighbor in neighbors:
            G.add_edge(robot_id, neighbor)
    return G