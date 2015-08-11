#!/usr/bin/env python

"""
Main module
"""

#
# TODO: Do a sanity check of the config-path directory somewhere
# (are all necessary files there?)
#

#===============================================================================
# Imports
#===============================================================================
import sys
import os
import subprocess
import random

import argparse
from argparse import RawTextHelpFormatter

import mutators.boolean

#===============================================================================
# Common definitions
#===============================================================================
TEST_EXECUTION_HOOK_NAME    = 'execute-tests'
SRC_LIST_NAME               = 'src-list'

#===============================================================================
# Arguments
#===============================================================================
PARSER = argparse.ArgumentParser(
                    description='A Mutation testing tool for C.\n'
                    '\n'
                    'See the example_project directory for an example on how\n'
                    'to set up the tool.',
                    formatter_class = RawTextHelpFormatter)

PARSER.add_argument('-p', '--project-root',
                    help=
                    'Absolute path to the root directory of your project\n'
                    '(e.g. a Git repo).',
                    required = True)

PARSER.add_argument('-c', '--config-path',
                    help=
                    'Absolute path to a directory containing user provided\n'
                    'hook scripts and configuration files.\n'
                    '\n'
                    'This directory should contain the following files:\n'
                    '\n'
                    + '"' + TEST_EXECUTION_HOOK_NAME + '"' + '\n'
                    '   A script (bash/python/etc) building and running\n'
                    '   your test suite (e.g. by Make commands).\n'
                    '\n'
                    + '"' + SRC_LIST_NAME + '"' + '\n'
                    '   A text file containing a list of source files to\n'
                    '   mutate (absolute paths, or relative to project root).',
                    required = True)

PARSER.add_argument('-o', '--output-path',
                    help=
                    'Absolute path to a directory where reports will be\n'
                    'written. This is also used as a working directory to\n'
                    'store temporary files.',
                    required = True)

PARSER.add_argument('-s', '--rng-seed',
                    help=
                    'Optional custom seed for the random number generator.\n'
                    'Can be useful to deterministically recreate test runs.',
                    required = False)

ARGS = PARSER.parse_args()

PROJECT_ROOT = ARGS.project_root
CONFIG_PATH  = ARGS.config_path
OUTPUT_PATH  = ARGS.output_path
RNG_SEED     = ARGS.rng_seed

print 'Paths:'
print ' * PROJECT_ROOT ' , PROJECT_ROOT
print ' * CONFIG_PATH  ' , CONFIG_PATH
print ' * OUTPUT_PATH  ' , OUTPUT_PATH

#===============================================================================
# Main function
#===============================================================================
def main():
    '''
    Entry point
    '''  
    os.chdir(CONFIG_PATH)

    # Init RNG
    rng = random.Random()

    if RNG_SEED:
        print 'Using custom seed: ' + RNG_SEED
        rng.seed(RNG_SEED)

    # Read the source list file, and shuffle the list
    with open(SRC_LIST_NAME) as src_list_f:
        src_list = src_list_f.read().splitlines()

    rng.shuffle(src_list)

    os.chdir(PROJECT_ROOT)

    # Get the last source file in the list, and erase that entry
    src_file_rel_path = src_list.pop(-1)

    print ''
    print 'Source file to mutate: ' + src_file_rel_path

    # Make a list of possible mutators, and shuffle the list
    mutator_list = [mutators.boolean.Mutator()]

    rng.shuffle(mutator_list)

    # Get the last source file in the list, and erase that entry
    mutator = mutator_list.pop(-1)

    print ''
    print 'Attempting to apply mutator: ' + mutator.__module__
    mutator.run()

    print ''
    print 'Mutation successful!'

    print ''
    print 'Running user test execution hook script at: ' + \
        CONFIG_PATH + '/' + TEST_EXECUTION_HOOK_NAME

    os.chdir(CONFIG_PATH)

    subprocess.call(['./' + TEST_EXECUTION_HOOK_NAME])

if __name__ == "__main__":
    sys.exit(main())
