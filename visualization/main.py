import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import importlib


if 'visualization' in sys.modules:
    # We're running from inside the visualization package
    import_str = 'visualization.'
else:
    
    # We're running from outside the visualization package
    import_str = ''


settings = importlib.import_module(f'{import_str}settings')



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
        plt.fill_between(range(len(avg_series)), avg_series - error, avg_series + error, color=color, alpha=settings.ALPHA) # standard deviation
    elif error_type == 'se':
        plt.fill_between(range(len(avg_series)), avg_series - error, avg_series + error, color=color, alpha=settings.ALPHA) # standard error


def plot_series(series_list,labels=[], filename=None, avg=True, show_individual=True, error_type='std',to_pdf=False):
    if to_pdf:
        settings = importlib.import_module(f'{import_str}settings_to_print')
    else:
        settings = importlib.import_module(f'{import_str}settings')

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


