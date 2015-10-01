'''
TBD
'''

import subprocess
import os

from proc import filenames
from proc import args

import util.trace

def run():
    '''
    TBD
    '''
    os.chdir(args.CONFIG_PATH)

    util.trace.info('Running user test execution hook script at:' +
        args.CONFIG_PATH + '/' +
        filenames.TEST_EXECUTION_HOOK_NAME)

    subprocess.call(['./' + filenames.TEST_EXECUTION_HOOK_NAME])

    util.trace.info('Finished user test execution')
