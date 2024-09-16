#!/bin/bash

# Define the base directory and other parameters
BASE_DIR="1123/avoidAttract/30"
METHOD="order"

# Loop over the different hyperparameter sets
for i in {0..9}; do
    HYPERPARAMETER_SET="hyperparameter_set_$i"
    echo "Running: python3 main.py -i ${BASE_DIR}/${HYPERPARAMETER_SET}/ -m ${METHOD}" -rc "30"
    python3 main.py -i "${BASE_DIR}/${HYPERPARAMETER_SET}/" -m "${METHOD}" -rc "30"
done