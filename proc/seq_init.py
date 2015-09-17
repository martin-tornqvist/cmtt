'''
TBD
'''

import os
import hashlib

import util.trace

from proc import args
from proc import cfg_filenames

def _get_file_sha1(path):
    '''
    TBD
    '''
    blocksize = 4096

    hasher = hashlib.sha1()

    with open(path, 'rb') as file_to_calc:
        buf = file_to_calc.read(blocksize)

        while len(buf) > 0:
            hasher.update(buf)
            buf = file_to_calc.read(blocksize)

    return hasher.hexdigest()


def run():
    '''
    TBD
    '''

    #===========================================================================
    # Get source base sha1 list
    #===========================================================================
    os.chdir(args.CONFIG_PATH)

    with open(cfg_filenames.SRC_LIST_NAME, 'r') as src_list_f:
        src_base_list = src_list_f.read().splitlines()

    with open(cfg_filenames.TEST_SRC_LIST_NAME, 'r') as test_src_list_f:
        src_base_list += test_src_list_f.read().splitlines()

    # Filter out empty lines
    src_base_list = [src_f for src_f in src_base_list if src_f != '']

    os.chdir(args.PROJECT_ROOT)

    sha1_list = []

    for file_path in src_base_list:
        sha1 = _get_file_sha1(file_path)

        sha1_list.append(sha1)

    #===========================================================================
    # TODO: Continue with sequence init
    #===========================================================================
    # TODO: Debug stuff, to be removed...
    os.chdir(args.OUTPUT_PATH)

    with open('src-base-sha1', 'w') as sha1_list_f:
        for sha1 in sha1_list:
            sha1_list_f.write('%s\n' % sha1)

    util.trace.exit_error('Bye!')
