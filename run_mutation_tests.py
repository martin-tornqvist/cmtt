#!/usr/bin/env python

"""
Main module
"""

import sys

import argparse

import mutation_operators.logical
import mutation_operators.statement_deletion

PARSER = argparse.ArgumentParser(description='Mutation tester for C/C++.')

PARSER.add_argument('--src-root',
                    help='Path to root directory of your project (e.g. '
                    'a Git repo).',
                    required=True)

PARSER.add_argument('--src-list',
                    help='Path to a user provided file which should contain '
                    'a list of source files to mutate. Paths starting with '
                    '"/" are considered absolute paths, otherwise they are '
                    'interpreted relative to the "src-root" argument path.',
                    required=True)

PARSER.add_argument('--test-hook',
                    help='Path to a user provided test execution shell script '
                    '(typically running a Make command).',
                    required=True)

ARGS = PARSER.parse_args()

SRC_ROOT_PATH  = ARGS.src_root
SRC_LIST_PATH  = ARGS.src_list
TEST_HOOK_PATH = ARGS.test_hook

print 'SRC_ROOT_PATH  : ', ARGS.src_root
print 'SRC_LIST_PATH  : ', ARGS.src_list
print 'TEST_HOOK_PATH : ', ARGS.test_hook
print ''

def main():
    '''
    Entry point
    '''

    print 'main()'

    mutator = mutation_operators.logical.Mutator()

    mutator.run()

    print ''

    mutator = mutation_operators.statement_deletion.Mutator()

    mutator.run()

if __name__ == "__main__":
    sys.exit(main())
