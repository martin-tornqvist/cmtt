'''
Functionality for handling sequences. This includes deciding if a new sequence
should be started (and if so, initialize it), or continue an old one. It also
provides sequence information such as check which diffs has been applied before.
'''

import os
import re
import datetime
import shutil
import functools

from process import user_tests
from process import settings

import util.log
import util.checksum
import util.diff

#===============================================================================
# Regex patterns for finding sequence directories
#===============================================================================
# Any sequence directory:
# "[year][month][day].[hour].[minute].[second]-*"
#                     YYYY MM DD . hh . mm . ss-*
SEQ_DIR_PATTERN = r'^\d...\d.\d.\.\d.\.\d.\.\d.-.*'

# Finalized sequence directory:
# "[year][month][day].[hour].[minute].[second]-[year]*"
#                               YYYY MM DD . hh . mm . ss- YYYY*
FINALIZED_SEQ_DIR_PATTERN = r'^\d...\d.\d.\.\d.\.\d.\.\d.-\d....*'

# Ongoing sequence directory:
# "[year][month][day].[hour].[minute].[second]-"
#                             YYYY MM DD . hh . mm . ss-
ONGOING_SEQ_DIR_PATTERN = r'^\d...\d.\d.\.\d.\.\d.\.\d.-$'

# Date format for sequence directories (for converting between timestamps
# and strings)
SEQ_DIR_DATE_FORMAT = "%Y%m%d.%H.%M.%S"

def init():
    '''
    TBD
    '''
    src_base_sha1_list = _get_src_base_sha1_list()

    cur_seq_dir_path = get_ongoing_seq_dir_name()

    if cur_seq_dir_path:
        settings.CUR_SEQ_DIR = cur_seq_dir_path
        settings.CUR_SEQ_DIR = _verify_ongoing_seq(src_base_sha1_list)

    if settings.CUR_SEQ_DIR:
        util.log.info('Continuing previous sequence: ' + settings.CUR_SEQ_DIR)
    else:
        # No previous sequence available to continue from - start a new one
        # NOTE: This will set the current sequence directory path
        _start_new_seq(src_base_sha1_list)

    # Assert that a sequence directory has been set at this point
    if not os.path.isdir(settings.CUR_SEQ_DIR):
        util.log.exit_error('Failed to find/create sequence directory')

    if not os.path.isabs(settings.CUR_SEQ_DIR):
        util.log.exit_error('Sequence directory not absolute: ' +
                              settings.CUR_SEQ_DIR)

def get_ongoing_seq_dir_name():
    '''
    Searches for an ongoing sequence directory (i.e. a directory named with a
    start time prefix and no end time suffix, found in the output directory)
    '''
    os.chdir(settings.OUTPUT_PATH)

    subdirs = os.listdir('.')

    ongoing_dir_path = ''

    # Search for a sub directory matching the ongoing sequence pattern
    for subdir in subdirs:
        if os.path.isdir(subdir) and re.match(ONGOING_SEQ_DIR_PATTERN, subdir):
            ongoing_dir_path = settings.OUTPUT_PATH + '/' + subdir
            break

    return ongoing_dir_path

def get_seq_dirs():
    '''
    TBD
    '''
    os.chdir(settings.OUTPUT_PATH)

    dir_content = os.listdir('.')

    sub_dir_paths = []

    # Search for sub directories matching the sequence pattern
    for entry in dir_content:
        if os.path.isdir(entry) and _is_seq_dir(entry):
                sub_dir_paths.append(entry)

    return sub_dir_paths

def is_seq_finalized(path):
    '''
    Determines if a sequence is finalized by reading the directory name
    '''
    if not os.path.isdir(path):
        util.log.exit_error('Path does not exist, or not a directory: ' +
                            path)

    dir_name = os.path.basename(path)

    return re.match(FINALIZED_SEQ_DIR_PATTERN, dir_name)

def get_seq_start_date(path):
    '''
    Determines sequence start date by reading the directory name
    '''
    if not os.path.isdir(path):
        util.log.exit_error('Path does not exist, or not a directory: ' +
                            path)

    if not _is_seq_dir(path):
        util.log.exit_error('Not a sequence directory: ' + path)

    dir_name = os.path.basename(path)

    start_str = dir_name.split('-')[0]

    date = datetime.datetime.today().strptime(start_str, SEQ_DIR_DATE_FORMAT)

    return date

def get_seq_end_date(path):
    '''
    Determines sequence end date by reading the directory name
    '''
    if not os.path.isdir(path):
        util.log.exit_error('Path does not exist, or not a directory: ' +
                            path)

    if not _is_seq_dir(path):
        util.log.exit_error('Not a sequence directory: ' + path)

    if not is_seq_finalized(path):
        util.log.exit_error('Sequence directory not finalized: ' + path)

    dir_name = os.path.basename(path)

    end_str = dir_name.split('-')[1]

    date = datetime.datetime.today().strptime(end_str, SEQ_DIR_DATE_FORMAT)

    return date

def is_patch_applied_cur_seq(file_path, patch_path):
    '''
    Check if a given patch has already been applied in the current sequence.
    '''
    if not os.path.isfile(file_path):
        util.log.exit_error('Missing file: ' + file_path)

    if not os.path.isfile(patch_path):
        util.log.exit_error('Missing patch: ' + patch_path)

    # Assuming absolute paths
    if not os.path.isabs(file_path):
        util.log.exit_error('Not absolute path: ' + file_path)

    if not os.path.isabs(patch_path):
        util.log.exit_error('Not absolute path: ' + patch_path)

    if not os.path.isdir(settings.CUR_SEQ_DIR):
        util.log.exit_error('Missing sequence directory')

    mut_dirs = _get_mut_serial_dirs()

    for mut_dir_name in mut_dirs:

        compare_patch_path = \
            settings.CUR_SEQ_DIR + '/' + \
            mut_dir_name + '/' + \
            settings.MUT_PATCH_NAME

        if util.diff.is_patch_applied(file_path, compare_patch_path):
            return True

    return False

def mk_mut_serial_dir():
    '''
    Creates a new serial numbered directory to put mutation data and results in.
    '''
    if not os.path.isdir(settings.CUR_SEQ_DIR):
        util.log.exit_error('Missing sequence directory')

    os.chdir(settings.CUR_SEQ_DIR)

    mut_dirs = _get_mut_serial_dirs()

    serial_nr = -1

    for mut_dir in mut_dirs:
        if mut_dir.isdigit():
            serial_nr = int(mut_dir)

    serial_nr += 1

    serial_dir_name = str(serial_nr)

    if os.path.isdir(serial_dir_name):
        util.log.exit_error('Mutation output serial number directory ' +
                            'already exists: ' + serial_dir_name)

    os.mkdir(serial_dir_name)

    settings.CUR_MUTATION_DIR = settings.CUR_SEQ_DIR + '/' + serial_dir_name

    util.log.info('Created new mutation serial directory at: ' +
                    settings.CUR_MUTATION_DIR)

def _is_seq_dir(path):
    '''
    Determines if path is a sequence directory by reading the directory name
    '''
    if not os.path.isdir(path):
        util.log.exit_error('Path does not exist, or not a directory: ' +
                            path)

    return re.match(SEQ_DIR_PATTERN, path)

def _get_mut_serial_dirs():
    '''
    Returns a sorted list of the names of all mutation serial directories under
    the current sequence directory
    '''
    if not os.path.isdir(settings.CUR_SEQ_DIR):
        util.log.exit_error('Missing sequence directory')

    os.chdir(settings.CUR_SEQ_DIR)

    mut_dirs = os.listdir('.')

    # Strip non-digit directories (not mutation serial directories)
    mut_dirs = [dir_name for dir_name in mut_dirs if dir_name.isdigit()]

    # Sort the directories numerically
    def numeric_compare(element_1, element_2):
        '''
        No docstring
        '''
        return int(element_1) - int(element_2)


    mut_dirs.sort(key=functools.cmp_to_key(numeric_compare))

    return mut_dirs

def _start_new_seq(src_base_sha1_list):
    '''
    Creates a new sequence directory, sets the sequence directory path, and
    runs a "clean" test execution and stores the "golden" test output.
    '''
    os.chdir(settings.OUTPUT_PATH)

    seq_dir_name = _mk_new_seq_dir()

    settings.CUR_SEQ_DIR = settings.OUTPUT_PATH + '/' + seq_dir_name

    util.log.info('New sequence: ' + seq_dir_name)

    os.chdir(settings.CUR_SEQ_DIR)

    with open(settings.SRC_BASE_SHA1_NAME, 'w') as sha1_f:
        for sha1 in src_base_sha1_list:
            sha1_f.write("%s\n" % sha1)

    # Perform a test execution with unmodified source code, to get a clean
    # ("golden") test output that we can compare against.
    user_tests.run()

    os.chdir(settings.OUTPUT_PATH)

    pure_result_orig_path = \
        settings.OUTPUT_PATH + '/' + \
        settings.TEST_RESULTS_NAME

    pure_result_dst_path = \
        settings.CUR_SEQ_DIR + '/' + \
        settings.PURE_TEST_RESULTS_NAME

    shutil.copy(pure_result_orig_path, pure_result_dst_path)

    # Verify that the file was copied to the sequence directory
    if os.path.isfile(pure_result_dst_path) == False:
        util.log.exit_error('Could not copy test results to: ' +
                            pure_result_dst_path)

    os.remove(pure_result_orig_path)

def _verify_ongoing_seq(src_base_sha1_list):
    '''
    Compares the current source code base to the source base for the ongoing
    sequence directory. If a mismatch is found, the sequence directory is set to
    an empty variable.
    '''
    # If an ongoing sequence was found, check if sha1 of that sequence match
    # the current source base
    if settings.CUR_SEQ_DIR:
        os.chdir(settings.CUR_SEQ_DIR)

        if not os.path.isfile(settings.SRC_BASE_SHA1_NAME):
            util.log.exit_error('File "' + settings.SRC_BASE_SHA1_NAME + '" ' +
                                'missing from sequence directory: ' +
                                settings.CUR_SEQ_DIR)

        with open(settings.SRC_BASE_SHA1_NAME, 'r') as sha1_f:
            sha1_f_content = sha1_f.read()

        seq_sha1_list = sha1_f_content.splitlines()

        if seq_sha1_list != src_base_sha1_list:
            util.log.info('Source base sha1 list differs from sha1 list ' + \
                            'of ongoing sequence')

            # "Finalize" the ongoing sequence by adding an end date suffix to
            # the directory name
            new_dir_name = settings.CUR_SEQ_DIR + _get_cur_date_str()

            util.log.info('Renaming ' + settings.CUR_SEQ_DIR + ' to ' +
                            new_dir_name + ' (finalized)')

            os.chdir(settings.OUTPUT_PATH)

            os.rename(settings.CUR_SEQ_DIR, new_dir_name)

            # Reset current sequence directory string to trigger creation of
            # a new sequence
            settings.CUR_SEQ_DIR = ''

    return settings.CUR_SEQ_DIR


def _get_src_base_sha1_list():
    '''
    TBD
    '''
    os.chdir(settings.CONFIG_PATH)

    with open(settings.SRC_BASE_NAME, 'r') as src_list_f:
        src_base_list = src_list_f.read().splitlines()

    # Filter out empty lines
    src_base_list = [src_f for src_f in src_base_list if src_f != '']

    os.chdir(settings.PROJECT_ROOT)

    src_base_sha1_list = []

    for file_path in src_base_list:
        sha1 = util.checksum.get_file_sha1(file_path)

        src_base_sha1_list.append(sha1)

    if not src_base_sha1_list:
        util.log.exit_error('Failed to read sha1 list for source base')

    return src_base_sha1_list

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
    return datetime.datetime.today().strftime(SEQ_DIR_DATE_FORMAT)
