import networkx as nx

class Board:
    """Store a Nurikabe board."""
    def __init__(self,grid):
        """Initialize with any graph."""
        self.grid = grid

    def __str__(self):
        return str(self.grid)

class BoardRectangle(Board):
    """A rectangular square-grid Nurikabe board."""
    def __init__(self,width,height):
        self.width = width
        self.height = height
        Board.__init__(self,nx.grid_graph([width,height]))

    def __str__(self):
        """ASCII art represenation of the board."""
        out = ''
        for y in range(self.height):
            out += ''.join(['.' for x in range(self.width)])+'\n'
        return out.rstrip('\n')

if __name__=='__main__':
    b = BoardRectangle(6,3)
    print b

                

               
