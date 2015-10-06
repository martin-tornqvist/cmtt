'''
TBD
'''

import os

import mutators.list

import util.trace

from process import codes
from process import args
from process import test_suite_execution

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
            origin_content = src_f.read()

        # Run mutation tests on the source file
        _mutation_test_src_file(origin_content, path, mutator_list, rng)

    return codes.DONE

def _mutation_test_src_file(origin_content, path, mutator_list, rng):
    '''
    TBD
    '''
    origin_lines = origin_content.splitlines()

    nr_lines = len(origin_lines)

    util.trace.empty_line()

    util.trace.info('Running mutation testing on source file: ' + path + \
                    ' (' + str(nr_lines) + ' lines)')

    # Iterate over each line in the source file
    for line_nr in range(0, nr_lines):

        util.trace.empty_line()

        util.trace.info('Original line (' + \
                        str(line_nr + 1) + \
                        '/' + str(nr_lines) + '):\n' + \
                        origin_lines[line_nr])

        # TODO: Ignore empty lines, or lines inside comments

        # Run mutation tests on this line in the source file
        _mutation_test_line(origin_content, origin_lines, path, line_nr,
                            mutator_list, rng)

def _mutation_test_line(origin_content, origin_lines, path, line_nr,
                        mutator_list, rng):
    '''
    TBD
    '''
    # Try each mutator on the current line
    for mutator in mutator_list:

        # Copy the source file lines
        working_lines = list(origin_lines)

        mutate_result = mutator(working_lines, line_nr, rng)

        if mutate_result == mutators.codes.MUTATE_OK:
            util.trace.info('Line was modified by ' + mutator.__module__ +
                            ':\n' + \
                            working_lines[line_nr])

            # Run user tests with the currently applied mutation
            _modify_and_user_test_f(origin_content, working_lines, path)

def _modify_and_user_test_f(origin_conent, modified_lines, path):
    '''
    Modifies a given source file with the provided mutated lines, runs the test
    execution hook, and finally restores the file to the original lines.
    '''
    with open(path, 'w') as src_f:
        src_f.write('\n'.join(modified_lines))

    test_suite_execution.run()

    os.chdir(args.PROJECT_ROOT)

    util.trace.info('Restoring source file')

    with open(path, 'w') as src_f:
        src_f.write(origin_conent)
