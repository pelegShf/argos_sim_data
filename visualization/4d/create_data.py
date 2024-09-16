import os
import pandas as pd
import argparse

OUTPUT_FOLDER = "./visualization/graphs/4d/"
INPUT_FOLDER = "./visualization/4d/lists/"
FILE_TYPE_TXT = ".txt"
FILE_TYPE_CSV = ".csv" 


def parse_settings(settings_file):
    """
    Parse the _settings.txt file to extract the mixedRdesired values.
    
    Parameters:
        settings_file (str): Path to the _settings.txt file.
        
    Returns:
        tuple: A tuple of (r1, r2, r3).
    """
    with open(settings_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        if 'mixedRdesired' in line:
            r_values = line.split('{')[1].split('}')[0].split(',')
            r1, r2, r3 = map(float, r_values)
            return r1, r2, r3
    return None


def calculate_val(metrics_file,experiment_length=5000,window_size=1):
    """
    Calculate the average val from metrics_list.csv every 5000 rows.
    
    Parameters:
        metrics_file (str): Path to the metrics_list.csv file.
        
    Returns:
        float: The average value of the 'order' column.
    """
    df = pd.read_csv(metrics_file)
    order_values = df['orders']

    segment_averages = []
    for start in range(0, len(order_values), experiment_length):
        end = start + experiment_length
        if end > len(order_values):
            break
        segment = order_values.iloc[end - window_size:end]
        segment_avg = segment.mean()
        segment_averages.append(segment_avg)

    overall_avg = sum(segment_averages) / len(segment_averages)
    return overall_avg


def process_experiment_folder(folder_path,settings_prefix='X_RAY/logs/',metrics_prefix='results/'):
    """
    Process a single experiment folder to extract r1, r2, r3, and val.
    
    Parameters:
        folder_path (str): Path to the experiment folder.
        
    Returns:
        tuple: A tuple of (r1, r2, r3, val).
    """
    settings_file = os.path.join(folder_path,settings_prefix, '_settings.txt')
    results_folder = os.path.join(folder_path, metrics_prefix)

    r1, r2, r3 = parse_settings(settings_file)
    metric_file = find_metric_file(results_folder)
    if metric_file is None:
        raise FileNotFoundError(f"Could not find metric.csv in {results_folder}")
    

    val = calculate_val(metric_file)
    
    return r1, r2, r3, val


def create_csv_from_locations(file_with_locations, output_csv):
    """
    Create a CSV file with r1, r2, r3, and val for all experiment locations listed in a file.
    
    Parameters:
        file_with_locations (str): Path to the file containing all experiment folder paths.
        output_csv (str): Path to the output CSV file.
    """
    rows = []
    
    with open(INPUT_FOLDER + file_with_locations+FILE_TYPE_TXT, 'r') as f:
        folder_paths = f.readlines()
    
    for folder_path in folder_paths:
        folder_path = folder_path.strip()
        folder_path = "../data/DB/"+folder_path
        if os.path.isdir(folder_path):
            try:
                r1, r2, r3, val = process_experiment_folder(folder_path)
                rows.append([r1, r2, r3, val])
            except Exception as e:
                print(f"Error processing {folder_path}: {e}")
    # Create DataFrame and save to CSV
    df = pd.DataFrame(rows, columns=['r1', 'r2', 'r3', 'val'])
    full_output_csv = os.path.join(OUTPUT_FOLDER, output_csv+FILE_TYPE_CSV)
    df.to_csv(full_output_csv, index=False)
    
    print(f"[INFO] Data saved to {full_output_csv}")

def create_csv_for_plotting(base_folder, db, date, time, output_csv):
    """
    Create a CSV file with r1, r2, r3, and val for all experiments.
    
    Parameters:
        base_folder (str): Base folder containing all data.
        db (str): Database folder name.
        date (str): Date folder in 'yyyy_mm/ddmmyyyy' format.
        time (str): Time folder in 'hhmm' format.
        output_csv (str): Path to the output CSV file.
    """
    main_folder_path = os.path.join(base_folder, db, date, time)
    
    if not os.path.isdir(main_folder_path):
        raise FileNotFoundError(f"Folder {main_folder_path} not found")
    
    rows = []
    
    # Loop through each hyperparameter_set_d folder
    for sub_folder in os.listdir(main_folder_path):
        full_sub_folder_path = os.path.join(main_folder_path, sub_folder)
        
        if os.path.isdir(full_sub_folder_path) and sub_folder.startswith('hyperparameter_set_'):
            r1, r2, r3, val = process_experiment_folder(full_sub_folder_path)
            rows.append([r1, r2, r3, val])
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame(rows, columns=['r1', 'r2', 'r3', 'val'])
    df.to_csv(output_csv, index=False)


def find_metric_file(results_folder):
    """
    Search for the metrics_list.csv file in the results folder with an unknown name.
    
    Parameters:
        results_folder (str): Path to the results folder.
        
    Returns:
        str: Path to the found metric.csv file, or None if not found.
    """
    for sub_folder in os.listdir(results_folder):
        sub_folder_path = os.path.join(results_folder, sub_folder)
        if os.path.isdir(sub_folder_path):
            metric_file = os.path.join(sub_folder_path, 'metrics_list.csv')
            if os.path.isfile(metric_file):
                return metric_file
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process experiment data and create a CSV for plotting.")
    parser.add_argument('--base_folder', type=str,default="../data/",  help="Base folder containing all data")
    parser.add_argument('--db', type=str, default="DB/" ,help="Database folder name (e.g., 'DB')")
    parser.add_argument('--date', type=str, help="Date folder in 'yyyy_mm/ddmmyyyy' format")
    parser.add_argument('--time', type=str, help="Time folder in 'hhmm' format")
    parser.add_argument('--output_csv', type=str, default="output.csv", help="Output CSV file name (without .csv)")
    parser.add_argument('--locations_file', type=str, help="File name containing all experiment folder paths (without .txt)")

    args = parser.parse_args()
    
    if args.locations_file:
        create_csv_from_locations(args.locations_file,args.output_csv)
    else:
        if not (args.base_folder and args.db and args.date and args.time):
            parser.error("If not using --locations_file, --base_folder, --db, --date, and --time are required.")
        create_csv_for_plotting(args.base_folder, args.db, args.date, args.time, args.output_csv)
