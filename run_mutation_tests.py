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

import argparse
from argparse import RawTextHelpFormatter

import mutation_operators.boolean
import mutation_operators.statement_deletion

#===============================================================================
# Common definitions
#===============================================================================
TEST_EXECUTION_HOOK_NAME    = 'execute-tests'
SRC_LIST_NAME               = 'src-list'

SEPARATOR_LINE = '============================================================='

#===============================================================================
# Arguments 
#===============================================================================
PARSER = argparse.ArgumentParser(description='A Mutation test tool for C.\n'
                                 '\n'
                                 'See the example_project directory for an\n'
                                 'example on how to set up the tool.',
                                 formatter_class=RawTextHelpFormatter)

PARSER.add_argument('-p', '--project-root',
                    help=
                    'Full path to the root directory of your project (e.g. a\n'
                    'Git repo).',
                    required=True)

PARSER.add_argument('-c', '--config-path',
                    help=
                    'Full path to a directory containing user provided hook\n'
                    'scripts and configuration files.\n'
                    '\n'
                    'This directory should contain the following files:\n'
                    '\n'
                    + TEST_EXECUTION_HOOK_NAME + '\n'
                    '   A script (bash/python/etc) building and running\n'
                    '   your test suite (e.g. by calling Make commands).\n'
                    '\n'
                    + SRC_LIST_NAME + '\n'
                    '   A text file containing a list of source files to\n'
                    '   mutate. Paths starting with "/" are considered\n'
                    '   absolute paths, otherwise they are interpreted\n'
                    '   relative to the project root.',
                    required=True)

ARGS = PARSER.parse_args()

PROJECT_ROOT = ARGS.project_root
CONFIG_PATH  = ARGS.config_path

TEST_EXECUTION_HOOK_PATH    = CONFIG_PATH + '/' + TEST_EXECUTION_HOOK_NAME
SRC_LIST_PATH               = CONFIG_PATH + '/' + SRC_LIST_NAME

print SEPARATOR_LINE
print 'Paths'
print SEPARATOR_LINE
print 'PROJECT_ROOT:             ' , PROJECT_ROOT
print 'CONFIG_PATH:              ' , CONFIG_PATH
print 'TEST_EXECUTION_HOOK_PATH: ' , TEST_EXECUTION_HOOK_PATH
print 'SRC_LIST_PATH:            ' , SRC_LIST_PATH
print ''

#===============================================================================
# Main function
#===============================================================================
def main():
    '''
    Entry point
    '''   

    print SEPARATOR_LINE
    print 'Running mutation'
    print SEPARATOR_LINE
    
    mutator = mutation_operators.boolean.Mutator()

    mutator.run()
   
    mutator = mutation_operators.statement_deletion.Mutator()

    mutator.run()

    print ''

    print SEPARATOR_LINE
    print 'Running user test execution hook script, at: '
    print CONFIG_PATH + '/' + TEST_EXECUTION_HOOK_NAME
    print SEPARATOR_LINE

    os.chdir(CONFIG_PATH)

    subprocess.call(['./' + TEST_EXECUTION_HOOK_NAME])

if __name__ == "__main__":
    sys.exit(main())
