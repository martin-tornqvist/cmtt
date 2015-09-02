'''
TBD
'''

import re

def strip_escapes(line):
    '''
    TBD
    '''
    return line.replace('\\', '')

def match_list(re_str, line):
    pattern = re.compile(re_str)

    match_iterator = re.finditer(pattern, line)

    return list(match_iterator)
