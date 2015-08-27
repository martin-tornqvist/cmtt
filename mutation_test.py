#!/usr/bin/env python

'''
Main module
'''

#
# TODO: Do a sanity check of the config-path directory somewhere to make sure
# all necessary files are there.
#

#===============================================================================
# Imports
#===============================================================================
import sys
import os
import random
import argparse

import mutators.list

import proc.paths
import proc.test

import util.trace

#===============================================================================
# Arguments
#===============================================================================
PARSER = argparse.ArgumentParser(
                    description='A Mutation testing tool for C.\n'
                    '\n'
                    'See the example_project directory for an example on how\n'
                    'to set up the tool.',
                    formatter_class=argparse.RawTextHelpFormatter)

PARSER.add_argument(
                    '-p', '--project-root',
                    help=
                    'Absolute path to the root directory of your project\n'
                    '(e.g. a Git repo).',
                    required=True)

PARSER.add_argument(
                    '-c', '--config-path',
                    help=
                    'Absolute path to a directory containing user provided\n'
                    'hook scripts and configuration files. When any user\n'
                    'provided script is executed, the current directory is\n'
                    'changed to the configuration directory.\n'
                    '\n'
                    'The configuration directory should contain the\n'
                    'following files:\n'
                    '\n'
                    + '"' + proc.paths.TEST_EXECUTION_HOOK_NAME + '"' + '\n'
                    '   A script (bash/python/etc) building and running\n'
                    '   your test suite (e.g. by Make commands).\n'
                    '\n'
                    + '"' + proc.paths.SRC_LIST_NAME + '"' + '\n'
                    '   A text file containing a mutator_list of source\n'
                    '   files to mutate (absolute paths, or relative to\n'
                    '   project root)',
                        required=True)

PARSER.add_argument(
                    '-o', '--output-path',
                    help=
                    'Absolute path to a directory where reports will be\n'
                    'written. This is also used as a working directory to\n'
                    'store temporary files.',
                    required=True)

PARSER.add_argument(
                    '-s', '--rng-seed',
                    help=
                    'Optional custom seed for the random number generator.\n'
                    'Can be useful to deterministically recreate test runs.\n'
                    'If not specified, the current date and time is used.',
                    required=False)

ARGS = PARSER.parse_args()

PROJECT_ROOT = ARGS.project_root
CONFIG_PATH = ARGS.config_path
OUTPUT_PATH = ARGS.output_path
RNG_SEED = ARGS.rng_seed

util.trace.info('Paths:\n' + \
                ' * PROJECT_ROOT ' + PROJECT_ROOT + '\n' + \
                ' * CONFIG_PATH  ' + CONFIG_PATH + '\n' + \
                ' * OUTPUT_PATH  ' + OUTPUT_PATH)

#===============================================================================
# Main function
#===============================================================================
def main():
    '''
    Entry point
    '''
    os.chdir(CONFIG_PATH)

    # Init random number generator
    rng = random.Random()

    if RNG_SEED:
        util.trace.info('Using custom seed: ' + RNG_SEED)
        rng.seed(RNG_SEED)

    # Read the source mutator_list file into a list, and shuffle the list
    with open(proc.paths.SRC_LIST_NAME) as src_list_f:
        src_list = src_list_f.read().splitlines()

    rng.shuffle(src_list)

    # Get a list of mutators
    mutator_list = mutators.list.get()

    os.chdir(PROJECT_ROOT)

    src_file_path = src_list.pop()

    util.trace.empty_lines()

    util.trace.info('Current source file to mutate: ' + src_file_path)

    # Verify that the file exists
    if os.path.isfile(src_file_path) == False:
        util.trace.exit_error('Could not find ' + src_file_path)

    # Read the source file
    with open(src_file_path, 'r') as src_f:
        src_file_origin_content = src_f.read()

    src_file_origin_lines = src_file_origin_content.splitlines()

    nr_lines = len(src_file_origin_lines)

    util.trace.info('Read ' + str(nr_lines) + ' lines')

    # Iterate over each line in the source file
    for cur_line_nr in range(0, nr_lines):

        util.trace.empty_lines()

        util.trace.info('Original line (' + \
                        str(cur_line_nr + 1) + '/' + str(nr_lines) + '):\n' + \
                        src_file_origin_lines[cur_line_nr])

        # Try each mutator on the current line
        for mutator in mutator_list:

            # Copy the source file lines
            src_file_working_lines = list(src_file_origin_lines)

            util.trace.info('Attempting to apply "' + mutator.__module__ + '"')
            mutate_result = mutator.run(src_file_working_lines,
                                        cur_line_nr, rng)

            if mutate_result == mutators.codes.MUTATE_OK:
                util.trace.info('Modified line:\n' + \
                                src_file_working_lines[cur_line_nr])

                util.trace.info('Writing modified source file')

                with open(src_file_path, 'w') as src_f:
                    src_f.write('\n'.join(src_file_working_lines))

                os.chdir(CONFIG_PATH)

                util.trace.info('Running user test execution hook script at:' +
                    CONFIG_PATH + '/' + proc.paths.TEST_EXECUTION_HOOK_NAME)

                proc.test.run()

                os.chdir(PROJECT_ROOT)

                util.trace.info('Restoring source file')
                with open(src_file_path, 'w') as src_f:
                    src_f.write(src_file_origin_content)

            else:
                util.trace.info('Line ignored by mutator')

if __name__ == "__main__":
    sys.exit(main())
