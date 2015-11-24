'''
TBD
'''

import os
import shutil

import util.log
import util.html

from process import settings

def run():
    '''
    TBD
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

    util.html.paragraph('This is a parapgraph, hello', html_path)
