import networkx as nx
import graph
import regions

class Board:
    """Store a Nurikabe board."""
    def __init__(self,g):
        """Initialize with any graph."""
        self.g = g
        
        # set base node and successor dictionary for board traversal
        self.basenode = g.nodes()[0]
        self.bfs_next = graph.bfs_list(g,self.basenode)

        # pools are defined as water cycles of minimum length
        # find all the pools in the graph, indexed by nodes
        (self.pool_size,self.pools) = graph.find_shortest_cycles(g)

        # set up regions of the board
        self.regions = []
        self.max_region_size = 0
        self.water = regions.Water()
        for n in self.g.nodes():
            self._set_region(n,None)
        self.land = regions.Land() # temporary anonymous land region

    def __str__(self):
        return str(self.g)

    def add_region(self,r):
        """Add a region to the board."""
        assert r not in self.regions
        self.regions.append(r)
        self.max_region_size = max(self.max_region_size,r.size)

        # mark nodes as in a region
        for n in r.nodes:
            self._set_region(n,r)


    def _set_region(self,n,r):
        """Set the region of a node to r. Generally, use set_node instead."""
        self.g.node[n]['region'] = r
        
    def get_region(self,n):
        """Return the region of a node."""
        return self.g.node[n]['region']

    def set_node(self,n,r):
        """Set node n to be in region r."""
        assert not self.is_set(n)
        r.add_node(n)
        self._set_region(n,r)

    def unset_node(self,n):
        """Return node to unset state (neither water nor land)."""
        r = self.get_region(n)
        if r:
            self._set_region(n,None)
            r.remove_node(n)

    def is_set(self,n):
        """Return True if node is in a region."""
        return self.get_region(n) != None

    def is_water(self,n):
        """Return True if node is in the water region."""
        return n in self.water.nodes

    def is_land(self,n):
        """Return True if node is in any land region."""
        return self.is_set(n) and not self.is_water(n)

    def would_pool(self,node):
        """Determine if the node would create a pool."""
        possiblepools = self.pools[node]
        for p in possiblepools:
            ispool = True
            for n in p:
                if n == node:
                    continue
                if not self.is_water(n):
                    ispool = False
            if ispool:
                return True
        return False

    def ok_for_land(self,n):
        """Try to set node to land. Return """
        for nbr in self.g[n]:
            if not self.is_water(nbr) and self.is_set(nbr):
                return False
        return True

    def _solve(self,n):
        """Operate on a node, using _solve recursively."""
        if n == None:
            print '='*30
            print 'Solved!'
            print self
            print '='*30
            return

        #print 'Ready for node',n
        #raw_input()
        
        if self.is_set(n):
            # node is already set. move along.
            self._solve(self.bfs_next[n])
            return

        if not self.would_pool(n):
            self.set_node(n,self.water)
            # print 'Try node',n,'as water:'
            # print self
            self._solve(self.bfs_next[n])
            self.unset_node(n)
        #else:
        #    print 'Node',n,'cannot be water'

        if self.ok_for_land(n):
            self.set_node(n,self.land)
            #print 'Try node',n,'as land:'
            #print self
            self._solve(self.bfs_next[n])
            self.unset_node(n)
        #else:
        #    print 'Node',n,'cannot be land'
            
    def solve(self):
        """Brute force recursive solver."""
        self._solve(self.basenode)
        
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
    b = BoardRectangle(6,8)
    i1 = regions.Island((0,0),4)
    i1.add_node((0,1))
    i2 = regions.Island((4,2),2)
    b.add_region(i1)
    b.add_region(i2)
    b.set_node((5,1),b.water)

    print b
    print
    print 'Solving...'
    b.solve()
