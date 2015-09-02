'''
Arithmetic operator mutator
'''

import re

from mutators import common
from mutators import codes

def mutate(lines, line_nr, rng):
    '''
    TBD
    '''

    line = lines[line_nr]

    operators = [r' \+ ', r' \- ', r' \* ', r' \/ ', r' \% ']

    rng.shuffle(operators)

    for operator_idx in range(0, len(operators)):
        op_str = operators[operator_idx]

        pattern = re.compile(op_str)

        match_iterator = re.finditer(pattern, line)

        match_list = list(match_iterator)

        if match_list:
            # Remove the matched operator from the operator list
            operators.pop(operator_idx)

            # Choose a random replacement operator
            op_repl_str = rng.choice(operators)

            # Remove escape slashes
            op_repl_str = common.strip_escapes(op_repl_str)

            # Choose a random match
            match = rng.choice(match_list)

            # Put the replacement operator in the line
            line = line[:match.start()] + op_repl_str + line[match.end():]

            lines[line_nr] = line

            return codes.MUTATE_OK

    return codes.MUTATE_FAILED
