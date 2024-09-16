import argparse
import os
import re

DB = "../data/DB/"

def find_matching_subdirs(base_dir, output_file):
    """
    Find all subdirectories matching the pattern hyperparameter_set_X/results/dDDMMYY_TTTT/
    and write them to a file with the format '<path> set_X'.
    
    Parameters:
        base_dir (str): The base directory to search within.
        output_file (str): The output file to write the list of matching subdirectories.
    """
    pattern = re.compile(r'.*/hyperparameter_set_(\d+)/results/d\d{6}_\d{4}/')
    matching_subdirs = []
    for root, dirs, files in os.walk(DB+base_dir):
        for dir_name in dirs:
            subdir_path = os.path.join(root, dir_name)
            # Convert the subdir_path to a relative path before checking the pattern
            rel_path = os.path.relpath(subdir_path, base_dir) + '/'
            match = pattern.match(rel_path)
            if match:
                set_number = match.group(1)
                matching_subdirs.append(f"{rel_path[len(DB)*2+4:]} set_{set_number}")

    with open(output_file, 'w') as f:
        for subdir in matching_subdirs:
            f.write(subdir + '\n')


parser = argparse.ArgumentParser(description="List all subdirectories in the given base directory.")
parser.add_argument('-i', type=str, help="Base directory to search within")
parser.add_argument('-o', type=str, help="Output file to write the list of subdirectories")
args = parser.parse_args()

# Create the list of subdirectories
find_matching_subdirs(args.i, args.o)

print(f"List of subdirectories saved to {args.o}")