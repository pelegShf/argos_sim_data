

from matplotlib import pyplot as plt
import pandas as pd
from consts import PRECISION, ROBOT_ID_COL, TIMESTEP_COL, SPEED_COL


def calc_avg_speed(df):
    avg_speed = df[SPEED_COL].mean()
    return avg_speed


def get_speed(df):
    speed_series = df.groupby(TIMESTEP_COL).apply(calc_avg_speed)
    speed_series = speed_series.round(4)
    # order_series = data_cleaning(order_series)

    return speed_series


def get_individ_speed(trial=1, robotNum=1, avg_over_frames=50, ax=None):
    exp_data = pd.read_csv(f"../data/DB/07052024_1235/avoidAttract/40/hyperparameter_set_0/X_RAY/raw_data_{trial}.csv")

    df_robot = exp_data[exp_data[ROBOT_ID_COL] == f"n{robotNum}"]

    # Group by each set of 10 frames and calculate the mean speed
    df_robot = df_robot.copy()
    df_robot['FrameGroup'] = df_robot[TIMESTEP_COL] // avg_over_frames
    df_robot_avg = df_robot.groupby('FrameGroup')[SPEED_COL].mean()

    # Create a new subplot if no Axes object was provided
    if ax is None:
        fig, ax = plt.subplots()

    # Plot the average speed
    ax.plot(df_robot_avg.index * avg_over_frames, df_robot_avg.values, label='Average Speed')
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Average Speed')
    ax.set_title(f'Robot {robotNum} Average Speed')
    ax.legend()
    

    return ax
    

def get_individ_speed_rolling(trial=1, robotNum=1, avg_over_frames=50, ax=None):
    exp_data = pd.read_csv(f"../data/DB/07052024_1220/avoidAttract/40/hyperparameter_set_0/X_RAY/raw_data_{trial}.csv")

    df_robot = exp_data[exp_data[ROBOT_ID_COL] == f"n{robotNum}"]

    # Calculate the rolling average speed
    df_robot_avg = df_robot[SPEED_COL].rolling(window=avg_over_frames).mean()

    # Create a new subplot if no Axes object was provided
    if ax is None:
        fig, ax = plt.subplots()

    # Plot the average speed
    ax.plot(df_robot[TIMESTEP_COL], df_robot_avg.values, label='Average Speed')
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Average Speed')
    ax.set_title(f'Robot {robotNum} Average Speed')
    ax.legend()

    return ax