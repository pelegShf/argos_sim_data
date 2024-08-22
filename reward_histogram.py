import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

def plot_histograms(data, unique_states, unique_actions,save_dir=""):
    # Determine the number of rows for plotting
    num_states = len(unique_states)
    num_actions = len(unique_actions)

    # Create subplots
    fig, axes = plt.subplots(num_states, num_actions, figsize=(12, 2 * num_states))

    # Ensure axes is always a 2D array
    if num_states == 1:
        axes = [axes]

    # Plot histograms for each state-action pair
    for i, state in enumerate(unique_states):
        for j, action in enumerate(unique_actions):
            filtered_data = data[(data['state'] == state) & (data['action'] == action)]
            ax = axes[i][j] if num_states > 1 else axes[j]
            ax.hist(filtered_data['reward'], bins=20, edgecolor='black')
            # ax.set_xlim(-0.025, 0.0)
            # ax.set_ylim(0, 100)
            ax.set_xlabel('Reward', fontsize=8)
            ax.set_ylabel('Frequency', fontsize=8)
            ax.tick_params(axis='x', labelrotation=45, labelsize=8)
            ax.tick_params(axis='y', labelsize=8)

            # Add state title to the left of each row
            if j == 0:
                ax.set_ylabel(f'State {state}', fontsize=10, rotation=0, labelpad=10, ha='right')

            # Add action title to the top of each column
            if i == 0:
                ax.set_title(f'Action {action}', fontsize=10)

            # Print the average reward for each state-action pair
            avg_reward = filtered_data['reward'].mean()
            print(f'Average reward for state {state}, action {action}: {avg_reward}')

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.5, wspace=0.3)
    if save_dir != "":
        plt.savefig(save_dir+"_histogram_rewards.png")
    plt.show()

def plot_avg_rewards(data, unique_states, unique_actions,save_dir=""):
    # Calculate the average reward for each state-action pair
    avg_rewards = data.groupby(['state', 'action'])['reward'].mean().unstack()

    # Plot the average rewards
    avg_rewards.plot(kind='bar', figsize=(12, 6))
    plt.xlabel('State')
    plt.ylabel('Average Reward')
    plt.title('Average Reward per Action Grouped by State')
    plt.legend(title='Action')
    plt.xticks(rotation=0)
    plt.tight_layout()
    if save_dir != "":
        plt.savefig(save_dir+"_avg_rewards.png")
    plt.show()
    

    # Print the average reward for each state-action pair
    for state in unique_states:
        for action in unique_actions:
            avg_reward = avg_rewards.loc[state, action]
            print(f'Average reward for state {state}, action {action}: {avg_reward}')

def main(db_dir, month_date, hour, model, filename, plot_type):
    # Construct the file path
    file_path = os.path.join(db_dir, month_date, hour, model, filename)

    # Read the data
    data = pd.read_csv(file_path, names=['state', 'action', 'reward'])

    # Get unique states and actions
    unique_states = data['state'].unique()
    unique_actions = data['action'].unique()

    if plot_type == 'histograms':
        plot_histograms(data, unique_states, unique_actions,os.path.join(db_dir, month_date, hour, model))
    elif plot_type == 'avg_rewards':
        plot_avg_rewards(data, unique_states, unique_actions,os.path.join(db_dir, month_date, hour, model))
    else:
        print(f"Unknown plot type: {plot_type}. Please choose 'histograms' or 'avg_rewards'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot reward histograms or average rewards for state-action pairs.')
    parser.add_argument('--db_dir', type=str, default='../data/DB/', help='Database directory')
    parser.add_argument('--month_date', type=str, default='2024_07/27072024/', help='Month and date')
    parser.add_argument('--hour', type=str, default='1508/', help='Hour')
    parser.add_argument('--model', type=str, default='MABLearning/40/hyperparameter_set_0/X_RAY/', help='Model path')
    parser.add_argument('--filename', type=str, default='rewards_1_1.csv', help='Filename')
    parser.add_argument('--plot_type', type=str, default='histograms', choices=['histograms', 'avg_rewards'], help='Type of plot to generate')

    args = parser.parse_args()
    main(args.db_dir, args.month_date, args.hour, args.model, args.filename, args.plot_type)