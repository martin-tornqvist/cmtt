'''
TBD
'''

import os
import shutil

import mutators.list

import util.trace

from process import codes, args, test_suite_execution

def run(src_file_path_list, rng):
    '''
    TBD
    '''
    os.chdir(args.PROJECT_ROOT)

    # Get a list of mutators
    mutator_list = mutators.list.get()

    # TODO: Implement global timeout

    # Iterate over the source files, and run mutation testing on each until
    # finished, or until a global timeout expires
    for path in src_file_path_list:

        # Verify that the file exists
        if os.path.isfile(path) == False:
            util.trace.exit_error('Could not find source file: ' + path)

        # Read the source file
        with open(path, 'r') as src_f:
            origin_lines = src_f.read().splitlines()

        # Run mutation tests on the source file until done
        _mutation_test_src_f(origin_lines, path, mutator_list, rng)

    return codes.DONE

def _mutation_test_src_f(origin_lines, path, mutator_list, rng):
    '''
    TBD
    '''
    nr_lines = len(origin_lines)

    util.trace.empty_line()

    util.trace.info('Running mutation testing on source file: ' + path +
                    ' (' + str(nr_lines) + ' lines)')

    # Iterate over each line in the source file
    for line_nr in range(0, nr_lines):

        # TODO: Ignore lines inside comments

        if not origin_lines[line_nr]:
            continue

        # Run mutation tests on this line in the source file
        # Try each mutator on the current line
        for mutator in mutator_list:

            # Copy the source file lines
            working_lines = list(origin_lines)

            mutate_result = mutator(working_lines, line_nr, rng)

            if mutate_result == mutators.codes.MUTATE_OK:

                util.trace.empty_line()

                util.trace.info('Line ' + str(line_nr + 1) + '/' +
                                str(nr_lines) + ':\n' +
                                origin_lines[line_nr])

                util.trace.info('Was modified by ' +
                                mutator.__module__ + ':\n' +
                                working_lines[line_nr])

                os.chdir(args.PROJECT_ROOT)

                backup_path = path + '.backup'

                util.trace.empty_line()
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

                os.chdir(args.PROJECT_ROOT)

                util.trace.empty_line()
                util.trace.info('Restoring source file')

                os.remove(path)

                shutil.move(backup_path, path)