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
import shutil

import proc.args
import proc.cfg_filenames
import proc.seq_init
import proc.test

import mutators.list

import util.trace

#===============================================================================
# Main function
#===============================================================================
def main():
    '''
    Entry point
    '''
    #===========================================================================
    # Parse program arguments and set up global variables (e.g. paths)
    #===========================================================================
    proc.args.parse()

    # Ensure that the output directory exists. Abort the whole execution if it
    # doesn't exist and cannot be created (e.g. we have a permission problem)
    # be created)
    try:
        os.makedirs(proc.args.OUTPUT_PATH)
    except OSError:
        if not os.path.isdir(proc.args.OUTPUT_PATH):
            raise

    #===========================================================================
    # Setup sequence (check if source code base has changed, etc)
    #===========================================================================
    proc.seq_init.run()

    #===========================================================================
    # Copy style.css to output path
    # TODO: This should be done in a process module
    #===========================================================================
    util.trace.info('Copying style.css to output path')

    os.chdir(proc.args.MUTATION_TOOL_ROOT)

    shutil.copy('css/style.css', proc.args.OUTPUT_PATH)
    #===========================================================================

    os.chdir(proc.args.CONFIG_PATH)

    # Init random number generator
    rng = random.Random()

    if proc.args.RNG_SEED:
        util.trace.info('Using custom seed: ' + proc.args.RNG_SEED)
        rng.seed(proc.args.RNG_SEED)

    # Read the source mutator_list file into a list, and shuffle the list
    with open(proc.cfg_filenames.SRC_LIST_NAME) as src_list_f:
        src_list = src_list_f.read().splitlines()

    rng.shuffle(src_list)

    # Get a list of mutators
    mutator_list = mutators.list.get()

    os.chdir(proc.args.PROJECT_ROOT)

    src_file_path = src_list.pop()

    util.trace.empty_line()

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

        util.trace.empty_line()

        util.trace.info('Original line (' + \
                        str(cur_line_nr + 1) + '/' + str(nr_lines) + '):\n' + \
                        src_file_origin_lines[cur_line_nr])

        # TODO: Ignore empty lines, or lines inside comments

        # Try each mutator on the current line
        for mutator in mutator_list:

            # Copy the source file lines
            src_file_working_lines = list(src_file_origin_lines)

            mutate_result = mutator(src_file_working_lines, cur_line_nr, rng)

            if mutate_result == mutators.codes.MUTATE_OK:
                util.trace.info('Line modified by ' + mutator.__module__ +
                                ':\n' + \
                                src_file_working_lines[cur_line_nr])

                util.trace.info('Writing modified source file')

                with open(src_file_path, 'w') as src_f:
                    src_f.write('\n'.join(src_file_working_lines))

                os.chdir(proc.args.CONFIG_PATH)

                util.trace.info('Running user test execution hook script at:' +
                    proc.args.CONFIG_PATH + '/' +
                    proc.cfg_filenames.TEST_EXECUTION_HOOK_NAME)

                proc.test.run()

                os.chdir(proc.args.PROJECT_ROOT)

                util.trace.info('Restoring source file')
                with open(src_file_path, 'w') as src_f:
                    src_f.write(src_file_origin_content)

            else:
                util.trace.info('Line ignored by ' + mutator.__module__)

if __name__ == "__main__":
    sys.exit(main())
