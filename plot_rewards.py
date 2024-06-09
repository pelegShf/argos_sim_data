import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

file_dir = "../data/DB/09062024_1037/avoidAttract/40/hyperparameter_set_0/X_RAY/robot_actions_1.csv"
# Load the data
df = pd.read_csv(file_dir)

use_rolling_average = True  # Change this to False to use average of every 100

all_rewards = []  # List to store all rewards

# Plot rewards for each row
for row_number, row_data in df.iterrows():
    rewards = pd.Series([float(reward) for reward in row_data["Rewards"].split()])
    if use_rolling_average:
        avg_rewards = rewards.rolling(window=100).mean()
    else:
        avg_rewards = [np.mean(rewards[i:i+100]) for i in range(0, len(rewards), 100)]
        # Pad avg_rewards with np.nan to make sure all avg_rewards have the same length
        avg_rewards += [np.nan] * (len(rewards) // 100 + 1 - len(avg_rewards))
    plt.plot(avg_rewards, label='Row {}'.format(row_number))
    all_rewards.append(pd.Series(avg_rewards))  # Convert avg_rewards to a Series before appending

# Calculate and plot average reward across all rows
average_reward = pd.concat(all_rewards, axis=1).mean(axis=1)
plt.plot(average_reward, label='Average', color='black', linewidth=2)

if use_rolling_average:
    plt.title('Rolling average of rewards for all agents')
else:
    plt.title('Average of every 100 rewards for all agents')
plt.xlabel('Action index')
plt.ylabel('Average reward')
# plt.legend() 
plt.show()