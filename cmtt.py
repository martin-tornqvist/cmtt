#!/usr/bin/env python

'''
Main module for CMTT (C Mutation Test Tool)
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
import time

import process.args
import process.settings
import process.seq
import process.mutation_testing

import util.log

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
    process.args.parse()

    # Ensure that the output directory exists. Abort the whole execution if it
    # doesn't exist and cannot be created (e.g. we have a permission problem)
    # be created)
    try:
        os.makedirs(process.settings.OUTPUT_PATH)
    except OSError:
        if not os.path.isdir(process.settings.OUTPUT_PATH):
            raise

    #===========================================================================
    # Get tool start time (for global timeout functionality)
    #===========================================================================
    process.settings.TOOL_START_TIME = time.time()

    #===========================================================================
    # Start a new sequence (if the code base has changed, or if this is the
    # first execution ever), or continue an existing. If a new sequence is
    # started, we run an "unmutated" test execution on a clean code base
    # to get results to compare against (a "golden file").
    #===========================================================================
    process.seq.init()

    #===========================================================================
    # Copy style.css to output path
    # TODO: This should be done in a process module
    #===========================================================================
    util.log.info('Copying style.css to output path')

    os.chdir(process.settings.MUTATION_TOOL_ROOT)

    shutil.copy('css/style.css', process.settings.OUTPUT_PATH)
    #===========================================================================

    os.chdir(process.settings.CONFIG_PATH)

    # Init random number generator
    rng = random.Random()

    if process.settings.RNG_SEED:
        util.log.info('Using custom seed: ' + process.settings.RNG_SEED)
        rng.seed(process.settings.RNG_SEED)

    # Read the source source list file into a list
    with open(process.settings.MUTATION_FILES_NAME) as src_list_f:
        src_list = src_list_f.read().splitlines()

    # Filter out empty lines
    src_list = [src_f for src_f in src_list if src_f != '']

    #===========================================================================
    # Run mutation testing until finished or timeout
    #===========================================================================
    process.mutation_testing.run(src_list, rng)

if __name__ == "__main__":
    sys.exit(main())
