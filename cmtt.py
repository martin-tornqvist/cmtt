#!/usr/bin/env python3.4

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
import time

import process.args
import process.settings
import process.seq
import process.mutation_testing
import process.report

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

    #===========================================================================
    # If dry run flag is set by user, we exit here
    #===========================================================================
    if process.settings.DRY_RUN:
        util.log.info('Everything looks good so far!')
        return

    #===========================================================================
    # Ensure that the output directory exists. Abort the whole execution if it
    # doesn't exist and cannot be created (e.g. we have a permission problem)
    #===========================================================================
    try:
        os.makedirs(process.settings.OUTPUT_PATH)
    except OSError:
        if not os.path.isdir(process.settings.OUTPUT_PATH):
            raise

    #===========================================================================
    # Tool start time (used e.g. for global timeout functionality)
    #===========================================================================
    process.settings.TOOL_START_TIME = time.time()

    #===========================================================================
    # If report flag is set by user, just generate a html report and exit
    #===========================================================================
    if process.settings.GEN_REPORTS:
        process.report.run()
        return

    #===========================================================================
    # Start a new sequence (if the code base has changed, or if this is the
    # first execution ever), or continue an existing. If a new sequence is
    # started, we run an "unmutated" test execution on a clean code base
    # to get results to compare against (a "golden file").
    #===========================================================================
    process.seq.init()

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
