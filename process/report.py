'''
TBD
'''

import os
import shutil

import util.log
import util.html

from process import settings, seq

def run():
    '''
    Generates html reports based on the contents of the mutation output dir.
    '''
    # Copy style.css to output path
    util.log.info('Copying style.css to output path')

    html_dir = settings.OUTPUT_PATH

    html_path = html_dir + '/' + settings.HTML_REPORT_NAME

    css_origin_path = settings.CMTT_ROOT + '/css/style.css'

    if not os.path.isfile(css_origin_path):
        util.log.exit_error('Missing origin style.css')

    shutil.copy(css_origin_path, html_dir)

    if os.path.isfile(html_path):
        os.remove(html_path)

    util.html.doc_start('Mutation test overview', html_path)

    util.html.header('Mutation test overview', 1, html_path)

    seq_dirs = seq.get_seq_dirs()

    for seq_dir_name in seq_dirs:

        seq_path = settings.OUTPUT_PATH + '/' + seq_dir_name

        start = seq.get_seq_start_date(seq_path)

        header_str = str(start.date()) + ' (' + str(start.time()) + ')'

        if seq.is_seq_finalized(seq_path):
            end = seq.get_seq_end_date(seq_path)

            header_str += \
                ' to ' + str(end.date()) + ' (' + str(end.time()) + ')'
        else:
            header_str += ' *** In progress ***'

        util.html.header(header_str, 2, html_path)

        mut_dir_names = seq.get_mut_serial_dir_names(seq_path)

        nr_muts_tot = len(mut_dir_names)

        pure_result_path = seq_path + '/' + settings.PURE_TEST_RESULTS_NAME

        pure_sha1 = util.checksum.get_file_sha1(pure_result_path)

        nr_live = 0

        nr_missing_results = 0

        for mut_dir_name in mut_dir_names:
            mutated_result_path = \
                seq_path + '/' + \
                mut_dir_name + '/' + \
                settings.TEST_RESULTS_NAME

            if not os.path.isfile(mutated_result_path):
                nr_missing_results += 1
            else:
                mutated_sha1 = util.checksum.get_file_sha1(mutated_result_path)

                if mutated_sha1 == pure_sha1:
                    nr_live += 1

        nr_non_living = nr_muts_tot - nr_live

        score = (nr_non_living * 100) / nr_muts_tot

        score_rounded = round(score, 2)

        nr_killed = nr_non_living - nr_missing_results

        util.html.paragraph('Score (percentage non-live).............: ' + \
                            str(score_rounded) + '%',
                            html_path)

        util.html.paragraph('Mutations performed.....................: ' + \
                            str(nr_muts_tot),
                            html_path)

        util.html.paragraph('Mutants live............................: ' + \
                            str(nr_live),
                            html_path)

        util.html.paragraph('Mutants killed..........................: ' + \
                            str(nr_killed),
                            html_path)

        util.html.paragraph('Results missing (crash/freeze)..........: ' + \
                            str(nr_missing_results),
                            html_path)
