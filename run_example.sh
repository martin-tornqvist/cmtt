#!/bin/bash

example_project_dir=./example_project

./run_mutation_tests.py \
    --project-root=$example_project_dir \
    --config-path=$example_project_dir/mutation_config
