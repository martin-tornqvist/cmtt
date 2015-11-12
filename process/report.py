'''
TBD
'''

import os
import shutil

import util.log

from process import settings

def run():
    '''
    TBD
    '''
    # Copy style.css to output path
    util.log.info('Copying style.css to output path')

    os.chdir(settings.MUTATION_TOOL_ROOT)

    shutil.copy('css/style.css', settings.OUTPUT_PATH)
