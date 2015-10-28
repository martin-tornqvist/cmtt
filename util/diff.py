'''
Functionality for handling diffs
'''

import subprocess
import os

from util import checksum, trace

def gen_patch(path_from, path_to, patch_output_path):
    '''
    Generates a diff between two files at given paths, and writes the diff to
    the given output path
    '''
    if not os.path.isfile(path_from):
        trace.exit_error('File missing when trying to generate patch: ' +
                         path_from)

    if not os.path.isfile(path_to):
        trace.exit_error('File missing when trying to generate patch: ' +
                         path_to)

    nr_lines_context_str = '5'

    subprocess.call('diff -u' + nr_lines_context_str + ' ' +
                    path_from + ' ' + path_to +
                    ' > ' + patch_output_path,
                    shell=True)

def is_same(path_1, path_2):
    '''
    Returns if files at path_1 and path_2 are equal (by checksum comparison)
    '''
    if not os.path.isfile(path_1):
        trace.exit_error('File missing when check file equality: ' + path_1)

    if not os.path.isfile(path_2):
        trace.exit_error('File missing when check file equality: ' + path_2)

    checksum_1 = checksum.get_file_sha1(path_1)
    checksum_2 = checksum.get_file_sha1(path_2)

    return checksum_1 == checksum_2
