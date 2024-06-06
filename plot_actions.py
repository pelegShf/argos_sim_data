import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import pandas as pd
import numpy as np


file_dir = "../data/DB/06062024_1711/avoidAttract/40/hyperparameter_set_0/X_RAY/robot_actions_1.csv"
# Load the data
df = pd.read_csv(file_dir)
# Create a color map

row_number = 0  # Change this to your desired row
row_data = df.iloc[row_number]
row_data=row_data["Actions"].split()

# Select a part of the list
start = 2200  # Change this to your desired start index
end = 2800  # Change this to your desired end index
row_data = row_data[start:end]

actions = ["-180","-150","-120","-90","-60","-30","0","30","60","90","120","150","180"]
colors = ['red', 'green', 'blue', 'yellow', 'purple','pink', 'orange', 'cyan', 'magenta', 'lime', 'navy', 'teal','black']
action_color_map = dict(zip(actions, colors))

legend_patches = [mpatches.Patch(color=color, label=action) for action, color in action_color_map.items()]

for row_number in range(len(df)):
    row_data = df.iloc[row_number]
    row_data=row_data["Actions"].split()
    row_data = row_data[start:end]
    for i, action in enumerate(row_data):
        plt.plot(i, row_number, color=action_color_map[action], marker='o', linestyle='')

plt.legend(handles=legend_patches)

plt.show()