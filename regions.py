import itertools, string
import networkx as nx

#class RegionError(Exception):
#    pass

class Region:
    """Track a region of the board."""
    def __init__(self,board):
        """Requires a board."""
        self.nodes = []
        self.board = board

    def add_node(self,node):
        assert node not in self.nodes
        self.nodes.append(node)

    def remove_node(self,node):
        self.nodes.remove(node)
        
    def __str__(self):
        return '%d nodes' % len(self.nodes)

class Water(Region):
    """Track a water region of the board."""
    def __init__(self,board):
        Region.__init__(self,board)
        self.style = '#'

    def __str__(self):
        return 'Water, %s.' % Region.__str__(self)

    def would_pool(self,node):
        """Determine if the node would create a pool."""
        possiblepools = self.board.pools[node]
        for p in possiblepools:
            ispool = True
            for n in p:
                if n == node:
                    continue
                if n not in self.nodes:
                    ispool = False
            if ispool:
                return True
        return False

class Island(Region):
    """Track an island region of the board."""

    # An iterator to generate different 'styles' for different regions
    newstyle = itertools.cycle(string.lowercase).next

    def __init__(self,board,anchor,size):
        """Create with an anchor node and desired size,
           or use anchor of None for the water."""
        Region.__init__(self,board)
        self.anchor = anchor
        self.size = size
        self.style = Island.newstyle()
        self.add_node(anchor)

    def remove_node(self,node):
        """Remove a node. Raise an exception if trying to remove the anchor."""
        if node == self.anchor:
            raise ValueError('Cannot remove the anchor.')
        Region.remove_node(self)

    def add_node(self,node):
        """Add a node.  Will raise an exception if overfull."""
        if self.is_full():
            raise RegionError('Island %s is full.' % str(self.style))
        Region.add_node(self,node)

    def is_hungry(self):
        """Return True if the region's desired size is smaller than the
        number of nodes in the region."""
        return len(self.nodes) < self.size

    def is_full(self):
        """Return True if the region's desired size is equal to the number
        of nodes in the region."""
        return not self.is_hungry()

    def __str__(self):
        return 'Island %s with anchor %s desiring size %d, %s' % (
            str(self.style), str(self.anchor), self.size, Region.__str__(self))

if __name__=='__main__':
    w = Water(None)
    r1 = Island(None,(1,0),4)
    r2 = Island(None,(2,2),2)
    r2.add_node((2,3))

    print 'w: ',w
    print 'r1:',r1
    print 'r2:',r2

    print 'r1 hungry?',r1.is_hungry()
    print 'r2 full?',r2.is_full()

        
