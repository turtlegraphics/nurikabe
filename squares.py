"""
Each node of the board contains a Square subclass.
Only when using square grids do these actually correspond to anything square.
"""
class Square:
    """One square of the board."""
    theMark = 0
    @staticmethod
    def clear_marks():
        Square.theMark += 1
    def __init__(self):
        self.marker = None
    def mark(self):
        self.marker = Square.theMark
    def marked(self):
        return self.marker == Square.theMark

class Empty(Square):
    def __str__(self):
        return '.'
class Water(Square):
    def __str__(self):
        return '#'
class Land(Square):
    def __str__(self):
        return '+'
class Anchor(Land):
    def __init__(self,size):
        Land.__init__(self)
        assert size > 0
        self.size = size
    def __str__(self):
        return str(self.size)
