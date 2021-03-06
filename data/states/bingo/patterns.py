"""Classes to help with matching patterns of squares on the cards"""

from . import loggable
from .settings import SETTINGS as S


class Pattern(loggable.Loggable):
    """A pattern of squares that would win the game"""

    lx, rx = S['card-square-cols'][0], S['card-square-cols'][-1]
    by, ty = S['card-square-rows'][0], S['card-square-rows'][-1]

    def __init__(self):
        """Initialise the pattern"""
        self.addLogger()

    def get_matches(self, card):
        """Return a sequence of matching squares"""
        for offsets in self.get_square_offsets():
            yield [
                card.squares[offset] for offset in offsets
            ]

    def get_square_offsets(self):
        """Return a sequence of matching square offsets"""
        raise NotImplementedError('Must implement the get_square_offsets method')


class CornersPattern(Pattern):
    """All the corners of the card"""

    def get_square_offsets(self):
        """Return a sequence of matching square offsets"""
        return [
            [(self.lx, self.by), (self.lx, self.ty), (self.rx, self.by), (self.rx, self.ty)],
        ]


class LinesPattern(Pattern):
    """Straight lines"""

    def get_square_offsets(self):
        """Return a sequence of matching square offsets"""
        for row in S['card-square-rows']:
            yield [(row, col) for col in S['card-square-cols']]
        for col in S['card-square-cols']:
            yield [(row, col) for row in S['card-square-rows']]
        yield [(row, row) for row in S['card-square-rows']]
        yield [(-row, row) for row in S['card-square-rows']]


class CoverallPattern(Pattern):
    """A blackout of the entire card"""

    def get_square_offsets(self):
        """Return a sequence of matching square offsets"""
        yield [
            (row, col) for row in S['card-square-rows'] for col in S['card-square-cols']
        ]


class CenterPattern(Pattern):
    """All the center squares"""

    def get_square_offsets(self):
        """Return a sequence of matching square offsets"""
        yield [
            (row, col) for row in S['card-square-rows'][1:-1] for col in S['card-square-cols'][1:-1]
        ]


class StampPattern(Pattern):
    """A stamp in one corner"""

    def get_square_offsets(self):
        """Return a sequence of matching square offsets"""
        yield [
            (row, col) for row in S['card-square-rows'][:-3] for col in S['card-square-cols'][:-3]
        ]
        yield [
            (row, col) for row in S['card-square-rows'][3:] for col in S['card-square-cols'][3:]
        ]
        yield [
            (row, col) for row in S['card-square-rows'][:-3] for col in S['card-square-cols'][3:]
        ]
        yield [
            (row, col) for row in S['card-square-rows'][3:] for col in S['card-square-cols'][:-3]
        ]