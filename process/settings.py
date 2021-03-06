'''
Global paths and variables
'''

#===============================================================================
# Config directory
#===============================================================================
EXECUTE_TESTS_HOOK_NAME = 'execute_tests'
MUTATION_FILES_NAME = 'mutation_files'
SRC_BASE_NAME = 'src_base'

#===============================================================================
# Output directory
#===============================================================================
SRC_BASE_SHA1_NAME = 'src_base_sha1'
PURE_TEST_RESULTS_NAME = 'pure_test_results'
TEST_RESULTS_NAME = 'test_results'
MUT_PATCH_NAME = 'mutation_patch'
HTML_REPORT_NAME = 'report.html'

#===============================================================================
# css origin (relative to CMTT root)
#===============================================================================
CSS_PATH_FROM_ROOT = 'css/style.css'

#===============================================================================
# Current sequence directory
#===============================================================================
CUR_SEQ_DIR = ''

#===============================================================================
# Serial numbered directory under the sequence directory to store output
# specific for the current mutation (e.g. a patch and test result)
#===============================================================================
CUR_MUTATION_DIR = ''

#===============================================================================
# User arguments
#===============================================================================
CMTT_ROOT = ''
PROJECT_ROOT = ''
CONFIG_PATH = ''
OUTPUT_PATH = ''
RNG_SEED = ''
DRY_RUN = False
GEN_REPORTS = False

# Test execution subprocess timeout (in seconds)
TEST_TIMEOUT = 0

# Global timeout (in seconds)
GLOBAL_TIMEOUT = 0

#===============================================================================
# Start time of this program
#===============================================================================
TOOL_START_TIME = -1
