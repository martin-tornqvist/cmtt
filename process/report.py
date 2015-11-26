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

    util.html.doc_start('Just a test', html_path)

    util.html.header('This is a header', 1, html_path)

    seq_dirs = seq.get_seq_dirs()

    for seq_dir in seq_dirs:
        start = seq.get_seq_start_date(seq_dir)

        header_str = str(start.date()) + ' (' + str(start.time()) + ')'

        if seq.is_seq_finalized(seq_dir):
            end = seq.get_seq_end_date(seq_dir)

            header_str += \
                ' to ' + str(end.date()) + ' (' + str(end.time()) + ')'
        else:
            header_str += ' *** In progress ***'

        util.html.header(header_str, 2, html_path)

        util.html.paragraph('Stuff goes here...', html_path)
