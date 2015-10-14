'''
TBD
'''

import subprocess
import os

from process import args, vars

import util.trace

def run():
    '''
    TBD
    '''
    os.chdir(vars.CONFIG_PATH)

    util.trace.info('Running user test execution hook script at: ' +
                    vars.CONFIG_PATH + '/' +
                    vars.EXECUTE_TESTS_HOOK_NAME)

    subprocess.call(['./' + vars.EXECUTE_TESTS_HOOK_NAME])

    util.trace.info('Finished user test execution')

    test_result_path = vars.OUTPUT_PATH + '/' + vars.TEST_RESULTS

    # Verify that the test results file exists in the output directory
    if os.path.isfile(test_result_path) == False:
        util.trace.exit_error('Could not find test results file: ' +
                              test_result_path)
