'''
Functionality for handling sequences. This includes deciding if a new sequence
should be started (and if so, initialize it), or continue an old one. It also
includes providing sequence information such as check which diffs has been
applied before.
'''

import os
import re
import datetime
import shutil

from process import vars, test_suite_execution

import util.trace
import util.checksum

def init():
    '''
    TBD
    '''
    src_base_sha1_list = _get_src_base_sha1_list()

    cur_seq_dir_name = _get_ongoing_seq_dir_name()

    if cur_seq_dir_name:
        vars.CUR_SEQ_DIR = vars.OUTPUT_PATH + '/' + cur_seq_dir_name
        vars.CUR_SEQ_DIR = _verify_ongoing_seq(src_base_sha1_list)

    if vars.CUR_SEQ_DIR:
        util.trace.info('Continuing previous sequence: ' + vars.CUR_SEQ_DIR)
    else:
        # No previous sequence available to continue from - start a new one
        # NOTE: This will set the current sequence directory path
        _start_new_seq(src_base_sha1_list)

    # Assert that a sequence directory has been set at this point
    if not os.path.isdir(vars.CUR_SEQ_DIR):
        util.trace.exit_error('Failed to find/create sequence directory')

    if not os.path.isabs(vars.CUR_SEQ_DIR):
        util.trace.exit_error('Sequence directory not absolute: ' +
                              vars.CUR_SEQ_DIR)

def is_patch_applied_cur_seq(patch_path):
    '''
    Check if a given patch has already been applied in the current sequence.
    '''
    # TODO Implement this
    return False

def mk_mut_serial_dir():
    '''
    Creates a new serial numbered directory to put mutation data and results in.
    '''
    if not os.path.isdir(vars.CUR_SEQ_DIR):
        util.trace.exit_error('Missing sequence directory when trying to ' +
                              'create mutation output serial number directory')

    os.chdir(vars.CUR_SEQ_DIR)

    # Get a list of existing mutation directories
    mut_dirs = os.listdir('.')

    # Strip non-digit directories (not mutation serial directories)
    mut_dirs = [dir_name for dir_name in mut_dirs if dir_name.isdigit()]

    def numeric_compare(element_1, element_2):
        return int(element_1) - int(element_2)

    mut_dirs.sort(cmp=numeric_compare)

    serial_nr = -1

    for mut_dir in mut_dirs:
        dir_name = str(mut_dir)

        if dir_name.isdigit():
            serial_nr = int(dir_name)

    serial_nr += 1

    serial_dir_name = str(serial_nr)

    if os.path.isdir(serial_dir_name):
        util.trace.exit_error('Mutation output serial number directory ' +
                              'already exists: ' + serial_dir_name)

    os.mkdir(serial_dir_name)

    vars.CUR_MUTATION_DIR = vars.CUR_SEQ_DIR + '/' + serial_dir_name

    util.trace.info('Created new mutation serial directory at: ' +
                    vars.CUR_MUTATION_DIR)

def _start_new_seq(src_base_sha1_list):
    '''
    Creates a new sequence directory, sets the sequence directory path, and
    runs a "clean" test execution and stores the "golden" test output.
    '''
    os.chdir(vars.OUTPUT_PATH)

    seq_dir_name = _mk_new_seq_dir()

    vars.CUR_SEQ_DIR = vars.OUTPUT_PATH + '/' + seq_dir_name

    util.trace.info('New sequence: ' + seq_dir_name)

    os.chdir(vars.CUR_SEQ_DIR)

    with open(vars.SRC_BASE_SHA1, 'w') as sha1_f:
        for sha1 in src_base_sha1_list:
            sha1_f.write("%s\n" % sha1)

    # Perform a test execution with unmodified source code, to get a clean
    # ("golden") test output that we can compare against.
    test_suite_execution.run()

    os.chdir(vars.OUTPUT_PATH)

    clean_result_orig_path = vars.OUTPUT_PATH + '/' + vars.TEST_RESULTS

    clean_result_dst_path = vars.CUR_SEQ_DIR + '/' + vars.CLEAN_TEST_RESULTS

    shutil.copy(clean_result_orig_path, clean_result_dst_path)

    # Verify that the file was copied to the sequence directory
    if os.path.isfile(clean_result_dst_path) == False:
        util.trace.exit_error('Could not copy test results to: ' +
                              clean_result_dst_path)

    os.remove(clean_result_orig_path)

def _verify_ongoing_seq(src_base_sha1_list):
    '''
    Compares the current source code base to the source base for the ongoing
    sequence directory. If a mismatch is found, the sequence directory is set to
    an empty variable.
    '''
    # If an ongoing sequence was found, check if sha1 of that sequence match
    # the current source base
    if vars.CUR_SEQ_DIR:
        os.chdir(vars.CUR_SEQ_DIR)

        if not os.path.isfile(vars.SRC_BASE_SHA1):
            util.trace.exit_error('File "' + vars.SRC_BASE_SHA1 + '" ' + \
                                  'missing from sequence directory: ' + \
                                  vars.CUR_SEQ_DIR)

        with open(vars.SRC_BASE_SHA1, 'r') as sha1_f:
            sha1_f_content = sha1_f.read()

        seq_sha1_list = sha1_f_content.splitlines()

        if seq_sha1_list != src_base_sha1_list:
            util.trace.info('Source base sha1 list differs from sha1 list ' + \
                            'of ongoing sequence')

            # "Finalize" the ongoing sequence by adding an end date suffix to
            # the directory name
            new_dir_name = vars.CUR_SEQ_DIR + _get_cur_date_str()

            util.trace.info('Renaming ' + vars.CUR_SEQ_DIR + ' to ' +
                            new_dir_name + ' (finalized)')

            os.chdir(vars.OUTPUT_PATH)

            os.rename(vars.CUR_SEQ_DIR, new_dir_name)

            # Reset current sequence directory string to trigger creation of
            # a new sequence
            vars.CUR_SEQ_DIR = ''

    return vars.CUR_SEQ_DIR


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
        sha1 = util.checksum.get_file_sha1(file_path)

        src_base_sha1_list.append(sha1)

    if not src_base_sha1_list:
        util.trace.exit_error('Failed to read sha1 list for source base')

    return src_base_sha1_list

def _get_ongoing_seq_dir_name():
    '''
    TBD
    '''
    os.chdir(vars.OUTPUT_PATH)

    subdirs = os.listdir('.')

    # Find sub directories of the form:
    # "year-month-day-minute-second-microsecond"
    # Note:                       YYYY- MM- DD . hh . mm . ss-
    ongoing_seq_dir_pattern = r'^\d...-\d.-\d.\.\d.\.\d.\.\d.-$'

    cur_dir_name = ''

    # Search for a sub directory matching the ongoing sequence pattern
    for subdir in subdirs:
        if os.path.isdir(subdir) and re.match(ongoing_seq_dir_pattern, subdir):
            cur_dir_name = subdir
            break

    return cur_dir_name

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
