import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

ALPHA = 0.3

def set_plot_params(large):
    plt.rcParams['figure.figsize'] = (10, 6)  # figure size
    plt.rcParams['axes.grid'] = True  # Show grid by default
    sns.set_palette("colorblind")

    if large: # Good for pdfs and papers
        plt.rcParams['font.size'] = 18  # font size
        plt.rcParams['axes.titlesize'] = 24  # title font size
        plt.rcParams['axes.labelsize'] = 18  # label font size
        plt.rcParams['lines.linewidth'] = 4  # line width
        plt.rcParams['xtick.labelsize'] = 14  # tick label font size
        plt.rcParams['ytick.labelsize'] = 14  # tick label font size
        plt.rcParams['legend.fontsize'] = 16  # legend font size
    else: # Good for checking plots
        plt.rcParams['font.size'] = 12  # font size
        plt.rcParams['axes.titlesize'] = 16  # title font size
        plt.rcParams['axes.labelsize'] = 14  # label font size
        plt.rcParams['lines.linewidth'] = 2  # line width
        plt.rcParams['xtick.labelsize'] = 10  # tick label font size
        plt.rcParams['ytick.labelsize'] = 10  # tick label font size
        plt.rcParams['legend.fontsize'] = 12  # legend font size


def plot_individual_series(series_list,color,label='Series'):

    for i, series in enumerate(series_list):
        plt.plot(series, color=color, label=label)


def plot_avg_series(series_list,color,label='Average Series', error_type='std'):
    avg_series = np.mean(series_list, axis=0)
    if error_type == 'std':
        error = np.std(series_list, axis=0)
    elif error_type == 'se':
        error = np.std(series_list, axis=0) / np.sqrt(len(series_list))

    plt.plot(avg_series, color=color, label=label)
    if error_type == 'std':
        plt.fill_between(range(len(avg_series)), avg_series - error, avg_series + error, color=color, alpha=ALPHA) # standard deviation
    elif error_type == 'se':
        plt.fill_between(range(len(avg_series)), avg_series - error, avg_series + error, color=color, alpha=ALPHA) # standard error


def plot_series(series_list,labels=[], filename=None, avg=True, show_individual=True, error_type='std',to_pdf=False,fix_y_axis=False):
    set_plot_params(to_pdf)


    colors = sns.color_palette()
    for idx,series in enumerate(series_list):
        if show_individual:
            plot_individual_series(series,colors[idx])

        if avg:
            if(len(labels)>0):
                plot_avg_series(series,colors[idx],label=labels[idx],error_type=error_type)
            else:
                plot_avg_series(series,colors[idx], error_type=error_type)

    plt.legend()
    if fix_y_axis: # Fix y-axis to 0-1 for order parameter plots
        plt.ylim(0,1)
    if filename is not None:
        plt.savefig(f'{filename}.png')
    else:
        plt.show()

    plt.clf()

# Example usage
# num_series = 10
# series_list = [np.random.rand(100) for _ in range(num_series)]  # Generate random series for demonstration
# series_list2= [np.random.rand(100) for _ in range(num_series)]  # Generate random series for demonstration
# plot_series([series_list,series_list2], avg=True, show_individual=False, error_type='se',to_pdf=True)


