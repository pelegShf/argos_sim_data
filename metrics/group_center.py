from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from consts import IS_FAULTY_COL, ROBOT_ID_COL, X_COL, Y_COL
from utils import build_graph

import networkx as nx
import numpy as np

def calculate_group_centers(graph,df):
    # Get the connected components of the graph
    components = nx.connected_components(graph)

    # Calculate the center of each component
    centers = []
    count = 0
    for component in components:
         # If all robots in the component are faulty, skip this component
        if IS_FAULTY_COL in df.columns:
            if df.loc[df[ROBOT_ID_COL].isin(component), IS_FAULTY_COL].all():
                continue
        # Get the x, y coordinates of the robots in the component
        x_coords = [graph.nodes[robot_id][X_COL] for robot_id in component]
        y_coords = [graph.nodes[robot_id][Y_COL] for robot_id in component]

        # Calculate the centroid
        centroid = (np.mean(x_coords), np.mean(y_coords))

        # Get the count of elements in the group
        count = len(component)

        # Append the centroid and count to the centers list
        centers.append((centroid, count))
        count += 1

    return centers

def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def average_distance(centers):
    # Calculate the average distance between the centers
    if(len(centers) == 1):
        return 0
    distances = []
    for i in range(len(centers)):
        for j in range(i+1, len(centers)):
            distances.append(distance(centers[i][0], centers[j][0]))

    return np.mean(distances)


def get_groups_center_and_amount(G=None):
    idx = 0
    centers = []

    for graph, df in G:
        center = calculate_group_centers(graph,df)
        centers.append(center)
        idx += 1

    return centers


def get_distance_between_centers(df,G=None):
    centers = get_groups_center_and_amount(G)
    distances = [average_distance(center) for center in centers]
    return distances

