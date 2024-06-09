import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def load_data(file_dir):
    return pd.read_csv(file_dir)

def calculate_rewards(df, use_rolling_average):
    all_rewards = []  # List to store all rewards
    for row_number, row_data in df.iterrows():
        rewards = pd.Series([float(reward) for reward in row_data["Rewards"].split()])
        if use_rolling_average:
            avg_rewards = rewards.rolling(window=100).mean()
        else:
            avg_rewards = [np.mean(rewards[i:i+100]) for i in range(0, len(rewards), 100)]
            # Pad avg_rewards with np.nan to make sure all avg_rewards have the same length
            avg_rewards += [np.nan] * (len(rewards) // 100 + 1 - len(avg_rewards))
        all_rewards.append(pd.Series(avg_rewards))  # Convert avg_rewards to a Series before appending
    return all_rewards

def plot_rewards(all_rewards, use_rolling_average):
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
    plt.legend()
    plt.show()

def main():
    file_dir = "../data/DB/09062024_1925/MABLearning/40/hyperparameter_set_0/X_RAY/robot_actions_1.csv"
    use_rolling_average = True  # Change this to False to use average of every 100
    df = load_data(file_dir)
    all_rewards = calculate_rewards(df, use_rolling_average)
    plot_rewards(all_rewards, use_rolling_average)

if __name__ == "__main__":
    main()