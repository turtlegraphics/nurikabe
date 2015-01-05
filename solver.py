import sys,logging
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

import graphutil
from squares import *

class Solver:
    def __init__(self,board):
        self.board = board
        # set base node and successor dictionary for board traversal
        self.basenode = board.graph.nodes()[0]
        self.bfs_next = graphutil.bfs_list(board.graph,self.basenode)

    def new_water_ok(self,node):
        """Check if water just placed at node is legal."""
        # Check if pool was made
        if self.board.in_pool(node):
            return False
        # Check if neighbor islands got cut off
        for n in self.board.graph[node]:
            if self.board.is_Land(n) and not self.board.legal_island(n):
                return False
        return True

    def new_land_ok(self,node):
        """Check if land just placed at node is legal."""
        if not self.board.legal_island(node):
            return False
        if not self.board.connected_water():
            return False
        return True

    def _solve(self,n):
        """Operate on a node, using _solve recursively."""
        if n == None:
            print '='*30
            print 'Solved!'
            print self.board
            print
            return

        logging.debug('Ready for node '+str(n))
        if logging.getLogger().getEffectiveLevel() <= logging.DEBUG:
            raw_input()
        
        if not self.board.is_Empty(n):
            # node is already set. move along.
            self._solve(self.bfs_next[n])
            return

        logging.debug('Try node'+str(n)+'as water:')
        self.board.set_node(n,Water())
        logging.debug('\n'+str(self.board))
        if self.new_water_ok(n):
            self._solve(self.bfs_next[n])
        else:
            logging.debug('Node'+str(n)+'cannot be water')
        self.board.clear_node(n)

        logging.debug('Try node'+str(n)+'as land:')
        self.board.set_node(n,Land())
        logging.debug('\n'+str(self.board))
        if self.new_land_ok(n):
            self._solve(self.bfs_next[n])
        else:
            logging.debug('Node'+str(n)+'cannot be land')
        self.board.clear_node(n)

    def solve(self):
        """Brute force recursive solver."""
        self._solve(self.basenode)

if __name__=='__main__':
    import board
    b = board.BoardRectangle(4,3)
    b.set_anchor((0,0),3)
    b.set_anchor((3,2),3)

    print 'Board'
    print b

    Solver(b).solve()
