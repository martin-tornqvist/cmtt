'''
TBD
'''

import sys
import os
import argparse

from process import settings

import util.log

#===============================================================================
# Argument parsing
#===============================================================================
def parse():
    '''
    Reads and stores user parameters
    '''
    parser = argparse.ArgumentParser(
                    description='CMTT - C Mutation Test Tool.\n'
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
                    + '* ' + settings.EXECUTE_TESTS_HOOK_NAME + '\n'
                    '  A script (bash/python/etc) building and running\n'
                    '  your test suite (e.g. by Make commands).\n'
                    '\n'
                    + '* ' + settings.MUTATION_FILES_NAME + '\n'
                    '  A text file containing a list of source files to \n'
                    '  mutate (absolute paths, or relative to project root).\n'
                    '\n'
                    + '* ' + settings.SRC_BASE_NAME + '\n'
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

    parser.add_argument(
                    '-r', '--report',
                    help=
                    'Instead of running mutation testing, generate a html\n'
                    'report in the output directory.',
                    required=False,
                    action='store_true')

    args = parser.parse_args()

    #===========================================================================
    # Required arguments
    #===========================================================================
    settings.MUTATION_TOOL_ROOT = sys.path[0]

    settings.PROJECT_ROOT = args.project_root

    settings.CONFIG_PATH = args.config_path

    settings.OUTPUT_PATH = args.output_path

    if not os.path.isabs(settings.PROJECT_ROOT):
        util.log.exit_error('Project root path not absolute directory.')

    if not os.path.isabs(settings.CONFIG_PATH):
        util.log.exit_error('Config root path not absolute directory.')

    if not os.path.isabs(settings.OUTPUT_PATH):
        util.log.exit_error('Output path not absolute directory.')

    #===========================================================================
    # Optional arguments
    #===========================================================================
    if args.rng_seed is not None:
        settings.RNG_SEED = args.rng_seed

    if args.global_timeout is not None:
        settings.GLOBAL_TIMEOUT = float(args.global_timeout)

    settings.GEN_REPORTS = args.report

    #===========================================================================
    # Print mode (mutation/report)
    #===========================================================================
    print ''
    print '================================================='
    if settings.GEN_REPORTS:
        print ' Running report mode (no tests will be executed)'
    else:
        print ' Running mutation testing mode'
    print '================================================='

    #===========================================================================
    # Print argument info/confirmation
    #===========================================================================
    util.log.info('Paths:\n' + \
                    ' * PROJECT_ROOT ' + settings.PROJECT_ROOT + '\n' + \
                    ' * CONFIG_PATH  ' + settings.CONFIG_PATH + '\n' + \
                    ' * OUTPUT_PATH  ' + settings.OUTPUT_PATH)

    if settings.GEN_REPORTS:
        util.log.info('Running report mode (no tests will be executed)')
    else:
        # These settings are irrelevant in report mode
        if settings.RNG_SEED:
            util.log.info('Custom RNG seed: ' + settings.RNG_SEED)
        else:
            util.log.info('Using current date as RNG seed')

        util.log.info('Global timeout: ' + str(settings.GLOBAL_TIMEOUT) + 's')
