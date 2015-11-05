'''
TBD
'''

import os
import shutil
import time

import mutators.list

import util.log
import util.diff

from process import codes, seq
from process import user_tests
from process import settings

def run(src_file_path_list, rng):
    '''
    TBD
    '''
    os.chdir(settings.PROJECT_ROOT)

    # Run mutation tests on the file paths until the global timeout finishes
    while True:
        util.log.info('Starting new mutation test loop over source file list')

        # Shuffle the source file list
        rng.shuffle(src_file_path_list)

        # Iterate over the source files, and run mutation testing on each until
        # finished, or until a global timeout expires
        for path in src_file_path_list:

            # Verify that the file exists
            if os.path.isfile(path) == False:
                util.log.exit_error('Missing source file: ' + path)

            # Read the source file
            with open(path, 'r') as src_f:
                origin_lines = src_f.read().splitlines()


            nr_lines = len(origin_lines)

            util.log.info('Running mutation testing on source file: ' + path +
                            ' (' + str(nr_lines) + ' lines)')

            # Iterate over each line in the source file
            for line_nr in range(0, nr_lines):

                # Skip empty lines
                if not origin_lines[line_nr]:
                    continue

                # TODO: Ignore lines inside comments

                # Run mutation tests on the source file until done
                _mut_test_src_line(origin_lines, line_nr, path, rng)

                time_now = time.time()

                if time_now > (settings.TOOL_START_TIME + settings.GLOBAL_TIMEOUT):
                    util.log.info('Global timeout hit (' +
                                    str(settings.GLOBAL_TIMEOUT) + 's), bye!')

                    return codes.GLOBAL_TIMEOUT_EXCEEDED

    return codes.DONE

def _mut_test_src_line(origin_lines, line_nr, path, rng):
    '''
    TBD
    '''

    nr_lines = len(origin_lines)

    # Get a list of mutators
    mutator_list = mutators.list.get()

    # Try each mutator on the current line in the source file, and run user
    # tests for any mutations applied
    for mutator in mutator_list:

        # Copy the source file lines
        working_lines = list(origin_lines)

        mutate_result = mutator(working_lines, line_nr, rng)

        if mutate_result == mutators.codes.MUTATE_OK:

            util.log.info('Line ' + str(line_nr + 1) + '/' +
                            str(nr_lines) + ':\n' +
                            origin_lines[line_nr])

            util.log.info('Was modified by ' +
                            mutator.__module__ + ':\n' +
                            working_lines[line_nr])

            os.chdir(settings.PROJECT_ROOT)

            backup_path = path + '.backup'

            # Make backup of source file
            shutil.copy(path, backup_path)

            # Overwrite the file with the modified lines
            with open(path, 'w') as src_f:
                for line in working_lines:
                    src_f.write("%s\n" % line)

            patch_path = settings.OUTPUT_PATH + '/' + settings.MUT_PATCH_NAME

            util.diff.gen_patch(backup_path, path, patch_path)

            if seq.is_patch_applied_cur_seq(os.path.abspath(path), patch_path):
                util.log.info('Mutation already applied previously in this '
                              'sequence - skipping')
            else:
                # Mutation has not been applied before in this sequence

                seq.mk_mut_serial_dir()

                # Move the patch to the mutation serial folder
                shutil.move(patch_path, settings.CUR_MUTATION_DIR)

                user_tests.run()

            os.chdir(settings.PROJECT_ROOT)

            # Restore source file

            os.remove(path)

            shutil.move(backup_path, path)
