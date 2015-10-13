'''
Comparison operator mutator
'''

from mutators import common, codes

def mutate(lines, line_nr, rng):
    '''
    TBD
    '''

    line = lines[line_nr]

    op_re_list = [r' == ', r' != ', r' > ', r' < ', r' >= ', r' <= ']

    rng.shuffle(op_re_list)

    for op_idx in range(0, len(op_re_list)):
        op_re_str = op_re_list[op_idx]

        match_list = common.match_list(op_re_str, line)

        if match_list:
            # Remove the matched operator from the operator list
            op_re_list.pop(op_idx)

            # Choose a random replacement operator
            new_op_str = rng.choice(op_re_list)

            # Remove escape slashes
            # new_op_str = common.strip_escapes(new_op_str)

            # Choose a random match
            match = rng.choice(match_list)

            # Put the replacement operator in the line
            line = line[:match.start()] + new_op_str + line[match.end():]

            lines[line_nr] = line

            return codes.MUTATE_OK

    return codes.MUTATE_FAILED
