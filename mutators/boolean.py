"""
Boolean operator mutations
"""

from mutators import base
from mutators import codes

class Mutator(base.Mutator):
    """
    TBD
    """

    def __init__(self):
        base.Mutator.__init__(self)

    def run(self, lines, line_nr):
        """
        TBD
        """
        return codes.MUTATE_FAILED
