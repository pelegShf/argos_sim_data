


import argparse
import glob
import time

import pandas as pd
from debug.main import create_video, debug_code
from metrics.group_center import get_group_center, get_distance_between_centers
from visualization.main import plot_series
from metrics.order import get_order
from metrics.union import get_union
from consts import DB, RAW_DATA_FILE
from utils import data_cleaning, read_csv


# Get args from the command line
parser = argparse.ArgumentParser(description="Run multiple experiments" )
# Add command-line arguments with default values
parser.add_argument("-p", "--path", type=str, default="", help="Template for experiments")
parser.add_argument("-d", "--debug", type=int, default=False, help="Template for experiments")


args = parser.parse_args()
experiment_path = args.path
debug = bool(args.debug)

idx = 0
unions_list = []
file_len = len(glob.glob(DB + experiment_path + '/**/' + RAW_DATA_FILE, recursive=True))
start_time = time.time()  # Start the timer
for filename in glob.glob(DB + experiment_path + '/**/' + RAW_DATA_FILE, recursive=True):

    exp_data = read_csv(filename)
    # order = get_order(exp_data)
    union = get_union(exp_data,40)
    unions_list.append(union)
    # centers = get_group_center(exp_data)
    # avg_distance = get_distance_between_centers(exp_data)


    if(debug):
        if 'order' not in locals():
            order = get_order(exp_data)
        if 'union' not in locals():
            union = get_union(exp_data)
        if 'centers' not in locals():
            centers = get_group_center(exp_data)
        debug_code(debug, filename, order, union, idx)
        create_video(centers)
    print(f"Finished {idx}/{file_len} - {filename}")
    idx += 1

end_time = time.time()  # Stop the timer

# save to file
tst = pd.DataFrame(unions_list).T
tst = data_cleaning(tst)

# Save the DataFrame to a CSV file
tst.to_csv(f'unions_list_{end_time}.csv', index=False)

# plot_series(unions_list, 'Union')

# To print later
# test = pd.read_csv('unions_list.csv')
plot_series(unions_list, f'Union_{end_time}')
print(f"Running time: {end_time - start_time} seconds")