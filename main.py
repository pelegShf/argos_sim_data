


import argparse
import os
from order import get_order
from consts import DB
from utils import read_csv


# Get args from the command line
parser = argparse.ArgumentParser(description="Run multiple experiments" )
# Add command-line arguments with default values
parser.add_argument("-p", "--path", type=str, default="", help="Template for experiments")


args = parser.parse_args()
experiment_path = args.path


exp_data = read_csv(DB+experiment_path)

print(exp_data.head())
order = get_order(exp_data)
print(order.head())