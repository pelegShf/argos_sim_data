# get dir of two files create from them DF and compare them

import argparse
import os
import pandas as pd
import numpy as np

from main import plot_series



# Get args from the command line
parser = argparse.ArgumentParser(description="Run multiple experiments" )
# Add command-line arguments with default values
parser.add_argument("-f1", "--first_file", type=str, default="", help="First file to compare")
parser.add_argument("-f2", "--second_file", type=str, default=False, help="Second file to compare")

args = parser.parse_args()
# Define a function to process each file
def process_file(file_path):
    df = pd.read_csv(file_path)[["orders"]]
    print(df.shape)
    df['group'] = df.index // 6000
    dfs = [group["orders"].values for _, group in df.groupby('group')]
    print(len(dfs))
    return dfs

# Define the base file path and file names
dir_path = "../data/DB/"
file_name = 'metrics_list.csv'
file_paths = [
    "05052024_2137/avoidAttract/results/r45_d050524_2146/",
    "05052024_2151/avoidAttract/results/r45_d050524_2154/",
    "05052024_2232/avoidAttract/results/r45_d050524_2236/",
    "05052024_2242/avoidAttract/results/r45_d050524_2246/",
    "05052024_2256/avoidAttract/results/r45_d050524_2258/"
]

# Process each file and store the results in a list
dfs = [process_file(dir_path + file_path + file_name) for file_path in file_paths]

labels = ["Naive","P&G w. early stoppage","P&G w. early stoppage 100%","P&G no early stoppage","Force"]


plot_series(dfs, labels=labels, avg=True, show_individual=False, error_type='se', to_pdf=True)