#!/usr/bin/python
"""
Nurikabe solver
2015 Bryan Clair

Pass board in text file as single argument,
or with no arguements on on stdin.

Board spaces can be:
*       .       Empty space
*  1-9AB...Z    Island anchor and size (A=10, etc)
*     a-z       Island size, but unknown (islands with same variable must have same size)
*      #        Water
*      +        Land
"""

import re
import sys
import logging
import time
import solver
import board
from squares import *

def parse_board(data,coding={'.':Empty,'+':Land,'#':Water}):
    """Create a rectangular square-grid board from an ASCII representation.
    Can give the coding as a dictionary keyed on char with values the type
    of node (Empty, Land, Water), but anchors must be ASCII 1-9."""
    rows = data.split()
    cols = len(rows[0])
    for r in rows:
        if len(r) != cols:
            raise ValueError('All rows must be the same width.')

    b = board.BoardRectangle(cols,len(rows))

    (x,y) = (0,0)
    for r in rows:
        for c in r:
            if c in coding:
                b.set_node((x,y),coding[c]())
            else:
                val = 0
                if c.isdigit():
                    val = ord(c) - ord('0')
                elif c.isupper():
                    val = ord(c) - ord('A') + 10
                elif c.islower():
                    val = c
                if val == 0:
                    raise ValueError('Bad character: '+c)
                b.set_anchor((x,y),val)
            x += 1
        x = 0
        y += 1

    return b

def solve(layout,vals='123456789',depth=''):
    """Solve a nurikabe puzzle by trying all possible values for variable island sizes,
    then creating a board and calling the simple nurikabe solver."""
    match = re.search('[a-z]',layout)
    if not match:
        b = parse_board(layout)
        logging.info(depth)
        solutions = solver.Solver(b).solve()
        if solutions and depth:
            print depth
        for s in solutions:
            print s
            print
        return solutions
    else:
        letter = match.group(0)
        solutions = []
        for v in vals:
            solutions.extend(solve(layout.replace(letter,v), vals, depth + letter+'='+v+' '))
        return solutions

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(epilog=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),default=sys.stdin)
    parser.add_argument('-m', '--maxvars', type=int, default=9,
                        help="Max value to try with variable islands.")
    parser.add_argument('-d', '--debug', dest='debug', action='store_true',
                    help="Turn on debug output.")
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                    help="Turn on progress info.")
    args = parser.parse_args()

    log_level = logging.WARNING # default
    if args.debug:
        log_level = logging.DEBUG
    elif args.verbose:
        log_level = logging.INFO
    logging.basicConfig(level=log_level)

    layout = args.infile.read()

    b = parse_board(layout)
    print b
    print

    start = time.time()
    solutions = solve(layout,vals='123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:args.maxvars])
    end = time.time()

    plural = 'solution'
    if len(solutions) > 1:
        plural += 's'
    print len(solutions),plural,'found.'
    print end-start,'elapsed.'
    
