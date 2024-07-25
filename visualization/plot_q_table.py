import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Update according to the number of states in the code.
start = 0.04
end = 0.19
STATE_SIZE = 8

step = (end - start) / (STATE_SIZE - 1)
ranges = [start + i * step for i in range(STATE_SIZE)]

parser = argparse.ArgumentParser(description="Run multiple experiments" )
parser.add_argument("-i", "--file_paths", type=str, required=True, help="File containing the paths to the files to process")
parser.add_argument("-pre", "--prefix", type=str, default="/MABLearning/40/hyperparameter_set_0/X_RAY/", help="File containing the paths to the files to process")
parser.add_argument("-m", "--method", choices=['argmax', 'max'], default='argmax', help="Choose method for processing (default: argmax)")
parser.add_argument("-d","--data_type", choices=['count', 'value', 'q'], default='q', help="Choose data type to process (default: q)")

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
elif data_type == 'value':
    col = 1
else:
    col = 2

# Initialize a list to store the argmax results
argmax_list = []

# Iterate over the file indices
for idx in range(0, 39):  # Assuming 25 files
    file_type =f"learner_1_{idx}.csv"

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

# Convert the list of argmax values to a DataFrame
argmax_df = pd.DataFrame(argmax_list, columns=[f'{ranges[i]:.2f}' for i in range(len(argmax_list[0]))])

# Plot the heatmap
plt.figure(figsize=(12, 8))  # Adjust the size as needed

cbar = True

#Format the digits by column
if method == 'max' and (data_type == 'value' or data_type == 'q'):
    fmt='.4f'
else:
    fmt='.0f'
    if method == 'argmax':
        cbar = False
    
sns.heatmap(argmax_df, annot=True, cmap='viridis', cbar=cbar, fmt=fmt)

# Customize the plot
plt.title(f'{data_type} of agents per state')
plt.xlabel('State')
plt.ylabel('Agent Index')

plt.savefig(f'{dir_path}{data_file_name}{model_size_path}heatmap_{data_type}_{method}.png')
# Show the plot
plt.show()
