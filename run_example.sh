#!/bin/bash

example_path=./example
example_proj_path=$example_path/example_project

./run_mutation_tests.py \
    --src-root=$example_proj_path \
    --src-list=$example_path/filelist \
    --test-hook=$example_path/test_hook.sh
