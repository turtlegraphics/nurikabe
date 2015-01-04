import networkx as nx
import regions

class Board:
    """Store a Nurikabe board."""
    def __init__(self,grid):
        """Initialize with any graph."""
        self.grid = grid
        self.regions = []
        self.water = regions.Water()
        for n in self.grid.nodes():
            self.grid.node[n]['region'] = None
        
    def __str__(self):
        return str(self.grid)

    def add_region(self,r):
        """Add a region to the board."""
        assert r not in self.regions
        self.regions.append(r)

        # mark node as in a region
        for n in r.nodes:
            self.grid.node[n]['region'] = r

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
            for x in range(self.width):
                r = self.grid.node[(x,y)]['region']
                out += str(r.style) if r else '.'
            out += '\n'

        return out.rstrip('\n')

if __name__=='__main__':
    b = BoardRectangle(6,3)
    print b
    print
    i1 = regions.Island((0,0),4)
    i1.add_node((0,1))
    i2 = regions.Island((4,2),2)
    b.add_region(i1)
    b.add_region(i2)
    print b
