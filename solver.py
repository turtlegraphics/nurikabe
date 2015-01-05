"""
solver module
   Implements recursive brute-force solution search.

2015 Bryan Clair
"""

import sys,logging
logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

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

    def _solve(self,n):
        """Operate on a node, using _solve recursively."""
        if n == None:
            logging.info('Found solution:\n'+str(self.board))
            self.solutions.append(str(self.board))
            return

        logging.debug('Ready for node '+str(n))
        
        if not self.board.is_Empty(n):
            # node is already set. move along.
            self._solve(self.bfs_next[n])
            return

        logging.debug('Try node'+str(n)+'as water:')
        self.board.set_node(n,Water())
        logging.debug('\n'+str(self.board))
        if self.node_ok(n):
            self._solve(self.bfs_next[n])
        else:
            logging.debug('Node'+str(n)+'cannot be water')
        self.board.clear_node(n)

        logging.debug('Try node'+str(n)+'as land:')
        self.board.set_node(n,Land())
        logging.debug('\n'+str(self.board))
        if self.node_ok(n):
            self._solve(self.bfs_next[n])
        else:
            logging.debug('Node'+str(n)+'cannot be land')
        self.board.clear_node(n)

    def solve(self):
        """Brute force recursive solver."""
        self.solutions = []
        self._solve(self.basenode)
        return self.solutions

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


