import os
import matplotlib.pyplot as plt
import imageio

from consts import DEBUG_FOLDER, MATH_THRESHOLD
from utils import  read_csv
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
        plot_series([order,order_params["Polarization"]], f"{DEBUG_FOLDER}debug_order_{idx}")
        #debug_metric(order_params["Polarization"].round(4),order)
        debug_metric(order_params["Union"].round(4),union)
        plot_series([union,order_params["Union"]], f"{DEBUG_FOLDER}debug_union_{idx}")



def create_video(df, every_T_frames=10):
    # Create a list to store the filenames of the plots
    filenames = []

    # Find the min and max x and y coordinates
    min_x, max_x, min_y, max_y = float('inf'), float('-inf'), float('inf'), float('-inf')
    for centers in df:
        coords, _ = zip(*centers)
        x_coords, y_coords = zip(*coords)
        min_x = min(min_x, min(x_coords))
        max_x = max(max_x, max(x_coords))
        min_y = min(min_y, min(y_coords))
        max_y = max(max_y, max(y_coords))

    # Add 10% padding to the limits
    x_padding = (max_x - min_x) * 0.1
    y_padding = (max_y - min_y) * 0.1
    min_x -= x_padding
    max_x += x_padding
    min_y -= y_padding
    max_y += y_padding

    for i, centers in enumerate(df):
        # Only create a plot every T frames
        if i % every_T_frames == 0:
            # Unpack the x, y coordinates and sizes
            coords, sizes = zip(*centers)
            x_coords, y_coords = zip(*coords)

            # Increase all sizes by 2
            sizes = [size * 3 for size in sizes]

            # Create a scatter plot of the group centers
            plt.scatter(x_coords, y_coords, s=sizes, color='blue')
            plt.xlim([min_x, max_x])  # Set the limits of the x-axis
            plt.ylim([min_y, max_y])  # Set the limits of the y-axis
            plt.title(f'Time: {i}')

            # Add the coordinates next to the points
            for j in range(len(x_coords)):
                plt.text(x_coords[j], y_coords[j], f'({x_coords[j]:.4f}, {y_coords[j]:.4f})')

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