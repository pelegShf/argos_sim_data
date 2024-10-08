import argparse
from datetime import datetime
import glob
import subprocess
import time
from consts import *
import utils
from visualization.main import plot_series, plot_multi_lines


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
    parser = argparse.ArgumentParser(description="Run multiple experiments")

    parser.add_argument(
        "-fp", "--input_path", type=str, default=default_path, help="Dir of file."
    )
    parser.add_argument(
        "-i", "--file_name", type=str, default=time_path, help="File name"
    )

    parser.add_argument(
        "-d", "--debug", type=int, default=False, help="Template for experiments"
    )
    parser.add_argument(
        "-m",
        "--metric",
        type=lambda s: s.split(","),
        default="all",
        help="all or any of: order, union, centers, avg_distance, speed",
    )
    parser.add_argument("-l", "--log", type=int, default=True, help="Log the output")
    parser.add_argument(
        "-rc",
        "--robot_count",
        type=int,
        default=40,
        help="The count of robots in the swarm.",
    )
    args = parser.parse_args()
    experiment_path = args.input_path
    file_name = args.file_name
    log = bool(args.log)
    metrics = args.metric
    robot_count = args.robot_count

    # Get all the files in the experiment path
    swarm_data_file_list = glob.glob(
        DB + experiment_path + file_name + "/**/" + SWARM_DATA_FILE, recursive=True
    )
    file_len = len(swarm_data_file_list)
    if file_len == 0:
        print("[ERROR] No data found.")
        return

    # for each file generate the plots
    order_list = []
    reward_list = []
    avg_reward_list = []
    for i, swarm_data_file in enumerate(swarm_data_file_list):
        # csv to dataframe
        swarm_data = utils.read_csv(swarm_data_file)
        order_col = swarm_data[ORDER_COL]
        reward_col = swarm_data[REWARD_COL]
        avg_reward_col = swarm_data[AVG_REWARD_COL]
        order_list.append(order_col)
        reward_list.append(reward_col)
        avg_reward_list.append(avg_reward_col)
    if (len(order_list) == 0):
        print("[ERROR] No data found.")
        return
    print(len(order_list))
    # plot order
    plot_series(
        [order_list],
        labels=["Order"],
        filename=f"{DB}{experiment_path}{file_name}/order",
        show_individual=False,
        error_type="se",
        fix_y_axis=1,
    )

    # plot reward
    plot_series(
        [reward_list],
        labels=["Reward"],
        filename=f"{DB}{experiment_path}{file_name}/reward",
        show_individual=False,
        error_type="se",
        fix_y_axis=0,
    )

        # plot reward
    plot_series(
        [avg_reward_list],
        labels=["Average Reward"],
        filename=f"{DB}{experiment_path}{file_name}/avg_reward",
        show_individual=False,
        error_type="se",
        fix_y_axis=0,
    )

    end_time = time.time()  # Stop the timer
    print(f"Running time: {end_time - start_time} seconds")

    send_notification(
        "Metric anlysis completed", f"Data is ready at {experiment_path}results/."
    )


def send_notification(title, message):
    subprocess.run(["notify-send", title, message])


if __name__ == "__main__":
    main()
