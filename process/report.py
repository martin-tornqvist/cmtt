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
    html_path = settings.OUTPUT_PATH + '/' + settings.HTML_REPORT_NAME

    header_text = 'Mutation test overview'

    _init_report(html_path, header_text)

    seq_dirs = seq.get_seq_dirs()

    seq_dirs.reverse()

    for seq_dir_name in seq_dirs:
        _report_seq(html_path, seq_dir_name)

    util.html.doc_end(html_path)

    util.log.info('Report written at: \n' + html_path)

def _report_seq(html_path, seq_dir_name):
    '''
    TBD
    '''
    seq_path = settings.OUTPUT_PATH + '/' + seq_dir_name

    start = seq.get_seq_start_date(seq_path)

    seq_title = str(start.date()) + ' (' + str(start.time()) + ')'

    if seq.is_seq_finalized(seq_path):
        end = seq.get_seq_end_date(seq_path)
        seq_title += ' to ' + str(end.date()) + ' (' + str(end.time()) + ')'
    else:
        seq_title += ' *** In progress ***'

    util.html.header('Sequence ' + seq_title, 2, html_path)

    mut_dir_names = seq.get_mut_serial_dir_names(seq_path)

    nr_muts_tot = len(mut_dir_names)

    pure_result_path = seq_path + '/' + settings.PURE_TEST_RESULTS_NAME

    pure_sha1 = util.checksum.get_file_sha1(pure_result_path)

    live_mut_report_path = seq_path + '/live_mutants.html'

    _init_report(live_mut_report_path, 'Live mutants in sequence')

    util.html.text('Sequence: ' + seq_title, live_mut_report_path)

    nr_alive = 0
    nr_missing_results = 0

    for mut_dir_name in mut_dir_names:
        mut_dir_path = seq_path + '/' + mut_dir_name

        mutated_result_path = mut_dir_path + '/' + settings.TEST_RESULTS_NAME

        if not os.path.isfile(mutated_result_path):
            nr_missing_results += 1
        else:
            mutated_sha1 = util.checksum.get_file_sha1(mutated_result_path)

            if mutated_sha1 == pure_sha1:
                nr_alive += 1

                patch_path = mut_dir_path + '/' + settings.MUT_PATCH_NAME

                if not os.path.isfile(patch_path):
                    util.log.exit_error('Missing mutation patch: ' +
                                        patch_path)

                util.html.header('Subdirectory: ' + mut_dir_name + '/',
                                 3, live_mut_report_path)

                with open(patch_path, 'r') as patch_f:
                    patch_lines = patch_f.read().splitlines()

                    dashes = '----------------------------------------'

                    util.html.start_pre(live_mut_report_path)
                    util.html.raw(dashes, live_mut_report_path)

                    for line in patch_lines:
                        util.html.raw(line, live_mut_report_path)

                    util.html.raw(dashes, live_mut_report_path)
                    util.html.end_pre(live_mut_report_path)

    # Finalize the live mutants sequence report
    util.html.doc_end(live_mut_report_path)

    nr_tested = nr_muts_tot - nr_missing_results
    nr_killed = nr_tested - nr_alive
    score = (nr_killed * 100) / nr_tested
    score_rounded = round(score, 2)

    util.html.text('Score (killed / [alive + killed]).......: ' + \
                        str(score_rounded) + '%',
                        html_path)

    util.html.text('Tests finished..........................: ' + \
                        str(nr_tested),
                        html_path)

    util.html.inline('Mutants alive...........................: ' + \
                        str(nr_alive),
                        html_path)

    util.html.link('[Detailed info]', live_mut_report_path, html_path)
    util.html.newline(html_path)

    util.html.text('Mutants killed..........................: ' + \
                     str(nr_killed),
                     html_path)

    util.html.text('Results missing (e.g. crash/freeze).....: ' + \
                        str(nr_missing_results),
                        html_path)

def _init_report(html_path, header_text):
    '''
    TBD
    '''
    css_origin_path = settings.CMTT_ROOT + '/' + settings.CSS_PATH_FROM_ROOT

    if not os.path.isfile(css_origin_path):
        util.log.exit_error('Missing css file: ' + css_origin_path)

    report_dir_path = os.path.dirname(html_path)

    if not os.path.isdir(report_dir_path):
        util.log.exit_error('Html report target directory does not exist: ' +
                            report_dir_path)

    shutil.copy(css_origin_path, report_dir_path)

    if os.path.isfile(html_path):
        os.remove(html_path)

    util.html.doc_start(header_text, html_path)

    util.html.header(header_text, 1, html_path)
