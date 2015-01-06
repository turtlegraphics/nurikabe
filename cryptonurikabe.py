#!/usr/bin/env python
"""
Cryptonurikabe solver
2015 Bryan Clair

Pass board in text file as single argument,
or with no arguements on on stdin.

Example:

python nurikabe.py crypto.txt
or
python nurikabe.py < crypto.txt

where crypto.txt might contain
...2.
.....
....x
.....
.4...

Lowercase letters represent unknown island sizes.
Letters which match will have the same size.
"""
import re
import sys
import time
import solver
import board

def solve_crypto(layout,depth):
    match = re.search('[a-z]',layout)
    if not match:
        b = board.BoardFromASCII(layout)
        solutions = solver.Solver(b).solve()
        if solutions:
            print '='*20
            print depth
        for s in solutions:
            print s
            print
        return len(solutions)
    else:
        letter = match.group(0)
        num = 0
        for v in '123456789':
            num += solve_crypto(layout.replace(letter,v),
                         depth + letter+'='+v+' ')
        return num

if len(sys.argv) == 1:
    infile = sys.stdin
elif len(sys.argv) == 2:
    infile = file(sys.argv[1])
else:
    sys.stderr.write('usage: cryptonurikabe.py [filename]\n')
    sys.exit()

layout = infile.read()

start = time.time()
numsols = solve_crypto(layout,'')
end = time.time()

print numsols,'solutions found.'
print end-start,'elapsed.'
