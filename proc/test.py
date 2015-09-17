'''
TBD
'''

import subprocess

from proc import cfg_filenames

def run():
    '''
    TBD
    '''
    subprocess.call(['./' + cfg_filenames.TEST_EXECUTION_HOOK_NAME])
