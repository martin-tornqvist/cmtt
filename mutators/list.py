'''
This module contains a list of all mutators. This list must be kept up to date
If mutators are added, removed or renamed.
'''

from mutators import boolean, arithmetic, compound_assign, comparison, incr_decr

def get():
    '''
    Returns a list containing an instance of each type of mutator
    '''

    ret = []

    ret.append(boolean.mutate)
    ret.append(arithmetic.mutate)
    ret.append(compound_assign.mutate)
    ret.append(comparison.mutate)
    ret.append(incr_decr.mutate)

    return ret
