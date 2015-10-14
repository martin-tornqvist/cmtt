'''
TBD
'''

import os
import hashlib
import re
import datetime
import shutil

from process import args, vars, test_suite_execution

import util.trace

def run():
    '''
    TBD
    '''
    src_base_sha1_list = _get_src_base_sha1_list()

    cur_seq_dir = _get_ongoing_seq_dir()

    cur_seq_dir = _verify_ongoing_seq(cur_seq_dir, src_base_sha1_list)

    if cur_seq_dir:
        util.trace.info('Continuing previous sequence: ' + cur_seq_dir)
    else:
        # No previous sequence available to continue from - start a new one
        cur_seq_dir = _start_new_seq(cur_seq_dir, src_base_sha1_list)

    # Assert that a sequence directory has been set at this point
    if not cur_seq_dir:
        util.trace.exit_error('Failed to find/create sequence directory')

def _start_new_seq(dir_name, src_base_sha1_list):
    '''
    TBD
    '''
    os.chdir(vars.OUTPUT_PATH)

    dir_name = _mk_new_seq_dir()

    util.trace.info('New sequence: ' + dir_name)

    os.chdir(dir_name)

    with open(vars.SRC_BASE_SHA1, 'w') as sha1_f:
        for sha1 in src_base_sha1_list:
            sha1_f.write("%s\n" % sha1)

    # Perform a test execution with unmodified source code, to get a clean
    # ("golden") test output that we can compare against.
    test_suite_execution.run()

    os.chdir(vars.OUTPUT_PATH)

    clean_result_orig_path = vars.OUTPUT_PATH + '/' + vars.TEST_RESULTS

    clean_result_dst_path = vars.OUTPUT_PATH + '/' + dir_name + '/' + \
                            vars.CLEAN_TEST_RESULTS

    shutil.copy(clean_result_orig_path, clean_result_dst_path)

    # Verify that the file was copied to the sequence directory
    if os.path.isfile(clean_result_dst_path) == False:
        util.trace.exit_error('Could not copy test results to: ' +
                              clean_result_dst_path)

    os.remove(clean_result_orig_path)

    return dir_name

def _verify_ongoing_seq(dir_name, src_base_sha1_list):
    '''
    TBD
    '''
    # If an ongoing sequence was found, check if sha1 of that sequence match
    # the current source base
    if dir_name:
        os.chdir(dir_name)

        if not os.path.isfile(vars.SRC_BASE_SHA1):
            util.trace.exit_error('File "' + vars.SRC_BASE_SHA1 + '" ' + \
                                  'missing from sequence directory: ' + \
                                  dir_name)

        with open(vars.SRC_BASE_SHA1, 'r') as sha1_f:
            sha1_f_content = sha1_f.read()

        seq_sha1_list = sha1_f_content.splitlines()

        if seq_sha1_list != src_base_sha1_list:
            util.trace.info('Source base sha1 list differs from sha1 list ' + \
                            'of ongoing sequence')

            # "Finalize" the ongoing sequence by adding an end date suffix to
            # the directory name
            new_dir_name = dir_name + _get_cur_date_str()

            util.trace.info('Renaming ' + dir_name + ' to ' +
                            new_dir_name + ' (finalized)')

            os.chdir(vars.OUTPUT_PATH)

            os.rename(dir_name, new_dir_name)

            # Reset current sequence directory string to trigger creation of
            # a new sequence
            dir_name = ''

    return dir_name


def _get_src_base_sha1_list():
    '''
    TBD
    '''
    os.chdir(vars.CONFIG_PATH)

    with open(vars.SRC_BASE_NAME, 'r') as src_list_f:
        src_base_list = src_list_f.read().splitlines()

    # Filter out empty lines
    src_base_list = [src_f for src_f in src_base_list if src_f != '']

    os.chdir(vars.PROJECT_ROOT)

    src_base_sha1_list = []

    for file_path in src_base_list:
        sha1 = _get_file_sha1(file_path)

        src_base_sha1_list.append(sha1)

    if not src_base_sha1_list:
        util.trace.exit_error('Failed to read sha1 list for source base')

    return src_base_sha1_list

def _get_ongoing_seq_dir():
    '''
    TBD
    '''
    os.chdir(vars.OUTPUT_PATH)

    subdirs = os.listdir('.')

    # Find sub directories of the form:
    # "year-month-day-minute-second-microsecond"
    # Note:                       YYYY- MM- DD . hh . mm . ss-
    ongoing_seq_dir_pattern = r'^\d...-\d.-\d.\.\d.\.\d.\.\d.-$'

    cur_seq_dir = ''

    # Search for a sub directory matching the ongoing sequence pattern
    for subdir in subdirs:
        if os.path.isdir(subdir) and re.match(ongoing_seq_dir_pattern, subdir):
            cur_seq_dir = subdir
            break

    return cur_seq_dir

def _get_file_sha1(path):
    '''
    TBD
    '''
    if not os.path.isfile(path):
        util.trace.exit_error('File missing when trying to read sha1: ' + path)

    blocksize = 4096

    hasher = hashlib.sha1()

    with open(path, 'rb') as file_to_calc:
        buf = file_to_calc.read(blocksize)

        while len(buf) > 0:
            hasher.update(buf)
            buf = file_to_calc.read(blocksize)

    return hasher.hexdigest()

def _mk_new_seq_dir():
    '''
    TBD
    '''
    dir_name = _get_cur_date_str() + '-'

    os.mkdir(dir_name)

    return dir_name

def _get_cur_date_str():
    '''
    TBD
    '''
    return datetime.datetime.today().strftime("%Y-%m-%d.%H.%M.%S")
