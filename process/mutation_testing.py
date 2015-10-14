'''
TBD
'''

import os
import shutil
import time

import mutators.list

import util.trace

from process import codes, vars, test_suite_execution

def run(src_file_path_list, rng):
    '''
    TBD
    '''
    os.chdir(vars.PROJECT_ROOT)

    # Run mutation tests on the file paths until the global timeout finishes
    # TODO: Implement global timeout
    while True:
        util.trace.info('Starting new mutation test loop over source file list')

        # Shuffle the source file list
        rng.shuffle(src_file_path_list)

        # Iterate over the source files, and run mutation testing on each until
        # finished, or until a global timeout expires
        for path in src_file_path_list:

            # Verify that the file exists
            if os.path.isfile(path) == False:
                util.trace.exit_error('Could not find source file: ' + path)

            # Read the source file
            with open(path, 'r') as src_f:
                origin_lines = src_f.read().splitlines()


            nr_lines = len(origin_lines)

            util.trace.info('Running mutation testing on source file: ' + path +
                            ' (' + str(nr_lines) + ' lines)')

            # Iterate over each line in the source file
            for line_nr in range(0, nr_lines):

                # Skip empty lines
                if not origin_lines[line_nr]:
                    continue

                # TODO: Ignore lines inside comments

                # Run mutation tests on the source file until done
                _mutation_test_src_line(origin_lines, line_nr, path, rng)

                time_now = time.time()

                if time_now > (vars.TOOL_START_TIME + vars.GLOBAL_TIMEOUT):
                    util.trace.info('Global timeout hit (' +
                                    str(vars.GLOBAL_TIMEOUT) +
                                    's), bye!')
                    return

    return codes.DONE

def _mutation_test_src_line(origin_lines, line_nr, path, rng):
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

            util.trace.info('Line ' + str(line_nr + 1) + '/' +
                            str(nr_lines) + ':\n' +
                            origin_lines[line_nr])

            util.trace.info('Was modified by ' +
                            mutator.__module__ + ':\n' +
                            working_lines[line_nr])

            os.chdir(vars.PROJECT_ROOT)

            backup_path = path + '.backup'

            util.trace.info('Creating backup of source file')

            shutil.copy(path, backup_path)

            # Overwrite the file with the modified lines
            with open(path, 'w') as src_f:
                for line in working_lines:
                    src_f.write("%s\n" % line)

            # TODO: Make a diff from the original file to the modified file,
            #       only run tests if diff has not been applied before.

            test_suite_execution.run()

            # TODO: Verify test execution, and if mutation was not covered,
            #       store the diff permanently.

            os.chdir(vars.PROJECT_ROOT)

            util.trace.info('Restoring source file')

            os.remove(path)

            shutil.move(backup_path, path)
