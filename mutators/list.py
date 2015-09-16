'''
This module contains a list of all mutators. This list must be kept up to date
If mutators are added, removed or renamed.
'''

import mutators.boolean
import mutators.arithmetic
import mutators.compound_assign

def get():
    '''
    Returns a list containing an instance of each type of mutator
    '''

    ret = []

    ret.append(mutators.boolean.mutate)
    ret.append(mutators.arithmetic.mutate)
    ret.append(mutators.compound_assign.mutate)

    return ret
