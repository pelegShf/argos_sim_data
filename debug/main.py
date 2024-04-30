import os

from consts import DEBUG_FOLDER, MATH_THRESHOLD
from utils import data_cleaning, read_csv
from visualization.main import plot_series


def debug_metric(cpp,py):
    for r,(i,j) in enumerate(zip(cpp,py)):
        if(abs(i-j)> MATH_THRESHOLD and r > 0):
            print(r,i,j)
    print("**********")

def debug_code(debug, filename, order, union, idx):
    if debug:
        # Replace 'raw_data_' with 'order_params_' in the filename
        order_params_filename = os.path.join(os.path.dirname(filename), 
                                            os.path.basename(filename).replace('raw_data_', 'order_params_'))

        # Read the corresponding order_params_ file
        order_params = read_csv(order_params_filename)
        order_params = data_cleaning(order_params)
        plot_series([order,order_params["Polarization"]], f"{DEBUG_FOLDER}debug_order_{idx}")
        #debug_metric(order_params["Polarization"].round(4),order)
        debug_metric(order_params["Union"].round(4),union)
        plot_series([union,order_params["Union"]], f"{DEBUG_FOLDER}debug_union_{idx}")

import matplotlib.pyplot as plt
import imageio
import os

import matplotlib.pyplot as plt
import imageio
import os

def create_video(df, min_x, max_x, min_y, max_y):
    # Create a list to store the filenames of the plots
    filenames = []

    for i, centers in enumerate(df):
        # Unpack the x, y coordinates
        x_coords, y_coords = zip(*centers)

        # Create a scatter plot of the group centers
        plt.scatter(x_coords, y_coords, color='blue')
        plt.xlim([min_x, max_x])  # Set the limits of the x-axis
        plt.ylim([min_y, max_y])  # Set the limits of the y-axis
        plt.title(f'Time: {i}')

        # Save the plot to a file
        filename = f'plot_{i}.png'
        plt.savefig(filename)
        filenames.append(filename)

        # Clear the plot for the next one
        plt.clf()

    # Create a video from the plots
    with imageio.get_writer('group_centers.mp4', mode='I') as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)

    # Remove the plot files
    for filename in filenames:
        os.remove(filename)