"""
solver module
   Implements recursive brute-force solution search.

2015 Bryan Clair
"""

import logging

import graphutil
from squares import *

class Solver:
    def __init__(self,board):
        self.board = board
        # set base node and successor dictionary for board traversal
        self.basenode = board.graph.nodes()[0]
        self.bfs_next = graphutil.bfs_list(board.graph,self.basenode)

    def node_ok(self,node):
        """Check if newly placed node is legal."""
        if self.board.is_Land(node):
            if not self.board.legal_island(node):
                logging.debug('land at '+str(node)+' makes bad island')
                return False
        else: # Water node
            if self.board.in_pool(node):
                logging.debug('water at '+str(node)+' makes pool')
                return False
            for n in self.board.graph[node]:
                if self.board.is_Land(n) and not self.board.legal_island(n):
                    logging.debug('water at' + str(node) +
                                  ' constricts island at '+str(n))
                    return False
        # Check for connected water
        if not self.board.connected_water():
            logging.debug('node at '+str(node)+' disconnects water')
            return False
        
        return True

    def _test_and_set_node(self,node,Type):
        """Set node to Type if legal. Return True if set."""
        assert(self.board.is_Empty(node))

        self.board.set_node(node,Type())

        if self.node_ok(node):
            logging.debug('Node '+str(node)+' set to '+Type.__name__)
            return True
        else:
            self.board.clear_node(node)
            logging.debug('Node '+str(node)+' cannot be '+Type.__name__)
            return False

    def _scan_islands(self):
        """
        Look for forced nodes next to islands:
        * If island is full, all free adjacent nodes
        * If island has only one free adjacent node, and it's hungry
        * If two islands share a free adjacent node
        """
        found = []
        fans = []
        for anchor in self.board.anchors:
            (size, freedoms, a) = self.board.explore_island(anchor)
            if size == self.board.get_node(anchor).size:
                found.extend(freedoms)
            elif len(freedoms) == 1:
                found.extend(freedoms)
            else:
                found.extend(set(freedoms).intersection(fans))
            fans.extend(freedoms)

        if found:
            logging.debug('Found nodes to work on:'+str(found))
        return found

    def _find_good_node_to_work_on(self):
        while self.goodnodes:
            node = self.goodnodes.pop()
            if self.board.is_Empty(node):
                return node

        self.goodnodes = self._scan_islands()

        while self.goodnodes:
            node = self.goodnodes.pop()
            if self.board.is_Empty(node):
                return node

        # Find an empty node in BFS order
        node = self.basenode
        while node and not self.board.is_Empty(node):
            node = self.bfs_next[node]
        return node

    def _solve(self):
        """
        Brute force recursive solver.
        """
        solutions = []
        logging.debug('\n'+str(self.board))

        node = self._find_good_node_to_work_on()

        # All nodes full? Solved
        if node == None:
            return [str(self.board)]

        logging.debug('Working node '+str(node))

        # Recurse on empty node
        for Type in [Water, Land]:
            if self._test_and_set_node(node,Type):
                solutions.extend(self._solve())
                self.board.clear_node(node)

        return solutions

    def solve(self):
        """
        Find all solutions to the board in its current state,
        return them as list.
        """
        self.goodnodes = []
        return self._solve()

if __name__=='__main__':
    import board

    def doboard(s):
        b = board.BoardFromASCII(s)
        print b
        print 'Solutions:'
        answers = Solver(b).solve()
        if answers:
            for a in answers:
                print a
                print
        else:
            print 'None\n'
        
    print 'Board with unique solution'
    doboard(
"""
...2.
.....
....3
.....
.4...
""")

    print 'Board with no solutions'
    doboard(
"""
....
3.1.
...4
....
""")
    print 'Board with six solutions'
    doboard('3...\n....\n...3')


