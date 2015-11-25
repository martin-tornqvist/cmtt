#!/bin/bash

# This script shows a usage example

# Get absolute path of example project
example_path=`readlink -e ./example_project`

# Run mutation testing
./cmtt.py \
    --project-root=$example_path \
    --config-path=$example_path/mutation_config \
    --output-path=$example_path/mutation_output \
    --global-timeout=10

# Mutation testing done, time to generate a report
./cmtt.py \
    --project-root=$example_path \
    --config-path=$example_path/mutation_config \
    --output-path=$example_path/mutation_output \
    --report
