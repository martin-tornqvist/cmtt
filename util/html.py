'''
Utility module for writing html code
'''

import os

from util import log

def doc_start(title, html_path):
    '''
    TBD
    '''
    if os.path.isfile(html_path):
        log.exit_error('html report already exist')

    _write('<!DOCTYPE html>', html_path)
    _write('<html>', html_path)
    _write('<head>', html_path)
    _write('<title>' + title + '</title>', html_path)
    _write('<link rel="stylesheet" type="text/css" href="style.css">',
           html_path)
    _write('</head>', html_path)
    _write('<body>', html_path)

def doc_end(html_path):
    '''
    TBD
    '''
    _write('</body>', html_path)
    _write('</html>', html_path)

def header(text, level, html_path):
    '''
    TBD
    '''
    level_str = str(level)

    _write('<h' + level_str + '>' + text + '</h' + level_str + '>', html_path)

def paragraph(text, html_path):
    '''
    TBD
    '''
    _write('<pre>' + text + '</pre>', html_path)

def _write(text, html_path):
    '''
    TBD
    '''
    with open(html_path, 'a') as html_file:
        html_file.write(text + '\n')
