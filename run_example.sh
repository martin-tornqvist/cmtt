#!/bin/bash

echo "Example runner for CMTT"

example_path=`readlink -e ./example_project`

echo "Example project path: $example_path"
echo "-------------------------------------------------------------------------"

./cmtt.py \
    --project-root=$example_path \
    --config-path=$example_path/mutation_config \
    --output-path=$example_path/mutation_output \
    --global-timeout=5
