import os
import pandas as pd
import numpy as np
import networkx as nx
import math
from multiprocessing.shared_memory import SharedMemory

from visualization.main import plot_series
from consts import *
import csv


def read_csv(file_path):
    return pd.read_csv(file_path)

def read_custom_csv(file_path, num_columns=40):
    dataframes = []
    
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Split the single cell by spaces to get the list of numbers
            numbers = list(map(int, row[0].split()))
            
            # Ensure the numbers list is divisible by the number of columns
            if len(numbers) % num_columns != 0:
                print("Error: The number of elements is not divisible by the number of columns.")
                return []
            
            # Reshape the list into the required DataFrame format
            reshaped_data = [numbers[i:i + num_columns] for i in range(0, len(numbers), num_columns)]
            df = pd.DataFrame(reshaped_data)
            
            # Append the DataFrame to the list
            dataframes.append(df)
    
    return dataframes


def build_graph(df):
    G = nx.Graph()

 # Add nodes with attributes
    # df.apply(lambda row: G.add_node(row[ROBOT_ID_COL], 
    #                                  X=row[X_COL], 
    #                                  Y=row[Y_COL], 
    #                                  heading=row[HEADING_COL], 
    #                                  is_faulty=row[IS_FAULTY_COL]), axis=1)
    df.apply(lambda row: G.add_node(row[ROBOT_ID_COL], 
                                     X=row[X_COL], 
                                     Y=row[Y_COL], 
                                     heading=row[HEADING_COL]), axis=1)
    # Add edges
    edges = df.assign(neighbors=df[NEIGHBORS_COL].str.split()).explode('neighbors')
    G.add_edges_from(edges[[ROBOT_ID_COL, 'neighbors']].values)

    return G

def build_graphs(df, num_rows_per_timestep):
    # df = data_cleaning(df)

    G = []
    for i in range(0, len(df), num_rows_per_timestep):
        df_subset = df[i:i+num_rows_per_timestep]
        G.append((build_graph(df_subset), df_subset))
    return G
 
 
def get_coordinates(df, robot_id):
    row = df[(df[ROBOT_ID_COL] == robot_id)]
    x = row[X_COL].values[0]
    y = row[Y_COL].values[0]
    return x, y
        
def calculate_distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    distance = math.sqrt(dx**2 + dy**2)
    return distance