'''
TBD
'''

import sys
import traceback

def info(text):
    '''TBD'''
    empty_line()
    print('>>> ' + text)

def empty_line():
    '''TBD'''
    print('')

def exit_error(text):
    '''TBD'''
    empty_line()

    print('')
    print('ERROR: ' + text)
    print('')

    print(traceback.print_stack())

    sys.exit(1)
