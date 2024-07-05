import networkx as nx
from consts import *
from utils import build_graph, get_coordinates, calculate_distance
import math


def count_components(G, current_timestep_df,prev_timestep_df):
    count = 0
    components_sizes, components_distances = [],[]
    # if(nx.is_connected(G)):
    #     return 1
    for component in nx.connected_components(G):
        component_distance = 0
        count += 1
        if prev_timestep_df is not None:
            for robot_id in component:
                current_x, current_y = get_coordinates(current_timestep_df,robot_id)
                prev_x, prev_y = get_coordinates(prev_timestep_df,robot_id)
                component_distance += calculate_distance(current_x,current_y,prev_x,prev_y)
        components_distances.append(component_distance)
        components_sizes.append(len(component))        

        # Count the component only if not all of its members are faulty
        #  for robot_id in component:
        #     if not df.loc[current_timestep_df[ROBOT_ID_COL] == robot_id, IS_FAULTY_COL].item():
        #         count += 1
        #         break

    return (count, components_sizes, components_distances)

def worker(graph_df_tuple, prev_graph_df_tuple):    
    graph, df_subset = graph_df_tuple
    prev_graph, prev_df_subset = prev_graph_df_tuple if prev_graph_df_tuple else (None, None)
    
    return count_components(graph, df_subset, prev_df_subset)

def get_union(df, num_rows_per_timestep, G=None):

    # Create a multiprocessing Pool
    # with mp.Pool(mp.cpu_count()) as pool:
    #     # Use the pool.map function to parallelize the computation
    #     unions = pool.map(worker, G)
    # unions = [worker(g) for g in G]
    unions = [worker(g, G[i-1] if i > 0 else None) for i, g in enumerate(G)]
    return unions