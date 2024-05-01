from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

from utils import build_graph, data_cleaning

import networkx as nx
import numpy as np

def calculate_group_centers(graph):
    # Get the connected components of the graph
    components = nx.connected_components(graph)

    # Calculate the center of each component
    centers = []
    for component in components:
        # Get the x, y coordinates of the robots in the component
        x_coords = [graph.nodes[robot_id]['X'] for robot_id in component]
        y_coords = [graph.nodes[robot_id]['Y'] for robot_id in component]

        # Calculate the centroid
        centroid = (np.mean(x_coords), np.mean(y_coords))

        # Get the count of elements in the group
        count = len(component)

        # Append the centroid and count to the centers list
        centers.append((centroid, count))

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


def get_group_center(df,G=None):
    if G is None:
        G = df.groupby('TimeStep').apply(build_graph)
    centers = G.apply(lambda x: calculate_group_centers(x))
    print(centers.head())
    centers = data_cleaning(centers)


    return centers


def get_distance_between_centers(df,G=None):
    if G is None:
        G = df.groupby('TimeStep').apply(build_graph)
    centers = get_group_center(df,G)
    distances = centers.apply(average_distance)
    distances = data_cleaning(distances)

    return distances

