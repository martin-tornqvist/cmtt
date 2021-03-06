'''
Functionality for retrieving checksum of a file
'''

import os
import hashlib

from util import log

def get_file_sha1(path):
    '''
    Returns sha1 of the given file
    '''
    if not os.path.isfile(path):
        log.exit_error('Missing file: ' + path)

    blocksize = 4096

    hasher = hashlib.sha1()

    with open(path, 'rb') as file_to_calc:
        buf = file_to_calc.read(blocksize)

        while len(buf) > 0:
            hasher.update(buf)
            buf = file_to_calc.read(blocksize)

    return hasher.hexdigest()
