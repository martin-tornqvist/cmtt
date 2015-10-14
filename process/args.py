'''
TBD
'''

import sys
import argparse

from process import vars

import util.trace

#===============================================================================
# Argument parsing
#===============================================================================
def parse():
    '''
    TBD
    '''
    parser = argparse.ArgumentParser(
                    description='A Mutation testing tool for C.\n'
                    '\n'
                    'See the example_project directory for an example on how\n'
                    'to set up the tool.',
                    formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument(
                    '-c', '--config-path',
                    help=
                    'Absolute path to a directory containing user provided\n'
                    'hook scripts and configuration files. This directory\n'
                    'must contain the following files:\n'
                    '\n'
                    + '* ' + vars.EXECUTE_TESTS_HOOK_NAME + '\n'
                    '  A script (bash/python/etc) building and running\n'
                    '  your test suite (e.g. by Make commands).\n'
                    '\n'
                    + '* ' + vars.MUTATION_FILES_NAME + '\n'
                    '  A text file containing a list of source files to \n'
                    '  mutate (absolute paths, or relative to project root).\n'
                    '\n'
                    + '* ' + vars.SRC_BASE_NAME + '\n'
                    '  A text file containing a list of files constituting\n'
                    '  your source code base (absolute paths, or relative\n'
                    '  to project root). This can (or should) include both\n'
                    '  your code under test, and your test code. These\n'
                    '  files are read to determine if the source code base\n'
                    '  has changed since the last test execution (which\n'
                    '  will trigger a new test sequence).',
                    required=True)

    parser.add_argument(
                    '-o', '--output-path',
                    help=
                    'Absolute path to a directory where reports will be\n'
                    'written. This is also used as a working directory to\n'
                    'store temporary files.',
                    required=True)

    parser.add_argument(
                    '-p', '--project-root',
                    help=
                    'Absolute path to the root directory of your project\n'
                    '(e.g. a Git repo).',
                    required=True)

    parser.add_argument(
                    '-s', '--rng-seed',
                    help=
                    'Optional custom seed for the random number generator.\n'
                    'Can be useful to deterministically recreate test runs.\n'
                    'If not specified, the current date and time is used.',
                    required=False)

    parser.add_argument(
                    '-T', '--global-timeout',
                    help=
                    'How many seconds the tool should be kept running (the\n'
                    'number of possible mutations is practically endless, so\n'
                    'you will want to abort execution at some point, and\n'
                    'perhaps resume testing another day.',
                    required=False)

    args = parser.parse_args()

    #===========================================================================
    # Required arguments
    #===========================================================================
    vars.MUTATION_TOOL_ROOT = sys.path[0]

    vars.PROJECT_ROOT = args.project_root

    vars.CONFIG_PATH = args.config_path

    vars.OUTPUT_PATH = args.output_path

    #===========================================================================
    # Optional arguments
    #===========================================================================
    if args.rng_seed is not None:
        vars.RNG_SEED = args.rng_seed

    if args.global_timeout is not None:
        vars.GLOBAL_TIMEOUT = float(args.global_timeout)

    #===========================================================================
    # Print argument info/confirmation
    #===========================================================================
    util.trace.info('Paths:\n' + \
                    ' * PROJECT_ROOT ' + vars.PROJECT_ROOT + '\n' + \
                    ' * CONFIG_PATH  ' + vars.CONFIG_PATH + '\n' + \
                    ' * OUTPUT_PATH  ' + vars.OUTPUT_PATH)

    if vars.RNG_SEED:
        util.trace.info('Custom RNG seed: ' + vars.RNG_SEED)
    else:
        util.trace.info('Using current date as RNG seed')

    util.trace.info('Global timeout: ' + str(vars.GLOBAL_TIMEOUT) + 's')
