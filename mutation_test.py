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
import proc.mutation_testing

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

    # Read the source source list file into a list, and shuffle the list
    with open(proc.cfg_filenames.SRC_LIST_NAME) as src_list_f:
        src_list = src_list_f.read().splitlines()

    # Filter out empty lines
    src_list = [src_f for src_f in src_list if src_f != '']

    rng.shuffle(src_list)

    # TODO: Check mutation testing result code
    proc.mutation_testing.run(src_list, rng)

if __name__ == "__main__":
    sys.exit(main())
