#!/bin/bash

example_path=`readlink -e ./example_project`

./cmtt.py \
    --project-root=$example_path \
    --config-path=$example_path/mutation_config \
    --output-path=$example_path/mutation_output \
    --global-timeout=5

# Mutation testing done, time to generate a report
./cmtt.py \
    --project-root=$example_path \
    --config-path=$example_path/mutation_config \
    --output-path=$example_path/mutation_output \
    --report
