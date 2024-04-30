


import argparse
import glob
from debug.main import create_video, debug_code
from metrics.group_center import get_group_center, get_distance_between_centers
from visualization.main import plot_series
from metrics.order import get_order
from metrics.union import get_union
from consts import DB, RAW_DATA_FILE
from utils import read_csv


# Get args from the command line
parser = argparse.ArgumentParser(description="Run multiple experiments" )
# Add command-line arguments with default values
parser.add_argument("-p", "--path", type=str, default="", help="Template for experiments")
parser.add_argument("-d", "--debug", type=int, default=False, help="Template for experiments")


args = parser.parse_args()
experiment_path = args.path
debug = bool(args.debug)

idx = 0
for filename in glob.glob(DB + experiment_path + '/**/' + RAW_DATA_FILE, recursive=True):

    exp_data = read_csv(filename)
    # order = get_order(exp_data)
    union = get_union(exp_data)

    centers = get_group_center(exp_data)
    plot_series([union], f"debug_centers_{idx}")
    avg_distance = get_distance_between_centers(exp_data)
    plot_series([avg_distance], f"debug_avg_distance_{idx}")

    create_video(centers, -0.1, 0.1, -0.1, 0.1)

    if(debug):
        if 'order' not in locals():
            order = get_order(exp_data)
        if 'union' not in locals():
            union = get_union(exp_data)
        debug_code(debug, filename, order, union, idx)

    idx += 1

# for each file in the directory

# exp_data = read_csv(DB+experiment_path)

# print(exp_data.head())
# order = get_order(exp_data)
# print(order.head())

# graphs_by_timestep = exp_data.groupby('TimeStep').apply(get_union, include_groups=False)
# print(graphs_by_timestep)

# # Read data from parameters.csv
# exp_metrics = read_csv(DB+experiment_path)