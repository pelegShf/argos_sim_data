import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import entropy

STATE_DISTANCE = 8
STATE_ANGLE = 8

# Update according to the number of states in the code.
start = 0.03
end = 0.19
STATE_SIZE = 8

# Create the state map
state_map = {}
t = 0
for i in range(STATE_DISTANCE):
    for j in range(STATE_ANGLE):
        state_map[(i, j)] = t
        t += 1

step = (end - start) / (STATE_SIZE - 1)
ranges = [start + i * step for i in range(STATE_SIZE)]
parser = argparse.ArgumentParser(description="Run multiple experiments")
parser.add_argument("-i", "--file_paths", type=str, required=True, help="File containing the paths to the files to process")
parser.add_argument("-pre", "--prefix", type=str, default="/mixGroupLearning/40/hyperparameter_set_0/X_RAY/", help="File containing the paths to the files to process")
parser.add_argument("-m", "--method", choices=['argmax', 'max'], default='argmax', help="Choose method for processing (default: argmax)")
parser.add_argument("-d", "--data_type", choices=['count', 'value', 'q'], default='q', help="Choose data type to process (default: q)")

args = parser.parse_args()
data_file_name = args.file_paths
method = args.method
data_type = args.data_type
model_size_path = args.prefix

dir_path = "../data/DB/"
full_path = dir_path + data_file_name + model_size_path

# Define col by data type
if data_type == 'count':
    col = 0
else:
    col = 1

# Initialize a list to store the argmax results
argmax_list = []
sum_list = []
experiment_number = 1
for experiment in range(1, 2):
    # Iterate over the file indices
    for idx in range(0, 40): 
        file_type = f"{experiment}/logs/q_table/learner_{experiment}_{idx}.csv"
        file_path = os.path.join(full_path, file_type)

        # Load the CSV file
        data = pd.read_csv(file_path, header=None)
        
        # Extract the last number in each element and convert to float
        last_numbers = data.map(lambda x: float(x.split()[col]))
        
        # Find the index of the maximum value in each row (argmax)
        if method == 'argmax':
            max_in_rows = last_numbers.idxmax(axis=1)
        else:
            max_in_rows = last_numbers.max(axis=1)

        # Append the argmax values to the list
        argmax_list.append(max_in_rows.values)


# Create a list of state labels based on the state_map
state_labels = [f'{state_map[(i, j)]}' for i in range(STATE_DISTANCE) for j in range(STATE_ANGLE)]

# Convert the list of argmax values to a DataFrame using state labels
argmax_df = pd.DataFrame(argmax_list, columns=state_labels[:len(argmax_list[0])])

# Calculate entropy, std, and mean for each state
entropy_values = []
std_values = []
mean_values = []
for col in argmax_df.columns:
    col_data = argmax_df[col].value_counts(normalize=True)
    entropy_values.append(entropy(col_data))
    std_values.append(argmax_df[col].std())
    mean_values.append(argmax_df[col].mean())

average_entropy = sum(entropy_values) / len(entropy_values)
print(f"average_entropy: {average_entropy}")

# Print the count of each value if method is argmax
# if method == 'argmax':
#     print("Count of each value in argmax results:")
#     for col in argmax_df.columns:
#         print(f"State {col}:")
#         print(argmax_df[col].value_counts())
#         print(argmax_df[col].value_counts()/len(argmax_df[col]))

# Plot the heatmap of argmax values
plt.figure(figsize=(12, 8))
cbar = True
fmt = '.0f' if (method == 'argmax' or data_type == 'count') else '.4f'
if method == 'argmax':
    cbar = False
    
sns.heatmap(argmax_df, annot=True, cmap='viridis', cbar=cbar, fmt=fmt)

# Customize the plot
plt.title(f'{data_type} of agents per state')
plt.xlabel('State')
plt.ylabel('Agent Index')
plt.savefig(f'{dir_path}{data_file_name}{model_size_path}/{experiment}/heatmap_{data_type}_{method}_{experiment_number}.png')
plt.show()

