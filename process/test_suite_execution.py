'''
TBD
'''

import subprocess
import os

from process import args, filenames

import util.trace

def run():
    '''
    TBD
    '''
    os.chdir(args.CONFIG_PATH)

    util.trace.empty_line()
    util.trace.info('Running user test execution hook script at: ' +
                    args.CONFIG_PATH + '/' +
                    filenames.EXECUTE_TESTS_HOOK_NAME)

    subprocess.call(['./' + filenames.EXECUTE_TESTS_HOOK_NAME])

    util.trace.empty_line()
    util.trace.info('Finished user test execution')

    test_result_path = args.OUTPUT_PATH + '/' + filenames.TEST_RESULTS

    # Verify that the test results file exists in the output directory
    if os.path.isfile(test_result_path) == False:
        util.trace.exit_error('Could not find test results file: ' +
                              test_result_path)
