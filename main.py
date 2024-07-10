import argparse
from datetime import datetime
import glob
import os
import subprocess
import time
from numpy import argmax
import pandas as pd
import multiprocessing

from metrics.speed import get_speed
from metrics.group_center import get_groups_center_and_amount, get_distance_between_centers
from visualization.main import plot_series, plot_multi_lines
from metrics.order import get_order
from metrics.union import get_union
from consts import DB, RAW_DATA_FILE
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
    filename, metrics,robot_count = args

    exp_data = utils.read_csv(filename)
    # rows_per_timestep = int(filename.split('/')[-4])
    rows_per_timestep = robot_count
    order_in_metrics, union_in_metrics, centers_in_metrics, avg_distance_in_metrics, speed_in_metrics = get_metrics(metrics)
    # print(f"outputing order: {order_in_metrics} | union: {union_in_metrics} | distance: {avg_distance_in_metrics} | speed: {speed_in_metrics}" )
    # Build graphs
    # start_time = time.time()
    G = utils.build_graphs(exp_data, rows_per_timestep)

    order = get_order(exp_data, rows_per_timestep) if order_in_metrics else []
    union = get_union(exp_data, rows_per_timestep, G=G) if union_in_metrics else []
    centers = get_groups_center_and_amount(G=G) if centers_in_metrics else ([], [])
    avg_distance = get_distance_between_centers(exp_data, G=G) if avg_distance_in_metrics else []
    avg_speed = get_speed(exp_data) if speed_in_metrics else []
    # print(f"Time taken for {filename}: {time.time() - start_time} seconds")
    return order, union, centers, avg_distance,avg_speed



def save_logs(experiment_path,results ,metrics):
    orders_list, unions_list, centers_list, avg_distance_lists,speeds_list = zip(*results)
    order_in_metrics, union_in_metrics, centers_in_metrics, avg_distance_in_metrics, speed_in_metrics = get_metrics(metrics)
    # Get the length of the first tuple


    output_dir_name = DB + experiment_path +f"/results/d{datetime.now().strftime('%d%m%y_%H%M')}"
    os.makedirs(output_dir_name, exist_ok=True)
    data = {}
    
    

    if union_in_metrics:
        data['unions'] = [item[0] for sublist in unions_list for item in sublist]
        components_list, components_size_list, components_passed_distance_list = [], [], []
        for unions in unions_list:
            components, components_size, components_passed_distance = zip(*unions)
            components_list.append(pd.Series(components))
            components_size_list.append(pd.Series(components_size))
            components_passed_distance_list.append(pd.Series(components_passed_distance))
            

        
        plot_series([components_list],labels=["Avg. union"], filename=output_dir_name+f'/Union',show_individual=False,error_type='se')
        print(components_list)
        plot_series([components_passed_distance_list],labels=["Avg. reward"], filename=output_dir_name+f'/reward',show_individual=False,error_type='se')
        
        # components, components_size, components_passed_distance= zip(*unions_list[0])
        # max_passed_distances = [max(t) for t in components_passed_distance]
        # components = [tuple([pd.Series(components)])]
        # max_passed_distances = [tuple([pd.Series(max_passed_distances)])]
        # plot_series(components,labels=["Avg. union"], filename=output_dir_name+f'/Union',show_individual=False,error_type='se')
        # plot_multi_lines(components_passed_distance,filename=output_dir_name+f'/Swarm_reward')

    if order_in_metrics:
        data['orders'] = [item for sublist in orders_list for item in sublist]
        plot_series([orders_list],labels=["Avg. order"], filename=output_dir_name+f'/Order',show_individual=False,error_type='se',fix_y_axis=True)

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

    # Get args from the command line
    parser = argparse.ArgumentParser(description="Run multiple experiments" )

    parser.add_argument("-i", "--input_path", type=str, default="", help="Template for experiments")
    parser.add_argument("-d", "--debug", type=int, default=False, help="Template for experiments")
    parser.add_argument("-m", "--metric", type=lambda s: s.split(','), default="all", help="all or any of: order, union, centers, avg_distance, speed")
    parser.add_argument("-l", "--log", type=int, default=True, help="Log the output")
    parser.add_argument("-rc", "--robot_count", type=int, default=40, help="The count of robots in the swarm.")
    args = parser.parse_args()
    experiment_path = args.input_path
    debug = bool(args.debug)
    log = bool(args.log)
    metrics = args.metric
    robot_count = args.robot_count

    # Get all the files in the experiment path
    file_list = glob.glob(DB + experiment_path + '/**/' + RAW_DATA_FILE, recursive=True)
    file_len = len(file_list)
    print(f"Total files: {file_len}")

    num_processes = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_processes)
    print(f"Number of processes: {num_processes}")

    file_list_with_metrics = [(file, metrics,robot_count) for file in file_list]
    results = pool.map(process_file, file_list_with_metrics)

    if log:
        save_logs(experiment_path,results, metrics)
        
    end_time = time.time()  # Stop the timer
    print(f"Running time: {end_time - start_time} seconds")
 
    send_notification('Metric anlysis completed', f'Data is ready at {experiment_path}results/.')


def send_notification(title, message):
    subprocess.run(['notify-send', title, message])
    
    
if __name__ == "__main__":
    main()
