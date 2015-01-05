"""
Nurikabe solver.
2015 Bryan Clair
Pass text-based board on stdin. Example:

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

layout = sys.stdin.read()

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
