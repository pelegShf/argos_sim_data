import networkx as nx
from numpy import argmax
from consts import *
from utils import build_graph, get_coordinates, calculate_distance
import math


def count_components(G, current_timestep_df, prev_timestep_df):
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
    
    for component in nx.connected_components(G):
        component_distance = 0
        count += 1
        if prev_timestep_df is not None:
            for robot_id in component:
                current_x, current_y = get_coordinates(current_timestep_df, robot_id)
                prev_x, prev_y = get_coordinates(prev_timestep_df, robot_id)
                component_distance += calculate_distance(current_x, current_y, prev_x, prev_y)
        components_distances.append(component_distance)
        components_sizes.append(len(component))        
    max_idx = argmax(components_sizes)
    
    #Now returns only the biggest swarm component. If needed, we can return all components.
    # This will require to uncomment the code in the main.py file, under     if union_in_metrics:
    return (count, components_sizes[max_idx], components_distances[max_idx])

def worker(graph_df_tuple, prev_graph_df_tuple):    
    graph, df_subset = graph_df_tuple
    # If it is the first timstep, handle set prev to None.
    prev_graph, prev_df_subset = prev_graph_df_tuple if prev_graph_df_tuple else (None, None)
    return count_components(graph, df_subset, prev_df_subset)

def get_union(df, num_rows_per_timestep, G=None):
    unions = [worker(g, G[i-1] if i > 0 else None) for i, g in enumerate(G)]
    return unions