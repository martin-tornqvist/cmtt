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

    test_results_orig_path = \
        settings.OUTPUT_PATH + '/' + settings.TEST_RESULTS_NAME

    # Verify that no test results exists in the output directory prior to
    # running user tests
    if os.path.isfile(test_results_orig_path):
        util.log.exit_error('User test results exists in output directory '
                            'prior to running user tests: ' +
                            test_results_orig_path)

    util.log.info('Running user test execution hook script at: ' +
                    settings.CONFIG_PATH + '/' +
                    settings.EXECUTE_TESTS_HOOK_NAME)

    subprocess.call(['./' + settings.EXECUTE_TESTS_HOOK_NAME], shell=True)

    util.log.info('Finished user test execution')
