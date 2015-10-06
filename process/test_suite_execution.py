'''
TBD
'''

import subprocess
import os

from process import filenames
from process import args

import util.trace

def run():
    '''
    TBD
    '''
    os.chdir(args.CONFIG_PATH)

    util.trace.info('Running user test execution hook script at:' +
        args.CONFIG_PATH + '/' +
        filenames.EXECUTE_TESTS_HOOK_NAME)

    subprocess.call(['./' + filenames.EXECUTE_TESTS_HOOK_NAME])

    util.trace.info('Finished user test execution')
