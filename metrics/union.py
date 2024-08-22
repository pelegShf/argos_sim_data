import networkx as nx
from numpy import argmax
from metrics.utils import degrees_to_vector, is_angle_greater_than_90
from consts import *
import math
import numpy as np
from scipy.linalg import eigvals



def get_coordinates_dict(df):
    return {row[ROBOT_ID_COL]: (row[X_COL], row[Y_COL],row[HEADING_COL]) for _, row in df.iterrows()}

def calculate_distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx**2 + dy**2)

def calculate_distances(current_coords, prev_coords, component):
    distances = [
        calculate_distance_in_forward_direction(current_coords[robot_id][0], current_coords[robot_id][1],
                           prev_coords[robot_id][0], prev_coords[robot_id][1],prev_coords[robot_id][2])
        for robot_id in component
    ]
    return sum(distances)





def calculate_distance_in_forward_direction(x1, y1, x2, y2, direction_degrees):
    """
    Positive distance is if the bearing between the two points is between [pi/2,-pi/2]
    Negative distance is if the bearing between the two points is between [pi,-pi/2] or [pi/2,-pi]
    """
    
    if(x1 == x2 and y1 == y2):
        return 0
    
    x = x1 - x2
    y= y1 - y2
    x_dir, y_dir = degrees_to_vector(direction_degrees)
    dist = calculate_distance(x1, y1, x2, y2)
    if is_angle_greater_than_90(x_dir, y_dir, x, y):
        dist = -dist
    # print(f"Distance: {dist}")
    return dist
    
    
    

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




