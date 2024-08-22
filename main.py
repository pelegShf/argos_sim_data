import argparse
from datetime import datetime
import glob
import math
import os
import subprocess
import time
import unittest
from numpy import argmax
import pandas as pd
import multiprocessing
import matplotlib.pyplot as plt
import numpy as np
from metrics.speed import get_speed
from metrics.group_center import get_groups_center_and_amount, get_distance_between_centers
from visualization.main import plot_series, plot_multi_lines
from metrics.order import get_order
from metrics.union import get_union
from consts import DB, RAW_DATA_FILE, NEIGHBORS_FILE
import utils





def get_metrics(metrics):
    all_in_metrics = 'all' in metrics
    if all_in_metrics:
        return True, True, True, True, True
    order_in_metrics = 'order' in metrics
    union_in_metrics = 'union' in metrics
    centers_in_metrics = 'centers' in metrics
    avg_distance_in_metrics = 'avg_distance' in metrics
    speed_in_metrics = 'speed' in metrics
    return order_in_metrics, union_in_metrics, centers_in_metrics, avg_distance_in_metrics, speed_in_metrics

# Define a function to process a single file
def process_file(args):
    raw_data_filename, metrics,robot_count = args

    exp_data = utils.read_csv(raw_data_filename)

    # rows_per_timestep = int(filename.split('/')[-4])
    rows_per_timestep = robot_count
    order_in_metrics, union_in_metrics, centers_in_metrics, avg_distance_in_metrics, speed_in_metrics = get_metrics(metrics)
    # print(f"outputing order: {order_in_metrics} | union: {union_in_metrics} | distance: {avg_distance_in_metrics} | speed: {speed_in_metrics}" )
    # Build graphs
    G = utils.build_graphs(exp_data, rows_per_timestep) # Around 17 seconds
    order = get_order(exp_data, rows_per_timestep) if order_in_metrics else [] # Around 1 second
    union = get_union(G=G) if union_in_metrics else [] # Around 17 second
    centers = get_groups_center_and_amount(G=G) if centers_in_metrics else ([], [])
    avg_distance = get_distance_between_centers(exp_data, G=G) if avg_distance_in_metrics else []
    avg_speed = get_speed(exp_data) if speed_in_metrics else []
    # print(f"Time taken for {filename}: {time.time() - start_time} seconds")
    return order, union, centers, avg_distance,avg_speed

def infinite_horizon_rewards(rewards):
    # Compute the cumulative sum of the rewards array
    cumulative_sum = np.cumsum(rewards)
    
    # Compute the infinite horizon rewards
    infinite_horizon = cumulative_sum / np.arange(1, len(rewards) + 1)
    
    return infinite_horizon

def save_logs(experiment_path,results ,metrics):
    orders_list, unions_list, centers_list, avg_distance_lists,speeds_list = zip(*results)
    order_in_metrics, union_in_metrics, centers_in_metrics, avg_distance_in_metrics, speed_in_metrics = get_metrics(metrics)
    # Get the length of the first tuple


    output_dir_name = DB + experiment_path +f"/results/d{datetime.now().strftime('%d%m%y_%H%M')}"
    os.makedirs(output_dir_name, exist_ok=True)
    data = {}
    
    

    if union_in_metrics:
        data['unions'] = [item[0] for sublist in unions_list for item in sublist]
        components_list, components_size_list, components_passed_distance_list, infinite_horizon_rewards_list = [], [], [],[]
        for unions in unions_list:
            components, components_size, components_passed_distance = zip(*unions)
            components_list.append(pd.Series(components))
            components_size_list.append(pd.Series(components_size))
            components_passed_distance_list.append(pd.Series(components_passed_distance))
            infinite_horizon_rewards_list.append(pd.Series(infinite_horizon_rewards(components_passed_distance)))
        data['swarm_reward'] = [item for sublist in components_passed_distance_list for item in sublist]

        plot_series([components_list],labels=["Avg. union"], filename=output_dir_name+f'/Union',show_individual=False,error_type='se')
        plot_series([components_passed_distance_list],labels=["Avg. reward"], filename=output_dir_name+f'/reward',show_individual=False,error_type='se',fix_y_axis=(-0.08,0.08))
        plot_series([infinite_horizon_rewards_list],labels=["Infinite horizon avg. reward"], filename=output_dir_name+f'/infinte_horizon_reward',show_individual=False,error_type='se',fix_y_axis=(-0.08,0.08))


    if order_in_metrics:
        data['orders'] = [item for sublist in orders_list for item in sublist]
        plot_series([orders_list],labels=["Avg. order"], filename=output_dir_name+f'/Order',show_individual=False,error_type='se',fix_y_axis=1)

    if centers_in_metrics:
        data['centers'] = [item for sublist in centers_list for item in sublist]

    if avg_distance_in_metrics:
        data['avg_distance'] = [item for sublist in avg_distance_lists for item in sublist]
        plot_series([avg_distance_lists],labels=["Avg. distance between groups"], filename=output_dir_name+f'/Avg_distance',show_individual=False,error_type='se')
        
    if speed_in_metrics:
        data['speed'] = [item for sublist in speeds_list for item in sublist]
        plot_series([speeds_list],labels=["Avg. speed"], filename=output_dir_name+f'/Speed',show_individual=False,error_type='se')
        
    save_df = pd.DataFrame(data)
    # Save the DataFrame to a CSV file
    save_df.to_csv(output_dir_name+f'/metrics_list.csv', index=False)
 
def sanity_checks(raw_data_file_list, neighbors_file_list):
    assert len(raw_data_file_list) > 0, "No files found"
    assert len(neighbors_file_list) > 0, "No neighbors files found"
    assert len(raw_data_file_list) == len(neighbors_file_list), "Number of raw data files and neighbors files do not match"
    
def main(): 
    """
    Run multiple experiments based on command line arguments.

    Args:
        -i, --input_path (str): Template for experiments.
        -d, --debug (int): Debug mode flag.
        -m, --metric (list): List of metrics to calculate.
        -l, --log (int): Log the output flag.

    Returns:
        None
    """
    start_time = time.time()  # Start the timer
    # Get the current date and time
    now = datetime.now()

    # Format it to match your folder structure
    default_path = now.strftime("%Y_%m/%d%m%Y/")
    time_path = now.strftime("%H%M")

    # Get args from the command line
    parser = argparse.ArgumentParser(description="Run multiple experiments" )

    parser.add_argument("-fp", "--input_path", type=str, default=default_path, help="Dir of file.")
    parser.add_argument("-i", "--file_name", type=str, default=time_path, help="File name")
    
    
    parser.add_argument("-d", "--debug", type=int, default=False, help="Template for experiments")
    parser.add_argument("-m", "--metric", type=lambda s: s.split(','), default="all", help="all or any of: order, union, centers, avg_distance, speed")
    parser.add_argument("-l", "--log", type=int, default=True, help="Log the output")
    parser.add_argument("-rc", "--robot_count", type=int, default=40, help="The count of robots in the swarm.")
    args = parser.parse_args()
    experiment_path = args.input_path
    file_name = args.file_name
    debug = bool(args.debug)
    log = bool(args.log)
    metrics = args.metric
    robot_count = args.robot_count

    # Get all the files in the experiment path
    raw_data_file_list = glob.glob(DB + experiment_path + file_name+'/**/' + RAW_DATA_FILE, recursive=True)
    print(DB + experiment_path + file_name+'/**/' + RAW_DATA_FILE)
    file_len = len(raw_data_file_list)
    print(f"Total files: {file_len}")

    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=(num_processes-4))
    print(f"Number of processes: {num_processes} running on {num_processes-4} cores")

    files_list_with_metrics = [(raw_data_file, metrics,robot_count) for raw_data_file in raw_data_file_list]
    results = pool.map(process_file, files_list_with_metrics)

    if log:
        save_logs(f"{experiment_path}/{file_name}",results, metrics)
        
    end_time = time.time()  # Stop the timer
    print(f"Running time: {end_time - start_time} seconds")
 
    send_notification('Metric anlysis completed', f'Data is ready at {experiment_path}results/.')


def send_notification(title, message):
    subprocess.run(['notify-send', title, message])
    



if __name__ == "__main__":
    main()
