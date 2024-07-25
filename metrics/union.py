import networkx as nx
from numpy import argmax
from consts import *
from utils import build_graph, get_coordinates, calculate_distance
import math
import numpy as np
from scipy.linalg import eigvals

# def laplacian_matrix(adj_matrix):
#     degree_matrix = np.diag(adj_matrix.sum(axis=1))
#     return degree_matrix - adj_matrix

# def count_connected_components(adj_matrix):
#     # Compute the Laplacian matrix
#     L = laplacian_matrix(adj_matrix)
    
#     # Compute the eigenvalues of the Laplacian matrix
#     eigenvalues = eigvals(L)
    
#     # Count the number of zero eigenvalues (considering a small threshold to handle numerical precision)
#     num_components = np.sum(np.isclose(eigenvalues, 0, atol=1e-10))
    
#     return num_components


def get_coordinates_dict(df):
    return {row[ROBOT_ID_COL]: (row[X_COL], row[Y_COL]) for _, row in df.iterrows()}

def calculate_distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx**2 + dy**2)

def calculate_distances(current_coords, prev_coords, component):
    distances = [
        calculate_distance(current_coords[robot_id][0], current_coords[robot_id][1],
                           prev_coords[robot_id][0], prev_coords[robot_id][1])
        for robot_id in component
    ]
    return sum(distances)



def count_components(G, current_timestep_df, prev_timestep_df,idx):
    """
    Counts the number of connected components in a graph and calculates the sizes and distances of each component.

    Parameters:
    - G (networkx.Graph): The graph representing the connections between nodes.
    - current_timestep_df (pandas.DataFrame): The DataFrame containing the current timestep data.
    - prev_timestep_df (pandas.DataFrame): The DataFrame containing the previous timestep data.

    Returns:
    - tuple: A tuple containing the count of components, sizes of each component, and distances of each component.

    """
    count = 0
    components_sizes, components_distances = [], []
    
    current_coords = get_coordinates_dict(current_timestep_df)
    prev_coords = get_coordinates_dict(prev_timestep_df) if prev_timestep_df is not None else None
    
    for component in nx.connected_components(G):
        count += 1
        component_size = len(component)
        components_sizes.append(component_size)
        
        if idx > 0:
            component_distance = calculate_distances(current_coords, prev_coords, component)
            components_distances.append(component_distance)
        else:
            components_distances.append(0)
    
    max_idx = np.argmax(components_sizes)
    
    #Now returns only the biggest swarm component. If needed, we can return all components.
    # This will require to uncomment the code in the main.py file, under     if union_in_metrics:
    return (count, components_sizes[max_idx], components_distances[max_idx])

def worker(graph_df_tuple, prev_graph_df_tuple,idx):    
    graph, df_subset = graph_df_tuple
    # If it is the first timstep, handle set prev to None.
    prev_graph, prev_df_subset = prev_graph_df_tuple if prev_graph_df_tuple else (None, None)
    return count_components(graph, df_subset, prev_df_subset,idx)

def get_union( G=None):
    unions = [worker(g, G[i-1] if i > 0 else None,i) for i, g in enumerate(G)]    
    return unions