'''
TBD
'''

import sys

def info(text):
    '''TBD'''
    empty_line()
    print '>>> ' + text

def empty_line():
    '''TBD'''
    print ''

def exit_error(text):
    '''TBD'''
    empty_line()
    print 'ERROR: ' + text
    sys.exit()
