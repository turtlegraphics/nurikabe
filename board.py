"""
board module
  Implements the board and a number of functions to check
  for legal arrangements.

2015 Bryan Clair
"""

import networkx as nx
import graphutil
import logging
from squares import *

class Board:
    """Store a Nurikabe board."""
    def __init__(self,g):
        """Initialize with any graph."""
        self.graph = g

        # Fill with emptiness.
        for n in self.graph:
            self.graph.node[n]['val'] = Empty()

        # track anchors and largest anchor (to limit un-anchored islands)
        self.anchors = []
        self.anchor_maxsize = 0

        # pools are defined as water cycles of minimum length
        # find all the pools in the graph, indexed by nodes
        (self.pool_size,self.pools) = graphutil.find_shortest_cycles(g)

        # keep track as well as possible whether water could be connected.
        # True: possible to connect water using more water
        # False: impossible to connect water
        # None: State unknown
        self.water_connected = None

        self.cwtries = 0
        self.cwfails = 0

    def __str__(self):
        return str(self.graph)

    def set_node(self,node,val):
        # Complicated logic here to determine water_connected status
        if self.water_connected is True:
            if isinstance(val,Land):
                if self._nonLand_neighbors(node) > 1:
                    self.water_connected = None
            elif isinstance(val,Water):
                if self._water_neighbors(node) == 0:
                    self.water_connected = None
        elif self.water_connected is False:
            if self.is_Land(node):
                if self._nonLand_neighbors(node) > 1:
                    self.water_connected = None
            elif self.is_Water(node):
                if self._water_neighbors(node) == 0:
                    self.water_connected = None

        if self.water_connected is not None:
            if self.water_connected != self._water_connectedness_search():
                logging.warn('FAIL: setting '+str(node)+' from '+str(self.get_node(node))+'to'+str(val)+'wc='+str(self.water_connected))

        self.graph.node[node]['val'] = val
        

    def set_anchor(self,node,size):
        """Create an anchor of given size at node n."""
        assert self.is_Empty(node)
        self.set_node(node,Anchor(size))
        self.anchor_maxsize = max(self.anchor_maxsize,size)
        self.anchors.append(node)

    def clear_node(self,node):
        self.set_node(node,Empty())

    def get_node(self,node):
        """Return the value of a node."""
        return self.graph.node[node]['val']

    def is_Empty(self,node):
        return isinstance(self.get_node(node),Empty)
        
    def is_Water(self,node):
        return isinstance(self.get_node(node),Water)

    def is_Land(self,node):
        return isinstance(self.get_node(node),Land)

    def is_Anchor(self,node):
        """Return size of Anchor or 0."""
        me = self.get_node(node)
        if isinstance(me,Anchor):
            return me.size
        else:
            return 0

    def in_pool(self,node):
        """Determine if the node is in a pool."""
        possiblepools = self.pools[node]
        for p in possiblepools:
            ispool = True
            for n in p:
                if not self.is_Water(n):
                    ispool = False
            if ispool:
                return True
        return False

    def _ei(self,node,anchors):
        """Recursive search of the island.  Add newly discovered Anchors
        to the anchors list.
        Return the island size and list of adjacent empty nodes."""

        v = self.get_node(node)
        if v.marked():
            # been here before
            return (0,[])
        v.mark()

        if self.is_Empty(node):
            return (0,[node])
        if not self.is_Land(node):
            return (0,[])
        
        # found new piece of the island
        if self.is_Anchor(node):
            anchors.append(node)

        # recursively check all neighbors
        size = 1  # count this node
        freedoms = []
        for n in self.graph[node]:
            (s,f) = self._ei(n,anchors)
            size += s
            freedoms.extend(f)

        return (size,freedoms)

    def explore_island(self,node):
        """Return the size of the island containing node, and a list
        of any Anchors in the island."""
        Square.clear_marks()
        anchors = []
        (size,freedoms) = self._ei(node,anchors)
        return (size,freedoms,anchors)

    def legal_island(self,node):
        """True if the node is part of a legal island.
        It should have only one anchor, and either be that size or
        be smaller with at least one freedom."""
        (size, freedoms, anchors) = self.explore_island(node)
        if len(anchors) > 1:
            return False
        if anchors:
            wantsize = self.get_node(anchors[0]).size
            if size == wantsize:
                return True
            if size < wantsize and freedoms:
                return True
            return False

        # no anchors.. free terrain.
        # needs to have a freedom and cap on size
        return freedoms and size <= self.anchor_maxsize - 1

    def _has_water(self,bunch):
        """True if there is a Water node in the list of nodes."""
        for node in bunch:
            if self.is_Water(node):
                return True
        return False

    def _water_neighbors(self,node):
        """Return count of Water nodes neighboring given node."""
        count = 0
        for n in self.graph[node]:
            if self.is_Water(n):
                count += 1
        return count

    def _nonLand_neighbors(self,node):
        """Return count of non-Land nodes neighboring given node."""
        count = 0
        for n in self.graph[node]:
            if not self.is_Land(n):
                count += 1
        return count

    def _water_connectedness_search(self):
        """True if Water+Empty nodes form a connected subgraph."""
        wetset = [n for n in self.graph if not self.is_Land(n)]
        wetgraph = self.graph.subgraph(wetset)
        water_component = None
        for component in nx.connected_components(wetgraph):
            if self._has_water(component):
                if water_component:
                    return False # found second water component
                else:
                    water_component = component
        return True

    def slow_but_surely_connected_water(self):
        slowway = self._water_connectedness_search()
        if self.water_connected is None:
            self.water_connected = slowway
        assert self.water_connected == slowway
        return self.water_connected

    def connected_water(self):
        self.cwtries += 1
        if self.water_connected is None:
            self.cwfails += 1
            self.water_connected = self._water_connectedness_search()
        return self.water_connected

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
                out += str(self.get_node((x,y)))+' '
            out += '\n'

        return out.rstrip('\n')

if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG)

    b = BoardRectangle(5,3)
    b.set_anchor((0,0),3)
    b.set_anchor((3,2),3)
    for n in [ (0,1), (0,2), (2,2), (4,1) ]:
        b.set_node(n,Land())
    for n in [ (2,0), (3,0), (1,1), (2,1), (3,1), (1,2) ]:
        b.set_node(n,Water())

    print 'Board'
    print b

    if b.connected_water():
        print 'Water is connected.'
    else:
        print 'Water is not connected.'

    print ' Node\tEmpty\tWater\tLand\tAnchor'
    for n in [ (0,0), (0,1), (1,0), (1,1) ]:
        print '%s\t%s\t%s\t%s\t%s' % (str(n),
                                      str(b.is_Empty(n)),
                                      str(b.is_Water(n)),
                                      str(b.is_Land(n)),
                                      str(b.is_Anchor(n)))
    print 'Pool locations:'
    for y in range(3):
        for x in range(5):
            if b.in_pool((x,y)):
                print 'P',
            else:
                print '-',
        print

    print 'Islands'
    print '   Base  : size, free, anchors, Legal?'
    for n in [(0,0),(0,1),(0,2),(1,0),(1,1),(2,2),(3,2)]:
        print ' ',n,':',b.explore_island(n),'\t',b.legal_island(n)

    print
    print 'New Board'
    b.set_node((1,2),Land())
    b.set_node((2,1),Land())
    b.set_node((1,0),Land())
    b.clear_node((2,0))
    b.clear_node((3,1))
    print b

    if b.connected_water():
        print 'Water is connected.'
    else:
        print 'Water is not connected.'

    print 'Islands'
    print '   Base  : size, free, anchors, Legal?'
    for n in [(0,0),(2,2),(2,1)]:
        print ' ',n,':',b.explore_island(n),'\t',b.legal_island(n)
