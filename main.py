import argparse
from datetime import datetime
import glob
import os
import time
import pandas as pd
from tqdm import tqdm
import networkx as nx
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import subprocess


from debug.main import create_video, debug_code
from metrics.group_center import get_groups_center_and_amount, get_distance_between_centers
from visualization.main import plot_series
from metrics.order import get_order
from metrics.union import get_union
from consts import DB, RAW_DATA_FILE
from utils import build_graph, build_graphs, read_csv



# Define a function to process a single file
def process_file(filename):
    exp_data = read_csv(filename)
    rows_per_timestep = int(filename.split('/')[-4])

    # Build graphs
    start_time = time.time()
    G = build_graphs(exp_data, rows_per_timestep)

    order = get_order(exp_data, rows_per_timestep) if order_in_metrics or debug else []
    union = get_union(exp_data, rows_per_timestep, G=G) if union_in_metrics or debug else []
    centers = get_groups_center_and_amount(G=G) if centers_in_metrics or debug else ([], [])
    avg_distance = get_distance_between_centers(exp_data, G=G) if avg_distance_in_metrics else []
    print(f"Time taken for {filename}: {time.time() - start_time} seconds")
    return order, union, centers, avg_distance


# Get args from the command line
parser = argparse.ArgumentParser(description="Run multiple experiments" )
# Add command-line arguments with default values
parser.add_argument("-i", "--input_path", type=str, default="", help="Template for experiments")
parser.add_argument("-d", "--debug", type=int, default=False, help="Template for experiments")
parser.add_argument("-m", "--metric", type=lambda s: s.split(','), default="order", help="order, union, centers, avg_distance")
parser.add_argument("-l", "--log", type=int, default=False, help="Log the output")
args = parser.parse_args()
experiment_path = args.input_path
debug = bool(args.debug)
log = bool(args.log)

idx = 0
orders_list,unions_list,centers_list,avg_distance_lists = [],[],[],[]
start_time = time.time()  # Start the timer


file_list = glob.glob(DB + experiment_path + '/**/' + RAW_DATA_FILE, recursive=True)
file_len = len(file_list)
print(f"Total files: {file_len}")

metrics = args.metric
order_in_metrics = 'order' in metrics
union_in_metrics = 'union' in metrics
centers_in_metrics = 'centers' in metrics
avg_distance_in_metrics = 'avg_distance' in metrics

num_processes = multiprocessing.cpu_count()
print(f"Number of processes: {num_processes}")
pool = multiprocessing.Pool(processes=num_processes)

results = pool.map(process_file, file_list)
orders_list, unions_list, centers_list, avg_distance_lists = zip(*results)

end_time = time.time()  # Stop the timer
if log:
    output_dir_name = DB + experiment_path +f"results/r45_d{datetime.now().strftime('%d%m%y_%H%M')}"
    os.makedirs(output_dir_name, exist_ok=True)
    data = {}
    if union_in_metrics:
        data['unions'] = [item for sublist in unions_list for item in sublist]
        plot_series([unions_list], output_dir_name+f'/Union',show_individual=False,error_type='se')

    if order_in_metrics:
        data['orders'] = [item for sublist in orders_list for item in sublist]
        plot_series([orders_list], output_dir_name+f'/Order',show_individual=False,error_type='se')

    if centers_in_metrics:
        data['centers'] = [item for sublist in centers_list for item in sublist]

    if avg_distance_in_metrics:
        data['avg_distance'] = [item for sublist in avg_distance_lists for item in sublist]
        plot_series([avg_distance_lists], output_dir_name+f'/Avg_distance',show_individual=False,error_type='se')
    save_df = pd.DataFrame(data)
    # Save the DataFrame to a CSV file
    save_df.to_csv(output_dir_name+f'/metrics_list.csv', index=False)

print(f"Running time: {end_time - start_time} seconds")

