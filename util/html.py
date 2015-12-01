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

def text(text, html_path):
    '''
    Write preformatted text
    '''
    _write('<pre>' + text + '</pre>', html_path)

def start_pre(html_path):
    '''
    TBD
    '''
    _write('<pre>', html_path)

def end_pre(html_path):
    '''
    TBD
    '''
    _write('</pre>', html_path)

def raw(text, html_path):
    '''
    TBD
    '''
    _write(text, html_path)

def inline(text, html_path):
    '''
    TBD
    '''
    _write('<span>' + text + '</span>', html_path)

def newline(html_path):
    '''
    TBD
    '''
    _write('<br>', html_path)

def link(text, url, html_path):
    '''
    TBD
    '''
    _write('<a href=' + url + ' target="_blank">' + text + '</a>', html_path)

def _write(text, html_path):
    '''
    TBD
    '''
    with open(html_path, 'a') as html_file:
        html_file.write(text + '\n')
