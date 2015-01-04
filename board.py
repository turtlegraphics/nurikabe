import networkx as nx
import regions

class Board:
    """Store a Nurikabe board."""
    def __init__(self,g):
        """Initialize with any graph."""
        self.g = g
        
        # set base node and successor dictionary for breadth first search
        self.basenode = g.nodes()[0]
        self.bfs_successors = nx.bfs_successors(g,self.basenode)

        # pools are defined as water cycles of minimum length
        # here, find the girth of the graph (there's no built-in girth
        # for networkx, so I'm using this kludge, which may actually be
        # incorrect in general. For now, try it, and assert it worked.
        self.pool_length = min([len(cycle) for cycle in nx.cycle_basis(g)])
        assert self.pool_length == 4

        # set up regions of the board
        self.regions = []
        self.water = regions.Water(self)
        for n in self.g.nodes():
            self.set_region(n,None)
        
    def __str__(self):
        return str(self.g)

    def add_region(self,r):
        """Add a region to the board."""
        assert r not in self.regions
        self.regions.append(r)

        # mark node as in a region
        for n in r.nodes:
            self.set_region(n,r)


    def set_region(self,n,r):
        """Set the region of a node to r."""
        self.g.node[n]['region'] = r
        
    def get_region(self,n):
        """Return the region of a node."""
        return self.g.node[n]['region']

    def is_set(self,n):
        """Return True if node is in a region."""
        return self.get_region(n) != None

    def unset_node(self,n):
        """Return node to unset state (neither water nor land)."""
        r = self.get_region(n)
        r.remove_node(n)

    def set_node_to_water(self,n):
        """Try to set node n to water. Raise exception on failure."""
        assert not self.is_set(n)
        self.water.add_node(n)
        self.set_region(n,self.water)

    def _worknode(self,n,successors):
        """Operate on a node, using _solve recursively."""
        print 'Working node',n
        if self.is_set(n):
            # node is already set. move along.
            self._solve(successors)
            return

        try:
            self.set_node_to_water(n)
        except region.RegionError:
            pass
        else:
            self._solve(successors)
            self.unset_node(n)

    def _solve(self,successors):
        """Recursively walk the nodes in BFS order."""
        if not successors:
            print 'Solved!'
            print self
            return
        n = successors.pop(0)
        try:
            successors.extend(self.bfs_successors[n])
        except KeyError:
            pass

        self._worknode(n,successors)

        successors.insert(0,n)

    def solve(self):
        """Brute force recursive solver."""
        source = self.g.nodes()[0]
        self._solve([self.basenode])
        
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
                r = self.g.node[(x,y)]['region']
                out += str(r.style) if r else '.'
            out += '\n'

        return out.rstrip('\n')

if __name__=='__main__':
    b = BoardRectangle(6,3)
    print b
    print
    i1 = regions.Island(b,(0,0),4)
    i1.add_node((0,1))
    i2 = regions.Island(b,(4,2),2)
    b.add_region(i1)
    b.add_region(i2)
    b.set_node_to_water((5,1))

    print b

    b.solve()
