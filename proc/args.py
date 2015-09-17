'''
TBD
'''

import sys
import argparse

from proc import cfg_filenames
import util.trace

#===============================================================================
# Global variables
#===============================================================================
MUTATION_TOOL_ROOT = ''
PROJECT_ROOT = ''
CONFIG_PATH = ''
OUTPUT_PATH = ''
RNG_SEED = ''

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
                    '-p', '--project-root',
                    help=
                    'Absolute path to the root directory of your project\n'
                    '(e.g. a Git repo).',
                    required=True)

    parser.add_argument(
                    '-c', '--config-path',
                    help=
                    'Absolute path to a directory containing user provided\n'
                    'hook scripts and configuration files. When any user\n'
                    'provided script is executed, the current directory is\n'
                    'changed to the configuration directory.\n'
                    '\n'
                    'The configuration directory must contain the\n'
                    'following files:\n'
                    '\n'
                    + '* ' + cfg_filenames.TEST_EXECUTION_HOOK_NAME + '\n'
                    '   A script (bash/python/etc) building and running\n'
                    '   your test suite (e.g. by Make commands).\n'
                    '\n'
                    + '* ' + cfg_filenames.SRC_LIST_NAME + '\n'
                    '   A text file containing a list of source files to \n'
                    '   mutate (absolute paths, or relative to project root).\n'
                    '\n'
                    + '* ' + cfg_filenames.TEST_SRC_LIST_NAME + '\n'
                    '   A text file containing a list of test source files\n'
                    '   (absolute paths, or relative to project root). These\n'
                    '   files are only read to determine if the source code\n'
                    '   base has changed since last test execution.',
                    required=True)

    parser.add_argument(
                    '-o', '--output-path',
                    help=
                    'Absolute path to a directory where reports will be\n'
                    'written. This is also used as a working directory to\n'
                    'store temporary files.',
                    required=True)

    parser.add_argument(
                    '-s', '--rng-seed',
                    help=
                    'Optional custom seed for the random number generator.\n'
                    'Can be useful to deterministically recreate test runs.\n'
                    'If not specified, the current date and time is used.',
                    required=False)

    args = parser.parse_args()

    global MUTATION_TOOL_ROOT
    MUTATION_TOOL_ROOT = sys.path[0]

    global PROJECT_ROOT
    PROJECT_ROOT = args.project_root

    global CONFIG_PATH
    CONFIG_PATH = args.config_path

    global OUTPUT_PATH
    OUTPUT_PATH = args.output_path

    global RNG_SEED
    RNG_SEED = args.rng_seed

    util.trace.info('Paths:\n' + \
                    ' * PROJECT_ROOT ' + PROJECT_ROOT + '\n' + \
                    ' * CONFIG_PATH  ' + CONFIG_PATH + '\n' + \
                    ' * OUTPUT_PATH  ' + OUTPUT_PATH)
