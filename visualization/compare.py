# get dir of two files create from them DF and compare them

import argparse
import json
import os
import pandas as pd
import numpy as np

from main import plot_series

SAVE_GRAPH = "./visualization/graphs/"
READ_DATA = "./visualization/compare_lists/"
DATA_FILE_TYPE = ".txt"
# Get args from the command line
parser = argparse.ArgumentParser(description="Run multiple experiments" )
# Add command-line arguments with default values
parser.add_argument("-i", "--file_paths", type=str, required=True, help="File containing the paths to the files to process")
parser.add_argument("-el", "--experiment_length", type=int, default=5000, help="Length of each experiment")

args = parser.parse_args()
data_file_name = args.file_paths
experiment_length = args.experiment_length

# Define a function to process each file
def process_file(file_path):
    df = pd.read_csv(file_path)[["orders"]]
    print(df.shape)
    df['group'] = df.index // experiment_length
    dfs = [group["orders"].values for _, group in df.groupby('group')]
    print(len(dfs))
    return dfs

# Define the base file path and file names
dir_path = "../data/DB/"
file_name = 'metrics_list.csv'

complete_path = READ_DATA + data_file_name + DATA_FILE_TYPE
with open(complete_path, 'r') as f:
    file_paths, labels = zip(*[line.strip().split(maxsplit=1) for line in f if not line.strip().startswith('#')])

# Process each file and store the results in a list
dfs = [process_file(dir_path + file_path + file_name) for file_path in file_paths]

# labels = ["Naive","P&G w. early stoppage","P&G w. early stoppage 100%","P&G no early stoppage","Force","Fast"]

plot_filename = f"{SAVE_GRAPH}{data_file_name}"
plot_series(dfs,filename=plot_filename, labels=labels, avg=True, show_individual=False, error_type='se', to_pdf=False, fix_y_axis=True)

metadata = {'file_paths': file_paths}
with open(f'{plot_filename}_metadata.json', 'w') as f:
    json.dump(metadata, f)