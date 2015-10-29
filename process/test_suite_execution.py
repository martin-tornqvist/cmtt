'''
TBD
'''

import subprocess
import os

from process import settings

import util.log

def run():
    '''
    TBD
    '''
    os.chdir(settings.CONFIG_PATH)

    util.log.info('Running user test execution hook script at: ' +
                    settings.CONFIG_PATH + '/' +
                    settings.EXECUTE_TESTS_HOOK_NAME)

    subprocess.call(['./' + settings.EXECUTE_TESTS_HOOK_NAME], shell=True)

    util.log.info('Finished user test execution')

    test_result_path = settings.OUTPUT_PATH + '/' + settings.TEST_RESULTS_NAME

    # Verify that the test results file exists in the output directory
    if os.path.isfile(test_result_path) == False:
        util.log.exit_error('Missing test results file: ' + test_result_path)
