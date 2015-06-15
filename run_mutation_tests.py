#!/usr/bin/env python

"""
Main module
"""

import sys

import mutation_operators.logical
import mutation_operators.statement_deletion

def main():
    print 'main()'

    mutator = mutation_operators.logical.Mutator()

    mutator.run()

    print ''

    mutator = mutation_operators.statement_deletion.Mutator()

    mutator.run()


if __name__ == "__main__":
    sys.exit(main())
