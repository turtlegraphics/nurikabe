#!/usr/bin/env python
"""
Nurikabe solver.
2015 Bryan Clair

Pass board in text file as single argument,
or with no arguements on on stdin.

Example:

python nurikabe.py example.txt
or
python nurikabe.py < example.txt

where example.txt might contain
...2.
.....
....3
.....
.4...

"""
import sys
import time
import solver
import board

if len(sys.argv) == 1:
    infile = sys.stdin
elif len(sys.argv) == 2:
    infile = file(sys.argv[1])
else:
    sys.stderr.write('usage: nurikabe.py [filename]\n')
    sys.exit()

layout = infile.read()

b = board.BoardFromASCII(layout)
print 'Board:'
print b
print
print 'Solutions:'
start = time.time()
answers = solver.Solver(b).solve()
end = time.time()
if answers:
    for a in answers:
        print a
        print
else:
    print 'None\n'

print end-start,'elapsed.'
