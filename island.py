import itertools, string

class Island:
    """Track an island region of the board."""

    # An iterator to generate different 'styles' for different regions
    newstyle = itertools.cycle(string.lowercase).next

    def __init__(self,anchor,size):
        """Create with an anchor node and desired size,
           or use anchor of None for the water."""
        self.anchor = anchor
        self.size = size
        self.nodes = [anchor]
        self.style = Island.newstyle()

    def add_node(self,node):
        """Add a node.  Will raise an exception if overfull."""
        if self.is_full():
            raise ValueError('Island %s is full.' % str(self.style))
        self.nodes.append(node)

    def is_hungry(self):
        """Return True if the region's desired size is smaller than the
        number of nodes in the region."""
        return len(self.nodes) < self.size

    def is_full(self):
        """Return True if the region's desired size is equal to the number
        of nodes in the region."""
        return not self.is_hungry()

    def __str__(self):
        return 'Region %s with anchor %s desiring size %d has %d nodes' % (
            str(self.style), str(self.anchor), self.size, len(self.nodes))

if __name__=='__main__':
    r1 = Island((1,0),4)
    r2 = Island((2,2),2)
    r2.add_node((2,3))

    print 'r1:',r1
    print 'r2:',r2

    print 'r1 hungry?',r1.is_hungry()
    print 'r2 full?',r2.is_full()

        
