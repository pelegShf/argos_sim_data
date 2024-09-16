import argparse
import numpy as np
import pandas as pd
import networkx as nx
import cudf
import cugraph
import matplotlib.pyplot as plt
from datetime import datetime
from colorama import Fore, Style, init
import concurrent.futures

DB = "../data/DB/"
RAW_DATA_FILE = "raw_data/raw_data_1"
CSV = ".csv"

DB = "../data/DB/"
METRICS_FILE = "order_params_*.csv"
NEIGHBORS_FILE = "neighbor_matrix_*.csv"
MATH_THRESHOLD = 0.01
DEBUG_FOLDER = "./debug/"
PRECISION = 4

# DF columns
X_COL = "X"
Y_COL = "Y"
HEADING_COL = "Heading"
SPEED_COL = "Speed"
STATE_COL = "State"
IS_FAULTY_COL = "IsFaulty"
ROBOT_ID_COL = "RobotID"
NEIGHBORS_COL = "Neighbors"
TIMESTEP_COL = "TimeStep"

# Visualization
ALPHA = 0.3

NAME = ""

def get_cmd_args():
    parser = argparse.ArgumentParser(
        description='Analyze the results of a single experiment')

    # Add the arguments
    parser.add_argument('-i', type=str, help='The name of the data file')
    parser.add_argument('-m', type=str, help='Year of experiment')
    parser.add_argument('-y', type=str, help='Month of experiment')
    parser.add_argument('-d', type=str, help='Date of experiment')
    parser.add_argument('-t', type=str, help='Time of experiment')
    parser.add_argument('--model', type=str,default="mixGroupLearning", help='Model type')
    parser.add_argument('--size', type=str,default="25", help='Size of swarm')
    parser.add_argument('--set', type=str,default="0", help='Parameter set')
    parser.add_argument('--verbose', type=int, help='Verbose mode')

    # Parse the arguments
    args = parser.parse_args()

    # If -m, -y, -d, -t are not provided, use the current date
    now = datetime.now()

    if not args.m:
        args.m = f"{now.month:02d}"
        print(Fore.CYAN + "[Note] Month not provided, using current month: " +
              f"{args.m}" + Style.RESET_ALL)
    if not args.y:
        args.y = f"{now.year}"
        print(Fore.CYAN + "[Note] Year not provided, using current year: " +
              f"{args.y}" + Style.RESET_ALL)
    if not args.d:
        args.d = f"{now.day:02d}"
        print(Fore.CYAN + "[Note] Date not provided, using current date: " +
              f"{args.d}" + Style.RESET_ALL)
    if not args.t:
        args.t = now.strftime("%H:%M:%S")
        print(Fore.CYAN + "[Note] Time not provided, using current time: " +
              f"{args.t}" + Style.RESET_ALL)

    return args


def load_data(data_file,gpu=False):
    try:
        raw_data_file = f"{DB}{data_file}{RAW_DATA_FILE}{CSV}"
        print(Fore.CYAN +
              f"[INFO] Loading data from {raw_data_file}" + Style.RESET_ALL)
        if(gpu):
            raw_data_df = cudf.read_csv(raw_data_file)
        else:
            raw_data_df = pd.read_csv(raw_data_file)
    except pd.errors.EmptyDataError:
        print(Fore.RED + f"File {raw_data_file} is empty" + Style.RESET_ALL)
        return None
    except FileNotFoundError:
        print(Fore.RED + f"File {raw_data_file} not found" + Style.RESET_ALL)
        return None
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)
        return None
    return raw_data_df


def _build_data_file_name(args):
    return f"{args.y}_{args.m}/{args.d}{args.m}{args.y}/{args.t}/{args.model}/{args.size}/hyperparameter_set_{args.set}/X_RAY/logs/"


def _calc_time_diff(start_time):
    finish_time = datetime.now()
    elapsed_time = finish_time - start_time
    minutes, seconds = divmod(elapsed_time.total_seconds(), 60)
    return minutes, seconds

##################################
###### Data Preprocessing ########
##################################

def split_df_by_timestep(df):
    # Get the unique timesteps
    timesteps = df[TIMESTEP_COL].unique()

    # Split the dataframe by timestep
    return [df[df[TIMESTEP_COL] == timestep] for timestep in timesteps]

def calc_order_params(df):
    N = len(df)

    # Convert to radians and normalize
    thetha_i = np.radians(df[HEADING_COL] % 360)

    # Create a unit vector at the angle thetha_i
    currentHeadingVec = np.column_stack((np.cos(thetha_i), np.sin(thetha_i)))

    # Only consider rows where 'IsFaulty' is False if the column exists
    if(IS_FAULTY_COL in df.columns):
        print(df[IS_FAULTY_COL])
        currentHeadingVec = currentHeadingVec[df[IS_FAULTY_COL] == False]
    # Calculate the sum
    sum = currentHeadingVec.sum(axis=0)

    # Normalize the sum
    if IS_FAULTY_COL in df.columns:
        sum /= (N - df[IS_FAULTY_COL].sum())
    else:
        sum /= N

    # Calculate the order
    order = np.linalg.norm(sum)

    return order

##################################
###### Order and Union ###########
##################################





def build_graph(df):
    G = nx.from_pandas_edgelist(df.assign(neighbors=df[NEIGHBORS_COL].str.split()).explode('neighbors'),
                                source=ROBOT_ID_COL, target='neighbors')

    # Set node attributes
    node_attributes = df.set_index(ROBOT_ID_COL)[[X_COL, Y_COL, HEADING_COL]].to_dict('index')
    nx.set_node_attributes(G, node_attributes)

    return G

    


def calc_order_all_experiment(dfs_by_timestep):
    order = []
    for i in range(len(dfs_by_timestep)):
        order_i = calc_order_params(dfs_by_timestep[i])
        order.append(order_i)
    return order

def calc_union(df):
    G = build_graph(df)
    return nx.number_connected_components(G)

def calc_union_all_experiment(dfs_by_timestep):
    union = []
    for i in range(len(dfs_by_timestep)):
        union_i = calc_union(dfs_by_timestep[i])
        union.append(union_i)
    return union

def process_per_timestep(cudf_df, timestep_col=TIMESTEP_COL):
    results = []

    # Step 1: Group by TIMESTEP_COL
    grouped = cudf_df.groupby(timestep_col)
    
    # Step 2: Process each group (batch) separately
    for timestep, group in grouped:
        # Example metrics
        num_robots = len(group)
        avg_speed = group['Speed'].mean()
        summary_stats = group[['X', 'Y', 'Heading', 'Speed']].describe()
        
        # Collect the results
        results.append({
            'TimeStep': timestep,
            'NumRobots': num_robots,
            'AvgSpeed': avg_speed,
            'SummaryStats': summary_stats.to_pandas()  # Convert to pandas DataFrame for easier handling
        })
    
    # Convert results to a DataFrame if needed
    results_df = cudf.DataFrame(results)
    
    return results_df

def cuGraph_build(fname):
    edge_df = cudf.read_csv(fname, names=['source', 'destination'], header=None)
    # Step 2: Create a cuGraph Graph from the edge DataFrame
    G = cugraph.Graph()
    G.from_cudf_edgelist(edge_df, source='source', destination='destination')
    return G

def cuGraph_connected_components(G):
      # Step 3: Compute the connected components
    connected_components = cugraph.connected_components(G)
    # For example, count the number of unique connected components
    num_components = connected_components['labels'].nunique()
    return num_components


def process_graph(i):
    """Process a single graph file."""
    file_path = f"{DB}{_build_data_file_name(args)}graph + {i}.csv"
    G = cuGraph_build(file_path)
    return cuGraph_connected_components(G)
##################################
########### Data Plot ############
##################################

def plot(lst):
     plt.plot(lst)
     plt.show()
    



def main():
    # Load the data
    args = get_cmd_args()
    # construct the data file name
    data_file = _build_data_file_name(args)
    start_time = datetime.now()
    
    ###### Load the data ######
    data = load_data(data_file)
    if args.verbose:
        minutes, seconds = _calc_time_diff(start_time)
        print(Fore.MAGENTA + f"[VERBOSE] Data loaded successfully in {int(minutes):02d}:{int(seconds):02d} secs" + Style.RESET_ALL)
        print(data.head())
        start_time = datetime.now()

    ###### Split the data by timestep ######
    dfs_by_timestep = split_df_by_timestep(data)
    if args.verbose:
        minutes, seconds = _calc_time_diff(start_time)
        print("*" * 100)
        print(Fore.MAGENTA + f"[VERBOSE] Data split into {len(dfs_by_timestep)} timesteps in {int(minutes):02d}:{int(seconds):02d} secs" + Style.RESET_ALL)
        print(dfs_by_timestep[0].head())
        start_time = datetime.now()
        
    
    ###### Calculate order series ######    
    order_by_timestep = calc_order_all_experiment(dfs_by_timestep)
    if args.verbose:
        minutes, seconds = _calc_time_diff(start_time)
        print("*" * 100)
        print(Fore.MAGENTA + f"[VERBOSE] Order series calculated in {int(minutes):02d}:{int(seconds):02d} secs" + Style.RESET_ALL)
        start_time = datetime.now()

    
    ###### Calculate union ######
    union_by_timestep = calc_union_all_experiment(dfs_by_timestep)
    if args.verbose:
        minutes, seconds = _calc_time_diff(start_time)
        print("*" * 100)
        print(Fore.MAGENTA + f"[VERBOSE] Union calculated in {int(minutes):02d}:{int(seconds):02d} secs" + Style.RESET_ALL)
        start_time = datetime.now()

    ###### Plot the order series ######
    # plot(order_by_timestep)
    plot(union_by_timestep)


    cudf_df = load_data(data_file,gpu=True)
    if args.verbose:
        minutes, seconds = _calc_time_diff(start_time)
        print("*" * 100)
        print(Fore.MAGENTA + f"[VERBOSE] calculated in {int(minutes):02d}:{int(seconds):02d} secs" + Style.RESET_ALL)
        start_time = datetime.now()
    print(cudf_df.dtypes)

    union = []
    # Parallel processing using ThreadPoolExecutor
    NAME = _build_data_file_name(args)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(process_graph, range(1, 5000))
        union = list(results)
    print(len(union))
    if args.verbose:
        minutes, seconds = _calc_time_diff(start_time)
        print("*" * 100)
        print(Fore.MAGENTA + f"[VERBOSE] calculated in {int(minutes):02d}:{int(seconds):02d} secs" + Style.RESET_ALL)
        start_time = datetime.now()
        
    plot(union)


if __name__ == '__main__':
    import cupy as cp
    device = cp.cuda.Device()

    print(device)  # Correct way to get the name of your GPU
    init() # Initialize colorama
    main()
