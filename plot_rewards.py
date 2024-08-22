import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
from visualization.main import plot_series

def load_data(file_dir):
    return pd.read_csv(file_dir)

def calculate_rolling_average(rewards, window=100):
    """Calculate rolling average of rewards."""
    return rewards.rolling(window=window).mean()

def calculate_chunked_average(rewards, chunk_size=100):
    """Calculate average of rewards in chunks."""
    avg_rewards = [np.mean(rewards[i:i+chunk_size]) for i in range(0, len(rewards), chunk_size)]
    # Pad avg_rewards with np.nan to make sure all avg_rewards have the same length
    avg_rewards += [np.nan] * (len(rewards) // chunk_size + 1 - len(avg_rewards))
    return avg_rewards

def calculate_rewards(df, use_rolling_average):
    all_rewards = []  # List to store all rewards
    for row_number, row_data in df.iterrows():
        rewards = pd.Series([float(reward) for reward in row_data["Rewards"].split()]).fillna(0.0)
        if use_rolling_average:
            avg_rewards = calculate_rolling_average(rewards)
        else:
            avg_rewards = calculate_chunked_average(rewards)
        all_rewards.append(pd.Series(avg_rewards).fillna(0.0))  # Convert avg_rewards to a Series before appending
    return all_rewards

def plot_rewards(all_rewards, use_rolling_average,file_dir, idx):
    for i, avg_rewards in enumerate(all_rewards):
        plt.plot(avg_rewards, label='Row {}'.format(i))
    average_reward = pd.concat(all_rewards, axis=1).mean(axis=1)
    plt.plot(average_reward, label='Average', color='black', linewidth=2)
    if use_rolling_average:
        plt.title('Rolling average of rewards for all agents')
    else:
        plt.title('Average of every 100 rewards for all agents')
    plt.xlabel('Action index')
    plt.ylabel('Average reward')
    # plt.legend()
    plt.savefig(f"{file_dir}img_rewards{idx}")
    plt.show()
    

def main():
    
    # Plot a single experiment
    # idx = 1
    time = "1246"
    # file_dir = f"../data/DB/{idx}/robot_actions_{idx}.csv"
    dir = f"../data/DB/2024_07/25072024/{time}/MABLearning/40/hyperparameter_set_0/X_RAY/"
    # file_dir = f"{dir}/{idx}/robot_actions_{idx}.csv"
    # use_rolling_average = True  # Change this to False to use average of every 100
    # df = load_data(file_dir)
    # all_rewards = calculate_rewards(df, use_rolling_average)
    # plot_rewards(all_rewards, use_rolling_average,dir, f"{idx}_{time}")
    
    
    # Plot rewards for every 10th experiment from 850 to 1050
    for idx in range(1, 2,1):
        file_dir = f"{dir}/robot_actions/robot_actions_{idx}.csv"
        use_rolling_average = True  # Change this to False to use average of every 100
        df = load_data(file_dir)
        all_rewards = calculate_rewards(df, use_rolling_average)    
        plot_rewards(all_rewards, use_rolling_average,dir, f"{idx}_{time}")
        #  Clear the current figure
        plt.clf()
if __name__ == "__main__":
    main()