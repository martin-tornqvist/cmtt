'''
Functionality for handling diffs
'''

import subprocess
import os

from util import checksum
from util import log

def gen_patch(path_from, path_to, patch_output_path):
    '''
    Generates a diff between two files at given paths, and writes the diff to
    the given output path
    '''
    if not os.path.isfile(path_from):
        log.exit_error('Missing file: ' + path_from)

    if not os.path.isfile(path_to):
        log.exit_error('Missing file: ' + path_to)

    nr_lines_context_str = '2'

    subprocess.call('diff --show-c-function' +
                    ' --label ' + path_from +
                    ' --label ' + path_to +
                    ' -u' + nr_lines_context_str +
                    ' ' + path_from + ' ' + path_to +
                    ' > ' + patch_output_path,
                    shell=True)

def is_patch_applied(file_path, patch_path):
    '''
    Check if a given patch has been applied before on a given file
    '''
    if not os.path.isfile(file_path):
        log.exit_error('Missing file: ' + file_path)

    if not os.path.isfile(patch_path):
        log.exit_error('Missing patch: ' + patch_path)

    return_code = subprocess.call('patch -NR --dry-run ' + file_path + ' ' + \
                                  patch_path + \
                                  ' > /dev/null',
                                  shell=True)

    return return_code == 0

def is_same(path_1, path_2):
    '''
    Returns if files at path_1 and path_2 are equal (by checksum comparison)
    '''
    if not os.path.isfile(path_1):
        log.exit_error('Missing file: ' + path_1)

    if not os.path.isfile(path_2):
        log.exit_error('Missing file: ' + path_2)

    checksum_1 = checksum.get_file_sha1(path_1)
    checksum_2 = checksum.get_file_sha1(path_2)

    return checksum_1 == checksum_2
